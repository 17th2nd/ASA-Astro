"""Transparent evidence-stage image-space segmentation and feature extraction.

This module makes no astronomical identity or physical-distance claims.  Its outputs
are pixel-region detections with explicit heuristic provenance.
"""

from __future__ import annotations

from collections.abc import Iterable
import math
from statistics import median
from typing import Any

from PIL import Image, ImageFilter

from .models import (
    DetectionParameters,
    estimated_uncertainty,
    record_metadata,
    stable_id,
    uncalibrated_confidence,
)


Coordinate = tuple[int, int]


def _clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return max(lower, min(upper, value))


def _luminance(rgb: tuple[int, int, int]) -> int:
    red, green, blue = rgb
    return (2126 * red + 7152 * green + 722 * blue + 5000) // 10000


def _connected_components(
    mask: list[bool], width: int, height: int, minimum_pixels: int
) -> list[list[Coordinate]]:
    visited = bytearray(width * height)
    components: list[list[Coordinate]] = []
    neighbours = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))

    for start in range(width * height):
        if visited[start] or not mask[start]:
            continue
        visited[start] = 1
        stack = [start]
        component: list[Coordinate] = []
        while stack:
            index = stack.pop()
            y, x = divmod(index, width)
            component.append((x, y))
            for dx, dy in neighbours:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    neighbour_index = ny * width + nx
                    if mask[neighbour_index] and not visited[neighbour_index]:
                        visited[neighbour_index] = 1
                        stack.append(neighbour_index)
        if len(component) >= minimum_pixels:
            component.sort(key=lambda item: (item[1], item[0]))
            components.append(component)
    return components


def _bbox(component: Iterable[Coordinate]) -> dict[str, Any]:
    points = list(component)
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    minimum_x, maximum_x = min(xs), max(xs)
    minimum_y, maximum_y = min(ys), max(ys)
    return {
        "x": minimum_x,
        "y": minimum_y,
        "width": maximum_x - minimum_x + 1,
        "height": maximum_y - minimum_y + 1,
        "unit": "pixel",
    }


def _ring_background(
    bbox: dict[str, Any], luminance: list[int], width: int, height: int, fallback: float
) -> float:
    x0 = max(0, bbox["x"] - 3)
    y0 = max(0, bbox["y"] - 3)
    x1 = min(width, bbox["x"] + bbox["width"] + 3)
    y1 = min(height, bbox["y"] + bbox["height"] + 3)
    bx0, by0 = bbox["x"], bbox["y"]
    bx1, by1 = bx0 + bbox["width"], by0 + bbox["height"]
    ring = [
        luminance[y * width + x]
        for y in range(y0, y1)
        for x in range(x0, x1)
        if not (bx0 <= x < bx1 and by0 <= y < by1)
    ]
    return float(median(ring)) if ring else float(fallback)


