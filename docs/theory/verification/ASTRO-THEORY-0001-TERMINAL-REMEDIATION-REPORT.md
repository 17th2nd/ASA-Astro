# ASTRO-THEORY-0001
## Terminal Remediation Report — Version 1 Deterministic Core

## 1. Control

| Field | Value |
|---|---|
| Repository | `17th2nd/ASA-Astro` |
| Baseline commit | `691a4d866ef164ba8e177ea59cf1bb3d1565c9b7` |
| `HEAD == origin/main`, `0/0`, clean worktree before mutation | Confirmed |
| Theory blob before → after | `c20ca91fa18551f247dfa1c150dea3f9d9b510d5` → `6fc866796b0a9c39d3f7384d4118fce8ee7ae5ac` |
| Authoritative defect basis | `verification/ASTRO-THEORY-0001-FINAL-VERSION-1-VERIFICATION.md`, read in full |
| Date | 2026-08-02 (Australia/Brisbane) |
| Files modified | `docs/theory/ASTRO-THEORY-0001.md` only |
| Part B | Byte-identical |
| Existing verification reports | Not modified |
| Status | **Candidate.** Not frozen |

Sixteen audits were required. Each is reported below with its result and, where a check is mechanical, the evidence.

---

## 2. Primitive-completeness audit

Every primitive needed to interpret every Part A definition and axiom is now a row of Definition 3.18.3. The three omissions the final verification recorded as blocking are resolved:

| Prior blocking omission | Resolution |
|---|---|
| Class-$\mathsf{W}_1$ operation $\oplus$ and identity $0_W$ | Now the **class datum $\mathsf{c}$**, a required typed component of the codomain object $\mathbb{W}$ (Definition 3.6), carried in the frame and tabulated with its role in A4, Definition 3.15 (W-c), Theorems 1, 7′ and Proposition 11.1′ |
| Optional cross-context transport $t$ or its typed absence | **No longer used.** Definition 8.9 and A7 are withdrawn (Observation 8.9.1), so no such primitive is owed |
| Identified-output function and carrier | Declared: carrier $\widehat{W}^{\mathrm{id}}$ (Definition 3.8.1) and function $\mathrm{Id}^b_C$ (Definition 7.5); tabulated as a derived object in Definition 3.18.4 |
| $\bot_{\mathrm{abs}}$ omitted from the table (recorded as table incompleteness) | Row added |

The table's closing assertion was previously **false**. It is now checked term by term:

| Axiom | Data it ranges over | All tabulated? |
|---|---|---|
| A3 | $\mathcal{G}$, $\mathcal{C}$, and $\widehat W$ via Definition 3.16 | Yes |
| A4 | $\mathcal{C}$ and the class datum $\mathsf{c}$ | Yes |
| A5 | $\widehat W$ | Yes |
| A8 | $\approx_C$, $\delta_C$ | Yes |
| A9 | $\Omega^b_C$, from $M_C$, $T_C$, $\delta_C$ | Yes |
| A10 | $\mathsf{r}$ and $\mathrm{Id}^b_C$ (Definition 3.18.4) | Yes |

A new **Definition 3.18.4** tabulates twelve derived objects with declared type, totality and formation condition, so that no axiom depends on an object whose type is only implicit.

**Result: pass.**

---

## 3. Formal-signature audit

The signature is closed under the following check: every symbol occurring in a Part A definition, axiom, theorem statement or proof is either (i) a component of the theory instance, (ii) a derived object of Definition 3.18.4, or (iii) locally quantified by the statement that uses it.

Locally quantified data — $g$, $h$, $S$, $\beta$, $\mathcal{K}$, $f$, $\varphi$, $p$, $w_0$ and the quotient projection — remain local, as the final verification accepted.

**Result: pass.**

---

## 4. Codomain-structure audit

