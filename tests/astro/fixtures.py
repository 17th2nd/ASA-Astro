"""Shared synthetic fixtures for Astro tests (labelled synthetic; no real measurements)."""

from __future__ import annotations

from pathlib import Path

from astro.domain import Coordinates, Entity, EntityState, EvidenceRecord, Provenance, RelationshipAssertion, Universe

ROOT = Path(__file__).resolve().parents[2]
FACET = ROOT / "registry" / "relationship_types.astro.candidate.json"
SYN = Provenance("astro-test-fixture", "synthetic", "tests/astro/fixtures.py")


def small_universe() -> Universe:
    host = Entity.create("star", "SYN-HOST-1", catalogue_ids={"SYN": "1"}, coordinates=Coordinates(30.0, -25.0), source=SYN,
                         attributes={"magnitude_v": 9.2, "spectral_type": "G5V"})
    planet = Entity.create("exoplanet", "SYN-HOST-1 b", catalogue_ids={"SYN": "1b"}, source=SYN)
    plain = Entity.create("star", "SYN-PLAIN-2", catalogue_ids={"SYN": "2"}, coordinates=Coordinates(31.0, -24.5), source=SYN,
                          attributes={"magnitude_v": 10.1})
    inst = Entity.create("telescope", "SYN-SCOPE", catalogue_ids={"SYN": "T1"}, source=SYN, attributes={"aperture_m": 0.5})
    eph = EvidenceRecord.create("ephemeris", host.entity_id, values={"period_days": 3.5, "epoch_utc": "2026-09-01T02:00:00Z", "duration_hours": 2.4},
                                source=SYN, quality=0.9)
    phot = EvidenceRecord.create("photometry", host.entity_id, values={"mag_v": 9.2}, uncertainty={"mag_v": 0.01},
                                 observed_at="2026-08-20T03:00:00Z", source=SYN, quality=0.95, instrument_id=inst.entity_id)
    hosts = RelationshipAssertion.create("hosts", {"host": host.entity_id, "companion": planet.entity_id}, evidence_ids=[eph.evidence_id],
                                         confidence=0.97, source=SYN)
    near = RelationshipAssertion.create("near", {"pair": [host.entity_id, plain.entity_id]}, literals={"separation_arcsec": 1800}, source=SYN)
    st = EntityState(host.entity_id, "2026-09-01T00:00:00Z", observation_status="observed", last_observed_at="2026-08-20T03:00:00Z")
    return Universe.create("small", "synthetic", [host, planet, plain, inst], [eph, phot], [hosts, near], [st])
