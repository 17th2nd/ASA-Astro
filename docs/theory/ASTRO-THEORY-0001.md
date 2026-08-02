# ASTRO-THEORY-0001 — Contextual Difference Theory

| Field | Value |
|---|---|
| Status | **Theory Candidate.** Not frozen in this pass. |
| Structure | **Part A — Version 1 Deterministic Core Candidate** · **Part B — Candidate Enrichments** |
| Verification | Not externally verified. The prior edition was independently examined for freeze and returned **NOT READY FOR VERSION 1** on the single blocking defect **FFV-001** — Definition 7.7 was not a complete definition. That examination established no contradiction, no failed witness, no theorem exceeding its proof and no Part B dependency. This edition closes FFV-001 and awaits re-verification. |
| Empirical status | Not empirically validated. Evidence level `EH-0`. |
| Novelty | No novelty is claimed. No universal prior-art subsumption is claimed. No minimality is claimed. |
| Prior edition | Blob `6fc866796b0a9c39d3f7384d4118fce8ee7ae5ac`. Not silently overwritten; every change is mapped in `verification/ASTRO-THEORY-0001-FFV-001-CHANGE-MAP.md`. |

**Freeze boundary.** Part A is self-contained: **no Part A definition, axiom, theorem or proof depends on anything in Part B.** Part B is Candidate, non-frozen, not required by the deterministic core, outside the consistency claim, and outside any Version 1 verification claim.

**What changed in this pass — micro-remediation of one defect only.** **Definition 7.7 is withdrawn** (Observation 7.7.1) and removed from the signature of Proposition 11.1′, closing **FFV-001**. It named four notions and defined three of them not at all: minimal sufficiency, a distinguishability indicator and an equality partition had no symbol, domain, codomain or rule, while its fourth notion merely duplicated Definition 7.4. **Sufficiency is retained, unchanged, in Definition 7.4.** The three undefined notions are **not part of Version 1** and are deferred as **OB-A7**.

**Nothing else changed.** No axiom, theorem, proof, witness calculation, codomain structure, transport rule or representation component was touched, and Part B is byte-identical. The non-blocking observation FFV-NB-001 — a surplus $\mathsf{r}=\bot_{\mathrm{abs}}$ hypothesis in Theorem 1 — is **deliberately not corrected here**, being outside the authorised scope of a single-defect pass.

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

**Definition 3.5 (Codomain carrier) — primitive.** A triple $(W,\preceq_W,\Sigma_W)$: a nonempty set, a partial order on it, and a $\sigma$-algebra on it. This triple carries **no** algebraic structure; additional structure is never implicit and is supplied only by the class datum of Definition 3.6.

**Definition 3.5.1 (Point-separating carrier) — derived.** A codomain carrier $(W,\preceq_W,\Sigma_W)$ is *point-separating* if for all $x\neq y$ in $W$ there is $A\in\Sigma_W$ with $x\in A$ and $y\notin A$. This is a property of the carrier alone and is **independent of the class datum** of Definition 3.6.

**Observation 3.5.2 — remediates FV-003.** Point separation is equivalent to injectivity of $x\mapsto\delta_x$ from $W$ into $\Delta(W)$. If some $A\in\Sigma_W$ separates $x$ from $y$ then $\delta_x(A)=1\neq0=\delta_y(A)$; conversely if no measurable set separates them then $\delta_x$ and $\delta_y$ agree on every measurable set. Borel $\mathbb{R}_{\ge0}$ is point-separating; a two-point set with the trivial $\sigma$-algebra $\{\emptyset,W\}$ is not.

**Definition 3.6 (Codomain object) — primitive. Remediates TR-2.** A *codomain object* is a pair
$$\mathbb{W}=\big((W,\preceq_W,\Sigma_W),\ \mathsf{c}\big)$$
of a codomain carrier (Definition 3.5) and a **codomain-class datum** $\mathsf{c}$, which is **exactly one** of:

- $\mathsf{c}=\mathsf{W}_1(\oplus,0_W)$ — a **selected** binary operation $\oplus:W\times W\to W$ and a **selected** element $0_W\in W$ satisfying, for all $x,y,z\in W$:
 **(M1)** $(x\oplus y)\oplus z=x\oplus(y\oplus z)$; **(M2)** $x\oplus y=y\oplus x$; **(M3)** $x\oplus 0_W=x$; **(M4)** $x\preceq_W y\Rightarrow x\oplus z\preceq_W y\oplus z$; **(M5)** $0_W\preceq_W x$.
 Equivalently, $(W,\oplus,0_W,\preceq_W)$ is an ordered commutative monoid with $0_W$ least. Such an object is *of class $\mathsf{W}_1$* (*magnitude*).
- $\mathsf{c}=\bot_{\mathrm{abs}}$ — the **typed absence** of additional algebraic structure. Such an object is *of class $\mathsf{W}_0$*.

Write $W(\mathbb{W})$, $\preceq_{\mathbb{W}}$, $\Sigma_{\mathbb{W}}$ and $\mathsf{c}(\mathbb{W})$ for the components; where no ambiguity arises the carrier is written $W$.

**Observation 3.6.1 (Selection is a datum, not a property) — remediates TR-2.** One carrier triple may admit many operations satisfying **(M1)–(M5)**, and admits none of them canonically. The class datum therefore records **which** structure is selected, so that "preserves the class-$\mathsf{W}_1$ structure" (Definition 3.15) and "$\sigma_C(b)=0_W$" (A4) denote a determinate condition on a determinate instance. A codomain object of class $\mathsf{W}_0$ has no $\oplus$ and no $0_W$, and no Part A statement may refer to either for such an object.

**Observation 3.6.2 (Which laws Part A actually uses).** No Part A proof invokes **(M1)–(M5)** abstractly. A4 uses only the selected element $0_W$; Definition 3.15 uses only the pair $(\oplus,0_W)$ as the target of a preservation condition; Theorem 1, Theorem 7′ and Proposition 11.1′ each declare the concrete realisation $(\mathbb{R}_{\ge0},\le,\mathcal{B}(\mathbb{R}_{\ge0}))$ with $\mathsf{c}=\mathsf{W}_1(+,0)$, for which **(M1)–(M5)** hold by ordinary arithmetic. The laws are stated so that the class is a determinate condition, not because a proof below discharges them abstractly.

**Definition 3.7 (Order-intervals) — derived.** $\mathcal{I}(W):=\{[u,v]:u,v\in W,\ u\preceq_W v\}$ where $[u,v]=\{x\in W:u\preceq_W x\preceq_W v\}$.

**Definition 3.8 (Output codomain) — derived.** $\widehat{W}:=W\sqcup\mathcal{I}(W)\sqcup\{\bot_{\mathrm{ind}},\bot_{\mathrm{inc}},\bot_{\mathrm{und}}\}$, a disjoint union. It is the carrier of deterministic significance (Definition 5.3, A5) and of nothing else. **$\widehat W$ contains no subset of $W$ other than the order-intervals $\mathcal{I}(W)$**, and is **not** extended anywhere below.

**Definition 3.8.1 (Identified-output carrier) — derived. Remediates TR-4.** $$\widehat{W}^{\mathrm{id}}:=\mathcal{P}_{\neq\emptyset}(W)\ \sqcup\ \{\bot_{\mathrm{inc}},\bot_{\mathrm{und}}\},$$ a disjoint union of the set of **nonempty** subsets of $W$ with two bottoms. It is the carrier of the identified-output function (Definition 7.5) and of nothing else.

**Observation 3.8.2 (The two output carriers are distinct) — remediates TR-4.** $\widehat W$ and $\widehat{W}^{\mathrm{id}}$ are different declared objects and neither is a subobject of the other: $\widehat W$ carries points, intervals and three bottoms; $\widehat{W}^{\mathrm{id}}$ carries arbitrary nonempty subsets and two bottoms. No Part A statement places an identified output in $\widehat W$, and no Part A statement places a significance value in $\widehat{W}^{\mathrm{id}}$. In particular the set-valued output of Definition 7.5 is **not** smuggled into $\widehat W$, and $\widehat W$ is not extended to receive it.

**Definition 3.9 (Absent value) — primitive.** A symbol $\bot_{\mathrm{abs}}$, the value of an optional component deliberately not supplied. Distinct from $\bot_{\mathrm{und}}$.

### A.2.3 Contexts

**Definition 3.10 (Context) — primitive.** Over a fixed $\mathfrak{B}$ and $(\mathfrak{M},\mathcal{F})$, a context is the seven-tuple
$$C=\big(\mu_C,\ (\mathcal{Y}_C,\mathcal{G}_C),\ M_C,\ T_C,\ \approx_C,\ \delta_C,\ (\mathbb{W}_C,\rho_C)\big)$$
where $\mathbb{W}_C$ is a **codomain object** (Definition 3.6). Write $W_C:=W(\mathbb{W}_C)$, $\preceq_{W_C}$, $\Sigma_{W_C}$ and $\mathsf{c}_C:=\mathsf{c}(\mathbb{W}_C)$ for its components.

| Component | Type | Mark |
|---|---|---|
| $\mu_C$ | probability measure on $(\mathfrak{M},\mathcal{F})$ | required |
| $(\mathcal{Y}_C,\mathcal{G}_C)$ | measurable outcome space | required, context-indexed |
| $M_C:\mathfrak{M}\to\mathcal{Y}_C$ | measurable, total | required |
| $T_C:\mathfrak{B}\rightharpoonup\mathrm{Op}(\mathfrak{M})$ | operation assignment | required, **partial** |
| $\approx_C$ | equivalence on $\mathcal{Y}_C$, or $\bot_{\mathrm{abs}}$ | optional |
| $\delta_C:\mathcal{Y}_C\times\mathcal{Y}_C\rightharpoonup W_C$ | measurable on its domain $D_C\in\mathcal{G}_C\otimes\mathcal{G}_C$ | required, **partial** |
| $(\mathbb{W}_C,\rho_C)$ | codomain object (Definition 3.6) and reduction | required; fixed to the frame's codomain object by Definition 3.18 clause 3 |

**Definition 3.11 (Reduction) — primitive, partial.** $\rho_C:\Delta(W_C)\rightharpoonup\widehat{W_C}$, where $\Delta(W_C)$ is the set of probability measures on $(W_C,\Sigma_{W_C})$.

**Definition 3.12 (Location functional) — derived.** For $\mathbb{W}_C$ realised as the carrier $(\mathbb{R}_{\ge0},\le,\mathcal{B}(\mathbb{R}_{\ge0}))$ with class datum $\mathsf{c}_C=\mathsf{W}_1(+,0)$, a *location functional* is a partial $\ell:\Delta(\mathbb{R}_{\ge0})\rightharpoonup\mathbb{R}_{\ge0}$ with $\inf\operatorname{supp}\nu\le\ell(\nu)\le\sup\operatorname{supp}\nu$ where defined, and $\ell(\delta_x)=x$.

**Definition 3.12.1 (Atom reduction) — derived, partial.** For a **point-separating** carrier $W$, the *atom reduction* $\rho^{\mathrm{at}}:\Delta(W)\rightharpoonup W$ has domain $\{\delta_x:x\in W\}$ and $\rho^{\mathrm{at}}(\delta_x)=x$. It is a well-defined function by Observation 3.5.2.

**Observation 3.12.2 — remediates FV-003.** On a carrier that is not point-separating the atom reduction is **not** a function: one measure would have to be sent to two distinct atoms. Every use of $\rho^{\mathrm{at}}$ below declares point separation.

