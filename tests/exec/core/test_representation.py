"""Contracts for canonical representation, hashing, identifiers, and errors."""

from __future__ import annotations

import io
import math
import tempfile
import unittest
from pathlib import Path

from astro_exec.core.canonical_json import canonical_bytes, canonical_text
from astro_exec.core.errors import CanonicalJSONError, UnresolvedRequirement
from astro_exec.core.hashing import fingerprint, sha256_bytes, sha256_file, sha256_stream
from astro_exec.core.ids import stable_identifier, validate_identifier


class CanonicalJSONTests(unittest.TestCase):
    """Verify the Phase 2 canonical JSON contract."""

    def test_mapping_order_does_not_change_bytes(self) -> None:
        left = {"z": [1, 2.5, True], "a": "α"}
        right = {"a": "α", "z": [1, 2.5, True]}

        self.assertEqual(canonical_bytes(left), canonical_bytes(right))
        self.assertEqual(canonical_text(left), '{"a":"α","z":[1,2.5,true]}')

    def test_non_finite_and_non_json_values_fail_closed(self) -> None:
        for value in (math.inf, -math.inf, math.nan, {"bad": object()}, {1: "bad"}):
            with self.subTest(value=value), self.assertRaises(CanonicalJSONError):
                canonical_bytes(value)


class HashingAndIdentifierTests(unittest.TestCase):
    """Verify content hashing and time-independent identifier derivation."""

    def test_hash_primitives_agree(self) -> None:
        content = b"deterministic\n"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "content.bin"
            path.write_bytes(content)
            self.assertEqual(sha256_bytes(content), sha256_stream(io.BytesIO(content)))
            self.assertEqual(sha256_bytes(content), sha256_file(path))

    def test_identifiers_depend_only_on_canonical_content(self) -> None:
        first = stable_identifier("RUN", {"b": 2, "a": 1})
        second = stable_identifier("RUN", {"a": 1, "b": 2})

        self.assertEqual(first, second)
        self.assertEqual(validate_identifier(first, prefix="RUN"), first)
        self.assertEqual(first.removeprefix("RUN-"), fingerprint({"a": 1, "b": 2}))


class StructuredErrorTests(unittest.TestCase):
    """Verify stable exception records without resolving open requirements."""

    def test_unresolved_requirement_names_the_blocker(self) -> None:
        error = UnresolvedRequirement("UR-001")

        self.assertEqual(
            error.to_record(),
            {
                "code": "UNRESOLVED_REQUIREMENT",
                "details": {"requirement_id": "UR-001"},
                "message": "execution blocked by unresolved requirement UR-001",
            },
        )


if __name__ == "__main__":
    unittest.main()
