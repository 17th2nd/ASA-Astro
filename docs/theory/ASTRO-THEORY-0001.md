# ASTRO-THEORY-0001 — Contextual Difference Theory

---

## 1. Purpose

This document states the mathematical theory of contextual difference: the theory of what it is for one element of a modelled situation to matter, relative to a declared question, and of what can and cannot be proved about such valuations.

The theory exists to fix the objects, to fix the axioms, and to establish which formulations are consistent with those axioms and which are not.

**Observation 1.1.** A theory of this kind earns its place only by ruling things out. The principal content below is negative: §12 and §14 are the load-bearing sections.

---

## 2. Scope

**In scope.** Primitive objects; axioms; the theory of counterfactual operations, contexts, differences, significance, composition, and representation invariance; theorems, proofs, corollaries, limitations, and open questions.

**Out of scope.** Implementation; any particular domain; experimental design; questions of governance or record-keeping. No statement below depends on any of these, and no statement below should be read as licensing any of them.

**Observation 2.1.** Theorems 6 and 7 formalise results obtained independently in the Codex A mathematical reconstruction, which is held here in summary rather than in full. Their proofs below are self-contained and do not depend on that source.

**Observation 2.2.** The theory is silent on how a context is chosen. It says only what a context must supply for a valuation to be well defined. Choice of context is prior to the theory and is not a mathematical act.

---

## 3. Primitive mathematical objects

**Definition 3.1 (Model space).** A *model space* is a measurable space $(\mathfrak{M}, \mathcal{F})$. An element $m \in \mathfrak{M}$ is a *model*: a specification complete enough to determine every outcome considered by the theory.

**Definition 3.2 (Knowledge state).** A *knowledge state* is a probability measure $\mu$ on $(\mathfrak{M}, \mathcal{F})$. It is the theory's only representation of uncertainty.

**Definition 3.3 (Representation).** A *representation map* is a measurable map $r : \mathfrak{M} \to \mathcal{R}$ into a measurable space $\mathcal{R}$ of representations. $R := r(m)$ is what is available; $m$ is not.

**Definition 3.4 (Arena).** An *arena* $A$ is a set whose elements are the candidates for valuation. Elements of $A$ are called *items*.

**Definition 3.5 (Outcome space and outcome map).** An *outcome space* is a measurable space $Y$. An *outcome map* is a measurable $M : \mathfrak{M} \to Y$.

**Definition 3.6 (Operation).** An *operation* is a measurable map $\tau : \mathfrak{M} \to \mathfrak{M}$. The *factual operation* is $\mathrm{id}_\mathfrak{M}$.

**Definition 3.7 (Operation family).** An *operation family* over an arena $A$ is a collection $\{\tau_a\}_{a \in A}$ of operations indexed by items.

**Definition 3.8 (Valuation space).** A *valuation space* is a measurable space $V$ equipped with a partial order $\le_V$. Elements of $V$ carry a fixed dimension.

**Definition 3.9 (Discrepancy).** A *discrepancy* is a measurable map $d : Y \times Y \to V$.

**Definition 3.10 (Reduction).** A *reduction* is a map $\rho : \Delta(V) \to V \cup \mathcal{I}(V) \cup \{\bot\}$, where $\Delta(V)$ is the set of probability measures on $V$, $\mathcal{I}(V)$ is the set of order-intervals of $V$, and $\bot$ is a distinguished symbol denoting refusal.

**Definition 3.11 (Relation instance).** A *relation instance* is a pair $e = (t, \nu)$ with $t$ in a set $T$ of *types* and $\nu$ in a set $N$ of *signatures*. Signatures carry the conditions under which the instance holds.

**Definition 3.12 (Structure).** A *structure* is a tuple $R = (U, E, \mathrm{src}, \mathrm{tgt}, \lambda)$ where $U$ is a set of elements, $E$ a set of relation instances, $\mathrm{src}, \mathrm{tgt} : E \to U$, and $\lambda : E \to T \times N$.

---

## 4. Axioms

**Axiom A1 (Contrast).** Every significance value is a valuation of a comparison between an outcome under the factual operation and an outcome under a declared operation. No significance value is a property of an item alone.

**Axiom A2 (Contextual completeness).** A context supplies exactly: an admissibility restriction on the knowledge state, an outcome map, an operation family over the arena, a discrepancy, and a reduction. A valuation for which any of these is unsupplied is undefined, not defaulted.

**Axiom A3 (Representation invariance).** Let $\iota$ be an isomorphism of structures and $\iota_*$ the induced transport of contexts. Then $\sigma_{\iota_* C}(\iota a) = \sigma_C(a)$ for every item $a$.

**Axiom A4 (Contextual nullity).** For every item $a$ there exists a context $C$ with $\sigma_C(a) = 0_V$.

**Axiom A5 (Non-fabrication).** If the contrast is not determined by the available representation, the value is the determined set, or $\bot$. It is never a point chosen from an undetermined set.

**Axiom A6 (Joint uncertainty).** Uncertainty is carried by a single joint knowledge state. Marginal and conditional quantities are derived from it and are never primitive.

**Axiom A7 (Dimensional coherence).** All values arising under one context lie in that context's valuation space. Values arising under distinct contexts are not combined.

**Observation 4.1.** A1 and A4 together are the whole of the theory's rejection of intrinsic importance. A3 is the whole of its rejection of representational artefacts. Everything proved below is a consequence of these five together with A2, A5, A6 and A7.

