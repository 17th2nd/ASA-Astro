"""Plan: the concrete scientific work Astro chooses to do given a significance evaluation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from astro.asa.adapter import RelationalSnapshot
from astro.domain.identity import content_id
from astro.objectives import Objective, ObservingContext
from astro.objectives.context import parse_utc
from astro.significance import SignificanceEvaluation


@dataclass(frozen=True, slots=True)
class PlannedAction:
    sequence: int
    action: str
    entity_id: str
    designation: str
    duration_minutes: int
    rank: int
    score: float
    basis: tuple[str, ...]          # feature names that contributed at or above the explanation threshold

    def to_record(self) -> dict[str, Any]:
        return {"sequence": self.sequence, "action": self.action, "entity_id": self.entity_id, "designation": self.designation,
                "duration_minutes": self.duration_minutes, "rank": self.rank, "score": self.score, "basis": list(self.basis)}


@dataclass(frozen=True, slots=True)
class SkippedEntity:
    entity_id: str
    designation: str
    status: str
    reason: str

    def to_record(self) -> dict[str, Any]:
        return {"entity_id": self.entity_id, "designation": self.designation, "status": self.status, "reason": self.reason}


@dataclass(frozen=True, slots=True)
class Plan:
    plan_id: str
    evaluation_id: str
    objective_id: str
    context_id: str
    actions: tuple[PlannedAction, ...]
    skipped: tuple[SkippedEntity, ...]
    total_minutes: int

    def selected_ids(self) -> tuple[str, ...]:
        return tuple(a.entity_id for a in self.actions)

    def to_record(self) -> dict[str, Any]:
        return {"plan_id": self.plan_id, "evaluation_id": self.evaluation_id, "objective_id": self.objective_id,
                "context_id": self.context_id, "actions": [a.to_record() for a in self.actions],
                "skipped": [s.to_record() for s in self.skipped], "total_minutes": self.total_minutes}


def plan_from_evaluation(evaluation: SignificanceEvaluation, objective: Objective, context: ObservingContext,
                         snapshot: RelationalSnapshot | None = None) -> Plan:
    """Select the top-ranked eligible entities within the objective's budgets.

    Declared plan policy (``objective.plan``): ``max_targets``, ``duration_minutes``, optional ``min_score``
    (below it the work is not worth the telescope time for this objective) and optional
    ``min_repeat_gap_hours`` (an entity whose ASA-registered state says it was observed more recently is
    skipped). The context's ``available_minutes`` bounds the total.
    """
    spec = objective.plan_map
    action, max_targets, duration = spec["action"], int(spec["max_targets"]), int(spec["duration_minutes"])
    min_score = float(spec.get("min_score", 0.0))
    repeat_gap = spec.get("min_repeat_gap_hours")
    budget = context.constraint_map.get("available_minutes")
    actions, skipped, total = [], [], 0
    for r in evaluation.results:
        if r.status == "eligible" and (r.score or 0.0) < min_score:
            skipped.append(SkippedEntity(r.entity_id, r.designation, r.status, f"score {r.score:.4f} below the objective's minimum {min_score}"))
            continue
        if r.status == "eligible" and repeat_gap is not None and snapshot is not None:
            state = snapshot.state_of(r.entity_id)
            last = dict(state.literals).get("last_observed_at") if state else None
            if last:
                gap_h = (context.now - parse_utc(last)).total_seconds() / 3600.0
                if gap_h < float(repeat_gap):
                    skipped.append(SkippedEntity(r.entity_id, r.designation, r.status,
                                                 f"observed {gap_h:.1f} h ago; objective repeat gap is {float(repeat_gap):g} h"))
                    continue
        if r.status != "eligible":
            fails = [e["detail"] for e in r.eligibility if not e["passed"]]
            unavailable = [c["feature"] for c in r.contributions if c["status"] != "available" and c["required"]]
            reason = "; ".join(fails + [f"required feature unavailable: {u}" for u in unavailable]) or r.status
            skipped.append(SkippedEntity(r.entity_id, r.designation, r.status, reason))
            continue
        if len(actions) >= max_targets:
            skipped.append(SkippedEntity(r.entity_id, r.designation, r.status, f"rank {r.rank} beyond the objective's {max_targets}-target budget"))
            continue
        if budget is not None and total + duration > int(budget):
            skipped.append(SkippedEntity(r.entity_id, r.designation, r.status, f"insufficient time: {total}+{duration} > {budget} minutes"))
            continue
        basis = tuple(c["feature"] for c in r.contributions if c["status"] == "available" and c["value"] is not None
                      and c["value"] >= objective.explanation_threshold)
        actions.append(PlannedAction(len(actions) + 1, action, r.entity_id, r.designation, duration, r.rank or 0, r.score or 0.0, basis))
        total += duration
    body = {"evaluation_id": evaluation.evaluation_id, "objective_id": objective.objective_id, "context_id": context.context_id,
            "actions": [a.to_record() for a in actions], "skipped": [s.to_record() for s in skipped]}
    return Plan(content_id("PLAN", body), evaluation.evaluation_id, objective.objective_id, context.context_id,
                tuple(actions), tuple(skipped), total)
