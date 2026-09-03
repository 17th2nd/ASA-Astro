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


def derive_geometry(universe: Universe, *, near_arcsec: float = 900.0, comparison_delta_mag: float = 1.5,
                    transient_arcsec: float = 60.0) -> tuple[list[EvidenceRecord], list[RelationshipAssertion], dict]:
    evidence, relationships = [], []
    hosts = [e for e in universe.entities if e.kind == "star" and any(e.entity_id in r.role_map.get("host", ()) for r in universe.relationships_of(e.entity_id, "hosts"))]
    stars = [e for e in universe.entities if e.kind in ("star", "variable_star") and e.coordinates is not None]
    clusters = [e for e in universe.entities if e.kind == "star_cluster" and e.coordinates is not None and "r50_deg" in e.attribute_map]
    galaxies = [e for e in universe.entities if e.kind == "galaxy" and e.coordinates is not None]
    transients = [e for e in universe.entities if e.kind == "transient" and e.coordinates is not None]
    star_grid, cluster_grid, galaxy_grid = SkyGrid(stars), SkyGrid(clusters), SkyGrid(galaxies)
    counts = {"near": 0, "comparison_star_for": 0, "member_of": 0, "hosted_transient": 0}
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
        plx = None
        for rec in universe.evidence_for(host.entity_id, "astrometry"):
            if "parallax_mas" in rec.value_map:
                plx, plx_err = float(rec.value_map["parallax_mas"]), float(rec.uncertainty_map.get("parallax_mas", 0.1))
        if plx is not None:
            for cl, sep in cluster_grid.near(host.coordinates.ra_deg, host.coordinates.dec_deg, 3600.0 * 5):
                r50 = float(cl.attribute_map["r50_deg"]) * 3600.0
                cplx = cl.attribute_map.get("parallax_mas")
                if sep <= 2.0 * r50 and cplx is not None and abs(plx - float(cplx)) <= max(0.3, 3 * plx_err):
                    agree = 1.0 - min(1.0, abs(plx - float(cplx)) / max(0.3, 3 * plx_err))
                    rec = EvidenceRecord.create("derived_measurement", host.entity_id, source=DERIVED, quality=0.8,
                                                values={"cluster": cl.entity_id, "separation_over_r50": round(sep / r50, 3), "parallax_host_mas": plx, "parallax_cluster_mas": float(cplx),
                                                        "method": "within 2 r50 and parallax agreement within max(0.3 mas, 3σ)"})
                    evidence.append(rec)
                    relationships.append(RelationshipAssertion.create("member_of", {"member": host.entity_id, "group": cl.entity_id}, evidence_ids=[rec.evidence_id],
                                                                      confidence=round(0.5 + 0.4 * agree, 3), source=DERIVED, status="candidate"))
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
