# ASTRO-EXEC-001 — Risk Register

Likelihood and consequence are `Low` / `Medium` / `High`. **Blocking threshold** states the condition at which the programme must stop rather than proceed.

---

### RK-01 — The estimator under test does not exist
**Likelihood:** Certain (present state) · **Consequence:** High
**Detail:** `UR-001`. `ASTRO-EXP-0001` tests a frozen ASA estimator that no repository artefact specifies, and no artefact connects `ASTRO-THEORY-0001` to four-perturber selection.
**Detection:** Phase 0 inspection; run-start check for a digest-pinned estimator.
**Mitigation:** Architect the estimator as a sealed plug-in; build and validate the entire apparatus without it using negative controls; require a separate scientific deposit.
**Owner:** Custodian / ASA laboratory (scientific, not engineering).
**Blocking threshold:** Phase 10 must not begin. **If an engineer supplies an estimator, the experiment is void by construction (F1).**

### RK-02 — An implementer silently resolves an open requirement
**Likelihood:** High · **Consequence:** High
**Detail:** Nine requirements need custodian rulings. A plausible default chosen in code becomes an undocumented scientific decision that changes $W$.
**Detection:** Contract tests must cite a protocol section or a ruling id; code review rejects any scientific constant without a citation; blocked paths raise `UnresolvedRequirement`.
**Mitigation:** Fail closed by default; traceability matrix marks blocked rows; no `UR` closable by an implementer.
**Owner:** Operator A (enforcement), Custodian (closure).
**Blocking threshold:** any scientific constant merged without a traceable source.

### RK-03 — Floating-point divergence changes selections
**Likelihood:** Medium · **Consequence:** High
**Detail:** Different platforms, compiler flags or summation orders shift $E_m(t)$; near a materiality boundary that flips a win, hence $W$.
**Detection:** Cross-platform comparison; byte-identical replay on the reference platform; margin analysis reporting per-target distance to the boundary.
**Mitigation:** Strict FP policy — no fast-math, no FMA contraction, compensated summation in fixed order, canonical reduction order, no parallel accumulation.
**Owner:** Operator C.
**Blocking threshold:** any cross-platform run that changes a selection or $W$. Tolerance applies to $E_m(t)$ only, never to the decision.

### RK-04 — Numerical resolution $\delta_t$ is outcome-relevant and unspecified
**Likelihood:** High · **Consequence:** High
**Detail:** `UR-005`. $\delta_t$ enters the materiality test directly; the tolerance pair defining it is unspecified, so an implementer's choice moves the win threshold.
**Detection:** Sensitivity analysis over candidate tolerance pairs, reported before any deployment run.
**Mitigation:** Custodian ruling fixing scheme and tolerances before Phase 5; publish $\delta_t$ per target with the tightening evidence.
**Owner:** Custodian.
**Blocking threshold:** deployment must not run on an unruled tolerance pair.

### RK-05 — Outcome leakage to the ASA laboratory (F1)
**Likelihood:** Medium · **Consequence:** High — voids the experiment
**Detail:** The protocol forbids the ASA laboratory seeing comparator or counterfactual outcomes before its selections are sealed. A monolithic engine makes leakage easy and undetectable.
**Detection:** `LeakageGuard` capability enforcement; sealed-archive digests published before opening; blind-integrity test that must fail closed.
**Mitigation:** Role partition into separately executable applications with disjoint capability sets.
**Owner:** Operator A (guard), Operator D (sealing).
**Blocking threshold:** any evidence of pre-seal access to truth outputs → declare F1 and publish the breach.

### RK-06 — Live-service dependency destroys reproducibility
**Likelihood:** Medium · **Consequence:** High
**Detail:** `UR-007`. Horizons is permitted for apparatus check 2. If queried live during measurement or replay, the experiment is not reproducible.
**Detection:** Network access disabled by default; any socket attempt inside a measurement run aborts.
**Mitigation:** Capture once into a digest-registered fixture; replay from fixture; live access only in an explicit separate acquisition mode.
**Owner:** Operator B.
**Blocking threshold:** any measurement run that opens a network connection.

### RK-07 — Gaia fit choices change the posterior and the endpoint
**Likelihood:** High · **Consequence:** High
**Detail:** `UR-003`. Estimator, weighting and outlier policy determine $C_t$, hence $L_t$, hence all 32 draws, hence every reported error.
**Detection:** Reduced-$\chi^2$ apparatus check 1; sensitivity comparison across defensible fit choices.
**Mitigation:** Custodian ruling before the manifest is frozen — the protocol requires the 32 states be published before either deployment selection, so the fit must be settled first.
**Owner:** Custodian.
**Blocking threshold:** manifest must not be frozen on an unruled fit.

### RK-08 — Target ordering ambiguity permits an unfavourable-set challenge
**Likelihood:** Medium · **Consequence:** High
**Detail:** `UR-004`. The SHA-256 pre-image encoding is unspecified; a different encoding yields a different 27-target set. This is precisely the manipulation the salt ceremony exists to prevent.
**Detection:** Published test vectors as contract tests; the ordering is recomputable by any third party from the published salt.
**Mitigation:** Custodian ruling fixing exact pre-image bytes with worked examples.
**Owner:** Custodian.
**Blocking threshold:** target selection must not run before the encoding is ruled and test-vector-verified.

### RK-09 — Tests validate implementation behaviour rather than frozen intent
**Likelihood:** High · **Consequence:** High
**Detail:** The classic failure: tests assert what the code does, so a misreading of the protocol becomes "correct" and is locked in by a green suite.
**Detection:** Review rule — every scientific test cites the `ASTRO-EXP-0001` section it enforces; tests without a citation are rejected.
**Mitigation:** Independent reviewer for scientific correctness; no operator accepts their own numerical routine; known-answer and analytic tests preferred over regression snapshots.
**Owner:** Operator D plus independent reviewer.
**Blocking threshold:** a scientific test merged without a protocol citation.

