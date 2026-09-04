"""The single pre-registered run of ASTRO-REAL-DATA-EXP-0001: evaluate once, score the declared baselines, compute the
declared metrics, write everything machine-readable. No parameter here is chosen after seeing a result."""

from __future__ import annotations

import csv
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from astro.domain import Universe
from astro.objectives import Objective, ObservingContext
from astro.objectives.loaders import load_objective
from astro.pipeline import ROOT, decide
from astro.receipts import astro_commit
from astro.significance import evaluate, explain
from astro_exec.core.canonical_json import canonical_text
from . import EXP_ID
from .baselines import brightness, degree, pagerank, projected_uncertainty_formula, random_baseline, sigma_period
from .dataset import DATASET_DIR, GRADE, RESULTS_DIR, load_reference, load_selection, verify_dataset
from .manifest import (BOOTSTRAP_RESAMPLES, BOOTSTRAP_SEED, MARGIN, NDCG_K, OBJECTIVE_PATH, PAGERANK_DAMPING, PAGERANK_ITERATIONS, PRECISION_K,
                       RANDOM_BASELINE_SEED, TOPOLOGY_LIMIT, declare_context, load_manifest, verify_manifest)
from .metrics import bootstrap_ci, ndcg_at_k, ordering, precision_at_k, spearman
from .universe import build_universe, host_of_planet, load_kernel

DECISIVE_BASELINES = ("brightness", "sigma_period", "degree", "pagerank")
DIAGNOSTIC_BASELINES = ("random", "projected_uncertainty_formula")


def _write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(canonical_text(value) + "\n", encoding="utf-8")


def preconditions() -> dict[str, Any]:
    ds = verify_dataset()
    mf = verify_manifest()
    ok = all(v["ok"] for v in ds.values()) and mf["ok"]
    return {"dataset": ds, "manifest": mf, "ok": ok}


def astro_scores(evaluation, hosts: Iterable[str]) -> tuple[dict[str, float | None], dict[str, str]]:
    scores, status = {}, {}
    for h in hosts:
        r = evaluation.result_for(h)
        status[h] = r.status
        scores[h] = r.score if r.status == "eligible" else None
    return scores, status


def sample_metrics(name: str, ids: list[str], grade_of: dict[str, float], methods: dict[str, dict[str, float | None]], *, bootstrap: bool) -> dict[str, Any]:
    out: dict[str, Any] = {"sample": name, "n": len(ids), "grade_counts": {g: sum(1 for i in ids if grade_of[i] == GRADE[g]) for g in GRADE}, "methods": {}}
    grades = [grade_of[i] for i in ids]
    for m, sc in methods.items():
        vals = [sc.get(i) for i in ids]
        order = ordering(ids, vals)
        out["methods"][m] = {
            "spearman_rho": None if (r := spearman(vals, grades)) is None else round(r, 4),
            f"ndcg_at_{NDCG_K}": round(ndcg_at_k(order, grade_of, NDCG_K), 4),
            f"precision_at_{PRECISION_K}": round(precision_at_k(order, grade_of, PRECISION_K), 4),
            "unranked": sum(1 for v in vals if v is None),
        }
    if bootstrap:
        out["bootstrap"] = {"astro": bootstrap_ci(ids, grade_of, methods["astro"], None, BOOTSTRAP_RESAMPLES, BOOTSTRAP_SEED)}
        for b in DECISIVE_BASELINES:
            out["bootstrap"][f"astro_minus_{b}"] = bootstrap_ci(ids, grade_of, methods["astro"], methods[b], BOOTSTRAP_RESAMPLES, BOOTSTRAP_SEED)
    return out


