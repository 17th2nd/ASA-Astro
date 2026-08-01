# ASTRO-THEORY-0001 — Verification-Ready Change Map

**Purpose.** To let an independent mathematical reviewer locate every change between the prior and hardened editions without diffing prose.

**Prior edition.** commit `460b436`, blob `facdba01b4238283beafcda8c4e390f26c45937a`
**Hardened edition.** this working tree, same path
**Status of both.** Theory Candidate. Neither is verified.

**Reading note.** "Prior §" refers to section numbering of blob `facdba0`. "Revised §" refers to the hardened edition. Where a prior section has no counterpart the cell reads *(none)*, and where a revised section is wholly new the prior cell reads *(new)*.

---

## 1. Structural changes

| Prior § | Revised § | Reason | Finding | Semantic effect | Proof effect |
|---|---|---|---|---|---|
| *(none)* | Status block, Provenance limitation | Document must remain a Candidate and must disclose that the defect basis was not read | — | Removes any implication of verification | None |
| 3 Primitive objects | 3 Formal signature (3.1–3.6) | A single explicit signature is required before theorems | V3–V8, V13, V16 | Every carrier now typed and marked primitive/derived/optional/partial/context-indexed | All theorem hypotheses become checkable |
| 4 Axioms A1–A7 | 4 Axioms A1–A10 | Three gaps closed | V1, V9, V15 | Congruence, non-vacuity and consistency preconditions now axiomatic | Corollaries 3.1, 3.2 gain hypotheses |
| *(none)* | 9 Encodability | The central epistemic limitation was unproved | V17 | Framework declared non-falsifiable, as a theorem | New Theorem 10 and two corollaries |
| *(none)* | 12 Consistency witness | No witness existed | V18 | Consistency claimed only for a named fragment | New Proposition 12.1 |
| 11 Proven theorems | 13 Proven statements | Renumbering after insertions | — | None | None |
| 12 Proven limitations | 14 Limitations + open obligations | Obligations must be visible | V13, V18 | Three obligations recorded | OB-1, OB-2, OB-3 |

---

## 2. Signature changes

| Prior | Revised | Reason | Finding | Semantic effect | Proof effect |
|---|---|---|---|---|---|
| Def 3.4 *Arena*, elements "items" | Def 3.1 *Bearers* $\mathfrak{B}$; Def 3.8 *Operation assignment* $T_C$ | Bearers must be separate from states, linked by an explicit partial map | V3 | Bearers provably not in any state space; $T_C$ partial, so "not valuable under $C$" is expressible | Theorems 1, 2, 5, 6, 7, 14 restated over $\mathfrak{B}$; content unchanged |
| *(none)* | Obs 3.10 *No bearer composition* | Notation $b\circ a$ must be defined or avoided | V11, V12 | The "avoid" branch is taken explicitly, with the hypothesis that would otherwise be needed | None |
| Def 3.8 *Valuation space* $(V,\le_V)$ | Def 3.12 *Codomain classes* $\mathsf{W}_0$–$\mathsf{W}_4$ | Addition was used in a structure that guaranteed only an order | V5, V6 | Signed contrasts no longer forced into a codomain where $0$ is least | Theorem 7 restricted to $\mathsf{W}_1$; Theorem 10 requires $\mathsf{W}_2$; Theorem 5 hypotheses split per part |
| Def 3.10 *Reduction* on $\Delta(V)$ | Def 3.16 *Reduction* on a declared profile class | Domain and multiplicity handling were implicit | V7, V8 | Set / multiset / measure / probability-coupled distinguished; multiplicity preserved where declared | Theorem 1 and Prop 12.1 declare probability-coupled |
| *(none)* | Def 3.18 $\bot_{\mathrm{ind}}$, $\bot_{\mathrm{inc}}$, $\bot_{\mathrm{und}}$ | Three failure modes were conflated | V9, V15 | Indeterminate, inconsistent and undefined now distinct | Def 7.5 routes three cases |
| Def 6.1 *Context* (five components) | Def 3.14 *Context* (eight components) | $\mathcal{Y}_C$, $\approx_C$ and $W_C$ were not context components | V1, V16 | Context now carries its outcome space, indistinguishability and codomain | A2 now has eight components to check |
| *(none)* | Def 3.15 *Level of the evaluator* | The raw / quotient / congruent levels were mixed | V1 | The third level is adopted throughout and the others excluded | Theorem 4 depends on it |
| A3 with undefined $\iota_*$ | Def 3.21, Def 3.22, restated A3, Obs 3.23 | Transport was invoked but never defined | V4 | A3 becomes a well-formed equation; covariance distinguished from invariance | Theorem 2 hypothesis $\pi_*C=C$ now meaningful; prior Theorem 13 becomes checkable and is demoted |
| *(none)* | Def 3.19, Def 3.20 | Decision and kernel structure were used in §8 but never declared | V13, V14 | Marked optional enrichment | Theorem 5(ii),(iii) hypotheses |

