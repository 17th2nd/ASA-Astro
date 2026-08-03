"""Content-addressed provenance primitive tests."""

from __future__ import annotations

import unittest

from astro_exec.core.errors import ConfigurationError
from astro_exec.core.hashing import SHA256Digest
from astro_exec.core.ids import ConfigurationIdentity, TransformationIdentity
from astro_exec.core.provenance import (
    DependencyEnvironment,
    DerivedArtefact,
    ProvenanceGraph,
    ProvenanceNode,
    ProvenanceRelationship,
    SourceArtefact,
)


class ProvenanceTests(unittest.TestCase):
    """Verify immutable identifiers, parent integrity, and deterministic export."""

    def test_node_identity_and_graph_export_are_order_independent(self) -> None:
        """G1 provenance: nodes are content-addressed and export canonically."""
        left = ProvenanceNode.create("config", {"b": 2, "a": 1})
        right = ProvenanceNode.create("config", {"a": 1, "b": 2})
        child = ProvenanceNode.create("dry-run", {"status": "empty"}, (left.node_id,))
        graph = ProvenanceGraph()
        graph.add(left)
        graph.add(child)

        self.assertEqual(left, right)
        self.assertEqual(graph.ancestors(child.node_id), (left.node_id,))
        self.assertEqual(graph.to_record()["nodes"], sorted(graph.to_record()["nodes"], key=lambda item: item["node_id"]))

    def test_missing_parent_fails_closed(self) -> None:
        """G1 provenance: an output cannot cite an absent input record."""
        graph = ProvenanceGraph()
        orphan = ProvenanceNode.create("orphan", {}, ("PV-" + "0" * 64,))
        with self.assertRaises(ConfigurationError):
            graph.add(orphan)

    def test_source_and_derived_records_are_complete(self) -> None:
        """G1 provenance: source, version, digests, software, config, and inputs persist."""

        source = SourceArtefact.create("inputs/source.bin", "release-1", SHA256Digest("1" * 64))
        environment = DependencyEnvironment("requirements.lock", SHA256Digest("2" * 64), "CPython-3.12.3")
        transformation = TransformationIdentity.derive({"contract": "copy-v1"})
        configuration = ConfigurationIdentity.derive({"config": "v1"})
        derived = DerivedArtefact.create(
            digest=SHA256Digest("3" * 64),
            transformation=transformation,
            configuration=configuration,
            software_commit="4" * 40,
            environment=environment,
            inputs=(source.identity,),
        )
        relationship = ProvenanceRelationship(source.identity, derived.identity, transformation)

        self.assertEqual(source.to_record()["source_path"], "inputs/source.bin")
        self.assertEqual(derived.to_record()["input_artefact_ids"], [str(source.identity)])
        self.assertEqual(relationship.to_record()["output_artefact_id"], str(derived.identity))

    def test_incomplete_derived_provenance_fails_closed(self) -> None:
        """G1 provenance: missing input ancestry and abbreviated commits are rejected."""

        environment = DependencyEnvironment("requirements.lock", SHA256Digest("2" * 64), "CPython-3.12.3")
        arguments = {
            "digest": SHA256Digest("3" * 64),
            "transformation": TransformationIdentity.derive({"contract": "copy-v1"}),
            "configuration": ConfigurationIdentity.derive({"config": "v1"}),
            "environment": environment,
            "inputs": (),
        }
        with self.assertRaises(ConfigurationError):
            DerivedArtefact.create(software_commit="short", **arguments)
        with self.assertRaises(ConfigurationError):
            DerivedArtefact.create(software_commit="4" * 40, **arguments)


if __name__ == "__main__":
    unittest.main()
