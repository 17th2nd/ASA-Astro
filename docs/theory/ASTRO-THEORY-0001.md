# ASTRO-THEORY-0001 — Contextual Difference Theory

| Field | Value |
|---|---|
| Status | **Theory Candidate.** Not frozen in this pass. |
| Structure | **Part A — Version 1 Deterministic Core Candidate** · **Part B — Candidate Enrichments** |
| Verification | Not externally verified. The prior edition was independently re-verified as **DETERMINISTIC CORE REQUIRES BOUNDED REMEDIATION** (findings FV-001 – FV-006). This edition remediates those findings and awaits final re-verification. |
| Empirical status | Not empirically validated. Evidence level `EH-0`. |
| Novelty | No novelty is claimed. No universal prior-art subsumption is claimed. |
| Prior edition | Blob `0d64e4fd1fa8d6668ece38c6ec4f0fab73479210`. Not silently overwritten; every change is mapped. |

**Freeze boundary.** Part A is self-contained: **no Part A definition, axiom, theorem or proof depends on anything in Part B.** Part B is Candidate, non-frozen, not required by the deterministic core, outside the consistency claim, and outside any Version 1 verification claim.

**What changed in this pass.** A context family and an admissible morphism universe are now declared signature objects (FV-001). The profile of an almost-everywhere-defined contrast is now formally constructed (FV-002). Theorem 10′ was **false** for an allowed codomain and is replaced by Theorem 10″ restricted to point-separating codomains (FV-003). The consistency witness contained a **false closure claim** and is replaced (FV-004, FV-005). Rejection 16.1 is **withdrawn**: the deterministic core does not exclude intrinsic significance (FV-006).

---

# PART A — VERSION 1 DETERMINISTIC CORE CANDIDATE

## A.1 Scope of the core

**In the core.** Bearers; model space; contexts; deterministic operations; outcome maps; deterministic contrast evaluators; contextual difference; deterministic significance; representation covariance; factorisation; contextual nullity; the deterministic consistency witness; and exactly the limitations that follow.

**Not in the core.** Everything in Part B.

**Observation A.1.1.** Part A proves less than earlier editions asserted. §A.10.2 lists what is **not** proved, including two things the core is now explicit that it cannot do.

---

## A.2 Deterministic signature

### A.2.1 Carriers

**Definition 3.1 (Bearers) — primitive.** A set $\mathfrak{B}$. Elements $b$ are *bearers*. $\mathfrak{B}$ is not a subset of any state space.

**Definition 3.2 (Model space) — primitive.** A measurable space $(\mathfrak{M},\mathcal{F})$.

**Definition 3.3 (Representation map) — primitive, optional.** A measurable $r:\mathfrak{M}\to(\mathcal{R},\mathcal{H})$.

**Definition 3.4 (Operation) — derived, total.** A measurable $\tau:\mathfrak{M}\to\mathfrak{M}$. $\mathrm{Op}(\mathfrak{M})$ is the set of these.

### A.2.2 Codomains

**Definition 3.5 (Codomain) — primitive, context-indexed.** A triple $(W,\preceq_W,\Sigma_W)$: a nonempty set, a partial order on it, and a $\sigma$-algebra on it. It is of class $\mathsf{W}_1$ (*magnitude*) if it additionally carries $(\oplus,0_W)$ making $(W,\oplus,0_W,\preceq_W)$ an ordered commutative monoid with $0_W$ least.

**Definition 3.5.1 (Point-separating codomain) — derived.** A codomain is *point-separating* if for all $x\neq y$ in $W$ there is $A\in\Sigma_W$ with $x\in A$ and $y\notin A$.

**Observation 3.5.2 — remediates FV-003.** Point separation is equivalent to injectivity of $x\mapsto\delta_x$ from $W$ into $\Delta(W)$. If some $A\in\Sigma_W$ separates $x$ from $y$ then $\delta_x(A)=1\neq0=\delta_y(A)$; conversely if no measurable set separates them then $\delta_x$ and $\delta_y$ agree on every measurable set. Borel $\mathbb{R}_{\ge0}$ is point-separating; a two-point set with the trivial $\sigma$-algebra $\{\emptyset,W\}$ is not.

**Definition 3.7 (Order-intervals) — derived.** $\mathcal{I}(W):=\{[u,v]:u,v\in W,\ u\preceq_W v\}$ where $[u,v]=\{x\in W:u\preceq_W x\preceq_W v\}$.

**Definition 3.8 (Output codomain) — derived.** $\widehat{W}:=W\sqcup\mathcal{I}(W)\sqcup\{\bot_{\mathrm{ind}},\bot_{\mathrm{inc}},\bot_{\mathrm{und}}\}$, a disjoint union.

**Definition 3.9 (Absent value) — primitive.** A symbol $\bot_{\mathrm{abs}}$, the value of an optional component deliberately not supplied. Distinct from $\bot_{\mathrm{und}}$.

### A.2.3 Contexts

**Definition 3.10 (Context) — primitive.** Over a fixed $\mathfrak{B}$ and $(\mathfrak{M},\mathcal{F})$, a context is the seven-tuple
$$C=\big(\mu_C,\ (\mathcal{Y}_C,\mathcal{G}_C),\ M_C,\ T_C,\ \approx_C,\ \delta_C,\ (W_C,\rho_C)\big)$$

| Component | Type | Mark |
|---|---|---|
| $\mu_C$ | probability measure on $(\mathfrak{M},\mathcal{F})$ | required |
| $(\mathcal{Y}_C,\mathcal{G}_C)$ | measurable outcome space | required, context-indexed |
| $M_C:\mathfrak{M}\to\mathcal{Y}_C$ | measurable, total | required |
| $T_C:\mathfrak{B}\rightharpoonup\mathrm{Op}(\mathfrak{M})$ | operation assignment | required, **partial** |
| $\approx_C$ | equivalence on $\mathcal{Y}_C$, or $\bot_{\mathrm{abs}}$ | optional |
| $\delta_C:\mathcal{Y}_C\times\mathcal{Y}_C\rightharpoonup W_C$ | measurable on its domain $D_C\in\mathcal{G}_C\otimes\mathcal{G}_C$ | required, **partial** |
| $(W_C,\rho_C)$ | codomain and reduction | required, context-indexed |

**Definition 3.11 (Reduction) — primitive, partial.** $\rho_C:\Delta(W_C)\rightharpoonup\widehat{W_C}$, where $\Delta(W_C)$ is the set of probability measures on $(W_C,\Sigma_{W_C})$.

**Definition 3.12 (Location functional) — derived.** For $W_C$ realised as $(\mathbb{R}_{\ge0},+,0,\le)$ with the Borel $\sigma$-algebra, a *location functional* is a partial $\ell:\Delta(\mathbb{R}_{\ge0})\rightharpoonup\mathbb{R}_{\ge0}$ with $\inf\operatorname{supp}\nu\le\ell(\nu)\le\sup\operatorname{supp}\nu$ where defined, and $\ell(\delta_x)=x$.

**Definition 3.12.1 (Atom reduction) — derived, partial.** For a **point-separating** codomain $W$, the *atom reduction* $\rho^{\mathrm{at}}:\Delta(W)\rightharpoonup W$ has domain $\{\delta_x:x\in W\}$ and $\rho^{\mathrm{at}}(\delta_x)=x$. It is a well-defined function by Observation 3.5.2.

**Observation 3.12.2 — remediates FV-003.** On a codomain that is not point-separating the atom reduction is **not** a function: one measure would have to be sent to two distinct atoms. Every use of $\rho^{\mathrm{at}}$ below declares point separation.

### A.2.4 Representation morphisms

**Definition 3.14.1 (Homogeneous frame) — primitive. Remediates DCV-001.** A *frame* is a quadruple
$$\mathbb{F}=\big(\mathfrak{B},\ (\mathfrak{M},\mathcal{F}),\ (\mathcal{Y},\mathcal{G}_{\mathcal{Y}}),\ (W,\preceq_W,\Sigma_W)\big)$$
consisting of a bearer set, a measurable model space, **one** measurable outcome space and **one** codomain. **Version 1 is homogeneous:** every context of a theory instance uses the frame's outcome space and codomain.

