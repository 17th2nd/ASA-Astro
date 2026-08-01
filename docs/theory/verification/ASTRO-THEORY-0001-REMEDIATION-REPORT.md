# ASTRO-THEORY-0001 — Remediation Report

**Subject:** `docs/theory/ASTRO-THEORY-0001.md`
**Defect basis:** independent verification report, disposition **NOT FORMALLY SOUND**, findings AV-001 – AV-028. Read in full; not modified.
**Pre-remediation blob:** `08a2257aaea6e5f23b316682025022b62d834d68`, confirmed at `HEAD` before mutation.
**Baseline:** `HEAD = origin/main = a9df42f901c7a67a7198910d7c7f58c002dd59bb`, branch `main`, 0 ahead / 0 behind.

---

## 1. Remediation summary

The verification was accepted essentially in full. Every counterexample it supplied was reconstructed independently, and every one held. **No finding was rejected**, and none was relabelled to a lower severity.

The remediation is **subtraction-dominant**. The prior candidate failed not because it lacked machinery but because it asserted more than it had proved. Accordingly:

| Measure | Count |
|---|---|
| Findings adjudicated | **28 of 28** |
| Accepted | 11 |
| Accepted with Modification | 16 |
| Deferred Open Obligation | 1 |
| Rejected with Proof | 0 |
| Theorems withdrawn or replaced | **6** |
| Corollaries withdrawn | **11** |
| Definitions withdrawn | **6** |
| Axioms demoted out of the formal system | **2** |
| Limitations withdrawn | 7 · narrowed 2 · added 2 |
| Rejections withdrawn | 7 · narrowed 7 · retained 5 |
| Whole subsections withdrawn | **1** (recognisability) |
| Open obligations, of which blocking | 4, of which **1 blocking** |

**Three statements of the prior edition were outright false**, each with an independently reproduced counterexample: Corollary 3.1 (computability), Corollary 3.2 (forced abstention), and Theorem 7 (additive context-free scalar). A fourth, Theorem 4, was false under one reading and incomplete under the other. All four are withdrawn; two are replaced by correctly hypothesised statements.

**The single most consequential change** is the withdrawal of the prior Corollary 10.1 — *"the unrestricted framework has no empirical content whatever."* This was the candidate's principal epistemic claim and it did not follow from its theorem. It is replaced by Corollary 10.1′, a bounded single-context statement about the deterministic contrast form only. **The remediated document draws no conclusion about the empirical content of the framework as a whole.**

### Did the central theory survive?

**Yes, in reduced form.** The central proposition — that significance is a contextual valuation of a factual/counterfactual contrast, well defined only when the context supplies its components — survives. What did not survive is the surrounding apparatus of universal negative conclusions that the prior edition had built on top of it. The theory is smaller, and its remaining claims match their proofs.

---

## 2. Blocking findings resolved

Fifteen Blocking findings, each closed under exactly one of the four permitted outcomes.

| Finding | Outcome | Resolution |
|---|---|---|
| AV-001 | Withdrawn | `𝔄_C` deleted; `μ_C` is the component; three profile classes deleted; `I(W)` and `Ŵ` defined |
| AV-002 | Repaired with proof | Extended action `ι̂_W` defined on intervals and bottoms; all seven components transported |
| AV-004 | Withdrawn + narrowed | Undefined profile classes deleted; Definition 5.3 case table made exhaustive, closing the `0 < μ(Ω) < 1` branch |
| AV-005 | Withdrawn | A1 and A6 demoted to non-formal design principles, cited by no proof; A5, A9, A10 formalised as typed predicates |
| AV-009 | Withdrawn | Corollary 3.1 withdrawn as **false**; no computability claim remains anywhere |
| AV-010 | Withdrawn + narrowed | Corollary 3.2 withdrawn as **false**; Theorem 3.2′ proved under an explicit totality hypothesis |
| AV-011 | Withdrawn + replaced | Theorem 4 withdrawn; Theorem 4′ proved on `D̄_C` with the pullback relation stated exactly |
| AV-014 | Withdrawn + narrowed | Theorem 7 withdrawn as **false**; Theorem 7′ proved on a nullity-closed family |
| AV-017 | Repaired with proof | Projection evaluator replaces subtraction; the proof now needs no algebraic hypothesis at all |
| AV-018 | Withdrawn + narrowed | "All forms" label, Corollary 10.1 and Corollary 10.2 withdrawn; Corollary 10.1′ bounded to the deterministic form |
| AV-019 | Repaired | Complete composition signature with `U`, `E`, `src`, `tgt`, primitive `⊙`, endpoint coherence |
| AV-020 | Withdrawn + replaced | Corollaries 12.2–12.3 withdrawn; Theorem 12′ gives an explicit instance-level construction |
| AV-022 | Withdrawn | Recognisability subsection withdrawn in full; Open Question 15.6 reopened |
| AV-024 | Withdrawn + replaced | Proposition 12.1 withdrawn; Proposition 11.1 checks A3 for a **nontrivial** involution over a context set **proved closed** under transport |
| AV-027 | Withdrawn + narrowed | Limitation and rejection sections rebuilt from the post-remediation dependency closure |

