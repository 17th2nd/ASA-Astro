"""Frozen-artefact verification and LeakageGuard isolation tests."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from astro_exec.core.config import RoleCapabilities, load_config
from astro_exec.core.errors import FrozenArtefactDrift, LeakageViolation
from astro_exec.core.frozen import verify_frozen_artefacts
from astro_exec.core.leakage_guard import LeakageGuard


ROOT = Path(__file__).resolve().parents[3]


class FrozenArtefactTests(unittest.TestCase):
    """Verify run-start drift detection aborts on any byte change."""

    def test_repository_frozen_artefacts_match(self) -> None:
        config = load_config(ROOT / "config/astro-exec-phase2.toml")
        verified = verify_frozen_artefacts(config, ROOT)

        self.assertEqual(len(verified), 6)
        self.assertTrue(all(item.to_record()["status"] == "verified" for item in verified))

    def test_changed_frozen_artefact_aborts(self) -> None:
        config = load_config(ROOT / "config/astro-exec-phase2.toml")
        with tempfile.TemporaryDirectory() as directory:
            fake_root = Path(directory)
            for item in config.frozen_artefacts:
                destination = fake_root / item.path
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes((ROOT / item.path).read_bytes())
            (fake_root / config.frozen_artefacts[0].path).write_text("drift", encoding="utf-8")
            with self.assertRaises(FrozenArtefactDrift):
                verify_frozen_artefacts(config, fake_root)


class LeakageGuardTests(unittest.TestCase):
    """Verify role capability isolation and symlink-escape rejection."""

    def test_asalab_cannot_read_truth_outputs(self) -> None:
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
        capabilities = RoleCapabilities("asalab", ("inputs",), ("outputs",))
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            root = Path(directory)
            (root / "inputs").mkdir()
            secret = Path(outside) / "outcome.json"
            secret.write_bytes(b"outcome")
            (root / "inputs/link").symlink_to(secret)
            with self.assertRaises(LeakageViolation):
                LeakageGuard(root, capabilities).read_bytes("inputs/link")


if __name__ == "__main__":
    unittest.main()
