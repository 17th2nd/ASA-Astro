"""Derive the knowledge frontier for a universe and write it into the universe and ASA."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from astro.asa.adapter import AstroAdapter
from astro.domain import Entity, EvidenceRecord, Provenance, RelationshipAssertion, Universe
from .claims import derive_claims
from .expectations import expected_kinds
from .geometry import derive_geometry
from .tiles import derive_tiles

DERIVED = Provenance("astro-knowledge-frontier", "derived", "src/astro/knowledge/frontier.py")


@dataclass
class Frontier:
    as_of: str
    entities: list[Entity] = field(default_factory=list)
    evidence: list[EvidenceRecord] = field(default_factory=list)
    relationships: list[RelationshipAssertion] = field(default_factory=list)
    contradictions: list[tuple[RelationshipAssertion, RelationshipAssertion]] = field(default_factory=list)
    counts: dict[str, Any] = field(default_factory=dict)

    def apply(self, universe: Universe, label: str | None = None) -> Universe:
        return Universe.create(label or universe.label + "+frontier", universe.data_class, list(universe.entities) + self.entities,
                               list(universe.evidence) + self.evidence, list(universe.relationships) + self.relationships, universe.states)


def derive_gaps(universe: Universe, as_of: str) -> tuple[list[EvidenceRecord], list[RelationshipAssertion], dict]:
    evidence, rels, by_kind = [], [], {}
    for entity in universe.entities:
        present = {r.kind for r in universe.evidence_for(entity.entity_id) if r.status == "admissible"}
        for exp in expected_kinds(entity, universe):
            if exp.evidence_kind in present:
                continue
            rels.append(RelationshipAssertion.create("lacks_evidence", {"subject": entity.entity_id}, literals={"evidence_kind": exp.evidence_kind, "expectation_ref": exp.ref, "as_of": as_of},
                                                     confidence=1.0, source=DERIVED))
            by_kind[exp.evidence_kind] = by_kind.get(exp.evidence_kind, 0) + 1
    return evidence, rels, {"gaps": len(rels), "by_missing_kind": dict(sorted(by_kind.items()))}


def derive_frontier(universe: Universe, as_of: str, *, tiles: bool = True) -> Frontier:
    f = Frontier(as_of)
    ev, rels, c = derive_gaps(universe, as_of)
    f.evidence += ev; f.relationships += rels; f.counts["gaps"] = c
    ev, rels, c = derive_geometry(universe)
    f.evidence += ev; f.relationships += rels; f.counts["geometry"] = c
    ev, claims, contradictions, c = derive_claims(universe)
    f.evidence += ev; f.relationships += claims; f.contradictions += contradictions; f.counts["claims"] = c
    if tiles:
        ents, ev, c = derive_tiles(universe)
        f.entities += ents; f.evidence += ev; f.counts["tiles"] = c
    return f


def load_frontier(adapter: AstroAdapter, universe_with_frontier: Universe, frontier: Frontier) -> dict[str, Any]:
    """Register the frontier universe in ASA, then the contradictions between registered claims, then retire
    lacks-evidence relationships whose evidence has since arrived."""
    counts = adapter.load_universe(universe_with_frontier)
    recorded = 0
    for a, b in frontier.contradictions:
        ka, kb = adapter.find_relationship(a), adapter.find_relationship(b)
        if ka and kb and adapter.propose_contradiction(ka, kb) is not None:
            recorded += 1
    counts["contradictions"] = recorded
    present_gaps = {(r.role_map["subject"][0], r.literal_map["evidence_kind"]) for r in frontier.relationships if r.relationship_type == "lacks_evidence"}
    retired = 0
    snap = adapter.snapshot()
    for edge in snap.edges:
        if edge.type_name == "lacks_evidence" and edge.lifecycle == "registered":
            subject = dict(edge.bindings)["subject"][0]
            if (subject, dict(edge.literals).get("evidence_kind")) not in present_gaps:
                adapter.retire_relationship(edge.key, "evidence-arrived")
                retired += 1
    counts["gaps_retired"] = retired
    return counts
