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
from .observation_honesty import project_observation_evidence, project_action_residuals

ROOT = pinmod.ROOT
_LOCK = threading.Lock()
SLUG = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,80}$")
# Plain receipt dir (JSON-only / no-upload) OR content-keyed upload run dir.
# Upload runs: RCPT-<64>__src-<source-sha256>__meta-<metadata-sha256|none>
RUN_ID = re.compile(
    r"^RCPT-[0-9a-f]{64}"
    r"(?:__src-[0-9a-f]{64}__meta-(?:[0-9a-f]{64}|none))?$"
)
RECEIPT_ID = re.compile(r"^RCPT-[0-9a-f]{64}$")
ARTIFACTS = ("pin.json", "snapshot.json", "objective.json", "context.json", "evaluation.json", "plan.json",
             "receipt.json", "receipt.sha256", "run.json", "view.json", "uploaded_source.json",
             "observation_wcs.json", "observation_localisations.json", "observation_crossmatches.json", "observed_vs_expected.json", "bridge_manifest.json")
CORE_ARTIFACTS = ("pin.json", "snapshot.json", "objective.json", "context.json", "evaluation.json", "plan.json",
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



def _metadata_sha256(metadata_bytes: bytes | None) -> str:
    """Stable metadata content key; 'none' when absent (matches observation-bundle naming)."""
    return _sha(metadata_bytes) if metadata_bytes else "none"


def run_storage_key(
    receipt_id: str,
    *,
    uploaded_source: dict | None = None,
    metadata_bytes: bytes | None = None,
) -> str:
    """Unique, append-only run directory name.

    No upload → receipt_id alone (preserves prior JSON-only behaviour).
    Upload → (receipt_id, source sha256, metadata sha256) so distinct uploads never
    share a directory even when the Objective receipt id collides (R-INT-01).
    """
    if not RECEIPT_ID.match(receipt_id):
        raise ValueError(f"invalid receipt_id {receipt_id!r}")
    if uploaded_source is None:
        return receipt_id
    source_sha = uploaded_source.get("sha256")
    if not isinstance(source_sha, str) or not re.fullmatch(r"[0-9a-f]{64}", source_sha):
        raise ValueError("uploaded_source.sha256 must be a 64-hex digest")
    meta_sha = _metadata_sha256(metadata_bytes)
    return f"{receipt_id}__src-{source_sha}__meta-{meta_sha}"

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



def _uploaded_source_view(uploaded_source: dict | None) -> dict[str, Any]:
    """Honesty block for a preserved upload. Absent → present=false (JSON-only run)."""
    if not uploaded_source:
        return {
            "present": False,
            "note": "No observation source was uploaded for this run.",
        }
    obs = uploaded_source.get("process_observation") or {}
    return {
        "present": True,
        "original_filename": uploaded_source.get("original_filename"),
        "sha256": uploaded_source.get("sha256"),
        "byte_size": uploaded_source.get("byte_size"),
        "media_type": uploaded_source.get("media_type"),
        "stored_path": uploaded_source.get("stored_path"),
        "registration_policy": uploaded_source.get("registration_policy"),
        "integrity_status": uploaded_source.get("integrity_status"),
        "processable_by_process_observation": uploaded_source.get("processable_by_process_observation"),
        "store_only": uploaded_source.get("store_only"),
        "process_observation_invoked": bool(obs.get("invoked")),
        "process_observation_reason": obs.get("reason"),
        "observation_bundle_path": obs.get("bundle_path"),
        "bundle_source_sha256_verified": obs.get("bundle_source_sha256_verified"),
        "objective_bridge": obs.get("objective_bridge") or (
            "absent — upload preserved; primary Objective path requires "
            "asa_astro.bridge.observation_bundle_to_objective (G-SIG-1)."
        ),
        "label": "record",
        "source": _ref("uploaded_source.json", ""),
        "pointers": {
            "original_filename": _ref("uploaded_source.json", "/original_filename"),
            "sha256": _ref("uploaded_source.json", "/sha256"),
            "stored_path": _ref("uploaded_source.json", "/stored_path"),
        },
    }


def build_view(run_id: str, pin: dict, snap: dict, objective: dict, context: dict, receipt: dict, run: dict,
               observation_wcs: dict | None = None,
               observation_localisations: list | None = None,
               observation_crossmatches: list | None = None,
               uploaded_source: dict | None = None,
               observed_vs_expected: dict | None = None,
               observation_identity: dict | None = None) -> dict[str, Any]:
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
    bridge_path = (run.get("universe_provenance") or {}).get("bridge_path")
    if uploaded_source and bridge_path not in (
        "observation_bundle_to_objective",
        "sky_to_objective_primary",
    ):
        unknowns.append({
            "kind": "observation-objective-bridge",
            "text": (
                "uploaded observation source is preserved"
                + (f" (sha256={uploaded_source.get('sha256')})" if uploaded_source.get("sha256") else "")
                + "; observation graph was not mapped into this Objective universe "
                "(see GAPS G-SIG-1)"
            ),
            "source": _ref("uploaded_source.json", "/sha256"),
        })

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
        "uploaded_source": _uploaded_source_view(uploaded_source),
        # F-SCI-03: present-only pipeline observation_identity (never invent; never = Objective RCPT).
        "observation_identity": observation_identity if isinstance(observation_identity, dict) else None,
        "observation_evidence": project_observation_evidence(
            wcs=observation_wcs,
            localisations=observation_localisations,
            crossmatches=observation_crossmatches,
        ),
        "observed_vs_expected": project_action_residuals(observed_vs_expected),
        "universe_provenance": run.get("universe_provenance") or {
            "bridge_path": "synthetic_demo_slice1",
            "data_class": data_class,
            "universe_id": snap["universe"]["universe_id"],
            "label": "synthetic/demo",
        },
        "compat_shims": run["compat_shims"],
    }


