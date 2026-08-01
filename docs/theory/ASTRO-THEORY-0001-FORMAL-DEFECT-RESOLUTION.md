# ASTRO-THEORY-0001 — Formal Defect Resolution Record

**Subject:** `docs/theory/ASTRO-THEORY-0001.md`
**Status of subject after this record:** **Theory Candidate.** Not verified. Not frozen. Not Version 1.
**Source candidate blob at inspection:** `facdba01b4238283beafcda8c4e390f26c45937a`
**Repository state at inspection:** `HEAD = origin/main = 460b4365485b361aa234c6e20ae022066328ab99`, branch `main`, no staged files.

---

## 0. Provenance of the defect basis — read first

**The Codex mathematical verification report was not located in the repository and has not been read by the author of this record.**

A repository-wide search for the report and for its distinctive vocabulary returned nothing:

| Construct cited by V1–V20 | Occurrences in source candidate |
|---|---|
| `bearer` | 0 |
| `minimal` / minimality claim | 0 |
| contextual outcome equivalence $\sim_c$ | 0 |
| symbols $q$, $K$ | 0 |
| aggregation operator | 0 |
| bearer composition $b \circ a$ | 0 |
| transformation composition $T_b$ | 0 |
| profile | 0 |

The findings were received in prose. Six of them — V2, V7, V8, V11, V12 and part of V17 — cite constructs that do not occur anywhere in the source candidate. **This is evidence that the verification report was written against a different artefact.**

Consequences, stated plainly:

1. No claim is made here that "the Codex verification report has been discharged." What has been discharged is **the findings as transmitted**, each translated to the source candidate where a translation exists.
2. Where no translation exists, the disposition is **Rejected — construct absent from source**, with the reason recorded. A repair has not been fabricated to make a finding appear resolved.
3. Independent verification must first establish which artefact the report targets. If it targets a different document, this record does not apply to it.

---

## 1. Executive disposition

| Measure | Count |
|---|---|
| Findings dispositioned | 20 of 20 |
| Accepted | 11 |
| Accepted with Modification | 4 |
| Rejected — construct absent from source | 5 |
| Withdrawn | 0 |
| Deferred as Open | 0 (three *new* open obligations were created: OB-1, OB-2, OB-3) |
| Theorems retained unchanged in content | 9 |
| Theorems narrowed | 3 |
| Theorems demoted | 1 |
| Theorems added | 3 |
| Axioms added | 3 |
| Definitions added | 14 |

**The prior edition was not silently overwritten.** It remains in repository history at commit `460b436`, blob `facdba0`, and the changes are enumerated in `ASTRO-THEORY-0001-CHANGE-MAP.md`. Three statements of the prior edition were withdrawn or demoted, and each withdrawal is recorded in §3 and §7 below rather than removed without trace.

---

## 2. V1–V20 resolution matrix

---

### V1 — Quotient compatibility

**Defect statement.** The nullity condition does not ensure the contrast evaluator factors through contextual equivalence classes; the level at which the evaluator is defined is not stated.

**Disposition.** **Accepted with Modification.**

**Affected.** Prior edition had no contextual outcome equivalence and made no quotient-level sufficiency claim, so the defect as stated could not arise. The *underlying* requirement — that the level be declared and congruence stated if a quotient is used — did apply and was unmet.

**Exact repair.** Added Definition 3.15 fixing the level as **raw outcomes subject to congruence**; added Axiom **A8** stating the congruence condition in exactly the required form; added **Theorem 4 (Quotient descent)** with proof, including the negative clause that without A8 no map on classes exists in general.

**Mathematical justification.** A8 is precisely the well-definedness condition for the universal property of the quotient. Theorem 4's negative clause is by explicit counterexample on a two-point outcome space.

**Remaining assumptions.** $\approx_C$ is optional; where undeclared, A8 is vacuous and no quotient claim is made.

**Downstream impact.** None. No prior theorem used a quotient.

**New proof obligation.** None.

**Verification status.** Repair internally checkable. Correspondence to the original finding **unconfirmed** — see §0.

---

### V2 — Minimality overclaim

**Defect statement.** The claim that the ordered pair of contextual outcome classes is universally minimal must be withdrawn or narrowed.

**Disposition.** **Rejected — construct absent from source.**

**Affected.** Nothing. The source candidate contains no minimality claim; the word does not occur, and no construction is described as minimal, universal, initial or terminal.

