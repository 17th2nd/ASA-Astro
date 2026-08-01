# ASTRO-THEORY-0001 — Signature Completion Report

**Subject:** `docs/theory/ASTRO-THEORY-0001.md`
**Sole basis:** `ASTRO-THEORY-0001-VERSION-1-DETERMINISTIC-CORE-VERIFICATION.md`, findings **DCV-001** (Blocking) and **DCV-002** (Major).
**Pre-remediation blob:** `ad86bb978dc2d9a215af9f90d3a8cf9771f48d69`, confirmed at `HEAD` and worktree.
**Baseline:** `HEAD = origin/main = 848dc48a9e0cfdc1f7c03bcb0adc5d9a59ad5e07`, `main`, 0/0, clean worktree.
**Status:** Theory Candidate. **Not frozen in this pass.**

---

## 1. Summary

Two findings, both fully closed. The pass is a signature completion, not a redesign: **no theorem statement or proof was altered**, and Part B is byte-identical to `HEAD`.

| Measure | Count |
|---|---|
| Findings adjudicated | 2 of 2 |
| Blocking closed | 1 (DCV-001) |
| Major closed | 1 (DCV-002) |
| Theorems altered | **0** |
| Definitions added | 3 (3.14.1, 3.18.3, and the retyped 3.15) |
| Observations added | 4 (3.14.2, 3.15.1, 3.17.0, 3.18.2) |
| Definitions amended | 2 (3.17, 3.18) |
| Axioms rewritten | 1 (A10) |
| Obligations added | 2 (OB-A4, OB-A5), both non-blocking |
| Part A lines | 374 → 441 |
| Part B | unchanged |

**Option A adopted for DCV-001,** with the three-part justification in the adjudication: no Part A theorem uses heterogeneous carriers, so nothing is lost; every group law reduces to a componentwise fact, so nothing new is needed; and Option B would require positing target carriers as morphism data plus a coherence proof, which is additional structure this pass may not add.

**Version 1 is homogeneous.** Heterogeneous context-indexed outcome spaces and codomains are removed from Version 1 and deferred as Candidate material. Their formal placement inside Part B is **OB-A5**, deferred only because this pass was instructed not to modify Part B.

---

## 2. DCV-001 — closed

The report's decisive point was that $\iota_*C$ must be typed **before** the closure predicate $\iota_*C\in\mathcal{C}$ can be evaluated, so closure could not supply the missing domains and codomains, and functoriality presupposed a composability it did not establish.

Repair chain, each link discharging a named obligation:

1. **Definition 3.14.1** declares a frame with one outcome space and one codomain.
2. **Definition 3.15** tabulates each morphism component with **explicit source and target**; $\iota_{\mathcal{Y}}$ is a bimeasurable bijection of the frame's $(\mathcal{Y},\mathcal{G}_{\mathcal{Y}})$ and $\iota_W$ an automorphism of the frame's $(W,\preceq_W,\Sigma_W)$.
3. **Observation 3.15.1** proves identity, composition, inverse, associativity and unit componentwise, so $\mathrm{Mor}(\mathbb{F})$ is a group.
4. **Observation 3.17.0** proves transport is well typed, so $\iota_*C$ is a context over the same frame and the closure predicate is evaluable before closure is imposed.
5. **Definition 3.18** clauses 1, 3, 4 carry the frame, the homogeneity requirement, and $\mathcal{G}\le\mathrm{Mor}(\mathbb{F})$.

Everything the instruction required to be well typed now is: transported contexts, closure, A3, $\mathrm{Aut}(C)$, Corollary 6.2, Proposition 11.1′ and the four-context witness. **Corollary 6.2 becomes unconditional**, where the report had marked it "conditionally pass".

## 3. DCV-002 — closed

**Definition 3.18 clause 2** places the representation component in the tuple as exactly one of a supplied total measurable $(r,(\mathcal{R},\mathcal{H}))$ or the typed absence $\bot_{\mathrm{abs}}$. **Observation 3.18.2** types both branches: supplied means A10 and Definitions 7.1, 7.4, 7.5, 7.7 are interpreted with that $r$; absent means they are **typed inapplicable**, with A10 neither true nor false and no identified output or sufficiency predicate defined. Theorem 3 and Corollary 3.3 are explicitly unaffected either way, since they quantify over their own hypothesised maps.

**A10 is rewritten** to name the instance component. **Definition 3.18.3** supplies the primitive-completeness table and the closing statement, itemised axiom by axiom, that no Part A axiom depends on data absent from the instance.

---

