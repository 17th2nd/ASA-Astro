"""Universe fragments produced by parsers, merged into one universe."""

from __future__ import annotations

from dataclasses import dataclass, field

from astro.domain import Entity, EntityState, EvidenceRecord, RelationshipAssertion, Universe


@dataclass
class Fragment:
    source_key: str
    entities: list[Entity] = field(default_factory=list)
    evidence: list[EvidenceRecord] = field(default_factory=list)
    relationships: list[RelationshipAssertion] = field(default_factory=list)
    states: list[EntityState] = field(default_factory=list)
    skipped: list[dict] = field(default_factory=list)

    def summary(self) -> dict:
        return {"source": self.source_key, "entities": len(self.entities), "evidence": len(self.evidence),
                "relationships": len(self.relationships), "states": len(self.states), "skipped": len(self.skipped)}


def merge_fragments(label: str, *fragments: Fragment, extra_entities: list[Entity] = ()) -> Universe:
    """Merge by identity: the same entity from two catalogues is one entity (first record wins), evidence and
    relationships accumulate. The result is labelled ``real`` — every record's own provenance still says which
    source it came from and whether it is real or derived."""
    seen_e, seen_v, seen_r = {}, {}, {}
    for e in list(extra_entities) + [e for f in fragments for e in f.entities]:
        seen_e.setdefault(e.entity_id, e)
    for f in fragments:
        for v in f.evidence:
            seen_v.setdefault(v.evidence_id, v)
        for r in f.relationships:
            seen_r.setdefault(r.assertion_id, r)
    states = {}
    for f in fragments:
        for s in f.states:
            states[s.entity_id] = s
    return Universe.create(label, "real", list(seen_e.values()), list(seen_v.values()), list(seen_r.values()), list(states.values()))
