"""Per-objective utility oracles for the synthetic benchmark.

An executed action is *useful* when it satisfies the objective's declared question according
to the universe's own records at execution time. These functions are benchmark scorers; the
engine never calls them.
"""

from __future__ import annotations

from datetime import timedelta
from typing import Callable

from astro.domain import Universe
from astro.execution import ScheduledAction
from astro.objectives.context import parse_utc


def _transit_in(action: ScheduledAction, universe: Universe) -> bool:
    start, end = parse_utc(action.start_utc), parse_utc(action.end_utc)
    for rec in universe.evidence_for(action.entity_id, "ephemeris"):
        if rec.status != "admissible":
            continue
        v = rec.value_map
        period, epoch = timedelta(days=float(v["period_days"])), parse_utc(v["epoch_utc"])
        n = int((start - epoch) / period)
        for k in (n - 1, n, n + 1, n + 2):
            t = epoch + k * period
            if start <= t <= end:
                return True
    return False


def transit_followup(action: ScheduledAction, universe: Universe) -> bool:
    """Useful iff a transit of an admissible ephemeris actually occurs during the observation."""
    return _transit_in(action, universe)


def transient_followup(action: ScheduledAction, universe: Universe) -> bool:
    """Useful iff the target has an admissible alert and no spectrum was obtained before this action."""
    alerts = [a for a in universe.evidence_for(action.entity_id, "alert") if a.status == "admissible"]
    if not alerts:
        return False
    start = parse_utc(action.start_utc)
    prior = [s for s in universe.evidence_for(action.entity_id, "spectrum") if s.observed_at and parse_utc(s.observed_at) <= start]
    return not prior


def variability_monitoring(action: ScheduledAction, universe: Universe) -> bool:
    """Useful iff the target has time-series evidence, still lacks a 90-day span, and was not observed in the prior 48 h."""
    series = [s for s in universe.evidence_for(action.entity_id, "time_series") if s.status == "admissible"]
    if not series:
        return False
    span = sum(float(s.value_map.get("span_days", 0.0)) for s in series)
    if span >= 90.0:
        return False
    start = parse_utc(action.start_utc)
    recent = [s for s in series if s.observed_at and start - parse_utc(s.observed_at) < timedelta(hours=48)]
    return not recent


def calibration(action: ScheduledAction, universe: Universe, anchors: tuple[str, ...] = ()) -> bool:
    """Useful iff the target is an evidenced calibration reference for one of the context's anchor targets."""
    for rel in universe.relationships_of(action.entity_id, "calibration_reference_for"):
        roles = rel.role_map
        if action.entity_id in roles.get("reference", ()) and rel.evidence_ids and any(t in anchors for t in roles.get("target", ())):
            return True
    return False


ORACLES: dict[str, Callable] = {
    "Exoplanet transit follow-up": transit_followup,
    "Transient-event follow-up": transient_followup,
    "Stellar variability monitoring": variability_monitoring,
    "Calibration reference selection": calibration,
}
