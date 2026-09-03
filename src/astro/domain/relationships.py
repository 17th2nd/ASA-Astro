"""First-class relationship assertions between entities (typed, evidenced, directional)."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Mapping

from .identity import Provenance, content_id, freeze_mapping, thaw

# type name -> (ordered role names, symmetric, evidence class)
RELATIONSHIP_TYPES: dict[str, dict[str, Any]] = {
    "hosts": {"roles": ("host", "companion"), "symmetric": False, "evidence": "supported"},
    "member_of": {"roles": ("member", "group"), "symmetric": False, "evidence": "supported"},
    "catalogued_as": {"roles": ("object", "entry"), "symmetric": False, "evidence": "definitional"},
    "near": {"roles": ("pair",), "symmetric": True, "evidence": "supported", "literals": ("separation_arcsec",)},
    "calibration_reference_for": {"roles": ("reference", "target"), "symmetric": False, "evidence": "supported"},
    "comparison_star_for": {"roles": ("comparison", "target"), "symmetric": False, "evidence": "supported"},
    "hosted_transient": {"roles": ("host", "transient"), "symmetric": False, "evidence": "supported"},
    "observed_with": {"roles": ("record", "instrument"), "symmetric": False, "evidence": "definitional"},
    "located_at": {"roles": ("instrument", "site"), "symmetric": False, "evidence": "definitional"},
    "candidate_of": {"roles": ("candidate", "survey"), "symmetric": False, "evidence": "definitional"},
    # knowledge-frontier types: absence, claims and their disagreement, containment in a sky tile
    "lacks_evidence": {"roles": ("subject",), "symmetric": False, "evidence": "definitional", "literals": ("evidence_kind", "expectation_ref", "as_of")},
    "measures": {"roles": ("subject",), "symmetric": False, "evidence": "supported", "literals": ("quantity", "value", "unit", "source_key")},
    "located_in": {"roles": ("object", "region"), "symmetric": False, "evidence": "definitional"},
}


@dataclass(frozen=True, slots=True)
class RelationshipAssertion:
    assertion_id: str
    relationship_type: str
    roles: tuple[tuple[str, tuple[str, ...]], ...]   # role -> entity ids (symmetric types bind 2 under one role)
    literals: tuple[tuple[str, Any], ...]
    evidence_ids: tuple[str, ...]
    confidence: float
    status: str
    source: Provenance

    @classmethod
    def create(
        cls,
        relationship_type: str,
        roles: Mapping[str, str | list[str] | tuple[str, ...]],
        *,
        source: Provenance,
        evidence_ids: tuple[str, ...] | list[str] = (),
        literals: Mapping[str, Any] | None = None,
        confidence: float = 1.0,
        status: str = "asserted",
    ) -> "RelationshipAssertion":
        spec = RELATIONSHIP_TYPES.get(relationship_type)
        if spec is None:
            raise ValueError(f"relationship type {relationship_type!r} not in RELATIONSHIP_TYPES")
        bound: dict[str, tuple[str, ...]] = {}
        for role, refs in roles.items():
            if role not in spec["roles"]:
                raise ValueError(f"role {role!r} not declared by {relationship_type}")
            bound[role] = (refs,) if isinstance(refs, str) else tuple(refs)
        for role in spec["roles"]:
            if role not in bound:
                raise ValueError(f"role {role!r} of {relationship_type} is unbound")
        if spec["symmetric"]:
            (only,) = spec["roles"]
            if len(bound[only]) != 2 or len(set(bound[only])) != 2:
                raise ValueError(f"symmetric type {relationship_type} binds exactly two distinct entities")
            bound[only] = tuple(sorted(bound[only]))
        else:
            for role, refs in bound.items():
                if len(refs) != 1:
                    raise ValueError(f"role {role!r} of {relationship_type} binds exactly one entity")
        for name in (literals or {}):
            if name not in spec.get("literals", ()):
                raise ValueError(f"literal {name!r} not declared by {relationship_type}")
        if not 0.0 <= confidence <= 1.0:
            raise ValueError("confidence must lie in [0, 1]")
        role_items = tuple(sorted((r, tuple(v)) for r, v in bound.items()))
        body = {
            "relationship_type": relationship_type, "roles": {r: list(v) for r, v in role_items},
            "literals": dict(literals or {}), "evidence_ids": sorted(evidence_ids), "confidence": confidence,
            "source": source.to_record(),
        }
        return cls(
            assertion_id=content_id("REL", body), relationship_type=relationship_type, roles=role_items,
            literals=freeze_mapping(literals), evidence_ids=tuple(sorted(evidence_ids)), confidence=confidence,
            status=status, source=source,
        )

    def with_status(self, status: str) -> "RelationshipAssertion":
        """Same assertion, new lifecycle status; identity unchanged."""
        return replace(self, status=status)

    @property
    def role_map(self) -> dict[str, tuple[str, ...]]:
        return dict(self.roles)

    @property
    def literal_map(self) -> dict[str, Any]:
        return thaw(self.literals)

    def participants(self) -> tuple[str, ...]:
        return tuple(sorted({ref for _, refs in self.roles for ref in refs}))

    def to_record(self) -> dict[str, Any]:
        return {
            "assertion_id": self.assertion_id, "relationship_type": self.relationship_type,
            "roles": {r: list(v) for r, v in self.roles}, "literals": self.literal_map,
            "evidence_ids": list(self.evidence_ids), "confidence": self.confidence, "status": self.status,
            "source": self.source.to_record(),
        }

    @classmethod
    def from_record(cls, r: Mapping[str, Any]) -> "RelationshipAssertion":
        rel = cls.create(
            r["relationship_type"], r["roles"], source=Provenance.from_record(r["source"]),
            evidence_ids=tuple(r.get("evidence_ids") or ()), literals=r.get("literals") or {},
            confidence=float(r.get("confidence", 1.0)), status=r.get("status", "asserted"),
        )
        if r.get("assertion_id") and r["assertion_id"] != rel.assertion_id:
            raise ValueError(f"assertion_id {r['assertion_id']} does not match content identity {rel.assertion_id}")
        return rel