| Check | Result |
|---|---|
| Carrier and additional structure separated | Definition 3.5 is the bare carrier and explicitly carries **no** algebraic structure; Definition 3.6 is the codomain object |
| Class datum is a selection, not a property | Observation 3.6.1: one carrier may admit many operations satisfying (M1)–(M5) and none canonically |
| Laws stated | (M1) associativity, (M2) commutativity, (M3) unit, (M4) order compatibility, (M5) $0_W$ least |
| Laws honestly scoped | Observation 3.6.2 records that **no Part A proof discharges (M1)–(M5) abstractly**; they make the class determinate, and the concrete realisation satisfies them by arithmetic |
| Typed absence | $\mathsf{c}=\bot_{\mathrm{abs}}$ gives class $\mathsf{W}_0$; no statement may then refer to $\oplus$ or $0_W$ |
| Morphisms preserve **exactly** the selection | Definition 3.15 (W-a)–(W-c), with (W-c) branching on $\mathsf{c}$ and imposing nothing in the $\mathsf{W}_0$ branch |
| Group closure under the new condition | Observation 3.15.1 proves composition and inverse preserve (W-c), with the computations shown |
| Instance selects it explicitly | Definition 3.18 frame slot 4; clause 3 requires $\mathbb{W}_C=\mathbb{W}$, class datum included |
| Witness instantiates through the tuple | Proposition 11.1′ frame paragraph; (M1)–(M5) verified for $(\mathbb{R}_{\ge0},+,0,\le)$ |
| $\mathsf{W}_1$ not required where unused | Theorem 10″ admits either class and says so; Theorems 3, 3.3, 4′, 9 and Corollary 6.2 impose no class condition |

**Result: pass.**

---

## 5. Theory-instance audit

The tuple is seven components: $\mathfrak{B}$, $(\mathfrak{M},\mathcal{F})$, $(\mathcal{Y},\mathcal{G}_{\mathcal{Y}})$, $\mathbb{W}$, $\mathsf{r}$, $\mathcal{C}$, $\mathcal{G}$. $\mathbb{F}$ and $\mathbb{T}$ are **declared abbreviations** for exactly these, introduced by Definition 3.18, which states that $\mathbb{T}$ "has no components other than the seven displayed above."

The superseded equality $\mathbb{T}=(\mathfrak{B},\mathfrak{M},\mathcal{C},\mathcal{G})$ is removed from the axiom section and replaced by a *Ranging convention* that displays the complete tuple and states that **every axiom ranges over it**. The four-component form is recorded as superseded and withdrawn, and expressly **not** an abbreviation for the current tuple.

Mechanical check: the string `(\mathfrak{B},\mathfrak{M},\mathcal{C},\mathcal{G})` occurs once in Part A, inside the sentence that withdraws it.

**Result: pass.**

---

## 6. Extended-action audit

Definition 3.16 now declares $\widehat{\iota_W}:\widehat W\to\widehat W$. Observation 3.16.1 verifies, in order:

| Check | Where | Result |
|---|---|---|
| Ordinary values | row 1; 3.16.1(c) | $\iota_W(x)\in W$ by (W-a) |
| Intervals | row 2; 3.16.1(b),(c) | Representation-independent, because $u$ and $v$ are the least and greatest elements of the set $[u,v]$ and are unique by antisymmetry; the image is an interval by (W-a) |
| Every bottom | row 3 | All three bottoms fixed, individually |
| Identity | 3.16.1(d) | $\widehat{\mathrm{id}_W}=\mathrm{id}_{\widehat W}$ |
| Composition | 3.16.1(e) | $\widehat{\iota_W\circ\kappa_W}=\widehat{\iota_W}\circ\widehat{\kappa_W}$, checked on all three summands |
| Inverse | 3.16.1(f) | $\widehat{(\iota_W)^{-1}}=(\widehat{\iota_W})^{-1}$; $\widehat{\iota_W}$ is a bijection |
| Transported reductions | 3.16.1(g), Observation 3.17.0 | $\rho_{\iota_*C}:\Delta(W)\rightharpoonup\widehat W$ derived, not asserted |
| A3 | 3.16.1(g), A3 | Both sides shown to lie in the one set $\widehat W$ |
| Corollary 6.2 | proof rewritten | $\widehat{\pi_W}=\mathrm{id}_{\widehat W}$ now derived from 3.16.1(d) |
| Witness | Proposition 11.1′, *Extended action* | $\widehat{\jmath_W}=\mathrm{id}_{\widehat W}$ derived from 3.16.1(d) |

