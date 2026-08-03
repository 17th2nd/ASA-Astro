"""Deterministic lifecycle transition tests."""

from __future__ import annotations

import unittest

from astro_exec.core.errors import RunStateError
from astro_exec.core.lifecycle import RunLifecycle, RunState


class LifecycleTests(unittest.TestCase):
    """Verify the only successful Phase 2 path and terminal failure behavior."""

    def test_dry_run_path_is_explicit_and_terminal(self) -> None:
        """G1 lifecycle: proposed through sealed is explicit and terminal."""

        lifecycle = RunLifecycle("RUN-" + "0" * 64)
        for state in (RunState.VALIDATING, RunState.READY, RunState.EXECUTING, RunState.COMPLETED, RunState.SEALED):
            lifecycle.transition(state)
        self.assertEqual([item.sequence for item in lifecycle.history], list(range(5)))
        self.assertTrue(all(item.provenance_id.startswith("PV-") for item in lifecycle.history))
        self.assertEqual(lifecycle.to_record()["state"], "sealed")
        with self.assertRaises(RunStateError):
            lifecycle.transition(RunState.PROPOSED)

    def test_illegal_transition_does_not_change_state(self) -> None:
        """G1 lifecycle: illegal transitions fail without history or state mutation."""

        lifecycle = RunLifecycle("RUN-" + "0" * 64)
        with self.assertRaises(RunStateError):
            lifecycle.transition(RunState.COMPLETED)
        self.assertEqual(lifecycle.state, RunState.PROPOSED)
        self.assertEqual(lifecycle.history, ())

    def test_failed_runs_may_only_be_sealed(self) -> None:
        """G1 lifecycle: failed is recorded and only sealing remains legal."""

        lifecycle = RunLifecycle("RUN-" + "0" * 64)
        lifecycle.fail()
        with self.assertRaises(RunStateError):
            lifecycle.transition(RunState.EXECUTING)
        lifecycle.seal()
        self.assertEqual(lifecycle.state, RunState.SEALED)


if __name__ == "__main__":
    unittest.main()
