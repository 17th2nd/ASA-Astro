# ASTRO-THEORY-0001 — Contextual Difference Theory

## Theory Candidate

| Field | Value |
|---|---|
| Status | **Theory Candidate.** Not frozen. Not Version 1. |
| Verification | **Not externally verified.** |
| Empirical status | **Not empirically validated.** |
| Novelty | **No novelty is claimed.** See §18. |
| Coverage | **Not a complete theory of every use of the word "significance."** |
| Supersedes | Nothing. The prior edition of this document is preserved in repository history and was not silently overwritten. |

**Provenance limitation (read before use).** This edition was hardened against formal verification findings V1–V20 as transmitted to the author in prose. **The underlying Codex mathematical verification report was not located in the repository and has not been read by the author.** Findings V2, V7, V8, V11, V12, and part of V17 cite constructs — a minimality claim, aggregation operators, bearer composition $b \circ a$, transformation composition $T_{b \circ a}$, and symbols $q$ and $K$ — that do not occur anywhere in the source candidate. This is evidence that the verification report was written against a different artefact. Those findings are dispositioned as not applicable, with reasons, in `ASTRO-THEORY-0001-FORMAL-DEFECT-RESOLUTION.md`. **Until the report is located and the correspondence confirmed, no claim that V1–V20 are discharged is warranted.**

---

## 1. Purpose

This document states a candidate mathematical theory of contextual difference: what it is for a bearer to make a difference relative to a declared question, and what can and cannot be proved about such valuations.

**Observation 1.1.** A theory of this kind earns its place by ruling things out. The principal content is negative: §10, §15 and §18 are load-bearing.

**Observation 1.2.** §10 establishes that the unrestricted framework has no empirical content whatever. Any reader seeking predictive claims should begin there.

---

## 2. Scope

**In scope.** A formal signature; axioms; the theory of counterfactual operations, contexts, differences, significance, composition and representation invariance; theorems with proofs; limitations; open obligations.

**Out of scope.** Implementation; any application domain; experimental design; governance. No statement below depends on these, and none licenses them.

**Observation 2.1.** The theory is silent on how a context is chosen. It states only what a context must supply for a valuation to be well formed. Choice of context is prior to the theory and is not a mathematical act. §10 shows this is not a minor omission.

**Observation 2.2.** Every component below is marked **primitive**, **derived**, **optional enrichment**, **partial**, or **context-indexed**. No theorem may use a component not licensed by its hypotheses.

---

## 3. Formal signature

### 3.1 Carriers

**Definition 3.1 (Bearers) — primitive.** $\mathfrak{B}$ is a set. Its elements $b$ are *bearers*: the things whose difference-making is valued. $\mathfrak{B}$ is **not** a subset of any state space and no state-space map is applied to it.

**Definition 3.2 (Model space) — primitive.** $(\mathfrak{M}, \mathcal{F})$ is a measurable space. Elements $m$ are *models*.

**Definition 3.3 (Knowledge state) — primitive, context-indexed.** A knowledge state is a probability measure on $(\mathfrak{M},\mathcal{F})$.

**Definition 3.4 (Contexts) — primitive.** $\mathcal{C}$ is a set whose elements are contexts, each a tuple specified in Definition 3.14.

**Definition 3.5 (Outcome space) — primitive, context-indexed.** For each $C$, $(\mathcal{Y}_C, \mathcal{G}_C)$ is a measurable space.

**Definition 3.6 (Representation map) — primitive, optional enrichment.** A measurable $r : \mathfrak{M} \to \mathcal{R}$ into a measurable space $\mathcal{R}$.

### 3.2 Operations and the bearer map

**Definition 3.7 (Operation) — derived.** An *operation* is a measurable map $\tau : \mathfrak{M} \to \mathfrak{M}$. $\mathrm{Op}(\mathfrak{M})$ denotes the set of operations. The *factual operation* is $\mathrm{id}_{\mathfrak{M}}$.

**Definition 3.8 (Operation assignment) — primitive, context-indexed, partial.** For each $C$ a partial map
$$T_C : \mathfrak{B} \rightharpoonup \mathrm{Op}(\mathfrak{M}).$$
This is the only link between bearers and models. Where $T_C(b)$ is undefined, $b$ is *not valuable under $C$*.

**Observation 3.9.** Definition 3.8 discharges the requirement that bearers and states be kept separate. Nothing below applies a map with domain $\mathfrak{M}$ to an element of $\mathfrak{B}$.

**Observation 3.10 (No bearer composition).** The theory declares **no** composition operation on $\mathfrak{B}$. Notation of the form $b \circ a$ is not defined and is not used. Any statement about a composite bearer would require the additional hypothesis $T_C(b \circ a) = T_C(b) \circ T_C(a)$, which the theory neither supplies nor assumes. Composition is defined only on operations (Definition 3.7, composition of measurable maps) and on relation instances (§11).

**Definition 3.11 (Model operation) — derived.** An operation is *model-term* when it acts on the specification of a model only. The theory admits no other kind, and no theorem licenses reading $\tau$ as acting on anything but a model.

### 3.3 Codomains

**Definition 3.12 (Codomain classes) — primitive, context-indexed.** A context declares its valuation codomain in exactly one of the following classes.

| Class | Structure | Admits |
|---|---|---|
| $\mathsf{W}_0$ *qualitative* | pointed preorder $(W, \preceq, 0_W)$ | order comparison only |
| $\mathsf{W}_1$ *magnitude* | ordered commutative monoid $(W, \oplus, 0_W, \le)$ with $0_W$ least | order, addition, triangle inequalities |
| $\mathsf{W}_2$ *signed* | ordered abelian group $(W, +, 0_W, \le)$; $0_W$ **not** least | order, addition, subtraction, sign |
| $\mathsf{W}_3$ *interval* | order-intervals of a $\mathsf{W}_0$, $\mathsf{W}_1$ or $\mathsf{W}_2$ carrier | set inclusion |
| $\mathsf{W}_4$ *distributional* | probability measures on a measurable $\mathsf{W}_1$ or $\mathsf{W}_2$ carrier | integration where declared |

**Observation 3.13.** No theorem may use $\oplus$ or $+$ in a $\mathsf{W}_0$ codomain, and no theorem may assume $0_W$ is least in a $\mathsf{W}_2$ codomain. Every theorem below names its required class.

### 3.4 Contexts

**Definition 3.14 (Context) — primitive.** A context is a tuple
$$C \;=\; \big(\mathfrak{A}_C,\; \mathcal{Y}_C,\; M_C,\; T_C,\; \approx_C,\; \delta_C,\; W_C,\; \rho_C\big)$$
with components:

| Component | Type | Mark |
|---|---|---|
| $\mathfrak{A}_C$ | admissibility restriction determining a knowledge state $\mu_C$ | primitive |
| $\mathcal{Y}_C$ | outcome space (Definition 3.5) | context-indexed |
| $M_C : \mathfrak{M} \to \mathcal{Y}_C$ | measurable outcome map | primitive |
| $T_C : \mathfrak{B} \rightharpoonup \mathrm{Op}(\mathfrak{M})$ | operation assignment (Definition 3.8) | partial |
| $\approx_C$ | equivalence on $\mathcal{Y}_C$ (*contextual indistinguishability*) | optional enrichment |
| $\delta_C : \mathcal{Y}_C \times \mathcal{Y}_C \rightharpoonup W_C$ | contrast evaluator, measurable where defined | partial |
| $W_C$ | codomain in a declared class of Definition 3.12 | context-indexed |
| $\rho_C$ | reduction (Definition 3.16) | primitive |

