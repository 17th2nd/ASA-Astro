from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from PIL import Image

from asa_astro.evidence.detection import detect_regions
from asa_astro.evidence.graph import _relationship, build_relationships
from asa_astro.evidence.models import DetectionParameters
from tests.fixtures.generate_fixture import create_fixture


class DetectionTest(unittest.TestCase):
    def test_fixture_exercises_extended_dark_and_contamination_paths(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = create_fixture(Path(directory) / "fixture.ppm")
            with Image.open(fixture) as image:
                detections, evidence, statistics = detect_regions(
                    image,
                    "source-00000000000000000000",
                    "detector-output-00000000000000000000",
                    "provenance-00000000000000000000",
                    DetectionParameters(),
                )
        classes = {item["provisional_observation_class"] for item in detections}
        flags = {flag for item in detections for flag in item["flags"]}
        self.assertIn("extended_luminous_region", classes)
        self.assertIn("dark_or_occluding_region", classes)
        self.assertIn("possible_diffraction_spike_contamination", flags)
        self.assertIsNotNone(statistics["major_detection_id"])
        self.assertEqual({item["evidence_record_id"] for item in detections}, {item["id"] for item in evidence})
        for item in detections:
            self.assertIn("integrated_intensity", item["features"])
            self.assertIn("local_density", item["features"])
            self.assertIn("distance_from_major_structure", item["features"])
            self.assertFalse(item["features"]["integrated_intensity"]["calibrated"])


class RelationshipTest(unittest.TestCase):
    def test_forbidden_physical_relationship_cannot_be_emitted(self) -> None:
        with self.assertRaisesRegex(ValueError, "physical relationship is outside pipeline scope"):
            _relationship(
                "candidate-00000000000000000001",
                "candidate-00000000000000000002",
                "gravitational",
                "hypothesis",
                "hypothesis",
                0.2,
                "unknown",
                "prohibited test",
                0.1,
                ["evidence-00000000000000000001"],
                ["Negative fixture"],
                "provenance-00000000000000000000",
            )

    def test_orientation_strength_and_confidence_are_separate(self) -> None:
        parameters = DetectionParameters()
        detections = [
            {
                "id": "det-00000000000000000001",
                "provenance_record_id": "provenance-00000000000000000000",
                "bbox": {"x": 0, "y": 0, "width": 8, "height": 2, "unit": "pixel"},
                "centroid": {"x": 4.0, "y": 1.0, "unit": "pixel"},
                "features": {"elongation": {"value": 4.0}, "orientation": {"value": 5.0}},
                "provisional_observation_class": "extended_luminous_region",
            },
            {
                "id": "det-00000000000000000002",
                "provenance_record_id": "provenance-00000000000000000000",
                "bbox": {"x": 12, "y": 1, "width": 8, "height": 2, "unit": "pixel"},
                "centroid": {"x": 16.0, "y": 2.0, "unit": "pixel"},
                "features": {"elongation": {"value": 3.5}, "orientation": {"value": 10.0}},
                "provisional_observation_class": "extended_luminous_region",
            },
        ]
        candidates = [
            {
                "id": "candidate-00000000000000000001",
                "candidate_type": "background_extended_object",
                "detection_ids": [detections[0]["id"]],
                "supporting_evidence_ids": ["evidence-00000000000000000001"],
                "confidence": {"value": 0.4},
            },
            {
                "id": "candidate-00000000000000000002",
                "candidate_type": "background_extended_object",
                "detection_ids": [detections[1]["id"]],
                "supporting_evidence_ids": ["evidence-00000000000000000002"],
                "confidence": {"value": 0.35},
            },
        ]
        edges = build_relationships(
            "source-00000000000000000000", candidates, detections, parameters
        )
        orientation = next(edge["assertion"] for edge in edges if edge["edge_type"] == "orientation_alignment")
        self.assertEqual("normalized_orientation_alignment", orientation["relationship_strength"]["unit"])
        self.assertEqual(0.35, orientation["confidence"]["value"])
        self.assertNotEqual(
            orientation["relationship_strength"]["derivation"],
            orientation["uncertainty"]["method"],
        )


if __name__ == "__main__":
    unittest.main()