def acceptance_from_metrics(primary: dict[str, Any], topology: dict[str, float | None]) -> dict[str, Any]:
    m = primary["methods"]
    rho = {k: v["spearman_rho"] for k, v in m.items()}
    nd = {k: v[f"ndcg_at_{NDCG_K}"] for k, v in m.items()}
    ci = primary["bootstrap"]["astro"]["rho_ci95"]
    checks = {
        "rho_margin": {b: (rho["astro"] is not None and rho[b] is not None and rho["astro"] >= rho[b] + MARGIN) for b in DECISIVE_BASELINES},
        "ci_above_zero": bool(ci and ci[0] > 0),
        "ndcg_not_below": {b: nd["astro"] >= nd[b] for b in DECISIVE_BASELINES},
        "topology_below_limit": {k: (v is not None and abs(v) < TOPOLOGY_LIMIT) for k, v in topology.items()},
        "reproduces_topology": bool(topology.get("pagerank") is not None and abs(topology["pagerank"]) >= TOPOLOGY_LIMIT and rho["astro"] is not None and rho["pagerank"] is not None and rho["astro"] <= rho["pagerank"] + 0.05),
    }
    brightness_graph_ok = all(checks["rho_margin"][b] for b in ("brightness", "degree", "pagerank"))
    all_margin_ok = all(checks["rho_margin"].values())
    if not brightness_graph_ok or not checks["ci_above_zero"] or checks["reproduces_topology"]:
        metric_verdict = "FAIL"
    elif all_margin_ok and all(checks["ndcg_not_below"].values()) and all(checks["topology_below_limit"].values()):
        metric_verdict = "PASS"
    else:
        metric_verdict = "MIXED"
    return {"checks": checks, "metric_verdict_before_adversarial": metric_verdict}