# ---- run --------------------------------------------------------------------------------------
def _attach_upload_artifacts(
    target: Path,
    *,
    pin: dict,
    snap: dict,
    objective_record: dict,
    context_record: dict,
    receipt: dict,
    run: dict,
    uploaded_source: dict | None,
    observation_consume: dict | None,
) -> dict[str, Any]:
    """Write upload / observation honesty artifacts and rebuild view.json in place.

    Writes only artifacts this consume produced: absent WCS / empty crossmatches are
    omitted (never left over from a sibling upload). Callers must pass a fresh target
    directory — existing run dirs are append-only and must not be rewritten (R-INT-01).
    """
    obs_wcs = None
    obs_locs = None
    obs_xm = None
    source_record = None
    if uploaded_source is not None:
        source_record = dict(uploaded_source)
        if observation_consume is not None:
            source_record["process_observation"] = {
                k: observation_consume.get(k)
                for k in (
                    "invoked", "reason", "bundle_path", "bundle_source_sha256_verified",
                    "sky_localisation_count", "wcs_present", "catalogue_crossmatch_count",
                    "coordinates_invented", "source_image_mutated", "objective_bridge",
                    "metadata_path", "summary", "observation_identity",
                )
            }
        (target / "uploaded_source.json").write_text(_canon(source_record), encoding="utf-8")
        if observation_consume and observation_consume.get("invoked"):
            obs_wcs = observation_consume.get("wcs")
            obs_locs = observation_consume.get("localisations") or []
            obs_xm = observation_consume.get("crossmatches") or []
            if obs_wcs is not None:
                (target / "observation_wcs.json").write_text(_canon(obs_wcs), encoding="utf-8")
            (target / "observation_localisations.json").write_text(_canon({"localisations": obs_locs}), encoding="utf-8")
            if obs_xm:
                (target / "observation_crossmatches.json").write_text(_canon({"crossmatches": obs_xm}), encoding="utf-8")
    ove = None
    if observation_consume and isinstance(observation_consume.get("observed_vs_expected"), dict):
        ove = observation_consume["observed_vs_expected"]
        if ove.get("present"):
            (target / "observed_vs_expected.json").write_text(_canon(ove), encoding="utf-8")
    obs_identity = None
    if observation_consume and isinstance(observation_consume.get("observation_identity"), dict):
        obs_identity = observation_consume["observation_identity"]
    view = build_view(
        run["run_id"], pin, snap, objective_record, context_record, receipt, run,
        observation_wcs=obs_wcs,
        observation_localisations=obs_locs,
        observation_crossmatches=obs_xm,
        uploaded_source=source_record,
        observed_vs_expected=ove,
        observation_identity=obs_identity,
    )
    (target / "view.json").write_text(_canon(view), encoding="utf-8")
    # Refresh run.json artifact digests for any files now present.
    artifacts = {}
    for name in ARTIFACTS:
        p = target / name
        if p.is_file():
            artifacts[name] = _sha(p.read_bytes())
    run = dict(run)
    run["artifacts"] = artifacts
    if source_record is not None:
        run["uploaded_source"] = {
            "original_filename": source_record.get("original_filename"),
            "sha256": source_record.get("sha256"),
            "stored_path": source_record.get("stored_path"),
            "integrity_status": source_record.get("integrity_status"),
            "process_observation_invoked": bool((source_record.get("process_observation") or {}).get("invoked")),
        }
    (target / "run.json").write_text(_canon(run), encoding="utf-8")
    return view


