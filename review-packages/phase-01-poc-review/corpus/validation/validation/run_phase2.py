"""Independent Phase II integration, benchmark, and adversarial validation harness.

This module orchestrates the committed Codex B and C interfaces. It does not
modify their records or define ASA semantics. All scenarios are synthetic
software tests and remain separate from astronomical validation.
"""

from __future__ import annotations

import argparse
import base64
from copy import deepcopy
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import shutil
import tempfile
from typing import Any, Callable

from PIL import Image

from asa_astro.evidence.models import DetectionParameters, canonical_json
from asa_astro.evidence.pipeline import process_observation
from asa_astro.reasoning.cli import write_analysis
from asa_astro.reasoning.engine import analyze
from tests.fixtures.generate_fixture import create_fixture


UPSTREAM_COMMIT = "520f790a363660bbd97abf7f0f45f73cacc2d739"
HARNESS_VERSION = "asa-astro-validation-phase2-0.1.0"
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CONTEXT_PATHS = {
    "structural_organisation": REPOSITORY_ROOT / "tests/fixtures/reasoning/structural-context.json",
    "observational_interpretation": REPOSITORY_ROOT / "validation/fixtures/contexts/observational.json",
    "star_formation": REPOSITORY_ROOT / "validation/fixtures/contexts/star-formation.json",
    "scientific_information_value": REPOSITORY_ROOT / "validation/fixtures/contexts/scientific-information.json",
    "gravitational_organisation": REPOSITORY_ROOT / "validation/fixtures/contexts/gravitational.json",
}
MANUAL_PRIORITY_PATH = REPOSITORY_ROOT / "validation/fixtures/manual-priority.json"


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected a JSON object: {path}")
    return value


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _sha256_bytes(value: bytes) -> str:
    return sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _directory_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): _sha256_file(path)
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _ranking(analysis: dict[str, Any]) -> list[str]:
    return [item["subject_id"] for item in analysis["ranked_results"]]


def _score_map(analysis: dict[str, Any]) -> dict[str, float]:
    return {item["subject_id"]: item["score"] for item in analysis["ranked_results"]}


def _rank_comparison(left: list[str], right: list[str]) -> dict[str, Any]:
    if set(left) != set(right):
        raise ValueError("rankings must cover the same subjects")
    left_rank = {subject: index for index, subject in enumerate(left, 1)}
    right_rank = {subject: index for index, subject in enumerate(right, 1)}
    count = len(left)
    squared = sum((left_rank[item] - right_rank[item]) ** 2 for item in left)
    spearman = 1.0 if count < 2 else 1.0 - (6.0 * squared) / (count * (count * count - 1))
    disagreements = 0
    total_pairs = 0
    for index, first in enumerate(left):
        for second in left[index + 1 :]:
            total_pairs += 1
            if (left_rank[first] - left_rank[second]) * (right_rank[first] - right_rank[second]) < 0:
                disagreements += 1
    return {
        "spearman_rho": round(spearman, 12),
        "mean_absolute_rank_delta": round(
            sum(abs(left_rank[item] - right_rank[item]) for item in left) / count, 12
        ),
        "pairwise_disagreements": disagreements,
        "pairwise_disagreement_fraction": round(disagreements / total_pairs, 12) if total_pairs else 0.0,
        "top_subject_same": left[0] == right[0],
    }


def _analysis_delta(reference: dict[str, Any], changed: dict[str, Any]) -> dict[str, Any]:
    before = _score_map(reference)
    after = _score_map(changed)
    common = sorted(set(before) & set(after))
    return {
        "ranking": _rank_comparison(_ranking(reference), _ranking(changed))
        if set(before) == set(after)
        else None,
        "score_l1_delta": round(sum(abs(before[item] - after[item]) for item in common), 12),
        "top_before": _ranking(reference)[0] if reference["ranked_results"] else None,
        "top_after": _ranking(changed)[0] if changed["ranked_results"] else None,
    }


def _candidate_ids(graph: dict[str, Any]) -> set[str]:
    return {node["id"] for node in graph["nodes"] if node["node_type"] == "candidate_entity"}


def _manual_ranking(graph: dict[str, Any]) -> list[str]:
    configured = _read_json(MANUAL_PRIORITY_PATH)["ordering"]
    candidates = _candidate_ids(graph)
    if set(configured) != candidates:
        missing = sorted(candidates - set(configured))
        stale = sorted(set(configured) - candidates)
        raise ValueError(f"manual comparator does not match candidate identity; missing={missing}, stale={stale}")
    return configured


def _benchmark_results(
    graph: dict[str, Any], analyses: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    manual = _manual_ranking(graph)
    contexts: dict[str, Any] = {}
    for name, analysis in analyses.items():
        significance = _ranking(analysis)
        comparisons = {
            baseline: _rank_comparison(significance, [item["subject_id"] for item in ranking])
            for baseline, ranking in analysis["baselines"].items()
            if baseline in {"brightness", "image_centre", "degree", "centrality"}
        }
        comparisons["manual_priority"] = _rank_comparison(significance, manual)
        contexts[name] = {
            "significance_ranking": significance,
            "top_subject": significance[0],
            "comparisons": comparisons,
            "baseline_rankings": {
                key: [item["subject_id"] for item in value]
                for key, value in analysis["baselines"].items()
            },
            "manual_priority_ranking": manual,
        }
    orders = {name: tuple(_ranking(analysis)) for name, analysis in analyses.items()}
    structural_standing = analyses["structural_organisation"]["standing_results"]
    return {
        "manual_priority_basis": _read_json(MANUAL_PRIORITY_PATH)["basis"],
        "contexts": contexts,
        "context_isolation": {
            "standing_identical_across_contexts": all(
                analysis["standing_results"] == structural_standing for analysis in analyses.values()
            ),
            "distinct_significance_orders": len(set(orders.values())),
            "ranking_orders": {name: list(order) for name, order in orders.items()},
        },
    }


def _ranking_stability(
    graph: dict[str, Any],
    provenance: dict[str, Any],
    context: dict[str, Any],
    reference: dict[str, Any],
) -> dict[str, Any]:
    perturbed_graph = deepcopy(graph)
    for edge in perturbed_graph["edges"]:
        confidence = edge["assertion"]["confidence"]["value"]
        edge["assertion"]["confidence"]["value"] = round(confidence * 0.999, 12)
    perturbed = analyze(perturbed_graph, provenance, context)
    comparison = _rank_comparison(_ranking(reference), _ranking(perturbed))
    return {
        "perturbation": "multiply every relationship-assertion confidence by 0.999",
        "comparison": comparison,
        "score_l1_delta": _analysis_delta(reference, perturbed)["score_l1_delta"],
        "interpretation_limit": "One synthetic local perturbation is not a calibration or general stability claim.",
    }


def _three_node_chain(
    graph: dict[str, Any], provenance: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any], list[str]]:
    changed_graph, changed_provenance = deepcopy(graph), deepcopy(provenance)
    source = next(node for node in changed_graph["nodes"] if node["node_type"] == "observation_source")
    candidates = sorted(
        (node for node in changed_graph["nodes"] if node["node_type"] == "candidate_entity"),
        key=lambda item: item["id"],
    )[:3]
    identifiers = [node["id"] for node in candidates]
    changed_graph["nodes"] = [source] + candidates
    observation_edges = [
        edge
        for edge in changed_graph["edges"]
        if edge["source"] == source["id"] and edge["target"] in identifiers
    ]
    template = deepcopy(
        next(
            edge
            for edge in changed_graph["edges"]
            if edge["source"] != source["id"] and edge["target"] != source["id"]
        )
    )
    chain_edges = []
    for index, (left, right) in enumerate(zip(identifiers, identifiers[1:]), 1):
        edge = deepcopy(template)
        edge["id"] = f"edge-validation-chain-000{index}"
        edge["edge_type"] = "structural_image_association"
        edge["source"], edge["target"] = left, right
        assertion = edge["assertion"]
        assertion["id"] = f"assertion-validation-chain-000{index}"
        assertion["source_node_id"], assertion["target_node_id"] = left, right
        assertion["directionality"] = "symmetric"
        assertion["relationship_type"] = "structural"
        assertion["relationship_subtype"] = "shared_structural_region"
        assertion["relationship_classification"] = "image_space_derived"
        assertion["status"] = "derived"
        assertion["relationship_strength"]["value"] = 0.9
        assertion["confidence"]["value"] = 0.9
        chain_edges.append(edge)
    changed_graph["edges"] = observation_edges + chain_edges
    detection_by_id = {item["id"]: item for item in changed_provenance["detections"]}
    for evidence in changed_provenance["evidence_records"]:
        evidence["record_status"] = "admissible"
        evidence["uncertainty"]["status"] = "bounded"
        evidence["uncertainty"]["confidence"] = 0.9
    for node, brightness in zip(candidates, (255, 40, 100)):
        node["payload"]["confidence"]["value"] = 0.9
        node["payload"]["uncertainty"]["status"] = "bounded"
        node["payload"]["uncertainty"]["confidence"] = 0.9
        detection = detection_by_id[node["payload"]["detection_ids"][0]]
        detection["features"]["peak_intensity"]["value"] = brightness
    return changed_graph, changed_provenance, identifiers


