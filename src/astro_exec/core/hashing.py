"""SHA-256 primitives for files, canonical records, and fingerprints."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any, BinaryIO

from .canonical_json import canonical_bytes
from .errors import DigestMismatch, DigestValidationError

_CHUNK_SIZE = 1024 * 1024
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_GIT_SHA1 = re.compile(r"^[0-9a-f]{40}$")


class DigestKind(StrEnum):
    """Algorithms whose identities must never be silently interchanged."""

    SHA256_CONTENT = "sha256-content"
    GIT_BLOB_SHA1 = "git-blob-sha1"


@dataclass(frozen=True, slots=True)
class SHA256Digest:
    """Typed SHA-256 identity of uninterpreted content bytes."""

    hexdigest: str

    def __post_init__(self) -> None:
        """Reject non-canonical or malformed SHA-256 text."""

        if not isinstance(self.hexdigest, str) or not _SHA256.fullmatch(self.hexdigest):
            raise DigestValidationError("invalid SHA-256 content digest", details={"digest": self.hexdigest})

    @property
    def kind(self) -> DigestKind:
        """Return the explicit content-digest algorithm classification."""

        return DigestKind.SHA256_CONTENT

    def to_record(self) -> dict[str, str]:
        """Return a machine-readable typed digest record."""

        return {"algorithm": self.kind.value, "hexdigest": self.hexdigest}

    def __str__(self) -> str:
        """Return the canonical lowercase hexadecimal form."""

        return self.hexdigest


@dataclass(frozen=True, slots=True)
class GitBlobDigest:
    """Typed SHA-1 identity of bytes under Git's ``blob <n>\\0`` framing."""

    hexdigest: str

    def __post_init__(self) -> None:
        """Reject values that are not current-repository Git blob identities."""

        if not isinstance(self.hexdigest, str) or not _GIT_SHA1.fullmatch(self.hexdigest):
            raise DigestValidationError("invalid Git SHA-1 blob digest", details={"digest": self.hexdigest})

    @property
    def kind(self) -> DigestKind:
        """Return the explicit Git-object algorithm classification."""

        return DigestKind.GIT_BLOB_SHA1

    def to_record(self) -> dict[str, str]:
        """Return a machine-readable typed Git blob record."""

        return {"algorithm": self.kind.value, "hexdigest": self.hexdigest}

    def __str__(self) -> str:
        """Return the canonical lowercase hexadecimal form."""

        return self.hexdigest


def sha256_bytes(content: bytes) -> str:
    """Return the lowercase SHA-256 hexadecimal digest of ``content``."""

    return hashlib.sha256(content).hexdigest()


def content_digest(content: bytes) -> SHA256Digest:
    """Return the typed SHA-256 identity of raw ``content`` bytes."""

    return SHA256Digest(sha256_bytes(content))


def git_blob_digest(content: bytes) -> GitBlobDigest:
    """Return Git's typed SHA-1 blob identity for raw ``content`` bytes."""

    header = f"blob {len(content)}\0".encode("ascii")
    return GitBlobDigest(hashlib.sha1(header + content, usedforsecurity=False).hexdigest())


def sha256_stream(stream: BinaryIO) -> str:
    """Hash a binary stream from its current position using bounded memory."""

    digest = hashlib.sha256()
    while chunk := stream.read(_CHUNK_SIZE):
        digest.update(chunk)
    return digest.hexdigest()


def sha256_file(path: str | Path) -> str:
    """Return the SHA-256 digest of a file without interpreting its bytes."""

    with Path(path).open("rb") as stream:
        return sha256_stream(stream)


def content_digest_file(path: str | Path) -> SHA256Digest:
    """Return a typed SHA-256 identity for one file's exact bytes."""

    return SHA256Digest(sha256_file(path))


def verify_content_digest(content: bytes, expected: SHA256Digest) -> None:
    """Fail when ``content`` does not match the declared SHA-256 identity."""

    actual = content_digest(content)
    if actual != expected:
        raise DigestMismatch(
            "content digest mismatch",
            details={"actual": actual.to_record(), "expected": expected.to_record()},
        )


def fingerprint(value: Any) -> str:
    """Hash a value through the canonical JSON contract."""

    return sha256_bytes(canonical_bytes(value))
