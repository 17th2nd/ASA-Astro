"""Transparent proof-of-concept Standing and contextual Significance engine.

The formulas in this module are replaceable ASA-Astro hypotheses.  They consume
the published ontology and Codex B graph without asserting ASA conformance.
"""

from __future__ import annotations

from collections import deque
from copy import deepcopy
from math import hypot
from typing import Any

from .models import (
    ALGORITHM_VERSION,
    ASA_DEPENDENCY_STATUS,
    ASSERTION_CLASS_FACTORS,
    EVIDENCE_STATUS_FACTORS,
    ONTOLOGY_VERSION,
    RELATIONSHIP_PERSISTENCE,
    REASONING_SCHEMA_VERSION,
    TAXONOMY_VERSION,
    bounded,
    content_sha256,
    result_id,
    score,
    standing_policy,
)
from .validation import validate_context, validate_input_bundle, validate_reasoning_instance


def _candidate_nodes(graph: dict[str, Any]) -> list[dict[str, Any]]:
    return sorted(
        (node for node in graph["nodes"] if node["node_type"] == "candidate_entity"),
        key=lambda item: item["id"],
    )


def _normalise(values: dict[str, float], method: str = "max") -> dict[str, float]:
    if not values:
        return {}
    if method == "none":
        return {key: bounded(value) for key, value in values.items()}
    if method == "min_max":
        low, high = min(values.values()), max(values.values())
        if high == low:
            return {key: (0.0 if high == 0 else 1.0) for key in values}
        return {key: (value - low) / (high - low) for key, value in values.items()}
    high = max(values.values())
    return {key: (value / high if high > 0 else 0.0) for key, value in values.items()}


def _uncertainty_burden(record: dict[str, Any]) -> float:
    uncertainty = record.get("uncertainty", {})
    status = uncertainty.get("status", "unknown")
    base = {
        "not_applicable": 0.0,
        "bounded": 0.20,
        "estimated": 0.35,
        "unknown": 0.70,
        "unavailable": 0.80,
        "contested": 0.90,
        "withheld": 1.00,
    }.get(status, 0.75)
    confidence = uncertainty.get("confidence")
    if isinstance(confidence, (int, float)):
        base = max(base, 1.0 - bounded(confidence))
    return bounded(base)


def _confidence(record: dict[str, Any]) -> float:
    value = record.get("confidence", {}).get("value")
    return bounded(value) if isinstance(value, (int, float)) else 0.0


def _evidence_quality(evidence_ids: list[str], evidence: dict[str, dict[str, Any]]) -> float:
    if not evidence_ids:
        return 0.0
    values = []
    for evidence_id in evidence_ids:
        item = evidence[evidence_id]
        lifecycle = EVIDENCE_STATUS_FACTORS.get(item.get("record_status", "unavailable"), 0.0)
        values.append(lifecycle * (1.0 - 0.5 * _uncertainty_burden(item)))
    return sum(values) / len(values)


def _edge_vector(edge: dict[str, Any], evidence: dict[str, dict[str, Any]]) -> dict[str, Any]:
    assertion = edge["assertion"]
    strength = bounded(assertion["relationship_strength"]["value"])
    confidence = bounded(assertion["confidence"]["value"])
    evidence_quality = _evidence_quality(assertion["evidence_ids"], evidence)
    classification_factor = ASSERTION_CLASS_FACTORS[assertion["relationship_classification"]]
    persistence = RELATIONSHIP_PERSISTENCE.get(assertion["relationship_type"], 0.25)
    supported = strength * confidence * evidence_quality * classification_factor
    return {
        "edge_id": edge["id"],
        "source": edge["source"],
        "target": edge["target"],
        "relationship_type": assertion["relationship_type"],
        "relationship_subtype": assertion["relationship_subtype"],
        "directionality": assertion["directionality"],
        "relationship_strength": strength,
        "confidence": confidence,
        "evidence_quality": score(evidence_quality),
        "classification": assertion["relationship_classification"],
        "classification_factor": classification_factor,
        "persistence": persistence,
        "supported_weight": supported,
        "evidence_ids": sorted(assertion["evidence_ids"]),
        "provenance_record_id": assertion["provenance_record_id"],
        "uncertainty_burden": _uncertainty_burden(assertion),
    }


