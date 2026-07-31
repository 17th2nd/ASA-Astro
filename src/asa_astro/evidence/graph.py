"""Evidence-stage candidate grouping and image-space assertion construction."""

from __future__ import annotations

from itertools import combinations
import math
from typing import Any

from .models import (
    DetectionParameters,
    estimated_uncertainty,
    record_metadata,
    stable_id,
    uncalibrated_confidence,
)


FORBIDDEN_PHYSICAL_RELATIONSHIPS = {
    "causal",
    "evolutionary",
    "gravitational",
    "orbital",
    "physical_distance",
}

RELATIONSHIP_SEMANTICS = {
    "proximity": ("spatial", "symmetric", "image_region_peer", "image_region_peer"),
    "overlap": ("spatial", "symmetric", "overlapping_region", "overlapping_region"),
    "containment": ("containment", "directed", "contained_image_region", "container_image_region"),
    "orientation_alignment": ("spatial", "symmetric", "aligned_region", "aligned_region"),
    "morphological_association": ("structural", "symmetric", "morphology_peer", "morphology_peer"),
    "occlusion": ("occlusion", "directed", "possible_occluding_region", "possibly_occluded_region"),
    "shared_structural_region": ("structural", "directed", "represented_region", "major_image_region"),
    "observational_dependency": ("observational", "directed", "derived_representation", "observation_source"),
}


def _candidate_type(
    detection: dict[str, Any], major_detection_id: str | None, parameters: DetectionParameters
) -> tuple[str, str, float, list[str]]:
    observed = detection["provisional_observation_class"]
    confidence = detection["segmentation_confidence"]["value"]
    hypothesis_cap = parameters.maximum_hypothesis_confidence
    flags = set(detection["flags"])
    basis = [f"Derived from detection {detection['id']} classified as {observed}."]

    if "possible_diffraction_spike_contamination" in flags:
        return (
            "unknown_image_region",
            "unknown",
            min(confidence, hypothesis_cap),
            basis + ["Elongated low-fill morphology is compatible with imaging artefact contamination."],
        )
    if detection["id"] == major_detection_id:
        return (
            "primary_extended_object",
            "provisional",
            min(confidence, 0.8),
            basis + ["Largest segmented extended image region in this processing run; not a system-centre claim."],
        )
    if observed == "internal_luminous_substructure":
        return (
            "internal_substructure",
            "provisional",
            min(confidence, 0.7),
            basis + ["High-threshold core lies within a lower-threshold extended segmentation."],
        )
    if observed == "bright_point_like_region":
        peak = detection["features"]["peak_intensity"]["value"]
        if peak >= parameters.foreground_peak_min:
            return (
                "likely_foreground_point_source",
                "hypothesis",
                min(confidence * 0.55, hypothesis_cap),
                basis + ["Bright compact morphology is only a foreground-candidate heuristic; depth is unavailable."],
            )
        return (
            "unresolved_background_object_candidate",
            "hypothesis",
            min(confidence * 0.45, hypothesis_cap),
            basis + ["Unresolved image morphology does not establish identity or depth."],
        )
    if observed == "extended_luminous_region":
        distance = detection["features"]["distance_from_major_structure"]["value"]
        if distance is not None and distance <= parameters.proximity_radius_pixels * 2:
            return (
                "possible_companion_object",
                "hypothesis",
                min(confidence * 0.55, hypothesis_cap),
                basis + ["Image-space proximity to the major extended region does not establish a physical association."],
            )
        return (
            "background_extended_object",
            "hypothesis",
            min(confidence * 0.4, hypothesis_cap),
            basis + ["Separate extended morphology is present; background placement is not established from one image."],
        )
    if observed == "diffuse_luminous_region":
        return (
            "diffuse_or_uncertain_region",
            "unknown",
            min(confidence, 0.55),
            basis + ["Low-contrast extended segmentation is retained without astronomical identity."],
        )
    if observed == "dark_or_occluding_region":
        return (
            "dark_or_occluding_region",
            "hypothesis",
            min(confidence * 0.6, hypothesis_cap),
            basis + ["Local encoded-intensity deficit is not proof of physical occlusion or visible-matter absence."],
        )
    return (
        "unknown_image_region",
        "unknown",
        min(confidence, 0.5),
        basis + ["No more specific bounded image-region label was supported."],
    )


