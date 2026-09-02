"""Load objective and context declarations from JSON, resolving designations against a universe."""

from __future__ import annotations

import json
from pathlib import Path

from astro.domain import Universe
from .context import ObservingContext
from .objective import Objective


def load_objective(path: str | Path) -> Objective:
    return Objective.from_record(json.loads(Path(path).read_text(encoding="utf-8")))


def load_context(path: str | Path, universe: Universe) -> ObservingContext:
    r = json.loads(Path(path).read_text(encoding="utf-8"))
    site = r.get("site_id") or (universe.find(r["site_designation"]).entity_id if r.get("site_designation") else None)
    inst = r.get("instrument_id") or (universe.find(r["instrument_designation"]).entity_id if r.get("instrument_designation") else None)
    anchors = list(r.get("anchor_targets") or []) + [universe.find(d).entity_id for d in r.get("anchor_target_designations", [])]
    return ObservingContext.declare(label=r["label"], as_of=r["as_of"], window_start=r["window_start"], window_end=r["window_end"],
                                    site_id=site, instrument_id=inst, constraints=r.get("constraints") or {}, anchor_targets=anchors)
