"""Observed-vs-expected residuals + missing-expected + next-evidence (Action UI)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from asa_astro.evidence.crossmatch import crossmatch_localisation
from asa_astro.evidence.wcs import localise_detection
from asa_astro.residuals import compute_observed_vs_expected, write_observed_vs_expected


def _wcs(crval=(180.0, -20.0)):
    return {
        "frame": "ICRS",
        "epoch": "J2000.0",
        "crpix": [100.0, 100.0],
        "crval_deg": [crval[0], crval[1]],
        "cd_deg_per_pixel": [[1.0 / 3600.0, 0.0], [0.0, 1.0 / 3600.0]],
    }


def _loc(x=100.0, y=100.0, wcs=None):
    return localise_detection(
        {"id": "detection-aaaaaaaaaaaaaaaaaaaa", "centroid": {"x": x, "y": y, "unit": "pixel"}},
        wcs if wcs is not None else _wcs(),
        candidate_id="candidate-bbbbbbbbbbbbbbbbbbbb",
    )


class ObservedVsExpectedTest(unittest.TestCase):
    def test_within_tolerance_and_hypothesis_flags(self) -> None:
        loc = _loc()
        expected = [
            {
                "catalogue_id": "EXP-1",
                "catalogue_name": "synthetic-expected",
                "ra_deg": 180.0,
                "dec_deg": -20.0,
                "evidence_ids": ["ev-1"],
                "labels": ["star"],
            }
        ]
        xm = crossmatch_localisation(
            loc,
            expected,
            match_radius_arcsec=5.0,
            catalogue_provenance={
                "catalogue_name": "synthetic-expected",
                "release": "t0",
                "query_description": "in-memory",
            },
        )
        report = compute_observed_vs_expected(
            [loc], expected, crossmatches=[xm], residual_tolerance_arcsec=2.0
        )
        self.assertFalse(report["epistemic"]["established_identity_promoted"])
        self.assertFalse(report["epistemic"]["coordinates_invented"])
        self.assertEqual(report["summary"]["within_tolerance_count"], 1)
        self.assertEqual(report["residuals"][0]["status"], "within_tolerance")
        self.assertEqual(report["residuals"][0]["classification_status"], "hypothesis")
        self.assertTrue(report["action_ui"]["honesty"]["hypothesis_only"])
        self.assertTrue(any("tolerance" in r["plain_language"].lower() or "hypothesis" in r["plain_language"].lower() for r in report["residuals"]))
        self.assertTrue(report["next_evidence_recommendations"])
        self.assertIn("hypothesis", report["next_evidence_recommendations"][0]["plain_language"].lower())

    def test_missing_expected_and_recommendation(self) -> None:
        loc = _loc()
        expected = [
            {
                "catalogue_id": "EXP-NEAR",
                "catalogue_name": "synthetic-expected",
                "ra_deg": 180.0,
                "dec_deg": -20.0,
                "evidence_ids": ["ev-near"],
            },
            {
                "catalogue_id": "EXP-FAR",
                "catalogue_name": "synthetic-expected",
                "ra_deg": 181.0,
                "dec_deg": -20.0,
                "evidence_ids": ["ev-far"],
            },
        ]
        report = compute_observed_vs_expected([loc], expected, match_radius_arcsec=5.0)
        self.assertEqual(report["summary"]["missing_expected_count"], 1)
        self.assertEqual(report["missing_expected"][0]["catalogue_id"], "EXP-FAR")
        self.assertIn("not matched", report["missing_expected"][0]["plain_language"].lower())
        codes = {r["code"] for r in report["next_evidence_recommendations"]}
        self.assertIn("recover_missing_expected", codes)
        self.assertTrue(report["action_ui"]["missing_lines"])

    def test_unlocalised_fail_closed(self) -> None:
        loc = localise_detection(
            {"id": "detection-aaaaaaaaaaaaaaaaaaaa", "centroid": {"x": 100.0, "y": 100.0, "unit": "pixel"}},
            None,
        )
        report = compute_observed_vs_expected(
            [loc],
            [{"catalogue_id": "E", "catalogue_name": "c", "ra_deg": 1.0, "dec_deg": 1.0}],
        )
        self.assertEqual(report["residuals"][0]["status"], "unlocalised")
        self.assertIsNone(report["residuals"][0]["observed_sky"])
        self.assertTrue(report["summary"]["wcs_fail_closed"])
        self.assertIn("not invented", report["residuals"][0]["plain_language"].lower())
        codes = {r["code"] for r in report["next_evidence_recommendations"]}
        self.assertIn("supply_declared_wcs", codes)
        self.assertIn("WCS", report["action_ui"]["headline"])

    def test_offset_residual(self) -> None:
        # 3 arcsec offset from CRVAL with tolerance 1"
        loc = _loc(x=103.0, y=100.0)
        expected = [
            {
                "catalogue_id": "EXP-OFF",
                "catalogue_name": "synthetic-expected",
                "ra_deg": 180.0,
                "dec_deg": -20.0,
                "evidence_ids": ["ev"],
            }
        ]
        report = compute_observed_vs_expected(
            [loc], expected, match_radius_arcsec=5.0, residual_tolerance_arcsec=1.0
        )
        self.assertEqual(report["residuals"][0]["status"], "offset")
        self.assertFalse(report["residuals"][0]["within_tolerance"])
        codes = {r["code"] for r in report["next_evidence_recommendations"]}
        self.assertIn("verify_wcs_or_epoch", codes)

    def test_write_report(self) -> None:
        loc = _loc()
        report = compute_observed_vs_expected(
            [loc],
            [{"catalogue_id": "E", "catalogue_name": "c", "ra_deg": 180.0, "dec_deg": -20.0, "evidence_ids": ["e"]}],
        )
        with tempfile.TemporaryDirectory(prefix="asa-resid-", dir="/tmp") as tmp:
            path = write_observed_vs_expected(report, Path(tmp) / "observed_vs_expected.json")
            self.assertTrue(path.is_file())
            text = path.read_text(encoding="utf-8")
            self.assertIn("asa-astro-observed-vs-expected-v1", text)
            self.assertLess(path.stat().st_size, 100_000)


if __name__ == "__main__":
    unittest.main()