**Exact repair.** None required. Prophylactically added **Definition 7.7** distinguishing the four notions the finding requires be kept apart — sufficiency, minimal sufficiency relative to an evaluator, the distinguishability bit, and the kernel quotient — and **Observation 7.8** stating explicitly that no minimality is claimed.

**Mathematical justification.** A rejection on grounds of absence requires no mathematics; the added definitions prevent the defect from arising later.

**Remaining assumptions.** None.

**Downstream impact.** None.

**New proof obligation.** None.

**Verification status.** Rejection is checkable by inspection of the prior blob. **This finding is evidence the report targets a different artefact.**

---

### V3 — Bearer map

**Defect statement.** A separate bearer map is required; a state-space map must not be applied to bearers unless bearers are embedded in states.

**Disposition.** **Accepted.**

**Affected.** Prior Definition 3.4 ("arena", "items") left the relation between valued things and models informal; operations were indexed by items with no typed map.

**Exact repair.** Added **Definition 3.1** ($\mathfrak{B}$, bearers, explicitly not a subset of any state space) and **Definition 3.8** (the operation assignment $T_C : \mathfrak{B} \rightharpoonup \mathrm{Op}(\mathfrak{M})$, partial and context-indexed) as the sole link. Added **Observation 3.9** recording that no map with domain $\mathfrak{M}$ is applied to an element of $\mathfrak{B}$.

**Mathematical justification.** Typing. $T_C$ has domain $\mathfrak{B}$ and codomain $\mathrm{Op}(\mathfrak{M})$; no composition in the document applies an $\mathfrak{M}$-domain map to $\mathfrak{B}$.

**Remaining assumptions.** $T_C$ is partial; a bearer with $T_C(b)$ undefined is not valuable under $C$, yielding $\bot_{\mathrm{und}}$ by Definition 5.3.

**Downstream impact.** Theorems 1, 2, 5, 6, 7, 14 restated over $\mathfrak{B}$ with $T_C$; content unchanged.

**New proof obligation.** None.

**Verification status.** Repair internally checkable.

---

### V4 — Representation morphisms and covariance

**Defect statement.** Representation morphisms must be defined over all relevant types; transported evaluator covariance is not invariance under arbitrary coordinate change; the value-preserving transformations must be stated precisely.

**Disposition.** **Accepted.**

**Affected.** Prior Axiom A3 invoked an undefined transport $\iota_*$ and a structure isomorphism defined only over the relational structure. Prior Theorem 13 depended on this and was therefore not fully checkable.

**Exact repair.** Added **Definition 3.21** (representation morphism as a four-component family over bearers, models, outcomes and codomain) and **Definition 3.22** (transported context, component by component, all eight components). Restated **A3** as covariance with the explicit $\iota_W$ on the right-hand side. Added **Observation 3.23** stating that covariance is not invariance under arbitrary reparametrisation, and naming the value-preserving transformations as exactly the morphisms of Definition 3.21 acting as in Definition 3.22.

**Mathematical justification.** With Definition 3.22 supplying $\iota_*C$ componentwise, A3 is a well-formed equation between elements of $W'$.

**Remaining assumptions.** $\iota_W$ must be an isomorphism *in the declared codomain class*; a map preserving order but not $\oplus$ is not a morphism for a $\mathsf{W}_1$ codomain.

**Downstream impact.** Theorem 2 now has a well-defined hypothesis $\pi_*C = C$ with $\iota_W = \mathrm{id}$. Prior Theorem 13 demoted — see V19 and §7.

**New proof obligation.** None.

**Verification status.** Repair internally checkable.

---

### V5 — Codomain structure

**Defect statement.** Significance codomains must not be required to be merely a pointed preorder while addition is used undefined.

**Disposition.** **Accepted.**

**Affected.** Prior Definition 3.8 gave $V$ only a partial order, while A4 referred to $0_V$ (no distinguished element guaranteed) and Theorem 6 used real addition.

**Exact repair.** Added **Definition 3.12** with five codomain classes $\mathsf{W}_0$–$\mathsf{W}_4$, each with its declared structure and permitted operations. Every theorem now names its required class.

**Mathematical justification.** Each operation used is licensed by the declared class: order only in $\mathsf{W}_0$; $\oplus$ and $0$ least in $\mathsf{W}_1$; subtraction and sign in $\mathsf{W}_2$.

**Remaining assumptions.** A context declares exactly one class.

**Downstream impact.** Theorem 7 restricted to $\mathsf{W}_1$; A4 restricted to $\mathsf{W}_1$ so that $0_{W_C}$ exists and is least; Theorem 10 requires $\mathsf{W}_2$ for subtraction.

