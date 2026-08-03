"""Frozen-artefact verification and LeakageGuard isolation tests."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from astro_exec.core.config import RoleCapabilities, load_config
from astro_exec.core.errors import FrozenArtefactDrift, LeakageViolation
from astro_exec.core.frozen import load_frozen_manifest, verify_frozen_artefacts
from astro_exec.core.leakage_guard import LeakageGuard


ROOT = Path(__file__).resolve().parents[3]


def _copy_declared_artefacts(destination: Path) -> None:
    manifest_path = ROOT / "config/frozen-artefacts-v1.json"
    copied_manifest = destination / "config/frozen-artefacts-v1.json"
    copied_manifest.parent.mkdir(parents=True, exist_ok=True)
    copied_manifest.write_bytes(manifest_path.read_bytes())
    for item in load_frozen_manifest(manifest_path).artefacts:
        target = destination / item.path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((ROOT / item.path).read_bytes())


class FrozenArtefactTests(unittest.TestCase):
    """Verify run-start drift detection aborts on any byte change."""

    def test_repository_frozen_artefacts_match(self) -> None:
        """R-061/G1 drift guard: every declared repository artefact verifies."""
        config = load_config(ROOT / "config/astro-exec-phase2.toml")
        verified = verify_frozen_artefacts(config, ROOT)

        self.assertEqual(len(verified), 6)
        self.assertTrue(all(item.to_record()["verification_status"] == "verified" for item in verified))

    def test_changed_frozen_artefact_aborts(self) -> None:
        """R-061/G1 drift guard: changed bytes abort with exact drift type."""
        config = load_config(ROOT / "config/astro-exec-phase2.toml")
        with tempfile.TemporaryDirectory() as directory:
            fake_root = Path(directory)
            _copy_declared_artefacts(fake_root)
            changed = load_frozen_manifest(fake_root / config.frozen_manifest).artefacts[0].path
            (fake_root / changed).write_text("drift", encoding="utf-8")
            with self.assertRaises(FrozenArtefactDrift) as raised:
                verify_frozen_artefacts(config, fake_root)
            self.assertEqual(raised.exception.details["drift_type"], "changed")

    def test_missing_and_substituted_artefacts_abort(self) -> None:
        """R-061/G1 drift guard: missing files and symlink substitutions fail closed."""

        config = load_config(ROOT / "config/astro-exec-phase2.toml")
        with tempfile.TemporaryDirectory() as directory:
            fake_root = Path(directory)
            _copy_declared_artefacts(fake_root)
            first = load_frozen_manifest(fake_root / config.frozen_manifest).artefacts[0].path
            (fake_root / first).unlink()
            with self.assertRaises(FrozenArtefactDrift) as missing:
                verify_frozen_artefacts(config, fake_root)
            self.assertEqual(missing.exception.details["drift_type"], "missing")

            source = ROOT / first
            (fake_root / first).symlink_to(source)
            with self.assertRaises(FrozenArtefactDrift) as substituted:
                verify_frozen_artefacts(config, fake_root)
            self.assertEqual(substituted.exception.details["drift_type"], "substituted")

    def test_extra_authoritative_artefact_aborts(self) -> None:
        """R-061/G1 drift guard: prohibited extras in a closed set are reported."""

        config = load_config(ROOT / "config/astro-exec-phase2.toml")
        with tempfile.TemporaryDirectory() as directory:
            fake_root = Path(directory)
            _copy_declared_artefacts(fake_root)
            (fake_root / "docs/claims/UNDECLARED.md").write_text("extra", encoding="utf-8")
            with self.assertRaises(FrozenArtefactDrift) as raised:
                verify_frozen_artefacts(config, fake_root)
            self.assertEqual(raised.exception.details["drift_type"], "extra")
            self.assertEqual(raised.exception.details["paths"], ["docs/claims/UNDECLARED.md"])

    def test_theory_part_a_and_part_b_statuses_are_distinct(self) -> None:
        """G1 freeze boundary: Part A is frozen while Part B remains Candidate."""

        manifest = load_frozen_manifest(ROOT / "config/frozen-artefacts-v1.json")
        theory = next(item for item in manifest.artefacts if item.path == "docs/theory/ASTRO-THEORY-0001.md")
        self.assertEqual(theory.document_status, "mixed")
        self.assertEqual(
            {section.name: section.status for section in theory.sections},
            {
                "Part A — Version 1 Deterministic Core": "frozen",
                "Part B — Candidate Enrichments": "candidate-not-frozen",
            },
        )


class LeakageGuardTests(unittest.TestCase):
    """Verify role capability isolation and symlink-escape rejection."""

    def test_asalab_cannot_read_truth_outputs(self) -> None:
        """R-029/G1 LeakageGuard: allowed reads pass and cross-role reads fail."""
        capabilities = RoleCapabilities("asalab", ("inputs/estimator",), ("selections/asa",))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            allowed = root / "inputs/estimator/target.json"
            truth = root / "truth/outcome.json"
            allowed.parent.mkdir(parents=True)
            truth.parent.mkdir(parents=True)
            allowed.write_bytes(b"input")
            truth.write_bytes(b"outcome")
            guard = LeakageGuard(root, capabilities)

            self.assertEqual(guard.read_bytes("inputs/estimator/target.json"), b"input")
            with self.assertRaises(LeakageViolation):
                guard.read_bytes("truth/outcome.json")

    def test_symlink_escape_is_rejected(self) -> None:
        """R-029/G1 LeakageGuard: symlink escape cannot bypass a capability."""
        capabilities = RoleCapabilities("asalab", ("inputs",), ("outputs",))
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            root = Path(directory)
            (root / "inputs").mkdir()
            secret = Path(outside) / "outcome.json"
            secret.write_bytes(b"outcome")
            (root / "inputs/link").symlink_to(secret)
            with self.assertRaises(LeakageViolation):
                LeakageGuard(root, capabilities).read_bytes("inputs/link")

    def test_parent_traversal_is_rejected(self) -> None:
        """R-029/G1 LeakageGuard: path traversal outside a role root is denied."""

        capabilities = RoleCapabilities("asalab", ("inputs/estimator",), ("outputs",))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "truth").mkdir()
            (root / "truth/outcome.json").write_bytes(b"outcome")
            with self.assertRaises(LeakageViolation):
                LeakageGuard(root, capabilities).read_bytes("inputs/estimator/../../truth/outcome.json")


if __name__ == "__main__":
    unittest.main()