**Undeclared $W'$: eliminated.** Search over the repaired text returns the symbol only in the sentence recording its removal and in the quoted withdrawn Definition 8.9.

**Result: pass.**

---

## 7. Transport audit

Option A was taken: Definition 8.9 and axiom A7 are **withdrawn**. The three grounds are recorded in Observation 8.9.1 and adjudicated in the Terminal Adjudication §4.1.

The instruction's terminal condition — "A7 must be a testable predicate over the declared theory instance **or** be withdrawn from Version 1" — is met by withdrawal.

Verification that removal withdraws no result: each retained statement was checked individually for a citation of Definition 8.9 or A7.

| Statement | Cites 8.9 or A7? |
|---|---|
| Theorem 1, Theorem 3, Corollary 3.3, Theorem 3.2′, Theorem 4′, Theorem 7′, Theorem 9, Theorem 10″, Corollary 6.2, Corollary 10.1″, Proposition 11.1′ | **None** |

Consequential propagation was completed at every site: Observation A.3.1, Observation A.3.2, Definition 3.18.3 (row and closing sentence), Observation 10.1.1, Proposition 11.1′ (claim and satisfaction list), limitation 14.7 → 14.7′, rejected formulation 16.12 (withdrawn), and OB-A6 (new).

**No heterogeneous transport system was introduced.**

**Result: pass.**

---

## 8. Optionality audit

Three optional data exist, each with an explicitly typed absence:

| Optional datum | Supplied form | Typed absence | Effect of absence |
|---|---|---|---|
| $\mathsf{r}$ | $(r,(\mathcal{R},\mathcal{H}))$, $r$ total and measurable | $\bot_{\mathrm{abs}}$ | A10, Theorem 3.2′ and Definitions 7.1, 7.4, 7.5, 7.7 **not formed**; inapplicable, not vacuously true (Observation 3.18.2) |
| $\mathsf{c}$ | $\mathsf{W}_1(\oplus,0_W)$ | $\bot_{\mathrm{abs}}$ (class $\mathsf{W}_0$) | A4 **not satisfied**; Definition 3.15 (W-c) imposes no condition (Observation A.3.0) |
| $\approx_C$ | equivalence on $\mathcal{Y}$ | $\bot_{\mathrm{abs}}$ | A8 antecedent false; Theorem 4′ inapplicable |

The distinction is maintained: $\mathsf{r}$ absent produces **inapplicability**, whereas $\mathsf{c}$ absent produces **failure of A4**. These are different states and the text says so explicitly. A4 was deliberately **not** converted into a typed-inapplicability branch, since that would redesign the axiom system rather than close a defect.

**Result: pass.**

---

## 9. Identified-output type audit

| Required declaration | Value | Where |
|---|---|---|
| Symbol | $\mathrm{Id}^b_C$ | Definition 7.5 |
| Domain | $\mathcal{R}$ | Definition 7.5 |
| Codomain | $\widehat{W}^{\mathrm{id}}$ | Definitions 3.8.1, 7.5 |
| Total / partial | Total on $\mathcal{R}$; family formed exactly when $\mathsf{r}$ supplied and $T_C(b)$ defined | Definition 7.5, Observation 7.5.1(a) |
| Supplied-$\mathsf{r}$ applicability | Supplied branch only | Definition 7.5, Observation 3.18.2 |
| Output carrier contains $\bot_{\mathrm{inc}}$ | Yes | Definition 3.8.1 |
| Output carrier contains $\bot_{\mathrm{und}}$ | Yes | Definition 3.8.1 |
| Output carrier contains the set-valued output | Yes — $\mathcal{P}_{\neq\emptyset}(W)$ | Definition 3.8.1, Observation 7.5.1(b) |