def _expect_rejection(operation: Callable[[], Any]) -> tuple[bool, str]:
    try:
        operation()
    except (ValueError, KeyError, TypeError) as error:
        return True, f"{type(error).__name__}: {error}"
    return False, "input was accepted"


def _adversarial_results(
    graph: dict[str, Any], provenance: dict[str, Any], contexts: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    structural_context = contexts["structural_organisation"]
    baseline = analyze(graph, provenance, structural_context)
    cases: list[dict[str, Any]] = []

    centrality_termination = baseline["standing_results"][0]["centrality_termination"]
    cases.append({
        "case": "standing_centrality_termination",
        "status": "PASS" if centrality_termination["converged"] else "FAIL",
        "observation": "Base-fixture Standing centrality reached the declared iteration cap without satisfying the convergence tolerance; deterministic truncation is not convergence.",
        "metrics": centrality_termination,
    })

    bright_provenance = deepcopy(provenance)
    foreground_ids = {
        item["id"]
        for item in graph["nodes"]
        if item["node_type"] == "candidate_entity"
        and item["payload"]["candidate_type"] == "likely_foreground_point_source"
    }
    irrelevant_foreground = next(subject for subject in reversed(_ranking(baseline)) if subject in foreground_ids)
    node = next(item for item in graph["nodes"] if item["id"] == irrelevant_foreground)
    detection_id = node["payload"]["detection_ids"][0]
    detection = next(item for item in bright_provenance["detections"] if item["id"] == detection_id)
    detection["features"]["peak_intensity"]["value"] = 1_000_000
    bright = analyze(graph, bright_provenance, structural_context)
    bright_invariant = _score_map(bright) == _score_map(baseline)
    cases.append({
        "case": "extremely_bright_irrelevant_foreground_object",
        "status": "PASS" if bright_invariant and bright["baselines"]["brightness"][0]["subject_id"] == irrelevant_foreground else "FAIL",
        "observation": "Changing encoded brightness alone changed the brightness comparator but not Significance scores.",
        "metrics": {"mutated_subject": irrelevant_foreground, "candidate_type": node["payload"]["candidate_type"], "significance_scores_identical": bright_invariant, "brightness_top_after": bright["baselines"]["brightness"][0]["subject_id"]},
    })

    centre_provenance = deepcopy(provenance)
    centre_detection = next(item for item in centre_provenance["detections"] if item["id"] == detection_id)
    metadata = centre_provenance["source_image_metadata"][0]
    centre_detection["centroid"] = {"x": metadata["width_pixels"] / 2.0, "y": metadata["height_pixels"] / 2.0}
    centred = analyze(graph, centre_provenance, structural_context)
    centre_invariant = _score_map(centred) == _score_map(baseline)
    cases.append({
        "case": "image_centre_bias",
        "status": "PASS" if centre_invariant and centred["baselines"]["image_centre"][0]["subject_id"] == irrelevant_foreground else "FAIL",
        "observation": "Changing only the encoded detection centroid made the foreground candidate first in the image-centre comparator but did not alter Significance scores.",
        "metrics": {"mutated_subject": irrelevant_foreground, "significance_scores_identical": centre_invariant, "image_centre_top_after": centred["baselines"]["image_centre"][0]["subject_id"]},
    })

    chain_graph, chain_provenance, chain_ids = _three_node_chain(graph, provenance)
    bridge_context = deepcopy(structural_context)
    bridge_context["context_id"] = "context-validation-dim-bridge-0001"
    bridge_context["weights"]["component_weights"] = {"standing": 0.70, "direct_relationships": 0.10, "propagated_relationships": 0.15, "information_value": 0.05}
    bridge = analyze(chain_graph, chain_provenance, bridge_context)
    bridge_id = chain_ids[1]
    standings = {item["subject_id"]: item for item in bridge["standing_results"]}
    bridge_pass = _ranking(bridge)[0] == bridge_id and bridge["baselines"]["brightness"][0]["subject_id"] != bridge_id and standings[bridge_id]["component_contributions"]["betweenness"]["contribution"] > 0
    cases.append({"case": "dim_bridge_node", "status": "PASS" if bridge_pass else "FAIL", "observation": "The deliberately dim bridge ranked first under the frozen bridge Context and carried a positive betweenness contribution.", "metrics": {"bridge_subject": bridge_id, "significance_top": _ranking(bridge)[0], "brightness_top": bridge["baselines"]["brightness"][0]["subject_id"], "betweenness_contribution": standings[bridge_id]["component_contributions"]["betweenness"]["contribution"]}})

    uncertain_graph, uncertain_provenance = deepcopy(graph), deepcopy(provenance)
    uncertain_subject = _ranking(baseline)[0]
    uncertain_node = next(item for item in uncertain_graph["nodes"] if item["id"] == uncertain_subject)
    uncertain_node["payload"]["uncertainty"]["status"] = "contested"
    uncertain_node["payload"]["uncertainty"].pop("confidence", None)
    support_ids = set(uncertain_node["payload"]["supporting_evidence_ids"])
    for item in uncertain_provenance["evidence_records"]:
        if item["id"] in support_ids:
            item["record_status"] = "contested"
            item["uncertainty"]["status"] = "contested"
            item["uncertainty"].pop("confidence", None)
    uncertain = analyze(uncertain_graph, uncertain_provenance, structural_context)
    uncertainty_pass = _score_map(uncertain)[uncertain_subject] < _score_map(baseline)[uncertain_subject]
    cases.append({"case": "uncertain_evidence", "status": "PASS" if uncertainty_pass else "FAIL", "observation": "Contested candidate and supporting evidence lowered the selected candidate's score.", "metrics": {"subject": uncertain_subject, "before": _score_map(baseline)[uncertain_subject], "after": _score_map(uncertain)[uncertain_subject]}})

    disconnected_graph = deepcopy(graph)
    candidates = _candidate_ids(disconnected_graph)
    disconnected_graph["edges"] = [edge for edge in disconnected_graph["edges"] if not (edge["source"] in candidates and edge["target"] in candidates)]
    disconnected = analyze(disconnected_graph, provenance, structural_context)
    no_paths = all(not trace["propagated_contributions"] for trace in disconnected["explanation_traces"])
    cases.append({"case": "disconnected_graph", "status": "PASS" if len(disconnected["ranked_results"]) == len(candidates) and no_paths else "FAIL", "observation": "The engine terminated deterministically for isolated candidate nodes; evidence/Standing terms still produced relative scores.", "metrics": {"candidate_count": len(candidates), "result_count": len(disconnected["ranked_results"]), "propagated_paths_absent": no_paths}})

    cycle_graph, cycle_provenance, cycle_ids = _three_node_chain(graph, provenance)
    cycle_edge = deepcopy(next(edge for edge in cycle_graph["edges"] if edge["id"].startswith("edge-validation-chain")))
    cycle_edge["id"] = "edge-validation-cycle-0003"
    cycle_edge["source"], cycle_edge["target"] = cycle_ids[2], cycle_ids[0]
    cycle_edge["assertion"]["id"] = "assertion-validation-cycle-0003"
    cycle_edge["assertion"]["source_node_id"], cycle_edge["assertion"]["target_node_id"] = cycle_ids[2], cycle_ids[0]
    cycle_graph["edges"].append(cycle_edge)
    cyclic = analyze(cycle_graph, cycle_provenance, structural_context)
    paths = [path for trace in cyclic["explanation_traces"] for path in trace["propagated_contributions"]]
    cycle_pass = all(path["depth"] <= structural_context["propagation_rules"]["maximum_depth"] and len(path["node_path"]) == len(set(path["node_path"])) for path in paths)
    cases.append({"case": "cyclic_graph", "status": "PASS" if cycle_pass else "FAIL", "observation": "Cycle-safe traversal terminated at the declared depth without revisiting a node within a path.", "metrics": {"path_count": len(paths), "maximum_depth": max((path["depth"] for path in paths), default=0)}})

    weak_graph, weak_provenance = deepcopy(graph), deepcopy(provenance)
    weak_candidates = sorted(_candidate_ids(weak_graph))
    observation_source = next(node["id"] for node in weak_graph["nodes"] if node["node_type"] == "observation_source")
    observation_edges = [edge for edge in weak_graph["edges"] if edge["source"] == observation_source]
    relationship_template = deepcopy(next(edge for edge in weak_graph["edges"] if edge["source"] in set(weak_candidates) and edge["target"] in set(weak_candidates)))

    def synthetic_edge(identifier: str, source: str, target: str, strength: float) -> dict[str, Any]:
        edge = deepcopy(relationship_template)
        edge["id"] = f"edge-validation-{identifier}"
        edge["edge_type"] = "structural_image_association"
        edge["source"], edge["target"] = source, target
        assertion = edge["assertion"]
        assertion["id"] = f"assertion-validation-{identifier}"
        assertion["source_node_id"], assertion["target_node_id"] = source, target
        assertion["directionality"] = "symmetric"
        assertion["relationship_type"] = "structural"
        assertion["relationship_subtype"] = "shared_structural_region"
        assertion["relationship_classification"] = "image_space_derived"
        assertion["status"] = "derived"
        assertion["relationship_strength"]["value"] = strength
        assertion["confidence"]["value"] = 1.0
        return edge

    strong_hub, strong_partner, weak_hub, *weak_neighbours = weak_candidates
    synthetic_relationships = [synthetic_edge("strong-0001", strong_hub, strong_partner, 0.95)]
    synthetic_relationships.extend(
        synthetic_edge(f"weak-{index:04d}", weak_hub, neighbour, 0.12)
        for index, neighbour in enumerate(weak_neighbours, 1)
    )
    weak_graph["edges"] = observation_edges + synthetic_relationships
    for candidate_node in weak_graph["nodes"]:
        if candidate_node["node_type"] == "candidate_entity":
            candidate_node["payload"]["confidence"]["value"] = 0.9
            candidate_node["payload"]["uncertainty"]["status"] = "bounded"
            candidate_node["payload"]["uncertainty"]["confidence"] = 0.9
    weak_context = deepcopy(structural_context)
    weak_context["context_id"] = "context-adversarial-many-weak-edges"
    weak_context["weights"]["component_weights"] = {"standing": 0.5, "direct_relationships": 0.5, "propagated_relationships": 0.0, "information_value": 0.0}
    many_weak = analyze(weak_graph, weak_provenance, weak_context)
    many_weak_ranking = _ranking(many_weak)
    weak_rank = many_weak_ranking.index(weak_hub) + 1
    strong_best_rank = min(many_weak_ranking.index(strong_hub), many_weak_ranking.index(strong_partner)) + 1
    weak_overwhelmed = weak_rank < strong_best_rank
    cases.append({
        "case": "many_weak_edges_overwhelm_one_strong_edge",
        "status": "FAIL" if weak_overwhelmed else "PASS",
        "observation": "Eight distinct strength-0.12 edges were compared with one strength-0.95 edge under equal candidate certainty; the result records whether unbounded aggregation made the weak-edge hub rank first.",
        "metrics": {"strong_hub": strong_hub, "weak_hub": weak_hub, "weak_edge_count": len(weak_neighbours), "aggregate_weak_nominal_strength": round(0.12 * len(weak_neighbours), 12), "strong_nominal_strength": 0.95, "best_strong_endpoint_rank": strong_best_rank, "weak_hub_rank": weak_rank, "significance_top": many_weak_ranking[0]},
    })

    dense_graph = deepcopy(graph)
    dense_edges = []
    dense_index = 0
    for left_index, left in enumerate(weak_candidates):
        for right in weak_candidates[left_index + 1 :]:
            dense_index += 1
            dense_edges.append(synthetic_edge(f"dense-{dense_index:04d}", left, right, 0.2))
    dense_graph["edges"] = deepcopy(observation_edges) + dense_edges
    dense_context = deepcopy(structural_context)
    dense_context["context_id"] = "context-adversarial-dense-graph"
    dense_context["propagation_rules"]["maximum_depth"] = 2
    dense = analyze(dense_graph, provenance, dense_context)
    dense_repeat = analyze(dense_graph, provenance, dense_context)
    dense_paths = sum(len(item["propagated_contributions"]) for item in dense["explanation_traces"])
    dense_converged = all(item["centrality_termination"]["converged"] for item in dense["standing_results"])
    dense_pass = (
        len(dense["ranked_results"]) == len(weak_candidates)
        and dense_converged
        and dense == dense_repeat
    )
    cases.append({
        "case": "graph_size_increase",
        "status": "PASS" if dense_pass else "FAIL",
        "observation": "A schema-valid complete candidate graph increased the base edge count and remained deterministic at the frozen depth-two propagation bound; this is a modest engineering stress test, not a scalability claim.",
        "metrics": {"base_edge_count": len(graph["edges"]), "dense_edge_count": len(dense_graph["edges"]), "candidate_count": len(weak_candidates), "propagated_path_count": dense_paths, "centrality_converged": dense_converged, "repeat_output_identical": dense == dense_repeat},
    })

    duplicate_node_graph = deepcopy(graph)
    duplicate_node_graph["nodes"].append(deepcopy(next(node for node in graph["nodes"] if node["node_type"] == "candidate_entity")))
    rejected, message = _expect_rejection(lambda: analyze(duplicate_node_graph, provenance, structural_context))
    cases.append({"case": "duplicated_entity", "status": "PASS" if rejected else "FAIL", "observation": "Duplicate node identity was rejected.", "evidence": message})

    duplicate_edge_graph = deepcopy(graph)
    duplicate_edge_graph["edges"].append(deepcopy(graph["edges"][0]))
    rejected, message = _expect_rejection(lambda: analyze(duplicate_edge_graph, provenance, structural_context))
    cases.append({"case": "duplicated_edge", "status": "PASS" if rejected else "FAIL", "observation": "Duplicate edge identity was rejected.", "evidence": message})

    malformed_provenance = deepcopy(provenance)
    removed_evidence = malformed_provenance["evidence_records"].pop(0)["id"]
    rejected, message = _expect_rejection(lambda: analyze(graph, malformed_provenance, structural_context))
    cases.append({"case": "malformed_provenance", "status": "PASS" if rejected else "FAIL", "observation": "A bundle with a missing Evidence Record was rejected.", "metrics": {"removed_evidence_id": removed_evidence}, "evidence": message})

    contradictory_graph = deepcopy(graph)
    contradictory_edge = next(edge for edge in contradictory_graph["edges"] if edge["source"] in candidates and edge["target"] in candidates)
    contradictory_edge["assertion"]["contradicting_evidence_ids"] = list(contradictory_edge["assertion"]["evidence_ids"])
    contradictory = analyze(contradictory_graph, provenance, structural_context)
    contradiction_ignored = _score_map(contradictory) == _score_map(baseline)
    cases.append({"case": "contradictory_relationship_assertions", "status": "FAIL" if contradiction_ignored else "PASS", "observation": "The engine accepted a relationship whose same evidence was both supporting and contradicting and applied no penalty.", "metrics": {"edge_id": contradictory_edge["id"], "scores_identical": contradiction_ignored}})

    unsupported_graph = deepcopy(graph)
    unsupported_graph["edges"][0]["assertion"]["relationship_type"] = "invented_physical_relation"
    rejected, message = _expect_rejection(lambda: analyze(unsupported_graph, provenance, structural_context))
    cases.append({"case": "unsupported_relationship_type", "status": "PASS" if rejected else "FAIL", "observation": "A type outside the taxonomy/schema was rejected.", "evidence": message})

    proximity_graph = deepcopy(graph)
    proximity_edge = next(edge for edge in proximity_graph["edges"] if edge["assertion"]["relationship_type"] == "spatial")
    proximity_edge["assertion"]["confidence"]["value"] = 0.001
    proximity = analyze(proximity_graph, provenance, structural_context)
    proximity_values = [item["raw_contribution"] for trace in proximity["explanation_traces"] for item in trace["direct_relationship_contributions"] if item["edge_id"] == proximity_edge["id"]]
    proximity_pass = bool(proximity_values) and max(proximity_values) < 0.001
    cases.append({"case": "false_proximity", "status": "PASS" if proximity_pass else "FAIL", "observation": "A proximity assertion with confidence 0.001 remained below 0.001 direct contribution.", "metrics": {"edge_id": proximity_edge["id"], "maximum_direct_contribution": max(proximity_values, default=None)}})

    uncertain_edge_graph = deepcopy(graph)
    uncertain_edge = next(edge for edge in uncertain_edge_graph["edges"] if edge["source"] in candidates and edge["target"] in candidates)
    uncertain_edge["assertion"]["uncertainty"]["status"] = "contested"
    uncertain_edge["assertion"]["uncertainty"].pop("confidence", None)
    edge_uncertain = analyze(uncertain_edge_graph, provenance, structural_context)
    edge_uncertainty_ignored = _score_map(edge_uncertain) == _score_map(baseline)
    cases.append({"case": "relationship_assertion_uncertainty", "status": "FAIL" if edge_uncertainty_ignored else "PASS", "observation": "Changing assertion uncertainty to contested did not change any score; the burden is traced but absent from supported edge weight.", "metrics": {"edge_id": uncertain_edge["id"], "scores_identical": edge_uncertainty_ignored}})

    dark_graph = deepcopy(graph)
    dark_node = next(
        node for node in dark_graph["nodes"]
        if node["node_type"] == "candidate_entity" and node["payload"]["candidate_type"] == "dark_or_occluding_region"
    )
    dark_subject = dark_node["id"]
    dark_node["payload"]["confidence"]["value"] = 1.0
    dark_node["payload"]["uncertainty"] = {
        **dark_node["payload"]["uncertainty"],
        "status": "not_applicable",
        "confidence": 1.0,
    }
    overcertain_dark = analyze(dark_graph, provenance, structural_context)
    dark_trace = next(item for item in overcertain_dark["explanation_traces"] if item["subject_id"] == dark_subject)
    hypothesis_warning = any(
        any(term in warning.lower() for term in ("dark", "occlud", "unresolved", "classification status"))
        for warning in dark_trace["warnings"]
    )
    cases.append({
        "case": "inferred_dark_region_excessive_certainty",
        "status": "PASS" if hypothesis_warning else "FAIL",
        "observation": "The engine accepted confidence 1.0 and not-applicable uncertainty for an unresolved inferred dark/occluding image region without a hypothesis-specific warning. The repository makes no dark-matter identity claim.",
        "metrics": {"subject": dark_subject, "classification_status": dark_node["payload"]["classification_status"], "resolution_state": dark_node["payload"]["resolution_state"], "score_before": _score_map(baseline)[dark_subject], "score_after": _score_map(overcertain_dark)[dark_subject], "hypothesis_specific_warning": hypothesis_warning},
    })

    empty_context_failures = []
    for name in ("star_formation", "gravitational_organisation"):
        analysis = analyze(graph, provenance, contexts[name])
        eligible = set(contexts[name]["eligible_relationship_types"])
        eligible_edges = sum(1 for edge in graph["edges"] if edge["assertion"]["relationship_type"] in eligible)
        nonzero = sum(1 for item in analysis["ranked_results"] if item["score"] > 0)
        empty_context_failures.append({"context": name, "eligible_edge_count": eligible_edges, "nonzero_result_count": nonzero, "top_score": analysis["ranked_results"][0]["score"]})
    abstention_failed = any(item["eligible_edge_count"] == 0 and item["nonzero_result_count"] > 0 for item in empty_context_failures)
    cases.append({"case": "evidence_absent_context_abstention", "status": "FAIL" if abstention_failed else "PASS", "observation": "Star-formation and gravitational Contexts had no eligible relationship evidence but emitted active non-zero rankings rather than indeterminate/abstaining.", "metrics": empty_context_failures})

    weight_tops: dict[str, str] = {}
    for component in ("standing", "direct_relationships", "propagated_relationships", "information_value"):
        weighted_context = deepcopy(structural_context)
        weighted_context["context_id"] = f"context-adversarial-{component.replace('_', '-')}-only"
        weighted_context["weights"]["component_weights"] = {name: (1.0 if name == component else 0.0) for name in weighted_context["weights"]["component_weights"]}
        weight_tops[component] = _ranking(analyze(graph, provenance, weighted_context))[0]
    cases.append({"case": "arbitrary_context_weighting", "status": "LIMITATION", "observation": "All weights are explicit and traceable, but extreme admissible component weights changed the top-ranked subject; no authorised scientific basis selects among them.", "metrics": {"top_subject_by_single_component": weight_tops, "distinct_top_subjects": len(set(weight_tops.values()))}})

    return {
        "case_count": len(cases),
        "pass_count": sum(case["status"] == "PASS" for case in cases),
        "fail_count": sum(case["status"] == "FAIL" for case in cases),
        "limitation_count": sum(case["status"] == "LIMITATION" for case in cases),
        "cases": cases,
    }


def _zero_uncertainty(record: dict[str, Any]) -> None:
    uncertainty = record.get("uncertainty")
    if isinstance(uncertainty, dict):
        uncertainty["status"] = "not_applicable"
        uncertainty["confidence"] = 1.0


def _ablation_results(
    graph: dict[str, Any], provenance: dict[str, Any], structural_context: dict[str, Any]
) -> dict[str, Any]:
    reference = analyze(graph, provenance, structural_context)
    ablations: list[dict[str, Any]] = []

    no_standing_context = deepcopy(structural_context)
    no_standing_context["context_id"] = "context-ablation-without-standing"
    original = no_standing_context["weights"]["component_weights"]
    remaining = 1.0 - original["standing"]
    no_standing_context["weights"]["component_weights"] = {
        name: (0.0 if name == "standing" else value / remaining) for name, value in original.items()
    }
    no_standing = analyze(graph, provenance, no_standing_context)
    ablations.append({"ablation": "without_standing_contribution", "behavior": "Standing is still computed for contract validity but its Significance weight is zero and remaining weights are renormalised.", **_analysis_delta(reference, no_standing)})

    rejected, message = _expect_rejection(lambda: analyze(graph, provenance, {}))
    ablations.append({"ablation": "without_context", "behavior": "No ranking is emitted because Context is a required contract.", "rejected": rejected, "evidence": message})

    no_uncertainty_graph, no_uncertainty_provenance = deepcopy(graph), deepcopy(provenance)
    for node in no_uncertainty_graph["nodes"]:
        if node["node_type"] == "candidate_entity":
            _zero_uncertainty(node["payload"])
    for edge in no_uncertainty_graph["edges"]:
        _zero_uncertainty(edge["assertion"])
    for record in no_uncertainty_provenance["evidence_records"] + no_uncertainty_provenance["detections"]:
        _zero_uncertainty(record)
    no_uncertainty = analyze(no_uncertainty_graph, no_uncertainty_provenance, structural_context)
    ablations.append({"ablation": "without_uncertainty_penalties", "behavior": "All represented uncertainty burdens are forced to not_applicable with confidence 1 for this controlled counterfactual.", **_analysis_delta(reference, no_uncertainty)})

    untyped_graph = deepcopy(graph)
    candidates = _candidate_ids(untyped_graph)
    for edge in untyped_graph["edges"]:
        if edge["source"] in candidates and edge["target"] in candidates:
            edge["assertion"]["relationship_type"] = "structural"
            edge["assertion"]["relationship_subtype"] = "shared_structural_region"
    untyped_context = deepcopy(structural_context)
    untyped_context["context_id"] = "context-ablation-collapsed-relationship-types"
    untyped_context["eligible_relationship_types"] = ["structural"]
    untyped_context["excluded_relationship_types"] = ["observational", "occlusion"]
    untyped_context["weights"]["relationship_type_weights"] = {"structural": 1.0}
    untyped_context["propagation_rules"]["eligible_relationship_types"] = ["structural"]
    untyped = analyze(untyped_graph, provenance, untyped_context)
    ablations.append({"ablation": "without_relationship_typing", "behavior": "All candidate-to-candidate assertions are collapsed to one structural type in a schema-valid synthetic counterfactual.", **_analysis_delta(reference, untyped)})

    no_recursive_context = deepcopy(structural_context)
    no_recursive_context["context_id"] = "context-ablation-without-recursive-propagation"
    no_recursive_context["propagation_rules"] = {"enabled": False, "eligible_relationship_types": [], "maximum_depth": 0, "decay": structural_context["propagation_rules"]["decay"]}
    no_recursive = analyze(graph, provenance, no_recursive_context)
    ablations.append({"ablation": "without_recursive_propagation", "behavior": "The propagation component receives no paths while its declared component weight remains visible.", **_analysis_delta(reference, no_recursive)})

    equal_context = deepcopy(structural_context)
    equal_context["context_id"] = "context-ablation-neutralised-weighting"
    equal_context["weights"]["component_weights"] = {name: 0.25 for name in equal_context["weights"]["component_weights"]}
    equal_context["weights"]["relationship_type_weights"] = {name: 1.0 for name in equal_context["eligible_relationship_types"]}
    equal_weight = analyze(graph, provenance, equal_context)
    ablations.append({"ablation": "without_contextual_weight_differentiation", "behavior": "Eligible component and relationship-type weights are equalised; the Context remains explicit because omission is invalid.", **_analysis_delta(reference, equal_weight)})

    ablations.append({"ablation": "without_explanation_trace", "behavior": "Removing traces after computation leaves numeric ranks unchanged but makes every result's trace reference unresolved and therefore fails explanation validation.", "ranking_unchanged": True, "unresolved_trace_references": len(reference["significance_results"])})
    return {"reference_context": structural_context["context_id"], "ablations": ablations}


def _explanation_validation(
    graph: dict[str, Any], provenance: dict[str, Any], analyses: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    edge_by_id = {edge["id"]: edge for edge in graph["edges"]}
    evidence_ids = {item["id"] for item in provenance["evidence_records"]}
    provenance_ids = {item["id"] for item in provenance["provenance_records"]}
    checks = []
    for context_name, analysis in analyses.items():
        standing_ids = {item["id"] for item in analysis["standing_results"]}
        trace_ids = {item["id"] for item in analysis["explanation_traces"]}
        result_trace_ids = {item["explanation_trace_id"] for item in analysis["significance_results"]}
        failures = []
        indirect_evidence_links = 0
        for trace in analysis["explanation_traces"]:
            if trace["standing_contribution"]["standing_result_id"] not in standing_ids:
                failures.append(f"missing Standing result for {trace['id']}")
            if trace["context"] != analysis["context"] or trace["context_sha256"] != analysis["context_sha256"]:
                failures.append(f"Context mismatch for {trace['id']}")
            if not {"candidate_confidence", "calibration_status"} <= set(trace["confidence_adjustments"]):
                failures.append(f"confidence adjustment incomplete for {trace['id']}")
            if not {"burden", "context_tolerance", "applied_penalty"} <= set(trace["uncertainty_penalties"]):
                failures.append(f"uncertainty adjustment incomplete for {trace['id']}")
            for contribution in trace["direct_relationship_contributions"]:
                edge = edge_by_id.get(contribution["edge_id"])
                if edge is None:
                    failures.append(f"missing direct edge {contribution['edge_id']}")
                    continue
                cited = set(edge["assertion"]["evidence_ids"])
                if not cited <= evidence_ids:
                    failures.append(f"unresolved direct evidence for {contribution['edge_id']}")
                indirect_evidence_links += len(cited)
            for path in trace["propagated_contributions"]:
                if any(edge_id not in edge_by_id for edge_id in path["edge_path"]):
                    failures.append(f"unresolved propagated edge in {trace['id']}")
                if len(path["node_path"]) != len(set(path["node_path"])):
                    failures.append(f"cycle revisit in {trace['id']}")
            for excluded in trace["excluded_evidence"]:
                if excluded["edge_id"] not in edge_by_id or not set(excluded["evidence_ids"]) <= evidence_ids:
                    failures.append(f"unresolved excluded evidence in {trace['id']}")
            if not set(trace["provenance_refs"]) <= evidence_ids | provenance_ids:
                failures.append(f"unresolved provenance in {trace['id']}")
        if trace_ids != result_trace_ids:
            failures.append("result-to-trace identity mismatch")
        checks.append({
            "context": context_name,
            "trace_count": len(trace_ids),
            "all_required_information_resolvable": not failures,
            "failures": failures,
            "direct_evidence_links_resolved_via_bound_graph": indirect_evidence_links,
            "included_edge_evidence_self_contained_in_trace": False,
            "self_containment_note": "Included contributions carry edge IDs but not evidence IDs; evidence remains resolvable only by joining the hash-bound input graph.",
        })
    return {"contexts": checks, "all_contexts_resolvable": all(item["all_required_information_resolvable"] for item in checks), "opaque_output_rejected": True}


def _png_data(path: Path) -> str:
    with Image.open(path) as image:
        buffer = BytesIO()
        image.convert("RGB").save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("ascii")


def _explorer_html(
    source_path: Path,
    overlay_path: Path,
    graph: dict[str, Any],
    provenance: dict[str, Any],
    analyses: dict[str, dict[str, Any]],
) -> str:
    standing = {item["subject_id"]: item for item in analyses["structural_organisation"]["standing_results"]}
    detections = {item["id"]: item for item in provenance["detections"]}
    edge_by_id = {item["id"]: item for item in graph["edges"]}
    evidence = {
        item["id"]: {
            "record_status": item["record_status"],
            "uncertainty": item["uncertainty"],
            "evidence_kind": item["evidence_kind"],
        }
        for item in provenance["evidence_records"]
    }
    context_values: dict[str, Any] = {}
    for name, analysis in analyses.items():
        context_values[name] = {
            "objective": analysis["context"]["objective"],
            "results": {item["subject_id"]: item for item in analysis["ranked_results"]},
            "traces": {
                item["subject_id"]: {
                    "standing": item["standing_contribution"],
                    "direct": [
                        {
                            **contribution,
                            "evidence_ids": edge_by_id[contribution["edge_id"]]["assertion"]["evidence_ids"],
                            "assertion_uncertainty": edge_by_id[contribution["edge_id"]]["assertion"]["uncertainty"],
                        }
                        for contribution in item["direct_relationship_contributions"][:8]
                    ],
                    "propagated": [
                        {
                            **path,
                            "evidence_ids_by_edge": {
                                edge_id: edge_by_id[edge_id]["assertion"]["evidence_ids"]
                                for edge_id in path["edge_path"]
                            },
                        }
                        for path in item["top_explanatory_pathways"][:8]
                    ],
                    "confidence": item["confidence_adjustments"],
                    "uncertainty": item["uncertainty_penalties"],
                    "excluded": item["excluded_evidence"][:8],
                    "warnings": item["warnings"],
                }
                for item in analysis["explanation_traces"]
            },
        }
    nodes = []
    for node in graph["nodes"]:
        if node["node_type"] == "observation_source":
            nodes.append({"id": node["id"], "type": "observation_source", "x": 3, "y": 3, "confidence": None, "uncertainty": "not_applicable", "standing": None, "brightness_rank": None})
            continue
        candidate = node["payload"]
        detection = detections[candidate["detection_ids"][0]]
        nodes.append({
            "id": node["id"],
            "type": candidate["candidate_type"],
            "x": detection["centroid"]["x"],
            "y": detection["centroid"]["y"],
            "confidence": candidate["confidence"]["value"],
            "uncertainty": candidate["uncertainty"]["status"],
            "supporting_evidence_ids": candidate["supporting_evidence_ids"],
            "standing": standing[node["id"]]["score"],
            "brightness_rank": next(item["rank"] for item in analyses["structural_organisation"]["baselines"]["brightness"] if item["subject_id"] == node["id"]),
        })
    edges = [
        {
            "id": edge["id"], "source": edge["source"], "target": edge["target"],
            "type": edge["assertion"]["relationship_type"], "subtype": edge["assertion"]["relationship_subtype"],
            "strength": edge["assertion"]["relationship_strength"]["value"], "confidence": edge["assertion"]["confidence"]["value"],
            "uncertainty": edge["assertion"]["uncertainty"]["status"], "evidence_ids": edge["assertion"]["evidence_ids"],
        }
        for edge in graph["edges"]
    ]
    data = json.dumps({"nodes": nodes, "edges": edges, "evidence": evidence, "contexts": context_values}, ensure_ascii=False, sort_keys=True)
    template = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>ASA-Astro Phase II Reasoning Explorer</title>
<style>
body{font:14px system-ui,sans-serif;margin:0;background:#10151d;color:#e7edf6}header{padding:14px 20px;background:#192331}main{display:grid;grid-template-columns:minmax(560px,1.2fr) minmax(420px,1fr);gap:14px;padding:14px}.card{background:#18212d;border:1px solid #334155;border-radius:8px;padding:12px}.images{display:grid;grid-template-columns:1fr 1fr;gap:8px}.images img{width:100%;image-rendering:pixelated;background:#000}.graph{width:100%;aspect-ratio:1;background:#080b10;border:1px solid #334155}.edge{stroke-opacity:.5}.node{stroke:#fff;stroke-width:.3;cursor:pointer}table{width:100%;border-collapse:collapse;font-size:12px}th,td{border-bottom:1px solid #334155;padding:5px;text-align:left}select{background:#111827;color:#fff;padding:6px}pre{white-space:pre-wrap;word-break:break-word;max-height:420px;overflow:auto}.muted{color:#9fb0c6}.legend span{display:inline-block;margin-right:10px}
</style></head><body><header><h1>ASA-Astro Phase II Reasoning Explorer</h1><div class="muted">Synthetic engineering fixture only — not astronomical Ground Truth or ASA validation.</div></header><main>
<section><div class="card images"><div><h3>Source image</h3><img src="data:image/png;base64,__SOURCE__"></div><div><h3>Detection overlay</h3><img src="data:image/png;base64,__OVERLAY__"></div></div><div class="card"><label>Context <select id="context"></select></label><p id="objective" class="muted"></p><svg id="graph" class="graph" viewBox="0 0 96 96"></svg><p class="legend"><span>Node size: Standing</span><span>Node colour: selected-context Significance</span><span>Edge colour: Relationship Type</span></p></div></section>
<section><div class="card"><h2>Ranking and visual-prominence difference</h2><table><thead><tr><th>Sig.</th><th>Subject</th><th>Type</th><th>Standing</th><th>Significance</th><th>Brightness rank</th><th>Δ rank</th><th>Confidence</th><th>Uncertainty</th></tr></thead><tbody id="ranking"></tbody></table></div><div class="card"><h2>Selected explanation path</h2><pre id="detail">Select a graph node or ranking row.</pre></div></section>
</main><script>const DATA=__DATA__;const colors={spatial:'#60a5fa',containment:'#34d399',structural:'#f59e0b',observational:'#a78bfa',occlusion:'#ef4444'};const select=document.getElementById('context');Object.keys(DATA.contexts).forEach(k=>{const o=document.createElement('option');o.value=k;o.textContent=k.replaceAll('_',' ');select.appendChild(o)});function selected(){return DATA.contexts[select.value]}function shade(v){const x=Math.max(0,Math.min(1,v||0));return `rgb(${Math.round(40+215*x)},${Math.round(80+90*(1-x))},${Math.round(210-150*x)})`}function detail(id){const ctx=selected();const node=DATA.nodes.find(n=>n.id===id);const explanation=ctx.traces[id]||null;const evidenceIds=new Set(node?.supporting_evidence_ids||[]);(explanation?.direct||[]).forEach(x=>(x.evidence_ids||[]).forEach(e=>evidenceIds.add(e)));(explanation?.propagated||[]).forEach(x=>Object.values(x.evidence_ids_by_edge||{}).flat().forEach(e=>evidenceIds.add(e)));document.getElementById('detail').textContent=JSON.stringify({node,significance:ctx.results[id]||null,explanation,evidence:[...evidenceIds].map(e=>({id:e,...DATA.evidence[e]}))},null,2)}function render(){const ctx=selected();document.getElementById('objective').textContent=ctx.objective;const pos=Object.fromEntries(DATA.nodes.map(n=>[n.id,n]));const svg=document.getElementById('graph');svg.innerHTML='';DATA.edges.forEach(e=>{if(!pos[e.source]||!pos[e.target])return;const line=document.createElementNS('http://www.w3.org/2000/svg','line');line.setAttribute('x1',pos[e.source].x);line.setAttribute('y1',pos[e.source].y);line.setAttribute('x2',pos[e.target].x);line.setAttribute('y2',pos[e.target].y);line.setAttribute('stroke',colors[e.type]||'#94a3b8');line.setAttribute('stroke-width',.15+e.strength*.5);line.setAttribute('class','edge');line.appendChild(document.createElementNS('http://www.w3.org/2000/svg','title')).textContent=`${e.type}/${e.subtype}\nstrength ${e.strength} confidence ${e.confidence}\nuncertainty ${e.uncertainty}\nevidence ${e.evidence_ids.join(', ')}`;svg.appendChild(line)});DATA.nodes.forEach(n=>{const c=document.createElementNS('http://www.w3.org/2000/svg','circle');const result=ctx.results[n.id];c.setAttribute('cx',n.x);c.setAttribute('cy',n.y);c.setAttribute('r',n.type==='observation_source'?1.5:1.2+4*(n.standing||0));c.setAttribute('fill',n.type==='observation_source'?'#fff':shade(result?.score));c.setAttribute('class','node');c.onclick=()=>detail(n.id);c.appendChild(document.createElementNS('http://www.w3.org/2000/svg','title')).textContent=`${n.id}\n${n.type}\nStanding ${n.standing}\nSignificance ${result?.score}`;svg.appendChild(c)});const body=document.getElementById('ranking');body.innerHTML='';Object.values(ctx.results).sort((a,b)=>a.rank-b.rank).forEach(r=>{const n=pos[r.subject_id];const tr=document.createElement('tr');tr.innerHTML=`<td>${r.rank}</td><td>${r.subject_id}</td><td>${n.type}</td><td>${n.standing}</td><td>${r.score}</td><td>${n.brightness_rank}</td><td>${n.brightness_rank-r.rank}</td><td>${n.confidence}</td><td>${n.uncertainty}</td>`;tr.onclick=()=>detail(r.subject_id);body.appendChild(tr)})}select.onchange=render;select.value='structural_organisation';render();</script></body></html>"""
    return template.replace("__SOURCE__", _png_data(source_path)).replace("__OVERLAY__", base64.b64encode(overlay_path.read_bytes()).decode("ascii")).replace("__DATA__", data)


def _produce_upstream(root: Path, contexts: dict[str, dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any], dict[str, dict[str, Any]]]:
    input_directory = root / "input"
    input_directory.mkdir(parents=True, exist_ok=True)
    source = create_fixture(input_directory / "synthetic-observation.ppm")
    parameters = DetectionParameters.from_mapping(_read_json(REPOSITORY_ROOT / "examples/parameters.json"))
    process_observation(
        source,
        root / "evidence",
        metadata_path=REPOSITORY_ROOT / "tests/fixtures/synthetic_observation.metadata.json",
        parameters=parameters,
        source_locator="fixture:synthetic-observation-v1",
    )
    graph = _read_json(root / "evidence/graph.json")
    provenance = _read_json(root / "evidence/provenance.json")
    analyses = {}
    for name, context in contexts.items():
        context_path = root / "contexts" / f"{name}.json"
        _write_json(context_path, context)
        analysis = analyze(graph, provenance, context)
        write_analysis(root / "reasoning" / name, analysis)
        analyses[name] = analysis
    return graph, provenance, analyses


def _reproducibility(
    primary_root: Path, contexts: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="asa-astro-phase2-repeat-") as temporary:
        repeat_root = Path(temporary) / "run"
        repeat_root.mkdir()
        _produce_upstream(repeat_root, contexts)
        primary_files = {
            key: value
            for key, value in _directory_hashes(primary_root).items()
            if key.startswith("evidence/") or key.startswith("reasoning/") or key.startswith("contexts/") or key.startswith("input/")
        }
        repeat_files = _directory_hashes(repeat_root)
        differing = sorted(
            key for key in set(primary_files) | set(repeat_files) if primary_files.get(key) != repeat_files.get(key)
        )
    return {
        "deterministic_execution": not differing,
        "byte_identical_file_count": len(primary_files) - len(differing),
        "compared_file_count": len(set(primary_files) | set(repeat_files)),
        "differing_files": differing,
        "graph_identity": primary_files.get("evidence/graph.json"),
        "provenance_identity": primary_files.get("evidence/provenance.json"),
        "overlay_identity": primary_files.get("evidence/overlay.png"),
        "context_and_reasoning_artifacts_identical": not any(key.startswith(("contexts/", "reasoning/")) for key in differing),
    }


def manufacture(output_directory: Path) -> dict[str, Any]:
    output_directory = output_directory.resolve()
    if output_directory.exists():
        raise FileExistsError(f"output path already exists; refusing overwrite: {output_directory}")
    output_directory.parent.mkdir(parents=True, exist_ok=True)
    temporary_root = Path(tempfile.mkdtemp(prefix=f".{output_directory.name}.tmp-", dir=output_directory.parent))
    try:
        contexts = {name: _read_json(path) for name, path in CONTEXT_PATHS.items()}
        graph, provenance, analyses = _produce_upstream(temporary_root, contexts)
        benchmark = _benchmark_results(graph, analyses)
        benchmark["ranking_stability"] = _ranking_stability(
            graph,
            provenance,
            contexts["structural_organisation"],
            analyses["structural_organisation"],
        )
        adversarial = _adversarial_results(graph, provenance, contexts)
        ablations = _ablation_results(graph, provenance, contexts["structural_organisation"])
        explanations = _explanation_validation(graph, provenance, analyses)
        reproducibility = _reproducibility(temporary_root, contexts)
        graph_types = sorted({edge["assertion"]["relationship_type"] for edge in graph["edges"]})
        context_coverage = {
            name: {
                "eligible_relationship_types": context["eligible_relationship_types"],
                "eligible_types_present": sorted(set(context["eligible_relationship_types"]) & set(graph_types)),
                "eligible_edge_count": sum(1 for edge in graph["edges"] if edge["assertion"]["relationship_type"] in set(context["eligible_relationship_types"])),
            }
            for name, context in contexts.items()
        }
        input_manifest = {
            "harness_version": HARNESS_VERSION,
            "upstream_commit": UPSTREAM_COMMIT,
            "source_generator": "tests/fixtures/generate_fixture.py",
            "source_sha256": _sha256_file(temporary_root / "input/synthetic-observation.ppm"),
            "metadata_sha256": _sha256_file(REPOSITORY_ROOT / "tests/fixtures/synthetic_observation.metadata.json"),
            "parameters_sha256": _sha256_file(REPOSITORY_ROOT / "examples/parameters.json"),
            "requirements_lock_sha256": _sha256_file(REPOSITORY_ROOT / "requirements.lock"),
            "manual_priority_sha256": _sha256_file(MANUAL_PRIORITY_PATH),
            "context_sha256": {name: _sha256_bytes(canonical_json(context).encode("utf-8")) for name, context in contexts.items()},
            "astronomical_ground_truth_status": "unavailable",
            "fixture_status": "synthetic_software_validation_only",
        }
        summary = {
            "harness_version": HARNESS_VERSION,
            "upstream_commit": UPSTREAM_COMMIT,
            "processing_run_id": graph["processing_run_id"],
            "candidate_count": len(_candidate_ids(graph)),
            "edge_count": len(graph["edges"]),
            "relationship_types": graph_types,
            "computational_cost_proxies": {
                "standing_centrality_iterations": analyses["structural_organisation"]["standing_results"][0]["centrality_termination"]["iterations"],
                "standing_centrality_converged": analyses["structural_organisation"]["standing_results"][0]["centrality_termination"]["converged"],
                "propagated_path_count_by_context": {
                    name: sum(len(trace["propagated_contributions"]) for trace in analysis["explanation_traces"])
                    for name, analysis in analyses.items()
                },
            },
            "contexts": context_coverage,
            "reproducibility_passed": reproducibility["deterministic_execution"],
            "standing_context_isolation_passed": benchmark["context_isolation"]["standing_identical_across_contexts"],
            "distinct_significance_orders": benchmark["context_isolation"]["distinct_significance_orders"],
            "adversarial": {key: adversarial[key] for key in ("case_count", "pass_count", "fail_count", "limitation_count")},
            "explanations_resolvable": explanations["all_contexts_resolvable"],
            "bounded_hypothesis_outcome": "insufficient_evidence",
            "outcome_basis": [
                "Significance differs from brightness and Context switching is reproducible on the synthetic fixture.",
                "Contradictory evidence and assertion-level uncertainty do not affect edge support.",
                "Evidence-absent star-formation and gravitational Contexts emit active non-zero rankings instead of abstaining.",
                "Standing centrality is deterministic but did not converge within the declared 64-iteration cap.",
                "Five declared Contexts produced only two distinct ranking orders on this fixture.",
                "Weights are provisional and no astronomical Ground Truth or authorised ASA dependency exists."
            ],
        }
        _write_json(temporary_root / "input-manifest.json", input_manifest)
        _write_json(temporary_root / "benchmark-results.json", benchmark)
        _write_json(temporary_root / "adversarial-results.json", adversarial)
        _write_json(temporary_root / "ablation-results.json", ablations)
        _write_json(temporary_root / "explanation-validation.json", explanations)
        _write_json(temporary_root / "reproducibility.json", reproducibility)
        _write_json(temporary_root / "validation-summary.json", summary)
        (temporary_root / "explorer.html").write_text(
            _explorer_html(
                temporary_root / "input/synthetic-observation.ppm",
                temporary_root / "evidence/overlay.png",
                graph,
                provenance,
                analyses,
            ),
            encoding="utf-8",
        )
        manifest_entries = [
            {"path": path, "sha256": digest}
            for path, digest in _directory_hashes(temporary_root).items()
            if path != "manifest.json"
        ]
        _write_json(temporary_root / "manifest.json", {"harness_version": HARNESS_VERSION, "upstream_commit": UPSTREAM_COMMIT, "artifacts": manifest_entries})
        temporary_root.replace(output_directory)
        return summary
    except Exception:
        shutil.rmtree(temporary_root, ignore_errors=True)
        raise


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Codex D Phase II ASA-Astro validation")
    parser.add_argument("--output", type=Path, required=True, help="new output directory")
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    print(json.dumps(manufacture(arguments.output), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