**Definition 3.15 (Level of the evaluator).** $\delta_C$ is defined **on raw outcomes, subject to congruence when $\approx_C$ is declared** (Axiom A8). It is not defined on quotient classes. The three levels — raw, quotient, raw-subject-to-congruence — are never mixed, and the theory adopts the third throughout.

**Definition 3.16 (Reduction) — primitive, partial.** A reduction is a partial map
$$\rho_C : \mathcal{P}_C \rightharpoonup W_C \;\cup\; \mathcal{I}(W_C) \;\cup\; \{\bot_{\mathrm{ind}}, \bot_{\mathrm{inc}}, \bot_{\mathrm{und}}\}$$
whose domain $\mathcal{P}_C$ is the declared *profile class*, exactly one of:

| Profile class | Domain | Multiplicity |
|---|---|---|
| set-valued | finite subsets of $W_C$ | discarded |
| multiset-valued | finite multisets over $W_C$ | preserved |
| measure-valued | finite measures on $W_C$ | preserved as mass |
| probability-coupled | probability measures on $W_C$ | preserved as probability |

**Observation 3.17.** A context whose valuation depends on multiplicity or probability weight and which declares the set-valued profile class is ill-formed. The profile class must be declared; it is not inferred.

**Definition 3.18 (Indeterminacy symbols).** $\bot_{\mathrm{ind}}$ denotes *indeterminate* (the value is not determined by the available information); $\bot_{\mathrm{inc}}$ denotes *inconsistent* (no model is compatible with the evidence); $\bot_{\mathrm{und}}$ denotes *undefined* (a required component or comparison is absent). These are pairwise distinct and none is a member of $W_C$.

### 3.5 Decision and information structure

**Definition 3.19 (Decision problem) — optional enrichment, context-indexed.** A pair $D_C = (\mathcal{A}_C, L_C)$ with action set $\mathcal{A}_C \neq \emptyset$ and loss $L_C : \mathcal{A}_C \times \mathfrak{M} \to \mathbb{R}$ such that $L_C(\alpha, \cdot)$ is measurable and $\mu_C$-integrable for every $\alpha$.

**Definition 3.20 (Evidence kernel) — optional enrichment.** For a bearer $b$, a Markov kernel $K_b$ from $\mathfrak{M}$ to a measurable space $\mathcal{E}_b$, together with the induced posterior family.

### 3.6 Representation morphisms

**Definition 3.21 (Representation morphism) — derived.** A *representation morphism* is a family
$$\iota \;=\; \big(\iota_{\mathfrak{B}},\; \iota_{\mathfrak{M}},\; \iota_{\mathcal{Y}},\; \iota_{W}\big)$$
of bijections $\iota_{\mathfrak{B}} : \mathfrak{B} \to \mathfrak{B}'$, bimeasurable $\iota_{\mathfrak{M}} : \mathfrak{M} \to \mathfrak{M}'$, bimeasurable $\iota_{\mathcal{Y}} : \mathcal{Y}_C \to \mathcal{Y}'$, and an isomorphism $\iota_W : W_C \to W'$ in the declared codomain class.

**Definition 3.22 (Transported context) — derived.** For a representation morphism $\iota$ and context $C$, the *transported context* $\iota_* C$ has components
$$\mu_{\iota_*C} = (\iota_{\mathfrak{M}})_*\mu_C, \quad M_{\iota_*C} = \iota_{\mathcal{Y}} \circ M_C \circ \iota_{\mathfrak{M}}^{-1}, \quad T_{\iota_*C}(\iota_{\mathfrak{B}} b) = \iota_{\mathfrak{M}} \circ T_C(b) \circ \iota_{\mathfrak{M}}^{-1},$$
$$y \approx_{\iota_*C} y' \iff \iota_{\mathcal{Y}}^{-1}y \approx_C \iota_{\mathcal{Y}}^{-1}y', \quad \delta_{\iota_*C} = \iota_W \circ \delta_C \circ (\iota_{\mathcal{Y}}^{-1} \times \iota_{\mathcal{Y}}^{-1}), \quad \rho_{\iota_*C} = \iota_W \circ \rho_C \circ (\iota_W^{-1})_*.$$

**Observation 3.23 (Covariance is not invariance).** Axiom A3 asserts *covariance* of significance under transport of the whole tuple. It does **not** assert invariance under arbitrary reparametrisation of any single component. A change of $\mathcal{Y}_C$ that is not accompanied by the corresponding change of $\delta_C$ and $W_C$ is not a representation morphism and the theory says nothing about it. The transformations that preserve theory values are exactly the representation morphisms of Definition 3.21 acting as in Definition 3.22, and no others.

---

## 4. Axioms

**A1 (Contrast).** Every significance value is a valuation of a comparison between an outcome under the factual operation and an outcome under a declared operation. No significance value is a property of a bearer alone.

**A2 (Contextual completeness).** A valuation for which any component of Definition 3.14 is unsupplied is $\bot_{\mathrm{und}}$, not defaulted.

**A3 (Covariance under representation morphisms).** For every representation morphism $\iota$, every context $C$, and every bearer $b$ with $T_C(b)$ defined,
$$\sigma_{\iota_* C}(\iota_{\mathfrak{B}} b) \;=\; \iota_W\big(\sigma_C(b)\big).$$

**A4 (Contextual nullity).** For every $b \in \mathfrak{B}$ there exists $C \in \mathcal{C}$ with $W_C$ in class $\mathsf{W}_1$ and $\sigma_C(b) = 0_{W_C}$.

**A5 (Non-fabrication).** If the contrast is not determined by the available information, the value is the determined set, an interval containing it, or the appropriate symbol of Definition 3.18. It is never a point selected from an undetermined set.

**A6 (Joint uncertainty).** Uncertainty is carried by a single joint knowledge state. Marginal and conditional quantities are derived, never primitive.

**A7 (Dimensional coherence).** All values arising under $C$ lie in $W_C$. Values arising under distinct contexts are not combined, and are compared only via an explicitly declared transport (Definition 8.10).

**A8 (Congruence, conditional).** If $\approx_C$ is declared, then for all $y, \tilde y, y', \tilde y' \in \mathcal{Y}_C$ on which $\delta_C$ is defined,
$$y \approx_C \tilde y \;\text{ and }\; y' \approx_C \tilde y' \;\;\Longrightarrow\;\; \delta_C(y,y') = \delta_C(\tilde y, \tilde y').$$

**A9 (Non-vacuity).** A valuation quantified over an empty comparison set is $\bot_{\mathrm{und}}$. Vacuous quantification never yields a substantive element of $W_C$.

**A10 (Consistency precondition).** Identifiability notions (§7) are defined only when the model class compatible with the evidence is nonempty. An empty compatible class yields $\bot_{\mathrm{inc}}$.

**Observation 4.1.** A1 and A4 exclude intrinsic importance. A3 excludes representational artefacts. A8, A9 and A10 exclude the three ways a valuation can appear defined while resting on nothing.

---

## 5. Counterfactual theory

**Definition 5.1 (Pointwise contrast) — derived, partial.** For a context $C$ and a bearer $b$ with $\tau := T_C(b)$ defined,
$$\delta^{\,b}_C : \mathfrak{M} \rightharpoonup W_C, \qquad \delta^{\,b}_C(m) \;=\; \delta_C\big(M_C(m),\, M_C(\tau m)\big),$$
defined at $m$ exactly when $\delta_C$ is defined at the displayed pair.

