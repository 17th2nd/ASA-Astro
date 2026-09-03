"""Astro → ASA adapter.

Translates the Astro universe into ASA Kernel consumer-contract calls and reads
ASA relational state back as a :class:`RelationalSnapshot`. It imports only
``asa_kernel.api``, ``asa_kernel.identity`` and ``asa_kernel.storage`` — the same
surface the ASAW adapter is held to. No storage, governor or projection internals.

Mapping
-------
- Entity            → UAO ``asa:uao:astro/<32 hex>`` (attributes: kind, astro_id, designation, record_digest)
- EvidenceRecord    → UAO (kind ``evidence``) + definitional URO ``astro/evidence-of@1`` (record → subject)
- Relationship      → URO of the matching ``astro/*`` type; each cited evidence UAO adds an
                      ``asa.core/supports@1`` URO, which endorses a ``supported`` relationship
- EntityState       → definitional URO ``astro/observation-state@1``; a newer state supersedes the older

Numbers that reach the kernel are restricted decimal strings (JCS §6). Full-precision
values stay in the Astro universe, bound to the kernel record by ``record_digest``.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Any, Mapping

from astro.asa.locator import asa_baseline_sha, ensure_importable
from astro.domain import Entity, EntityState, EvidenceRecord, RelationshipAssertion, Universe
from astro.domain.relationships import RELATIONSHIP_TYPES
from astro_exec.core.hashing import fingerprint

ensure_importable()

from asa_kernel.api import Kernel, Receipt  # noqa: E402
from asa_kernel.identity import derive_uao_id  # noqa: E402
from asa_kernel.storage import FileStorage, MemoryStorage  # noqa: E402

NS = "astro"
CANONICAL = "asa:persp:asa.core/canonical"
SUPPORTS = "asa:type:asa.core/supports@1"
CONTRADICTS = "asa:type:asa.core/contradicts@1"
STREAM_PREFIX = "asa:log:astro/"
ACTOR = "asa:uao:astro/adapter"
POLICY = {
    "id": "asa:policy:astro/admission@1",
    "rules": {"version": 1, "definitional_types": "endorsed-after-schema-validation",
              "non_definitional_types": "require-one-valid-supports",
              "unsupported_non_definitional": "registered-unevaluated",
              "contradicted": "endorsed-with-propagation-blocked-until-adjudicated",
              "every_decision_evented": True, "meta_types_admitted_on_schema_validation": True},
}
PERSPECTIVES = [{"id": CANONICAL, "label": "canonical"}, {"id": "asa:persp:astro/operator-view", "label": "operator-view"}]
TYPE_ID = {name: f"asa:type:astro/{name.replace('_', '-')}@1" for name in RELATIONSHIP_TYPES}
TYPE_ID["evidence_of"] = "asa:type:astro/evidence-of@1"
TYPE_ID["observation_state"] = "asa:type:astro/observation-state@1"
TYPE_NAME = {v: k for k, v in TYPE_ID.items()}
TYPE_NAME[CONTRADICTS] = "contradicts"
DOMAIN_TYPES = sorted(TYPE_ID.values())


class AstroAdapterError(RuntimeError):
    """The kernel rejected an Astro translation; nothing partial survives."""


def decimal_text(value: float | int | str) -> str:
    """Restricted decimal string per ASA-SPEC-0001 §6 (no exponent, no trailing zeros, no -0)."""
    d = Decimal(str(value)) if not isinstance(value, Decimal) else value
    text = format(d, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    if text in ("-0", ""):
        text = "0"
    return text


def deterministic_clock(start: str = "2026-01-01T00:00:00Z"):
    """Monotonic timestamps derived from a fixed origin: kernel bytes never depend on wall time."""
    origin = datetime.fromisoformat(start.replace("Z", "+00:00")).astimezone(timezone.utc)
    n = [0]

    def clock() -> str:
        n[0] += 1
        return (origin + timedelta(seconds=n[0])).strftime("%Y-%m-%dT%H:%M:%SZ")

    return clock


def uao_id(astro_id: str) -> str:
    return derive_uao_id(NS, {"astro_id": astro_id})


# ---- read model ------------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class Edge:
    key: str
    type_name: str
    lifecycle: str
    stance: str
    bindings: tuple[tuple[str, tuple[str, ...]], ...]   # role -> astro ids
    literals: tuple[tuple[str, Any], ...]
    supported_by: tuple[str, ...]                       # evidence ids with a registered supports URO

    def participants(self) -> tuple[str, ...]:
        return tuple(sorted({ref for _, refs in self.bindings for ref in refs}))

    def role_of(self, entity_id: str) -> str | None:
        for role, refs in self.bindings:
            if entity_id in refs:
                return role
        return None

    def others(self, entity_id: str) -> tuple[str, ...]:
        return tuple(p for p in self.participants() if p != entity_id)


@dataclass(frozen=True, slots=True)
class EvidenceLink:
    key: str
    evidence_id: str
    subject_id: str
    evidence_kind: str
    status: str
    stance: str


@dataclass(frozen=True, slots=True)
class StateLink:
    key: str
    entity_id: str
    lifecycle: str
    literals: tuple[tuple[str, Any], ...]


@dataclass(frozen=True)
class RelationalSnapshot:
    """ASA relational state as Astro consumes it. Immutable; identified by the kernel digest."""

    asa_baseline: str
    kernel_version: str
    registry_digest: str
    stream: str
    seq: int
    head: str
    digest: str
    edges: tuple[Edge, ...]
    evidence_links: tuple[EvidenceLink, ...]
    states: tuple[StateLink, ...]

    def _index(self) -> dict[str, dict]:
        idx = self.__dict__.get("_idx")
        if idx is None:
            edges: dict[str, list[Edge]] = {}
            for e in self.edges:
                for p in e.participants():
                    edges.setdefault(p, []).append(e)
            links: dict[str, list[EvidenceLink]] = {}
            for l in self.evidence_links:
                links.setdefault(l.subject_id, []).append(l)
            states = {s.entity_id: s for s in self.states if s.lifecycle == "registered"}
            disputes: dict[str, list[Edge]] = {}
            for e in self.edges:
                if e.type_name == "contradicts" and e.lifecycle == "registered":
                    for k in e.participants():
                        disputes.setdefault(k, []).append(e)
            idx = {"edges": edges, "links": links, "states": states, "disputes": disputes}
            object.__setattr__(self, "_idx", idx)
        return idx

    def edges_of(self, entity_id: str, type_name: str | None = None) -> tuple[Edge, ...]:
        return tuple(e for e in self._index()["edges"].get(entity_id, ()) if type_name is None or e.type_name == type_name)

    def evidence_of(self, entity_id: str) -> tuple[EvidenceLink, ...]:
        return tuple(self._index()["links"].get(entity_id, ()))

    def state_of(self, entity_id: str) -> StateLink | None:
        return self._index()["states"].get(entity_id)

    def disputes_of(self, entity_id: str) -> tuple[tuple[Edge, Edge], ...]:
        """(claim edge, contradiction edge) pairs for the entity's registered claims."""
        out = []
        for claim in self.edges_of(entity_id, "measures"):
            for c in self._index()["disputes"].get(claim.key, ()):
                out.append((claim, c))
        return tuple(out)

    def to_record(self) -> dict[str, Any]:
        return {
            "asa_baseline": self.asa_baseline, "kernel_version": self.kernel_version, "registry_digest": self.registry_digest,
            "stream": self.stream, "seq": self.seq, "head": self.head, "digest": self.digest,
            "edges": len(self.edges), "evidence_links": len(self.evidence_links), "states": len(self.states),
        }


