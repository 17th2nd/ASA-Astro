# ASTRO-THEORY-0001 — DCV Adjudication

**Subject:** `docs/theory/ASTRO-THEORY-0001.md`
**Sole remediation basis:** `docs/theory/verification/ASTRO-THEORY-0001-VERSION-1-DETERMINISTIC-CORE-VERIFICATION.md`, determination **DETERMINISTIC CORE REQUIRES BOUNDED REMEDIATION**. Read in full. Not modified.
**Pre-remediation blob:** `ad86bb978dc2d9a215af9f90d3a8cf9771f48d69` — confirmed at `HEAD` and in the worktree before mutation.
**Baseline:** `HEAD = origin/main = 848dc48a9e0cfdc1f7c03bcb0adc5d9a59ad5e07`, branch `main`, 0 ahead / 0 behind, worktree clean, no staged, modified or untracked files.
**Status after this pass:** Theory Candidate. Not frozen.

**Basis discipline.** The AV and FV findings were used only as historical context. The report records FV-001 – FV-006 as **Closed** and this pass does not reopen them. DCV-001 and DCV-002 are the sole remediation basis.

**Scope discipline.** No theorem was altered except as strictly required by the two signature repairs. Part B was **not modified** — verified mechanically by byte comparison of the Part B region against `HEAD`. No frozen research control was touched.

---

## DCV-001 — The representation group has no declared action on context-indexed carriers

- **Severity:** Blocking
- **Exact defect.** Definition 3.10 made both $(\mathcal{Y}_C,\mathcal{G}_C)$ and $W_C$ context-indexed, while Definition 3.15 gave a representation morphism one untyped $\iota_{\mathcal{Y}}$ and one untyped $\iota_W$ — no source or target outcome space for the former, no source or target codomain for the latter. Definition 3.18 nevertheless made a single group $\mathcal{G}$ act on every $C\in\mathcal{C}$ and required composition in it. The report's decisive observation: **$\iota_*C$ must already be typed before the closure predicate $\iota_*C\in\mathcal{C}$ can be evaluated**, so closure cannot supply the missing domains, codomains or composition law. Functoriality (Observation 3.17.1) presupposed composability rather than establishing it. A3 was well typed only in the homogeneous witness, where both maps are identities.
- **Affected sections.** Definitions 3.10, 3.15–3.18; A3; Definition 6.1; Corollary 6.2.
- **Disposition:** **Accepted with Modification — Option A adopted.**

### Choice of option and justification

**Option A (homogeneous carriers) is adopted.** Three reasons, each checked against the text.

1. **No Part A theorem uses heterogeneity.** Theorem 1 varies only $M_C$ between $C_1$ and $C_2$; Theorem 7′ fixes $W=(\mathbb{R}_{\ge0},+,0,\le)$ across its family $\mathcal{K}$; Theorem 10″ constructs a single context; Corollary 6.2 operates inside one context; Proposition 11.1′ was already homogeneous, sharing $\mathcal{Y}=\mathbb{R}$ and $W=\mathbb{R}_{\ge0}$ across all four contexts. **Option A therefore removes no retained result and requires no numerical change to the witness.**
2. **It is the bounded repair.** Under Option A every morphism component is an endomorphism of a fixed object, so identity, composition, inverse, associativity and functoriality reduce to the ordinary componentwise facts about automorphism groups. No coherence apparatus is introduced.
3. **Option B would be a redesign, which this pass is not authorised to perform.** A context-indexed action requires components $\iota_{\mathcal{Y},C}:\mathcal{Y}_C\to\mathcal{Y}_{\iota_*C}$ whose target is named by the very transport they are used to define. To break that circularity the target carrier must be posited as part of the morphism datum rather than derived from the transport, and coherence laws — identity, composition over the index, inverse, compatibility with transported contexts and with $\widehat{W}$ — must then be stated and proved. That is additional structure.

**Explicit statement required by the instruction:** **Version 1 is homogeneous.** Heterogeneous context-indexed outcome spaces and codomains, and any indexed or groupoid action over them, are **removed from Version 1** and deferred as Candidate material (Observation 3.14.2). Their formal placement inside Part B is deferred and recorded as **OB-A5**, because this pass was instructed not to modify Part B.

### Exact repair

