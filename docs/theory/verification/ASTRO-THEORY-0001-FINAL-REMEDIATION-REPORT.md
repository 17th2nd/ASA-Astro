# ASTRO-THEORY-0001 — Final Deterministic-Core Remediation Report

**Subject:** `docs/theory/ASTRO-THEORY-0001.md`
**Sole defect basis:** `docs/theory/verification/ASTRO-THEORY-0001-FINAL-INDEPENDENT-VERIFICATION.md`, determination **DETERMINISTIC CORE REQUIRES BOUNDED REMEDIATION**, findings FV-001 – FV-006. Read in full; not modified.
**Pre-remediation blob:** `0d64e4fd1fa8d6668ece38c6ec4f0fab73479210`, confirmed at `HEAD` and worktree before mutation.
**Baseline:** `HEAD = origin/main = 26417eb4e7dad9bf09260b1d60d6b46ca78d759b`, branch `main`, 0 ahead / 0 behind.
**Status after this pass:** Theory Candidate. **Not frozen.**

---

## 1. Remediation summary

Six findings, all adjudicated, none rejected. Every counterexample in the report was reconstructed independently before adjudication and every one held.

| Measure | Count |
|---|---|
| Findings adjudicated | **6 of 6** |
| Blocking | 3 — FV-001, FV-003, FV-004 |
| Major | 3 — FV-002, FV-005, FV-006 |
| Accepted | 2 |
| Accepted with Modification | 3 |
| Withdrawn Statement | 1 |
| Rejected with Proof | 0 |
| Theorems withdrawn and replaced | **2** (Theorem 10′, Proposition 11.1) |
| Corollaries withdrawn and replaced | **1** (Corollary 10.1′) |
| Rejections withdrawn | **2** (16.1, 16.13) |
| Definitions added | **5** (3.5.1, 3.12.1, 3.18, plus Observations 3.5.2, 3.17.1 carrying proofs) |
| Axioms narrowed | **1** (A3) |
| Axioms reclassified | **1** (A2 → formation rule FR-1) |

**The pass is bounded.** No new architecture, no novelty claim, no scope expansion. Part B enrichments were relocated and labelled but not otherwise altered, except where the deterministic core required it — namely the two signed codomain classes, which moved out of the core because no Part A theorem uses subtraction.

**Two things the core now says it cannot do.** §A.10.2.1 states that the deterministic core **does not exclude intrinsic significance**: the assignment $\sigma_C(b)=0$ for all $C$ and $b$ is context-independent, satisfies A4, and is excluded by no Part A axiom. §A.10.2.2 states that no universal absence of a context-free ordering is established. Both were previously asserted, in weaker or stronger form, and both are now withdrawn with the counterexample recorded in the text rather than only in this report.

---

## 2. Blocking findings resolved

| Finding | Outcome | Resolution |
|---|---|---|
| **FV-001** | Repaired with proof; axiom narrowed | Definition 3.18 declares the theory instance $(\mathfrak{B},\mathfrak{M},\mathcal{C},\mathcal{G})$ with closure under transport as an instance requirement. A3 now quantifies over the declared $\mathcal{G}$ — an explicit narrowing, recorded as such — and A4 over the declared $\mathcal{C}$. Both become predicates over declared carriers. |
| **FV-003** | Scope narrowed with proof | Theorem 10′ was **false** on the two-point codomain with the trivial $\sigma$-algebra. Definition 3.5.1 introduces point-separating codomains; Observation 3.5.2 proves point separation equivalent to injectivity of $x\mapsto\delta_x$, which is exactly what makes the atom reduction (Definition 3.12.1) a function. Theorem 10″ and Corollary 10.1″ carry the hypothesis. |
| **FV-004** | Affected proposition withdrawn and replaced | The claim $\jmath_*C_0=C_0$ was **false**; the transport yields outcome map $y$ and operations shifting $x$. Proposition 11.1′ adds $C_0':=\jmath_*C_0$ to the context set and **proves** closure from functoriality (Observation 3.17.1) and involutivity of $\jmath$, rather than asserting it. |

## 3. Blocking findings remaining

**None.**

