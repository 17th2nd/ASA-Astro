# ASTRO-RESEARCH-0003 — Convergence Architecture

**Programme:** Adaptive Significance Architecture — Astronomy Validation Programme
**Date:** 2026-08-01
**Status:** DRAFT — working document in `09_Drafts/`. No architectural authority. Not a validation result.
**Inputs:** `ASTRO-RESEARCH-0001` (V0, criticism of record), `ASTRO-RESEARCH-0002` (V1, accepted candidate architecture), `09_Drafts/Codex/2026-08-01_Codex_Minimum-ASA-Disproof-Experiment.md`, and the six-angle programme decision.
**Method:** convergence only. No new concepts. The architecture below is smaller than V1 in every dimension.

## 0. Source provenance — stated because it bounds this document's authority

| Source | Held |
|---|---|
| Claude V0 (`0001`) | **In full** — in repository |
| Claude V1 (`0002`) | **In full** — in repository |
| Codex minimum disproof experiment | **In full** — in repository |
| Codex A, Codex C, Codex D | **In summary only** — via the programme decision text, not the review documents |
| Gemini, Codex B | **Not held.** No review text is in the repository or in this conversation |

This document therefore synthesises three full sources and three summarised ones, and cannot claim to represent Gemini or Codex B. Any convergence claim resting on those two angles is unsupported here and is recorded as unresolved (§U-7).

---

## 1. What convergence means here

V1 answered criticism by adding: 28 architectural decisions, 25 invariants, 11 new invalidating conditions. That was the correct response to *internal contradiction*, and it removed the contradictions it was aimed at. It was the wrong response to *scope inflation*, and it made B9 — complexity as a threat to falsifiability — worse.

Convergence is subtraction. Every section below either deletes a V1 element, replaces one with something smaller, or retains one unchanged. Nothing is added.

**Net change: 28 decisions → 11. 25 invariants → 14. One named layer deleted outright.**

---

## 2. Convergence architecture

```text
1  Evidence and provenance
2  Entity and relationship hypotheses
3  Joint uncertainty model
4  Context declaration
5  Contextual evidence adequacy          ← replaces Standing
6  Traversal, under declared semantics
      a. diffusion / search
      b. physical or logical composition
7  Counterfactual or decision functional
8  Effect distribution, interval, or abstention
9  Reasoning or action
```

**Deleted as a named layer:** Standing.
**Deleted as a claim:** new graph mathematics; significance-before-reasoning as an architecture; broad significance-first intelligence.
**Retained as a mechanism but withdrawn as a novelty claim:** instance-level composition validity (moved to Track B as an open question).

---

## 3. Retained design decisions

Eleven. Each answers three questions.

---

### C-01 — Standing is deleted; admissibility becomes contextual evidence adequacy

**Decision.** `Standing(entity) → admissible | inadmissible` is removed from the architecture. Two things replace it, both of which already existed in V1:

- **Well-formedness** — context-free. Schema validity, validity-signature completeness, provenance resolvability, unit coherence. This is input validation and is named as such.
- **Evidence adequacy(entity, context) → admit | reject | indeterminate** — contextual. Thresholded against the context's declared cost of false admission and false rejection.

Unordered structural descriptors survive only as features a context may consume. They are not a layer and carry no ordering.

**Which criticism does this resolve?** Codex A's decisive result: a context-independent scalar Standing either becomes intrinsic importance, hides a meta-context, or is an arbitrary compression; and it cannot add epistemic information because it is derived from the graph. It also resolves Codex A's second finding, which V1 missed — that even Standing-as-gate is not context-free, because an entity at 80% identity confidence may be admissible for exploratory analysis and inadmissible for spacecraft navigation.

**Which criticism does it reject?** It rejects V1's own AD-03, which retained Standing *on probation* pending benchmark evidence. The probation criterion is now redundant: Codex A's argument is analytic, not empirical, so waiting for a benchmark to decide it would be waiting for evidence that cannot bear on the question.

