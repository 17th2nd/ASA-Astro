"""Present-only observation honesty projection (Operator C / Significance contract)."""

from __future__ import annotations

import unittest

from app.observation_honesty import (
    ALLOWED_CLASSIFICATION,
    project_crossmatch,
    project_localisation,
    project_observation_evidence,
    project_wcs,
)


class WcsProjection(unittest.TestCase):
    def test_absent_is_none(self):
        self.assertIsNone(project_wcs(None))
        self.assertIsNone(project_wcs({"status": "something-else"}))

    def test_declared_surfaces_frame_epoch_source(self):
        view = project_wcs({
            "status": "declared",
            "epistemic_classification": "externally_supplied",
            "frame": "ICRS",
            "epoch": "J2000.0",
            "source_reference": "fits-hdr:abc",
        })
        self.assertTrue(view["present"])
        self.assertIn("WCS declared", view["text"])
        self.assertIn("ICRS", view["text"])
        self.assertEqual(view["source"]["source_reference"], "fits-hdr:abc")
        self.assertEqual(view["label"], "record")


class LocalisationProjection(unittest.TestCase):
    def test_unavailable_shows_reason_no_sky(self):
        view = project_localisation({
            "id": "loc-1",
            "detection_id": "det-1",
            "status": "unavailable",
            "classification_status": "unknown",
            "wcs_present": False,
            "pixel_centroid": {"x": 1, "y": 2},
            "sky": {"ra_deg": None, "dec_deg": None, "frame": None, "epoch": None},
            "unavailable_reason": "WCS absent",
            "inference_basis": ["no-wcs"],
        })
        self.assertEqual(view["status"], "unavailable")
        self.assertIsNone(view["sky"])
        self.assertIn("WCS absent", view["text"])
        self.assertEqual(view["classification_status"], "unknown")
        self.assertNotEqual(view["label"], "established")

    def test_localised_shows_sky_and_hypothesis_badge(self):
        view = project_localisation({
            "id": "loc-2",
            "detection_id": "det-2",
            "status": "localised",
            "classification_status": "hypothesis",
            "wcs_present": True,
            "pixel_centroid": {"x": 10, "y": 20},
            "sky": {"ra_deg": 12.3, "dec_deg": -4.5, "frame": "ICRS", "epoch": "J2000.0"},
            "inference_basis": ["declared-wcs-linear-cd"],
        })
        self.assertEqual(view["sky"]["ra_deg"], 12.3)
        self.assertEqual(view["classification_status"], "hypothesis")
        self.assertIn(view["label"], ALLOWED_CLASSIFICATION)
        self.assertEqual(view["source"]["schema"], "schemas/observation/sky-localisation.schema.json")
        # F-SCI-01: primary text must label image-space / linear-CD / hypothesis (not RA/Dec-only).
        low = view["text"].lower()
        self.assertIn("image-space", low)
        self.assertTrue("linear-cd" in low or "local-linear" in low)
        self.assertIn("hypothesis", low)
        self.assertNotRegex(view["text"], r"^localised detection .+ → ra=")
        self.assertEqual(view["projection_model"], "local-linear-CD")
        self.assertEqual(view["coordinate_standing"], "image-space-projection-hypothesis")

    def test_localised_prefers_pipeline_projection_fields(self):
        view = project_localisation({
            "id": "loc-2b",
            "detection_id": "det-2b",
            "status": "localised",
            "classification_status": "hypothesis",
            "wcs_present": True,
            "pixel_centroid": {"x": 1, "y": 2},
            "sky": {"ra_deg": 1.0, "dec_deg": 2.0, "frame": "ICRS", "epoch": "J2000.0"},
            "projection_model": "local-linear-CD",
            "coordinate_standing": "image-space-projection-hypothesis",
            "inference_basis": ["pipeline-emitted-standing"],
        })
        self.assertEqual(view["projection_model"], "local-linear-CD")
        self.assertIn("pipeline-emitted-standing", view["text"])

    def test_rejects_established_classification(self):
        view = project_localisation({
            "id": "loc-3",
            "detection_id": "det-3",
            "status": "localised",
            "classification_status": "established",  # not allowed — demoted to unknown
            "wcs_present": True,
            "pixel_centroid": {"x": 0, "y": 0},
            "sky": {"ra_deg": 1.0, "dec_deg": 2.0, "frame": "ICRS", "epoch": "J2000.0"},
            "inference_basis": ["x"],
        })
        self.assertEqual(view["classification_status"], "unknown")
        self.assertNotEqual(view["label"], "established")


class CrossmatchProjection(unittest.TestCase):
    def test_matched_requires_evidence_qualified(self):
        base = {
            "id": "xm-1",
            "localisation_id": "loc-1",
            "detection_id": "det-1",
            "classification_status": "hypothesis",
            "match_radius_arcsec": 2.0,
            "catalogue_provenance": {
                "catalogue_name": "Gaia",
                "release": "DR3",
                "query_description": "cone",
            },
            "inference_basis": ["positional"],
            "candidates": [{
                "catalogue_id": "G1",
                "catalogue_name": "Gaia",
                "separation_arcsec": 0.4,
                "evidence_ids": ["ev-1"],
                "sky": {"ra_deg": 1.0, "dec_deg": 2.0},
            }],
        }
        ok = project_crossmatch({**base, "resolution_state": "matched", "evidence_qualified": True})
        self.assertEqual(ok["resolution_state"], "matched")
        self.assertIn("evidence-qualified", ok["text"])

        bad = project_crossmatch({**base, "resolution_state": "matched", "evidence_qualified": False})
        self.assertEqual(bad["resolution_state"], "unresolved")

    def test_contested_lists_without_winner(self):
        view = project_crossmatch({
            "id": "xm-2",
            "localisation_id": "loc-2",
            "detection_id": "det-2",
            "resolution_state": "contested",
            "classification_status": "hypothesis",
            "evidence_qualified": False,
            "match_radius_arcsec": 2.0,
            "catalogue_provenance": {
                "catalogue_name": "Gaia",
                "release": "DR3",
                "query_description": "cone",
            },
            "inference_basis": ["positional"],
            "candidates": [
                {"catalogue_id": "A", "catalogue_name": "Gaia", "separation_arcsec": 0.1,
                 "evidence_ids": ["e1"], "sky": {"ra_deg": 1, "dec_deg": 2}},
                {"catalogue_id": "B", "catalogue_name": "Gaia", "separation_arcsec": 0.2,
                 "evidence_ids": ["e2"], "sky": {"ra_deg": 1.01, "dec_deg": 2.01}},
            ],
        })
        self.assertEqual(view["resolution_state"], "contested")
        self.assertIn("without picking a winner", view["text"])
        self.assertIn("Gaia/A", view["text"])
        self.assertIn("Gaia/B", view["text"])
        self.assertIn(view["label"], ALLOWED_CLASSIFICATION)


class Aggregate(unittest.TestCase):
    def test_empty_path_present_false(self):
        block = project_observation_evidence()
        self.assertFalse(block["present"])
        self.assertIsNone(block["wcs"])
        self.assertEqual(block["localisations"], [])
        self.assertEqual(block["crossmatches"], [])
        self.assertTrue(block["display_rules"]["never_established_from_this_slice"])

    def test_present_when_any_record(self):
        block = project_observation_evidence(wcs={
            "status": "declared",
            "epistemic_classification": "externally_supplied",
            "frame": "ICRS",
            "epoch": "J2000.0",
        })
        self.assertTrue(block["present"])
        self.assertIsNotNone(block["wcs"])


if __name__ == "__main__":
    unittest.main()