No blocking obligation is created by this pass. OB-A1, OB-A2 and OB-A3 are non-blocking and are used by no Part A theorem. The former OB-1 is split: its deterministic portion — A3 over the morphism universe — is **discharged for the core** by Definition 3.18 and Proposition 11.1′; its enrichment portion becomes OB-B3 and is Candidate, outside the Version 1 claim.

---

## 4. Theorems withdrawn

| Statement | Ground |
|---|---|
| **Theorem 10′** — encodability on every nonempty codomain | **False.** $W=\{0,1\}$ with $\Sigma_W=\{\emptyset,W\}$ carries exactly one probability measure, so $\delta_0=\delta_1$ and no reduction can return both atoms. |
| **Corollary 10.1′** — bounded underdetermination on every codomain | Depends on Theorem 10′. |
| **Proposition 11.1** — deterministic consistency | Contains a **false componentwise equality** ($\jmath_*C_0=C_0$); the context set was not closed; the fragment omitted Definitions 5.1–5.3. |
| **Rejection 16.1** — rejection of intrinsic significance | **Does not follow.** A function of $(C,b)$ may be constant in $C$; $\sigma\equiv0$ satisfies A4 and no other axiom excludes it. |
| **Rejection 16.13** — artefact independence | "Artefact relabelling" and "declared universe" are undefined in the signature. Only Corollary 6.2 survives. |
| **Axiom A2** | Reclassified as formation rule FR-1; Definition 3.10 already requires all seven components, so A2 was not a substantive predicate. |

## 5. Theorems narrowed

| Statement | Narrowing |
|---|---|
| **A3** | Quantifier narrowed from all representation morphisms to the instance's declared group $\mathcal{G}$ |
| **Theorem 1** | Declares point separation and the named atom reduction; quantifier and totality stated explicitly |
| **Theorem 7′** | Family $\mathcal{K}$ is now a subset of a declared $\mathcal{C}$ |
| **Theorem 10″** | Point-separating codomains only; deterministic contrast form; projection evaluator; single context |
| **Corollary 10.1″** | Same restriction; explicit non-conclusions in Observation 10.1.1 |
| **Observation 10.0.1** | Universal assertion removed; explicit silence on non-separating codomains |
| **Limitation 14.11′, 14.12′** | Restricted to the proved class and the exact witness instance respectively |
| **Rejection 16.17** | Annotated as a statement about the signature only, not about the existence of a context-independent significance function |

**Verified and unchanged:** Theorem 3, Theorem 3.2′, Corollary 3.3, Theorem 4′, Theorem 9, Corollary 6.2, Limitations 14.4 and 14.7 — each confirmed by the verifier and carried forward without alteration to content.

---

## 6. Consistency status