**New proof obligation.** None.

**Verification status.** Repair internally checkable.

---

### V6 — Signed contrasts and metric hypotheses

**Defect statement.** Signed contrasts must not be forced into a codomain where zero is least; triangle inequalities require an ordered commutative monoid or metric codomain explicitly.

**Disposition.** **Accepted.**

**Affected.** Prior Definition 3.9 mapped into a single $V$ with no distinction between magnitude and signed contrast.

**Exact repair.** $\mathsf{W}_1$ (magnitude, $0$ least, monoid, supports triangle inequalities) and $\mathsf{W}_2$ (signed, ordered abelian group, $0$ **not** least) are separated in Definition 3.12. **Observation 3.13** forbids assuming $0$ least in $\mathsf{W}_2$. Definition 8.1 (effect) requires $\mathsf{W}_1$ and a metric $d_Y$; Definitions 8.2 and 8.4 require $\mathsf{W}_2$ realised in $\mathbb{R}$.

**Mathematical justification.** Decision and information significance are differences of risks and are signed objects in principle; they are proved non-negative in Theorem 5 by optimality and concavity, not by codomain fiat. This is the substantive point: non-negativity is now a *theorem*, not a typing assumption.

**Remaining assumptions.** Where a triangle inequality is invoked, $\mathsf{W}_1$ with $\oplus$ is required. No such inequality is currently invoked.

**Downstream impact.** Theorem 5 hypotheses stated per part.

**New proof obligation.** None.

**Verification status.** Repair internally checkable.

---

### V7 — Aggregation type and domain

**Defect statement.** The type and domain of each aggregation operator must be defined.

**Disposition.** **Accepted with Modification.**

**Affected.** The source candidate has no aggregation operator in the sense the finding appears to intend. Its only aggregation-like component is the reduction $\rho$, whose domain was given as $\Delta(V)$ with no declaration mechanism.

**Exact repair.** **Definition 3.16** now types $\rho_C$ as a partial map from a **declared profile class** $\mathcal{P}_C$ to $W_C \cup \mathcal{I}(W_C) \cup \{\bot_{\mathrm{ind}},\bot_{\mathrm{inc}},\bot_{\mathrm{und}}\}$, with the profile class one of four named options.

**Mathematical justification.** Typing.

**Remaining assumptions.** The profile class is declared, not inferred (Observation 3.17).

**Downstream impact.** Theorem 1 and Proposition 12.1 declare the probability-coupled class.

**New proof obligation.** None.

**Verification status.** Repair internally checkable. Correspondence to the original finding **unconfirmed**.

---

### V8 — Multiplicity preservation

**Defect statement.** Multiplicity or probability weight must be preserved where aggregation depends on it; set-, multiset-, measure- and probability-coupled profiles must be distinguished.

**Disposition.** **Accepted.**

**Affected.** Prior $\Delta(V)$ silently fixed the probability-coupled case and offered no alternative.

**Exact repair.** The four profile classes are tabulated in **Definition 3.16** with an explicit multiplicity column. **Observation 3.17** declares a context ill-formed if its valuation depends on multiplicity while it declares the set-valued class.

**Mathematical justification.** Typing.

**Remaining assumptions.** None beyond declaration.

**Downstream impact.** None on existing theorems.

**New proof obligation.** None.

**Verification status.** Repair internally checkable.

---

### V9 — Empty comparator sets

**Defect statement.** Evaluation must be partial or typed-indeterminate when no admissible comparison exists; vacuous truth must not produce a substantive value.

**Disposition.** **Accepted.**

**Affected.** Prior Definition 7.3 formed an identified set that could be empty, and prior corollaries did not say what an empty set yields.

**Exact repair.** Added **Axiom A9** (a valuation quantified over an empty comparison set is $\bot_{\mathrm{und}}$); added **Definition 3.18** separating $\bot_{\mathrm{ind}}$, $\bot_{\mathrm{inc}}$ and $\bot_{\mathrm{und}}$; restated **Definition 7.5** to route the empty-fibre and nowhere-defined cases to $\bot_{\mathrm{inc}}$ and $\bot_{\mathrm{und}}$ respectively.

**Mathematical justification.** An infimum or supremum over the empty set is $+\infty$ or $-\infty$, and a universally quantified statement over the empty set is vacuously true; both would yield substantive values from no evidence. A9 blocks this by typing.

