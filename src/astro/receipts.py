"""AstroDecisionReceipt: machine-readable provenance for one evaluation → plan decision."""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from astro import ASTRO_VERSION
from astro.asa.adapter import RelationalSnapshot
from astro.domain import Universe
from astro.domain.identity import content_id
from astro.execution import Plan
from astro.objectives import Objective, ObservingContext
from astro.significance import SignificanceEvaluation, explain
from astro_exec.core.canonical_json import canonical_text
from astro_exec.core.hashing import fingerprint, sha256_bytes

ROOT = Path(__file__).resolve().parents[2]


def astro_commit() -> str:
    try:
        out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
        dirty = subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
        return out + ("-dirty" if dirty else "")
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


@dataclass(frozen=True, slots=True)
class AstroDecisionReceipt:
    receipt_id: str
    body: dict[str, Any]
    issued_at: str            # diagnostic only; excluded from receipt identity

    def to_record(self) -> dict[str, Any]:
        return {"receipt_id": self.receipt_id, "issued_at": self.issued_at, "issued_at_classification": "diagnostic-non-authoritative", **self.body}

    def write(self, directory: str | Path) -> Path:
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / "receipt.json"
        text = canonical_text(self.to_record())
        path.write_text(text + "\n", encoding="utf-8")
        (directory / "receipt.sha256").write_text(sha256_bytes(text.encode("utf-8")) + "  receipt.json\n", encoding="utf-8")
        return path


def build_receipt(
    *, universe: Universe, snapshot: RelationalSnapshot, objective: Objective, context: ObservingContext,
    evaluation: SignificanceEvaluation, plan: Plan, commit: str | None = None, issued_at: str | None = None,
) -> AstroDecisionReceipt:
    counts = {"eligible": 0, "ineligible": 0, "indeterminate": 0}
    for r in evaluation.results:
        counts[r.status] += 1
    selected = plan.selected_ids()
    explanations = {eid: explain(evaluation, objective, eid) for eid in selected}
    for s in plan.skipped:
        if s.status == "eligible":
            explanations[s.entity_id] = explain(evaluation, objective, s.entity_id)
    body = {
        "receipt_schema": "astro-decision-receipt-v1",
        "astro_version": ASTRO_VERSION,
        "astro_commit": commit or astro_commit(),
        "asa_baseline": snapshot.asa_baseline,
        "kernel_version": snapshot.kernel_version,
        "kernel_digest": snapshot.digest,
        "kernel_head": snapshot.head,
        "kernel_seq": snapshot.seq,
        "registry_digest": snapshot.registry_digest,
        "objective_id": objective.objective_id,
        "objective_version": objective.version,
        "objective_name": objective.name,
        "weighting_policy_ref": objective.weighting_policy_ref,
        "context_id": context.context_id,
        "universe_id": universe.universe_id,
        "universe_data_class": universe.data_class,
        "candidate_set_digest": fingerprint(sorted(e.entity_id for e in universe.entities)),
        "evidence_digest": fingerprint(sorted(l.evidence_id for l in snapshot.evidence_links)),
        "relationship_digest": fingerprint(sorted(e.key for e in snapshot.edges)),
        "evaluation_id": evaluation.evaluation_id,
        "ranking": list(evaluation.ranking()),
        "eligibility_summary": counts,
        "plan_id": plan.plan_id,
        "selected_actions": [a.to_record() for a in plan.actions],
        "skipped": [s.to_record() for s in plan.skipped],
        "explanations": explanations,
        "results": [r.to_record() for r in evaluation.results],
    }
    return AstroDecisionReceipt(content_id("RCPT", body), body, issued_at or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))


def load_receipt(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))