def _adjacency(
    node_ids: set[str], vectors: list[dict[str, Any]], relationship_types: set[str] | None = None
) -> dict[str, list[tuple[str, dict[str, Any]]]]:
    adjacency: dict[str, list[tuple[str, dict[str, Any]]]] = {node_id: [] for node_id in node_ids}
    for vector in vectors:
        if relationship_types is not None and vector["relationship_type"] not in relationship_types:
            continue
        source, target = vector["source"], vector["target"]
        if source in adjacency and target in adjacency:
            adjacency[source].append((target, vector))
            if vector["directionality"] == "symmetric":
                adjacency[target].append((source, vector))
    for node_id in adjacency:
        adjacency[node_id].sort(key=lambda pair: (pair[1]["edge_id"], pair[0]))
    return adjacency


def _incident_adjacency(node_ids: set[str], vectors: list[dict[str, Any]]) -> dict[str, list[tuple[str, dict[str, Any]]]]:
    """Return both endpoints for incident-structure and direct-contribution views."""
    adjacency: dict[str, list[tuple[str, dict[str, Any]]]] = {node_id: [] for node_id in node_ids}
    for vector in vectors:
        source, target = vector["source"], vector["target"]
        if source in adjacency and target in adjacency:
            adjacency[source].append((target, vector))
            adjacency[target].append((source, vector))
    for node_id in adjacency:
        adjacency[node_id].sort(key=lambda pair: (pair[1]["edge_id"], pair[0]))
    return adjacency


def _eigenvector(adjacency: dict[str, list[tuple[str, dict[str, Any]]]], maximum: int, tolerance: float) -> tuple[dict[str, float], int, bool]:
    if not adjacency:
        return {}, 0, True
    values = {node_id: 1.0 for node_id in adjacency}
    for iteration in range(1, maximum + 1):
        updated = {
            node_id: sum(vector["supported_weight"] * vector["persistence"] * values[neighbour] for neighbour, vector in links)
            for node_id, links in adjacency.items()
        }
        norm = max(updated.values(), default=0.0)
        if norm == 0:
            return {node_id: 0.0 for node_id in adjacency}, iteration, True
        updated = {node_id: value / norm for node_id, value in updated.items()}
        delta = max(abs(updated[node_id] - values[node_id]) for node_id in values)
        values = updated
        if delta <= tolerance:
            return values, iteration, True
    return values, maximum, False


def _betweenness(adjacency: dict[str, list[tuple[str, dict[str, Any]]]]) -> dict[str, float]:
    """Deterministic unweighted Brandes centrality on supported topology."""
    result = {node_id: 0.0 for node_id in adjacency}
    for source in sorted(adjacency):
        stack: list[str] = []
        predecessors = {node_id: [] for node_id in adjacency}
        paths = {node_id: 0.0 for node_id in adjacency}
        paths[source] = 1.0
        distance = {node_id: -1 for node_id in adjacency}
        distance[source] = 0
        queue = deque([source])
        while queue:
            current = queue.popleft()
            stack.append(current)
            for neighbour, vector in adjacency[current]:
                if vector["supported_weight"] <= 0:
                    continue
                if distance[neighbour] < 0:
                    queue.append(neighbour)
                    distance[neighbour] = distance[current] + 1
                if distance[neighbour] == distance[current] + 1:
                    paths[neighbour] += paths[current]
                    predecessors[neighbour].append(current)
        dependency = {node_id: 0.0 for node_id in adjacency}
        while stack:
            target = stack.pop()
            if paths[target]:
                for predecessor in predecessors[target]:
                    dependency[predecessor] += (paths[predecessor] / paths[target]) * (1.0 + dependency[target])
            if target != source:
                result[target] += dependency[target]
    return result