**Remaining assumptions.** None.

**Downstream impact.** Corollary 3.2 now presupposes a nonempty fibre.

**New proof obligation.** None.

**Verification status.** Repair internally checkable.

---

### V10 — Intervention mapping

**Defect statement.** It must not be claimed that an intervention on model space always induces a deterministic map on observable state space; the exact existence condition must be stated.

**Disposition.** **Accepted with Modification.**

**Affected.** The prior edition defined $\tau : \mathfrak{M}\to\mathfrak{M}$ and composed on $\mathfrak{M}$, so it never asserted an induced outcome map — but it also never stated the condition, leaving the question open to misreading.

**Exact repair.** Added **Corollary 3.3** giving the exact condition: an induced $\phi$ with $M_C\circ\tau = \phi\circ M_C$ exists **iff** $M_C\circ\tau$ is constant on the fibres of $M_C$, with $\phi$ unique on $M_C(\mathfrak{M})$. Added **Observation 3.4** tabulating the three admissible representations — deterministic (under the condition), relational, kernel — and recording that §5 never requires a deterministic induced map because Definition 5.1 composes on $\mathfrak{M}$.

**Mathematical justification.** Corollary 3.3 is Theorem 3 applied with $r := M_C$ and $g := M_C\circ\tau$. No new machinery is needed.

**Remaining assumptions.** The kernel representation requires a disintegration of $\mu_C$ along $M_C$, which exists under standard Borel conditions not assumed globally here.

**Downstream impact.** None; no theorem used an induced outcome map.

**New proof obligation.** None.

**Verification status.** Repair internally checkable.

---

### V11 — Bearer composition

**Defect statement.** It must be defined whether bearers have a partial composition operation.

**Disposition.** **Rejected — construct absent from source.**

**Affected.** Nothing. The source candidate contains no bearer composition, and the notation $b\circ a$ does not occur.

**Exact repair.** None required. Prophylactically added **Observation 3.10** declaring that no composition on $\mathfrak{B}$ is defined, that $b\circ a$ is not used, and that any composite statement would require the additional hypothesis $T_C(b\circ a) = T_C(b)\circ T_C(a)$, which the theory neither supplies nor assumes.

**Mathematical justification.** Rejection on grounds of absence.

**Remaining assumptions.** None.

**Downstream impact.** None.

**New proof obligation.** None.

**Verification status.** Checkable by inspection of the prior blob. **Evidence the report targets a different artefact.**

---

### V12 — Composite-significance hypothesis

**Defect statement.** Every composite-significance result must explicitly assume $T_{b\circ a} = T_b \circ T_a$ or avoid the notation.

**Disposition.** **Rejected — construct absent from source.**

**Affected.** Nothing. There is no composite-significance result in the source candidate.

**Exact repair.** None required. **Observation 3.10** takes the "avoid the notation" branch explicitly, and states the hypothesis that would be required if the branch were ever abandoned. Composition is confined to operations (composition of measurable maps) and relation instances (§10).

**Mathematical justification.** Rejection on grounds of absence.

**Remaining assumptions.** None.

**Downstream impact.** None.

**New proof obligation.** None.

**Verification status.** Checkable by inspection. **Evidence the report targets a different artefact.**

---

### V13 — Measurability

**Defect statement.** All measurable-space assumptions required for probabilistic significance must be stated; integration into a general preorder must not occur.

**Disposition.** **Accepted.**

**Affected.** Prior Definitions 8.2 and 8.3 and prior Theorem 4 took expectations with no measurability or integrability hypothesis, and prior Definition 3.10 admitted $\Delta(V)$ for a $V$ carrying only a partial order.

**Exact repair.** Added **Assumption 8.0** stating measurability of $M_C$, of every $\tau$, and of $\delta_C$; a $\sigma$-algebra on $W_C$ making $\delta^{\,b}_C$ measurable; existence and finiteness of every expectation written; Markov-kernel status for every kernel; and nonemptiness of $\mathfrak{M}_x$. Added **Observation 8.0.1** stating that no integral is taken into a $\mathsf{W}_0$ codomain and that the theory supplies no integration theory for a general preorder.

**Mathematical justification.** Every integral in §8 is now over $\mathbb{R}$, where Lebesgue integration is available.

**Remaining assumptions.** Measurability of $\delta^{\,b}_C$ is **assumed, not derived** — recorded as **OB-2**.

**Downstream impact.** Theorem 5 and Theorem 6 are asserted only under Assumption 8.0.

