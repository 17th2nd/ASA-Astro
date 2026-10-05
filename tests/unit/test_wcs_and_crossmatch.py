"""WCS-when-present localisation and evidence-qualified catalogue crossmatch."""

from __future__ import annotations

import math
import unittest

from asa_astro.evidence.crossmatch import (
    angular_separation_arcsec,
    crossmatch_localisation,
    crossmatch_localisations,
)
from asa_astro.evidence.validation import load_schemas, validate_instance
from asa_astro.evidence.wcs import (
    COORDINATE_STANDING,
    PROJECTION_MODEL,
    WcsUnavailable,
    compute_coordinates_invented,
    localise_detection,
    localise_detections,
    parse_declared_wcs,
    pixel_to_sky,
    wcs_content_digest,
)


def _wcs(**overrides):
    base = {
        "frame": "ICRS",
        "epoch": "J2000.0",
        "crpix": [100.0, 100.0],
        "crval_deg": [180.0, -20.0],
        # 1 arcsec/pixel on both axes, no rotation
        "cd_deg_per_pixel": [[1.0 / 3600.0, 0.0], [0.0, 1.0 / 3600.0]],
        "pixel_origin": "0-based-image-pixel",
        "source_reference": "synthetic-test-wcs",
    }
    base.update(overrides)
    return base


def _detection(det_id: str = "detection-aaaaaaaaaaaaaaaaaaaa", x: float = 100.0, y: float = 100.0):
    return {
        "id": det_id,
        "centroid": {"x": x, "y": y, "unit": "pixel"},
    }


PROVENANCE = {
    "catalogue_name": "synthetic-fixture-catalogue",
    "release": "test-0",
    "query_description": "in-memory test rows only; no disk dump",
}


class WcsParseTest(unittest.TestCase):
    def test_parse_declared_wcs_round_trip(self) -> None:
        record = parse_declared_wcs(_wcs())
        validate_instance("wcs_solution", record)
        self.assertEqual(record["status"], "declared")
        self.assertEqual(record["epistemic_classification"], "externally_supplied")
        self.assertEqual(record["projection_model"], PROJECTION_MODEL)
        self.assertEqual(record["coordinate_standing"], COORDINATE_STANDING)
        self.assertIsNotNone(wcs_content_digest(record))

    def test_absent_wcs_fail_closed(self) -> None:
        with self.assertRaisesRegex(WcsUnavailable, "absent"):
            parse_declared_wcs(None)
        with self.assertRaisesRegex(WcsUnavailable, "incomplete"):
            parse_declared_wcs({"frame": "ICRS"})

    def test_pixel_to_sky_at_crpix(self) -> None:
        wcs = parse_declared_wcs(_wcs())
        sky = pixel_to_sky(100.0, 100.0, wcs)
        self.assertAlmostEqual(sky["ra_deg"], 180.0, places=9)
        self.assertAlmostEqual(sky["dec_deg"], -20.0, places=9)

    def test_pixel_to_sky_offset(self) -> None:
        wcs = parse_declared_wcs(_wcs())
        # +10 px in x → +10 arcsec in RA
        sky = pixel_to_sky(110.0, 100.0, wcs)
        self.assertAlmostEqual(sky["ra_deg"], 180.0 + 10.0 / 3600.0, places=9)
        self.assertAlmostEqual(sky["dec_deg"], -20.0, places=9)

    def test_never_invent_coords_when_wcs_absent(self) -> None:
        result = localise_detection(_detection(), None)
        validate_instance("sky_localisation", result)
        self.assertEqual(result["status"], "unavailable")
        self.assertFalse(result["wcs_present"])
        self.assertIsNone(result["sky"]["ra_deg"])
        self.assertIsNone(result["sky"]["dec_deg"])
        self.assertEqual(result["classification_status"], "unknown")
        self.assertTrue(any("not invented" in note.lower() or "not invented" in note for note in result["inference_basis"]) or any("invented" in note.lower() for note in result["inference_basis"]))


class LocaliseTest(unittest.TestCase):
    def test_localise_hypothesis_label(self) -> None:
        result = localise_detection(_detection(), _wcs(), candidate_id="candidate-bbbbbbbbbbbbbbbbbbbb")
        validate_instance("sky_localisation", result)
        self.assertEqual(result["status"], "localised")
        self.assertTrue(result["wcs_present"])
        self.assertEqual(result["classification_status"], "hypothesis")
        self.assertEqual(result["candidate_id"], "candidate-bbbbbbbbbbbbbbbbbbbb")
        self.assertAlmostEqual(result["sky"]["ra_deg"], 180.0, places=9)
        self.assertEqual(result["projection_model"], "local-linear-CD")
        self.assertEqual(result["coordinate_standing"], "image-space-projection-hypothesis")
        self.assertFalse(compute_coordinates_invented([result]))

    def test_compute_coordinates_invented_detects_escape(self) -> None:
        """F-SCI-04: invented flag is computed, not hard-coded False."""
        honest = localise_detection(_detection(), _wcs())
        self.assertFalse(compute_coordinates_invented([honest]))
        escaped = {
            "status": "localised",
            "wcs_present": False,
            "sky": {"ra_deg": 1.0, "dec_deg": 2.0, "frame": "ICRS", "epoch": "J2000.0"},
        }
        self.assertTrue(compute_coordinates_invented([escaped]))

    def test_localise_many(self) -> None:
        dets = [
            _detection("detection-aaaaaaaaaaaaaaaaaaaa", 100.0, 100.0),
            _detection("detection-cccccccccccccccccccc", 110.0, 100.0),
        ]
        results = localise_detections(dets, _wcs())
        self.assertEqual(len(results), 2)
        for item in results:
            validate_instance("sky_localisation", item)
            self.assertEqual(item["status"], "localised")


