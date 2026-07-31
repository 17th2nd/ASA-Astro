from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from asa_astro.evidence.pipeline import process_observation
from asa_astro.reasoning.cli import main as reasoning_main
from asa_astro.reasoning.engine import analyze, analyze_counterfactual, compute_standing
from asa_astro.reasoning.validation import validate_context
from tests.fixtures.generate_fixture import create_fixture


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


def context(context_id: str = "context-structural-0001", mode: str = "structural") -> dict:
    if mode == "structural":
        configured = json.loads((REPOSITORY_ROOT / "tests/fixtures/reasoning/structural-context.json").read_text(encoding="utf-8"))
        configured["context_id"] = context_id
        return configured
    if mode == "observational":
        eligible = ["observational", "spatial"]
        excluded = ["containment", "structural", "occlusion"]
        type_weights = {"observational": 1.0, "spatial": 0.25}
        components = {"standing": 0.10, "direct_relationships": 0.45, "propagated_relationships": 0.05, "information_value": 0.40}
        propagate = ["spatial"]
    elif mode == "star_formation":
        # No star-formation fact is asserted: this intentionally demonstrates an
        # evidence-limited context over the image-space types B actually supplies.
        eligible = ["structural", "containment", "observational"]
        excluded = ["spatial", "occlusion"]
        type_weights = {"structural": 0.8, "containment": 0.6, "observational": 0.2}
        components = {"standing": 0.20, "direct_relationships": 0.30, "propagated_relationships": 0.30, "information_value": 0.20}
        propagate = ["structural", "containment"]
    return {
        "schema_version": "0.1.0",
        "ontology_version": "ASTRO-ONTOLOGY-0001",
        "record_status": "active",
        "epistemic_classification": "externally_supplied",
        "context_id": context_id,
        "context_version": "0.1.0",
        "objective": f"Synthetic {mode} comparison; not a scientific conclusion",
        "authority": {"status": "provisional_non_canonical", "decision_register_dependencies": ["DR-0001", "DR-0008", "DR-0010", "DR-0012"]},
        "eligible_relationship_types": eligible,
        "excluded_relationship_types": excluded,
        "weights": {"component_weights": components, "relationship_type_weights": type_weights},
        "propagation_rules": {"enabled": True, "eligible_relationship_types": propagate, "maximum_depth": 3, "decay": 0.55},
        "uncertainty_tolerance": 0.20,
        "normalization_method": "max",
        "explanation_requirements": {"include_excluded_evidence": True, "include_warnings": True, "maximum_pathways": 8},
        "baseline_configuration": {"manual_class_priorities": {"internal_substructure": 1.0, "primary_extended_object": 0.8, "likely_foreground_point_source": 0.05}},
        "assumptions": ["All numeric weights are replaceable proof-of-concept hypotheses.", "Codex B relationships remain image-space assertions, not physical facts."],
    }


class ReasoningEngineTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary = tempfile.TemporaryDirectory()
        root = Path(cls.temporary.name)
        image = create_fixture(root / "synthetic-observation.ppm")
        bundle = root / "bundle"
        process_observation(image, bundle, metadata_path=REPOSITORY_ROOT / "tests/fixtures/synthetic_observation.metadata.json")
        cls.graph = json.loads((bundle / "graph.json").read_text(encoding="utf-8"))
        cls.provenance = json.loads((bundle / "provenance.json").read_text(encoding="utf-8"))

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary.cleanup()

    def _three_node_chain(self) -> tuple[dict, dict, list[str]]:
        """Build B-schema-valid A/B/C scenarios from versioned B fixture records."""
        graph, provenance = deepcopy(self.graph), deepcopy(self.provenance)
        source = next(node for node in graph["nodes"] if node["node_type"] == "observation_source")
        candidates = sorted((node for node in graph["nodes"] if node["node_type"] == "candidate_entity"), key=lambda item: item["id"])[:3]
        identifiers = [node["id"] for node in candidates]
        graph["nodes"] = [source] + candidates
        observation_edges = [edge for edge in graph["edges"] if edge["source"] == source["id"] and edge["target"] in identifiers]
        template = deepcopy(next(edge for edge in graph["edges"] if edge["source"] != source["id"] and edge["target"] != source["id"]))
        chain_edges = []
        for index, (left, right) in enumerate(zip(identifiers, identifiers[1:]), 1):
            edge = deepcopy(template)
            edge["id"] = f"edge-synthetic-chain-000{index}"
            edge["edge_type"] = "structural_image_association"
            edge["source"], edge["target"] = left, right
            assertion = edge["assertion"]
            assertion["id"] = f"assertion-synthetic-chain-000{index}"
            assertion["source_node_id"], assertion["target_node_id"] = left, right
            assertion["directionality"] = "symmetric"
            assertion["relationship_type"] = "structural"
            assertion["relationship_subtype"] = "shared_structural_region"
            assertion["relationship_classification"] = "image_space_derived"
            assertion["status"] = "derived"
            assertion["relationship_strength"]["value"] = 0.9
            assertion["confidence"]["value"] = 0.9
            chain_edges.append(edge)
        graph["edges"] = observation_edges + chain_edges
        detection_by_id = {item["id"]: item for item in provenance["detections"]}
        for evidence in provenance["evidence_records"]:
            evidence["record_status"] = "admissible"
            evidence["uncertainty"]["status"] = "bounded"
            evidence["uncertainty"]["confidence"] = 0.9
        for node, brightness in zip(candidates, (255, 40, 100)):
            node["payload"]["confidence"]["value"] = 0.9
            node["payload"]["uncertainty"]["status"] = "bounded"
            node["payload"]["uncertainty"]["confidence"] = 0.9
            detection = detection_by_id[node["payload"]["detection_ids"][0]]
            detection["features"]["peak_intensity"]["value"] = brightness
        return graph, provenance, identifiers

    def test_determinism_and_trace_completeness(self) -> None:
        first = analyze(self.graph, self.provenance, context())
        second = analyze(self.graph, self.provenance, context())
        self.assertEqual(first, second)
        required = {"context", "final_score", "standing_contribution", "direct_relationship_contributions", "propagated_contributions", "confidence_adjustments", "uncertainty_penalties", "excluded_evidence", "warnings", "top_explanatory_pathways"}
        for trace in first["explanation_traces"]:
            self.assertTrue(required <= set(trace))
            self.assertLessEqual(max((path["depth"] for path in trace["propagated_contributions"]), default=0), 3)

    def test_standing_is_context_free_and_significance_is_context_sensitive(self) -> None:
        structural = analyze(self.graph, self.provenance, context())
        observational = analyze(self.graph, self.provenance, context("context-observational-0001", "observational"))
        star_formation = analyze(self.graph, self.provenance, context("context-star-formation-0001", "star_formation"))
        self.assertEqual(structural["standing_results"], observational["standing_results"])
        self.assertEqual(structural["standing_results"], star_formation["standing_results"])
        self.assertNotEqual(structural["ranked_results"], observational["ranked_results"])
        self.assertNotEqual(observational["ranked_results"], star_formation["ranked_results"])

    def test_brightness_is_a_comparator_not_significance(self) -> None:
        output = analyze(self.graph, self.provenance, context())
        significance_order = [item["subject_id"] for item in output["ranked_results"]]
        brightness_order = [item["subject_id"] for item in output["baselines"]["brightness"]]
        self.assertNotEqual(significance_order, brightness_order)
        brightest = brightness_order[0]
        self.assertNotEqual(1, significance_order.index(brightest) + 1)

    def test_dim_bridge_has_structural_standing_without_brightness_equivalence(self) -> None:
        graph, provenance, identifiers = self._three_node_chain()
        structural_context = context("context-bridge-standing-0001")
        structural_context["weights"]["component_weights"] = {"standing": 0.70, "direct_relationships": 0.10, "propagated_relationships": 0.15, "information_value": 0.05}
        output = analyze(graph, provenance, structural_context)
        bridge = identifiers[1]
        self.assertEqual(bridge, output["ranked_results"][0]["subject_id"])
        self.assertEqual(identifiers[0], output["baselines"]["brightness"][0]["subject_id"])
        standings = {item["subject_id"]: item for item in output["standing_results"]}
        self.assertGreater(standings[bridge]["component_contributions"]["betweenness"]["contribution"], 0)
        self.assertGreater(standings[bridge]["score"], standings[identifiers[0]]["score"])

    def test_uncertainty_and_weak_evidence_reduce_scores(self) -> None:
        baseline = analyze(self.graph, self.provenance, context())
        high_degree = baseline["baselines"]["degree"][0]["subject_id"]
        changed = analyze_counterfactual(self.graph, self.provenance, context(), {"kind": "drop_observational_confidence", "node_id": high_degree, "factor": 0.05})
        row = next(item for item in changed["comparison"] if item["subject_id"] == high_degree)
        self.assertLess(row["after_score"], row["before_score"])
        modified_graph = deepcopy(self.graph)
        node = next(item for item in modified_graph["nodes"] if item["id"] == high_degree)
        node["payload"]["uncertainty"]["status"] = "contested"
        node["payload"]["uncertainty"].pop("confidence", None)
        before = {item["subject_id"]: item["score"] for item in compute_standing(self.graph, self.provenance)}
        after = {item["subject_id"]: item["score"] for item in compute_standing(modified_graph, self.provenance)}
        self.assertLess(after[high_degree], before[high_degree])

    def test_low_confidence_proximity_cannot_dominate(self) -> None:
        graph = deepcopy(self.graph)
        edge = next(item for item in graph["edges"] if item["assertion"]["relationship_type"] == "spatial")
        edge["assertion"]["confidence"]["value"] = 0.001
        output = analyze(graph, self.provenance, context())
        traces = {item["subject_id"]: item for item in output["explanation_traces"]}
        contributions = [item["raw_contribution"] for trace in traces.values() for item in trace["direct_relationship_contributions"] if item["edge_id"] == edge["id"]]
        self.assertTrue(contributions)
        self.assertTrue(all(value < 0.001 for value in contributions))

    def test_counterfactuals_are_bounded_and_preserve_baseline(self) -> None:
        edge = self.graph["edges"][0]
        weakened = analyze_counterfactual(self.graph, self.provenance, context(), {"kind": "weaken_edge", "edge_id": edge["id"], "factor": 0.1})
        self.assertTrue(any(item["score_delta"] not in (None, 0) for item in weakened["comparison"]))
        node_id = weakened["baseline"]["ranked_results"][0]["subject_id"]
        removed = analyze_counterfactual(self.graph, self.provenance, context(), {"kind": "remove_node", "node_id": node_id})
        row = next(item for item in removed["comparison"] if item["subject_id"] == node_id)
        self.assertIsNone(row["after_score"])
        self.assertIn(node_id, {item["subject_id"] for item in weakened["baseline"]["ranked_results"]})

    def test_provenance_is_retained_and_intrinsic_scores_rejected(self) -> None:
        output = analyze(self.graph, self.provenance, context())
        available = {item["id"] for item in self.provenance["evidence_records"]} | {item["id"] for item in self.provenance["provenance_records"]}
        for result in output["standing_results"] + output["significance_results"]:
            self.assertTrue(set(result["provenance_refs"]) <= available)
        malformed = deepcopy(self.graph)
        candidate = next(node for node in malformed["nodes"] if node["node_type"] == "candidate_entity")
        candidate["payload"]["significance"] = 1.0
        with self.assertRaisesRegex(ValueError, "Significance cannot be intrinsic|Additional properties|not valid"):
            analyze(malformed, self.provenance, context())

    def test_context_rejects_unbounded_or_non_taxonomy_configuration(self) -> None:
        malformed = context()
        malformed["propagation_rules"]["maximum_depth"] = 9
        with self.assertRaises(ValueError):
            validate_context(malformed)
        malformed = context()
        malformed["eligible_relationship_types"].append("invented_physical_relation")
        with self.assertRaises(ValueError):
            validate_context(malformed)

    def test_cli_emits_reproducible_versioned_bundle_and_refuses_overwrite(self) -> None:
        root = Path(self.temporary.name)
        invocation = root / "cli-inputs"
        invocation.mkdir(exist_ok=True)
        graph_path, provenance_path, context_path = invocation / "graph.json", invocation / "provenance.json", invocation / "context.json"
        graph_path.write_text(json.dumps(self.graph), encoding="utf-8")
        provenance_path.write_text(json.dumps(self.provenance), encoding="utf-8")
        context_path.write_text(json.dumps(context()), encoding="utf-8")
        output = root / "reasoning-output"
        self.assertEqual(0, reasoning_main(["--graph", str(graph_path), "--provenance", str(provenance_path), "--context", str(context_path), "--output", str(output)]))
        self.assertTrue({"manifest.json", "standing-results.json", "significance-results.json", "explanation-traces.json", "baselines.json"} <= {path.name for path in output.iterdir()})
        with self.assertRaisesRegex(FileExistsError, "refusing overwrite"):
            reasoning_main(["--graph", str(graph_path), "--provenance", str(provenance_path), "--context", str(context_path), "--output", str(output)])


if __name__ == "__main__":
    unittest.main()
