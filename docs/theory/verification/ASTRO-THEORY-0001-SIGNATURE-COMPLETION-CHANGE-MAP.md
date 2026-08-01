# ASTRO-THEORY-0001 — Signature Completion Change Map

**Old edition:** blob `ad86bb978dc2d9a215af9f90d3a8cf9771f48d69` at commit `848dc48`.
**New edition:** this working tree, same path.
**Basis:** `ASTRO-THEORY-0001-VERSION-1-DETERMINISTIC-CORE-VERIFICATION.md`, findings DCV-001 and DCV-002.
**Both editions:** Theory Candidate. Neither is frozen.
**Part B:** **byte-identical** to `HEAD`, verified mechanically.

---

## 1. DCV-001 — representation action

| Old § | New § | Reason | Semantic effect | Proof effect | Status |
|---|---|---|---|---|---|
| *(none)* | **Def 3.14.1 Homogeneous frame** | DCV-001 | One outcome space and one codomain per instance, declared as a frame | Gives $\iota_{\mathcal{Y}}$ and $\iota_W$ objects to act on | **Added** |
| *(none)* | **Obs 3.14.2 Option A declared** | DCV-001 | States Version 1 is homogeneous; three-part justification; heterogeneous carriers removed from Version 1 | None — a scoping statement | **Added** |
| **Def 3.15** untyped $\iota_{\mathcal{Y}}$, $\iota_W$ | **Def 3.15** with a source/target table | DCV-001 | Each component's source and target declared; $\iota_W$ required to preserve order, $\sigma$-algebra and declared class-$\mathsf{W}_1$ structure | Makes every later composite well typed | **Rewritten** |
| *(none)* | **Obs 3.15.1 Group laws** | DCV-001 | Identity, composition, inverse, associativity, unit — each componentwise | **Proves** $\mathrm{Mor}(\mathbb{F})$ is a group; supplies the composability that Obs 3.17.1 previously presupposed | **Added** |
| **Def 3.17** carrier line $W_{\iota_*C}=\iota_W(W_C)$ | **Def 3.17** carriers fixed: $(\mathcal{Y}_{\iota_*C},\mathcal{G}_{\iota_*C})=(\mathcal{Y},\mathcal{G}_{\mathcal{Y}})$, $(W_{\iota_*C},\preceq,\Sigma)=(W,\preceq_W,\Sigma_W)$ | DCV-001 | Redundant image expression removed; carriers are the frame's | Transported context is a context over the same frame | **Amended** |
| *(none)* | **Obs 3.17.0 Transport is well typed** | DCV-001 | Every component of $\iota_*C$ has declared source and target | **Closes the report's decisive gap**: $\iota_*C\in\mathcal{C}$ is evaluable *before* closure is imposed | **Added** |
| **Def 3.18** clauses | **Def 3.18** clauses 1, 3, 4 | DCV-001 | Instance carries the frame; homogeneity requirement on every $C\in\mathcal{C}$; $\mathcal{G}$ a **subgroup of $\mathrm{Mor}(\mathbb{F})$** | Closure predicate now evaluable | **Amended** |
| Obs 3.17.1 Functoriality | unchanged | DCV-001 | — | Hypothesis now **supplied** by Obs 3.15.1 rather than presupposed | **Retained** |
| Cor 6.2 | unchanged | DCV-001 | — | Becomes **unconditional**; the report had marked it "conditionally pass" pending a typed action | **Retained, strengthened** |

## 2. DCV-002 — representation component