## 4. Witness recheck

Recomputed in full against the repaired signature. **No numerical value changed.** What changed is provenance: every datum is now a clause of Definition 3.18 or a component of Definition 3.10, so the witness instantiates the **general** signature rather than a private structure.

- Frame, $\mathsf{r}$, $\mathcal{C}$, $\mathcal{G}$ each checked against their clause.
- $\jmath$'s four components each checked against Definition 3.15's source/target table — a statement the prior signature could not make.
- Closure proved from functoriality and $\jmath\circ\jmath=\mathbf{1}$.
- All four transports recomputed: $C_1\leftrightarrow C_2$, $C_0\leftrightarrow C_0'$.
- Significance: $2,1,1,2,0,0,0,0$.
- **All eight non-identity A3 equations hold**, and $\jmath\neq\mathbf{1}$, so A3 is verified non-vacuously.
- A4, A5, A7, A8, A9, A10 each rechecked; A10 now draws $r$ from the instance.

---

## 5. Validation performed

| Audit | Result |
|---|---|
| Primitive-completeness | **Pass** — Definition 3.18.3 covers seven instance and six context primitives; no Part A axiom depends on absent data |
| Theory-instance tuple | **Pass** — frame, $\mathsf{r}$, $\mathcal{C}$, $\mathcal{G}$, with homogeneity and closure clauses |
| Source/target type | **Pass** — Definition 3.15 table |
| Group action | **Pass** — Observation 3.15.1 |
| Identity | **Pass** — $\mathbf{1}$ exhibited componentwise |
| Composition | **Pass** — componentwise closure of each component class |
| Inverse | **Pass** — each component class closed under inverse |
| Functoriality | **Pass** — Observation 3.17.1 retained, hypothesis now supplied |
| Transport | **Pass** — Observation 3.17.0 |
| A3 typing | **Pass** — both sides in $\widehat W$ for the frame's single $W$ |
| A10 typing | **Pass** — instance component named; absent branch typed inapplicable |
| Witness reconstruction | **Pass** — no value changed; every datum instance-sourced |
| Part A / Part B boundary | **Pass** — mechanical check returns no Part A reference to a Part B identifier; Part B byte-identical to `HEAD` |
| Theorem dependency | **Pass** — no theorem statement or proof altered |
| Cross-reference | **Pass** — all references resolve; only withdrawn statements are cited in withdrawal contexts |
| Notation | **Pass** — no symbol overloaded across incompatible types |
| Markdown / LaTeX | **Pass** — inline and display delimiters balanced; braces balanced |

Mechanical checks are evidence of document integrity only. They are not mathematical proof.

---

## 6. Remaining obligations

**Part A, all non-blocking and used by no proof:** OB-A1 fibre-constancy characterisation; OB-A2 wider-setting measurability; OB-A3 encodability outside point-separating codomains; **OB-A4** whether $\mathsf{r}$ should be $\mathcal{G}$-equivariant — recorded as *not required*, since no Part A statement couples them; **OB-A5** formal placement of the removed heterogeneous case in Part B.

**Part B:** OB-B1 – OB-B4 unchanged, Candidate, outside this pass.

**No blocking obligation remains against the deterministic core.**

---

## 7. Re-verification readiness

A verifier should check, in order:

1. **Definition 3.15's table** — that every component has a declared source and target and that the classes are closed under composition and inverse.
2. **Observation 3.15.1** — the five group laws.
3. **Observation 3.17.0** — that $\iota_*C$ is typed independently of the closure requirement. This is the specific defect DCV-001 identified.
4. **Definition 3.18** — five clauses; in particular that homogeneity is imposed at instance level and that $\mathcal{G}\le\mathrm{Mor}(\mathbb{F})$.
5. **Definition 3.18.3** — completeness of the primitive table against every Part A axiom.
6. **Observation 3.18.2** — that the $\bot_{\mathrm{abs}}$ branch is typed rather than left silent.
7. **Proposition 11.1′** — that the witness instantiates the general signature and that all eight A3 equations still hold.
8. **Part B** — byte-identical to `848dc48`.

**Known scope reduction.** Option A narrows the admitted instances: only homogeneous ones remain in Version 1. This is a real loss of generality, stated in Observation 3.14.2 rather than concealed, and it costs no retained result.

---

## 8. Final determination

> **ASTRO-THEORY-0001 SIGNATURE COMPLETED — READY FOR FINAL VERIFICATION**

Both findings are fully closed. No theorem was altered. Part B and the frozen research controls are untouched. The theory is **not frozen** in this pass.
