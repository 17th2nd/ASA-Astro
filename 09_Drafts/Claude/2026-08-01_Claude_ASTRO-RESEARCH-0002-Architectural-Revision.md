# ASTRO-RESEARCH-0002 — Astronomy Validation Programme: Architectural Revision

**Programme:** Adaptive Significance Architecture — Astronomy Validation Programme
**Supersedes for design purposes:** nothing. **Baseline:** `ASTRO-RESEARCH-0001` (Version 0), which remains the criticism of record and is not amended, defended, or withdrawn.
**Author cell:** Claude (Principal Research Scientist role)
**Date:** 2026-08-01
**Status:** DRAFT — working document in `09_Drafts/`. No architectural authority. Not a validation result. Not a ratified ASA or ASA-Astro record.
**Repository:** ASA-Astro (sole repository for this concept)

---

## 0. Standing of this document

`ASTRO-RESEARCH-0001` is Version 0. Every criticism it raised is preserved verbatim in the attack ledger of §2 and is carried forward into the residual-risk register of §9. **No criticism has been deleted, softened, or reclassified as resolved-by-assertion.** Where a criticism has been remedied, the remedy is a named architectural decision with an invariant and a falsification test. Where a criticism cannot be remedied, it is recorded as a conceded scope limit.

This document manufactures **Version 1 of the scientific architecture**. It contains no implementation, no algorithms in executable form, and no code. It defines types, invariants, contracts, and the obligations a conforming implementation must satisfy.

**The benchmark is not weakened anywhere in this document.** Every change to the benchmark in §7 adds a mandatory emission, an invalidating condition, or a control. Version 1 is strictly harder to pass than Version 0.

**Naming convention used throughout.**
`A#` — a falsification attack from V0 that succeeded or was untested.
`B#` — a falsification attack raised in §8 of this document against V1 itself.
`AD-##` — an architectural decision in V1.
`INV-##` — an invariant a conforming implementation must satisfy.

---

## 1. The single conceptual change

Version 0 treated significance as **a score of unclear referent** — a number whose meaning was defined by the procedure that produced it. That is the root cause of four of the eight successful attacks: an unfalsifiable hypothesis (A1), standing as intrinsic significance (A3), equivalence to personalised PageRank (A7), and no defence against physics (A6). A score with no referent cannot be wrong, cannot be calibrated, and cannot be distinguished from any other score with the same ordering.

Version 1 makes one change from which most of the architecture follows:

> **Significance is redefined as an estimator of a declared counterfactual quantity.**
>
> `σ_C(v)` estimates how much the outcome the context cares about would change if `v`'s contribution were withdrawn.

This single move does the following work:

| It gives significance | Which remedies |
|---|---|
| A **target of estimation** — something it can be wrong about | A1 (unfalsifiability) |
| **Units** inherited from the outcome functional | V0 §7.2 B1 (dimensional invalidity), cross-graph incomparability |
| **Calibratable error** — the estimate can be compared to the measured value | A1, and makes H2 sharp |
| **Structural context-dependence** — no outcome functional, no significance | A1, A3 (nothing is left for an intrinsic score to mean) |
| An **honest relationship to physics** — ASA estimates what physics computes exactly | A6 |
| A **basis for principled abstention** — refuse when the estimator's variance exceeds tolerance | abstention gaming |

Everything else in Version 1 is the machinery required to make that estimator honest.

---

## 2. Attack ledger — V0 criticisms and their disposition

Preserved in full. Nothing removed.

| # | Attack (V0) | V0 outcome | V1 disposition | Remedy |
|---|---|---|---|---|
| A1 | The primary hypothesis is a definition, not a hypothesis | **Succeeded** | **Remedied** | AD-09, AD-11, AD-12; revised hypotheses §6 |
| A2 | Brightness enters through catalogue topology, not features | **Untested** | **Remedied and made mandatory-to-test** | AD-17, AD-18, AD-19 |
| A3 | Standing is intrinsic significance renamed | **Succeeded** | **Remedied, and the layer put on probation** | AD-01, AD-02, AD-03 |
| A4 | Path measures are meaningless on a non-composable graph | **Succeeded** | **Remedied** | AD-04 – AD-08 |
| A5 | Contexts chosen to flatter the architecture | **Untested** | **Remedied** | AD-13, AD-15, AD-16 |
| A6 | A one-line physical formula wins | **Succeeded for single-physics contexts** | **Conceded and reframed** — physics is the ground truth, not the competitor | AD-09, AD-29 |
| A7 | It reproduces personalised PageRank | **Partially succeeded** | **Remedied by strict containment** — PPR is now a provable degenerate case | AD-05, AD-08, AD-26 |
| A8 | Attention already does significance-before-reasoning | **Succeeded on the ordering claim** | **Ordering claim withdrawn; replaced by an auditable data-flow invariant** | AD-24 |

Two V0 findings were not attacks but structural defects, and are also carried:

| # | Defect (V0) | V1 disposition | Remedy |
|---|---|---|---|
| D1 | Max-normalisation makes scores graph-relative and incomparable | **Remedied** | AD-10 (σ is dimensioned and absolute) |
| D2 | Dimensional invalidity of aggregated edge strengths | **Remedied** | AD-04, AD-10 |

---

## 3. Version 1 architecture

