# ASTRO-EXEC-001 — Astronomy Execution Engine
## Constitutional Engineering Blueprint

| Field | Value |
|---|---|
| Identifier | `ASTRO-EXEC-001` |
| Title | Astronomy Execution Engine — Engineering Blueprint |
| Status | **Blueprint. Not approved. No implementation authorised.** |
| Date | 2026-08-02 |
| Repository | `17th2nd/ASA-Astro`, branch `main` |
| Baseline commit inspected | `25d7c58c3059d5d97cd2c622176206de34eb5f03` |
| Purpose | Define the software system that executes `ASTRO-EXP-0001@1.0` exactly as written |
| Evidence level at issue | `EH-0`. No experiment has been executed |

**Companion artefacts.** [Requirements Traceability](ASTRO-EXEC-001-REQUIREMENTS-TRACEABILITY.md) · [Unresolved Requirements](ASTRO-EXEC-001-UNRESOLVED-REQUIREMENTS.md) · [Technology Decision](ASTRO-EXEC-001-TECHNOLOGY-DECISION.md) · [Manufacturing Roadmap](ASTRO-EXEC-001-MANUFACTURING-ROADMAP.md) · [Operator Allocation](ASTRO-EXEC-001-OPERATOR-ALLOCATION.md) · [Risk Register](ASTRO-EXEC-001-RISK-REGISTER.md) · [Acceptance Gates](ASTRO-EXEC-001-ACCEPTANCE-GATES.md)

---

## 1. Executive engineering definition

`ASTRO-EXP-0001` is a **solar-system dynamics experiment**. It asks one question: does a frozen ASA estimator, calibrated on 27 Gaia DR3 main-belt asteroids, transfer to 27 disjoint near-Earth asteroids and select a materially better four-perturber reduced dynamical model than direct leave-one-perturber-out analysis, on at least 20 of 27 targets?

The engine's job is to make that measurement, exactly once, with provenance sufficient to survive adversarial review, and to record the outcome — positive or negative — in an append-only ledger.

The engine is a **measurement apparatus**, not a research tool. Its correctness criterion is not "produces a good result" but "produces the result the frozen protocol defines, and can prove it did".

### 1.1 The two findings that shape this blueprint

Phase 0 inspection of authoritative `main` produced two findings that dominate every downstream decision. Both are stated here rather than buried, because a blueprint written without them would be fiction.

**Finding 1 — the existing codebase does not implement this experiment and is largely not reusable.**

`src/asa_astro/` is an image-processing and graph-centrality pipeline: it ingests a PPM image, detects regions, builds a candidate graph, and computes eigenvector/betweenness-based "standing" and "significance". `ASTRO-EXP-0001` requires numerical orbit determination, N-body propagation with relativistic corrections, and JPL ephemeris handling. These are disjoint problem domains. The existing module's own docstring states its formulas are *"replaceable ASA-Astro hypotheses"* consumed *"without asserting ASA conformance"* — it is explicitly not the frozen theory's deterministic significance, and it is not an implementation of `ASTRO-EXP-0001`.

Reusable: repository conventions, `schemas/` patterns, canonical-JSON and content-hashing habits, provenance discipline, test layout. **Not reusable**: detection, image pipeline, candidate graph, the centrality-based standing/significance engine, `validation/run_phase2.py`.

**Finding 2 — the object under test does not exist.**

`ASTRO-EXP-0001` tests "one fully specified ASA estimator" and requires the ASA laboratory to *deposit a complete scientific specification of one estimator … and a cryptographic digest of that frozen specification*. **No such specification exists in the repository.** Furthermore, `ASTRO-EXP-0001`, `ASTRO-CLAIMS-0001` and `ASTRO-RESULTS-0001` contain **zero references** to `ASTRO-THEORY-0001` or to any path under `docs/theory/` — mechanically verified. The frozen theory and the frozen experiment are formally disjoint instruments.

Consequently there is no authoritative mapping from the theory's deterministic significance $\sigma_C(b)$ to the experiment's required output — four distinct `SB441-N16` identifiers per target. **This is recorded as blocking unresolved requirement `UR-001` and is not invented here.**

### 1.2 What this means for sequencing — the decisive scoping decision

