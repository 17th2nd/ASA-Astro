"""Objective declaration.

Adopts the ASTRO-CONTEXT-MODEL-0001 §2/§3 invariants: every field is explicit,
weights are an immutable identified policy, the declaration is content-identified
and immutable once used, and no objective may grant brightness or proximity an
implicit relevance (those inputs must be declared as features with a rationale).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from astro.domain.entities import ENTITY_KINDS
from astro.domain.evidence import EVIDENCE_KINDS
from astro.domain.identity import content_id, freeze_mapping, thaw
from astro.domain.relationships import RELATIONSHIP_TYPES

PURPOSE_CLASSES = ("follow_up", "survey", "monitoring", "calibration", "characterisation", "discovery")
MISSINGNESS_POLICIES = ("indeterminate", "zero_with_trace")
UNEVALUATED_POLICIES = ("exclude", "include")
OUTPUT_SEMANTICS = {
    "direction": "higher_is_more_significant",
    "range": "[0, 1]",
    "tie_rule": "entity_id_ascending",
    "comparable_across_objectives": False,
    "meaning": "relevance to this objective's question in this context; not importance in general",
}


class ObjectiveError(ValueError):
    """The objective declaration is incomplete or invalid."""


@dataclass(frozen=True, slots=True)
class FeatureSpec:
    """One declared feature: a named Astro feature function with weight, parameters and a rationale."""

    name: str
    weight: float
    rationale: str
    required: bool = False
    params: tuple[tuple[str, Any], ...] = ()

    @property
    def param_map(self) -> dict[str, Any]:
        return thaw(self.params)

    def to_record(self) -> dict[str, Any]:
        return {"name": self.name, "weight": self.weight, "rationale": self.rationale, "required": self.required, "params": self.param_map}

    @classmethod
    def from_record(cls, r: Mapping[str, Any]) -> "FeatureSpec":
        if not r.get("rationale"):
            raise ObjectiveError(f"feature {r.get('name')!r} has no scientific rationale")
        if float(r["weight"]) < 0:
            raise ObjectiveError(f"feature {r['name']!r} weight must be non-negative")
        return cls(r["name"], float(r["weight"]), r["rationale"], bool(r.get("required", False)), freeze_mapping(r.get("params") or {}))


@dataclass(frozen=True, slots=True)
class Objective:
    objective_id: str
    name: str
    version: str
    purpose_class: str
    question: str
    authority: str
    target_kinds: tuple[str, ...]
    required_evidence: tuple[str, ...]
    eligible_relationship_types: tuple[str, ...]
    unevaluated_relationships: str
    features: tuple[FeatureSpec, ...]
    weighting_policy_ref: str
    missingness_policy: str
    exclusions: tuple[str, ...]
    explanation_threshold: float
    plan: tuple[tuple[str, Any], ...]

    @classmethod
    def declare(
        cls,
        *,
        name: str,
        version: str,
        purpose_class: str,
        question: str,
        authority: str,
        target_kinds: list[str] | tuple[str, ...],
        features: list[FeatureSpec | Mapping[str, Any]],
        required_evidence: list[str] | tuple[str, ...] = (),
        eligible_relationship_types: list[str] | tuple[str, ...] = (),
        unevaluated_relationships: str = "exclude",
        missingness_policy: str = "indeterminate",
        exclusions: list[str] | tuple[str, ...] = (),
        explanation_threshold: float = 0.25,
        plan: Mapping[str, Any] | None = None,
    ) -> "Objective":
        if purpose_class not in PURPOSE_CLASSES:
            raise ObjectiveError(f"purpose_class {purpose_class!r} not in {PURPOSE_CLASSES}")
        if missingness_policy not in MISSINGNESS_POLICIES:
            raise ObjectiveError(f"missingness_policy {missingness_policy!r} invalid")
        if unevaluated_relationships not in UNEVALUATED_POLICIES:
            raise ObjectiveError(f"unevaluated_relationships {unevaluated_relationships!r} invalid")
        for k in target_kinds:
            if k not in ENTITY_KINDS:
                raise ObjectiveError(f"target kind {k!r} unknown")
        for k in required_evidence:
            if k not in EVIDENCE_KINDS:
                raise ObjectiveError(f"required evidence kind {k!r} unknown")
        for t in eligible_relationship_types:
            if t not in RELATIONSHIP_TYPES:
                raise ObjectiveError(f"relationship type {t!r} unknown")
        if not question or not authority or not name or not version:
            raise ObjectiveError("name, version, question and authority are required")
        specs = tuple(f if isinstance(f, FeatureSpec) else FeatureSpec.from_record(f) for f in features)
        if not specs:
            raise ObjectiveError("an objective declares at least one feature")
        names = [s.name for s in specs]
        if len(set(names)) != len(names):
            raise ObjectiveError("duplicate feature declaration")
        if sum(s.weight for s in specs) <= 0:
            raise ObjectiveError("total feature weight must be positive")
        plan_rec = dict(plan or {"action": "observe", "max_targets": 3, "duration_minutes": 30})
        weighting_ref = content_id("WPOL", [s.to_record() for s in specs])
        body = {
            "name": name, "version": version, "purpose_class": purpose_class, "question": question, "authority": authority,
            "target_kinds": sorted(target_kinds), "required_evidence": sorted(required_evidence),
            "eligible_relationship_types": sorted(eligible_relationship_types), "unevaluated_relationships": unevaluated_relationships,
            "features": [s.to_record() for s in specs], "weighting_policy_ref": weighting_ref,
            "missingness_policy": missingness_policy, "exclusions": sorted(exclusions),
            "explanation_threshold": explanation_threshold, "plan": plan_rec, "output_semantics": OUTPUT_SEMANTICS,
        }
        return cls(
            objective_id=content_id("OBJ", body), name=name, version=version, purpose_class=purpose_class, question=question,
            authority=authority, target_kinds=tuple(sorted(target_kinds)), required_evidence=tuple(sorted(required_evidence)),
            eligible_relationship_types=tuple(sorted(eligible_relationship_types)), unevaluated_relationships=unevaluated_relationships,
            features=specs, weighting_policy_ref=weighting_ref, missingness_policy=missingness_policy,
            exclusions=tuple(sorted(exclusions)), explanation_threshold=explanation_threshold, plan=freeze_mapping(plan_rec),
        )

    @property
    def plan_map(self) -> dict[str, Any]:
        return thaw(self.plan)

    @property
    def total_weight(self) -> float:
        return sum(s.weight for s in self.features)

    def to_record(self) -> dict[str, Any]:
        return {
            "objective_id": self.objective_id, "name": self.name, "version": self.version, "purpose_class": self.purpose_class,
            "question": self.question, "authority": self.authority, "target_kinds": list(self.target_kinds),
            "required_evidence": list(self.required_evidence), "eligible_relationship_types": list(self.eligible_relationship_types),
            "unevaluated_relationships": self.unevaluated_relationships, "features": [s.to_record() for s in self.features],
            "weighting_policy_ref": self.weighting_policy_ref, "missingness_policy": self.missingness_policy,
            "exclusions": list(self.exclusions), "explanation_threshold": self.explanation_threshold,
            "plan": self.plan_map, "output_semantics": OUTPUT_SEMANTICS,
        }

    @classmethod
    def from_record(cls, r: Mapping[str, Any]) -> "Objective":
        obj = cls.declare(
            name=r["name"], version=r["version"], purpose_class=r["purpose_class"], question=r["question"], authority=r["authority"],
            target_kinds=r["target_kinds"], features=r["features"], required_evidence=r.get("required_evidence", ()),
            eligible_relationship_types=r.get("eligible_relationship_types", ()),
            unevaluated_relationships=r.get("unevaluated_relationships", "exclude"),
            missingness_policy=r.get("missingness_policy", "indeterminate"), exclusions=r.get("exclusions", ()),
            explanation_threshold=float(r.get("explanation_threshold", 0.25)), plan=r.get("plan"),
        )
        if r.get("objective_id") and r["objective_id"] != obj.objective_id:
            raise ObjectiveError(f"objective_id {r['objective_id']} does not match content identity {obj.objective_id}")
        return obj
