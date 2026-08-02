# ASTRO-EXEC-001 — Acceptance Gates

A gate is passed only when its evidence exists on GitHub `main` and has been verified from the remote. **Local success is not evidence.**

## G0 — Blueprint accepted
- [ ] Blueprint and six companions published on `main` and retrievable from the remote
- [ ] Every requirement traces to a frozen artefact or a recorded engineering decision
- [ ] Every unresolved requirement is registered, not invented
- [ ] Human approval of the blueprint and of the first bounded manufacturing package

**Blocks:** all implementation.

## G1 — Contracts frozen (Phase 2)
- [ ] `astro_exec.core` published; canonical JSON, identifiers, hashing, config, provenance, errors, logging, `LeakageGuard`
- [ ] Contract tests green on a fresh clone in a clean environment
- [ ] Frozen-artefact digest verification aborts on drift
- [ ] Two dry runs byte-identical except run id
- [ ] `astro_exec` does not import `asa_astro` (import-graph test)
- [ ] Interfaces documented sufficiently for B–E to proceed without conversation context

**Blocks:** Operators B, C, D, E.

## G2 — Data foundation (Phase 3)
- [ ] `UR-003`, `UR-004`, `UR-007` closed by custodian ruling
- [ ] Ordering matches published test vectors exactly
- [ ] Eligibility enforces all five rules
- [ ] Unpermitted datasets and release substitutions rejected
- [ ] Manifest reproduced byte-identically from digests **with no network access**
- [ ] Acquisition cannot execute inside a measurement run

## G3 — Context foundation (Phase 4)
- [ ] Every context value traces to a protocol section or validation fails
- [ ] Context validation rejects a missing EIH term, an altered epoch grid, or a changed four-term budget
- [ ] No authoritative value exists without a provenance chain to registered dataset digests

## G4 — Deterministic scientific core (Phase 5)
- [ ] `UR-005`, `UR-006` closed by custodian ruling
- [ ] Two-body Kepler analytic check passes
- [ ] Energy and momentum drift within declared bounds over 20 years
- [ ] EIH 1PN applied in every propagation; $\beta=\gamma=1$
- [ ] Deletion intervention verified singular — exactly one term changes
- [ ] Cholesky factor lower-triangular with positive diagonal
- [ ] Sobol points match published test vectors
- [ ] Byte-identical replay on the reference platform
- [ ] Cross-platform run yields identical selections and identical $W$
- [ ] Known-answer synthetic system recovers its four dominant perturbers exactly

**This is the highest-risk gate. A silent defect here corrupts every downstream number.**

## G5 — Experiment execution (Phase 6)
- [ ] `UR-010` closed
- [ ] LOO ranking and increasing-permanent-number tie-break correct
- [ ] Exactly four distinct identifiers enforced
- [ ] Abstention, duplicate, invalid or missing submission counts as a non-win
- [ ] No pre-seal access to truth outputs; blind-integrity test fails closed
- [ ] No post-seal mutation of any earlier input, comparator result, tolerance or trajectory
- [ ] Single unblinding enforced; an interim look is impossible, not merely discouraged
- [ ] All seven stopping rules enforced
- [ ] **Negative controls: fixed, shuffled and mass-ranked estimators all fail to reach $W\ge20$**
- [ ] Every control run stamped `apparatus-validation`, never `authoritative-scientific`

## G6 — Validation and claims (Phase 7)
- [ ] Exact binomial reproduces `0.0095786452293396` at $W{=}20$
- [ ] Power reproduces `0.8444402928110182` at $p{=}0.8$
- [ ] F0–F3 classification correct on injected failures
- [ ] No metric can alter the primary decision
- [ ] Claims are read-only; comparator emits only bounded permitted wording
- [ ] No generated artefact contains a forbidden claim

## G7 — Results and ledger (Phase 8)
- [ ] `UR-009` closed
- [ ] Run package complete; every artefact classified
- [ ] 14-item minimum evidence package resolvable, else held at `EH-1`
- [ ] Candidate event validates against the ledger's own rules and chains to the canonical tip
- [ ] Serialized allocation with fast-forward retry; never merge, rebase, force, renumber or edit
- [ ] **The engine cannot write to `ASTRO-RESULTS-0001`**

## G8 — External interfaces (Phase 9)
- [ ] Read-only API cannot mutate a run package
- [ ] No engine module imports a rendering library
- [ ] Adapter specifications published; no renderer built

## G9 — First empirical run readiness (Phase 10)
- [ ] **`UR-001` closed** — estimator specification deposited with a cryptographic digest
- [ ] All other `UR` entries closed
- [ ] G1–G8 passed and verified remotely
- [ ] Estimator returns exactly four distinct identifiers for every admissible input, deterministically
- [ ] Estimator digest pinned and verified at run start
- [ ] Deployment salt generated in a witnessed ceremony, published, never redrawn
- [ ] Manifest frozen and published **before** either deployment selection, including the 32 posterior states and Sobol source points
- [ ] Apparatus checks 1–4 passed for all 27 targets, with exclusions and check values published
- [ ] Comparator archive sealed and digest-published before ASA selections are opened
- [ ] Independent replay reproduces target-level errors within registered $\delta_t$
- [ ] Publication set complete per §Publication policy — **regardless of result**

**Only when every box above is ticked may the frozen experiment be executed.**

## G10 — Result accepted
- [ ] Run completed with full provenance
- [ ] Independent replay within registered resolutions
- [ ] Failure class determined and recorded
- [ ] Ledger candidate generated and validated
- [ ] Human appended the event to `ASTRO-RESULTS-0001`
- [ ] Evidence level determined by the ledger's own rules, not by the engine

**A negative result passes this gate exactly as a positive one does.** `ASTRO-RESULTS-0001` `INV-R08` requires negative evidence to have equal permanence, and `ASTRO-EXP-0001` requires publication regardless of outcome.

---

## Standing conditions — apply at every gate

1. Evidence exists on GitHub `main` and was verified from the remote, not locally.
2. No frozen scientific artefact was modified.
3. No `UR` was closed by an implementer.
4. Every scientific test cites the protocol section it enforces.
5. No scientific constant exists without a traceable source.
6. Evidence level remains `EH-0` until G10.
