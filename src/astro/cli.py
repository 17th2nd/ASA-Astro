"""``astro`` command line: evaluate, explain, demo, version. Data-first; no LLM anywhere."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from astro import ASTRO_VERSION
from astro.asa.locator import asa_baseline_sha, kernel_version_record
from astro.domain import Universe
from astro.objectives.loaders import load_context, load_objective
from astro.pipeline import ROOT, decide, open_or_bootstrap
from astro.significance import explain
from astro_exec.core.canonical_json import canonical_text

DATA = ROOT / "data"


def _write(path: Path, value) -> None:
    path.write_text(canonical_text(value) + "\n", encoding="utf-8")


def _table(decision, universe, limit: int | None = None) -> str:
    lines = [f"  {'rank':>4}  {'status':13} {'designation':20} {'score':>7}  basis"]
    rows = decision.evaluation.results if limit is None else decision.evaluation.results[:limit]
    for r in rows:
        basis = ", ".join(c["feature"] for c in r.contributions if c["status"] == "available" and (c["value"] or 0) >= 0.25) if r.status == "eligible" else \
            "; ".join([e["detail"] for e in r.eligibility if not e["passed"]] + [c["feature"] + " unavailable" for c in r.contributions if c["status"] != "available" and c["required"]])
        score = f"{r.score:.4f}" if r.score is not None else "-"
        lines.append(f"  {r.rank or '-':>4}  {r.status:13} {r.designation:20} {score:>7}  {basis[:90]}")
    lines.append("  plan: " + (" → ".join(f"{a.sequence}. {a.action} {a.designation} ({a.duration_minutes} min)" for a in decision.plan.actions) or "nothing selected"))
    return "\n".join(lines)


def cmd_version(args) -> int:
    kv = kernel_version_record()
    print(json.dumps({"astro_version": ASTRO_VERSION, "asa_baseline": asa_baseline_sha(), "kernel_version": kv["kernel"], "kernel_status": kv["status"]}, sort_keys=True))
    return 0


def cmd_evaluate(args) -> int:
    universe = Universe.load(args.universe)
    objective = load_objective(args.objective)
    context = load_context(args.context, universe)
    adapter = open_or_bootstrap(universe, args.store)
    d = decide(universe, objective, context, adapter)
    print(f"objective: {objective.name}  context: {context.label}")
    print(f"universe {universe.universe_id}\nkernel digest {d.snapshot.digest}  ASA baseline {d.snapshot.asa_baseline[:12]}")
    print(_table(d, universe))
    if args.out:
        out = Path(args.out)
        out.mkdir(parents=True, exist_ok=True)
        _write(out / "evaluation.json", d.evaluation.to_record())
        _write(out / "plan.json", d.plan.to_record())
        _write(out / "objective.json", objective.to_record())
        _write(out / "context.json", context.to_record())
        d.receipt.write(out)
        print(f"written: {out}/evaluation.json plan.json objective.json context.json receipt.json receipt.sha256  receipt {d.receipt.receipt_id}")
    return 0


def cmd_explain(args) -> int:
    out = Path(args.out)
    receipt = json.loads((out / "receipt.json").read_text(encoding="utf-8"))
    universe = Universe.load(args.universe)
    objective = load_objective(out / "objective.json")
    entity = universe.find(args.entity)
    ex = receipt["explanations"].get(entity.entity_id)
    if ex is None:
        from astro.significance.evaluator import SignificanceEvaluation, SignificanceResult
        rec = next(r for r in receipt["results"] if r["entity_id"] == entity.entity_id)
        result = SignificanceResult(rec["entity_id"], rec["designation"], rec["kind"], rec["status"], rec["score"], rec["rank"],
                                    tuple(rec["contributions"]), tuple(rec["eligibility"]), tuple(rec["relationship_keys"]),
                                    tuple(rec["evidence_ids"]), tuple(rec["unavailable"]))
        ev = SignificanceEvaluation(receipt["evaluation_id"], receipt["objective_id"], receipt["objective_version"], receipt["context_id"],
                                    receipt["universe_id"], receipt["asa_baseline"], receipt["kernel_version"], receipt["kernel_digest"],
                                    receipt["kernel_head"], receipt["registry_digest"], receipt["astro_version"], receipt["weighting_policy_ref"], (result,))
        ex = explain(ev, objective, entity.entity_id)
    print(f"Target: {ex['designation']}\nCurrent objective: {ex['objective']}\nStatus: {ex['status']}  score: {ex['score']}  rank: {ex['rank']}")
    print("Why significant now:" if ex["why_significant_now"] else "Why significant now: (nothing at or above the explanation threshold)")
    for line in ex["why_significant_now"]:
        print(f"  - {line}")
    print("Why not more:")
    for line in ex["why_not_more"] or ["(no limiting factor recorded)"]:
        print(f"  - {line}")
    print(f"Evidence used: {len(ex['evidence_used'])}  relationships used: {len(ex['relationships_used'])}  evaluation {ex['evaluation_id']}")
    return 0


def cmd_demo(args) -> int:
    universe = Universe.load(DATA / "universe" / "slice1.json")
    context = load_context(DATA / "contexts" / "night-2026-09-03.json", universe)
    adapter = open_or_bootstrap(universe)
    names = {"A": "A-exoplanet-transit-followup.json", "B": "B-transient-followup.json", "C": "C-stellar-variability.json", "D": "D-calibration.json"}
    objectives = {k: load_objective(DATA / "objectives" / v) for k, v in names.items()}
    print(f"Universe {universe.universe_id} ({universe.data_class}, {len(universe.entities)} entities, {len(universe.evidence)} evidence, {len(universe.relationships)} relationships)")
    print(f"ASA kernel digest {adapter.digest()}  baseline {asa_baseline_sha()[:12]}\n")
    if args.scenario == "context-switch":
        before = (universe.to_record(), adapter.digest())
        for k in ("A", "B", "C", "D"):
            d = decide(universe, objectives[k], context, adapter)
            print(f"Objective {k}: {objectives[k].name}")
            print(_table(d, universe, limit=5))
            print()
        after = (universe.to_record(), adapter.digest())
        print("Universe unchanged:", before[0] == after[0], " ASA relational state unchanged:", before[1] == after[1])
        print("Only the objective changed; the significance ranking and the selected work changed with it.")
    elif args.scenario == "evidence-arrival":
        from astro.domain import EvidenceRecord, Provenance
        syn = Provenance("astro-demo", "synthetic", "astro demo evidence-arrival")
        first = decide(universe, objectives["A"], context, adapter)
        print("Objective A before new evidence:")
        print(_table(first, universe, limit=3))
        host_a, host_b = universe.find("SYN-HOST-A"), universe.find("SYN-HOST-B")
        old_a = universe.evidence_for(host_a.entity_id, "ephemeris")[0]
        corrected_a = EvidenceRecord.create("ephemeris", host_a.entity_id, values={"period_days": 2.75, "epoch_utc": "2026-09-01T03:30:00Z", "duration_hours": 2.1}, source=syn, quality=0.97)
        refined_b = EvidenceRecord.create("ephemeris", host_b.entity_id, values={"period_days": 9.4, "epoch_utc": "2026-09-03T14:00:00Z", "duration_hours": 3.0}, source=syn, quality=0.95)
        u2 = universe.supersede_evidence(old_a.evidence_id, corrected_a).with_evidence(refined_b, label="slice1+evidence")
        counts = adapter.load_universe(u2)
        second = decide(u2, objectives["A"], context, adapter)
        print("\nNew evidence: a corrected ephemeris epoch for SYN-HOST-A (supersedes the old record; tonight's transit moves out of the window);")
        print(f"a refined ephemeris for SYN-HOST-B with a transit tonight. ASA registered {counts['evidence']} records and {counts['status_updates']} status update.")
        print(f"Universe {u2.universe_id}  kernel digest {second.snapshot.digest}\n\nObjective A after new evidence (same objective, same context):")
        print(_table(second, universe, limit=3))
        print(f"\nEntity identities unchanged: {[e.entity_id for e in universe.entities] == [e.entity_id for e in u2.entities]}")
    elif args.scenario == "session":
        from astro.session import run_session
        for k in ("A", "C"):
            adapter = open_or_bootstrap(universe)
            s = run_session(universe, objectives[k], context, adapter)
            print(f"Objective {k}: {objectives[k].name} — session {s.session_id[:20]}")
            for c in s.cycles:
                ex = c.outcome.action if c.outcome else None
                ranked = ", ".join(f"{r.designation} {r.score:.3f}" for r in c.decision.evaluation.ranked()[:3])
                skipped = "; ".join(f"{x.designation}: {x.reason}" for x in c.decision.plan.skipped if x.status == "eligible")
                print(f"  cycle {c.index} as of {c.as_of}: ranked [{ranked}]")
                print(f"    plan {[a.designation for a in c.decision.plan.actions]}" + (f"  skipped: {skipped}" if skipped else ""))
                print(f"    executed {ex.designation} {ex.start_utc}–{ex.end_utc}; {len(c.outcome.evidence)} simulated evidence records → universe {c.outcome.universe_after[:16]}" if ex else "    nothing schedulable; session ends")
            print(f"  executed: {list(s.executed())}  final universe {s.final_universe.universe_id[:16]}  kernel {adapter.digest()[:23]}\n")
    return 0


def cmd_session(args) -> int:
    from astro.session import run_session
    universe = Universe.load(args.universe)
    objective = load_objective(args.objective)
    context = load_context(args.context, universe)
    adapter = open_or_bootstrap(universe, args.store)
    s = run_session(universe, objective, context, adapter, max_cycles=args.max_cycles)
    for c in s.cycles:
        ex = c.outcome.action if c.outcome else None
        print(f"cycle {c.index} as of {c.as_of}: ranked {[r.designation for r in c.decision.evaluation.ranked()][:4]} plan {[a.designation for a in c.decision.plan.actions]}")
        print(f"  {'executed ' + ex.designation + ' ' + ex.start_utc + '–' + ex.end_utc if ex else 'nothing schedulable; session ends'}")
    print(f"session {s.session_id}\nexecuted {list(s.executed())}\nfinal universe {s.final_universe.universe_id}\nkernel digest {adapter.digest()}")
    if args.out:
        out = Path(args.out)
        out.mkdir(parents=True, exist_ok=True)
        _write(out / "session.json", s.to_record())
        s.final_universe.save(out / "universe-final.json")
        for c in s.cycles:
            c.decision.receipt.write(out / f"cycle-{c.index:02d}")
        print(f"written: {out}/session.json universe-final.json cycle-NN/receipt.json")
    return 0


def cmd_benchmark(args) -> int:
    from astro.benchmark import run_benchmark
    universe = Universe.load(args.universe)
    context = load_context(args.context, universe)
    records = []
    for path in args.objective:
        objective = load_objective(path)
        b = run_benchmark(universe, objective, context)
        records.append(b.to_record())
        print(f"{objective.name}  (universe {universe.universe_id[:16]}, benchmark {b.benchmark_id[:16]})")
        print(f"  {'strategy':16} {'useful':>8} {'wasted':>12} {'first useful':>13}  executed")
        for r in b.results:
            first = f"{r.time_to_first_useful_minutes} min" if r.time_to_first_useful_minutes is not None else "never"
            print(f"  {r.strategy:16} {r.useful_actions:>3}/{len(r.executed):<4} {r.wasted_minutes:>5}/{r.total_minutes:<5}min {first:>13}  " + ", ".join(f"{e['designation']}{'' if e['useful'] else ' ✗'}" for e in r.executed))
        print()
    print("Baselines apply only the kind filter and the objective's budgets; they never see evidence, relationships or significance.")
    print("`oracle` selects with the benchmark's ground-truth scorer and is an upper bound, not a runnable strategy.")
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        _write(Path(args.out), {"benchmarks": records})
        print(f"written: {args.out}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="astro", description="Astro — Astronomy Execution Engine on ASA")
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("version").set_defaults(fn=cmd_version)
    e = sub.add_parser("evaluate", help="evaluate a universe under an objective and context; write evaluation, plan and receipt")
    e.add_argument("--universe", required=True)
    e.add_argument("--objective", required=True)
    e.add_argument("--context", required=True)
    e.add_argument("--out", help="output directory")
    e.add_argument("--store", help="persistent ASA store directory (default: in-memory)")
    e.set_defaults(fn=cmd_evaluate)
    x = sub.add_parser("explain", help="explain one entity's result from a written decision")
    x.add_argument("--out", required=True, help="directory written by `astro evaluate --out`")
    x.add_argument("--universe", required=True)
    x.add_argument("--entity", required=True, help="designation or alias")
    x.set_defaults(fn=cmd_explain)
    d = sub.add_parser("demo", help="run a canonical demonstration on the slice-1 synthetic universe")
    d.add_argument("scenario", choices=["context-switch", "evidence-arrival", "session"])
    d.set_defaults(fn=cmd_demo)
    s = sub.add_parser("session", help="run the evaluate → plan → schedule → execute → re-evaluate loop with the simulated executor")
    s.add_argument("--universe", required=True)
    s.add_argument("--objective", required=True)
    s.add_argument("--context", required=True)
    s.add_argument("--out")
    s.add_argument("--store")
    s.add_argument("--max-cycles", type=int, default=6)
    s.set_defaults(fn=cmd_session)
    b = sub.add_parser("benchmark", help="compare ASA-guided execution with fifo, random, static-priority and oracle strategies")
    b.add_argument("--universe", required=True)
    b.add_argument("--objective", required=True, nargs="+")
    b.add_argument("--context", required=True)
    b.add_argument("--out")
    b.set_defaults(fn=cmd_benchmark)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
