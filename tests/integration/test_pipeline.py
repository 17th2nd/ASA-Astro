from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import tempfile
import unittest

from asa_astro.evidence.graph import FORBIDDEN_PHYSICAL_RELATIONSHIPS
from asa_astro.evidence.pipeline import hash_file, process_observation
from tests.fixtures.generate_fixture import create_fixture


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


def _tree_bytes(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


class PipelineIntegrationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.input_path = create_fixture(self.root / "synthetic-observation.ppm")
        self.metadata_path = REPOSITORY_ROOT / "tests/fixtures/synthetic_observation.metadata.json"
        self.expectations = json.loads(
            (REPOSITORY_ROOT / "tests/fixtures/expected_assertions.json").read_text(encoding="utf-8")
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_pipeline_preserves_evidence_and_emits_bounded_graph(self) -> None:
        before_hash = hash_file(self.input_path)
        output = self.root / "run"
        result = process_observation(
            self.input_path,
            output,
            metadata_path=self.metadata_path,
            source_locator="fixture:synthetic-observation-v1",
        )
        self.assertEqual(before_hash, hash_file(self.input_path))
        graph = json.loads((output / "graph.json").read_text(encoding="utf-8"))
        provenance = json.loads((output / "provenance.json").read_text(encoding="utf-8"))
        manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(before_hash, graph["source_sha256"])
        self.assertEqual(before_hash, provenance["observation_sources"][0]["sha256"])
        self.assertEqual(before_hash, result["source_sha256"])
        source_artifact = next(item for item in manifest["artifacts"] if item["role"] == "immutable_source_copy")
        self.assertEqual(before_hash, source_artifact["sha256"])
        self.assertEqual(
            before_hash,
            sha256((output / source_artifact["path"]).read_bytes()).hexdigest(),
        )

        candidates = [node["payload"] for node in graph["nodes"] if node["node_type"] == "candidate_entity"]
        extended_types = {
            "primary_extended_object",
            "possible_companion_object",
            "background_extended_object",
            "diffuse_or_uncertain_region",
        }
        self.assertGreaterEqual(
            sum(candidate["candidate_type"] in extended_types for candidate in candidates),
            self.expectations["minimum_extended_candidates"],
        )
        self.assertNotIn("system_central", {candidate["candidate_type"] for candidate in candidates})
        point_candidates = [candidate for candidate in candidates if candidate["candidate_type"] == "likely_foreground_point_source"]
        self.assertTrue(point_candidates)
        self.assertTrue(all(candidate["classification_status"] == "hypothesis" for candidate in point_candidates))

        evidence_ids = {record["id"] for record in provenance["evidence_records"]}
        self.assertTrue(graph["edges"])
        for edge in graph["edges"]:
            assertion = edge["assertion"]
            self.assertTrue(assertion["evidence_ids"])
            self.assertTrue(set(assertion["evidence_ids"]) <= evidence_ids)
            self.assertFalse(assertion["physical_claim"])
            self.assertNotIn(assertion["relationship_type"], FORBIDDEN_PHYSICAL_RELATIONSHIPS)
            self.assertNotIn(assertion["relationship_subtype"], FORBIDDEN_PHYSICAL_RELATIONSHIPS)
            self.assertIn("relationship_strength", assertion)
            self.assertIn("confidence", assertion)
            self.assertEqual("uncalibrated", assertion["confidence"]["calibration_status"])

        for detection in provenance["detections"]:
            distance = detection["features"]["distance_from_major_structure"]
            self.assertEqual("pixel", distance["unit"])
            self.assertFalse(distance["calibrated"])
        self.assertEqual("unavailable", provenance["scientific_ground_truth_status"])

        actual_required = {path.name for path in output.iterdir() if path.is_file()}
        self.assertTrue(set(self.expectations["required_bundle_files"]) <= actual_required)

    def test_repeated_runs_are_byte_equivalent(self) -> None:
        first = self.root / "first"
        second = self.root / "second"
        process_observation(self.input_path, first, metadata_path=self.metadata_path)
        process_observation(self.input_path, second, metadata_path=self.metadata_path)
        self.assertEqual(_tree_bytes(first), _tree_bytes(second))

    def test_existing_output_is_never_overwritten(self) -> None:
        output = self.root / "existing"
        output.mkdir()
        sentinel = output / "sentinel.txt"
        sentinel.write_text("preserve", encoding="utf-8")
        with self.assertRaisesRegex(FileExistsError, "refusing overwrite"):
            process_observation(self.input_path, output)
        self.assertEqual("preserve", sentinel.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
