"""Domain model tests: identity invariance, no intrinsic significance, universe integrity."""

from __future__ import annotations

import unittest

from astro.domain import (
    Coordinates, Entity, EntityState, EvidenceRecord, IntrinsicSignificanceError, Provenance,
    RelationshipAssertion, Universe, UniverseError,
)

SYN = Provenance("astro-test-fixture", "synthetic", "unit")


def star(name: str, ra: float = 10.0, dec: float = -20.0, **attrs) -> Entity:
    return Entity.create("star", name, catalogue_ids={"TEST": name}, coordinates=Coordinates(ra, dec), source=SYN, attributes=attrs)


class TestIdentity(unittest.TestCase):
    def test_identity_is_content_derived_and_stable(self):
        a = star("Alpha", magnitude_v=5.0)
        b = star("Alpha", magnitude_v=9.0)     # attributes differ, identity fields do not
        self.assertEqual(a.entity_id, b.entity_id)
        self.assertTrue(a.entity_id.startswith("ENT-"))
        self.assertNotEqual(a.entity_id, star("Beta").entity_id)

    def test_identity_ignores_coordinates_and_source(self):
        a = Entity.create("star", "Gamma", catalogue_ids={"X": "1"}, coordinates=Coordinates(1, 1), source=SYN)
        b = Entity.create("star", "Gamma", catalogue_ids={"X": "1"})
        self.assertEqual(a.entity_id, b.entity_id)

    def test_no_intrinsic_significance_on_entity(self):
        for bad in ("significance", "priority", "importance_score", "rank"):
            with self.assertRaises(IntrinsicSignificanceError):
                star("Delta", **{bad: 1})

    def test_no_intrinsic_significance_in_evidence_values(self):
        s = star("Eps")
        with self.assertRaises(IntrinsicSignificanceError):
            EvidenceRecord.create("photometry", s.entity_id, values={"priority": 3}, source=SYN)

    def test_round_trip_preserves_identity(self):
        s = star("Zeta", magnitude_v=7.5)
        self.assertEqual(Entity.from_record(s.to_record()), s)
        with self.assertRaises(ValueError):
            Entity.from_record({**s.to_record(), "entity_id": "ENT-" + "0" * 64})


class TestEvidenceAndRelationships(unittest.TestCase):
    def test_evidence_identity_and_round_trip(self):
        s = star("Eta")
        e = EvidenceRecord.create("photometry", s.entity_id, values={"mag_v": 8.1}, uncertainty={"mag_v": 0.02},
                                  observed_at="2026-09-01T10:00:00Z", source=SYN, quality=0.9)
        self.assertTrue(e.evidence_id.startswith("EVD-"))
        self.assertEqual(EvidenceRecord.from_record(e.to_record()), e)
        self.assertNotEqual(e.evidence_id, EvidenceRecord.from_record({**e.to_record(), "evidence_id": None, "quality": 0.8}).evidence_id)

    def test_relationship_roles_are_explicit(self):
        a, b = star("A"), star("B")
        with self.assertRaises(ValueError):
            RelationshipAssertion.create("hosts", {"host": a.entity_id}, source=SYN)          # companion unbound
        with self.assertRaises(ValueError):
            RelationshipAssertion.create("near", {"pair": [a.entity_id]}, source=SYN)          # symmetric needs 2
        r = RelationshipAssertion.create("near", {"pair": [b.entity_id, a.entity_id]}, literals={"separation_arcsec": 12.5}, source=SYN)
        r2 = RelationshipAssertion.create("near", {"pair": [a.entity_id, b.entity_id]}, literals={"separation_arcsec": 12.5}, source=SYN)
        self.assertEqual(r.assertion_id, r2.assertion_id)                                        # order-free symmetric identity
        self.assertEqual(r.participants(), tuple(sorted((a.entity_id, b.entity_id))))

    def test_unknown_type_rejected(self):
        with self.assertRaises(ValueError):
            RelationshipAssertion.create("orbits", {"a": "x"}, source=SYN)


class TestUniverse(unittest.TestCase):
    def build(self):
        a, b = star("A"), star("B", 11.0, -21.0)
        e = EvidenceRecord.create("photometry", a.entity_id, values={"mag_v": 8.0}, source=SYN, observed_at="2026-09-01T00:00:00Z")
        r = RelationshipAssertion.create("near", {"pair": [a.entity_id, b.entity_id]}, literals={"separation_arcsec": 30}, evidence_ids=[e.evidence_id], source=SYN)
        st = EntityState(a.entity_id, "2026-09-01T00:00:00Z", observation_status="observed", last_observed_at="2026-09-01T00:00:00Z")
        return a, b, e, r, st, Universe.create("t", "synthetic", [a, b], [e], [r], [st])

    def test_universe_digest_and_lookups(self):
        a, b, e, r, st, u = self.build()
        self.assertTrue(u.universe_id.startswith("UNI-"))
        self.assertEqual(u.evidence_for(a.entity_id, "photometry"), (e,))
        self.assertEqual(u.relationships_of(b.entity_id, "near"), (r,))
        self.assertEqual(u.state_of(a.entity_id), st)
        self.assertEqual(Universe.from_record(u.to_record()).universe_id, u.universe_id)

    def test_universe_rejects_dangling_references(self):
        a = star("A")
        e = EvidenceRecord.create("photometry", star("Ghost").entity_id, values={"mag_v": 1}, source=SYN)
        with self.assertRaises(UniverseError):
            Universe.create("t", "synthetic", [a], [e])
        with self.assertRaises(UniverseError):
            Universe.create("t", "synthetic", [a, a])

    def test_evolution_never_mutates_the_original(self):
        a, b, e, r, st, u = self.build()
        e2 = EvidenceRecord.create("photometry", b.entity_id, values={"mag_v": 9.0}, source=SYN, observed_at="2026-09-02T00:00:00Z")
        u2 = u.with_evidence(e2)
        self.assertNotEqual(u.universe_id, u2.universe_id)
        self.assertEqual(len(u.evidence), 1)
        self.assertEqual(len(u2.evidence), 2)
        self.assertEqual(Universe.create("t", "synthetic", [a, b], [e], [r], [st]).universe_id, u.universe_id)


if __name__ == "__main__":
    unittest.main()
