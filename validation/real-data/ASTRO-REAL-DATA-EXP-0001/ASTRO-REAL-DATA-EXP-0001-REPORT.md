# ASTRO-REAL-DATA-EXP-0001 — Report and verdict

Programme: CLAUDE ASTRO PROGRAMME — REAL-DATA VALIDATION 001 · Operator: Claude · Run 2026-09-04T09:34:40Z (UTC)
Engine commit `00118ff1099ff65e59d27d08b2165b242e334071` (clean) · ASA baseline `b855d4c7` (kernel 0.1.0-alpha10) · Manifest sha256 `b6895cc59aca1571e7e9337e373c04579c5e53f1af386644196c204bde6a9452`

## Verdict: **FAIL**

Under the pre-registered acceptance rules (manifest §acceptance), the Astro engine's ranking did not outperform the
declared simple baselines by the required margin, and one critical evidence-handling check failed:

| Rule | Required | Observed | Met |
|---|---|---|---|
| ρ(ASTRO) ≥ ρ(brightness) + 0.10 | ≥ 0.3584 | 0.2745 | no |
| ρ(ASTRO) ≥ ρ(sigma_period) + 0.10 | ≥ 0.4953 | 0.2745 | no (ASTRO is below the scalar baseline) |
| ρ(ASTRO) ≥ ρ(degree) + 0.10 | ≥ 0.1388 | 0.2745 | yes |
| ρ(ASTRO) ≥ ρ(pagerank) + 0.10 | ≥ 0.1485 | 0.2745 | yes |
| bootstrap 95% CI of ρ(ASTRO) above 0 | — | [0.066, 0.454] | yes |
| NDCG@25 not below every baseline | — | below sigma_period (0.490 vs 0.569) | no |
| Spearman(ASTRO, degree / PageRank) < 0.8 | — | 0.184 / 0.081 | yes |
| critical evidence-handling checks | all pass | AC3 failed: a host lacking one of its two ephemeris uncertainties is scored with that uncertainty silently taken as zero | no |

The FAIL is on two independent grounds: the metric rule against the brightness and period-uncertainty baselines, and
the AC3 missing-evidence check. Either alone would have produced FAIL. Nothing was changed after the result.

This is engineering evidence about the Astro engine (`src/astro/`) under one declared objective on one small real
dataset. It is not a result under `ASTRO-EXP-0001`, changes no `ASTRO-CLM-*` status, and leaves the evidence level at
EH-0. It is also not evidence that ASA or ASTRO cannot add value on a different task; see §8.

## 1. Experiment performed

One evaluation of the declared objective **Ephemeris maintenance** (id `OBJ-63f56419…`, four existing features:
ephemeris_drift 4.0 required, relationship_support 1.0, evidence_quality 1.0, instrument_suitability 1.0) under the
declared Context **epoch 2029-01-01, site-independent, V ≤ 14** (id `CTX-66365bb2…`), over a universe built from the frozen
extract by the unchanged catalogue parsers and frontier derivation, loaded into an in-memory ASA kernel at the pinned
baseline. The engine's score per candidate host was compared with the ExoClock ephemeris priority (alert 3 / high 2 /
medium 1 / low 0) using Spearman ρ (primary), NDCG@25 and Precision@25, against four decisive baselines and two
diagnostics, all declared before the run.

| Item | Value |
|---|---|
| Universe | `UNI-405fbcc6…`, label `ASTRO-REAL-DATA-EXP-0001`, data_class `real`: 1,234 entities (598 hosts, 636 planets), 4,751 evidence records, 4,757 relationships after the frontier (1,198 lacks-evidence gaps, 2,918 measurement claims, 34 contradictions, 597 derived distances, 3 near, 2 comparison-star candidates) |
| Kernel | in-memory, seq 73,823, digest `sha256:231848fd…`, ASA baseline `b855d4c7`, registry facet `sha256:6ccc3b43…` |
| Evaluation / receipt | `SIG-f6d49b3b…` / `RCPT-b4c3dd27…` (`results/primary-run/`, receipt sha256 `e3ef0a3399121fbb…`) |
| Timings | universe 0.7 s · kernel load 15.9 s · evaluate 1.1 s · baselines 0.9 s · metrics 1.0 s |
| Reproduction | the adversarial module rebuilt the universe and kernel from the frozen extract and obtained the identical evaluation id `SIG-f6d49b3b…` |

