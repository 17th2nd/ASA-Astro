# ASTRO-THEORY-0001 — Remediation Change Map

**Old edition:** blob `08a2257aaea6e5f23b316682025022b62d834d68` at commit `a9df42f9`.
**New edition:** this working tree, same path.
**Basis:** independent verification report, findings AV-001 – AV-028.
**Status of both editions:** Theory Candidate. Neither is verified.

"Old §" refers to the numbering of blob `08a2257`. "New §" refers to the remediated edition. *(none)* means no counterpart.

---

## 1. Signature

| Old § | New § | AV | Semantic effect | Proof effect | Status |
|---|---|---|---|---|---|
| Def 3.14 component `𝔄_C` | *(none)* | AV-001, AV-024 | Undefined admissibility object removed; `μ_C` is itself the component; context is a seven-tuple | Prop 11.1's "all components supplied" becomes true | **Withdrawn** |
| Def 3.16 four profile classes | Def 3.11 single class | AV-004 | Set, multiset and measure-valued classes deleted; only the pushforward construction remains | Removes the undefined profile-induction gap from every §8 proof | **Withdrawn (3 of 4)** |
| *(none)* | Def 3.7 `I(W)` | AV-001 | Order-intervals defined | Makes `Ŵ` well defined | **Added** |
| *(none)* | Def 3.8 `Ŵ` | AV-001, AV-002 | Output codomain as a disjoint union | Gives A3 and A5 a determinate codomain | **Added** |
| *(none)* | Def 3.9 `⊥_abs` | AV-003 | Typed absent value for optional components | Makes A2 unambiguous; every context supplies all seven components | **Added** |
| Def 3.12 classes `W₀`–`W₄` | Def 3.5 classes `W₁`, `W₂`, `W₂^m` | AV-005, AV-017 | Unused classes removed; measurable subtraction separated as `W₂^m` | No theorem may use subtraction without declaring `W₂^m` | **Narrowed** |
| *(none)* | Obs 3.6 | AV-017 | Countable–cocountable counterexample recorded | Blocks reuse of the invalid Theorem 10 proof | **Added** |
| *(none)* | Def 3.12 location functional | AV-013 | "Location functional" given support bounds and Dirac value | Theorem 5(i) and Theorem 6 now have determinate reductions | **Added** |
| Def 3.20 evidence kernel | Def 3.14 regular evidence structure | AV-012 | Regularity, barycentre identity, risk measurability and integrability made hypotheses | Theorem 5(iii) becomes provable exactly where declared | **Narrowed** |
| Def 3.21–3.22 transport | Def 3.15–3.17 | AV-002 | All seven components transported; `ι̂_W` acts on intervals and fixes bottoms | A3 becomes a formula for every possible output | **Repaired** |

## 2. Axioms

| Old § | New § | AV | Semantic effect | Proof effect | Status |
|---|---|---|---|---|---|
| A1 | DP-1 (§4.1) | AV-005 | Demoted to a non-formal design principle | Cited by no proof; verified by inspection | **Withdrawn from formal system** |
| A6 | DP-2 (§4.1) | AV-005 | Demoted to a non-formal design principle | Cited by no proof | **Withdrawn from formal system** |
| A2 | A2 | AV-003 | Restricted to *required* components; `⊥_abs` counts as supplied | Removes the optional/required contradiction | **Narrowed** |
| A3 | A3 | AV-002 | Stated with `ι̂_W` over `Ŵ` | Well typed for interval and bottom outputs | **Repaired** |
| A4 | A4 | AV-007 | Unchanged as an existential schema | Satisfied non-vacuously by `C₀` in Prop 11.1 | **Retained** |
| A5 | A5 | AV-005 | Replaced by an output-typing predicate referring to Def 5.3 | Satisfaction now checkable | **Repaired** |
| A7 | A7 | AV-016, AV-027 | Unchanged; the transport exception made explicit | Limitation 14.7 and Rejection 16.12 narrowed accordingly | **Retained** |
| A8 | A8 | AV-011 | Unchanged | Now used only by Theorem 4′ on `D̄_C` | **Retained** |
| A9 | A9 | AV-005 | Replaced by a predicate on `Ω^b_C = ∅` | Satisfaction checkable | **Repaired** |
| A10 | A10 | AV-005 | Replaced by a predicate on `r^{-1}(x) = ∅` | Satisfaction checkable | **Repaired** |

## 3. Theorems and corollaries