The estimator gap does **not** block most of the engine. Of the four protocol roles, three are completely specified by the frozen protocol and can be manufactured now:

| Role | Specified by frozen protocol? | Buildable now? |
|---|---|---|
| Protocol custodian — manifest freeze, eligibility, ordering, salt application | **Yes, completely** | **Yes** |
| Truth laboratory — posterior draws, propagation, LOO comparator, endpoint, resolution $\delta_t$ | **Yes, completely** | **Yes** |
| Independent statistician — $W$, exact binomial, publication set | **Yes, completely** | **Yes** |
| ASA laboratory — the estimator | **No. `UR-001`** | **No** |

The engine is therefore architected so that the ASA estimator is a **replaceable, digest-pinned plug-in behind a narrow interface**, and everything else is built and validated against it being absent. This is not a workaround; it is the correct architecture for a blinded experiment, where the estimator must be sealed and swappable without touching the apparatus.

**The apparatus can reach full validation, including negative controls and self-replay, before `UR-001` is resolved.** Only Phase 10 — the deployment measurement — is gated on it.

---

## 2. Authoritative input inventory

Verified present on `main` at `25d7c58c`. Digests are Git blob identities.

| Artefact | Path | Blob | Status |
|---|---|---|---|
| `ASTRO-THEORY-0001` | `docs/theory/ASTRO-THEORY-0001.md` | `f6b4337e617a426fe1b62528272bc11bb8bda28f` | Frozen V1; Part A frozen, Part B Candidate |
| `ASTRO-EXP-0001` | `validation/benchmarks/ASTRO-EXP-0001.md` | `8b6606947421cfa96a572bb45726be4d4f3e51ce` | Frozen `1.0`; **primary requirements source** |
| `ASTRO-CLAIMS-0001` | `docs/claims/ASTRO-CLAIMS-0001.md` | `f1b4d94527cec10c650358036a0009bd5e4e46cc` | Frozen; 72 claims; `0070`–`0072` under test |
| `ASTRO-RESULTS-0001` | `validation/results/ASTRO-RESULTS-0001.md` | `c1a3739119bd56e5cdf745243970f78e0848848d` | Frozen; ledger tip `AR1-E000003`; `EH-0` |
| Research-controls freeze | `reports/ASTRO-V1-RESEARCH-CONTROLS-FREEZE-REPORT.md` | `d0b57c90af5009300a0d6ce5cd8de26bce3009c6` | Frozen |
| Theory freeze record | `docs/theory/ASTRO-THEORY-0001-V1-FREEZE-RECORD.md` | `0883e3171af6…` | Frozen V1 |

**Integrity control.** The engine MUST verify these blobs at every run start and refuse to execute on a mismatch (`FrozenArtefactDrift`). The theory's mathematical-body digest `383a9a8bf1d1d19a230caa79b3febcf6abddf293b6d83ed697cdf0dcf20c16c1` is recorded for completeness; note §1.1 Finding 2 — no current execution path consumes the theory.

---

## 3. Extracted executable requirements

Full mapping in the [Requirements Traceability](ASTRO-EXEC-001-REQUIREMENTS-TRACEABILITY.md) artefact. Summary of the binding numbers, all from `ASTRO-EXP-0001`:

| Quantity | Value | Source |
|---|---|---|
| Deployment targets | 27, plus 10 ordered reserves | §Target population |
| Calibration targets | 27 main-belt | §Calibration environment |
| Candidate perturbers | 16, from JPL `SB441-N16` | §The single experiment |
| Terms retained by each method | Exactly 4, distinct | §The single experiment |
| Posterior draws per target | 32, Sobol points 2–33, 6-D | §Ground truth |
| Epoch grid | Daily, $k=0..7305$ | §Primary endpoint |
| Window | 2017-07-01 00:00 TDB → 2037-07-01 00:00 TDB | §Primary endpoint |
| Frames / units | Barycentric ICRF3; kilometres; TDB | §Primary endpoint, §Ground truth |
| Materiality | $E_{ASA}(t)+\delta_t \le 0.80\,E_{LOO}(t)$ | §Primary endpoint |
| Resolution | $\delta_t = 3\times$ largest change under tightened accuracy | §Primary endpoint |
| Success | $W \ge 20$ | §Primary endpoint |
| Exact one-sided $p$ at $W{=}20$ | `0.0095786452293396` | §Statistical analysis |
| Power at $p{=}0.8$ | `0.8444402928110182` | §Statistical analysis |
| Force model | Newtonian point-mass: Sun, Moon, 8 planets, Pluto, 16 asteroids; EIH 1PN with $\beta=\gamma=1$; **no nongravitational terms** | §Ground truth |
| Propagation budget | ≈20,000 twenty-year test-particle propagations | §Cost and duration |

