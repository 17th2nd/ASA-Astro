# ASTRO-REAL-DATA-EXP-0001 — Preflight

Programme: CLAUDE ASTRO PROGRAMME — REAL-DATA VALIDATION 001 · Operator: Claude · Date: 2026-09-04 (UTC)

This document records the state of the repository before any experiment code was written. It is a
preflight, not a result. Nothing in it is evidence for any ASA or ASTRO claim.

## 1. Repository

| Item | Value |
|---|---|
| Path | `/home/brock-gerand/ASA-Astro` → `https://github.com/17th2nd/ASA-Astro.git` |
| Branch | `main` (repository rule from claudeastro001: no branches, commit direct to `main`, push each session) |
| HEAD | `00118ff1099ff65e59d27d08b2165b242e334071` — "docs: store 3 frontier report counts (claudeastro005 §6)", 2026-09-04 12:49 +1000 |
| Working tree | clean (0 modified, 0 untracked tracked-path changes) before this programme |
| Python | CPython 3.12.3 in `.venv`; `pip freeze` matches `requirements.lock` exactly (attrs 23.2.0, jsonschema 4.10.3, Pillow 10.2.0, pyrsistent 0.20.0, setuptools 68.1.2) |
| Astro engine | `src/astro/`, `ASTRO_VERSION = "0.1.0"` |
| ASA baseline | `config/asa-baseline.json`: `17th2nd/ASA` branch `kernel/v0.1-alpha`, sha `b855d4c730dc2553db7a693d91c7d4d0cf25d03c`, kernel `0.1.0-alpha10`, status "ENGINEERING ALPHA — NOT RATIFIED"; materialised at `.asa/ASA` (gitignored) |

## 2. Relevant repository instructions

- `README.md` — Astro is a proving implementation on astronomy workloads; all committed Astro data is synthetic or simulated and labelled; real catalogue rows are fetched, never committed; nothing in Astro touches the frozen scientific instruments or claims empirical validation of ASA. "No repository artefact declares ASA or ASA-Astro scientifically validated."
- `governance/decision-register.md` — DR-0018 (expert annotation protocol) and DR-0019 (ground-truth correction policy) are **Open**; DR-0020 (release/change authority) is Open: no operator may declare scientific validation complete.
- `governance/integration-issues.md` — INT-0020 to INT-0025 (contradiction handling, assertion uncertainty, missing-evidence behaviour, Standing convergence, explanation evidence links, inferred-hypothesis certainty) are **Open**. They were raised against the legacy Codex C reasoning engine (`src/asa_astro/reasoning`), see §7.
- `temp/claudeastro001.md`–`claudeastro005.md` — operator reports for the current engine; `temp/astro-asa-integration.md` — what Astro consumes from ASA.
- The frozen-artefact manifest `config/frozen-artefacts-v1.json` declares `docs/claims` and `validation/benchmarks` as closed directories. Nothing in this programme writes there.

## 3. Test commands and results (this machine, 2026-09-04)

| Suite | Command | Result |
|---|---|---|
| Whole repository | `PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -t .` | **128 tests, OK** (84 s) |
| Astro engine | `… discover -s tests/astro -t .` | 65 tests, OK |
| ASTRO-EXEC-002 skeleton | `… discover -s tests/exec -t .` | 38 tests, OK |
| Legacy POC (unit / reasoning / integration) | `… discover -s tests/unit|tests/reasoning|tests/integration -t .` | 8 / 10 / 7 tests, OK |
| Frozen artefacts | `.venv/bin/astro-exec validate-frozen --config config/astro-exec-phase2.toml` | `{"artefact_count":6,"status":"verified"}`, exit 0 (re-run after the experiment: unchanged) |

The brief's "63/63 tests" is the Phase 2 engineering figure recorded in `reports/ASA-ASTRO-POC-VALIDATION-REPORT-0001.md`
for the legacy pipeline; the suites as they stand today are the counts above. All pass. The baseline is not broken.

## 4. Frozen-file integrity

Every file in the Research Controls V1 freeze unit and the Theory V1 freeze was checked against the digests recorded at freeze time.

