"""Dry-run package, replay, and deterministic comparison tests."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from astro_exec.core.config import load_config
from astro_exec.core.determinism import compare_dry_runs
from astro_exec.core.errors import ConfigurationError, FrozenArtefactDrift, ReplayMismatch
from astro_exec.core.frozen import load_frozen_manifest
from astro_exec.core.replay import verify_run_package
from astro_exec.core.run_package import create_dry_run


ROOT = Path(__file__).resolve().parents[3]


class DryRunPackageTests(unittest.TestCase):
    """Verify G1 empty-package completeness and replay determinism."""

    def test_two_dry_runs_have_byte_identical_authoritative_content(self) -> None:
        """G1 determinism: invocation variation cannot alter authoritative bytes."""
        config = load_config(ROOT / "config/astro-exec-phase2.toml")
        with tempfile.TemporaryDirectory() as directory:
            left = Path(directory) / "left"
            right = Path(directory) / "right"
            left_id = create_dry_run(left, config=config, repository_root=ROOT, run_label="left")
            right_id = create_dry_run(right, config=config, repository_root=ROOT, run_label="right")

            self.assertEqual(left_id, right_id)
            comparison = compare_dry_runs(left, right)
            self.assertTrue(comparison.authoritative_equivalent)
            self.assertEqual(comparison.differing_files, ())
            replay = verify_run_package(left)
            self.assertEqual(replay.status, "verified")
            self.assertEqual(len(replay.authoritative_digest), 64)
            run = json.loads((left / "run.json").read_text(encoding="utf-8"))
            provenance = json.loads((left / "provenance/graph.json").read_text(encoding="utf-8"))
            lifecycle = json.loads((left / "lifecycle.json").read_text(encoding="utf-8"))
            left_invocation = json.loads((left.parent / "left.invocation.json").read_text(encoding="utf-8"))
            right_invocation = json.loads((right.parent / "right.invocation.json").read_text(encoding="utf-8"))
            self.assertFalse(run["scientific_computation"])
            self.assertEqual(run["evidence_level"], "EH-0")
            self.assertNotIn("authoritative-scientific", {item["classification"] for item in run["artefacts"]})
            self.assertEqual(len(provenance["nodes"]), 9)
            self.assertEqual(lifecycle["state"], "sealed")
            self.assertEqual(run["software_commit"], run["run_identity_inputs"]["software_commit"])
            self.assertEqual(len(run["software_commit"]), 40)
            self.assertNotEqual(left_invocation["invocation_id"], right_invocation["invocation_id"])
            self.assertEqual(left_invocation["classification"], "diagnostic-non-authoritative")
            self.assertFalse(any("invocation" in path.name for path in left.rglob("*")))

            inventory = {}
            for line in (left / "AUTHORITATIVE-CONTENT.sha256").read_text(encoding="ascii").splitlines():
                digest, relative = line.split("  ", 1)
                inventory[relative] = digest
            self.assertNotIn("logs/events.jsonl", inventory)
            self.assertNotIn("CHECKSUMS.sha256", inventory)
            self.assertIn("run.json", inventory)
            for relative in inventory:
                self.assertEqual((left / relative).read_bytes(), (right / relative).read_bytes())

    def test_existing_output_and_tampering_fail_closed(self) -> None:
        """G1 replay: overwrite and checksum tampering are rejected."""
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
        """R-061/G1 run creation: drift prevents any package directory creation."""
        config = load_config(ROOT / "config/astro-exec-phase2.toml")
        with tempfile.TemporaryDirectory() as directory:
            fake_root = Path(directory) / "repository"
            output = Path(directory) / "run"
            source_manifest = ROOT / config.frozen_manifest
            destination_manifest = fake_root / config.frozen_manifest
            destination_manifest.parent.mkdir(parents=True, exist_ok=True)
            destination_manifest.write_bytes(source_manifest.read_bytes())
            for item in load_frozen_manifest(source_manifest).artefacts:
                destination = fake_root / item.path
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes((ROOT / item.path).read_bytes())
            first = load_frozen_manifest(source_manifest).artefacts[0]
            (fake_root / first.path).write_text("drift", encoding="utf-8")

            with self.assertRaises(FrozenArtefactDrift):
                create_dry_run(output, config=config, repository_root=fake_root, run_label="drift")
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
