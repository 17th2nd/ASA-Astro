"""End-to-end immutable evidence registration and candidate-graph generation."""

from __future__ import annotations

from hashlib import sha256
from html import escape
from io import BytesIO
import json
import mimetypes
import os
from pathlib import Path
import platform
import shutil
import tempfile
from typing import Any

from PIL import Image, ImageDraw, __version__ as pillow_version

from .detection import detect_regions
from .graph import build_candidates, build_graph, build_relationships
from .models import (
    DetectionParameters,
    ONTOLOGY_VERSION,
    PIPELINE_VERSION,
    SCHEMA_VERSION,
    canonical_json,
    record_metadata,
    stable_id,
)
from .validation import validate_generated_records


def hash_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _artifact(path: Path, root: Path, role: str, media_type: str) -> dict[str, Any]:
    return {
        "path": path.relative_to(root).as_posix(),
        "role": role,
        "media_type": media_type,
        "byte_size": path.stat().st_size,
        "sha256": hash_file(path),
    }


def _safe_suffix(path: Path) -> str:
    suffix = path.suffix.lower()
    return suffix if suffix and suffix[1:].isalnum() else ".bin"


def _load_declared_metadata(metadata_path: Path | None) -> tuple[dict[str, Any], str | None]:
    if metadata_path is None:
        return {}, None
    if not metadata_path.is_file():
        raise FileNotFoundError(f"associated metadata file does not exist: {metadata_path}")
    with metadata_path.open("r", encoding="utf-8") as source:
        value = json.load(source)
    if not isinstance(value, dict):
        raise ValueError("associated metadata must be a JSON object")
    return value, hash_file(metadata_path)


def _declared_value(
    metadata: dict[str, Any], key: str, unavailable_reason: str
) -> dict[str, Any]:
    if key in metadata and metadata[key] is not None:
        return {"status": "declared", "value": metadata[key]}
    return {"status": "unavailable", "value": None, "reason": unavailable_reason}


def _declared_string_list(metadata: dict[str, Any], key: str) -> list[str]:
    value = metadata.get(key, [])
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"declared metadata field {key} must be an array of strings")
    return value


def _software_record() -> dict[str, str]:
    package_root = Path(__file__).resolve().parent
    repository_root = Path(__file__).resolve().parents[3]
    code_paths = sorted(package_root.glob("*.py")) + [repository_root / "src/asa_astro/cli.py"]
    schema_paths = sorted((repository_root / "schemas").rglob("*.schema.json"))

    def tree_digest(paths: list[Path], root: Path) -> str:
        digest = sha256()
        for path in paths:
            digest.update(path.relative_to(root).as_posix().encode("utf-8"))
            digest.update(b"\0")
            digest.update(path.read_bytes())
            digest.update(b"\0")
        return digest.hexdigest()

    return {
        "pipeline": "asa-astro-observation-to-graph",
        "pipeline_version": PIPELINE_VERSION,
        "code_sha256": tree_digest(code_paths, repository_root),
        "schema_bundle_sha256": tree_digest(schema_paths, repository_root),
        "python": platform.python_version(),
        "pillow": pillow_version,
    }


def _render_overlay(
    image: Image.Image,
    candidates: list[dict[str, Any]],
    detections: list[dict[str, Any]],
) -> bytes:
    overlay = image.convert("RGB").copy()
    draw = ImageDraw.Draw(overlay)
    detection_by_id = {item["id"]: item for item in detections}
    colours = {
        "primary_extended_object": (0, 255, 255),
        "likely_foreground_point_source": (255, 255, 0),
        "internal_substructure": (0, 255, 0),
        "possible_companion_object": (255, 128, 0),
        "background_extended_object": (128, 128, 255),
        "diffuse_or_uncertain_region": (255, 0, 255),
        "unresolved_background_object_candidate": (255, 255, 255),
        "dark_or_occluding_region": (255, 0, 0),
        "unknown_image_region": (160, 160, 160),
    }
    for index, candidate in enumerate(sorted(candidates, key=lambda item: item["id"]), start=1):
        detection = detection_by_id[candidate["detection_ids"][0]]
        bbox = detection["bbox"]
        x0, y0 = bbox["x"], bbox["y"]
        x1, y1 = x0 + bbox["width"] - 1, y0 + bbox["height"] - 1
        colour = colours[candidate["candidate_type"]]
        draw.rectangle((x0, y0, x1, y1), outline=colour, width=1)
        draw.text((x0 + 1, max(0, y0 - 9)), f"C{index:03d}", fill=colour)
    buffer = BytesIO()
    overlay.save(buffer, format="PNG", optimize=False, compress_level=9)
    return buffer.getvalue()