def build_candidates(
    detections: list[dict[str, Any]], major_detection_id: str | None, parameters: DetectionParameters
) -> list[dict[str, Any]]:
    candidates = []
    for detection in detections:
        candidate_type, status, confidence, basis = _candidate_type(
            detection, major_detection_id, parameters
        )
        candidate_id = stable_id("candidate", {"detection_ids": [detection["id"]], "type": candidate_type})
        candidates.append(
            {
                **record_metadata("inferred"),
                "id": candidate_id,
                "provenance_record_id": detection["provenance_record_id"],
                "candidate_type": candidate_type,
                "classification_status": status,
                "resolution_state": "unresolved",
                "representation_space": "image_region",
                "source_representation_ids": [detection["id"]],
                "detection_ids": [detection["id"]],
                "supporting_evidence_ids": [detection["evidence_record_id"]],
                "contradicting_evidence_ids": [],
                "alternative_candidate_ids": [],
                "confidence": uncalibrated_confidence(
                    confidence,
                    f"detection {detection['id']} supports provisional candidate type {candidate_type}",
                    "bounded image-morphology grouping heuristic",
                    [detection["evidence_record_id"]],
                ),
                "uncertainty": estimated_uncertainty(
                    confidence,
                    "bounded image-morphology grouping heuristic",
                    "Candidate labels are provisional representations, not confirmed astronomical entities.",
                    target=f"candidate grouping proposition for {candidate_id}",
                ),
                "inference_basis": basis,
            }
        )
    return sorted(candidates, key=lambda item: item["id"])


def _bbox_area(bbox: dict[str, Any]) -> int:
    return bbox["width"] * bbox["height"]


def _intersection_area(left: dict[str, Any], right: dict[str, Any]) -> int:
    x_overlap = max(0, min(left["x"] + left["width"], right["x"] + right["width"]) - max(left["x"], right["x"]))
    y_overlap = max(0, min(left["y"] + left["height"], right["y"] + right["height"]) - max(left["y"], right["y"]))
    return x_overlap * y_overlap


def _centroid_inside(inner: dict[str, Any], outer: dict[str, Any]) -> bool:
    return (
        outer["x"] <= inner["x"] < outer["x"] + outer["width"]
        and outer["y"] <= inner["y"] < outer["y"] + outer["height"]
    )


def _angle_difference(left: float, right: float) -> float:
    difference = abs(left - right) % 180
    return min(difference, 180 - difference)


def _relationship(
    source: str,
    target: str,
    relationship_subtype: str,
    classification: str,
    status: str,
    strength: float,
    strength_unit: str,
    strength_derivation: str,
    confidence: float,
    evidence_ids: list[str],
    basis: list[str],
    provenance_record_id: str,
) -> dict[str, Any]:
    if relationship_subtype in FORBIDDEN_PHYSICAL_RELATIONSHIPS:
        raise ValueError(f"physical relationship is outside pipeline scope: {relationship_subtype}")
    if relationship_subtype not in RELATIONSHIP_SEMANTICS:
        raise ValueError(f"unsupported relationship subtype: {relationship_subtype}")
    relationship_type, directionality, source_role, target_role = RELATIONSHIP_SEMANTICS[relationship_subtype]
    bounded_confidence = max(0.0, min(1.0, confidence))
    resolved_evidence_ids = sorted(set(evidence_ids))
    assertion_payload = {
        "source": source,
        "target": target,
        "type": relationship_type,
        "subtype": relationship_subtype,
        "evidence_ids": resolved_evidence_ids,
        "strength": round(strength, 6),
    }
    assertion_id = stable_id("relation", assertion_payload)
    assertion = {
        **record_metadata("inferred" if status == "hypothesis" else "computed"),
        "id": assertion_id,
        "provenance_record_id": provenance_record_id,
        "taxonomy_version": "ASTRO-RELATIONSHIP-TAXONOMY-0001",
        "claimant_method": "asa-astro-observation-to-graph-image-heuristic",
        "source_node_id": source,
        "target_node_id": target,
        "source_role": source_role,
        "target_role": target_role,
        "directionality": directionality,
        "relationship_type": relationship_type,
        "relationship_subtype": relationship_subtype,
        "relationship_classification": classification,
        "coordinate_space": "image_pixel",
        "reference_frame": {"status": "declared", "value": "decoded_image_pixel_grid"},
        "epoch": {"status": "unavailable", "value": None, "reason": "No authorised observation epoch was supplied."},
        "observing_band": {"status": "unavailable", "value": None, "reason": "Encoded RGB is not treated as a declared astronomy band."},
        "observer": {"status": "unavailable", "value": None, "reason": "Observer/line-of-sight metadata was not supplied."},
        "status": status,
        "relationship_strength": {
            "value": round(strength, 6),
            "unit": strength_unit,
            "derivation": strength_derivation,
            "calibrated": False,
        },
        "confidence": uncalibrated_confidence(
            bounded_confidence,
            f"evidence supports {relationship_subtype} between {source} and {target}",
            "relationship-specific deterministic image-space heuristic",
            resolved_evidence_ids,
        ),
        "evidence_ids": resolved_evidence_ids,
        "supporting_evidence_ids": resolved_evidence_ids,
        "contradicting_evidence_ids": [],
        "contextual_evidence_ids": [],
        "inference_basis": basis,
        "physical_claim": False,
        "uncertainty": estimated_uncertainty(
            bounded_confidence,
            "relationship-specific deterministic image-space heuristic",
            "Relationship strength is separate from confidence.",
            "No gravitational, orbital, causal, evolutionary, or physical-distance relation is asserted.",
            target=f"relationship assertion {assertion_id}",
        ),
    }
    return {
        **record_metadata("computed"),
        "id": assertion_id,
        "edge_type": relationship_subtype,
        "source": source,
        "target": target,
        "assertion": assertion,
    }


