# ASTRO-EXEC-001 — Unresolved Requirements Register

Engineering requirements that **cannot be established from an authoritative artefact**. Each is recorded rather than invented, as required by the programme brief §3 and §4.

**Rule.** No entry here may be closed by an implementation operator choosing a reasonable answer. Closure requires either (a) a custodian ruling recorded as an approved engineering decision in this repository, or (b) a superseding scientific instrument. Until closed, any code path that would need the answer must fail closed with an explicit `UnresolvedRequirement` error naming the `UR` id.

| Id | Title | Severity | Blocks |
|---|---|---|---|
| `UR-001` | Frozen ASA estimator specification does not exist | **Blocking** | Phase 10 only |
| `UR-002` | "Standing" has no counterpart in the frozen experiment | Scope | Nothing — module not built |
| `UR-003` | Gaia orbit-fit estimator, weighting and outlier policy unspecified | **Blocking** | Phases 3, 5 |
| `UR-004` | Byte encoding of ordering pre-images unspecified | **Blocking** | Phase 3 |
| `UR-005` | Integrator, step control and "tightened accuracy" pair unspecified | **Blocking** | Phase 5 |
| `UR-006` | Sobol variant and indexing convention unspecified | **Blocking** | Phase 5 |
| `UR-007` | Horizons capture and replay policy unspecified | **Blocking** | Phase 3 |
| `UR-008` | Theory and experiment are formally disjoint | Programme | Interpretation |
| `UR-009` | Ledger append authority and role identity unspecified | Moderate | Phase 8 |
| `UR-010` | Reserve-substitution ordering under multiple failures ambiguous | Moderate | Phase 6 |

---

## UR-001 — The frozen ASA estimator specification does not exist

**Evidence.** `ASTRO-EXP-0001` §Calibration environment: calibration "ends when the laboratory deposits a complete scientific specification of one estimator, all fitted quantities, its transformation from the permitted inputs to four selections, and a cryptographic digest of that frozen specification." §Deployment environment: it "must return exactly four distinct `SB441-N16` identifiers for every target."

No such specification exists in the repository. Mechanically confirmed: `ASTRO-EXP-0001`, `ASTRO-CLAIMS-0001` and `ASTRO-RESULTS-0001` contain **zero** occurrences of `ASTRO-THEORY` and zero references to any `docs/theory/` path. The frozen theory and the frozen experiment are formally disjoint instruments.

**Why this cannot be invented.** The experiment's entire scientific content is a test *of this estimator*. An engineer who supplies one is not implementing the experiment — they are silently authoring the hypothesis under test, and any resulting $W$ would measure the engineer's choice. That is an F1 integrity failure by construction.

**Consequence for the engine.** Bounded, and smaller than it first appears. The estimator is one plug-in behind a four-method interface (`astro_exec/estimator/interface.py`). The custodian, truth-laboratory and statistician roles — the great majority of the apparatus — are fully specified and can be manufactured and validated without it, using negative-control estimators (fixed selection, shuffled selection, mass-ranked selection) that **must not** achieve $W\ge20$.

**Resolution route.** A separate scientific instrument — e.g. `ASTRO-EST-0001` — depositing the estimator specification and its digest, produced by the ASA laboratory role, before any deployment execution. It must specify inputs consumed, the transformation to four selections, all fitted quantities, and determinism guarantees. **This is a scientific deliverable, not an engineering one.**

**Interim engine behaviour.** `select()` raises `UnresolvedRequirement("UR-001")` unless a digest-pinned estimator plug-in is registered. Negative-control estimators are permitted for apparatus validation and are **hard-flagged** as non-scientific: any run using one is stamped `apparatus-validation`, never `authoritative-scientific`, and cannot generate a ledger candidate.

---

## UR-002 — "Standing" has no counterpart in the frozen experiment

**Evidence.** `ASTRO-EXP-0001` contains no Standing concept, input, output or decision rule. The programme brief §9.8 requires a Standing Engine "according to the frozen Version 1 scientific contracts", but no frozen contract defines Standing for this experiment. The only implementation, `compute_standing` in `src/asa_astro/reasoning/engine.py`, is POC-grade and declares itself non-conformant.

