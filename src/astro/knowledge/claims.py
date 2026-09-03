"""Measurement claims and their contradictions.

Two catalogues that report the same quantity for the same object make two claims. Each becomes a
``measures`` relationship in ASA, supported by its evidence record. Where they disagree beyond a
declared tolerance, Astro records an ``asa.core/contradicts`` meta-claim between them. Nothing is
averaged or silently preferred.
"""

from __future__ import annotations

from typing import Any

from astro.domain import EvidenceRecord, Provenance, RelationshipAssertion, Universe

DERIVED = Provenance("astro-knowledge-claims", "derived", "src/astro/knowledge/claims.py")

# quantity -> (evidence kinds to read, value keys, unit, relative tolerance)
QUANTITIES: dict[str, dict[str, Any]] = {
    "teff_k": {"kinds": ("derived_measurement", "catalogue_measurement"), "keys": ("teff_k",), "unit": "K", "tolerance": 0.07},
    "distance_pc": {"kinds": ("catalogue_measurement", "derived_measurement"), "keys": ("distance_pc",), "unit": "pc", "tolerance": 0.15},
    "period_days": {"kinds": ("ephemeris", "classification"), "keys": ("period_days",), "unit": "d", "tolerance": 0.01},
}


def _source_key(rec: EvidenceRecord) -> str:
    return rec.source.reference.split(":", 1)[0] or rec.source.source


def derive_claims(universe: Universe) -> tuple[list[EvidenceRecord], list[RelationshipAssertion], list[tuple[RelationshipAssertion, RelationshipAssertion]], dict]:
    """Return (derived evidence, claim relationships, contradicting claim pairs, counts)."""
    evidence, claims, contradictions = [], [], []
    counts = {"claims": 0, "contradictions": 0, "derived_distance": 0}
    for entity in universe.entities:
        by_quantity: dict[str, list[tuple[float, EvidenceRecord]]] = {}
        recs = list(universe.evidence_for(entity.entity_id))
        # Gaia parallax → derived distance claim, so it can be compared with a tabulated distance
        for rec in recs:
            if rec.kind == "astrometry" and rec.status == "admissible" and rec.value_map.get("parallax_mas", 0) and float(rec.value_map["parallax_mas"]) > 0:
                plx = float(rec.value_map["parallax_mas"])
                d = EvidenceRecord.create("derived_measurement", entity.entity_id, source=DERIVED, quality=rec.quality, derived_from=[rec.evidence_id],
                                          values={"distance_pc": round(1000.0 / plx, 3), "method": "1000/parallax (no zero-point or prior correction)", "from": _source_key(rec)})
                evidence.append(d)
                recs.append(d)
                counts["derived_distance"] += 1
        for rec in recs:
            if rec.status != "admissible":
                continue
            for q, spec in QUANTITIES.items():
                if rec.kind in spec["kinds"]:
                    for key in spec["keys"]:
                        v = rec.value_map.get(key)
                        if isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0:
                            qname = f"{q}[{rec.value_map['planet']}]" if rec.kind == "ephemeris" and rec.value_map.get("planet") else q
                            by_quantity.setdefault(qname, []).append((float(v), rec))
        for q, items in by_quantity.items():
            spec = QUANTITIES[q.split("[", 1)[0]]
            made = []
            seen = set()
            for value, rec in items:
                src = rec.value_map.get("from", _source_key(rec)) if rec.source.data_class == "derived" else _source_key(rec)
                if (round(value, 6), src) in seen:
                    continue
                seen.add((round(value, 6), src))
                claim = RelationshipAssertion.create("measures", {"subject": entity.entity_id}, literals={"quantity": q, "value": round(value, 6), "unit": spec["unit"], "source_key": src},
                                                     evidence_ids=[rec.evidence_id], confidence=rec.quality, source=DERIVED)
                claims.append(claim)
                made.append((value, claim))
                counts["claims"] += 1
            for i in range(len(made)):
                for j in range(i + 1, len(made)):
                    a, b = made[i][0], made[j][0]
                    if abs(a - b) / max(abs(a), abs(b)) > spec["tolerance"]:
                        contradictions.append((made[i][1], made[j][1]))
                        counts["contradictions"] += 1
    return evidence, claims, contradictions, counts


def contradicting_pairs(universe: Universe) -> list[tuple[RelationshipAssertion, RelationshipAssertion]]:
    """Contradictions among the ``measures`` claims a universe already carries (the same rule as
    :func:`derive_claims`, applied to registered claims so that any load path — store build, session
    cycle, benchmark bootstrap — records the same disputes in ASA)."""
    by: dict[tuple[str, str], list[RelationshipAssertion]] = {}
    for rel in universe.relationships:
        if rel.relationship_type != "measures":
            continue
        lit = rel.literal_map
        if "quantity" not in lit or "value" not in lit:
            continue
        by.setdefault((rel.role_map["subject"][0], str(lit["quantity"])), []).append(rel)
    pairs = []
    for (_, q), claims in by.items():
        spec = QUANTITIES.get(q.split("[", 1)[0])
        if spec is None or len(claims) < 2:
            continue
        for i in range(len(claims)):
            for j in range(i + 1, len(claims)):
                a, b = float(claims[i].literal_map["value"]), float(claims[j].literal_map["value"])
                if max(abs(a), abs(b)) > 0 and abs(a - b) / max(abs(a), abs(b)) > spec["tolerance"]:
                    pairs.append((claims[i], claims[j]))
    return pairs