def _summary_markdown(
    observation_source: dict[str, Any],
    image_metadata: dict[str, Any],
    candidates: list[dict[str, Any]],
    detections: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    processing_run_id: str,
) -> str:
    detection_by_id = {item["id"]: item for item in detections}
    lines = [
        "# ASA-Astro Candidate Graph Summary",
        "",
        f"- Processing run: `{processing_run_id}`",
        f"- Source SHA-256: `{observation_source['sha256']}`",
        f"- Source dimensions: {image_metadata['width_pixels']} × {image_metadata['height_pixels']} pixels",
        f"- Candidate regions: {len(candidates)}",
        f"- Relationship assertions: {len(edges)}",
        "- Coordinate space: image pixels only",
        "- Physical calibration used: no",
        "- Standing computed: no",
        "- Significance computed: no",
        "",
        "## Candidate regions",
        "",
        "| Candidate | Provisional type | Status | Confidence | Bounding box (px) |",
        "|---|---|---|---:|---|",
    ]
    for candidate in candidates:
        detection = detection_by_id[candidate["detection_ids"][0]]
        bbox = detection["bbox"]
        rendered_bbox = f"x={bbox['x']}, y={bbox['y']}, w={bbox['width']}, h={bbox['height']}"
        lines.append(
            f"| `{candidate['id']}` | `{candidate['candidate_type']}` | `{candidate['classification_status']}` | {candidate['confidence']['value']:.6f} (uncalibrated) | {rendered_bbox} |"
        )
    lines.extend(
        [
            "",
            "## Relationship assertions",
            "",
            "| Edge | Type | Classification | Strength | Confidence | Evidence records |",
            "|---|---|---|---:|---:|---:|",
        ]
    )
    for edge in edges:
        assertion = edge["assertion"]
        lines.append(
            f"| `{edge['id']}` | `{edge['edge_type']}` | `{assertion['relationship_classification']}` | {assertion['relationship_strength']['value']:.6f} | {assertion['confidence']['value']:.6f} (uncalibrated) | {len(assertion['evidence_ids'])} |"
        )
    lines.extend(
        [
            "",
            "## Scientific boundary",
            "",
            "This output is a deterministic image-space candidate graph. A detection is not a confirmed astronomical entity; a relationship assertion is not an established physical relationship. Encoded brightness is neither physical luminosity nor significance. Unknown depth, calibration, identity, and causal structure remain unknown.",
            "",
        ]
    )
    return "\n".join(lines)


def _graphml(graph: dict[str, Any]) -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<graphml xmlns="http://graphml.graphdrawing.org/xmlns">',
        '  <key id="type" for="all" attr.name="type" attr.type="string"/>',
        '  <key id="payload" for="all" attr.name="payload" attr.type="string"/>',
        '  <graph id="candidate-graph" edgedefault="directed">',
    ]
    for node in graph["nodes"]:
        lines.extend(
            [
                f'    <node id="{escape(node["id"])}">',
                f'      <data key="type">{escape(node["node_type"])}</data>',
                f'      <data key="payload">{escape(canonical_json(node["payload"]))}</data>',
                "    </node>",
            ]
        )
    for edge in graph["edges"]:
        lines.extend(
            [
                f'    <edge id="{escape(edge["id"])}" source="{escape(edge["source"])}" target="{escape(edge["target"])}">',
                f'      <data key="type">{escape(edge["edge_type"])}</data>',
                f'      <data key="payload">{escape(canonical_json(edge["assertion"]))}</data>',
                "    </edge>",
            ]
        )
    lines.extend(["  </graph>", "</graphml>", ""])
    return "\n".join(lines)