def compute_standing(graph: dict[str, Any], provenance: dict[str, Any]) -> list[dict[str, Any]]:
    """Compute Context-independent, decomposable structural Standing records."""
    validate_input_bundle(graph, provenance)
    policy = standing_policy()
    candidates = _candidate_nodes(graph)
    node_ids = {node["id"] for node in candidates}
    evidence = {item["id"]: item for item in provenance["evidence_records"]}
    vectors = [_edge_vector(edge, evidence) for edge in graph["edges"]]
    structural_vectors = [vector for vector in vectors if vector["source"] in node_ids and vector["target"] in node_ids]
    adjacency = _incident_adjacency(node_ids, structural_vectors)
    eigen, iterations, converged = _eigenvector(adjacency, policy["centrality_max_iterations"], policy["centrality_tolerance"])
    betweenness = _betweenness(adjacency)
    raw: dict[str, dict[str, float]] = {node_id: {} for node_id in node_ids}
    node_by_id = {node["id"]: node for node in candidates}
    for node_id in sorted(node_ids):
        links = adjacency[node_id]
        incident_types = {vector["relationship_type"] for _, vector in links}
        raw[node_id]["typed_degree"] = float(len(incident_types))
        raw[node_id]["weighted_connectivity"] = sum(vector["supported_weight"] for _, vector in links)
        raw[node_id]["eigenvector_influence"] = eigen[node_id]
        raw[node_id]["betweenness"] = betweenness[node_id]
        raw[node_id]["containment_hierarchy"] = sum(vector["supported_weight"] for _, vector in links if vector["relationship_type"] == "containment")
        raw[node_id]["relationship_persistence"] = sum(vector["supported_weight"] * vector["persistence"] for _, vector in links)
        candidate = node_by_id[node_id]["payload"]
        raw[node_id]["evidence_support"] = _confidence(candidate) * _evidence_quality(candidate["supporting_evidence_ids"], evidence)
        raw[node_id]["structural_dependency"] = sum(
            vector["supported_weight"] for _, vector in links if vector["relationship_type"] in {"structural", "containment"}
        )
    normalised: dict[str, dict[str, float]] = {node_id: {} for node_id in node_ids}
    for component in policy["component_weights"]:
        values = {node_id: raw[node_id][component] for node_id in node_ids}
        for node_id, value in _normalise(values, policy["normalisation_method"]).items():
            normalised[node_id][component] = value

    graph_hash = content_sha256(graph)
    provenance_hash = content_sha256(provenance)
    results = []
    for node_id in sorted(node_ids):
        candidate = node_by_id[node_id]["payload"]
        components = {}
        pre_adjustment = 0.0
        for name, weight in policy["component_weights"].items():
            contribution = normalised[node_id][name] * weight
            pre_adjustment += contribution
            components[name] = {
                "raw_value": round(raw[node_id][name], 12),
                "normalised_value": score(normalised[node_id][name]),
                "weight": weight,
                "contribution": score(contribution),
            }
        confidence_adjustment = _confidence(candidate)
        uncertainty = _uncertainty_burden(candidate)
        penalty = policy["uncertainty_penalty_weight"] * uncertainty
        final = pre_adjustment * confidence_adjustment * (1.0 - penalty)
        provenance_refs = sorted(set(candidate["supporting_evidence_ids"] + [candidate["provenance_record_id"]]))
        result = {
            "schema_version": REASONING_SCHEMA_VERSION,
            "ontology_version": ONTOLOGY_VERSION,
            "taxonomy_version": TAXONOMY_VERSION,
            "record_status": "active",
            "epistemic_classification": "computed",
            "id": result_id("standing", {"graph": graph_hash, "provenance": provenance_hash, "subject": node_id, "policy": policy}),
            "subject_id": node_id,
            "algorithm_version": ALGORITHM_VERSION,
            "policy": policy,
            "asa_dependency_status": ASA_DEPENDENCY_STATUS,
            "input_graph_sha256": graph_hash,
            "input_provenance_sha256": provenance_hash,
            "score": score(final),
            "raw_score": round(pre_adjustment, 12),
            "component_contributions": components,
            "confidence_adjustment": score(confidence_adjustment),
            "uncertainty_penalty": score(penalty),
            "centrality_termination": {"iterations": iterations, "converged": converged, "maximum_iterations": policy["centrality_max_iterations"]},
            "provenance_refs": provenance_refs,
            "warnings": ["Provisional non-canonical Standing hypothesis; DR-0001 and DR-0009 remain open."],
        }
        validate_reasoning_instance("standing_result", result)
        results.append(result)
    return results


