"""SHA-256 primitives for files, canonical records, and fingerprints."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, BinaryIO

from .canonical_json import canonical_bytes

_CHUNK_SIZE = 1024 * 1024


def sha256_bytes(content: bytes) -> str:
    """Return the lowercase SHA-256 hexadecimal digest of ``content``."""

    return hashlib.sha256(content).hexdigest()


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


def fingerprint(value: Any) -> str:
    """Hash a value through the canonical JSON contract."""

    return sha256_bytes(canonical_bytes(value))