**$\widehat W$ was not extended.** Definition 3.8 now states that $\widehat W$ contains no subset of $W$ other than the order-intervals and is not extended anywhere below; Observation 3.8.2 records that the two carriers are distinct and that neither is a subobject of the other. One coherent design is chosen and stated, and the reason a single-valued design was rejected — Theorem 3.2′ must be able to state $|\mathcal{S}_C(b,x)|\ge2$ — is recorded in Observation 7.5.1(c).

A10 and Theorem 3.2′ were updated to use the typed function.

**Result: pass.**

---

## 10. Axiom quantifier audit

| Axiom | Quantification |
|---|---|
| A3 | "For every $\iota\in\mathcal{G}$, every $C\in\mathcal{C}$ and every $b\in\mathfrak{B}$" — explicit before and after |
| A4 | Class conjunct on the instance; "for every $b\in\mathfrak{B}$ there exists $C\in\mathcal{C}$" |
| A5 | **Added:** "For every $C\in\mathcal{C}$ and every $b\in\mathfrak{B}$" |
| A8 | **Added:** "For every $C\in\mathcal{C}$ … for all $(y,y'),(\tilde y,\tilde y')\in D_C$" |
| A9 | **Added:** "For every $C\in\mathcal{C}$ and every $b\in\mathfrak{B}$ with $T_C(b)$ defined" |
| A10 | **Added:** "for every $C\in\mathcal{C}$, every $b\in\mathfrak{B}$ with $T_C(b)$ defined, and every $x\in\mathcal{R}$" |
| A7 | Withdrawn; no quantifier owed |

No free variable remains in any axiom. The axioms of Version 1 are exactly **A3, A4, A5, A8, A9, A10**, recorded in Observation A.3.1.

**Result: pass.**

---

## 11. Theorem dependency audit

Every retained theorem was re-checked against its stated hypotheses under the repaired signature.

| Result | Depends on | Determination |
|---|---|---|
| Theorem 1 | Definitions 3.6, 3.10, 5.1–5.3, 3.12.1 | **Pass.** Unaffected except that its codomain object is now supplied as a tuple |
| Corollary 6.2 | A3, Definitions 3.16, 6.1 | **Pass, and now typed.** Depended on the extended action, which TR-1 repaired; proof rewritten to derive $\widehat{\pi_W}=\mathrm{id}_{\widehat W}$ |
| Theorem 3 | Definition 7.1 only; arbitrary $r$ | **Pass.** Applicable in both $\mathsf{r}$ branches; untouched |
| Corollary 3.3 | Theorem 3 with $r:=M_C$ | **Pass.** Untouched |
| Theorem 3.2′ | $\mathsf{r}$ supplied; Definitions 7.4, 7.5; Theorem 3 | **Pass in the supplied branch, and now gated to it.** Absent branch typed inapplicable, no vacuous truth |
| Theorem 4′ | A8, $\approx_C$ supplied | **Pass.** Untouched |
| Theorem 7′ | Instance with $\mathbb{W}$ concrete; hypotheses (a), (b) | **Pass.** Hypothesis restated through the codomain object |
| Theorem 9 | Arithmetic only | **Pass.** Untouched |
| Theorem 10″ | Point-separating carrier; class datum arbitrary | **Pass as a context-existence theorem**, now stated as one, with its frame made explicit |
| Proposition 11.1′ | The full repaired signature | **Pass.** Recomputed in §14 |

No retained proof cites Part B. No proof cites a withdrawn object.

**Result: pass.**

---

## 12. Corollary-scope audit

The final verification's finding was that Corollary 10.1″ exceeded Theorem 10″ under the homogeneous A4 requirement. Option **B** was adopted.

