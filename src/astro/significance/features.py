"""Astro feature library: deterministic functions from (entity, ASA relational state, evidence, objective, context) to [0, 1].

Every feature returns a :class:`FeatureValue` with an explicit status and a trace naming the
evidence ids, relationship keys and numbers it used. A feature never reads a value that is
not registered in ASA. Brightness and proximity are only consulted by features that an
objective declares explicitly with a rationale (`instrument_suitability`, `proximity_to_anchor`).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Callable

from astro.asa.adapter import Edge, RelationalSnapshot
from astro.domain import Entity, EvidenceRecord, Universe
from astro.objectives import Objective, ObservingContext
from astro.objectives.context import parse_utc

OBSERVATIONAL_KINDS = ("photometry", "astrometry", "spectrum", "time_series", "observation_log")


@dataclass(frozen=True, slots=True)
class FeatureValue:
    name: str
    value: float | None
    status: str                      # available | unavailable | not_applicable
    trace: dict[str, Any] = field(default_factory=dict)

    def to_record(self) -> dict[str, Any]:
        return {"name": self.name, "value": self.value, "status": self.status, "trace": self.trace}


@dataclass(frozen=True, slots=True)
class FeatureInput:
    entity: Entity
    universe: Universe
    snapshot: RelationalSnapshot
    objective: Objective
    context: ObservingContext
    eligible_edges: tuple[Edge, ...]                 # relationships passing the objective's relationship policy
    admissible_evidence: tuple[EvidenceRecord, ...]  # ASA-registered evidence with admissible status

    def evidence(self, *kinds: str) -> tuple[EvidenceRecord, ...]:
        return tuple(e for e in self.admissible_evidence if not kinds or e.kind in kinds)

    def edges(self, type_name: str) -> tuple[Edge, ...]:
        return tuple(e for e in self.eligible_edges if e.type_name == type_name)


def _clip(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def _hours(a: datetime, b: datetime) -> float:
    return (a - b).total_seconds() / 3600.0


def _unavailable(name: str, reason: str, **trace: Any) -> FeatureValue:
    return FeatureValue(name, None, "unavailable", {"reason": reason, **trace})


# ---- features ------------------------------------------------------------------------------------
def transit_window_proximity(fi: FeatureInput, params: dict[str, Any]) -> FeatureValue:
    """1.0 when a predicted transit falls inside the observing window; 0 outside it unless the objective declares a
    ``horizon_hours`` over which a near miss decays linearly (default 0: strictly this window)."""
    name = "transit_window_proximity"
    horizon = float(params.get("horizon_hours", 0.0))
    eph = fi.evidence("ephemeris")
    companions = [o for e in fi.edges("hosts") for o in e.others(fi.entity.entity_id)]
    for comp in companions:
        for rec in fi.universe.evidence_for(comp, "ephemeris"):
            if rec.status == "admissible" and any(l.evidence_id == rec.evidence_id for l in fi.snapshot.evidence_of(comp)):
                eph = eph + (rec,)
    if not eph:
        return _unavailable(name, "no admissible ephemeris evidence registered for the entity or an endorsed companion")
    t0, t1 = fi.context.window
    best: tuple[float, dict[str, Any]] | None = None
    for rec in sorted(eph, key=lambda r: r.evidence_id):
        v = rec.value_map
        try:
            period = timedelta(days=float(v["period_days"]))
            epoch = parse_utc(v["epoch_utc"])
        except (KeyError, ValueError):
            continue
        n = math.ceil((t0 - epoch) / period) if t0 > epoch else 0
        t_next = epoch + n * period
        if t0 <= t_next <= t1:
            score, outside = 1.0, 0.0
        else:
            outside = _hours(t_next, t1) if t_next > t1 else _hours(t0, t_next)
            score = _clip(1.0 - outside / horizon) if horizon > 0 else 0.0
        trace = {"evidence_id": rec.evidence_id, "period_days": float(v["period_days"]), "next_transit_utc": t_next.strftime("%Y-%m-%dT%H:%M:%SZ"),
                 "hours_outside_window": round(outside, 3), "horizon_hours": horizon}
        if best is None or score > best[0]:
            best = (score, trace)
    if best is None:
        return _unavailable(name, "ephemeris evidence lacks period_days/epoch_utc")
    return FeatureValue(name, round(best[0], 12), "available", best[1])


def observation_gap(fi: FeatureInput, params: dict[str, Any]) -> FeatureValue:
    """Time since the last registered observation relative to the desired cadence; never observed → 1.0."""
    name = "observation_gap"
    cadence = float(params.get("cadence_hours", 168.0))
    kinds = tuple(params.get("evidence_kinds", OBSERVATIONAL_KINDS))
    stamps = [parse_utc(e.observed_at) for e in fi.evidence(*kinds) if e.observed_at]
    state = fi.snapshot.state_of(fi.entity.entity_id)
    last_state = dict(state.literals).get("last_observed_at") if state else None
    if last_state:
        stamps.append(parse_utc(last_state))
    if not stamps:
        return FeatureValue(name, 1.0, "available", {"reason": "never observed", "cadence_hours": cadence})
    last = max(stamps)
    gap = _hours(fi.context.now, last)
    return FeatureValue(name, round(_clip(gap / cadence), 12), "available",
                        {"last_observed_utc": last.strftime("%Y-%m-%dT%H:%M:%SZ"), "gap_hours": round(gap, 3), "cadence_hours": cadence})


def evidence_quality(fi: FeatureInput, params: dict[str, Any]) -> FeatureValue:
    name = "evidence_quality"
    kinds = tuple(params.get("evidence_kinds", ()))
    recs = fi.evidence(*kinds)
    if not recs:
        return _unavailable(name, "no admissible evidence of the declared kinds", kinds=list(kinds))
    mean = sum(r.quality for r in recs) / len(recs)
    return FeatureValue(name, round(mean, 12), "available", {"evidence_ids": [r.evidence_id for r in recs], "count": len(recs)})


def evidence_scarcity(fi: FeatureInput, params: dict[str, Any]) -> FeatureValue:
    """Scientific value of one more record: 1 - count/needed."""
    name = "evidence_scarcity"
    needed = max(1, int(params.get("needed", 3)))
    kinds = tuple(params.get("evidence_kinds", OBSERVATIONAL_KINDS))
    recs = fi.evidence(*kinds)
    return FeatureValue(name, round(_clip(1.0 - len(recs) / needed), 12), "available",
                        {"count": len(recs), "needed": needed, "evidence_ids": [r.evidence_id for r in recs]})


def _latest_alert(fi: FeatureInput) -> EvidenceRecord | None:
    alerts = [a for a in fi.evidence("alert") if a.observed_at]
    return max(alerts, key=lambda a: (parse_utc(a.observed_at), a.evidence_id)) if alerts else None


def alert_freshness(fi: FeatureInput, params: dict[str, Any]) -> FeatureValue:
    name = "alert_freshness"
    half_life = float(params.get("half_life_hours", 24.0))
    alert = _latest_alert(fi)
    if alert is None:
        return _unavailable(name, "no admissible alert evidence")
    age = max(0.0, _hours(fi.context.now, parse_utc(alert.observed_at)))
    return FeatureValue(name, round(0.5 ** (age / half_life), 12), "available",
                        {"evidence_id": alert.evidence_id, "age_hours": round(age, 3), "half_life_hours": half_life})


def alert_confidence(fi: FeatureInput, params: dict[str, Any]) -> FeatureValue:
    name = "alert_confidence"
    alert = _latest_alert(fi)
    if alert is None or "confidence" not in alert.value_map:
        return _unavailable(name, "no admissible alert evidence with a confidence value")
    return FeatureValue(name, round(_clip(alert.value_map["confidence"]), 12), "available", {"evidence_id": alert.evidence_id})


def alert_rarity(fi: FeatureInput, params: dict[str, Any]) -> FeatureValue:
    name = "alert_rarity"
    alert = _latest_alert(fi)
    if alert is None or "rarity" not in alert.value_map:
        return _unavailable(name, "no admissible alert evidence with a rarity value")
    return FeatureValue(name, round(_clip(alert.value_map["rarity"]), 12), "available",
                        {"evidence_id": alert.evidence_id, "note": "rarity as declared by the alert source"})


def _gmst_hours(t: datetime) -> float:
    """Greenwich mean sidereal time (hours), IAU 1982 polynomial; sufficient for visibility gating."""
    jd = 2440587.5 + (t - datetime(1970, 1, 1, tzinfo=t.tzinfo)).total_seconds() / 86400.0
    T = (jd - 2451545.0) / 36525.0
    gmst = 280.46061837 + 360.98564736629 * (jd - 2451545.0) + 0.000387933 * T * T - T ** 3 / 38710000.0
    return (gmst % 360.0) / 15.0


def altitude_deg(ra_deg: float, dec_deg: float, lat_deg: float, lon_deg: float, t: datetime) -> float:
    lst_deg = (_gmst_hours(t) * 15.0 + lon_deg) % 360.0
    ha = math.radians((lst_deg - ra_deg + 540.0) % 360.0 - 180.0)
    lat, dec = math.radians(lat_deg), math.radians(dec_deg)
    return math.degrees(math.asin(math.sin(lat) * math.sin(dec) + math.cos(lat) * math.cos(dec) * math.cos(ha)))


def visibility(fi: FeatureInput, params: dict[str, Any]) -> FeatureValue:
    """Peak geometric altitude in the window against ``min_altitude_deg`` (no refraction, twilight or Moon)."""
    name = "visibility"
    min_alt = float(params.get("min_altitude_deg", 30.0))
    step = int(params.get("step_minutes", 10))
    if fi.entity.coordinates is None:
        return _unavailable(name, "entity has no coordinates")
    if not fi.context.site_id:
        return _unavailable(name, "context declares no site")
    try:
        site = fi.universe.entity(fi.context.site_id)
    except KeyError:
        return _unavailable(name, "context site is not in the universe", site_id=fi.context.site_id)
    attrs = site.attribute_map
    if "latitude_deg" not in attrs or "longitude_deg" not in attrs:
        return _unavailable(name, "site lacks latitude_deg/longitude_deg", site_id=site.entity_id)
    t0, t1 = fi.context.window
    t, best, best_t = t0, -90.0, t0
    while t <= t1:
        alt = altitude_deg(fi.entity.coordinates.ra_deg, fi.entity.coordinates.dec_deg, float(attrs["latitude_deg"]), float(attrs["longitude_deg"]), t)
        if alt > best:
            best, best_t = alt, t
        t += timedelta(minutes=step)
    value = _clip((best - min_alt) / (90.0 - min_alt)) if best > min_alt else 0.0
    return FeatureValue(name, round(value, 12), "available",
                        {"site_id": site.entity_id, "peak_altitude_deg": round(best, 3), "peak_utc": best_t.strftime("%Y-%m-%dT%H:%M:%SZ"),
                         "min_altitude_deg": min_alt, "model": "geometric altitude only; no refraction, twilight or Moon"})


def instrument_suitability(fi: FeatureInput, params: dict[str, Any]) -> FeatureValue:
    """Feasibility gate declared by the objective: target magnitude within the context's limiting magnitude."""
    name = "instrument_suitability"
    attr = params.get("magnitude_attribute", "magnitude_v")
    limit = fi.context.constraint_map.get("limiting_magnitude")
    mag = fi.entity.attribute_map.get(attr)
    if limit is None:
        return _unavailable(name, "context declares no limiting_magnitude")
    if mag is None:
        phot = [e for e in fi.evidence("photometry") if "mag_v" in e.value_map]
        if not phot:
            return _unavailable(name, f"entity has no {attr} attribute and no photometry")
        mag = phot[-1].value_map["mag_v"]
    return FeatureValue(name, 1.0 if float(mag) <= float(limit) else 0.0, "available",
                        {"magnitude": float(mag), "limiting_magnitude": float(limit), "note": "brightness used only as instrument feasibility"})


