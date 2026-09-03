"""Relationships derived from geometry: proximity, cluster membership, transient hosting.

Everything here is labelled ``derived``. A derived relationship is asserted with a
``derived_measurement`` evidence record (the separation or parallax agreement) so ASA endorses it
on that basis; where the geometry is only suggestive (a comparison-star candidate) the relationship
is asserted without evidence and stays *unevaluated* in ASA — that is the semantic edge, on record.
"""

from __future__ import annotations

import math
from collections import defaultdict
from typing import Iterable

from astro.domain import Entity, EvidenceRecord, Provenance, RelationshipAssertion, Universe

DERIVED = Provenance("astro-knowledge-geometry", "derived", "src/astro/knowledge/geometry.py")
CELL_DEG = 2.0


def separation_arcsec(ra1: float, dec1: float, ra2: float, dec2: float) -> float:
    """Angular separation via the haversine formula, in arcseconds."""
    r1, d1, r2, d2 = map(math.radians, (ra1, dec1, ra2, dec2))
    a = math.sin((d2 - d1) / 2) ** 2 + math.cos(d1) * math.cos(d2) * math.sin((r2 - r1) / 2) ** 2
    return math.degrees(2 * math.asin(min(1.0, math.sqrt(a)))) * 3600.0


class SkyGrid:
    """Coarse cell index over entities with coordinates; neighbours within ``radius_arcsec``."""

    def __init__(self, entities: Iterable[Entity]):
        self.cells: dict[tuple[int, int], list[Entity]] = defaultdict(list)
        for e in entities:
            if e.coordinates is not None:
                self.cells[self._cell(e.coordinates.ra_deg, e.coordinates.dec_deg)].append(e)

    @staticmethod
    def _cell(ra: float, dec: float) -> tuple[int, int]:
        return int(ra // CELL_DEG), int((dec + 90.0) // CELL_DEG)

    def near(self, ra: float, dec: float, radius_arcsec: float) -> list[tuple[Entity, float]]:
        reach = max(1, int(math.ceil(radius_arcsec / 3600.0 / CELL_DEG)))
        cx, cy = self._cell(ra, dec)
        out = []
        for dx in range(-reach, reach + 1):
            for dy in range(-reach, reach + 1):
                for e in self.cells.get(((cx + dx) % int(360 // CELL_DEG), cy + dy), ()):
                    sep = separation_arcsec(ra, dec, e.coordinates.ra_deg, e.coordinates.dec_deg)
                    if sep <= radius_arcsec:
                        out.append((e, sep))
        return sorted(out, key=lambda t: (t[1], t[0].entity_id))


def _mag(e: Entity, universe: Universe) -> float | None:
    a = e.attribute_map
    for key in ("magnitude_v", "magnitude_max", "magnitude_g"):
        if key in a:
            return float(a[key])
    for rec in universe.evidence_for(e.entity_id, "photometry"):
        for key in ("mag_v", "mag_g"):
            if key in rec.value_map:
                return float(rec.value_map[key])
    return None


KM_S_PER_MAS_YR_AT_1KPC = 4.74047  # tangential velocity: v = 4.74047 · μ[mas/yr] / ϖ[mas]  (km/s)


def derive_geometry(universe: Universe, *, near_arcsec: float = 900.0, comparison_delta_mag: float = 1.5,
                    transient_arcsec: float = 60.0, max_tangential_km_s: float = 3.0, max_ruwe: float = 1.4) -> tuple[list[EvidenceRecord], list[RelationshipAssertion], dict]:
    """Cluster membership (2026-09-04 revision): position within 2 r50 and parallax agreement are necessary but not
    sufficient — the 2026-09-03 candidates GPX-1/Trumpler 2, Kepler-1383/HSC_603, Kepler-780/HSC_565 and
    KOI-94/CWNU_1183 all passed them and all fail on proper motion (Δv_tan 20–130 km/s; GPX-1 was ruled out by its
    discovery paper on exactly this test). Membership is therefore *endorsed* only when host and cluster proper
    motions agree to ``max_tangential_km_s`` and the host's Gaia RUWE is at most ``max_ruwe``; with no proper motion
    on either side, or an untrustworthy RUWE, the relationship is asserted without evidence and stays unevaluated;
    with disagreeing proper motions no relationship is asserted at all."""
    evidence, relationships = [], []
    hosts = [e for e in universe.entities if e.kind == "star" and any(e.entity_id in r.role_map.get("host", ()) for r in universe.relationships_of(e.entity_id, "hosts"))]
    stars = [e for e in universe.entities if e.kind in ("star", "variable_star") and e.coordinates is not None]
    clusters = [e for e in universe.entities if e.kind == "star_cluster" and e.coordinates is not None and "r50_deg" in e.attribute_map]
    galaxies = [e for e in universe.entities if e.kind == "galaxy" and e.coordinates is not None]
    transients = [e for e in universe.entities if e.kind == "transient" and e.coordinates is not None]
    star_grid, cluster_grid, galaxy_grid = SkyGrid(stars), SkyGrid(clusters), SkyGrid(galaxies)
    counts = {"near": 0, "comparison_star_for": 0, "member_of": 0, "member_of_unevaluated": 0, "member_of_rejected_proper_motion": 0, "hosted_transient": 0}
    seen_pairs = set()
    for host in hosts:
        if host.coordinates is None:
            continue
        hmag = _mag(host, universe)
        for other, sep in star_grid.near(host.coordinates.ra_deg, host.coordinates.dec_deg, near_arcsec):
            if other.entity_id == host.entity_id:
                continue
            pair = tuple(sorted((host.entity_id, other.entity_id)))
            if pair in seen_pairs:
                continue
            seen_pairs.add(pair)
            sep_rec = EvidenceRecord.create("derived_measurement", host.entity_id, source=DERIVED, quality=0.95,
                                            values={"angular_separation_arcsec": round(sep, 3), "other": other.entity_id, "method": "haversine on catalogue coordinates"})
            evidence.append(sep_rec)
            relationships.append(RelationshipAssertion.create("near", {"pair": list(pair)}, literals={"separation_arcsec": round(sep, 3)}, evidence_ids=[sep_rec.evidence_id],
                                                              confidence=0.99, source=DERIVED))
            counts["near"] += 1
            omag = _mag(other, universe)
            if other.kind == "star" and hmag is not None and omag is not None and abs(hmag - omag) <= comparison_delta_mag:
                # suggestive only: no photometric stability is known → asserted without evidence, stays unevaluated in ASA
                relationships.append(RelationshipAssertion.create("comparison_star_for", {"comparison": other.entity_id, "target": host.entity_id}, confidence=0.5, source=DERIVED, status="candidate"))
                counts["comparison_star_for"] += 1
        plx = pm = ruwe = None
        for rec in universe.evidence_for(host.entity_id, "astrometry"):
            if "parallax_mas" in rec.value_map:
                plx, plx_err = float(rec.value_map["parallax_mas"]), float(rec.uncertainty_map.get("parallax_mas", 0.1))
                if "pmra_mas_yr" in rec.value_map and "pmdec_mas_yr" in rec.value_map:
                    pm = (float(rec.value_map["pmra_mas_yr"]), float(rec.value_map["pmdec_mas_yr"]))
                if rec.value_map.get("ruwe") is not None:
                    ruwe = float(rec.value_map["ruwe"])
        if plx is not None and plx > 0:
            for cl, sep in cluster_grid.near(host.coordinates.ra_deg, host.coordinates.dec_deg, 3600.0 * 5):
                r50 = float(cl.attribute_map["r50_deg"]) * 3600.0
                cplx = cl.attribute_map.get("parallax_mas")
                if not (sep <= 2.0 * r50 and cplx is not None and abs(plx - float(cplx)) <= max(0.3, 3 * plx_err)):
                    continue
                cpm = (cl.attribute_map.get("pmra_mas_yr"), cl.attribute_map.get("pmdec_mas_yr"))
                roles = {"member": host.entity_id, "group": cl.entity_id}
                if pm is None or None in cpm or (ruwe is not None and ruwe > max_ruwe):
                    # geometry alone is suggestive, not evidence: on record, unevaluated
                    # (reason — untrusted RUWE or missing proper motion — is deliberately not a literal: it is not identity)
                    relationships.append(RelationshipAssertion.create("member_of", roles, confidence=0.3, source=DERIVED, status="candidate"))
                    counts["member_of_unevaluated"] += 1
                    continue
                dmu = math.hypot(pm[0] - float(cpm[0]), pm[1] - float(cpm[1]))
                dv = KM_S_PER_MAS_YR_AT_1KPC * dmu / plx
                if dv > max_tangential_km_s:
                    counts["member_of_rejected_proper_motion"] += 1
                    continue
                agree_plx = 1.0 - min(1.0, abs(plx - float(cplx)) / max(0.3, 3 * plx_err))
                agree_pm = 1.0 - dv / max_tangential_km_s
                rec = EvidenceRecord.create("derived_measurement", host.entity_id, source=DERIVED, quality=0.8,
                                            values={"cluster": cl.entity_id, "separation_over_r50": round(sep / r50, 3), "parallax_host_mas": plx, "parallax_cluster_mas": float(cplx),
                                                    "proper_motion_host_mas_yr": [pm[0], pm[1]], "proper_motion_cluster_mas_yr": [float(cpm[0]), float(cpm[1])],
                                                    "delta_tangential_velocity_km_s": round(dv, 3), "host_ruwe": ruwe,
                                                    "method": f"within 2 r50, parallax agreement within max(0.3 mas, 3σ), tangential velocity agreement within {max_tangential_km_s} km/s, RUWE ≤ {max_ruwe}"})
                evidence.append(rec)
                relationships.append(RelationshipAssertion.create("member_of", roles, evidence_ids=[rec.evidence_id],
                                                                  confidence=round(0.5 + 0.25 * agree_plx + 0.2 * agree_pm, 3), source=DERIVED, status="candidate"))
                counts["member_of"] += 1
    for tr in transients:
        for gal, sep in galaxy_grid.near(tr.coordinates.ra_deg, tr.coordinates.dec_deg, max(transient_arcsec, 60.0 * 3)):
            major = float(gal.attribute_map.get("major_axis_arcmin", 0.0)) * 60.0
            if sep <= max(transient_arcsec, 0.75 * major):
                rec = EvidenceRecord.create("derived_measurement", tr.entity_id, source=DERIVED, quality=0.8,
                                            values={"galaxy": gal.entity_id, "angular_separation_arcsec": round(sep, 2), "galaxy_major_axis_arcsec": round(major, 1), "method": "separation within 0.75 major axis or 60 arcsec"})
                evidence.append(rec)
                relationships.append(RelationshipAssertion.create("hosted_transient", {"host": gal.entity_id, "transient": tr.entity_id}, evidence_ids=[rec.evidence_id],
                                                                  confidence=0.7, source=DERIVED, status="candidate"))
                counts["hosted_transient"] += 1
                break
    return evidence, relationships, counts