**Decision.** **Not built for Version 1.** Building it would invent an experimental requirement. Recorded as a scope decision with rationale, not an omission. If the estimator specification (`UR-001`) turns out to consume a Standing quantity, this entry is reopened and Standing is specified *there*, as an estimator input, not as an independent engine concept.

---

## UR-003 — Gaia orbit-fit estimator, weighting and outlier policy unspecified

**Evidence.** §Ground truth requires "the full Gaia fit produces a six-dimensional state mean $\hat{\mathbf x}_t$ and covariance $C_t$ at the common start epoch". §Apparatus checks 1 requires fitting "the full dynamical model to the chronologically first 70% of the Gaia transits" with reduced $\chi^2\in[0.5,2.0]$ on the final 30% "under the published Gaia covariance model".

Unspecified: the estimation method (batch least squares, weighted least squares, sequential filter); the treatment of the within-transit systematic component of the Gaia error model relative to the random component; outlier rejection policy and threshold; convergence criterion; whether the fit is iterated with the dynamical model.

**Why it matters.** $C_t$ determines the Cholesky factor $L_t$, hence all 32 posterior draws, hence **every** reported error and the endpoint itself. Two defensible fitting choices give different $E_m(t)$ and can change $W$.

**Resolution route.** Custodian ruling specifying estimator, weighting, outlier policy and convergence, recorded as an approved engineering decision. **Must be fixed before the manifest is frozen**, since §Ground truth requires the 32 state vectors be published before either deployment selection.

---

## UR-004 — Byte encoding of ordering pre-images unspecified

**Evidence.** §Target population: order by "the hexadecimal SHA-256 digest of `ASTRO-EXP-0001-CAL-v1 | number`" and of `salt | ASTRO-EXP-0001-DEP-v1 | number`.

Unspecified: whether `|` is a literal pipe byte, a separator with surrounding spaces as printed, or notation; the encoding of `salt` (raw 32 bytes, lowercase hex, uppercase hex); string encoding (UTF-8 assumed but unstated); presence of a trailing newline; and whether the digest is compared as a hex string or as a big-endian integer — these differ in ordering only if compared as strings of unequal length, but the convention must still be fixed.

**Why it matters.** A different encoding yields a different permutation, hence a **different 27-target set**. Target selection is the one thing the protocol most carefully protects against manipulation; leaving it ambiguous is unacceptable.

**Resolution route.** Custodian ruling fixing the exact pre-image byte string, plus published test vectors: at least three worked `(number, digest)` pairs for the calibration rule and three for the deployment rule with a stated example salt. The engine implements the test vectors as contract tests.

---

## UR-005 — Integrator, step control and "tightened accuracy" pair unspecified

**Evidence.** §Primary endpoint: $\delta_t$ is set by "repeating the full and two selected-model propagations with **tightened numerical accuracy**" and taking three times the largest resulting change. §Apparatus checks 3 references "the numerical integration floor"; check 4 references "tightened numerical accuracy".

Unspecified: the integration scheme; step-size control; the nominal tolerance; the tightened tolerance; the definition of "integration floor"; whether output at daily epochs uses dense interpolation or forced steps.

**Why it matters.** $\delta_t$ enters the materiality test directly. A larger $\delta_t$ makes wins harder; a smaller one makes them easier. The tolerance pair is therefore **outcome-relevant** and cannot be an implementation preference.

**Engineering recommendation, for ruling not adoption.** Gauss–Radau (RADAU15) or an adaptive high-order integrator with dense output; nominal and tightened tolerances separated by ≥2 decades; "integration floor" defined as the maximum position change under tolerance tightening on the unperturbed full model. **Recorded as a proposal requiring custodian approval, not as a decision.**

---

## UR-006 — Sobol variant and indexing convention unspecified

**Evidence.** §Ground truth: "the second through thirty-third points $\mathbf u_q$ of the standard six-dimensional Sobol sequence".

Unspecified: which "standard" sequence — Joe–Kuo direction numbers are the common choice but are not named; whether the sequence is scrambled (it must not be, for reproducibility, but this is not stated); whether "the second point" means index 1 in 0-based indexing where index 0 is the origin $(0,\dots,0)$ — the natural reading, since the origin would map to the distribution mean and waste a draw.

**Why it matters.** Different direction numbers give different $\mathbf u_q$, hence different states, hence different errors. The protocol requires the unit-cube source points be published, which makes the convention auditable **after** the fact but does not fix it in advance.

