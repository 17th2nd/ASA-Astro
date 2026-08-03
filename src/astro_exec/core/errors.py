"""Structured exception taxonomy for deterministic execution failures."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Any


class AstroExecError(Exception):
    """Base exception carrying a stable machine-readable code and details."""

    code = "ASTRO_EXEC_ERROR"

    def __init__(self, message: str, *, details: Mapping[str, Any] | None = None) -> None:
        """Create an error without retaining a caller-mutable details mapping."""

        super().__init__(message)
        self.message = message
        self.details = MappingProxyType(dict(details or {}))

    def to_record(self) -> dict[str, Any]:
        """Return the deterministic JSON-compatible representation."""

        return {"code": self.code, "details": dict(self.details), "message": self.message}


class CanonicalJSONError(AstroExecError):
    """Raised when a value cannot be represented by the canonical JSON contract."""

    code = "CANONICAL_JSON_ERROR"


class ConfigurationError(AstroExecError):
    """Raised when execution configuration is malformed or unsafe."""

    code = "CONFIGURATION_ERROR"


class FrozenArtefactDrift(AstroExecError):
    """Raised when a frozen authoritative artefact differs from its pinned digest."""

    code = "FROZEN_ARTEFACT_DRIFT"


class LeakageViolation(AstroExecError):
    """Raised when a role attempts access outside its declared capability set."""

    code = "LEAKAGE_VIOLATION"


class RunStateError(AstroExecError):
    """Raised for an invalid deterministic run-lifecycle transition."""

    code = "RUN_STATE_ERROR"


class ReplayMismatch(AstroExecError):
    """Raised when a run package fails deterministic replay verification."""

    code = "REPLAY_MISMATCH"


class UnresolvedRequirement(AstroExecError):
    """Fail closed when execution reaches a requirement awaiting human ruling."""

    code = "UNRESOLVED_REQUIREMENT"

    def __init__(self, requirement_id: str) -> None:
        """Identify the unresolved requirement without selecting a default."""

        super().__init__(
            f"execution blocked by unresolved requirement {requirement_id}",
            details={"requirement_id": requirement_id},
        )
        self.requirement_id = requirement_id