```text
Observation
   │
   ▼
Evidence Record ────────────────────────────────┐
   │                                            │  (provenance, units, frame,
   ▼                                            │   epoch, band, calibration,
Entity Candidate                                │   detectability δ)
   │                                            │
   ▼                                            │
Relationship Assertion  ◄───────────────────────┘
   │   carries validity signature ν = ⟨frame, epoch-interval, band,
   │                                   model-family, role-pair, dimension⟩
   ▼
Assertion Graph  G
   │
   ▼
╔═══════════════════════════════════════════════════════════════════════╗
║  STANDING GATE  Σ                                    [AD-01, AD-03]   ║
║  Σ : V ∪ E → {admissible, inadmissible, indeterminate} × SupportSet   ║
║  No scalar. No ordering. No aggregate. On probation.                  ║
╚═══════════════════════════════════════════════════════════════════════╝
   │
   ▼
Admissible Assertion Graph  G⁺
   │
   │  ┌──────────────────────────────────────────────────────────────┐
   │  │  CONTEXT CONTRACT  C                        [AD-11 – AD-16]  │
   │  │    Δ_C   designation set (non-empty, required)               │
   │  │    M_C   outcome functional (what σ estimates against)       │
   │  │    ⊖_C   withdrawal semantics (enumerated)                   │
   │  │    L_C   composition licence restriction                     │
   │  │    S_M   selection model + correction method                 │
   │  │    Ω_C   abstention policy, costs, budget                    │
   │  │    Π_C   sealed predictions (commit–reveal)                  │
   │  │    origin, genericity proof, paired counter-context          │
   │  └──────────────────────────────────────────────────────────────┘
   │                       │
   ▼                       ▼
╔═══════════════════════════════════════════════════════════════════════╗
║  COMPOSITION LICENCE  ⊙                              [AD-04 – AD-08]  ║
║  Schema level:   automaton 𝒜 over relationship-type sequences         ║
║  Instance level: compatibility predicates on ν                        ║
║  Failure ⇒ ⊥ (a recorded halt, never a zero)                          ║
╚═══════════════════════════════════════════════════════════════════════╝
   │
   ▼
Licensed Traversal Graph  G_C   — every walk is a valid composite relation
   │
   ▼
╔═══════════════════════════════════════════════════════════════════════╗
║  SIGNIFICANCE FUNCTIONAL  σ_C                        [AD-09 – AD-12]  ║
║  σ_C(v)  ≈  ‖ M_C(G⁺) − M_C(G⁺ ⊖_C v) ‖                              ║
║  anchored at Δ_C · dimensioned in M_C's units · carries variance      ║
║  selection-corrected · may return ⊥ with a typed reason               ║
╚═══════════════════════════════════════════════════════════════════════╝
   │
   ▼
Significance Event  ⟨estimate ± uncertainty | ⊥reason, C-hash, trace, δ-correlation⟩
   │
   ▼
Reasoning   — read-only consumer. No write path back to σ. [AD-24]
```

**What was deleted from V0, not renamed:** the eight-component context-free aggregate `S_i`; the additive term `β_S·S_i`; the neighbour term `(0.5 + 0.5·S_j)`; max-normalisation of scores; and unrestricted power iteration and betweenness over the mixed-type graph.

---

## 4. Architectural decisions

Each decision names the criticism it remedies, the invariant it imposes, and the test that would show the decision was wrong.

---

### 4.1 Reading B Standing

#### AD-01 — Standing is a non-ordering admissibility gate

**Remedies:** A3.

**Decision.** Standing is redefined with the type

```
Σ : V ∪ E  →  {admissible, inadmissible, indeterminate} × SupportSet
```

where `SupportSet` is a *set* of evidence identifiers, quality flags, and unresolved-dependency markers. It is ordered only by set inclusion, which is a partial order and admits no total order. Standing emits **no numeric field whatsoever**.

**Rationale.** A3 succeeded because a context-independent, totally ordered scalar attached to an entity is an intrinsic importance score regardless of its name. The remedy is not to rename the scalar or shrink its weight. It is to remove the codomain in which an intrinsic ordering can exist.

**INV-01 (No-Ordering).** No downstream component may apply any function `ρ : Standing → ℝ`, nor any total-order comparison over `SupportSet`. Conformance requires that the standing record be structurally incapable of producing a rank: it contains sets and enumerated states, never magnitudes.

**Falsification test.** Attempt to reconstruct a ranking from standing records alone and correlate it with σ. If a reconstruction achieves material rank correlation with σ across contexts, INV-01 has been violated in practice and the gate has leaked an ordering.

---

#### AD-02 — The context-free aggregate is deleted, not relocated

**Remedies:** A3, A7.

**Decision.** The eight standing components of V0 — typed degree, weighted connectivity, eigenvector-like influence, betweenness, containment hierarchy, relationship persistence, evidence support, structural dependency — are **not** computed context-free. Any of them that a context needs is declared by that context and computed **inside** the significance functional, on the licensed traversal graph `G_C`.

**Rationale.** Relocating the aggregate behind a gate would leave A3 intact: a pre-computed context-free structural score would still be an intrinsic ordering, merely gated. The aggregate must not exist prior to context.

**INV-02 (No Pre-Context Aggregation).** No stored artefact may contain a graph-derived numeric summary of an entity computed without reference to a context contract.

**Falsification test.** Audit every persisted artefact for entity-level numeric fields. Any such field that is not a directly measured quantity with units and provenance is a violation.

---

#### AD-03 — Standing is retained on probation with an explicit deletion criterion

**Remedies:** A3; anticipates B6 (§8).

**Decision.** Version 1 keeps the standing gate, but declares in advance the conditions under which the layer is **deleted from the architecture** rather than revised:

1. the gate's rejection set is empty or negligible on the benchmark — i.e. it rejects nothing that schema and provenance validation would not already reject; **or**
2. removing the gate entirely produces no degradation in any predeclared metric.

If either holds, standing is not a layer. It is a rename of input validation, and V2 must delete it.

**Rationale.** V0 established that standing cannot add information (data-processing inequality). Its justification is therefore computational, governance, or inductive-bias — and a justification of that kind must be earned empirically or the layer removed. Retaining an unearned layer is exactly the complexity that B9 attacks.

**INV-03 (Probation).** Every benchmark run must emit the standing gate's rejection set, its size, and the specific validation rule that would otherwise have admitted each rejected item.

**Falsification test.** The deletion criterion above *is* the test. It is predeclared and it points at deleting our own work.

---

### 4.2 Composition Algebra and Relationship Composition

#### AD-04 — Every assertion instance carries a validity signature

**Remedies:** A4; V0 defect D2.

**Decision.** Every relationship assertion carries

```
ν(e) = ⟨ frame, epoch-interval, band, model-family, role-pair, dimension ⟩
```

where `dimension` is the physical dimension of the assertion's magnitude (or `dimensionless`, or `none` for purely relational assertions), and `epoch-interval` is a validity interval, not a timestamp.

**Rationale.** A4 succeeded because path algorithms summed over edge sequences whose composition has no referent. Composition validity cannot be decided at the type level alone: two `contained_in` assertions in different frames do not compose, while two in the same frame may. The decision must be made per instance, which requires the instance to carry the deciding information.