**Observation 3.14.2 (Option A declared, with justification) — remediates DCV-001.** Definition 3.10 permits $(\mathcal{Y}_C,\mathcal{G}_C)$ and $W_C$ to vary with $C$, while a single group was required to act on all of $\mathcal{C}$; the group's outcome and codomain components had no declared source or target, so transported contexts, closure, A3, $\mathrm{Aut}(C)$ and functoriality were not typed for heterogeneous carriers. Two completions were available. **Option A (homogeneous carriers) is adopted**, for three reasons.

1. **No Part A theorem uses heterogeneity.** Theorem 1 varies only $M_C$; Theorem 7′ fixes $W=(\mathbb{R}_{\ge0},+,0,\le)$ throughout its family; Theorem 10″ constructs one context; Corollary 6.2 works inside one context; Proposition 11.1′ is already homogeneous. Option A therefore removes no result.
2. **It is the bounded repair.** Under Option A every morphism component is an endomorphism of a fixed object, so identity, composition, inverse and functoriality are the ordinary componentwise facts about automorphism groups and need no new coherence apparatus.
3. **Option B would be a redesign.** A context-indexed action needs components $\iota_{\mathcal{Y},C}:\mathcal{Y}_C\to\mathcal{Y}_{\iota_*C}$ whose target is named by the very transport they define, so the target carrier must be posited as part of the datum rather than derived, and coherence laws must then be proved. That is additional structure, which this pass is not authorised to add.

**Consequence.** **Heterogeneous context-indexed outcome spaces and codomains, and any indexed or groupoid action over them, are removed from Version 1 and deferred as Candidate material.** They are outside Part A, outside the consistency claim of Proposition 11.1′, and outside any Version 1 verification claim. Their formal placement within Part B is deferred, because the pass that adopted Option A was not authorised to modify Part B; the deferral is recorded as **OB-A5**.

**Definition 3.15 (Representation morphism) — derived. Remediates DCV-001.** Over a frame $\mathbb{F}$, a *representation morphism* is a family $\iota=(\iota_{\mathfrak{B}},\iota_{\mathfrak{M}},\iota_{\mathcal{Y}},\iota_W)$ with

| Component | Source | Target | Condition |
|---|---|---|---|
| $\iota_{\mathfrak{B}}$ | $\mathfrak{B}$ | $\mathfrak{B}$ | bijection |
| $\iota_{\mathfrak{M}}$ | $(\mathfrak{M},\mathcal{F})$ | $(\mathfrak{M},\mathcal{F})$ | bimeasurable bijection |
| $\iota_{\mathcal{Y}}$ | $(\mathcal{Y},\mathcal{G}_{\mathcal{Y}})$ | $(\mathcal{Y},\mathcal{G}_{\mathcal{Y}})$ | bimeasurable bijection |
| $\iota_W$ | $(W,\preceq_W,\Sigma_W)$ | $(W,\preceq_W,\Sigma_W)$ | automorphism: order isomorphism, measurable isomorphism, and isomorphism of any declared class-$\mathsf{W}_1$ structure |

Write $\mathrm{Mor}(\mathbb{F})$ for the set of these.

**Observation 3.15.1 (Group laws) — remediates DCV-001.** Every component of Definition 3.15 has the **same source and target**, so componentwise composition and componentwise inverse are defined without further data.
*Identity.* $\mathbf{1}:=(\mathrm{id}_{\mathfrak{B}},\mathrm{id}_{\mathfrak{M}},\mathrm{id}_{\mathcal{Y}},\mathrm{id}_W)\in\mathrm{Mor}(\mathbb{F})$.
*Composition.* $(\iota\circ\kappa)$ is defined componentwise and lies in $\mathrm{Mor}(\mathbb{F})$: a composite of bijections is a bijection, of bimeasurable bijections is bimeasurable, and of codomain automorphisms is a codomain automorphism.
*Inverse.* $\iota^{-1}$ is defined componentwise and lies in $\mathrm{Mor}(\mathbb{F})$, since each component class is closed under inverse.
*Associativity and unit laws* hold componentwise because composition of functions is associative with the identity as unit.
Hence $\mathrm{Mor}(\mathbb{F})$ is a group, and $\mathcal{G}$ of Definition 3.18 is a subgroup of it. $\square$