### A.2.4 Representation morphisms

**Definition 3.14.1 (Homogeneous frame) — primitive. Remediates DCV-001, TR-2.** A *frame* is a quadruple
$$\mathbb{F}=\big(\mathfrak{B},\ (\mathfrak{M},\mathcal{F}),\ (\mathcal{Y},\mathcal{G}_{\mathcal{Y}}),\ \mathbb{W}\big)$$
consisting of a bearer set, a measurable model space, **one** measurable outcome space and **one codomain object** $\mathbb{W}=((W,\preceq_W,\Sigma_W),\mathsf{c})$ in the sense of Definition 3.6 — carrier **and** selected class datum. **Version 1 is homogeneous:** every context of a theory instance uses the frame's outcome space and the frame's codomain object, class datum included.

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
| $\iota_W$ | $\mathbb{W}$ | $\mathbb{W}$ | automorphism of the codomain object, in the exact sense of (W-a)–(W-c) below |

**Codomain-object automorphism — remediates TR-2.** $\iota_W:W\to W$ is an *automorphism of $\mathbb{W}$* iff

**(W-a)** it is an order isomorphism: a bijection with $x\preceq_W y\iff\iota_W x\preceq_W\iota_W y$;
**(W-b)** it is a measurable isomorphism: $\iota_W$ and $\iota_W^{-1}$ are $\Sigma_W/\Sigma_W$-measurable;
**(W-c)** it preserves **exactly the selected class datum** $\mathsf{c}$ — that is,
 — if $\mathsf{c}=\mathsf{W}_1(\oplus,0_W)$: $\iota_W(x\oplus y)=\iota_W(x)\oplus\iota_W(y)$ for all $x,y\in W$, and $\iota_W(0_W)=0_W$;
 — if $\mathsf{c}=\bot_{\mathrm{abs}}$: **no** further condition.

Condition (W-c) is determinate because $\mathsf{c}$ is a component of $\mathbb{W}$ and hence of the instance. It is neither vacuous nor over-strong: nothing beyond the selected datum must be preserved, and the selected datum must be preserved exactly.

Write $\mathrm{Mor}(\mathbb{F})$ for the set of these.

**Observation 3.15.1 (Group laws) — remediates DCV-001.** Every component of Definition 3.15 has the **same source and target**, so componentwise composition and componentwise inverse are defined without further data.
*Identity.* $\mathbf{1}:=(\mathrm{id}_{\mathfrak{B}},\mathrm{id}_{\mathfrak{M}},\mathrm{id}_{\mathcal{Y}},\mathrm{id}_W)\in\mathrm{Mor}(\mathbb{F})$.
*Composition.* $(\iota\circ\kappa)$ is defined componentwise and lies in $\mathrm{Mor}(\mathbb{F})$: a composite of bijections is a bijection, of bimeasurable bijections is bimeasurable, and of codomain-object automorphisms is a codomain-object automorphism — (W-a) and (W-b) compose, and under $\mathsf{c}=\mathsf{W}_1(\oplus,0_W)$ so does (W-c), since $\iota_W\kappa_W(x\oplus y)=\iota_W(\kappa_Wx\oplus\kappa_Wy)=\iota_W\kappa_Wx\oplus\iota_W\kappa_Wy$ and $\iota_W\kappa_W(0_W)=0_W$.
*Inverse.* $\iota^{-1}$ is defined componentwise and lies in $\mathrm{Mor}(\mathbb{F})$, since each component class is closed under inverse; for (W-c) under $\mathsf{c}=\mathsf{W}_1(\oplus,0_W)$, applying $\iota_W^{-1}$ to $\iota_W(\iota_W^{-1}x\oplus\iota_W^{-1}y)=x\oplus y$ gives $\iota_W^{-1}(x\oplus y)=\iota_W^{-1}x\oplus\iota_W^{-1}y$, and $\iota_W(0_W)=0_W$ gives $\iota_W^{-1}(0_W)=0_W$. Under $\mathsf{c}=\bot_{\mathrm{abs}}$ there is nothing to check.
*Associativity and unit laws* hold componentwise because composition of functions is associative with the identity as unit.
Hence $\mathrm{Mor}(\mathbb{F})$ is a group, and $\mathcal{G}$ of Definition 3.18 is a subgroup of it. $\square$

**Definition 3.16 (Extended action) — derived. Remediates TR-1.** Let $\iota\in\mathrm{Mor}(\mathbb{F})$, so that $\iota_W:W\to W$ is an automorphism of the frame's codomain object $\mathbb{W}$ (Definition 3.15). The *extended action* is the map
$$\widehat{\iota_W}:\widehat W\longrightarrow\widehat W$$
**on the fixed $\widehat W$ of Definition 3.8**, defined by cases on the three summands of that disjoint union:

| Summand | Value |
|---|---|
| $x\in W$ | $\widehat{\iota_W}(x):=\iota_W(x)\in W$ |
| $[u,v]\in\mathcal{I}(W)$ | $\widehat{\iota_W}([u,v]):=[\iota_Wu,\iota_Wv]\in\mathcal{I}(W)$ |
| $\bot_{\mathrm{ind}},\bot_{\mathrm{inc}},\bot_{\mathrm{und}}$ | fixed: $\widehat{\iota_W}(\bot_\bullet):=\bot_\bullet$ for each of the three bottoms |

**Source and target are both $\widehat W$.** No second codomain is introduced, posited or referred to anywhere in Version 1; the symbol $W'$ of the prior edition was unbound and is removed.

**Observation 3.16.1 (The extended action is well defined and functorial) — remediates TR-1.**

*(a) Totality and case-disjointness.* Definition 3.8 is a disjoint union, so every element of $\widehat W$ lies in exactly one summand and exactly one row applies. Hence $\widehat{\iota_W}$ is a total function on $\widehat W$.

*(b) Well-definedness on intervals.* An interval $[u,v]$ is a **set**, so the middle row must not depend on the chosen endpoints. It does not: since $u\preceq_Wv$, both $u,v\in[u,v]$, and $u$ is the least and $v$ the greatest element of $[u,v]$ under $\preceq_W$. Least and greatest elements are unique by antisymmetry, so the pair $(u,v)$ is recovered from the set $[u,v]$ and the assignment is representation-independent.

*(c) The value lies in the target.* $\iota_W(x)\in W$ by (W-a). For an interval, (W-a) gives $u\preceq_Wv\Rightarrow\iota_Wu\preceq_W\iota_Wv$, so $[\iota_Wu,\iota_Wv]\in\mathcal{I}(W)$ by Definition 3.7. The bottoms are fixed. Hence $\widehat{\iota_W}(\widehat W)\subseteq\widehat W$.

*(d) Identity.* $\widehat{\mathrm{id}_W}=\mathrm{id}_{\widehat W}$: it is $\mathrm{id}_W$ on $W$; on intervals $[u,v]\mapsto[u,v]$; and each bottom is fixed by definition.

*(e) Composition.* $\widehat{\iota_W\circ\kappa_W}=\widehat{\iota_W}\circ\widehat{\kappa_W}$. On $W$ both sides are $\iota_W\kappa_W$. On $\mathcal{I}(W)$, $[u,v]\mapsto[\iota_W\kappa_Wu,\iota_W\kappa_Wv]$ on both sides, using (c) to see that the intermediate value $[\kappa_Wu,\kappa_Wv]$ is again an interval with those endpoints, which by (b) are the ones the outer map reads. On each bottom both sides are the identity.

*(f) Inverse.* $\widehat{(\iota_W)^{-1}}=\big(\widehat{\iota_W}\big)^{-1}$, by (d) and (e) applied to $\iota_W\circ\iota_W^{-1}=\iota_W^{-1}\circ\iota_W=\mathrm{id}_W$. In particular $\widehat{\iota_W}$ is a bijection of $\widehat W$.

*(g) Consequences.* By (d), $\widehat{\pi_W}=\mathrm{id}_{\widehat W}$ whenever $\pi_W=\mathrm{id}_W$, which is what the proof of **Corollary 6.2** uses. By (e) and (f), the reduction transport $\rho_{\iota_*C}=\widehat{\iota_W}\circ\rho_C\circ((\iota_W)^{-1})_*$ of Definition 3.17 has target $\widehat W$, and the functoriality of Observation 3.17.1 holds in the reduction slot. Both sides of **A3** are therefore elements of the one declared set $\widehat W$. $\square$

