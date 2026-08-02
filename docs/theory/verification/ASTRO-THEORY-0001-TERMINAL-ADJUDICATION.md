# ASTRO-THEORY-0001
## Terminal Adjudication — Version 1 Deterministic Core

## 1. Adjudication control

| Field | Verified value |
|---|---|
| Repository | `17th2nd/ASA-Astro` |
| Authoritative ref | `origin/main` after a fresh fetch |
| Branch | `main` |
| `HEAD == origin/main` before mutation | Yes |
| Ahead / behind before mutation | `0 / 0` |
| Worktree before mutation | Clean; no staged, modified or untracked files |
| Baseline commit | `691a4d866ef164ba8e177ea59cf1bb3d1565c9b7` |
| Theory blob before | `c20ca91fa18551f247dfa1c150dea3f9d9b510d5` |
| Theory blob after | `6fc866796b0a9c39d3f7384d4118fce8ee7ae5ac` |
| Adjudication date | 2026-08-02 (Australia/Brisbane) |
| Part B edited | **No** — byte-identical, verified by region hash |
| Frozen research controls edited | **No** |
| Theory frozen | **No** — remains Candidate |

The expected baseline commit was confirmed exactly. The sole authoritative defect basis, `docs/theory/verification/ASTRO-THEORY-0001-FINAL-VERSION-1-VERIFICATION.md`, was read in full before any mutation.

**Basis integrity.** The final verification report records that it examined commit `ba3ccc097a024b5354b58199094719e7b1f3e271`, whereas current `main` is `691a4d8`. The difference was checked and is confined to the addition of the verification report itself (`1 file changed, 393 insertions(+)`). The theory blob at `ba3ccc09` and at `691a4d8` is the same object, `c20ca91f`. **The theory and verification basis are unchanged; closure proceeds.**

## 2. Authority and scope

This pass is **terminal formal closure of the existing homogeneous theory**. It does not redesign the theory, does not expand Part A, does not alter Part B, adds no novelty claim, and modifies no frozen research control. Earlier AV, FV and DCV findings were used only where the final report expressly incorporates them.

Where the final report's finding was that a statement is **invalid**, the statement has been corrected or withdrawn. **No invalid statement has been preserved for continuity.**

## 3. Blocking findings and adjudication

The six blocking findings of §15 of the final verification are labelled **TR-1 – TR-6** in the repaired theory.

| № | Blocking finding (final verification §15) | Repair | Adjudication |
|---|---|---|---|
| TR-1 | Definition 3.16 has undeclared target $W'$; extended action, reduction transport and A3 not fully typed | Repair 1 | **Closed** |
| TR-2 | Homogeneous frame structurally incomplete: selected class-$\mathsf{W}_1$ operation and zero used by A4 and by morphism preservation are not frame or instance components | Repair 2 | **Closed** |
| TR-3 | Primitive completeness fails: optional cross-context transport and its typed absence are not instance data; Definition 8.9 retains an unconstrained heterogeneous source/target | Repair 3 | **Closed by withdrawal** |
| TR-4 | DCV-002 incompletely propagated: superseded four-component tuple reinstated; Theorem 3.2′ not gated to the supplied branch; identified output has no declared type | Repairs 4, 5 | **Closed** |
| TR-5 | Corollary 10.1″, Observation 10.0.1 and limitation 14.11′ claim axiom-level encodability that homogeneity plus A4 defeats | Repair 6 | **Closed by narrowing** |
| TR-6 | Proposition 11.1′ does not instantiate the exact written general signature | Consistency proposition | **Closed** |

Non-blocking findings of §16 are labelled **NB-1 – NB-4** and are adjudicated in §5.

## 4. Elective decisions taken

Three repairs offered a choice. Each choice is recorded with its ground, because each changes what Version 1 asserts.

### 4.1 Repair 3 — Option A (removal), not Option B (typed transport component)

**Decision: remove Definition 8.9, and withdraw axiom A7 with it.**

The instruction directs "Prefer removal if it is unused" and requires that after repair "A7 must be a testable predicate over the declared theory instance or be withdrawn from Version 1."

Grounds, each verified against the text:

1. **Unused.** No retained Part A theorem, corollary, proposition or proof cites Definition 8.9 or A7. The full retained set — Theorems 1, 3, 3.2′, 4′, 7′, 9, 10″, Corollaries 3.3, 6.2, 10.1″, Proposition 11.1′ — was checked individually.
2. **Not a predicate.** No transport datum, supplied or absent, was ever a component of the theory instance, so A7's second clause could be neither satisfied nor violated by any instance.
3. **A7's first clause is not lost.** Under homogeneity, "values under $C$ lie in $\widehat{W_C}$" is literally A5, which is retained.
4. **Its type was heterogeneous.** $t:W_C\to W_{C'}$ presupposes two context-indexed codomains, the very structure Observation 3.14.2 removed from Version 1.

Option B was rejected because it would add a datum no retained statement consumes, and a genuinely cross-context transport would require the heterogeneous carriers Version 1 excludes. **No heterogeneous transport system was introduced.** The deferral is recorded as **OB-A6**.

**Consequential withdrawal.** Rejected formulation **16.12** cited "A7 with Definition 8.9" as its entire warrant. With both withdrawn, 16.12 has no basis and is withdrawn rather than retained for continuity. Limitation **14.7** is replaced by **14.7′**, which states what Version 1 actually supplies.

### 4.2 Repair 5 — set-valued identified output on a separate declared carrier

**Decision: declare $\widehat{W}^{\mathrm{id}}:=\mathcal{P}_{\neq\emptyset}(W)\sqcup\{\bot_{\mathrm{inc}},\bot_{\mathrm{und}}\}$ (Definition 3.8.1) and the total function $\mathrm{Id}^b_C:\mathcal{R}\to\widehat{W}^{\mathrm{id}}$ (Definition 7.5).**

| Required declaration | Value |
|---|---|
| Domain | $\mathcal{R}$, the representation carrier of $\mathsf{r}$ |
| Codomain | $\widehat{W}^{\mathrm{id}}$ (Definition 3.8.1) |
| Total / partial | **Total on $\mathcal{R}$**; the family is formed exactly when $\mathsf{r}$ is supplied and $T_C(b)$ is defined |
| Supplied-$\mathsf{r}$ applicability | Formed in the supplied branch only; not formed in the absent branch |
| Output carrier contents | $\bot_{\mathrm{inc}}$, $\bot_{\mathrm{und}}$, and the admissible set-valued output $\mathcal{S}_C(b,x)$ |

The alternative — collapsing the output into $\widehat W$ — was rejected because Theorem 3.2′ must be able to state $|\mathcal{S}_C(b,x)|\ge2$, which a single-valued output cannot express. **$\widehat W$ was not extended**: Observation 3.8.2 records that the two carriers are distinct and that no arbitrary subset of $W$ is placed in $\widehat W$.

### 4.3 Repair 6 — Option B (restrict to the construction), not A or C

**Decision: restrict Corollary 10.1″ to the single-context construction and state explicitly that it does not establish satisfaction of all axioms.**

- **Option A rejected.** Restricting the corollary to point-separating codomains carrying the exact class-$\mathsf{W}_1$ structure required by A4 would still not follow from Theorem 10″, because Theorem 10″ constructs one context and **verifies no axiom at all** — not A3, not A4, not A5, A8, A9 or A10. Option A would have replaced an overbroad claim with a narrower unproved one.
- **Option C rejected.** The construction itself is sound and worth recording.
- **Option B adopted.** The corollary now asserts only what Theorem 10″ proves: realisability by the construction.

The instruction's prohibition is honoured: **the encodability claim that the axioms exclude no assignment, in that or any equivalent form, is asserted nowhere in Version 1.** Verified by search. Two occurrences of the wording survive and neither asserts the claim: in **Observation 10.1.0** it appears inside the sentence that forbids it, and in **§A.10.2.1** the wording "excluded by no Part A axiom" carries the separate FV-006 statement about the single assignment $\sigma\equiv0_W$ — now itself qualified to require a class-$\mathsf{W}_1$ instance. Full detail in the Terminal Remediation Report §12.

The same correction was applied to **Observation 10.0.1**, **Observation 10.1.1**, **limitation 14.11′** and the **result-register entry for 10″**. A new **Observation 10.0.2** records that Theorem 10″ is a context-existence theorem, and **Observation 10.1.0** records why the prior conclusion was withdrawn — including that on a carrier admitting no $\mathsf{W}_1$ structure the full axioms **do** exclude assignments.

## 5. Non-blocking findings

| № | Finding (final verification §16) | Action | Status |
|---|---|---|---|
| NB-1 | Definition 5.3 labelled "partial" although its four exhaustive cases make $\sigma_C$ total | Heading changed to **total**; a totality paragraph proves exhaustiveness and disjointness; $\sigma_C:\mathfrak{B}\to\widehat W$ declared total in the derived-object table | **Closed** |
| NB-2 | A5, A7, A8, A9 use implicit free variables | Explicit universal quantifiers added to A5, A8, A9; A10 quantified over $C$, $b$, $x$; A7 withdrawn, so no quantifier is owed | **Closed** |
| NB-3 | 3.18.x declaration order non-monotone | Reordered to Observation 3.18.1, Observation 3.18.2, Definition 3.18.3, Definition 3.18.4 | **Closed** |
| NB-4 | Stale superseded wording, malformed notation, cross-references | Superseded four-component tuple removed; $W'$ removed; header and change-summary rewritten; $\mathrm{id}_{W_C}$ → $\mathrm{id}_W$ in Definition 6.1; "codomain" → "carrier" where the property is carrier-only | **Closed** |

OB-A1 – OB-A5 remain genuine research or placement questions, are used by no proof, and are untouched. **OB-A6** is added to record the deferral created by §4.1.

## 6. Boundary and control confirmations

| Control | Result |
|---|---|
| Part B byte region unchanged | **Confirmed.** SHA-256 `05f1720f10f0a1c2670db644373a832ad26f5fb74e184e1dc1e463fc4d5a6c3c` before and after, identical to the value recorded in the final verification report §12 |
| No Part A proof cites Part B | Confirmed by inspection of every retained proof |
| Frozen research controls | Untouched; `validation/` and `review-packages/` not modified |
| Existing verification reports | **Not modified.** The four terminal files are new |
| Theory status | Remains **Candidate**; no freeze performed or claimed |
| Novelty | No novelty claim added; the existing disclaimer is retained verbatim |

## 7. Residual matters disclosed

These are **not** blocking findings; they are properties of the theory that the repairs make visible and that a freeze verification should see stated plainly.

1. **A5 is derivable, not independent.** Definition 5.3 already returns an element of $\widehat W$ in every case, so A5 restates a consequence of the definition. This was true before this pass and is unchanged by it.
2. **A10 is satisfied by construction in every supplied instance.** Definition 7.5 case 1 assigns $\bot_{\mathrm{inc}}$ on an empty fibre, which is exactly what A10 asserts. Typing the identified output made this visible; it did not create it. A10 remains stated as an axiom, as in the prior edition.
3. **Version 1 has no cross-context comparison apparatus.** This is a deliberate consequence of §4.1 and is recorded in limitation 14.7′ and OB-A6.
4. **Axiom labels A1, A2, A6, A7 are unused.** Labels were not renumbered, to preserve cross-referencing with the prior verification record.
5. **The class datum is a required, typed component.** An instance of class $\mathsf{W}_0$ is a well-formed theory instance but does not satisfy A4 (Observation A.3.0). A4 was not weakened into a typed-inapplicability branch, because that would have been a redesign of the axiom system rather than a closure of a defect.

## 8. Determination

All six blocking findings and all four non-blocking findings of the final Version 1 verification are closed within the authorised scope. No repair required redesigning the theory, expanding Part A, altering Part B, or adding a novelty claim.

**ASTRO-THEORY-0001 TERMINAL REMEDIATION COMPLETE — READY FOR FREEZE VERIFICATION**

The theory remains **Candidate**. This adjudication performs no freeze and makes no freeze claim; it records that the defects which blocked freeze have been closed and that an independent freeze verification may now proceed against theory blob `6fc866796b0a9c39d3f7384d4118fce8ee7ae5ac`.