| File | Recorded | Current | State |
|---|---|---|---|
| `validation/benchmarks/ASTRO-EXP-0001.md` | blob `8b66069…`, sha256 `a387968…` | blob `8b66069…` | unchanged |
| `docs/claims/ASTRO-CLAIMS-0001.md` | blob `f1b4d94…`, sha256 `44282ba…` | blob `f1b4d94…` | unchanged |
| `validation/results/ASTRO-RESULTS-0001.md` | blob `c1a3739…`, sha256 `434e4d4…` | blob `c1a3739…` | unchanged; ledger ends at `AR1-E000003`, no execution event |
| `reports/ASTRO-V1-RESEARCH-CONTROLS-FREEZE-REPORT.md` | blob `d0b57c9…` | blob `d0b57c9…` | unchanged |
| `09_Drafts/Codex/ASTRO-EXP-0001_Minimum-Validation-Programme.md` | blob `2b8ce54…` | blob `2b8ce54…` | unchanged |
| `09_Drafts/Codex/2026-08-01_Codex_ASTRO-PRIOR-ART-0001.md` | blob `64fe1d2…` | blob `64fe1d2…` | unchanged |
| `docs/theory/ASTRO-THEORY-0001.md` | post-freeze blob `f6b4337…`, file sha256 `c1289b3…`, **mathematical-body sha256 `383a9a8bf1d1d19a230caa79b3febcf6abddf293b6d83ed697cdf0dcf20c16c1`** | blob `f6b4337…`, file sha256 `c1289b3…`, math-body `383a9a8b…` | unchanged (recomputed with the manifest's own procedure) |
| `docs/theory/ASTRO-THEORY-0001-V1-FREEZE-RECORD.md` | blob `0883e31…` | blob `0883e31…` | unchanged |
| `README.md` | in the freeze unit; blob `b47f19d…` at freeze | blob `22ed829…` | changed by 7 later commits (additive programme sections). Recorded, not a finding of this programme. |

Evidence level remains **EH-0**. Experiments executed under `ASTRO-EXP-0001`: **0**.

## 5. The existing `ASTRO-EXP-0001` protocol

`ASTRO-EXP-0001@1.0` is a frozen, unexecuted, single-experiment protocol: a frozen ASA estimator selecting four of
sixteen `SB441-N16` asteroid perturbers for 27 Gaia DR3 near-Earth asteroids, compared with direct
leave-one-perturber-out finite perturbation on 20-year propagations; endpoint `W ≥ 20` material wins; four separated
roles, a witnessed salt, ~20,000 propagations, AUD 30–60k, six to eight weeks. It states "There is no Experiment 2"
and "F0 and F1 … do not authorise another, easier benchmark".

That protocol cannot be executed here (no truth laboratory, no custodian, no propagator, no independent statistician,
and unresolved custodian rulings UR-001..010 recorded in `docs/execution/ASTRO-EXEC-001-UNRESOLVED-REQUIREMENTS.md`).
It is **not** what this programme runs. This programme is an engineering value evaluation of the Astro execution
engine on one small real dataset, under the founder's brief. It does not execute, amend, or interpret
`ASTRO-EXP-0001`; it appends nothing to `ASTRO-RESULTS-0001`; it changes no claim status; it cannot move the
evidence level from EH-0. Any result here is engineering evidence about the Astro engine, not scientific evidence for
`ASTRO-CLM-0070`.

## 6. What "ASTRO" is being tested

Two engines exist in the repository:

| Engine | Location | State |
|---|---|---|
| Legacy Codex B/C pipeline | `src/asa_astro/` | image-region candidate graph + provisional Standing/Significance over image regions; declared obsolete as engine (claudeastro001); cannot consume catalogue data; INT-0020..0025 were raised against it |
| Astro execution engine | `src/astro/` | domain model, ASA adapter (pinned kernel), objective-scoped significance evaluator (21 declared features, weighted, traced), planner/scheduler, receipts, real-catalogue store, knowledge frontier (gaps, claims, contradictions, derived geometry), benchmark harness with baselines and independent oracles |

**Decision recorded:** this programme tests `src/astro/`. The brief's list of concerns (contradiction handling,
assertion uncertainty, missing-evidence behaviour, centrality convergence, results tracking graph topology) is mapped to the
current engine's equivalents in the adversarial checks: ASA `contradicts` stance on registered claims; relationship
stance (endorsed vs unevaluated) and confidence; missingness policy (`indeterminate` abstention vs `zero_with_trace`);
there is no iterative Standing/centrality in the current engine, so "remove Standing" becomes "remove stance gating" and
"topology alone" becomes explicit degree/PageRank baselines over the ASA relational graph.

## 7. Real-data state already in the repository

- Seven public catalogues are fetched to `data/catalogues/raw/` (gitignored) with digests, retrieval times, releases and
  licences in `data/catalogues/manifest.json`: NASA Exoplanet Archive `pscomppars` (retrieved 2026-09-02T22:42:44Z, sha256
  `efe83528…`), Gaia DR3 hosts, GCVS 5.1, OpenNGC (CC-BY-SA-4.0), Hunt & Reffert 2023, MPC observatory codes, ALeRCE ZTF.
  All snapshot files are present and verify.
- Persistent stores `var/astro-store2`, `var/astro-store3` (gitignored, 12 GB each) and universe JSONs under `var/`
  exist but are not reproducible from a clean checkout and are **not** inputs to this experiment.
- Existing real-data benchmarks (claudeastro005 §5, §7) compare strategies against oracles written by the same operator;
  they are not independent reference truth and are not reused as such here.

## 8. Unresolved decisions affecting this experiment (assumptions stated)

| # | Decision | Assumption taken |
|---|---|---|
| U1 | Which engine is "ASTRO" | `src/astro/` (§6). |
| U2 | Authority to run a real-data test outside `ASTRO-EXP-0001` ("nothing else is authorised") | The founder's brief authorises an engineering value evaluation; it is labelled as such everywhere and touches no frozen instrument (§5). |
| U3 | No existing objective asks a question for which an independent label set exists | One objective is declared from the existing feature library only, pre-registered in the manifest before any run, with content id and rationale; existing objective E is run as a secondary, non-decisive comparison. No feature code is changed. |
| U4 | Redistribution of the frozen dataset extract | The extract holds only the candidate rows (public-domain NASA data; ExoClock public database, citation required). Committed for reproducibility; wider publication is a founder decision, as with OpenNGC. |
| U5 | Commit and push | Repository rule (claudeastro001): commit to `main`, push each session. Applied at the end. |
| U6 | DR-0018/DR-0019 open | No expert annotation is created; the reference labels are an existing external programme's published labels, versioned by retrieval date and digest. |

## 9. Can a real-data experiment proceed without violating a freeze?

**Yes**, under the boundaries in §5 and §8. The experiment writes only to new paths
(`validation/real-data/ASTRO-REAL-DATA-EXP-0001/`, `src/astro/realdata/`, `tools/`, `tests/astro/`, `temp/`); it reads
frozen files only to verify their digests; it declares no claim, appends no ledger event, and modifies no theory,
protocol, weight or acceptance threshold of any existing instrument. Proceed to Phase 2.