---

## 5. Counterfactual theory

**Definition 5.1 (Pointwise contrast).** Given an outcome map $M$, a discrepancy $d$ and an operation $\tau$, the *pointwise contrast* is the measurable map
$$\delta_{M,d,\tau} : \mathfrak{M} \to V, \qquad \delta_{M,d,\tau}(m) = d\big(M(m),\, M(\tau m)\big).$$

**Definition 5.2 (Contrast law).** Given a knowledge state $\mu$, the *contrast law* is the pushforward $(\delta_{M,d,\tau})_* \mu \in \Delta(V)$.

**Observation 5.3.** The contrast is a property of the pair $(M, \tau)$, not of $\tau$ alone. An operation with large effect on the model but no effect on the outcome map has null contrast.

**Definition 5.4 (Model-term operation).** An operation $\tau$ is *model-term* when it acts on the specification of a model and not on any purported underlying object. The theory admits only model-term operations.

**Observation 5.5.** Definition 5.4 is a restriction of the theory, not a claim about the world. Nothing below requires that the operation be physically realisable, and no theorem below licenses reading $\tau$ as an intervention on anything other than a model.

**Theorem 1 (Order reversal).** There exist a model space, an arena $A = \{a, b\}$, and two contexts $C_1, C_2$ differing only in their outcome maps, such that
$$\sigma_{C_1}(a) > \sigma_{C_1}(b) \quad\text{and}\quad \sigma_{C_2}(a) < \sigma_{C_2}(b).$$

*Proof.* Let $\mathfrak{M} = \mathbb{R}^2$ with $\mu = \delta_{(0,0)}$. Let $\tau_a(x,y) = (x+2, y+1)$ and $\tau_b(x,y) = (x+1, y+2)$. Let $M_1(x,y) = x$ and $M_2(x,y) = y$, with $V = \mathbb{R}_{\ge 0}$, $d(u,v) = |u-v|$, and $\rho$ the evaluation of a point mass. Then $\sigma_{C_1}(a) = 2 > 1 = \sigma_{C_1}(b)$ and $\sigma_{C_2}(a) = 1 < 2 = \sigma_{C_2}(b)$. $\blacksquare$

**Corollary 1.1.** No function on items alone induces the significance orderings of all contexts. In particular there is no context-free ordering of an arena consistent with every context.

**Corollary 1.2 (Nullity is attainable).** Taking $\tau_a(x,y) = (x, y+1)$ and $M_1(x,y)=x$ gives $\sigma_{C_1}(a) = 0$. Hence A4 is satisfiable and is not vacuous.

---

## 6. Context theory

**Definition 6.1 (Context).** A *context* is a tuple
$$C = \big(\mathfrak{A},\, M,\, \{\tau_a\}_{a \in A},\, d,\, \rho\big)$$
where $\mathfrak{A}$ is an admissibility restriction determining a knowledge state $\mu_C$, and $M, \tau, d, \rho$ are as in Definitions 3.5, 3.7, 3.9 and 3.10.

**Definition 6.2 (Significance).** The *significance* of item $a$ under context $C$ is
$$\sigma_C(a) \;=\; \rho\Big( \big(\delta_{M, d, \tau_a}\big)_* \mu_C \Big).$$

**Observation 6.3.** Definition 6.2 satisfies A1 by construction and satisfies A2 by construction. It is the unique form compatible with both, up to the choice of the five components.

**Definition 6.4 (Designation).** A context $C$ *designates* if any of its components depends on data not invariant under $\mathrm{Aut}(R)$. Data effecting such dependence is the context's *designation*.

**Definition 6.5 (Filter context).** A context is a *filter context* if all of its components are determined by $\mathrm{Aut}(R)$-invariant data.

**Theorem 2 (Designation necessity).** Assume A3. Let $\pi \in \mathrm{Aut}(R)$ and suppose $\pi_* C = C$. Then $\sigma_C(\pi a) = \sigma_C(a)$ for every item $a$.

*Proof.* By A3, $\sigma_{\pi_* C}(\pi a) = \sigma_C(a)$. Since $\pi_* C = C$, the left side is $\sigma_C(\pi a)$. $\blacksquare$

**Corollary 2.1 (Filters cannot break symmetry).** A filter context cannot assign distinct significance to two items in the same $\mathrm{Aut}(R)$-orbit.

*Proof.* If every component of $C$ is determined by $\mathrm{Aut}(R)$-invariant data then $\pi_* C = C$ for all $\pi \in \mathrm{Aut}(R)$; apply Theorem 2. $\blacksquare$

**Corollary 2.2.** If a question's correct answer distinguishes two items in the same $\mathrm{Aut}(R)$-orbit, then any context answering it designates. Designation is therefore necessary, not merely convenient.

**Observation 6.6.** Theorem 2 is the precise sense in which context must *anchor* rather than *restrict*. Restriction by invariant predicates is an endomorphism of the invariance class; only non-invariant data leaves it.

**Observation 6.7.** Theorem 2 gives a necessary condition, not a sufficient one. A designating context may still fail to separate two items, for reasons unrelated to symmetry.

---

## 7. Difference theory

**Definition 7.1 (Observational equivalence).** Define $m \sim m'$ iff $r(m) = r(m')$. The equivalence classes are the *fibres* of $r$.

