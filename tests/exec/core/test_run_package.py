"""Dry-run package, replay, and deterministic comparison tests."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from astro_exec.core.config import load_config
from astro_exec.core.determinism import compare_dry_runs
from astro_exec.core.errors import ConfigurationError, FrozenArtefactDrift, ReplayMismatch
from astro_exec.core.replay import verify_run_package
from astro_exec.core.run_package import create_dry_run


ROOT = Path(__file__).resolve().parents[3]


class DryRunPackageTests(unittest.TestCase):
    """Verify G1 empty-package completeness and replay determinism."""

    def test_two_dry_runs_are_identical_except_run_id(self) -> None:
        config = load_config(ROOT / "config/astro-exec-phase2.toml")
        with tempfile.TemporaryDirectory() as directory:
            left = Path(directory) / "left"
            right = Path(directory) / "right"
            left_id = create_dry_run(left, config=config, repository_root=ROOT, run_label="left")
            right_id = create_dry_run(right, config=config, repository_root=ROOT, run_label="right")

            self.assertNotEqual(left_id, right_id)
            self.assertTrue(compare_dry_runs(left, right).equivalent_except_run_id)
            self.assertEqual(verify_run_package(left).status, "verified")
            run = json.loads((left / "run.json").read_text(encoding="utf-8"))
            provenance = json.loads((left / "provenance/graph.json").read_text(encoding="utf-8"))
            self.assertFalse(run["scientific_computation"])
            self.assertEqual(run["evidence_level"], "EH-0")
            self.assertNotIn("authoritative-scientific", {item["classification"] for item in run["artefacts"]})
            self.assertEqual(len(provenance["nodes"]), 8)

    def test_existing_output_and_tampering_fail_closed(self) -> None:
        config = load_config(ROOT / "config/astro-exec-phase2.toml")
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "run"
            create_dry_run(output, config=config, repository_root=ROOT, run_label="one")
            with self.assertRaises(ConfigurationError):
                create_dry_run(output, config=config, repository_root=ROOT, run_label="two")
            (output / "manifest.json").write_text("{}", encoding="utf-8")
            with self.assertRaises(ReplayMismatch):
                verify_run_package(output)

    def test_frozen_artefact_drift_aborts_before_output_creation(self) -> None:
        config = load_config(ROOT / "config/astro-exec-phase2.toml")
        with tempfile.TemporaryDirectory() as directory:
            fake_root = Path(directory) / "repository"
            output = Path(directory) / "run"
            for item in config.frozen_artefacts:
                destination = fake_root / item.path
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes((ROOT / item.path).read_bytes())
            (fake_root / config.frozen_artefacts[0].path).write_text("drift", encoding="utf-8")

            with self.assertRaises(FrozenArtefactDrift):
                create_dry_run(output, config=config, repository_root=fake_root, run_label="drift")
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