**Resolution route.** Custodian ruling naming the direction-number set and indexing convention, with the 32 six-dimensional points published as test vectors.

---

## UR-007 — Horizons capture and replay policy unspecified

**Evidence.** §Datasets permits "JPL Horizons only for the apparatus check described below". §Apparatus checks 2 requires agreement with "the frozen JPL Horizons vectors to within 1 km".

Unspecified: how Horizons responses are captured, versioned, hashed, cached and replayed; which Horizons parameters are pinned (reference frame, aberration, centre, step); behaviour when Horizons is unreachable during replay.

**Why it matters.** The programme brief §11 is explicit: "Live network services must not become an invisible dependency of a supposedly reproducible experiment."

**Engineering recommendation, for ruling.** Capture once into a digest-registered fixture with full request parameters recorded; **all** subsequent runs, including replication, read the fixture; live access permitted only in an explicit `acquire` mode that writes a new registered dataset and never executes inside a measurement run.

---

## UR-008 — Theory and experiment are formally disjoint

**Evidence.** Zero cross-references in either direction, mechanically verified. The research-controls freeze report §3 independently determined that the theory records "do not materially alter a meaning, identifier, dependency, or status used by `ASTRO-EXP-0001`, `ASTRO-CLAIMS-0001`, or `ASTRO-RESULTS-0001`", and that none of the research-control records references `ASTRO-THEORY-0001`.

**Observation, not a defect.** The disjunction may be deliberate: `ASTRO-EXP-0001` §Purpose states that "mathematical novelty … and general architectural value are not tested", and the theory itself claims no empirical content. But it has a consequence that must be stated plainly:

> **A successful `ASTRO-EXP-0001` result would not, on the current artefacts, constitute evidence for `ASTRO-THEORY-0001`.** Nothing traces the estimator's behaviour to the frozen mathematics.

**Resolution route.** Either (a) `UR-001`'s estimator specification explicitly derives the selection rule from the frozen theory, creating the link; or (b) the programme records that Version 1 empirical work is deliberately independent of the frozen theory. Both are acceptable; leaving it unstated is not, because it invites later overstatement of what a positive result means.

---

## UR-009 — Ledger append authority and role identity unspecified

**Evidence.** `ASTRO-RESULTS-0001` §4 requires `recorded_by.name_or_stable_id`, `recorded_by.role` and `authority_or_basis` on every event. §17 serializes identifier allocation against canonical `origin/main`.

Unspecified for an automated engine: what stable id and role an engine-generated candidate carries; whether an engine may append at all, or only propose.

**Engine decision, recorded as an engineering position.** The Ledger Writer **only proposes**. It emits a candidate event with `recorded_by.role: "execution-engine"` and leaves `authority_or_basis` requiring human completion. A human appends. Rationale: `ASTRO-RESULTS-0001` §17.4 requires judgement on collision handling, and the ledger is the permanent scientific record. **Requires custodian confirmation.**

---

## UR-010 — Reserve-substitution ordering under multiple failures ambiguous

**Evidence.** §Apparatus checks: a failed check "is replaced by the next reserve". §Stopping rules 3: "replace an apparatus-invalid target only with the next ordered reserve." §Target population: "The next ten are ordered reserves."

Unspecified: whether a reserve that itself fails is replaced by the following reserve (natural reading) and whether the pool can therefore be exhausted below 27 + 10; whether substitutions are processed in target order or failure-detection order — these differ if checks run in parallel.

**Engine decision pending ruling.** Process substitutions deterministically in **ascending ordered position**, never in detection order; a failed reserve is replaced by the next unused reserve; if the ordered pool is exhausted, raise **F0** per §Stopping rules 2 rather than extending the pool. Deterministic and conservative, but **requires confirmation**.

---

## Closure procedure

1. Custodian issues a ruling citing the `UR` id and the protocol section it interprets.
2. The ruling is committed to this repository as an approved engineering decision with its own identifier.
3. This register is updated: status, ruling reference, and the date.
4. Contract tests encoding the ruling — including published test vectors where applicable — are added before the dependent module is implemented.
5. The [Requirements Traceability](ASTRO-EXEC-001-REQUIREMENTS-TRACEABILITY.md) matrix gains a row whose source is the ruling, not an inference.

**No `UR` entry is closed by implementation.**
