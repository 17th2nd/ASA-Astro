"""Offline integrity verification for deterministic Phase 2 run packages."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .errors import ReplayMismatch
from .hashing import fingerprint, sha256_file
from .ids import validate_identifier


@dataclass(frozen=True, slots=True)
class ReplayReport:
    """Immutable result of verifying one dry-run package."""

    run_id: str
    verified_files: tuple[str, ...]
    status: str = "verified"

    def to_record(self) -> dict[str, Any]:
        """Return the canonical replay report."""

        return {"run_id": self.run_id, "status": self.status, "verified_files": list(self.verified_files)}


def _checksums(path: Path) -> dict[str, str]:
    try:
        lines = (path / "CHECKSUMS.sha256").read_text(encoding="ascii").splitlines()
        entries = dict(line.split("  ", 1)[::-1] for line in lines)
    except (OSError, ValueError) as exc:
        raise ReplayMismatch("run package checksum inventory is malformed") from exc
    if not entries:
        raise ReplayMismatch("run package checksum inventory is empty")
    return entries


def verify_run_package(path: str | Path) -> ReplayReport:
    """Verify checksums, configuration fingerprint, state, and dry-run classification."""

    root = Path(path)
    expected = _checksums(root)
    actual_files = {item.relative_to(root).as_posix() for item in root.rglob("*") if item.is_file() and item.name != "CHECKSUMS.sha256"}
    if set(expected) != actual_files:
        raise ReplayMismatch("run package file set differs from checksum inventory")
    for relative, digest in expected.items():
        actual = sha256_file(root / relative)
        if actual != digest:
            raise ReplayMismatch("run package checksum mismatch", details={"actual": actual, "expected": digest, "path": relative})

    try:
        run = json.loads((root / "run.json").read_text(encoding="utf-8"))
        snapshot = json.loads((root / "config.snapshot.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ReplayMismatch("run package core records are unreadable") from exc
    run_id = validate_identifier(run.get("run_id", ""), prefix="RUN")
    if run.get("state") != "DRY_RUN_COMPLETE" or run.get("dry_run") is not True:
        raise ReplayMismatch("run package is not a completed Phase 2 dry run")
    recorded_fingerprint = snapshot.pop("config_fingerprint", None)
    if recorded_fingerprint != fingerprint(snapshot):
        raise ReplayMismatch("configuration snapshot fingerprint mismatch")
    if any(item.get("classification") == "authoritative-scientific" for item in run.get("artefacts", [])):
        raise ReplayMismatch("dry-run package contains an authoritative-scientific classification")
    return ReplayReport(run_id, tuple(sorted(actual_files)))