def _component_features(
    component: list[Coordinate],
    rgb_pixels: list[tuple[int, int, int]],
    luminance: list[int],
    width: int,
    height: int,
    global_background: float,
    dark: bool,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    bbox = _bbox(component)
    local_background = _ring_background(bbox, luminance, width, height, global_background)
    indices = [y * width + x for x, y in component]
    values = [luminance[index] for index in indices]
    weights = [max(1.0, local_background - value if dark else value - local_background) for value in values]
    weight_sum = sum(weights)
    centroid_x = sum(point[0] * weight for point, weight in zip(component, weights)) / weight_sum
    centroid_y = sum(point[1] * weight for point, weight in zip(component, weights)) / weight_sum

    covariance_xx = sum(weight * (point[0] - centroid_x) ** 2 for point, weight in zip(component, weights)) / weight_sum
    covariance_yy = sum(weight * (point[1] - centroid_y) ** 2 for point, weight in zip(component, weights)) / weight_sum
    covariance_xy = sum(
        weight * (point[0] - centroid_x) * (point[1] - centroid_y)
        for point, weight in zip(component, weights)
    ) / weight_sum
    discriminant = math.sqrt(max(0.0, (covariance_xx - covariance_yy) ** 2 + 4 * covariance_xy**2))
    eigen_major = max(0.0, (covariance_xx + covariance_yy + discriminant) / 2)
    eigen_minor = max(0.0, (covariance_xx + covariance_yy - discriminant) / 2)
    elongation = math.sqrt((eigen_major + 0.25) / (eigen_minor + 0.25))
    orientation = math.degrees(math.atan2(2 * covariance_xy, covariance_xx - covariance_yy) / 2)

    red_values = [rgb_pixels[index][0] for index in indices]
    green_values = [rgb_pixels[index][1] for index in indices]
    blue_values = [rgb_pixels[index][2] for index in indices]
    area = len(component)
    fill_ratio = area / (bbox["width"] * bbox["height"])
    mean_intensity = sum(values) / area
    net_intensity = sum((local_background - value) if dark else (value - local_background) for value in values)
    features = {
        "area_pixels": area,
        "integrated_intensity": {
            "value": round(sum(values), 6),
            "unit": "encoded_luminance_8bit_sum",
            "derivation": "sum of deterministic Rec.709 integer luminance over segmented pixels",
            "calibrated": False,
        },
        "background_adjusted_intensity": {
            "value": round(net_intensity, 6),
            "unit": "encoded_luminance_8bit_sum",
            "derivation": "segmented-pixel luminance minus local ring median; sign reversed for dark deficit",
            "calibrated": False,
        },
        "peak_intensity": {
            "value": min(values) if dark else max(values),
            "unit": "encoded_luminance_8bit",
            "derivation": "minimum for dark deficit or maximum for luminous segmentation",
            "calibrated": False,
        },
        "mean_intensity": {
            "value": round(mean_intensity, 6),
            "unit": "encoded_luminance_8bit",
            "derivation": "arithmetic mean over segmented pixels",
            "calibrated": False,
        },
        "local_background_estimate": {
            "value": round(local_background, 6),
            "unit": "encoded_luminance_8bit",
            "derivation": "median of a three-pixel ring around the bounding box",
            "calibrated": False,
        },
        "mean_red": {"value": round(sum(red_values) / area, 6), "unit": "encoded_channel_8bit", "derivation": "mean source RGB red channel", "calibrated": False},
        "mean_green": {"value": round(sum(green_values) / area, 6), "unit": "encoded_channel_8bit", "derivation": "mean source RGB green channel", "calibrated": False},
        "mean_blue": {"value": round(sum(blue_values) / area, 6), "unit": "encoded_channel_8bit", "derivation": "mean source RGB blue channel", "calibrated": False},
        "extent": {"value": round(fill_ratio, 6), "unit": "fraction_of_bounding_box", "derivation": "segmented area divided by bounding-box area", "calibrated": False},
        "orientation": {"value": round(orientation, 6), "unit": "degree_image_axis", "derivation": "major eigenvector of intensity-weighted pixel covariance", "calibrated": False},
        "elongation": {"value": round(elongation, 6), "unit": "axis_ratio", "derivation": "square root of regularized covariance eigenvalue ratio", "calibrated": False},
        "local_density": {"value": None, "unit": "detections_per_pixel_squared", "derivation": "populated after all detections are known", "calibrated": False},
        "distance_from_major_structure": {"value": None, "unit": "pixel", "derivation": "populated after the provisional major image structure is selected", "calibrated": False},
    }
    centroid = {"x": round(centroid_x, 6), "y": round(centroid_y, 6), "unit": "pixel"}
    return bbox, centroid, features


def _classify_bright(features: dict[str, Any], parameters: DetectionParameters) -> str:
    area = features["area_pixels"]
    elongation = features["elongation"]["value"]
    contrast = features["mean_intensity"]["value"] - features["local_background_estimate"]["value"]
    if area <= parameters.point_max_pixels and elongation < parameters.diffraction_elongation_min:
        return "bright_point_like_region"
    if area >= parameters.diffuse_min_pixels and contrast < parameters.bright_min_delta * 2.0:
        return "diffuse_luminous_region"
    if area >= parameters.extended_min_pixels:
        return "extended_luminous_region"
    return "unresolved_luminous_region"


def detect_regions(
    image: Image.Image,
    observation_source_id: str,
    detector_output_id: str,
    provenance_record_id: str,
    parameters: DetectionParameters,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    """Detect image regions and emit provenance-linked records.

    The algorithm is deterministic for a decoded RGB pixel array and parameter set.
    Confidence values are bounded heuristic scores, not empirically calibrated probabilities.
    """

    parameters.validate()
    rgb_image = image.convert("RGB")
    width, height = rgb_image.size
    rgb_pixels = list(rgb_image.getdata())
    luminance = [_luminance(pixel) for pixel in rgb_pixels]
    global_background = float(median(luminance))
    absolute_deviations = [abs(value - global_background) for value in luminance]
    mad = float(median(absolute_deviations))
    robust_sigma = max(1.0, 1.4826 * mad)
    bright_threshold = min(255.0, global_background + max(parameters.bright_min_delta, parameters.bright_sigma * robust_sigma))
    core_threshold = min(255.0, global_background + max(parameters.core_min_delta, parameters.core_sigma * robust_sigma))

    low_mask = [value >= bright_threshold for value in luminance]
    core_mask = [value >= core_threshold for value in luminance]
    low_components = _connected_components(low_mask, width, height, parameters.min_component_pixels)
    core_components = _connected_components(core_mask, width, height, parameters.min_component_pixels)
    low_components = low_components[: parameters.maximum_components_per_pass]
    core_components = core_components[: parameters.maximum_components_per_pass]

    component_records: list[tuple[list[Coordinate], str, bool, str]] = []
    low_sets: list[set[Coordinate]] = []
    low_classes: list[str] = []
    for component in low_components:
        _, _, features = _component_features(component, rgb_pixels, luminance, width, height, global_background, False)
        classification = _classify_bright(features, parameters)
        component_records.append((component, "bright_low_threshold", False, classification))
        low_sets.append(set(component))
        low_classes.append(classification)

    for component in core_components:
        component_set = set(component)
        parent_index = next((index for index, low_set in enumerate(low_sets) if component_set & low_set), None)
        if parent_index is None:
            continue
        parent_area = len(low_components[parent_index])
        if low_classes[parent_index] in {"extended_luminous_region", "diffuse_luminous_region"} and len(component) < parent_area * 0.8:
            component_records.append((component, "bright_core", False, "internal_luminous_substructure"))

    blurred = rgb_image.convert("L").filter(ImageFilter.GaussianBlur(radius=parameters.background_blur_radius))
    blurred_values = list(blurred.getdata())
    dark_mask = [
        blurred_value - value >= parameters.dark_local_delta
        and blurred_value >= global_background + parameters.bright_min_delta
        for value, blurred_value in zip(luminance, blurred_values)
    ]
    dark_components = _connected_components(
        dark_mask, width, height, parameters.dark_min_component_pixels
    )[: parameters.maximum_components_per_pass]
    component_records.extend(
        (component, "dark_local_deficit", True, "dark_or_occluding_region")
        for component in dark_components
    )

    detections: list[dict[str, Any]] = []
    for component, segmentation_kind, dark, classification in component_records:
        bbox, centroid, features = _component_features(
            component, rgb_pixels, luminance, width, height, global_background, dark
        )
        contrast = abs(features["mean_intensity"]["value"] - features["local_background_estimate"]["value"])
        contrast_reference = parameters.dark_local_delta if dark else parameters.bright_min_delta
        area_factor = min(1.0, math.log2(features["area_pixels"] + 1) / 7.0)
        confidence = _clamp(0.2 + 0.45 * min(1.0, contrast / max(1.0, contrast_reference * 2)) + 0.25 * area_factor, 0.05, 0.9)
        flags: list[str] = []
        low_fill_bright_structure = (
            not dark
            and features["peak_intensity"]["value"] >= parameters.foreground_peak_min
            and features["extent"]["value"] <= parameters.diffraction_fill_ratio_max
        )
        if low_fill_bright_structure and (
            features["elongation"]["value"] >= parameters.diffraction_elongation_min
            or features["area_pixels"] > parameters.point_max_pixels
        ):
            flags.append("possible_diffraction_spike_contamination")
            confidence = min(confidence, 0.55)
        if dark:
            flags.append("occlusion_not_established_from_intensity_deficit")
            confidence = min(confidence, 0.6)

        identity_payload = {
            "observation_source_id": observation_source_id,
            "segmentation_kind": segmentation_kind,
            "bbox": bbox,
            "area_pixels": features["area_pixels"],
        }
        detection_id = stable_id("det", identity_payload)
        evidence_id = stable_id("evidence", {"detection_id": detection_id, "provenance": provenance_record_id})
        detections.append(
            {
                **record_metadata("computed"),
                "id": detection_id,
                "provenance_record_id": provenance_record_id,
                "observation_source_id": observation_source_id,
                "detector_output_id": detector_output_id,
                "evidence_record_id": evidence_id,
                "segmentation_kind": segmentation_kind,
                "bbox": bbox,
                "centroid": centroid,
                "features": features,
                "provisional_observation_class": classification,
                "classification_status": "hypothesis" if dark else "provisional",
                "segmentation_confidence": uncalibrated_confidence(
                    confidence,
                    f"pixels satisfy {segmentation_kind} and provisional class {classification}",
                    "unvalidated deterministic threshold and morphology heuristic",
                    [evidence_id],
                ),
                "uncertainty": estimated_uncertainty(
                    confidence,
                    "unvalidated deterministic threshold heuristic",
                    "Confidence is not calibrated against an astronomical source catalogue.",
                    "Classification describes an image region, not a confirmed astronomical entity.",
                    target=f"segmentation and morphology proposition for {detection_id}",
                ),
                "flags": sorted(flags),
            }
        )

    major_candidates = [
        detection
        for detection in detections
        if detection["segmentation_kind"] == "bright_low_threshold"
        and detection["provisional_observation_class"] in {"extended_luminous_region", "diffuse_luminous_region"}
    ]
    major_detection = max(
        major_candidates,
        key=lambda item: (item["features"]["area_pixels"], item["features"]["integrated_intensity"]["value"], item["id"]),
        default=None,
    )
    for detection in detections:
        cx, cy = detection["centroid"]["x"], detection["centroid"]["y"]
        neighbours = sum(
            1
            for other in detections
            if other["id"] != detection["id"]
            and math.hypot(cx - other["centroid"]["x"], cy - other["centroid"]["y"])
            <= parameters.local_density_radius_pixels
        )
        density = neighbours / (math.pi * parameters.local_density_radius_pixels**2)
        detection["features"]["local_density"]["value"] = round(density, 9)
        if major_detection is not None:
            distance = math.hypot(
                cx - major_detection["centroid"]["x"],
                cy - major_detection["centroid"]["y"],
            )
            detection["features"]["distance_from_major_structure"]["value"] = round(distance, 6)

    detections.sort(key=lambda item: item["id"])
    evidence_records = []
    for detection in detections:
        evidence_records.append(
            {
                **record_metadata("computed", "admissible"),
                "id": detection["evidence_record_id"],
                "subject_id": detection["id"],
                "supported_claim": f"Detection {detection['id']} satisfies the recorded image-space segmentation rule.",
                "evidence_role": "supports",
                "observation_source_id": observation_source_id,
                "detector_output_id": detector_output_id,
                "provenance_record_id": provenance_record_id,
                "evidence_kind": "local_intensity_deficit" if detection["segmentation_kind"] == "dark_local_deficit" else "pixel_segmentation",
                "image_region": detection["bbox"],
                "coordinate_context": {
                    "frame": {"status": "declared", "value": "decoded_image_pixel_grid"},
                    "epoch": {"status": "unavailable", "value": None, "reason": "No authorised source epoch was supplied."},
                    "band": {"status": "unavailable", "value": None, "reason": "Encoded RGB channels are not treated as a declared observing band."},
                },
                "measurements": detection["features"],
                "quality_flags": detection["flags"],
                "limitations": [
                    "Evidence is derived from one encoded image representation.",
                    "The segmentation confidence is an uncalibrated heuristic score.",
                    "The evidence does not establish astronomical identity or physical association.",
                ],
                "independence_group": f"source-digest:{observation_source_id}",
                "uncertainty": detection["uncertainty"],
                "derivation": {
                    "method": detection["segmentation_kind"],
                    "parameters": parameters.to_dict(),
                },
            }
        )
    evidence_records.sort(key=lambda item: item["id"])
    statistics = {
        "global_background_median": round(global_background, 6),
        "global_median_absolute_deviation": round(mad, 6),
        "robust_sigma_estimate": round(robust_sigma, 6),
        "bright_threshold": round(bright_threshold, 6),
        "core_threshold": round(core_threshold, 6),
        "major_detection_id": major_detection["id"] if major_detection else None,
        "physical_calibration_used": False,
    }
    return detections, evidence_records, statistics