---

## 3. Axiom changes

| Prior | Revised | Reason | Finding | Semantic effect | Proof effect |
|---|---|---|---|---|---|
| A3 | A3 restated with $\iota_W$ | Undefined transport | V4 | Covariance stated as an equation in $W'$ | Theorem 2, Corollary 14.2 |
| A4 | A4 restricted to $\mathsf{W}_1$ | $0_V$ required a distinguished least element | V5 | Nullity now well typed | Theorem 7 |
| A7 | A7 with reference to Def 8.10 | Cross-context comparison had no mechanism | V16 | Comparison defined only relative to a declared transport | Limitation 14.7 |
| *(none)* | **A8** Congruence | Quotient factorisation was unsupported | V1 | Congruence stated in exactly the required form | Theorem 4 |
| *(none)* | **A9** Non-vacuity | Empty comparison could yield a substantive value | V9 | Vacuous truth blocked by typing | Def 7.5, Corollary 3.2 |
| *(none)* | **A10** Consistency precondition | Empty compatible class was indistinguishable from undefined | V15 | $\bot_{\mathrm{inc}}$ separated | Corollaries 3.1, 3.2 |

---

## 4. Theorem changes

| Prior | Revised | Reason | Finding | Semantic effect | Proof effect |
|---|---|---|---|---|---|
| Thm 1 | Thm 1 | Hypotheses now explicit; codomain class and profile class declared | V5, V7 | None | Proof unchanged; construction now type-checks |
| Thm 2 | Thm 2 | $\pi_*C=C$ now defined | V4 | None | Proof unchanged, now checkable |
| Thm 3 | Thm 3 + **Obs 7.3** | Corollaries read more broadly than the theorem licensed | V19 | Seven non-claims listed exhaustively; uniqueness only modulo equality on $r(\mathfrak{M})$ | Proof unchanged |
| *(new)* | **Cor 3.3** *Induced outcome map* | The condition for a deterministic induced map was never stated | V10 | Exact iff condition supplied; three admissible representations tabulated in Obs 3.4 | Proved as an instance of Theorem 3 |
| *(new)* | **Thm 4** *Quotient descent* | Congruence needed a consequence | V1 | Descent holds iff A8; negative clause by counterexample | New proof |
| Thm 4 | **Thm 5** | $\arg\min$ without existence; no measurability | V13, V14 | (ii) now proved for **any** selection rule, attained or not — the theorem is strengthened | Proof of (ii) rewritten via $\mathcal{A}^*_\varepsilon\subseteq\mathcal{A}_C$; (iii) unchanged modulo integrability hypothesis |
| Thm 5 | **Thm 6** | Hypotheses; attainment noted for squared loss | V13, V14 | None | Constructions unchanged; attainment now remarked |
| Thm 6 | **Thm 7** | Codomain class | V5 | Restricted to $\mathsf{W}_1$ | Proof unchanged |
| Thm 7 | **Thm 8** | Hypotheses made explicit | V13 | None | Proof unchanged |
| Thm 8 | **Thm 9** | — | — | None | Proof unchanged |
| *(new)* | **Thm 10** *Universal encodability* | The framework's non-falsifiability was asserted nowhere and proved nowhere | V17 | **Principal result.** Any assignment is realisable by some context | New constructive proof |
| Thm 9 | **Thm 11** | — | — | None | Proof unchanged |
| Thm 10 | **Thm 12** | — | — | None | Proof unchanged |
| Cor 10.3 | **Cor 12.3** | — | — | None | Proof unchanged |
| Thm 11 | **Thm 13** | — | — | None | Proof unchanged |
| Thm 12 | **Thm 14** | — | — | None | Proof unchanged |
| **Thm 13** | **Cor 14.2** | One-line consequence of A3 with no content beyond it | V4, V19 | **Demoted.** Theorem status not retained for appearance | Proof reduces to a single application of A3; demotion recorded at Obs 11.3 |
| *(new)* | **Prop 12.1** *Consistency witness* | No witness existed | V18 | Consistency for the deterministic–decision fragment only | New proof, axiom by axiom |

---

## 5. Definition changes not covered above

