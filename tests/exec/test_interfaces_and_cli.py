"""Estimator, role, and CLI skeleton contract tests."""

from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from astro_exec.cli import main
from astro_exec.core.errors import UnresolvedRequirement
from astro_exec.estimator import TargetInputs, UnresolvedEstimator
from astro_exec.roles import DryRunRole, Role


ROOT = Path(__file__).resolve().parents[2]


class InterfaceTests(unittest.TestCase):
    """Verify interfaces remain non-scientific and unresolved paths fail closed."""

    def test_estimator_placeholder_names_ur_001(self) -> None:
        target = TargetInputs("target-fixture", "0" * 64)
        with self.assertRaises(UnresolvedRequirement) as raised:
            UnresolvedEstimator().select(target)
        self.assertEqual(raised.exception.requirement_id, "UR-001")

    def test_all_role_entry_points_are_dry_run_only(self) -> None:
        results = [DryRunRole(role).execute() for role in Role]
        self.assertTrue(all(result.dry_run and not result.scientific_computation for result in results))


class CLITests(unittest.TestCase):
    """Verify run and replay commands through the public entry point."""

    def test_cli_creates_and_replays_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "run"
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                status = main(
                    [
                        "run",
                        "--dry-run",
                        "--config",
                        str(ROOT / "config/astro-exec-phase2.toml"),
                        "--repository-root",
                        str(ROOT),
                        "--run-label",
                        "cli-test",
                        "--output",
                        str(output),
                    ]
                )
            self.assertEqual(status, 0)
            self.assertIn("DRY_RUN_COMPLETE", stdout.getvalue())
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main(["replay", str(output)]), 0)


if __name__ == "__main__":
    unittest.main()
