"""Declared expectations: which evidence kinds an entity of a given kind ought to have, and why.

An expectation is a scientific statement about completeness, not a rule of the engine. Each has an
identifier so a gap record can say which expectation it fails.
"""

from __future__ import annotations

from dataclasses import dataclass

from astro.domain import Entity, Universe
from astro.domain.identity import content_id


@dataclass(frozen=True, slots=True)
class Expectation:
    kind: str                 # entity kind
    evidence_kind: str
    rationale: str
    condition: str = "always"  # always | transiting_host | has_alert | bright (within the programme's 1 m-class reach, V ≤ 14)

    @property
    def ref(self) -> str:
        return content_id("EXP", {"kind": self.kind, "evidence_kind": self.evidence_kind, "condition": self.condition})


BRIGHT_LIMIT_MAG = 14.0   # scope of the current instrument class; a declared boundary, recorded on every gap it excludes

EXPECTATIONS: tuple[Expectation, ...] = (
    Expectation("star", "ephemeris", "A transiting-planet host needs a current transit ephemeris to be observable on purpose.", "transiting_host"),
    Expectation("star", "astrometry", "Position, parallax and proper motion fix identity and distance.", "transiting_host"),
    Expectation("star", "photometry", "Calibrated brightness sets exposure and feasibility.", "transiting_host"),
    Expectation("star", "spectrum", "A spectrum constrains stellar parameters that planet radius and mass depend on.", "transiting_host"),
    Expectation("star", "time_series", "A light curve tests the ephemeris and reveals additional transits or activity.", "transiting_host"),
    Expectation("variable_star", "time_series", "A variable star's class and period are only as good as its light curve.", "bright"),
    Expectation("variable_star", "classification", "An assigned variability class.", "bright"),
    Expectation("variable_star", "photometry", "Calibrated magnitudes.", "bright"),
    Expectation("transient", "spectrum", "Classification of a transient needs a spectrum.", "has_alert"),
    Expectation("transient", "photometry", "A light curve after discovery tracks its evolution.", "has_alert"),
    Expectation("galaxy", "catalogue_measurement", "A magnitude or redshift places the galaxy.", "always"),
    Expectation("star_cluster", "catalogue_measurement", "Distance, age and membership.", "always"),
)


def _condition_holds(exp: Expectation, entity: Entity, universe: Universe) -> bool:
    if exp.condition == "always":
        return True
    if exp.condition == "transiting_host":
        return any(r.relationship_type == "hosts" and entity.entity_id in r.role_map.get("host", ()) for r in universe.relationships_of(entity.entity_id, "hosts")) \
            and bool(universe.evidence_for(entity.entity_id, "ephemeris") or universe.evidence_for(entity.entity_id, "photometry"))
    if exp.condition == "has_alert":
        return bool(universe.evidence_for(entity.entity_id, "alert"))
    if exp.condition == "bright":
        m = entity.attribute_map.get("magnitude_max", entity.attribute_map.get("magnitude_v"))
        return m is not None and float(m) <= BRIGHT_LIMIT_MAG
    return False


def expected_kinds(entity: Entity, universe: Universe) -> tuple[Expectation, ...]:
    return tuple(e for e in EXPECTATIONS if e.kind == entity.kind and _condition_holds(e, entity, universe))