**Why?** An analytic defeat does not need an experiment. V1 kept the layer because it had built a gate for it; that is sunk-cost reasoning, not convergence.

---

### C-02 — Traversal splits by declared semantics; the composition licence applies only to inference

**Decision.** Two traversal mechanisms, never conflated:

| Mechanism | Licence required |
|---|---|
| **Diffusion / search** — random walks, spreading, retrieval, candidate generation | A declared transition policy. **No composition licence.** |
| **Physical or logical composition** — deriving a relation from a chain of relations | Composition rules: frame, epoch, dimension, validity interval, roles, model family, calibration and evidence dependency |

Every traversal declares which it is. Undeclared traversal is inadmissible.

**Which criticism does this resolve?** Codex A's correction to the path argument. It also resolves the underdetermination this leaves behind: a measure whose traversal semantics is undeclared is mathematically valid but scientifically uninterpretable.

**Which criticism does it reject?** It rejects my own claim, made in V0 §5.5 and hardened into V1's INV-08, that path-based centrality is *semantically invalid* on a graph whose relations are mostly non-transitive.

**Why?** The claim was over-broad and Codex A is right. Social friendship is non-transitive, yet random walks over friendship graphs are meaningful — because the walk models diffusion, not inference. Eigenvector centrality and betweenness are well defined on any graph. The defect V0 detected was real but misdiagnosed: it is not invalidity, it is **undeclared semantics**. V1's fix — confining all centrality to the composition-licensed subgraph — would have forbidden legitimate diffusion measures. This is a correction to my own work and the register in §Rejected records it as such.

---

### C-03 — Significance names exactly three quantities, never one

**Decision.** Three explicitly distinguished quantities. Never collapsed, never compared across kinds, never aggregated:

| Quantity | Definition |
|---|---|
| **Physical-effect significance** | Change in a declared observable under a declared intervention |
| **Decision significance** | Regret incurred by ignoring the entity, under a declared decision problem |
| **Information significance** | Value of obtaining further evidence about the entity, under a declared question |

Expert attention and graph centrality are **not** significance. Attention is a confounded proxy for one of the three; centrality is a structural descriptor.

**Which criticism does this resolve?** Codex D's finding that "significance" currently spans physical effect, utility, relevance, expert attention, information gain and centrality, and that these cannot be treated as interchangeable measurements of one latent property.

**Which criticism does it reject?** It rejects V1's AD-09, which defined significance solely as an estimator of counterfactual physical effect and presented that as the general definition.

**Why?** V1's definition was correct for one of the three and silently annexed the other two. That is the same error the programme was created to stop — collapsing distinct constructs into one score — committed one level up.

---

### C-04 — Significance is the contextual valuation of a factual–counterfactual contrast

**Decision.** For each of the three quantities, the form is the same:

```text
value = ϝ( outcome under the factual system,
           outcome under the declared counterfactual operation )
```

where the context declares the outcome, the counterfactual operation, and the discrepancy or utility function `ϝ`. A graph is useful only when it is a sufficient representation of the evidence and physical model needed to estimate that contrast.

**Which criticism does this resolve?** Codex A's positive formulation, and V0's A1 — the original hypothesis was a definition, not a hypothesis. This form is falsifiable pointwise because the contrast is measurable where the counterfactual is computable.

**Which criticism does it reject?** It rejects the "significance emerges" language in every prior document, including V0 and the original architecture.

**Why?** "Emerges" specifies no mechanism and cannot be wrong. A declared context determining which counterfactual difference is valued, and how, is a mechanism.

---

### C-05 — The counterfactual operation is declared from an enumeration

**Decision.** Retained unchanged from V1 AD-13. The withdrawal or intervention operation is chosen from a fixed enumeration and declared; results with differing operations are not comparable.

**Which criticism does this resolve?** V1's own B7 — "remove the entity" is underdetermined and an ambiguous operation reopens A1 by making the referent ambiguous.

**Which criticism does it reject?** None.