**New proof obligation.** **OB-2** (conditions sufficient for measurability of $\delta^{\,b}_C$); **OB-3** (conditions for integrability of $\mathfrak{r}(\mu_C^{K_b})$).

**Verification status.** Repair internally checkable; OB-2 and OB-3 open.

---

### V14 — Decision optimiser existence

**Defect statement.** Infimum-based definitions must be used where optimisers may not exist, or attainment must be assumed explicitly; $\arg\min$ must not be used without existence conditions.

**Disposition.** **Accepted.**

**Affected.** Prior Definition 8.2 used $\alpha^*(\nu) \in \arg\min$ with no existence condition, and prior Theorem 4(ii) relied on it.

**Exact repair.** **Definition 8.2** rewritten with $\mathfrak{r}(\nu) := \inf_\alpha \mathbb{E}_\nu L$, the $\varepsilon$-optimal set $\mathcal{A}^*_\varepsilon$ (nonempty for $\varepsilon>0$ by definition of infimum), and significance defined as an infimum over $\mathcal{A}^*_\varepsilon(\mu_C^\tau)$ minus $\mathfrak{r}(\mu_C)$. For $\varepsilon = 0$ attainment is required explicitly and the value is $\bot_{\mathrm{und}}$ absent it. Added **Observation 8.3** recording that no $\arg\min$ is used.

**Mathematical justification.** Theorem 5(ii) now proves non-negativity **without** attainment: $\mathbb{E}_{\mu_C}L(\alpha,\cdot) \ge \mathfrak{r}(\mu_C)$ for every $\alpha \in \mathcal{A}_C$, and $\mathcal{A}^*_\varepsilon \subseteq \mathcal{A}_C$, so the infimum over the subset preserves the bound. The repair strengthens the theorem.

**Remaining assumptions.** $\mathfrak{r}$ finite; $\varepsilon$ declared.

**Downstream impact.** Theorem 6(i)–(iii) use squared loss on $\mathbb{R}$, for which attainment holds and is noted, so the constructions remain valid.

**New proof obligation.** None.

**Verification status.** Repair internally checkable.

---

### V15 — Empty model class

**Defect statement.** The model class consistent with the evidence must be nonempty before identifiability is defined; an empty class is inconsistency, not identified significance.

**Disposition.** **Accepted.**

**Affected.** Prior Definition 7.3 formed $\mathcal{S}_C(a,x)$ over $r^{-1}(x)$ without requiring it nonempty; an empty class would have produced an empty identified set indistinguishable from an undefined evaluator.

**Exact repair.** Added **Axiom A10** (identifiability notions defined only for a nonempty compatible class; empty yields $\bot_{\mathrm{inc}}$). Added **Definition 7.2** ($\mathfrak{M}_x := r^{-1}(x)$). Restated **Definition 7.5** to distinguish three cases: nonempty fibre with defined evaluator; empty fibre yielding $\bot_{\mathrm{inc}}$; nonempty fibre with nowhere-defined evaluator yielding $\bot_{\mathrm{und}}$.

**Mathematical justification.** The three cases have different remedies — respectively none, revision of the evidence or model, and supply of a missing component — and are therefore separated.

**Remaining assumptions.** None.

**Downstream impact.** Corollary 3.1 and Corollary 3.2 now carry A10.

**New proof obligation.** None.

**Verification status.** Repair internally checkable.

---

### V16 — Context-dependent codomains

**Defect statement.** Significance must be a context-indexed family or dependent type; cross-context comparison requires an explicit transport.

**Disposition.** **Accepted.**

**Affected.** Prior Definition 3.8 gave a single global $V$ while A7 asserted values from distinct contexts are not combined — a latent type inconsistency.

