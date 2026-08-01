# ASTRO-THEORY-0001 — Final Deterministic-Core Remediation Change Map

**Old edition:** blob `0d64e4fd1fa8d6668ece38c6ec4f0fab73479210` at commit `26417eb`.
**New edition:** this working tree, same path.
**Basis:** final independent verification, findings FV-001 – FV-006.
**Both editions:** Theory Candidate. Neither is frozen.

"Old §" is the numbering of blob `0d64e4fd`. "New §" is the remediated edition. *(none)* means no counterpart.

---

## 1. Structural change — freeze boundary

| Old § | New § | FV | Semantic effect | Proof effect | Status |
|---|---|---|---|---|---|
| Single undivided document | **Part A — Version 1 Deterministic Core Candidate** and **Part B — Candidate Enrichments** | Freeze-boundary rule | The core is now separable and self-contained; every Part B item is labelled Candidate, non-frozen, not required by the core, outside the consistency claim and outside any Version 1 claim | Every Part A proof cites only Part A objects; checked by inspection | **Added** |
| §4.1 Design principles | §B.1 | — | DP-1, DP-2 relocated to Part B; still non-formal and unusable in proofs | None; no proof cited them before or now | **Relocated** |
| Def 3.5 classes $\mathsf{W}_2$, $\mathsf{W}_2^{\mathrm{m}}$ | §B.2 | — | Signed classes relocated; core Definition 3.5 retains only the base codomain and class $\mathsf{W}_1$ | No Part A theorem uses subtraction | **Relocated** |
| Def 3.13–3.14, 8.1–8.4, Thm 5, Thm 6 | §B.3 | — | Decision and evidence structure and the three forms relocated | Not cited by any Part A proof | **Relocated** |
| Thm 8 | §B.4 | — | Information lemma relocated | Not cited by any Part A proof | **Relocated** |
| Def 10.1–10.3, Thm 11, 12′, 13′ | §B.5 | — | Composition signature relocated | Not cited by any Part A proof | **Relocated** |
| OB-1 – OB-4 | §A.11 (OB-A1–A3) and §B.6 (OB-B1–B4) | FV-001 | Core and enrichment obligations separated; no core obligation blocks | See adjudication §"Effect on the earlier OB register" | **Split** |

## 2. Signature

| Old § | New § | FV | Semantic effect | Proof effect | Status |
|---|---|---|---|---|---|
| *(none)* | **Def 3.18 Theory instance** | FV-001 | $\mathcal{C}$ and $\mathcal{G}$ become declared signature objects; closure under transport is a requirement on instances | A3 and A4 become predicates over declared carriers; Prop 11.1′ must exhibit closure | **Added** |
| *(none)* | **Def 3.5.1 Point-separating codomain** | FV-003 | Isolates the hypothesis that makes Dirac measures identify their atoms | Hypothesis of Thm 10″; declared by Thm 1 and Prop 11.1′ | **Added** |
| *(none)* | **Obs 3.5.2** | FV-003 | Proves point separation $\iff$ injectivity of $x\mapsto\delta_x$ | Licenses Def 3.12.1 | **Added** |
| *(none)* | **Def 3.12.1 Atom reduction** | FV-003 | The reduction used by Thm 1, Thm 10″ and Prop 11.1′ is now a named partial function with a stated domain | Removes the implicit "Dirac-atom reduction" | **Added** |
| *(none)* | **Obs 3.12.2** | FV-003 | Records that the atom reduction is not a function on non-separating codomains | Blocks reuse of the false Thm 10′ construction | **Added** |
| *(none)* | **Obs 3.17.1 Functoriality** | FV-004 | $(\iota\circ\kappa)_*=\iota_*\circ\kappa_*$ and $\mathrm{id}_*=\mathrm{id}$ | Used by the closure proof in Prop 11.1′ | **Added** |
| Def 3.5 (three classes) | Def 3.5 (base + $\mathsf{W}_1$) | — | $\mathsf{W}_2$, $\mathsf{W}_2^{\mathrm{m}}$ moved to Part B; $W$ now required nonempty | Thm 3's nonemptiness hypothesis is now inherited | **Narrowed** |
| Def 3.15 | Def 3.15 | FV-001 | Morphisms are endomorphisms over fixed $\mathfrak{B}$, $\mathfrak{M}$, matching Def 3.18 | Makes $\mathcal{G}$ a group under composition | **Narrowed** |

## 3. Formation rule and axioms

| Old § | New § | FV | Semantic effect | Proof effect | Status |
|---|---|---|---|---|---|
| A2 | **FR-1** + Obs FR-1.1 | verifier's note | Reclassified as a formation rule; not counted as an axiom | Not cited as an axiom in any satisfaction check | **Reclassified** |
| A3 (all morphisms) | A3 (over declared $\mathcal{G}$) | FV-001 | Quantifier **narrowed** to the instance's morphism group | Prop 11.1′ now checks A3 under the quantifier the axiom actually states | **Narrowed** |
| A4 (over undeclared $\mathcal{C}$) | A4 (over declared $\mathcal{C}$) | FV-001 | Becomes a predicate over a declared carrier | Satisfaction checkable | **Repaired** |
| A5, A7, A8, A9, A10 | unchanged | — | — | — | **Retained** |
| Obs 4.2.1 | **Obs A.3.1** | FV-001 | Restated: A3 and A4 are now predicates over declared carriers; FR-1 is a formation rule | — | **Replaced** |

## 4. Contrast and significance

