"""Evidence records: traceable measurements and reports about entities."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Mapping

from .identity import Provenance, content_id, forbid_intrinsic, freeze_mapping, thaw

EVIDENCE_KINDS = (
    "photometry", "astrometry", "spectrum", "time_series", "ephemeris", "alert", "catalogue_measurement",
    "observation_log", "derived_measurement", "calibration_assessment", "classification", "coverage_gap",
)
EVIDENCE_STATUSES = ("admissible", "limited", "contested", "superseded", "rejected")


@dataclass(frozen=True, slots=True)
class EvidenceRecord:
    evidence_id: str
    kind: str
    subject_id: str
    observed_at: str | None
    values: tuple[tuple[str, Any], ...]
    uncertainty: tuple[tuple[str, Any], ...]
    quality: float
    status: str
    source: Provenance
    derived_from: tuple[str, ...] = ()
    instrument_id: str | None = None

    @classmethod
    def create(
        cls,
        kind: str,
        subject_id: str,
        *,
        values: Mapping[str, Any],
        source: Provenance,
        observed_at: str | None = None,
        uncertainty: Mapping[str, Any] | None = None,
        quality: float = 1.0,
        status: str = "admissible",
        derived_from: tuple[str, ...] | list[str] = (),
        instrument_id: str | None = None,
    ) -> "EvidenceRecord":
        if kind not in EVIDENCE_KINDS:
            raise ValueError(f"evidence kind {kind!r} not in EVIDENCE_KINDS")
        if status not in EVIDENCE_STATUSES:
            raise ValueError(f"evidence status {status!r} not in EVIDENCE_STATUSES")
        if not 0.0 <= quality <= 1.0:
            raise ValueError("quality must lie in [0, 1]")
        forbid_intrinsic(values, f"EvidenceRecord({kind}) values")
        body = {
            "kind": kind, "subject_id": subject_id, "observed_at": observed_at, "values": dict(values),
            "uncertainty": dict(uncertainty or {}), "quality": quality, "source": source.to_record(),
            "derived_from": sorted(derived_from), "instrument_id": instrument_id,
        }
        return cls(
            evidence_id=content_id("EVD", body), kind=kind, subject_id=subject_id, observed_at=observed_at,
            values=freeze_mapping(values), uncertainty=freeze_mapping(uncertainty), quality=quality, status=status,
            source=source, derived_from=tuple(sorted(derived_from)), instrument_id=instrument_id,
        )

    def with_status(self, status: str) -> "EvidenceRecord":
        """Same record, new lifecycle status. Identity is unchanged: status is not content."""
        if status not in EVIDENCE_STATUSES:
            raise ValueError(f"evidence status {status!r} not in EVIDENCE_STATUSES")
        return replace(self, status=status)

    @property
    def value_map(self) -> dict[str, Any]:
        return thaw(self.values)

    @property
    def uncertainty_map(self) -> dict[str, Any]:
        return thaw(self.uncertainty)

    def to_record(self) -> dict[str, Any]:
        return {
            "evidence_id": self.evidence_id, "kind": self.kind, "subject_id": self.subject_id,
            "observed_at": self.observed_at, "values": self.value_map, "uncertainty": self.uncertainty_map,
            "quality": self.quality, "status": self.status, "source": self.source.to_record(),
            "derived_from": list(self.derived_from), "instrument_id": self.instrument_id,
        }

    @classmethod
    def from_record(cls, r: Mapping[str, Any]) -> "EvidenceRecord":
        ev = cls.create(
            r["kind"], r["subject_id"], values=r.get("values") or {}, source=Provenance.from_record(r["source"]),
            observed_at=r.get("observed_at"), uncertainty=r.get("uncertainty") or {}, quality=float(r.get("quality", 1.0)),
            status=r.get("status", "admissible"), derived_from=tuple(r.get("derived_from") or ()),
            instrument_id=r.get("instrument_id"),
        )
        if r.get("evidence_id") and r["evidence_id"] != ev.evidence_id:
            raise ValueError(f"evidence_id {r['evidence_id']} does not match content identity {ev.evidence_id}")
        return ev