| Old § | New § | AV | Semantic effect | Proof effect | Status |
|---|---|---|---|---|---|
| Thm 1 | Thm 1 | AV-007 | Contexts completed; conclusion labelled existential | Proof unchanged; now instantiates a complete tuple | **Retained, narrowed** |
| Cor 1.1 | *(none)* | AV-007 | Universal "no context-free ordering" removed | — | **Withdrawn** |
| Cor 1.2 | inside Prop 11.1 | AV-007 | Absorbed into the A4 satisfaction check | — | **Absorbed** |
| Thm 2 | Cor 6.2 | AV-006, AV-023 | "Designation necessity" removed; only orbit constancy under a fixed context survives | One line from A3 | **Demoted** |
| Def 6.2–6.3, Cor 2.1–2.2 | *(none)* | AV-006 | Designation and filter contexts removed; underlying structure was undefined | — | **Withdrawn** |
| Thm 3 | Thm 3 | AV-008 | Final σ-algebra declared; `h` total; codomain any measurable space | Measurability step now justified; `𝖵 ≠ ∅` added | **Repaired** |
| Cor 3.1 | *(none)* | AV-009 | Computability claim removed as **false** | — | **Withdrawn** |
| Cor 3.2 | Thm 3.2′ | AV-010 | **False** universal replaced by a totality-hypothesised statement | New proof under totality | **Withdrawn and replaced** |
| Cor 3.3 | Cor 3.3 | AV-008 | Now a literal instance of the widened Theorem 3 | Proof unchanged | **Repaired** |
| Thm 4 | Thm 4′ | AV-011 | **False/incomplete** replaced by partial descent on `D̄_C` with the pullback relation stated | New proof | **Withdrawn and replaced** |
| Thm 5(i) | Thm 5(i) | AV-013 | "Location functional" now defined | Proof cites Def 3.12 | **Repaired** |
| Thm 5(ii) | Thm 5(ii) | — | Unchanged | Verified by the verifier; proof unchanged | **Retained** |
| Thm 5(iii) | Thm 5(iii) | AV-012 | Restricted to a regular evidence structure | Jensen step now licensed | **Narrowed** |
| Thm 6 | Thm 6 | AV-013 | `ρ = ` mean, `ε = 0` with attainment, complete contexts, part (iii) computed exactly | Displayed values now proved | **Repaired** |
| Cor 6.1 | *(none)* | AV-013 | Latent-quantity claim removed | — | **Withdrawn** |
| Thm 7 | Thm 7′ | AV-014 | **False** replaced by a nullity-closed-family hypothesis | Proof valid under (a) | **Withdrawn and replaced** |
| Thm 8 | Thm 8 | AV-015 | Renamed *Conditional information redundancy* | Proof unchanged | **Retained** |
| Cor 8.1 | Obs 8.1′ | AV-015 | **False** epistemic claim replaced by the conditional statement | — | **Withdrawn** |
| Thm 9 | Thm 9 | AV-016 | `A` nonempty stated | Proof unchanged | **Retained** |
| Cor 9.1–9.2 | Obs 9.1′ | AV-016 | Incomparability and uncalibratability claims removed | — | **Withdrawn** |
| Thm 10 | Thm 10′ | AV-017, AV-018 | Proof replaced by a projection evaluator; algebraic hypothesis dropped; scope cut to the deterministic form | New proof, hypothesis-free on measurability | **Withdrawn proof, replaced** |
| Cor 10.1 | Cor 10.1′ | AV-018 | **"No empirical content whatever" withdrawn**; bounded single-context underdetermination substituted | Follows from Thm 10′ | **Withdrawn and replaced** |
| Cor 10.2 | *(none)* | AV-018 | Exhaustiveness claim removed | — | **Withdrawn** |
| Def 10.1–10.6 | Def 10.1–10.3 | AV-019 | `U`, `E`, `src`, `tgt`, primitive `⊙`, `w` supplied; empty paths excluded | §10 theorems acquire a signature | **Repaired** |
| Thm 11 | Thm 11 | AV-027 | Hypothesis made explicit | Proof unchanged | **Retained, narrowed** |
| Thm 12 | Thm 12′ | AV-020 | Type table replaced by an explicit instance-level construction | New proof | **Withdrawn and replaced** |
| Cor 12.2–12.3 | Obs 12.1′ | AV-020 | Universal claims removed; "substructure" was undefined | — | **Withdrawn** |
| Thm 13 | Thm 13′ | AV-021 | Graph, endpoints and `⊙` output supplied; path finiteness established by inspection | New complete proof | **Repaired** |
| Obs 10.7–10.9 | Obs 10.4′ | AV-022 | **Recognisability subsection withdrawn in full**, including the state count, decidability and prior-art subsumption claims | — | **Withdrawn** |
| Def 11.1–11.2, Thm 14, Cor 14.1 | *(none)* | AV-023 | Structural valuation, artefact morphism, orbit-constancy theorem and the "depends on data outside" clause removed | Survives only as Cor 6.2 | **Withdrawn** |
| Cor 14.2 | Cor 6.2 | AV-023 | Merged into the fixed-context corollary | — | **Merged** |
| Prop 12.1 | Prop 11.1 | AV-024 | All components supplied; nontrivial involution checked; context set proved closed under transport | A3 check is no longer vacuous | **Withdrawn and replaced** |