**Definition 5.2 (Contrast profile) — derived.** Where $\delta^{\,b}_C$ is defined $\mu_C$-almost everywhere and measurable, the *contrast profile* is the element of the declared profile class $\mathcal{P}_C$ induced by $\mu_C$: for the probability-coupled class, the pushforward $(\delta^{\,b}_C)_*\mu_C$.

**Definition 5.3 (Significance) — derived, partial, context-indexed.**
$$\sigma_C(b) \;=\; \rho_C\big(\text{contrast profile of } b \text{ under } C\big),$$
and $\sigma_C(b) = \bot_{\mathrm{und}}$ whenever $T_C(b)$ is undefined, $\delta^{\,b}_C$ is nowhere defined, or the profile lies outside $\mathrm{dom}\,\rho_C$.

**Observation 5.4.** The contrast is a property of the pair $(M_C, \tau)$, not of $\tau$ alone. An operation with large effect on the model and none on the outcome map has null contrast.

**Theorem 1 (Order reversal).**
*Hypotheses.* $\mathfrak{B} = \{b_1,b_2\}$; $\mathfrak{M} = \mathbb{R}^2$ with the Borel $\sigma$-algebra; $\mu = \delta_{(0,0)}$; codomain class $\mathsf{W}_1$ with $W = (\mathbb{R}_{\ge 0}, +, 0, \le)$; probability-coupled profile class; $\rho$ evaluation at a Dirac profile.
*Conclusion.* There exist contexts $C_1, C_2$ differing only in $M_C$ with
$$\sigma_{C_1}(b_1) > \sigma_{C_1}(b_2) \quad\text{and}\quad \sigma_{C_2}(b_1) < \sigma_{C_2}(b_2).$$
*Applies to.* Deterministic form.

*Proof.* Set $T(b_1) = \tau_1$ with $\tau_1(x,y) = (x+2,\,y+1)$ and $T(b_2) = \tau_2$ with $\tau_2(x,y) = (x+1,\,y+2)$; both are measurable. Let $\mathcal{Y} = \mathbb{R}$, $\delta(u,v) = |u-v| \in \mathbb{R}_{\ge0}$, which is measurable and total. Let $M_{C_1}(x,y) = x$ and $M_{C_2}(x,y) = y$. Under $\mu = \delta_{(0,0)}$ each contrast profile is a Dirac measure, so $\rho$ returns its atom. Then $\sigma_{C_1}(b_1) = 2 > 1 = \sigma_{C_1}(b_2)$ and $\sigma_{C_2}(b_1) = 1 < 2 = \sigma_{C_2}(b_2)$. $\blacksquare$

**Corollary 1.1.** No function on $\mathfrak{B}$ alone induces the significance orderings of all contexts.

**Corollary 1.2 (A4 is satisfiable).** Taking $\tau(x,y) = (x,\,y+1)$ with $M_{C_1}(x,y)=x$ gives $\sigma_{C_1}(b)=0$. Hence A4 is not vacuous.

---

## 6. Context theory

**Definition 6.1 (Automorphism).** $\mathrm{Aut}(C)$ is the group of representation morphisms $\pi$ with $\pi_* C = C$ componentwise.

**Definition 6.2 (Designation).** A context *designates* if some component of Definition 3.14 depends on data not fixed by every automorphism of the underlying structure.

**Definition 6.3 (Filter context).** A context all of whose components are fixed by every automorphism of the underlying structure.

**Theorem 2 (Designation necessity).**
*Hypotheses.* A3; a representation morphism $\pi$ with $\pi_* C = C$ and $\iota_W = \mathrm{id}_{W_C}$; a bearer $b$ with $T_C(b)$ defined.
*Conclusion.* $\sigma_C(\pi_{\mathfrak{B}} b) = \sigma_C(b)$.
*Applies to.* All forms.

*Proof.* By A3, $\sigma_{\pi_*C}(\pi_{\mathfrak{B}}b) = \iota_W(\sigma_C(b)) = \sigma_C(b)$. Since $\pi_*C = C$ the left side is $\sigma_C(\pi_{\mathfrak{B}}b)$. $\blacksquare$

**Corollary 2.1 (Filters cannot break symmetry).** A filter context assigns equal significance to bearers in one automorphism orbit.

**Corollary 2.2.** If a question's correct answer distinguishes two bearers in one orbit, any context answering it designates. Designation is necessary, not convenient.

**Observation 6.4.** Theorem 2 gives a necessary condition only. A designating context may still fail to separate two bearers for reasons unrelated to symmetry.

---

## 7. Difference theory

**Definition 7.1 (Observational equivalence).** $m \sim_r m' \iff r(m) = r(m')$. The classes are the *fibres* of $r$.

**Definition 7.2 (Compatible model class).** For an observation $x \in \mathcal{R}$, $\mathfrak{M}_x := r^{-1}(x)$.

**Theorem 3 (Factorisation).**
*Hypotheses.* $r : \mathfrak{M} \to \mathcal{R}$ measurable; $g : \mathfrak{M} \to W$ measurable, with $W$ in any class of Definition 3.12; $\mathcal{R}$ carries the $\sigma$-algebra induced by $r$.
*Conclusion.* $g = h \circ r$ for some measurable $h$ **iff** $g$ is constant on the fibres of $r$.
*Applies to.* All forms.

*Proof.* ($\Rightarrow$) If $g = h\circ r$ and $r(m)=r(m')$ then $g(m)=g(m')$.
($\Leftarrow$) If $g$ is constant on fibres, define $h$ on $r(\mathfrak{M})$ by $h(x) := g(m)$ for any $m \in r^{-1}(x)$; well defined by hypothesis. For measurable $B \subseteq W$, $h^{-1}(B) = r\big(g^{-1}(B)\big)$ is measurable in the $\sigma$-algebra induced by $r$, since $g^{-1}(B)$ is a union of fibres. $\blacksquare$

**Observation 7.3 (Scope of Theorem 3 — exhaustive).** Theorem 3 is a statement about one measurable function and one measurable map, at a fixed context, on realised model pairs, under contrast extensionality. It establishes **none** of the following, and no corollary below extends it to any of them:

- no factorisation through $\approx_C$ or any quotient other than the fibres of $r$;
- no uniqueness of $h$ except modulo equality on $r(\mathfrak{M})$;
- no minimality of $r$ in any sense (see Definition 7.7);
- no identifiability of any quantity not equal to $g$;
- no empirical prediction;
- no representation invariance beyond the explicit morphisms of Definition 3.21;
- no statement about probabilistic, decision, information, or path-composition forms except by separate hypothesis.

**Corollary 3.3 (Induced outcome map — the exact condition).** Let $\tau = T_C(b)$. There exists a map $\phi : \mathcal{Y}_C \to \mathcal{Y}_C$ with $M_C \circ \tau = \phi \circ M_C$ **iff** $M_C \circ \tau$ is constant on the fibres of $M_C$; $\phi$ is then measurable with respect to the $\sigma$-algebra induced by $M_C$, and is unique on $M_C(\mathfrak{M})$.

*Proof.* Theorem 3 with $r := M_C$ and $g := M_C \circ \tau$. $\blacksquare$

**Observation 3.4 (No deterministic induced map in general).** An operation on model space does **not** in general induce a deterministic map on outcome space. Where the condition of Corollary 3.3 fails, the theory offers three admissible representations, of which exactly one must be declared:

| Representation | Object | Requires |
|---|---|---|
| deterministic | $\phi : \mathcal{Y}_C \to \mathcal{Y}_C$ | the fibre-constancy condition of Corollary 3.3 |
| relational | $\Phi \subseteq \mathcal{Y}_C \times \mathcal{Y}_C$, $\Phi = \{(M_C(m), M_C(\tau m))\}$ | nothing beyond measurability |
| kernel | Markov kernel $\mathcal{K}$ from $\mathcal{Y}_C$ to $\mathcal{Y}_C$ | a disintegration of $\mu_C$ along $M_C$ |

The theory asserts no deterministic induced map absent the stated condition, and §5 never requires one: Definition 5.1 composes on $\mathfrak{M}$, where $\tau$ is defined, and not on $\mathcal{Y}_C$.

**Definition 7.4 (Sufficiency).** $r$ is *$C$-sufficient for $b$* if $\delta^{\,b}_C$ is defined everywhere and constant on the fibres of $r$.

**Corollary 3.1 (Computability).** Under A10 and Definition 7.4, the contrast is computable from the representation iff $r$ is $C$-sufficient for $b$.

*Proof.* Theorem 3 with $g = \delta^{\,b}_C$. $\blacksquare$

**Definition 7.5 (Identified set) — partial.** For $x \in \mathcal{R}$ with $\mathfrak{M}_x \neq \emptyset$,
$$\mathcal{S}_C(b,x) \;=\; \big\{\, \delta^{\,b}_C(m) \;:\; m \in \mathfrak{M}_x,\ \delta^{\,b}_C \text{ defined at } m \,\big\}.$$
If $\mathfrak{M}_x = \emptyset$ the value is $\bot_{\mathrm{inc}}$ by A10. If $\mathfrak{M}_x \neq \emptyset$ but $\delta^{\,b}_C$ is defined nowhere on it, the value is $\bot_{\mathrm{und}}$ by A9.

**Corollary 3.2 (Forced abstention).** If $r$ is not $C$-sufficient for $b$ then for some $x$ with $\mathfrak{M}_x \neq \emptyset$, $\mathcal{S}_C(b,x)$ has at least two elements, and no representation-measurable function equals $\delta^{\,b}_C$. By A5 the admissible output is $\mathcal{S}_C(b,x)$, an interval containing it, or $\bot_{\mathrm{ind}}$.

*Proof.* Non-sufficiency gives a fibre on which $\delta^{\,b}_C$ is non-constant; Theorem 3 denies factorisation; A5 forbids a point. $\blacksquare$

**Observation 7.6.** Abstention is a consequence of the axioms, not a policy choice. Conversely, whether $\bot$ is *available* is a property of the context: a context whose reduction has codomain $W_C$ only cannot abstain, and under such a context a non-sufficient representation yields an ill-formed request rather than a refusal.

**Definition 7.7 (Four distinct notions, none of which is minimality of $r$).**
(i) $r$ is *sufficient for $(C,b)$* — Definition 7.4.
(ii) $r$ is *minimal sufficient relative to $\delta^{\,b}_C$* if it is sufficient and factors through every sufficient map.
(iii) The *distinguishability bit* of a pair $m,m'$ is $\mathbb{1}[\delta^{\,b}_C(m) \neq \delta^{\,b}_C(m')]$.
(iv) The *kernel quotient* of $\delta^{\,b}_C$ is $\mathfrak{M}/\!\ker \delta^{\,b}_C$.

**Observation 7.8 (No minimality is claimed).** The theory asserts (i) where hypothesised and asserts nothing about (ii). Sufficiency is not minimality, and no construction below is claimed universal, initial, terminal, or minimal in any category.