---

## 3. Blocking findings remaining

**None of the twenty-eight findings remains unresolved.**

One **blocking obligation is created and retained as blocking**, arising from AV-024 and AV-025:

> **OB-1 — Full-signature consistency.** Proposition 11.1 establishes consistency only for the deterministic fragment with a `W₁` codomain, and A3 only over the finite morphism universe `𝒢 = {id, ȷ}`. Consistency is **not** established for: codomain classes `W₂` and `W₂^m`; interval or bottom-valued outputs; non-trivial `≈_C`; decision structure; evidence structure; non-atomic measures; the composition signature of §10; or A3 over the class of all representation morphisms.

This is stated as blocking in the theory document (§15) and in Observation 11.1.2, which carries the binding exclusion list. **The document does not call the full theory consistent anywhere.**

Non-blocking obligations: **OB-2** (measurability of `δ^b_C` assumed, not derived), **OB-3** (existence conditions for a regular evidence structure), **OB-4** (formalise DP-1/DP-2 or show neither is needed).

---

## 4. Theorems withdrawn

| Prior statement | Ground |
|---|---|
| **Corollary 3.1** — computability from the representation | **False.** Measurable factorisation is not an algorithm; `1_A` for non-computable `A` is a counterexample |
| **Corollary 3.2** — forced abstention in every non-sufficient case | **False.** Non-sufficiency includes failure of totality, under which every fibre may carry one value |
| **Theorem 4** — quotient descent | **False** under the total reading; **incomplete** under the partial reading |
| **Theorem 7** — triviality of an additive context-free scalar | **False.** The A4 nullity witness need not lie in the family assumed to decompose |
| **Corollary 6.1** — no common latent quantity | Relies on an undefined latent quantity and an unsupported monotone-map argument |
| **Corollary 8.1** — no epistemic role for derived summaries | **False.** A derived summary is informative to an observer lacking `R` |
| **Corollaries 9.1–9.2** — cross-arena incomparability, uncalibratability | Do not follow from Theorem 9 |
| **Corollary 10.1** — no empirical content whatever | Not proved; other forms are constrained by Theorem 5; single-context only |
| **Corollary 10.2** — exhaustive sources of empirical content | Exhaustiveness never argued |
| **Corollaries 12.2–12.3** — universal bracketing dependence, substructure | Universal overreach; "substructure" undefined |
| **Theorem 2** — designation necessity | Displayed equality is an instance of A3; "underlying structure" undefined |
| **Theorem 14, Corollary 14.1 (2nd clause)** — structural valuation | Tautological once typed; the causal clause is not a consequence |
| **Proposition 12.1** — consistency witness | Missing component; vacuous A3 check; context set not closed under transport |
| **Observations 10.7–10.9** — recognisability, state count, prior-art subsumption | Undefined objects; missing finiteness and effectiveness; unquantified universal claim |
| **Axioms A1, A6** | Not predicates over the signature; demoted to DP-1, DP-2 |

## 5. Theorems narrowed

| Statement | Narrowing |
|---|---|
| **Theorem 1** | Labelled existential; contexts completed; no universal corollary drawn |
| **Theorem 3** | Final σ-algebra declared; `h` total; codomain any measurable space; `𝖵 ≠ ∅` |
| **Theorem 5(i)** | Depends on the now-defined location functional |
| **Theorem 5(iii)** | Restricted to a regular evidence structure (Definition 3.14) |
| **Theorem 6** | `ρ =` mean, `ε = 0` with attainment, complete contexts, part (iii) computed exactly |
| **Theorem 7′** | Requires a nullity-closed family |
| **Theorem 10′** | Deterministic contrast form only, with a projection evaluator; explicitly not effect, decision, information or composition |
| **Theorem 11** | Conditional on its hypothesis that `κ` is not type-determined; the type-determined case explicitly conceded |
| **Theorem 12′, 13′** | Existential over an exhibited signature |
| **Corollary 6.2** | Fixed context, fixed group, declared codomain |

**Verified unchanged:** Theorem 5(ii) — the verifier's own assessment — Theorem 8's two identities, and Theorem 9's inequality.

---

## 6. Consistency status

**Established:** the deterministic fragment. Proposition 11.1 exhibits a model with `𝔅 = {b₁,b₂}`, `𝔐 = ℝ²` Borel, `r = id`, a `W₁` codomain, three contexts, and a declared morphism universe `𝒢 = {id, ȷ}` with `ȷ` the coordinate-swap involution. All eight formal axioms are checked. **A3 is checked non-vacuously**: the transported context `ȷ_*C₁` is computed from Definition 3.17 and shown to satisfy the covariance equation, and `𝒞` is proved closed under `𝒢`.

