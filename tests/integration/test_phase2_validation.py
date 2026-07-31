from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import tempfile
import unittest

from validation.run_phase2 import manufacture


class PhaseTwoValidationHarnessTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary = tempfile.TemporaryDirectory()
        cls.output = Path(cls.temporary.name) / "phase2"
        cls.summary = manufacture(cls.output)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary.cleanup()

    def _json(self, name: str) -> dict:
        return json.loads((self.output / name).read_text(encoding="utf-8"))

    def test_full_pipeline_is_reproducible_and_context_isolated(self) -> None:
        reproducibility = self._json("reproducibility.json")
        benchmark = self._json("benchmark-results.json")
        self.assertTrue(reproducibility["deterministic_execution"])
        self.assertEqual([], reproducibility["differing_files"])
        self.assertTrue(reproducibility["context_and_reasoning_artifacts_identical"])
        self.assertTrue(benchmark["context_isolation"]["standing_identical_across_contexts"])
        self.assertGreaterEqual(benchmark["context_isolation"]["distinct_significance_orders"], 2)

    def test_adversarial_failures_are_preserved_not_hidden(self) -> None:
        adversarial = self._json("adversarial-results.json")
        cases = {item["case"]: item for item in adversarial["cases"]}
        self.assertEqual("PASS", cases["extremely_bright_irrelevant_foreground_object"]["status"])
        self.assertEqual("PASS", cases["dim_bridge_node"]["status"])
        self.assertEqual("PASS", cases["duplicated_entity"]["status"])
        self.assertEqual("PASS", cases["duplicated_edge"]["status"])
        self.assertEqual("PASS", cases["malformed_provenance"]["status"])
        self.assertEqual("PASS", cases["unsupported_relationship_type"]["status"])
        self.assertEqual("FAIL", cases["contradictory_relationship_assertions"]["status"])
        self.assertEqual("FAIL", cases["relationship_assertion_uncertainty"]["status"])
        self.assertEqual("FAIL", cases["evidence_absent_context_abstention"]["status"])
        self.assertEqual("FAIL", cases["standing_centrality_termination"]["status"])
        self.assertEqual("PASS", cases["many_weak_edges_overwhelm_one_strong_edge"]["status"])
        self.assertEqual("FAIL", cases["inferred_dark_region_excessive_certainty"]["status"])
        self.assertEqual("PASS", cases["image_centre_bias"]["status"])
        self.assertEqual("PASS", cases["graph_size_increase"]["status"])
        self.assertEqual("LIMITATION", cases["arbitrary_context_weighting"]["status"])
        self.assertEqual("insufficient_evidence", self.summary["bounded_hypothesis_outcome"])

    def test_explanations_explorer_and_manifest_are_complete(self) -> None:
        explanations = self._json("explanation-validation.json")
        self.assertTrue(explanations["all_contexts_resolvable"])
        self.assertTrue(all(item["trace_count"] == 11 for item in explanations["contexts"]))
        explorer = (self.output / "explorer.html").read_text(encoding="utf-8")
        for label in ("Source image", "Detection overlay", "Standing", "Significance", "Brightness rank"):
            self.assertIn(label, explorer)
        manifest = self._json("manifest.json")
        listed = {item["path"]: item["sha256"] for item in manifest["artifacts"]}
        actual = {
            path.relative_to(self.output).as_posix(): sha256(path.read_bytes()).hexdigest()
            for path in self.output.rglob("*")
            if path.is_file() and path != self.output / "manifest.json"
        }
        self.assertEqual(actual, listed)

    def test_output_overwrite_is_rejected(self) -> None:
        with self.assertRaisesRegex(FileExistsError, "refusing overwrite"):
            manufacture(self.output)


if __name__ == "__main__":
    unittest.main()