| Old § | New § | FV | Semantic effect | Proof effect | Status |
|---|---|---|---|---|---|
| Def 5.2 (pushforward of a partial map) | **Def 5.2 (subspace construction)** | FV-002 | Profile built as the pushforward of a restricted probability measure along a restricted total map | The expression is now an instance of a declared operation; no extension, so no extension-independence question | **Repaired** |
| *(none)* | **Obs 5.2.1** | FV-002 | Records the defect and the construction | — | **Added** |
| Def 5.3 (five rows) | Def 5.3 (four rows) | FV-002 | $\Omega^b_C=\emptyset$ and $0<\mu(\Omega)<1$ merged into one $\mu(\Omega)<1$ row | Still exhaustive; still agrees with A9 | **Simplified** |
| Thm 1 | Thm 1 | FV-003 | Declares point separation and the named atom reduction; quantifier and totality stated | Proof unchanged; reduction now licensed by Def 3.12.1 | **Repaired** |
| Obs 1.1′ | Obs 1.1′ | — | Strengthened non-conclusion wording | — | **Retained** |

## 5. Theorems

| Old § | New § | FV | Semantic effect | Proof effect | Status |
|---|---|---|---|---|---|
| Cor 6.2 | Cor 6.2 | FV-001 | $\mathrm{Aut}(C)$ now a subgroup of the declared $\mathcal{G}$ | Proof unchanged | **Repaired** |
| Thm 3 | Thm 3 | — | Unchanged | Verified by the verifier; proof unchanged | **Retained** |
| Cor 3.3 | Cor 3.3 | — | Nonemptiness of $\mathcal{Y}_C$ noted | Proof unchanged | **Retained** |
| Thm 3.2′ | Thm 3.2′ | — | Unchanged | Verified; proof unchanged | **Retained** |
| Thm 4′ | Thm 4′ | — | Quantifier line added | Verified; proof unchanged | **Retained** |
| Thm 7′ | Thm 7′ | FV-001 | Family $\mathcal{K}$ now a subset of a declared $\mathcal{C}$ | Verified once $\mathcal{C}$ supplied; proof unchanged | **Repaired** |
| Thm 9 | Thm 9 | — | Unchanged | Verified; proof unchanged | **Retained** |
| **Thm 10′** | **Thm 10″** | FV-003 | **False** for arbitrary codomains; point separation added as hypothesis | Proof otherwise unchanged; still needs no algebraic structure | **Withdrawn and replaced** |
| **Cor 10.1′** | **Cor 10.1″** | FV-003 | Restricted to point-separating codomains | Follows from Thm 10″ | **Withdrawn and replaced** |
| Obs 10.0 | Obs 10.0 | FV-003 | Now records the two-point trivial-$\sigma$-algebra counterexample | — | **Replaced** |
| Obs 10.0.1 | Obs 10.0.1 | FV-003 | Universal assertion removed; explicit silence on non-separating codomains | — | **Narrowed** |
| Obs 10.1.1 | Obs 10.1.1 | FV-003 | Adds that constraints come from A3 over $\mathcal{G}$, A4 over $\mathcal{C}$, A7 | — | **Retained, sharpened** |
| **Prop 11.1** | **Prop 11.1′** | FV-004, FV-005 | Context set extended to $\{C_1,C_2,C_0,C_0'\}$; closure **proved**; fragment names Defs 5.1–5.3 | A3 checked over eight non-identity instances; non-vacuous | **Withdrawn and replaced** |
| Obs 11.1.1 | Obs 11.1.1 | FV-004, FV-005 | Records the false equality $\jmath_*C_0=C_0$ and the repair | — | **Replaced** |
| Obs 11.1.2 | Obs 11.1.2 | FV-004 | Exclusion list extended with non-point-separating codomains | — | **Retained, extended** |

## 6. Limitations, rejections, and non-conclusions

| Old § | New § | FV | Semantic effect | Status |
|---|---|---|---|---|
| *(none)* | **§A.10.2** | FV-006 | New subsection enumerating what the core does **not** establish, so withdrawals are visible rather than merely absent | **Added** |
| *(none)* | **§A.10.2.1** | FV-006 | States plainly that the core **does not exclude intrinsic significance**, with the $\sigma\equiv0$ counterexample | **Added** |
| Lim 14.11 | **Lim 14.11′** | FV-003, FV-006 | Restricted to point-separating codomains, single context, deterministic form | **Narrowed** |
| Lim 14.12 | **Lim 14.12′** | FV-004 | Restricted to the exact instance of Prop 11.1′ | **Narrowed** |
| Lim 14.4, 14.7 | unchanged | — | Verified by the verifier | **Retained** |
| **Rej 16.1** | *(none)* | FV-006 | Rejection of intrinsic significance **withdrawn**; a two-argument function may be constant in its first argument | **Withdrawn** |
| **Rej 16.13** | *(none)* | FV-006 | Artefact independence **withdrawn as stated**; "artefact relabelling" and "declared universe" undefined; only Cor 6.2 survives | **Withdrawn** |
| Rej 16.17 | Rej 16.17 | FV-006 | Annotated so it is not read as excluding a context-independent significance function | **Narrowed** |
| Rej 16.3, 16.6, 16.8, 16.10, 16.15 | *(none in Part A)* | — | Depend on Part B objects (information lemma, composition signature) or on non-core notions; not retained in the core | **Removed from core** |
| Rej 16.12, 16.16, 16.18, 16.19 | unchanged | — | Verified by the verifier as statements about the signature | **Retained** |

## 7. Verified-results table

| Old | New | FV |
|---|---|---|
| Ten entries including Thm 10′ "deterministic form" | Ten entries with **Thm 10″** and **Prop 11.1′**, each carrying an explicit quantifier column | FV-003, FV-004 |
| Enrichment theorems listed alongside core | Enrichment theorems removed from the core table entirely | Freeze-boundary rule |