**Not established:** everything in Observation 11.1.2′s exclusion list. **OB-1, blocking.**

**Not claimed anywhere:** consistency of the full signature. The fragment witness does not silently support the whole theory; the exclusion list is stated in the theory document itself, not only here.

---

## 7. Validation performed

| Audit | Method | Result |
|---|---|---|
| Definition completeness | manual | Every symbol in a formal claim is defined or the claim is withdrawn |
| Type | manual, per theorem | Each theorem names its codomain class and form |
| Domain/codomain | manual | `ρ_C : Δ(W_C) ⇀ Ŵ_C`; `δ_C` partial on `D_C`; `⊙ : κ → E` |
| Quantifier | manual | Theorem 1 existential; Theorem 7′ carries its family hypothesis; no universal claim rests on a single example |
| Partiality | manual | `T_C`, `δ_C`, `ρ_C`, `σ_C`, `δ̄_C`, `[[·]]_comp` all marked partial |
| Empty domain | manual | A9, A10, Definition 5.3 row 2, Definition 7.5 |
| Quotient/congruence | manual | A8 with Theorem 4′ on `D̄_C`; saturation stated |
| Measurability | manual | Assumption 8.0; class `W₂^m` isolates measurable subtraction; OB-2 open |
| Integrability | manual | Assumption 8.0; Definition 3.14; OB-3 open |
| Optimiser existence | manual | No `argmin`; ε-optimality, or attainment stated |
| Representation morphism | manual | Definitions 3.15–3.17; extended action on `Ŵ` |
| Context indexing | manual | `𝒴_C`, `W_C`, `ρ_C`, `T_C`, `δ_C`, `≈_C` all indexed |
| Theorem dependency | manual | Thm 3.2′←Thm 3; Cor 3.3←Thm 3; Thm 4′←A8; Thm 5←Asm 8.0 + Def 3.14; Thm 7′←A4-closure; Cor 6.2←A3; Cor 10.1′←Thm 10′ |
| Proof reconstruction | manual | Every retained proof re-derived from the remediated definitions |
| Counterexample search | manual | All four verifier counterexamples reproduced; all hold |
| Consistency model | manual | Proposition 11.1 checked axiom by axiom |
| Universal encodability | manual | Proof rebuilt on the projection evaluator; scope cut to match |
| Notation | manual | No symbol overloaded across incompatible types |
| Theorem numbering | manual | Primes mark replacements; withdrawn numbers not reused |
| Cross-reference | mechanical + manual | All resolve; no reference to a nonexistent section |
| Markdown/LaTeX delimiters | mechanical | Balanced |

**Mechanical checks do not constitute mathematical verification.** They establish only that the source parses and that references resolve.

---

## 8. Re-verification readiness

The candidate is offered for fresh independent re-verification. A re-verifier should prioritise:

1. **Theorem 7′** — confirm hypothesis (a) is exactly what the prior proof needed, and that the verifier's countermodel no longer satisfies the hypotheses.
2. **Theorem 3.2′** — confirm the totality hypothesis excludes the counterexample, and that the non-totality branch is routed to `⊥_und` and not to a two-element set.
3. **Theorem 4′** — confirm uniqueness is claimed only on `D̄_C`, and check the saturation clause against both prior counterexamples.
4. **Theorem 10′** — confirm the projection evaluator is measurable without algebraic hypotheses, and that the conclusion is not extrapolated beyond the deterministic form. **Attempt to falsify Corollary 10.1′.**
5. **Proposition 11.1** — confirm `𝒞` is closed under `𝒢`, recompute `ȷ_*C₁`, and confirm the A3 check is non-vacuous.
6. **Observation 11.1.2** — confirm the exclusion list is complete, and that no statement anywhere claims consistency beyond the fragment.
7. **§13** — confirm every withdrawal listed is genuinely absent from the remediated text, and that no withdrawn statement survives implicitly in a limitation or rejection.
8. **§4.1** — confirm no proof cites DP-1 or DP-2.

**Known limitations of this remediation:**

- OB-1 is blocking and unresolved by design; the theory is consistent only on a fragment.
- OB-2, OB-3, OB-4 remain open.
- The composition signature (§10) is complete but its theorems are existential only; nothing general is proved about composition.
- No empirical claim, novelty claim, or freeze is made or implied.

**Final disposition of this remediation:**

> **ASTRO-THEORY-0001 REMEDIATED WITH EXPLICIT BLOCKING OBLIGATIONS**

The blocking obligation is **OB-1**, full-signature consistency. It is recorded as blocking in the theory document, in the adjudication record, and here.
