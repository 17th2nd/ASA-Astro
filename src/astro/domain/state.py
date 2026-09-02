"""Temporal state of an entity as of an instant. State is not significance."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

OBSERVATION_STATUSES = ("unobserved", "scheduled", "observed")
CANDIDATE_STATUSES = ("none", "candidate", "confirmed", "rejected")
ALERT_STATES = ("none", "active", "expired")


@dataclass(frozen=True, slots=True)
class EntityState:
    entity_id: str
    as_of: str
    observation_status: str = "unobserved"
    candidate_status: str = "none"
    alert_state: str = "none"
    last_observed_at: str | None = None
    stale: bool = False

    def __post_init__(self) -> None:
        if self.observation_status not in OBSERVATION_STATUSES:
            raise ValueError(f"observation_status {self.observation_status!r} invalid")
        if self.candidate_status not in CANDIDATE_STATUSES:
            raise ValueError(f"candidate_status {self.candidate_status!r} invalid")
        if self.alert_state not in ALERT_STATES:
            raise ValueError(f"alert_state {self.alert_state!r} invalid")
        if not self.as_of:
            raise ValueError("as_of is required")

    def to_record(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id, "as_of": self.as_of, "observation_status": self.observation_status,
            "candidate_status": self.candidate_status, "alert_state": self.alert_state,
            "last_observed_at": self.last_observed_at, "stale": self.stale,
        }

    @classmethod
    def from_record(cls, r: Mapping[str, Any]) -> "EntityState":
        return cls(
            r["entity_id"], r["as_of"], r.get("observation_status", "unobserved"), r.get("candidate_status", "none"),
            r.get("alert_state", "none"), r.get("last_observed_at"), bool(r.get("stale", False)),
        )

    def updated(self, **changes: Any) -> "EntityState":
        record = self.to_record()
        record.update(changes)
        return EntityState.from_record(record)
