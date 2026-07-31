from __future__ import annotations

import unittest

from asa_astro.evidence.models import DetectionParameters, canonical_json, stable_id
from asa_astro.evidence.validation import load_schemas


class ModelsAndSchemasTest(unittest.TestCase):
    def test_all_schemas_are_valid_draft_2020_12(self) -> None:
        schemas = load_schemas()
        expected = {
            "candidate-entity.schema.json",
            "candidate-graph.schema.json",
            "common.schema.json",
            "confidence.schema.json",
            "detection.schema.json",
            "detector-output.schema.json",
            "evidence-record.schema.json",
            "candidate-graph-edge.schema.json",
            "candidate-graph-node.schema.json",
            "observation-source.schema.json",
            "observation.schema.json",
            "provenance-record.schema.json",
            "candidate-relationship-assertion.schema.json",
            "source-image-metadata.schema.json",
            "uncertainty.schema.json",
        }
        self.assertTrue(expected <= set(schemas))

    def test_candidate_schema_rejects_identity_without_evidence(self) -> None:
        from asa_astro.evidence.validation import validate_instance

        with self.assertRaisesRegex(ValueError, "candidate_entity schema validation failed"):
            validate_instance(
                "candidate_entity",
                {
                    "schema_version": "0.1.0",
                    "ontology_version": "ASTRO-ONTOLOGY-0001",
                    "record_status": "active",
                    "epistemic_classification": "inferred",
                    "id": "candidate-00000000000000000000",
                },
            )

    def test_identifiers_are_canonical_and_order_independent(self) -> None:
        self.assertEqual(canonical_json({"b": 2, "a": 1}), '{"a":1,"b":2}')
        self.assertEqual(stable_id("test", {"a": 1, "b": 2}), stable_id("test", {"b": 2, "a": 1}))

    def test_parameter_file_rejects_unknown_values(self) -> None:
        with self.assertRaisesRegex(ValueError, "unknown detection parameter"):
            DetectionParameters.from_mapping({"undocumented_threshold": 2})

    def test_parameter_invariants_are_enforced(self) -> None:
        with self.assertRaisesRegex(ValueError, "point_max_pixels"):
            DetectionParameters(point_max_pixels=50, extended_min_pixels=45).validate()


if __name__ == "__main__":
    unittest.main()
