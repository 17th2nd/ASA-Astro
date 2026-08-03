"""Deterministic run lifecycle with explicit, closed transitions."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .errors import RunStateError


class RunState(StrEnum):
    """States implemented by the Phase 2 dry-run lifecycle."""

    CREATED = "CREATED"
    VERIFYING = "VERIFYING"
    VERIFIED = "VERIFIED"
    MATERIALIZING = "MATERIALIZING"
    DRY_RUN_COMPLETE = "DRY_RUN_COMPLETE"
    ABORTED = "ABORTED"


_TRANSITIONS = {
    RunState.CREATED: {RunState.VERIFYING, RunState.ABORTED},
    RunState.VERIFYING: {RunState.VERIFIED, RunState.ABORTED},
    RunState.VERIFIED: {RunState.MATERIALIZING, RunState.ABORTED},
    RunState.MATERIALIZING: {RunState.DRY_RUN_COMPLETE, RunState.ABORTED},
    RunState.DRY_RUN_COMPLETE: set(),
    RunState.ABORTED: set(),
}


@dataclass(slots=True)
class RunLifecycle:
    """Mutable state cursor governed by the immutable Phase 2 transition table."""

    run_id: str
    state: RunState = RunState.CREATED

    def transition(self, target: RunState) -> RunState:
        """Advance to ``target`` or fail without changing current state."""

        if target not in _TRANSITIONS[self.state]:
            raise RunStateError(
                "illegal run lifecycle transition",
                details={"run_id": self.run_id, "source": self.state.value, "target": target.value},
            )
        self.state = target
        return self.state

    def abort(self) -> RunState:
        """Enter the terminal aborted state from any non-terminal state."""

        return self.transition(RunState.ABORTED)
