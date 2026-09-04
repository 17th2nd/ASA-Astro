"""Pre-registration manifest for ASTRO-REAL-DATA-EXP-0001.

``freeze_manifest`` is called once, after the dataset is frozen and before any evaluation is run. It records
everything the experiment depends on and everything that may not change afterwards. Its sha256 is written next to
it; ``verify_manifest`` re-checks it and the runner refuses to run against a changed manifest.
"""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
from pathlib import Path
from typing import Any

from astro import ASTRO_VERSION
from astro.asa.locator import asa_baseline_sha, kernel_version_record
from astro.objectives import ObservingContext
from astro.objectives.loaders import load_objective
from astro.pipeline import FACET, ROOT
from astro_exec.core.hashing import sha256_file
from . import EXP_ID, HASH_SALT
from .dataset import DATASET_DIR, EXP_DIR, GRADE, MIN_SAMPLE, PRIMARY_SAMPLE_SIZE, load_selection

MANIFEST_PATH = EXP_DIR / f"{EXP_ID}-MANIFEST.json"
OBJECTIVE_PATH = EXP_DIR / "objective-ephemeris-maintenance.json"
CONTEXT_PATH = EXP_DIR / "context-ephemeris-maintenance-2029.json"
BOOTSTRAP_SEED = 20260904
BOOTSTRAP_RESAMPLES = 2000
RANDOM_BASELINE_SEED = 20260904
PAGERANK_DAMPING = 0.85
PAGERANK_ITERATIONS = 200
MARGIN = 0.10
TOPOLOGY_LIMIT = 0.80
NDCG_K = 25
PRECISION_K = 25


def declare_context() -> ObservingContext:
    r = json.loads(CONTEXT_PATH.read_text(encoding="utf-8"))
    return ObservingContext.declare(label=r["label"], as_of=r["as_of"], window_start=r["window_start"], window_end=r["window_end"],
                                    site_id=None, instrument_id=None, constraints=r.get("constraints") or {}, anchor_targets=())