**Definition 3.17 (Transported context) — derived.** $\iota_*C$ has
$$\mu_{\iota_*C}=(\iota_{\mathfrak{M}})_*\mu_C,\qquad M_{\iota_*C}=\iota_{\mathcal{Y}}\circ M_C\circ\iota_{\mathfrak{M}}^{-1},\qquad T_{\iota_*C}(\iota_{\mathfrak{B}}b)=\iota_{\mathfrak{M}}\circ T_C(b)\circ\iota_{\mathfrak{M}}^{-1},$$
$$\approx_{\iota_*C}=\bot_{\mathrm{abs}}\ \text{if}\ \approx_C=\bot_{\mathrm{abs}},\ \text{else}\ \{(\iota_{\mathcal{Y}}y,\iota_{\mathcal{Y}}y'):y\approx_Cy'\},$$
$$\delta_{\iota_*C}=\iota_W\circ\delta_C\circ(\iota_{\mathcal{Y}}^{-1}\times\iota_{\mathcal{Y}}^{-1}),\qquad \rho_{\iota_*C}=\widehat{\iota_W}\circ\rho_C\circ((\iota_W)^{-1})_*.$$
The carriers are unchanged: $(\mathcal{Y}_{\iota_*C},\mathcal{G}_{\iota_*C})=(\mathcal{Y},\mathcal{G}_{\mathcal{Y}})$ and $\mathbb{W}_{\iota_*C}=\mathbb{W}$ — the **whole codomain object, class datum included** — because $\iota_{\mathcal{Y}}$ is an automorphism of the frame's fixed outcome space and $\iota_W$ is an automorphism of the frame's fixed codomain object, preserving $\mathsf{c}$ exactly by (W-c).

**Observation 3.17.0 (Transport is well typed) — remediates DCV-001.** Every displayed component of $\iota_*C$ is a composite of maps whose sources and targets are declared by Definition 3.15 and the frame: $M_{\iota_*C}:\mathfrak{M}\to\mathcal{Y}$; $T_{\iota_*C}(b'):\mathfrak{M}\to\mathfrak{M}$; $\delta_{\iota_*C}:\mathcal{Y}\times\mathcal{Y}\rightharpoonup W$; and $\rho_{\iota_*C}:\Delta(W)\rightharpoonup\widehat W$, since $((\iota_W)^{-1})_*:\Delta(W)\to\Delta(W)$ is pushforward along a measurable isomorphism, $\rho_C:\Delta(W)\rightharpoonup\widehat W$, and $\widehat{\iota_W}:\widehat W\to\widehat W$ by Definition 3.16 — the composite therefore lands in $\widehat W$ and in no other set. Hence $\iota_*C$ is a context over the same frame, and the predicate $\iota_*C\in\mathcal{C}$ of Definition 3.18 is evaluable **before** any closure requirement is imposed. Under the prior edition it was not, because $\iota_{\mathcal{Y}}$ and $\iota_W$ had no declared source or target.

**Observation 3.17.1 (Functoriality).** $(\mathrm{id})_*C=C$ and $(\iota\circ\kappa)_*C=\iota_*(\kappa_*C)$.
*Proof.* Each component of Definition 3.17 is built from $\iota_{\mathfrak{B}},\iota_{\mathfrak{M}},\iota_{\mathcal{Y}},\iota_W$ by composition and inverse; composition of bijections is associative and the identity acts trivially in each slot. $\square$
This is used by the closure argument of Proposition 11.1′.

### A.2.5 Theory instance

**Definition 3.18 (Theory instance) — primitive. Remediates FV-001, DCV-001, DCV-002, TR-2, TR-4.** A *theory instance* is the seven-component tuple
$$\mathbb{T}=\big(\underbrace{\mathfrak{B},\ (\mathfrak{M},\mathcal{F}),\ (\mathcal{Y},\mathcal{G}_{\mathcal{Y}}),\ \mathbb{W}}_{\text{frame }\mathbb{F}},\ \ \mathsf{r},\ \ \mathcal{C},\ \ \mathcal{G}\big),
\qquad \mathbb{W}=\big((W,\preceq_W,\Sigma_W),\ \mathsf{c}\big),$$
subject to:

1. **Frame.** $\mathbb{F}$ is a homogeneous frame (Definition 3.14.1).
2. **Representation component $\mathsf{r}$ — remediates DCV-002.** Exactly one of:
 - $\mathsf{r}=\big(r,(\mathcal{R},\mathcal{H})\big)$ with $(\mathcal{R},\mathcal{H})$ a measurable space and $r:\mathfrak{M}\to\mathcal{R}$ **total and measurable**; or
 - $\mathsf{r}=\bot_{\mathrm{abs}}$, the typed absence.
3. **Contexts.** $\mathcal{C}$ is a nonempty set of contexts in the sense of Definition 3.10 with $(\mathcal{Y}_C,\mathcal{G}_C)=(\mathcal{Y},\mathcal{G}_{\mathcal{Y}})$ and $\mathbb{W}_C=\mathbb{W}$ — the **whole codomain object, class datum $\mathsf{c}$ included** — for every $C\in\mathcal{C}$: the **homogeneity requirement**.
4. **Group.** $\mathcal{G}$ is a subgroup of $\mathrm{Mor}(\mathbb{F})$ (Observation 3.15.1).
5. **Closure.** $\iota\in\mathcal{G}$ and $C\in\mathcal{C}$ imply $\iota_*C\in\mathcal{C}$, a predicate evaluable by Observation 3.17.0.

**Declared abbreviation.** $\mathbb{F}$ and $\mathbb{T}$ are written
$$\mathbb{F}=\big(\mathfrak{B},(\mathfrak{M},\mathcal{F}),(\mathcal{Y},\mathcal{G}_{\mathcal{Y}}),\mathbb{W}\big),
\qquad
\mathbb{T}=\big(\mathbb{F},\ \mathsf{r},\ \mathcal{C},\ \mathcal{G}\big).$$
These are **abbreviations for the displayed components**, introduced by this definition and used throughout Part A. $\mathbb{F}$ is not a further primitive, and $\mathbb{T}$ has no components other than the seven displayed above. Every occurrence of "theory instance" below refers to this complete tuple.

**Observation 3.18.1 — remediates FV-001.** The prior edition used $\mathcal{C}$ in A4 and Theorem 7′, and used a morphism universe inside its consistency proof, without declaring either; A3 meanwhile quantified over *every* representation morphism while the proof checked only a model-specific set. Both objects are now signature components, A3 quantifies over the declared $\mathcal{G}$, and **closure is a requirement on instances rather than a claim to be proved about a particular one**. A3 and A4 are consequently predicates over the declared signature.

**Observation 3.18.2 (Effect of $\mathsf{r}$) — remediates DCV-002, TR-4.** $\mathsf{r}$ is instance data, not external data.

*Supplied branch.* If $\mathsf{r}=(r,(\mathcal{R},\mathcal{H}))$, then **A10**, **Definitions 7.1, 7.4 and 7.5** and **Theorem 3.2′** are interpreted with that $r$, and $\mathcal{H}_r$ of Definition 7.1 is computed from it.

*Absent branch.* If $\mathsf{r}=\bot_{\mathrm{abs}}$, then those statements have no instance to interpret and are **typed as inapplicable**: A10 is not asserted; the identified-output function $\mathrm{Id}^b_C$ of Definition 7.5 is **not formed**; no sufficiency, fibre-constancy or totality predicate of Definition 7.4 is defined; and **the hypotheses and conclusion of Theorem 3.2′ are not formed**, so the theorem is neither true nor false and **no vacuous truth is inferred from it**. Inapplicability is a typed state, not a truth value.

*Unaffected either way.* Theorem 3 and Corollary 3.3 quantify over an arbitrary measurable $r$, or over $M_C$, supplied as their own hypothesis rather than drawn from $\mathsf{r}$; they are therefore applicable in both branches.

**Definition 3.18.3 (Primitive-completeness table) — remediates DCV-001, DCV-002, TR-2, TR-3, TR-4.** Every primitive required to interpret every Part A definition and axiom:

| Primitive | Type | Required / optional | Global / context-indexed | Total / partial | Role in axioms and theorems |
|---|---|---|---|---|---|
| $\mathfrak{B}$ | set | required | global | — | bearers; A3, A4, Thms 1, 7′, 10″ |
| $(\mathfrak{M},\mathcal{F})$ | measurable space | required | global | — | models; Defs 3.4, 5.1; Thm 3 |
| $(\mathcal{Y},\mathcal{G}_{\mathcal{Y}})$ | measurable space | required | global (homogeneous) | — | outcomes; Defs 3.10, 5.1; Cor 3.3 |
| $\mathbb{W}=\big((W,\preceq_W,\Sigma_W),\mathsf{c}\big)$ | **codomain object** (Def 3.6) | required | global (homogeneous) | — | values; A5; Defs 3.7, 3.8, 3.11, 3.16 |
| ↳ carrier $(W,\preceq_W,\Sigma_W)$ | codomain carrier (Def 3.5) | required | global | — | Defs 3.7, 3.8, 3.12.1; A5 |
| ↳ class datum $\mathsf{c}$ | $\mathsf{W}_1(\oplus,0_W)$ **or** $\bot_{\mathrm{abs}}$ | **required, typed** | global | — | **A4** ($0_W$); Def 3.15 (W-c); Thms 1, 7′; Prop 11.1′ |
| $\mathsf{r}$ | $(r,(\mathcal{R},\mathcal{H}))$ **or** $\bot_{\mathrm{abs}}$ | **optional, typed** | global | total if supplied | A10; Defs 7.1, 7.4, 7.5; Thm 3.2′; Prop 11.1′ |
| $\mathcal{C}$ | set of contexts | required | global | — | A3, A4; Thm 7′; Prop 11.1′ |
| $\mathcal{G}$ | subgroup of $\mathrm{Mor}(\mathbb{F})$ | required | global | — | A3; Def 6.1; Cor 6.2 |
| $\bot_{\mathrm{abs}}$ | symbol (Def 3.9) | required | global | — | typed absence of $\mathsf{c}$, $\mathsf{r}$, $\approx_C$; FR-1 |
| $\mu_C$ | probability measure on $(\mathfrak{M},\mathcal{F})$ | required | context-indexed | total | Defs 5.2, 5.3 |
| $M_C$ | $\mathfrak{M}\to\mathcal{Y}$ measurable | required | context-indexed | total | Defs 5.1; Cor 3.3 |
| $T_C$ | $\mathfrak{B}\rightharpoonup\mathrm{Op}(\mathfrak{M})$ | required | context-indexed | **partial** | Defs 5.1, 5.3 |
| $\approx_C$ | equivalence on $\mathcal{Y}$, or $\bot_{\mathrm{abs}}$ | optional, typed | context-indexed | — | A8; Thm 4′ |
| $\delta_C$ | $\mathcal{Y}\times\mathcal{Y}\rightharpoonup W$ | required | context-indexed | **partial** | Defs 5.1, 5.2; A8 |
| $\mathbb{W}_C$ | codomain object | required; $=\mathbb{W}$ by clause 3 | context-indexed slot | — | Defs 3.10, 3.11 |
| $\rho_C$ | $\Delta(W)\rightharpoonup\widehat W$ | required | context-indexed | **partial** | Def 5.3; A5 |

**No Part A axiom depends on data absent from this table.** A3 ranges over $\mathcal{G}$ and $\mathcal{C}$, and over $\widehat W$ through Definition 3.16; A4 over $\mathcal{C}$ and over the class datum $\mathsf{c}$; A5 over $\widehat W$; A8 over $\approx_C$ and $\delta_C$; A9 over $\Omega^b_C$, derived from $M_C$, $T_C$, $\delta_C$; A10 over $\mathsf{r}$ and the function $\mathrm{Id}^b_C$ of Definition 3.18.4. **There is no axiom A7**: it is withdrawn from Version 1 by Observation 8.9.1, and no table entry is required for it.

**Definition 3.18.4 (Derived-object table) — remediates TR-1, TR-4.** Every derived object used by a Part A axiom or retained theorem, with its declared type. Each is recoverable from the primitives above and is **not** an additional component of $\mathbb{T}$.

| Derived object | Declared type | Total / partial | Formed when | Source |
|---|---|---|---|---|
| $\mathcal{I}(W)$ | set of order-intervals of $W$ | — | always | Def 3.7 |
| $\widehat W$ | $W\sqcup\mathcal{I}(W)\sqcup\{\bot_{\mathrm{ind}},\bot_{\mathrm{inc}},\bot_{\mathrm{und}}\}$ | — | always | Def 3.8 |
| $\widehat{W}^{\mathrm{id}}$ | $\mathcal{P}_{\neq\emptyset}(W)\sqcup\{\bot_{\mathrm{inc}},\bot_{\mathrm{und}}\}$ | — | always | Def 3.8.1 |
| $\widehat{\iota_W}$ | $\widehat W\to\widehat W$ | **total** | each $\iota\in\mathcal{G}$ | Def 3.16 |
| $\iota_*C$ | context over $\mathbb{F}$ | — | each $\iota\in\mathcal{G}$, $C\in\mathcal{C}$ | Def 3.17 |
| $\Omega^b_C$ | element of $\mathcal{F}$ | — | $T_C(b)$ defined | Def 5.1 |
| $\delta^{\,b}_C$ | $\Omega^b_C\to W$ | total on $\Omega^b_C$ | $T_C(b)$ defined | Def 5.1 |
| $P^b_C$ | element of $\Delta(W)$ | — | $T_C(b)$ defined and $\mu_C(\Omega^b_C)=1$ | Def 5.2 |
| $\sigma_C$ | $\mathfrak{B}\to\widehat W$ | **total** | every $C\in\mathcal{C}$ | Def 5.3 |
| $\mathrm{Aut}(C)$ | subgroup of $\mathcal{G}$ | — | every $C\in\mathcal{C}$ | Def 6.1 |
| $\mathcal{H}_r$ | $\sigma$-algebra on $\mathcal{R}$ | — | $\mathsf{r}$ supplied | Def 7.1 |
| $\mathrm{Id}^b_C$ | $\mathcal{R}\to\widehat{W}^{\mathrm{id}}$ | **total in $x$** | $\mathsf{r}$ supplied and $T_C(b)$ defined | Def 7.5 |

---

## A.3 Formation rule and axioms

**Formation rule FR-1.** A seven-tuple missing a required component of Definition 3.10 is not a context, and no significance is defined for it. An optional component supplied as $\bot_{\mathrm{abs}}$ is supplied.

**Observation FR-1.1.** This was stated as Axiom A2. It is a formation rule, not a substantive predicate over the class of contexts, because Definition 3.10 already requires all seven components. It is reclassified and is not counted among the axioms.

**Ranging convention — remediates TR-4.** Fix a theory instance
$$\mathbb{T}=\big(\mathbb{F},\ \mathsf{r},\ \mathcal{C},\ \mathcal{G}\big),
\qquad
\mathbb{F}=\big(\mathfrak{B},\ (\mathfrak{M},\mathcal{F}),\ (\mathcal{Y},\mathcal{G}_{\mathcal{Y}}),\ \mathbb{W}\big),
\qquad
\mathbb{W}=\big((W,\preceq_W,\Sigma_W),\ \mathsf{c}\big),$$
in the sense of Definition 3.18, using the abbreviations declared there. **Every axiom below ranges over this complete tuple**, and every symbol occurring in an axiom is a component of it or a derived object of Definition 3.18.4. The four-component form $(\mathfrak{B},\mathfrak{M},\mathcal{C},\mathcal{G})$ used by earlier editions is **superseded and withdrawn**: it omitted the outcome space, the codomain object and the representation component, and it is not an abbreviation for the tuple above.

By homogeneity (Definition 3.18 clause 3), $\mathbb{W}_C=\mathbb{W}$ and hence $W_C=W$ and $\widehat{W_C}=\widehat W$ for every $C\in\mathcal{C}$; the axioms are stated in the frame's symbols accordingly.

**A3 (Covariance over $\mathcal{G}$).** For every $\iota\in\mathcal{G}$, every $C\in\mathcal{C}$ and every $b\in\mathfrak{B}$:
$$\sigma_{\iota_*C}(\iota_{\mathfrak{B}}b)=\widehat{\iota_W}\big(\sigma_C(b)\big),$$
an equation **in $\widehat W$**: the left side lies in $\widehat W$ by A5 applied to $\iota_*C$, and the right side lies in $\widehat W$ because $\widehat{\iota_W}:\widehat W\to\widehat W$ (Definition 3.16). Well formed because $\iota_*C\in\mathcal{C}$ by Definition 3.18 clause 5.

**A4 (Nullity over $\mathcal{C}$).** The instance's class datum is $\mathsf{c}=\mathsf{W}_1(\oplus,0_W)$; and for every $b\in\mathfrak{B}$ there exists $C\in\mathcal{C}$ with
$$\sigma_C(b)=0_W.$$

**Observation A.3.0 (Exact force of A4 under homogeneity) — remediates TR-2, TR-5.** Earlier editions wrote A4 as "for every $b$ there is $C\in\mathcal{C}$ with $W_C$ of class $\mathsf{W}_1$ and $\sigma_C(b)=0_{W_C}$". Under Definition 3.18 clause 3 the conjunct "$W_C$ of class $\mathsf{W}_1$" does not depend on $C$, so that form is **equivalent** to the two-part statement above; the restatement changes no content. Its consequence must nevertheless be stated plainly: **a theory instance whose codomain object is of class $\mathsf{W}_0$ does not satisfy A4.** A4 is therefore a substantive constraint on the instance and not merely on $\mathcal{C}$, and $0_W$ denotes the **selected** identity of $\mathsf{c}$, not an arbitrary least element.

**A5 (Output typing).** For every $C\in\mathcal{C}$ and every $b\in\mathfrak{B}$: $\sigma_C(b)\in\widehat W$, with the value determined by Definition 5.3.

**A8 (Congruence).** For every $C\in\mathcal{C}$: if $\approx_C\neq\bot_{\mathrm{abs}}$, then for all $(y,y'),(\tilde y,\tilde y')\in D_C$ with $y\approx_C\tilde y$ and $y'\approx_C\tilde y'$: $\delta_C(y,y')=\delta_C(\tilde y,\tilde y')$.

**A9 (Empty contrast domain).** For every $C\in\mathcal{C}$ and every $b\in\mathfrak{B}$ with $T_C(b)$ defined: if $\Omega^b_C=\emptyset$ then $\sigma_C(b)=\bot_{\mathrm{und}}$.

**A10 (Empty fibre).** If $\mathsf{r}=(r,(\mathcal{R},\mathcal{H}))$, then for every $C\in\mathcal{C}$, every $b\in\mathfrak{B}$ with $T_C(b)$ defined, and every $x\in\mathcal{R}$ with $r^{-1}(x)=\emptyset$:
$$\mathrm{Id}^b_C(x)=\bot_{\mathrm{inc}},$$
where $\mathrm{Id}^b_C:\mathcal{R}\to\widehat{W}^{\mathrm{id}}$ is the identified-output function of Definition 7.5. If $\mathsf{r}=\bot_{\mathrm{abs}}$, then $\mathrm{Id}^b_C$ is not formed, A10 is **typed as inapplicable** and is not asserted (Observation 3.18.2).

**Observation A.3.1 — replaces the prior Observation 4.2.1.** A3 and A4 are predicates over declared carriers, since $\mathcal{G}$, $\mathcal{C}$ and $\mathsf{c}$ are instance components. A5, A8, A9 and A10 are predicates over declared functions, A10 in its supplied branch only. FR-1 is a formation rule. The axioms of Version 1 are exactly **A3, A4, A5, A8, A9, A10**; the labels A1, A2, A6 and A7 are not in use. Satisfaction of these six is therefore testable in a model, which is what Proposition 11.1′ does.

**Observation A.3.2 (Withdrawal of A7) — remediates TR-3.** The prior edition carried an axiom **A7 (Codomain confinement)** whose first clause asserted that values under $C$ lie in $\widehat{W_C}$, and whose second clause stipulated that values under distinct contexts are related only through a declared transport (the withdrawn Definition 8.9). **A7 is withdrawn from Version 1.** Its first clause is, under homogeneity, literally A5 and is retained there. Its second clause was not a predicate over any declared component — no transport datum existed in the theory instance — and it is withdrawn with Definition 8.9 by Observation 8.9.1. No retained Part A theorem, corollary or proof cited A7. The label A7 is **not reused**.

---

## A.4 Contrast and deterministic significance

**Definition 5.1 (Pointwise contrast) — derived, partial.** For $\tau=T_C(b)$ defined,
$$\delta^{\,b}_C(m)=\delta_C\big(M_C(m),M_C(\tau m)\big),\qquad \Omega^b_C:=\{m:(M_C(m),M_C(\tau m))\in D_C\}.$$
$\Omega^b_C\in\mathcal{F}$, since $m\mapsto(M_C(m),M_C(\tau m))$ is measurable into $\mathcal{G}_C\otimes\mathcal{G}_C$ and $D_C$ is measurable.

**Definition 5.2 (Profile) — derived, partial. Remediates FV-002.** Suppose $\mu_C(\Omega^b_C)=1$. Write $\Omega:=\Omega^b_C$, give $\Omega$ the trace $\sigma$-algebra $\mathcal{F}|_\Omega=\{F\cap\Omega:F\in\mathcal{F}\}$, let $\mu^\Omega_C$ be the restriction of $\mu_C$ to $\mathcal{F}|_\Omega$ — a probability measure, since $\mu_C(\Omega)=1$ — and let $\delta^{b,\Omega}_C:\Omega\to W_C$ be the restriction of $\delta^{\,b}_C$, which is **total and measurable** on $(\Omega,\mathcal{F}|_\Omega)$. The *profile* is
$$P^b_C:=\big(\delta^{b,\Omega}_C\big)_*\mu^\Omega_C\ \in\ \Delta(W_C).$$
If $\mu_C(\Omega^b_C)<1$, no profile exists.

**Observation 5.2.1 — remediates FV-002.** The prior edition wrote the ordinary pushforward of a **partial** map, which is not an instance of any operation declared in the candidate. Definition 5.2 instead pushes forward a restricted probability measure along a restricted map that is total on its domain. No extension off the null complement is used, so no existence or extension-independence question arises.

**Definition 5.3 (Deterministic significance) — derived, total. Remediates NB-1.** For every $C\in\mathcal{C}$ this defines a **total** function $\sigma_C:\mathfrak{B}\to\widehat W$, exhaustively:

| Case | $\sigma_C(b)$ |
|---|---|
| $T_C(b)$ undefined | $\bot_{\mathrm{und}}$ |
| $T_C(b)$ defined and $\mu_C(\Omega^b_C)<1$ — this includes $\Omega^b_C=\emptyset$ | $\bot_{\mathrm{und}}$ |
| $\mu_C(\Omega^b_C)=1$ and $P^b_C\notin\operatorname{dom}\rho_C$ | $\bot_{\mathrm{und}}$ |
| $\mu_C(\Omega^b_C)=1$ and $P^b_C\in\operatorname{dom}\rho_C$ | $\rho_C(P^b_C)$ |

**Totality — remediates NB-1.** The four cases are mutually exclusive and jointly exhaustive: case 1 covers $T_C(b)$ undefined, and cases 2–4 partition the remaining possibilities by the value of $\mu_C(\Omega^b_C)$ and by membership of $P^b_C$ in $\operatorname{dom}\rho_C$. Every $b\in\mathfrak{B}$ therefore receives exactly one value in $\widehat W$, so $\sigma_C$ is **total on $\mathfrak{B}$**, and the heading of this definition says so. The prior edition labelled it *partial*, which was a terminology error rather than a mathematical one: the partiality of $T_C$ and $\rho_C$ is absorbed by the bottom-valued cases. The four cases agree with A9, whose antecedent falls under case 2.

**Theorem 1 (Order reversal exists).**
*Hypotheses.* $\mathfrak{B}=\{b_1,b_2\}$; $\mathfrak{M}=\mathbb{R}^2$ Borel; the codomain object $\mathbb{W}=\big((\mathbb{R}_{\ge0},\le,\mathcal{B}(\mathbb{R}_{\ge0})),\ \mathsf{W}_1(+,0)\big)$ — class $\mathsf{W}_1$ and **point-separating**; $\rho=\rho^{\mathrm{at}}$; $\approx=\bot_{\mathrm{abs}}$; $\mathsf{r}=\bot_{\mathrm{abs}}$.
*Quantifier.* **Existential** in the pair of contexts. *Totality.* $M$, $\tau$, $\delta$ total; $T$, $\rho$ partial. *Codomain class.* $\mathsf{W}_1$, point-separating.
*Conclusion.* There exist contexts $C_1,C_2$ agreeing in every component but $M_C$ with $\sigma_{C_1}(b_1)>\sigma_{C_1}(b_2)$ and $\sigma_{C_2}(b_1)<\sigma_{C_2}(b_2)$.

*Proof.* Take $\mu=\delta_{(0,0)}$; $\mathcal{Y}=\mathbb{R}$ Borel; $T(b_1)(x,y)=(x+2,y+1)$ and $T(b_2)(x,y)=(x+1,y+2)$, both measurable; $\delta(u,v)=|u-v|$, total and measurable, so $D_C=\mathcal{Y}^2$ and $\Omega^b_C=\mathfrak{M}$; $M_{C_1}(x,y)=x$ and $M_{C_2}(x,y)=y$. All seven components are supplied. Each profile is a Dirac measure and $\rho^{\mathrm{at}}$ returns its atom, well defined by point separation. Then $\sigma_{C_1}(b_1)=2>1=\sigma_{C_1}(b_2)$ and $\sigma_{C_2}(b_1)=1<2=\sigma_{C_2}(b_2)$. $\blacksquare$

**Observation 1.1′ (Non-conclusions).** Existential only. Theorem 1 does **not** show that every context family reverses, and **no universal statement about the absence of a context-free ordering follows from it.**

---

## A.5 Invariance

**Definition 6.1 (Context automorphism).** $\mathrm{Aut}(C):=\{\pi\in\mathcal{G}:\pi_*C=C\ \text{componentwise and}\ \pi_W=\mathrm{id}_W\}$, a subgroup of $\mathcal{G}$.

**Corollary 6.2 (Fixed-context orbit constancy).** For every $\pi\in\mathrm{Aut}(C)$ and every $b$: $\sigma_C(\pi_{\mathfrak{B}}b)=\sigma_C(b)$.

*Proof.* $\pi\in\mathrm{Aut}(C)$ gives $\pi_W=\mathrm{id}_W$, hence $\widehat{\pi_W}=\mathrm{id}_{\widehat W}$ by Observation 3.16.1(d) — an identity of maps $\widehat W\to\widehat W$, both sides now typed. A3 gives $\sigma_{\pi_*C}(\pi_{\mathfrak{B}}b)=\widehat{\pi_W}(\sigma_C(b))=\sigma_C(b)$, and $\pi_*C=C$. $\blacksquare$

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

**Definition 7.5 (Identified output) — derived. Remediates TR-4.** *Applicability.* Formed exactly when the instance's representation component is supplied, $\mathsf{r}=(r,(\mathcal{R},\mathcal{H}))$, and $T_C(b)$ is defined — so that $\Omega^b_C$ and $\delta^{\,b}_C$ exist by Definition 5.1. Otherwise it is **not formed** (Observation 3.18.2).

*Declaration.* For each such pair $(C,b)$ the **identified-output function** is
$$\mathrm{Id}^b_C:\ \mathcal{R}\ \longrightarrow\ \widehat{W}^{\mathrm{id}},$$
with **domain** $\mathcal{R}$ — the representation carrier of $\mathsf{r}$ — **codomain** the identified-output carrier $\widehat{W}^{\mathrm{id}}$ of Definition 3.8.1, and **total on $\mathcal{R}$**, given by

| Case | $\mathrm{Id}^b_C(x)$ |
|---|---|
| $r^{-1}(x)=\emptyset$ | $\bot_{\mathrm{inc}}$ |
| $r^{-1}(x)\neq\emptyset$ and $r^{-1}(x)\cap\Omega^b_C=\emptyset$ | $\bot_{\mathrm{und}}$ |
| $r^{-1}(x)\cap\Omega^b_C\neq\emptyset$ | $\mathcal{S}_C(b,x):=\{\delta^{\,b}_C(m):m\in r^{-1}(x)\cap\Omega^b_C\}$ |

**Observation 7.5.1 (The declaration is complete and coherent) — remediates TR-4.**

*(a) Totality.* The three cases are mutually exclusive and jointly exhaustive over $x\in\mathcal{R}$, so exactly one applies and $\mathrm{Id}^b_C$ is a total function on $\mathcal{R}$.

*(b) Every value lies in the declared codomain.* In case 3 the set $r^{-1}(x)\cap\Omega^b_C$ is nonempty and $\delta^{\,b}_C$ is total on $\Omega^b_C$ (Definition 5.1), so $\mathcal{S}_C(b,x)$ is a **nonempty** subset of $W$ and hence an element of $\mathcal{P}_{\neq\emptyset}(W)\subseteq\widehat{W}^{\mathrm{id}}$. Cases 1 and 2 return the two bottoms of $\widehat{W}^{\mathrm{id}}$.

*(c) No carrier is overloaded.* $\widehat{W}^{\mathrm{id}}$ is **not** $\widehat W$, and $\widehat W$ is **not** extended to contain arbitrary subsets of $W$ (Observation 3.8.2). The identified output is set-valued by declaration, which is what Theorem 3.2′ requires when it exhibits a fibre with $|\mathcal{S}_C(b,x)|\ge2$; a single-valued design in $\widehat W$ would have made that conclusion unstatable. This is the coherent design chosen, and the only one used below.

*(d) Relation to significance.* $\mathrm{Id}^b_C$ and $\sigma_C$ are different functions with different domains and different codomains: $\sigma_C:\mathfrak{B}\to\widehat W$, $\mathrm{Id}^b_C:\mathcal{R}\to\widehat{W}^{\mathrm{id}}$. No axiom or theorem equates or compares them. $\bot_{\mathrm{inc}}$ and $\bot_{\mathrm{und}}$ occur in both carriers as distinct declared symbols of Definition 3.8 and Definition 3.8.1 respectively.

*(e) Measurability.* None is asserted for $\mathrm{Id}^b_C$, and none is used: no Part A statement integrates, pushes forward, or takes a preimage under it. $\widehat{W}^{\mathrm{id}}$ carries no $\sigma$-algebra.

**Theorem 3.2′ (Non-constancy under totality) — applicability gated under TR-4.**
*Applicability.* **The instance's representation component is supplied:** $\mathsf{r}=(r,(\mathcal{R},\mathcal{H}))$, and $T_C(b)$ is defined. When $\mathsf{r}=\bot_{\mathrm{abs}}$ this theorem is **typed as inapplicable**: the predicates of Definition 7.4 and the function $\mathrm{Id}^b_C$ of Definition 7.5 are not formed, so neither its hypotheses nor its conclusion is a proposition, and **no vacuous truth is inferred** (Observation 3.18.2).
*Hypotheses.* $C\in\mathcal{C}$ and $b\in\mathfrak{B}$ with $r$ total for $(C,b)$ and not fibre-constant. *Quantifier.* Existential in $x$.
*Conclusion.* There is $x\in\mathcal{R}$ with $r^{-1}(x)\neq\emptyset$ and $\mathrm{Id}^b_C(x)=\mathcal{S}_C(b,x)\in\mathcal{P}_{\neq\emptyset}(W)$ satisfying $|\mathcal{S}_C(b,x)|\ge2$; and no total measurable $h$ with $\delta^{\,b}_C=h\circ r$ exists.
*Proof.* Failure of fibre-constancy under totality yields $x$ and $m,m'\in r^{-1}(x)$ with $\delta^{\,b}_C(m)\neq\delta^{\,b}_C(m')$. Since $r$ is total for $(C,b)$, $\Omega^b_C=\mathfrak{M}$, so $r^{-1}(x)\cap\Omega^b_C=r^{-1}(x)\ni m,m'$ is nonempty; Definition 7.5 case 3 therefore applies and $\mathrm{Id}^b_C(x)=\mathcal{S}_C(b,x)$, which contains the two distinct values $\delta^{\,b}_C(m)\neq\delta^{\,b}_C(m')$. Theorem 3 then denies factorisation. $\blacksquare$