def run_slice(
    objective_slug: str | None = None,
    *,
    upload_bytes: bytes | None = None,
    upload_filename: str | None = None,
    upload_media_type: str | None = None,
    metadata_bytes: bytes | None = None,
    demo: bool = False,
) -> dict[str, Any]:
    """Pin → snapshot → one Objective → receipt.

    Paths (R1 / G-SIG-1):
    - **Upload + localised rows** → primary Objective via
      ``asa_astro.bridge.observation_bundle_to_objective`` (never silent ``slice1.json``).
    - **Upload + bridge fail-closed** → raise; no silent synthetic substitute.
    - **No-upload / explicit demo** → ``data/universe/slice1.json``, labelled synthetic/demo.
    """
    cfg = pinmod.app_config()
    slug = objective_slug or cfg["default_inputs"]["objective"]
    if not SLUG.match(slug) or slug not in {o["slug"] for o in list_objectives()}:
        raise ValueError(f"unknown objective {slug!r}")

    uploaded_source = None
    observation_consume = None
    if upload_bytes is not None:
        from . import upload as uploadmod
        uploaded_source = uploadmod.store_bytes(
            upload_bytes,
            original_filename=upload_filename,
            media_type=upload_media_type,
        )
        observation_consume = uploadmod.run_process_observation(
            uploaded_source, metadata_bytes=metadata_bytes,
        )

    with _LOCK:
        pin = pinmod.activate()
        from astro.domain import Universe
        from astro.objectives.loaders import load_context, load_objective
        from astro.pipeline import FACET, decide, open_or_bootstrap
        from astro.domain.identity import content_id
        from asa_astro.bridge import SkyToObjectiveBridgeError, observation_bundle_to_objective
        from .compat import PinnedAdapter, SHIM_RECORD

        universe_path = ROOT / cfg["default_inputs"]["universe"]
        context_path = ROOT / cfg["default_inputs"]["context"]
        objective_path = ROOT / cfg["objectives_dir"] / f"{slug}.json"

        bridge_result = None
        bridge_out: Path | None = None

        if uploaded_source is not None and not demo:
            if not observation_consume or not observation_consume.get("invoked"):
                raise ValueError(
                    "Upload did not yield a process_observation bundle; refusing silent "
                    "slice1.json substitute (sky→Objective fail-closed / honesty)."
                )
            bundle_rel = observation_consume.get("bundle_path")
            if not bundle_rel:
                raise ValueError(
                    "process_observation produced no bundle_path; refusing silent "
                    "slice1.json substitute."
                )
            bundle_dir = data_dir() / bundle_rel
            if not bundle_dir.is_dir():
                raise ValueError(
                    f"observation bundle missing at {bundle_rel}; refusing silent slice1.json."
                )
            site = None
            instrument = None
            if metadata_bytes:
                try:
                    meta_obj = json.loads(metadata_bytes.decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError):
                    meta_obj = None
                if isinstance(meta_obj, dict):
                    if isinstance(meta_obj.get("site"), dict):
                        site = meta_obj["site"]
                    if isinstance(meta_obj.get("instrument"), dict):
                        instrument = meta_obj["instrument"]
                    elif isinstance(meta_obj.get("instrument"), str):
                        instrument = {"designation": meta_obj["instrument"]}
            runs_dir().mkdir(parents=True, exist_ok=True)
            bridge_staging = Path(tempfile.mkdtemp(prefix=".bridge-", dir=runs_dir()))
            try:
                bridge_out = bridge_staging / "out"
                bridge_result = observation_bundle_to_objective(
                    bundle_dir,
                    bridge_out,
                    site=site,
                    instrument=instrument,
                    allow_synthetic_demo_site=False,
                    commit="app-r1-observation-bundle",
                )
            except SkyToObjectiveBridgeError as exc:
                shutil.rmtree(bridge_staging, ignore_errors=True)
                raise ValueError(
                    f"sky→Objective bridge fail-closed (no silent slice1): {exc}"
                ) from exc
            except Exception:
                shutil.rmtree(bridge_staging, ignore_errors=True)
                raise

            universe = Universe.load(bridge_out / "universe.json")
            objective = load_objective(bridge_out / "objective.json")
            context = load_context(bridge_out / "context.json", universe)
            adapter = open_or_bootstrap(universe)
            decision_snapshot = adapter.snapshot()
            evaluation_record = json.loads((bridge_out / "evaluation.json").read_text(encoding="utf-8"))
            plan_record = json.loads((bridge_out / "plan.json").read_text(encoding="utf-8"))
            receipt = json.loads((bridge_out / "receipt.json").read_text(encoding="utf-8"))

            class _Rec:
                def __init__(self, record):
                    self._record = record

                def to_record(self):
                    return self._record

            decision = type("DecisionShim", (), {})()
            decision.snapshot = decision_snapshot
            decision.evaluation = _Rec(evaluation_record)
            decision.plan = _Rec(plan_record)

            observation_consume = dict(observation_consume)
            observation_consume["objective_bridge"] = (
                "primary — asa_astro.bridge.observation_bundle_to_objective "
                f"(universe_id={bridge_result.get('universe_id')}; "
                f"slice1_substituted={bridge_result.get('slice1_substituted')})"
            )
            if bridge_result.get("observation_identity") and not observation_consume.get(
                "observation_identity"
            ):
                observation_consume["observation_identity"] = bridge_result["observation_identity"]
            engine_call = (
                "asa_astro.bridge.observation_bundle_to_objective("
                "bundle_directory, out_directory, allow_synthetic_demo_site=False)"
            )
            slice_steps = [
                "pin",
                "upload",
                "process_observation",
                "observation_bundle_to_objective",
                "receipt",
            ]
            inputs = {
                "universe": f"bridge:{bridge_result.get('universe_id')}",
                "context": f"bridge:{bridge_result.get('context_id')}",
                "objective": f"bridge:{bridge_result.get('objective_id')}",
                "universe_sha256": _sha((bridge_out / "universe.json").read_bytes()),
                "context_sha256": _sha((bridge_out / "context.json").read_bytes()),
                "objective_sha256": _sha((bridge_out / "objective.json").read_bytes()),
                "observation_bundle": bundle_rel,
                "bridge_api": "asa_astro.bridge.observation_bundle_to_objective",
            }
            oid = bridge_result.get("observation_identity") or observation_consume.get(
                "observation_identity"
            )
            universe_provenance = {
                "bridge_path": "observation_bundle_to_objective",
                "api": "asa_astro.bridge.observation_bundle_to_objective",
                "universe_id": bridge_result.get("universe_id") or universe.universe_id,
                "data_class": universe.data_class,
                "slice1_substituted": bool(bridge_result.get("slice1_substituted")),
                "site_standing": bridge_result.get("site_standing"),
                "site_demo_only": bridge_result.get("site_demo_only"),
                "source_sha256": (
                    (oid or {}).get("source_sha256")
                    if isinstance(oid, dict)
                    else uploaded_source.get("sha256")
                ),
                "observation_claim_id": (
                    (oid or {}).get("observation_claim_id") if isinstance(oid, dict) else None
                ),
                "observation_claim_digest": (
                    (oid or {}).get("observation_claim_digest") if isinstance(oid, dict) else None
                ),
                "label": "observation+bridge",
            }
            shim_note = dict(SHIM_RECORD)
            shim_note["applied_on_this_run"] = False
            shim_note["path_note"] = (
                "primary bridge uses tip open_or_bootstrap inside "
                "observation_bundle_to_objective; app PinnedAdapter shim not applied on this path"
            )
            compat_shims = [shim_note]
        else:
            universe = Universe.load(universe_path)
            objective = load_objective(objective_path)
            context = load_context(context_path, universe)
            adapter = PinnedAdapter.in_memory_registered(FACET, "astro")
            adapter.load_universe(universe)
            decision = decide(universe, objective, context, adapter)
            receipt = decision.receipt.to_record()
            engine_call = "astro.pipeline.decide(universe, objective, context, adapter)"
            slice_steps = ["pin", "snapshot", "objective", "receipt"]
            if demo and uploaded_source is not None:
                slice_steps = ["pin", "upload", "demo_slice1", "objective", "receipt"]
            inputs = {
                "universe": str(universe_path.relative_to(ROOT)),
                "context": str(context_path.relative_to(ROOT)),
                "objective": str(objective_path.relative_to(ROOT)),
                "universe_sha256": _sha(universe_path.read_bytes()),
                "context_sha256": _sha(context_path.read_bytes()),
                "objective_sha256": _sha(objective_path.read_bytes()),
            }
            universe_provenance = {
                "bridge_path": "synthetic_demo_slice1",
                "universe_id": universe.universe_id,
                "data_class": universe.data_class,
                "slice1_substituted": False,
                "source_path": str(universe_path.relative_to(ROOT)),
                "label": "synthetic/demo",
                "demo": bool(demo) or uploaded_source is None,
            }
            compat_shims = [SHIM_RECORD]
            if observation_consume is not None and demo:
                observation_consume = dict(observation_consume)
                observation_consume["objective_bridge"] = (
                    "demo — explicit demo=True; primary receipt uses synthetic slice1.json "
                    "(labelled synthetic/demo; not a silent upload substitute)"
                )

        body = {
            k: v
            for k, v in receipt.items()
            if k not in ("receipt_id", "issued_at", "issued_at_classification")
        }
        verified = content_id("RCPT", body) == receipt["receipt_id"]
        from astro_exec.core.canonical_json import canonical_text

        receipt_text = canonical_text(receipt)
        receipt_id = receipt["receipt_id"]
        run_id = run_storage_key(
            receipt_id,
            uploaded_source=uploaded_source,
            metadata_bytes=metadata_bytes,
        )
        snap = _snapshot_detail(decision.snapshot, universe)
        run = {
            "run_schema": "asa-astro-app-run-v1",
            "app_version": APP_VERSION,
            "run_id": run_id,
            "receipt_id": receipt_id,
            "slice": slice_steps,
            "inputs": inputs,
            "engine_call": engine_call,
            "compat_shims": compat_shims,
            "universe_provenance": universe_provenance,
            "receipt_id_verified": verified,
            "receipt_id_verification": (
                "content_id('RCPT', receipt body without receipt_id/issued_at) recomputed by the app"
            ),
            "receipt_file_sha256": _sha(receipt_text),
            "self_acceptance": "NO",
        }
        if uploaded_source is not None:
            run["upload_key"] = {
                "source_sha256": uploaded_source["sha256"],
                "metadata_sha256": _metadata_sha256(metadata_bytes),
                "binding": (
                    "run directory keyed by (receipt_id, source sha256, metadata sha256); "
                    "never rewritten"
                ),
            }
        target = runs_dir() / run_id
        invocation = {
            "issued_at": receipt["issued_at"],
            "receipt_id": receipt_id,
            "run_id": run_id,
            "receipt_file_sha256": run["receipt_file_sha256"],
            "recorded_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "bridge_path": universe_provenance.get("bridge_path"),
        }
        if uploaded_source is not None:
            invocation["uploaded_source_sha256"] = uploaded_source["sha256"]
            invocation["uploaded_original_filename"] = uploaded_source["original_filename"]
            invocation["metadata_sha256"] = _metadata_sha256(metadata_bytes)
            if observation_consume is not None:
                invocation["process_observation_invoked"] = bool(observation_consume.get("invoked"))
                invocation["observation_bundle_path"] = observation_consume.get("bundle_path")

        if target.exists():
            prior = json.loads((target / "receipt.json").read_text(encoding="utf-8"))
            invocation["reproduced_identical_receipt_id"] = prior["receipt_id"] == receipt_id
            invocation["run_dir_mutated"] = False
            with (target / "invocations.jsonl").open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(invocation, sort_keys=True) + "\n")
            view = json.loads((target / "view.json").read_text(encoding="utf-8"))
            view["reproduced"] = True
            if bridge_out is not None:
                shutil.rmtree(bridge_out.parent, ignore_errors=True)
            return view

        runs_dir().mkdir(parents=True, exist_ok=True)
        tmp = Path(tempfile.mkdtemp(prefix=".run-", dir=runs_dir()))
        try:
            files = {
                "pin.json": _canon(pin),
                "snapshot.json": _canon(snap),
                "objective.json": _canon(objective.to_record()),
                "context.json": _canon(context.to_record()),
                "evaluation.json": _canon(decision.evaluation.to_record()),
                "plan.json": _canon(decision.plan.to_record()),
                "receipt.json": receipt_text + "\n",
                "receipt.sha256": run["receipt_file_sha256"] + "  receipt.json\n",
            }
            for name, text_body in files.items():
                (tmp / name).write_text(text_body, encoding="utf-8")
            if bridge_out is not None and (bridge_out / "bridge_manifest.json").is_file():
                (tmp / "bridge_manifest.json").write_text(
                    (bridge_out / "bridge_manifest.json").read_text(encoding="utf-8"),
                    encoding="utf-8",
                )
            (tmp / "invocations.jsonl").write_text(
                json.dumps(
                    invocation
                    | {"reproduced_identical_receipt_id": None, "run_dir_mutated": False},
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
            )
            (tmp / "run.json").write_text(_canon(run), encoding="utf-8")
            view = _attach_upload_artifacts(
                tmp,
                pin=pin,
                snap=snap,
                objective_record=objective.to_record(),
                context_record=context.to_record(),
                receipt=receipt,
                run=run,
                uploaded_source=uploaded_source,
                observation_consume=observation_consume,
            )
            tmp.replace(target)
        except Exception:
            shutil.rmtree(tmp, ignore_errors=True)
            raise
        finally:
            if bridge_out is not None:
                shutil.rmtree(bridge_out.parent, ignore_errors=True)
        view["reproduced"] = False
        return view

def parse_run_storage_key(run_id: str) -> dict[str, Any]:
    """Split keyed upload run_id into receipt_id + src/meta discriminators (U-RUN-LIST-01)."""
    m = re.fullmatch(
        r"(RCPT-[0-9a-f]{64})(?:__src-([0-9a-f]{64})__meta-([0-9a-f]{64}|none))?",
        run_id,
    )
    if not m:
        return {"receipt_id": None, "source_sha256": None, "meta_sha256": None, "keyed": False}
    return {
        "receipt_id": m.group(1),
        "source_sha256": m.group(2),
        "meta_sha256": m.group(3),
        "keyed": m.group(2) is not None,
    }


def _list_run_discriminators(run_id: str, view: dict[str, Any]) -> dict[str, Any]:
    """Human + content-addressed discriminators for Runs list (U-RUN-LIST-01).

    F-SCI-03: science observation-claim identity is observation_identity (when present),
    never bare Objective RCPT and never app-only run_id. run_id remains the storage key.
    """
    parts = parse_run_storage_key(run_id)
    us = view.get("uploaded_source") or {}
    oe = view.get("observation_evidence") or {}
    oid = view.get("observation_identity") if isinstance(view.get("observation_identity"), dict) else None
    receipt_id = (view.get("receipt") or {}).get("receipt_id") or parts["receipt_id"] or run_id
    present = bool(us.get("present"))
    src_sha = None
    if oid and isinstance(oid.get("source_sha256"), str):
        src_sha = oid["source_sha256"]
    elif present:
        src_sha = us.get("sha256")
    else:
        src_sha = parts["source_sha256"]
    meta_sha = None
    if oid and "metadata_sha256" in oid:
        meta_sha = oid.get("metadata_sha256")
    else:
        meta_sha = parts["meta_sha256"]
    # Primary upload display id: observation_claim_id / observation_claim_digest
    # (F-SCI-03 / HA-F-2 tip fields); legacy "digest" accepted for older bundles.
    # Never bare Objective RCPT.
    obs_claim = None
    if oid:
        obs_claim = (
            oid.get("observation_claim_id")
            or oid.get("observation_claim_digest")
            or oid.get("digest")
        )
    if obs_claim is None and parts["keyed"]:
        obs_claim = None  # no science claim id yet; UI must not imply bare RCPT
    return {
        "receipt_id": receipt_id,
        "original_filename": us.get("original_filename") if present else None,
        "source_sha256": src_sha,
        "source_sha256_short": (src_sha[:12] if isinstance(src_sha, str) else None),
        "meta_sha256": meta_sha,
        "meta_sha256_short": (
            None if meta_sha in (None, "none")
            else (meta_sha[:12] if isinstance(meta_sha, str) and meta_sha != "none" else None)
        ),
        "keyed_upload": bool(parts["keyed"]),
        "wcs_declared": bool(oe.get("wcs")),
        "observation_identity": oid,
        "observation_claim_key": obs_claim,
    }


def list_runs(query: str | None = None) -> list[dict[str, Any]]:
    out = []
    if not runs_dir().exists():
        return out
    q = (query or "").strip().lower()
    for d in sorted(runs_dir().iterdir()):
        if not RUN_ID.match(d.name) or not (d / "view.json").exists():
            continue
        view = json.loads((d / "view.json").read_text(encoding="utf-8"))
        disc = _list_run_discriminators(d.name, view)
        item = {"run_id": d.name, "objective": view["objective"]["name"], "context": view["objective"]["context_label"],
                "kernel_digest": view["receipt"]["kernel_digest"], "asa_baseline": view["receipt"]["asa_baseline"],
                "issued_at": view["receipt"]["issued_at"], "data_class": view["receipt"]["universe_data_class"],
                "top": [c["text"] for c in view["claims"] if c["group"] == "objective-result"][:1],
                **disc}
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
