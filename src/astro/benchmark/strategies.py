"""Selection strategies. Each returns a Decision-shaped object whose ``plan`` the session loop executes.

Baselines apply only the objective's *kind* filter (they know what sort of object the programme
is about) and its per-action duration and target budget. They do not see evidence, relationships,
significance or ASA state. ``asa`` is the real engine. ``oracle`` selects with the benchmark's
utility oracle and is an upper bound, not a strategy anyone could run without ground truth.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Callable

from astro.asa.adapter import AstroAdapter
from astro.domain import Universe
from astro.domain.identity import content_id
from astro.execution import Plan, PlannedAction, SkippedEntity
from astro.objectives import Objective, ObservingContext
from astro.objectives.context import parse_utc
from astro.pipeline import decide
from .oracles import ORACLES


@dataclass(frozen=True, slots=True)
class BaselineDecision:
    plan: Plan
    evaluation: None = None


def _candidates(universe: Universe, objective: Objective) -> list:
    return [e for e in universe.entities if e.kind in objective.target_kinds]


def _plan(ordered, objective: Objective, context: ObservingContext, strategy: str, universe: Universe) -> BaselineDecision:
    spec = objective.plan_map
    action, max_targets, duration = spec["action"], int(spec["max_targets"]), int(spec["duration_minutes"])
    repeat_gap = spec.get("min_repeat_gap_hours")
    actions, skipped = [], []
    for e in ordered:
        st = universe.state_of(e.entity_id)
        if repeat_gap is not None and st and st.last_observed_at and (context.now - parse_utc(st.last_observed_at)).total_seconds() / 3600.0 < float(repeat_gap):
            skipped.append(SkippedEntity(e.entity_id, e.designation, "eligible", "observed within the repeat gap"))
            continue
        if len(actions) >= max_targets:
            skipped.append(SkippedEntity(e.entity_id, e.designation, "eligible", "beyond target budget"))
            continue
        actions.append(PlannedAction(len(actions) + 1, action, e.entity_id, e.designation, duration, len(actions) + 1, 0.0, (strategy,)))
    body = {"strategy": strategy, "objective_id": objective.objective_id, "context_id": context.context_id, "actions": [a.to_record() for a in actions]}
    return BaselineDecision(Plan(content_id("PLAN", body), f"baseline:{strategy}", objective.objective_id, context.context_id, tuple(actions), tuple(skipped),
                                 sum(a.duration_minutes for a in actions)))


def fifo(universe: Universe, objective: Objective, context: ObservingContext, adapter: AstroAdapter):
    """Catalogue order: entities as the universe lists them (sorted by identity), kind-filtered."""
    return _plan(_candidates(universe, objective), objective, context, "fifo", universe)


def random_selection(universe: Universe, objective: Objective, context: ObservingContext, adapter: AstroAdapter, seed: int = 2026):
    cands = _candidates(universe, objective)
    random.Random(f"{seed}:{context.as_of}").shuffle(cands)
    return _plan(cands, objective, context, "random", universe)


def static_priority(universe: Universe, objective: Objective, context: ObservingContext, adapter: AstroAdapter):
    """The classic intrinsic-importance ranker: brightest first (lowest magnitude_v), then identity."""
    cands = sorted(_candidates(universe, objective), key=lambda e: (float(e.attribute_map.get("magnitude_v", 99.0)), e.entity_id))
    return _plan(cands, objective, context, "static_priority", universe)


def asa(universe: Universe, objective: Objective, context: ObservingContext, adapter: AstroAdapter):
    return decide(universe, objective, context, adapter, commit="0" * 40, issued_at=context.as_of)


def oracle(universe: Universe, objective: Objective, context: ObservingContext, adapter: AstroAdapter):
    """Upper bound: orders candidates by whether an action starting now would be useful per the oracle."""
    from astro.execution import ScheduledAction
    fn = ORACLES[objective.name]
    duration = int(objective.plan_map["duration_minutes"])
    t0 = max(context.now, context.window[0])
    end = (t0 + __import__("datetime").timedelta(minutes=duration)).strftime("%Y-%m-%dT%H:%M:%SZ")
    def useful(e):
        a = ScheduledAction(1, objective.plan_map["action"], e.entity_id, e.designation, t0.strftime("%Y-%m-%dT%H:%M:%SZ"), end, {})
        kwargs = {"anchors": context.anchor_targets} if objective.name == "Calibration reference selection" else {}
        return fn(a, universe, **kwargs)
    cands = _candidates(universe, objective)
    scored = [(useful(e), e) for e in cands]
    ordered = [e for g, e in sorted(((float(g), e) for g, e in scored if g), key=lambda t: (-t[0], t[1].entity_id))]  # highest gain first; the oracle wastes nothing it can see
    return _plan(ordered, objective, context, "oracle", universe)


STRATEGIES: dict[str, Callable] = {"fifo": fifo, "random": random_selection, "static_priority": static_priority, "asa": asa, "oracle": oracle}