| Item | Repair |
|---|---|
| **Definition 3.14.1 (new)** | Declares the *homogeneous frame* $\mathbb{F}=(\mathfrak{B},(\mathfrak{M},\mathcal{F}),(\mathcal{Y},\mathcal{G}_{\mathcal{Y}}),(W,\preceq_W,\Sigma_W))$ with **one** outcome space and **one** codomain |
| **Observation 3.14.2 (new)** | Declares Option A, gives the three-part justification, and states the consequence for heterogeneous carriers |
| **Definition 3.15 (rewritten)** | Morphism components tabulated with **explicit source and target**: $\iota_{\mathcal{Y}}$ a bimeasurable bijection of $(\mathcal{Y},\mathcal{G}_{\mathcal{Y}})$; $\iota_W$ an automorphism of $(W,\preceq_W,\Sigma_W)$ preserving order, $\sigma$-algebra and any declared class-$\mathsf{W}_1$ structure. Writes $\mathrm{Mor}(\mathbb{F})$ |
| **Observation 3.15.1 (new)** | Proves the **group laws**: identity, composition, inverse, associativity and unit, each componentwise, concluding that $\mathrm{Mor}(\mathbb{F})$ is a group and $\mathcal{G}$ a subgroup |
| **Definition 3.17 (amended)** | The carrier lines now read $(\mathcal{Y}_{\iota_*C},\mathcal{G}_{\iota_*C})=(\mathcal{Y},\mathcal{G}_{\mathcal{Y}})$ and $(W_{\iota_*C},\preceq,\Sigma)=(W,\preceq_W,\Sigma_W)$; the prior $W_{\iota_*C}=\iota_W(W_C)$ is removed as redundant, since $\iota_W$ is an automorphism of the fixed $W$ |
| **Observation 3.17.0 (new)** | Proves **transport is well typed**: every component of $\iota_*C$ has declared source and target, so $\iota_*C$ is a context over the same frame and the closure predicate is evaluable **before** closure is imposed — the exact gap the report identified |
| **Definition 3.18 clauses 1, 3, 4** | Instance carries the frame; **homogeneity requirement** $(\mathcal{Y}_C,\mathcal{G}_C)=(\mathcal{Y},\mathcal{G}_{\mathcal{Y}})$ and $(W_C,\preceq,\Sigma)=(W,\preceq_W,\Sigma_W)$ for every $C\in\mathcal{C}$; $\mathcal{G}$ a **subgroup of $\mathrm{Mor}(\mathbb{F})$** |

### Proof obligations discharged

- **Source/target typing:** Definition 3.15's table.
- **Identity, composition, inverse, associativity:** Observation 3.15.1, componentwise.
- **Functoriality:** Observation 3.17.1 retained; its hypothesis — composability of components — is now supplied by Observation 3.15.1 rather than presupposed.
- **Transported contexts:** Observation 3.17.0.
- **Closure of $\mathcal{C}$ under $\mathcal{G}$:** now an evaluable predicate (Definition 3.18 clause 5).
- **A3:** both sides land in $\widehat{W}$ for the frame's single $W$; $\widehat{\iota_W}$ is Definition 3.16's extended action on that $\widehat{W}$.
- **$\mathrm{Aut}(C)$ and Corollary 6.2:** $\mathrm{Aut}(C)$ is a subgroup of $\mathcal{G}\le\mathrm{Mor}(\mathbb{F})$; Corollary 6.2's proof is unchanged and now rests on a typed action.
- **Proposition 11.1′ and the four-context witness:** §"Witness recheck" below.

- **Downstream effect on definitions.** Definitions 3.15, 3.17, 3.18 rewritten or amended; Definition 3.10 **unchanged** in shape, with homogeneity imposed at instance level rather than by altering the context tuple — the least invasive placement.
- **Downstream effect on theorems.** **No theorem statement or proof changed.** Corollary 6.2 becomes unconditional rather than conditional on a well-typed action; the report had marked it "conditionally pass" for exactly this reason.
- **New assumptions.** Homogeneity of $\mathcal{Y}$ and $W$ across an instance. This is a genuine narrowing of the admitted instances and is recorded as such.
- **Remaining proof obligation.** **OB-A5** — formal placement of the removed heterogeneous case in Part B. Non-blocking; it concerns Candidate material only.
- **Fully closed:** **Yes.**