def build_relationships(
    observation_source_id: str,
    candidates: list[dict[str, Any]],
    detections: list[dict[str, Any]],
    parameters: DetectionParameters,
) -> list[dict[str, Any]]:
    detection_by_id = {item["id"]: item for item in detections}
    detection_for_candidate = {
        candidate["id"]: detection_by_id[candidate["detection_ids"][0]] for candidate in candidates
    }
    provenance_record_id = detections[0]["provenance_record_id"] if detections else ""
    edges: list[dict[str, Any]] = []

    for candidate in candidates:
        edges.append(
            _relationship(
                candidate["id"],
                observation_source_id,
                "observational_dependency",
                "dependency",
                "derived",
                1.0,
                "dependency_fraction",
                "candidate has one or more detections derived from this observation source",
                1.0,
                candidate["supporting_evidence_ids"],
                ["Candidate representation depends directly on the cited pixel evidence."],
                provenance_record_id,
            )
        )

    for left, right in combinations(candidates, 2):
        left_detection = detection_for_candidate[left["id"]]
        right_detection = detection_for_candidate[right["id"]]
        left_bbox, right_bbox = left_detection["bbox"], right_detection["bbox"]
        left_centroid, right_centroid = left_detection["centroid"], right_detection["centroid"]
        evidence_ids = left["supporting_evidence_ids"] + right["supporting_evidence_ids"]
        distance = math.hypot(
            left_centroid["x"] - right_centroid["x"],
            left_centroid["y"] - right_centroid["y"],
        )
        maximum_distance = parameters.proximity_radius_pixels + max(
            math.hypot(left_bbox["width"], left_bbox["height"]),
            math.hypot(right_bbox["width"], right_bbox["height"]),
        ) / 2
        if distance <= maximum_distance:
            proximity_strength = max(0.0, 1.0 - distance / max(1.0, maximum_distance))
            edges.append(
                _relationship(
                    left["id"], right["id"], "proximity", "image_space_derived", "derived",
                    proximity_strength, "normalized_image_proximity", "one minus centroid distance divided by the parameterized image-space limit",
                    min(left["confidence"]["value"], right["confidence"]["value"], 0.8), evidence_ids,
                    [f"Centroid separation is {distance:.6f} pixels in the decoded image."],
                    provenance_record_id,
                )
            )

        intersection = _intersection_area(left_bbox, right_bbox)
        if intersection:
            union = _bbox_area(left_bbox) + _bbox_area(right_bbox) - intersection
            overlap_strength = intersection / union
            edges.append(
                _relationship(
                    left["id"], right["id"], "overlap", "image_space_derived", "derived",
                    overlap_strength, "bounding_box_iou", "bounding-box intersection divided by union",
                    min(left["confidence"]["value"], right["confidence"]["value"], 0.75), evidence_ids,
                    ["Axis-aligned image-space bounding boxes overlap; segmented pixels may not all overlap."],
                    provenance_record_id,
                )
            )
            containment_fraction = intersection / min(_bbox_area(left_bbox), _bbox_area(right_bbox))
            if containment_fraction >= 0.9:
                if _bbox_area(left_bbox) <= _bbox_area(right_bbox):
                    inner, outer = left, right
                else:
                    inner, outer = right, left
                edges.append(
                    _relationship(
                        inner["id"], outer["id"], "containment", "image_space_derived", "derived",
                        containment_fraction, "bounding_box_containment_fraction", "intersection divided by the smaller bounding-box area",
                        min(inner["confidence"]["value"], outer["confidence"]["value"], 0.7), evidence_ids,
                        ["Containment is based on image-space bounding boxes, not physical enclosure."],
                        provenance_record_id,
                    )
                )

            dark_candidate = next(
                (candidate for candidate in (left, right) if candidate["candidate_type"] == "dark_or_occluding_region"),
                None,
            )
            other_candidate = right if dark_candidate is left else left
            if dark_candidate is not None and other_candidate["candidate_type"] in {
                "primary_extended_object", "possible_companion_object", "background_extended_object", "diffuse_or_uncertain_region"
            }:
                edges.append(
                    _relationship(
                        dark_candidate["id"], other_candidate["id"], "occlusion", "hypothesis", "hypothesis",
                        containment_fraction, "image_overlap_fraction", "bounding-box intersection divided by the smaller bounding-box area",
                        min(dark_candidate["confidence"]["value"], other_candidate["confidence"]["value"], parameters.maximum_hypothesis_confidence), evidence_ids,
                        ["Local intensity deficit overlaps luminous image structure; dust, masking, sensor effects, and processing remain alternatives."],
                        provenance_record_id,
                    )
                )

        left_elongation = left_detection["features"]["elongation"]["value"]
        right_elongation = right_detection["features"]["elongation"]["value"]
        angle_difference = _angle_difference(
            left_detection["features"]["orientation"]["value"],
            right_detection["features"]["orientation"]["value"],
        )
        if left_elongation >= 2 and right_elongation >= 2 and angle_difference <= parameters.orientation_alignment_degrees:
            alignment_strength = 1.0 - angle_difference / parameters.orientation_alignment_degrees
            edges.append(
                _relationship(
                    left["id"], right["id"], "orientation_alignment", "image_space_derived", "derived",
                    alignment_strength, "normalized_orientation_alignment", "one minus acute major-axis angle difference divided by tolerance",
                    min(left["confidence"]["value"], right["confidence"]["value"], 0.65), evidence_ids,
                    [f"Image-plane major-axis angle difference is {angle_difference:.6f} degrees."],
                    provenance_record_id,
                )
            )

        if (
            left_detection["provisional_observation_class"] == right_detection["provisional_observation_class"]
            and distance <= maximum_distance * 2
        ):
            morphology_strength = max(0.0, 1.0 - distance / max(1.0, maximum_distance * 2))
            edges.append(
                _relationship(
                    left["id"], right["id"], "morphological_association", "hypothesis", "hypothesis",
                    morphology_strength, "normalized_morphology_proximity", "shared provisional morphology weighted by image-space proximity",
                    min(left["confidence"]["value"], right["confidence"]["value"], parameters.maximum_hypothesis_confidence), evidence_ids,
                    ["Candidates share a provisional image-morphology label; this does not establish common origin."],
                    provenance_record_id,
                )
            )

    primary = next((candidate for candidate in candidates if candidate["candidate_type"] == "primary_extended_object"), None)
    if primary is not None:
        primary_detection = detection_for_candidate[primary["id"]]
        for candidate in candidates:
            if candidate["id"] == primary["id"]:
                continue
            detection = detection_for_candidate[candidate["id"]]
            if _centroid_inside(detection["centroid"], primary_detection["bbox"]):
                evidence_ids = candidate["supporting_evidence_ids"] + primary["supporting_evidence_ids"]
                edges.append(
                    _relationship(
                        candidate["id"], primary["id"], "shared_structural_region", "hypothesis", "hypothesis",
                        1.0, "centroid_in_bounding_box", "candidate centroid falls within the major structure bounding box",
                        min(candidate["confidence"]["value"], primary["confidence"]["value"], parameters.maximum_hypothesis_confidence), evidence_ids,
                        ["Shared image region is provisional and does not establish membership in one astronomical system."],
                        provenance_record_id,
                    )
                )

    unique_edges = {edge["id"]: edge for edge in edges}
    return sorted(unique_edges.values(), key=lambda item: item["id"])


