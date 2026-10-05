"""process_observation WCS-when-present wiring and fail-closed absent path."""

from __future__ import annotations

import json
import tempfile
import unittest
from hashlib import sha256
from pathlib import Path

from asa_astro.evidence.pipeline import hash_file, process_observation
from asa_astro.evidence.validation import validate_instance
from tests.fixtures.generate_fixture import create_fixture

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


def _wcs_payload() -> dict:
    return {
        "frame": "ICRS",
        "epoch": "J2000.0",
        "crpix": [32.0, 32.0],
        "crval_deg": [150.0, -30.0],
        "cd_deg_per_pixel": [[1.0 / 3600.0, 0.0], [0.0, 1.0 / 3600.0]],
        "pixel_origin": "0-based-image-pixel",
        "source_reference": "process-observation-wcs-fixture",
    }


class ProcessObservationWcsWiringTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="asa-astro-wcs-", dir="/tmp")
        self.root = Path(self.temporary.name)
        self.input_path = create_fixture(self.root / "synthetic-observation.ppm")
        self.base_metadata = json.loads(
            (REPOSITORY_ROOT / "tests/fixtures/synthetic_observation.metadata.json").read_text(
                encoding="utf-8"
            )
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _write_metadata(self, payload: dict) -> Path:
        path = self.root / "metadata.json"
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return path

    def test_wcs_absent_fail_closed_no_invented_coords(self) -> None:
        before = hash_file(self.input_path)
        metadata_path = self._write_metadata(self.base_metadata)
        output = self.root / "run-absent"
        result = process_observation(self.input_path, output, metadata_path=metadata_path)

        self.assertEqual(before, hash_file(self.input_path))
        self.assertFalse(result["wcs_present"])
        self.assertFalse(result["coordinates_invented"])
        self.assertFalse(result["source_image_mutated"])
        self.assertGreater(result["sky_localisation_count"], 0)
        self.assertEqual(result["sky_localised_count"], 0)
        self.assertEqual(result["sky_unavailable_count"], result["sky_localisation_count"])

        sky = json.loads((output / "sky_localisations.json").read_text(encoding="utf-8"))
        self.assertFalse(sky["wcs_present"])
        self.assertFalse(sky["coordinates_invented"])
        self.assertFalse(sky["source_image_mutated"])
        self.assertIn("absent", (sky["wcs_unavailable_reason"] or "").lower())
        for item in sky["localisations"]:
            validate_instance("sky_localisation", item)
            self.assertEqual(item["status"], "unavailable")
            self.assertFalse(item["wcs_present"])
            self.assertIsNone(item["sky"]["ra_deg"])
            self.assertIsNone(item["sky"]["dec_deg"])
            self.assertEqual(item["classification_status"], "unknown")

        provenance = json.loads((output / "provenance.json").read_text(encoding="utf-8"))
        self.assertIsNone(provenance["wcs_solution"])
        self.assertFalse(provenance["sky_epistemic"]["coordinates_invented"])
        self.assertFalse(provenance["sky_epistemic"]["established_identity_promoted"])
        # F-SCI-03: digest-bound observation identity distinct from Objective RCPT
        oid = result["observation_identity"]
        self.assertEqual(oid["binding"], "content-addressed-observation-claim")
        self.assertEqual(oid["source_sha256"], before)
        self.assertIsNone(oid["wcs_digest"])
        self.assertTrue(oid["observation_claim_id"].startswith("obsclaim-"))
        self.assertEqual(oid, provenance["observation_identity"])
        self.assertEqual(oid, sky["observation_identity"])
        manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(oid, manifest["observation_identity"])
        self.assertFalse((output / "wcs_solution.json").exists())
        self.assertFalse((output / "catalogue_crossmatches.json").exists())
        summary = (output / "summary.md").read_text(encoding="utf-8")
        self.assertIn("fail closed", summary.lower())
        self.assertIn("not invented", summary.lower())

    def test_wcs_present_localises_hypothesis_and_crossmatches(self) -> None:
        before = hash_file(self.input_path)
        provenance_before = sha256(self.input_path.read_bytes()).hexdigest()
        metadata = dict(self.base_metadata)
        metadata["wcs"] = _wcs_payload()
        metadata["catalogue"] = {
            "match_radius_arcsec": 120.0,
            "provenance": {
                "catalogue_name": "synthetic-fixture-catalogue",
                "release": "test-0",
                "query_description": "in-memory process_observation test rows only",
            },
            "entries": [
                {
                    "catalogue_id": "SYN-PO-1",
                    "catalogue_name": "synthetic-fixture-catalogue",
                    "ra_deg": 150.0,
                    "dec_deg": -30.0,
                    "evidence_ids": ["evidence-catalogue-row-po-1"],
                    "labels": ["star"],
                }
            ],
        }
        metadata_path = self._write_metadata(metadata)
        output = self.root / "run-present"
        result = process_observation(self.input_path, output, metadata_path=metadata_path)

        self.assertEqual(before, hash_file(self.input_path))
        self.assertEqual(before, provenance_before)
        self.assertTrue(result["wcs_present"])
        self.assertFalse(result["coordinates_invented"])
        self.assertFalse(result["source_image_mutated"])
        self.assertGreater(result["sky_localised_count"], 0)
        self.assertEqual(result["sky_unavailable_count"], 0)
        self.assertEqual(result["catalogue_crossmatch_count"], result["sky_localisation_count"])

        wcs = json.loads((output / "wcs_solution.json").read_text(encoding="utf-8"))
        validate_instance("wcs_solution", wcs)
        self.assertEqual(wcs["status"], "declared")
        # F-SCI-01: projection honesty on declared WCS
        self.assertEqual(wcs["projection_model"], "local-linear-CD")
        self.assertEqual(wcs["coordinate_standing"], "image-space-projection-hypothesis")

        sky = json.loads((output / "sky_localisations.json").read_text(encoding="utf-8"))
        self.assertTrue(sky["wcs_present"])
        self.assertEqual(sky["projection_model"], "local-linear-CD")
        self.assertEqual(sky["coordinate_standing"], "image-space-projection-hypothesis")
        for item in sky["localisations"]:
            validate_instance("sky_localisation", item)
            self.assertEqual(item["status"], "localised")
            self.assertEqual(item["classification_status"], "hypothesis")
            self.assertIsNotNone(item["sky"]["ra_deg"])
            self.assertIsNotNone(item["sky"]["dec_deg"])
            self.assertIn("candidate_id", item)
            self.assertEqual(item["projection_model"], "local-linear-CD")
            self.assertEqual(item["coordinate_standing"], "image-space-projection-hypothesis")
            basis = " ".join(item["inference_basis"]).lower()
            self.assertIn("local-linear-cd", basis)
            self.assertIn("image-space", basis)

        # F-SCI-03: observation claim binds source+metadata+wcs
        oid = result["observation_identity"]
        self.assertEqual(oid["source_sha256"], before)
        self.assertIsNotNone(oid["metadata_sha256"])
        self.assertIsNotNone(oid["wcs_digest"])
        self.assertTrue(oid["observation_claim_id"].startswith("obsclaim-"))
        self.assertNotIn("RCPT", oid["observation_claim_id"])

        cross = json.loads((output / "catalogue_crossmatches.json").read_text(encoding="utf-8"))
        self.assertTrue(cross["evidence_qualified_only"])
        self.assertEqual(cross["classification_status_policy"], "hypothesis")
        self.assertFalse(cross["established_identity_promoted"])
        states = {item["resolution_state"] for item in cross["crossmatches"]}
        self.assertTrue(states <= {"matched", "unresolved", "contested"})
        for item in cross["crossmatches"]:
            validate_instance("catalogue_crossmatch", item)
            self.assertIn(item["classification_status"], {"hypothesis", "unknown"})
            if item["resolution_state"] == "matched":
                self.assertTrue(item["evidence_qualified"])
                self.assertEqual(item["classification_status"], "hypothesis")

        provenance = json.loads((output / "provenance.json").read_text(encoding="utf-8"))
        self.assertTrue(provenance["sky_epistemic"]["wcs_present"])
        self.assertFalse(provenance["sky_epistemic"]["established_identity_promoted"])
        self.assertEqual(provenance["observation_identity"], oid)
        self.assertEqual(provenance["sky_epistemic"]["projection_model"], "local-linear-CD")
        self.assertEqual(before, provenance["observation_sources"][0]["sha256"])
        source_copies = [
            path
            for path in (output / "source").iterdir()
            if path.is_file() and not path.name.startswith("metadata-")
        ]
        self.assertEqual(len(source_copies), 1)
        self.assertEqual(before, hash_file(source_copies[0]))
        self.assertTrue(source_copies[0].name.startswith(before))

        summary = (output / "summary.md").read_text(encoding="utf-8")
        self.assertIn("hypothesis", summary.lower())
        self.assertIn("evidence-qualified", summary.lower())

    def test_incomplete_wcs_fail_closed(self) -> None:
        metadata = dict(self.base_metadata)
        metadata["wcs"] = {"frame": "ICRS", "epoch": "J2000.0"}  # incomplete
        metadata_path = self._write_metadata(metadata)
        output = self.root / "run-incomplete"
        result = process_observation(self.input_path, output, metadata_path=metadata_path)
        self.assertFalse(result["wcs_present"])
        self.assertEqual(result["sky_localised_count"], 0)
        sky = json.loads((output / "sky_localisations.json").read_text(encoding="utf-8"))
        self.assertIn("incomplete", (sky["wcs_unavailable_reason"] or "").lower())
        for item in sky["localisations"]:
            self.assertEqual(item["status"], "unavailable")
            self.assertIsNone(item["sky"]["ra_deg"])


if __name__ == "__main__":
    unittest.main()