# ---- adapter -------------------------------------------------------------------------------------
class AstroAdapter:
    def __init__(self, kernel: Kernel):
        self.k = kernel
        self._astro_of: dict[str, str] = {}
        self._uro_index: dict[tuple, str] = {}
        self._uro_index_lit: dict[tuple, str] = {}
        self._rebuild_index()

    @staticmethod
    def _uro_key(type_id: str, bindings: Mapping[str, list[str]]) -> tuple:
        return (type_id, tuple(sorted((role, tuple(sorted(refs))) for role, refs in bindings.items())))

    # ---- lifecycle
    @classmethod
    def bootstrap(cls, storage, registry_facet, stream_slug: str, clock=None) -> "AstroAdapter":
        k = Kernel.bootstrap(storage, registry_facet, STREAM_PREFIX + stream_slug, POLICY, PERSPECTIVES, DOMAIN_TYPES,
                             clock=clock or deterministic_clock(), actor=ACTOR)
        return cls(k)

    @classmethod
    def open(cls, storage, registry_facet=None, clock=None) -> "AstroAdapter":
        return cls(Kernel.open(storage, registry_facet, clock=clock or deterministic_clock(), actor=ACTOR))

    @classmethod
    def in_memory(cls, registry_facet, stream_slug: str = "memory") -> "AstroAdapter":
        return cls.bootstrap(MemoryStorage(), registry_facet, stream_slug)

    # ---- helpers
    def _submit(self, op: str, **args) -> Receipt:
        r = self.k.submit(op, **args)
        if r.outcome == "rejected":
            raise AstroAdapterError(f"{op} rejected: " + "; ".join(str(d.to_dict()) for d in r.diagnostics))
        return r

    def _rebuild_index(self) -> None:
        self._astro_of = {}
        for uao in self.k.state.uaos.values():
            attrs = uao.get("attributes") or {}
            if "astro_id" in attrs:
                self._astro_of[uao["id"]] = attrs["astro_id"]
        self._uro_index, self._uro_index_lit = {}, {}
        for key, u in self.k.state.uros.items():
            if u["lifecycle"] == "registered":
                self._uro_index[self._uro_key(u["type"], u["bindings"])] = key
                self._uro_index_lit[self._uro_key(u["type"], u["bindings"]) + (self._lit_key(u["literals"]),)] = key

    def _submit_uro(self, type_id: str, bindings: Mapping[str, list[str]], literals: Mapping[str, Any]) -> Receipt:
        r = self._submit("propose", type_id=type_id, bindings=bindings, literals=dict(literals), proposer=ACTOR)
        if r.key:
            self._uro_index[self._uro_key(type_id, bindings)] = r.key
            self._uro_index_lit[self._uro_key(type_id, bindings) + (self._lit_key(literals),)] = r.key
        return r

    @staticmethod
    def _lit_key(literals: Mapping[str, Any] | None) -> tuple:
        return tuple(sorted((k, str(v)) for k, v in (literals or {}).items()))

    def _find_uro(self, type_id: str, bindings: Mapping[str, list[str]], literals: Mapping[str, Any] | None = None) -> str | None:
        """Key of a registered URO with identical type, bindings and (when given) literals, else None.

        The kernel folds duplicates into a governed `merged` decision, which is itself an event;
        Astro therefore checks before proposing so that reloading a universe appends nothing.
        Types whose identity includes literals (measures, lacks-evidence, observation-state) can hold
        several UROs under one binding, so literal-qualified lookups use the literal-keyed index.
        """
        if literals is not None:
            key = self._uro_index_lit.get(self._uro_key(type_id, bindings) + (self._lit_key(literals),))
        else:
            key = self._uro_index.get(self._uro_key(type_id, bindings))
        if key is None:
            return None
        u = self.k.uro(key)
        if u is None or u["lifecycle"] != "registered":
            return None
        if literals is not None and u["literals"] != dict(literals):
            return None
        return key

    def _register_uao(self, astro_id: str, attributes: Mapping[str, Any]) -> str:
        uid = uao_id(astro_id)
        if self.k.query(uid) is None:
            self._submit("register_entity", uao_id=uid, attributes={"astro_id": astro_id, **attributes})
            self._astro_of[uid] = astro_id
        return uid

    # ---- writes: whole universe
    def load_universe(self, universe: Universe) -> dict[str, int]:
        """Register everything in the universe that the kernel does not already hold. Idempotent."""
        counts = {"entities": 0, "evidence": 0, "relationships": 0, "supports": 0, "states": 0, "status_updates": 0}
        for entity in universe.entities:
            if self.k.query(uao_id(entity.entity_id)) is None:
                self.register_entity(entity)
                counts["entities"] += 1
        for ev in universe.evidence:
            if self.k.query(uao_id(ev.evidence_id)) is None:
                self.register_evidence(ev)
                counts["evidence"] += 1
        for ev in universe.evidence:
            counts["status_updates"] += int(self.sync_evidence_status(ev))
        for rel in universe.relationships:
            added, supports = self.register_relationship(rel)
            counts["relationships"] += int(added)
            counts["supports"] += supports
        for st in universe.states:
            counts["states"] += int(self.register_state(st))
        return counts

    def register_entity(self, entity: Entity) -> str:
        return self._register_uao(entity.entity_id, {
            "kind": entity.kind, "designation": entity.designation, "record_digest": fingerprint(entity.to_record()),
        })

    def register_evidence(self, ev: EvidenceRecord) -> str:
        uid = self._register_uao(ev.evidence_id, {
            "kind": "evidence", "evidence_kind": ev.kind, "subject": ev.subject_id, "record_digest": fingerprint(ev.to_record()),
        })
        eb = {"record": [uid], "subject": [uao_id(ev.subject_id)]}
        if self._find_uro(TYPE_ID["evidence_of"], eb) is None:
            self._submit_uro(TYPE_ID["evidence_of"], eb, {"evidence_kind": ev.kind, "status": ev.status, "quality": decimal_text(ev.quality),
                                                          "observed_at": ev.observed_at or ""})
        if ev.instrument_id:
            ib = {"record": [uid], "instrument": [uao_id(ev.instrument_id)]}
            if self._find_uro(TYPE_ID["observed_with"], ib) is None:
                self._submit_uro(TYPE_ID["observed_with"], ib, {})
        return uid

    def sync_evidence_status(self, ev: EvidenceRecord) -> bool:
        """Bring the evidence-of URO's non-identity ``status`` literal in line with the universe record."""
        key = self._find_uro(TYPE_ID["evidence_of"], {"record": [uao_id(ev.evidence_id)], "subject": [uao_id(ev.subject_id)]})
        if key is None:
            return False
        if self.k.uro(key)["literals"].get("status") == ev.status:
            return False
        self._submit("update_state", key=key, literals={"status": ev.status})
        return True

    def register_relationship(self, rel: RelationshipAssertion) -> tuple[bool, int]:
        """Propose the relationship URO and one supports URO per cited evidence record."""
        bindings = {role: [uao_id(ref) for ref in refs] for role, refs in rel.roles}
        literals = {k: decimal_text(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else v for k, v in rel.literal_map.items()}
        key = self._find_uro(TYPE_ID[rel.relationship_type], bindings, literals)
        added = False
        if key is None:
            r = self._submit_uro(TYPE_ID[rel.relationship_type], bindings, literals)
            key, added = r.key, r.outcome == "admitted"
        supports = 0
        for eid in rel.evidence_ids:
            sb = {"source": [uao_id(eid)], "target": [key]}
            if self._find_uro(SUPPORTS, sb) is None:
                s = self._submit_uro(SUPPORTS, sb, {"strength": decimal_text(rel.confidence)})
                supports += int(s.outcome == "admitted")
        return added, supports

    def propose_contradiction(self, key_a: str, key_b: str) -> Receipt | None:
        """Record that two registered claims (UROs) contradict each other. The kernel registers the meta-claim;
        Astro reads it back as a dispute. Returns None when it already exists."""
        bindings = {"claims": sorted([key_a, key_b])}
        if self._find_uro(CONTRADICTS, bindings) is not None:
            return None
        return self._submit_uro(CONTRADICTS, bindings, {})

    def retire_relationship(self, key: str, cause: str) -> None:
        self._submit("retire_uro", key=key, cause=cause)
        self._uro_index = {k: v for k, v in self._uro_index.items() if v != key}
        self._uro_index_lit = {k: v for k, v in self._uro_index_lit.items() if v != key}

    def find_relationship(self, rel: RelationshipAssertion) -> str | None:
        bindings = {role: [uao_id(ref) for ref in refs] for role, refs in rel.roles}
        literals = {k: decimal_text(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else v for k, v in rel.literal_map.items()}
        return self._find_uro(TYPE_ID[rel.relationship_type], bindings, literals)

    def register_state(self, state: EntityState) -> bool:
        subject = uao_id(state.entity_id)
        current = self._current_state_key(subject)
        literals = {"as_of": state.as_of, "observation_status": state.observation_status, "candidate_status": state.candidate_status,
                    "alert_state": state.alert_state, "last_observed_at": state.last_observed_at or "", "stale": state.stale}
        if self._find_uro(TYPE_ID["observation_state"], {"subject": [subject]}, literals) is not None:
            return False
        r = self._submit_uro(TYPE_ID["observation_state"], {"subject": [subject]}, literals)
        if r.outcome != "admitted":
            return False
        if current and current != r.key:
            self._submit("supersede", key=current, successor=r.key)
            self._uro_index.pop(self._uro_key(TYPE_ID["observation_state"], {"subject": [subject]}), None)
            self._uro_index[self._uro_key(TYPE_ID["observation_state"], {"subject": [subject]})] = r.key
        return True

    def _current_state_key(self, subject_uao: str) -> str | None:
        key = self._uro_index.get(self._uro_key(TYPE_ID["observation_state"], {"subject": [subject_uao]}))
        if key is not None and self.k.uro(key) and self.k.uro(key)["lifecycle"] == "registered":
            return key
        keys = [u["recorded_key"] for u in self.k.relationships(subject_uao)
                if u["type"] == TYPE_ID["observation_state"] and u["lifecycle"] == "registered"]
        return keys[0] if keys else None

    # ---- reads
    def snapshot(self) -> RelationalSnapshot:
        stance = self.k.project(CANONICAL)
        edges, links, states = [], [], []
        support_targets: dict[str, list[str]] = {}
        for key, u in sorted(self.k.state.uros.items()):
            if u["type"] == SUPPORTS and u["lifecycle"] == "registered":
                support_targets.setdefault(u["bindings"]["target"][0], []).append(self._astro_of.get(u["bindings"]["source"][0], u["bindings"]["source"][0]))
        for key, u in sorted(self.k.state.uros.items()):
            name = TYPE_NAME.get(u["type"])
            if name is None:
                continue
            bindings = tuple(sorted((role, tuple(self._astro_of.get(r, r) for r in refs)) for role, refs in u["bindings"].items()))
            if name == "contradicts":
                edges.append(Edge(key, name, u["lifecycle"], stance.get(key, "unevaluated"), bindings, (), ()))
                continue
            if name == "evidence_of":
                links.append(EvidenceLink(key, dict(bindings)["record"][0], dict(bindings)["subject"][0],
                                          u["literals"].get("evidence_kind", ""), u["literals"].get("status", ""), stance.get(key, "unevaluated")))
            elif name == "observation_state":
                states.append(StateLink(key, dict(bindings)["subject"][0], u["lifecycle"], tuple(sorted(u["literals"].items()))))
            else:
                edges.append(Edge(key, name, u["lifecycle"], stance.get(key, "unevaluated"), bindings,
                                  tuple(sorted(u["literals"].items())), tuple(sorted(support_targets.get(key, ())))))
        head = self.k.head()
        info = self.k.registry_info()
        return RelationalSnapshot(asa_baseline_sha(), Kernel.version()["kernel"], info["digest"], head["stream"], head["seq"], head["head"],
                                  self.k.digest(), tuple(edges), tuple(links), tuple(states))

    def provenance(self, astro_id: str) -> list[dict]:
        return self.k.provenance(uao_id(astro_id))

    def digest(self) -> str:
        return self.k.digest()

    def verify(self) -> dict:
        return self.k.verify()

    def replay_digest(self, upto_seq: int | None = None) -> str:
        return self.k.replay(upto_seq).digest()


FACET_DEFAULT = "registry/relationship_types.astro.candidate.json"
__all__ = ["AstroAdapter", "AstroAdapterError", "Edge", "EvidenceLink", "FileStorage", "MemoryStorage", "RelationalSnapshot",
           "StateLink", "decimal_text", "deterministic_clock", "uao_id", "FACET_DEFAULT", "CANONICAL"]