**INV-04 (Signature Completeness).** An assertion without a complete validity signature is inadmissible. Absent components must be explicit states (`unknown`, `not_applicable`), never omitted, and `unknown` in a component required by a compatibility predicate forces `⊥` at composition time.

---

#### AD-05 — Composition is a partial function gated at two levels

**Remedies:** A4, A7.

**Decision.** Composition is defined as

```
⊙ : (Type × ν) × (Type × ν)  ⇀  (Type × ν)
```

licensed only when **both** hold:

- **Schema level.** A finite automaton `𝒜` over relationship-type sequences accepts the type sequence. `𝒜` is authored from physical semantics and frozen (AD-07).
- **Instance level.** All compatibility predicates hold on the two validity signatures: frame-compatible (identical, or a declared transform with recorded uncertainty inflation); epoch-overlap (intervals intersect, or a declared propagation with uncertainty inflation); band-compatible; model-family-compatible; role-chaining valid (the target role of the left assertion unifies with the source role of the right); dimension-composable.

Composition is **uncertainty-monotone**: the composite's uncertainty is not less than either component's, and each licensed step applies a declared composition penalty.

Composition is **not assumed associative**. Evaluation order is fixed left-to-right from the designated anchor and the bracketing is recorded in the trace.

**Rationale.** This is the precise remedy to A4 and the substance of the N1 novelty claim from V0 §5.6. It is also the remedy to A7: personalised PageRank is the special case in which `𝒜` accepts every sequence and all compatibility predicates are trivially true.

**INV-05 (Two-Level Licence).** No traversal may cross an assertion pair for which either level is unlicensed.

---

#### AD-06 — An unlicensed composition halts with `⊥`, which is an abstention, not a zero

**Remedies:** A4; connects to abstention (AD-20).

**Decision.** When composition is refused, traversal halts on that path and records `⊥` with the specific predicate that failed. `⊥` never contributes zero weight to a sum; it removes the path from the estimator's support and is reported.

**Rationale.** Treating a refused composition as zero would silently convert a semantic refusal into a numerical statement of no effect — the same category error V0 identified in converting `unknown` to zero.

**INV-06 (Halt Is Not Zero).** Every `⊥` is counted, typed, and surfaced in the significance event. A run in which `⊥` events are not enumerated is invalid.

---

#### AD-07 — The licence automaton is frozen before data and independently ablated

**Remedies:** A4; anticipates B2 (§8).

**Decision.** `𝒜` and the compatibility predicates are content-hashed and frozen **before any benchmark data is retrieved**. They are versioned separately from experiments. Any change after data contact requires a new benchmark identity.

Three mandatory licence controls accompany every run:

| Control | Purpose |
|---|---|
| **Permissive licence** (accept all sequences) | Recovers the V0 behaviour; if it performs as well, licensing is decorative |
| **Random licence** (same acceptance rate, shuffled) | If it performs as well, the *content* of the licence table is decorative |
| **Frozen licence** (the real one) | The tested configuration |

**Rationale.** A licence table authored by the architecture's designers is an ontology with tunable parameters. Without freezing and without a random control, it is a place to hide fitting.

**INV-07 (Licence Freeze).** The licence hash must predate the earliest dataset retrieval timestamp in the run manifest.

**Falsification test.** If the random licence matches the frozen licence on the predeclared metric, the composition algebra is not doing work and the N1 novelty claim is empty.

---

#### AD-08 — Path-based measures exist only on the licensed traversal graph

**Remedies:** A4.

**Decision.** Any measure defined by summation over walks or paths — eigenvector-family influence, betweenness, closeness, Katz, path-counting reachability — is computed **only** on `G_C`, the graph whose walks are exactly the automaton-accepted, instance-compatible, cycle-free, depth-bounded paths. Non-composable relationship types contribute at depth 1 only.

**Rationale.** On `G_C` every walk in the sum denotes a licensed composite relation, so the measure has a referent. This is the direct repair of A4.

**INV-08 (Licensed Topology).** No centrality-family measure may be computed on `G` or `G⁺`. Only `G_C`.

---

#### AD-09' — Extended taxonomy and role algebra adopted

**Remedies:** taxonomy gaps identified in V0 §4.2.

**Decision.** The seven additional relationship types from V0 are adopted as first-class: identity/cross-identification (threshold-gated equivalence, with a mandatory non-transitivity fixture), classification/typing, statistical association, **selection/censoring dependency**, calibration dependency, contradiction/competing claim, and derivation. Role chaining is required for all composition.

---

### 4.3 Counterfactual Significance

#### AD-09 — Significance is an estimator of a declared counterfactual

**Remedies:** A1, A6.

**Decision.** For a context `C` declaring an outcome functional `M_C` and withdrawal semantics `⊖_C`, significance is defined as

```
σ_C(v)  ≜  an estimate of  ‖ M_C(G⁺) − M_C(G⁺ ⊖_C v) ‖
```

computed from relational evidence over `G_C` **without evaluating `M_C` directly**. Direct evaluation of `M_C` is ground truth and its use as an input is leakage.

The output is a triple: `⟨point estimate, uncertainty, support⟩`, or `⊥` with a typed reason.

**Rationale.** This is the change described in §1. A1 succeeded because significance had no referent. Under AD-09 it has one, and it can therefore be wrong by a measurable amount.

**On A6.** A6 is conceded, not defeated. Where the counterfactual is exactly computable — solar-system dynamics, simulation merger trees — **physics is the ground truth and the target of estimation, not a competitor.** ASA's claim is not that it beats an exact calculation. It is that a relational estimator can approximate the exact counterfactual where the exact calculation is available, so that it may be trusted where it is not. Any document claiming ASA outperforms `GM/r²` on gravitational significance is making a false claim and must be corrected.

**INV-09 (Referent).** No significance event may be emitted without naming its outcome functional, its withdrawal semantics, and its units.

---

#### AD-10 — Significance is dimensioned and absolute; rank normalisation is prohibited

**Remedies:** V0 defects D1 and D2; supports A1.

**Decision.** `σ_C(v)` carries the units of `M_C` — kilometres of ephemeris displacement, magnitudes of flux, dimensionless probability shift. **Max-normalisation and any other within-run rank normalisation are prohibited.** Rankings, where required, are derived *from* the dimensioned estimates, never stored in their place.

