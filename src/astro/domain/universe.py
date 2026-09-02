"""The astronomical universe as presented to Astro: an immutable, digest-identified bundle."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

from .entities import Entity
from .evidence import EvidenceRecord
from .identity import DATA_CLASSES, content_id
from .relationships import RelationshipAssertion
from .state import EntityState


class UniverseError(ValueError):
    """The universe is internally inconsistent."""


@dataclass(frozen=True)
class Universe:
    universe_id: str
    label: str
    data_class: str
    entities: tuple[Entity, ...]
    evidence: tuple[EvidenceRecord, ...]
    relationships: tuple[RelationshipAssertion, ...]
    states: tuple[EntityState, ...]

    def _index(self) -> dict[str, Any]:
        """Derived lookup tables, built once per (immutable) universe; never part of identity."""
        idx = self.__dict__.get("_idx")
        if idx is None:
            by_entity = {e.entity_id: e for e in self.entities}
            by_name: dict[str, Entity] = {}
            for e in self.entities:
                by_name.setdefault(e.designation, e)
                for a in e.aliases:
                    by_name.setdefault(a, e)
            ev_by_subject: dict[str, list[EvidenceRecord]] = {}
            for ev in self.evidence:
                ev_by_subject.setdefault(ev.subject_id, []).append(ev)
            rel_by_participant: dict[str, list[RelationshipAssertion]] = {}
            for r in self.relationships:
                for p in r.participants():
                    rel_by_participant.setdefault(p, []).append(r)
            by_cat = {(c, i): e for e in self.entities for c, i in e.catalogue_ids}
            idx = {"entity": by_entity, "name": by_name, "evidence": ev_by_subject, "relationships": rel_by_participant,
                   "state": {s.entity_id: s for s in self.states}, "catalogue": by_cat}
            object.__setattr__(self, "_idx", idx)
        return idx

    @classmethod
    def create(
        cls,
        label: str,
        data_class: str,
        entities: Iterable[Entity],
        evidence: Iterable[EvidenceRecord] = (),
        relationships: Iterable[RelationshipAssertion] = (),
        states: Iterable[EntityState] = (),
    ) -> "Universe":
        if data_class not in DATA_CLASSES:
            raise UniverseError(f"data_class {data_class!r} not in {DATA_CLASSES}")
        ents = tuple(sorted(entities, key=lambda e: e.entity_id))
        evs = tuple(sorted(evidence, key=lambda e: e.evidence_id))
        rels = tuple(sorted(relationships, key=lambda r: r.assertion_id))
        sts = tuple(sorted(states, key=lambda s: (s.entity_id, s.as_of)))
        cls._validate(ents, evs, rels, sts)
        digest_payload = {
            "label": label, "data_class": data_class,
            "entities": [e.to_record() for e in ents], "evidence": [e.to_record() for e in evs],
            "relationships": [r.to_record() for r in rels], "states": [s.to_record() for s in sts],
        }
        return cls(content_id("UNI", digest_payload), label, data_class, ents, evs, rels, sts)

    @staticmethod
    def _validate(ents, evs, rels, sts) -> None:
        ids = [e.entity_id for e in ents]
        if len(set(ids)) != len(ids):
            raise UniverseError("duplicate entity identity")
        known = set(ids)
        ev_ids = [e.evidence_id for e in evs]
        if len(set(ev_ids)) != len(ev_ids):
            raise UniverseError("duplicate evidence identity")
        ev_ids = set(ev_ids)
        for ev in evs:
            if ev.subject_id not in known:
                raise UniverseError(f"evidence {ev.evidence_id} subject {ev.subject_id} unknown")
            if ev.instrument_id and ev.instrument_id not in known:
                raise UniverseError(f"evidence {ev.evidence_id} instrument {ev.instrument_id} unknown")
            for dep in ev.derived_from:
                if dep not in set(ev_ids):
                    raise UniverseError(f"evidence {ev.evidence_id} derived from unknown {dep}")
        for rel in rels:
            for ref in rel.participants():
                if ref not in known:
                    raise UniverseError(f"relationship {rel.assertion_id} binds unknown entity {ref}")
            for eid in rel.evidence_ids:
                if eid not in set(ev_ids):
                    raise UniverseError(f"relationship {rel.assertion_id} cites unknown evidence {eid}")
        seen = set()
        for st in sts:
            if st.entity_id not in known:
                raise UniverseError(f"state for unknown entity {st.entity_id}")
            if st.entity_id in seen:
                raise UniverseError(f"entity {st.entity_id} has more than one current state")
            seen.add(st.entity_id)

    # ---- lookups -------------------------------------------------------------
    def entity(self, entity_id: str) -> Entity:
        return self._index()["entity"][entity_id]

    def find(self, designation: str) -> Entity:
        return self._index()["name"][designation]

    def find_by_catalogue(self, catalogue: str, identifier: str) -> Entity:
        return self._index()["catalogue"][(catalogue, identifier)]

    def evidence_for(self, entity_id: str, kind: str | None = None) -> tuple[EvidenceRecord, ...]:
        return tuple(e for e in self._index()["evidence"].get(entity_id, ()) if kind is None or e.kind == kind)

    def relationships_of(self, entity_id: str, relationship_type: str | None = None) -> tuple[RelationshipAssertion, ...]:
        return tuple(r for r in self._index()["relationships"].get(entity_id, ())
                     if relationship_type is None or r.relationship_type == relationship_type)

    def state_of(self, entity_id: str) -> EntityState | None:
        return self._index()["state"].get(entity_id)

    # ---- evolution (always a new universe; the old one is untouched) ----------
    def with_evidence(self, *new_evidence: EvidenceRecord, label: str | None = None) -> "Universe":
        return Universe.create(label or self.label, self.data_class, self.entities, self.evidence + tuple(new_evidence),
                               self.relationships, self.states)

    def with_evidence_status(self, evidence_id: str, status: str, label: str | None = None) -> "Universe":
        """Change one evidence record's lifecycle status (e.g. ``superseded``); its identity is unchanged."""
        found = False
        evidence = []
        for e in self.evidence:
            if e.evidence_id == evidence_id:
                evidence.append(e.with_status(status))
                found = True
            else:
                evidence.append(e)
        if not found:
            raise UniverseError(f"evidence {evidence_id} not in universe")
        return Universe.create(label or self.label, self.data_class, self.entities, evidence, self.relationships, self.states)

    def supersede_evidence(self, old_evidence_id: str, new_record: EvidenceRecord, label: str | None = None) -> "Universe":
        """Register a replacement record and mark the old one superseded, in one step."""
        return self.with_evidence(new_record, label=label).with_evidence_status(old_evidence_id, "superseded", label=label)

    def with_relationships(self, *new: RelationshipAssertion, label: str | None = None) -> "Universe":
        return Universe.create(label or self.label, self.data_class, self.entities, self.evidence,
                               self.relationships + tuple(new), self.states)

    def with_states(self, *new_states: EntityState, label: str | None = None) -> "Universe":
        replaced = {s.entity_id: s for s in new_states}
        kept = tuple(s for s in self.states if s.entity_id not in replaced)
        return Universe.create(label or self.label, self.data_class, self.entities, self.evidence, self.relationships,
                               kept + tuple(replaced.values()))

    # ---- serialization --------------------------------------------------------
    def to_record(self) -> dict[str, Any]:
        return {
            "universe_id": self.universe_id, "label": self.label, "data_class": self.data_class,
            "entities": [e.to_record() for e in self.entities], "evidence": [e.to_record() for e in self.evidence],
            "relationships": [r.to_record() for r in self.relationships], "states": [s.to_record() for s in self.states],
        }

    @classmethod
    def from_record(cls, r: Mapping[str, Any]) -> "Universe":
        universe = cls.create(
            r["label"], r["data_class"],
            [Entity.from_record(e) for e in r.get("entities", [])],
            [EvidenceRecord.from_record(e) for e in r.get("evidence", [])],
            [RelationshipAssertion.from_record(x) for x in r.get("relationships", [])],
            [EntityState.from_record(s) for s in r.get("states", [])],
        )
        if r.get("universe_id") and r["universe_id"] != universe.universe_id:
            raise UniverseError(f"universe_id {r['universe_id']} does not match content identity {universe.universe_id}")
        return universe

    @classmethod
    def load(cls, path: str | Path) -> "Universe":
        return cls.from_record(json.loads(Path(path).read_text(encoding="utf-8")))

    def save(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps(self.to_record(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
