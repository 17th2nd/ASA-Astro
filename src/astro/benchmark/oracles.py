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


# ---- knowledge-frontier objectives (2026-09-04) ---------------------------------------------------------------
# These recompute the ground truth from raw evidence records and the declared expectations. They never read the
# engine's derived relationships (lacks_evidence, measures, contradicts) or its features, so a defect in the
# derivation would show up here as a disagreement, not be inherited.

_GAP_KINDS_A_BLOCK_CAN_FILL = ("time_series", "photometry", "spectrum")
_DISPUTE_TOLERANCE = {"teff_k": 0.07, "distance_pc": 0.15}


def _observed_within(action: ScheduledAction, universe: Universe, hours: float) -> bool:
    start = parse_utc(action.start_utc)
    return any(l.observed_at and (start - parse_utc(l.observed_at)) < timedelta(hours=hours) for l in universe.evidence_for(action.entity_id, "observation_log"))


def _decayed_transit_in(action: ScheduledAction, universe: Universe, max_period_fraction: float = 0.01) -> bool:
    """A transit of an ephemeris whose predicted-time uncertainty exceeds its duration falls in the window."""
    import math
    start = parse_utc(action.start_utc)
    for rec in universe.evidence_for(action.entity_id, "ephemeris"):
        v, u = rec.value_map, rec.uncertainty_map
        if rec.status != "admissible" or "period_days" not in v or "epoch_utc" not in v or not u:
            continue
        period, sig_p = float(v["period_days"]), float(u.get("period_days", 0.0))
        if period <= 0 or sig_p / period > max_period_fraction:
            continue
        n = abs((start - parse_utc(v["epoch_utc"])).total_seconds() / 86400.0 / period)
        sigma_h = math.sqrt(float(u.get("epoch_days", 0.0)) ** 2 + (n * sig_p) ** 2) * 24.0
        if sigma_h >= (float(v.get("duration_hours", 2.0)) or 2.0) and _transit_in(action, universe):
            return True
    return False


def knowledge_gap_reduction(action: ScheduledAction, universe: Universe) -> int:
    """Graded: the number of expected evidence kinds the block supplies (time series, photometry, spectrum)
    that the target lacks, plus one when a decayed transit ephemeris has a transit inside the window.
    Zero (not useful) when nothing is gained or the target was observed in the prior 24 h. Graded because
    on real data almost every star lacks *something*, so a yes/no oracle cannot tell strategies apart."""
    from astro.knowledge.expectations import expected_kinds
    if _observed_within(action, universe, 24.0):
        return 0
    entity = universe.entity(action.entity_id)
    present = {e.kind for e in universe.evidence_for(action.entity_id) if e.status == "admissible"}
    missing = {x.evidence_kind for x in expected_kinds(entity, universe)} - present
    return len(missing & set(_GAP_KINDS_A_BLOCK_CAN_FILL)) + int(_decayed_transit_in(action, universe))


def _source_of(rec) -> str:
    if rec.source.data_class == "derived" and rec.value_map.get("from"):
        return str(rec.value_map["from"])
    return rec.source.reference.split(":", 1)[0] or rec.source.source


def dispute_adjudication(action: ScheduledAction, universe: Universe) -> bool:
    """Useful iff two admissible records from different sources give the same quantity (Teff or distance,
    Gaia parallax counted as 1000/ϖ) differing beyond the declared tolerance, and no adjudicating observation
    was made in the prior 24 h."""
    if _observed_within(action, universe, 24.0):
        return False
    values: dict[str, list[tuple[float, str]]] = {"teff_k": [], "distance_pc": []}
    for rec in universe.evidence_for(action.entity_id):
        if rec.status != "admissible":
            continue
        if rec.kind == "astrometry" and float(rec.value_map.get("parallax_mas", 0) or 0) > 0:
            values["distance_pc"].append((1000.0 / float(rec.value_map["parallax_mas"]), _source_of(rec)))
        if rec.kind in ("catalogue_measurement", "derived_measurement", "spectrum"):
            for q in values:
                v = rec.value_map.get(q)
                if isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0:
                    values[q].append((float(v), _source_of(rec)))
    for q, items in values.items():
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                (a, sa), (b, sb) = items[i], items[j]
                if sa != sb and abs(a - b) / max(a, b) > _DISPUTE_TOLERANCE[q]:
                    return True
    return False


ORACLES: dict[str, Callable] = {
    "Knowledge-gap reduction": knowledge_gap_reduction,
    "Dispute adjudication": dispute_adjudication,
    "Exoplanet transit follow-up": transit_followup,
    "Transient-event follow-up": transient_followup,
    "Stellar variability monitoring": variability_monitoring,
    "Calibration reference selection": calibration,
}