**Rationale.** V0's max-normalisation made every score graph-relative, uncomparable across graphs, and uncalibratable. A dimensioned estimate is comparable across graphs, across contexts sharing an outcome functional, and against measured ground truth. This is what makes calibration possible at all.

**INV-10 (Dimension).** Every significance event carries an explicit unit. Aggregating quantities of differing dimension is a validation failure, not a modelling choice.

---

#### AD-11 — The designation set is required, non-empty, and structurally load-bearing

**Remedies:** A1; implements Context Irreducibility.

**Decision.** Every context contract declares a designation set `Δ_C` — the entities, observables, or questions the outcome functional is about. `Δ_C` must be non-empty. **`σ_C` is undefined when `Δ_C` is empty**; the architecture returns `⊥` rather than a global score.

**Rationale.** V0's result R1 established that structure-only significance is constant on automorphism orbits, so any question whose answer distinguishes automorphic nodes provably requires context. But V0's context acted mainly as a *filter*, and a filter can wash out, leaving a near-global ranking — which is exactly how the architecture could collapse into a single score. Requiring a designation set makes the symmetry-breaking information mandatory and structural.

**INV-11 (Designation Required).** A significance request without a designation set is rejected, not defaulted.

---

#### AD-12 — Significance is anchored at the designation, not filtered by it

**Remedies:** A1, A3, A7.

**Decision.** `σ_C(v)` is computed as a functional of the licensed paths **from `v` to `Δ_C`**. Context does not merely restrict which edges are eligible; it supplies the anchor relative to which relevance is defined. Remove the anchor and the functional has no argument — it does not degrade to a global measure.

**Rationale.** This makes context irreducibility architectural rather than aspirational. Under AD-12 there is no well-formed computation that ignores context, so the collapse mode A3 describes is not merely discouraged, it is unrepresentable.

**INV-12 (Anchoring).** Every path contributing to a significance estimate must terminate in `Δ_C`. Paths not reaching the designation contribute nothing and are reported as unreached, not as zero-effect.

---

#### AD-13 — The withdrawal operator is declared from an enumerated set

**Remedies:** A1; anticipates B7 (§8).

**Decision.** `⊖_C` is chosen from a fixed enumeration, each with declared semantics:

| Operator | Semantics |
|---|---|
| `node_and_incident` | Remove the entity and all assertions incident to it |
| `evidence_withdrawal` | Remove the entity's evidence records and re-derive every value that depended on them |
| `role_neutralisation` | Retain the entity but neutralise its participation in the roles relevant to `M_C` |
| `mass_zeroing` (physical contexts) | Retain the entity with its outcome-relevant physical quantity set to zero |

Results are comparable **only** within the same withdrawal semantics.

**Rationale.** "Remove the entity" is underdetermined, and different readings yield materially different counterfactuals. Leaving it implicit would make σ's referent ambiguous and reopen A1 through the back door.

**INV-13 (Withdrawal Declaration).** Comparing significance events with different `⊖_C` is a protocol violation.

---

### 4.4 Selection Function Leakage

#### AD-17 — Detectability is carried on every entity and assertion

**Remedies:** A2.

**Decision.** Every entity and assertion carries a **detectability record** `δ`: the modelled propensity that this item would appear in the graph given the survey configuration, instrument, band, depth, cadence and cross-match procedure — with its own uncertainty and provenance.

**Rationale.** A2 was untested in V0 and is, in my assessment, the most dangerous open risk: catalogue degree correlates with observability, so the architecture can rank by brightness through topology while passing every explicit brightness control. Selection cannot be corrected for unless it is represented.

**INV-17 (Detectability Presence).** An assertion without a detectability record — or an explicit `selection_unmodelled` state — is inadmissible at the standing gate.

---

#### AD-18 — The selection model is a required contract element, with correction or declared bias

**Remedies:** A2.

**Decision.** Every context contract references a versioned selection model `S_M` and a correction method. Where correction is impossible, the contract must declare `selection_uncorrected` **and** the run must emit a computed sensitivity bound on the resulting bias.

Where no selection model exists at all, the correct output is `indeterminate_selection` (AD-20), not an uncorrected estimate presented as an estimate.

**Rationale.** The censored graph is a realisation of an incomplete process. An estimator that ignores this is estimating a different quantity than the one declared, and its error is systematic rather than random.

**INV-18 (Censoring Declaration).** No significance event may be emitted without either a selection model reference plus correction method, or an explicit uncorrected flag plus a sensitivity bound.

---

#### AD-19 — The observability correlation is a mandatory emitted field with self-invalidation

**Remedies:** A2.

**Decision.** Every run computes an **observability baseline** `O` from `δ` alone — a ranking driven purely by how likely each item was to be observed — and emits `corr(σ_C, O)` as a **required field of every significance run**, not as an optional experiment. If it exceeds the bound declared in the context contract, **the run self-invalidates.**

**Rationale.** V0 identified the control but left it as an experiment, and experiments can be omitted, deferred, or reported selectively. Making it a mandatory emission of the computation itself means the architecture cannot produce a result without producing its own most damaging diagnostic alongside it.

**INV-19 (Mandatory Self-Diagnosis).** A significance run that does not carry its observability correlation is malformed. A run exceeding the declared bound is invalid, not merely failing.

---

### 4.5 Context Contracts

#### AD-14 — Contexts are bilateral contracts carrying sealed predictions

**Remedies:** A5.

**Decision.** A context is no longer a declaration only. It is a **contract** that additionally states, before execution:

- which entities it expects to rank high, and why;
- which baselines it expects to beat;
- **which baselines it expects to lose to**;
- the abstention rate it expects.

These prediction fields `Π_C` are **content-hashed and committed** to an append-only register pushed to the repository before any data is touched, and revealed at reporting (commit–reveal).

**Rationale.** A5 was untested and is a researcher-degrees-of-freedom attack. Freezing the declaration alone does not stop post-hoc rationalisation of *which* results count as success. Committing the predictions does.

**INV-14 (Sealed Prediction).** A context whose prediction commitment postdates the first data retrieval is inadmissible for the benchmark.