**Theorem 4 (Quotient descent).**
*Hypotheses.* $\approx_C$ declared; A8.
*Conclusion.* There is a unique $\bar\delta_C$ on $(\mathcal{Y}_C/\!\approx_C)^2$ with $\bar\delta_C([y],[y']) = \delta_C(y,y')$ wherever $\delta_C$ is defined. Without A8 no such map exists in general.
*Applies to.* All forms with $\approx_C$ declared.

*Proof.* Existence and well-definedness are exactly A8. Uniqueness: any two such maps agree on all classes with a defined representative pair. For the negative clause, take $\mathcal{Y}=\{y,\tilde y\}$ with $y \approx \tilde y$, $W = \mathbb{R}$, $\delta(y,y)=0$, $\delta(\tilde y, y)=1$; then $[\,y\,]=[\,\tilde y\,]$ but the two defining expressions differ, so no map on classes exists. $\blacksquare$

**Observation 7.9.** Theorem 4 is the reason Definition 3.15 fixes the evaluator at the raw level subject to congruence. Quotient-level sufficiency is claimed only where A8 is assumed, and nowhere else.

---

## 8. Significance theory

### 8.1 Standing assumptions for §8

**Assumption 8.0 (Measurability and integrability).** Throughout §8: $M_C$ is measurable; every $\tau = T_C(b)$ is measurable; $\delta_C$ is measurable on its domain; $W_C$ carries a $\sigma$-algebra making $\delta^{\,b}_C$ measurable; every expectation written below is assumed to exist and be finite; every kernel invoked is a Markov kernel; and $\mathfrak{M}_x \neq \emptyset$ where identifiability is discussed (A10). Statements in §8 are asserted only under Assumption 8.0.

**Observation 8.0.1.** No integral is taken into a codomain of class $\mathsf{W}_0$. Where an expectation appears, the codomain is $\mathsf{W}_1$ or $\mathsf{W}_2$ realised in $\mathbb{R}$, for which the Lebesgue integral is available. The theory supplies no integration theory for a general preorder and asserts none.

### 8.2 The three forms

**Definition 8.1 (Effect significance) — requires $\mathsf{W}_1$.** Let $(\mathcal{Y}_C, d_Y)$ be a metric space, $W_C = (\mathbb{R}_{\ge0}, +, 0, \le)$, $\delta_C = d_Y$, and $\rho_C$ a location functional on the declared profile class. Then
$$\sigma^{\mathrm{eff}}_C(b) \;=\; \rho_C\Big(\big(m \mapsto d_Y(M_C(m), M_C(\tau m))\big)_*\mu_C\Big), \qquad \tau = T_C(b).$$

**Definition 8.2 (Decision significance) — requires $\mathsf{W}_2$ realised in $\mathbb{R}$, and Definition 3.19.** Let $\mathfrak{r}(\nu) := \inf_{\alpha \in \mathcal{A}_C} \mathbb{E}_\nu L_C(\alpha,\cdot)$, assumed finite. For $\varepsilon \ge 0$ let $\mathcal{A}^*_\varepsilon(\nu) := \{\alpha : \mathbb{E}_\nu L_C(\alpha,\cdot) \le \mathfrak{r}(\nu) + \varepsilon\}$, which is nonempty for every $\varepsilon > 0$ by definition of the infimum. For a declared $\varepsilon > 0$,
$$\sigma^{\mathrm{dec}}_C(b) \;=\; \inf\Big\{\, \mathbb{E}_{\mu_C} L_C(\alpha,\cdot) \;:\; \alpha \in \mathcal{A}^*_\varepsilon\big(\mu_C^{\,\tau}\big) \Big\} \;-\; \mathfrak{r}(\mu_C),$$
where $\mu_C^{\,\tau} := \tau_*\mu_C$. For $\varepsilon = 0$ the definition additionally requires that the infimum defining $\mathfrak{r}(\mu_C^{\,\tau})$ be attained; absent attainment the value is $\bot_{\mathrm{und}}$.

**Observation 8.3.** Definition 8.2 uses no $\arg\min$. Existence of an optimiser is not assumed; $\varepsilon$-optimality is used instead, and the attainment hypothesis is stated explicitly where $\varepsilon = 0$.

**Definition 8.4 (Information significance) — requires $\mathsf{W}_2$ realised in $\mathbb{R}$, Definitions 3.19 and 3.20.**
$$\sigma^{\mathrm{inf}}_C(b) \;=\; \mathfrak{r}(\mu_C) \;-\; \mathbb{E}\big[\mathfrak{r}(\mu_C^{\,K_b})\big],$$
where $\mu_C^{\,K_b}$ is the posterior induced by the kernel $K_b$ and the outer expectation is over the marginal law of the evidence, assumed to exist.

**Theorem 5 (Non-negativity).**
*Hypotheses.* Assumption 8.0; for (i) the codomain class $\mathsf{W}_1$ and $\rho_C$ a location functional preserving the support bound; for (ii) $\varepsilon > 0$ or attainment; for (iii) integrability of $\mathfrak{r}(\mu_C^{K_b})$.
*Conclusion.* (i) $\sigma^{\mathrm{eff}}_C \ge 0$; (ii) $\sigma^{\mathrm{dec}}_C \ge -\,0$, indeed $\sigma^{\mathrm{dec}}_C \ge 0$; (iii) $\sigma^{\mathrm{inf}}_C \ge 0$.
*Applies to.* Deterministic, decision and information forms respectively.

*Proof.* (i) $d_Y \ge 0$, so the profile is supported in $\mathbb{R}_{\ge0}$ and a location functional of such a profile is $\ge 0$.
(ii) For every $\alpha \in \mathcal{A}_C$, $\mathbb{E}_{\mu_C} L_C(\alpha,\cdot) \ge \inf_{\alpha'} \mathbb{E}_{\mu_C} L_C(\alpha',\cdot) = \mathfrak{r}(\mu_C)$. Taking the infimum over $\alpha \in \mathcal{A}^*_\varepsilon(\mu_C^\tau)$, a subset of $\mathcal{A}_C$, preserves the bound. Hence the difference is $\ge 0$. Note this holds for **any** selection rule, attained or not.
(iii) $\nu \mapsto \mathbb{E}_\nu L_C(\alpha,\cdot)$ is affine in $\nu$; an infimum of affine functionals is concave, so $\mathfrak{r}$ is concave. By the tower property $\mathbb{E}[\mu_C^{K_b}] = \mu_C$. By Jensen's inequality for concave functionals, $\mathbb{E}[\mathfrak{r}(\mu_C^{K_b})] \le \mathfrak{r}(\mu_C)$. $\blacksquare$

**Theorem 6 (Pairwise non-equivalence).**
*Hypotheses.* Assumption 8.0; the constructions below.
*Conclusion.* The three forms are pairwise non-equivalent: for each pair there are a context and two bearers on which the orderings disagree.
*Applies to.* Deterministic, decision and information forms jointly.

*Proof.* Three constructions.

(i) *Effect against decision.* $\mathfrak{M} = \mathbb{R}^2$ Borel, $\mu = \delta_{(0,0)}$, $M = \mathrm{id}$, $d_Y$ Euclidean, $\mathcal{A} = \mathbb{R}$, $L(\alpha,(x,y)) = (\alpha-x)^2$, which is measurable, integrable, and attains its infimum at $\alpha = \mathbb{E}[x]$. Let $T(b_1)(x,y) = (x, y+10)$ and $T(b_2)(x,y) = (x+1, y)$.
Effect: $\sigma^{\mathrm{eff}}(b_1) = 10 > 1 = \sigma^{\mathrm{eff}}(b_2)$.
Decision: $T(b_1)$ leaves the $x$-marginal fixed, so $\mathfrak{r}(\mu^{\tau_1})$ is attained at the same action as $\mathfrak{r}(\mu)$ and $\sigma^{\mathrm{dec}}(b_1)=0$. For $b_2$ the optimiser moves from $0$ to $1$, giving $\sigma^{\mathrm{dec}}(b_2) = \mathbb{E}_\mu(1-x)^2 - \mathbb{E}_\mu(0-x)^2 = 1 > 0$.
Orderings disagree.

(ii) *Decision against information.* $\mathfrak{M} = \mathbb{R}^2$ with coordinates $(\theta_1,\theta_2)$ independent under $\mu$, $L(\alpha,\theta) = (\alpha - \theta_1 - \theta_2)^2$, so $\mathfrak{r}(\nu) = \mathrm{Var}_\nu[\theta_1+\theta_2]$, attained. Let $\theta_1$ be degenerate at $0$ and $\theta_2 \sim \mathcal{N}(0,s^2)$, $s^2>0$.
For $b_1$: $K_{b_1}$ trivial by degeneracy, so $\sigma^{\mathrm{inf}}(b_1)=0$; $T(b_1)$ shifts $\theta_1$ by $1$, moving the optimiser, so $\sigma^{\mathrm{dec}}(b_1)=1>0$.
For $b_2$: let $T(b_2)$ replace $\theta_2$ by its mean, preserving $\mathbb{E}[\theta_1+\theta_2]$, so the optimiser is unchanged and $\sigma^{\mathrm{dec}}(b_2)=0$; let $K_{b_2}$ reveal $\theta_2$ exactly, giving $\sigma^{\mathrm{inf}}(b_2)=s^2>0$.
Orderings disagree.

(iii) *Effect against information.* Retain (ii) with $M=\mathrm{id}$ and $d_Y$ Euclidean. Then $\sigma^{\mathrm{eff}}(b_1)=1$ and $\sigma^{\mathrm{inf}}(b_1)=0$, while for $s$ small $\sigma^{\mathrm{eff}}(b_2) < 1$ and $\sigma^{\mathrm{inf}}(b_2)=s^2>0$. Orderings disagree. $\blacksquare$

**Corollary 6.1.** The three are not measurements of one latent quantity: monotone maps preserve order, and the orders disagree.

**Corollary 6.2.** A scalar presented as "significance" without naming which form it is, is underdetermined.

### 8.3 Context-free scalars

**Theorem 7 (Triviality of additive context-free valuation).**
*Hypotheses.* $W_C = (\mathbb{R}_{\ge0},+,0,\le)$ in class $\mathsf{W}_1$ for every $C$ in the family considered; $S : \mathfrak{B} \to \mathbb{R}_{\ge0}$; $\beta > 0$; for every such $C$ a $g_C : \mathfrak{B} \to \mathbb{R}_{\ge0}$ with $\sigma_C(b) = \beta S(b) + g_C(b)$ for all $b$; A4.
*Conclusion.* $S \equiv 0$.
*Applies to.* All forms with a $\mathsf{W}_1$ codomain.

*Proof.* Fix $b$. By A4 choose $C$ with $\sigma_C(b)=0$. Then $\beta S(b) + g_C(b)=0$ with both summands $\ge 0$ and $\beta>0$; a sum of non-negative reals vanishes only if each does, so $S(b)=0$. $\blacksquare$

**Observation 7.1'.** Non-negativity of $g_C$ is essential. Dropping it, set $g'_C := \beta S + g_C$; then $\sigma_C = g'_C$ identically and $S$ is eliminated without changing a value. Hence the additive decomposition is either forced to triviality by Theorem 7 or is absorbable and carries no content. This is why the theory admits no such primitive.

**Theorem 8 (No epistemic gain from derived summaries).**
*Hypotheses.* $Z$ a random element on a common probability space; $R$ a random element; $S = f(R)$ with $f$ measurable; all mutual informations defined.
*Conclusion.* $I(Z;S,R) = I(Z;R)$ and $I(Z;S \mid R) = 0$.
*Applies to.* All forms.

*Proof.* $\sigma(S) \subseteq \sigma(R)$, so $\sigma(S,R) = \sigma(R)$; mutual information depends on the joint law only through the generated $\sigma$-algebras. The chain rule gives the second claim. $\blacksquare$

**Corollary 8.1.** A quantity derived from the representation cannot be justified epistemically. Any justification must be structural, computational, or normative.

### 8.4 Normalisation and cross-context comparison

**Definition 8.5 (Arena normalisation).** For finite $A \subseteq \mathfrak{B}$ and $\varphi : A \to \mathbb{R}_{>0}$, $\nu^A(b) = \varphi(b)/\max_{b'\in A}\varphi(b')$.

**Theorem 9 (Normalisation is arena-dependent).**
*Hypotheses.* $A \subsetneq A'$ finite, $\varphi$ extends to $A'$, $\max_{A'}\varphi > \max_A \varphi$.
*Conclusion.* $\nu^{A'}(b) < \nu^{A}(b)$ for every $b \in A$, while the two induce the same order on $A$.
*Applies to.* All forms.

*Proof.* With $\mathsf{m} = \max_A\varphi < \mathsf{m}' = \max_{A'}\varphi$ and $\varphi(b)>0$, $\varphi(b)/\mathsf{m}' < \varphi(b)/\mathsf{m}$. Both are positive multiples of $\varphi$ on $A$. $\blacksquare$

**Corollary 9.1.** Normalised values are not comparable across arenas and their cross-arena equality carries no information.

**Corollary 9.2.** A normalised value is dimensionless and by A7 cannot be calibrated against a dimensioned quantity.

**Definition 8.10 (Cross-context transport) — optional enrichment.** A *transport* from $C$ to $C'$ is a declared order-embedding $t : W_C \to W_{C'}$. Comparison of $\sigma_C(b)$ with $\sigma_{C'}(b')$ is defined only relative to a declared $t$.

**Observation 8.11.** The theory distinguishes no transport. By A7, absent a declared $t$, cross-context comparison is $\bot_{\mathrm{und}}$, not false and not zero.

---

## 9. Encodability and the limits of the unrestricted framework

This section is the theory's principal epistemic result. It is stated as a theorem because a hedge would understate it.

**Definition 9.1 (Independent instantiation).** A context $C$ is *independently instantiated* relative to an assessment if every component of Definition 3.14 is fixed by a procedure that does not depend on the values $\sigma_C$ subsequently produces.

**Theorem 10 (Universal encodability).**
*Hypotheses.* $\mathfrak{B}$ any set; $W$ any codomain in class $\mathsf{W}_2$; $f : \mathfrak{B} \to W$ any function; $W$ measurable with singletons measurable.
*Conclusion.* There exists a context $C$ with $W_C = W$ and $\sigma_C(b) = f(b)$ for every $b \in \mathfrak{B}$.
*Applies to.* All forms.

*Proof.* Take $\mathfrak{M} := W$ with its $\sigma$-algebra, $\mathcal{Y}_C := W$, $M_C := \mathrm{id}_W$, $\mu_C := \delta_{0_W}$, and $\delta_C(y,y') := y' - y$, available since $W$ is an ordered abelian group. For each $b$ let $T_C(b)$ be the constant map $m \mapsto f(b)$, which is measurable. Declare the probability-coupled profile class and let $\rho_C$ return the atom of a Dirac profile. Then $\delta^{\,b}_C(m) = M_C(T_C(b)m) - M_C(m) = f(b) - 0_W = f(b)$ for $\mu_C$-almost every $m$, so the profile is $\delta_{f(b)}$ and $\sigma_C(b) = f(b)$. $\blacksquare$

**Corollary 10.1 (The unrestricted framework has no empirical content).** The unrestricted framework excludes no assignment of values to bearers. It therefore forbids no observation and is not empirically falsifiable.

*Proof.* Immediate from Theorem 10: any proposed assignment is realised by some context. $\blacksquare$

**Corollary 10.2 (Where content comes from).** Empirical content arises only when $M_C$, $T_C$, $\delta_C$ and $\rho_C$ are constrained by an independently specified model, and when $C$ is independently instantiated in the sense of Definition 9.1. Predictive content is a property of an instantiation, never of the framework.

**Observation 10.3.** Definition 9.1 does not by itself create empirical content. It removes one route by which a valuation can be fitted to its own assessment; it does not supply the external constraint that Corollary 10.2 requires.

**Observation 10.4 (Statement of the consequence, in the required plain form).** The unrestricted theory is **not** empirically falsifiable. Instantiated models **may** be falsifiable. The theory is a representation and valuation framework, not a scientific hypothesis, unless an external scientific model constrains its primitives.

---

## 10. Composition theory

**Definition 10.1 (Relation instance) — primitive, optional enrichment.** A pair $e = (t, \nu)$ with $t$ in a type set $T$ and $\nu$ in a signature set $N$.

**Definition 10.2 (Compatibility) — primitive, partial.** A relation $\kappa \subseteq E \times E$.

**Definition 10.3 (Partial composition) — derived, partial.** A partial map $\odot : E \times E \rightharpoonup E$ with domain $\kappa$.

**Definition 10.4 (Path).** A finite sequence $p=(e_1,\dots,e_k)$ with matching endpoints.

**Definition 10.5 (Composition semantics) — partial.** $[\![p]\!]_{\mathrm{comp}}$ is the result of evaluating $e_1 \odot \cdots \odot e_k$ under a **declared bracketing**, or $\bot_{\mathrm{und}}$ if any required composition is undefined.

**Definition 10.6 (Diffusion semantics) — total.** Given $w : E \to \mathbb{R}_{\ge0}$, $[\![p]\!]_{\mathrm{diff}} = \prod_{i=1}^k w(e_i)$.

**Theorem 11 (Insufficiency of type-level licensing).**
*Hypotheses.* $\kappa$ is not a function of types alone: there exist $e_1,e_2,e_1',e_2'$ with $t(e_1)=t(e_1')$, $t(e_2)=t(e_2')$, $(e_1,e_2)\in\kappa$, $(e_1',e_2')\notin\kappa$.
*Conclusion.* Every predicate depending only on types is unsound or incomplete with respect to $\kappa$.
*Applies to.* Path-composition form.

*Proof.* Such a predicate takes one value on both pairs. If *admit*, it admits $(e_1',e_2')\notin\kappa$ and is unsound; if *refuse*, it refuses $(e_1,e_2)\in\kappa$ and is incomplete. $\blacksquare$

**Theorem 12 (Non-associativity).**
*Hypotheses.* A composition table as constructed.
*Conclusion.* There exist $e_1,e_2,e_3$ with $(e_1\odot e_2)\odot e_3$ undefined and $e_1\odot(e_2\odot e_3)$ defined.
*Applies to.* Path-composition form.

*Proof.* Let $T=\{P,Q,R\}$ with $P\odot Q = R$, $Q\odot Q = Q$, $R\odot Q$ undefined, all other pairs undefined. Take $t(e_1)=P$, $t(e_2)=t(e_3)=Q$. Left: $e_1\odot e_2$ has type $R$ and $R\odot Q$ is undefined. Right: $e_2\odot e_3$ has type $Q$ and $P\odot Q=R$ is defined. $\blacksquare$

**Corollary 12.1.** $(E,\odot)$ is a partial magma, not in general a partial semigroup.

**Corollary 12.2.** A path does not determine its composite; a bracketing must be declared and distinct bracketings are distinct computations.

**Corollary 12.3 (Licensed paths do not form a substructure).** The licensed paths are not the path set of any substructure.

*Proof.* Substructure membership is a condition on instances alone, hence independent of bracketing; Theorem 12 exhibits bracketing-dependent licensure. $\blacksquare$

**Theorem 13 (Semantic separation).**
*Hypotheses.* $\kappa$ an arbitrary relation on distinct instances, as permitted by Definition 10.2.
*Conclusion.* There exist a structure, weight $w$, designation $\Delta$ and bearers $a,b$ with $\sum_{p:a\to\Delta}[\![p]\!]_{\mathrm{diff}} > \sum_{p:b\to\Delta}[\![p]\!]_{\mathrm{diff}}$ while every $a\to\Delta$ path composes to $\bot_{\mathrm{und}}$ and some $b\to\Delta$ path composes.
*Applies to.* Path-composition and diffusion forms.

*Proof.* Elements $\{a,b,c,c',z\}$, $\Delta=\{z\}$, instances $e_1:a\to c$, $e_2:c\to z$, $f_1:b\to c'$, $f_2:c'\to z$, so the only paths are $(e_1,e_2)$ and $(f_1,f_2)$. Set $w(e_i)=1$, $w(f_i)=1/10$, giving sums $1$ and $1/100$. Set $(e_1,e_2)\notin\kappa$ and $(f_1,f_2)\in\kappa$, admissible since the instances are distinct and $\kappa$ is arbitrary. $\blacksquare$

**Observation 13.1.** Theorem 13 does not show diffusion functionals invalid. $[\![\cdot]\!]_{\mathrm{diff}}$ is total on any weighted structure whatever the transitivity of the relations. The theorem shows the two semantics independent, so identifying a diffusion value with a relational claim is an interpretive error, not a mathematical one.

**Observation 13.2.** Accordingly the assertion *"path functionals are invalid when relations are non-transitive"* is **false** and is rejected in §18. The defensible assertion is that traversal semantics must be declared.

### 10.1 Recognisability

**Observation 10.7 (Path language class).** The licensed-path structure is a guarded register automaton over a data path: a finite automaton over relation types together with a guard on registers carrying the previously composed signature, evaluated on the product $U \times Q \times \mathcal{S}$ where $\mathcal{S}$ is the register content set.

- If $\mathcal{S}$ is finite, the product is finite-state and the licensed-path language is regular in the product alphabet; recognisability is decidable and the state count is $|U|\cdot|Q|\cdot|\mathcal{S}|$.
- If $\mathcal{S}$ is unbounded — as it is when the register retains full composed-signature history — the automaton is infinite-state and the licensed-path language **need not be regular**. No claim of finite recognisability is made in that case.

**Observation 10.8 (Consequence).** Arbitrary path-history constraints are therefore **not** claimed finitely recognisable. A theory instance wanting decidable licensure must bound the register content; one retaining full history accepts unbounded state and the associated computational cost.

**Observation 10.9 (Prior art — preserved).** The licensed-path machinery of this section is established guarded/register-automaton and data-path theory. It is **not** novel mathematics, and no part of §10 is offered as a novelty claim. This conclusion is preserved from the prior-art analysis and is not reopened here.

---

## 11. Representation invariance

**Definition 11.1 (Structural valuation).** $\varphi$ is *structural* if $\varphi(\pi_{\mathfrak{B}} b) = \varphi(b)$ for every automorphism $\pi$ (Definition 6.1).

**Theorem 14 (Orbit constancy).**
*Hypotheses.* Definition 11.1.
*Conclusion.* Every structural valuation is constant on automorphism orbits.
*Applies to.* All forms.

*Proof.* The orbit of $b$ is $\{\pi_{\mathfrak{B}}b\}$, on which $\varphi$ takes the value $\varphi(b)$ by definition. $\blacksquare$

**Corollary 14.1.** A valuation distinguishing two bearers in one orbit is not structural and depends on data outside the invariance class.

**Definition 11.2 (Artefact morphism).** A representation morphism whose induced action on every typed component of Definition 3.14 is the identity, and which differs only in the labelling of carriers.

**Corollary 14.2 (Artefact independence).** Under A3, $\sigma$ is unchanged by every artefact morphism.

*Proof.* Immediate from A3 with $\iota_W = \mathrm{id}$ and $\iota_* C = C$. $\blacksquare$

**Observation 11.3 (Demotion recorded).** In the prior edition this appeared as a theorem. It is a one-line consequence of A3 with no content beyond the axiom, and is demoted to a corollary. Theorem status is not retained for appearance.

**Observation 11.4.** Theorem 2 and Theorem 14 are two faces of one fact. Invariance constrains what a valuation may see; designation supplies what invariance does not cover. Neither is dispensable.

---

## 12. Consistency witness

**Proposition 12.1 (Consistency of the deterministic–decision fragment).** The axioms A1–A10, restricted to the fragment comprising Definitions 3.1–3.19 with codomain classes $\mathsf{W}_1$ and $\mathsf{W}_2$, the probability-coupled profile class, and no path structure, are jointly satisfiable.

*Proof.* Exhibit the model $\mathcal{W}$:
$\mathfrak{B}=\{b_1,b_2\}$; $\mathfrak{M}=\mathbb{R}^2$ Borel; $\mathcal{R}=\mathbb{R}^2$ with $r=\mathrm{id}$; $\mathcal{C}=\{C_1,C_2,C_0\}$.
For $C_1$: $\mu=\delta_{(0,0)}$; $\mathcal{Y}=\mathbb{R}$; $M(x,y)=x$; $T(b_1)(x,y)=(x+2,y+1)$, $T(b_2)(x,y)=(x+1,y+2)$; $\approx$ is equality; $\delta(u,v)=|u-v|$; $W=(\mathbb{R}_{\ge0},+,0,\le)$; probability-coupled profile; $\rho$ the atom of a Dirac profile.
$C_2$ as $C_1$ with $M(x,y)=y$.
$C_0$ as $C_1$ with $T(b_i)(x,y)=(x,y+1)$ for both $i$.
Decision structure on $C_1$: $\mathcal{A}=\mathbb{R}$, $L(\alpha,(x,y))=(\alpha-x)^2$, integrable under $\delta_{(0,0)}$, infimum attained.

Verification: **A1** every value is a $\delta$ of a factual and an operated outcome, by construction. **A2** all eight components are supplied for each context. **A3** holds for the identity morphism, and for any bimeasurable relabelling by Definition 3.22, which transports every component. **A4** witnessed by $C_0$, under which both bearers have contrast $|x-x|=0$. **A5** $r=\mathrm{id}$ makes every fibre a singleton, so every contrast is determined and no fabricated point arises. **A6** a single $\mu$ per context. **A7** all values of $C_i$ lie in that context's $W$; no cross-context combination occurs. **A8** $\approx$ is equality, so congruence is trivial. **A9** every comparison set is a singleton, hence nonempty. **A10** every fibre is nonempty. $\blacksquare$

**Observation 12.2 (Scope of the witness — binding).** Proposition 12.1 establishes consistency **only** for the named fragment. It does **not** establish consistency for: non-trivial $\approx_C$ with a non-degenerate congruence requirement; the $\mathsf{W}_0$, $\mathsf{W}_3$ or $\mathsf{W}_4$ codomain classes; the set-, multiset- or measure-valued profile classes; the evidence-kernel structure of Definition 3.20; non-atomic knowledge states; or the path structure of §10. Consistency of the full signature is an **open proof obligation** (§14, OB-1). No consistency claim is made for structures the witness does not instantiate.

---

## 13. Proven statements

| № | Statement | Form | §  |
|---|---|---|---|
| 1 | Significance orderings are strictly reversible across contexts | deterministic | 5 |
| 2 | A context fixed by an automorphism cannot separate bearers it relates | all | 6 |
| 3 | Factorisation through fibres holds iff the function is fibre-constant | all | 7 |
| 4 | A congruent evaluator descends to the quotient; without congruence it need not | all with $\approx_C$ | 7 |
| 5 | The three significance forms are non-negative under stated hypotheses | det./dec./inf. | 8 |
| 6 | The three forms are pairwise non-equivalent | det./dec./inf. | 8 |
| 7 | A non-negative additive context-free scalar is identically zero under nullity | $\mathsf{W}_1$ | 8 |
| 8 | A summary derived from the representation adds no information | all | 8 |
| 9 | Max-normalised values are arena-dependent and dimensionless | all | 8 |
| 10 | **Every assignment of values to bearers is realised by some context** | all | 9 |
| 11 | Type-level licensing is unsound or incomplete | path | 10 |
| 12 | Partial composition is not associative | path | 10 |
| 13 | Diffusion and composition semantics are independent | path/diffusion | 10 |
| 14 | Structural valuations are constant on automorphism orbits | all | 11 |

---

## 14. Proven limitations and open proof obligations

**Limitation 14.1 (No context-free ordering).** By Corollary 1.1 no ordering of $\mathfrak{B}$ is consistent with every context.

**Limitation 14.2 (No context-free scalar contribution).** By Theorem 7 and Observation 7.1'.

**Limitation 14.3 (No epistemic role for derived summaries).** By Theorem 8.

**Limitation 14.4 (The reduction is not determined).** A2 requires $\rho_C$; the theory supplies none. Distinct reductions of one profile induce distinct orderings whenever the profile is asymmetric.

**Limitation 14.5 (Path values are not intrinsic).** By Corollary 12.2.

**Limitation 14.6 (Identification is not guaranteed).** By Corollary 3.2, with $\bot_{\mathrm{inc}}$ reserved for the empty compatible class by A10.

**Limitation 14.7 (No cross-context comparison).** By A7 and Observation 8.11.

**Limitation 14.8 (Designation is exogenous).** Theorem 2 shows designation necessary and says nothing about its source.

**Limitation 14.9 (No empirical content unrestricted).** By Theorem 10 and Corollary 10.1. This is the strongest limitation in the document.

**Limitation 14.10 (Recognisability is conditional).** By Observations 10.7–10.8.

**Open proof obligation OB-1.** Consistency of the full signature, beyond the fragment of Proposition 12.1. See Observation 12.2 for the exact list of uninstantiated structures.

**Open proof obligation OB-2.** Measurability of $\delta^{\,b}_C$ is *assumed* in Assumption 8.0 rather than derived. Conditions on $M_C$, $\tau$ and $\delta_C$ sufficient for it are not established here.

**Open proof obligation OB-3.** Theorem 5(iii) assumes integrability of $\mathfrak{r}(\mu_C^{K_b})$. Conditions guaranteeing it are not established here.

---

## 15. Open mathematical questions

**Open Question 15.1.** Under what conditions does a composition table admit an associative refinement, and is there an obstruction theory for the failure?

**Open Question 15.2.** Characterise $C$-sufficiency structurally: is there a computable criterion for fibre-constancy of $\delta^{\,b}_C$?

**Open Question 15.3.** Is there an axiomatisation of preferences over contrast profiles forcing a unique reduction $\rho_C$? If not, on what class of contexts is $\rho_C$ determined up to monotone equivalence?

**Open Question 15.4.** Do the three forms of §8 arise as fibres of a single indexed structure over a base of question-types, so that Theorem 6 states non-triviality of that fibration?

**Open Question 15.5.** Is contextual admissibility reducible to a threshold on a decision-theoretic loss, or is the admit/reject/indeterminate trichotomy irreducibly three-valued?

**Open Question 15.6 — closed, negatively.** *Is there an invariant of the licensed-path structure not expressible in an existing typed, temporal or dimensionally annotated formalism?* **No.** The structure is a guarded register automaton over a data path — established graph-database theory, with guards instantiated by existing temporal, spatial and dimensional vocabularies. Retained as a closed record. **Observation:** this closure disturbs no theorem of §10; Theorems 11–13 concern the structure, not its novelty.

**Open Question 15.7.** Is there a pseudometric on contexts under which significance is continuous? A negative answer would mean small changes of question can produce discontinuous changes of valuation.

**Open Question 15.8.** For which operation families is $b \mapsto \sigma_C(b)$ determined by single-bearer contrasts, and for which are joint operations required? Does the theory need a coalitional extension?

---

## 16. Explicitly rejected formulations

Each rejection names the result that defeats it.

**16.1.** *Significance is an intrinsic attribute of a bearer.* — Theorem 1, Corollary 1.1.

**16.2.** *Significance decomposes as a context-free scalar plus a context-dependent remainder.* — Theorem 7 with Observation 7.1'.

**16.3.** *A context-free summary supplies information not in the representation.* — Theorem 8.

**16.4.** *Significance is a rank normalised within an arena.* — Theorem 9, Corollaries 9.1–9.2.

**16.5.** *Significance is one quantity, variously measured.* — Theorem 6, Corollary 6.1.

**16.6.** *Significance emerges from structure.* — Rejected as a formulation: it supplies no component of Definition 3.14, so by A2 it yields $\bot_{\mathrm{und}}$.

**16.7.** *A context acts by restricting the admissible structure.* — Theorem 2, Corollary 2.1.

**16.8.** *Composition is licensed at the level of types.* — Theorem 11.

**16.9.** *A path has a value determined by the path.* — Theorem 12, Corollary 12.2.

**16.10.** *Path functionals are invalid when relations are non-transitive.* — Rejected as **false** by Observations 13.1–13.2.

**16.11.** *A point value may be returned when the contrast is set-identified.* — Corollary 3.2 with A5.

**16.12.** *Values under distinct contexts may be compared.* — A7, Observation 8.11.

**16.13.** *Significance may depend on the encoding.* — Corollary 14.2.

**16.14.** *The framework has empirical content of its own.* — Theorem 10, Corollary 10.1.

**16.15.** *Context is discovered from evidence.* — Rejected: $T_C$, $\delta_C$ and $\rho_C$ are primitives of Definition 3.14, supplied not derived. The theory contains no construction producing them from $\mu_C$.

**16.16.** *The framework derives its evaluator automatically.* — Rejected by the same reading of Definition 3.14, and by Theorem 10, under which any evaluator whatever is realisable.

**16.17.** *Standing.* — No context-free ordering primitive exists in the signature. Theorem 7 forbids reintroducing one additively; Theorem 8 denies it an epistemic role.

**16.18.** *Mathematical or graph-theoretic novelty.* — No novelty is claimed anywhere in this document. Observation 10.9 records the licensed-path machinery as established prior art.

**16.19.** *Significance-first intelligence.* — Not a statement of this theory; no definition, axiom or theorem above refers to it.

---

*End of ASTRO-THEORY-0001 — Theory Candidate. Not verified. Not frozen.*