| Prior | Revised | Reason | Finding | Semantic effect | Proof effect |
|---|---|---|---|---|---|
| Def 5.1 pointwise contrast | Def 5.1 with partiality | $\delta_C$ is partial | V9 | Undefined points explicit | Def 5.2 requires a.e. definedness |
| Def 5.2 contrast law | Def 5.2 contrast profile | Profile class must be declared | V7, V8 | Multiplicity handling explicit | Theorem 1 |
| Def 6.2 significance | Def 5.3 significance, partial | Three failure modes | V9, V15 | $\bot_{\mathrm{und}}$ routed | Everywhere |
| Def 7.3 identified set | Def 7.5 with three cases | Empty fibre | V15 | $\bot_{\mathrm{inc}}$ vs $\bot_{\mathrm{und}}$ | Corollary 3.2 |
| *(none)* | Def 7.7, Obs 7.8 | Sufficiency must not be called minimality | V2 | Four notions separated; no minimality claimed | None |
| *(none)* | Assumption 8.0, Obs 8.0.1 | Measurability never stated; integration into a preorder possible | V13 | §8 asserted only under stated hypotheses | Theorems 5, 6 |
| Def 8.2 decision significance | Def 8.2 infimum-based | $\arg\min$ | V14 | $\varepsilon$-optimality; $\bot_{\mathrm{und}}$ absent attainment at $\varepsilon=0$ | Theorem 5(ii) strengthened |
| Def 8.3 information significance | Def 8.4 with kernel | Kernel was informal | V13 | Markov kernel required | Theorem 5(iii) |
| *(none)* | Def 8.10, Obs 8.11 | Cross-context comparison had no mechanism | V16 | Comparison is $\bot_{\mathrm{und}}$ absent a declared transport | Limitation 14.7 |
| Obs 10.4 | Obs 10.7, 10.8, 10.9 | Language class, state size, prior art | V20 | Regular only for bounded registers; no finite-recognisability claim otherwise | None |

---

## 6. Rejections added to §16

| New | Reason | Finding |
|---|---|---|
| 16.14 *The framework has empirical content of its own* | Defeated by Theorem 10, Corollary 10.1 | V17 |
| 16.15 *Context is discovered from evidence* | $T_C$, $\delta_C$, $\rho_C$ are primitives of Def 3.14 | Retained scope |
| 16.16 *The framework derives its evaluator automatically* | Same, plus Theorem 10 | Retained scope |
| 16.17 *Standing* | No context-free ordering primitive; Theorems 7 and 8 | Retained scope |
| 16.18 *Mathematical or graph-theoretic novelty* | Observation 10.9 | V20 |
| 16.19 *Significance-first intelligence* | Not a statement of this theory | Retained scope |

Prior rejections 14.1–14.13 are preserved as 16.1–16.13 with proof references updated to the new numbering. **None was removed.**

---

## 7. Validation performed

Each check was run against the hardened edition. Automated structural checks are recorded as such and are **not** treated as mathematical verification.

| Audit | Method | Result |
|---|---|---|
| Notation | manual sweep of all symbols against §3 | Every symbol used is introduced in §3 or at first use |
| Type | manual, per theorem | Every theorem names its codomain class and form |
| Symbol definition | manual | No symbol used before definition |
| Theorem dependency | manual | Thm 4←A8; Cor 3.3←Thm 3; Thm 5←Asm 8.0; Thm 7←A4, $\mathsf{W}_1$; Thm 10←Def 3.12 $\mathsf{W}_2$; Cor 14.2←A3 |
| Proof dependency | manual | No proof invokes a statement later than itself |
| Empty domain | manual | A9, A10, Def 7.5 cover empty comparison set, empty fibre, undefined evaluator |
| Partial function | manual | $T_C$, $\delta_C$, $\rho_C$, $\odot$, $\sigma_C$ all marked partial |
| Quotient / congruence | manual | A8 + Def 3.15 + Thm 4; no quotient claim without A8 |
| Measurability | manual | Assumption 8.0; residual gap recorded as OB-2 |
| Optimiser existence | manual | No $\arg\min$ remains; $\varepsilon$-optimality or explicit attainment |
| Codomain operation | manual | No $\oplus$ in $\mathsf{W}_0$; $0$ not assumed least in $\mathsf{W}_2$ |
| Cross-context comparison | manual | Def 8.10 + Obs 8.11; A7 unviolated |
| Context independence | manual | Def 9.1 present; Obs 10.3 states it is insufficient alone |
| Prior-art novelty | manual | Obs 10.9 and §16.18; no novelty claim anywhere |
| Markdown / LaTeX delimiters | automated + manual | Balanced; see below |
| Internal cross-reference | manual | Every reference resolves to an existing numbered statement |

**Automated structural check.** Delimiter balance was checked mechanically over the three documents. This establishes only that the source parses; it establishes nothing mathematical.

---

## 8. What a reviewer should check first

1. **Theorem 10** — the principal result. Attempt to exhibit an assignment not realisable by any context.
2. **Proposition 12.1** and **Observation 12.2** — confirm the witness verifies all ten axioms and that the exclusion list is complete.
3. **Theorem 5(ii)** — confirm non-negativity holds without attainment.
4. **Theorem 4** — confirm the negative clause.
5. **The five Rejected dispositions** in the resolution record, against blob `facdba0`.
