"""Session loop: evaluate → plan → schedule → execute one action → new evidence → re-evaluate.

This is the canonical Astro feedback loop. Each cycle is receipted; the universe is never
mutated in place (every step yields a new digest-identified universe); ASA holds the
relational history.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from astro.asa.adapter import AstroAdapter
from astro.domain import Universe
from astro.domain.identity import content_id
from astro.objectives import Objective, ObservingContext
from astro.pipeline import Decision, decide
from astro.execution.execute import ExecutionOutcome, Executor, SimulatedExecutor, apply_outcome
from astro.execution.schedule import Schedule, schedule_plan


@dataclass(frozen=True, slots=True)
class Cycle:
    index: int
    as_of: str
    universe_id: str
    decision: Decision
    schedule: Schedule
    outcome: ExecutionOutcome | None

    def to_record(self) -> dict[str, Any]:
        ev = getattr(self.decision, "evaluation", None)
        rc = getattr(self.decision, "receipt", None)
        snap = getattr(self.decision, "snapshot", None)
        return {
            "index": self.index, "as_of": self.as_of, "universe_id": self.universe_id,
            "evaluation_id": ev.evaluation_id if ev else None, "receipt_id": rc.receipt_id if rc else None,
            "kernel_digest": snap.digest if snap else None, "ranking": [r.designation for r in ev.ranked()] if ev else None,
            "plan": [a.designation for a in self.decision.plan.actions], "schedule": self.schedule.to_record(),
            "executed": self.outcome.action.to_record() if self.outcome else None,
            "new_evidence": [e.evidence_id for e in self.outcome.evidence] if self.outcome else [],
            "universe_after": self.outcome.universe_after if self.outcome else self.universe_id,
        }


@dataclass(frozen=True, slots=True)
class Session:
    session_id: str
    objective_id: str
    context_id: str
    cycles: tuple[Cycle, ...]
    final_universe: Universe

    def executed(self) -> tuple[str, ...]:
        return tuple(c.outcome.action.designation for c in self.cycles if c.outcome)

    def to_record(self) -> dict[str, Any]:
        return {"session_id": self.session_id, "objective_id": self.objective_id, "context_id": self.context_id,
                "cycles": [c.to_record() for c in self.cycles], "executed": list(self.executed()),
                "final_universe_id": self.final_universe.universe_id}


def run_session(universe: Universe, objective: Objective, context: ObservingContext, adapter: AstroAdapter, *,
                executor: Executor | None = None, max_cycles: int = 6, commit: str | None = None, issued_at: str | None = None,
                planner=None) -> Session:
    """Run the loop. ``planner(universe, objective, context, adapter) -> Decision`` defaults to the ASA-guided
    ``pipeline.decide``; benchmark baselines supply their own planner and are never confused with it."""
    executor = executor or SimulatedExecutor()
    plan_step = planner or (lambda u, o, c, a: decide(u, o, c, a, commit=commit, issued_at=issued_at))
    cycles: list[Cycle] = []
    current, ctx = universe, context
    for i in range(1, max_cycles + 1):
        adapter.load_universe(current)
        decision = plan_step(current, objective, ctx, adapter)
        sched = schedule_plan(decision.plan, decision.evaluation, current, ctx)
        if not sched.scheduled:
            cycles.append(Cycle(i, ctx.as_of, current.universe_id, decision, sched, None))
            break
        action = sched.scheduled[0]
        evidence, state = executor.execute(action, current, ctx)
        outcome = apply_outcome(current, action, evidence, state)
        cycles.append(Cycle(i, ctx.as_of, current.universe_id, decision, sched, outcome))
        current = current.with_evidence(*evidence).with_states(state)
        ctx = ctx.with_changes(as_of=action.end_utc)
        if ctx.now >= ctx.window[1]:
            break
    adapter.load_universe(current)
    body = {"objective_id": objective.objective_id, "context_id": context.context_id, "cycles": [c.to_record() for c in cycles]}
    return Session(content_id("SESS", body), objective.objective_id, context.context_id, tuple(cycles), current)