def _git(*args: str) -> str:
    try:
        return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def build_manifest() -> dict[str, Any]:
    sel = load_selection()
    prov = json.loads((DATASET_DIR / "PROVENANCE.json").read_text(encoding="utf-8"))
    objective = load_objective(OBJECTIVE_PATH)
    context = declare_context()
    kv = kernel_version_record()
    return {
        "experiment": EXP_ID,
        "manifest_schema": "astro-real-data-exp-manifest-v1",
        "status": "PRE-REGISTERED; frozen before the first evaluation run",
        "authority": "CLAUDE ASTRO PROGRAMME — REAL-DATA VALIDATION 001 (founder brief, 2026-09-04). Engineering value evaluation of the Astro engine. Not an execution of ASTRO-EXP-0001; no ASTRO-CLM-* claim is tested; evidence level stays EH-0.",
        "research_question": (
            "Under the Context 'transit-ephemeris maintenance in 2029', does the Astro engine's ranking of candidate host stars, computed from "
            "NASA Exoplanet Archive composite ephemerides, Gaia DR3 astrometry and ASA relational state, agree with the ExoClock project's "
            "independently assigned ephemeris priority better than a brightness baseline, a tabulated period-uncertainty baseline, and "
            "graph-topology baselines (degree, PageRank) over the same ASA relational state?"),
        "dataset": {
            "record": "ASTRO-REAL-DATA-EXP-0001-DATASET-RECORD.md",
            "sources": {k: {kk: v.get(kk) for kk in ("role", "title", "url", "release", "licence", "retrieved_at", "sha256", "bytes")} | ({"files": v["files"]} if "files" in v else {})
                        for k, v in prov["sources"].items()},
            "frozen_extract": sel["input_files"],
            "separation": {"astro_input": ["input_pscomppars_rows.csv", "input_gaia_rows.csv"], "reference_truth": ["reference_exoclock_priority.json"], "leakage_check": ["leakage_reflinks.csv"]},
        },
        "candidates": {
            "rules": [
                "1. Planet present in the ExoClock database at retrieval with priority in {alert, high, medium, low}.",
                "2. Exact name match to an archive pl_name after removing spaces and hyphens and case-folding; unmatched names listed.",
                "3. Archive row has tran_flag = 1, pl_orbper, pl_tranmid, and both pl_orbpererr1 and pl_tranmiderr1; rows lacking either uncertainty are the missing-evidence adversarial set.",
                "4. The host has exactly one transiting planet in the archive snapshot and exactly one ExoClock entry (unit of analysis = host star).",
                "5. Leakage exclusion: either archive ephemeris reference link cites an ExoClock publication (refstr contains KOKORI), or the live reference-link row's ephemeris values differ from the 2026-09-02 snapshot.",
                f"6. Primary sample: the first {PRIMARY_SAMPLE_SIZE} of the remaining pool ordered by SHA-256('{HASH_SALT} | <pl_name>').",
            ],
            "hash_salt": HASH_SALT, "primary_sample_size": PRIMARY_SAMPLE_SIZE, "minimum_sample": MIN_SAMPLE,
            "counts": sel["counts"], "primary": sel["primary"], "candidates_json_sha256": sha256_file(DATASET_DIR / "candidates.json"),
            "secondary_analyses": ["full remaining pool (non-decisive)", "pool plus leakage-flagged planets with the flag reported (non-decisive)"],
        },
        "context": {"declaration_file": CONTEXT_PATH.name, "context_id": context.context_id, "record": context.to_record(),
                    "note": "Site-independent: ExoClock priority does not depend on an observatory. The Context epoch is the ExoClock definition epoch."},
        "objective": {"declaration_file": OBJECTIVE_PATH.name, "objective_id": objective.objective_id, "weighting_policy_ref": objective.weighting_policy_ref,
                      "record": objective.to_record(), "feature_code_changed": False,
                      "note": "Declared from the existing feature library only. Weights, params, policies and thresholds are frozen here and never changed."},
        "relationship_types_in_scope": {"hosts": "planet <-> host, supported by archive ephemeris/period evidence -> endorsed; without evidence -> unevaluated (excluded by the objective)",
                                        "measures": "per-quantity claims (Teff, distance, per-planet period) from each source, supported by their evidence",
                                        "contradicts": "asa.core/contradicts between claims disagreeing beyond tolerance (Teff 7%, distance 15%, period 1%)",
                                        "lacks_evidence": "declared expectations unmet (transiting hosts: spectrum, time_series, ... )",
                                        "near": "geometry-derived angular neighbours among universe entities, with separation evidence"},
        "standing_inputs": "ASA relational state as read by RelationalSnapshot from an in-memory kernel at the pinned baseline: registered UROs, canonical-perspective stance (endorsed / unevaluated), supports links, evidence-of links, contradicts meta-claims. No Standing/centrality field exists in this engine; stance gating is the equivalent.",
        "uncertainty_treatment": "The archive's 1-sigma upper errors pl_orbpererr1 and pl_tranmiderr1 enter the ephemeris record as period_days / epoch_days uncertainties; ephemeris_drift propagates them to the Context epoch and normalises by the tabulated (or assumed 2.0 h) transit duration, clipping at 1.0; sigma_P/P > 0.01 is treated as an undetermined period (feature unavailable). Missing required feature -> status indeterminate (abstain), never scored.",
        "asa": {"baseline_sha": asa_baseline_sha(), "kernel_version": kv["kernel"], "kernel_status": kv["status"], "registry_facet": str(FACET.relative_to(ROOT)), "registry_facet_sha256": sha256_file(FACET)},
        "universe_construction": "parse_exoplanets(input_pscomppars_rows.csv) + parse_gaia_hosts(input_gaia_rows.csv) via the unchanged catalogue parsers; merged with merge_fragments; knowledge frontier derived with derive_frontier(tiles=False) at the Context epoch (gaps, geometry, claims, contradictions); loaded into an in-memory kernel with load_frontier. Universe label 'ASTRO-REAL-DATA-EXP-0001', data_class real.",
        "baselines": {
            "brightness": "host magnitude_v (archive sy_vmag), brighter first; no value -> unranked",
            "sigma_period": "tabulated period uncertainty pl_orbpererr1 (days) as carried on the ephemeris record, larger first",
            "degree": "number of registered relational edges binding the host in the ASA snapshot plus its evidence-of links, larger first",
            "pagerank": f"PageRank (damping {PAGERANK_DAMPING}, {PAGERANK_ITERATIONS} power iterations, uniform start) on the undirected ASA relational graph: nodes = entities, evidence records, UROs; links = entity-URO bindings, evidence-URO supports, evidence-subject links, claim-contradicts bindings; host node score, larger first",
            "random": f"uniform shuffle, seed {RANDOM_BASELINE_SEED}; chance floor, descriptive",
            "projected_uncertainty_formula": "DIAGNOSTIC ONLY (non-decisive): sqrt(sigma_T0^2 + (n sigma_P)^2) * 24 / duration_hours at 2029-01-01 computed directly from the frozen archive row, not through the engine; locates where any ASTRO value comes from",
            "objective_E_as_declared": "DIAGNOSTIC ONLY (non-decisive): data/objectives/E-knowledge-gap-reduction.json unchanged, evaluated under the same Context with visibility unavailable -> the required visibility feature makes every candidate indeterminate; reported as-is",
        },
        "metrics": {
            "grades": GRADE,
            "primary": "Spearman rank correlation rho between method score and label grade over the primary sample; tie-averaged ranks on both sides; a candidate the method does not rank (abstention / missing value) is placed below every ranked candidate, tied; abstention counts reported",
            "secondary": [f"NDCG@{NDCG_K} with gain = grade (alert 3, high 2, medium 1, low 0), ties broken by entity_id ascending", f"Precision@{PRECISION_K} for grade >= 2 (alert or high)"],
            "uncertainty": f"paired bootstrap over candidates, {BOOTSTRAP_RESAMPLES} resamples, seed {BOOTSTRAP_SEED}; 95% percentile CI for ASTRO's rho and for rho(ASTRO) - rho(baseline)",
            "topology_similarity": "Spearman rho between ASTRO score and each of degree and PageRank over the primary sample",
        },
        "acceptance": {
            "PASS": [f"rho(ASTRO) >= rho(b) + {MARGIN} for every b in {{brightness, sigma_period, degree, pagerank}}",
                     "bootstrap 95% CI of rho(ASTRO) lies above 0",
                     f"NDCG@{NDCG_K}(ASTRO) >= NDCG@{NDCG_K}(b) for every b in {{brightness, sigma_period, degree, pagerank}}",
                     f"Spearman(ASTRO, PageRank) < {TOPOLOGY_LIMIT} and Spearman(ASTRO, degree) < {TOPOLOGY_LIMIT}",
                     "every adversarial check with a pass criterion passes"],
            "MIXED": [f"rho(ASTRO) >= rho(b) + {MARGIN} for brightness, degree and pagerank and the CI lies above 0, but the sigma_period margin, the NDCG condition, the topology limit, or one bounded behavioural check fails"],
            "FAIL": [f"rho(ASTRO) < rho(b) + {MARGIN} for any of brightness, degree, pagerank", "bootstrap 95% CI of rho(ASTRO) includes 0",
                     f"Spearman(ASTRO, PageRank) >= {TOPOLOGY_LIMIT} and rho(ASTRO) <= rho(pagerank) + 0.05 (primarily reproduces topology)",
                     "a critical evidence-handling check fails: a registered contradiction is silently ignored, a missing required uncertainty is scored as if known, or an injected record changes a score without appearing in the trace"],
            "INVALID": ["the leakage exclusion cannot be evaluated", "a frozen dataset digest or the manifest digest does not verify at run time",
                        f"fewer than {MIN_SAMPLE} candidates in the primary sample, or fewer than 5 candidates with grade >= 2 or fewer than 5 with grade 0",
                        "protocol deviation, or an implementation failure that cannot be repaired without a scientific choice"],
        },
        "adversarial_checks": [
            {"id": "AC1", "name": "contradictory evidence", "subject": "ASTRO rank-1 candidate of the primary run", "intervention": "add a second admissible ephemeris record (labelled simulated, source 'ASTRO-REAL-DATA-EXP-0001 adversarial') with period x 1.02 and the same uncertainties",
             "expected": "ASA registers a contradicts meta-claim between the two per-planet period claims; ephemeris_drift's trace names the record it used; the score change is bounded by w_drift/W", "pass": "contradiction registered and visible via disputes_of; drift trace names an evidence id; |delta score| <= 4/7"},
            {"id": "AC2", "name": "high-confidence incorrect evidence", "subject": "ASTRO rank-1 candidate", "intervention": "supersede its ephemeris with a copy whose uncertainties are 1e-9 d",
             "expected": "drift -> ~0 and the candidate drops toward the bottom; the trace names the superseding record and its sigma", "pass": "score change fully traced to the injected record (evidence id in the drift trace); recorded as a known limitation that stated uncertainty is trusted"},
            {"id": "AC3", "name": "missing evidence", "subject": "the held-out planets lacking a period or epoch uncertainty (real rows)", "intervention": "none (real missingness)",
             "expected": "status indeterminate for every one; none ranked", "pass": "all indeterminate with the required feature named in the trace"},
            {"id": "AC4", "name": "uncertain relationship", "subject": "ASTRO rank-1 candidate", "intervention": "strip the evidence ids from its hosts relationship (stance becomes unevaluated)",
             "expected": "relationship excluded under the objective's policy; relationship_support -> 0; delta score = -1/7 * previous relationship_support value; recorded in eligibility.excluded", "pass": "exclusion recorded and the score change equals the removed contribution"},
            {"id": "AC5", "name": "isolated candidate", "subject": "a simulated copy of the rank-1 host with only its ephemeris and no relationships", "intervention": "add the entity and evidence",
             "expected": "eligible and ranked (relationship_support 0), not indeterminate", "pass": "eligible with trace"},
            {"id": "AC6", "name": "highly connected but irrelevant candidate", "subject": "a simulated host with 30 evidenced near relationships and 30 measurement claims but no ephemeris", "intervention": "add it",
             "expected": "ASTRO: ineligible (required ephemeris missing); degree and PageRank baselines rank it first", "pass": "ASTRO ineligible; both graph baselines rank it 1"},
            {"id": "AC7a", "name": "Context change: epoch", "subject": "primary sample", "intervention": "as_of = 2026-09-04T00:00:00Z (retrieval date) instead of 2029-01-01",
             "expected": "every drift value non-increasing (fewer elapsed cycles); ranking Spearman with the primary reported", "pass": "no drift value increases; every change traced to cycles_since_epoch"},
            {"id": "AC7b", "name": "Context change: feasibility", "subject": "primary sample", "intervention": "limiting_magnitude = 10",
             "expected": "instrument_suitability -> 0 for hosts fainter than V = 10; those scores fall by 1/7; others unchanged", "pass": "exactly that"},
            {"id": "AC8", "name": "relationship removal (ablation)", "subject": "primary sample", "intervention": "objective variant with no relationship feature and no eligible relationship types", "expected": "rho reported; delta rho = the value relationships add", "pass": None},
            {"id": "AC9", "name": "stance removal (ablation)", "subject": "primary sample", "intervention": "every relationship's evidence stripped and the objective set to include unevaluated relationships (trust every assertion)", "expected": "rho reported", "pass": None},
            {"id": "AC10", "name": "uncertainty removal", "subject": "primary sample", "intervention": "strip every ephemeris uncertainty; (a) declared objective, (b) variant with missingness zero_with_trace",
             "expected": "(a) every candidate indeterminate - the engine abstains rather than ranking without uncertainty; (b) rho reported", "pass": "(a) all indeterminate"},
            {"id": "AC11", "name": "topology alone", "subject": "primary sample", "intervention": "none", "expected": f"Spearman(ASTRO, degree) and Spearman(ASTRO, PageRank) both < {TOPOLOGY_LIMIT}", "pass": f"both < {TOPOLOGY_LIMIT}"},
            {"id": "ACL", "name": "leakage report", "subject": "pool", "intervention": "none", "expected": "count of leakage-flagged planets reported; secondary run including them reported with the flag", "pass": None},
        ],
        "seeds": {"bootstrap": BOOTSTRAP_SEED, "random_baseline": RANDOM_BASELINE_SEED, "hash_salt": HASH_SALT},
        "software": {"python": platform.python_version(), "requirements_lock_sha256": sha256_file(ROOT / "requirements.lock"), "astro_version": ASTRO_VERSION,
                     "astro_commit_at_freeze": _git("rev-parse", "HEAD"), "asa_baseline_sha": asa_baseline_sha(), "kernel_version": kv["kernel"]},
        "prohibited_after_results": ["changing any weight, parameter, policy, threshold or feature of the declared objective", "changing the Context", "changing candidate rules, the sample, or the hash salt",
                                     "replacing, adding or removing a baseline", "changing a metric, K, margin or acceptance rule", "removing inconvenient candidates or adversarial cases",
                                     "any change to src/astro/significance, src/astro/asa, src/astro/knowledge or src/astro/catalogues"],
        "engineering_repair_rule": "An implementation defect in the experiment apparatus (src/astro/realdata, tools/realdata_exp0001.py) may be repaired; the repair is recorded in the report and the whole experiment is rerun. A defect in the engine itself is reported, not repaired, unless it prevents execution, in which case the repair and the rerun are recorded and distinguished from tuning.",
    }


def freeze_manifest() -> dict[str, Any]:
    if MANIFEST_PATH.exists():
        raise RuntimeError(f"{MANIFEST_PATH.name} already exists; a pre-registration is frozen once")
    m = build_manifest()
    text = json.dumps(m, indent=1, sort_keys=True) + "\n"
    MANIFEST_PATH.write_text(text, encoding="utf-8")
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    MANIFEST_PATH.with_suffix(".sha256").write_text(f"{digest}  {MANIFEST_PATH.name}\n", encoding="utf-8")
    return {"manifest": MANIFEST_PATH.name, "sha256": digest, "objective_id": m["objective"]["objective_id"], "context_id": m["context"]["context_id"]}


def load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def verify_manifest() -> dict[str, Any]:
    recorded = MANIFEST_PATH.with_suffix(".sha256").read_text(encoding="utf-8").split()[0]
    actual = sha256_file(MANIFEST_PATH)
    return {"recorded": recorded, "actual": actual, "ok": recorded == actual}
