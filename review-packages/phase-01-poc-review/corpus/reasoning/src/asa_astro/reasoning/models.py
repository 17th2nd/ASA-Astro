"""Versioned constants and deterministic helpers for the reasoning proof of concept.

These values are ASA-Astro test hypotheses.  They are not ASA definitions and do
not close any item in the repository decision register.
"""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
from typing import Any

from asa_astro.evidence.models import canonical_json, stable_id


REASONING_SCHEMA_VERSION = "0.1.0"
ALGORITHM_VERSION = "asa-astro-reasoning-poc-0.1.0"
ONTOLOGY_VERSION = "ASTRO-ONTOLOGY-0001"
TAXONOMY_VERSION = "ASTRO-RELATIONSHIP-TAXONOMY-0001"
ASA_DEPENDENCY_STATUS = "unavailable_not_consumed"

RELATIONSHIP_TYPES = frozenset(
    {
        "spatial",
        "gravitational",
        "orbital",
        "containment",
        "membership",
        "structural",
        "causal",
        "energetic",
        "radiative",
        "compositional",
        "temporal",
        "developmental",
        "lineage_or_shared_origin",
        "observational",
        "occlusion",
        "uncertainty_dependency",
        "inferred_dark_matter_mediated",
    }
)

# Provisional factors make the evidence-stage status materially affect results.
# They are deliberately replaceable and are documented in ASTRO-SIGNIFICANCE-MODEL-0001.
ASSERTION_CLASS_FACTORS = {
    "image_space_derived": 0.70,
    "hypothesis": 0.35,
    "dependency": 0.90,
}

RELATIONSHIP_PERSISTENCE = {
    "spatial": 0.35,
    "containment": 0.75,
    "structural": 0.70,
    "observational": 0.95,
    "occlusion": 0.40,
}

EVIDENCE_STATUS_FACTORS = {
    "active": 0.90,
    "admissible": 1.00,
    "limited": 0.65,
    "contested": 0.35,
    "invalid": 0.00,
    "rejected": 0.00,
    "superseded": 0.20,
    "unavailable": 0.00,
    "uncalibrated": 0.55,
}

_STANDING_POLICY = {
    "policy_id": "standing-policy-provisional-0001",
    "policy_version": "0.1.0",
    "authority_status": "provisional_non_canonical",
    "asa_dependency_status": ASA_DEPENDENCY_STATUS,
    "normalisation_method": "max",
    "component_weights": {
        "typed_degree": 0.12,
        "weighted_connectivity": 0.18,
        "eigenvector_influence": 0.14,
        "betweenness": 0.12,
        "containment_hierarchy": 0.10,
        "relationship_persistence": 0.10,
        "evidence_support": 0.14,
        "structural_dependency": 0.10,
    },
    "uncertainty_penalty_weight": 0.35,
    "centrality_max_iterations": 64,
    "centrality_tolerance": 1e-12,
    "notes": [
        "Proof-of-concept hypothesis only; not an ASA Standing contract.",
        "No Context field is consumed by this policy.",
        "Encoded brightness, pixel area, and candidate class are excluded.",
    ],
}


def standing_policy() -> dict[str, Any]:
    """Return an independent copy of the explicit provisional Standing policy."""

    return deepcopy(_STANDING_POLICY)


def content_sha256(value: Any) -> str:
    """Hash a JSON-compatible value using the repository canonical JSON encoding."""

    return sha256(canonical_json(value).encode("utf-8")).hexdigest()


def bounded(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def score(value: float) -> float:
    return round(bounded(value), 12)


def result_id(prefix: str, payload: Any) -> str:
    return stable_id(prefix, {"algorithm": ALGORITHM_VERSION, "payload": payload})
