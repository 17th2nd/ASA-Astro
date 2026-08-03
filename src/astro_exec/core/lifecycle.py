"""Deterministic run lifecycle with provenance-bearing closed transitions."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .errors import RunStateError
from .ids import ProvenanceRecordIdentity, validate_identifier


class RunState(StrEnum):
    """Required Phase 2 run states in their canonical serialized form."""

    PROPOSED = "proposed"
    VALIDATING = "validating"
    READY = "ready"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    SEALED = "sealed"


_TRANSITIONS = {
    RunState.PROPOSED: {RunState.VALIDATING, RunState.FAILED},
    RunState.VALIDATING: {RunState.READY, RunState.FAILED},
    RunState.READY: {RunState.EXECUTING, RunState.FAILED},
    RunState.EXECUTING: {RunState.COMPLETED, RunState.FAILED},
    RunState.COMPLETED: {RunState.SEALED},
    RunState.FAILED: {RunState.SEALED},
    RunState.SEALED: set(),
}


@dataclass(frozen=True, slots=True)
class LifecycleTransition:
    """Immutable content-addressed provenance for one state transition."""

    provenance_id: str
    run_id: str
    sequence: int
    source: RunState
    target: RunState

    @classmethod
    def create(
        cls,
        run_id: str,
        sequence: int,
        source: RunState,
        target: RunState,
    ) -> "LifecycleTransition":
        """Derive transition provenance without wall-clock or process metadata."""

        payload = {
            "run_id": run_id,
            "sequence": sequence,
            "source": source.value,
            "target": target.value,
        }
        return cls(str(ProvenanceRecordIdentity.derive(payload)), run_id, sequence, source, target)

    def to_record(self) -> dict[str, Any]:
        """Return the canonical lifecycle-transition record."""

        return {
            "provenance_id": self.provenance_id,
            "run_id": self.run_id,
            "sequence": self.sequence,
            "source": self.source.value,
            "target": self.target.value,
        }


@dataclass(slots=True)
class RunLifecycle:
    """Per-run state cursor governed without mutable module-global run state."""

    run_id: str
    state: RunState = field(default=RunState.PROPOSED, init=False)
    _history: list[LifecycleTransition] = field(default_factory=list, repr=False)

    def __post_init__(self) -> None:
        """Require a valid authoritative run identity."""

        validate_identifier(self.run_id, prefix="RUN")

    @property
    def history(self) -> tuple[LifecycleTransition, ...]:
        """Return transition provenance as an immutable tuple."""

        return tuple(self._history)

    def transition(self, target: RunState) -> LifecycleTransition:
        """Advance legally and record provenance, or fail without mutation."""

        if target not in _TRANSITIONS[self.state]:
            raise RunStateError(
                "illegal run lifecycle transition",
                details={"run_id": self.run_id, "source": self.state.value, "target": target.value},
            )
        transition = LifecycleTransition.create(self.run_id, len(self._history), self.state, target)
        self.state = target
        self._history.append(transition)
        return transition

    def fail(self) -> LifecycleTransition:
        """Enter ``failed`` from a non-terminal active state."""

        return self.transition(RunState.FAILED)

    def seal(self) -> LifecycleTransition:
        """Seal a completed or failed run record."""

        return self.transition(RunState.SEALED)

    def to_record(self) -> dict[str, Any]:
        """Return the current state and complete transition provenance."""

        return {
            "run_id": self.run_id,
            "schema_version": "astro-exec-lifecycle-v1",
            "state": self.state.value,
            "transitions": [item.to_record() for item in self._history],
        }