---

## DCV-002 — The theory-instance tuple omits the optional representation map

- **Severity:** Major
- **Exact defect.** Definition 3.3 declared the optional primitive $r:\mathfrak{M}\to(\mathcal{R},\mathcal{H})$, but Definition 3.18 defined an instance as $(\mathfrak{B},(\mathfrak{M},\mathcal{F}),\mathcal{C},\mathcal{G})$ and recorded neither $r$ nor its typed absence. A10 was therefore not a predicate determined by the declared tuple, and Proposition 11.1′ supplied $r:=\mathrm{id}_{\mathfrak{M}}$ **outside** the tuple when checking A10.
- **Affected sections.** Definition 3.3; Definition 3.18; A10; Definitions 7.1, 7.4, 7.5, 7.7; Proposition 11.1′.
- **Disposition:** **Accepted**

### Exact repair

**Definition 3.18 clause 2** adds the representation component $\mathsf{r}$, with **exactly one** of two typed values:

- $\mathsf{r}=(r,(\mathcal{R},\mathcal{H}))$ — $(\mathcal{R},\mathcal{H})$ a declared measurable space and $r:\mathfrak{M}\to\mathcal{R}$ declared **total and measurable**; or
- $\mathsf{r}=\bot_{\mathrm{abs}}$ — the typed absence.

**Observation 3.18.2 (new)** types the consequences of each branch:

| Branch | A10 | Definitions 7.1, 7.4, 7.5, 7.7 | Theorem 3, Corollary 3.3 |
|---|---|---|---|
| $\mathsf{r}$ supplied | interpreted with that $r$; $\mathcal{H}_r$ computed from it | interpreted with that $r$ | unaffected |
| $\mathsf{r}=\bot_{\mathrm{abs}}$ | **typed as inapplicable**; not asserted; neither true nor false | **inapplicable**: no identified output, no sufficiency, fibre-constancy or totality predicate is defined | unaffected — they quantify over an arbitrary measurable map or over $M_C$ supplied as their own hypothesis, not over $\mathsf{r}$ |

**A10 rewritten** to name the instance component explicitly and to state the inapplicable branch, so it is now a predicate determined by the tuple.

**Definition 3.18.3 (new)** gives the **primitive-completeness table** required by the instruction — primitive, type, required/optional, global/context-indexed, total/partial, and role in axioms or theorems — covering the seven instance-level primitives and the six context-level components, with the closing statement that **no Part A axiom depends on data absent from the table**, itemised axiom by axiom.

- **Proof or counterexample.** None required; the defect is an omission from a tuple. The repair is verified by the completeness table and by the witness, which now supplies $\mathsf{r}$ as clause 2 of the instance rather than as a side remark.
- **Downstream effect on definitions.** Definition 3.18 gains clause 2; Definition 3.18.3 added; A10 rewritten. Definitions 7.1, 7.4, 7.5, 7.7 unchanged in content, now with a declared interpretation source.
- **Downstream effect on theorems.** **None.** No theorem using a separately stated $r$ is refuted, exactly as the report anticipated. Proposition 11.1′'s A10 check is unchanged in substance and now draws $r$ from the instance.
- **New assumptions.** None. The optional primitive is relocated, not strengthened.
- **Remaining proof obligation.** **OB-A4** — whether $\mathsf{r}$ should be required $\mathcal{G}$-equivariant. Recorded as **not required**: no Part A statement couples $\mathsf{r}$ and $\mathcal{G}$, since A3 does not mention $r$ and A10 and Definitions 7.1–7.7 do not mention $\mathcal{G}$. Non-blocking.
- **Fully closed:** **Yes.**

---

## Witness recheck under the repaired signature

Recomputed in full. **No numerical value changed**; what changed is that every datum is now drawn from the declared instance.