def process_observation(
    input_path: Path,
    output_directory: Path,
    parameters: DetectionParameters | None = None,
    metadata_path: Path | None = None,
    source_locator: str | None = None,
) -> dict[str, Any]:
    """Process one immutable image input into a new, auditable bundle.

    The function refuses any pre-existing output path and never writes to the input.
    """

    input_path = input_path.resolve()
    output_directory = output_directory.resolve()
    metadata_path = metadata_path.resolve() if metadata_path else None
    if not input_path.is_file():
        raise FileNotFoundError(f"input image does not exist: {input_path}")
    if output_directory.exists():
        raise FileExistsError(f"output path already exists; refusing overwrite: {output_directory}")
    if metadata_path is not None and metadata_path == input_path:
        raise ValueError("image input and associated metadata must be separate files")

    active_parameters = parameters or DetectionParameters()
    active_parameters.validate()
    declared_metadata, metadata_sha256 = _load_declared_metadata(metadata_path)
    source_sha256 = hash_file(input_path)
    software = _software_record()
    run_payload = {
        "source_sha256": source_sha256,
        "associated_metadata_sha256": metadata_sha256,
        "parameters": active_parameters.to_dict(),
        "software": software,
    }
    processing_run_id = stable_id("run", run_payload)
    observation_source_id = stable_id("source", {"sha256": source_sha256})
    provenance_record_id = stable_id("provenance", run_payload)

    with Image.open(input_path) as opened_image:
        opened_image.load()
        source_format = opened_image.format or "UNKNOWN"
        source_mode = opened_image.mode
        source_channels = list(opened_image.getbands())
        source_dimensions = opened_image.size
        working_image = opened_image.convert("RGB")

    media_type = Image.MIME.get(source_format, mimetypes.guess_type(input_path.name)[0] or "application/octet-stream")
    observation_source = {
        **record_metadata("externally_supplied"),
        "id": observation_source_id,
        "provenance_record_id": provenance_record_id,
        "source_type": "image",
        "source_locator": source_locator or f"file:{input_path.name}",
        "source_origin": {
            "status": "declared",
            "value": source_locator or f"file:{input_path.name}",
        },
        "source_version": _declared_value(
            declared_metadata, "source_version", "No source release or version was supplied."
        ),
        "retrieval_time": _declared_value(
            declared_metadata, "retrieval_time", "No authoritative retrieval time was supplied."
        ),
        "use_authority": _declared_value(
            declared_metadata, "source_rights", "No source licence or use authority was supplied."
        ),
        "original_filename": input_path.name,
        "media_type": media_type,
        "sha256": source_sha256,
        "byte_size": input_path.stat().st_size,
        "registration_policy": "content-addressed-copy",
        "integrity_status": "verified_sha256",
        "associated_metadata_sha256": metadata_sha256,
    }
    calibration_status = declared_metadata.get("calibration_status", "unavailable")
    physical_scale_status = declared_metadata.get("physical_scale_status", "unavailable")
    if calibration_status not in {"unavailable", "provided_unverified", "verified"}:
        raise ValueError("declared calibration_status is not supported")
    if physical_scale_status not in {"unavailable", "provided_unverified", "verified"}:
        raise ValueError("declared physical_scale_status is not supported")
    image_metadata = {
        **record_metadata("computed"),
        "id": stable_id("image-meta", {"source": observation_source_id, "dimensions": source_dimensions}),
        "provenance_record_id": provenance_record_id,
        "observation_source_id": observation_source_id,
        "width_pixels": source_dimensions[0],
        "height_pixels": source_dimensions[1],
        "format": source_format,
        "mode": source_mode,
        "channels": source_channels,
        "coordinate_frame": {"status": "declared", "value": "decoded_image_pixel_grid"},
        "epoch": _declared_value(
            declared_metadata, "epoch", "No authoritative observation epoch was supplied."
        ),
        "observing_band": _declared_value(
            declared_metadata, "observing_band", "Encoded RGB channels are not treated as a declared observing band."
        ),
        "calibration_status": calibration_status,
        "physical_scale_status": physical_scale_status,
        "declared_metadata": declared_metadata,
    }
    observation_id = stable_id(
        "observation",
        {"source": observation_source_id, "declared_metadata_sha256": metadata_sha256},
    )
    observation = {
        **record_metadata("externally_supplied"),
        "id": observation_id,
        "provenance_record_id": provenance_record_id,
        "observation_source_id": observation_source_id,
        "acquisition_time": _declared_value(
            declared_metadata, "acquisition_time", "No authoritative acquisition time was supplied."
        ),
        "instrument": _declared_value(
            declared_metadata, "instrument", "No authoritative instrument identity was supplied."
        ),
        "observing_band": image_metadata["observing_band"],
        "coordinate_frame": image_metadata["coordinate_frame"],
        "calibration_references": _declared_string_list(declared_metadata, "calibration_references"),
        "quality_flags": _declared_string_list(declared_metadata, "quality_flags"),
        "use_authority": observation_source["use_authority"],
    }
    detector_output_id = stable_id(
        "detector-output",
        {
            "observation": observation_id,
            "run": processing_run_id,
            "shape": source_dimensions,
            "conversion": "pillow-rgb-decode",
        },
    )
    detector_output = {
        **record_metadata("computed"),
        "id": detector_output_id,
        "provenance_record_id": provenance_record_id,
        "observation_id": observation_id,
        "observation_source_id": observation_source_id,
        "shape": {
            "width": source_dimensions[0],
            "height": source_dimensions[1],
            "channels": 3,
        },
        "encoded_units": "encoded_rgb_8bit",
        "calibration_state": calibration_status,
        "detector_geometry": {
            "status": "declared",
            "value": "decoded_image_pixel_grid",
        },
        "mask_state": {
            "status": "unavailable",
            "value": None,
            "reason": "No detector mask was supplied.",
        },
        "quality_flags": [
            "decoded_representation_not_astronomical_reality",
            "encoded_rgb_not_photometric_flux",
        ],
        "processing_method": {"name": "pillow-rgb-decode", "version": pillow_version},
        "uncertainty": {
            "schema_version": SCHEMA_VERSION,
            "ontology_version": ONTOLOGY_VERSION,
            "record_status": "active",
            "status": "unavailable",
            "target": f"calibrated detector values for {detector_output_id}",
            "method": "declared metadata inspection",
            "notes": ["No calibrated uncertainty array or detector model was supplied."],
            "provenance_inherited_from_parent": True,
        },
    }
    provenance_record = {
        **record_metadata("computed"),
        "id": provenance_record_id,
        "processing_run_id": processing_run_id,
        "output_identifiers": [observation_source_id, observation_id, detector_output_id, image_metadata["id"]],
        "ordered_parent_identifiers": [observation_source_id],
        "input_artifacts": [
            {"role": "source_image", "sha256": source_sha256},
            *([{"role": "associated_metadata", "sha256": metadata_sha256}] if metadata_sha256 else []),
        ],
        "operator_or_executable": "asa-astro-observation-to-graph",
        "software": software,
        "version_context": {
            "schema": SCHEMA_VERSION,
            "ontology": ONTOLOGY_VERSION,
            "relationship_taxonomy": "ASTRO-RELATIONSHIP-TAXONOMY-0001",
            "asa_dependency": "unavailable_not_consumed",
        },
        "parameters": active_parameters.to_dict(),
        "deterministic_seed": {
            "status": "not_applicable",
            "value": None,
            "reason": "The pipeline contains no random operation.",
        },
        "execution_time": {
            "status": "unavailable",
            "value": None,
            "reason": "No trusted execution clock is accepted as an input; omission preserves deterministic bundles.",
        },
        "environment_identifier": stable_id("environment", software),
        "transformations": [
            {"name": "decode", "description": "Decode source image with the recorded Pillow version; do not alter source bytes."},
            {"name": "rgb_conversion", "description": "Convert decoded pixels to RGB for deterministic channel features."},
            {"name": "encoded_luminance", "description": "Compute integer Rec.709-weighted encoded luminance; no physical calibration."},
            {"name": "threshold_segmentation", "description": "Apply documented global bright/core and local dark-deficit thresholds."},
            {"name": "connected_components", "description": "Create deterministic eight-connected pixel regions."},
            {"name": "candidate_grouping", "description": "Assign bounded provisional image-region labels."},
            {"name": "relationship_construction", "description": "Derive image-space edges with evidence, separate strength, and confidence."},
        ],
        "warnings": [
            "ASA dependency is unavailable and is not consumed by this pipeline.",
            "Scientific ground truth, calibrated confidence, physical scale, and authorised catalogue identity are unavailable.",
        ],
        "manual_interventions": [],
    }

    detections, evidence_records, processing_statistics = detect_regions(
        working_image,
        observation_source_id,
        detector_output_id,
        provenance_record_id,
        active_parameters,
    )
    candidates = build_candidates(
        detections, processing_statistics["major_detection_id"], active_parameters
    )
    edges = build_relationships(
        observation_source_id, candidates, detections, active_parameters
    )
    graph = build_graph(observation_source, processing_run_id, candidates, edges)
    provenance_record["output_identifiers"] = sorted(
        {
            observation_source_id,
            observation_id,
            detector_output_id,
            image_metadata["id"],
            provenance_record_id,
            *(detection["id"] for detection in detections),
            *(evidence["id"] for evidence in evidence_records),
            *(candidate["id"] for candidate in candidates),
            *(edge["id"] for edge in edges),
        }
    )
    validate_generated_records(
        observation_source,
        observation,
        detector_output,
        image_metadata,
        detections,
        candidates,
        evidence_records,
        provenance_record,
        graph,
    )

    provenance_bundle = {
        **record_metadata("computed"),
        "processing_run_id": processing_run_id,
        "observation_sources": [observation_source],
        "observations": [observation],
        "detector_outputs": [detector_output],
        "source_image_metadata": [image_metadata],
        "detections": detections,
        "evidence_records": evidence_records,
        "provenance_records": [provenance_record],
        "relationship_assertions": [edge["assertion"] for edge in edges],
        "processing_statistics": processing_statistics,
        "scientific_ground_truth_status": "unavailable",
    }

    output_directory.parent.mkdir(parents=True, exist_ok=True)
    temporary_root = Path(
        tempfile.mkdtemp(prefix=f".{output_directory.name}.tmp-", dir=output_directory.parent)
    )
    try:
        source_directory = temporary_root / "source"
        source_directory.mkdir()
        source_copy = source_directory / f"{source_sha256}{_safe_suffix(input_path)}"
        shutil.copyfile(input_path, source_copy)
        if hash_file(source_copy) != source_sha256:
            raise OSError("content-addressed source copy failed hash verification")

        artifact_paths: list[tuple[Path, str, str]] = [
            (source_copy, "immutable_source_copy", media_type),
        ]
        if metadata_path is not None and metadata_sha256 is not None:
            metadata_copy = source_directory / f"metadata-{metadata_sha256}.json"
            shutil.copyfile(metadata_path, metadata_copy)
            if hash_file(metadata_copy) != metadata_sha256:
                raise OSError("associated metadata copy failed hash verification")
            artifact_paths.append((metadata_copy, "immutable_metadata_copy", "application/json"))

        graph_path = temporary_root / "graph.json"
        provenance_path = temporary_root / "provenance.json"
        summary_path = temporary_root / "summary.md"
        graphml_path = temporary_root / "graph.graphml"
        overlay_path = temporary_root / "overlay.png"
        graph_path.write_bytes(_json_bytes(graph))
        provenance_path.write_bytes(_json_bytes(provenance_bundle))
        summary_path.write_text(
            _summary_markdown(
                observation_source, image_metadata, candidates, detections, edges, processing_run_id
            ),
            encoding="utf-8",
        )
        graphml_path.write_text(_graphml(graph), encoding="utf-8")
        overlay_path.write_bytes(_render_overlay(working_image, candidates, detections))
        artifact_paths.extend(
            [
                (graph_path, "canonical_candidate_graph", "application/json"),
                (provenance_path, "provenance_bundle", "application/json"),
                (summary_path, "human_readable_summary", "text/markdown"),
                (graphml_path, "graph_exchange", "application/graphml+xml"),
                (overlay_path, "diagnostic_overlay", "image/png"),
            ]
        )
        manifest = {
            **record_metadata("computed"),
            "processing_run_id": processing_run_id,
            "source_sha256": source_sha256,
            "parameters_sha256": sha256(canonical_json(active_parameters.to_dict()).encode("utf-8")).hexdigest(),
            "software": software,
            "artifacts": sorted(
                (_artifact(path, temporary_root, role, artifact_media_type) for path, role, artifact_media_type in artifact_paths),
                key=lambda item: item["path"],
            ),
            "manifest_self_digest": "excluded_to_avoid_recursive_digest",
        }
        (temporary_root / "manifest.json").write_bytes(_json_bytes(manifest))
        os.replace(temporary_root, output_directory)
    except Exception:
        shutil.rmtree(temporary_root, ignore_errors=True)
        raise

    return {
        "processing_run_id": processing_run_id,
        "output_directory": str(output_directory),
        "source_sha256": source_sha256,
        "candidate_count": len(candidates),
        "relationship_count": len(edges),
    }