**Endpoint, normative form.** For method $m$ and target $t$:

$$E_m(t)=\operatorname{median}_{q=1..32}\ \max_{k=0..7305}\ \left\|\mathbf r_{full,q}(t_k)-\mathbf r^{(4)}_{m,q}(t_k)\right\|$$

**Comparator, normative form.** For candidate $j$: $L_j=\operatorname{median}_q \max_k \|\mathbf r_{full,q}(t_k)-\mathbf r_{-j,q}(t_k)\|$; rank decreasing $L_j$; ties broken by **increasing permanent number**; retain top 4. No fitted parameter.

**Ordering rules.** Calibration order: SHA-256 of `ASTRO-EXP-0001-CAL-v1 | number`, hex ascending. Deployment order: SHA-256 of `salt | ASTRO-EXP-0001-DEP-v1 | number`. `number` is the decimal permanent number without leading zeroes. The exact byte encoding of the separator and salt is **`UR-004`**.

---

## 4. System architecture

### 4.1 Role partition — the primary architectural driver

`ASTRO-EXP-0001` §Blind protocol mandates four separated roles and forbids outcome leakage to the ASA laboratory before its 27 selections are sealed. **This is a software architecture requirement, not a procedural one.** The engine is partitioned into four independently executable role applications over a shared core, communicating only through **sealed, digest-committed archives**.

```
                  ┌──────────────────────────────────────────┐
                  │  astro-core  (shared, no role authority)  │
                  │  ids · canonical JSON · hashing · config  │
                  │  provenance · manifest · logging · errors │
                  └──────────────────────────────────────────┘
                       ▲          ▲            ▲          ▲
        ┌──────────────┘          │            │          └──────────────┐
        │                         │            │                         │
┌───────┴────────┐   ┌────────────┴───┐  ┌─────┴──────────┐   ┌──────────┴─────┐
│  custodian     │   │  truthlab      │  │  asalab        │   │  statistician  │
│                │   │                │  │                │   │                │
│ dataset freeze │   │ posterior      │  │ SEALED PLUGIN  │   │ opens archives │
│ eligibility    │   │ propagation    │  │ estimator      │   │ computes W     │
│ ordering/salt  │   │ LOO comparator │  │ 4 ids/target   │   │ binomial p     │
│ apparatus chks │   │ δ_t resolution │  │  (UR-001)      │   │ ledger event   │
└────────────────┘   └────────────────┘  └────────────────┘   └────────────────┘
        │                    │                   │                     │
        └──── sealed archive ┴─── sealed archive ┴─────────────────────┘
                   (content-addressed, digest-committed)
```

**Information barrier, enforced in software.** The `asalab` application is given a filesystem/API view containing only the inputs declared at calibration. It has **no import path** to truth-laboratory outputs. Its selection archive is sealed and digest-published before `truthlab` runs the ASA-selected reduced models. A `LeakageGuard` in `astro-core` fails closed if a role process opens a path outside its declared capability set.

**Why this matters more than it looks.** A monolithic engine that computes everything in one process cannot demonstrate the blind held. Under an F1 integrity challenge, the only defence is architectural: the ASA selections were digest-committed before the comparator archive was opened, and the digests are in the published record.

### 4.2 Execution pipeline

The mission pipeline in the programme brief maps onto `ASTRO-EXP-0001` as follows. Where a named stage has no counterpart in the frozen protocol, that is recorded rather than invented.