---

#### AD-15 — Context genericity: one contract, many designations

**Remedies:** A5; anticipates B1 (§8).

**Decision.** A context contract must be **instantiable over a family of designations without modification**. The same contract must produce well-formed significance requests for at least *k* distinct designation sets (k declared per benchmark, minimum 10 for GT-B contexts) by swapping `Δ_C` alone.

If a contract must be rewritten per target, it is a label attached to one answer, not a context.

**Rationale.** This is the strongest single defence against a context that smuggles the answer in. A contract that encodes target-specific knowledge cannot survive designation swapping.

**INV-15 (Genericity).** Every context contract carries a genericity proof: the list of designations over which it was instantiated unmodified, with the hash of the single shared contract body.

---

#### AD-16 — External origin quota, paired counter-contexts, and expected-failure coverage

**Remedies:** A5.

**Decision.** Three benchmark-composition requirements:

1. **External origin quota.** No more than a declared fraction of benchmark contexts may be `synthetic_internal`. The remainder must trace to an external artefact — a target-selection carton, a broker science filter, a mission requirement, a published proposal science case.
2. **Paired counter-context.** Every context is submitted with a counterpart sharing the same graph and designation but a **different outcome functional**, with a predeclared expectation that the rankings differ. This instruments context-irreducibility per context rather than only in aggregate.
3. **Expected-failure coverage.** At least one context must be predeclared as expected-to-fail. If it passes, that is a signal to investigate, not to celebrate.

**Rationale.** If every context in a benchmark is one the architecture handles well, the benchmark measures nothing. These three requirements make the context set an object of scrutiny rather than a free parameter.

**INV-16 (Composition).** A benchmark violating any of the three is invalid.

---

### 4.6 Abstention

#### AD-20 — Three typed abstentions, never merged

**Remedies:** abstention gaming; supports A2 and A4.

**Decision.** Three distinct null outcomes, each with a reason chain naming the specific gate that fired:

| Outcome | Meaning |
|---|---|
| `indeterminate_evidence` | Insufficient admissible evidence to estimate within tolerance |
| `indeterminate_licence` | Traversal halted at `⊥`; no licensed path from the entity to the designation |
| `indeterminate_selection` | No selection model, or correction impossible within the declared bias bound |

These are never collapsed into one another or into "ranked last".

**Rationale.** The three have entirely different remedies. Merging them destroys the diagnostic value of refusal and makes the abstention rate uninterpretable.

**INV-20 (Typed Refusal).** Every abstention carries its type and the identity of the gate that produced it.

---

#### AD-21 — Abstention is priced, budgeted, and neutrality-tested

**Remedies:** abstention gaming; anticipates B4 (§8).

**Decision.** Each context contract declares a cost for each abstention type and a maximum admissible abstention rate. Exceeding the budget yields a run status of `insufficient` — a third outcome distinct from both pass and fail.

Additionally, every run emits the **distribution of true counterfactual effect among abstained cases** where ground truth is available.

**INV-21 (Abstention Neutrality).** If the effect-size distribution of abstained cases differs materially from that of answered cases, the difference must be declared and penalised. Abstaining preferentially on high-effect cases is a worse failure than answering them wrongly, because it is invisible in accuracy metrics.

**Rationale.** V0 noted that unpriced abstention lets a system abstain its way to a good score. Pricing caps the rate; neutrality testing catches the more dangerous behaviour of abstaining exactly where it matters.

---

#### AD-22 — Abstention must be actionable

**Remedies:** abstention as evasion.

**Decision.** Every abstention names the **specific additional evidence, licence, or selection model that would resolve it**.

**Rationale.** This converts refusal from a defensive posture into an experimental design output, and connects the architecture to expected-value-of-information without claiming to have invented it. It also makes abstention falsifiable: if supplying the named evidence does not resolve the abstention, the reason chain was wrong.

---

### 4.7 Learning discipline and positioning

#### AD-24 — Parameter provenance replaces the forward-ordering claim

**Remedies:** A8.

**Decision.** The claim that ASA is distinguished by computing significance *before* reasoning is **withdrawn**. It describes the forward pass of every attention-based model and is not a distinction.

It is replaced by an auditable data-flow invariant. Every free parameter of `σ_C` must trace to exactly one of:

- (a) the context contract, frozen and hashed;
- (b) a measured physical quantity or published constant, with citation;
- (c) a fit on a declared calibration partition **whose outcome functional differs from the evaluation one**.

Anything else is a leakage failure.

**INV-24 (No Objective Feedback).** No parameter of the significance functional may be fitted using any signal derived from the reasoning stage or from the evaluation targets. Reasoning has no write path to `σ`.

**Rationale.** The real distinction from learned salience is not architectural ordering; it is that ASA forbids fitting significance to the reasoning objective. Under AD-24 that becomes something an auditor can check on the data-flow graph rather than something asserted in a diagram.

---

#### AD-26 — Personalised PageRank is a declared degenerate case; dominance is claimed only where it is real

**Remedies:** A7.

**Decision.** V1 states explicitly that personalised PageRank is the special case of the significance functional in which the licence automaton accepts all sequences, all compatibility predicates are trivially true, there is no abstention, no uncertainty, no selection correction, and the output has no referent or units.

The claim of superiority is correspondingly narrowed. **V1 does not claim to beat personalised PageRank on rank correlation.** It claims to dominate on four measurable axes it possesses and PPR does not:

1. calibrated effect-size estimation (PPR has no referent to be calibrated against);
2. correct abstention (PPR always answers);
3. selection-corrected estimation (PPR is uncorrected);
4. cross-context transfer (see AD-25).

**INV-26 (Baseline Mandatory).** Personalised PageRank with a designation-derived teleport vector is a required baseline in every context. A run omitting it is incomplete.

**Rationale.** A7 partially succeeded and the honest response is containment, not denial. Claiming to beat PPR at ranking would be an overclaim that a reviewer would test in an afternoon.

---

#### AD-25 — Cross-context transfer is the differentiating test; a supervised regressor is the upper anchor

**Remedies:** A6, A7; anticipates B3 (§8).

**Decision.** Two additions to the baseline set:

- **Supervised counterfactual regressor** — fitted directly on measured counterfactual ground truth with full feature access. Reported as an **upper anchor**, in the same status as an oracle, never as a peer baseline.
- **Cross-context transfer** as the primary differentiating metric: fit or configure on one context family, evaluate on a **held-out context family with a different outcome functional**.

**Rationale.** If significance is an estimator of a counterfactual, a supervised regressor will estimate it better in-distribution. That is expected and must be pre-conceded. The architecture's claim must be that its structural, non-fitted estimator **transfers to unseen contexts**, where a fitted regressor should not. This is where H3 becomes a real test with a real chance of failure.

**INV-25 (Transfer Reporting).** Every benchmark reports in-distribution and transfer performance separately. A claim of value based on in-distribution performance alone is inadmissible.

---

### 4.8 Ground truth and operating envelope

#### AD-29 — Ground-truth tiering with an explicit anchor/oracle distinction

**Remedies:** A6; V0 §9.

**Decision.** Four ground-truth families are retained from V0 with their epistemic statuses fixed and non-interchangeable:

| Family | Status | Role |
|---|---|---|
| **GT-B** counterfactual (leave-one-out physical integration) | **Primary target of estimation** | What σ estimates |
| **GT-A** structural catalogues | Validates the lower pipeline only | Never evidence about significance |
| **GT-D** simulation | Causal/developmental types; the only venue for measuring censoring bias directly | Within-model validity only |
| **GT-C** revealed human relevance | **Realism probe. Never ground truth.** | May never be cited as validation of correctness |

Closed-form physics (`GM/r²`) is an **anchor**, not a baseline: agreement with it is a success criterion, not a competition.

**INV-29 (Status Fixity).** A result citing GT-C as validation of correctness is invalid regardless of its numbers.

---

#### AD-27 — Declared operating envelope

**Remedies:** anticipates B5 (§8).

**Decision.** V1 declares the conditions under which it is fully operable:

1. a characterised selection model exists for the dataset;
2. the counterfactual outcome functional is computable for at least a subset sufficient to calibrate;
3. validity signatures are recoverable from source metadata;
4. at least *k* designations exist for each context contract.

Outside this envelope the architecture is expected to abstain heavily, and **that is the intended behaviour**, not a defect. Claims made outside the envelope are inadmissible.

**Rationale.** An architecture that does not state where it stops working will be evaluated where it does not work and will fail for uninteresting reasons.

---

#### AD-28 — Knob inventory, simplicity baseline, and the V2 simplification rule

**Remedies:** anticipates B9 (§8).

**Decision.** Three anti-complexity requirements:

1. **Knob inventory.** Every free parameter, threshold and policy choice in the architecture is enumerated in a single published register, with its provenance under AD-24. The total count is itself a reported benchmark metric.
2. **Simplicity baseline.** The simplest defensible estimator for each context — typically a single physical or catalogue quantity — is a mandatory baseline.
3. **The V2 rule.** If V1's added machinery does not measurably earn its complexity against the simplicity baseline, **the correct next version is a simplification, not a further elaboration.**

**Rationale.** V1 has more gates than V0. More gates means more researcher degrees of freedom and more places for silent defects. An architecture that can only grow is not a scientific architecture.

---

## 5. Invariant summary

| ID | Invariant | Remedies |
|---|---|---|
| INV-01 | No ordering may be derived from standing | A3 |
| INV-02 | No pre-context graph-derived numeric summary may exist | A3, A7 |
| INV-03 | Standing's rejection set must be emitted; deletion criterion predeclared | A3, B6 |
| INV-04 | Complete validity signature or inadmissible | A4, D2 |
| INV-05 | Two-level composition licence enforced on every traversal | A4 |
| INV-06 | `⊥` is enumerated and never contributes zero | A4 |
| INV-07 | Licence hash predates first dataset retrieval | A4, B2 |
| INV-08 | Centrality-family measures only on `G_C` | A4 |
| INV-09 | Every significance event names its referent and units | A1 |
| INV-10 | Dimensioned output; rank normalisation prohibited | D1, D2 |
| INV-11 | Non-empty designation required; no default global score | A1 |
| INV-12 | Every contributing path terminates in the designation | A1, A3 |
| INV-13 | Withdrawal semantics declared; cross-semantics comparison prohibited | A1, B7 |
| INV-14 | Predictions sealed before data contact | A5 |
| INV-15 | Genericity proof over ≥ k designations | A5, B1 |
| INV-16 | External-origin quota, counter-context pairing, expected-failure coverage | A5 |
| INV-17 | Detectability record present or explicitly unmodelled | A2 |
| INV-18 | Selection model + correction, or uncorrected flag + sensitivity bound | A2 |
| INV-19 | Observability correlation emitted; exceeding bound self-invalidates | A2 |
| INV-20 | Three typed abstentions, never merged | abstention |
| INV-21 | Abstention priced, budgeted, and neutrality-tested | B4 |
| INV-24 | No objective feedback into `σ` parameters | A8 |
| INV-25 | In-distribution and transfer reported separately | A6, A7, B3 |
| INV-26 | Personalised PageRank mandatory in every context | A7 |
| INV-29 | Ground-truth family statuses fixed and non-interchangeable | A6 |

---

## 6. Revised hypotheses

V0 established that the original hypothesis was a definition. V1 replaces it with three claims, each now guaranteed measurable **by architecture** rather than by good intentions.

**H1′ — Context Irreducibility.**
No context-independent estimator matches the counterfactual ground truth across the benchmark's context set as well as the designation-anchored estimator does.
*Architecturally instrumented by:* AD-11, AD-12 (anchoring makes a context-free variant a genuinely different computation, not a degenerate parameter setting) and AD-16 (paired counter-contexts measure it per context).
*Falsified if:* the best context-independent estimator lands within the predeclared non-inferiority margin.

**H2′ — Relational Counterfactual Estimability.**
Significance computed from licensed relational structure estimates the measured counterfactual effect with calibrated uncertainty, approaching the closed-form physical anchor where one exists.
*Falsified if:* estimates are materially miscalibrated; or a single intrinsic attribute matches the relational estimator; or the anchor is not approached at all.
*Note:* superiority over the anchor is **not** claimed and would be a false claim.

