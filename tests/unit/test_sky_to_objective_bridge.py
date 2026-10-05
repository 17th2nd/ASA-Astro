"""Sky→candidates→Objective bridge: hypothesis labels + receipt; fail closed without WCS localisation.

S1 (Runtime handoff A): observation_bundle_to_objective binds observation_identity;
SYN-SITE is demo-only; no silent slice1 substitute.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from asa_astro.bridge import (
    DEMO_SITE_DESIGNATION,
    SkyToObjectiveBridgeError,
    UNDECLARED_SITE_DESIGNATION,
    bridge_sky_localisations_to_objective,
    default_sky_candidate_objective,
    observation_bundle_to_objective,
)
from asa_astro.bridge.sky_to_objective import build_temporary_universe
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


def _observation_identity(**overrides):
    base = {
        "binding": "content-addressed-observation-claim",
        "source_sha256": "a" * 64,
        "metadata_sha256": "b" * 64,
        "wcs_digest": "c" * 64,
        "observation_claim_digest": "d" * 64,
        "observation_claim_id": "obsclaim-" + "d" * 64,
    }
    base.update(overrides)
    return base


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

    def test_bridge_writes_receipt_with_hypothesis_flags_demo_site(self) -> None:
        """Synthetic demo path remains available under explicit allow_synthetic_demo_site."""
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
        result = bridge_sky_localisations_to_objective(
            [loc], out, crossmatches=[xm], allow_synthetic_demo_site=True
        )

        self.assertFalse(result["established_identity_promoted"])
        self.assertFalse(result["coordinates_invented"])
        self.assertEqual(result["hypothesis_entity_count"], 1)
        self.assertTrue(result["site_demo_only"])
        self.assertEqual(result["site_standing"], "synthetic-demo-only")
        self.assertFalse(result["slice1_substituted"])
        self.assertTrue((out / "receipt.json").is_file())
        self.assertTrue((out / "receipt.sha256").is_file())
        self.assertTrue((out / "bridge_manifest.json").is_file())

        manifest = json.loads((out / "bridge_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["epistemic"]["sky_candidates_are"], "hypothesis")
        self.assertFalse(manifest["epistemic"]["established_identity_promoted"])
        self.assertFalse(manifest["epistemic"]["catalogue_match_promotes_identity"])
        self.assertFalse(manifest["epistemic"]["slice1_substituted"])
        self.assertEqual(manifest["hypothesis_entities"][0]["classification_status"], "hypothesis")
        self.assertFalse(manifest["hypothesis_entities"][0]["established_identity"])
        self.assertEqual(manifest["hypothesis_entities"][0]["crossmatch_resolution_state"], "matched")
        self.assertTrue(manifest["hypothesis_entities"][0]["crossmatch_evidence_qualified"])
        self.assertEqual(manifest["site"]["designation"], DEMO_SITE_DESIGNATION)

        universe = json.loads((out / "universe.json").read_text(encoding="utf-8"))
        candidates = [e for e in universe["entities"] if e["kind"] == "candidate"]
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0]["attributes"]["classification_status"], "hypothesis")
        self.assertFalse(candidates[0]["attributes"]["established_identity"])
        # Demo SYN-SITE is present only under the explicit flag.
        sites = [e for e in universe["entities"] if e["kind"] == "site"]
        self.assertEqual(sites[0]["designation"], DEMO_SITE_DESIGNATION)
        self.assertTrue(sites[0]["attributes"]["demo_only"])

        receipt = json.loads((out / "receipt.json").read_text(encoding="utf-8"))
        self.assertEqual(receipt["receipt_id"], result["receipt_id"])
        self.assertIn("results", receipt)

    def test_real_path_undeclared_site_no_invented_latlon(self) -> None:
        """Without declared site and without demo flag: undeclared hypothesis, no lat/lon."""
        loc = _loc()
        oid = _observation_identity()
        out = self.root / "out-undeclared"
        result = bridge_sky_localisations_to_objective(
            [loc], out, observation_identity=oid, allow_synthetic_demo_site=False
        )
        self.assertEqual(result["site_standing"], "undeclared")
        self.assertFalse(result["site_demo_only"])
        self.assertEqual(result["observation_identity"]["observation_claim_digest"], oid["observation_claim_digest"])
        universe = json.loads((out / "universe.json").read_text(encoding="utf-8"))
        sites = [e for e in universe["entities"] if e["kind"] == "site"]
        self.assertEqual(sites[0]["designation"], UNDECLARED_SITE_DESIGNATION)
        self.assertNotIn("latitude_deg", sites[0]["attributes"])
        self.assertNotIn("longitude_deg", sites[0]["attributes"])
        self.assertFalse(sites[0]["attributes"]["coordinates_present"])
        candidates = [e for e in universe["entities"] if e["kind"] == "candidate"]
        self.assertEqual(
            candidates[0]["attributes"]["observation_claim_digest"],
            oid["observation_claim_digest"],
        )

    def test_declared_site_used_without_demo_coords(self) -> None:
        loc = _loc()
        out = self.root / "out-declared"
        result = bridge_sky_localisations_to_objective(
            [loc],
            out,
            site={
                "designation": "SSO-AAT",
                "latitude_deg": -31.2754,
                "longitude_deg": 149.0672,
                "elevation_m": 1164.0,
            },
            allow_synthetic_demo_site=False,
        )
        self.assertEqual(result["site_standing"], "declared-metadata")
        self.assertFalse(result["site_demo_only"])
        universe = json.loads((out / "universe.json").read_text(encoding="utf-8"))
        sites = [e for e in universe["entities"] if e["kind"] == "site"]
        self.assertEqual(sites[0]["designation"], "SSO-AAT")
        self.assertEqual(sites[0]["attributes"]["latitude_deg"], -31.2754)
        self.assertNotEqual(sites[0]["designation"], DEMO_SITE_DESIGNATION)

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
            observation_bundle_to_objective(bundle, self.root / "from-bundle")
        self.assertFalse((self.root / "from-bundle").exists())

    def test_bundle_fail_closed_no_localised_no_slice1_fallback(self) -> None:
        """S1-(2): no localisations → fail-closed; slice1 is not substituted."""
        bundle = self.root / "bundle-noloc"
        bundle.mkdir()
        oid = _observation_identity(wcs_digest=None, observation_claim_digest="e" * 64,
                                    observation_claim_id="obsclaim-" + "e" * 64)
        (bundle / "sky_localisations.json").write_text(
            json.dumps(
                {
                    "wcs_present": True,
                    "observation_identity": oid,
                    "localisations": [
                        {
                            "id": "skyloc-bbbbbbbbbbbbbbbbbbbb",
                            "detection_id": "detection-aaaaaaaaaaaaaaaaaaaa",
                            "status": "unavailable",
                            "wcs_present": True,
                            "sky": {"ra_deg": None, "dec_deg": None, "frame": "ICRS", "epoch": "J2000.0"},
                        }
                    ],
                    "coordinates_invented": False,
                }
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(SkyToObjectiveBridgeError, "slice1 was not substituted"):
            observation_bundle_to_objective(bundle, self.root / "no-fallback")
        self.assertFalse((self.root / "no-fallback").exists())
        # Ensure the shared synthetic universe file was never copied in.
        slice1 = Path(__file__).resolve().parents[2] / "data" / "universe" / "slice1.json"
        self.assertTrue(slice1.is_file())  # still present on disk as a demo fixture
        # But the refused out dir must not contain it.
        self.assertFalse((self.root / "no-fallback" / "universe.json").exists())

    def test_observation_bundle_to_objective_binds_identity(self) -> None:
        """S1-(1): localised fixture → Objective receipt + observation digests bound."""
        loc = _loc()
        oid = _observation_identity()
        bundle = self.root / "bundle-ok"
        bundle.mkdir()
        (bundle / "sky_localisations.json").write_text(
            json.dumps(
                {
                    "wcs_present": True,
                    "observation_identity": oid,
                    "localisations": [loc],
                    "coordinates_invented": False,
                    "source_image_mutated": False,
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        out = self.root / "bridged"
        result = observation_bundle_to_objective(
            bundle,
            out,
            site={"designation": "TEST-SITE", "latitude_deg": -31.0, "longitude_deg": 149.0},
        )
        self.assertEqual(result["api"], "asa_astro.bridge.observation_bundle_to_objective")
        self.assertFalse(result["slice1_substituted"])
        self.assertFalse(result["site_demo_only"])
        self.assertEqual(result["site_standing"], "declared-metadata")
        self.assertIsNotNone(result["observation_identity"])
        self.assertEqual(
            result["observation_identity"]["observation_claim_digest"],
            oid["observation_claim_digest"],
        )
        self.assertEqual(
            result["observation_identity"]["source_sha256"],
            oid["source_sha256"],
        )
        self.assertTrue((out / "receipt.json").is_file())
        self.assertTrue((out / "observation_identity.json").is_file())
        written_oid = json.loads((out / "observation_identity.json").read_text(encoding="utf-8"))
        self.assertEqual(written_oid["observation_claim_id"], oid["observation_claim_id"])
        manifest = json.loads((out / "bridge_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["observation_identity"]["observation_claim_digest"], oid["observation_claim_digest"])
        self.assertEqual(manifest["epistemic"]["primary_universe_source"], "sky-localisations-bridge")
        self.assertFalse(manifest["epistemic"]["slice1_substituted"])
        universe = json.loads((out / "universe.json").read_text(encoding="utf-8"))
        # Must not be the slice1 universe id / shared synthetic catalogue entities.
        slice1 = json.loads(
            (Path(__file__).resolve().parents[2] / "data" / "universe" / "slice1.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertNotEqual(universe.get("universe_id"), slice1.get("universe_id"))
        candidates = [e for e in universe["entities"] if e["kind"] == "candidate"]
        self.assertEqual(candidates[0]["attributes"]["observation_claim_id"], oid["observation_claim_id"])

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