def _contextual_edge_weight(vector: dict[str, Any], context: dict[str, Any]) -> float:
    return vector["supported_weight"] * context["weights"]["relationship_type_weights"].get(vector["relationship_type"], 0.0)


def _propagated_paths(
    start: str,
    adjacency: dict[str, list[tuple[str, dict[str, Any]]]],
    standing: dict[str, float],
    context: dict[str, Any],
) -> list[dict[str, Any]]:
    rules = context["propagation_rules"]
    if not rules["enabled"]:
        return []
    eligible = set(rules["eligible_relationship_types"])
    paths: list[dict[str, Any]] = []

    def walk(current: str, visited: tuple[str, ...], edge_ids: tuple[str, ...], product: float, depth: int) -> None:
        if depth >= rules["maximum_depth"]:
            return
        for neighbour, vector in adjacency.get(current, []):
            if vector["relationship_type"] not in eligible or neighbour in visited:
                continue
            next_depth = depth + 1
            next_product = product * _contextual_edge_weight(vector, context) * (rules["decay"] ** next_depth)
            next_edges = edge_ids + (vector["edge_id"],)
            if next_depth >= 2:
                paths.append({
                    "node_path": list(visited + (neighbour,)),
                    "edge_path": list(next_edges),
                    "depth": next_depth,
                    "contribution": score(next_product * standing.get(neighbour, 0.0)),
                })
            walk(neighbour, visited + (neighbour,), next_edges, next_product, next_depth)

    walk(start, (start,), (), 1.0, 0)
    return sorted(paths, key=lambda item: (-item["contribution"], item["edge_path"], item["node_path"]))