| Old § | New § | Reason | Semantic effect | Proof effect | Status |
|---|---|---|---|---|---|
| **Def 3.18** tuple $(\mathfrak{B},(\mathfrak{M},\mathcal{F}),\mathcal{C},\mathcal{G})$ | **Def 3.18** clause 2 adds $\mathsf{r}$ | DCV-002 | $\mathsf{r}$ is exactly one of a supplied total measurable $(r,(\mathcal{R},\mathcal{H}))$ or the typed absence $\bot_{\mathrm{abs}}$ | A10 becomes a predicate determined by the tuple | **Amended** |
| *(none)* | **Obs 3.18.2 Effect of $\mathsf{r}$** | DCV-002 | Types both branches: supplied ⇒ A10 and Defs 7.1, 7.4, 7.5, 7.7 interpreted; absent ⇒ those are **typed inapplicable**, A10 neither true nor false | Thm 3 and Cor 3.3 explicitly unaffected either way | **Added** |
| *(none)* | **Def 3.18.3 Primitive-completeness table** | DCV-002 | Seven instance primitives and six context components, each with type, requiredness, indexing, totality and role | Closing statement: no Part A axiom depends on data absent from the table | **Added** |
| **A10** "If $r$ is supplied…" | **A10** names the instance component and the inapplicable branch | DCV-002 | No undeclared external datum | Prop 11.1′'s A10 check now draws $r$ from the instance | **Rewritten** |

## 3. Witness

| Old § | New § | Reason | Semantic effect | Proof effect | Status |
|---|---|---|---|---|---|
| Prop 11.1′ *Proof.* "Exhibit $\mathbb{T}=(\mathfrak{B},\mathfrak{M},\mathcal{C},\mathcal{G})$" | "Exhibit $\mathbb{T}=(\mathbb{F},\mathsf{r},\mathcal{C},\mathcal{G})$… component by component" | DCV-001, DCV-002 | Instance presented against the repaired tuple | — | **Amended** |
| **Carriers** paragraph | **Frame $\mathbb{F}$** paragraph | DCV-001 | Frame's four objects declared, including point separation of $W$ | — | **Rewritten** |
| $r$ mentioned inside *Carriers* | **Representation component $\mathsf{r}$ — supplied** | DCV-002 | $r$ stated as clause 2 of the instance, explicitly "instance data, not an external datum" | A10 check unchanged in substance | **Rewritten** |
| **Morphism group** paragraph | same, with per-component source/target check | DCV-001 | Each $\jmath$ component checked against Def 3.15's table; $\mathcal{G}\le\mathrm{Mor}(\mathbb{F})$ | Makes $\jmath\in\mathrm{Mor}(\mathbb{F})$ statable, which the prior signature could not | **Amended** |
| **Shared context components** | same, plus homogeneity note | DCV-001 | Records that clause 3 holds and that the witness instantiates the **general** signature, not a private structure | — | **Amended** |
| Contexts, closure, significance, eight A3 equations, A4–A10 | unchanged | — | **No numerical value changed** | All eight A3 equations recomputed and hold | **Retained** |
| Prop 11.1′ fragment list | adds Defs 3.14.1, 3.18.3; splits 3.15–3.18 | DCV-001, DCV-002 | Fragment closed under its own dependencies | — | **Amended** |

## 4. Obligations

| Old | New | Reason | Status |
|---|---|---|---|
| OB-A1 – OB-A3 | unchanged | — | **Retained**, non-blocking |
| *(none)* | **OB-A4** | DCV-002 | Whether $\mathsf{r}$ should be $\mathcal{G}$-equivariant. Recorded as **not required**: no Part A statement couples $\mathsf{r}$ and $\mathcal{G}$ | **Added**, non-blocking |
| *(none)* | **OB-A5** | DCV-001 | Formal placement in Part B of the heterogeneous carriers removed from Version 1; deferred because this pass may not modify Part B | **Added**, non-blocking |
| "None of OB-A1 – OB-A3 blocks" | "None of OB-A1 – OB-A5 blocks" | — | — | **Amended** |

## 5. Not changed

| Item | Evidence |
|---|---|
| **Part B** | Byte-identical to `HEAD`; verified by comparing the region from `# PART B` to end |
| Every Part A theorem statement and proof | Theorems 1, 3, 3.2′, 4′, 7′, 9, 10″, Corollaries 3.3, 6.2, 10.1″ — text unchanged |
| Definitions 3.1–3.12.1, 5.1–5.3, 6.1, 7.1, 7.4, 7.5, 7.7, 8.9 | unchanged |
| FR-1, A3, A4, A5, A7, A8, A9 | unchanged; only A10 rewritten |
| §A.10 results, limitations, rejections | unchanged |
| Frozen research controls | not staged, not modified |
| Prior verification reports | not modified |