**Exact repair.** $\mathcal{Y}_C$ and $W_C$ are **context-indexed** throughout (Definitions 3.5, 3.12, 3.14), and $\sigma$ is a context-indexed partial family (Definition 5.3). Added **Definition 8.10** (cross-context transport as a declared order-embedding $t : W_C \to W_{C'}$) and **Observation 8.11** (the theory distinguishes none; absent a declared $t$, comparison is $\bot_{\mathrm{und}}$, not false and not zero).

**Mathematical justification.** Typing, plus A7.

**Remaining assumptions.** A transport, where used, must be declared and is not derived.

**Downstream impact.** Corollary 1.1 and Limitation 14.7 are stated within this typing.

**New proof obligation.** None.

**Verification status.** Repair internally checkable.

---

### V17 — Arbitrary context encoding

**Defect statement.** The unrestricted framework can encode arbitrary assigned rankings; this must not be concealed. A formal independence condition is required, and the consequence — that the unrestricted theory is not empirically falsifiable — must be stated.

**Disposition.** **Accepted**, and strengthened beyond what the finding requires.

**Affected.** The prior edition contained only Observation 2.2 ("choice of context is prior to the theory"), which understated the problem and proved nothing. The finding's specific symbols $q$ and $K$ do not occur in the source; the substance applies regardless and is accepted in full.

**Exact repair.** Added **§9** in its entirety:

- **Definition 9.1 (Independent instantiation)** — the formal independence condition: every component of Definition 3.14 fixed by a procedure not depending on the values $\sigma_C$ subsequently produces.
- **Theorem 10 (Universal encodability)** with proof — for any $f : \mathfrak{B}\to W$ with $W$ in class $\mathsf{W}_2$, there is a context $C$ with $\sigma_C = f$.
- **Corollary 10.1** — the unrestricted framework excludes no assignment, forbids no observation, and is not empirically falsifiable.
- **Corollary 10.2** — empirical content arises only from independently constrained primitives and independent instantiation.
- **Observation 10.3** — Definition 9.1 does not by itself create empirical content.
- **Observation 10.4** — the consequence in the required plain form.
- **§16.14** — the corresponding rejection.

**Mathematical justification.** The proof of Theorem 10 is constructive: $\mathfrak{M} := W$, $M_C := \mathrm{id}_W$, $\mu_C := \delta_{0_W}$, $\delta_C := $ subtraction, $T_C(b) := $ the constant map to $f(b)$. Then $\delta^{\,b}_C \equiv f(b)$ and $\sigma_C(b) = f(b)$. Every component is measurable and every axiom is respected.

**Remaining assumptions.** $W$ in class $\mathsf{W}_2$ (subtraction required); singletons measurable.

**Downstream impact.** This is the strongest result in the document and subordinates every other. It is recorded as Limitation 14.9 and referenced from Observation 1.2 so that a reader meets it early.

**New proof obligation.** None.

**Verification status.** Repair internally checkable. **This is the finding whose acceptance most changes the document's claims.**

---

### V18 — Consistency witness

**Defect statement.** A complete model of the actual formal signature must be provided; consistency must not be claimed for structures the witness does not instantiate; alternatively the claim must be limited to a named deterministic fragment.

**Disposition.** **Accepted with Modification** — the alternative branch is taken.

**Affected.** The prior edition provided **no** consistency witness at all. Prior Corollary 1.2 established only that A4 is satisfiable.

**Exact repair.** Added **Proposition 12.1** exhibiting a model $\mathcal{W}$ with $\mathfrak{B}$, $\mathfrak{M}$, $r$, three contexts, a decision structure, and an axiom-by-axiom verification of A1–A10. Added **Observation 12.2** limiting the claim explicitly and listing every uninstantiated structure: non-trivial $\approx_C$; codomain classes $\mathsf{W}_0$, $\mathsf{W}_3$, $\mathsf{W}_4$; the set-, multiset- and measure-valued profile classes; the evidence-kernel structure; non-atomic knowledge states; the path structure of §10.

**Mathematical justification.** Each axiom is verified against the exhibited model in the proof. The limitation is a statement about what the model does not instantiate and requires no proof.

**Remaining assumptions.** The witness uses an atomic knowledge state, so it does not exercise integration.

**Downstream impact.** Any theorem quantifying over the full signature is now supported only to the extent of the fragment.

**New proof obligation.** **OB-1** — consistency of the full signature.

**Verification status.** Fragment consistency internally checkable. Full consistency **open**.

---

### V19 — Final theorem scope

**Defect statement.** The factorisation theorem must state exactly what it proves, and claim no quotient factorisation, uniqueness beyond realised-pair equivalence, minimality, identifiability, empirical prediction, or representation invariance beyond explicit structure-preserving maps.

**Disposition.** **Accepted.**

**Affected.** Prior Theorem 3 was correctly stated as the factorisation lemma but was followed by Corollaries 3.1 and 3.2 that read more broadly than the theorem licensed, and by no scope limitation.

**Exact repair.** **Theorem 3** restated with explicit hypotheses, conclusion, and an *applies to* line. Added **Observation 7.3** listing exhaustively the seven things the theorem does not establish, in the order the finding specifies, and stating that no corollary extends it to any of them. Uniqueness of $h$ is now stated only modulo equality on $r(\mathfrak{M})$. Minimality is separately disclaimed in Observation 7.8.

**Mathematical justification.** The proof is unchanged and remains the standard factorisation argument; only the surrounding claims are narrowed.

**Remaining assumptions.** $\mathcal{R}$ carries the $\sigma$-algebra induced by $r$; this is now stated in the hypotheses rather than left to the proof.

**Downstream impact.** Corollaries 3.1, 3.2 and the new 3.3 are all now visibly within scope.

**New proof obligation.** None.

**Verification status.** Repair internally checkable. Note: the finding calls this the *final* theorem; in the source candidate it is Theorem 3 and the final theorem is a different statement. **Minor evidence of artefact mismatch.**

---

### V20 — Path recognisability

**Defect statement.** The class of path languages supported must be stated; arbitrary path-history constraints must not be implied finitely recognisable; state-size consequences must be given if full history is retained; the prior-art conclusion must be preserved.

**Disposition.** **Accepted.**

**Affected.** Prior Observation 10.4 named the register-automaton carrier but stated no language class, no bound, and no computational consequence.

**Exact repair.** Added **Observation 10.7** giving the product $U\times Q\times\mathcal{S}$ and splitting two cases: finite $\mathcal{S}$ yields a regular language in the product alphabet with state count $|U|\cdot|Q|\cdot|\mathcal{S}|$; unbounded $\mathcal{S}$ yields an infinite-state automaton whose language **need not be regular**, with no finite-recognisability claim. Added **Observation 10.8** stating the consequence for an instance retaining full history. Added **Observation 10.9** preserving the prior-art conclusion that the machinery is established guarded/register-automaton and data-path theory and **not novel**.

**Mathematical justification.** The finite case is the standard product construction. The unbounded case makes no positive claim, so none requires proof.

**Remaining assumptions.** None.

**Downstream impact.** None on Theorems 11–13, which concern the structure and not its recognisability.

**New proof obligation.** None.

**Verification status.** Repair internally checkable.

---

## 3. Statements withdrawn

| Prior statement | Reason |
|---|---|
| Prior Observation 2.2, insofar as it implied that the exogeneity of context choice was a minor scoping remark | Superseded by §9. The issue is not scoping; it is that the unrestricted framework has no empirical content (Theorem 10, Corollary 10.1). |
| Prior claim, implicit in Definition 3.8, that a single global valuation space $V$ suffices | Withdrawn as a type error; replaced by context-indexed $W_C$ per V16. |
| Prior Theorem 13 (Artefact exclusion) as a theorem | Demoted — see §7. |

---

## 4. Statements repaired

| Prior | Repair | Finding |
|---|---|---|
| Def. 3.4 arena/items | Def. 3.1 bearers + Def. 3.8 operation assignment | V3 |
| Def. 3.8 valuation space | Def. 3.12 five codomain classes | V5, V6 |
| Def. 3.10 reduction | Def. 3.16 typed reduction with declared profile class | V7, V8 |
| A3 with undefined transport | Def. 3.21, Def. 3.22, restated A3, Obs. 3.23 | V4 |
| Def. 7.3 identified set | Def. 7.5 with three typed cases | V9, V15 |
| Def. 8.2 with $\arg\min$ | Def. 8.2 infimum-based with $\varepsilon$-optimality | V14 |
| Def. 8.3 information significance | Def. 8.4 with explicit kernel and integrability | V13 |
| Thm 3 unbounded corollaries | Thm 3 + Obs. 7.3 exhaustive scope | V19 |
| Obs. 10.4 register carrier | Obs. 10.7–10.9 with language class and state size | V20 |

---

## 5. Theorems retained

Content unchanged; hypotheses now explicit. Prior numbering in brackets.

Theorem 1 [1] order reversal · Theorem 2 [2] designation necessity · Theorem 3 [3] factorisation · Theorem 7 [6] triviality of additive context-free valuation · Theorem 8 [7] no epistemic gain · Theorem 9 [8] normalisation arena-dependence · Theorem 11 [9] type-level licensing · Theorem 12 [10] non-associativity · Theorem 13 [11] semantic separation · Theorem 14 [12] orbit constancy.

## 6. Theorems narrowed

| Theorem | Narrowing | Finding |
|---|---|---|
| Theorem 3 [3] | Scope limitation Observation 7.3; uniqueness only modulo equality on $r(\mathfrak{M})$ | V19 |
| Theorem 5 [4] non-negativity | Hypotheses split per part; Assumption 8.0; $\varepsilon$-optimality replaces attainment in (ii) | V13, V14 |
| Theorem 7 [6] | Restricted to codomain class $\mathsf{W}_1$ | V5 |

## 7. Theorems demoted

| Prior | Now | Reason |
|---|---|---|
| Theorem 13 (Artefact exclusion) | **Corollary 14.2** | It is a one-line consequence of A3 with no content beyond the axiom. Theorem status is not retained for appearance. Recorded at Observation 11.3. |

**No statement was demoted to Conjecture.** Every retained theorem has a proof completed from the preceding definitions.

## 8. Definitions replaced or added

Added: 3.1 bearers · 3.8 operation assignment · 3.10 no bearer composition · 3.12 codomain classes · 3.14 context (eight components) · 3.15 evaluator level · 3.16 typed reduction and profile classes · 3.18 indeterminacy symbols · 3.19 decision problem · 3.20 evidence kernel · 3.21 representation morphism · 3.22 transported context · 7.2 compatible model class · 7.7 four distinct notions · 8.10 cross-context transport · 9.1 independent instantiation · 11.2 artefact morphism.

Replaced: prior 3.4 (arena) → 3.1 + 3.8 · prior 3.8 (valuation space) → 3.12 · prior 3.10 (reduction) → 3.16 · prior 7.3 (identified set) → 7.5.

## 9. New assumptions

| ID | Assumption | Introduced for |
|---|---|---|
| A8 | Congruence of $\delta_C$ with $\approx_C$ where declared | V1 |
| A9 | Non-vacuity: empty comparison set yields $\bot_{\mathrm{und}}$ | V9 |
| A10 | Consistency precondition: nonempty compatible model class | V15 |
| Assumption 8.0 | Measurability and integrability throughout §8 | V13 |
| Declared $\varepsilon > 0$, or attainment | Decision significance well-defined | V14 |
| Declared profile class | Reduction domain fixed | V7, V8 |
| Declared codomain class | Operations licensed | V5, V6 |
| Declared transport for cross-context comparison | A7 | V16 |

## 10. Remaining open proof obligations

**OB-1.** Consistency of the full signature. Proposition 12.1 covers only the deterministic–decision fragment; Observation 12.2 lists every uninstantiated structure. **Blocking for any claim of consistency beyond the fragment.**

**OB-2.** Conditions on $M_C$, $\tau$ and $\delta_C$ sufficient for measurability of $\delta^{\,b}_C$. Currently assumed in Assumption 8.0.

**OB-3.** Conditions guaranteeing integrability of $\mathfrak{r}(\mu_C^{K_b})$ in Theorem 5(iii).

## 11. Remaining epistemic limitations

1. **The unrestricted framework is not empirically falsifiable** (Theorem 10, Corollary 10.1). This is proved, not conceded, and it bounds every other claim in the document.
2. The reduction $\rho_C$ is not determined by the theory (Limitation 14.4).
3. Designation is exogenous (Limitation 14.8).
4. Recognisability is conditional on bounded register content (Limitation 14.10).
5. **The defect basis itself is unconfirmed** (§0). This is an epistemic limitation of *this record*, not of the theory.

## 12. Verification handoff

An independent verifier should, in order:

1. **Locate the Codex mathematical verification report** and determine which artefact it targets. If it targets a document other than blob `facdba0`, this record does not apply and must be redone.
2. Confirm the five **Rejected — construct absent from source** dispositions (V2, V7 in part, V11, V12, V17 notation) by inspecting blob `facdba0` at commit `460b436`.
3. Check the three new theorems — **Theorem 4** (quotient descent), **Theorem 10** (universal encodability), **Corollary 3.3** (induced outcome map) — against the preceding definitions.
4. Check that **Theorem 5(ii)** is now proved without attainment.
5. Check **Proposition 12.1** axiom by axiom, and confirm that **Observation 12.2** excludes everything the witness omits.
6. Attempt to falsify **Theorem 10**: exhibit an assignment $f$ not realisable by any context. Success would overturn the document's principal result.
7. Confirm no rejected claim of §16 has been reintroduced.

**Disposition of this record:**

> **ASTRO-THEORY-0001 CANDIDATE HARDENED WITH OPEN NON-BLOCKING QUESTIONS**

with the qualification that **OB-1 is blocking for any consistency claim beyond the named fragment**, and that the defect basis is unconfirmed per §0.