**Why?** The Codex experiment demonstrates the requirement concretely: its counterfactual is a **model-term** counterfactual — setting a candidate's direct acceleration on the target to zero while the DE440 background, which contains 343 asteroid perturbations, remains fixed. That is emphatically not "removing an asteroid from the Solar System." Without a declared operation, the two readings are indistinguishable and the result is uninterpretable.

---

### C-06 — Output is a distribution, an interval, or `indeterminate` — never a fabricated scalar

**Decision.** If the counterfactual is not identified from the evidence and assumptions, return an interval or `indeterminate`. Uncertainty remains joint and provenance-aware; it is not reduced to a point at any stage.

**Whether abstention is admissible is declared by the context.** Under a hard allocation budget, it is not.

**Which criticism does this resolve?** V1's abstention discipline, and Codex's constraint that under a fixed four-perturber budget an abstention counts as failure because the task *is* allocation.

**Which criticism does it reject?** It rejects V1's AD-20/INV-20 in their general form, which made typed abstention universally available.

**Why?** Both positions are right in their domain and V1 over-generalised one of them. A system that may refuse when the contrast is unidentifiable is being honest; a system that refuses when the task is to allocate a fixed budget is failing to perform the task. The context is the only thing that can tell them apart, and the context already carries an abstention policy.

---

### C-07 — Effect estimates are dimensioned; rank normalisation is prohibited

**Decision.** Retained unchanged from V1 AD-10. Values carry the units of the declared outcome. No within-run max-normalisation.

**Which criticism does this resolve?** V0 defects D1 and D2 — graph-relative scores that cannot be compared across graphs or calibrated against measurement.

**Which criticism does it reject?** None.

**Why?** The Codex primary endpoint is a ratio of dimensioned trajectory errors against a numerical convergence floor. A normalised score cannot enter that comparison at all.

---

### C-08 — Context is a complete valuation specification, frozen and hashed before results

**Decision.** A context declares: target; observer, frame and epoch; admissible evidence; outcome; counterfactual operation; discrepancy or utility; horizon; uncertainty and abstention rule. Frozen and content-hashed before scoring.

Two V1 requirements survive because the Codex experiment independently arrives at both:

- **Genericity** — one contract instantiated over a family of designations without modification. Codex applies a single frozen context specification across eight hash-ordered targets.
- **Counter-context pairing** — Codex retains two horizons because "horizon is the smallest physically meaningful change of context", and combines them into one result per target rather than scoring them as independent samples.

**Which criticism does this resolve?** V0's A5, contexts chosen to flatter. Genericity is the defence against a context that encodes its own answer.

**Which criticism does it reject?** It rejects V1's AD-16 in part: the external-origin quota and the mandatory expected-failure context are dropped.

**Why?** Both were compensating controls for a benchmark the programme designed for itself. The Codex experiment is constructed to terminate the programme; an expected-failure quota inside it is redundant, and its contexts are physical rather than curated, so an origin quota has nothing to police.

---

### C-09 — No objective feedback; the significance function may not see the outcome it is scored against

**Decision.** Retained from V1 AD-24. Parameters trace to the frozen context, to measured physical quantities, or to a calibration partition with a different outcome functional. Nothing else.

Codex's operational form: ASA's scoring rule, parameters, transformations and executable hash are frozen before target identities are revealed, and it may not consume any leave-one-out integration, future full-model trajectory, held-out residual, or quantity derived from them.

**Which criticism does this resolve?** V0's A8. The distinction from learned salience is not that significance is computed first — that describes attention's forward pass — but that it is not fitted to the objective it is judged by.

**Which criticism does it reject?** It rejects the significance-before-reasoning ordering as an architectural novelty.

**Why?** The ordering claim describes every attention-based model. Only the prohibition on fitting is distinctive, and only as a discipline, not as mathematics.

---

### C-10 — Baselines are the strongest existing method for the task, not straw comparators

