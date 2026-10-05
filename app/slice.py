"""Thin V1 slice: pin → kernel snapshot → exactly one Objective → digest-identified receipt.

Everything scientific shown by the app comes from the records written here, which come from
``astro.pipeline.decide`` (src/astro) running on the pinned ASA kernel. The derived view
(labels, unknowns, next evidence) only re-states fields that exist and cites each one by
artifact + JSON pointer. Nothing here invents a score, a confidence or a scientific claim.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import tempfile
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import APP_VERSION
from . import pin as pinmod

ROOT = pinmod.ROOT
_LOCK = threading.Lock()
SLUG = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,80}$")
RUN_ID = re.compile(r"^RCPT-[0-9a-f]{64}$")
ARTIFACTS = ("pin.json", "snapshot.json", "objective.json", "context.json", "evaluation.json", "plan.json",
             "receipt.json", "receipt.sha256", "run.json", "view.json")

LABEL_POLICY = {
    "id": "app-honesty-labels-v1",
    "established": "established-in-ASA-state: the pinned kernel's canonical projection endorses the record, its lifecycle is "
                   "'registered', evidence status (if any) is 'admissible', and the data class is 'real'. This means "
                   "established inside this ASA relational state only — it is NOT empirical validation (README: empirical "
                   "validation not commenced).",
    "hypothesis": "hypothesis: anything that fails one of those tests, plus every Objective score, rank, explanation and "
                  "plan, which are Astro-derived constructs under a declared weighting policy.",
    "record": "record: an engineering fact (hash, digest, verified checkout) — not a scientific claim.",
}


def data_dir() -> Path:
    """``ASA_ASTRO_APP_DATA_DIR`` overrides ``app/config.json:data_dir`` (used by tests)."""
    override = os.environ.get("ASA_ASTRO_APP_DATA_DIR")
    return Path(override) if override else ROOT / pinmod.app_config()["data_dir"]


def runs_dir() -> Path:
    return data_dir() / "runs"


def list_objectives() -> list[dict[str, Any]]:
    folder = ROOT / pinmod.app_config()["objectives_dir"]
    out = []
    for path in sorted(folder.glob("*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        out.append({"slug": path.stem, "name": record.get("name"), "question": record.get("question"),
                    "authority": record.get("authority"), "path": str(path.relative_to(ROOT))})
    return out


def _canon(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _sha(text: str | bytes) -> str:
    return hashlib.sha256(text.encode("utf-8") if isinstance(text, str) else text).hexdigest()


def _ref(artifact: str, pointer: str) -> dict[str, str]:
    return {"artifact": artifact, "pointer": pointer}


# ---- derivations (only from fields that exist) -------------------------------------------------
def _snapshot_detail(snapshot, universe) -> dict[str, Any]:
    names = {e.entity_id: e.designation for e in universe.entities}
    ev_by_id = {e.evidence_id: e for e in universe.evidence}

    def nm(ref: str) -> str:
        return names.get(ref, ref)

    edges = [{"key": e.key, "type": e.type_name, "lifecycle": e.lifecycle, "asa_stance": e.stance,
              "bindings": {role: list(refs) for role, refs in e.bindings},
              "bindings_named": {role: [nm(r) for r in refs] for role, refs in e.bindings},
              "literals": {k: v for k, v in e.literals}, "supported_by": list(e.supported_by)} for e in snapshot.edges]
    links = []
    for l in snapshot.evidence_links:
        ev = ev_by_id.get(l.evidence_id)
        links.append({"key": l.key, "evidence_id": l.evidence_id, "subject_id": l.subject_id, "subject": nm(l.subject_id),
                      "evidence_kind": l.evidence_kind, "status": l.status, "asa_stance": l.stance,
                      "data_class": ev.source.data_class if ev is not None and ev.source is not None else None,
                      "source": ev.source.source if ev is not None and ev.source is not None else None})
    states = [{"key": s.key, "entity_id": s.entity_id, "entity": nm(s.entity_id), "lifecycle": s.lifecycle,
               "literals": {k: v for k, v in s.literals}} for s in snapshot.states]
    return {"summary": snapshot.to_record(), "edges": edges, "evidence_links": links, "states": states,
            "universe": {"universe_id": universe.universe_id, "data_class": universe.data_class,
                         "entities": len(universe.entities), "evidence": len(universe.evidence),
                         "relationships": len(universe.relationships)},
            "detail_note": "edges/evidence_links/states rendered by the app from RelationalSnapshot fields; names mapped from the universe file"}


def _label_edge(edge: dict[str, Any], data_class: str) -> tuple[str, list[str]]:
    reasons = []
    if edge["asa_stance"] != "endorsed":
        reasons.append(f"ASA stance is '{edge['asa_stance']}'")
    if edge["lifecycle"] != "registered":
        reasons.append(f"lifecycle is '{edge['lifecycle']}'")
    if data_class != "real":
        reasons.append(f"universe data_class is '{data_class}'")
    return ("established-in-ASA-state" if not reasons else "hypothesis"), reasons


def _label_link(link: dict[str, Any]) -> tuple[str, list[str]]:
    reasons = []
    if link["asa_stance"] != "endorsed":
        reasons.append(f"ASA stance is '{link['asa_stance']}'")
    if link["status"] != "admissible":
        reasons.append(f"evidence status is '{link['status']}'")
    if link.get("data_class") != "real":
        reasons.append(f"evidence data_class is '{link.get('data_class')}'")
    return ("established-in-ASA-state" if not reasons else "hypothesis"), reasons


def build_view(run_id: str, pin: dict, snap: dict, objective: dict, context: dict, receipt: dict, run: dict) -> dict[str, Any]:
    data_class = snap["universe"]["data_class"]
    claims: list[dict[str, Any]] = []
    for i, e in enumerate(snap["edges"]):
        label, reasons = _label_edge(e, data_class)
        parts = "; ".join(f"{role}: {', '.join(v)}" for role, v in sorted(e["bindings_named"].items()))
        claims.append({"group": "relationship", "text": f"{e['type']} — {parts}", "label": label, "reasons": reasons,
                       "source": _ref("snapshot.json", f"/edges/{i}")})
    for i, l in enumerate(snap["evidence_links"]):
        label, reasons = _label_link(l)
        claims.append({"group": "evidence", "text": f"{l['evidence_kind']} evidence {l['evidence_id'][:16]}… about {l['subject']}",
                       "label": label, "reasons": reasons, "source": _ref("snapshot.json", f"/evidence_links/{i}")})
    for i, r in enumerate(receipt["results"]):
        if r["status"] == "eligible":
            claims.append({"group": "objective-result",
                           "text": f"{r['designation']} ranks {r['rank']} under '{receipt['objective_name']}' (score {r['score']})",
                           "label": "hypothesis",
                           "reasons": ["Objective score/rank is an Astro-derived construct under weighting policy "
                                       f"{receipt['weighting_policy_ref']}; not empirically validated"],
                           "source": _ref("receipt.json", f"/results/{i}")})
    for i, a in enumerate(receipt["selected_actions"]):
        claims.append({"group": "plan", "text": f"plan step {a['sequence']}: {a['action']} {a['designation']} ({a['duration_minutes']} min)",
                       "label": "hypothesis", "reasons": ["a plan is a recommendation derived from the Objective evaluation"],
                       "source": _ref("receipt.json", f"/selected_actions/{i}")})

    unknowns: list[dict[str, Any]] = []
    if "NOT A FROZEN" in (pin.get("pin_status_declared") or "").upper() or "NOT RATIFIED" in (pin.get("kernel_status_reported_by_kernel") or "").upper():
        unknowns.append({"kind": "pin-status", "text": f"ASA pin status: {pin.get('pin_status_declared')}; kernel reports '{pin.get('kernel_status_reported_by_kernel')}'",
                         "source": _ref("pin.json", "/pin_status_declared")})
    if pin.get("pin_kernel_version_declared") != pin.get("kernel_version_reported_by_kernel"):
        unknowns.append({"kind": "pin-version", "text": f"pin file declares kernel_version '{pin.get('pin_kernel_version_declared')}' but the kernel reports '{pin.get('kernel_version_reported_by_kernel')}'",
                         "source": _ref("pin.json", "/kernel_version_reported_by_kernel")})
    for i, r in enumerate(receipt["results"]):
        for j, c in enumerate(r["contributions"]):
            if c.get("status") != "available":
                unknowns.append({"kind": "feature-unavailable", "text": f"{r['designation']}: feature '{c['feature']}' is {c.get('status')}",
                                 "source": _ref("receipt.json", f"/results/{i}/contributions/{j}")})
        for j, u in enumerate(r.get("unavailable") or []):
            unknowns.append({"kind": "unavailable", "text": f"{r['designation']}: {u}", "source": _ref("receipt.json", f"/results/{i}/unavailable/{j}")})
        in_scope = all(el["passed"] for el in r["eligibility"] if el["rule"] == "target_kind")
        for j, el in enumerate(r["eligibility"]):
            if in_scope and not el["passed"] and el["rule"] == "required_evidence":
                unknowns.append({"kind": "missing-required-evidence", "text": f"{r['designation']}: {el['detail']}",
                                 "source": _ref("receipt.json", f"/results/{i}/eligibility/{j}")})
    seen_models = set()
    for i, r in enumerate(receipt["results"]):
        for j, c in enumerate(r["contributions"]):
            model = (c.get("trace") or {}).get("model")
            if model and (c["feature"], model) not in seen_models:
                seen_models.add((c["feature"], model))
                unknowns.append({"kind": "model-limitation", "text": f"feature '{c['feature']}' model: {model}",
                                 "source": _ref("receipt.json", f"/results/{i}/contributions/{j}/trace/model")})
    for i, e in enumerate(snap["edges"]):
        if e["asa_stance"] == "unevaluated":
            unknowns.append({"kind": "unevaluated-relationship", "text": f"ASA has not evaluated {e['type']} ({'; '.join(', '.join(v) for v in e['bindings_named'].values())})",
                             "source": _ref("snapshot.json", f"/edges/{i}")})
        if e["type"] in ("lacks_evidence", "lacks-evidence"):
            unknowns.append({"kind": "lacks-evidence", "text": f"lacks-evidence: {e['bindings_named']} {e['literals']}", "source": _ref("snapshot.json", f"/edges/{i}")})
        if e["type"] == "contradicts":
            unknowns.append({"kind": "dispute", "text": f"contradiction recorded between {e['bindings_named']}", "source": _ref("snapshot.json", f"/edges/{i}")})
    for i, l in enumerate(snap["evidence_links"]):
        if l["status"] != "admissible":
            unknowns.append({"kind": "contested-evidence", "text": f"{l['evidence_kind']} evidence about {l['subject']} has status '{l['status']}'",
                             "source": _ref("snapshot.json", f"/evidence_links/{i}")})
    unknowns.append({"kind": "data-class", "text": f"the evaluated universe is labelled '{data_class}'; no result here describes the real sky",
                     "source": _ref("snapshot.json", "/universe/data_class")})

    next_evidence: list[dict[str, Any]] = []
    for i, a in enumerate(receipt["selected_actions"]):
        next_evidence.append({"kind": "planned-observation", "text": f"the Astro plan proposes: {a['action']} {a['designation']} ({a['duration_minutes']} min)",
                              "source": _ref("receipt.json", f"/selected_actions/{i}")})
    for i, r in enumerate(receipt["results"]):
        rules = {el["rule"]: (j, el) for j, el in enumerate(r["eligibility"])}
        kind_ok = rules.get("target_kind", (None, {"passed": True}))[1]["passed"]
        if kind_ok and "required_evidence" in rules and not rules["required_evidence"][1]["passed"]:
            j, el = rules["required_evidence"]
            others_pass = all(x["passed"] for x in r["eligibility"] if x["rule"] != "required_evidence")
            tail = "; required_evidence is its only failing eligibility rule" if others_pass else "; other eligibility rules also fail"
            next_evidence.append({"kind": "required-evidence", "text": f"{r['designation']} ({r['kind']}) is a target kind of this Objective but {el['detail']}{tail}",
                                  "source": _ref("receipt.json", f"/results/{i}/eligibility/{j}")})
    for i, e in enumerate(snap["edges"]):
        if e["type"] in ("lacks_evidence", "lacks-evidence"):
            next_evidence.append({"kind": "lacks-evidence", "text": f"ASA records missing evidence {e['literals']} for {e['bindings_named']}", "source": _ref("snapshot.json", f"/edges/{i}")})
    for i, l in enumerate(snap["evidence_links"]):
        if l["status"] == "contested":
            next_evidence.append({"kind": "adjudicate", "text": f"independent {l['evidence_kind']} evidence about {l['subject']} (current record is contested)",
                                  "source": _ref("snapshot.json", f"/evidence_links/{i}")})
    for item in next_evidence:
        item["label"] = "hypothesis"

    explanations = []
    for eid, ex in sorted(receipt["explanations"].items(), key=lambda kv: (kv[1].get("rank") or 99, kv[0])):
        explanations.append({"designation": ex["designation"], "status": ex["status"], "score": ex["score"], "rank": ex["rank"],
                             "why_significant_now": ex["why_significant_now"], "why_not_more": ex["why_not_more"],
                             "label": "hypothesis", "source": _ref("receipt.json", f"/explanations/{eid}")})
    top = [r for r in receipt["results"] if r["status"] == "eligible"]
    es = receipt["eligibility_summary"]
    summary = [
        {"text": f"Objective: “{receipt['objective_name']}” — {objective.get('question')}", "source": _ref("objective.json", "/question")},
        {"text": f"Context: {context.get('label')}", "source": _ref("context.json", "/label")},
        {"text": f"Of {sum(es.values())} entities, {es['eligible']} were eligible, {es['ineligible']} ineligible, {es['indeterminate']} indeterminate.",
         "source": _ref("receipt.json", "/eligibility_summary")},
        {"text": (f"The engine ranks {top[0]['designation']} first (score {top[0]['score']}, a hypothesis)." if top else "No entity was eligible."),
         "source": _ref("receipt.json", "/results/0")},
        {"text": ("Plan: " + "; ".join(f"{a['action']} {a['designation']}" for a in receipt["selected_actions"])) if receipt["selected_actions"] else "Plan: nothing selected.",
         "source": _ref("receipt.json", "/selected_actions")},
        {"text": f"All data in this run are labelled '{data_class}'.", "source": _ref("snapshot.json", "/universe/data_class")},
    ]
    results = [{"designation": r["designation"], "kind": r["kind"], "status": r["status"], "score": r["score"], "rank": r["rank"],
                "failed_rules": [el["detail"] for el in r["eligibility"] if not el["passed"]],
                "label": "hypothesis" if r["status"] == "eligible" else "record",
                "source": _ref("receipt.json", f"/results/{i}")} for i, r in enumerate(receipt["results"])]
    counts = {"established-in-ASA-state": sum(c["label"] == "established-in-ASA-state" for c in claims),
              "hypothesis": sum(c["label"] == "hypothesis" for c in claims)}
    return {
        "view_schema": "asa-astro-app-view-v1", "app_version": APP_VERSION, "run_id": run_id, "label_policy": LABEL_POLICY,
        "pin": pin,
        "snapshot": {"summary": snap["summary"], "universe": snap["universe"],
                     "source": _ref("snapshot.json", "/summary"), "label": "record"},
        "objective": {"objective_id": receipt["objective_id"], "name": receipt["objective_name"], "version": receipt["objective_version"],
                      "question": objective.get("question"), "authority": objective.get("authority"),
                      "weighting_policy_ref": receipt["weighting_policy_ref"], "context_id": receipt["context_id"],
                      "context_label": context.get("label"), "source": _ref("objective.json", "")},
        "receipt": {k: receipt[k] for k in ("receipt_id", "receipt_schema", "issued_at", "issued_at_classification", "astro_commit", "asa_baseline",
                                            "kernel_version", "kernel_digest", "kernel_head", "kernel_seq", "registry_digest", "universe_id",
                                            "universe_data_class", "evaluation_id", "plan_id", "candidate_set_digest", "evidence_digest",
                                            "relationship_digest", "eligibility_summary")} | {
            "receipt_id_verified": run["receipt_id_verified"], "receipt_file_sha256": run["receipt_file_sha256"],
            "source": _ref("receipt.json", ""), "label": "record"},
        "explanation": {"summary": summary, "per_entity": explanations, "label": "hypothesis",
                        "note": "Summary sentences are filled only from the cited fields; per-entity lines are astro.significance.explain output carried in the receipt."},
        "results": results, "claims": claims, "claim_counts": counts,
        "unknowns": unknowns, "next_evidence": next_evidence,
        "compat_shims": run["compat_shims"],
    }


# ---- run --------------------------------------------------------------------------------------
def run_slice(objective_slug: str | None = None) -> dict[str, Any]:
    cfg = pinmod.app_config()
    slug = objective_slug or cfg["default_inputs"]["objective"]
    if not SLUG.match(slug) or slug not in {o["slug"] for o in list_objectives()}:
        raise ValueError(f"unknown objective {slug!r}")
    with _LOCK:
        pin = pinmod.activate()
        from astro.domain import Universe
        from astro.objectives.loaders import load_context, load_objective
        from astro.pipeline import FACET, decide
        from astro.domain.identity import content_id
        from .compat import PinnedAdapter, SHIM_RECORD

        universe_path = ROOT / cfg["default_inputs"]["universe"]
        context_path = ROOT / cfg["default_inputs"]["context"]
        objective_path = ROOT / cfg["objectives_dir"] / f"{slug}.json"
        universe = Universe.load(universe_path)
        objective = load_objective(objective_path)
        context = load_context(context_path, universe)
        adapter = PinnedAdapter.in_memory_registered(FACET, "astro")
        adapter.load_universe(universe)
        decision = decide(universe, objective, context, adapter)   # snapshot → evaluate ONE objective → plan → receipt
        receipt = decision.receipt.to_record()
        body = {k: v for k, v in receipt.items() if k not in ("receipt_id", "issued_at", "issued_at_classification")}
        verified = content_id("RCPT", body) == receipt["receipt_id"]
        from astro_exec.core.canonical_json import canonical_text
        receipt_text = canonical_text(receipt)
        run_id = receipt["receipt_id"]
        snap = _snapshot_detail(decision.snapshot, universe)
        run = {
            "run_schema": "asa-astro-app-run-v1", "app_version": APP_VERSION, "run_id": run_id,
            "slice": ["pin", "snapshot", "objective", "receipt"],
            "inputs": {"universe": str(universe_path.relative_to(ROOT)), "context": str(context_path.relative_to(ROOT)),
                       "objective": str(objective_path.relative_to(ROOT)),
                       "universe_sha256": _sha(universe_path.read_bytes()), "context_sha256": _sha(context_path.read_bytes()),
                       "objective_sha256": _sha(objective_path.read_bytes())},
            "engine_call": "astro.pipeline.decide(universe, objective, context, adapter)",
            "compat_shims": [SHIM_RECORD],
            "receipt_id_verified": verified,
            "receipt_id_verification": "content_id('RCPT', receipt body without receipt_id/issued_at) recomputed by the app",
            "receipt_file_sha256": _sha(receipt_text),
            "self_acceptance": "NO",
        }
        target = runs_dir() / run_id
        invocation = {"issued_at": receipt["issued_at"], "receipt_id": run_id, "receipt_file_sha256": run["receipt_file_sha256"],
                      "recorded_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
        if target.exists():
            prior = json.loads((target / "receipt.json").read_text(encoding="utf-8"))
            invocation["reproduced_identical_receipt_id"] = prior["receipt_id"] == run_id
            with (target / "invocations.jsonl").open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(invocation, sort_keys=True) + "\n")
            view = json.loads((target / "view.json").read_text(encoding="utf-8"))
            view["reproduced"] = True
            return view
        runs_dir().mkdir(parents=True, exist_ok=True)
        tmp = Path(tempfile.mkdtemp(prefix=".run-", dir=runs_dir()))
        try:
            files = {
                "pin.json": _canon(pin), "snapshot.json": _canon(snap), "objective.json": _canon(objective.to_record()),
                "context.json": _canon(context.to_record()), "evaluation.json": _canon(decision.evaluation.to_record()),
                "plan.json": _canon(decision.plan.to_record()), "receipt.json": receipt_text + "\n",
                "receipt.sha256": run["receipt_file_sha256"] + "  receipt.json\n",
            }
            view = build_view(run_id, pin, snap, objective.to_record(), context.to_record(), receipt, run)
            files["view.json"] = _canon(view)
            run["artifacts"] = {name: _sha(text) for name, text in sorted(files.items())}
            files["run.json"] = _canon(run)
            for name, text in files.items():
                (tmp / name).write_text(text, encoding="utf-8")
            (tmp / "invocations.jsonl").write_text(json.dumps(invocation | {"reproduced_identical_receipt_id": None}, sort_keys=True) + "\n", encoding="utf-8")
            tmp.replace(target)
        except Exception:
            shutil.rmtree(tmp, ignore_errors=True)
            raise
        view["reproduced"] = False
        return view


def list_runs(query: str | None = None) -> list[dict[str, Any]]:
    out = []
    if not runs_dir().exists():
        return out
    q = (query or "").strip().lower()
    for d in sorted(runs_dir().iterdir()):
        if not RUN_ID.match(d.name) or not (d / "view.json").exists():
            continue
        view = json.loads((d / "view.json").read_text(encoding="utf-8"))
        item = {"run_id": d.name, "objective": view["objective"]["name"], "context": view["objective"]["context_label"],
                "kernel_digest": view["receipt"]["kernel_digest"], "asa_baseline": view["receipt"]["asa_baseline"],
                "issued_at": view["receipt"]["issued_at"], "data_class": view["receipt"]["universe_data_class"],
                "top": [c["text"] for c in view["claims"] if c["group"] == "objective-result"][:1]}
        haystack = json.dumps(item).lower()
        if not q or q in haystack:
            out.append(item)
    return sorted(out, key=lambda i: i["issued_at"], reverse=True)


def load_view(run_id: str) -> dict[str, Any] | None:
    if not RUN_ID.match(run_id):
        return None
    path = runs_dir() / run_id / "view.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def artifact_path(run_id: str, name: str) -> Path | None:
    if not RUN_ID.match(run_id) or name not in ARTIFACTS:
        return None
    path = runs_dir() / run_id / name
    return path if path.exists() else None
