"""Deterministic parameters and identifiers for the Codex B evidence pipeline."""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from hashlib import sha256
import json
from typing import Any, Mapping


PIPELINE_VERSION = "0.1.0"
SCHEMA_VERSION = "0.1.0"
ONTOLOGY_VERSION = "ASTRO-ONTOLOGY-0001"


def canonical_json(value: Any) -> str:
    """Return the canonical JSON representation used for identifiers and hashes."""

    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def stable_id(prefix: str, value: Any, length: int = 20) -> str:
    """Create a stable, content-derived identifier."""

    digest = sha256(canonical_json(value).encode("utf-8")).hexdigest()[:length]
    return f"{prefix}-{digest}"


def record_metadata(epistemic_classification: str, record_status: str = "active") -> dict[str, str]:
    """Return common ontology/version/lifecycle fields for a record."""

    return {
        "schema_version": SCHEMA_VERSION,
        "ontology_version": ONTOLOGY_VERSION,
        "epistemic_classification": epistemic_classification,
        "record_status": record_status,
    }


def uncalibrated_confidence(
    value: float,
    target_proposition: str,
    method: str,
    evidence_ids: list[str] | None = None,
) -> dict[str, Any]:
    """Represent an uncalibrated heuristic score without calling it probability."""

    bounded = round(max(0.0, min(1.0, value)), 6)
    return {
        "schema_version": SCHEMA_VERSION,
        "ontology_version": ONTOLOGY_VERSION,
        "record_status": "uncalibrated",
        "value": bounded,
        "scale_semantics": "bounded_heuristic_support_score_0_to_1",
        "target_proposition": target_proposition,
        "method": method,
        "calibration_status": "uncalibrated",
        "evidence_ids": sorted(set(evidence_ids or [])),
        "provenance_inherited_from_parent": True,
    }


def estimated_uncertainty(confidence: float, method: str, *notes: str, target: str = "parent record proposition") -> dict[str, Any]:
    """Represent bounded algorithmic uncertainty without claiming calibration."""

    bounded = round(max(0.0, min(1.0, confidence)), 6)
    return {
        "schema_version": SCHEMA_VERSION,
        "ontology_version": ONTOLOGY_VERSION,
        "record_status": "active",
        "status": "estimated",
        "confidence": bounded,
        "target": target,
        "method": method,
        "notes": list(notes),
        "provenance_inherited_from_parent": True,
    }


def unavailable_uncertainty(method: str, *notes: str) -> dict[str, Any]:
    """Represent information that the image and metadata cannot provide."""

    return {
        "schema_version": SCHEMA_VERSION,
        "ontology_version": ONTOLOGY_VERSION,
        "record_status": "active",
        "status": "unavailable",
        "target": "parent record proposition",
        "method": method,
        "notes": list(notes),
        "provenance_inherited_from_parent": True,
    }


@dataclass(frozen=True)
class DetectionParameters:
    """Explicit, versioned parameters for the transparent baseline detector."""

    bright_sigma: float = 2.5
    bright_min_delta: int = 18
    core_sigma: float = 5.0
    core_min_delta: int = 42
    dark_local_delta: int = 16
    background_blur_radius: float = 5.0
    min_component_pixels: int = 3
    dark_min_component_pixels: int = 4
    point_max_pixels: int = 24
    extended_min_pixels: int = 45
    diffuse_min_pixels: int = 80
    proximity_radius_pixels: float = 16.0
    local_density_radius_pixels: float = 24.0
    orientation_alignment_degrees: float = 15.0
    diffraction_elongation_min: float = 5.0
    diffraction_fill_ratio_max: float = 0.45
    foreground_peak_min: int = 220
    maximum_hypothesis_confidence: float = 0.45
    maximum_components_per_pass: int = 128

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_mapping(cls, values: Mapping[str, Any] | None) -> "DetectionParameters":
        if values is None:
            return cls()
        allowed = {field.name for field in fields(cls)}
        unknown = sorted(set(values) - allowed)
        if unknown:
            raise ValueError(f"unknown detection parameter(s): {', '.join(unknown)}")
        instance = cls(**dict(values))
        instance.validate()
        return instance

    def validate(self) -> None:
        positive = {
            "bright_sigma": self.bright_sigma,
            "bright_min_delta": self.bright_min_delta,
            "core_sigma": self.core_sigma,
            "core_min_delta": self.core_min_delta,
            "dark_local_delta": self.dark_local_delta,
            "background_blur_radius": self.background_blur_radius,
            "min_component_pixels": self.min_component_pixels,
            "dark_min_component_pixels": self.dark_min_component_pixels,
            "point_max_pixels": self.point_max_pixels,
            "extended_min_pixels": self.extended_min_pixels,
            "diffuse_min_pixels": self.diffuse_min_pixels,
            "proximity_radius_pixels": self.proximity_radius_pixels,
            "local_density_radius_pixels": self.local_density_radius_pixels,
            "orientation_alignment_degrees": self.orientation_alignment_degrees,
            "diffraction_elongation_min": self.diffraction_elongation_min,
            "maximum_components_per_pass": self.maximum_components_per_pass,
        }
        bad = [name for name, value in positive.items() if value <= 0]
        if bad:
            raise ValueError(f"parameters must be positive: {', '.join(sorted(bad))}")
        if not 0 < self.diffraction_fill_ratio_max <= 1:
            raise ValueError("diffraction_fill_ratio_max must be in (0, 1]")
        if not 0 <= self.maximum_hypothesis_confidence <= 1:
            raise ValueError("maximum_hypothesis_confidence must be in [0, 1]")
        if self.point_max_pixels >= self.extended_min_pixels:
            raise ValueError("point_max_pixels must be smaller than extended_min_pixels")