**Decision.** One strong baseline: the method a domain practitioner would actually use. For perturber selection that is a tangent-linear variational calculation along the nominal trajectory. Both selectors receive identical physical quantities.

**Which criticism does this resolve?** Codex's exclusion of straw baselines, and V0's A6 — a one-line physical formula beats an elaborate architecture on its home problem.

**Which criticism does it reject?** It rejects V1's INV-26, which made personalised PageRank a mandatory baseline **in every context**.

**Why?** PPR remains the right baseline where no purpose-built method exists, because it is the closest prior art to a context-conditioned graph ranking. It is the wrong baseline where a purpose-built method does exist: beating PPR while losing to variational sensitivity is not a result an astrophysicist has any reason to care about. V1 universalised a locally correct requirement.

---

### C-11 — Selection-function machinery is scoped to where selection operates

**Decision.** Detectability records, selection models and the mandatory observability correlation are retained **for catalogue-derived work**, and are not carried into Track A.

**Which criticism does this resolve?** V0's A2 — brightness entering through catalogue topology — remains fully in force wherever the graph is assembled from a censored catalogue.

**Which criticism does it reject?** It rejects V1's INV-17/18/19 as universal requirements.

**Why?** In the Codex experiment the candidate set is a fixed, complete list of sixteen force terms supplied identically to both selectors. There is no censoring to correct, no observability gradient to leak through, and no selection model to declare. Requiring the machinery anyway would add apparatus that cannot affect the result — which is precisely the complexity B9 warns about.

---

## 4. Programme structure

Two tracks. **Their claims do not combine.** Either may fail while the other stands.

**Track A — Counterfactual astronomy benchmark.** The Codex minimum disproof experiment, unchanged in apparatus, with the three-outcome decision rule below.

**Track B — Physically valid relationship traversal.** Whether instance-level frame-, epoch-, unit- and model-aware composition rules offer anything not already available in temporal RDF, scientific knowledge graphs, dimensional-analysis systems, or typed query languages. This is the stronger novelty investigation and it does not depend on Track A.

### Track A decision rule

Codex's endpoint and preregistration are retained exactly: `R_t < 1` beyond the numerical floor on all eight targets, median `R_t ≤ 0.80`, no greater selection wall time, full release. Both horizons combine into one result per target; the eight targets are the independence unit, giving an exact sign test at `p = 0.0078125`.

What changes is only the **scope of the consequence**:

| Outcome | Consequence |
|---|---|
| **A — ASA loses materially** | Terminate the claim that ASA improves perturber allocation; terminate the solar-system counterfactual stream; terminate any claim of advantage over established sensitivity methods |
| **B — approximate match** | No demonstrated performance advantage. Possible auditability or representation benefit only, and only if separately proven |
| **C — ASA wins blind** | Proceed to replication and mechanism analysis. Claim exactly: *ASA improved perturber allocation in this frozen Gaia–DE440 benchmark* |

**Codex's anti-repair clause is retained in full and applies to all three outcomes:** no second catalogue, revised context, new weighting rule, or broader simulation programme follows a failure. A new programme requires a different independently motivated claim, not a repair of this benchmark.

**Which criticism does the three-outcome rule resolve?** That a loss to a purpose-built variational selector on its home problem does not establish that all context-conditioned relational significance models are worthless.

**Which criticism does it reject?** It rejects any reading of the three outcomes as a softening. Outcome A is terminal for the astronomy claim, and the anti-repair clause survives intact.

**Why?** The two positions were never in conflict. Codex's own text already scopes its conclusion — "a finite benchmark cannot refute every possible interpretation of ASA; it can decisively refute the programme's reason for asking astrophysicists to use it." The revision makes explicit what that sentence already implied, and adds nothing that permits the programme to escape a failure.

---

## Accepted criticisms

