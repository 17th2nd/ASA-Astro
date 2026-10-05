"""R1: primary Objective via observation_bundle_to_objective for uploads."""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

from app import pin as pinmod

try:
    PIN = pinmod.verify_pin()
    PIN_ERROR = None
except Exception as exc:  # pragma: no cover
    PIN, PIN_ERROR = None, str(exc)

NEEDS_PIN = unittest.skipIf(
    PIN is None,
    f"pinned ASA checkout not verified ({PIN_ERROR}); run "
    "python3 tools/asa_baseline.py --config config/asa-baseline-current-dev.json",
)


class _TempDataDir(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self._old = os.environ.get("ASA_ASTRO_APP_DATA_DIR")
        os.environ["ASA_ASTRO_APP_DATA_DIR"] = self._tmp.name

    def tearDown(self):
        if self._old is None:
            os.environ.pop("ASA_ASTRO_APP_DATA_DIR", None)
        else:
            os.environ["ASA_ASTRO_APP_DATA_DIR"] = self._old
        self._tmp.cleanup()


def _fixture_ppm(path: Path) -> Path:
    from tests.fixtures.generate_fixture import create_fixture

    return create_fixture(path)


def _wcs_meta(**extra):
    meta = {
        "instrument": "synthetic-test",
        "wcs": {
            "frame": "ICRS",
            "epoch": "J2000.0",
            "crpix": [32.0, 32.0],
            "crval_deg": [150.0, -30.0],
            "cd_deg_per_pixel": [[1.0 / 3600.0, 0.0], [0.0, 1.0 / 3600.0]],
            "pixel_origin": "0-based-image-pixel",
            "source_reference": "app-r1-test",
        },
        "site": {
            "designation": "TEST-SITE-R1",
            "latitude_deg": -31.2733,
            "longitude_deg": 149.0644,
            "elevation_m": 1165.0,
        },
    }
    meta.update(extra)
    return meta


@NEEDS_PIN
class PrimaryBridgeUpload(_TempDataDir):
    def test_upload_localised_uses_observation_bundle_to_objective(self):
        from app import slice as s

        img = _fixture_ppm(Path(self._tmp.name) / "r1-wcs.ppm")
        view = s.run_slice(
            upload_bytes=img.read_bytes(),
            upload_filename="r1-wcs.ppm",
            metadata_bytes=(json.dumps(_wcs_meta()) + "\n").encode("utf-8"),
        )
        prov = view["universe_provenance"]
        self.assertEqual(prov["bridge_path"], "observation_bundle_to_objective")
        self.assertFalse(prov.get("slice1_substituted"))
        self.assertEqual(prov.get("label"), "observation+bridge")
        self.assertNotEqual(prov.get("source_path"), "data/universe/slice1.json")
        self.assertTrue(view["observation_evidence"]["present"])
        self.assertTrue(any(l["status"] == "localised" for l in view["observation_evidence"]["localisations"]))
        us = view["uploaded_source"]
        self.assertTrue(us["present"])
        self.assertIn("observation_bundle_to_objective", us.get("objective_bridge") or "")
        self.assertIn("primary", us.get("objective_bridge") or "")
        # Must not be the demo slice1 universe path in inputs
        run = json.loads(
            (Path(os.environ["ASA_ASTRO_APP_DATA_DIR"]) / "runs" / view["run_id"] / "run.json").read_text()
        )
        self.assertNotIn("data/universe/slice1.json", run["inputs"].get("universe", ""))
        self.assertIn("observation_bundle_to_objective", run["slice"])
        self.assertTrue(prov.get("universe_id"))
        self.assertTrue(prov.get("data_class"))
        # observation claim ids when present
        if prov.get("observation_claim_id") or prov.get("observation_claim_digest"):
            self.assertTrue(prov.get("source_sha256"))

    def test_upload_no_wcs_fail_closed_no_silent_slice1(self):
        from app import slice as s

        img = _fixture_ppm(Path(self._tmp.name) / "r1-nowcs.ppm")
        with self.assertRaisesRegex(ValueError, r"fail-closed|refusing silent slice1"):
            s.run_slice(
                upload_bytes=img.read_bytes(),
                upload_filename="r1-nowcs.ppm",
            )

    def test_no_upload_demo_uses_slice1_labelled(self):
        from app import slice as s

        view = s.run_slice()
        prov = view["universe_provenance"]
        self.assertEqual(prov["bridge_path"], "synthetic_demo_slice1")
        self.assertEqual(prov.get("label"), "synthetic/demo")
        self.assertTrue(prov.get("demo"))
        self.assertEqual(prov.get("source_path"), "data/universe/slice1.json")
        self.assertFalse(view["observation_evidence"]["present"])
        self.assertTrue(view["receipt"]["receipt_id_verified"])


if __name__ == "__main__":
    unittest.main()
