"""Run-package comparison under the G1 run-id-only difference contract."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .canonical_json import canonical_bytes
from .errors import ReplayMismatch


@dataclass(frozen=True, slots=True)
class DeterminismReport:
    """Result of comparing two complete dry-run packages."""

    equivalent_except_run_id: bool
    differing_files: tuple[str, ...]

    def to_record(self) -> dict[str, Any]:
        """Return the canonical comparison record."""

        return {
            "differing_files": list(self.differing_files),
            "equivalent_except_run_id": self.equivalent_except_run_id,
        }


def _normalize(value: Any, run_id: str) -> Any:
    if isinstance(value, dict):
        return {key: _normalize(child, run_id) for key, child in value.items()}
    if isinstance(value, list):
        return [_normalize(child, run_id) for child in value]
    return "<RUN-ID>" if value == run_id else value


def _normalized_file(path: Path, run_id: str) -> bytes:
    if path.suffix == ".json":
        return canonical_bytes(_normalize(json.loads(path.read_text(encoding="utf-8")), run_id))
    if path.suffix == ".jsonl":
        records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
        return b"\n".join(canonical_bytes(_normalize(record, run_id)) for record in records) + b"\n"
    return path.read_bytes()


def compare_dry_runs(left: str | Path, right: str | Path) -> DeterminismReport:
    """Compare packages after replacing only their declared run-id values."""

    roots = (Path(left), Path(right))
    try:
        run_ids = tuple(json.loads((root / "run.json").read_text(encoding="utf-8"))["run_id"] for root in roots)
    except (OSError, json.JSONDecodeError, KeyError) as exc:
        raise ReplayMismatch("dry-run package has no readable run identifier") from exc
    file_sets = [
        {path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file() and path.name != "CHECKSUMS.sha256"}
        for root in roots
    ]
    differing = set(file_sets[0] ^ file_sets[1])
    for relative in file_sets[0] & file_sets[1]:
        if _normalized_file(roots[0] / relative, run_ids[0]) != _normalized_file(roots[1] / relative, run_ids[1]):
            differing.add(relative)
    result = tuple(sorted(differing))
    return DeterminismReport(not result, result)
