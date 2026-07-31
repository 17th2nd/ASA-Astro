"""Schema and cross-record invariants for generated Codex B evidence artefacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, RefResolver

from .graph import FORBIDDEN_PHYSICAL_RELATIONSHIPS


SCHEMA_BY_RECORD = {
    "observation_source": "observation-source.schema.json",
    "observation": "observation.schema.json",
    "detector_output": "detector-output.schema.json",
    "source_image_metadata": "source-image-metadata.schema.json",
    "detection": "detection.schema.json",
    "candidate_entity": "candidate-entity.schema.json",
    "relationship_assertion": "candidate-relationship-assertion.schema.json",
    "evidence_record": "evidence-record.schema.json",
    "provenance_record": "provenance-record.schema.json",
    "graph_node": "candidate-graph-node.schema.json",
    "graph_edge": "candidate-graph-edge.schema.json",
    "candidate_graph": "candidate-graph.schema.json",
    "confidence": "confidence.schema.json",
}


def default_schema_root() -> Path:
    """Locate root schemas in a source checkout.

    Wheel schema packaging is intentionally deferred for this bounded proof of concept.
    """

    return Path(__file__).resolve().parents[3] / "schemas"


def load_schemas(schema_root: Path | None = None) -> dict[str, dict[str, Any]]:
    root = schema_root or default_schema_root()
    schemas: dict[str, dict[str, Any]] = {}
    for path in sorted(root.rglob("*.schema.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        schemas[path.name] = schema
        if "$id" in schema:
            schemas[schema["$id"]] = schema
    missing = sorted(set(SCHEMA_BY_RECORD.values()) - set(schemas))
    if missing:
        raise ValueError(f"missing required schema file(s): {', '.join(missing)}")
    return schemas


def validate_instance(
    record_type: str,
    instance: dict[str, Any],
    schemas: dict[str, dict[str, Any]] | None = None,
) -> None:
    available = schemas or load_schemas()
    schema_name = SCHEMA_BY_RECORD[record_type]
    schema = available[schema_name]
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


def validate_generated_records(
    observation_source: dict[str, Any],
    observation: dict[str, Any],
    detector_output: dict[str, Any],
    image_metadata: dict[str, Any],
    detections: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    evidence_records: list[dict[str, Any]],
    provenance_record: dict[str, Any],
    graph: dict[str, Any],
    schemas: dict[str, dict[str, Any]] | None = None,
) -> None:
    available = schemas or load_schemas()
    validate_instance("observation_source", observation_source, available)
    validate_instance("observation", observation, available)
    validate_instance("detector_output", detector_output, available)
    validate_instance("source_image_metadata", image_metadata, available)
    validate_instance("provenance_record", provenance_record, available)
    for detection in detections:
        validate_instance("detection", detection, available)
    for candidate in candidates:
        validate_instance("candidate_entity", candidate, available)
    for evidence in evidence_records:
        validate_instance("evidence_record", evidence, available)
    for node in graph["nodes"]:
        validate_instance("graph_node", node, available)
    for edge in graph["edges"]:
        validate_instance("graph_edge", edge, available)
        validate_instance("relationship_assertion", edge["assertion"], available)
    validate_instance("candidate_graph", graph, available)
    _validate_cross_record_invariants(
        observation_source, detections, candidates, evidence_records, provenance_record, graph
    )


def _validate_cross_record_invariants(
    observation_source: dict[str, Any],
    detections: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    evidence_records: list[dict[str, Any]],
    provenance_record: dict[str, Any],
    graph: dict[str, Any],
) -> None:
    evidence_ids = {record["id"] for record in evidence_records}
    detection_ids = {record["id"] for record in detections}
    node_ids = {record["id"] for record in graph["nodes"]}
    if graph["source_sha256"] != observation_source["sha256"]:
        raise ValueError("graph source hash does not match observation source")
    if graph["processing_run_id"] != provenance_record["processing_run_id"]:
        raise ValueError("graph and provenance processing-run identifiers differ")
    for detection in detections:
        if detection["evidence_record_id"] not in evidence_ids:
            raise ValueError(f"detection lacks resolvable evidence: {detection['id']}")
    for candidate in candidates:
        if not set(candidate["detection_ids"]) <= detection_ids:
            raise ValueError(f"candidate cites missing detection: {candidate['id']}")
        if not set(candidate["supporting_evidence_ids"]) <= evidence_ids:
            raise ValueError(f"candidate cites missing evidence: {candidate['id']}")
    for edge in graph["edges"]:
        assertion = edge["assertion"]
        if edge["source"] not in node_ids or edge["target"] not in node_ids:
            raise ValueError(f"edge cites missing node: {edge['id']}")
        if not assertion["evidence_ids"] or not set(assertion["evidence_ids"]) <= evidence_ids:
            raise ValueError(f"edge lacks resolvable evidence: {edge['id']}")
        if assertion["physical_claim"]:
            raise ValueError(f"physical claim is prohibited in candidate graph: {edge['id']}")
        if (
            assertion["relationship_type"] in FORBIDDEN_PHYSICAL_RELATIONSHIPS
            or assertion["relationship_subtype"] in FORBIDDEN_PHYSICAL_RELATIONSHIPS
        ):
            raise ValueError(f"forbidden physical relationship: {edge['id']}")
        if assertion["relationship_strength"]["value"] == assertion["confidence"]["value"]:
            # Equality can occur numerically, but the fields must still retain distinct derivations.
            if assertion["relationship_strength"]["derivation"] == assertion["uncertainty"]["method"]:
                raise ValueError(f"relationship strength and confidence are not separated: {edge['id']}")
