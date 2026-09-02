"""Simulated execution: a scheduled action becomes an observation log, state update and new evidence.

Simulated observations record only facts about the observation itself (what, when, how long,
with which instrument). They never fabricate a scientific measurement. Provenance is labelled
``simulated``. A real-instrument executor implements the same ``Executor`` protocol.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from astro.domain import EntityState, EvidenceRecord, Provenance, Universe
from astro.objectives import ObservingContext
from astro.objectives.context import parse_utc
from .schedule import ScheduledAction

SIMULATED = Provenance("astro-simulated-executor", "simulated", "src/astro/execution/execute.py")


@dataclass(frozen=True, slots=True)
class ExecutionOutcome:
    action: ScheduledAction
    evidence: tuple[EvidenceRecord, ...]
    state: EntityState
    universe_before: str
    universe_after: str


class Executor(Protocol):
    def execute(self, action: ScheduledAction, universe: Universe, context: ObservingContext) -> tuple[tuple[EvidenceRecord, ...], EntityState]: ...


class SimulatedExecutor:
    """Deterministic executor: the observation happened as scheduled, nothing more is claimed."""

    def execute(self, action: ScheduledAction, universe: Universe, context: ObservingContext) -> tuple[tuple[EvidenceRecord, ...], EntityState]:
        start, end = parse_utc(action.start_utc), parse_utc(action.end_utc)
        minutes = int((end - start).total_seconds() // 60)
        log = EvidenceRecord.create("observation_log", action.entity_id, observed_at=action.end_utc, source=SIMULATED, quality=1.0,
                                    instrument_id=context.instrument_id,
                                    values={"action": action.action, "start_utc": action.start_utc, "end_utc": action.end_utc,
                                            "duration_minutes": minutes, "simulated": True})
        records = [log]
        if action.action == "classify_transient":
            records.append(EvidenceRecord.create("spectrum", action.entity_id, observed_at=action.end_utc, source=SIMULATED, quality=0.5,
                                                 instrument_id=context.instrument_id, derived_from=[log.evidence_id],
                                                 values={"exposure_minutes": minutes, "simulated": True,
                                                         "note": "spectrum obtained in simulation; no classification is derived"}))
        elif action.action == "observe_calibrator":
            records.append(EvidenceRecord.create("photometry", action.entity_id, observed_at=action.end_utc, source=SIMULATED, quality=0.5,
                                                 instrument_id=context.instrument_id, derived_from=[log.evidence_id],
                                                 values={"frames": max(1, minutes // 2), "simulated": True,
                                                         "note": "calibration frames obtained in simulation; no magnitude is derived"}))
        if action.action in ("time_series_block", "observe_transit"):
            records.append(EvidenceRecord.create("time_series", action.entity_id, observed_at=action.end_utc, source=SIMULATED, quality=0.5,
                                                 instrument_id=context.instrument_id, derived_from=[log.evidence_id],
                                                 values={"span_days": round(minutes / 1440.0, 6), "cadence_minutes": 2.0,
                                                         "n_points": minutes // 2, "simulated": True,
                                                         "note": "coverage facts of a simulated observation; contains no measured signal"}))
        prev = universe.state_of(action.entity_id)
        state = (prev.updated(as_of=action.end_utc, observation_status="observed", last_observed_at=action.end_utc)
                 if prev else EntityState(action.entity_id, action.end_utc, observation_status="observed", last_observed_at=action.end_utc))
        return tuple(records), state


def apply_outcome(universe: Universe, action: ScheduledAction, evidence: tuple[EvidenceRecord, ...], state: EntityState) -> ExecutionOutcome:
    after = universe.with_evidence(*evidence).with_states(state)
    return ExecutionOutcome(action, evidence, state, universe.universe_id, after.universe_id)