| # | Criticism | Source | Where resolved |
|---|---|---|---|
| AC-1 | A context-independent scalar Standing becomes intrinsic importance, hides a meta-context, or is arbitrary compression; it cannot add epistemic information | Codex A | C-01 — Standing deleted |
| AC-2 | An additive positive Standing term contradicts contextual nullity when an entity is irrelevant in some context | Codex A | C-01 |
| AC-3 | Standing-as-admissibility-gate is not context-free either; evidence thresholds depend on the costs of false admission and rejection | Codex A | C-01 — evidence adequacy is contextual |
| AC-4 | Non-transitivity does not invalidate centrality; the real defect is undeclared traversal semantics | Codex A | C-02 — diffusion and composition separated |
| AC-5 | ASA's representational machinery reduces to typed, attributed, temporal knowledge graphs with reified n-ary relations, perspective labels and event history | Codex C | §2 — graph-mathematics novelty withdrawn |
| AC-6 | ASA's additional needs belong to argumentation, probability, decision theory, game theory and concurrency, not a new branch of graph theory | Codex C | §2 |
| AC-7 | "Significance" spans several distinct constructs that are not interchangeable measurements of one latent property | Codex D | C-03 — three named quantities |
| AC-8 | The broad significance-first intelligence claim must be retired from the experimental programme | Codex D | §2 |
| AC-9 | Significance is the contextual valuation of a factual–counterfactual contrast, not fundamentally a graph score | Codex A | C-04 |
| AC-10 | The counterfactual must be a declared model-term operation, not an ambiguous removal | Codex experiment | C-05 |
| AC-11 | Straw baselines are worthless; the comparator must be the method a practitioner would use | Codex experiment | C-10 |
| AC-12 | Under a hard allocation budget, abstention is failure | Codex experiment | C-06 |
| AC-13 | Explanation, provenance and context-sensitivity scores cannot be promoted to co-primary endpoints or rescue a failed operational comparison | Codex experiment | Track A endpoint unchanged |
| AC-14 | The original terminal rule over-reached: a loss terminates the astronomy claim, not every relational significance model | Programme decision | Track A three outcomes |
| AC-15 | ASA must demonstrate benefit beyond sensitivity analysis, counterfactual reasoning and decision theory rather than renaming them | Programme decision | Track A Outcome C claim wording |
| AC-16 | Complexity is itself a threat to falsifiability | Claude V1 B9 | §1 — 28 decisions to 11, 25 invariants to 14 |

---

## Rejected criticisms

| # | Criticism | Rejected because |
|---|---|---|
| RJ-1 | *Path-based centrality is semantically invalid on a graph of mostly non-transitive relations* — Claude V0 §5.5, hardened into V1 INV-08 | **Over-broad, and wrong as stated.** Centrality is well defined on any graph. Codex A's counterexample holds: friendship is non-transitive yet random walks over it are meaningful, because the walk models diffusion rather than inference. The valid residue — that a measure with undeclared traversal semantics is scientifically underdetermined — is retained in C-02. This is a correction to my own prior work. |
| RJ-2 | *Standing should be retained on probation pending benchmark evidence* — Claude V1 AD-03 | The defeat is analytic, not empirical. No benchmark result can bear on whether a context-free scalar is a context-free scalar. Waiting was sunk-cost reasoning. |
| RJ-3 | *Significance is an estimator of counterfactual physical effect* — Claude V1 AD-09, as a general definition | Correct for one of three quantities and silently annexes the other two. Repeats the collapse error one level up. Retained in scoped form in C-03 and C-04. |
| RJ-4 | *Typed abstention is universally available* — Claude V1 AD-20 | Correct where the contrast may be unidentifiable; wrong where the task is allocation under a fixed budget. Context now decides. |
| RJ-5 | *Personalised PageRank is a mandatory baseline in every context* — Claude V1 INV-26 | Correct where no purpose-built method exists; actively misleading where one does. Beating PPR while losing to variational sensitivity is not a result worth reporting. |
| RJ-6 | *Selection-function machinery is universally required* — Claude V1 INV-17/18/19 | The Track A candidate set is fixed, complete and identical for both selectors. There is no censoring to correct. Retained for catalogue-derived work only. |
| RJ-7 | *External-origin quota and a mandatory expected-failure context* — Claude V1 AD-16 | Compensating controls for a self-designed benchmark. Track A is designed to terminate the programme and its contexts are physical; both controls have nothing to police. |
| RJ-8 | *Requiring ASA to beat a purpose-built method is unfair, so the experiment should be changed* | **Rejected as grounds for changing the experiment; accepted as grounds for scoping the conclusion.** The claim under test is explicitly incremental — whether ASA adds anything after ordinary celestial mechanics is present. If context-conditioned allocation under relational evidence is the pitch, this is its cleanest instance. |
| RJ-9 | *No internal contradiction remains in V1* — Claude V1 §8.10 | False. Codex A found one V1 missed: the admissibility gate's context-independence. The claim is withdrawn. |
| RJ-10 | *Astronomy removes human interpretation* — original programme framing | Already withdrawn in V0 §2.2 and not revived. Catalogue types, membership criteria and object boundaries are curated human artefacts. |

