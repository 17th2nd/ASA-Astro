"""Contracts for canonical representation, hashing, identifiers, and errors."""

from __future__ import annotations

import io
import math
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from astro_exec.core.canonical_json import canonical_bytes, canonical_text, canonical_timestamp
from astro_exec.core.errors import (
    CanonicalJSONError,
    ConfigurationError,
    DigestMismatch,
    DigestValidationError,
    UnresolvedRequirement,
)
from astro_exec.core.hashing import (
    GitBlobDigest,
    SHA256Digest,
    content_digest,
    fingerprint,
    git_blob_digest,
    sha256_bytes,
    sha256_file,
    sha256_stream,
    verify_content_digest,
)
from astro_exec.core.ids import (
    ArtefactIdentity,
    ConfigurationIdentity,
    InvocationIdentity,
    ProvenanceRecordIdentity,
    RunIdentity,
    stable_identifier,
    validate_identifier,
)


class CanonicalJSONTests(unittest.TestCase):
    """Verify the Phase 2 canonical JSON contract."""

    def test_mapping_order_does_not_change_bytes(self) -> None:
        """G1 canonical JSON: key ordering and UTF-8 have a known answer."""
        left = {"z": [1, 2.5, True], "a": "α"}
        right = {"a": "α", "z": [1, 2.5, True]}

        self.assertEqual(canonical_bytes(left), canonical_bytes(right))
        self.assertEqual(canonical_text(left), '{"a":"α","z":[1,2.5,true]}')

    def test_non_finite_and_non_json_values_fail_closed(self) -> None:
        """G1 canonical JSON: unsupported and non-finite values are rejected."""
        for value in (math.inf, -math.inf, math.nan, {"bad": object()}, {1: "bad"}):
            with self.subTest(value=value), self.assertRaises(CanonicalJSONError):
                canonical_bytes(value)

    def test_timestamp_and_scalar_known_answer_vector(self) -> None:
        """G1 canonical JSON: timestamps, null, arrays, and numbers are fixed."""

        stamp = datetime(2026, 8, 3, 12, 34, 56, 7, tzinfo=timezone(timedelta(hours=10)))
        value = {"stamp": stamp, "values": [None, -0.0, 2.5, 3, False]}
        self.assertEqual(canonical_timestamp(stamp), "2026-08-03T02:34:56.000007Z")
        self.assertEqual(
            canonical_bytes(value),
            b'{"stamp":"2026-08-03T02:34:56.000007Z","values":[null,-0.0,2.5,3,false]}',
        )
        with self.assertRaises(CanonicalJSONError):
            canonical_bytes(datetime(2026, 8, 3))


class HashingAndIdentifierTests(unittest.TestCase):
    """Verify content hashing and time-independent identifier derivation."""

    def test_hash_primitives_agree(self) -> None:
        """G1 hashing: SHA-256 file, stream, and byte vectors agree."""
        content = b"deterministic\n"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "content.bin"
            path.write_bytes(content)
            self.assertEqual(sha256_bytes(content), sha256_stream(io.BytesIO(content)))
            self.assertEqual(sha256_bytes(content), sha256_file(path))

    def test_typed_digest_vectors_and_mismatch(self) -> None:
        """G1 hashing: content and Git identities remain distinct and verified."""

        content = b"test content\n"
        sha = content_digest(content)
        git = git_blob_digest(content)
        self.assertEqual(str(sha), "a1fff0ffefb9eace7230c24e50731f0a91c62f9cefdfe77121c2f607125dffae")
        self.assertEqual(str(git), "d670460b4b4aece5915caf5c68d12f560a9fe3e4")
        self.assertNotEqual(sha.to_record()["algorithm"], git.to_record()["algorithm"])
        verify_content_digest(content, sha)
        with self.assertRaises(DigestMismatch):
            verify_content_digest(b"changed", sha)
        with self.assertRaises(DigestValidationError):
            SHA256Digest(str(git))
        with self.assertRaises(DigestValidationError):
            GitBlobDigest(str(sha))

    def test_identifiers_depend_only_on_canonical_content(self) -> None:
        """G1 identifiers: generic identities depend only on canonical content."""
        first = stable_identifier("RUN", {"b": 2, "a": 1})
        second = stable_identifier("RUN", {"a": 1, "b": 2})

        self.assertEqual(first, second)
        self.assertEqual(validate_identifier(first, prefix="RUN"), first)
        self.assertEqual(first.removeprefix("RUN-"), fingerprint({"a": 1, "b": 2}))

    def test_domain_identity_types_cannot_be_substituted(self) -> None:
        """G1 identifiers: each authoritative domain has a separate type."""

        payload = {"declared": "input"}
        identities = (
            ArtefactIdentity.derive(payload),
            ConfigurationIdentity.derive(payload),
            RunIdentity.derive(payload),
            InvocationIdentity.derive(payload),
            ProvenanceRecordIdentity.derive(payload),
        )
        self.assertEqual(len({str(item) for item in identities}), len(identities))
        self.assertEqual(InvocationIdentity.derive(payload).to_record()["classification"], "diagnostic-non-authoritative")
        with self.assertRaises(ConfigurationError):
            RunIdentity(str(ArtefactIdentity.derive(payload)))


class StructuredErrorTests(unittest.TestCase):
    """Verify stable exception records without resolving open requirements."""

    def test_unresolved_requirement_names_the_blocker(self) -> None:
        """G1 structured errors: stable code and details preserve UR status."""
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