## 2. Dataset and independent reference

| Role | Source | Identity |
|---|---|---|
| ASTRO input | NASA Exoplanet Archive `pscomppars` snapshot 2026-09-02T22:42:44Z | sha256 `efe83528…`; frozen rows for the 598 hosts in scope: `dataset/input_pscomppars_rows.csv` |
| ASTRO input | Gaia DR3 `gaia_source_lite` for those hosts, snapshot 2026-09-02T22:53:43Z | sha256 `64f14a90…`; `dataset/input_gaia_rows.csv` |
| Reference truth | ExoClock planet database, retrieved 2026-09-04T09:25:16Z | sha256 `fb762669…` (1,672,157 bytes); labels only in `dataset/reference_exoclock_priority.json` |
| Leakage check | Archive ephemeris reference links (`tran_flag = 1`), retrieved 2026-09-04T09:25:22Z | sha256 `7c7c9ef7…`; `dataset/leakage_reflinks.csv` |

Selection (`dataset/candidates.json`, sha256 `bfc6ea3f47c79ee1…`): 776 ExoClock planets → 772 matched by normalised name (4 unmatched:
HD108236d, Kepler-1658b, Kepler-854b, TOI-836c) → 598 with a single-transiting-planet host → 10 held out for missing
uncertainties → 2 excluded because the live archive values differ from the snapshot → **61 excluded as leakage** (the
archive's period or transit-midpoint reference is an ExoClock publication, Kokori et al. 2023) → pool 527 → primary
sample = first 100 by SHA-256 hash order (alert 2, high 40, medium 22, low 36).

Licences: NASA public domain (cite doi:10.26133/NEA13); ESA Gaia data policy; ExoClock public database, cite Kokori et
al. 2022, 2023. Wider redistribution of the extract is a founder decision.

## 3. ASTRO score

| Sample | n | Spearman ρ | 95% CI | NDCG@25 | P@25 (grade ≥ 2) | abstentions |
|---|---:|---:|---|---:|---:|---:|
| **primary** | 100 | **0.2745** | [0.066, 0.454] | 0.4898 | 0.56 | 0 |
| pool (secondary) | 527 | 0.1346 | — | 0.6299 | 0.84 | 0 |
| pool + leakage-flagged (secondary) | 588 | 0.1129 | — | 0.5869 | 0.76 | 0 |

Top of the primary ranking: TOI-172 b, TOI-3082 b, TOI-2048 b (all "high", drift saturated at 1.0), CoRoT-10 b ("alert"),
TOI-4603 b, TOI-257 b, TOI-1338 b ("high"), then TrES-5 b ("low"), CoRoT-1 b ("medium"), Qatar-6 b ("low"). Bottom:
TOI-3235 b, LHS 3844 b ("high" — a well-timed TESS planet the archive lists with σ_P = 4.4e-8 d), Kepler-17 b.

## 4. Baseline scores (primary sample, n = 100)

| Method | ρ | ρ difference CI (ASTRO − method) | NDCG@25 | P@25 |
|---|---:|---|---:|---:|
| **sigma_period** (tabulated σ_P, larger first) | **0.3953** | [−0.258, 0.016] | 0.5688 | 0.72 |
| brightness (brighter first) | 0.2584 | [−0.243, 0.256] | 0.4485 | 0.52 |
| pagerank (ASA relational graph) | 0.0485 | [−0.038, 0.488] | 0.3917 | 0.44 |
| degree (ASA relational graph) | 0.0388 | [−0.010, 0.462] | 0.3060 | 0.40 |
| random (diagnostic, seed 20260904) | 0.0417 | — | 0.3486 | 0.44 |
| projected-uncertainty formula (diagnostic, unclipped, straight from the archive row) | 0.2189 | — | 0.4898 | 0.56 |
| objective E as declared (diagnostic; visibility unavailable, counted as zero under its `zero_with_trace` policy) | 0.2911 | — | — | — |

On the full pool the ordering is the same: sigma_period 0.397 > ASTRO 0.135 > brightness 0.099 > graph baselines ≈ −0.04.

Reading: the label signal that these inputs can see sits almost entirely in the tabulated period uncertainty. Propagating
it over elapsed cycles and normalising by transit duration (the engine's declared drift, and equally the diagnostic
formula computed outside the engine) *lowers* agreement with ExoClock relative to the raw scalar. The engine's other three
features are near-constant on this sample (relationship_support = 1.0 for every host; instrument_suitability = 1.0 for
all but the faintest; evidence_quality 0.9 or 0.7), so ASTRO ≈ drift. Graph topology carries no signal (≈ random), and
ASTRO is not correlated with it.

## 5. Adversarial and ablation checks (`results/adversarial.json`, sha256 `94bd100375574d84…`)

Subject for the single-candidate checks: the ASTRO rank-1 primary candidate, **TOI-172** (score 0.9857, drift 1.0).

| Check | Result | What happened |
|---|---|---|
| AC1 contradictory evidence | **pass** | A second admissible ephemeris (period × 1.02, labelled simulated) produced two `asa.core/contradicts` meta-claims on `period_days[TOI-172 b]`, visible through the snapshot's disputes. ephemeris_drift kept the original record (trace names it); score unchanged (already saturated). The contradiction is registered and traceable but the declared objective never consults it — only objective F would. |
| AC2 high-confidence incorrect evidence | **pass** (limitation recorded) | Superseding the ephemeris with σ = 1e-9 d drove drift from 1.0 to 2.0e-6 and the score from 0.986 to 0.414 (rank 1 → 89 of 100); the trace names the injected record; the old record is excluded as superseded. The engine trusts a stated uncertainty; nothing cross-checks it. |
| AC3 missing evidence | **FAIL** | Of 10 real held-out hosts lacking a period or epoch uncertainty, **9 were scored** (e.g. GJ 3470 with only σ_P; Qatar-5 with only σ_T0) because `ephemeris_drift` reads the absent component as 0.0 without saying so in its trace; only TrES-3 (both absent) was indeterminate. This is the pre-registered critical condition "a missing required uncertainty is scored as if known". |
| AC4 uncertain relationship | pass | Stripping the evidence from TOI-172's `hosts` relationship made it unevaluated; the objective excluded it (recorded in eligibility), relationship_support fell 1.0 → 0.0 and the score fell by exactly 1/7 (0.9857 → 0.8429); the `include` policy restores the original score. |
| AC5 isolated candidate | pass | A simulated host with only an ephemeris and no relationships is eligible (0.8429) with an empty relationship list. |
| AC6 hub | pass | A simulated host with 30 evidenced `near` edges and 30 claims but no ephemeris: degree 120 vs primary median 16; degree rank 1 and PageRank rank 1; ASTRO: ineligible, "missing ephemeris". |
| AC7a Context: epoch → 2026-09-04 | pass | 98 of 100 drift values changed, none increased; ranking Spearman with the primary 0.9987; ρ vs labels 0.268. |
| AC7b Context: V ≤ 10 | pass | 80 hosts fainter than V = 10 lost exactly 1/7; 20 unchanged. ρ vs labels rose to 0.3015 — brightness correlates with the ExoClock label (see §4). |
| AC8 relationship removal (ablation) | — | ρ 0.2745 → **0.2745**. Relationships add nothing on this task. |
| AC9 stance removal (ablation) | — | Every relationship unevidenced (endorsed 1,198 / unevaluated 3,593 edges); ρ 0.2745 under "trust everything", 0.2745 under the declared policy. Stance gating changes nothing here. |
| AC10 uncertainty removal | pass | Declared objective: **100/100 indeterminate** — the engine abstains rather than ranking without uncertainty. `zero_with_trace` variant: ρ 0.1069 (what evidence_quality and feasibility alone carry). |
| AC11 topology alone | pass | Spearman(ASTRO, degree) 0.184; (ASTRO, PageRank) 0.081. |
| ACL leakage | — | 61 of 588 matched single-host planets carry an ExoClock-published ephemeris in the archive and were excluded; including them does not change the picture (ASTRO 0.113 vs σ_P 0.371). |

## 6. Defects discovered

| # | Where | Defect | Class | Action |
|---|---|---|---|---|
| D1 | engine, `astro/significance/features.py` `ephemeris_drift` | A missing `epoch_days` or `period_days` uncertainty is read as 0.0 (`u.get(..., 0.0)`) and the trace does not say so; the host is scored, not abstained on. | engine evidence-handling defect (AC3) | **Not repaired** (the manifest forbids engine changes during the experiment). Reported. |
| D2 | engine, objective semantics | Under `missingness_policy: zero_with_trace` a `required: true` feature has no effect: objective E as declared scores every candidate with visibility = 0 instead of abstaining. The word "required" only bites under `indeterminate`. | declaration-semantics trap | Reported. |
| D3 | engine, `ephemeris_drift` | Clips at σ_T ≥ duration, so the most uncertain planets tie (3 of 100 here). | minor | Reported. |
| D4 | apparatus, `realdata/adversarial.py` AC10 | Re-creating ephemeris records without uncertainty changed their content ids; the `hosts` relationships still cited the old ids (`UniverseError`). | apparatus | Repaired (evidence ids remapped); all checks rerun. |
| D5 | apparatus, `realdata/adversarial.py` | The reproduction check opened the base kernel under a different stream name than the primary run, so the evaluation id differed by construction. | apparatus | Repaired (same stream); rerun; reproduction exact. |

D4 and D5 are engineering repairs of the experiment apparatus, made before any check result was read as a result, with
the whole adversarial suite rerun; no weight, candidate, baseline, metric or threshold changed. The primary run was
executed once.

## 7. Files created (nothing existing was modified)

```
validation/real-data/ASTRO-REAL-DATA-EXP-0001/
  ASTRO-REAL-DATA-EXP-0001-PREFLIGHT.md
  ASTRO-REAL-DATA-EXP-0001-DATASET-RECORD.md
  ASTRO-REAL-DATA-EXP-0001-MANIFEST.json  (+ .sha256)          pre-registration, frozen before the run
  ASTRO-REAL-DATA-EXP-0001-REPORT.md                            this report
  ASTRO-REAL-DATA-EXP-0001-FOUNDER-SUMMARY.md
  objective-ephemeris-maintenance.json · context-ephemeris-maintenance-2029.json
  dataset/PROVENANCE.json · candidates.json · input_pscomppars_rows.csv · input_gaia_rows.csv
          reference_exoclock_priority.json · leakage_reflinks.csv
  results/results.json (sha256 1424811bd676dd8c…) · adversarial.json (94bd100375574d84…) · candidates_scored.{csv,json}
          explanations.json (all 100 primary candidates) · COMPARISON.md · primary-run/{evaluation,plan,objective,context,receipt}.json + receipt.sha256
src/astro/realdata/{__init__,dataset,manifest,universe,baselines,metrics,experiment,adversarial}.py
tools/realdata_exp0001.py
tests/astro/test_realdata.py   (13 tests)
temp/claudeastro006.md
```
Raw downloads (gitignored): `data/catalogues/raw/exoclock_planets.json`, `exoplanetarchive_pscomppars_reflinks.csv`.

## 8. What the result does and does not say

- It says: on this task, the engine ran on real data deterministically and reproducibly, every score traces to named
  evidence and relationships, abstention works when uncertainty is wholly absent, Context changes act exactly as
  declared, and the engine does not reproduce graph centrality. It also says the engine's value on this task reduces to
  one declared feature, that feature underperforms the raw scalar it is built from, and the relationship and stance
  machinery contribute nothing measurable.
- It does not say that ASA or ASTRO have no value on tasks where relationships carry information; this task's
  relationships (one endorsed `hosts` edge per candidate) are constant by construction of the candidate rule. It does
  not say ExoClock's priority is fully predictable from these inputs: the label's recency component is invisible to
  every method here.
- Reference truth caveats: ExoClock priority mixes projected uncertainty with observation recency; 61 planets were
  removed for leakage; the primary sample has only two "alert" planets.

## 9. Reproduction

```
PYTHONPATH=src python3 tools/realdata_exp0001.py verify        # dataset digests
PYTHONPATH=src python3 tools/realdata_exp0001.py run           # rebuilds universe + kernel, re-evaluates, rewrites results/
PYTHONPATH=src python3 tools/realdata_exp0001.py adversarial
PYTHONPATH=src python3 -m unittest tests.astro.test_realdata
```
`fetch` and `select` are needed only to re-derive the frozen extract from live sources; a re-fetch of the live sources
is expected to differ and would constitute a new dataset version.
