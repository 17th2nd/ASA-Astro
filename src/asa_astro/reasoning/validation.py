"""Contract and semantic validation for Codex C reasoning inputs and outputs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, RefResolver

from asa_astro.evidence.graph import FORBIDDEN_PHYSICAL_RELATIONSHIPS
from asa_astro.evidence.validation import load_schemas, validate_instance as validate_evidence_instance

from .models import RELATIONSHIP_TYPES


REASONING_SCHEMAS = {
    "context": "context.schema.json",
    "standing_result": "standing-result.schema.json",
    "significance_result": "significance-result.schema.json",
    "explanation_trace": "explanation-trace.schema.json",
}


def repository_root() -> Path:
    return Path(__file__).resolve().parents[3]


def load_reasoning_schemas() -> dict[str, dict[str, Any]]:
    """Load all repository schemas so relative and canonical references resolve."""

    schemas = load_schemas(repository_root() / "schemas")
    missing = sorted(set(REASONING_SCHEMAS.values()) - set(schemas))
    if missing:
        raise ValueError(f"missing reasoning schema file(s): {', '.join(missing)}")
    return schemas


def validate_reasoning_instance(
    record_type: str,
    instance: dict[str, Any],
    schemas: dict[str, dict[str, Any]] | None = None,
) -> None:
    available = schemas or load_reasoning_schemas()
    schema = available[REASONING_SCHEMAS[record_type]]
    resolver = RefResolver.from_schema(schema, store=available)
    errors = sorted(
        Draft202012Validator(schema, resolver=resolver).iter_errors(instance),
        key=lambda error: list(error.absolute_path),
    )
    if errors:
        rendered = "; ".join(
            f"{'/'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
            for error in errors
        )
        raise ValueError(f"{record_type} schema validation failed: {rendered}")


def validate_context(context: dict[str, Any]) -> None:
    validate_reasoning_instance("context", context)
    if context["authority"]["status"] != "provisional_non_canonical":
        raise ValueError(
            "this implementation can execute only provisional_non_canonical contexts while DR-0001 and DR-0008 remain open"
        )
    eligible = set(context["eligible_relationship_types"])
    excluded = set(context["excluded_relationship_types"])
    if not eligible <= RELATIONSHIP_TYPES or not excluded <= RELATIONSHIP_TYPES:
        raise ValueError("context contains a relationship type outside ASTRO-RELATIONSHIP-TAXONOMY-0001")
    overlap = eligible & excluded
    if overlap:
        raise ValueError(f"relationship types cannot be both eligible and excluded: {', '.join(sorted(overlap))}")
    relationship_weights = context["weights"]["relationship_type_weights"]
    undeclared_weights = set(relationship_weights) - eligible
    if undeclared_weights:
        raise ValueError(
            "relationship weights require eligibility: " + ", ".join(sorted(undeclared_weights))
        )
    component_weights = context["weights"]["component_weights"]
    total = sum(component_weights.values())
    if abs(total - 1.0) > 1e-9:
        raise ValueError("context component weights must sum to exactly 1.0")
    propagation = context["propagation_rules"]
    if propagation["enabled"]:
        if not 1 <= propagation["maximum_depth"] <= 8:
            raise ValueError("enabled propagation maximum_depth must be between 1 and 8")
        if not set(propagation["eligible_relationship_types"]) <= eligible:
            raise ValueError("propagation relationship types must be eligible in the context")
    elif propagation["maximum_depth"] != 0:
        raise ValueError("disabled propagation must declare maximum_depth 0")


def validate_input_bundle(graph: dict[str, Any], provenance: dict[str, Any]) -> None:
    """Validate the published Codex B graph plus its companion provenance bundle."""

    validate_evidence_instance("candidate_graph", graph)
    if graph.get("processing_run_id") != provenance.get("processing_run_id"):
        raise ValueError("graph and provenance processing_run_id differ")
    evidence = {item["id"]: item for item in provenance.get("evidence_records", [])}
    detections = {item["id"]: item for item in provenance.get("detections", [])}
    provenance_ids = {item["id"] for item in provenance.get("provenance_records", [])}
    if not evidence or not detections or not provenance_ids:
        raise ValueError("provenance bundle must include evidence_records, detections, and provenance_records")
    node_ids = {node["id"] for node in graph["nodes"]}
    if len(node_ids) != len(graph["nodes"]):
        raise ValueError("graph node identifiers must be unique")
    edge_ids: set[str] = set()
    for node in graph["nodes"]:
        if node["node_type"] != "candidate_entity":
            continue
        candidate = node["payload"]
        if not set(candidate["detection_ids"]) <= set(detections):
            raise ValueError(f"candidate cites an unavailable detection: {candidate['id']}")
        if not set(candidate["supporting_evidence_ids"]) <= set(evidence):
            raise ValueError(f"candidate cites unavailable supporting evidence: {candidate['id']}")
        if candidate["provenance_record_id"] not in provenance_ids:
            raise ValueError(f"candidate cites unavailable provenance: {candidate['id']}")
        if "standing" in candidate or "significance" in candidate:
            raise ValueError("Standing and Significance cannot be intrinsic candidate attributes")
    for edge in graph["edges"]:
        if edge["id"] in edge_ids:
            raise ValueError(f"duplicate edge identifier: {edge['id']}")
        edge_ids.add(edge["id"])
        assertion = edge["assertion"]
        if edge["source"] not in node_ids or edge["target"] not in node_ids:
            raise ValueError(f"edge cites an unavailable node: {edge['id']}")
        if assertion["physical_claim"]:
            raise ValueError(f"physical claim is inadmissible: {edge['id']}")
        if assertion["relationship_type"] in FORBIDDEN_PHYSICAL_RELATIONSHIPS:
            raise ValueError(f"unsupported physical relationship is inadmissible: {edge['id']}")
        if assertion["relationship_type"] not in RELATIONSHIP_TYPES:
            raise ValueError(f"unknown taxonomy relationship type: {edge['id']}")
        if not set(assertion["evidence_ids"]) <= set(evidence):
            raise ValueError(f"edge cites unavailable evidence: {edge['id']}")
        strength = assertion["relationship_strength"]["value"]
        confidence = assertion["confidence"]["value"]
        if not isinstance(strength, (int, float)) or not 0 <= strength <= 1:
            raise ValueError(f"PoC relationship strength must be bounded in [0,1]: {edge['id']}")
        if not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
            raise ValueError(f"PoC relationship confidence must be bounded in [0,1]: {edge['id']}")


def load_json_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON input must be an object: {path}")
    return value