**Theorem 3 (Factorisation).** Let $g : \mathfrak{M} \to V$ be measurable. There exists measurable $h : \mathcal{R} \to V$ with $g = h \circ r$ if and only if $g$ is constant on the fibres of $r$.

*Proof.* ($\Rightarrow$) If $g = h \circ r$ and $m \sim m'$ then $r(m) = r(m')$, so $g(m) = h(r(m)) = h(r(m')) = g(m')$.
($\Leftarrow$) If $g$ is constant on fibres, define $h$ on $r(\mathfrak{M})$ by $h(x) := g(m)$ for any $m \in r^{-1}(x)$; this is well defined by hypothesis, and $g = h \circ r$. Measurability of $h$ holds with respect to the $\sigma$-algebra induced on $r(\mathfrak{M})$, which is the standard factorisation statement. $\blacksquare$

**Definition 7.2 (Sufficiency).** A representation map $r$ is *$C$-sufficient* if $\delta_{M,d,\tau_a}$ is constant on the fibres of $r$ for every $a \in A$.

**Corollary 3.1 (Computability).** The contrast is computable from the representation if and only if $r$ is $C$-sufficient.

*Proof.* Immediate from Theorem 3 applied to $g = \delta_{M,d,\tau_a}$. $\blacksquare$

**Definition 7.3 (Identified set).** For $x \in \mathcal{R}$, the *identified set* of the contrast is
$$\mathcal{S}_C(a, x) \;=\; \big\{\, \delta_{M,d,\tau_a}(m) \;:\; m \in r^{-1}(x) \,\big\} \subseteq V.$$

**Corollary 3.2 (Forced abstention).** If $r$ is not $C$-sufficient then for some $x$ the set $\mathcal{S}_C(a,x)$ is not a singleton, and no representation-measurable function equals the contrast. By A5 the admissible output is $\mathcal{S}_C(a,x)$, an interval containing it, or $\bot$.

*Proof.* Non-sufficiency means $\delta$ is non-constant on some fibre $r^{-1}(x)$, so $\mathcal{S}_C(a,x)$ has at least two elements. By Theorem 3 no $h$ satisfies $h \circ r = \delta$. A5 then forbids returning a point. $\blacksquare$

**Observation 7.4.** Corollary 3.2 establishes that abstention is a consequence of the axioms and not a policy choice. A theory admitting A5 cannot make abstention optional.

**Observation 7.5.** Conversely, A5 does not make abstention admissible in every setting. Where the arena is subject to an exogenous constraint requiring a selection, abstention fails to perform the required act, and the reduction $\rho$ of the governing context must have codomain $V$ rather than $V \cup \mathcal{I}(V) \cup \{\bot\}$. Whether $\bot$ is available is a property of the context, not of the theory.

---

## 8. Significance theory

**Definition 8.1 (Effect significance).** Let $(Y, d_Y)$ be a metric space, $V = \mathbb{R}_{\ge 0}$, $d = d_Y$, and $\rho$ a location functional. Then
$$\sigma^{\mathrm{eff}}_C(a) \;=\; \rho\Big(\big(m \mapsto d_Y(M(m), M(\tau_a m))\big)_* \mu_C\Big).$$

**Definition 8.2 (Decision significance).** Let $D = (\mathcal{A}, L)$ be a decision problem with action set $\mathcal{A}$ and loss $L : \mathcal{A} \times \mathfrak{M} \to \mathbb{R}$. Write $\alpha^*(\nu) \in \arg\min_{\alpha} \mathbb{E}_\nu L(\alpha, \cdot)$ and let $\mu_C^{\,\tau_a}$ denote the knowledge state obtained by applying $\tau_a$. Then
$$\sigma^{\mathrm{dec}}_C(a) \;=\; \mathbb{E}_{\mu_C} L\big(\alpha^*(\mu_C^{\,\tau_a}), \cdot\big) \;-\; \mathbb{E}_{\mu_C} L\big(\alpha^*(\mu_C), \cdot\big).$$

**Definition 8.3 (Information significance).** Let $\mathcal{E}_a$ be a random element denoting evidence bearing on $a$, and let $\mathfrak{r}(\nu) = \min_{\alpha} \mathbb{E}_\nu L(\alpha, \cdot)$ be the Bayes risk. Then
$$\sigma^{\mathrm{inf}}_C(a) \;=\; \mathfrak{r}(\mu_C) \;-\; \mathbb{E}\big[\mathfrak{r}(\mu_C^{\,\mathcal{E}_a})\big].$$

**Theorem 4 (Non-negativity).** $\sigma^{\mathrm{eff}}_C \ge 0$, $\sigma^{\mathrm{dec}}_C \ge 0$, and $\sigma^{\mathrm{inf}}_C \ge 0$.

*Proof.* For $\sigma^{\mathrm{eff}}$: $d_Y \ge 0$ and $\rho$ is a location functional of a measure supported on $\mathbb{R}_{\ge 0}$.
For $\sigma^{\mathrm{dec}}$: $\alpha^*(\mu_C)$ minimises $\alpha \mapsto \mathbb{E}_{\mu_C} L(\alpha, \cdot)$, so $\mathbb{E}_{\mu_C} L(\alpha, \cdot) \ge \mathbb{E}_{\mu_C} L(\alpha^*(\mu_C), \cdot)$ for every $\alpha$, in particular for $\alpha = \alpha^*(\mu_C^{\,\tau_a})$.
For $\sigma^{\mathrm{inf}}$: $\mathfrak{r}$ is an infimum of affine functionals of $\nu$, hence concave. By the tower property $\mathbb{E}[\mu_C^{\,\mathcal{E}_a}] = \mu_C$, and by Jensen's inequality for concave functionals $\mathbb{E}[\mathfrak{r}(\mu_C^{\,\mathcal{E}_a})] \le \mathfrak{r}(\mathbb{E}[\mu_C^{\,\mathcal{E}_a}]) = \mathfrak{r}(\mu_C)$. $\blacksquare$

**Theorem 5 (Pairwise non-equivalence).** The three significances are pairwise non-equivalent: for each pair there exist a context and two items on which the pair's orderings disagree.

*Proof.* Three constructions.

(i) *Effect against decision.* Let $\mathfrak{M} = \mathbb{R}^2$, $\mu = \delta_{(0,0)}$, $M = \mathrm{id}$, $d_Y$ the Euclidean metric, $\mathcal{A} = \mathbb{R}$ and $L(\alpha,(x,y)) = (\alpha - x)^2$, which depends only on $x$. Let $\tau_a(x,y) = (x,\, y+10)$ and $\tau_b(x,y) = (x+1,\, y)$.
Then $\sigma^{\mathrm{eff}}(a) = 10 > 1 = \sigma^{\mathrm{eff}}(b)$.
For the decision significance: $\tau_a$ leaves the $x$-marginal unchanged, so $\alpha^*(\mu^{\tau_a}) = \alpha^*(\mu) = 0$ and $\sigma^{\mathrm{dec}}(a) = 0$. For $b$: $\alpha^*(\mu^{\tau_b}) = 1$ while $\alpha^*(\mu) = 0$, so
$$\sigma^{\mathrm{dec}}(b) = \mathbb{E}_\mu (1 - x)^2 - \mathbb{E}_\mu (0-x)^2 = 1 - 0 = 1 > 0.$$
Hence $\sigma^{\mathrm{eff}}(a) > \sigma^{\mathrm{eff}}(b)$ while $\sigma^{\mathrm{dec}}(a) < \sigma^{\mathrm{dec}}(b)$.

(ii) *Decision against information.* Let $\mathfrak{M} = \mathbb{R}^2$ with independent coordinates $\theta_a, \theta_b$, and $L(\alpha, \theta) = (\alpha - \theta_a - \theta_b)^2$, so that $\alpha^*(\nu) = \mathbb{E}_\nu[\theta_a + \theta_b]$ and $\mathfrak{r}(\nu) = \mathrm{Var}_\nu[\theta_a + \theta_b]$.
Let $\theta_a$ be $\mu$-degenerate at $0$ and $\theta_b \sim \mathcal{N}(0, s^2)$ with $s^2 > 0$.
For $a$: degeneracy makes $\mathcal{E}_a$ $\mu$-almost surely uninformative, so $\mu^{\mathcal{E}_a} = \mu$ and $\sigma^{\mathrm{inf}}(a) = 0$. Let $\tau_a$ shift $\theta_a$ by $1$; then $\alpha^*(\mu^{\tau_a}) = 1 \ne 0 = \alpha^*(\mu)$ and $\sigma^{\mathrm{dec}}(a) = 1 > 0$.
For $b$: let $\tau_b$ replace $\theta_b$ by its mean $0$. This preserves $\mathbb{E}[\theta_a + \theta_b]$, so $\alpha^*(\mu^{\tau_b}) = \alpha^*(\mu)$ and $\sigma^{\mathrm{dec}}(b) = 0$. Let $\mathcal{E}_b$ reveal $\theta_b$ exactly; then $\mathbb{E}[\mathfrak{r}(\mu^{\mathcal{E}_b})] = 0$ while $\mathfrak{r}(\mu) = s^2$, so $\sigma^{\mathrm{inf}}(b) = s^2 > 0$.
Hence $\sigma^{\mathrm{dec}}(a) > \sigma^{\mathrm{dec}}(b)$ while $\sigma^{\mathrm{inf}}(a) < \sigma^{\mathrm{inf}}(b)$.

(iii) *Effect against information.* Retain the model of (ii) and set $M = \mathrm{id}$ with $d_Y$ Euclidean. Then $\sigma^{\mathrm{eff}}(a) = 1$, from the unit shift of $\theta_a$, while $\sigma^{\mathrm{inf}}(a) = 0$ by degeneracy. For $b$, mean-replacement gives $\sigma^{\mathrm{eff}}(b) = \rho(|\theta_b|) $, which for $s$ small is less than $1$, while $\sigma^{\mathrm{inf}}(b) = s^2 > 0$. Hence $\sigma^{\mathrm{eff}}(a) > \sigma^{\mathrm{eff}}(b)$ and $\sigma^{\mathrm{inf}}(a) < \sigma^{\mathrm{inf}}(b)$. $\blacksquare$

**Corollary 5.1.** The three significances are not measurements of one latent quantity. No monotone reparametrisation carries one into another, since monotone maps preserve order and the orders disagree.

**Corollary 5.2.** Any single scalar presented as "significance" without naming which of the three it is, is underdetermined.

**Theorem 6 (Triviality of additive context-free valuation).** Let $S : A \to \mathbb{R}_{\ge 0}$, let $\beta > 0$, and suppose that for every context $C$ there is $g_C : A \to \mathbb{R}_{\ge 0}$ with
$$\sigma_C(a) = \beta S(a) + g_C(a) \qquad \text{for all } a \in A.$$
Assume A4. Then $S \equiv 0$.

*Proof.* Fix $a \in A$. By A4 choose $C$ with $\sigma_C(a) = 0$. Then $\beta S(a) + g_C(a) = 0$ with $\beta S(a) \ge 0$ and $g_C(a) \ge 0$. A sum of two non-negative reals vanishes only if both vanish, so $\beta S(a) = 0$; since $\beta > 0$, $S(a) = 0$. As $a$ was arbitrary, $S \equiv 0$. $\blacksquare$

**Observation 6.1'.** The non-negativity of $g_C$ is essential. Dropping it, put $g'_C := \beta S + g_C$; then $\sigma_C = g'_C$ identically, and $S$ has been eliminated without altering any value. Hence the additive decomposition is either forced to triviality by Theorem 6, or is absorbable and therefore carries no content. In neither case does a context-free additive term do work.

**Corollary 6.2.** No non-trivial context-free scalar can enter significance as a non-negative additive term. Any context-free quantity retained by a theory satisfying A4 must be non-scalar, non-additive, or non-contributory.

**Theorem 7 (No epistemic gain from derived summaries).** Let $Z$ be any random element and $R$ the representation. Let $S = f(R)$ for measurable $f$. Then $I(Z; S, R) = I(Z; R)$, and consequently $I(Z; S \mid R) = 0$.

*Proof.* Since $S$ is a measurable function of $R$, $\sigma(S) \subseteq \sigma(R)$, hence $\sigma(S, R) = \sigma(R)$. Mutual information depends on the joint law only through the generated $\sigma$-algebras, so $I(Z; S, R) = I(Z; R)$. The chain rule $I(Z; S, R) = I(Z;R) + I(Z; S \mid R)$ then gives $I(Z; S \mid R) = 0$. $\blacksquare$

**Corollary 7.1.** A quantity derived from the representation cannot be justified epistemically. Any justification for retaining one must be structural, computational, or normative.

**Definition 8.4 (Arena normalisation).** For an arena $A$ and $\varphi : A \to \mathbb{R}_{>0}$, the *max-normalisation* is $\nu^A(a) = \varphi(a) / \max_{b \in A} \varphi(b)$.

**Theorem 8 (Normalisation is arena-dependent).** Let $A \subsetneq A'$ with $\varphi$ extending from $A$ to $A'$ and $\max_{A'} \varphi > \max_A \varphi$. Then $\nu^{A'}(a) < \nu^{A}(a)$ for every $a \in A$, while the restriction of $\nu^{A'}$ to $A$ induces the same order as $\nu^{A}$.

*Proof.* Write $\mathsf{m} = \max_A \varphi$ and $\mathsf{m}' = \max_{A'}\varphi > \mathsf{m}$. Then $\nu^{A'}(a) = \varphi(a)/\mathsf{m}' < \varphi(a)/\mathsf{m} = \nu^A(a)$ since $\varphi(a) > 0$. Both are positive multiples of $\varphi$ on $A$, so they induce the same order. $\blacksquare$

**Corollary 8.1.** Normalised values are not comparable across arenas, and their equality or inequality across arenas carries no information about the items.

**Corollary 8.2.** A normalised value is dimensionless and therefore cannot be compared with any dimensioned quantity. By A7 it cannot be calibrated.

**Observation 8.5.** Theorem 8 does not forbid ranking. It forbids treating a normalised value as a magnitude.

---

## 9. Composition theory

**Definition 9.1 (Compatibility).** A *compatibility predicate* is a relation $\kappa \subseteq E \times E$. Instances $e, f$ are *compatible* iff $(e,f) \in \kappa$.

**Definition 9.2 (Partial composition).** A *composition* is a partial map $\odot : E \times E \rightharpoonup E$ whose domain is $\kappa$.

**Definition 9.3 (Path).** A *path* is a finite sequence $p = (e_1, \dots, e_k)$ with $\mathrm{tgt}(e_i) = \mathrm{src}(e_{i+1})$.

**Definition 9.4 (Composition semantics).** $[\![p]\!]_{\mathrm{comp}}$ is the result of evaluating $e_1 \odot \cdots \odot e_k$ under a declared bracketing, or $\bot$ if any required composition is undefined.

**Definition 9.5 (Diffusion semantics).** Given a weight $w : E \to \mathbb{R}_{\ge 0}$, $[\![p]\!]_{\mathrm{diff}} = \prod_{i=1}^{k} w(e_i)$.

**Observation 9.6.** $[\![\cdot]\!]_{\mathrm{diff}}$ is total. $[\![\cdot]\!]_{\mathrm{comp}}$ is partial. The two have different codomains and different meanings: the first is a transport magnitude, the second a relation instance.

**Theorem 9 (Insufficiency of type-level licensing).** Suppose $\kappa$ is not a function of types alone, i.e. there exist $e_1, e_2, e_1', e_2'$ with $t(e_1) = t(e_1')$, $t(e_2) = t(e_2')$, $(e_1,e_2) \in \kappa$ and $(e_1', e_2') \notin \kappa$. Then every predicate $\hat\kappa$ depending only on types is either unsound or incomplete with respect to $\kappa$.

*Proof.* Let $\hat\kappa$ depend only on types. Since $t(e_1)=t(e_1')$ and $t(e_2)=t(e_2')$, $\hat\kappa$ takes the same value on $(e_1,e_2)$ and $(e_1',e_2')$. If that value is *admit*, then $\hat\kappa$ admits $(e_1',e_2') \notin \kappa$ and is unsound. If it is *refuse*, then $\hat\kappa$ refuses $(e_1,e_2) \in \kappa$ and is incomplete. $\blacksquare$

**Corollary 9.1.** If compatibility depends on signature data that varies within a type pair, instance-level licensing is necessary. No schema-level licence is simultaneously sound and complete.

**Theorem 10 (Non-associativity).** Partial composition is not associative in general: there exist a type set, a consistent composition table, and instances $e_1, e_2, e_3$ such that $(e_1 \odot e_2) \odot e_3$ is undefined while $e_1 \odot (e_2 \odot e_3)$ is defined.

*Proof.* Let $T = \{P, Q, R\}$ and define $\odot$ on types by
$$P \odot Q = R, \qquad Q \odot Q = Q, \qquad R \odot Q \text{ undefined},$$
all other pairs undefined. This table is a well-defined partial map. Take $t(e_1) = P$, $t(e_2) = t(e_3) = Q$.
Left bracketing: $e_1 \odot e_2$ has type $R$; then $R \odot Q$ is undefined, so $(e_1 \odot e_2)\odot e_3 = \bot$.
Right bracketing: $e_2 \odot e_3$ has type $Q$; then $P \odot Q = R$, so $e_1 \odot (e_2 \odot e_3)$ is defined with type $R$. $\blacksquare$

**Corollary 10.1.** $(E, \odot)$ is a partial magma and not in general a partial semigroup.

**Corollary 10.2.** The value of a path is not determined by the path. A bracketing must be declared, and distinct declared bracketings are distinct computations.

**Corollary 10.3 (Licensed paths do not form a substructure).** The set of licensed paths is not in general the path set of any substructure of $R$.

*Proof.* Suppose it were the path set of a substructure $R' \subseteq R$. Then a path is licensed iff each of its instances lies in $R'$, a condition on instances alone and hence independent of bracketing and of position within the path. Theorem 10 exhibits instances $e_1, e_2, e_3$, each licensed in some evaluation, for which one bracketing is defined and another is not. Under the substructure hypothesis both bracketings would be licensed. Contradiction. $\blacksquare$

**Observation 10.4.** Corollary 10.3 is the reason licensure must be carried by a state rather than by a set of admitted instances. The natural carrier is a product of the element set with an automaton state and a register holding the previously composed signature; admission is then a transition guard, not a membership test. Notation suggesting a licensed subgraph is therefore misleading, and no result above depends on such an object.

**Observation 10.3.** Theorem 10 is a statement about partial operations, not about uncertainty. If compatibility is gated only by a quantity that accumulates additively along a path with a threshold on the running total, associativity is preserved, since partial sums of non-negative terms are dominated by the total. Non-associativity requires the *type* or *kind* of the composite to feed back into compatibility.

**Theorem 11 (Semantic separation).** There exist a structure, a weight $w$, a designation $\Delta \subseteq U$, and items $a, b$ such that
$$\textstyle\sum_{p : a \to \Delta} [\![p]\!]_{\mathrm{diff}} \;>\; \sum_{p : b \to \Delta} [\![p]\!]_{\mathrm{diff}},$$
while $[\![p]\!]_{\mathrm{comp}} = \bot$ for every path $p$ from $a$ to $\Delta$ and $[\![q]\!]_{\mathrm{comp}} \ne \bot$ for some path $q$ from $b$ to $\Delta$.

*Proof.* Let $U = \{a, b, c, c', z\}$ with $\Delta = \{z\}$, and let $E$ consist of four instances
$$e_1 : a \to c, \quad e_2 : c \to z, \quad f_1 : b \to c', \quad f_2 : c' \to z,$$
so that the only path from $a$ to $z$ is $(e_1, e_2)$ and the only path from $b$ to $z$ is $(f_1, f_2)$.
Assign $w(e_1) = w(e_2) = 1$ and $w(f_1) = w(f_2) = \tfrac{1}{10}$. Then the diffusion sums are $1$ and $\tfrac{1}{100}$, so the displayed inequality holds.
Assign signatures so that $(e_1, e_2) \notin \kappa$ and $(f_1, f_2) \in \kappa$. This is admissible because $\kappa$ is by Definition 9.1 an arbitrary relation on instances, and the four instances are distinct. Then $[\![(e_1,e_2)]\!]_{\mathrm{comp}} = \bot$, exhausting the paths from $a$ to $\Delta$, while $[\![(f_1,f_2)]\!]_{\mathrm{comp}} \ne \bot$. $\blacksquare$

**Corollary 11.1.** A diffusion-derived ordering is not evidence of a composed relation, and the absence of a composed relation does not entail a small diffusion value.

**Observation 11.2.** Theorem 11 does not show that diffusion functionals are invalid. $[\![\cdot]\!]_{\mathrm{diff}}$ is well defined on any weighted structure, whatever the transitivity properties of the relations involved. The theorem shows only that the two semantics are independent, so that identifying a diffusion value with a relational or inferential claim is an error of interpretation and not of mathematics.

**Observation 11.3.** Consequently the assertion *"path functionals are invalid when the underlying relations are non-transitive"* is false. The defensible assertion is that a path functional whose semantics is undeclared is underdetermined: its mathematical value exists, and its meaning does not.

---

## 10. Representation invariance

**Definition 10.1 (Isomorphism).** An *isomorphism* of structures $\iota : R \to R'$ is a bijection on elements and on relation instances preserving $\mathrm{src}$, $\mathrm{tgt}$, type, and signature.

**Definition 10.2 (Automorphism group).** $\mathrm{Aut}(R)$ is the group of isomorphisms $R \to R$.

**Definition 10.3 (Structural valuation).** A valuation $\varphi : U \to V$ is *structural* if $\varphi(\pi u) = \varphi(u)$ for all $\pi \in \mathrm{Aut}(R)$.

**Theorem 12 (Orbit constancy).** Every structural valuation is constant on $\mathrm{Aut}(R)$-orbits.

*Proof.* Immediate from Definition 10.3: the orbit of $u$ is $\{\pi u : \pi \in \mathrm{Aut}(R)\}$, on which $\varphi$ takes the constant value $\varphi(u)$. $\blacksquare$

**Corollary 12.1.** If a valuation distinguishes two elements of one orbit, it is not structural, hence depends on data outside the isomorphism class of $R$.

**Definition 10.4 (Representational artefact).** A datum attached to a structure is a *representational artefact* if it is not preserved by every isomorphism onto an isomorphic structure — for example, element identifiers, enumeration order, or storage layout.

**Theorem 13 (Artefact exclusion).** Assume A3. Then $\sigma_C$ is independent of every representational artefact.

*Proof.* Let $\iota : R \to R'$ be an isomorphism differing only in artefacts, so that $\iota_* C = C$ under the identification of the two structures. By A3, $\sigma_{\iota_* C}(\iota a) = \sigma_C(a)$, hence $\sigma_C(\iota a) = \sigma_C(a)$. Since $\iota$ ranges over all artefact-changing isomorphisms, $\sigma_C$ is constant along them. $\blacksquare$

**Corollary 13.1.** Any valuation whose output changes when identifiers are permuted, or when items are stored in a different order, violates A3 and is not a significance in the sense of Definition 6.2.

**Observation 10.5.** Theorems 2 and 12 are two faces of one fact. Invariance is a constraint on what a valuation can see; designation is the supply of data the invariance does not cover. Neither is dispensable: without invariance the valuation depends on the encoding, and without designation it cannot separate symmetric items.

---

## 11. Proven theorems

| № | Statement | Established at |
|---|---|---|
| 1 | Significance orderings under distinct contexts can be strictly reversed | §5 |
| 2 | A context fixed by an automorphism cannot distinguish items related by it | §6 |
| 3 | A function factors through the representation iff it is constant on fibres | §7 |
| 4 | All three significances are non-negative | §8 |
| 5 | The three significances are pairwise non-equivalent | §8 |
| 6 | A non-negative additive context-free scalar is identically zero under contextual nullity | §8 |
| 7 | A summary derived from the representation carries no additional information | §8 |
| 8 | Max-normalised values depend on the arena and are dimensionless | §8 |
| 9 | Type-level licensing is unsound or incomplete when compatibility depends on signatures | §9 |
| 10 | Partial composition is not associative in general | §9 |
| 11 | Diffusion and composition semantics are independent | §9 |
| 12 | Structural valuations are constant on automorphism orbits | §10 |
| 13 | Significance is independent of representational artefacts | §10 |

---

## 12. Proven limitations

**Limitation 12.1 (No context-free ordering).** By Corollary 1.1 there is no ordering of an arena consistent with every context. The theory therefore cannot deliver a global importance ranking, and no extension of it can, short of abandoning A1 or A4.

**Limitation 12.2 (No context-free scalar contribution).** By Theorem 6 and Observation 6.1', a context-free scalar contributing additively and non-negatively is identically zero, and without non-negativity is absorbable. The theory admits no primitive of this kind.

**Limitation 12.3 (No epistemic role for derived summaries).** By Theorem 7, no quantity computed from the representation can inform anything beyond the representation. The theory can motivate such quantities only structurally, computationally, or normatively.

**Limitation 12.4 (The reduction is not determined).** A2 requires a reduction $\rho$; the theory does not supply one. Distinct reductions of the same contrast law induce distinct orderings whenever the law is asymmetric — for a two-item arena with contrast laws of equal mean and unequal median, the mean-reduction and median-reduction orderings disagree. Significance is therefore defined only relative to a declared reduction.

**Limitation 12.5 (Path values are not intrinsic).** By Corollary 10.2 a path does not determine its composite. Every path-valued quantity is relative to a declared bracketing, and the theory provides no canonical choice.

**Limitation 12.6 (Identification is not guaranteed).** By Corollary 3.2, whenever the representation is not $C$-sufficient the contrast is only set-identified. The theory gives no condition guaranteeing sufficiency, and supplies no point value in its absence.

**Limitation 12.7 (No cross-context comparison).** By A7 and Corollary 8.2, values from distinct contexts lie in distinct valuation spaces. Comparison requires a chosen order-embedding, and the theory distinguishes none.

**Limitation 12.8 (Designation is exogenous).** Theorem 2 shows designation is necessary and says nothing about where it comes from. The theory cannot generate a designation; it can only require one.

---

## 13. Open mathematical questions

**Open Question 13.1.** Under what conditions on a composition table does $(E, \odot)$ admit an associative refinement — a partial semigroup $\odot'$ with $\odot' \supseteq \odot$ agreeing wherever both are defined? Is there an obstruction theory for the failure?

**Open Question 13.2.** Characterise $C$-sufficiency structurally. Given a context $C$ and a representation map $r$, is there a computable criterion for constancy of $\delta_{M,d,\tau_a}$ on the fibres of $r$, or a useful sufficient condition?

**Open Question 13.3.** Is there a set of axioms on preferences over contrast laws forcing a unique reduction $\rho$, in the manner of the classical representation theorems? If not, what is the largest class of contexts on which $\rho$ is determined up to monotone equivalence?

**Open Question 13.4.** Do the three significances of §8 arise as fibres of a single indexed structure — a fibration over a base of question-types — such that the pairwise non-equivalence of Theorem 5 is the statement that the fibration is non-trivial? Such a structure would organise them without collapsing them.

**Open Question 13.5.** Is contextual admissibility reducible to a threshold on a decision-theoretic loss, or does it carry structure not expressible as a threshold? Equivalently: is the admit/reject/indeterminate trichotomy a coarsening of a real-valued criterion, or irreducibly three-valued?

**Open Question 13.6 — answered negatively; retained as a closed record.** *Question:* is there an invariant of the licensed-path structure — the pair $(E, \kappa)$ together with its signature algebra — not expressible in an existing typed, temporal, or dimensionally annotated formalism?

*Answer:* no. The structure of §9 is a guarded register automaton over a data path: a finite automaton over relation labels together with a guard on registers carrying previous or composed signatures, evaluated on the product state space $U \times Q \times R$. This is established graph-database theory — regular path queries, regular path queries with comparisons over values stored along a path, and register/binding formalisms for graph data. The guards are instantiated by existing temporal, spatial and dimensional vocabularies, and dimensional compatibility itself long predates any of them.

**Observation 13.6.1.** The closure of 13.6 does not disturb any theorem of §9. Theorems 9, 10 and 11 are statements about the structure, not about its novelty, and each remains proved. What is withdrawn is only the expectation that the structure is new.

**Open Question 13.7.** Define a pseudometric on contexts under which nearby contexts induce nearby significance orderings. Does such a pseudometric exist, and is significance continuous with respect to it? A negative answer would mean small changes of question can produce discontinuous changes of valuation.

**Open Question 13.8.** For which arenas and operation families is the map $a \mapsto \sigma_C(a)$ determined by the pairwise contrasts, and for which does it require joint operations $\tau_{\{a,b\}}$? Equivalently: when do items interact, and does the theory need a coalitional extension?

---

## 14. Explicitly rejected formulations

Each rejection names the result that defeats it.

**Rejection 14.1.** *Significance is an intrinsic attribute of an item.*
Defeated by Theorem 1 and Corollary 1.1: orderings under distinct contexts are strictly reversible, so no function of the item alone induces them.

**Rejection 14.2.** *Significance decomposes as a context-free scalar plus a context-dependent remainder.*
Defeated by Theorem 6 with Observation 6.1': under contextual nullity the scalar is identically zero, and without non-negativity it is absorbable.

**Rejection 14.3.** *A context-free summary of the representation supplies information not present in the representation.*
Defeated by Theorem 7.

**Rejection 14.4.** *Significance is a rank normalised within the arena under consideration.*
Defeated by Theorem 8 with Corollaries 8.1 and 8.2: the value depends on the arena and is dimensionless, hence uncalibratable.

**Rejection 14.5.** *Significance is one quantity, variously measured.*
Defeated by Theorem 5 and Corollary 5.1: the three significances disagree in order, and no monotone reparametrisation relates them.

**Rejection 14.6.** *Significance emerges from structure.*
Defeated as a formulation rather than as a claim: it specifies no map, no operation, and no valuation space, and therefore admits no instance of Definition 6.2. By A2 a valuation with unsupplied components is undefined.

**Rejection 14.7.** *A context acts by restricting the admissible structure.*
Defeated by Theorem 2 and Corollary 2.1: restriction by invariant data leaves the automorphism group acting, so a filter context cannot separate symmetric items.

**Rejection 14.8.** *Composition is licensed at the level of types.*
Defeated by Theorem 9 and Corollary 9.1 whenever compatibility depends on signature data varying within a type pair.

**Rejection 14.9.** *A path has a value determined by the path.*
Defeated by Theorem 10 and Corollary 10.2.

**Rejection 14.10.** *Path functionals are invalid when the underlying relations are non-transitive.*
Defeated by Observations 11.2 and 11.3. Diffusion semantics is total and requires no compositional structure; the functional is well defined and its interpretation, not its value, is what non-transitivity constrains. This formulation is rejected as false, and replaced by the requirement that traversal semantics be declared.

**Rejection 14.11.** *A point value may be returned when the contrast is set-identified.*
Defeated by Corollary 3.2 together with A5.

**Rejection 14.12.** *Values obtained under distinct contexts may be compared.*
Defeated by A7 with Limitation 12.7.

**Rejection 14.13.** *Significance may depend on the encoding of the structure.*
Defeated by Theorem 13 and Corollary 13.1.

---

*End of ASTRO-THEORY-0001.*
