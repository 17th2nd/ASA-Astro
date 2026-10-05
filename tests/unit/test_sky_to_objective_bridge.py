"""Sky→candidates→Objective bridge: hypothesis labels + receipt; fail closed without WCS localisation."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from asa_astro.bridge import (
    SkyToObjectiveBridgeError,
    bridge_sky_localisations_to_objective,
    default_sky_candidate_objective,
)
from asa_astro.bridge.sky_to_objective import bridge_observation_bundle_to_objective, build_temporary_universe
from asa_astro.evidence.crossmatch import crossmatch_localisation
from asa_astro.evidence.wcs import localise_detection


def _wcs():
    return {
        "frame": "ICRS",
        "epoch": "J2000.0",
        "crpix": [50.0, 50.0],
        "crval_deg": [120.0, -45.0],
        "cd_deg_per_pixel": [[1.0 / 3600.0, 0.0], [0.0, 1.0 / 3600.0]],
        "pixel_origin": "0-based-image-pixel",
    }


def _loc(det_id: str = "detection-aaaaaaaaaaaaaaaaaaaa", x: float = 50.0, y: float = 50.0):
    return localise_detection(
        {"id": det_id, "centroid": {"x": x, "y": y, "unit": "pixel"}},
        _wcs(),
        candidate_id="candidate-cccccccccccccccccccc",
    )


class SkyToObjectiveBridgeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="asa-sky-bridge-", dir="/tmp")
        self.root = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_fail_closed_when_no_localised(self) -> None:
        unavailable = localise_detection(
            {"id": "detection-aaaaaaaaaaaaaaaaaaaa", "centroid": {"x": 1.0, "y": 1.0, "unit": "pixel"}},
            None,
        )
        with self.assertRaisesRegex(SkyToObjectiveBridgeError, "Fail closed"):
            bridge_sky_localisations_to_objective([unavailable], self.root / "out-fail")
        self.assertFalse((self.root / "out-fail").exists())

    def test_bridge_writes_receipt_with_hypothesis_flags(self) -> None:
        loc = _loc()
        catalogue = [
            {
                "catalogue_id": "SYN-BRIDGE-1",
                "catalogue_name": "synthetic-fixture-catalogue",
                "ra_deg": 120.0,
                "dec_deg": -45.0,
                "evidence_ids": ["evidence-catalogue-bridge-1"],
                "labels": ["star"],
            }
        ]
        xm = crossmatch_localisation(
            loc,
            catalogue,
            match_radius_arcsec=5.0,
            catalogue_provenance={
                "catalogue_name": "synthetic-fixture-catalogue",
                "release": "test-0",
                "query_description": "in-memory bridge test",
            },
        )
        self.assertEqual(xm["resolution_state"], "matched")
        out = self.root / "out-ok"
        result = bridge_sky_localisations_to_objective([loc], out, crossmatches=[xm])

        self.assertFalse(result["established_identity_promoted"])
        self.assertFalse(result["coordinates_invented"])
        self.assertEqual(result["hypothesis_entity_count"], 1)
        self.assertTrue((out / "receipt.json").is_file())
        self.assertTrue((out / "receipt.sha256").is_file())
        self.assertTrue((out / "bridge_manifest.json").is_file())

        manifest = json.loads((out / "bridge_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["epistemic"]["sky_candidates_are"], "hypothesis")
        self.assertFalse(manifest["epistemic"]["established_identity_promoted"])
        self.assertFalse(manifest["epistemic"]["catalogue_match_promotes_identity"])
        self.assertEqual(manifest["hypothesis_entities"][0]["classification_status"], "hypothesis")
        self.assertFalse(manifest["hypothesis_entities"][0]["established_identity"])
        self.assertEqual(manifest["hypothesis_entities"][0]["crossmatch_resolution_state"], "matched")
        self.assertTrue(manifest["hypothesis_entities"][0]["crossmatch_evidence_qualified"])

        universe = json.loads((out / "universe.json").read_text(encoding="utf-8"))
        candidates = [e for e in universe["entities"] if e["kind"] == "candidate"]
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0]["attributes"]["classification_status"], "hypothesis")
        self.assertFalse(candidates[0]["attributes"]["established_identity"])

        receipt = json.loads((out / "receipt.json").read_text(encoding="utf-8"))
        self.assertEqual(receipt["receipt_id"], result["receipt_id"])
        self.assertIn("results", receipt)

    def test_objective_targets_candidate_kind(self) -> None:
        obj = default_sky_candidate_objective()
        self.assertIn("candidate", obj.target_kinds)
        self.assertIn("astrometry", obj.required_evidence)

    def test_bundle_path_fail_closed_without_wcs(self) -> None:
        bundle = self.root / "bundle"
        bundle.mkdir()
        (bundle / "sky_localisations.json").write_text(
            json.dumps(
                {
                    "wcs_present": False,
                    "localisations": [],
                    "coordinates_invented": False,
                }
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(SkyToObjectiveBridgeError, "no declared WCS"):
            bridge_observation_bundle_to_objective(bundle, self.root / "from-bundle")

    def test_build_universe_refuses_null_sky(self) -> None:
        bogus = {
            "id": "skyloc-aaaaaaaaaaaaaaaaaaaa",
            "detection_id": "detection-aaaaaaaaaaaaaaaaaaaa",
            "status": "localised",
            "sky": {"ra_deg": None, "dec_deg": None, "frame": "ICRS", "epoch": "J2000.0"},
        }
        with self.assertRaisesRegex(SkyToObjectiveBridgeError, "invent"):
            build_temporary_universe([bogus])


if __name__ == "__main__":
    unittest.main()
