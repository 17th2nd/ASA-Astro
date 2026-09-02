"""Observing context: the when, where and with-what under which an objective is evaluated."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping

from astro.domain.identity import content_id, freeze_mapping, thaw


def parse_utc(value: str) -> datetime:
    """Parse an ISO-8601 UTC instant (``...Z`` or explicit offset); naive values are rejected."""
    text = value[:-1] + "+00:00" if value.endswith("Z") else value
    dt = datetime.fromisoformat(text)
    if dt.tzinfo is None:
        raise ValueError(f"instant {value!r} has no UTC offset")
    return dt.astimezone(timezone.utc)


@dataclass(frozen=True, slots=True)
class ObservingContext:
    context_id: str
    label: str
    as_of: str
    window_start: str
    window_end: str
    site_id: str | None
    instrument_id: str | None
    constraints: tuple[tuple[str, Any], ...]
    anchor_targets: tuple[str, ...]

    @classmethod
    def declare(
        cls,
        *,
        label: str,
        as_of: str,
        window_start: str,
        window_end: str,
        site_id: str | None = None,
        instrument_id: str | None = None,
        constraints: Mapping[str, Any] | None = None,
        anchor_targets: list[str] | tuple[str, ...] = (),
    ) -> "ObservingContext":
        t0, t1, now = parse_utc(window_start), parse_utc(window_end), parse_utc(as_of)
        if t1 <= t0:
            raise ValueError("window_end must be after window_start")
        if now > t1:
            raise ValueError("as_of lies after the observing window")
        body = {
            "label": label, "as_of": as_of, "window_start": window_start, "window_end": window_end, "site_id": site_id,
            "instrument_id": instrument_id, "constraints": dict(constraints or {}), "anchor_targets": sorted(anchor_targets),
        }
        return cls(content_id("CTX", body), label, as_of, window_start, window_end, site_id, instrument_id,
                   freeze_mapping(constraints), tuple(sorted(anchor_targets)))

    @property
    def constraint_map(self) -> dict[str, Any]:
        return thaw(self.constraints)

    @property
    def window(self) -> tuple[datetime, datetime]:
        return parse_utc(self.window_start), parse_utc(self.window_end)

    @property
    def now(self) -> datetime:
        return parse_utc(self.as_of)

    def to_record(self) -> dict[str, Any]:
        return {
            "context_id": self.context_id, "label": self.label, "as_of": self.as_of, "window_start": self.window_start,
            "window_end": self.window_end, "site_id": self.site_id, "instrument_id": self.instrument_id,
            "constraints": self.constraint_map, "anchor_targets": list(self.anchor_targets),
        }

    @classmethod
    def from_record(cls, r: Mapping[str, Any]) -> "ObservingContext":
        ctx = cls.declare(
            label=r["label"], as_of=r["as_of"], window_start=r["window_start"], window_end=r["window_end"],
            site_id=r.get("site_id"), instrument_id=r.get("instrument_id"), constraints=r.get("constraints") or {},
            anchor_targets=r.get("anchor_targets") or (),
        )
        if r.get("context_id") and r["context_id"] != ctx.context_id:
            raise ValueError(f"context_id {r['context_id']} does not match content identity {ctx.context_id}")
        return ctx

    def with_changes(self, **changes: Any) -> "ObservingContext":
        record = self.to_record()
        record.pop("context_id")
        record.update(changes)
        return ObservingContext.from_record(record)
