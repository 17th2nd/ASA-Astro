"""Immutable, content-addressed provenance primitives and DAG export."""

from __future__ import annotations

from dataclasses import dataclass
import json
from types import MappingProxyType
from typing import Any

from .canonical_json import canonical_text
from .errors import ConfigurationError
from .ids import stable_identifier


@dataclass(frozen=True, slots=True)
class ProvenanceNode:
    """An immutable content-addressed provenance assertion."""

    node_id: str
    kind: str
    _attributes_json: str
    parents: tuple[str, ...]

    @classmethod
    def create(cls, kind: str, attributes: dict[str, Any], parents: tuple[str, ...] = ()) -> "ProvenanceNode":
        """Create a node whose identifier hashes its canonical content."""

        if not kind or not isinstance(kind, str):
            raise ConfigurationError("provenance kind must be a non-empty string")
        attributes_json = canonical_text(attributes)
        ordered_parents = tuple(sorted(parents))
        payload = {"attributes": json.loads(attributes_json), "kind": kind, "parents": list(ordered_parents)}
        return cls(stable_identifier("PV", payload), kind, attributes_json, ordered_parents)

    @property
    def attributes(self) -> MappingProxyType[str, Any]:
        """Return a fresh read-only view of the canonical attributes."""

        return MappingProxyType(json.loads(self._attributes_json))

    def to_record(self) -> dict[str, Any]:
        """Return the canonical self-verifying node record."""

        return {
            "attributes": dict(self.attributes),
            "kind": self.kind,
            "node_id": self.node_id,
            "parents": list(self.parents),
        }


class ProvenanceGraph:
    """A deterministic DAG that only admits nodes with present parents."""

    def __init__(self) -> None:
        """Create an empty graph."""

        self._nodes: dict[str, ProvenanceNode] = {}

    def add(self, node: ProvenanceNode) -> None:
        """Add a node after verifying its identity and parent references."""

        recreated = ProvenanceNode.create(node.kind, dict(node.attributes), node.parents)
        if recreated.node_id != node.node_id:
            raise ConfigurationError("provenance node identifier does not match its content")
        missing = sorted(set(node.parents) - self._nodes.keys())
        if missing:
            raise ConfigurationError("provenance parents are missing", details={"parents": missing})
        self._nodes[node.node_id] = node

    def ancestors(self, node_id: str) -> tuple[str, ...]:
        """Return all ancestors in stable identifier order."""

        if node_id not in self._nodes:
            raise ConfigurationError("unknown provenance node", details={"node_id": node_id})
        found: set[str] = set()
        pending = list(self._nodes[node_id].parents)
        while pending:
            parent = pending.pop()
            if parent not in found:
                found.add(parent)
                pending.extend(self._nodes[parent].parents)
        return tuple(sorted(found))

    def to_record(self) -> dict[str, Any]:
        """Export the complete graph in stable node-id order."""

        return {
            "nodes": [self._nodes[node_id].to_record() for node_id in sorted(self._nodes)],
            "schema_version": "astro-exec-provenance-v1",
        }