**Observation 3.2.1 (Non-conclusions).** Non-sufficiency arising from failure of **totality** alone yields $\bot_{\mathrm{und}}$ by Definition 5.3, and no two-valued fibre. The universal form asserted in an earlier edition was false and remains withdrawn. Nothing is concluded for an instance with $\mathsf{r}=\bot_{\mathrm{abs}}$.

**Observation 7.7.1 (Withdrawal of Definition 7.7) — remediates FFV-001.** The prior edition carried:

> **Definition 7.7 (Four distinct notions).** (i) sufficiency; (ii) minimal sufficiency relative to $\delta^{\,b}_C$; (iii) the distinguishability indicator on $\Omega^b_C\times\Omega^b_C$; (iv) the partition of $\Omega^b_C$ by equality of $\delta^{\,b}_C$. **No minimality is claimed anywhere.**

**Withdrawal.** That declaration is withdrawn from Version 1. It was not a definition: of the four notions it named, three were given no symbol, no domain, no codomain and no rule, and the fourth duplicated Definition 7.4. The grounds are exact.

1. **Sufficiency (i) is already defined, and is retained.** Definition 7.4 defines "*$C$-sufficient for $b$*" completely, as the conjunction of totality and fibre-constancy for $(C,b)$. Clause (i) added nothing to it. **Sufficiency is therefore preserved in Version 1 exactly as Definition 7.4 states it**, and every use of the word "sufficient" in Part A refers to that definition and to no other.
2. **Minimal sufficiency (ii) is not part of Version 1.** The phrase named no admissible class of sufficient representations, no comparison relation, and no minimality predicate, so it denoted nothing. Supplying those would introduce an ordering apparatus that no retained statement consumes, and would create precisely the minimality claim that Observation 3.0.1 and §A.10.2.4 disclaim. **No notion of minimal sufficiency exists in Version 1, and none is claimed.**
3. **The distinguishability indicator (iii) is not part of Version 1.** No symbol, codomain or value rule was declared, and the phrase occurs nowhere else in Part A.
4. **The equality partition (iv) is not part of Version 1.** No symbol or quotient notation was declared. It is not the quotient of Theorem 4′, which is taken by the supplied context equivalence $\approx_C$ on $\mathcal{Y}_C$ and is fully defined there; the two must not be conflated.

