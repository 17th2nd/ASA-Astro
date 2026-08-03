"""Content-derived identifiers that never depend on time or host state."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import ClassVar
from typing import Any

from .errors import ConfigurationError
from .hashing import fingerprint

_PREFIX = re.compile(r"^[A-Z][A-Z0-9_]{1,15}$")
_IDENTIFIER = re.compile(r"^(?P<prefix>[A-Z][A-Z0-9_]{1,15})-(?P<digest>[0-9a-f]{64})$")


def stable_identifier(prefix: str, payload: Any) -> str:
    """Return ``PREFIX-<sha256>`` for a canonical JSON payload."""

    if not _PREFIX.fullmatch(prefix):
        raise ConfigurationError("invalid identifier prefix", details={"prefix": prefix})
    return f"{prefix}-{fingerprint(payload)}"


def validate_identifier(identifier: str, *, prefix: str | None = None) -> str:
    """Validate and return a full content-derived identifier.

    When ``prefix`` is supplied, the identifier must carry that exact prefix.
    """

    match = _IDENTIFIER.fullmatch(identifier)
    if match is None or (prefix is not None and match.group("prefix") != prefix):
        raise ConfigurationError(
            "invalid content-derived identifier",
            details={"identifier": identifier, "required_prefix": prefix},
        )
    return identifier


@dataclass(frozen=True, slots=True)
class DeterministicIdentity:
    """Base value object for a domain-specific content-derived identity."""

    value: str
    prefix: ClassVar[str] = "ID"

    def __post_init__(self) -> None:
        """Validate that the serialized identity carries its domain prefix."""

        validate_identifier(self.value, prefix=self.prefix)

    @classmethod
    def derive(cls, authoritative_inputs: Any) -> "DeterministicIdentity":
        """Derive this identity type solely from declared canonical inputs."""

        return cls(stable_identifier(cls.prefix, authoritative_inputs))

    def __str__(self) -> str:
        """Return the stable serialized identity."""

        return self.value


class ArtefactIdentity(DeterministicIdentity):
    """Identity of an input or derived artefact."""

    prefix = "ART"


class ConfigurationIdentity(DeterministicIdentity):
    """Identity of an immutable validated configuration."""

    prefix = "CFG"


class RunIdentity(DeterministicIdentity):
    """Authoritative run identity derived without invocation metadata."""

    prefix = "RUN"


class InvocationIdentity(DeterministicIdentity):
    """Operational identity explicitly classified as non-authoritative."""

    prefix = "INV"

    def to_record(self) -> dict[str, str]:
        """Return the mandatory non-authoritative classification."""

        return {"classification": "diagnostic-non-authoritative", "invocation_id": self.value}


class ProvenanceRecordIdentity(DeterministicIdentity):
    """Identity of a content-addressed provenance assertion."""

    prefix = "PV"


class TransformationIdentity(DeterministicIdentity):
    """Identity of a declared infrastructure transformation contract."""

    prefix = "XFORM"
