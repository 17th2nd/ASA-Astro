"""Run-start verification for authoritative frozen artefacts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .config import ExecutionConfig
from .errors import FrozenArtefactDrift
from .hashing import sha256_file


@dataclass(frozen=True, slots=True)
class VerifiedArtefact:
    """A frozen artefact whose current bytes match its expected SHA-256."""

    path: str
    sha256: str

    def to_record(self) -> dict[str, str]:
        """Return a canonical verification record."""

        return {"path": self.path, "sha256": self.sha256, "status": "verified"}


def verify_frozen_artefacts(config: ExecutionConfig, repository_root: str | Path) -> tuple[VerifiedArtefact, ...]:
    """Verify every configured artefact and abort on missing or changed bytes."""

    root = Path(repository_root).resolve()
    verified: list[VerifiedArtefact] = []
    for artefact in config.frozen_artefacts:
        candidate = (root / artefact.path).resolve()
        try:
            candidate.relative_to(root)
        except ValueError as exc:
            raise FrozenArtefactDrift("frozen artefact escapes repository root", details={"path": artefact.path}) from exc
        try:
            actual = sha256_file(candidate)
        except OSError as exc:
            raise FrozenArtefactDrift("frozen artefact is unavailable", details={"path": artefact.path}) from exc
        if actual != artefact.sha256:
            raise FrozenArtefactDrift(
                "frozen artefact digest mismatch",
                details={"actual": actual, "expected": artefact.sha256, "path": artefact.path},
            )
        verified.append(VerifiedArtefact(artefact.path, actual))
    return tuple(verified)