def build_graph(
    observation_source: dict[str, Any],
    processing_run_id: str,
    candidates: list[dict[str, Any]],
    edges: list[dict[str, Any]],
) -> dict[str, Any]:
    nodes = [
        {
            **record_metadata("computed"),
            "id": observation_source["id"],
            "node_type": "observation_source",
            "payload": observation_source,
        }
    ]
    nodes.extend(
        {
            **record_metadata("computed"),
            "id": candidate["id"],
            "node_type": "candidate_entity",
            "payload": candidate,
        }
        for candidate in candidates
    )
    return {
        **record_metadata("computed"),
        "processing_run_id": processing_run_id,
        "source_sha256": observation_source["sha256"],
        "coordinate_space": "image_pixel",
        "nodes": sorted(nodes, key=lambda item: item["id"]),
        "edges": edges,
        "limitations": [
            "Nodes represent an observation source and provisional image-region candidates, not confirmed astronomical entities.",
            "All geometry and distance values are image-space pixels; no physical distance is inferred.",
            "Encoded pixel intensity is not calibrated luminosity and is not significance.",
            "Relationship strength and confidence are separate; neither is a standing or significance value.",
            "No gravitational, orbital, causal, or evolutionary relationship is emitted.",
            "No standing or context-dependent significance computation is performed by this pipeline.",
        ],
    }
