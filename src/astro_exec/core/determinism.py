"""Byte comparison for authoritative Phase 2 dry-run content."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .errors import ReplayMismatch


def _checksums(path: Path) -> dict[str, str]:
    try:
        entries = dict(line.split("  ", 1)[::-1] for line in path.read_text(encoding="ascii").splitlines())
    except (OSError, ValueError) as exc:
        raise ReplayMismatch("authoritative checksum inventory is malformed") from exc
    if not entries:
        raise ReplayMismatch("authoritative checksum inventory is empty")
    return entries


@dataclass(frozen=True, slots=True)
class DeterminismReport:
    """Result of byte-comparing two authoritative-content inventories."""

    authoritative_equivalent: bool
    differing_files: tuple[str, ...]

    @property
    def equivalent_except_run_id(self) -> bool:
        """Compatibility alias; run identity is now itself authoritative."""

        return self.authoritative_equivalent

    def to_record(self) -> dict[str, Any]:
        """Return the canonical comparison record."""

        return {
            "authoritative_equivalent": self.authoritative_equivalent,
            "differing_files": list(self.differing_files),
        }


def compare_dry_runs(left: str | Path, right: str | Path) -> DeterminismReport:
    """Compare exactly the files declared by both authoritative inventories."""

    roots = (Path(left), Path(right))
    inventories = tuple(_checksums(root / "AUTHORITATIVE-CONTENT.sha256") for root in roots)
    differing = set(inventories[0]) ^ set(inventories[1])
    for relative in set(inventories[0]) & set(inventories[1]):
        if inventories[0][relative] != inventories[1][relative]:
            differing.add(relative)
            continue
        try:
            if (roots[0] / relative).read_bytes() != (roots[1] / relative).read_bytes():
                differing.add(relative)
        except OSError as exc:
            raise ReplayMismatch("authoritative package file is unavailable", details={"path": relative}) from exc
    if (roots[0] / "AUTHORITATIVE-CONTENT.sha256").read_bytes() != (roots[1] / "AUTHORITATIVE-CONTENT.sha256").read_bytes():
        differing.add("AUTHORITATIVE-CONTENT.sha256")
    result = tuple(sorted(differing))
    return DeterminismReport(not result, result)