| Brief stage | ASTRO-EXP-0001 realisation | Module |
|---|---|---|
| Version-pinned input data | Gaia DR3 SSO, DE440, SB441-N16, Horizons check | Dataset Registry, Manifest Manager |
| Registered observations and evidence | Gaia transits, error model, per-target eligibility facts | Evidence Pipeline |
| Resolved entities | Asteroid = permanent minor-planet number. Resolution is **exact by number**, not inferential | Entity Manager (thin) |
| Relationship graph | Target × 16 candidate perturbers, with LOO effect $L_j$ as edge weight | Perturber Relation Set (thin, see §5.6) |
| Declared experimental context | Force model, epoch grid, frames, budget, thresholds | Context Engine |
| Standing | **No counterpart in `ASTRO-EXP-0001`. `UR-002`** | — |
| Deterministic significance | **No counterpart. The estimator is the only scoring step. `UR-001`** | Estimator Interface |
| Experimental outputs | $E_{ASA}$, $E_{LOO}$, $\delta_t$, rankings, selections | Truth Laboratory |
| Metrics and validation findings | $W$, ratios, apparatus checks, convergence | Metrics, Validation |
| Empirical results | Run package | Result Generator |
| Claims comparison | vs `ASTRO-CLM-0070/0071/0072` | Claim Comparator |
| Append-only ledger entry | `AR1-E…` candidate events | Ledger Writer |

### 4.3 Repository structure

```
src/
  astro_exec/
    core/          ids, canonical_json, hashing, config, provenance,
                   manifest, logging, errors, leakage_guard, determinism
    data/          registry, acquisition, cache, preprocess, gaia/, jpl/
    orbits/        state, frames, timescales, posterior (Sobol+Cholesky),
                   forcemodel, integrator (Rust FFI), propagate
    experiment/    eligibility, ordering, apparatus, controller,
                   comparator, endpoint, resolution
    estimator/     interface.py  (ABI only — no implementation; UR-001)
    analysis/      metrics, statistics, validation, claims
    results/       run_package, report, ledger_candidate
    roles/         custodian.py, truthlab.py, asalab.py, statistician.py
    cli/           astro_exec entry points
crates/
  astro_integrator/   Rust: EIH N-body integrator, deterministic FP
docs/execution/       this blueprint and companions
tests/exec/           unit, contract, integration, replay, negative, injection
validation/fixtures/exec/   reference fixtures, synthetic negative controls
```

`src/asa_astro/` is **left untouched**. It serves a different, historical purpose; deleting or refactoring it is out of scope for `ASTRO-EXEC-001` and would disturb the Phase-01 POC review corpus.

---

## 5. Module breakdown

Every module below carries the full contract required by the brief §10 in the [Requirements Traceability](ASTRO-EXEC-001-REQUIREMENTS-TRACEABILITY.md) companion. This section gives purpose, sole responsibility, explicit non-responsibilities, and the determinism/provenance obligations that differentiate them.

### 5.1 Input Manager
**Sole responsibility:** admit input into a run only through a frozen manifest reference. **Non-responsibilities:** acquisition, parsing, validation of scientific content. **Determinism:** refuses any input not in the run manifest. **Failure:** `UnmanifestedInput` — fail closed, never warn-and-continue.

### 5.2 Dataset Registry
**Sole responsibility:** record identity, source locator, retrieval time, release identifier, licence, and content digest of every dataset. **Non-responsibilities:** downloading, preprocessing, interpreting. **Provenance:** every dataset gets a permanent `DS-…` id; digests are SHA-256 over canonical bytes. Satisfies `ASTRO-EXP-0001` §Datasets manifest-freeze requirement.

### 5.3 Dataset Manifest Manager
**Sole responsibility:** produce the immutable per-run manifest — every source locator, retrieval time, release identifier, cryptographic digest, plus the 32 posterior state vectors and their unit-cube Sobol source points, which §Ground truth requires be published **before either deployment selection**. **Non-responsibilities:** deciding which datasets are scientifically appropriate.

### 5.4 Evidence Pipeline
**Sole responsibility:** turn admitted Gaia records into typed evidence — transits, epochs, covariances, eligibility facts — with provenance. **Explicit non-responsibility: generates no significance, no ranking, no score.** **Negative test:** an evidence record that carries a score fails the contract test.