---

## Unresolved criticisms

| # | Criticism | Status |
|---|---|---|
| U-1 | A supervised regressor fitted to measured counterfactuals will beat a structural estimator in-distribution; the architecture's value therefore rests on cross-context transfer | **Unresolved, and Track A cannot resolve it.** Track A is a single-domain allocation task with no transfer arm. |
| U-2 | Single-operator preregistration is weak evidence | **Partly mitigated, unresolved.** Codex assigns the held-out χ² gate to an independent orbit-dynamics reviewer. The ASA-side parameter and executable freeze has no equivalent external holder. |
| U-3 | Complexity accumulates faster than falsifiability | **Improved, not closed.** This document subtracts; the risk returns with the next addition and must be re-run against every version. |
| U-4 | No astronomical data has been acquired | **Unchanged and binding.** Track A requires Gaia DR3 SSO epoch astrometry with its published covariance model, DE440, `SB441-N16`, and an ASSIST-class variational integrator. None is in hand. |
| U-5 | The 8-of-8 rule has high specificity and low sensitivity | **Unresolved.** Against a method genuinely better on 80% of targets, the rule passes only ~17% of the time. A loss must therefore be reported as *no advantage demonstrated at this power*, not as *no advantage exists*. Whether the programme accepts that asymmetry is not settled. |
| U-6 | Whether Track B has any content at all | **Unresolved, and it has no disproof design.** Track A has a preregistered kill rule; Track B has none. Until it does, Track B cannot fail, which means it cannot yet be called research. |
| U-7 | The Gemini and Codex B review findings | **Not held.** No text in the repository or this conversation. Any convergence claim resting on them is unsupported. |
| U-8 | Whether contextual evidence adequacy has content beyond ordinary decision-theoretic thresholding | **Unresolved.** C-01 replaced a defeated construct with a correct one; it did not show the correct one is novel. |

---

## Research questions remaining

1. Does instance-level composition validity — frame, epoch, dimension, validity interval, roles, model family, calibration and evidence dependency, evaluated per instance rather than per schema — enforce anything that temporal RDF, a units ontology, SHACL and OWL cannot enforce in combination?
2. Is there an identifiable class of scientific inference where declared composition semantics prevents an error that a standards stack admits, demonstrable on a worked example that an expert rejects and the stack accepts?
3. For which of the three significance quantities — physical-effect, decision, information — does a relational representation help, and is the answer the same for all three?
4. Can the diffusion/composition distinction be given a formal criterion, or does it remain a modelling judgement declared by the analyst?
5. What is the power of the Track A decision rule against the range of effect sizes that would be practically meaningful to an orbital dynamicist, and what conclusion does a loss at that power license?
6. Is there a domain where the counterfactual is computable, the evidence is relational and heterogeneous, and no purpose-built sensitivity method already exists — and if not, what is the architecture for?
7. Does anything survive if Track A returns Outcome A and Track B's question 1 is answered *no*?
