# claudeastro006 — Real-data validation 001: ExoClock ephemeris priority

Programme: CLAUDE ASTRO PROGRAMME — REAL-DATA VALIDATION 001 · Operator: Claude · Date: 2026-09-04 · Directive: "Determine whether ASTRO adds measurable value on one small, real astronomical dataset."

```
ASTRO_HEAD    = 00118ff + this programme's commit   ASA_BASELINE = b855d4c730dc2553db7a693d91c7d4d0cf25d03c (unchanged)
TESTS         = 141/141 (128 existing + 13 new)     FROZEN       = 6/6 artefacts verified; theory math-body digest 383a9a8b… unchanged
VERDICT       = FAIL   (manifest b6895cc5…; results 1424811bd676dd8c…; adversarial 94bd100375574d84…)
```

## What was done

1. **Preflight** (`validation/real-data/ASTRO-REAL-DATA-EXP-0001/…-PREFLIGHT.md`): clean tree at 00118ff; all suites green; every freeze-unit blob and the theory mathematical-body digest match the freeze records; `ASTRO-EXP-0001` is a different, unexecutable asteroid-perturber protocol — this programme is an engineering value test of `src/astro/`, outside its authority, appending nothing to the results ledger.
2. **Dataset** (…-DATASET-RECORD.md, written before retrieval): ASTRO input = the repository's frozen 2026-09-02 NASA Exoplanet Archive + Gaia DR3 snapshots; reference truth = ExoClock's published ephemeris priority (alert/high/medium/low; definition: target uncertainty = 1/12 transit duration in 2029, plus recency of observation); leakage check = the archive's ephemeris reference links (61 planets whose archive ephemeris *is* an ExoClock publication were excluded). 776 → 772 matched → 598 single-host → pool 527 → primary 100 by hash order.
3. **Pre-registration** (…-MANIFEST.json, sha256 b6895cc5…, frozen before the run): objective "Ephemeris maintenance" (existing features only: ephemeris_drift 4 required, relationship_support 1, evidence_quality 1, instrument_suitability 1), Context epoch 2029-01-01 site-independent V ≤ 14, four decisive baselines (brightness, σ_P, degree, PageRank over the ASA relational graph), Spearman/NDCG@25/P@25, margins, bootstrap, twelve adversarial checks with pass criteria, prohibited post-result changes.
4. **Apparatus** (`src/astro/realdata/`, `tools/realdata_exp0001.py`, 13 tests): frozen extract → unchanged parsers → frontier → in-memory kernel → `decide`; baselines read only the snapshot; reference labels never reach the engine (AST-checked).
5. **One run**, then adversarial checks. Two apparatus defects (AC10 evidence-id remap; reproduction check used a different stream name) repaired and the checks rerun; primary run executed once; reproduction exact.

## Result (primary, n = 100)

| method | ρ | NDCG@25 | P@25 |
|---|---:|---:|---:|
| **asa** | 0.2745 [CI 0.066, 0.454] | 0.490 | 0.56 |
| sigma_period | **0.3953** | 0.569 | 0.72 |
| brightness | 0.2584 | 0.449 | 0.52 |
| pagerank / degree | 0.049 / 0.039 | 0.39 / 0.31 | 0.44 / 0.40 |
| random | 0.042 | 0.35 | 0.44 |

Pre-registered FAIL on two grounds: margin vs brightness and σ_P not met (ASTRO below the scalar), and AC3 failed (9 of 10 real hosts lacking one uncertainty component were scored with it silently zero). Passed: contradiction registration (AC1), traced supersession (AC2), stance exclusion arithmetic (AC4), isolated/hub behaviour (AC5/6), Context arithmetic (AC7), abstention with no uncertainty (AC10), no topology reproduction (AC11: ρ 0.18/0.08). Ablations: relationships and stance change ρ by exactly 0; uncertainty carries the signal (0.27 → 0.11 without it).

## Findings worth keeping

- **The engine's value on this task is one feature, and that feature loses to its own raw input.** Propagating σ_P over cycles and normalising by duration lowers agreement with ExoClock (formula diagnostic 0.22, engine 0.27, raw σ_P 0.40). The label's recency component is invisible to every method.
- **Engine defect D1** (`ephemeris_drift`): a missing `epoch_days`/`period_days` uncertainty is read as 0.0, untraced. Not repaired (manifest forbids engine changes mid-experiment). Fix candidates: abstain, or record the assumption in the trace and lower quality.
- **Declaration trap D2:** `required: true` has no effect under `missingness_policy: zero_with_trace` — objective E scores everything with visibility 0 when no site is declared. E should probably be `indeterminate`, or "required" should abstain regardless of policy.
- Brightness correlates with the ExoClock label (ρ 0.26); restricting to V ≤ 10 raised ASTRO's agreement to 0.30. Feasibility is doing work the objective did not claim.
- Relationships were constant by construction (one endorsed `hosts` edge per candidate). A task where relationships carry information is needed before "did relationships add value" can be answered positively or negatively in general.

## Not done / boundaries

No engine, objective, theory, protocol or ledger file modified. README untouched. No scientific validation claimed; EH-0 unchanged. Raw ExoClock/reflink downloads are gitignored; only the candidate rows are committed (public data, citations recorded; wider publication is a founder decision).

## Next (recommendation, not started)

Fix D1 in `ephemeris_drift`; decide whether D2 is a policy or a bug; then, only with an astronomer-declared objective on a relationship-bearing task, run ASTRO-REAL-DATA-EXP-0002 under the same discipline. Do not tune the ephemeris objective against ExoClock.