### 5.5 Entity Manager (thin, by design)
**Sole responsibility:** identity of an experimental object = its permanent minor-planet number. **Deliberately thin.** `ASTRO-EXP-0001` eligibility rule 1 requires a permanent number, so entity resolution is **exact lookup, not inference**. Building a probabilistic astronomical entity-resolution subsystem here would be inventing a requirement. Recorded as a scope decision, not an omission.

### 5.6 Perturber Relation Set (replaces "Relationship Graph")
**Sole responsibility:** for each target, hold the 16 candidate relations and their measured LOO effect $L_j$, provenance, and rank. **Assessment:** the brief's generic "Relationship Graph" module has no counterpart in `ASTRO-EXP-0001` beyond this fixed 16-element structure. A graph database or NetworkX dependency is **not justified**; the structure is a 27×16 table. Recorded as a deliberate simplification with rationale in the [Technology Decision](ASTRO-EXEC-001-TECHNOLOGY-DECISION.md).

### 5.7 Context Engine
**Sole responsibility:** load, validate and freeze the declared experimental context — force model composition, PPN parameters, epoch grid, frames, time scales, four-term budget, 20 % materiality threshold, $W\ge20$ rule. **Non-responsibility:** choosing any of them. Every value traces to a protocol section or fails validation.

### 5.8 Standing Engine — **not built for Version 1**
`ASTRO-EXP-0001` contains no Standing concept, no Standing input, and no Standing output. Building one would be inventing an experimental requirement. Recorded as **`UR-002`**. The existing `compute_standing` in `src/asa_astro/reasoning/engine.py` is POC-grade and non-conformant by its own docstring; it is not promoted.

### 5.9 Estimator Interface — **interface only, implementation blocked**
**Sole responsibility:** define the sealed ABI the frozen ASA estimator must satisfy:

```python
class FrozenEstimator(Protocol):
    spec_digest: str                      # digest of the deposited specification
    def select(self, target: TargetInputs) -> tuple[int, int, int, int]:
        """Return exactly 4 distinct SB441-N16 identifiers. Deterministic.
        MUST NOT access truth-laboratory outputs."""
```

Required by §Deployment environment: exactly four distinct identifiers, for **every** admissible input, deterministically; abstention or duplicates count as non-wins (§Stopping rules 5). The interface is buildable now; the implementation is **`UR-001`**.

### 5.10 Truth Laboratory
**Sole responsibility:** the four propagation classes of §Ground truth — 1 full, 16 single-deletion, 1 ASA-selected, 1 comparator-selected, per target per draw — plus tightened-accuracy repeats for $\delta_t$. **Non-responsibility:** it never sees ASA selections until they are sealed, and never alters an earlier input, comparator result, tolerance or trajectory (§Blind protocol).

### 5.11 Experiment Controller
**Sole responsibility:** sequence custodian → calibration → freeze → salt → deployment → seal → open → analyse, enforcing the stopping rules and the one-look constraint. **Critical invariant:** *there is no interim look*. The controller must make an interim look **impossible**, not merely discouraged.

### 5.12 Metrics Engine
**Sole responsibility:** compute only authorised quantities — $E_m(t)$, $L_j$, $\delta_t$, $W$, ratios $E_{ASA}/E_{LOO}$. **Non-responsibility:** no metric may be added because it is interesting. §Secondary endpoints says: **None.** Diagnostics are published but cannot qualify the decision.

### 5.13 Validation Engine
**Sole responsibility:** apparatus checks 1–4 (§Apparatus checks), schema/integrity/determinism/replay checks, negative controls, and the F0–F3 failure classification. **Failure classification is a first-class output**, not an error path.

### 5.14 Result Generator, 5.15 Claim Comparator, 5.16 Ledger Writer
Result Generator emits the immutable run package (§8). Claim Comparator evaluates the frozen conditions of `ASTRO-CLM-0070/0071/0072` and **never rewrites a claim**. Ledger Writer produces a **candidate** `AR1-E…` event conforming to the §4 envelope, honouring `INV-R01`–`INV-R12`, and implements the §17 serialized-allocation procedure against canonical `origin/main` including the fast-forward-retry rule. **It proposes; a human appends.**

