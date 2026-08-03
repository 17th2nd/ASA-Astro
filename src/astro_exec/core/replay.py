"""Offline integrity and identity verification for Phase 2 run packages."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from .errors import ReplayMismatch
from .hashing import fingerprint, sha256_file
from .ids import RunIdentity, validate_identifier
from .run_package import PACKAGE_SCHEMA_VERSION

_CHECKSUM_LINE = re.compile(r"^(?P<digest>[0-9a-f]{64})  (?P<path>[^\r\n]+)$")


@dataclass(frozen=True, slots=True)
class ReplayReport:
    """Immutable result of verifying one dry-run package."""

    run_id: str
    authoritative_digest: str
    verified_files: tuple[str, ...]
    status: str = "verified"

    def to_record(self) -> dict[str, Any]:
        """Return the canonical replay report."""

        return {
            "authoritative_digest": self.authoritative_digest,
            "run_id": self.run_id,
            "status": self.status,
            "verified_files": list(self.verified_files),
        }


def _checksums(path: Path, filename: str) -> dict[str, str]:
    try:
        lines = (path / filename).read_text(encoding="ascii").splitlines()
    except OSError as exc:
        raise ReplayMismatch("run package checksum inventory is malformed", details={"path": filename}) from exc
    entries: dict[str, str] = {}
    for line in lines:
        match = _CHECKSUM_LINE.fullmatch(line)
        if match is None:
            raise ReplayMismatch("run package checksum line is malformed", details={"inventory": filename})
        relative = match.group("path")
        parsed = PurePosixPath(relative)
        if parsed.is_absolute() or ".." in parsed.parts or "\\" in relative or relative in entries:
            raise ReplayMismatch("run package checksum path is unsafe or duplicated", details={"path": relative})
        entries[relative] = match.group("digest")
    if not entries:
        raise ReplayMismatch("run package checksum inventory is empty", details={"path": filename})
    return entries


def _verify_inventory(root: Path, expected: dict[str, str]) -> None:
    resolved_root = root.resolve()
    for relative, digest in expected.items():
        unresolved = root / relative
        current = root
        for part in PurePosixPath(relative).parts:
            current = current / part
            if current.is_symlink():
                raise ReplayMismatch("run package inventory path is a symlink", details={"path": relative})
        candidate = unresolved.resolve()
        try:
            candidate.relative_to(resolved_root)
            actual = sha256_file(candidate)
        except (OSError, ValueError) as exc:
            raise ReplayMismatch("run package inventory path is missing or unsafe", details={"path": relative}) from exc
        if actual != digest:
            raise ReplayMismatch(
                "run package checksum mismatch",
                details={"actual": actual, "expected": digest, "path": relative},
            )


def verify_run_package(path: str | Path) -> ReplayReport:
    """Verify file sets, authoritative bytes, identities, config, and lifecycle."""

    root = Path(path)
    complete = _checksums(root, "CHECKSUMS.sha256")
    actual_files = {
        item.relative_to(root).as_posix()
        for item in root.rglob("*")
        if item.is_file() and item.name != "CHECKSUMS.sha256"
    }
    if set(complete) != actual_files:
        raise ReplayMismatch(
            "run package file set differs from checksum inventory",
            details={"actual": sorted(actual_files), "expected": sorted(complete)},
        )
    _verify_inventory(root, complete)

    authoritative = _checksums(root, "AUTHORITATIVE-CONTENT.sha256")
    _verify_inventory(root, authoritative)
    try:
        run = json.loads((root / "run.json").read_text(encoding="utf-8"))
        snapshot = json.loads((root / "config.snapshot.json").read_text(encoding="utf-8"))
        lifecycle = json.loads((root / "lifecycle.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ReplayMismatch("run package core records are unreadable") from exc

    run_id = validate_identifier(run.get("run_id", ""), prefix="RUN")
    if run.get("schema_version") != PACKAGE_SCHEMA_VERSION or run.get("state") != "sealed" or run.get("dry_run") is not True:
        raise ReplayMismatch("run package is not a sealed Phase 2 dry run")
    if run.get("scientific_computation") is not False or run.get("evidence_level") != "EH-0":
        raise ReplayMismatch("dry-run evidence or scientific-execution classification is invalid")
    identity_inputs = run.get("run_identity_inputs")
    if not isinstance(identity_inputs, dict) or str(RunIdentity.derive(identity_inputs)) != run_id:
        raise ReplayMismatch("authoritative run identity does not match its declared inputs")

    recorded_fingerprint = snapshot.pop("config_fingerprint", None)
    if recorded_fingerprint != fingerprint(snapshot) or recorded_fingerprint != identity_inputs.get("config_fingerprint"):
        raise ReplayMismatch("configuration snapshot fingerprint mismatch")
    if lifecycle.get("run_id") != run_id or lifecycle.get("state") != "sealed":
        raise ReplayMismatch("lifecycle record does not seal the authoritative run")
    expected_states = [
        ("proposed", "validating"),
        ("validating", "ready"),
        ("ready", "executing"),
        ("executing", "completed"),
        ("completed", "sealed"),
    ]
    transitions = lifecycle.get("transitions", [])
    if [(item.get("source"), item.get("target")) for item in transitions] != expected_states:
        raise ReplayMismatch("lifecycle transition sequence is invalid")

    artefacts = run.get("artefacts", [])
    declared_authoritative = {
        item.get("path")
        for item in artefacts
        if item.get("authoritative_content") is True
    }
    if declared_authoritative != set(authoritative):
        raise ReplayMismatch("authoritative checksum set differs from run classification")
    if any(item.get("classification") == "authoritative-scientific" for item in artefacts):
        raise ReplayMismatch("dry-run package contains an authoritative-scientific classification")
    if run.get("diagnostic_logs", {}).get("classification") != "diagnostic-not-scientific-evidence":
        raise ReplayMismatch("diagnostic log classification is missing")
    if any("invocation" in relative.lower() for relative in actual_files):
        raise ReplayMismatch("operational invocation metadata leaked into the authoritative package")

    authoritative_digest = sha256_file(root / "AUTHORITATIVE-CONTENT.sha256")
    return ReplayReport(run_id, authoritative_digest, tuple(sorted(actual_files)))
