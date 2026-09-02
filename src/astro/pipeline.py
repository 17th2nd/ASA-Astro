"""The canonical Astro flow: universe → ASA → significance → plan → receipt."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from astro.asa.adapter import AstroAdapter, FileStorage, RelationalSnapshot
from astro.domain import Universe
from astro.execution import Plan, plan_from_evaluation
from astro.objectives import Objective, ObservingContext
from astro.receipts import AstroDecisionReceipt, build_receipt
from astro.significance import SignificanceEvaluation, evaluate

ROOT = Path(__file__).resolve().parents[2]
FACET = ROOT / "registry" / "relationship_types.astro.candidate.json"


@dataclass(frozen=True, slots=True)
class Decision:
    snapshot: RelationalSnapshot
    evaluation: SignificanceEvaluation
    plan: Plan
    receipt: AstroDecisionReceipt


def open_or_bootstrap(universe: Universe, store: str | Path | None = None, slug: str = "astro") -> AstroAdapter:
    """In-memory kernel by default; a persistent store when ``store`` is given. The universe is loaded either way."""
    if store is None:
        adapter = AstroAdapter.in_memory(FACET, slug)
    else:
        store = Path(store)
        adapter = AstroAdapter.open(FileStorage(store)) if (store / "manifest.json").exists() or any(store.glob("*")) else AstroAdapter.bootstrap(FileStorage(store), FACET, slug)
    adapter.load_universe(universe)
    return adapter


def decide(universe: Universe, objective: Objective, context: ObservingContext, adapter: AstroAdapter, *,
           commit: str | None = None, issued_at: str | None = None) -> Decision:
    snapshot = adapter.snapshot()
    evaluation = evaluate(universe, snapshot, objective, context)
    plan = plan_from_evaluation(evaluation, objective, context, snapshot)
    receipt = build_receipt(universe=universe, snapshot=snapshot, objective=objective, context=context, evaluation=evaluation, plan=plan,
                            commit=commit, issued_at=issued_at)
    return Decision(snapshot, evaluation, plan, receipt)