def compute_significance(
    graph: dict[str, Any], provenance: dict[str, Any], context: dict[str, Any], standing_results: list[dict[str, Any]] | None = None
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Compute runtime Significance and separate Explanation Trace records."""
    validate_input_bundle(graph, provenance)
    validate_context(context)
    standings = standing_results or compute_standing(graph, provenance)
    candidates = _candidate_nodes(graph)
    node_ids = {node["id"] for node in candidates}
    node_by_id = {node["id"]: node for node in candidates}
    standing_by_id = {item["subject_id"]: item for item in standings}
    standing_scores = {key: item["score"] for key, item in standing_by_id.items()}
    evidence = {item["id"]: item for item in provenance["evidence_records"]}
    vectors = [_edge_vector(edge, evidence) for edge in graph["edges"]]
    all_ids = {node["id"] for node in graph["nodes"]}
    adjacency = _adjacency(all_ids, vectors)
    incident = _incident_adjacency(all_ids, vectors)
    eligible = set(context["eligible_relationship_types"])
    excluded = set(context["excluded_relationship_types"])
    weights = context["weights"]["component_weights"]
    graph_hash, provenance_hash, context_hash = content_sha256(graph), content_sha256(provenance), content_sha256(context)

    direct_raw: dict[str, float] = {}
    info_raw: dict[str, float] = {}
    direct_details: dict[str, list[dict[str, Any]]] = {}
    propagation_details: dict[str, list[dict[str, Any]]] = {}
    for node_id in sorted(node_ids):
        details = []
        for neighbour, vector in incident.get(node_id, []):
            if vector["relationship_type"] not in eligible or vector["relationship_type"] in excluded:
                continue
            contribution = _contextual_edge_weight(vector, context) * (0.5 + 0.5 * standing_scores.get(neighbour, 0.0))
            details.append({**{key: vector[key] for key in ("edge_id", "relationship_type", "relationship_subtype", "relationship_strength", "confidence", "evidence_quality", "classification")}, "neighbour_id": neighbour, "raw_contribution": round(contribution, 12)})
        direct_details[node_id] = sorted(details, key=lambda item: (-item["raw_contribution"], item["edge_id"], item["neighbour_id"]))
        direct_raw[node_id] = sum(item["raw_contribution"] for item in details)
        candidate = node_by_id[node_id]["payload"]
        info_raw[node_id] = _evidence_quality(candidate["supporting_evidence_ids"], evidence)
        propagation_details[node_id] = _propagated_paths(node_id, adjacency, standing_scores, context)
    direct_norm = _normalise(direct_raw, context["normalization_method"])
    propagation_norm = _normalise({node_id: sum(item["contribution"] for item in propagation_details[node_id]) for node_id in node_ids}, context["normalization_method"])
    info_norm = _normalise(info_raw, context["normalization_method"])

    results, traces = [], []
    for node_id in sorted(node_ids):
        candidate = node_by_id[node_id]["payload"]
        component_values = {
            "standing": standing_scores[node_id],
            "direct_relationships": direct_norm[node_id],
            "propagated_relationships": propagation_norm[node_id],
            "information_value": info_norm[node_id],
        }
        component_contributions = {name: score(component_values[name] * weights[name]) for name in weights}
        pre_adjustment = sum(component_contributions.values())
        confidence_adjustment = _confidence(candidate)
        uncertainty = _uncertainty_burden(candidate)
        tolerance = context["uncertainty_tolerance"]
        penalty = uncertainty * (1.0 - tolerance)
        final = pre_adjustment * confidence_adjustment * (1.0 - penalty)
        included_edges = {item["edge_id"] for item in direct_details[node_id]}
        excluded_evidence = []
        for neighbour, vector in incident.get(node_id, []):
            if vector["edge_id"] in included_edges:
                continue
            reason = "relationship_type_excluded" if vector["relationship_type"] in excluded else "relationship_type_not_eligible"
            excluded_evidence.append({"edge_id": vector["edge_id"], "relationship_type": vector["relationship_type"], "reason": reason, "evidence_ids": vector["evidence_ids"]})
        warnings = ["Provisional non-canonical Significance hypothesis; DR-0001, DR-0008, DR-0010, and DR-0012 remain open."]
        if not direct_details[node_id]:
            warnings.append("No eligible direct relationship assertion supports this node in the declared Context.")
        trace_payload = {"graph": graph_hash, "provenance": provenance_hash, "context": context_hash, "subject": node_id}
        trace_id = result_id("trace", trace_payload)
        standing_id = standing_by_id[node_id]["id"]
        result = {
            "schema_version": REASONING_SCHEMA_VERSION,
            "ontology_version": ONTOLOGY_VERSION,
            "taxonomy_version": TAXONOMY_VERSION,
            "record_status": "active",
            "epistemic_classification": "computed",
            "id": result_id("significance", trace_payload),
            "subject_id": node_id,
            "algorithm_version": ALGORITHM_VERSION,
            "asa_dependency_status": ASA_DEPENDENCY_STATUS,
            "input_graph_sha256": graph_hash,
            "input_provenance_sha256": provenance_hash,
            "context_id": context["context_id"],
            "context_version": context["context_version"],
            "context_sha256": context_hash,
            "standing_result_id": standing_id,
            "explanation_trace_id": trace_id,
            "score": score(final),
            "raw_score": round(pre_adjustment, 12),
            "scale_semantics": "relative_contextual_proof_of_concept_score_0_to_1_not_probability",
            "component_contributions": component_contributions,
            "confidence_adjustment": score(confidence_adjustment),
            "uncertainty_penalty": score(penalty),
            "provenance_refs": sorted(set(candidate["supporting_evidence_ids"] + [candidate["provenance_record_id"]])),
            "warnings": warnings,
        }
        trace = {
            "schema_version": REASONING_SCHEMA_VERSION,
            "ontology_version": ONTOLOGY_VERSION,
            "taxonomy_version": TAXONOMY_VERSION,
            "record_status": "active",
            "epistemic_classification": "computed",
            "id": trace_id,
            "subject_id": node_id,
            "significance_result_id": result["id"],
            "algorithm_version": ALGORITHM_VERSION,
            "input_graph_sha256": graph_hash,
            "input_provenance_sha256": provenance_hash,
            "context_sha256": context_hash,
            "context": deepcopy(context),
            "final_score": result["score"],
            "standing_contribution": {"standing_result_id": standing_id, "standing_score": standing_scores[node_id], "weighted_contribution": component_contributions["standing"]},
            "direct_relationship_contributions": direct_details[node_id],
            "propagated_contributions": propagation_details[node_id],
            "confidence_adjustments": {"candidate_confidence": score(confidence_adjustment), "calibration_status": candidate["confidence"]["calibration_status"]},
            "uncertainty_penalties": {"burden": score(uncertainty), "context_tolerance": tolerance, "applied_penalty": score(penalty)},
            "excluded_evidence": sorted(excluded_evidence, key=lambda item: (item["edge_id"], item["reason"])),
            "warnings": warnings,
            "top_explanatory_pathways": propagation_details[node_id][: context["explanation_requirements"]["maximum_pathways"]],
            "provenance_refs": result["provenance_refs"],
        }
        validate_reasoning_instance("significance_result", result)
        validate_reasoning_instance("explanation_trace", trace)
        results.append(result)
        traces.append(trace)
    return sorted(results, key=lambda item: item["subject_id"]), sorted(traces, key=lambda item: item["subject_id"])


def compute_baselines(graph: dict[str, Any], provenance: dict[str, Any], context: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    """Compute explicit comparators; none feeds the Significance score."""
    candidates = _candidate_nodes(graph)
    node_ids = {node["id"] for node in candidates}
    detections = {item["id"]: item for item in provenance["detections"]}
    metadata = provenance["source_image_metadata"][0]
    cx, cy = metadata["width_pixels"] / 2.0, metadata["height_pixels"] / 2.0
    max_distance = hypot(cx, cy) or 1.0
    evidence = {item["id"]: item for item in provenance["evidence_records"]}
    vectors = [_edge_vector(edge, evidence) for edge in graph["edges"] if edge["source"] in node_ids and edge["target"] in node_ids]
    adjacency = _incident_adjacency(node_ids, vectors)
    eigen, _, _ = _eigenvector(adjacency, 64, 1e-12)
    raw: dict[str, dict[str, float]] = {name: {} for name in ("brightness", "degree", "centrality", "image_centre", "manual_class_priority")}
    priorities = context["baseline_configuration"]["manual_class_priorities"]
    for node in candidates:
        node_id, candidate = node["id"], node["payload"]
        detection = detections[candidate["detection_ids"][0]]
        raw["brightness"][node_id] = float(detection["features"]["peak_intensity"]["value"])
        raw["degree"][node_id] = float(len(adjacency[node_id]))
        raw["centrality"][node_id] = eigen[node_id]
        centroid = detection["centroid"]
        raw["image_centre"][node_id] = max(0.0, 1.0 - hypot(centroid["x"] - cx, centroid["y"] - cy) / max_distance)
        raw["manual_class_priority"][node_id] = float(priorities.get(candidate["candidate_type"], 0.0))
    output = {}
    for name, values in raw.items():
        normalised = _normalise(values, "max")
        ranked = sorted(values, key=lambda node_id: (-normalised[node_id], node_id))
        output[name] = [{"rank": rank, "subject_id": node_id, "score": score(normalised[node_id]), "raw_value": round(values[node_id], 12)} for rank, node_id in enumerate(ranked, 1)]
    return output


def analyze(graph: dict[str, Any], provenance: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    standings = compute_standing(graph, provenance)
    significance, traces = compute_significance(graph, provenance, context, standings)
    ranked = sorted(significance, key=lambda item: (-item["score"], item["subject_id"]))
    return {
        "schema_version": REASONING_SCHEMA_VERSION,
        "algorithm_version": ALGORITHM_VERSION,
        "asa_dependency_status": ASA_DEPENDENCY_STATUS,
        "input_graph_sha256": content_sha256(graph),
        "input_provenance_sha256": content_sha256(provenance),
        "context_sha256": content_sha256(context),
        "standing_policy": standing_policy(),
        "context": deepcopy(context),
        "standing_results": standings,
        "significance_results": significance,
        "ranked_results": [{"rank": index, "subject_id": item["subject_id"], "score": item["score"], "significance_result_id": item["id"]} for index, item in enumerate(ranked, 1)],
        "explanation_traces": traces,
        "baselines": compute_baselines(graph, provenance, context),
    }


def analyze_counterfactual(
    graph: dict[str, Any], provenance: dict[str, Any], context: dict[str, Any], intervention: dict[str, Any]
) -> dict[str, Any]:
    """Compare one bounded intervention with an unchanged versioned baseline."""
    baseline = analyze(graph, provenance, context)
    changed_graph, changed_provenance, changed_context = deepcopy(graph), deepcopy(provenance), deepcopy(context)
    kind = intervention.get("kind")
    if kind == "remove_node":
        node_id = intervention["node_id"]
        changed_graph["nodes"] = [node for node in changed_graph["nodes"] if node["id"] != node_id]
        changed_graph["edges"] = [edge for edge in changed_graph["edges"] if edge["source"] != node_id and edge["target"] != node_id]
    elif kind == "weaken_edge":
        factor = bounded(intervention["factor"])
        matches = [edge for edge in changed_graph["edges"] if edge["id"] == intervention["edge_id"]]
        if not matches:
            raise ValueError("counterfactual edge_id is unavailable")
        matches[0]["assertion"]["relationship_strength"]["value"] *= factor
    elif kind == "drop_observational_confidence":
        factor = bounded(intervention["factor"])
        node_id = intervention["node_id"]
        matches = [node for node in changed_graph["nodes"] if node["id"] == node_id and node["node_type"] == "candidate_entity"]
        if not matches:
            raise ValueError("counterfactual candidate node_id is unavailable")
        matches[0]["payload"]["confidence"]["value"] *= factor
    elif kind == "change_context":
        changed_context = deepcopy(intervention["context"])
    else:
        raise ValueError("unsupported counterfactual kind")
    changed = analyze(changed_graph, changed_provenance, changed_context)
    base_scores = {item["subject_id"]: item for item in baseline["ranked_results"]}
    changed_scores = {item["subject_id"]: item for item in changed["ranked_results"]}
    comparison = []
    for node_id in sorted(set(base_scores) | set(changed_scores)):
        before, after = base_scores.get(node_id), changed_scores.get(node_id)
        comparison.append({
            "subject_id": node_id,
            "before_score": before["score"] if before else None,
            "after_score": after["score"] if after else None,
            "score_delta": round(after["score"] - before["score"], 12) if before and after else None,
            "before_rank": before["rank"] if before else None,
            "after_rank": after["rank"] if after else None,
        })
    return {"intervention": deepcopy(intervention), "baseline": baseline, "counterfactual": changed, "comparison": comparison}
