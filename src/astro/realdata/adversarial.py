"""Bounded adversarial and ablation checks AC1–AC11 of ASTRO-REAL-DATA-EXP-0001, exactly as pre-registered in the manifest.

Each check builds its own universe and in-memory kernel from the frozen extract, applies one declared intervention,
evaluates under the declared objective and Context (or the declared variant), and records what happened against the
pre-registered pass criterion. Nothing here changes the engine.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from astro.domain import Entity, EvidenceRecord, Provenance, RelationshipAssertion, Universe
from astro.objectives import Objective, ObservingContext
from astro.objectives.loaders import load_objective
from astro.pipeline import decide
from astro.significance import evaluate
from astro_exec.core.canonical_json import canonical_text
from . import EXP_ID
from .baselines import degree, pagerank
from .dataset import RESULTS_DIR, load_selection
from .experiment import DECISIVE_BASELINES, preconditions
from .manifest import OBJECTIVE_PATH, PAGERANK_DAMPING, PAGERANK_ITERATIONS, TOPOLOGY_LIMIT, declare_context, load_manifest
from .metrics import spearman
from .universe import build_base_universe, load_kernel, with_frontier

ADVERSARIAL = Provenance(f"{EXP_ID} adversarial", "simulated", "src/astro/realdata/adversarial.py")


def _variant(objective: Objective, **changes: Any) -> Objective:
    rec = objective.to_record()
    rec.pop("objective_id"); rec.pop("weighting_policy_ref"); rec.pop("output_semantics")
    rec.update(changes)
    return Objective.from_record(rec)


def _drift(result) -> dict[str, Any] | None:
    return next((c for c in result.contributions if c["feature"] == "ephemeris_drift"), None)


def _feature(result, name: str) -> dict[str, Any] | None:
    return next((c for c in result.contributions if c["feature"] == name), None)


def _weight_sum(result) -> float:
    return sum(c["weight"] for c in result.contributions if c.get("contribution") is not None)


def _rho(evaluation, ids: list[str], grade_of: dict[str, float]) -> float | None:
    vals = [(evaluation.result_for(h).score if evaluation.result_for(h).status == "eligible" else None) for h in ids]
    r = spearman(vals, [grade_of[h] for h in ids])
    return None if r is None else round(r, 4)


def _statuses(evaluation, ids: list[str]) -> dict[str, int]:
    return {s: sum(1 for h in ids if evaluation.result_for(h).status == s) for s in ("eligible", "ineligible", "indeterminate")}


def _replace_relationships(u: Universe, rels: list[RelationshipAssertion]) -> Universe:
    return Universe.create(u.label, u.data_class, u.entities, u.evidence, rels, u.states)


def run_adversarial(out_dir: Path | None = None) -> dict[str, Any]:
    out = Path(out_dir) if out_dir else RESULTS_DIR
    pre = preconditions()
    if not pre["ok"]:
        return {"verdict": "INVALID", **pre}
    results = json.loads((out / "results.json").read_text(encoding="utf-8"))
    table = json.loads((out / "candidates_scored.json").read_text(encoding="utf-8"))
    manifest = load_manifest()
    objective = load_objective(OBJECTIVE_PATH)
    context = declare_context()
    sel = load_selection()

    base_u0 = build_base_universe()
    base_u, base_f = with_frontier(base_u0, context.as_of)
    base_a = load_kernel(base_u, base_f)   # same stream slug as the primary run: the evaluation id includes the kernel digest
    base_d = decide(base_u, objective, context, base_a, issued_at=context.as_of)
    reproduced = base_d.evaluation.evaluation_id == results["evaluation_id"]

    primary = [t["host_entity_id"] for t in table if t["in_primary"]]
    grade_of = {t["host_entity_id"]: float(t["grade"]) for t in table}
    heldout = [t["host_entity_id"] for t in table if t["missing_uncertainty_heldout"]]
    eligible_primary = [(t["astro_rank_overall"], t["host_entity_id"]) for t in table if t["in_primary"] and t["astro_status"] == "eligible"]
    rank1 = min(eligible_primary)[1]
    rank1_entity = base_u.entity(rank1)
    base_r1 = base_d.evaluation.result_for(rank1)
    eph = next(e for e in base_u.evidence_for(rank1, "ephemeris") if e.status == "admissible")
    W = _weight_sum(base_r1)
    checks: list[dict[str, Any]] = []

    # AC1 contradictory evidence ---------------------------------------------------------------------------------
    v = eph.value_map
    contra = EvidenceRecord.create("ephemeris", rank1, values={**v, "period_days": round(v["period_days"] * 1.02, 8)}, uncertainty=eph.uncertainty_map, source=ADVERSARIAL, quality=eph.quality)
    u1, f1 = with_frontier(base_u0.with_evidence(contra), context.as_of)
    d1 = decide(u1, objective, context, load_kernel(u1, f1, "ac1"), issued_at=context.as_of)
    r1 = d1.evaluation.result_for(rank1)
    disputes = d1.snapshot.disputes_of(rank1)
    period_disputes = [(dict(c.literals).get("quantity"), x.key) for c, x in disputes if str(dict(c.literals).get("quantity", "")).startswith("period_days")]
    dr = _drift(r1)
    delta = (r1.score or 0.0) - (base_r1.score or 0.0)
    checks.append({"id": "AC1", "name": "contradictory evidence", "subject": rank1_entity.designation, "injected_evidence_id": contra.evidence_id,
                   "contradiction_registered": bool(period_disputes), "period_disputes": period_disputes[:4], "all_disputes": len(disputes),
                   "drift_trace_evidence_id": dr["trace"].get("evidence_id") if dr else None, "drift_used_injected_record": bool(dr and dr["trace"].get("evidence_id") == contra.evidence_id),
                   "score_before": base_r1.score, "score_after": r1.score, "delta": round(delta, 6), "bound": round(4.0 / W, 6),
                   "ranking_consulted_the_contradiction": False,
                   "pass": bool(period_disputes) and bool(dr and dr["trace"].get("evidence_id")) and abs(delta) <= 4.0 / W + 1e-12,
                   "note": "The declared objective has no dispute feature; the contradiction is registered in ASA and traceable, but ephemeris_drift takes the largest ratio over admissible records, so a contradicting record can only raise the score. Objective F would consult it."})

    # AC2 high-confidence incorrect evidence --------------------------------------------------------------------
    sure = EvidenceRecord.create("ephemeris", rank1, values=v, uncertainty={"period_days": 1e-9, "epoch_days": 1e-9}, source=ADVERSARIAL, quality=eph.quality)
    u2, f2 = with_frontier(base_u0.supersede_evidence(eph.evidence_id, sure), context.as_of)
    d2 = decide(u2, objective, context, load_kernel(u2, f2, "ac2"), issued_at=context.as_of)
    r2 = d2.evaluation.result_for(rank1)
    dr2 = _drift(r2)
    ranks2 = sorted(((d2.evaluation.result_for(h).score or -1.0), h) for h in primary if d2.evaluation.result_for(h).status == "eligible")
    pos2 = [h for _, h in sorted(ranks2, reverse=True)].index(rank1) + 1 if rank1 in {h for _, h in ranks2} else None
    checks.append({"id": "AC2", "name": "high-confidence incorrect evidence", "subject": rank1_entity.designation, "injected_evidence_id": sure.evidence_id, "superseded_evidence_id": eph.evidence_id,
                   "drift_before": dr["value"] if (dr := _drift(base_r1)) else None, "drift_after": dr2["value"] if dr2 else None, "drift_trace": dr2["trace"] if dr2 else None,
                   "score_before": base_r1.score, "score_after": r2.score, "position_in_primary_after": pos2, "primary_size": len(primary),
                   "old_record_excluded_as_superseded": any(x.get("reason") == "status superseded" for e in r2.eligibility for x in e.get("excluded", []) if isinstance(x, dict)),
                   "pass": bool(dr2 and dr2["trace"].get("evidence_id") == sure.evidence_id),
                   "note": "Known limitation, recorded: the engine trusts a stated uncertainty; nothing cross-checks it against a second source unless a contradicting claim exists."})

    # AC3 missing evidence (real held-out rows) -----------------------------------------------------------------
    ac3 = []
    for h in heldout:
        r = base_d.evaluation.result_for(h)
        recs = [e for e in base_u.evidence_for(h, "ephemeris") if e.status == "admissible"]
        unc = sorted({k for e in recs for k in e.uncertainty_map})
        d3 = _drift(r)
        ac3.append({"host": base_u.entity(h).designation, "uncertainty_keys_present": unc, "status": r.status, "score": r.score,
                    "drift_status": d3["status"] if d3 else None, "drift_trace": d3["trace"] if d3 else None})
    checks.append({"id": "AC3", "name": "missing evidence", "subject": f"{len(heldout)} held-out hosts lacking a period or epoch uncertainty", "cases": ac3,
                   "indeterminate": sum(1 for c in ac3 if c["status"] == "indeterminate"), "scored": sum(1 for c in ac3 if c["status"] == "eligible"),
                   "pass": all(c["status"] == "indeterminate" for c in ac3),
                   "note": "ephemeris_drift is available when either uncertainty is present and treats the absent one as zero (u.get(..., 0.0)); a host lacking only one of the two is therefore scored, with no missingness statement in the trace."})

    # AC4 uncertain relationship --------------------------------------------------------------------------------
    hosts_rel = next(r for r in base_u0.relationships_of(rank1, "hosts") if rank1 in r.role_map.get("host", ()))
    stripped = RelationshipAssertion.create("hosts", {k: list(vv) for k, vv in hosts_rel.roles}, source=hosts_rel.source, evidence_ids=(), confidence=hosts_rel.confidence, status=hosts_rel.status)
    u4 = _replace_relationships(base_u0, [r for r in base_u0.relationships if r.assertion_id != hosts_rel.assertion_id] + [stripped])
    u4, f4 = with_frontier(u4, context.as_of)
    d4 = decide(u4, objective, context, load_kernel(u4, f4, "ac4"), issued_at=context.as_of)
    r4 = d4.evaluation.result_for(rank1)
    excluded = [x for e in r4.eligibility for x in e.get("excluded", []) if isinstance(x, dict) and x.get("type") == "hosts"]
    rel_before, rel_after = _feature(base_r1, "relationship_support"), _feature(r4, "relationship_support")
    expected_delta = -(rel_before["value"] * rel_before["weight"]) / W if rel_before and rel_before["value"] is not None else None
    delta4 = (r4.score or 0.0) - (base_r1.score or 0.0)
    d4_include = evaluate(u4, d4.snapshot, _variant(objective, unevaluated_relationships="include"), context).result_for(rank1)
    checks.append({"id": "AC4", "name": "uncertain relationship", "subject": rank1_entity.designation, "hosts_edge_excluded": excluded[:2], "relationship_support_before": rel_before["value"] if rel_before else None,
                   "relationship_support_after": rel_after["value"] if rel_after else None, "score_before": base_r1.score, "score_after": r4.score, "delta": round(delta4, 9),
                   "expected_delta": None if expected_delta is None else round(expected_delta, 9), "score_with_include_policy": d4_include.score,
                   "pass": bool(excluded) and rel_after is not None and rel_after["value"] == 0.0 and expected_delta is not None and abs(delta4 - expected_delta) < 1e-9})

    # AC5 isolated candidate ------------------------------------------------------------------------------------
    iso = Entity.create("star", f"SIM-ISOLATED {rank1_entity.designation}", coordinates=None, source=ADVERSARIAL, attributes=rank1_entity.attribute_map)
    iso_eph = EvidenceRecord.create("ephemeris", iso.entity_id, values=v, uncertainty=eph.uncertainty_map, source=ADVERSARIAL, quality=eph.quality)
    u5 = Universe.create(base_u0.label, base_u0.data_class, list(base_u0.entities) + [iso], list(base_u0.evidence) + [iso_eph], base_u0.relationships, base_u0.states)
    u5, f5 = with_frontier(u5, context.as_of)
    d5 = decide(u5, objective, context, load_kernel(u5, f5, "ac5"), issued_at=context.as_of)
    r5 = d5.evaluation.result_for(iso.entity_id)
    checks.append({"id": "AC5", "name": "isolated candidate", "subject": iso.designation, "status": r5.status, "score": r5.score, "relationship_keys": list(r5.relationship_keys),
                   "relationship_support": (_feature(r5, "relationship_support") or {}).get("value"), "drift": (_drift(r5) or {}).get("value"),
                   "pass": r5.status == "eligible" and not r5.relationship_keys})

    # AC6 highly connected but irrelevant candidate -------------------------------------------------------------
    hub = Entity.create("star", "SIM-HUB", coordinates=None, source=ADVERSARIAL, attributes={"magnitude_v": 10.0})
    hub_ev, hub_rel = [], []
    for i, other in enumerate(primary[:30]):
        sep = EvidenceRecord.create("derived_measurement", hub.entity_id, source=ADVERSARIAL, values={"angular_separation_arcsec": 100.0 + i, "other": other, "method": "simulated"}, quality=0.95)
        hub_ev.append(sep)
        hub_rel.append(RelationshipAssertion.create("near", {"pair": [hub.entity_id, other]}, literals={"separation_arcsec": 100.0 + i}, evidence_ids=[sep.evidence_id], confidence=0.99, source=ADVERSARIAL))
    for i in range(30):
        m = EvidenceRecord.create("catalogue_measurement", hub.entity_id, source=ADVERSARIAL, values={f"sim_quantity_{i:02d}": 1.0, "note": "simulated"}, quality=0.8)
        hub_ev.append(m)
        hub_rel.append(RelationshipAssertion.create("measures", {"subject": hub.entity_id}, literals={"quantity": f"sim_quantity_{i:02d}", "value": 1.0, "unit": "1", "source_key": f"sim{i}"}, evidence_ids=[m.evidence_id], confidence=0.8, source=ADVERSARIAL))
    u6 = Universe.create(base_u0.label, base_u0.data_class, list(base_u0.entities) + [hub], list(base_u0.evidence) + hub_ev, list(base_u0.relationships) + hub_rel, base_u0.states)
    u6, f6 = with_frontier(u6, context.as_of)
    d6 = decide(u6, objective, context, load_kernel(u6, f6, "ac6"), issued_at=context.as_of)
    r6 = d6.evaluation.result_for(hub.entity_id)
    ids6 = primary + [hub.entity_id]
    deg6, pr6 = degree(d6.snapshot, ids6), pagerank(d6.snapshot, ids6, PAGERANK_DAMPING, PAGERANK_ITERATIONS)
    deg_rank = sorted(ids6, key=lambda h: (-(deg6[h] or 0), h)).index(hub.entity_id) + 1
    pr_rank = sorted(ids6, key=lambda h: (-(pr6[h] or 0), h)).index(hub.entity_id) + 1
    checks.append({"id": "AC6", "name": "highly connected but irrelevant candidate", "subject": hub.designation, "astro_status": r6.status, "astro_failed_rules": [e["detail"] for e in r6.eligibility if not e["passed"]],
                   "hub_degree": deg6[hub.entity_id], "median_primary_degree": sorted(deg6[h] for h in primary)[len(primary) // 2], "degree_rank": deg_rank, "pagerank_rank": pr_rank,
                   "pass": r6.status == "ineligible" and deg_rank == 1 and pr_rank == 1})

    # AC7a Context change: epoch --------------------------------------------------------------------------------
    ctx_now = ObservingContext.declare(label=context.label + " | AC7a retrieval-date epoch", as_of="2026-09-04T00:00:00Z", window_start="2026-09-04T00:00:00Z", window_end="2026-09-05T00:00:00Z",
                                       constraints=context.constraint_map)
    e7a = evaluate(base_u, base_d.snapshot, objective, ctx_now)
    increases, changed = [], 0
    for h in primary:
        a, b = _drift(base_d.evaluation.result_for(h)), _drift(e7a.result_for(h))
        if a and b and a["value"] is not None and b["value"] is not None:
            if b["value"] > a["value"] + 1e-12:
                increases.append(h)
            if abs(b["value"] - a["value"]) > 1e-12:
                changed += 1
    rho7a = spearman([base_d.evaluation.result_for(h).score for h in primary], [e7a.result_for(h).score for h in primary])
    checks.append({"id": "AC7a", "name": "Context change: epoch", "context_id": ctx_now.context_id, "drift_values_changed": changed, "drift_values_increased": len(increases),
                   "ranking_spearman_with_primary": None if rho7a is None else round(rho7a, 4), "rho_vs_labels": _rho(e7a, primary, grade_of), "pass": not increases})

    # AC7b Context change: feasibility -------------------------------------------------------------------------
    ctx_faint = context.with_changes(constraints={**context.constraint_map, "limiting_magnitude": 10.0}, label=context.label + " | AC7b V<=10")
    e7b = evaluate(base_u, base_d.snapshot, objective, ctx_faint)
    ok7b, cases7b = True, {"fainter_dropped": 0, "bright_unchanged": 0, "no_magnitude_unchanged": 0, "unexpected": []}
    for h in primary:
        r0, rb = base_d.evaluation.result_for(h), e7b.result_for(h)
        i0, ib = _feature(r0, "instrument_suitability"), _feature(rb, "instrument_suitability")
        mag = base_u.entity(h).attribute_map.get("magnitude_v")
        d = (rb.score or 0.0) - (r0.score or 0.0)
        if i0 and i0["status"] == "available" and mag is not None and float(mag) > 10.0:
            exp = -(i0["value"] * i0["weight"]) / _weight_sum(r0)
            if abs(d - exp) < 1e-9 and ib and ib["value"] == 0.0:
                cases7b["fainter_dropped"] += 1
            else:
                ok7b = False; cases7b["unexpected"].append(base_u.entity(h).designation)
        elif i0 and i0["status"] == "available":
            if abs(d) < 1e-12:
                cases7b["bright_unchanged"] += 1
            else:
                ok7b = False; cases7b["unexpected"].append(base_u.entity(h).designation)
        else:
            if abs(d) < 1e-12:
                cases7b["no_magnitude_unchanged"] += 1
            else:
                ok7b = False; cases7b["unexpected"].append(base_u.entity(h).designation)
    checks.append({"id": "AC7b", "name": "Context change: feasibility", "context_id": ctx_faint.context_id, **cases7b, "rho_vs_labels": _rho(e7b, primary, grade_of), "pass": ok7b})

    # AC8 relationship removal (ablation) ------------------------------------------------------------------------
    obj8 = _variant(objective, features=[f.to_record() for f in objective.features if f.name != "relationship_support"], eligible_relationship_types=[])
    e8 = evaluate(base_u, base_d.snapshot, obj8, context)
    base_rho = _rho(base_d.evaluation, primary, grade_of)
    checks.append({"id": "AC8", "name": "relationship removal (ablation)", "objective_id": obj8.objective_id, "rho_vs_labels": _rho(e8, primary, grade_of), "rho_declared": base_rho, "pass": None})

    # AC9 stance removal (ablation) ------------------------------------------------------------------------------
    u9 = _replace_relationships(base_u, [RelationshipAssertion.create(r.relationship_type, {k: list(vv) for k, vv in r.roles}, source=r.source, evidence_ids=(), literals=r.literal_map, confidence=r.confidence, status=r.status)
                                         for r in base_u.relationships])
    a9 = load_kernel(u9, None, "ac9")
    s9 = a9.snapshot()
    stances = {}
    for e in s9.edges:
        stances[e.stance] = stances.get(e.stance, 0) + 1
    e9_include = evaluate(u9, s9, _variant(objective, unevaluated_relationships="include"), context)
    e9_exclude = evaluate(u9, s9, objective, context)
    checks.append({"id": "AC9", "name": "stance removal (ablation)", "edge_stances": stances, "rho_trust_everything": _rho(e9_include, primary, grade_of), "rho_declared_policy_on_unevidenced_graph": _rho(e9_exclude, primary, grade_of), "rho_declared": base_rho, "pass": None})

    # AC10 uncertainty removal ------------------------------------------------------------------------------------
    # Re-creating an ephemeris record without its uncertainty changes its content id, so every relationship that cites the
    # old record must cite the new one (apparatus repair recorded in the report, 2026-09-04; first run raised UniverseError).
    remap: dict[str, str] = {}
    no_unc = []
    for e in base_u0.evidence:
        if e.kind == "ephemeris":
            n = EvidenceRecord.create(e.kind, e.subject_id, values=e.value_map, source=e.source, observed_at=e.observed_at, uncertainty={}, quality=e.quality, status=e.status,
                                      derived_from=e.derived_from, instrument_id=e.instrument_id)
            remap[e.evidence_id] = n.evidence_id
            no_unc.append(n)
        else:
            no_unc.append(e)
    rels10 = [RelationshipAssertion.create(r.relationship_type, {k: list(vv) for k, vv in r.roles}, source=r.source, evidence_ids=[remap.get(x, x) for x in r.evidence_ids],
                                           literals=r.literal_map, confidence=r.confidence, status=r.status) for r in base_u0.relationships]
    u10, f10 = with_frontier(Universe.create(base_u0.label, base_u0.data_class, base_u0.entities, no_unc, rels10, base_u0.states), context.as_of)
    a10 = load_kernel(u10, f10, "ac10")
    e10a = evaluate(u10, a10.snapshot(), objective, context)
    e10b = evaluate(u10, a10.snapshot(), _variant(objective, missingness_policy="zero_with_trace"), context)
    st10 = _statuses(e10a, primary)
    checks.append({"id": "AC10", "name": "uncertainty removal", "declared_objective_status_counts": st10, "rho_zero_with_trace_variant": _rho(e10b, primary, grade_of), "rho_declared": base_rho,
                   "pass": st10["indeterminate"] == len(primary)})

    # AC11 topology alone -----------------------------------------------------------------------------------------
    topo = results["topology_similarity_primary"]
    checks.append({"id": "AC11", "name": "topology alone", **topo, "limit": TOPOLOGY_LIMIT, "pass": all(v is not None and abs(v) < TOPOLOGY_LIMIT for v in topo.values())})

    # ACL leakage report --------------------------------------------------------------------------------------------
    checks.append({"id": "ACL", "name": "leakage report", "leakage_flagged": sel["counts"]["leakage_flagged"], "pool": sel["counts"]["pool"],
                   "secondary_metrics": [{"sample": s["sample"], "astro_rho": s["methods"]["astro"]["spearman_rho"], **{b: s["methods"][b]["spearman_rho"] for b in DECISIVE_BASELINES}} for s in results["metrics"]["secondary"]], "pass": None})

    summary = {"experiment": EXP_ID, "base_evaluation_reproduced": reproduced, "base_evaluation_id": base_d.evaluation.evaluation_id, "rank1_primary": rank1_entity.designation,
               "checks": checks, "passed": [c["id"] for c in checks if c["pass"] is True], "failed": [c["id"] for c in checks if c["pass"] is False], "ablations": [c["id"] for c in checks if c["pass"] is None]}
    (out / "adversarial.json").write_text(canonical_text(summary) + "\n", encoding="utf-8")
    return {"reproduced": reproduced, "passed": summary["passed"], "failed": summary["failed"], "ablations": summary["ablations"]}