def calibration_suitability(fi: FeatureInput, params: dict[str, Any]) -> FeatureValue:
    """Fraction of the context's anchor targets this entity is an endorsed calibration reference for, scaled by assessed stability."""
    name = "calibration_suitability"
    anchors = set(fi.context.anchor_targets)
    if not anchors:
        return _unavailable(name, "context declares no anchor_targets")
    refs = [e for e in fi.edges("calibration_reference_for") if e.role_of(fi.entity.entity_id) == "reference"]
    covered = sorted({o for e in refs for o in e.others(fi.entity.entity_id) if o in anchors})
    stability = 1.0
    assess = fi.evidence("calibration_assessment")
    if assess:
        stability = sum(_clip(a.value_map.get("stability", 1.0)) for a in assess) / len(assess)
    value = (len(covered) / len(anchors)) * stability
    return FeatureValue(name, round(value, 12), "available",
                        {"relationship_keys": [e.key for e in refs], "anchors_covered": covered, "stability": stability,
                         "assessment_ids": [a.evidence_id for a in assess]})


def proximity_to_anchor(fi: FeatureInput, params: dict[str, Any]) -> FeatureValue:
    """Declared use of angular proximity to an anchor target via an eligible `near` relationship."""
    name = "proximity_to_anchor"
    max_sep = float(params.get("max_separation_arcsec", 3600.0))
    anchors = set(fi.context.anchor_targets)
    if not anchors:
        return _unavailable(name, "context declares no anchor_targets")
    best = None
    for e in fi.edges("near"):
        others = [o for o in e.others(fi.entity.entity_id) if o in anchors]
        if not others:
            continue
        sep = float(dict(e.literals).get("separation_arcsec", max_sep))
        v = _clip(1.0 - sep / max_sep)
        if best is None or v > best[0]:
            best = (v, {"relationship_key": e.key, "anchor": others[0], "separation_arcsec": sep, "max_separation_arcsec": max_sep})
    if best is None:
        return _unavailable(name, "no eligible near relationship to an anchor target")
    return FeatureValue(name, round(best[0], 12), "available", best[1])


