"""Canonical JSON Lines logging with deterministic per-run sequencing."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .canonical_json import canonical_bytes
from .errors import ConfigurationError

_SEVERITIES = {"debug", "error", "info", "warning"}


class StructuredLogger:
    """Append deterministic structured events to a newly created JSONL file."""

    def __init__(self, path: str | Path, run_id: str) -> None:
        """Create an empty log and refuse to overwrite an existing path."""

        self.path = Path(path)
        self.run_id = run_id
        self._sequence = 0
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            self.path.touch(exist_ok=False)
        except FileExistsError as exc:
            raise ConfigurationError("structured log already exists", details={"path": str(self.path)}) from exc

    def emit(self, severity: str, event: str, *, details: dict[str, Any] | None = None) -> dict[str, Any]:
        """Append and return one canonical event record."""

        if severity not in _SEVERITIES:
            raise ConfigurationError("unknown log severity", details={"severity": severity})
        if not event:
            raise ConfigurationError("log event must be non-empty")
        record = {
            "details": dict(details or {}),
            "event": event,
            "run_id": self.run_id,
            "sequence": self._sequence,
            "severity": severity,
        }
        with self.path.open("ab") as stream:
            stream.write(canonical_bytes(record) + b"\n")
        self._sequence += 1
        return record