### 5.17–5.20 Visualisation Interface · Configuration Manager · Telemetry · Logging · Reproducibility Manager
Visualisation is a **read-only export boundary** (§9) — no engine module may import a renderer. Configuration is loaded, validated, frozen and fingerprinted; the fingerprint enters provenance. Telemetry is bounded operational measurement written to a separate stream that **cannot** reach scientific outputs. Logging is structured, severity-classified, run-associated. Reproducibility Manager captures software, environment, dataset, dependency, configuration, seed and artefact identity sufficient for exact replay.

---

## 6. Determinism contract

**Guarantee.** Given identical engine version, frozen-artefact digests, dataset digests, preprocessing version, configuration fingerprint, context, Sobol construction, dependency lock and execution mode, the engine produces **byte-identical** authoritative outputs.

| Concern | Policy |
|---|---|
| Floating point | IEEE-754 binary64 throughout. Integrator compiled with strict FP; **fast-math and FMA contraction forbidden**. No `-ffast-math`, no reassociation. |
| Summation | Deterministic compensated (Neumaier) summation in force accumulation; fixed accumulation order by body index. |
| Reductions | $\max_k$ and $\operatorname{median}_q$ computed in fixed index order. Median of 32 = mean of sorted elements 16 and 17, stated explicitly. |
| Concurrency | Parallelism only across independent (target, draw) units. **No parallel reduction into shared accumulators.** Results merged in canonical index order, so output is independent of completion order. |
| Random numbers | **None.** Sobol is deterministic; the deployment salt is an external published constant, not generated at run time by the engine. |
| Serialization | Canonical JSON: UTF-8, sorted keys, no insignificant whitespace, `float` emitted via shortest round-trip repr. Parquet with pinned writer version and fixed row order. |
| Identifiers | Derived by SHA-256 over canonical field bytes — never from time, hostname, PID or memory address. |
| Time | All internal computation in TDB. Wall-clock appears only in provenance `recorded_at`, never in a scientific value. |
| Ordering | Every collection serialized in a declared canonical order — targets by permanent number, perturbers by `SB441-N16` index, epochs by $k$. |
| Platform | Byte-identical guaranteed on a pinned reference platform. Cross-platform: **semantic equivalence** — every target-level $E_m(t)$ within the registered $\delta_t$, and identical selections and identical $W$. |

**Justified non-byte-identical output.** Cross-architecture floating-point differences in transcendental library calls cannot be eliminated without vendoring a correctly-rounded math library. The engine therefore declares selections, $W$, and the decision as the byte-identical contract, and $E_m(t)$ as semantically equivalent within $\delta_t$. **If a cross-platform run changes any selection or $W$, that is a determinism defect, not a tolerance.**

---

## 7. Provenance model

Every authoritative value traces to run, dataset, dataset version and digest, source record, evidence item, entity, relation, context, configuration, software and dependency versions, frozen-artefact versions, and validation status. Provenance is a **content-addressed DAG** serialized as canonical JSON; each node id is the SHA-256 of its canonical content, so the graph is self-verifying and duplicate-free.

**No result may exist without provenance.** The Result Generator refuses to emit any authoritative value whose provenance chain does not terminate at registered dataset digests. Queryable by node id, ancestor traversal, and full-run export.

---

## 8. Run package

```
runs/<run-id>/
  manifest.json            frozen dataset manifest + posterior states + Sobol points
  config.snapshot.json     frozen configuration + fingerprint
  environment.json         OS, CPU, toolchain, dependency lock digest
  frozen-artefacts.json    digests of THEORY/EXP/CLAIMS/RESULTS at run start
  evidence/                typed evidence records
  entities/                target records
  relations/               per-target 16 candidate relations + L_j
  context.json             frozen experimental context
  selections/
    asa.sealed.json        + asa.digest        (sealed before truth opens)
    comparator.sealed.json + comparator.digest
  truth/                   E_full, E_LOO, E_ASA, δ_t per target/draw
  metrics/                 W, ratios, per-target table
  validation/              apparatus checks, controls, F-class, findings
  claims/                  comparison vs CLM-0070/0071/0072
  ledger/                  AR1-E… candidate event (proposal only)
  provenance/              provenance DAG
  logs/                    structured logs
  telemetry/               bounded operational measures
  reports/                 human-readable
  CHECKSUMS.sha256
```