def relationship_support(fi: FeatureInput, params: dict[str, Any]) -> FeatureValue:
    """Fraction of the listed relationship types for which an eligible relationship exists."""
    name = "relationship_support"
    types = list(params.get("types", fi.objective.eligible_relationship_types))
    if not types:
        return _unavailable(name, "no relationship types declared")
    present = [t for t in types if fi.edges(t)]
    return FeatureValue(name, round(len(present) / len(types), 12), "available",
                        {"types": types, "present": present, "relationship_keys": [e.key for e in fi.eligible_edges]})


def candidate_status(fi: FeatureInput, params: dict[str, Any]) -> FeatureValue:
    """Value of the entity's current ASA-registered candidate status under the objective's declared mapping."""
    name = "candidate_status"
    mapping = params.get("values", {"candidate": 1.0, "confirmed": 0.25, "none": 0.0, "rejected": 0.0})
    state = fi.snapshot.state_of(fi.entity.entity_id)
    if state is None:
        return _unavailable(name, "no registered observation state")
    status = dict(state.literals).get("candidate_status", "none")
    return FeatureValue(name, round(_clip(mapping.get(status, 0.0)), 12), "available", {"state_key": state.key, "candidate_status": status})


def time_series_coverage_gap(fi: FeatureInput, params: dict[str, Any]) -> FeatureValue:
    """Shortfall of registered time-series span against the required span (asteroseismic-style cadence needs)."""
    name = "time_series_coverage_gap"
    required = float(params.get("required_span_days", 90.0))
    series = fi.evidence("time_series")
    span = sum(float(s.value_map.get("span_days", 0.0)) for s in series)
    return FeatureValue(name, round(_clip(1.0 - span / required), 12), "available",
                        {"span_days": span, "required_span_days": required, "evidence_ids": [s.evidence_id for s in series]})


FEATURES: dict[str, Callable[[FeatureInput, dict[str, Any]], FeatureValue]] = {
    f.__name__: f for f in (
        transit_window_proximity, observation_gap, evidence_quality, evidence_scarcity, alert_freshness, alert_confidence,
        alert_rarity, visibility, instrument_suitability, calibration_suitability, proximity_to_anchor, relationship_support,
        candidate_status, time_series_coverage_gap,
    )
}