**Established.** Proposition 11.1′ exhibits a theory instance $\mathbb{T}=(\mathfrak{B},\mathfrak{M},\mathcal{C},\mathcal{G})$ with $\mathfrak{B}=\{b_1,b_2\}$, $\mathfrak{M}=\mathbb{R}^2$ Borel, $\mathcal{G}=\{\mathrm{id},\jmath\}$ the coordinate-swap involution group, and $\mathcal{C}=\{C_1,C_2,C_0,C_0'\}$ **proved closed** under $\mathcal{G}$. FR-1 and axioms A3, A4, A5, A7, A8, A9, A10 are each checked. A3 is checked over **eight non-identity instances** and $\jmath\neq\mathrm{id}$, so the check is **not vacuous**. A4 is satisfied by $C_0$, which gives $0_W$ to both bearers.

**Claim scope.** Observation 11.1.2 is binding: the claim covers exactly the deterministic core signature and axioms named in the proposition, over that instance. It does **not** cover anything in Part B, nor interval- or bottom-valued outputs, nontrivial $\approx_C$, non-atomic measures, non-point-separating codomains, or codomains outside class $\mathsf{W}_1$.

**The consistency claim does not exceed the witness.** No statement anywhere in the document calls the full theory consistent.

**Not relied upon:** identity-only morphisms; vacuous automorphism claims; omitted context components; undeclared reductions; uninstantiated codomain structures; undefined partial maps. Each of these was a defect of the prior witness and each is addressed.

---

## 7. Validation performed

| Audit | Method | Result |
|---|---|---|
| Deterministic signature | manual | Every Part A object has carrier, type, domain, codomain, totality, indexing and dependencies declared |
| Core/enrichment dependency | manual, per Part A proof | **No Part A proof cites a Part B object.** Verified by reading each proof's citations |
| Theorem dependency | manual | Thm 1 ← Def 3.12.1, 5.1–5.3; Cor 6.2 ← A3; Thm 3.2′ ← Thm 3; Cor 3.3 ← Thm 3; Thm 4′ ← A8; Thm 7′ ← A4, Def 3.18; Thm 10″ ← Def 3.5.1, 3.12.1; Prop 11.1′ ← Def 3.17.1, 3.18 |
| Consistency witness | manual | Closure proved, not asserted; A3 non-vacuous over eight instances; all named definitions enumerated |
| Type | manual | Every theorem names codomain class and form |
| Domain/codomain | manual | $\rho_C:\Delta(W_C)\rightharpoonup\widehat{W_C}$; $\rho^{\mathrm{at}}$ domain $\{\delta_x\}$; $\delta_C$ partial on $D_C$ |
| Partiality | manual | $T_C$, $\delta_C$, $\rho_C$, $\rho^{\mathrm{at}}$, $\ell$, $\sigma_C$, $\bar\delta_C$ all marked partial |
| Quantifier | manual | Thm 1 and Thm 10″ labelled existential; Thm 3, 4′, 7′, 9 and Cor 6.2 universal; verified-results table carries a quantifier column |
| Counterexample search | manual | Both verifier counterexamples reproduced (FV-003 two-point codomain; FV-004 transport of $C_0$); the FV-006 $\sigma\equiv0$ assignment checked against all seven axioms |
| Cross-reference | mechanical + manual | All references resolve; withdrawn statements are cited only in withdrawal contexts |
| Notation | manual | No symbol overloaded across incompatible types |
| LaTeX delimiters | mechanical | Balanced |
| Theorem numbering | manual | Double primes mark this pass's replacements; withdrawn numbers not reused |
| Frozen-control exclusion | mechanical | No frozen research control staged or modified |

**Mechanical checks do not constitute mathematical verification.**

---

## 8. Re-verification readiness

A re-verifier should prioritise:

1. **Definition 3.18** — confirm that declaring $\mathcal{C}$ and $\mathcal{G}$, with closure as an instance requirement, makes A3 and A4 predicates over the signature, and that the narrowing of A3's quantifier is stated rather than concealed.
2. **Theorem 10″** — confirm point separation excludes the two-point counterexample, and check Observation 3.5.2's equivalence in both directions. Consider whether point separation is *necessary* (OB-A3).
3. **Proposition 11.1′** — recompute $\jmath_*C_1$ and $\jmath_*C_0$, confirm $\mathcal{C}$ is closed, and confirm the eight A3 instances.
4. **Definition 5.2** — confirm the subspace construction is an instance of the ordinary pushforward and that no extension is used.
5. **§A.10.2** — confirm the core's stated non-conclusions are complete, particularly A.10.2.1 on intrinsic significance.
6. **Freeze boundary** — confirm no Part A proof cites a Part B object.

**Known limitations carried forward:**

- OB-A1, OB-A2, OB-A3 are open and non-blocking.
- OB-B1 – OB-B4 are Candidate and outside the Version 1 claim; **no Part B item has a consistency proof**.
- The deterministic core does not exclude intrinsic significance, and does not establish any universal absence of a context-free ordering.
- No empirical, novelty, recognisability or prior-art claim is made.

**Provenance caveat.** The final verification report was **untracked** in the worktree at the time of this pass. Per instruction it was neither modified nor staged. Its basis is pinned in the adjudication record by path, size and examined blob. If the report is later committed under a different content hash, this remediation's basis should be re-confirmed.

---

## 9. Final determination

> **ASTRO-THEORY-0001 DETERMINISTIC CORE REMEDIATED — READY FOR FINAL RE-VERIFICATION**

All three Blocking findings are closed: FV-001 by a declared signature object with a stated axiom narrowing, FV-003 by a proved hypothesis, FV-004 by a withdrawn proposition and a replacement whose closure is proved. All three Major findings are closed. No blocking obligation remains against the deterministic core, and the consistency claim does not exceed its witness.

The theory is **not frozen** in this pass.
