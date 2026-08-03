"""Non-scientific execution contract shared by the four protocol roles."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class Role(StrEnum):
    """Roles separated by ``ASTRO-EXP-0001`` §Blind protocol."""

    ASALAB = "asalab"
    CUSTODIAN = "custodian"
    STATISTICIAN = "statistician"
    TRUTHLAB = "truthlab"


@dataclass(frozen=True, slots=True)
class RoleResult:
    """Infrastructure-only result returned by a Phase 2 role entry point."""

    role: Role
    status: str
    dry_run: bool
    scientific_computation: bool = False


@dataclass(frozen=True, slots=True)
class DryRunRole:
    """Executable role skeleton that performs no scientific work."""

    role: Role

    def execute(self) -> RoleResult:
        """Return a deterministic empty result for interface verification."""

        return RoleResult(self.role, "interface-ready", True)
