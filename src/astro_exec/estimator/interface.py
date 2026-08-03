"""Digest-pinned estimator ABI without scientific selection logic."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from astro_exec.core.errors import ConfigurationError, UnresolvedRequirement

_SHA256 = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True, slots=True)
class TargetInputs:
    """Opaque digest-addressed input handed to a future frozen estimator."""

    target_id: str
    payload_digest: str

    def __post_init__(self) -> None:
        """Reject empty identity or a non-SHA-256 payload reference."""

        if not self.target_id or not _SHA256.fullmatch(self.payload_digest):
            raise ConfigurationError("invalid target input envelope")


@runtime_checkable
class FrozenEstimator(Protocol):
    """ABI required of the future digest-pinned ASA estimator.

    Implementations must deterministically return exactly four distinct
    SB441-N16 identifiers and must not access truth-laboratory outputs.
    Phase 2 defines this interface but supplies no implementation.
    """

    spec_digest: str

    def select(self, target: TargetInputs) -> tuple[int, int, int, int]:
        """Return four distinct identifiers for an admissible target."""

        ...


class UnresolvedEstimator:
    """Fail-closed placeholder proving Phase 2 does not invent ``UR-001``."""

    spec_digest = ""

    def select(self, target: TargetInputs) -> tuple[int, int, int, int]:
        """Always raise ``UnresolvedRequirement('UR-001')``."""

        del target
        raise UnresolvedRequirement("UR-001")