**Definition 3.16 (Extended action) — derived.** $\widehat{\iota_W}:\widehat{W}\to\widehat{W'}$ acts as $\iota_W$ on $W$, as $[u,v]\mapsto[\iota_Wu,\iota_Wv]$ on $\mathcal{I}(W)$, and as the identity on each bottom.

**Definition 3.17 (Transported context) — derived.** $\iota_*C$ has
$$\mu_{\iota_*C}=(\iota_{\mathfrak{M}})_*\mu_C,\qquad M_{\iota_*C}=\iota_{\mathcal{Y}}\circ M_C\circ\iota_{\mathfrak{M}}^{-1},\qquad T_{\iota_*C}(\iota_{\mathfrak{B}}b)=\iota_{\mathfrak{M}}\circ T_C(b)\circ\iota_{\mathfrak{M}}^{-1},$$
$$\approx_{\iota_*C}=\bot_{\mathrm{abs}}\ \text{if}\ \approx_C=\bot_{\mathrm{abs}},\ \text{else}\ \{(\iota_{\mathcal{Y}}y,\iota_{\mathcal{Y}}y'):y\approx_Cy'\},$$
$$\delta_{\iota_*C}=\iota_W\circ\delta_C\circ(\iota_{\mathcal{Y}}^{-1}\times\iota_{\mathcal{Y}}^{-1}),\qquad \rho_{\iota_*C}=\widehat{\iota_W}\circ\rho_C\circ((\iota_W)^{-1})_*.$$
The carriers are unchanged: $(\mathcal{Y}_{\iota_*C},\mathcal{G}_{\iota_*C})=(\mathcal{Y},\mathcal{G}_{\mathcal{Y}})$ and $(W_{\iota_*C},\preceq,\Sigma)=(W,\preceq_W,\Sigma_W)$, because $\iota_{\mathcal{Y}}$ and $\iota_W$ are automorphisms of the frame's fixed objects.

**Observation 3.17.0 (Transport is well typed) — remediates DCV-001.** Every displayed component of $\iota_*C$ is a composite of maps whose sources and targets are declared by Definition 3.15 and the frame: $M_{\iota_*C}:\mathfrak{M}\to\mathcal{Y}$; $T_{\iota_*C}(b'):\mathfrak{M}\to\mathfrak{M}$; $\delta_{\iota_*C}:\mathcal{Y}\times\mathcal{Y}\rightharpoonup W$; $\rho_{\iota_*C}:\Delta(W)\rightharpoonup\widehat W$. Hence $\iota_*C$ is a context over the same frame, and the predicate $\iota_*C\in\mathcal{C}$ of Definition 3.18 is evaluable **before** any closure requirement is imposed. Under the prior edition it was not, because $\iota_{\mathcal{Y}}$ and $\iota_W$ had no declared source or target.

**Observation 3.17.1 (Functoriality).** $(\mathrm{id})_*C=C$ and $(\iota\circ\kappa)_*C=\iota_*(\kappa_*C)$.
*Proof.* Each component of Definition 3.17 is built from $\iota_{\mathfrak{B}},\iota_{\mathfrak{M}},\iota_{\mathcal{Y}},\iota_W$ by composition and inverse; composition of bijections is associative and the identity acts trivially in each slot. $\square$
This is used by the closure argument of Proposition 11.1′.

### A.2.5 Theory instance

**Definition 3.18 (Theory instance) — primitive. Remediates FV-001, DCV-001, DCV-002.** A *theory instance* is a tuple
$$\mathbb{T}=\big(\underbrace{\mathfrak{B},\ (\mathfrak{M},\mathcal{F}),\ (\mathcal{Y},\mathcal{G}_{\mathcal{Y}}),\ (W,\preceq_W,\Sigma_W)}_{\text{frame }\mathbb{F}},\ \ \mathsf{r},\ \ \mathcal{C},\ \ \mathcal{G}\big)$$
subject to:

1. **Frame.** $\mathbb{F}$ is a homogeneous frame (Definition 3.14.1).
2. **Representation component $\mathsf{r}$ — remediates DCV-002.** Exactly one of:
 - $\mathsf{r}=\big(r,(\mathcal{R},\mathcal{H})\big)$ with $(\mathcal{R},\mathcal{H})$ a measurable space and $r:\mathfrak{M}\to\mathcal{R}$ **total and measurable**; or
 - $\mathsf{r}=\bot_{\mathrm{abs}}$, the typed absence.
3. **Contexts.** $\mathcal{C}$ is a nonempty set of contexts in the sense of Definition 3.10 with $(\mathcal{Y}_C,\mathcal{G}_C)=(\mathcal{Y},\mathcal{G}_{\mathcal{Y}})$ and $(W_C,\preceq,\Sigma)=(W,\preceq_W,\Sigma_W)$ for every $C\in\mathcal{C}$ — the **homogeneity requirement**.
4. **Group.** $\mathcal{G}$ is a subgroup of $\mathrm{Mor}(\mathbb{F})$ (Observation 3.15.1).
5. **Closure.** $\iota\in\mathcal{G}$ and $C\in\mathcal{C}$ imply $\iota_*C\in\mathcal{C}$, a predicate evaluable by Observation 3.17.0.

**Observation 3.18.2 (Effect of $\mathsf{r}$) — remediates DCV-002.** $\mathsf{r}$ is instance data, not external data. If $\mathsf{r}=(r,(\mathcal{R},\mathcal{H}))$, then **A10** and **Definitions 7.1, 7.4, 7.5 and 7.7** are interpreted with that $r$, and $\mathcal{H}_r$ of Definition 7.1 is computed from it. If $\mathsf{r}=\bot_{\mathrm{abs}}$, then those definitions have no instance to interpret and are **typed as inapplicable**: A10 is not asserted, no identified output is defined, and no sufficiency, fibre-constancy or totality predicate of Definition 7.4 is defined. Inapplicability is a typed state, not a truth value, and in particular A10 is neither true nor false for such an instance. Theorem 3 and Corollary 3.3 are unaffected either way, since they quantify over an arbitrary measurable $r$ or over $M_C$ supplied as their own hypothesis rather than over $\mathsf{r}$.

**Definition 3.18.3 (Primitive-completeness table) — remediates DCV-001, DCV-002.** Every primitive required to interpret every Part A definition and axiom:

| Primitive | Type | Required / optional | Global / context-indexed | Total / partial | Role in axioms and theorems |
|---|---|---|---|---|---|
| $\mathfrak{B}$ | set | required | global | — | bearers; A3, A4, Thms 1, 7′, 10″ |
| $(\mathfrak{M},\mathcal{F})$ | measurable space | required | global | — | models; Defs 3.4, 5.1; Thm 3 |
| $(\mathcal{Y},\mathcal{G}_{\mathcal{Y}})$ | measurable space | required | global (homogeneous) | — | outcomes; Defs 3.10, 5.1; Cor 3.3 |
| $(W,\preceq_W,\Sigma_W)$ | codomain | required | global (homogeneous) | — | values; A5, A7; Defs 3.7, 3.8, 3.11 |
| $\mathsf{r}$ | $(r,(\mathcal{R},\mathcal{H}))$ **or** $\bot_{\mathrm{abs}}$ | **optional, typed** | global | total if supplied | A10; Defs 7.1, 7.4, 7.5, 7.7; Prop 11.1′ |
| $\mathcal{C}$ | set of contexts | required | global | — | A3, A4; Thm 7′; Prop 11.1′ |
| $\mathcal{G}$ | subgroup of $\mathrm{Mor}(\mathbb{F})$ | required | global | — | A3; Def 6.1; Cor 6.2 |
| $\mu_C$ | probability measure on $(\mathfrak{M},\mathcal{F})$ | required | context-indexed | total | Defs 5.2, 5.3 |
| $M_C$ | $\mathfrak{M}\to\mathcal{Y}$ measurable | required | context-indexed | total | Defs 5.1; Cor 3.3 |
| $T_C$ | $\mathfrak{B}\rightharpoonup\mathrm{Op}(\mathfrak{M})$ | required | context-indexed | **partial** | Defs 5.1, 5.3 |
| $\approx_C$ | equivalence on $\mathcal{Y}$, or $\bot_{\mathrm{abs}}$ | optional, typed | context-indexed | — | A8; Thm 4′ |
| $\delta_C$ | $\mathcal{Y}\times\mathcal{Y}\rightharpoonup W$ | required | context-indexed | **partial** | Defs 5.1, 5.2; A8 |
| $\rho_C$ | $\Delta(W)\rightharpoonup\widehat W$ | required | context-indexed | **partial** | Def 5.3; A5 |

**No Part A axiom depends on data absent from this table.** A3 and A4 range over $\mathcal{G}$ and $\mathcal{C}$; A5 and A7 over $\widehat W$; A8 over $\approx_C$ and $\delta_C$; A9 over $\Omega^b_C$, derived from $M_C$, $T_C$, $\delta_C$; A10 over $\mathsf{r}$.

**Observation 3.18.1 — remediates FV-001.** The prior edition used $\mathcal{C}$ in A4 and Theorem 7′, and used a morphism universe inside its consistency proof, without declaring either; A3 meanwhile quantified over *every* representation morphism while the proof checked only a model-specific set. Both objects are now signature components, A3 quantifies over the declared $\mathcal{G}$, and **closure is a requirement on instances rather than a claim to be proved about a particular one**. A3 and A4 are consequently predicates over the declared signature.

---

## A.3 Formation rule and axioms

**Formation rule FR-1.** A seven-tuple missing a required component of Definition 3.10 is not a context, and no significance is defined for it. An optional component supplied as $\bot_{\mathrm{abs}}$ is supplied.

**Observation FR-1.1.** This was stated as Axiom A2. It is a formation rule, not a substantive predicate over the class of contexts, because Definition 3.10 already requires all seven components. It is reclassified and is not counted among the axioms.

Fix a theory instance $\mathbb{T}=(\mathfrak{B},\mathfrak{M},\mathcal{C},\mathcal{G})$.

**A3 (Covariance over $\mathcal{G}$).** For every $\iota\in\mathcal{G}$, $C\in\mathcal{C}$, $b\in\mathfrak{B}$:
$$\sigma_{\iota_*C}(\iota_{\mathfrak{B}}b)=\widehat{\iota_W}\big(\sigma_C(b)\big),$$
an equation in $\widehat{W_{\iota_*C}}$. Well formed because $\iota_*C\in\mathcal{C}$ by Definition 3.18.

**A4 (Nullity over $\mathcal{C}$).** For every $b\in\mathfrak{B}$ there is $C\in\mathcal{C}$ with $W_C$ of class $\mathsf{W}_1$ and $\sigma_C(b)=0_{W_C}$.

**A5 (Output typing).** $\sigma_C(b)\in\widehat{W_C}$, with the value determined by Definition 5.3.

**A7 (Codomain confinement).** Values under $C$ lie in $\widehat{W_C}$; values under distinct contexts are related only through a declared transport (Definition 8.9).

**A8 (Congruence).** If $\approx_C\neq\bot_{\mathrm{abs}}$, then for $(y,y'),(\tilde y,\tilde y')\in D_C$ with $y\approx_C\tilde y$ and $y'\approx_C\tilde y'$: $\delta_C(y,y')=\delta_C(\tilde y,\tilde y')$.

**A9 (Empty contrast domain).** If $\Omega^b_C=\emptyset$ then $\sigma_C(b)=\bot_{\mathrm{und}}$.

**A10 (Empty fibre).** If the instance's representation component is $\mathsf{r}=(r,(\mathcal{R},\mathcal{H}))$, then for every $x\in\mathcal{R}$ with $r^{-1}(x)=\emptyset$ the identified output at $x$ is $\bot_{\mathrm{inc}}$. If $\mathsf{r}=\bot_{\mathrm{abs}}$, A10 is **typed as inapplicable** and is not asserted (Observation 3.18.2).

**Observation A.3.1 — replaces the prior Observation 4.2.1.** A3 and A4 are predicates over declared carriers, since $\mathcal{G}$ and $\mathcal{C}$ are instance components. A5, A7, A8, A9, A10 are predicates over declared functions. FR-1 is a formation rule. Satisfaction of A3–A10 is therefore testable in a model, which is what Proposition 11.1′ does.

---

## A.4 Contrast and deterministic significance

**Definition 5.1 (Pointwise contrast) — derived, partial.** For $\tau=T_C(b)$ defined,
$$\delta^{\,b}_C(m)=\delta_C\big(M_C(m),M_C(\tau m)\big),\qquad \Omega^b_C:=\{m:(M_C(m),M_C(\tau m))\in D_C\}.$$
$\Omega^b_C\in\mathcal{F}$, since $m\mapsto(M_C(m),M_C(\tau m))$ is measurable into $\mathcal{G}_C\otimes\mathcal{G}_C$ and $D_C$ is measurable.

**Definition 5.2 (Profile) — derived, partial. Remediates FV-002.** Suppose $\mu_C(\Omega^b_C)=1$. Write $\Omega:=\Omega^b_C$, give $\Omega$ the trace $\sigma$-algebra $\mathcal{F}|_\Omega=\{F\cap\Omega:F\in\mathcal{F}\}$, let $\mu^\Omega_C$ be the restriction of $\mu_C$ to $\mathcal{F}|_\Omega$ — a probability measure, since $\mu_C(\Omega)=1$ — and let $\delta^{b,\Omega}_C:\Omega\to W_C$ be the restriction of $\delta^{\,b}_C$, which is **total and measurable** on $(\Omega,\mathcal{F}|_\Omega)$. The *profile* is
$$P^b_C:=\big(\delta^{b,\Omega}_C\big)_*\mu^\Omega_C\ \in\ \Delta(W_C).$$
If $\mu_C(\Omega^b_C)<1$, no profile exists.

**Observation 5.2.1 — remediates FV-002.** The prior edition wrote the ordinary pushforward of a **partial** map, which is not an instance of any operation declared in the candidate. Definition 5.2 instead pushes forward a restricted probability measure along a restricted map that is total on its domain. No extension off the null complement is used, so no existence or extension-independence question arises.

**Definition 5.3 (Deterministic significance) — derived, partial.** Exhaustively:

| Case | $\sigma_C(b)$ |
|---|---|
| $T_C(b)$ undefined | $\bot_{\mathrm{und}}$ |
| $T_C(b)$ defined and $\mu_C(\Omega^b_C)<1$ — this includes $\Omega^b_C=\emptyset$ | $\bot_{\mathrm{und}}$ |
| $\mu_C(\Omega^b_C)=1$ and $P^b_C\notin\operatorname{dom}\rho_C$ | $\bot_{\mathrm{und}}$ |
| $\mu_C(\Omega^b_C)=1$ and $P^b_C\in\operatorname{dom}\rho_C$ | $\rho_C(P^b_C)$ |

The four cases partition every possibility and agree with A9.

**Theorem 1 (Order reversal exists).**
*Hypotheses.* $\mathfrak{B}=\{b_1,b_2\}$; $\mathfrak{M}=\mathbb{R}^2$ Borel; $W=(\mathbb{R}_{\ge0},+,0,\le)$ Borel — class $\mathsf{W}_1$ and **point-separating**; $\rho=\rho^{\mathrm{at}}$; $\approx=\bot_{\mathrm{abs}}$; $r$ not supplied.
*Quantifier.* **Existential** in the pair of contexts. *Totality.* $M$, $\tau$, $\delta$ total; $T$, $\rho$ partial. *Codomain class.* $\mathsf{W}_1$, point-separating.
*Conclusion.* There exist contexts $C_1,C_2$ agreeing in every component but $M_C$ with $\sigma_{C_1}(b_1)>\sigma_{C_1}(b_2)$ and $\sigma_{C_2}(b_1)<\sigma_{C_2}(b_2)$.

*Proof.* Take $\mu=\delta_{(0,0)}$; $\mathcal{Y}=\mathbb{R}$ Borel; $T(b_1)(x,y)=(x+2,y+1)$ and $T(b_2)(x,y)=(x+1,y+2)$, both measurable; $\delta(u,v)=|u-v|$, total and measurable, so $D_C=\mathcal{Y}^2$ and $\Omega^b_C=\mathfrak{M}$; $M_{C_1}(x,y)=x$ and $M_{C_2}(x,y)=y$. All seven components are supplied. Each profile is a Dirac measure and $\rho^{\mathrm{at}}$ returns its atom, well defined by point separation. Then $\sigma_{C_1}(b_1)=2>1=\sigma_{C_1}(b_2)$ and $\sigma_{C_2}(b_1)=1<2=\sigma_{C_2}(b_2)$. $\blacksquare$

**Observation 1.1′ (Non-conclusions).** Existential only. Theorem 1 does **not** show that every context family reverses, and **no universal statement about the absence of a context-free ordering follows from it.**

---

## A.5 Invariance

**Definition 6.1 (Context automorphism).** $\mathrm{Aut}(C):=\{\pi\in\mathcal{G}:\pi_*C=C\ \text{componentwise and}\ \pi_W=\mathrm{id}_{W_C}\}$, a subgroup of $\mathcal{G}$.

**Corollary 6.2 (Fixed-context orbit constancy).** For every $\pi\in\mathrm{Aut}(C)$ and every $b$: $\sigma_C(\pi_{\mathfrak{B}}b)=\sigma_C(b)$.

*Proof.* A3 gives $\sigma_{\pi_*C}(\pi_{\mathfrak{B}}b)=\widehat{\mathrm{id}}(\sigma_C(b))=\sigma_C(b)$, and $\pi_*C=C$. $\blacksquare$

**Observation 6.2.1 (Non-conclusions).** This is exactly the A3 equation for an automorphism fixing the context and the codomain. It is **not** a designation theorem, and it says nothing about morphisms outside $\mathrm{Aut}(C)$.

---

## A.6 Difference theory

**Definition 7.1 (Final $\sigma$-algebra).** $\mathcal{H}_r:=\{A\subseteq\mathcal{R}:r^{-1}(A)\in\mathcal{F}\}$.

**Theorem 3 (Measurable factorisation).**
*Hypotheses.* $r:\mathfrak{M}\to\mathcal{R}$ measurable; $\mathcal{R}$ carrying $\mathcal{H}_r$; $(\mathsf{V},\Sigma_{\mathsf{V}})$ any measurable space with $\mathsf{V}\neq\emptyset$; $g:\mathfrak{M}\to\mathsf{V}$ measurable and total.
*Quantifier.* Universal in $g$.
*Conclusion.* A measurable total $h:\mathcal{R}\to\mathsf{V}$ with $g=h\circ r$ exists **iff** $g$ is constant on the fibres of $r$.

*Proof.* ($\Rightarrow$) $r(m)=r(m')\Rightarrow g(m)=g(m')$. ($\Leftarrow$) Fix $v_0\in\mathsf{V}$; set $h(x):=g(m)$ for $x\in r(\mathfrak{M})$ and any $m\in r^{-1}(x)$, well defined by fibre-constancy, and $h(x):=v_0$ otherwise. For $B\in\Sigma_{\mathsf{V}}$, $r^{-1}(h^{-1}(B))=g^{-1}(B)\in\mathcal{F}$, so $h^{-1}(B)\in\mathcal{H}_r$. $\blacksquare$

**Observation 3.0.1 (Non-conclusions — exhaustive).** Theorem 3 establishes none of: factorisation through any relation other than the fibres of $r$; uniqueness of $h$ off $r(\mathfrak{M})$; minimality of $r$; identifiability of anything other than $g$; **computability**; empirical prediction; invariance beyond Definition 3.15.

**Corollary 3.3 (Induced outcome map).** With $\mathcal{Y}_C$ carrying the final $\sigma$-algebra of $M_C$, a total measurable $\phi$ with $M_C\circ\tau=\phi\circ M_C$ exists **iff** $M_C\circ\tau$ is constant on the fibres of $M_C$.
*Proof.* Theorem 3 with $r:=M_C$, $g:=M_C\circ\tau$, $\mathsf{V}:=\mathcal{Y}_C$, which is nonempty. $\blacksquare$

**Observation 3.4.** Where the condition fails, only the relation $\{(M_C(m),M_C(\tau m)):m\in\mathfrak{M}\}$ is available. No deterministic induced outcome map is assumed anywhere; Definition 5.1 composes on $\mathfrak{M}$.

**Definition 7.4 (Three separate conditions).** $r$ is *total for* $(C,b)$ if $\Omega^b_C=\mathfrak{M}$; *fibre-constant for* $(C,b)$ if $\delta^{\,b}_C$ is constant on $r^{-1}(x)\cap\Omega^b_C$ for every $x$; *$C$-sufficient for $b$* if both.

**Definition 7.5 (Identified output).** If $r^{-1}(x)=\emptyset$: $\bot_{\mathrm{inc}}$. Else if $r^{-1}(x)\cap\Omega^b_C=\emptyset$: $\bot_{\mathrm{und}}$. Else the set $\mathcal{S}_C(b,x)=\{\delta^{\,b}_C(m):m\in r^{-1}(x)\cap\Omega^b_C\}$.

**Theorem 3.2′ (Non-constancy under totality).**
*Hypotheses.* $r$ total for $(C,b)$ and not fibre-constant. *Quantifier.* Existential in $x$.
*Conclusion.* There is $x$ with $r^{-1}(x)\neq\emptyset$ and $|\mathcal{S}_C(b,x)|\ge2$, and no total measurable $h$ with $\delta^{\,b}_C=h\circ r$ exists.
*Proof.* Failure of fibre-constancy under totality yields $x$ and $m,m'\in r^{-1}(x)$ with $\delta^{\,b}_C(m)\neq\delta^{\,b}_C(m')$; Theorem 3 then denies factorisation. $\blacksquare$

**Observation 3.2.1 (Non-conclusions).** Non-sufficiency arising from failure of **totality** alone yields $\bot_{\mathrm{und}}$ by Definition 5.3, and no two-valued fibre. The universal form asserted in an earlier edition was false and remains withdrawn.

**Definition 7.7 (Four distinct notions).** (i) sufficiency; (ii) minimal sufficiency relative to $\delta^{\,b}_C$; (iii) the distinguishability indicator on $\Omega^b_C\times\Omega^b_C$; (iv) the partition of $\Omega^b_C$ by equality of $\delta^{\,b}_C$. **No minimality is claimed anywhere.**

**Theorem 4′ (Partial quotient descent).**
*Hypotheses.* $\approx_C\neq\bot_{\mathrm{abs}}$; A8; $p$ the projection to $\mathcal{Y}_C/\!\approx_C$; $\bar D_C:=(p\times p)(D_C)$.
*Quantifier.* Universal in the defined pairs.
*Conclusion.* There is a unique **partial** $\bar\delta_C$ with domain exactly $\bar D_C$ satisfying $\bar\delta_C((p\times p)(y,y'))=\delta_C(y,y')$ for all $(y,y')\in D_C$. Its pullback has domain $(p\times p)^{-1}(\bar D_C)\supseteq D_C$ and agrees with $\delta_C$ on $D_C$; the inclusion is strict unless $D_C$ is saturated under $\approx_C\times\approx_C$.
*Proof.* A8 makes the value independent of the chosen defined representative pair, giving existence and well-definedness on $\bar D_C$. Every point of $\bar D_C$ has such a pair, forcing the value and giving uniqueness there. The pullback statement is immediate, and strictness fails exactly when $D_C$ is a union of $\approx_C\times\approx_C$-classes. $\blacksquare$

---

## A.7 Context-free scalars and normalisation

**Theorem 7′ (Additive scalar on a nullity-closed family).**
*Hypotheses.* A theory instance $\mathbb{T}$; a family $\mathcal{K}\subseteq\mathcal{C}$; $W=(\mathbb{R}_{\ge0},+,0,\le)$; $S:\mathfrak{B}\to\mathbb{R}_{\ge0}$; $\beta>0$; **(a)** for every $b$ there is $C\in\mathcal{K}$ with $\sigma_C(b)=0$; **(b)** for every $C\in\mathcal{K}$ there is $g_C:\mathfrak{B}\to\mathbb{R}_{\ge0}$ with $\sigma_C(b)=\beta S(b)+g_C(b)$ for all $b$.
*Quantifier.* Universal in $b$. *Conclusion.* $S\equiv0$.
*Proof.* Fix $b$ and take $C\in\mathcal{K}$ from (a). By (b), $\beta S(b)+g_C(b)=0$ with both summands $\ge0$ and $\beta>0$, so $S(b)=0$. $\blacksquare$

**Observation 7.0 (Non-conclusions).** Hypothesis (a) is indispensable. Without it the conclusion is false: an earlier edition drew its null witness from outside the decomposing family, and the theorem failed.

**Observation 7.1′.** Non-negativity of $g_C$ is essential: without it, $g'_C:=\beta S+g_C$ gives $\sigma_C=g'_C$ with no $S$ term, so the decomposition is absorbable and carries no content.

**Theorem 9 (Arena dependence of normalisation).**
*Hypotheses.* $A\subsetneq A'$ finite and nonempty; $\varphi:A'\to\mathbb{R}_{>0}$; $\max_{A'}\varphi>\max_A\varphi$; $\nu^A(b)=\varphi(b)/\max_A\varphi$.
*Quantifier.* Universal in $b\in A$.
*Conclusion.* $\nu^{A'}(b)<\nu^A(b)$ for every $b\in A$, and both induce the same order on $A$.
*Proof.* With $0<\mathsf{m}=\max_A\varphi<\mathsf{m}'=\max_{A'}\varphi$ and $\varphi(b)>0$, $\varphi(b)/\mathsf{m}'<\varphi(b)/\mathsf{m}$; both are positive multiples of $\varphi$ on $A$. $\blacksquare$

**Observation 9.1′ (Non-conclusions).** This does **not** establish cross-arena incomparability or uncalibratability. If the denominators are declared the original values are recoverable, and $x\mapsto Dx$ calibrates a dimensionless value against a declared dimensioned scale.

**Definition 8.9 (Cross-context transport) — optional.** A declared order-embedding $t:W_C\to W_{C'}$ with extended action $\widehat t$ per Definition 3.16. Comparison across contexts is defined only relative to a declared $t$.

---

## A.8 Bounded encodability

**Theorem 10″ (Encodability on point-separating codomains) — replaces the false Theorem 10′.**
*Hypotheses.* $(W,\preceq_W,\Sigma_W)$ a **point-separating** codomain (Definition 3.5.1); $\mathfrak{B}$ any set; $f:\mathfrak{B}\to W$ any function.
*Quantifier.* Existential in $C$, universal in $b$. *Form.* Deterministic contrast form with a projection evaluator. *Codomain class.* Any point-separating codomain; **no algebraic structure is required**.
*Conclusion.* There is a context $C$ with $W_C=W$ and $\sigma_C(b)=f(b)$ for every $b\in\mathfrak{B}$.

*Proof.* Take $\mathfrak{M}:=W$ with $\Sigma_W$; $\mathcal{Y}_C:=W$ with $\Sigma_W$; $M_C:=\mathrm{id}_W$; $\mu_C:=\delta_{w_0}$ for any $w_0\in W$, a probability measure on $(W,\Sigma_W)$; $\approx_C:=\bot_{\mathrm{abs}}$; $\delta_C(y,y'):=y'$, the second projection, total and $\Sigma_W\otimes\Sigma_W/\Sigma_W$-measurable with no algebraic hypothesis; $T_C(b):=$ the constant map $m\mapsto f(b)$, measurable; $\rho_C:=\rho^{\mathrm{at}}$, a well-defined partial function by point separation. Then $\delta^{\,b}_C(m)=f(b)$ for every $m$, so $\Omega^b_C=\mathfrak{M}$, $P^b_C=\delta_{f(b)}$, and $\sigma_C(b)=\rho^{\mathrm{at}}(\delta_{f(b)})=f(b)$. $\blacksquare$

**Observation 10.0 — remediates FV-003.** The prior Theorem 10′ claimed **every** nonempty codomain and is **false** there. Counterexample: $W=\{0,1\}$ with $\Sigma_W=\{\emptyset,W\}$ is a codomain under Definition 3.5, but it carries exactly one probability measure, so $\delta_0=\delta_1$ and every profile in $\Delta(W)$ is the same object; no reduction can return both $0$ and $1$. Point separation is exactly the hypothesis that repairs this. The projection evaluator was not at fault.

**Corollary 10.1″ (Bounded underdetermination).** Within the deterministic contrast form, on a point-separating codomain, with unrestricted evaluators, no single-context assignment $f:\mathfrak{B}\to W$ is excluded by the axioms.
*Proof.* Theorem 10″. $\blacksquare$

**Observation 10.1.1 (Non-conclusions — binding).** Corollary 10.1″ concerns **one** context, **one** form, and **point-separating** codomains only. It does **not** show that the framework forbids no observation, and **no conclusion about the empirical content of the framework as a whole is drawn anywhere in this document.** Assignments are additionally constrained by A3 over $\mathcal{G}$, by A4 over $\mathcal{C}$, and by A7.

**Observation 10.0.1 (Degenerate witness — scope corrected).** The witness evaluator $\delta_C(y,y')=y'$ ignores the factual outcome. On a point-separating codomain the axioms therefore do not exclude degenerate evaluators, and admitting them makes any assignment realisable in a single deterministic context. **No statement is made about non-point-separating codomains.**

---

## A.9 Deterministic consistency

**Proposition 11.1′ (Consistency of the deterministic core) — replaces the invalid Proposition 11.1.**
*Quantifier.* **Existential** in the theory instance; universal in $\iota\in\mathcal{G}$, $C\in\mathcal{C}$ and $b\in\mathfrak{B}$ within the satisfaction checks.
*Claim.* There is a theory instance satisfying FR-1 and axioms A3, A4, A5, A7, A8, A9, A10 over the deterministic core signature comprising **Definitions 3.1–3.5, 3.5.1, 3.7–3.12, 3.12.1, 3.14.1, 3.15, 3.16, 3.17, 3.18, 3.18.3, 5.1–5.3, 6.1, 7.1, 7.4, 7.5, 7.7 and 8.9**.

*Proof.* Exhibit the theory instance $\mathbb{T}=\big(\mathbb{F},\ \mathsf{r},\ \mathcal{C},\ \mathcal{G}\big)$ of Definition 3.18, component by component.

**Frame $\mathbb{F}$.** $\mathfrak{B}=\{b_1,b_2\}$; $(\mathfrak{M},\mathcal{F})=\mathbb{R}^2$ with the Borel $\sigma$-algebra; $(\mathcal{Y},\mathcal{G}_{\mathcal{Y}})=\mathbb{R}$ with the Borel $\sigma$-algebra; $(W,\preceq_W,\Sigma_W)=(\mathbb{R}_{\ge0},\le)$ with the Borel $\sigma$-algebra, carrying $(+,0)$ so that it is of class $\mathsf{W}_1$, and point-separating by Observation 3.5.2.

**Representation component $\mathsf{r}$ — supplied.** $\mathsf{r}=\big(r,(\mathcal{R},\mathcal{H})\big)$ with $(\mathcal{R},\mathcal{H})=(\mathfrak{M},\mathcal{F})$ and $r:=\mathrm{id}_{\mathfrak{M}}$, total and measurable. Hence $\mathcal{H}_r=\mathcal{F}$ by Definition 7.1, and A10 together with Definitions 7.4, 7.5 and 7.7 are interpreted with this $r$ — **as instance data, not as an external datum**.

**Morphism group $\mathcal{G}$.** $\mathcal{G}:=\{\mathbf{1},\jmath\}$ with $\jmath_{\mathfrak{B}}$ the transposition of $b_1$ and $b_2$; $\jmath_{\mathfrak{M}}(x,y)=(y,x)$; $\jmath_{\mathcal{Y}}=\mathrm{id}_{\mathbb{R}}$; $\jmath_W=\mathrm{id}_W$. Each component has the source and target required by Definition 3.15: $\jmath_{\mathfrak{B}}$ is a bijection of $\mathfrak{B}$; $\jmath_{\mathfrak{M}}$ is a bimeasurable bijection of $(\mathfrak{M},\mathcal{F})$; $\jmath_{\mathcal{Y}}$ is a bimeasurable bijection of $(\mathcal{Y},\mathcal{G}_{\mathcal{Y}})$; and $\jmath_W$ is an automorphism of $(W,\preceq_W,\Sigma_W)$ preserving $+$ and $0$. So $\jmath\in\mathrm{Mor}(\mathbb{F})$. Since $\jmath\circ\jmath=\mathbf{1}$ componentwise, $\mathcal{G}$ is a subgroup of $\mathrm{Mor}(\mathbb{F})$ of order two, as Definition 3.18 clause 4 requires.

**Shared context components.** $\mu=\delta_{(0,0)}$; $\approx=\bot_{\mathrm{abs}}$; $\delta(u,v)=|u-v|$, total, so $D_C=\mathcal{Y}^2$ and every $\Omega^b_C=\mathfrak{M}$; $\rho=\rho^{\mathrm{at}}$, well defined because $W$ is point-separating. Every context uses the frame's $(\mathcal{Y},\mathcal{G}_{\mathcal{Y}})$ and $(W,\preceq_W,\Sigma_W)$, so **the homogeneity requirement of Definition 3.18 clause 3 holds** and the witness instantiates the general repaired signature rather than a private structure.

**Contexts.**
$C_1$: $M(x,y)=x$; $T(b_1)(x,y)=(x+2,y+1)$; $T(b_2)(x,y)=(x+1,y+2)$.
$C_2:=\jmath_*C_1$. By Definition 3.17, $M_{C_2}(x,y)=M_{C_1}(\jmath^{-1}(x,y))=M_{C_1}(y,x)=y$; $T_{C_2}(b_2)=\jmath\circ T_{C_1}(b_1)\circ\jmath^{-1}$, which sends $(x,y)\mapsto(y,x)\mapsto(y+2,x+1)\mapsto(x+1,y+2)$; and $T_{C_2}(b_1)$ sends $(x,y)\mapsto(x+2,y+1)$.
$C_0$: $M(x,y)=x$; $T(b_1)=T(b_2)=\big((x,y)\mapsto(x,y+1)\big)$.
$C_0':=\jmath_*C_0$. By Definition 3.17, $M_{C_0'}(x,y)=y$ and $T_{C_0'}(b_i)(x,y)=(x+1,y)$.

$$\mathcal{C}:=\{C_1,\ C_2,\ C_0,\ C_0'\}.$$

**Closure under $\mathcal{G}$.** $\mathrm{id}_*C=C$ for every $C$ by Observation 3.17.1. $\jmath_*C_1=C_2$ and $\jmath_*C_0=C_0'$ by construction. Since $\jmath$ is an involution, Observation 3.17.1 gives $\jmath_*C_2=\jmath_*\jmath_*C_1=(\jmath\circ\jmath)_*C_1=\mathrm{id}_*C_1=C_1$, and likewise $\jmath_*C_0'=C_0$. Hence $\iota_*C\in\mathcal{C}$ for every $\iota\in\mathcal{G}$ and $C\in\mathcal{C}$, so $\mathbb{T}$ is a theory instance.

**Significance values.** All contrasts are total and all profiles are Dirac, so $\rho^{\mathrm{at}}$ returns the atom:
$$\sigma_{C_1}(b_1)=2,\quad \sigma_{C_1}(b_2)=1,\quad \sigma_{C_2}(b_1)=1,\quad \sigma_{C_2}(b_2)=2,\quad \sigma_{C_0}(b_i)=0,\quad \sigma_{C_0'}(b_i)=0.$$

**Satisfaction.**
*FR-1* — every context supplies all seven components; $\approx=\bot_{\mathrm{abs}}$ is a supplied optional value.
*A3* — for $\iota=\mathrm{id}$ the equation is trivial. For $\iota=\jmath$, with $\widehat{\jmath_W}=\mathrm{id}$, the required equations $\sigma_{\jmath_*C}(\jmath_{\mathfrak{B}}b)=\sigma_C(b)$ are:
 $(C_1,b_1)$: $\sigma_{C_2}(b_2)=2=\sigma_{C_1}(b_1)$. $(C_1,b_2)$: $\sigma_{C_2}(b_1)=1=\sigma_{C_1}(b_2)$.
 $(C_2,b_1)$: $\sigma_{C_1}(b_2)=1=\sigma_{C_2}(b_1)$. $(C_2,b_2)$: $\sigma_{C_1}(b_1)=2=\sigma_{C_2}(b_2)$.
 $(C_0,b_i)$: $\sigma_{C_0'}(\jmath_{\mathfrak{B}}b_i)=0=\sigma_{C_0}(b_i)$. $(C_0',b_i)$: $\sigma_{C_0}(\jmath_{\mathfrak{B}}b_i)=0=\sigma_{C_0'}(b_i)$.
 All eight non-identity instances hold, and $\jmath\neq\mathrm{id}$, so **the check is not vacuous**.
*A4* — $C_0\in\mathcal{C}$ has $W$ of class $\mathsf{W}_1$ and $\sigma_{C_0}(b_i)=0_W$ for both bearers.
*A5* — every value lies in $W\subseteq\widehat W$, assigned by Definition 5.3, row four.
*A7* — all values lie in $\widehat W$; no cross-context comparison is performed.
*A8* — vacuous, since $\approx=\bot_{\mathrm{abs}}$ in every context.
*A9* — every $\Omega^b_C=\mathfrak{M}\neq\emptyset$.
*A10* — $r=\mathrm{id}$, so every fibre is a singleton and none is empty. $\blacksquare$

**Observation 11.1.1 — remediates FV-004 and FV-005.** The prior witness asserted $\jmath_*C_0=C_0$. That is **false**: transporting $C_0$ by the coordinate swap yields outcome map $y$ and operations shifting $x$, which are the components of neither $C_0$ nor $C_1$ nor $C_2$. The repair adds $C_0':=\jmath_*C_0$ to $\mathcal{C}$ and **proves** closure using involutivity rather than asserting a false equality. The fragment declaration now also names **Definitions 5.1–5.3**, on which the proof depends and which the prior declaration omitted.

**Observation 11.1.2 (Scope of the claim — binding).** Proposition 11.1′ establishes consistency of **exactly** the deterministic core signature and axioms named in its claim, over the declared instance. It does **not** establish consistency for anything in Part B, nor for interval- or bottom-valued outputs, nontrivial $\approx_C$, non-atomic measures, non-point-separating codomains, or codomains outside class $\mathsf{W}_1$. **The consistency claim does not exceed the witness.**

---

## A.10 Deterministic results, limitations and rejections

### A.10.1 Verified deterministic results

| № | Statement | Quantifier | § |
|---|---|---|---|
| 1 | Order reversal exists between two contexts | existential | A.4 |
| 3 | Measurable factorisation iff fibre-constant | universal | A.6 |
| 3.2′ | Under totality, non-fibre-constancy forces a non-singleton identified set | existential in $x$ | A.6 |
| 3.3 | Induced outcome map iff fibre-constant | universal | A.6 |
| 4′ | Partial quotient descent on $\bar D_C$ | universal | A.6 |
| 6.2 | Fixed-context orbit constancy | universal | A.5 |
| 7′ | Additive context-free scalar vanishes on a nullity-closed family | universal | A.7 |
| 9 | Arena dependence of normalisation | universal | A.7 |
| 10″ | Encodability on point-separating codomains | existential in $C$ | A.8 |
| 11.1′ | Consistency of the deterministic core | existential | A.9 |

### A.10.2 What the deterministic core does **not** establish

**A.10.2.1 — remediates FV-006. The core does not exclude intrinsic significance.** Writing $\sigma$ as a function of $(C,b)$ does not prevent it from being constant in its first argument. The assignment $\sigma_C(b)=0$ for every $C$ and every $b$ is context-independent, satisfies A4, and is excluded by no Part A axiom. No non-formal design principle is available to close the gap, since none may be cited in a proof. **The earlier rejection of intrinsic significance is withdrawn, and no Part A result replaces it.**

**A.10.2.2.** No universal absence of a context-free ordering is established. Theorem 1 is existential.

**A.10.2.3.** No conclusion about the empirical content of the framework as a whole is drawn (Observation 10.1.1).

**A.10.2.4.** No computability, minimality, novelty, prior-art or recognisability result is established.

### A.10.3 Deterministic limitations

**14.4.** The reduction $\rho_C$ is primitive and is not determined by the theory. *(The earlier claim that distinct reductions always induce distinct orderings on asymmetric profiles is withdrawn: distinct positive rescalings induce the same ordering.)*

**14.7.** Absent a declared transport (Definition 8.9), values under distinct contexts are not compared. This is the A7 stipulation, and A7 expressly permits comparison through a declared transport.

**14.11′ — narrowed under FV-003 and FV-006.** On a **point-separating** codomain, within the deterministic contrast form and with unrestricted evaluators, no single-context assignment is excluded (Corollary 10.1″). Nothing follows for non-point-separating codomains, for other forms, or for joint assignments across $\mathcal{C}$.

**14.12′ — narrowed under FV-004.** Consistency is established for exactly the deterministic core signature over the instance of Proposition 11.1′, and for nothing else.

### A.10.4 Deterministic rejected formulations

Retained only where entailed by a Part A result or by inspection of the Part A signature.

**16.12.** *Values under distinct contexts may be compared without a declared transport.* — A7 with Definition 8.9.

**16.16.** *The framework derives its evaluator automatically.* — By inspection: $T_C$, $\delta_C$ and $\rho_C$ are primitives of Definition 3.10, and no construction produces them from $\mu_C$.

**16.17.** *A context-free ordering primitive exists in this signature.* — By inspection: no such component is declared. *(A statement about the signature only. It does **not** exclude a context-independent significance function — see A.10.2.1.)*

**16.18.** *This document claims novelty.* — No novelty claim is made, and no universal prior-art subsumption is claimed.

**16.19.** *Significance-first intelligence is a statement of this theory.* — The phrase occurs in no Part A definition, axiom or theorem.

**Withdrawn in this pass — FV-006.**
**16.1** (*rejection of intrinsic significance*) — **withdrawn**; see A.10.2.1. The counterexample $\sigma\equiv0$ is context-independent and compatible with A4.
**16.13** (*artefact independence*) — **withdrawn as stated**, since "artefact relabelling" and "declared universe" are not defined in the signature. What survives is exactly Corollary 6.2 — fixed-context orbit constancy for $\mathrm{Aut}(C)$ — and nothing more.

---

## A.11 Deterministic open obligations

**OB-A1.** A structural characterisation of fibre-constancy.
**OB-A2.** Conditions on $M_C$, $\tau$ and $\delta_C$ beyond those of Definition 5.1 that guarantee measurability of $\delta^{\,b}_C$ in wider settings.
**OB-A3.** Whether a deterministic encodability theorem holds for codomains that are not point-separating, or whether point separation is necessary as well as sufficient.

**OB-A4.** Whether the representation component $\mathsf{r}$ should be required $\mathcal{G}$-equivariant, i.e. whether an instance should carry $\iota_{\mathcal{R}}$ with $r\circ\iota_{\mathfrak{M}}=\iota_{\mathcal{R}}\circ r$. **No Part A statement couples $\mathsf{r}$ and $\mathcal{G}$**: A3 does not mention $r$, and A10 and Definitions 7.1–7.7 do not mention $\mathcal{G}$. Equivariance is therefore not required for well-typedness and is not imposed.

**OB-A5.** Formal placement, within Part B, of the heterogeneous context-indexed carriers and indexed action removed from Version 1 by Observation 3.14.2. Deferred because the adopting pass was not authorised to modify Part B.

**None of OB-A1 – OB-A5 blocks the deterministic core**, and none is used by any Part A theorem.

---

# PART B — CANDIDATE ENRICHMENTS

**Status of every item in Part B: Candidate · non-frozen · not required by the deterministic core · outside the consistency claim of Proposition 11.1′ · outside any Version 1 verification claim.**

**No Part A definition, axiom, theorem, proof or limitation depends on any item below.** Every Part A proof cites only Part A objects.

## B.1 Design principles — non-formal, not usable in any proof

**DP-1 (Candidate).** Significance is intended as a valuation of a comparison between a factual and an operated outcome, not as a property of a bearer alone.
**DP-2 (Candidate).** Uncertainty is intended to be carried by a single joint measure, with marginals and conditionals derived.

**Observation B.1.1.** These are not predicates over the signature. No proof in Part A or Part B cites them. Formalising them, or showing neither is needed, is **OB-B1**.

## B.2 Further codomain classes

**Definition B.2.1 (Class $\mathsf{W}_2$, signed) — Candidate.** A codomain additionally carrying $(+,0_W,-)$ making $(W,+,0_W,\preceq_W)$ an ordered abelian group; $0_W$ is **not** least.

**Definition B.2.2 (Class $\mathsf{W}_2^{\mathrm{m}}$, measurably signed) — Candidate.** Class $\mathsf{W}_2$ with $(y,y')\mapsto y'-y$ measurable.

**Observation B.2.3 (Candidate).** Class $\mathsf{W}_2$ does not imply measurable subtraction: $\mathbb{R}$ with the countable–cocountable $\sigma$-algebra has every singleton measurable, yet the diagonal is not product-measurable, so subtraction is not measurable. **No Part A theorem uses subtraction.**

## B.3 Decision and evidence structure

**Definition B.3.1 (Decision problem) — Candidate.** $(\mathcal{A}_C,L_C)$ with $\mathcal{A}_C\neq\emptyset$ and $L_C(\alpha,\cdot)$ measurable and integrable at every measure at which it is used.

**Definition B.3.2 (Regular evidence structure) — Candidate.** $(\mathcal{E}_b,K_b,\Pi_b)$ with $K_b$ a Markov kernel, $\Pi_b$ a **regular** conditional probability satisfying the barycentre identity $\int\Pi_b(\cdot\mid e)\,\lambda_b(de)=\mu_C$, and $e\mapsto\mathfrak{r}(\Pi_b(\cdot\mid e))$ measurable and $\lambda_b$-integrable.

**Definitions B.3.3–B.3.5 (Three significance forms) — Candidate.** Effect significance on a metric outcome space with a location functional; decision significance via $\mathfrak{r}(\nu)=\inf_\alpha\mathbb{E}_\nu L_C(\alpha,\cdot)$ and $\varepsilon$-optimal sets, with $\varepsilon=0$ requiring attainment; information significance as the expected Bayes-risk reduction under a regular evidence structure.

**Theorem B.3.6 (Non-negativity) — Candidate.** Under the above with the stated integrability hypotheses, all three forms are non-negative. Proofs: support non-negativity for the first; optimality of the infimum, which requires no attainment, for the second; concavity of $\mathfrak{r}$ with Jensen and the barycentre identity for the third.

**Theorem B.3.7 (Pairwise non-equivalence) — Candidate.** With $\rho=$ the mean, $\varepsilon=0$ with attainment, and three complete contexts, the three forms disagree pairwise in the order they induce on two bearers.

**Observation B.3.8 (Candidate).** No claim that the three forms lack a common latent order is made; that would require a formal hypothesis on admissible measurement maps, which is not supplied.

## B.4 Information-theoretic lemma

**Theorem B.4.1 (Conditional information redundancy) — Candidate.** For random elements $Z$, $R$ on a common space and $S=f(R)$ with $f$ measurable: $I(Z;S,R)=I(Z;R)$ and $I(Z;S\mid R)=0$.

**Observation B.4.2 (Candidate).** This does **not** show a derived summary is uninformative: with $Z=R=S$ a non-degenerate Bernoulli variable, $I(Z;S)=H(Z)>0$. Only redundancy conditional on simultaneous access to $R$ follows.

## B.5 Composition signature

**Definition B.5.1 (Composition signature) — Candidate.** $(U,E,\mathrm{src},\mathrm{tgt},t,\kappa,\odot,w)$ with $\mathrm{src},\mathrm{tgt}:E\to U$; $\kappa$ restricted to endpoint-compatible pairs; $\odot:\kappa\to E$ **primitive** and endpoint-coherent; $w:E\to\mathbb{R}_{\ge0}$. Paths are nonempty finite sequences with matching endpoints; empty paths are not admitted.

**Theorem B.5.2 (Type-level licensing dichotomy) — Candidate.** If $\kappa$ is not a function of types alone, every predicate on $T\times T$ is unsound or incomplete as a test for membership in $\kappa$. **Conditional on that hypothesis**: where $\kappa$ *is* exactly type-determined, type-level licensing is sound and complete.

**Theorem B.5.3 (An instance-level non-associative composition exists) — Candidate.** With $U=\{u_0,\dots,u_3\}$, $E=\{e_1,e_2,e_3,a,q\}$, endpoints $e_1:u_0\to u_1$, $e_2:u_1\to u_2$, $e_3:u_2\to u_3$, $a:u_0\to u_2$, $q:u_1\to u_3$, $\kappa=\{(e_1,e_2),(e_2,e_3),(e_1,q)\}$ and $e_1\odot e_2:=a$, $e_2\odot e_3:=q$, $e_1\odot q:=a$: $(e_1\odot e_2)\odot e_3$ is undefined while $e_1\odot(e_2\odot e_3)=a$ is defined. **Existential only** — some paths and some operations are bracketing-independent.

**Theorem B.5.4 (Diffusion and composition can disagree) — Candidate.** On a five-instance signature with $U=\{a,b,c,c',z\}$, the total diffusion weight from $a$ to $z$ exceeds that from $b$ to $z$ while every $a\to z$ path composes to $\bot_{\mathrm{und}}$ and some $b\to z$ path composes. Path sets are finite by inspection of the endpoint maps.

**Observation B.5.5 (Candidate).** Diffusion semantics is total on any signature. The assertion that path functionals are invalid under non-transitivity is **false**; the constraint is on interpretation, not on the value.

**Observation B.5.6 (Candidate).** No recognisability, state-count, decidability or prior-art subsumption claim is made. The earlier claims of that kind were withdrawn and are not reinstated.

## B.6 Candidate open obligations

**OB-B1.** Formalise DP-1 and DP-2, or show neither is needed.
**OB-B2.** Conditions guaranteeing existence of a regular evidence structure on given spaces.
**OB-B3.** Consistency of any Part B enrichment, jointly or severally. **Not covered by Proposition 11.1′.**
**OB-B4.** Whether a composition signature admits an associative $\odot$; and whether any invariant of it exceeds existing formalisms. **Open; no closure is claimed.**

---

*End of ASTRO-THEORY-0001. Part A is the Version 1 Deterministic Core Candidate; Part B is Candidate Enrichments. Not frozen. Not verified. Awaiting final independent re-verification.*
