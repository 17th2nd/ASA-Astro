"""Schedule: place planned actions in time against the observing window and target constraints."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

from astro.domain import Universe
from astro.domain.identity import content_id
from astro.objectives import ObservingContext
from astro.objectives.context import parse_utc
from astro.significance import SignificanceEvaluation
from astro.significance.features import altitude_deg
from .plan import Plan


def _iso(t: datetime) -> str:
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass(frozen=True, slots=True)
class ScheduledAction:
    sequence: int
    action: str
    entity_id: str
    designation: str
    start_utc: str
    end_utc: str
    basis: dict[str, Any]

    def to_record(self) -> dict[str, Any]:
        return {"sequence": self.sequence, "action": self.action, "entity_id": self.entity_id, "designation": self.designation,
                "start_utc": self.start_utc, "end_utc": self.end_utc, "basis": self.basis}


@dataclass(frozen=True, slots=True)
class Schedule:
    schedule_id: str
    plan_id: str
    context_id: str
    scheduled: tuple[ScheduledAction, ...]
    unscheduled: tuple[dict[str, Any], ...]

    def to_record(self) -> dict[str, Any]:
        return {"schedule_id": self.schedule_id, "plan_id": self.plan_id, "context_id": self.context_id,
                "scheduled": [s.to_record() for s in self.scheduled], "unscheduled": list(self.unscheduled)}


def _site(universe: Universe, context: ObservingContext):
    if not context.site_id:
        return None
    try:
        attrs = universe.entity(context.site_id).attribute_map
    except KeyError:
        return None
    if "latitude_deg" in attrs and "longitude_deg" in attrs:
        return float(attrs["latitude_deg"]), float(attrs["longitude_deg"])
    return None


def _visible_intervals(universe: Universe, context: ObservingContext, entity_id: str, min_alt: float, step: int = 10) -> list[tuple[datetime, datetime]]:
    """Intervals inside the window where geometric altitude ≥ min_alt; whole window if geometry is unavailable."""
    t0, t1 = context.window
    site = _site(universe, context)
    ent = universe.entity(entity_id)
    if site is None or ent.coordinates is None:
        return [(t0, t1)]
    out, start, t = [], None, t0
    while t <= t1:
        up = altitude_deg(ent.coordinates.ra_deg, ent.coordinates.dec_deg, site[0], site[1], t) >= min_alt
        if up and start is None:
            start = t
        if not up and start is not None:
            out.append((start, t))
            start = None
        t += timedelta(minutes=step)
    if start is not None:
        out.append((start, t1))
    return out


def _preferred_start(evaluation: SignificanceEvaluation, entity_id: str, duration: timedelta) -> datetime | None:
    """A transit-shaped action wants to be centred on the predicted mid-transit recorded in the evaluation trace."""
    r = evaluation.result_for(entity_id)
    for c in r.contributions:
        if c["feature"] == "transit_window_proximity" and c["status"] == "available" and "next_transit_utc" in c["trace"]:
            return parse_utc(c["trace"]["next_transit_utc"]) - duration / 2
    return None


def schedule_plan(plan: Plan, evaluation: SignificanceEvaluation, universe: Universe, context: ObservingContext) -> Schedule:
    """Greedy, deterministic placement in plan order; no overlaps; each action inside a visibility interval."""
    t0, t1 = context.window
    now = max(context.now, t0)
    min_alt = float(context.constraint_map.get("min_altitude_deg", 30.0))
    busy: list[tuple[datetime, datetime]] = []
    scheduled, unscheduled = [], []
    for a in plan.actions:
        duration = timedelta(minutes=a.duration_minutes)
        intervals = _visible_intervals(universe, context, a.entity_id, min_alt)
        preferred = _preferred_start(evaluation, a.entity_id, duration)
        candidates: list[datetime] = []
        for (s, e) in intervals:
            lo, hi = max(s, now), e - duration
            if hi < lo:
                continue
            if preferred is not None:
                candidates.append(min(max(preferred, lo), hi))
            candidates.append(lo)
            for (bs, be) in busy:                     # right after each existing booking
                if lo <= be <= hi:
                    candidates.append(be)
        placed = None
        for start in sorted(candidates, key=lambda c: (abs((c - preferred).total_seconds()) if preferred else 0, c)):
            end = start + duration
            if any(not (end <= bs or start >= be) for bs, be in busy):
                continue
            if not any(s <= start and end <= e for s, e in intervals):
                continue
            placed = (start, end)
            break
        if placed is None:
            unscheduled.append({"entity_id": a.entity_id, "designation": a.designation, "action": a.action,
                                "reason": "no conflict-free visibility interval long enough in the window",
                                "visible_intervals": [[_iso(s), _iso(e)] for s, e in intervals]})
            continue
        busy.append(placed)
        basis = {"visible_intervals": [[_iso(s), _iso(e)] for s, e in intervals], "min_altitude_deg": min_alt}
        if preferred is not None:
            basis["preferred_start_utc"] = _iso(preferred)
        scheduled.append(ScheduledAction(len(scheduled) + 1, a.action, a.entity_id, a.designation, _iso(placed[0]), _iso(placed[1]), basis))
    scheduled.sort(key=lambda s: (s.start_utc, s.entity_id))
    scheduled = [ScheduledAction(i + 1, s.action, s.entity_id, s.designation, s.start_utc, s.end_utc, s.basis) for i, s in enumerate(scheduled)]
    body = {"plan_id": plan.plan_id, "context_id": context.context_id, "scheduled": [s.to_record() for s in scheduled], "unscheduled": unscheduled}
    return Schedule(content_id("SCHED", body), plan.plan_id, context.context_id, tuple(scheduled), tuple(unscheduled))
