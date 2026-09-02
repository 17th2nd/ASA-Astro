"""Objective-scoped significance evaluation and explanation.

``evaluate`` turns (universe, ASA snapshot, objective, context) into a ranked, fully traced
:class:`SignificanceEvaluation`. ``explain`` renders one entity's result from the recorded
decision state only — no reason may appear that is not in the result record.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from astro import ASTRO_VERSION
from astro.asa.adapter import Edge, RelationalSnapshot
from astro.domain import Entity, EvidenceRecord, Universe
from astro.domain.identity import content_id
from astro.objectives import Objective, ObservingContext
from .features import FEATURES, FeatureInput, FeatureValue

STATUSES = ("eligible", "ineligible", "indeterminate")


@dataclass(frozen=True, slots=True)
class SignificanceResult:
    entity_id: str
    designation: str
    kind: str
    status: str
    score: float | None
    rank: int | None
    contributions: tuple[dict[str, Any], ...]
    eligibility: tuple[dict[str, Any], ...]
    relationship_keys: tuple[str, ...]
    evidence_ids: tuple[str, ...]
    unavailable: tuple[str, ...]

    def to_record(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id, "designation": self.designation, "kind": self.kind, "status": self.status,
            "score": self.score, "rank": self.rank, "contributions": list(self.contributions), "eligibility": list(self.eligibility),
            "relationship_keys": list(self.relationship_keys), "evidence_ids": list(self.evidence_ids), "unavailable": list(self.unavailable),
        }


@dataclass(frozen=True, slots=True)
class SignificanceEvaluation:
    evaluation_id: str
    objective_id: str
    objective_version: str
    context_id: str
    universe_id: str
    asa_baseline: str
    kernel_version: str
    kernel_digest: str
    kernel_head: str
    registry_digest: str
    astro_version: str
    weighting_policy_ref: str
    results: tuple[SignificanceResult, ...]

    def ranked(self) -> tuple[SignificanceResult, ...]:
        return tuple(r for r in self.results if r.status == "eligible")

    def ranking(self) -> tuple[str, ...]:
        return tuple(r.entity_id for r in self.ranked())

    def result_for(self, entity_id: str) -> SignificanceResult:
        for r in self.results:
            if r.entity_id == entity_id:
                return r
        raise KeyError(entity_id)

    def to_record(self) -> dict[str, Any]:
        return {
            "evaluation_id": self.evaluation_id, "objective_id": self.objective_id, "objective_version": self.objective_version,
            "context_id": self.context_id, "universe_id": self.universe_id, "asa_baseline": self.asa_baseline,
            "kernel_version": self.kernel_version, "kernel_digest": self.kernel_digest, "kernel_head": self.kernel_head,
            "registry_digest": self.registry_digest, "astro_version": self.astro_version,
            "weighting_policy_ref": self.weighting_policy_ref, "results": [r.to_record() for r in self.results],
        }


def _eligible_edges(entity_id: str, snapshot: RelationalSnapshot, objective: Objective) -> tuple[tuple[Edge, ...], list[dict[str, Any]]]:
    kept, excluded = [], []
    for e in snapshot.edges_of(entity_id):
        if e.type_name not in objective.eligible_relationship_types:
            excluded.append({"key": e.key, "type": e.type_name, "reason": "type not eligible for this objective"})
        elif e.lifecycle != "registered":
            excluded.append({"key": e.key, "type": e.type_name, "reason": f"lifecycle {e.lifecycle}"})
        elif e.stance != "endorsed" and objective.unevaluated_relationships == "exclude":
            excluded.append({"key": e.key, "type": e.type_name, "reason": f"stance {e.stance}; objective excludes unevaluated relationships"})
        else:
            kept.append(e)
    return tuple(kept), excluded


def _admissible_evidence(entity_id: str, universe: Universe, snapshot: RelationalSnapshot) -> tuple[tuple[EvidenceRecord, ...], list[dict[str, Any]]]:
    kept, excluded = [], []
    registered = {l.evidence_id for l in snapshot.evidence_of(entity_id) if l.stance == "endorsed"}
    for rec in universe.evidence_for(entity_id):
        if rec.evidence_id not in registered:
            excluded.append({"evidence_id": rec.evidence_id, "reason": "not registered in ASA"})
        elif rec.status != "admissible":
            excluded.append({"evidence_id": rec.evidence_id, "reason": f"status {rec.status}"})
        else:
            kept.append(rec)
    return tuple(sorted(kept, key=lambda r: r.evidence_id)), excluded


def _evaluate_entity(entity: Entity, universe: Universe, snapshot: RelationalSnapshot, objective: Objective, context: ObservingContext) -> SignificanceResult:
    eligibility: list[dict[str, Any]] = []
    edges, excluded_edges = _eligible_edges(entity.entity_id, snapshot, objective)
    evidence, excluded_evidence = _admissible_evidence(entity.entity_id, universe, snapshot)
    kind_ok = entity.kind in objective.target_kinds
    eligibility.append({"rule": "target_kind", "passed": kind_ok, "detail": f"kind {entity.kind}; objective targets {list(objective.target_kinds)}"})
    present_kinds = {e.kind for e in evidence}
    missing_required = [k for k in objective.required_evidence if k not in present_kinds]
    eligibility.append({"rule": "required_evidence", "passed": not missing_required,
                        "detail": "missing " + ", ".join(missing_required) if missing_required else "all required evidence kinds registered and admissible"})
    if excluded_edges:
        eligibility.append({"rule": "relationship_policy", "passed": True, "detail": "excluded relationships recorded", "excluded": excluded_edges})
    if excluded_evidence:
        eligibility.append({"rule": "evidence_policy", "passed": True, "detail": "excluded evidence recorded", "excluded": excluded_evidence})
    base = dict(entity_id=entity.entity_id, designation=entity.designation, kind=entity.kind,
                relationship_keys=tuple(e.key for e in edges), evidence_ids=tuple(e.evidence_id for e in evidence),
                eligibility=tuple(eligibility))
    if not kind_ok or missing_required:
        return SignificanceResult(status="ineligible", score=None, rank=None, contributions=(), unavailable=(), **base)

    fi = FeatureInput(entity, universe, snapshot, objective, context, edges, evidence)
    contributions, unavailable = [], []
    weighted, weight_sum = 0.0, 0.0
    indeterminate = False
    for spec in objective.features:
        fn = FEATURES.get(spec.name)
        if fn is None:
            raise ValueError(f"objective declares unknown feature {spec.name!r}")
        fv: FeatureValue = fn(fi, spec.param_map)
        rec = {"feature": spec.name, "weight": spec.weight, "required": spec.required, **fv.to_record()}
        if fv.status == "available" and fv.value is not None:
            rec["contribution"] = round(spec.weight * fv.value, 12)
            weighted += spec.weight * fv.value
            weight_sum += spec.weight
        else:
            rec["contribution"] = None
            unavailable.append(spec.name)
            if spec.required and objective.missingness_policy == "indeterminate":
                indeterminate = True
            elif objective.missingness_policy == "zero_with_trace":
                weight_sum += spec.weight
                rec["contribution"] = 0.0
                rec["trace"] = {**rec["trace"], "missingness": "counted as zero per objective policy"}
        contributions.append(rec)
    if indeterminate:
        return SignificanceResult(status="indeterminate", score=None, rank=None, contributions=tuple(contributions),
                                  unavailable=tuple(unavailable), **base)
    score = round(weighted / weight_sum, 12) if weight_sum > 0 else 0.0
    return SignificanceResult(status="eligible", score=score, rank=None, contributions=tuple(contributions),
                              unavailable=tuple(unavailable), **base)


def evaluate(universe: Universe, snapshot: RelationalSnapshot, objective: Objective, context: ObservingContext) -> SignificanceEvaluation:
    """Evaluate every entity in the universe under the objective and context. Deterministic."""
    results = [_evaluate_entity(e, universe, snapshot, objective, context) for e in universe.entities]
    eligible = sorted((r for r in results if r.status == "eligible"), key=lambda r: (-(r.score or 0.0), r.entity_id))
    ranked_ids = {r.entity_id: i + 1 for i, r in enumerate(eligible)}
    final = []
    for r in sorted(results, key=lambda r: (0 if r.status == "eligible" else 1, ranked_ids.get(r.entity_id, 0), r.entity_id)):
        if r.entity_id in ranked_ids:
            r = _with_rank(r, ranked_ids[r.entity_id])
        final.append(r)
    body = {
        "objective_id": objective.objective_id, "context_id": context.context_id, "universe_id": universe.universe_id,
        "kernel_digest": snapshot.digest, "asa_baseline": snapshot.asa_baseline, "astro_version": ASTRO_VERSION,
        "results": [r.to_record() for r in final],
    }
    return SignificanceEvaluation(
        evaluation_id=content_id("SIG", body), objective_id=objective.objective_id, objective_version=objective.version,
        context_id=context.context_id, universe_id=universe.universe_id, asa_baseline=snapshot.asa_baseline,
        kernel_version=snapshot.kernel_version, kernel_digest=snapshot.digest, kernel_head=snapshot.head,
        registry_digest=snapshot.registry_digest, astro_version=ASTRO_VERSION, weighting_policy_ref=objective.weighting_policy_ref,
        results=tuple(final),
    )


def _with_rank(r: SignificanceResult, rank: int) -> SignificanceResult:
    return SignificanceResult(r.entity_id, r.designation, r.kind, r.status, r.score, rank, r.contributions, r.eligibility,
                              r.relationship_keys, r.evidence_ids, r.unavailable)


def explain(evaluation: SignificanceEvaluation, objective: Objective, entity_id: str) -> dict[str, Any]:
    """Structured explanation derived only from the recorded result."""
    r = evaluation.result_for(entity_id)
    threshold = objective.explanation_threshold
    why, why_not = [], []
    for rule in r.eligibility:
        if not rule["passed"]:
            why_not.append(f"{rule['rule']}: {rule['detail']}")
    for c in r.contributions:
        if c["status"] != "available":
            why_not.append(f"{c['feature']}: unavailable — {c['trace'].get('reason', 'no value')}")
        elif c["value"] is not None and c["value"] >= threshold:
            why.append(f"{c['feature']} = {c['value']:.3f} (weight {c['weight']})")
        elif c["value"] is not None:
            why_not.append(f"{c['feature']} = {c['value']:.3f} below {threshold}")
    return {
        "entity_id": r.entity_id, "designation": r.designation, "objective": objective.name, "objective_id": evaluation.objective_id,
        "context_id": evaluation.context_id, "status": r.status, "score": r.score, "rank": r.rank,
        "why_significant_now": why, "why_not_more": why_not,
        "relationships_used": list(r.relationship_keys), "evidence_used": list(r.evidence_ids),
        "evaluation_id": evaluation.evaluation_id,
    }
