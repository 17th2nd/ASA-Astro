# ASTRO-THEORY-0001 — Contextual Difference Theory

## Theory Candidate — Remediated

| Field | Value |
|---|---|
| Status | **Theory Candidate.** Not frozen. Not Version 1. |
| Verification | **Not externally verified.** The prior candidate was independently verified and returned **NOT FORMALLY SOUND**. This edition remediates those findings and awaits fresh independent re-verification. |
| Empirical status | **Not empirically validated.** Evidence level `EH-0`. |
| Novelty | **No novelty is claimed.** No universal prior-art subsumption is claimed either — see Open Question 15.6. |
| Coverage | **Not a complete theory of every use of the word "significance."** |
| Basis of this edition | `docs/theory/verification/ASTRO-THEORY-0001-INDEPENDENT-VERIFICATION-REPORT.md`, findings AV-001 – AV-028. |
| Prior edition | Preserved at blob `08a2257aaea6e5f23b316682025022b62d834d68`. Not overwritten silently; every change is mapped. |

**What this edition does.** It removes more than it adds. Three theorems and eleven corollaries of the prior edition were **false or unproved** and are withdrawn or replaced; two axioms are demoted to non-formal design principles; the entire recognisability subsection is withdrawn; and the principal epistemic conclusion — "the unrestricted framework has no empirical content" — is **withdrawn as unproved** and replaced by a strictly weaker, proved statement. Readers of the prior edition should treat its §9 conclusion as retracted.

---

## 1. Purpose

To state a candidate mathematical theory of contextual difference: what it is for a bearer to make a difference relative to a declared question, and what can be proved about such valuations.

**Observation 1.1.** The content is largely negative. §13 (withdrawn results) is as important as §12 (verified results).

---

## 2. Scope

**In scope.** One formal signature; design principles; axioms; contrast, significance, difference, invariance and composition; theorems with proofs; withdrawals; open obligations.

**Out of scope.** Implementation; any application domain; experiments; governance.

**Observation 2.1.** Every component is marked **primitive**, **derived**, **optional**, **partial** or **context-indexed**. No proof may use a component not licensed by its hypotheses, and no proof may use a Design Principle of §4.1.

---

## 3. Formal signature

### 3.1 Carriers

**Definition 3.1 (Bearers) — primitive.** A set $\mathfrak{B}$. Elements $b$ are *bearers*. $\mathfrak{B}$ is not a subset of any state space.

**Definition 3.2 (Model space) — primitive.** A measurable space $(\mathfrak{M},\mathcal{F})$.

**Definition 3.3 (Representation map) — primitive, optional.** A measurable $r:\mathfrak{M}\to(\mathcal{R},\mathcal{H})$.

**Definition 3.4 (Operation) — derived.** A measurable $\tau:\mathfrak{M}\to\mathfrak{M}$; $\mathrm{Op}(\mathfrak{M})$ is the set of these. The factual operation is $\mathrm{id}_{\mathfrak{M}}$.

### 3.2 Codomains

**Definition 3.5 (Codomain) — primitive, context-indexed.** A *codomain* is a triple $(W,\preceq_W,\Sigma_W)$: a set, a partial order, and a $\sigma$-algebra on it. A codomain is of class