class CrossmatchTest(unittest.TestCase):
    def test_angular_separation_zero(self) -> None:
        self.assertAlmostEqual(angular_separation_arcsec(10.0, -5.0, 10.0, -5.0), 0.0, places=6)

    def test_matched_evidence_qualified(self) -> None:
        loc = localise_detection(_detection(), _wcs())
        catalogue = [
            {
                "catalogue_id": "SYN-1",
                "catalogue_name": "synthetic-fixture-catalogue",
                "ra_deg": 180.0,
                "dec_deg": -20.0,
                "evidence_ids": ["evidence-catalogue-row-1"],
                "labels": ["star"],
            }
        ]
        result = crossmatch_localisation(
            loc, catalogue, match_radius_arcsec=5.0, catalogue_provenance=PROVENANCE
        )
        validate_instance("catalogue_crossmatch", result)
        self.assertEqual(result["resolution_state"], "matched")
        self.assertTrue(result["evidence_qualified"])
        self.assertEqual(result["classification_status"], "hypothesis")
        self.assertEqual(len(result["candidates"]), 1)

    def test_sole_hit_without_evidence_stays_unresolved(self) -> None:
        loc = localise_detection(_detection(), _wcs())
        catalogue = [
            {
                "catalogue_id": "SYN-2",
                "catalogue_name": "synthetic-fixture-catalogue",
                "ra_deg": 180.0,
                "dec_deg": -20.0,
                "evidence_ids": [],
            }
        ]
        result = crossmatch_localisation(
            loc, catalogue, match_radius_arcsec=5.0, catalogue_provenance=PROVENANCE
        )
        validate_instance("catalogue_crossmatch", result)
        self.assertEqual(result["resolution_state"], "unresolved")
        self.assertFalse(result["evidence_qualified"])
        self.assertEqual(len(result["candidates"]), 1)

    def test_contested_multiple_hits(self) -> None:
        loc = localise_detection(_detection(), _wcs())
        catalogue = [
            {
                "catalogue_id": "SYN-A",
                "catalogue_name": "synthetic-fixture-catalogue",
                "ra_deg": 180.0,
                "dec_deg": -20.0,
                "evidence_ids": ["ev-a"],
            },
            {
                "catalogue_id": "SYN-B",
                "catalogue_name": "synthetic-fixture-catalogue",
                "ra_deg": 180.0 + 1.0 / 3600.0,
                "dec_deg": -20.0,
                "evidence_ids": ["ev-b"],
            },
        ]
        result = crossmatch_localisation(
            loc, catalogue, match_radius_arcsec=5.0, catalogue_provenance=PROVENANCE
        )
        validate_instance("catalogue_crossmatch", result)
        self.assertEqual(result["resolution_state"], "contested")
        self.assertFalse(result["evidence_qualified"])
        self.assertEqual(len(result["candidates"]), 2)

    def test_unresolved_outside_radius(self) -> None:
        loc = localise_detection(_detection(), _wcs())
        catalogue = [
            {
                "catalogue_id": "SYN-FAR",
                "catalogue_name": "synthetic-fixture-catalogue",
                "ra_deg": 181.0,
                "dec_deg": -20.0,
                "evidence_ids": ["ev-far"],
            }
        ]
        result = crossmatch_localisation(
            loc, catalogue, match_radius_arcsec=5.0, catalogue_provenance=PROVENANCE
        )
        validate_instance("catalogue_crossmatch", result)
        self.assertEqual(result["resolution_state"], "unresolved")
        self.assertEqual(result["candidates"], [])

    def test_unavailable_when_localisation_missing(self) -> None:
        loc = localise_detection(_detection(), None)
        result = crossmatch_localisation(
            loc, [], match_radius_arcsec=5.0, catalogue_provenance=PROVENANCE
        )
        validate_instance("catalogue_crossmatch", result)
        self.assertEqual(result["resolution_state"], "unavailable")
        self.assertFalse(result["evidence_qualified"])

    def test_batch_crossmatch(self) -> None:
        locs = localise_detections(
            [_detection("detection-aaaaaaaaaaaaaaaaaaaa"), _detection("detection-dddddddddddddddddddd", 200.0, 100.0)],
            _wcs(),
        )
        # second detection is 100" away in RA from CRVAL
        catalogue = [
            {
                "catalogue_id": "SYN-1",
                "catalogue_name": "synthetic-fixture-catalogue",
                "ra_deg": 180.0,
                "dec_deg": -20.0,
                "evidence_ids": ["ev-1"],
            }
        ]
        results = crossmatch_localisations(
            locs, catalogue, match_radius_arcsec=5.0, catalogue_provenance=PROVENANCE
        )
        self.assertEqual(results[0]["resolution_state"], "matched")
        self.assertEqual(results[1]["resolution_state"], "unresolved")

    def test_refuses_invented_catalogue_coords(self) -> None:
        loc = localise_detection(_detection(), _wcs())
        with self.assertRaisesRegex(ValueError, "lacks ra_deg"):
            crossmatch_localisation(
                loc,
                [{"catalogue_id": "X", "catalogue_name": "synthetic-fixture-catalogue", "evidence_ids": ["e"]}],
                match_radius_arcsec=5.0,
                catalogue_provenance=PROVENANCE,
            )


class SchemaRegistrationTest(unittest.TestCase):
    def test_new_schemas_loaded(self) -> None:
        schemas = load_schemas()
        for name in (
            "wcs-solution.schema.json",
            "sky-localisation.schema.json",
            "catalogue-crossmatch.schema.json",
        ):
            self.assertIn(name, schemas)


if __name__ == "__main__":
    unittest.main()