**H3′ — Constraint Value Under Transfer.**
The architectural constraints — standing gate, composition licence, selection correction, typed abstention — produce measurably better transfer to unseen context families than an unconstrained fitted estimator of equal access.
*Falsified if:* a supervised regressor transfers as well; or removing any constraint produces no degradation on its predeclared metric.
*This is the hypothesis most likely to fail, and it is where the architecture's value actually lives.*

---

## 7. Benchmark changes — additions only

Every change below adds an obligation. Nothing is relaxed.

**New mandatory emissions** (a run lacking any of these is malformed, not merely incomplete):
observability correlation `corr(σ, O)`; `⊥` enumeration by predicate; standing rejection set with the rule that would otherwise have admitted each item; abstention counts by type with reason chains; abstention effect-size distribution; knob count; units on every estimate; genericity proof; licence hash with timestamp ordering against dataset retrieval.

**New mandatory baselines:** personalised PageRank with designation-derived teleport (INV-26); permissive licence; random licence; simplicity baseline; supervised counterfactual regressor as upper anchor.

**New invalidating conditions** (added to V0's F1–F9, none of which is removed):

| # | Condition |
|---|---|
| F10 | Observability correlation exceeds the context's declared bound |
| F11 | Licence hash postdates first dataset retrieval |
| F12 | A context contract fails the genericity requirement |
| F13 | Prediction commitment postdates data contact |
| F14 | Abstention effect-size distribution differs materially and undeclared |
| F15 | Any significance event lacks units, referent, or withdrawal semantics |
| F16 | Significance events with differing withdrawal semantics compared |
| F17 | Rank normalisation applied to significance output |
| F18 | A centrality-family measure computed outside `G_C` |
| F19 | External-origin quota unmet, or no expected-failure context present |
| F20 | GT-C cited as validation of correctness |

**Unchanged and preserved:** every V0 failure condition F1–F9, every V0 success condition, and the prohibition on describing a demonstration as a validation.

---

## 8. Falsification of Version 1

Same discipline as V0 §8, applied to my own revision. Nine attacks. Four succeed outright, three succeed partially, two fail.

---

**B1 — The context contract is now expressive enough to contain the answer.**

V1 requires the context to declare a designation set, an outcome functional, withdrawal semantics, a licence restriction and a selection model. For the perturbation experiment, declaring `M_C` = ephemeris accuracy already encodes "gravity is what matters here". V0's contexts could be *flattering*; V1's contexts can be *informative*. Expressiveness is leakage surface.

**Outcome: succeeds against a naive reading.** **Remedied by AD-15 (genericity).** A contract that encodes target-specific knowledge cannot be instantiated unmodified over ten designations. The genericity proof is the test, and it is cheap to run and hard to fake.

**Residual:** genericity constrains *target-specific* smuggling but not *domain-specific* smuggling. Declaring the outcome functional is unavoidably an act of domain knowledge. I do not consider this eliminable — it is what makes the question well posed — but it must be stated: **V1 tests whether relational structure can estimate a counterfactual once the question is well posed. It does not test whether the question can be posed without domain knowledge.**

---

**B2 — The licence table is authored by the architecture's designers.**

If we write the composition licence, we can tune it until the experiment passes. That is fitting an ontology to a result.

**Outcome: succeeds.** **Remedied by AD-07**: freeze before data contact with a timestamp-ordered hash (INV-07, F11), plus mandatory permissive and random licence controls. If the random licence performs as well, the licence content is decorative and the N1 novelty claim is empty — and that finding must be reported.

**Residual:** freezing is a governance control, not a cryptographic one, when a single party controls both the licence and the clock. See B8.

---

**B3 — A supervised regressor will beat the structural estimator.**

If significance estimates a counterfactual, the best estimator is a regressor fitted to measured counterfactuals. Then ASA is a hand-built, worse version of a standard supervised baseline.

**Outcome: succeeds in-distribution, and this is conceded.** **Reframed by AD-25**: the regressor is an upper anchor, not a peer, and the differentiating claim moves to **cross-context transfer**. The architecture's bet is that a non-fitted structural estimator carries across outcome functionals where a fitted one does not.

**Residual: this is the most likely place for V1 to fail honestly.** If the regressor transfers as well, H3′ falls and the architecture has no demonstrated value. I estimate this is a real possibility and it should not be argued away when it happens.

---

**B4 — Tighten the gates and abstain on everything hard.**

Strict standing gate, narrow licence, demanding selection model — abstain on the difficult cases, look calibrated on the easy remainder. The abstention *budget* caps volume but not composition.

**Outcome: succeeds against the budget alone.** **Remedied by INV-21 (abstention neutrality)**: the effect-size distribution of abstained cases must not differ materially from answered cases, and the comparison is measurable against GT-B. Preferential abstention on high-effect cases becomes a reportable, penalised failure rather than an invisible advantage.

**Residual:** neutrality can only be tested where ground truth exists. Outside GT-B coverage, this control is unavailable, which reinforces AD-27's operating envelope.

---

**B5 — Selection models mostly do not exist.**

V1 requires a selection model or an abstention. For most real catalogues the selection function is unknown or only crudely characterised. Either the architecture abstains on nearly everything, or it accepts crude models whose correction introduces its own error.

**Outcome: succeeds, and is conceded as a scope limit.** **Handled by AD-27**: V1 declares its operating envelope. The first benchmark must use domains with characterised selection — simulations have exact selection functions; the Gaia DR3 open cluster census has a published one. Heavy abstention outside the envelope is intended behaviour.

**Residual: this materially narrows where V1 can be validated at all**, and that narrowing is a real cost of taking A2 seriously. I regard it as the correct trade, but it is a trade.

---

**B6 — The standing gate may be nothing but input validation renamed.**

If Reading B standing only decides admissibility, perhaps it is schema and provenance validation under a grander name, and the layer should be deleted rather than redefined.

**Outcome: possibly succeeds — and V1 pre-commits to acting on it.** **Handled by AD-03**: standing is retained *on probation* with a predeclared deletion criterion. If its rejection set is empty relative to schema validation, or its removal degrades nothing, V2 deletes the layer.

**This attack is not remedied. It is scheduled for resolution by evidence, with the answer allowed to be "delete our own component."**

---

**B7 — The withdrawal operator is underdetermined.**

"Remove the entity" has several inequivalent readings, and different readings yield different counterfactuals. An ambiguous `⊖` would reopen A1 by making σ's referent ambiguous.

**Outcome: succeeded against the first draft of AD-09; remedied by AD-13**, which enumerates the withdrawal semantics, requires declaration, and prohibits cross-semantics comparison (INV-13, F16).

**Residual:** the enumeration may be incomplete. New physical contexts may require semantics not listed, and adding one after seeing results is a benchmark-invalidating change.

---

**B8 — Commit–reveal is only as strong as the operator.**

A single party controls the predictions, the register, and the execution. They can decline to commit, commit several predictions and reveal the convenient one, or simply run the experiment first.

**Outcome: succeeds. Not fully remediable within a single-operator programme.** Mitigations: one commitment per context identity in an append-only register; the register pushed to the remote repository, whose timestamps are not operator-controlled, before data retrieval; the licence and dataset manifests ordered against the same clock (INV-07, INV-14).

**Residual, stated plainly: self-preregistration by a single party is weak evidence.** The honest fix is external review or a second independent operator holding the register. Until then, V1's preregistration should be described as a discipline, not a guarantee.

---

**B9 — V1 is more complex, and complexity is itself a threat to falsifiability.**

More gates mean more thresholds, more researcher degrees of freedom, and more places for silent defects. A more elaborate architecture can be *less* falsifiable in practice than a simple one, even while appearing more rigorous.

**Outcome: succeeds as a standing risk.** **Mitigated by AD-28**: a published knob inventory whose count is a reported metric, a mandatory simplicity baseline, and an explicit rule that if the machinery does not earn its complexity, **V2 is a simplification**.

**Residual: this attack cannot be closed, only monitored.** It should be re-run against every future version. An architecture whose response to criticism is always another layer is accumulating unfalsifiability, however disciplined each layer looks.

---

### 8.10 Verdict on Version 1

| Attack | Outcome | Disposition |
|---|---|---|
| B1 Context contains the answer | Succeeds naively | Remedied (AD-15); domain-knowledge residual stated |
| B2 Self-authored licence table | Succeeds | Remedied (AD-07); governance residual → B8 |
| B3 Supervised regressor wins | **Succeeds in-distribution** | Conceded; claim moved to transfer (AD-25) |
| B4 Abstain on the hard cases | Succeeds against budget alone | Remedied (INV-21); needs ground truth |
| B5 Selection models do not exist | **Succeeds** | Conceded as an operating-envelope limit (AD-27) |
| B6 Standing is input validation | **Possibly succeeds** | Scheduled for deletion-by-evidence (AD-03) |
| B7 Ambiguous withdrawal | Succeeded on first draft | Remedied (AD-13); enumeration completeness residual |
| B8 Weak self-preregistration | **Succeeds** | Mitigated only; needs an external party |
| B9 Complexity reduces falsifiability | Succeeds as standing risk | Monitored (AD-28); V2 rule |

**Four attacks survive remediation** — B3 in-distribution, B5, B6, B8 — and one (B9) is permanent. That is the honest state of Version 1. It is better than Version 0, where four attacks succeeded against the architecture itself; here the surviving attacks are about scope, evidence, governance and complexity rather than internal contradiction.

**No internal contradiction is known to remain in V1.** That is the specific improvement claimed, and it is the only one claimed.

---

## 9. What Version 1 gives up

Recorded so that these are not later mistaken for oversights.

1. **Superiority over physics.** Withdrawn permanently. Where a closed form exists it is the anchor and the ground truth.
2. **The significance-before-reasoning ordering claim.** Withdrawn. It describes attention.
3. **Beating personalised PageRank at ranking.** Not claimed. Dominance is claimed only on calibration, abstention, selection correction and transfer.
4. **Operation without a selection model.** Outside the declared envelope, the architecture abstains.
5. **Cross-context score comparison.** Only permitted within a shared outcome functional and withdrawal semantics.
6. **The standing layer's permanence.** It is on probation with a deletion criterion.
7. **Universality.** V1 is an architecture for estimating declared counterfactuals over heterogeneous relational evidence. It is not a theory of significance in general, and should stop being described as one.

---

## 10. Residual risk register

| # | Risk | Source | Status |
|---|---|---|---|
| RR-1 | Supervised regressor transfers as well as the structural estimator | B3 | **Open — most likely honest failure** |
| RR-2 | Selection models unavailable outside a narrow envelope | B5 | Open, scoped |
| RR-3 | Standing gate proves to be input validation | B6 | Open, deletion criterion set |
| RR-4 | Single-operator preregistration is weak | B8 | Open, needs external party |
| RR-5 | Complexity accumulates faster than falsifiability | B9 | Permanent, monitored |
| RR-6 | Domain knowledge enters through the outcome functional | B1 | Acknowledged, not eliminable |
| RR-7 | Withdrawal-semantics enumeration incomplete | B7 | Open |
| RR-8 | No astronomical data yet acquired | V0 R1 | **Unchanged and still the binding blocker** |
| RR-9 | Twenty decision-register items open | V0 R11 | Unchanged |
| RR-10 | Gaia DR4 (2 Dec 2026) obsoletes a DR3-frozen benchmark | V0 R6 | Unchanged |

**RR-8 is unchanged from V0 and is not addressed by any architectural work in this document.** No amount of architecture substitutes for a dataset.

---

## 11. What would make Version 2 necessary

Predeclared, so that V2 is triggered by evidence rather than by preference:

- Standing's rejection set is empty or its removal costs nothing → **delete the standing layer**.
- Random licence matches frozen licence → **delete the composition algebra**; N1 was empty.
- Supervised regressor transfers as well as the structural estimator → **the architecture has no demonstrated value**; report it and stop.
- Knob count grows while transfer performance does not → **V2 is a simplification**.
- Observability correlation cannot be brought below bound in any envelope → **the domain is unsuitable**; A2 wins permanently.

Each of these points at removing something we built. That is the intended shape of the criterion.

---

*End of ASTRO-RESEARCH-0002. Draft status. No architectural authority. Nothing in this document validates ASA, ASA-Astro, or any astronomical claim. `ASTRO-RESEARCH-0001` remains the criticism of record and is not superseded by this revision.*