| Site | Overbroad claim before | Now |
|---|---|---|
| Corollary 10.1″ | "no single-context assignment is excluded **by the axioms**" | Realisability by the Theorem 10″ construction only |
| Observation 10.0.1 | "the **axioms** therefore do not exclude degenerate evaluators" | "the **deterministic contrast form** does not itself exclude"; explicit disclaimer about the axioms |
| Observation 10.1.1 | Listed A3, A4, A7 as further constraints | Restated; A5, A8, A9, A10 added; A7 removed; realisability/consistency distinction made |
| Limitation 14.11′ | "no single-context assignment is excluded" | "realised by the construction"; "**Nothing follows about exclusion by the axioms**" |
| Result register, 10″ | "Encodability on point-separating codomains" | "**context-existence only; no axiom is verified**" |

**Prohibited phrase check.** The phrase "the axioms exclude no assignment" and its equivalents — "not excluded by the axioms", "the axioms do not exclude", "excluded by no Part A axiom" — were searched for across Part A. Exactly two occurrences survive:

| Site | Occurrence | Assessment |
|---|---|---|
| **Observation 10.1.0** | The phrase appears **inside the sentence that forbids it**: "The phrase … does not occur in Version 1" | Not an assertion of the claim |
| **§A.10.2.1** | "…is context-independent, satisfies A4, and is excluded by no Part A axiom" | A **different** claim — the FV-006 statement about intrinsic significance, about one specific assignment $\sigma\equiv0_W$ rather than about all assignments on an arbitrary carrier. Qualified in this pass to require a class-$\mathsf{W}_1$ instance |

**Observation 10.0.1 contains no such phrasing after repair**: it now says the *deterministic contrast form* "does not itself exclude degenerate evaluators", and adds an express disclaimer about the axioms.

The encodability claim itself — that the axioms exclude no assignment on an arbitrary point-separating carrier — occurs nowhere in Version 1.

**Result: pass.**

---

## 13. Consistency-witness reconstruction

The witness was reconstructed independently — not read back from the text — and then compared with the text.

**Frame.** $\mathfrak{B}=\{b_1,b_2\}$; $(\mathfrak{M},\mathcal{F})=(\mathbb{R}^2,\mathcal{B})$; $(\mathcal{Y},\mathcal{G}_{\mathcal{Y}})=(\mathbb{R},\mathcal{B})$; $\mathbb{W}=((\mathbb{R}_{\ge0},\le,\mathcal{B}),\mathsf{W}_1(+,0))$. (M1)–(M5) verified. Point-separating by Observation 3.5.2.

**Representation component.** $\mathsf{r}=(\mathrm{id}_{\mathfrak{M}},(\mathfrak{M},\mathcal{F}))$; total, measurable; $\mathcal{H}_r=\mathcal{F}$.

**Group.** $\mathcal{G}=\{\mathbf{1},\jmath\}$; (W-a), (W-b), (W-c) checked for $\jmath_W=\mathrm{id}$; $\jmath^2=\mathbf{1}$; order two.

**Every transport recomputed slot by slot** under Definition 3.17:

| Slot | Value at $\jmath_*C$ |
|---|---|
| $\mu$ | $\delta_{(0,0)}$ (Dirac pushed along the swap, fixed point) |
| $M$ | $M_C\circ\jmath_{\mathfrak{M}}$ |
| $T$ | $T_{\jmath_*C}(\jmath_{\mathfrak{B}}b)=\jmath_{\mathfrak{M}}\circ T_C(b)\circ\jmath_{\mathfrak{M}}$ |
| $\approx$ | $\bot_{\mathrm{abs}}$ |
| $\delta$ | unchanged, $\lvert u-v\rvert$; $D=\mathcal{Y}^2$ |
| $\rho$ | unchanged, $\rho^{\mathrm{at}}$ |
| carriers | $(\mathcal{Y},\mathcal{G}_{\mathcal{Y}})$ and $\mathbb{W}$ |

