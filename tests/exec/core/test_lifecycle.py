"""Deterministic lifecycle transition tests."""

from __future__ import annotations

import unittest

from astro_exec.core.errors import RunStateError
from astro_exec.core.lifecycle import RunLifecycle, RunState


class LifecycleTests(unittest.TestCase):
    """Verify the only successful Phase 2 path and terminal failure behavior."""

    def test_dry_run_path_is_explicit_and_terminal(self) -> None:
        lifecycle = RunLifecycle("RUN-" + "0" * 64)
        for state in (RunState.VERIFYING, RunState.VERIFIED, RunState.MATERIALIZING, RunState.DRY_RUN_COMPLETE):
            lifecycle.transition(state)
        with self.assertRaises(RunStateError):
            lifecycle.transition(RunState.CREATED)

    def test_illegal_transition_does_not_change_state(self) -> None:
        lifecycle = RunLifecycle("RUN-" + "0" * 64)
        with self.assertRaises(RunStateError):
            lifecycle.transition(RunState.DRY_RUN_COMPLETE)
        self.assertEqual(lifecycle.state, RunState.CREATED)


if __name__ == "__main__":
    unittest.main()
