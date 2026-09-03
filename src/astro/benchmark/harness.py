"""Run every strategy through the same session loop and score executed actions with the oracle."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from astro.domain import Universe
from astro.domain.identity import content_id
from astro.objectives import Objective, ObservingContext
from astro.objectives.context import parse_utc
from astro.pipeline import open_or_bootstrap
from astro.session import run_session
from .oracles import ORACLES
from .strategies import STRATEGIES


@dataclass(frozen=True, slots=True)
class StrategyResult:
    strategy: str
    executed: tuple[dict[str, Any], ...]
    useful_actions: int
    total_gain: float                # sum of graded oracle scores (equals useful_actions for yes/no oracles)
    wasted_minutes: int
    total_minutes: int
    time_to_first_useful_minutes: int | None
    candidates_considered: int
    reproducible: bool

    def to_record(self) -> dict[str, Any]:
        return {"strategy": self.strategy, "executed": list(self.executed), "useful_actions": self.useful_actions, "total_gain": self.total_gain,
                "wasted_minutes": self.wasted_minutes, "total_minutes": self.total_minutes,
                "time_to_first_useful_minutes": self.time_to_first_useful_minutes,
                "candidates_considered": self.candidates_considered, "reproducible": self.reproducible}


@dataclass(frozen=True, slots=True)
class BenchmarkResult:
    benchmark_id: str
    objective: str
    universe_id: str
    results: tuple[StrategyResult, ...]

    def to_record(self) -> dict[str, Any]:
        return {"benchmark_id": self.benchmark_id, "objective": self.objective, "universe_id": self.universe_id,
                "results": [r.to_record() for r in self.results]}


def _score(session, objective: Objective, context: ObservingContext, universe0: Universe) -> tuple[list[dict], int, float, int, int, int | None]:
    fn = ORACLES[objective.name]
    kwargs = {"anchors": context.anchor_targets} if objective.name == "Calibration reference selection" else {}
    executed, useful, gain, wasted, total, first = [], 0, 0.0, 0, 0, None
    t0 = context.window[0]
    for c in session.cycles:
        if not c.outcome:
            continue
        a = c.outcome.action
        # judge against the universe as it was when the action was planned (before its own evidence landed)
        u_before = universe0 if c.index == 1 else next(cc.outcome for cc in session.cycles if cc.index == c.index - 1)
        u_at = universe0 if c.index == 1 else None
        minutes = int((parse_utc(a.end_utc) - parse_utc(a.start_utc)).total_seconds() // 60)
        verdict = fn(a, _universe_at(session, c.index, universe0), **kwargs)
        ok, g = bool(verdict), float(verdict) if isinstance(verdict, (int, float)) and not isinstance(verdict, bool) else float(bool(verdict))
        executed.append({"cycle": c.index, "designation": a.designation, "action": a.action, "start_utc": a.start_utc, "end_utc": a.end_utc, "useful": ok, "gain": g})
        total += minutes
        gain += g
        if ok:
            useful += 1
            if first is None:
                first = int((parse_utc(a.start_utc) - t0).total_seconds() // 60)
        else:
            wasted += minutes
    return executed, useful, gain, wasted, total, first


def _universe_at(session, index: int, universe0: Universe) -> Universe:
    """Universe as it stood when cycle ``index`` planned: the original, plus the outcomes of earlier cycles."""
    u = universe0
    for c in session.cycles:
        if c.index >= index:
            break
        if c.outcome:
            u = u.with_evidence(*c.outcome.evidence).with_states(c.outcome.state)
    return u


def run_benchmark(universe: Universe, objective: Objective, context: ObservingContext, strategies: list[str] | None = None,
                  max_cycles: int = 8) -> BenchmarkResult:
    names = strategies or list(STRATEGIES)
    results = []
    for name in names:
        planner = STRATEGIES[name]
        runs = []
        for _ in range(2):                                   # run twice: reproducibility is a measured property
            adapter = open_or_bootstrap(universe, slug=f"bench-{name}")
            s = run_session(universe, objective, context, adapter, max_cycles=max_cycles, planner=planner)
            runs.append(s)
        s = runs[0]
        executed, useful, gain, wasted, total, first = _score(s, objective, context, universe)
        considered = len([e for e in universe.entities if e.kind in objective.target_kinds]) if name != "asa" else len(universe.entities)
        results.append(StrategyResult(name, tuple(executed), useful, gain, wasted, total, first, considered,
                                      runs[0].to_record() == runs[1].to_record()))
    body = {"objective": objective.objective_id, "context": context.context_id, "universe": universe.universe_id, "results": [r.to_record() for r in results]}
    return BenchmarkResult(content_id("BENCH", body), objective.name, universe.universe_id, tuple(results))