def run_experiment(out_dir: Path | None = None, hosts: Iterable[str] | None = None) -> dict[str, Any]:
    """The run. ``hosts``/``out_dir`` exist only so the apparatus can be smoke-tested on a subset into a scratch directory."""
    out = Path(out_dir) if out_dir else RESULTS_DIR
    pre = preconditions()
    if not pre["ok"]:
        _write(out / "INVALID.json", {"reason": "dataset or manifest digest does not verify", **pre})
        return {"verdict": "INVALID", **pre}
    manifest = load_manifest()
    objective = load_objective(OBJECTIVE_PATH)
    context = declare_context()
    assert objective.objective_id == manifest["objective"]["objective_id"], "objective declaration drifted from the manifest"
    assert context.context_id == manifest["context"]["context_id"], "context declaration drifted from the manifest"
    sel, reference = load_selection(), load_reference()
    timings: dict[str, float] = {}
    t = time.time()
    universe, frontier = build_universe(context.as_of, hosts=hosts)
    timings["universe_s"] = round(time.time() - t, 1)
    t = time.time()
    adapter = load_kernel(universe, frontier)
    timings["kernel_load_s"] = round(time.time() - t, 1)
    t = time.time()
    d = decide(universe, objective, context, adapter, issued_at=context.as_of)
    timings["evaluate_s"] = round(time.time() - t, 1)
    snapshot = d.snapshot

    def hosts_for(planets: Iterable[str]) -> dict[str, str]:
        found = {}
        for p in planets:
            try:
                found[p] = host_of_planet(universe, p).entity_id
            except KeyError:
                continue
        return found

    primary_map = hosts_for(sel["primary"])
    pool_map = hosts_for(sel["pool_ordered"])
    flagged_map = hosts_for([x["name"] for x in sel["leakage_flagged"]])
    missing_map = hosts_for(sel["missing_uncertainty"])
    all_hosts = sorted(set(pool_map.values()) | set(flagged_map.values()) | set(missing_map.values()))
    grade_of = {h: float(reference[p]["grade"]) for p, h in {**pool_map, **flagged_map, **missing_map}.items()}
    planet_of = {h: p for p, h in {**pool_map, **flagged_map, **missing_map}.items()}

    t = time.time()
    a_scores, a_status = astro_scores(d.evaluation, all_hosts)
    rows_by_host: dict[str, dict] = {}
    with (DATASET_DIR / "input_pscomppars_rows.csv").open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            try:
                h = universe.find(row["hostname"]).entity_id
            except KeyError:
                continue
            if row.get("tran_flag") == "1" and row.get("pl_orbper") and row.get("pl_tranmid"):
                rows_by_host[h] = row
    methods: dict[str, dict[str, float | None]] = {
        "astro": a_scores,
        "brightness": brightness(universe, all_hosts),
        "sigma_period": sigma_period(universe, all_hosts),
        "degree": degree(snapshot, all_hosts),
        "pagerank": pagerank(snapshot, all_hosts, PAGERANK_DAMPING, PAGERANK_ITERATIONS),
        "random": random_baseline(all_hosts, RANDOM_BASELINE_SEED),
        "projected_uncertainty_formula": projected_uncertainty_formula(rows_by_host, all_hosts, context.as_of),
    }
    timings["baselines_s"] = round(time.time() - t, 1)

    primary_ids = [primary_map[p] for p in sel["primary"] if p in primary_map]
    pool_ids = [pool_map[p] for p in sel["pool_ordered"] if p in pool_map]
    pool_plus_ids = pool_ids + [flagged_map[x["name"]] for x in sel["leakage_flagged"] if x["name"] in flagged_map]
    t = time.time()
    primary = sample_metrics("primary", primary_ids, grade_of, methods, bootstrap=True)
    secondary_pool = sample_metrics("pool (secondary, non-decisive)", pool_ids, grade_of, methods, bootstrap=False)
    secondary_plus = sample_metrics("pool + leakage-flagged (secondary, non-decisive)", pool_plus_ids, grade_of, methods, bootstrap=False)
    timings["metrics_s"] = round(time.time() - t, 1)
    p_astro = [a_scores[h] for h in primary_ids]
    topology = {"degree": None if (r := spearman(p_astro, [methods["degree"][h] or 0.0 for h in primary_ids])) is None else round(r, 4),
                "pagerank": None if (r := spearman(p_astro, [methods["pagerank"][h] or 0.0 for h in primary_ids])) is None else round(r, 4)}
    acceptance = acceptance_from_metrics(primary, topology)

    # diagnostic: objective E exactly as declared, same Context (no site -> visibility unavailable)
    obj_e = load_objective(ROOT / "data" / "objectives" / "E-knowledge-gap-reduction.json")
    ev_e = evaluate(universe, snapshot, obj_e, context)
    e_status = {s: sum(1 for h in primary_ids if ev_e.result_for(h).status == s) for s in ("eligible", "ineligible", "indeterminate")}
    e_scores = {h: (ev_e.result_for(h).score if ev_e.result_for(h).status == "eligible" else None) for h in primary_ids}
    e_rho = spearman([e_scores[h] for h in primary_ids], [grade_of[h] for h in primary_ids])

    # per-candidate table and explanations (every primary candidate)
    table = []
    for h in all_hosts:
        r = d.evaluation.result_for(h)
        drift = next((c for c in r.contributions if c["feature"] == "ephemeris_drift"), None)
        table.append({"planet": planet_of[h], "host": universe.entity(h).designation, "host_entity_id": h, "priority": reference[planet_of[h]]["priority"], "grade": grade_of[h],
                      "in_primary": h in set(primary_ids), "in_pool": h in set(pool_ids), "leakage_flagged": h in set(flagged_map.values()), "missing_uncertainty_heldout": h in set(missing_map.values()),
                      "astro_status": r.status, "astro_score": r.score, "astro_rank_overall": r.rank,
                      "ephemeris_drift": drift["value"] if drift else None, "ephemeris_drift_status": drift["status"] if drift else None,
                      **{m: methods[m].get(h) for m in methods if m != "astro"}})
    explanations = {planet_of[h]: explain(d.evaluation, objective, h) for h in primary_ids}

    result = {
        "experiment": EXP_ID, "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "astro_commit": astro_commit(),
        "manifest_sha256": pre["manifest"]["actual"], "preconditions": pre,
        "objective_id": objective.objective_id, "context_id": context.context_id, "universe_id": universe.universe_id,
        "universe_counts": {"entities": len(universe.entities), "evidence": len(universe.evidence), "relationships": len(universe.relationships)},
        "frontier_counts": frontier.counts, "kernel": {"seq": snapshot.seq, "head": snapshot.head, "digest": snapshot.digest, "asa_baseline": snapshot.asa_baseline, "kernel_version": snapshot.kernel_version},
        "evaluation_id": d.evaluation.evaluation_id, "receipt_id": d.receipt.receipt_id, "plan_id": d.plan.plan_id,
        "hosts": {"all": len(all_hosts), "primary": len(primary_ids), "pool": len(pool_ids), "leakage_flagged": len(flagged_map), "missing_uncertainty": len(missing_map),
                  "unresolved_planets": sorted(set(sel["primary"]) - set(primary_map))},
        "astro_status_counts_primary": {s: sum(1 for h in primary_ids if a_status[h] == s) for s in ("eligible", "ineligible", "indeterminate")},
        "metrics": {"primary": primary, "secondary": [secondary_pool, secondary_plus]},
        "topology_similarity_primary": topology, "acceptance": acceptance,
        "diagnostic_objective_E": {"objective_id": obj_e.objective_id, "status_counts_primary": e_status, "spearman_rho": None if e_rho is None else round(e_rho, 4)},
        "timings_s": timings,
    }
    _write(out / "results.json", result)
    _write(out / "candidates_scored.json", table)
    _write(out / "explanations.json", explanations)
    run_dir = out / "primary-run"
    run_dir.mkdir(parents=True, exist_ok=True)
    _write(run_dir / "evaluation.json", d.evaluation.to_record())
    _write(run_dir / "plan.json", d.plan.to_record())
    _write(run_dir / "objective.json", objective.to_record())
    _write(run_dir / "context.json", context.to_record())
    d.receipt.write(run_dir)
    with (out / "candidates_scored.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(table[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(table)
    (out / "COMPARISON.md").write_text(comparison_table(result), encoding="utf-8")
    return {"verdict_metrics_only": acceptance["metric_verdict_before_adversarial"], "primary": primary, "topology": topology, "timings": timings, "out": str(out)}


def comparison_table(result: dict[str, Any]) -> str:
    lines = [f"# {EXP_ID} — comparison table", "", f"Run {result['run_at']} · commit `{result['astro_commit']}` · manifest sha256 `{result['manifest_sha256']}`", ""]
    for block in [result["metrics"]["primary"], *result["metrics"]["secondary"]]:
        lines += [f"## {block['sample']} (n = {block['n']}; grades {block['grade_counts']})", "",
                  f"| method | Spearman ρ | NDCG@{NDCG_K} | P@{PRECISION_K} (grade ≥ 2) | unranked |", "|---|---:|---:|---:|---:|"]
        for m, v in block["methods"].items():
            tag = " (diagnostic)" if m in DIAGNOSTIC_BASELINES else ""
            lines.append(f"| {m}{tag} | {v['spearman_rho']} | {v[f'ndcg_at_{NDCG_K}']} | {v[f'precision_at_{PRECISION_K}']} | {v['unranked']} |")
        if "bootstrap" in block:
            lines += ["", "Bootstrap 95% CIs (paired, 2000 resamples):", ""]
            for k, v in block["bootstrap"].items():
                lines.append(f"- {k}: ρ CI {v['rho_ci95']}" + (f", difference CI {v['diff_ci95']}" if v.get("diff_ci95") else ""))
        lines.append("")
    lines += ["## Topology similarity (primary)", "", f"Spearman(ASTRO, degree) = {result['topology_similarity_primary']['degree']}; Spearman(ASTRO, PageRank) = {result['topology_similarity_primary']['pagerank']}", "",
              "## Objective E as declared (diagnostic)", "", f"status counts on the primary sample: {result['diagnostic_objective_E']['status_counts_primary']}; Spearman ρ = {result['diagnostic_objective_E']['spearman_rho']}", "",
              "## Acceptance checks (metrics only; adversarial checks are combined in the report)", "", "```", json.dumps(result["acceptance"], indent=1), "```", ""]
    return "\n".join(lines)