**Artefact classification is mandatory and machine-readable.** Each file carries a class: `authoritative-scientific` · `diagnostic` · `visualisation` · `cache` · `temporary` · `log` · `human-report`. Only `authoritative-scientific` may be cited as empirical evidence. Caches and temporaries are written outside the run package entirely.

---

## 9. Rendering independence

The engine has **no rendering dependency**, and no engine module may import one. Visual consumers — Godot, Unity, browser, desktop — read exported run packages through a stable read-only interface and **cannot** compute significance, modify scientific state, generate evidence, alter context, replace validation, or write to the ledger. Adapter specifications are Phase 9 and are deliberately deferred; specifying them before the data model stabilises would be premature.

---

## 10. Technology selection (summary)

Full assessment, including the candidates rejected and why, in the [Technology Decision](ASTRO-EXEC-001-TECHNOLOGY-DECISION.md).

| Layer | Selection |
|---|---|
| Primary language | **Python 3.12** — orchestration, data, analysis, CLI, results |
| Secondary language | **Rust** — one bounded crate: the EIH N-body integrator |
| Storage | **Parquet** trajectories/tables · **SQLite** run index · **canonical JSON** manifests and results |
| Graph | Plain typed structures. **No graph DB, no NetworkX** |
| Config | TOML in, canonical JSON snapshot out |
| Tests | `pytest` + `cargo test` |
| Dependencies | `uv` lock + `Cargo.lock`, fully pinned |
| CLI | `argparse` — no heavyweight CLI framework |

**Rationale for two languages.** ≈20,000 twenty-year propagations at daily output with 26 bodies and 1PN corrections is not tractable in pure Python, and byte-level FP determinism requires control that NumPy's threaded BLAS does not give. Rust supplies both, in a single small crate with a narrow FFI surface. Everything else stays Python, matching existing repository practice. Rejected: pure C++ (weaker dependency reproducibility), pure Python (too slow, FP control insufficient), DuckDB/graph DBs/Arrow-as-storage (unjustified for a 27×16 problem).

---

## 11. Testing, validation and reproducibility

Every module requires unit, contract, integration, deterministic-replay, negative, malformed-input, missing-data, provenance-integrity, failure-injection and reproducibility tests. The complete engine additionally requires clean-environment execution, fresh-clone reproduction, dependency-lock verification, fixture reference runs, cross-platform comparison, control and ablation verification, ledger-generation and claims-comparison validation, mutation-boundary tests, and frozen-artefact integrity tests.

**Scientific validation beyond software correctness:**

- **Two-body analytic check** — Kepler orbit reproduced to integrator tolerance.
- **Energy/momentum drift** bounded over 20 years.
- **Horizons agreement** — apparatus check 2, within 1 km at start/mid/end.
- **Known-answer LOO** — synthetic system where the four dominant perturbers are analytically known; the comparator must recover exactly those four.
- **Negative control** — an estimator returning fixed or shuffled selections must **not** produce $W\ge20$. If it does, the apparatus is broken.
- **Blind-integrity test** — a deliberate attempt to read truth outputs from `asalab` must fail closed.

**The most important test class.** Tests must validate **frozen scientific intent**, not implementation behaviour. Every scientific test cites the `ASTRO-EXP-0001` section it enforces. A test whose only justification is "this is what the code does" is rejected at review.

---

## 12. Error and failure model

Failure is a first-class output. Exceptions map to protocol classes:

| Engine condition | Protocol class | Behaviour |
|---|---|---|
| Target pool cannot be formed; unstable measurement | **F0** | `FAILED_EXPERIMENT`; no effect estimated |
| Leakage, unequal undeclared inputs, unfrozen estimator change, post-unblind exclusion | **F1** | `INVALID` or `FAILED_EXPERIMENT`; publish the breach |
| Valid run, $W\le19$ | **F2** | `NEGATIVE`; record `ASTRO-CLM-0072`; terminal |
| Replication fails | **F3** | `INCONSISTENT`/`FAILED_EXPERIMENT`; withdraw claim |

Engine-internal faults (I/O, arithmetic, corruption) are **never** silently mapped to a scientific class; they abort with `EXECUTION_ABORTED` and preserved evidence (`INV-R01`, §17 step 4).

---

## 13. Security and integrity

