"""Immutable, content-addressed provenance primitives and DAG export."""

from __future__ import annotations

from dataclasses import dataclass
import json
import re
from types import MappingProxyType
from typing import Any

from .canonical_json import canonical_text
from .errors import ConfigurationError
from .hashing import SHA256Digest
from .ids import (
    ArtefactIdentity,
    ConfigurationIdentity,
    ProvenanceRecordIdentity,
    TransformationIdentity,
)

_SOFTWARE_COMMIT = re.compile(r"^[0-9a-f]{40}$")


def _required_text(value: str, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise ConfigurationError("provenance field must be non-empty", details={"field": field})
    return value


@dataclass(frozen=True, slots=True)
class SourceArtefact:
    """Generic source artefact with path, version, and typed content digest."""

    identity: ArtefactIdentity
    source_path: str
    version: str
    digest: SHA256Digest

    @classmethod
    def create(cls, source_path: str, version: str, digest: SHA256Digest) -> "SourceArtefact":
        """Create a source identity from every required source field."""

        path = _required_text(source_path, "source_path")
        declared_version = _required_text(version, "version")
        identity = ArtefactIdentity.derive(
            {"digest": digest.to_record(), "source_path": path, "version": declared_version}
        )
        return cls(identity, path, declared_version, digest)

    def to_record(self) -> dict[str, Any]:
        """Return the complete canonical source-artefact record."""

        return {
            "artefact_id": str(self.identity),
            "digest": self.digest.to_record(),
            "source_path": self.source_path,
            "version": self.version,
        }


@dataclass(frozen=True, slots=True)
class DependencyEnvironment:
    """Dependency lock and runtime identity used by a transformation."""

    lock_path: str
    lock_digest: SHA256Digest
    runtime: str

    def __post_init__(self) -> None:
        """Require an explicit lock path and runtime identifier."""

        _required_text(self.lock_path, "lock_path")
        _required_text(self.runtime, "runtime")

    def to_record(self) -> dict[str, Any]:
        """Return the canonical dependency-environment record."""

        return {
            "lock_digest": self.lock_digest.to_record(),
            "lock_path": self.lock_path,
            "runtime": self.runtime,
        }


@dataclass(frozen=True, slots=True)
class DerivedArtefact:
    """Generic derived artefact with complete input/output provenance."""

    identity: ArtefactIdentity
    digest: SHA256Digest
    transformation: TransformationIdentity
    configuration: ConfigurationIdentity
    software_commit: str
    environment: DependencyEnvironment
    inputs: tuple[ArtefactIdentity, ...]

    @classmethod
    def create(
        cls,
        *,
        digest: SHA256Digest,
        transformation: TransformationIdentity,
        configuration: ConfigurationIdentity,
        software_commit: str,
        environment: DependencyEnvironment,
        inputs: tuple[ArtefactIdentity, ...],
    ) -> "DerivedArtefact":
        """Create a derived artefact only when its provenance is complete."""

        if not _SOFTWARE_COMMIT.fullmatch(software_commit):
            raise ConfigurationError("software commit must be a full Git SHA-1", details={"software_commit": software_commit})
        if not inputs:
            raise ConfigurationError("derived artefact requires at least one input identity")
        ordered_inputs = tuple(sorted(inputs, key=str))
        payload = {
            "configuration_id": str(configuration),
            "digest": digest.to_record(),
            "environment": environment.to_record(),
            "input_artefact_ids": [str(item) for item in ordered_inputs],
            "software_commit": software_commit,
            "transformation_id": str(transformation),
        }
        return cls(
            ArtefactIdentity.derive(payload),
            digest,
            transformation,
            configuration,
            software_commit,
            environment,
            ordered_inputs,
        )

    def to_record(self) -> dict[str, Any]:
        """Return the complete canonical derived-artefact record."""

        return {
            "artefact_id": str(self.identity),
            "configuration_id": str(self.configuration),
            "digest": self.digest.to_record(),
            "environment": self.environment.to_record(),
            "input_artefact_ids": [str(item) for item in self.inputs],
            "software_commit": self.software_commit,
            "transformation_id": str(self.transformation),
        }


@dataclass(frozen=True, slots=True)
class ProvenanceRelationship:
    """Directed relationship between an input and derived output record."""

    input_artefact: ArtefactIdentity
    output_artefact: ArtefactIdentity
    transformation: TransformationIdentity

    def to_record(self) -> dict[str, str]:
        """Return a stable machine-readable input/output relationship."""

        return {
            "input_artefact_id": str(self.input_artefact),
            "output_artefact_id": str(self.output_artefact),
            "relationship": "input-to-derived-output",
            "transformation_id": str(self.transformation),
        }


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
        return cls(str(ProvenanceRecordIdentity.derive(payload)), kind, attributes_json, ordered_parents)

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
