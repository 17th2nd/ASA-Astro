"""Sky coverage: the sky as regions, so emptiness has an identity and can compete for attention."""

from __future__ import annotations

from astro.domain import Coordinates, Entity, EvidenceRecord, Provenance, Universe

DERIVED = Provenance("astro-knowledge-tiles", "derived", "src/astro/knowledge/tiles.py")
TILE_DEG = 10.0


def tile_designation(ra: float, dec: float) -> str:
    return f"TILE-RA{int(ra // TILE_DEG) * int(TILE_DEG):03d}-DEC{int((dec + 90.0) // TILE_DEG) * int(TILE_DEG) - 90:+03d}"


def derive_tiles(universe: Universe) -> tuple[list[Entity], list[EvidenceRecord], dict]:
    counts: dict[str, dict[str, int]] = {}
    for e in universe.entities:
        if e.coordinates is None or e.kind in ("site", "sky_region"):
            continue
        d = tile_designation(e.coordinates.ra_deg, e.coordinates.dec_deg)
        c = counts.setdefault(d, {"entities": 0, "evidence": 0})
        c["entities"] += 1
        c["evidence"] += len(universe.evidence_for(e.entity_id))
    tiles, evidence = [], []
    densities = sorted(c["evidence"] for c in counts.values())
    n_ra, n_dec = int(360 / TILE_DEG), int(180 / TILE_DEG)
    for i in range(n_ra):
        for j in range(n_dec):
            ra0, dec0 = i * TILE_DEG, j * TILE_DEG - 90.0
            d = tile_designation(ra0 + 0.01, dec0 + 0.01)
            tile = Entity.create("sky_region", d, catalogue_ids={"ASTRO-TILE": d}, coordinates=Coordinates(ra0 + TILE_DEG / 2, min(89.99, dec0 + TILE_DEG / 2)),
                                 source=DERIVED, attributes={"ra_min_deg": ra0, "ra_max_deg": ra0 + TILE_DEG, "dec_min_deg": dec0, "dec_max_deg": dec0 + TILE_DEG, "tiling": "10x10 degree equirectangular"})
            tiles.append(tile)
            c = counts.get(d, {"entities": 0, "evidence": 0})
            rank = sum(1 for x in densities if x < c["evidence"]) / max(1, len(densities))
            evidence.append(EvidenceRecord.create("catalogue_measurement", tile.entity_id, source=DERIVED, quality=1.0,
                                                  values={"entities": c["entities"], "evidence_records": c["evidence"], "density_percentile": round(rank, 4), "note": "counts over the merged universe at derivation time"}))
            if c["evidence"] == 0 or rank < 0.25:
                evidence.append(EvidenceRecord.create("coverage_gap", tile.entity_id, source=DERIVED, quality=1.0,
                                                      values={"missing_kind": "any", "expectation_ref": "EXP-tile-density", "rationale": "region in the lowest quartile of evidence density (or empty) across the merged universe",
                                                              "density_percentile": round(rank, 4)}))
    return tiles, evidence, {"tiles": len(tiles), "populated": len(counts), "gap_tiles": sum(1 for v in evidence if v.kind == "coverage_gap")}
