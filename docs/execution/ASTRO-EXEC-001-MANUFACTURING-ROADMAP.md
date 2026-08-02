# ASTRO-EXEC-001 — Manufacturing Roadmap

Bounded phases. Each defines prerequisites, scope, non-scope, deliverables, tests, acceptance criteria, commit boundary, remote verification and blocking conditions.

**Governing rules.** No phase begins before its prerequisite is published and verified on GitHub `main`. Milestones are defined by **achieved evidence on `main`**, never by calendar estimate. A phase is complete only when its evidence exists remotely.

---

## Phase 0 — Authoritative artefact inspection · **COMPLETE**

**Deliverables** — artefact inventory with blob digests; extracted requirements; unresolved-requirements register; gap analysis against the existing repository. **Published in this blueprint set.**

**Findings.** The existing `src/asa_astro/` implements a different problem domain and is largely not reusable. The frozen ASA estimator does not exist (`UR-001`). Theory and experiment are formally disjoint (`UR-008`). Nine requirements are blocked on custodian rulings.

---

## Phase 1 — Engineering blueprint · **THIS DOCUMENT SET**

**Acceptance:** human approval of the blueprint and of the first bounded manufacturing package. **Implementation is not authorised by publication of this phase.**

---

## Phase 2 — Execution skeleton

**Prerequisites:** Phase 1 approved.
**Scope:** `astro_exec.core` — identifiers, canonical JSON, hashing, config load/validate/freeze/fingerprint, provenance primitives, structured logging, error taxonomy, run lifecycle, run-package skeleton, frozen-artefact digest verification, `LeakageGuard`, role entry points, initial CLI.
**Non-scope:** all scientific computation; all dataset acquisition; the integrator.
**Deliverables:** package skeleton; canonical JSON serializer with contract tests; `astro-exec run --dry-run` producing a complete, empty, provenance-valid run package.
**Tests:** canonical-JSON determinism; identifier determinism; config fingerprint stability; frozen-artefact drift aborts the run; role capability isolation; two dry-run packages byte-identical except run id.
**Acceptance:** a dry run replays byte-identically on a fresh clone in a clean environment.
**Commit boundary:** one commit per bounded unit; skeleton published before Phase 3 starts.
**Blocking:** none. **This phase is fully unblocked and is the recommended first implementation package.**

---

## Phase 3 — Dataset and evidence foundation

**Prerequisites:** Phase 2 verified; rulings on `UR-004`, `UR-007`; ruling on `UR-003` before orbit fitting.
**Scope:** dataset registry; acquisition mode with digest recording; local cache; Gaia DR3 SSO ingestion; DE440 and SB441-N16 loading; Horizons capture-and-replay fixture; declared, versioned, deterministic preprocessing; evidence records; eligibility facts; ordering functions with published test vectors.
**Non-scope:** propagation; selection; endpoint.
**Deliverables:** `DS-…` registry; frozen manifest generator; ordering implementation matching the custodian's test vectors exactly.
**Tests:** unpermitted dataset rejected; release substitution blocked; ordering test vectors; eligibility all five rules; TCB→TDB conversion; acquisition never runs inside a measurement run.
**Acceptance:** a manifest is reproduced byte-identically from registered digests on a fresh clone with **no network access**.
**Blocking:** `UR-004` blocks ordering; `UR-007` blocks apparatus check 2; `UR-003` blocks the fit.

---

## Phase 4 — Relations and context

**Prerequisites:** Phase 3 verified.
**Scope:** per-target 16-candidate relation set; context loader with full validation against protocol sections; context freeze and fingerprint; provenance traversal and export.
**Non-scope:** computing $L_j$ — that needs the integrator.
**Deliverables:** context schema; validated frozen context; provenance DAG with query API.
**Tests:** every context value traces to a protocol section or validation fails; provenance completeness; no authoritative value without a chain to dataset digests.
**Acceptance:** context validation rejects a context missing the EIH term, altering the epoch grid, or changing the four-term budget.

---

## Phase 5 — Deterministic orbital core

**Prerequisites:** Phase 4 verified; rulings on `UR-005`, `UR-006`.
**Scope:** `crates/astro_integrator`; force model with EIH 1PN; singular deletion intervention; Sobol + Cholesky posterior construction; timescale and frame handling; streaming reduction; canonical trajectory serialization.
**Non-scope:** the experiment controller; the estimator.
**Deliverables:** integrator crate with FFI; posterior generator; propagation API.
**Tests:** two-body Kepler analytic check; energy/momentum drift bounds; EIH applied in every run; deletion is singular — exactly one term changes; Cholesky lower-triangular with positive diagonal; Sobol test vectors; byte-identical replay on the reference platform; cross-platform semantic equivalence.
**Acceptance:** reference fixture trajectories reproduce byte-identically; a known-answer synthetic system recovers its four dominant perturbers exactly.
**Blocking:** `UR-005`, `UR-006`. **These are outcome-relevant and must not be chosen by an implementer.**

---