**Nothing retained uses the withdrawn notions.** Every retained statement — Theorems 1, 3, 3.2′, 4′, 7′, 9, 10″, Corollaries 3.3, 6.2, 10.1″, Proposition 11.1′, and axioms A3, A4, A5, A8, A9, A10 — was checked individually: none cites Definition 7.7, and none mentions minimal sufficiency, a distinguishability indicator, or the equality partition. Withdrawal therefore removes no result and changes no proof, witness or axiom.

**Removal was preferred to completion.** Completing (ii), (iii) and (iv) was the alternative. It was rejected because it would broaden the deterministic signature with structure no retained statement consumes, and because a minimality predicate would contradict the document's standing non-claims. The label **7.7** is not reused. Definition 7.7 is removed from the signature of Proposition 11.1′, since it declared no primitive that the consistency claim requires. Any future treatment of the three withdrawn notions is deferred as **OB-A7**.

**Theorem 4′ (Partial quotient descent).**
*Hypotheses.* $\approx_C\neq\bot_{\mathrm{abs}}$; A8; $p$ the projection to $\mathcal{Y}_C/\!\approx_C$; $\bar D_C:=(p\times p)(D_C)$.
*Quantifier.* Universal in the defined pairs.
*Conclusion.* There is a unique **partial** $\bar\delta_C$ with domain exactly $\bar D_C$ satisfying $\bar\delta_C((p\times p)(y,y'))=\delta_C(y,y')$ for all $(y,y')\in D_C$. Its pullback has domain $(p\times p)^{-1}(\bar D_C)\supseteq D_C$ and agrees with $\delta_C$ on $D_C$; the inclusion is strict unless $D_C$ is saturated under $\approx_C\times\approx_C$.
*Proof.* A8 makes the value independent of the chosen defined representative pair, giving existence and well-definedness on $\bar D_C$. Every point of $\bar D_C$ has such a pair, forcing the value and giving uniqueness there. The pullback statement is immediate, and strictness fails exactly when $D_C$ is a union of $\approx_C\times\approx_C$-classes. $\blacksquare$

---

## A.7 Context-free scalars and normalisation

**Theorem 7′ (Additive scalar on a nullity-closed family).**
*Hypotheses.* A theory instance $\mathbb{T}=(\mathbb{F},\mathsf{r},\mathcal{C},\mathcal{G})$ whose codomain object is $\mathbb{W}=\big((\mathbb{R}_{\ge0},\le,\mathcal{B}(\mathbb{R}_{\ge0})),\ \mathsf{W}_1(+,0)\big)$; a family $\mathcal{K}\subseteq\mathcal{C}$; $S:\mathfrak{B}\to\mathbb{R}_{\ge0}$; $\beta>0$; **(a)** for every $b$ there is $C\in\mathcal{K}$ with $\sigma_C(b)=0$; **(b)** for every $C\in\mathcal{K}$ there is $g_C:\mathfrak{B}\to\mathbb{R}_{\ge0}$ with $\sigma_C(b)=\beta S(b)+g_C(b)$ for all $b$.
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

**Observation 8.9.1 (Withdrawal of Definition 8.9 and axiom A7) — remediates TR-3.** The prior edition carried:

> **Definition 8.9 (Cross-context transport) — optional.** A declared order-embedding $t:W_C\to W_{C'}$ with extended action $\widehat t$ per Definition 3.16. Comparison across contexts is defined only relative to a declared $t$.

**Both Definition 8.9 and axiom A7 are withdrawn from Version 1.** The grounds are exact.

1. **It was not instance data.** No transport family, no supplied $t$ and no typed absence of $t$ was ever a component of the theory instance of Definition 3.18. A7, which referred to it, was therefore not a predicate over the declared tuple and could be neither satisfied nor violated by an instance.
2. **Its displayed type was heterogeneous.** The source $W_C$ and target $W_{C'}$ presuppose two distinct context-indexed codomains — exactly the structure Observation 3.14.2 removed from Version 1. Under Definition 3.18 clause 3, $W_C=W_{C'}=W$ for all $C,C'\in\mathcal{C}$, so the only order-embeddings the definition could ever have declared are order-embeddings $W\to W$, and the cross-context content was empty.
3. **Nothing retained uses it.** No Part A theorem, corollary, proposition or proof — Theorems 1, 3, 3.2′, 4′, 7′, 9, 10″, Corollaries 3.3, 6.2, 10.1″ and Proposition 11.1′ — cites Definition 8.9 or A7. Removal therefore withdraws no result.

**Removal was preferred to repair.** Adding a typed transport component to the instance would have been the alternative, but it would have introduced a datum that no retained statement consumes, and a genuinely cross-context transport would require the heterogeneous carriers that Version 1 excludes. **No heterogeneous transport system is introduced by this withdrawal.** The label **8.9** is not reused and the label **A7** is not reused. Formal placement of a cross-context transport discipline is deferred as **OB-A6**.

---

## A.8 Bounded encodability

**Theorem 10″ (Encodability on point-separating codomains) — replaces the false Theorem 10′. Frame made explicit under TR-5.**
*Hypotheses.* A codomain object $\mathbb{W}=\big((W,\preceq_W,\Sigma_W),\mathsf{c}\big)$ whose carrier is **point-separating** (Definition 3.5.1), with $\mathsf{c}$ **arbitrary** — either class; $\mathfrak{B}$ any set; $f:\mathfrak{B}\to W$ any function.
*Quantifier.* Existential in $C$, universal in $b$. *Form.* Deterministic contrast form with a projection evaluator. *Codomain class.* Any point-separating carrier; **no algebraic structure is required and none is used**.
*Conclusion.* There are a frame $\mathbb{F}_f:=\big(\mathfrak{B},(W,\Sigma_W),(W,\Sigma_W),\mathbb{W}\big)$ and a **single** context $C$ over $\mathbb{F}_f$ with $\mathbb{W}_C=\mathbb{W}$ and $\sigma_C(b)=f(b)$ for every $b\in\mathfrak{B}$.

*Proof.* Take $\mathfrak{M}:=W$ with $\Sigma_W$; $\mathcal{Y}:=W$ with $\Sigma_W$, so that $C$ is a context over $\mathbb{F}_f$ and the homogeneity requirement is met by the single context; $M_C:=\mathrm{id}_W$; $\mu_C:=\delta_{w_0}$ for any $w_0\in W$, a probability measure on $(W,\Sigma_W)$; $\approx_C:=\bot_{\mathrm{abs}}$; $\delta_C(y,y'):=y'$, the second projection, total and $\Sigma_W\otimes\Sigma_W/\Sigma_W$-measurable with no algebraic hypothesis; $T_C(b):=$ the constant map $m\mapsto f(b)$, measurable; $\rho_C:=\rho^{\mathrm{at}}$, a well-defined partial function by point separation. Then $\delta^{\,b}_C(m)=f(b)$ for every $m$, so $\Omega^b_C=\mathfrak{M}$, $P^b_C=\delta_{f(b)}$, and $\sigma_C(b)=\rho^{\mathrm{at}}(\delta_{f(b)})=f(b)$. $\blacksquare$

**Observation 10.0 — remediates FV-003.** The prior Theorem 10′ claimed **every** nonempty codomain and is **false** there. Counterexample: $W=\{0,1\}$ with $\Sigma_W=\{\emptyset,W\}$ is a codomain carrier under Definition 3.5, but it carries exactly one probability measure, so $\delta_0=\delta_1$ and every profile in $\Delta(W)$ is the same object; no reduction can return both $0$ and $1$. Point separation is exactly the hypothesis that repairs this. The projection evaluator was not at fault.

**Observation 10.0.1 (Degenerate witness — scope corrected under FV-003 and TR-5).** The witness evaluator $\delta_C(y,y')=y'$ ignores the factual outcome. On a point-separating carrier the **deterministic contrast form** therefore does not itself exclude degenerate evaluators, and admitting them makes any assignment realisable in a single deterministic context. **No claim is made that the axioms fail to exclude such an assignment**, and **no statement is made about non-point-separating carriers.**

**Observation 10.0.2 (Exactly what Theorem 10″ does and does not construct) — remediates TR-5.** The theorem constructs **a context**, and a frame for it to live over. It does **not** construct a theory instance: no $\mathcal{C}$, no $\mathcal{G}$, no $\mathsf{r}$ and no closure requirement is supplied or verified, and **no axiom of §A.3 is asserted or checked of the constructed context**. In particular A4 is not checked, and by Observation A.3.0 it could not be satisfied at all when $\mathsf{c}=\bot_{\mathrm{abs}}$. Theorem 10″ is therefore a **context-existence** theorem and is used below only as one.

**Corollary 10.1″ (Bounded underdetermination — narrowed under TR-5).** Within the deterministic contrast form, on a point-separating carrier, with unrestricted evaluators: **for every $f:\mathfrak{B}\to W$ the single-context construction of Theorem 10″ realises $f$**, so no assignment $f$ is excluded by **the requirement that it be realised by some context of the deterministic contrast form**.
*Proof.* Theorem 10″. $\blacksquare$

**Observation 10.1.0 (Scope of the narrowing — binding) — remediates TR-5.** The prior edition concluded that "no single-context assignment is excluded **by the axioms**". That conclusion **exceeded its proof and is withdrawn**. Theorem 10″ constructs one context and checks no axiom (Observation 10.0.2); it cannot establish that an assignment is compatible with A3, A4, A5, A8, A9 and A10. The obstruction is not merely one of proof technique: by Observation A.3.0, a theory instance whose codomain object is of class $\mathsf{W}_0$ **fails A4 outright**, and homogeneity (Definition 3.18 clause 3) forbids escaping this by adding a context over a different, class-$\mathsf{W}_1$ codomain. A point-separating carrier need not admit any $\mathsf{W}_1$ structure, so on such a carrier **assignments are excluded by the full axioms**, contrary to the withdrawn claim.

The corollary above is therefore **restricted to the single-context construction**, and it is stated explicitly that **it does not establish satisfaction of all axioms**. Of the three available corrections — restricting the corollary to point-separating codomains carrying the exact class-$\mathsf{W}_1$ structure required by A4, restricting the conclusion to the construction, or withdrawing the corollary — the **second** is adopted. The first was rejected because it would still not follow from Theorem 10″, which verifies no axiom even when a $\mathsf{W}_1$ datum is present; the third was rejected because the construction is sound and worth recording. **The phrase "the axioms exclude no assignment", in that or any equivalent form, does not occur in Version 1**, and no result of this document proves it for the homogeneous theory-instance class.

**Observation 10.1.1 (Non-conclusions — binding).** Corollary 10.1″ concerns **one** context, **one** form, and **point-separating** carriers only, and speaks of realisability by a construction rather than of consistency with the axioms. It does **not** show that the framework forbids no observation, and **no conclusion about the empirical content of the framework as a whole is drawn anywhere in this document.** Assignments realised by the construction remain subject to A3 over $\mathcal{G}$, to A4 over $\mathcal{C}$ — including A4's class requirement on the instance — and to A5, A8, A9 and A10, none of which Theorem 10″ verifies.

---

## A.9 Deterministic consistency

**Proposition 11.1′ (Consistency of the deterministic core) — replaces the invalid Proposition 11.1. Recomputed against the repaired signature under TR-6.**
*Quantifier.* **Existential** in the theory instance; universal in $\iota\in\mathcal{G}$, $C\in\mathcal{C}$ and $b\in\mathfrak{B}$ within the satisfaction checks.
*Claim.* There is a theory instance satisfying FR-1 and axioms **A3, A4, A5, A8, A9, A10** over the deterministic core signature comprising **Definitions 3.1–3.5, 3.5.1, 3.6, 3.7, 3.8, 3.8.1, 3.9–3.12, 3.12.1, 3.14.1, 3.15, 3.16, 3.17, 3.18, 3.18.3, 3.18.4, 5.1–5.3, 6.1, 7.1, 7.4 and 7.5**. There is no axiom A7, no Definition 8.9 and no Definition 7.7 in Version 1 (Observations A.3.2, 8.9.1, 7.7.1), so none is claimed. **Every definition named above is complete**, and each is instantiated by the witness below.

*Proof.* Exhibit the theory instance $\mathbb{T}=\big(\mathbb{F},\ \mathsf{r},\ \mathcal{C},\ \mathcal{G}\big)$ of Definition 3.18, component by component. **Every datum below is supplied through a declared slot of the tuple; no structure is introduced in prose.**

**Frame $\mathbb{F}=\big(\mathfrak{B},(\mathfrak{M},\mathcal{F}),(\mathcal{Y},\mathcal{G}_{\mathcal{Y}}),\mathbb{W}\big)$.** $\mathfrak{B}=\{b_1,b_2\}$; $(\mathfrak{M},\mathcal{F})=\big(\mathbb{R}^2,\mathcal{B}(\mathbb{R}^2)\big)$; $(\mathcal{Y},\mathcal{G}_{\mathcal{Y}})=\big(\mathbb{R},\mathcal{B}(\mathbb{R})\big)$; and the **codomain object**, supplied as the fourth frame slot in the sense of Definition 3.6,
$$\mathbb{W}:=\Big(\big(\mathbb{R}_{\ge0},\ \le,\ \mathcal{B}(\mathbb{R}_{\ge0})\big),\ \ \mathsf{c}\Big),
\qquad \mathsf{c}:=\mathsf{W}_1(+,0).$$

*The class datum is a component, not a remark.* $\mathsf{c}$ selects the operation $+$ and the element $0$, and **(M1)–(M5)** of Definition 3.6 hold for them: addition on $\mathbb{R}_{\ge0}$ is associative and commutative; $x+0=x$; $x\le y\Rightarrow x+z\le y+z$; and $0\le x$ for every $x\in\mathbb{R}_{\ge0}$. So $\mathbb{W}$ is of class $\mathsf{W}_1$, and its carrier is point-separating by Observation 3.5.2. **This is the structure A4 and Definition 3.15 (W-c) refer to**, and it reaches them through the tuple.

**Representation component $\mathsf{r}$ — supplied.** $\mathsf{r}=\big(r,(\mathcal{R},\mathcal{H})\big)$ with $(\mathcal{R},\mathcal{H})=(\mathfrak{M},\mathcal{F})$ and $r:=\mathrm{id}_{\mathfrak{M}}$, total and measurable. Hence $\mathcal{H}_r=\mathcal{F}$ by Definition 7.1, and A10, Theorem 3.2′ and Definitions 7.4 and 7.5 are interpreted with this $r$ — **as instance data, not as an external datum**. The instance is therefore in the supplied branch of Observation 3.18.2, and $\mathrm{Id}^b_C:\mathcal{R}\to\widehat{W}^{\mathrm{id}}$ is formed for every $(C,b)$.

**Morphism group $\mathcal{G}$.** $\mathcal{G}:=\{\mathbf{1},\jmath\}$ with $\jmath_{\mathfrak{B}}$ the transposition of $b_1$ and $b_2$; $\jmath_{\mathfrak{M}}(x,y)=(y,x)$; $\jmath_{\mathcal{Y}}=\mathrm{id}_{\mathbb{R}}$; $\jmath_W=\mathrm{id}_{\mathbb{R}_{\ge0}}$. Each component has the source and target required by Definition 3.15: $\jmath_{\mathfrak{B}}$ is a bijection of $\mathfrak{B}$; $\jmath_{\mathfrak{M}}$ is a bimeasurable bijection of $(\mathfrak{M},\mathcal{F})$; $\jmath_{\mathcal{Y}}$ is a bimeasurable bijection of $(\mathcal{Y},\mathcal{G}_{\mathcal{Y}})$; and $\jmath_W$ is an automorphism of the **codomain object** $\mathbb{W}$ — **(W-a)** $\mathrm{id}$ is an order isomorphism of $(\mathbb{R}_{\ge0},\le)$; **(W-b)** $\mathrm{id}$ and its inverse are Borel measurable; **(W-c)** with $\mathsf{c}=\mathsf{W}_1(+,0)$, $\mathrm{id}(x+y)=\mathrm{id}(x)+\mathrm{id}(y)$ and $\mathrm{id}(0)=0$, so the **selected** datum is preserved exactly. So $\jmath\in\mathrm{Mor}(\mathbb{F})$, and likewise $\mathbf{1}\in\mathrm{Mor}(\mathbb{F})$. Since $\jmath\circ\jmath=\mathbf{1}$ componentwise, $\mathcal{G}$ is a subgroup of $\mathrm{Mor}(\mathbb{F})$ of order two, as Definition 3.18 clause 4 requires.

*Extended action.* $\jmath_W=\mathrm{id}_W$ gives $\widehat{\jmath_W}=\mathrm{id}_{\widehat W}$ by Observation 3.16.1(d), a map $\widehat W\to\widehat W$ — the source and target used by A3 below, with no second codomain anywhere.

**Shared context components.** Every $C\in\mathcal{C}$ has $\mu_C=\delta_{(0,0)}$; $\approx_C=\bot_{\mathrm{abs}}$; $\delta_C(u,v)=|u-v|$, total and Borel, so $D_C=\mathcal{Y}^2$ and every $\Omega^b_C=\mathfrak{M}$; $\rho_C=\rho^{\mathrm{at}}$ with domain $\{\delta_w:w\in W\}$, a well-defined partial function because the carrier is point-separating; the frame outcome space $(\mathcal{Y},\mathcal{G}_{\mathcal{Y}})$; and $\mathbb{W}_C=\mathbb{W}$ — **the whole codomain object, class datum included**. Hence **the homogeneity requirement of Definition 3.18 clause 3 holds** and the witness instantiates the repaired general signature rather than a private structure.

**Contexts.** Two are given outright and two are defined as transports:
$C_1$: $M_{C_1}(x,y)=x$; $T_{C_1}(b_1)(x,y)=(x+2,y+1)$; $T_{C_1}(b_2)(x,y)=(x+1,y+2)$.
$C_0$: $M_{C_0}(x,y)=x$; $T_{C_0}(b_1)=T_{C_0}(b_2)=\big((x,y)\mapsto(x,y+1)\big)$.
$C_2:=\jmath_*C_1$ and $C_0':=\jmath_*C_0$, each computed below.

$$\mathcal{C}:=\{C_1,\ C_2,\ C_0,\ C_0'\}.$$

**Transport recomputation.** $\jmath$ is an involution in every component, so $\jmath^{-1}=\jmath$. Applying Definition 3.17 slot by slot, for $C\in\{C_1,C_0\}$:

| Slot | Rule (Definition 3.17) | Value at $\jmath_*C$ |
|---|---|---|
| $\mu$ | $(\jmath_{\mathfrak{M}})_*\mu_C$ | $(\jmath_{\mathfrak{M}})_*\delta_{(0,0)}=\delta_{\jmath_{\mathfrak{M}}(0,0)}=\delta_{(0,0)}$ |
| $M$ | $\jmath_{\mathcal{Y}}\circ M_C\circ\jmath_{\mathfrak{M}}^{-1}$ | $M_C\circ\jmath_{\mathfrak{M}}$, since $\jmath_{\mathcal{Y}}=\mathrm{id}$ |
| $T$ | $T_{\jmath_*C}(\jmath_{\mathfrak{B}}b)=\jmath_{\mathfrak{M}}\circ T_C(b)\circ\jmath_{\mathfrak{M}}^{-1}$ | see below |
| $\approx$ | $\bot_{\mathrm{abs}}$ if $\approx_C=\bot_{\mathrm{abs}}$ | $\bot_{\mathrm{abs}}$ |
| $\delta$ | $\jmath_W\circ\delta_C\circ(\jmath_{\mathcal{Y}}^{-1}\times\jmath_{\mathcal{Y}}^{-1})$ | $\delta_C=\lvert u-v\rvert$, since $\jmath_W$ and $\jmath_{\mathcal{Y}}$ are identities; $D_{\jmath_*C}=\mathcal{Y}^2$ |
| $\rho$ | $\widehat{\jmath_W}\circ\rho_C\circ((\jmath_W)^{-1})_*$ | $\mathrm{id}_{\widehat W}\circ\rho^{\mathrm{at}}\circ(\mathrm{id}_W)_*=\rho^{\mathrm{at}}$ |
| carriers | fixed by the frame | $(\mathcal{Y},\mathcal{G}_{\mathcal{Y}})$ and $\mathbb{W}_{\jmath_*C}=\mathbb{W}$ |

Hence $\jmath_*C_1$ and $\jmath_*C_0$ agree with $C_1$ and $C_0$ in $\mu$, $\approx$, $\delta$, $\rho$ and both carriers, and differ only in $M$ and $T$:

- $M_{C_2}(x,y)=M_{C_1}(\jmath_{\mathfrak{M}}(x,y))=M_{C_1}(y,x)=y$.
- $T_{C_2}(b_2)=\jmath_{\mathfrak{M}}\circ T_{C_1}(b_1)\circ\jmath_{\mathfrak{M}}$ sends $(x,y)\mapsto(y,x)\mapsto(y+2,x+1)\mapsto(x+1,y+2)$.
- $T_{C_2}(b_1)=\jmath_{\mathfrak{M}}\circ T_{C_1}(b_2)\circ\jmath_{\mathfrak{M}}$ sends $(x,y)\mapsto(y,x)\mapsto(y+1,x+2)\mapsto(x+2,y+1)$.
- $M_{C_0'}(x,y)=M_{C_0}(y,x)=y$.
- $T_{C_0'}(b_i)=\jmath_{\mathfrak{M}}\circ T_{C_0}(b_j)\circ\jmath_{\mathfrak{M}}$ sends $(x,y)\mapsto(y,x)\mapsto(y,x+1)\mapsto(x+1,y)$, for both bearers, since $T_{C_0}$ is the same map for both.

**Closure under $\mathcal{G}$.** $\mathbf{1}_*C=C$ for every $C$ by Observation 3.17.1. $\jmath_*C_1=C_2$ and $\jmath_*C_0=C_0'$ by construction. Since $\jmath$ is an involution, Observation 3.17.1 gives $\jmath_*C_2=\jmath_*\jmath_*C_1=(\jmath\circ\jmath)_*C_1=\mathbf{1}_*C_1=C_1$, and likewise $\jmath_*C_0'=C_0$. Hence $\iota_*C\in\mathcal{C}$ for every $\iota\in\mathcal{G}$ and $C\in\mathcal{C}$, so clause 5 holds and $\mathbb{T}$ is a theory instance.

**Significance values.** Every $T_C(b)$ is defined and every $\delta_C$ is total, so $\Omega^b_C=\mathfrak{M}$ and $\mu_C(\Omega^b_C)=1$; each $\delta^{\,b}_C$ is constant, so each profile $P^b_C$ is a Dirac measure and lies in $\operatorname{dom}\rho^{\mathrm{at}}$. Row four of Definition 5.3 therefore applies throughout and $\rho^{\mathrm{at}}$ returns the atom:
$$\sigma_{C_1}(b_1)=2,\quad \sigma_{C_1}(b_2)=1,\quad \sigma_{C_2}(b_1)=1,\quad \sigma_{C_2}(b_2)=2,\quad \sigma_{C_0}(b_i)=0,\quad \sigma_{C_0'}(b_i)=0.$$

**Satisfaction.**
*FR-1* — every context supplies all seven components of Definition 3.10; $\approx_C=\bot_{\mathrm{abs}}$ is a supplied optional value, not a missing one.
*A3* — for $\iota=\mathbf{1}$ the equation reads $\sigma_C(b)=\widehat{\mathrm{id}_W}(\sigma_C(b))=\sigma_C(b)$ by Observation 3.16.1(d). For $\iota=\jmath$, with $\widehat{\jmath_W}=\mathrm{id}_{\widehat W}$, the required equations $\sigma_{\jmath_*C}(\jmath_{\mathfrak{B}}b)=\sigma_C(b)$ in $\widehat W$ are:
 1. $(C_1,b_1)$: $\sigma_{C_2}(b_2)=2=\sigma_{C_1}(b_1)$.
 2. $(C_1,b_2)$: $\sigma_{C_2}(b_1)=1=\sigma_{C_1}(b_2)$.
 3. $(C_2,b_1)$: $\sigma_{C_1}(b_2)=1=\sigma_{C_2}(b_1)$.
 4. $(C_2,b_2)$: $\sigma_{C_1}(b_1)=2=\sigma_{C_2}(b_2)$.
 5. $(C_0,b_1)$: $\sigma_{C_0'}(b_2)=0=\sigma_{C_0}(b_1)$.
 6. $(C_0,b_2)$: $\sigma_{C_0'}(b_1)=0=\sigma_{C_0}(b_2)$.
 7. $(C_0',b_1)$: $\sigma_{C_0}(b_2)=0=\sigma_{C_0'}(b_1)$.
 8. $(C_0',b_2)$: $\sigma_{C_0}(b_1)=0=\sigma_{C_0'}(b_2)$.
 All eight non-identity instances hold, and $\jmath\neq\mathbf{1}$, so **the check is not vacuous**.
*A4* — both conjuncts hold: the instance class datum is $\mathsf{c}=\mathsf{W}_1(+,0)$, supplied in the frame slot; and $C_0\in\mathcal{C}$ gives $\sigma_{C_0}(b_i)=0=0_W$ for both bearers, where $0_W$ is the **selected** identity of $\mathsf{c}$.
*A5* — every value lies in $\mathbb{R}_{\ge0}=W\subseteq\widehat W$, assigned by row four of Definition 5.3.
*A8* — antecedent false in every context, since $\approx_C=\bot_{\mathrm{abs}}$; A8 holds.
*A9* — antecedent false, since every $\Omega^b_C=\mathfrak{M}\neq\emptyset$; A9 holds.
*A10* — $\mathsf{r}$ is supplied and $r=\mathrm{id}_{\mathfrak{M}}$, so every fibre $r^{-1}(x)=\{x\}$ is a singleton and no fibre is empty. Case 3 of Definition 7.5 therefore applies at every $x$, giving $\mathrm{Id}^b_C(x)=\{\delta^{\,b}_C(x)\}\in\mathcal{P}_{\neq\emptyset}(W)$; the antecedent of A10 is never met, and A10 holds vacuously in this instance. $\blacksquare$

**Observation 11.1.1 — remediates FV-004 and FV-005.** The prior witness asserted $\jmath_*C_0=C_0$. That is **false**: transporting $C_0$ by the coordinate swap yields outcome map $y$ and operations shifting $x$, which are the components of neither $C_0$ nor $C_1$ nor $C_2$. The repair adds $C_0':=\jmath_*C_0$ to $\mathcal{C}$ and **proves** closure using involutivity rather than asserting a false equality. The fragment declaration now also names **Definitions 5.1–5.3**, on which the proof depends and which the prior declaration omitted.

**Observation 11.1.2 (Scope of the claim — binding).** Proposition 11.1′ establishes consistency of **exactly** the deterministic core signature and axioms named in its claim, over the declared instance. It does **not** establish consistency for anything in Part B, nor for interval- or bottom-valued outputs, nontrivial $\approx_C$, non-atomic measures, non-point-separating carriers, or codomain objects of class $\mathsf{W}_0$. **The consistency claim does not exceed the witness.**

**Observation 11.1.3 (The witness instantiates the exact repaired signature) — remediates TR-6.** Every datum the proof uses is supplied through a declared slot:

| Datum | Slot it arrives through |
|---|---|
| $\mathfrak{B}$, $(\mathfrak{M},\mathcal{F})$, $(\mathcal{Y},\mathcal{G}_{\mathcal{Y}})$ | frame components 1–3 |
| carrier $(\mathbb{R}_{\ge0},\le,\mathcal{B})$ **and** class datum $\mathsf{W}_1(+,0)$ | frame component 4, the codomain object $\mathbb{W}$ (Definition 3.6) |
| $r$ and $(\mathcal{R},\mathcal{H})$ | $\mathsf{r}$, supplied branch of Definition 3.18 clause 2 |
| $C_1,C_2,C_0,C_0'$ | $\mathcal{C}$, Definition 3.18 clause 3 |
| $\mathbf{1}$, $\jmath$ | $\mathcal{G}$, Definition 3.18 clause 4 |
| $\mu_C$, $M_C$, $T_C$, $\approx_C$, $\delta_C$, $\mathbb{W}_C$, $\rho_C$ | the seven slots of each context, Definition 3.10 |

**No structure is added in explanatory prose.** In particular the operation $+$ and the element $0$ used by A4 and by Definition 3.15 (W-c) are the components of $\mathsf{c}$, not a remark about $\mathbb{R}_{\ge0}$; the prior edition supplied them only in prose, which is the defect this recomputation closes. No transport datum is required, since Definition 8.9 and A7 are withdrawn (Observation 8.9.1), so the claimed signature has no unfilled optional slot.

---

## A.10 Deterministic results, limitations and rejections

### A.10.1 Verified deterministic results

| № | Statement | Quantifier | § |
|---|---|---|---|
| 1 | Order reversal exists between two contexts | existential | A.4 |
| 3 | Measurable factorisation iff fibre-constant | universal | A.6 |
| 3.2′ | Under totality, non-fibre-constancy forces a non-singleton identified set — **supplied-$\mathsf{r}$ branch only** | existential in $x$ | A.6 |
| 3.3 | Induced outcome map iff fibre-constant | universal | A.6 |
| 4′ | Partial quotient descent on $\bar D_C$ | universal | A.6 |
| 6.2 | Fixed-context orbit constancy | universal | A.5 |
| 7′ | Additive context-free scalar vanishes on a nullity-closed family | universal | A.7 |
| 9 | Arena dependence of normalisation | universal | A.7 |
| 10″ | Encodability on point-separating carriers — **context-existence only; no axiom is verified** | existential in $C$ | A.8 |
| 11.1′ | Consistency of the deterministic core | existential | A.9 |

### A.10.2 What the deterministic core does **not** establish

**A.10.2.1 — remediates FV-006. The core does not exclude intrinsic significance.** Writing $\sigma$ as a function of $(C,b)$ does not prevent it from being constant in its first argument. In an instance whose codomain object is of class $\mathsf{W}_1$ — as A4 requires (Observation A.3.0) — the assignment $\sigma_C(b)=0_W$ for every $C$ and every $b$ is context-independent, satisfies A4, and is excluded by no Part A axiom. No non-formal design principle is available to close the gap, since none may be cited in a proof. **The earlier rejection of intrinsic significance is withdrawn, and no Part A result replaces it.**

**A.10.2.2.** No universal absence of a context-free ordering is established. Theorem 1 is existential.

**A.10.2.3.** No conclusion about the empirical content of the framework as a whole is drawn (Observation 10.1.1).

**A.10.2.4.** No computability, minimality, novelty, prior-art or recognisability result is established.

### A.10.3 Deterministic limitations

**14.4.** The reduction $\rho_C$ is primitive and is not determined by the theory. *(The earlier claim that distinct reductions always induce distinct orderings on asymmetric profiles is withdrawn: distinct positive rescalings induce the same ordering.)*

**14.7′ — restated under TR-3.** Version 1 supplies **no** apparatus for comparing values across contexts: the cross-context transport of the withdrawn Definition 8.9 was never instance data, and axiom A7 is withdrawn with it (Observation 8.9.1). Under homogeneity all contexts of an instance share the one codomain object, so values under distinct contexts are elements of the same $\widehat W$ and are comparable as such by $\preceq_W$ where both lie in $W$; **what Version 1 does not supply is any warrant for interpreting such a comparison as meaningful across contexts.** That warrant is deferred as **OB-A6**, and no Part A result depends on it.

**14.11′ — narrowed under FV-003, FV-006 and TR-5.** On a **point-separating carrier**, within the deterministic contrast form and with unrestricted evaluators, every single-context assignment is **realised by the construction of Theorem 10″** (Corollary 10.1″). **Nothing follows about exclusion by the axioms**: Theorem 10″ verifies no axiom, and by Observation A.3.0 an instance whose codomain object is of class $\mathsf{W}_0$ fails A4 outright, so on a carrier admitting no $\mathsf{W}_1$ structure the full axioms **do** exclude assignments. Nothing follows for non-point-separating carriers, for other forms, or for joint assignments across $\mathcal{C}$.

**14.12′ — narrowed under FV-004.** Consistency is established for exactly the deterministic core signature over the instance of Proposition 11.1′, and for nothing else.

### A.10.4 Deterministic rejected formulations

Retained only where entailed by a Part A result or by inspection of the Part A signature.

**16.16.** *The framework derives its evaluator automatically.* — By inspection: $T_C$, $\delta_C$ and $\rho_C$ are primitives of Definition 3.10, and no construction produces them from $\mu_C$.

**16.17.** *A context-free ordering primitive exists in this signature.* — By inspection: no such component is declared. *(A statement about the signature only. It does **not** exclude a context-independent significance function — see A.10.2.1.)*

**16.18.** *This document claims novelty.* — No novelty claim is made, and no universal prior-art subsumption is claimed.

**16.19.** *Significance-first intelligence is a statement of this theory.* — The phrase occurs in no Part A definition, axiom or theorem.

**Withdrawn in the prior pass — FV-006.**
**16.1** (*rejection of intrinsic significance*) — **withdrawn**; see A.10.2.1. The counterexample $\sigma\equiv0_W$ is context-independent and compatible with A4.
**16.13** (*artefact independence*) — **withdrawn as stated**, since "artefact relabelling" and "declared universe" are not defined in the signature. What survives is exactly Corollary 6.2 — fixed-context orbit constancy for $\mathrm{Aut}(C)$ — and nothing more.

**Withdrawn in this pass — TR-3.**
**16.12** (*values under distinct contexts may be compared without a declared transport*) — **withdrawn**. Its stated ground was "A7 with Definition 8.9", and both are withdrawn from Version 1 by Observation 8.9.1. A rejection whose only warrant has been removed is not retained for continuity; what Version 1 actually says about cross-context comparison is limitation 14.7′ and nothing more.

---

## A.11 Deterministic open obligations

**OB-A1.** A structural characterisation of fibre-constancy.
**OB-A2.** Conditions on $M_C$, $\tau$ and $\delta_C$ beyond those of Definition 5.1 that guarantee measurability of $\delta^{\,b}_C$ in wider settings.
**OB-A3.** Whether a deterministic encodability theorem holds for codomains that are not point-separating, or whether point separation is necessary as well as sufficient.

**OB-A4.** Whether the representation component $\mathsf{r}$ should be required $\mathcal{G}$-equivariant, i.e. whether an instance should carry $\iota_{\mathcal{R}}$ with $r\circ\iota_{\mathfrak{M}}=\iota_{\mathcal{R}}\circ r$. **No Part A statement couples $\mathsf{r}$ and $\mathcal{G}$**: A3 does not mention $r$, and A10 and Definitions 7.1–7.5 do not mention $\mathcal{G}$. Equivariance is therefore not required for well-typedness and is not imposed.

**OB-A5.** Formal placement, within Part B, of the heterogeneous context-indexed carriers and indexed action removed from Version 1 by Observation 3.14.2. Deferred because the adopting pass was not authorised to modify Part B.

**OB-A6 — recorded in this pass.** Formal placement of a cross-context transport discipline and of any axiom governing cross-context comparison, following the withdrawal of Definition 8.9 and axiom A7 (Observation 8.9.1). Any such treatment must declare the transport as typed instance data with source, target, preservation rules and typed absence, and — if it is to be genuinely cross-context — must first resolve the heterogeneous-carrier question of **OB-A5**. Deferred: the withdrawing pass was authorised to close defects, not to add structure, and no retained Part A statement consumes such a datum.

**OB-A7 — recorded in this pass.** Formal treatment, if any is wanted, of the three notions withdrawn with Definition 7.7 (Observation 7.7.1): minimal sufficiency relative to $\delta^{\,b}_C$, a distinguishability indicator on $\Omega^b_C\times\Omega^b_C$, and the partition of $\Omega^b_C$ by equality of $\delta^{\,b}_C$. Any such treatment must supply, for each notion, a symbol, a domain, a codomain, a complete rule, and — for minimal sufficiency — an admissible class, a comparison relation and a minimality predicate. Deferred: none is consumed by any retained Part A statement, and the pass that withdrew them was authorised to close a completeness defect, not to add structure. **No minimality result is claimed by Version 1**, consistently with Observation 3.0.1 and §A.10.2.4.

**None of OB-A1 – OB-A7 blocks the deterministic core**, and none is used by any Part A theorem.

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