### RK-10 — Reusing the existing non-conformant engine
**Likelihood:** Medium · **Consequence:** High
**Detail:** `src/asa_astro/reasoning/engine.py` computes something called "standing" and "significance". It is POC-grade, image-domain, and declares itself non-conformant. Reusing it because the names match would substitute an unrelated computation for the experiment.
**Detection:** Import-graph test — `astro_exec` must not import `asa_astro`.
**Mitigation:** Separate package; explicit non-reuse recorded in the blueprint.
**Owner:** Operator A.
**Blocking threshold:** any import of `asa_astro` from `astro_exec`.

### RK-11 — Storage or compute blowout
**Likelihood:** Low (mitigated) · **Consequence:** Medium
**Detail:** Naive full-trajectory retention needs ~3 TB.
**Detection:** Storage budget test on the reference fixture.
**Mitigation:** Streaming reduction — store full trajectories once (~151 MB), stream all reduced runs. Recorded in the Technology Decision §5.
**Owner:** Operator C.
**Blocking threshold:** none; design already resolves it.

### RK-12 — Result-ledger corruption or premature append
**Likelihood:** Low · **Consequence:** High — the ledger is the permanent scientific record
**Detail:** An automated append could renumber, break the `previous_event_id` chain, or record a result that does not meet §5.1.
**Detection:** Chain validation end-to-end; result-definition gate; envelope completeness tests.
**Mitigation:** The engine **proposes only**; a human appends. Serialized allocation with fast-forward retry, never merge/rebase/force.
**Owner:** Operator E.
**Blocking threshold:** any automated write to `ASTRO-RESULTS-0001`.

### RK-13 — Claim overstatement
**Likelihood:** Medium · **Consequence:** High
**Detail:** A positive $W$ invites language beyond the bounded permitted claim, especially given `UR-008` — nothing links the result to the frozen theory.
**Detection:** Forbidden-claim string tests over every generated output; claim comparator emits only the exact permitted wording.
**Mitigation:** Claims are read-only inputs; bounded wording is a constant, not a template.
**Owner:** Operator E.
**Blocking threshold:** any generated artefact containing a forbidden claim.

### RK-14 — Insufficient negative controls
**Likelihood:** Medium · **Consequence:** High
**Detail:** An apparatus that reports wins for a fixed or shuffled estimator is broken, and the defect is invisible without deliberate controls.
**Detection:** Mandatory negative-control runs in Phase 6 acceptance.
**Mitigation:** Fixed, shuffled and mass-ranked control estimators; all must fail to reach $W\ge20$.
**Owner:** Operator D.
**Blocking threshold:** any control estimator reaching $W\ge20$ halts the programme until explained.

### RK-15 — Local-only or unverified remote state
**Likelihood:** Medium · **Consequence:** Medium
**Detail:** Work completed locally but unpublished, or assumed published without verification, fragments authority across operators.
**Detection:** Every handoff cites a commit verified against `origin/main` by `ls-remote`, never by local state.
**Mitigation:** Publish-and-verify per bounded unit; no stacked unpublished work.
**Owner:** All operators.
**Blocking threshold:** any operator consuming an unpublished interface.

### RK-16 — Theory–experiment disjunction misread as validation
**Likelihood:** Medium · **Consequence:** High
**Detail:** `UR-008`. A successful run would not, on the current artefacts, be evidence for `ASTRO-THEORY-0001`, because nothing traces the estimator to the frozen mathematics.
**Detection:** Documentation review at Phase 10 readiness.
**Mitigation:** Either the estimator specification derives selection from the theory, or the programme records that Version 1 empirical work is deliberately independent of it. Stated in the blueprint and this register.
**Owner:** Custodian.
**Blocking threshold:** publishing a positive result as theory validation without a documented link.

### RK-17 — Premature optimisation alters numerical output
**Likelihood:** Medium · **Consequence:** High
**Detail:** A change to summation order, step control or vectorisation made for speed silently changes results.
**Detection:** Byte-identical replay against stored reference fixtures on every commit touching `orbits/` or the crate.
**Mitigation:** Any change affecting numerical output is a determinism change requiring full re-validation and a recorded justification.
**Owner:** Operator C.
**Blocking threshold:** a performance change that alters a reference fixture output without an accompanying re-validation record.

### RK-18 — Scope creep from the generic module list
**Likelihood:** Medium · **Consequence:** Medium
**Detail:** The programme brief names modules — Standing, Relationship Graph, Visualisation — with no counterpart in `ASTRO-EXP-0001`. Building them adds untested surface and invents requirements.
**Detection:** Reverse-trace table in the Requirements Traceability artefact; any component with no requirement row is challenged at review.
**Mitigation:** Explicit scope decisions recorded with rationale rather than silent omission.
**Owner:** Operator A.
**Blocking threshold:** a module merged with no traceable requirement.

---

## Summary

| Blocking today | Risks |
|---|---|
| Phase 10 only | RK-01 |
| Phases 3–6 | RK-02, RK-04, RK-06, RK-07, RK-08 |
| Continuous engineering discipline | RK-03, RK-05, RK-09, RK-10, RK-12, RK-13, RK-14, RK-15, RK-17, RK-18 |
| Programme interpretation | RK-16 |

The highest-consequence risks are not technical. **RK-01, RK-02, RK-09 and RK-16 are all failures of discipline in which the engine appears to work while measuring something other than the frozen experiment.**