| Instance component | Witness value | Clause satisfied |
|---|---|---|
| Frame $\mathbb{F}$ | $\mathfrak{B}=\{b_1,b_2\}$; $(\mathfrak{M},\mathcal{F})=\mathbb{R}^2$ Borel; $(\mathcal{Y},\mathcal{G}_{\mathcal{Y}})=\mathbb{R}$ Borel; $(W,\preceq_W,\Sigma_W)=(\mathbb{R}_{\ge0},\le)$ Borel with $(+,0)$, class $\mathsf{W}_1$, point-separating | 1 |
| $\mathsf{r}$ | $\big(\mathrm{id}_{\mathfrak{M}},(\mathfrak{M},\mathcal{F})\big)$, total and measurable; $\mathcal{H}_r=\mathcal{F}$ | 2 |
| $\mathcal{C}$ | $\{C_1,C_2,C_0,C_0'\}$, every context using the frame's $\mathcal{Y}$ and $W$ | 3 — homogeneity holds |
| $\mathcal{G}$ | $\{\mathbf{1},\jmath\}$, a subgroup of $\mathrm{Mor}(\mathbb{F})$ of order two | 4 |
| Closure | proved from Observation 3.17.1 and $\jmath\circ\jmath=\mathbf{1}$ | 5 |

**Morphism typing.** $\jmath_{\mathfrak{B}}$ is a bijection of $\mathfrak{B}$; $\jmath_{\mathfrak{M}}(x,y)=(y,x)$ is a bimeasurable bijection of $(\mathfrak{M},\mathcal{F})$; $\jmath_{\mathcal{Y}}=\mathrm{id}_{\mathbb{R}}$ is a bimeasurable bijection of $(\mathcal{Y},\mathcal{G}_{\mathcal{Y}})$; $\jmath_W=\mathrm{id}_W$ is an automorphism of $(W,\preceq_W,\Sigma_W)$ preserving $+$ and $0$. Each has the source and target Definition 3.15 requires, so $\jmath\in\mathrm{Mor}(\mathbb{F})$ — **which the prior signature could not state**.

**Transports.** $\jmath_*C_1=C_2$ (outcome map $y$; $T(b_2)(x,y)=(x+1,y+2)$, $T(b_1)(x,y)=(x+2,y+1)$); $\jmath_*C_2=C_1$; $\jmath_*C_0=C_0'$ (outcome map $y$; $T(b_i)(x,y)=(x+1,y)$); $\jmath_*C_0'=C_0$. Identity action fixes each context.

**Significance.** $\sigma_{C_1}(b_1)=2$, $\sigma_{C_1}(b_2)=1$, $\sigma_{C_2}(b_1)=1$, $\sigma_{C_2}(b_2)=2$, $\sigma_{C_0}(b_i)=0$, $\sigma_{C_0'}(b_i)=0$.

**Eight A3 equations**, with $\widehat{\jmath_W}=\mathrm{id}$: $(C_1,b_1)\!:\!2{=}2$; $(C_1,b_2)\!:\!1{=}1$; $(C_2,b_1)\!:\!1{=}1$; $(C_2,b_2)\!:\!2{=}2$; $(C_0,b_1)\!:\!0{=}0$; $(C_0,b_2)\!:\!0{=}0$; $(C_0',b_1)\!:\!0{=}0$; $(C_0',b_2)\!:\!0{=}0$. All hold, and $\jmath\neq\mathbf{1}$, so A3 is verified **non-vacuously**.

**Remaining axioms.** A4 — $C_0$ gives $0_W$ for both bearers in a class-$\mathsf{W}_1$ codomain. A5 — every value lies in $W\subseteq\widehat W$ via Definition 5.3 row four. A7 — all values in the common $\widehat W$; no cross-context comparison asserted. A8 — vacuous, every $\approx_C=\bot_{\mathrm{abs}}$. A9 — every $\Omega^b_C=\mathfrak{M}\neq\emptyset$. A10 — $\mathsf{r}$ supplied with $r=\mathrm{id}$, so no fibre is empty and the implication holds; the datum is now **instance data**.

**The witness instantiates the exact repaired general signature.** No private extra structure is used: every object it names is a clause of Definition 3.18 or a component of Definition 3.10.

---

## Disposition summary

| Finding | Severity | Disposition | Fully closed |
|---|---|---|---|
| DCV-001 | Blocking | Accepted with Modification — Option A | **Yes** |
| DCV-002 | Major | Accepted | **Yes** |

**No blocking obligation remains against the deterministic core.** OB-A1 – OB-A5 are non-blocking and used by no Part A proof. OB-A4 and OB-A5 are new in this pass and are disclosures, not defects.