## Phase 6 — Experiment execution

**Prerequisites:** Phase 5 verified; ruling on `UR-010`.
**Scope:** experiment controller; calibration and deployment sequencing; apparatus checks 1–4; LOO comparator with tie-break; sealing and digest publication; $\delta_t$; endpoint $E_m(t)$; stopping rules; single-unblinding enforcement.
**Non-scope:** the ASA estimator (`UR-001`); ledger append.
**Deliverables:** controller; comparator; resolution and endpoint calculators; sealed-archive mechanics.
**Tests:** LOO ranking and tie-break; exactly four distinct; abstention/duplicate/invalid counts as non-win; no pre-seal outcome access; no post-seal mutation; single unblinding; all seven stopping rules; substitution ordering.
**Acceptance:** a full end-to-end run completes using a **negative-control estimator**, is stamped `apparatus-validation`, and does **not** reach $W\ge20$. If a fixed or shuffled estimator does reach $W\ge20$, the apparatus is defective and the phase fails.

---

## Phase 7 — Validation and claims comparison

**Prerequisites:** Phase 6 verified.
**Scope:** validation engine; F0–F3 classification; negative controls; determinism and replay validation; exact binomial statistics; claim comparator against `ASTRO-CLM-0070/0071/0072`.
**Deliverables:** validation report generator; statistics module; claims comparison.
**Tests:** exact binomial equals `0.0095786452293396` at $W{=}20$; power equals `0.8444402928110182` at $p{=}0.8$; failure classification; forbidden-claim strings absent from every output; claims are read-only.
**Acceptance:** the statistics module reproduces both frozen constants to full stated precision, and the claim comparator emits the exact bounded wording for a simulated terminal outcome.

---

## Phase 8 — Results and ledger integration

**Prerequisites:** Phase 7 verified; ruling on `UR-009`.
**Scope:** immutable run package; artefact classification; checksums; human-readable report; ledger candidate generation implementing `ASTRO-RESULTS-0001` §4, §5.1, §16, §17 and `INV-R01`–`INV-R12`.
**Non-scope:** **appending to the ledger.** The engine proposes; a human appends.
**Deliverables:** run-package writer; ledger candidate generator with serialized allocation and fast-forward-retry.
**Tests:** envelope completeness; permitted event types only; result-definition gate; 14-item evidence package; allocation against canonical tip; never renumber or edit; artefact classification.
**Acceptance:** a candidate event validates against the ledger's own rules and chains correctly to `AR1-E000003`; a deliberately incomplete evidence package is held at `EH-1`.

---

## Phase 9 — External interfaces

**Prerequisites:** Phase 8 verified.
**Scope:** stable read-only programmatic API; inspection CLI; visualisation data interface; Godot and Unity adapter **specifications** only.
**Non-scope:** building any renderer.
**Acceptance:** the import-graph test proves no engine module imports a rendering library; the read API cannot mutate a run package.

---

## Phase 10 — First controlled empirical run

**Prerequisites:** Phases 2–9 verified; **`UR-001` closed** — a deposited, digest-pinned estimator specification exists; all other `UR` entries closed; the deployment salt generated in a witnessed ceremony and published.
**Scope:** execute the frozen experiment exactly once; validate reproducibility; independently replay; publish run evidence; prepare the ledger update.
**Acceptance:** the run completes with full provenance, replays independently within registered resolutions, and produces a valid ledger candidate — **whatever the value of $W$**.
**Blocking:** `UR-001`. **This is the only phase blocked by the estimator gap.**

> Phase 10 authorises no interpretation beyond the frozen permitted claims. A negative result is a complete and publishable outcome of equal permanence.

---

## Dependency and gating summary

```
P2 skeleton ──► P3 data ──► P4 context ──► P5 orbital core ──► P6 execution ──► P7 validation ──► P8 ledger ──► P9 interfaces
   (open)      UR-003/4/7                  UR-005/6            UR-010                              UR-009
                                                                                                        │
                                                          UR-001 ────────────────────────────────► P10 run
```

**Only Phase 2 is fully unblocked today.** Phases 3–9 need custodian rulings that are narrow and answerable. Phase 10 needs a scientific deliverable that does not yet exist.

## Milestone classes — evidence-defined

| Milestone | Evidence required on `main` |
|---|---|
| Architecture accepted | This blueprint approved |
| Contracts frozen | Phase 2 interfaces published, contract tests green |
| Deterministic skeleton replayed | Two fresh-clone dry runs byte-identical |
| Dataset manifest reproduced | Offline manifest reproduction from digests |
| Evidence pipeline validated | Eligibility and ordering match custodian test vectors |
| Scientific core reference outputs reproduced | Kepler, energy, known-answer LOO all pass |
| Controller passes all controls | Negative-control estimator fails to win |
| Complete clean-room replay | Full pipeline reproduced from a fresh clone |
| First empirical run accepted | Phase 10 run package published |
| Ledger candidate generated | Valid `AR1-E…` chaining to the canonical tip |
