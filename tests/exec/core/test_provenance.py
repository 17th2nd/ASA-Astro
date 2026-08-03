"""Content-addressed provenance primitive tests."""

from __future__ import annotations

import unittest

from astro_exec.core.errors import ConfigurationError
from astro_exec.core.provenance import ProvenanceGraph, ProvenanceNode


class ProvenanceTests(unittest.TestCase):
    """Verify immutable identifiers, parent integrity, and deterministic export."""

    def test_node_identity_and_graph_export_are_order_independent(self) -> None:
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
        graph = ProvenanceGraph()
        orphan = ProvenanceNode.create("orphan", {}, ("PV-" + "0" * 64,))
        with self.assertRaises(ConfigurationError):
            graph.add(orphan)


if __name__ == "__main__":
    unittest.main()