Evaluated at a generic point $(7,3)$, the reconstruction returns $T_{C_2}(b_1)=(9,4)$, $T_{C_2}(b_2)=(8,5)$, $T_{C_0'}(b_i)=(8,3)$, $M_{C_2}=3$, $M_{C_0'}=3$ — matching the closed forms $(x+2,y+1)$, $(x+1,y+2)$, $(x+1,y)$, $y$, $y$ stated in the text.

**Closure.** $\mathbf{1}_*C=C$; $\jmath_*C_1=C_2$, $\jmath_*C_0=C_0'$ by construction; $\jmath_*C_2=C_1$ and $\jmath_*C_0'=C_0$ by involutivity via Observation 3.17.1. $\mathcal{C}$ is closed.

**Significance.** $\sigma_{C_1}(b_1)=2$, $\sigma_{C_1}(b_2)=1$, $\sigma_{C_2}(b_1)=1$, $\sigma_{C_2}(b_2)=2$, $\sigma_{C_0}(b_i)=0$, $\sigma_{C_0'}(b_i)=0$ — reproduced independently.

**All eight non-identity A3 equations** recomputed and all eight hold; $\jmath\neq\mathbf{1}$, so the check is non-vacuous.

**Axiom checks.**

| Axiom | Result |
|---|---|
| FR-1 | Seven components supplied in every context; $\approx=\bot_{\mathrm{abs}}$ supplied |
| A3 | Eight equations hold; identity case from Observation 3.16.1(d) |
| A4 | Both conjuncts: class datum $\mathsf{W}_1(+,0)$ from the frame slot; $C_0$ gives $0_W$ for both bearers |
| A5 | Every value in $W\subseteq\widehat W$, via Definition 5.3 row four |
| A8 | Antecedent false; holds |
| A9 | Antecedent false; holds |
| A10 | Antecedent never met; **holds vacuously** — stated as such |
| A7 | Not applicable; withdrawn from Version 1 |

**Exact-signature instantiation.** Observation 11.1.3 maps every datum to the declared slot it arrives through. The class datum reaches A4 and (W-c) **through the tuple**, not through prose — the defect TR-6 named. The signature list in the claim was checked against the declaration inventory and names **exactly the 30 Definitions declared in Part A**.

**Result: pass.**

---

## 14. Part A / Part B boundary audit

| Check | Result |
|---|---|
| Part B byte region | SHA-256 `05f1720f10f0a1c2670db644373a832ad26f5fb74e184e1dc1e463fc4d5a6c3c` before **and** after — identical, and identical to the value recorded in the final verification report §12 |
| Part A proofs citing Part B | None |
| Part A references to Part B | Boundary and deferral statements only (OB-A5, OB-A6, the freeze-boundary paragraph) |
| Part B status labelling | Unchanged: Candidate, non-frozen, outside the consistency claim and any Version 1 verification claim |
| Frozen research controls | `validation/` and `review-packages/` untouched; `git status` shows one modified file |

**Result: pass.**

---

## 15. Notation audit

| Item | Result |
|---|---|
| Undeclared $W'$ | Removed; survives only in the removal note and the quoted withdrawn definition |
| $\mathrm{id}_{W_C}$ in Definition 6.1 | Corrected to $\mathrm{id}_W$ |
| $\widehat{W_{\iota_*C}}$ in A3 | Corrected to $\widehat W$, with membership justified on both sides |
| "codomain" where the property is carrier-only | Corrected in Definitions 3.5.1, 3.12.1, Observations 3.12.2, 10.0, 10.0.1, 10.1.1, 11.1.2, limitation 14.11′ |
| $\mathrm{id}_*C$ vs $\mathbf{1}_*C$ | Aligned to $\mathbf{1}$, matching Observation 3.15.1 |
| Superseded four-component tuple | Removed from the axiom section; retained once, explicitly as withdrawn |
| Declaration numbering | Definitions ascend 3.1 → 7.7 with no inversion; the 3.18.x sequence is now 3.18.1, 3.18.2, 3.18.3, 3.18.4; the 10.x and 11.1.x sequences ascend |

**Result: pass.**

---

## 16. Cross-reference audit

Mechanical: every `Definition`/`Theorem`/`Observation`/`Corollary`/`Proposition` reference in Part A was resolved against the declaration inventory.

| Check | Result |
|---|---|
| Unresolved references | **None** |
| References to withdrawn objects | Only inside the withdrawal notices, marked as prior-edition text |
| Proposition 11.1′ signature list | Names exactly the 30 declared Part A Definitions |
| Duplicate declaration headings | None. Two apparent hits (`Corollary 6.2`, `Theorem 3.2′`) are bold in-text references in prose, not declarations |

**Result: pass.**

---

## 17. Markdown and LaTeX audit

| Check | Value | Result |
|---|---|---|
| Lines / words / bytes | 692 / 10,415 / 85,798 | — |
| Display-math `$$` delimiters | 40 | Balanced (even) |
| Inline `$` parity, per line | Every line even after removing `$$` | Pass |
| Braces `{` / `}` | 1,253 / 1,253 | Balanced |
| Code fences | 0 | Pass |
| Unfinished markers (`TODO`, `TBD`, `FIXME`, `XXX`, `???`, unchecked box) | 0 | Pass |
| Heading hierarchy | Part A and Part B hierarchy balanced; no skipped structural level | Pass |
| Tables | All new tables have matching header, separator and body column counts | Pass |
| Status declarations | Consistently Candidate, not frozen, awaiting verification | Pass |

**Result: pass.**

---

## 18. Findings closed

| № | Blocking finding | Status |
|---|---|---|
| TR-1 | Definition 3.16 unbound target | **Closed** |
| TR-2 | Frame structurally incomplete | **Closed** |
| TR-3 | Transport not instance data; heterogeneous form | **Closed by withdrawal** |
| TR-4 | Tuple, Theorem 3.2′ gating, identified-output type | **Closed** |
| TR-5 | Corollary exceeds its proof | **Closed by narrowing** |
| TR-6 | Witness does not instantiate the exact signature | **Closed** |
| NB-1 | Definition 5.3 mislabelled partial | **Closed** |
| NB-2 | Implicit free variables | **Closed** |
| NB-3 | Non-monotone 3.18.x numbering | **Closed** |
| NB-4 | Stale wording, malformed notation, cross-references | **Closed** |

## 19. Matters disclosed, not defects

1. **A5 is derivable from Definition 5.3** and is not independent. Pre-existing; unchanged.
2. **A10 holds by construction** in every supplied instance, since Definition 7.5 case 1 assigns $\bot_{\mathrm{inc}}$ on an empty fibre. Typing the output made this visible; it did not create it. A10 is retained as an axiom, as before.
3. **Version 1 has no cross-context comparison apparatus**, by the deliberate choice recorded in Terminal Adjudication §4.1. Stated in limitation 14.7′ and deferred as OB-A6.
4. **Axiom labels A1, A2, A6, A7 are unused.** Not renumbered, to keep the prior verification record resolvable.
5. **Content withdrawn in this pass:** Definition 8.9, axiom A7, rejected formulation 16.12, and the axiom-level reading of Corollary 10.1″ / Observation 10.0.1 / limitation 14.11′. Each was withdrawn because the final verification found it invalid or unsupported, not for convenience, and none was preserved for continuity.

## 20. Determination

**ASTRO-THEORY-0001 TERMINAL REMEDIATION COMPLETE — READY FOR FREEZE VERIFICATION**

All six blocking and four non-blocking findings of the final Version 1 verification are closed. Part A is internally typed, its signature is complete against its axioms, its consistency witness instantiates the exact repaired signature, and no retained statement exceeds its proof. Part B is byte-identical and no frozen research control was touched.

The theory remains **Candidate**. This pass performs no freeze and claims none. Independent freeze verification may proceed against theory blob `6fc866796b0a9c39d3f7384d4118fce8ee7ae5ac`.