- $\mathsf{W}_1$ (*magnitude*) if it additionally carries $(\oplus,0_W)$ making $(W,\oplus,0_W,\preceq_W)$ an ordered commutative monoid with $0_W$ least;
- $\mathsf{W}_2$ (*signed*) if it additionally carries $(+,0_W,-)$ making $(W,+,0_W,\preceq_W)$ an ordered abelian group;
- $\mathsf{W}_2^{\mathrm{m}}$ (*measurably signed*) if it is of class $\mathsf{W}_2$ **and** $(y,y')\mapsto y'-y$ is $\Sigma_W\otimes\Sigma_W/\Sigma_W$-measurable.

**Observation 3.6 (Why $\mathsf{W}_2^{\mathrm{m}}$ is a separate class) — remediates AV-017.** Class $\mathsf{W}_2$ does **not** imply measurable subtraction. Give $\mathbb{R}$ its usual ordered group structure and the countable–cocountable $\sigma$-algebra: every singleton is measurable, yet the diagonal is not product-measurable, so subtraction is not measurable. No theorem below uses subtraction unless it declares class $\mathsf{W}_2^{\mathrm{m}}$.

**Definition 3.7 (Order-intervals) — derived.** $\mathcal{I}(W) := \{\,[u,v] : u,v\in W,\ u\preceq_W v\,\}$ where $[u,v]=\{x\in W: u\preceq_W x\preceq_W v\}$.

**Definition 3.8 (Output codomain) — derived.** $\widehat{W} := W \;\sqcup\; \mathcal{I}(W) \;\sqcup\; \{\bot_{\mathrm{ind}},\bot_{\mathrm{inc}},\bot_{\mathrm{und}}\}$, a disjoint union. The three bottoms are distinct and lie outside $W$ and $\mathcal{I}(W)$.

### 3.3 Contexts

**Definition 3.9 (Absent value) — primitive.** A distinguished symbol $\bot_{\mathrm{abs}}$, used as the value of an optional component that is deliberately not supplied. It is not $\bot_{\mathrm{und}}$.

**Definition 3.10 (Context) — primitive.** A context is a seven-tuple
$$C \;=\; \big(\mu_C,\ (\mathcal{Y}_C,\mathcal{G}_C),\ M_C,\ T_C,\ \approx_C,\ \delta_C,\ (W_C,\rho_C)\big)$$

| Component | Type | Mark |
|---|---|---|
| $\mu_C$ | probability measure on $(\mathfrak{M},\mathcal{F})$ | required, primitive |
| $(\mathcal{Y}_C,\mathcal{G}_C)$ | measurable outcome space | required, context-indexed |
| $M_C:\mathfrak{M}\to\mathcal{Y}_C$ | measurable outcome map | required |
| $T_C:\mathfrak{B}\rightharpoonup\mathrm{Op}(\mathfrak{M})$ | operation assignment | required, partial |
| $\approx_C$ | equivalence on $\mathcal{Y}_C$, **or** $\bot_{\mathrm{abs}}$ | optional |
| $\delta_C:\mathcal{Y}_C\times\mathcal{Y}_C\rightharpoonup W_C$ | contrast evaluator, measurable on its domain $D_C\in\mathcal{G}_C\otimes\mathcal{G}_C$ | required, partial |
| $(W_C,\rho_C)$ | codomain and reduction (Definition 3.11) | required, context-indexed |

**Observation 3.10.1 — remediates AV-001, AV-003, AV-024.** The prior edition carried an eighth component $\mathfrak{A}_C$, an "admissibility restriction determining $\mu_C$", which had no declared type and no rule determining $\mu_C$. It is **deleted**; $\mu_C$ is now itself the component. Optionality is handled by the typed value $\bot_{\mathrm{abs}}$, so a context always supplies all seven components and A2 is unambiguous.

**Definition 3.11 (Reduction) — primitive, partial.** A partial map $\rho_C:\Delta(W_C)\rightharpoonup\widehat{W_C}$, where $\Delta(W_C)$ is the set of probability measures on $(W_C,\Sigma_{W_C})$.

**Observation 3.11.1 — remediates AV-004.** The prior edition declared four profile classes (set, multiset, measure, probability-coupled) but defined the inducing operation for only one. The three undefined classes are **deleted**. Exactly one profile construction exists: the pushforward of $\mu_C$, a probability measure. Nothing below uses any other.

**Definition 3.12 (Location functional) — derived.** For a codomain of class $\mathsf{W}_1$ realised in $(\mathbb{R}_{\ge0},+,0,\le)$, a *location functional* is a map $\ell:\Delta(\mathbb{R}_{\ge0})\rightharpoonup\mathbb{R}_{\ge0}$ satisfying $\inf\operatorname{supp}\nu\le\ell(\nu)\le\sup\operatorname{supp}\nu$ where defined, and $\ell(\delta_x)=x$.

**Observation 3.12.1 — remediates AV-013.** "Location functional" was undefined in the prior edition, which permitted a reading returning a value outside the profile's plausible range. Definition 3.12 pins it between the support bounds and fixes it on Dirac profiles.

### 3.4 Decision and evidence structure

**Definition 3.13 (Decision problem) — optional, context-indexed.** $(\mathcal{A}_C,L_C)$ with $\mathcal{A}_C\neq\emptyset$ and $L_C(\alpha,\cdot)$ measurable and $\mu$-integrable for every $\alpha$ and every measure $\mu$ at which it is used.

**Definition 3.14 (Regular evidence structure) — optional.** A triple $(\mathcal{E}_b,K_b,\Pi_b)$ where $K_b$ is a Markov kernel from $\mathfrak{M}$ to $(\mathcal{E}_b,\mathcal{B}_b)$, $\Pi_b$ is a *regular* conditional probability on $\mathfrak{M}$ given $\mathcal{E}_b$ satisfying the barycentre identity $\int \Pi_b(\cdot\mid e)\,\lambda_b(de)=\mu_C$ where $\lambda_b$ is the evidence marginal, and $e\mapsto\mathfrak{r}(\Pi_b(\cdot\mid e))$ is measurable and $\lambda_b$-integrable.

**Observation 3.14.1 — remediates AV-012.** Regular conditional probabilities need not exist on arbitrary measurable spaces, and integrability alone supplies neither the barycentre identity nor measurability of the random risk. These are now hypotheses of the structure, not background assumptions.

### 3.5 Representation morphisms

**Definition 3.15 (Representation morphism) — derived.** A family $\iota=(\iota_{\mathfrak{B}},\iota_{\mathfrak{M}},\iota_{\mathcal{Y}},\iota_W)$: a bijection $\iota_{\mathfrak{B}}$, bimeasurable bijections $\iota_{\mathfrak{M}}$ and $\iota_{\mathcal{Y}}$, and an isomorphism $\iota_W$ of codomains in the declared class (order, $\sigma$-algebra, and any declared algebraic operations).

**Definition 3.16 (Extended action) — derived, remediates AV-002.** $\widehat{\iota_W}:\widehat{W}\to\widehat{W'}$ acts as $\iota_W$ on $W$, as $[u,v]\mapsto[\iota_W u,\iota_W v]$ on $\mathcal{I}(W)$ (well defined since $\iota_W$ is an order isomorphism), and as the identity on each of the three bottoms.

**Definition 3.17 (Transported context) — derived.** $\iota_*C$ has components
$$\mu_{\iota_*C}=(\iota_{\mathfrak{M}})_*\mu_C,\quad M_{\iota_*C}=\iota_{\mathcal{Y}}\circ M_C\circ\iota_{\mathfrak{M}}^{-1},\quad T_{\iota_*C}(\iota_{\mathfrak{B}}b)=\iota_{\mathfrak{M}}\circ T_C(b)\circ\iota_{\mathfrak{M}}^{-1},$$
$$\approx_{\iota_*C}\ =\ \begin{cases}\bot_{\mathrm{abs}} & \approx_C=\bot_{\mathrm{abs}}\\ \{(\iota_{\mathcal{Y}}y,\iota_{\mathcal{Y}}y'):y\approx_C y'\}&\text{otherwise}\end{cases},\quad \delta_{\iota_*C}=\iota_W\circ\delta_C\circ(\iota_{\mathcal{Y}}^{-1}\times\iota_{\mathcal{Y}}^{-1}),$$
$$W_{\iota_*C}=\iota_W(W_C),\qquad \rho_{\iota_*C}=\widehat{\iota_W}\circ\rho_C\circ((\iota_W)^{-1})_*.$$
Every component of Definition 3.10 is transported.

**Observation 3.17.1.** $\iota_*C$ is a context: each transported component has the required type, and $(\iota_W^{-1})_*$ is the pushforward on probability measures, which is the only profile class remaining after Observation 3.11.1.

---

## 4. Design principles and axioms

### 4.1 Design principles — non-formal, **not usable in any proof**

**Remediates AV-005.** The following were stated as axioms A1 and A6 in the prior edition. They are not predicates over the signature: "valuation of a comparison" and "joint uncertainty" name no object or relation. They are demoted to design principles, are excluded from every proof below, and are not part of the satisfaction relation.

**DP-1.** Significance is intended as a valuation of a comparison between a factual and an operated outcome, not as a property of a bearer alone.

**DP-2.** Uncertainty is intended to be carried by a single joint measure, with marginals and conditionals derived.

**Observation 4.1.1.** No proof in this document cites DP-1 or DP-2. This is checkable by inspection: the proofs cite only A2–A5, A7–A10 and the definitions.

### 4.2 Axioms — formal predicates over the signature

**A2 (Completeness).** If any *required* component of Definition 3.10 is not supplied, no significance is defined for $C$. An optional component supplied as $\bot_{\mathrm{abs}}$ is supplied.

**A3 (Covariance).** For every representation morphism $\iota$, context $C$, and bearer $b$: $\sigma_{\iota_*C}(\iota_{\mathfrak{B}}b)=\widehat{\iota_W}(\sigma_C(b))$, an equation in $\widehat{W_{\iota_*C}}$.

**A4 (Nullity schema).** For every $b\in\mathfrak{B}$ there exists $C\in\mathcal{C}$ with $W_C$ of class $\mathsf{W}_1$ and $\sigma_C(b)=0_{W_C}$.

**A5 (Output typing).** $\sigma_C(b)\in\widehat{W_C}$, and the value is determined by Definition 5.3. No other value is admitted.

**A7 (Codomain confinement).** Values arising under $C$ lie in $\widehat{W_C}$. Values under distinct contexts are related only through a declared transport (Definition 8.9).

**A8 (Congruence).** If $\approx_C\neq\bot_{\mathrm{abs}}$, then for all $(y,y'),(\tilde y,\tilde y')\in D_C$ with $y\approx_C\tilde y$ and $y'\approx_C\tilde y'$: $\delta_C(y,y')=\delta_C(\tilde y,\tilde y')$.

**A9 (Empty-domain typing).** If $\{m:\delta^{\,b}_C \text{ defined at } m\}=\emptyset$ then $\sigma_C(b)=\bot_{\mathrm{und}}$.

**A10 (Empty-fibre typing).** If $r$ is supplied and $r^{-1}(x)=\emptyset$ then the identified output at $x$ is $\bot_{\mathrm{inc}}$.

**Observation 4.2.1.** A2, A3, A5, A7, A8, A9, A10 are each a predicate over declared carriers and functions, and A4 is an existential schema over $\mathcal{C}$. Satisfaction is therefore testable in a model. This is what makes §11 possible.

---

## 5. Contrast and significance

**Definition 5.1 (Pointwise contrast) — derived, partial.** For $\tau=T_C(b)$ defined,
$$\delta^{\,b}_C(m)=\delta_C\big(M_C(m),M_C(\tau m)\big),$$
defined exactly on $\Omega^b_C:=\{m:(M_C(m),M_C(\tau m))\in D_C\}\in\mathcal{F}$.

**Definition 5.2 (Profile) — derived, partial.** If $\mu_C(\Omega^b_C)=1$, the *profile* is $(\delta^{\,b}_C)_*\mu_C\in\Delta(W_C)$. Otherwise no profile exists.

**Definition 5.3 (Significance) — derived, partial.** Exhaustively by cases:

| Case | $\sigma_C(b)$ |
|---|---|
| $T_C(b)$ undefined | $\bot_{\mathrm{und}}$ |
| $\Omega^b_C=\emptyset$ | $\bot_{\mathrm{und}}$ (A9) |
| $0<\mu_C(\Omega^b_C)<1$ | $\bot_{\mathrm{und}}$ |
| $\mu_C(\Omega^b_C)=1$ and the profile $\notin\operatorname{dom}\rho_C$ | $\bot_{\mathrm{und}}$ |
| $\mu_C(\Omega^b_C)=1$ and the profile $\in\operatorname{dom}\rho_C$ | $\rho_C\big((\delta^{\,b}_C)_*\mu_C\big)$ |

**Observation 5.3.1 — remediates AV-004.** The prior edition left the case $0<\mu_C(\Omega^b_C)<1$ unclassified: the contrast was neither nowhere defined nor defined almost everywhere, so no listed condition applied and no profile existed. That branch is now typed.

**Theorem 1 (Order reversal exists).**
*Hypotheses.* $\mathfrak{B}=\{b_1,b_2\}$; $\mathfrak{M}=\mathbb{R}^2$ Borel; $r$ not supplied; codomain $W=(\mathbb{R}_{\ge0},+,0,\le)$ with the Borel $\sigma$-algebra, class $\mathsf{W}_1$; $\rho=\ell$ the Dirac-atom location functional of Definition 3.12; $\approx=\bot_{\mathrm{abs}}$.
*Conclusion.* There exist contexts $C_1,C_2$, agreeing in every component except $M_C$, with $\sigma_{C_1}(b_1)>\sigma_{C_1}(b_2)$ and $\sigma_{C_2}(b_1)<\sigma_{C_2}(b_2)$.
*Applies to.* Deterministic form only.

*Proof.* Take $\mu=\delta_{(0,0)}$; $\mathcal{Y}=\mathbb{R}$ Borel; $T(b_1)(x,y)=(x+2,y+1)$ and $T(b_2)(x,y)=(x+1,y+2)$, both measurable; $\delta(u,v)=|u-v|$, total and measurable, so $D_C=\mathcal{Y}^2$; $M_{C_1}(x,y)=x$, $M_{C_2}(x,y)=y$. All seven components of Definition 3.10 are supplied. Each $\Omega^{b}_C=\mathfrak{M}$, so $\mu(\Omega)=1$ and each profile is a Dirac measure, on which $\ell$ returns the atom. Then $\sigma_{C_1}(b_1)=2>1=\sigma_{C_1}(b_2)$ and $\sigma_{C_2}(b_1)=1<2=\sigma_{C_2}(b_2)$. $\blacksquare$

**Observation 1.1′ — remediates AV-007.** Theorem 1 is **existential**. It shows the framework *permits* reversal. It does **not** show that every context family reverses, and no corollary asserting a universal absence of context-free ordering follows from it. The prior edition's Corollary 1.1 made that universal claim and is withdrawn (§13).

---

## 6. Invariance

**Definition 6.1 (Context automorphism).** $\mathrm{Aut}(C)$ is the group of representation morphisms $\pi$ with $\pi_*C=C$ componentwise and $\iota_W=\mathrm{id}_{W_C}$.

**Corollary 6.2 (Orbit constancy under a fixed context).** For $\pi\in\mathrm{Aut}(C)$ and every $b$: $\sigma_C(\pi_{\mathfrak{B}}b)=\sigma_C(b)$.

*Proof.* By A3, $\sigma_{\pi_*C}(\pi_{\mathfrak{B}}b)=\widehat{\mathrm{id}}(\sigma_C(b))=\sigma_C(b)$; and $\pi_*C=C$. $\blacksquare$

**Observation 6.2.1 — remediates AV-006, AV-023.** In the prior edition this was Theorem 2, "designation necessity", and it depended on automorphisms of an "underlying structure" that was never defined. The verification established that the displayed equality is a direct instance of A3 and not a designation theorem. Accordingly: the definitions of *designation* and *filter context* are **withdrawn**, the statement is demoted to a corollary of A3, and the claim that designation is *necessary* is withdrawn (§13). What survives is exactly the conditional orbit equality above.

---

## 7. Difference theory

**Definition 7.1 (Induced $\sigma$-algebra) — remediates AV-008.** Given measurable $r:\mathfrak{M}\to\mathcal{R}$, the *final $\sigma$-algebra* on $\mathcal{R}$ is $\mathcal{H}_r:=\{A\subseteq\mathcal{R}:r^{-1}(A)\in\mathcal{F}\}$.

**Theorem 3 (Factorisation).**
*Hypotheses.* $r:\mathfrak{M}\to\mathcal{R}$ measurable; $(\mathcal{R},\mathcal{H}_r)$ carrying the final $\sigma$-algebra; $(\mathsf{V},\Sigma_{\mathsf{V}})$ **any** measurable space; $g:\mathfrak{M}\to\mathsf{V}$ measurable and total; $\mathsf{V}\neq\emptyset$.
*Conclusion.* There is a measurable total $h:\mathcal{R}\to\mathsf{V}$ with $g=h\circ r$ **iff** $g$ is constant on the fibres of $r$.
*Applies to.* All forms.

*Proof.* ($\Rightarrow$) If $g=h\circ r$ and $r(m)=r(m')$ then $g(m)=g(m')$.
($\Leftarrow$) Fix $v_0\in\mathsf{V}$. Define $h(x):=g(m)$ for $x\in r(\mathfrak{M})$ and any $m\in r^{-1}(x)$ — well defined by fibre-constancy — and $h(x):=v_0$ for $x\notin r(\mathfrak{M})$. Then $g=h\circ r$. For $B\in\Sigma_{\mathsf{V}}$, $r^{-1}(h^{-1}(B))=g^{-1}(B)\in\mathcal{F}$, so $h^{-1}(B)\in\mathcal{H}_r$ by definition of the final $\sigma$-algebra. Hence $h$ is measurable. $\blacksquare$

**Observation 3.0 — remediates AV-008.** Two defects of the prior statement are repaired: the $\sigma$-algebra on $\mathcal{R}$ is now declared (final), and $h$ is now total on $\mathcal{R}$ rather than defined only on $r(\mathfrak{M})$. The codomain hypothesis is widened to an arbitrary measurable space, which is what Corollary 3.3 requires.

**Observation 3.0.1 (Scope — exhaustive).** Theorem 3 establishes none of: quotient factorisation through any relation other than the fibres of $r$; uniqueness of $h$ off $r(\mathfrak{M})$; minimality of $r$; identifiability of anything not equal to $g$; **computability**; empirical prediction; invariance beyond Definition 3.15.

**Corollary 3.3 (Induced outcome map).** Let $\tau=T_C(b)$. A total measurable $\phi:\mathcal{Y}_C\to\mathcal{Y}_C$ with $M_C\circ\tau=\phi\circ M_C$ exists **iff** $M_C\circ\tau$ is constant on the fibres of $M_C$, where $\mathcal{Y}_C$ carries the final $\sigma$-algebra of $M_C$.

*Proof.* Theorem 3 with $r:=M_C$, $g:=M_C\circ\tau$, $\mathsf{V}:=\mathcal{Y}_C$. $\blacksquare$

**Observation 3.4 (No deterministic induced map in general).** Where the condition fails, only the relation $\{(M_C(m),M_C(\tau m)):m\in\mathfrak{M}\}$ is available without further hypotheses; a kernel representation additionally requires a disintegration of $\mu_C$ along $M_C$, which is not assumed.

**Definition 7.4 (Two separate conditions) — remediates AV-010.** Say $r$ is
- **total for $(C,b)$** if $\Omega^b_C=\mathfrak{M}$;
- **fibre-constant for $(C,b)$** if $\delta^{\,b}_C$ is constant on $r^{-1}(x)\cap\Omega^b_C$ for every $x$;
- **$C$-sufficient for $b$** if both hold.

**Definition 7.5 (Identified output).** For $x\in\mathcal{R}$: if $r^{-1}(x)=\emptyset$, the output is $\bot_{\mathrm{inc}}$ (A10); else if $r^{-1}(x)\cap\Omega^b_C=\emptyset$, it is $\bot_{\mathrm{und}}$; else it is the set $\mathcal{S}_C(b,x)=\{\delta^{\,b}_C(m):m\in r^{-1}(x)\cap\Omega^b_C\}$.

**Theorem 3.2′ (Non-constancy forces a non-singleton identified set).**
*Hypotheses.* $r$ total for $(C,b)$ but not fibre-constant.
*Conclusion.* There is $x$ with $r^{-1}(x)\neq\emptyset$ and $|\mathcal{S}_C(b,x)|\ge2$; and no total measurable $h$ with $\delta^{\,b}_C=h\circ r$ exists.
*Applies to.* All forms.

*Proof.* Failure of fibre-constancy under totality gives $x$ and $m,m'\in r^{-1}(x)$ with $\delta^{\,b}_C(m)\neq\delta^{\,b}_C(m')$, so $|\mathcal{S}_C(b,x)|\ge2$. Theorem 3 then denies a factorisation. $\blacksquare$

**Observation 3.2.1 — remediates AV-010.** The prior Corollary 3.2 asserted this conclusion for **every** non-sufficient $r$. That is false: non-sufficiency also arises from failure of totality alone, and then every fibre may still carry at most one value. The verification's counterexample ($\mathfrak{M}=\{0,1\}$, $r=\mathrm{id}$, $\delta_C$ defined only at $(1,1)$) is decisive. The prior corollary is **withdrawn**; Theorem 3.2′ is its correct totality-restricted replacement, and the failure-of-totality branch yields $\bot_{\mathrm{und}}$ by Definition 5.3 rather than a set of two values.

**Observation 3.1.1 — remediates AV-009.** The prior Corollary 3.1 concluded that the contrast is **computable** from the representation iff $r$ is sufficient. That is false and is a category error: measurable factorisation is not an algorithm. Taking $\mathfrak{M}=\mathcal{R}=\mathbb{N}$ discrete, $r=\mathrm{id}$, and $\delta^{\,b}_C=\mathbb{1}_A$ for non-computable $A$ gives a sufficient $r$ with no algorithm. The corollary is **withdrawn**. The correct statement is Theorem 3: the contrast is a measurable function of the representation iff it is fibre-constant. No computability claim is made anywhere in this document.

**Definition 7.7 (Four distinct notions).** (i) sufficiency, Definition 7.4; (ii) minimal sufficiency relative to $\delta^{\,b}_C$, namely sufficiency together with factorisation through every sufficient map; (iii) the distinguishability indicator $\mathbb{1}[\delta^{\,b}_C(m)\neq\delta^{\,b}_C(m')]$ on $\Omega^b_C\times\Omega^b_C$; (iv) the partition of $\Omega^b_C$ induced by equality of $\delta^{\,b}_C$.

**Observation 7.8.** Only (i) is asserted where hypothesised. **No minimality is claimed anywhere.**

**Theorem 4′ (Partial quotient descent) — replaces the withdrawn Theorem 4.**
*Hypotheses.* $\approx_C\neq\bot_{\mathrm{abs}}$; A8; $D_C$ the domain of $\delta_C$; $p:\mathcal{Y}_C\to\mathcal{Y}_C/\!\approx_C$ the projection; $\bar D_C:=(p\times p)(D_C)$.
*Conclusion.* There is a unique **partial** map $\bar\delta_C$ with domain exactly $\bar D_C$ such that $\bar\delta_C\big((p\times p)(y,y')\big)=\delta_C(y,y')$ for every $(y,y')\in D_C$. Its pullback $\bar\delta_C\circ(p\times p)$ has domain $(p\times p)^{-1}(\bar D_C)\supseteq D_C$, and equals $\delta_C$ on $D_C$; the inclusion is strict unless $D_C$ is saturated under $\approx_C\times\approx_C$.
*Applies to.* All forms with $\approx_C$ supplied.

*Proof.* Existence and well-definedness on $\bar D_C$: if $(p\times p)(y,y')=(p\times p)(\tilde y,\tilde y')$ with both pairs in $D_C$, then $y\approx_C\tilde y$ and $y'\approx_C\tilde y'$, so A8 gives equal values. Uniqueness on $\bar D_C$: every point of $\bar D_C$ has a defined representative pair, on which the value is forced. The pullback statement is immediate, and strictness fails exactly when $D_C$ is a union of $\approx_C\times\approx_C$-classes. $\blacksquare$

**Observation 4.0 — remediates AV-011.** The prior Theorem 4 declared neither totality nor a quotient domain. Under a total reading uniqueness is false — with $\approx_C$ equality, $\mathcal{Y}=\{0,1\}$ and $\delta_C$ defined only at $(0,0)$, any total map may take arbitrary values on the other three quotient pairs. Under a partial reading it omitted the saturation condition, so the pullback need not return $D_C$. Theorem 4′ fixes the domain as $\bar D_C$, states uniqueness only there, and states the pullback relation exactly. The prior theorem is **withdrawn**.

---

## 8. Significance forms

**Assumption 8.0 (Standing hypotheses for §8).** $M_C$, every $\tau=T_C(b)$, and $\delta_C$ on $D_C$ are measurable; $W_C$ carries $\Sigma_{W_C}$; every expectation written exists and is finite; every evidence structure invoked is regular in the sense of Definition 3.14. Statements in §8 are asserted only under Assumption 8.0.

**Observation 8.0.1.** Every integral below is over $\mathbb{R}$. No integration into a general partial order occurs, and the theory supplies none.

**Definition 8.1 (Effect significance) — class $\mathsf{W}_1$.** $(\mathcal{Y}_C,d_Y)$ metric with Borel $\sigma$-algebra, $W_C=(\mathbb{R}_{\ge0},+,0,\le)$, $\delta_C=d_Y$, $\rho_C=\ell$ a location functional (Definition 3.12).

**Definition 8.2 (Decision significance) — class $\mathsf{W}_2$ realised in $\mathbb{R}$.** With $\mathfrak{r}(\nu):=\inf_{\alpha\in\mathcal{A}_C}\mathbb{E}_\nu L_C(\alpha,\cdot)$ finite and $\mathcal{A}^*_\varepsilon(\nu):=\{\alpha:\mathbb{E}_\nu L_C(\alpha,\cdot)\le\mathfrak{r}(\nu)+\varepsilon\}$, for a **declared** $\varepsilon\ge0$:
$$\sigma^{\mathrm{dec}}_C(b)=\inf\big\{\mathbb{E}_{\mu_C}L_C(\alpha,\cdot):\alpha\in\mathcal{A}^*_\varepsilon(\tau_*\mu_C)\big\}-\mathfrak{r}(\mu_C),$$
with the value $\bot_{\mathrm{und}}$ if $\varepsilon=0$ and the infimum defining $\mathfrak{r}(\tau_*\mu_C)$ is unattained.

**Definition 8.4 (Information significance) — class $\mathsf{W}_2$ realised in $\mathbb{R}$, requires Definition 3.14.**
$$\sigma^{\mathrm{inf}}_C(b)=\mathfrak{r}(\mu_C)-\int \mathfrak{r}\big(\Pi_b(\cdot\mid e)\big)\,\lambda_b(de).$$

**Theorem 5 (Non-negativity).**
*Hypotheses.* Assumption 8.0. (i) Definition 8.1. (ii) Definition 8.2 with $\varepsilon>0$, or $\varepsilon=0$ with attainment. (iii) Definition 8.4 with a regular evidence structure.
*Conclusion.* (i) $\sigma^{\mathrm{eff}}_C(b)\ge0$; (ii) $\sigma^{\mathrm{dec}}_C(b)\ge0$; (iii) $\sigma^{\mathrm{inf}}_C(b)\ge0$.

*Proof.* (i) $d_Y\ge0$, so the profile is supported in $\mathbb{R}_{\ge0}$; by Definition 3.12, $\ell(\nu)\ge\inf\operatorname{supp}\nu\ge0$.
(ii) For every $\alpha\in\mathcal{A}_C$, $\mathbb{E}_{\mu_C}L_C(\alpha,\cdot)\ge\mathfrak{r}(\mu_C)$. Since $\mathcal{A}^*_\varepsilon(\tau_*\mu_C)\subseteq\mathcal{A}_C$, the infimum over that subset is $\ge\mathfrak{r}(\mu_C)$. No attainment is used.
(iii) $\nu\mapsto\mathbb{E}_\nu L_C(\alpha,\cdot)$ is affine, so $\mathfrak{r}$ is an infimum of affine functionals and hence concave. Definition 3.14 supplies measurability and integrability of $e\mapsto\mathfrak{r}(\Pi_b(\cdot\mid e))$ and the barycentre identity $\int\Pi_b(\cdot\mid e)\lambda_b(de)=\mu_C$. Jensen's inequality for concave functionals gives $\int\mathfrak{r}(\Pi_b(\cdot\mid e))\lambda_b(de)\le\mathfrak{r}(\mu_C)$. $\blacksquare$

**Observation 5.0 — remediates AV-012.** Part (iii) is asserted only for a **regular** evidence structure. It is not a theorem over arbitrary measurable spaces.

**Theorem 6 (Pairwise non-equivalence).**
*Hypotheses.* Assumption 8.0; $\varepsilon=0$ with attainment throughout; $\rho_C=\ell$ with $\ell(\nu)=\int x\,\nu(dx)$ (the mean, a location functional by Definition 3.12); the three complete contexts displayed below.
*Conclusion.* For each pair of forms there are two bearers whose orderings under that pair disagree.

*Proof.* Throughout: $\mathfrak{M}=\mathbb{R}^2$ Borel, $r$ not supplied, $\approx=\bot_{\mathrm{abs}}$, $\mathcal{Y}=\mathbb{R}^2$ Borel, $M=\mathrm{id}$, $\mathcal{A}=\mathbb{R}$.

(i) *Effect against decision.* $\mu=\delta_{(0,0)}$; $L(\alpha,(x,y))=(\alpha-x)^2$, whose infimum is attained at $\mathbb{E}[x]$; $T(b_1)(x,y)=(x,y+10)$, $T(b_2)(x,y)=(x+1,y)$; $\delta=d_Y$ Euclidean. Profiles are Dirac, so $\ell$ returns the atom: $\sigma^{\mathrm{eff}}(b_1)=10>1=\sigma^{\mathrm{eff}}(b_2)$. For decision: $\tau_1$ fixes the $x$-marginal, so $\mathcal{A}^*_0(\tau_{1*}\mu)=\{0\}=\mathcal{A}^*_0(\mu)$ and $\sigma^{\mathrm{dec}}(b_1)=0$; $\mathcal{A}^*_0(\tau_{2*}\mu)=\{1\}$, so $\sigma^{\mathrm{dec}}(b_2)=\mathbb{E}_\mu(1-x)^2-\mathbb{E}_\mu(0-x)^2=1>0$.

(ii) *Decision against information.* Coordinates $(\theta_1,\theta_2)$ independent, $\theta_1\equiv0$, $\theta_2\sim\mathcal{N}(0,s^2)$, $s^2>0$; $L(\alpha,\theta)=(\alpha-\theta_1-\theta_2)^2$, so $\mathfrak{r}(\nu)=\operatorname{Var}_\nu[\theta_1+\theta_2]$, attained. For $b_1$: $\theta_1$ degenerate, so any $K_{b_1}$ concerning $\theta_1$ has $\Pi_{b_1}(\cdot\mid e)=\mu$ $\lambda$-a.s., giving $\sigma^{\mathrm{inf}}(b_1)=0$; $T(b_1)$ shifts $\theta_1$ by $1$, moving the optimum from $0$ to $1$, giving $\sigma^{\mathrm{dec}}(b_1)=1>0$. For $b_2$: $T(b_2)$ replaces $\theta_2$ by $0$, preserving $\mathbb{E}[\theta_1+\theta_2]=0$, so the optimum is unchanged and $\sigma^{\mathrm{dec}}(b_2)=0$; $K_{b_2}$ revealing $\theta_2$ exactly is a regular structure with $\int\mathfrak{r}\,d\lambda=0$, giving $\sigma^{\mathrm{inf}}(b_2)=s^2>0$.

(iii) *Effect against information.* Retain (ii) with $\delta=d_Y$ Euclidean and $\ell$ the mean. $\sigma^{\mathrm{eff}}(b_1)=1$ and $\sigma^{\mathrm{inf}}(b_1)=0$. For $b_2$ the contrast is $|\theta_2|$, so $\sigma^{\mathrm{eff}}(b_2)=\mathbb{E}|\theta_2|=s\sqrt{2/\pi}$, which is $<1$ for $s<\sqrt{\pi/2}$; and $\sigma^{\mathrm{inf}}(b_2)=s^2>0$. $\blacksquare$

**Observation 6.0 — remediates AV-013.** The prior proof declared neither $\rho_C$ nor $\varepsilon$ and left the part (iii) magnitude unspecified. All three are now fixed: $\ell$ is the mean, $\varepsilon=0$ with attainment, and part (iii) computes $\mathbb{E}|\theta_2|=s\sqrt{2/\pi}$ exactly, with the range of $s$ stated.

**Observation 6.1′ — remediates AV-013.** The prior Corollary 6.1 ("not measurements of one latent quantity") relied on an undefined notion of latent quantity. It is **withdrawn**. What is proved is exactly Theorem 6: the three orderings disagree on the exhibited contexts. Any claim that they cannot share a common latent order requires a formal hypothesis about admissible measurement maps that this theory does not supply.

**Theorem 7′ (Additive context-free scalar under a nullity-closed family) — replaces the withdrawn Theorem 7.**
*Hypotheses.* $W=(\mathbb{R}_{\ge0},+,0,\le)$; $S:\mathfrak{B}\to\mathbb{R}_{\ge0}$; $\beta>0$; a family $\mathcal{K}\subseteq\mathcal{C}$ such that (a) for every $b$ there is $C\in\mathcal{K}$ with $\sigma_C(b)=0$, and (b) for every $C\in\mathcal{K}$ there is $g_C:\mathfrak{B}\to\mathbb{R}_{\ge0}$ with $\sigma_C(b)=\beta S(b)+g_C(b)$ for all $b$.
*Conclusion.* $S\equiv0$.

*Proof.* Fix $b$. By (a) choose $C\in\mathcal{K}$ with $\sigma_C(b)=0$. By (b), $\beta S(b)+g_C(b)=0$ with both summands $\ge0$ and $\beta>0$, so $S(b)=0$. $\blacksquare$

**Observation 7.0 — remediates AV-014.** The prior Theorem 7 assumed the decomposition only on "the family considered" while drawing the nullity witness from the global $\mathcal{C}$. The verification's countermodel is decisive: with $\mathfrak{B}=\{b\}$, $\mathcal{C}=\{C_0,C_1\}$, family $\{C_1\}$, $\sigma_{C_0}(b)=0$, $S(b)=1$, $\beta=1$, $g_{C_1}(b)=0$, $\sigma_{C_1}(b)=1$, every hypothesis held and the conclusion failed. The prior theorem is **withdrawn**. Theorem 7′ adds hypothesis (a), which is exactly what the prior proof silently used.

**Observation 7.1′.** Non-negativity of $g_C$ remains essential: dropping it, $g'_C:=\beta S+g_C$ gives $\sigma_C=g'_C$ with no $S$ term, so the decomposition is absorbable and carries no content.

**Theorem 8 (Conditional information redundancy).**
*Hypotheses.* $Z$, $R$ random elements on a common space; $S=f(R)$ with $f$ measurable; all mutual informations defined.
*Conclusion.* $I(Z;S,R)=I(Z;R)$ and $I(Z;S\mid R)=0$.

*Proof.* $\sigma(S)\subseteq\sigma(R)$ gives $\sigma(S,R)=\sigma(R)$; mutual information depends on the joint law only through the generated $\sigma$-algebras. The chain rule gives the second identity. $\blacksquare$

**Observation 8.1′ — remediates AV-015.** The prior Corollary 8.1 concluded that a derived quantity "cannot be justified epistemically". That does not follow and is false: with $Z=R=S$ a non-degenerate Bernoulli variable, $I(Z;S\mid R)=0$ while $I(Z;S)=H(Z)>0$, so $S$ is informative to an observer without $R$. The corollary is **withdrawn**. What Theorem 8 supports is exactly: *a derived summary adds no information **to an observer who already has $R$***.

**Theorem 9 (Arena dependence of normalisation).**
*Hypotheses.* $A\subsetneq A'$ finite nonempty, $\varphi:A'\to\mathbb{R}_{>0}$, $\max_{A'}\varphi>\max_A\varphi$; $\nu^A(b)=\varphi(b)/\max_A\varphi$.
*Conclusion.* $\nu^{A'}(b)<\nu^{A}(b)$ for every $b\in A$, and both induce the same order on $A$.

*Proof.* With $\mathsf{m}=\max_A\varphi<\mathsf{m}'=\max_{A'}\varphi$ and $\varphi(b)>0$: $\varphi(b)/\mathsf{m}'<\varphi(b)/\mathsf{m}$. Both are positive multiples of $\varphi$ on $A$. $\blacksquare$

**Observation 9.1′ — remediates AV-016.** The prior Corollaries 9.1 and 9.2 concluded that normalised values are *incomparable* across arenas and *cannot be calibrated*. Neither follows. If the denominators are known the original values are recoverable; and for a declared dimensioned constant $D$, $x\mapsto Dx$ calibrates a dimensionless value. Both corollaries are **withdrawn**. What Theorem 9 supports is exactly: *a normalised value depends on its arena's maximum, so comparing normalised values across arenas without also declaring the denominators is uninformative about $\varphi$.*

**Definition 8.9 (Cross-context transport) — optional.** A declared order-embedding $t:W_C\to W_{C'}$ with the extended action $\widehat t$ of Definition 3.16. Comparison of values under distinct contexts is defined relative to a declared $t$ and is otherwise undefined by A7.

---

## 9. Encodability

**Theorem 10′ (Bounded encodability) — replaces the withdrawn Theorem 10 statement and proof.**
*Hypotheses.* $\mathfrak{B}$ any set; $(W,\preceq_W,\Sigma_W)$ any codomain with at least one element; $f:\mathfrak{B}\to W$ any function; a single context is to be constructed; the deterministic contrast form of Definition 5.1 with $\rho$ the Dirac-atom reduction.
*Conclusion.* There is a context $C$ with $W_C=W$ and $\sigma_C(b)=f(b)$ for every $b\in\mathfrak{B}$.
*Applies to.* The **deterministic contrast form only**, with a projection evaluator. **Not** to effect, decision, information, or composition forms.

*Proof.* Take $\mathfrak{M}:=W$ with $\Sigma_W$; $\mathcal{Y}_C:=W$ with $\Sigma_W$; $M_C:=\mathrm{id}_W$; $\mu_C:=$ any probability measure on $(W,\Sigma_W)$, for instance a Dirac measure at a chosen point; $\approx_C:=\bot_{\mathrm{abs}}$; $\delta_C(y,y'):=y'$, the second projection, which is total and $\Sigma_W\otimes\Sigma_W/\Sigma_W$-measurable **without any group structure**; $T_C(b):=$ the constant map $m\mapsto f(b)$, measurable; $\rho_C:=$ the partial map returning the atom of a Dirac profile. Then $\delta^{\,b}_C(m)=\delta_C(M_C(m),M_C(T_C(b)m))=f(b)$ for every $m$, so $\Omega^b_C=\mathfrak{M}$, the profile is $\delta_{f(b)}$, and $\sigma_C(b)=f(b)$. $\blacksquare$

**Observation 10.0 — remediates AV-017.** The prior proof used $\delta(y,y')=y'-y$ on a class $\mathsf{W}_2$ codomain. Class $\mathsf{W}_2$ does not make subtraction measurable (Observation 3.6), so the constructed $\delta_C$ need not satisfy Definition 3.10 and the published proof was **invalid**. Theorem 10′ uses the second projection instead, which is measurable on any measurable space, and consequently needs no algebraic hypothesis at all — the result is both repaired and freed from the $\mathsf{W}_2$ restriction.

**Observation 10.0.1 (The witness evaluator is degenerate).** $\delta_C(y,y')=y'$ ignores the factual outcome entirely. Theorem 10′ therefore states: *the axioms as given do not exclude degenerate evaluators, and admitting them makes every assignment realisable in the deterministic form.* This locates precisely where a restriction would bite — on the admissible class of evaluators — and it is the honest content of the result.

**Corollary 10.1′ (Bounded underdetermination) — replaces the withdrawn Corollary 10.1.** Within the deterministic contrast form with unrestricted evaluators, no single-context assignment of values to bearers is excluded by the axioms.

*Proof.* Immediate from Theorem 10′. $\blacksquare$

**Observation 10.1.1 — remediates AV-018. This is the most important withdrawal in the document.** The prior Corollary 10.1 asserted that the **unrestricted framework has no empirical content whatever** and that it forbids no observation. That does **not** follow, and the prior edition rested its principal epistemic claim on it. The verification is decisive on three counts:

1. Theorem 10′ constructs only a deterministic contrast valuation. It does not construct an effect, decision, information, or composition form.
2. Those forms **are** constrained: Theorem 5 forces $\sigma^{\mathrm{eff}}$, $\sigma^{\mathrm{dec}}$ and $\sigma^{\mathrm{inf}}$ to be non-negative under its hypotheses, so an assignment of $-1$ as effect significance is excluded outright.
3. Theorem 10′ concerns a **single** context. Joint assignments across contexts are additionally constrained by A3, A4 and A7.

Accordingly the "no empirical content" conclusion is **withdrawn**, and with it the prior Limitation 14.9 and Rejection 16.14. What survives is Corollary 10.1′: a bounded, single-context, deterministic-form underdetermination statement. **No conclusion about the empirical content of the whole framework is drawn anywhere in this document.**

**Observation 10.2′ — remediates AV-018.** The prior Corollary 10.2 asserted that empirical content can arise *only* by constraining four named components. That exhaustiveness claim is unproved and is **withdrawn**: restrictions on codomains, evaluator classes, priors, cross-context relations, or morphisms can each exclude assignments.

---

## 10. Composition

**Definition 10.1 (Composition signature) — primitive, remediates AV-019.** A tuple $(U,E,\mathrm{src},\mathrm{tgt},t,\kappa,\odot,w)$: $U$ a set of nodes; $E$ a set of *instances*; $\mathrm{src},\mathrm{tgt}:E\to U$; $t:E\to T$ a type map; $\kappa\subseteq\{(e,f)\in E\times E:\mathrm{tgt}(e)=\mathrm{src}(f)\}$; $\odot:\kappa\to E$ a **primitive** total map on $\kappa$ with $\mathrm{src}(e\odot f)=\mathrm{src}(e)$ and $\mathrm{tgt}(e\odot f)=\mathrm{tgt}(f)$; $w:E\to\mathbb{R}_{\ge0}$.

**Observation 10.1.1 — remediates AV-019.** The prior edition never defined $E$, gave instances no endpoints, and attempted to *derive* $\odot$ from $\kappa$ — which is impossible, since many operations share a domain. $\odot$ is now primitive and endpoint-coherent.

**Definition 10.2 (Path).** A nonempty finite sequence $p=(e_1,\dots,e_k)$, $k\ge1$, with $\mathrm{tgt}(e_i)=\mathrm{src}(e_{i+1})$. Empty paths are not admitted.

**Definition 10.3 (Semantics).** $[\![p]\!]_{\mathrm{comp}}$ under a **declared bracketing** is the iterated $\odot$-value, or $\bot_{\mathrm{und}}$ if any required pair lies outside $\kappa$. $[\![p]\!]_{\mathrm{diff}}:=\prod_{i=1}^k w(e_i)$, always defined.

**Theorem 11 (Type-level licensing dichotomy).**
*Hypotheses.* Definition 10.1; there exist $e_1,e_2,e_1',e_2'\in E$ with $t(e_1)=t(e_1')$, $t(e_2)=t(e_2')$, $(e_1,e_2)\in\kappa$, $(e_1',e_2')\notin\kappa$.
*Conclusion.* Every predicate on $T\times T$ is, as a test for membership in $\kappa$, unsound or incomplete.

*Proof.* Such a predicate takes one value on both type-pairs. *Admit* admits $(e_1',e_2')\notin\kappa$; *refuse* refuses $(e_1,e_2)\in\kappa$. $\blacksquare$

**Observation 11.0 — remediates AV-027.** Theorem 11 is conditional on its hypothesis. If $\kappa$ **is** exactly type-determined, a type-level predicate is sound and complete. Any unqualified rejection of type-level licensing is therefore unsupported.

**Theorem 12′ (An instance-level non-associative composition exists) — replaces the withdrawn Theorem 12.**
*Conclusion.* There is a composition signature and a path $(e_1,e_2,e_3)$ with $(e_1\odot e_2)\odot e_3$ undefined and $e_1\odot(e_2\odot e_3)$ defined.

*Proof.* Let $U=\{u_0,u_1,u_2,u_3\}$ and $E=\{e_1,e_2,e_3,a,q\}$ with
$\mathrm{src}/\mathrm{tgt}$: $e_1:u_0\!\to\!u_1$, $e_2:u_1\!\to\!u_2$, $e_3:u_2\!\to\!u_3$, $a:u_0\!\to\!u_2$, $q:u_1\!\to\!u_3$.
Types: $t(e_1)=P$, $t(e_2)=t(e_3)=t(q)=Q$, $t(a)=R$.
Let $\kappa=\{(e_1,e_2),(e_2,e_3),(e_1,q)\}$ — each pair endpoint-compatible — and define $\odot$ on $\kappa$ by $e_1\odot e_2:=a$, $e_2\odot e_3:=q$, $e_1\odot q:=a$. Endpoint coherence holds in each case.
Then $(e_1\odot e_2)\odot e_3=a\odot e_3$, and $(a,e_3)\notin\kappa$, so it is undefined. And $e_1\odot(e_2\odot e_3)=e_1\odot q=a$, defined. $\blacksquare$

**Observation 12.0 — remediates AV-020.** The prior Theorem 12 gave only a table on the type set $T$ and never constructed instances, intermediate results, or an instance-level operation; its hypothesis was the circular phrase "a composition table as constructed". Theorem 12′ exhibits the instances, the endpoints, and $\odot$ explicitly.

**Observation 12.1′ — remediates AV-020.** The prior Corollaries 12.2 and 12.3 are **withdrawn**. 12.2 converted an existential into the universal claim that *a path does not determine its composite*, which is false: for any one-edge path, and for any associative $\odot$, the path does determine it. 12.3 invoked "substructure" and "licensed path", neither defined. What is proved is exactly Theorem 12′: **some** path has bracketing-dependent definedness, so a bracketing must be declared **for those signatures in which $\odot$ is non-associative**.

**Theorem 13′ (Diffusion and composition can disagree).**
*Conclusion.* There is a finite composition signature with nodes $a,b,z$ such that the total diffusion weight from $a$ to $z$ strictly exceeds that from $b$ to $z$, while every $a\to z$ path has $[\![\cdot]\!]_{\mathrm{comp}}=\bot_{\mathrm{und}}$ and some $b\to z$ path does not.

*Proof.* $U=\{a,b,c,c',z\}$; $E=\{e_1:a\!\to\!c,\ e_2:c\!\to\!z,\ f_1:b\!\to\!c',\ f_2:c'\!\to\!z,\ g:b\!\to\!z\}$. By inspection of the endpoint maps, the only path from $a$ to $z$ is $(e_1,e_2)$ and the only paths from $b$ to $z$ are $(f_1,f_2)$ and $(g)$; the path sets are finite, so the sums are finite. Set $w(e_1)=w(e_2)=1$, $w(f_1)=w(f_2)=1/10$, $w(g)=0$. Then the $a$-sum is $1$ and the $b$-sum is $1/100$. Set $\kappa=\{(f_1,f_2)\}$ with $f_1\odot f_2:=g$, endpoint-coherent. Then $(e_1,e_2)\notin\kappa$ so $[\![(e_1,e_2)]\!]_{\mathrm{comp}}=\bot_{\mathrm{und}}$, while $[\![(f_1,f_2)]\!]_{\mathrm{comp}}=g$. $\blacksquare$

**Observation 13.0 — remediates AV-021.** The prior proof used endpoints absent from its definitions, asserted without a graph that exactly two paths existed, and left the composition output unspecified. All three are supplied, and finiteness of the path sets is established by inspection rather than assumed.

**Observation 13.1′ (What this does and does not show).** $[\![\cdot]\!]_{\mathrm{diff}}$ is total on any signature, whatever the transitivity of the underlying relations. Theorem 13′ shows the two semantics are independent on the exhibited signature. It does **not** show that path functionals are invalid under non-transitivity — that claim is false and is rejected in §16.

**Observation 10.4′ — remediates AV-022. The recognisability subsection is withdrawn in full.** The prior edition asserted that licensed paths form a guarded register automaton on $U\times Q\times S$, that finite $S$ yields a finite-state product with decidable recognition and exactly $|U||Q||S|$ states, and that the machinery is subsumed by existing formalisms. $U$, $Q$, registers, guards and the reduction from $\kappa$ were all undefined; no finiteness hypothesis was placed on $U$ or $Q$, so finite $S$ does not give a finite product; decidability needs an effective presentation, not a finite carrier; the state count is an upper bound before reachability; and an arbitrary $\kappa$ can encode a non-computable membership relation. **All of it is withdrawn**, together with the prior Limitation 14.10 and the negative closure of Open Question 15.6. The narrower disclaimer — *no novelty is claimed* — is retained, since it requires no proof of universal subsumption.

---

## 11. Consistency

**Proposition 11.1 (Consistency of the deterministic fragment).** The axioms A2, A3, A4, A5, A7, A8, A9, A10, restricted to the fragment comprising Definitions 3.1–3.12 and 3.15–3.17 with a class $\mathsf{W}_1$ codomain, the deterministic contrast form, and no decision, evidence, or composition structure, are jointly satisfiable.

*Proof.* Exhibit the model $\mathcal{W}$.

*Carriers.* $\mathfrak{B}=\{b_1,b_2\}$. $\mathfrak{M}=\mathbb{R}^2$ with the Borel $\sigma$-algebra. $r:=\mathrm{id}_{\mathfrak{M}}$, so $\mathcal{R}=\mathfrak{M}$ with $\mathcal{H}_r=\mathcal{F}$. $W=(\mathbb{R}_{\ge0},+,0,\le)$ with the Borel $\sigma$-algebra, class $\mathsf{W}_1$.

*Morphism universe.* $\mathcal{G}:=\{\mathrm{id},\jmath\}$ where $\jmath$ is the representation morphism with $\jmath_{\mathfrak{B}}$ the transposition $b_1\leftrightarrow b_2$, $\jmath_{\mathfrak{M}}(x,y)=(y,x)$, $\jmath_{\mathcal{Y}}=\mathrm{id}_{\mathbb{R}}$, $\jmath_W=\mathrm{id}_W$. $\mathcal{G}$ is a group of order two, since $\jmath\circ\jmath=\mathrm{id}$.

*Contexts.* All share $\mathcal{Y}=\mathbb{R}$ Borel, $\approx=\bot_{\mathrm{abs}}$, $\delta(u,v)=|u-v|$ total, $W$ as above, $\rho=$ the Dirac-atom reduction.
$C_1$: $\mu=\delta_{(0,0)}$, $M(x,y)=x$, $T(b_1)(x,y)=(x+2,y+1)$, $T(b_2)(x,y)=(x+1,y+2)$.
$C_2:=\jmath_*C_1$, computed from Definition 3.17: $\mu=\delta_{(0,0)}$, $M(x,y)=y$, $T(b_2)(x,y)=(x+1,y+2)$, $T(b_1)(x,y)=(x+2,y+1)$ with the bearer labels exchanged.
$C_0$: $\mu=\delta_{(0,0)}$, $M(x,y)=x$, $T(b_1)=T(b_2)=\big((x,y)\mapsto(x,y+1)\big)$.
Take $\mathcal{C}:=\{C_1,C_2,C_0\}$. This set is **closed under $\mathcal{G}$**: $\jmath_*C_1=C_2$, $\jmath_*C_2=C_1$ since $\jmath$ is an involution, and $\jmath_*C_0=C_0$ because $C_0$ is symmetric in the two bearers and its outcome map composed with $\jmath_{\mathfrak{M}}$ returns $C_0$'s own form under the relabelling. Every $\iota_*C$ for $\iota\in\mathcal{G}$, $C\in\mathcal{C}$ is therefore an element of $\mathcal{C}$.

*Satisfaction.*
**A2** — each context supplies all seven components; $\approx=\bot_{\mathrm{abs}}$ is a supplied optional value.
**A3** — quantified over $\mathcal{G}$, which is the model's declared universe of morphisms. For $\iota=\mathrm{id}$ the equation is trivial. For $\iota=\jmath$: $\sigma_{\jmath_*C_1}(\jmath_{\mathfrak{B}}b_1)=\sigma_{C_2}(b_2)$. Computing directly, $C_2$ has outcome map $y$ and assigns $b_2$ the operation $(x,y)\mapsto(x+2,y+1)$, giving contrast $|{(0+1)}-0|=1$; and $\sigma_{C_1}(b_1)=2$. These differ, so the check is **not** vacuous — and it fails unless the transported context is computed correctly. Recomputing $\jmath_*C_1$ strictly by Definition 3.17: $M_{\jmath_*C_1}=\jmath_{\mathcal{Y}}\circ M_{C_1}\circ\jmath_{\mathfrak{M}}^{-1}$, and $M_{C_1}(\jmath^{-1}_{\mathfrak{M}}(x,y))=M_{C_1}(y,x)=y$; and $T_{\jmath_*C_1}(\jmath_{\mathfrak{B}}b_1)=T_{\jmath_*C_1}(b_2)=\jmath_{\mathfrak{M}}\circ T_{C_1}(b_1)\circ\jmath_{\mathfrak{M}}^{-1}$, which sends $(x,y)\mapsto(y,x)\mapsto(y+2,x+1)\mapsto(x+1,y+2)$. Its contrast under outcome map $y$ is $|(0+2)-0|=2=\sigma_{C_1}(b_1)$, and $\widehat{\jmath_W}=\mathrm{id}$. So A3 holds for this pair, and symmetrically for $b_2$ and for $C_0$. **A3 is verified over a nontrivial morphism on a context set closed under transport.**
**A4** — $C_0$ gives contrast $|x-x|=0$ for both bearers, so $\sigma_{C_0}(b_i)=0_W$.
**A5** — every value computed above lies in $W\subseteq\widehat W$, assigned by Definition 5.3.
**A7** — all values lie in $\widehat W$; no cross-context comparison is performed.
**A8** — vacuous: $\approx=\bot_{\mathrm{abs}}$ in every context.
**A9** — every $\Omega^b_C=\mathfrak{M}\neq\emptyset$.
**A10** — $r=\mathrm{id}$, so every fibre is a singleton and no fibre is empty. $\blacksquare$

**Observation 11.1.1 — remediates AV-024.** The prior Proposition 12.1 failed for four reasons, each now addressed: the missing $\mathfrak{A}_C$ component (deleted from the signature, Observation 3.10.1); the unstated outcome $\sigma$-algebra (now Borel on $\mathbb{R}$); A3 checked only for the identity, which is vacuous (now checked for a **nontrivial involution** with the computation shown); and a context set not shown closed under transport (now proved closed under the declared group $\mathcal{G}$).

**Observation 11.1.2 (Scope of the witness — binding) — remediates AV-025.** Proposition 11.1 establishes consistency **only** for the named deterministic fragment, and A3 only over the finite morphism universe $\mathcal{G}$. It does **not** establish consistency for: codomain classes $\mathsf{W}_2$ and $\mathsf{W}_2^{\mathrm{m}}$; interval or bottom-valued outputs; non-trivial $\approx_C$ with a non-degenerate congruence requirement; decision structure; evidence structure; non-atomic measures; the composition signature of §10; or A3 over the class of *all* representation morphisms. Consistency beyond this fragment is **open obligation OB-1**, and it remains **blocking** for any consistency claim beyond the fragment.

---

## 12. Verified results

| № | Statement | Form | § |
|---|---|---|---|
| 1 | Order reversal **exists** between two contexts | deterministic | 5 |
| 3 | Measurable factorisation holds iff fibre-constant (final $\sigma$-algebra, total $h$) | all | 7 |
| 3.2′ | Under totality, non-fibre-constancy forces a non-singleton identified set | all | 7 |
| 3.3 | Induced outcome map exists iff fibre-constant | all | 7 |
| 4′ | Partial quotient descent on $\bar D_C$, with the pullback relation stated | with $\approx_C$ | 7 |
| 5 | Non-negativity of the three forms under stated hypotheses | eff./dec./inf. | 8 |
| 6 | The three forms disagree in order on exhibited contexts | eff./dec./inf. | 8 |
| 7′ | Additive context-free scalar is zero **on a nullity-closed family** | $\mathsf{W}_1$ | 8 |
| 8 | Conditional information redundancy | all | 8 |
| 9 | Arena dependence of normalisation | all | 8 |
| 10′ | Bounded encodability, deterministic form, projection evaluator | deterministic | 9 |
| 11 | Type-level licensing dichotomy, **conditional on its hypothesis** | composition | 10 |
| 12′ | An instance-level non-associative composition exists | composition | 10 |
| 13′ | Diffusion and composition can disagree on an exhibited signature | composition | 10 |
| 6.2 | Orbit constancy under a fixed context | all | 6 |
| 11.1 | Consistency of the deterministic fragment | fragment | 11 |

---

## 13. Withdrawn results

Each was a statement of the prior edition. None is asserted here.

| Prior statement | Ground for withdrawal | Finding |
|---|---|---|
| Theorem 2 "designation necessity" | Displayed equality is an instance of A3; "underlying structure" undefined | AV-006 |
| Definitions 6.2–6.3 designation / filter context | Underlying structure and group action undefined | AV-006 |
| Corollaries 2.1–2.2 | Depend on withdrawn definitions | AV-006 |
| Corollary 1.1 (no context-free ordering) | Universal claim from an existential theorem | AV-007 |
| Corollary 3.1 (computability) | **False**: measurable factorisation is not an algorithm | AV-009 |
| Corollary 3.2 (forced abstention in every non-sufficient case) | **False**: non-totality branch admits singleton fibres | AV-010 |
| Theorem 4 (quotient descent) | **False** under the total reading; incomplete under the partial reading | AV-011 |
| Corollary 6.1 (no common latent quantity) | Latent quantity undefined; monotone-map argument unsupported | AV-013 |
| Theorem 7 (additive scalar triviality) | **False**: nullity witness need not lie in the family | AV-014 |
| Corollary 8.1 (no epistemic role) | **False**: informative to an observer lacking $R$ | AV-015 |
| Corollaries 9.1–9.2 (incomparability, uncalibratability) | Do not follow from Theorem 9 | AV-016 |
| Theorem 10 proof, and its "all forms" label | Subtraction not measurable in class $\mathsf{W}_2$ | AV-017 |
| Corollary 10.1 (**no empirical content whatever**) | Not proved; other forms are constrained; single-context only | AV-018 |
| Corollary 10.2 (exhaustive sources of content) | Exhaustiveness unproved | AV-018 |
| Corollaries 12.2–12.3 | Universal overreach; undefined "substructure" | AV-020 |
| Observations 10.7–10.9 (recognisability, state count, prior-art subsumption) | Undefined objects; missing finiteness and effectiveness; universal claim unproved | AV-022 |
| Corollary 14.1 second clause ("depends on data outside") | Not a logical consequence of non-structurality | AV-023 |
| Proposition 12.1 as a consistency proof | Missing component; vacuous A3 check; set not closed under transport | AV-024 |
| Axioms A1, A6 | Not predicates over the signature; demoted to DP-1, DP-2 | AV-005 |
| Limitations 14.1, 14.2, 14.3, 14.5, 14.6, 14.9, 14.10 | Depend on withdrawn or false results | AV-027 |
| Rejections 16.2, 16.4, 16.5, 16.7, 16.9, 16.11, 16.14 | Depend on withdrawn or false results | AV-027 |
| Open Question 15.6's negative closure | Universal prior-art subsumption unproved | AV-022 |

---

## 14. Limitations that follow from verified results

**14.4.** The reduction $\rho_C$ is primitive and is not determined by the theory. *(The prior further claim that distinct reductions always induce distinct orderings on asymmetric profiles is withdrawn: distinct positive rescalings induce the same ordering — AV-027.)*

**14.7.** Absent a declared transport (Definition 8.9), values under distinct contexts are not compared. This is the A7 stipulation, not a theorem, and A7 expressly permits comparison through a declared transport.

**14.11 (new).** Within the deterministic contrast form with unrestricted evaluators, the axioms exclude no single-context assignment (Corollary 10.1′). **No conclusion about the framework as a whole follows.**

**14.12 (new).** Consistency is established only for the deterministic fragment over a finite morphism universe (Proposition 11.1, Observation 11.1.2).

---

## 15. Open obligations and questions

**OB-1 (Blocking).** Consistency beyond the deterministic fragment, including A3 over all representation morphisms. See Observation 11.1.2 for the exact exclusion list.

**OB-2.** Conditions on $M_C$, $\tau$ and $\delta_C$ sufficient for measurability of $\delta^{\,b}_C$, currently assumed in Assumption 8.0.

**OB-3.** Conditions guaranteeing existence of a regular evidence structure (Definition 3.14) on given spaces.

**OB-4 (new).** A formalisation of DP-1 and DP-2 as predicates over the signature, or a demonstration that none is needed.

**Open Question 15.1.** Conditions under which a composition signature admits an associative $\odot$.

**Open Question 15.2.** A structural characterisation of fibre-constancy.

**Open Question 15.3.** An axiomatisation of preferences over profiles forcing a unique reduction.

**Open Question 15.4.** Whether the three forms of §8 are fibres of a single indexed structure.

**Open Question 15.5.** Whether admissibility is reducible to a decision-theoretic threshold.

**Open Question 15.6 — reopened.** Is there an invariant of a composition signature not expressible in existing typed, temporal or dimensionally annotated formalisms? The prior edition closed this negatively. That closure is **withdrawn**: a universal subsumption claim over an unquantified comparison class was neither proved nor cited. The question is open. Independently of it, **no novelty is claimed by this document**.

**Open Question 15.7.** A pseudometric on contexts under which significance is continuous.

**Open Question 15.8.** Whether joint operations are required, i.e. whether a coalitional extension is needed.

---

## 16. Rejected formulations

Only those entailed by a verified result are retained. Each names its ground.

**16.1.** *Significance is an intrinsic attribute of a bearer.* — Rejected as a **stipulation** of Definition 5.3, under which $\sigma$ is a function of $(C,b)$. Theorem 1 shows only that context-reversal is permitted; it does not by itself refute intrinsicness.

**16.3.** *A derived summary supplies information beyond the representation to an observer who already has the representation.* — Theorem 8.

**16.6.** *Significance emerges from structure.* — Rejected as not a proposition of this signature: it supplies no component of Definition 3.10 and states no map.

**16.8.** *Type-level licensing is sound and complete in general.* — Theorem 11, **under its hypothesis** that $\kappa$ is not type-determined. Where $\kappa$ is exactly type-determined, type-level licensing is sound and complete.

**16.10.** *Path functionals are invalid when relations are non-transitive.* — Rejected as **false**: $[\![\cdot]\!]_{\mathrm{diff}}$ is total on any signature (Observation 13.1′).

**16.12.** *Values under distinct contexts may be compared **without a declared transport**.* — A7 with Definition 8.9. The unqualified prior form is withdrawn, since A7 expressly permits comparison through a declared transport.

**16.13.** *Significance may depend on artefact relabelling.* — Corollary 6.2, **for morphisms in the declared universe only**.

**16.15.** *Context is discovered from evidence.* — Rejected by inspection of Definition 3.10: $T_C$, $\delta_C$ and $\rho_C$ are primitives; no construction produces them from $\mu_C$.

**16.16.** *The framework derives its evaluator automatically.* — Same ground. *(Theorem 10′ realises value assignments, not evaluators; the prior appeal to it is withdrawn.)*

**16.17.** *A context-free ordering primitive exists in this signature.* — Rejected by inspection: no such component is declared. *(The prior theorem-based prohibitions are withdrawn with Theorem 7; Theorem 7′ prohibits only the additive decomposition on a nullity-closed family.)*

**16.18.** *This document claims novelty.* — Rejected: no novelty claim is made. **No universal prior-art subsumption is claimed either** (Open Question 15.6).

**16.19.** *Significance-first intelligence is a statement of this theory.* — Rejected: the phrase occurs in no definition, axiom or theorem.

---

*End of ASTRO-THEORY-0001 — Theory Candidate, remediated. Not verified. Not frozen. Awaiting independent re-verification.*
