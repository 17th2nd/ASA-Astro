# ASTRO-REAL-DATA-EXP-0001 — Failure note

Written 2026-10-03 against `main` @ `cf20f04`. Source of every number: `ASTRO-REAL-DATA-EXP-0001-REPORT.md` (run 2026-09-04T09:34:40Z, engine `00118ff`, manifest sha256 `b6895cc5…`). This note adds no new result. It records what failed, what is still open, and the hold that follows.

## What this experiment is, and is not

- It is a one-off real-data engineering test of the Astro engine (`src/astro/`) on one objective (ephemeris maintenance) against ExoClock priority labels, n = 100.
- It is **not** `ASTRO-EXP-0001`. The canonical protocol `ASTRO-EXP-0001` has still never been executed. `ASTRO-RESULTS-0001` stays at `EH-0` and no `ASTRO-CLM-*` status changed.

## What failed

The verdict was FAIL on two independent grounds. Either one alone would have failed it.

1. **Did not beat the simple baselines.** ASTRO Spearman ρ 0.2745 (95% CI 0.066–0.454).
   - Raw tabulated period uncertainty (`sigma_period`): ρ 0.3953. ASTRO is *below* it, not 0.10 above.
   - Brightness: ρ 0.2584. Required margin not met.
   - NDCG@25: 0.490 vs `sigma_period` 0.569.
   - ASTRO beat only the graph baselines (degree 0.039, PageRank 0.049), which score about the same as random (0.042).
2. **Critical evidence-handling check AC3 failed.** Of 10 real hosts missing one of their two ephemeris uncertainties, 9 were scored as if the missing value were 0.0, and the trace did not say so.

## Why it failed

- On this task the score reduces to one feature, `ephemeris_drift`. The other three features are near-constant: relationship_support is 1.0 for every host, instrument_suitability is 1.0 for nearly all, evidence_quality is 0.9 or 0.7.
- Propagating σ_P over elapsed cycles and normalising by transit duration *lowers* agreement with the labels compared with using σ_P directly.
- Relationships and stance contribute nothing measurable here. Removing relationships (AC8) left ρ at 0.2745. Removing stance (AC9) left ρ at 0.2745.
- That is partly by construction: each candidate has exactly one `hosts` edge. ExoClock's priority also depends on observation recency, which none of the inputs carry.

## Defects still open on `main` @ `cf20f04`

| # | Defect | State |
|---|---|---|
| D1 | `ephemeris_drift` (`src/astro/significance/features.py` ~L327–336) skips a record only when *both* uncertainties are absent. If one is absent, `u.get(…, 0.0)` reads it as zero and the trace does not say so. | **Open.** The code is unchanged since the run. |
| D2 | Under `missingness_policy: zero_with_trace`, a `required: true` feature never forces abstention. "required" only has an effect under `indeterminate`. | **Open.** Declaration-semantics trap. |
| D3 | `ephemeris_drift` clips at σ_T ≥ duration, so the most uncertain planets tie (3 of 100 here). | Open, minor. |

D4 and D5 were defects in the experiment apparatus. They were repaired during the run (see the report, §6).

## Hold

Until D1 and D2 are each either repaired with a regression test or explicitly accepted as limits:

- no kernel claim, and no claim that the Astro engine or ASA adds ranking value, may cite this experiment or this objective;
- no `ASTRO-CLM-*` status change may rest on Astro engine output.

A repair would change engine behaviour, so it needs a new pre-registered run with a new manifest. This run's frozen results must not be edited.
