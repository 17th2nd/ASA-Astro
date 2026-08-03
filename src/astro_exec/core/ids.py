"""Content-derived identifiers that never depend on time or host state."""

from __future__ import annotations

import re
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