Sealed archives use SHA-256 digests published before opening. Frozen artefacts are digest-verified at run start. The ledger is append-only with a `previous_event_id` chain validated end-to-end. The deployment salt is an external witnessed constant supplied to the engine, never generated by it. Network access is disabled by default; acquisition runs in an explicit, separately-invoked, digest-recording mode. No credential, token or personal datum enters a run package.

---

## 14. Performance strategy

Target: full deployment measurement within days on one workstation, not weeks.

The decisive optimisation is **streaming reduction**: $E_m(t)$ needs only $\max_k\|\Delta\mathbf r\|$, so reduced-model propagations are stepped in lockstep with the stored full trajectory and the maximum accumulated on the fly. Full trajectories are stored (27 × 32 × 7306 × 3 × 8 B ≈ 151 MB); the 16 deletion runs per target-draw are **not** stored, only their scalar $L_j$. This converts a ~3 TB storage problem into ~200 MB.

Parallelism is across independent (target, draw) units only, with canonical-order merge, so speed never affects the result. **No optimisation may alter numerical output**; any change to summation order, tolerance or step control is a determinism change requiring re-validation.

---

## 15. Roadmap, operators, risks, gates

Bounded phases, prerequisites, deliverables and blocking conditions: [Manufacturing Roadmap](ASTRO-EXEC-001-MANUFACTURING-ROADMAP.md). Component ownership, interface contracts and conflict-prevention: [Operator Allocation](ASTRO-EXEC-001-OPERATOR-ALLOCATION.md). Likelihood, consequence, detection, mitigation, owner and blocking threshold per risk: [Risk Register](ASTRO-EXEC-001-RISK-REGISTER.md). Evidence-defined milestones and gate criteria: [Acceptance Gates](ASTRO-EXEC-001-ACCEPTANCE-GATES.md).

**Phase summary.** P0 artefact inspection *(complete — this blueprint)* · P1 blueprint *(this document)* · P2 execution skeleton · P3 dataset and evidence · P4 relations and context · P5 orbital core · P6 experiment execution · P7 validation and claims · P8 results and ledger · P9 external interfaces · P10 first controlled empirical run **(gated on `UR-001`)**.

---

## 16. Unresolved requirements

Full register with impact and proposed resolution route: [Unresolved Requirements](ASTRO-EXEC-001-UNRESOLVED-REQUIREMENTS.md).

| Id | Issue | Severity |
|---|---|---|
| **`UR-001`** | The frozen ASA estimator specification does not exist; no authoritative mapping from `ASTRO-THEORY-0001` to four-perturber selection | **Blocking for P10 only** |
| `UR-002` | "Standing" has no counterpart in `ASTRO-EXP-0001` | Scope — not built |
| `UR-003` | Gaia DR3 orbit-fitting depth: the protocol requires a full six-dimensional fit with covariance, but does not specify the estimator, weighting or outlier policy | **Blocking for P3/P5** |
| `UR-004` | Exact byte encoding of the SHA-256 ordering pre-images (separator, salt encoding, whitespace) | Blocking for P3 |
| `UR-005` | Integrator, step control and tolerance pair for "tightened numerical accuracy" unspecified | Blocking for P5 |
| `UR-006` | Sobol generator variant, direction numbers and whether point 1 is the origin | Blocking for P5 |
| `UR-007` | Horizons capture/replay policy for apparatus check 2 | Blocking for P3 |
| `UR-008` | Theory–experiment disjunction: no artefact connects the frozen theory to the frozen experiment | Programme-level |

**None of these is repaired by invention.** Each requires a custodian ruling recorded as an approved engineering decision, or a superseding scientific instrument.

---

## 17. Success condition

`ASTRO-EXEC-001` succeeds when ASA-Astro holds a published, internally consistent, requirements-traceable engineering programme from which multiple operators can manufacture the engine without redesigning the science, inventing experimental requirements, duplicating existing work, fragmenting repository authority, introducing nondeterministic integration, relying on private conversation context, or producing results without provenance.

Until the frozen Version 1 programme is executed and passes its validation requirements, the empirical evidence level remains **`EH-0`**.

**This blueprint authorises no implementation.** Implementation begins only after explicit human approval of this blueprint and of the first bounded manufacturing package.