## 4. Limitations, rejections, questions

| Old § | New § | AV | Semantic effect | Status |
|---|---|---|---|---|
| Lim 14.1, 14.2, 14.3, 14.5, 14.6, 14.9, 14.10 | *(none)* | AV-007, AV-014, AV-015, AV-020, AV-010, AV-018, AV-022 | Each depended on a withdrawn or false result | **Withdrawn** |
| Lim 14.4 | Lim 14.4 | AV-027 | False second clause removed — distinct positive rescalings induce the same ordering | **Narrowed** |
| Lim 14.7 | Lim 14.7 | AV-016, AV-027 | Narrowed to the A7 stipulation absent a declared transport | **Narrowed** |
| *(none)* | Lim 14.11, 14.12 | AV-018, AV-025 | Bounded underdetermination; fragment-only consistency | **Added** |
| Rej 16.2, 16.4, 16.5, 16.7, 16.9, 16.11, 16.14 | *(none)* | AV-014, AV-016, AV-013, AV-006, AV-020, AV-010, AV-018 | Each depended on a withdrawn or false result | **Withdrawn** |
| Rej 16.1 | Rej 16.1 | AV-007 | Re-grounded on the stipulation in Def 5.3, not on Theorem 1 | **Narrowed** |
| Rej 16.3 | Rej 16.3 | AV-015 | Conditioned on simultaneous access to `R` | **Narrowed** |
| Rej 16.8 | Rej 16.8 | AV-027 | Conditioned on Theorem 11's hypothesis; type-determined case conceded | **Narrowed** |
| Rej 16.12 | Rej 16.12 | AV-027 | Conditioned on the absence of a declared transport | **Narrowed** |
| Rej 16.13 | Rej 16.13 | AV-023 | Restricted to the declared morphism universe | **Narrowed** |
| Rej 16.17 | Rej 16.17 | AV-014 | Reduced to an inspection claim; theorem-based prohibitions removed | **Narrowed** |
| Rej 16.18 | Rej 16.18 | AV-022 | Adds that no universal prior-art subsumption is claimed | **Narrowed** |
| Rej 16.6, 16.10, 16.15, 16.16, 16.19 | same | — | Unchanged in substance | **Retained** |
| OQ 15.6 negative closure | OQ 15.6 reopened | AV-022 | Prior closure retracted; universal subsumption was never proved | **Reopened** |
| OQ 15.2 | OQ 15.2 | AV-009 | Reworded to ask for a structural, not computational, criterion | **Narrowed** |
| OB-1 | OB-1 | AV-024, AV-025 | Retained and marked **Blocking** | **Retained** |
| OB-2, OB-3 | OB-2, OB-3 | AV-028, AV-012 | Carried forward; OB-3 reworded to the regular-structure repair | **Retained** |
| *(none)* | OB-4 | AV-005 | Formalise DP-1/DP-2 or show neither is needed | **Added** |

## 5. Reference and inventory corrections

| Old | New | AV |
|---|---|---|
| References to nonexistent §18 | All resolve to §16 | AV-026 |
| Composition referenced as §11 | Referenced as §10 | AV-026 |
| Proven table listing Thms 3, 4, 6, 7, 10, 12 as proved; Thm 10 "all forms" | §12 rebuilt post-remediation; Thm 10′ deterministic-form-only | AV-026, AV-018 |
| `E`, `I(W_C)`, `U`, `Q`, `S` undefined | `E`, `U`, `I(W)` defined; `Q`, `S` removed with the withdrawn subsection | AV-026, AV-019, AV-022 |
| *(none)* | §13 withdrawn-results register, 23 entries | AV-027 |
