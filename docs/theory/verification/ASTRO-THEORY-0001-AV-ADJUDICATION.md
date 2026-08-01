# ASTRO-THEORY-0001 — AV Adjudication Record

**Subject:** `docs/theory/ASTRO-THEORY-0001.md`
**Defect basis:** `docs/theory/verification/ASTRO-THEORY-0001-INDEPENDENT-VERIFICATION-REPORT.md` (blob `dca670e2…`), disposition **ASTRO-THEORY-0001 NOT FORMALLY SOUND**. Read in full. Not modified.
**Pre-remediation source blob:** `08a2257aaea6e5f23b316682025022b62d834d68` — confirmed at `HEAD` before mutation.
**Baseline:** `HEAD = origin/main = a9df42f901c7a67a7198910d7c7f58c002dd59bb`, branch `main`, 0/0.
**Status of subject after remediation:** Theory Candidate. Not verified. Not frozen.

**Basis discipline.** The earlier V1–V20 findings were **not** used as a remediation basis. Where an AV finding independently reproduces an earlier concern (notably AV-012 on posterior regularity and AV-017 on measurability), the AV statement alone is cited.

**Severity distribution:** Blocking 15 · Major 11 · Minor 1 · Observation 1 · **total 28**.

**Disposition distribution:** Accepted 11 · Accepted with Modification 16 · Deferred Open Obligation 1 · Rejected with Proof 0 · Withdrawn Statement 0 (as a *disposition*; twenty-three prior statements are withdrawn as *repairs*, listed per finding).

**On the absence of rejections.** No finding is rejected. Each was checked against the source blob and, where the report supplied a counterexample, the counterexample was reconstructed independently. Every one held. Manufacturing a rejection to demonstrate independence would be dishonest.

---

## AV-001 — Incomplete context signature

- **Severity:** Blocking
- **Exact verified defect:** `𝔄_C` has no declared carrier, type, or map determining `μ_C`; the profile class is required to be declared but is not a tuple component; `I(W_C)` is undefined. Two contexts can share all displayed components yet differ in profile class.
- **Disposition:** **Accepted with Modification** — repaired by deletion rather than by definition.
- **Exact affected section:** prior Definitions 3.14, 3.16.
- **Exact repair:** `𝔄_C` **deleted** from the tuple; `μ_C` is now itself the component (new Definition 3.10, seven components, Observation 3.10.1). Three of the four profile classes **deleted**, leaving only the probability-coupled construction, so no class selector is needed (Definition 3.11, Observation 3.11.1). `I(W)` defined as the set of order-intervals (Definition 3.7) and the output codomain `Ŵ` defined as a disjoint union (Definition 3.8).
- **Mathematical justification:** the smallest coherent repair is subtraction. `𝔄_C` did no work that `μ_C` does not do directly; the three undefined profile classes were used by no theorem. Deleting them removes the underdetermination without adding structure.
- **Effect on dependent definitions:** Definitions 3.10, 3.11, 3.17 rewritten; Definitions 5.1–5.3 now have determinate inputs.
- **Effect on dependent theorems:** Theorems 1, 5, 6, 10′ and Proposition 11.1 now instantiate a determinate tuple. No proof content changed.
- **New assumptions introduced:** none.
- **Remaining proof obligation:** none.
- **Remediation verification status:** internally checkable; awaiting re-verification.

## AV-002 — Representation transport and covariance are ill typed

- **Severity:** Blocking
- **Exact verified defect:** Definition 3.22 did not transport `𝔄_C` or the profile-class declaration; `(ι_W^{-1})_*` was undefined for finite-set and multiset profiles; `ι_W` was defined only on `W_C` while `ρ_C` and `σ_C` may return an interval or a bottom, so `ι_W(⊥_ind)` was outside its domain and A3 was not a formula for allowed values.
- **Disposition:** **Accepted**
- **Exact affected section:** prior Definitions 3.21–3.22, A3, Definition 8.10.
- **Exact repair:** `𝔄_C` no longer exists (AV-001), and only one profile class remains, so both untransported items are gone. New **Definition 3.16** defines the extended action `ι̂_W` on all of `Ŵ`: as `ι_W` on `W`, as `[u,v] ↦ [ι_W u, ι_W v]` on intervals, and as the identity on each bottom. **Definition 3.17** transports all seven components explicitly. **A3** restated as an equation in `Ŵ_{ι_*C}` using `ι̂_W`. Definition 8.9 uses the same extended action.
- **Mathematical justification:** `ι_W` is an order isomorphism, so it maps `[u,v]` onto `[ι_W u, ι_W v]` bijectively and the interval action is well defined. Fixing bottoms is forced: they are not elements of `W` and carry no order relation to be preserved.
- **Effect on dependent definitions:** Definitions 3.15–3.17, 8.9.
- **Effect on dependent theorems:** Corollary 6.2 and Proposition 11.1's A3 check are now well typed for every possible output.
- **New assumptions introduced:** none.
- **Remaining proof obligation:** A3 over the class of *all* representation morphisms remains unverified in any model — folded into **OB-1**.
- **Remediation verification status:** internally checkable.

## AV-003 — Optionality conflicts with contextual completeness

- **Severity:** Major
- **Exact verified defect:** an intentionally absent optional `≈_C` was indistinguishable from an unsupplied required component; the tuple reading and the A2 reading could not both govern.
- **Disposition:** **Accepted**
- **Exact affected section:** prior Definition 3.14 line for `≈_C`; prior A2.
- **Exact repair:** **Definition 3.9** introduces the typed absent value `⊥_abs`, distinct from `⊥_und`. `≈_C` is now `an equivalence **or** ⊥_abs`, so the component is always supplied. **A2** restricted to *required* components and states explicitly that an optional component supplied as `⊥_abs` counts as supplied.
- **Mathematical justification:** an absence convention makes the two readings agree by construction; no context is now both complete and incomplete.
- **Effect on dependent definitions:** Definition 3.10; Definition 3.17 transports `⊥_abs` to `⊥_abs`.
- **Effect on dependent theorems:** Theorems 1, 6, 10′ and Proposition 11.1 all set `≈ = ⊥_abs` explicitly and are therefore complete contexts.
- **New assumptions introduced:** one symbol, `⊥_abs`.
- **Remaining proof obligation:** none.
- **Remediation verification status:** internally checkable.

## AV-004 — Profile construction and partial-function handling are incomplete

- **Severity:** Blocking
- **Exact verified defect:** only the probability-coupled construction was defined; a probability measure induces no canonical finite multiset, and its support need not be finite; and the branch where `δ^b_C` is defined on a non-null set but not almost everywhere was unclassified — neither nowhere-defined nor a.e.-defined, so no listed `⊥_und` condition applied and no profile existed.
- **Disposition:** **Accepted with Modification** — repaired by deletion plus exhaustive typing.
- **Exact affected section:** prior Definition 3.16; prior Definitions 5.2–5.3.
- **Exact repair:** the set-, multiset- and measure-valued profile classes are **deleted** (Observation 3.11.1). **Definition 5.2** defines the profile only when `μ_C(Ω^b_C) = 1`. **Definition 5.3** is rewritten as an exhaustive five-row case table, whose third row assigns `⊥_und` to exactly the unclassified branch `0 < μ_C(Ω^b_C) < 1` (Observation 5.3.1).
- **Mathematical justification:** the case table is exhaustive by construction: `T_C(b)` is defined or not; if defined, `μ_C(Ω^b_C)` is `0`, in `(0,1)`, or `1`; if `1`, the profile is or is not in `dom ρ_C`. These five cases partition the space.
- **Effect on dependent definitions:** Definitions 3.11, 5.2, 5.3; A5, A9.
- **Effect on dependent theorems:** every §8 theorem now has a determinate profile; the verification's counterexample (uniform `μ` with `δ^b_C(m)=m`, infinite image) no longer arises because no finite-support class is offered.
- **New assumptions introduced:** none.
- **Remaining proof obligation:** none.
- **Remediation verification status:** internally checkable.

## AV-005 — Several axioms are not mathematical predicates

- **Severity:** Blocking
- **Exact verified defect:** "valuation of a comparison", "available information", "determined set", "joint uncertainty", "comparison set" and "model class compatible with the evidence" name no object or predicate in the signature; A5 mixed point, set, interval and bottom outputs without a single typed codomain; A10 used an undeclared compatibility relation. Joint satisfiability was therefore not formally meaningful.
- **Disposition:** **Accepted with Modification** — two axioms demoted, three formalised.
- **Exact affected section:** prior A1, A5, A6, A9, A10.
- **Exact repair:** **A1 and A6 demoted** to non-formal **Design Principles DP-1 and DP-2** (§4.1), explicitly excluded from every proof, with Observation 4.1.1 recording that no proof cites them. **A5** replaced by an output-typing predicate over `Ŵ_C` referring to the case table of Definition 5.3. **A9** replaced by a predicate on `Ω^b_C = ∅`. **A10** replaced by a predicate on `r^{-1}(x) = ∅`, quantified only where `r` is supplied.
- **Mathematical justification:** the retained axioms A2, A3, A4, A5, A7, A8, A9, A10 are each a predicate over declared carriers and functions, and A4 is an existential schema over `𝒞`. Satisfaction is therefore decidable in a model, which is what makes Proposition 11.1 possible at all.
- **Effect on dependent definitions:** Definitions 5.3, 7.5.
- **Effect on dependent theorems:** no retained proof cites DP-1 or DP-2; verified by inspection. Proposition 11.1 checks the eight formal axioms only.
- **New assumptions introduced:** none; two are removed from the formal system.
- **Remaining proof obligation:** **OB-4** — formalise DP-1 and DP-2, or show neither is needed.
- **Remediation verification status:** internally checkable.

## AV-006 — Designation and filter contexts use an undefined structure

- **Severity:** Major
- **Exact verified defect:** no underlying structure, carrier, or automorphism group was defined; `Aut(C)` was defined via context morphisms while Definitions 6.2–6.3 switched to automorphisms of a different unnamed object; Theorem 2's displayed equality is a direct instance of A3, not a theorem that designation is necessary.
- **Disposition:** **Accepted with Modification** — repaired by withdrawal.
- **Exact affected section:** prior Definitions 6.2–6.3, Theorem 2, Corollaries 2.1–2.2.
- **Exact repair:** the definitions of *designation* and *filter context* are **withdrawn**. Prior Theorem 2 is **demoted** to **Corollary 6.2 (Orbit constancy under a fixed context)**, proved in one line from A3 with `ι_W = id`. Corollaries 2.1–2.2 and the claim that designation is *necessary* are **withdrawn** (§13). Observation 6.2.1 records the demotion and its ground.
- **Mathematical justification:** with the unnamed structure absent there is no group action on `𝔅`, so orbit language had no referent. `Aut(C)` of Definition 6.1 is well defined, and Corollary 6.2 is exactly what A3 yields for it — no more.
- **Effect on dependent definitions:** prior Definition 11.1 (structural valuation) also withdrawn, as it depended on the same absent action (see AV-023).
- **Effect on dependent theorems:** prior Limitation 14.8 and Rejection 16.7 withdrawn.
- **New assumptions introduced:** none.
- **Remaining proof obligation:** none. Recovering a designation theorem would require declaring the underlying structure — out of scope for bounded remediation.
- **Remediation verification status:** internally checkable.

## AV-007 — Order reversal has a valid numerical core but incomplete contexts

- **Severity:** Major
- **Exact verified defect:** the arithmetic `2>1`, `1<2` is correct, but the proof supplied no `𝔄_C`, no profile-class component, and no absence value for `≈_C`; Corollary 1.1 generalised an existential construction into a universal claim; Corollary 1.2 exhibited a null contrast rather than a model of the universal A4 sentence. A theory instance with one `W_1` context giving zero contrast for both bearers satisfies A4 and admits a constant context-free ordering.
- **Disposition:** **Accepted**
- **Exact affected section:** prior Theorem 1, Corollaries 1.1–1.2.
- **Exact repair:** Theorem 1's proof now supplies all seven components of Definition 3.10 explicitly, including `≈ = ⊥_abs` and `ρ = ℓ` the Dirac-atom location functional. The conclusion is labelled **existential** and **Observation 1.1′** states that it does not show every context family reverses. Prior **Corollary 1.1 is withdrawn**; prior Corollary 1.2 is retained only as the A4 satisfiability witness inside Proposition 11.1.
- **Mathematical justification:** the quantifier actually proved is `∃C_1,C_2`. Nothing universal follows, exactly as the verification's countermodel shows.
- **Effect on dependent definitions:** none.
- **Effect on dependent theorems:** prior Limitation 14.1 and Rejection 16.1's theorem-based ground **withdrawn**; Rejection 16.1 is retained but re-grounded on the *stipulation* in Definition 5.3 that `σ` is a function of `(C,b)`, not on Theorem 1.
- **New assumptions introduced:** none.
- **Remaining proof obligation:** none.
- **Remediation verification status:** internally checkable.

## AV-008 — Factorisation requires a precise quotient sigma-algebra and domain

- **Severity:** Major
- **Exact verified defect:** "the σ-algebra induced by `r`" was undefined; `h` was constructed only on `r(𝔐)` while the conclusion required `h : ℛ → W`; the measurability calculation is valid under the final/quotient σ-algebra for saturated sets but that convention was unstated; and Corollary 3.3 applied the theorem with codomain `𝒴_C`, which need not be a codomain in the sense of Definition 3.12.
- **Disposition:** **Accepted**
- **Exact affected section:** prior Theorem 3 and Corollary 3.3.
- **Exact repair:** **Definition 7.1** defines the final σ-algebra `ℋ_r := {A ⊆ ℛ : r^{-1}(A) ∈ ℱ}`. **Theorem 3** now hypothesises `(ℛ, ℋ_r)`, requires a nonempty codomain, and constructs `h` **total** on `ℛ` by fixing `v₀ ∈ 𝖵` off `r(𝔐)`. The codomain hypothesis is widened from a Definition 3.12 class to **any measurable space** `(𝖵, Σ_𝖵)`, which is what Corollary 3.3 needs. Observation 3.0 records both repairs.
- **Mathematical justification:** for `B ∈ Σ_𝖵`, `r^{-1}(h^{-1}(B)) = g^{-1}(B) ∈ ℱ`, so `h^{-1}(B) ∈ ℋ_r` by definition of the final σ-algebra. Totality requires `𝖵 ≠ ∅` to supply `v₀`, now hypothesised.
- **Effect on dependent definitions:** Definitions 7.4, 7.5, 7.7 now reference the repaired theorem.
- **Effect on dependent theorems:** Corollary 3.3 is now a literal instance; Theorem 3.2′ uses the repaired statement.
- **New assumptions introduced:** `𝖵 ≠ ∅`; the final σ-algebra convention.
- **Remaining proof obligation:** none.
- **Remediation verification status:** internally checkable.

## AV-009 — Measurable factorisation does not imply computability

- **Severity:** Blocking
- **Exact verified defect:** Corollary 3.1 concluded the contrast is *computable* from the representation iff `r` is sufficient. Measurability is not an algorithm. Counterexample: `𝔐 = ℛ = ℕ` discrete, `r = id`, `δ^b_C = 1_A` for non-computable `A` — measurable, fibre-constant on singletons, so `r` is sufficient, yet no algorithm computes it.
- **Disposition:** **Accepted with Modification** — repaired by withdrawal.
- **Exact affected section:** prior Corollary 3.1.
- **Exact repair:** **Corollary 3.1 is withdrawn.** Observation 3.1.1 records the withdrawal and reproduces the counterexample. Observation 3.0.1 lists *computability* explicitly among the things Theorem 3 does not establish. **No computability claim is made anywhere in the remediated document.**
- **Mathematical justification:** the counterexample was reconstructed independently and holds: the indicator of any subset of `ℕ` is measurable for the discrete σ-algebra, and fibre-constancy on singleton fibres is automatic, so sufficiency holds while computability fails.
- **Effect on dependent definitions:** none.
- **Effect on dependent theorems:** prior Open Question 15.2 reworded to ask for a *structural* characterisation of fibre-constancy, not a computational criterion.
- **New assumptions introduced:** none.
- **Remaining proof obligation:** none. Reinstating a computability statement would require an effective presentation and algorithmic hypotheses — out of scope.
- **Remediation verification status:** internally checkable.

## AV-010 — Forced abstention theorem is false for partial contrasts

- **Severity:** Blocking
- **Exact verified defect:** Definition 7.4's sufficiency can fail through non-totality alone, not only through non-constancy on a fibre; the proof of Corollary 3.2 silently discarded that branch. Counterexample: `𝔐 = {0,1}`, `r = id`, `𝒴 = {0,1}`, `M_C = id`, `τ = id`, `δ_C` defined only at `(1,1)` with value `0`. Then `r` is not sufficient, every fibre is a singleton, and no fibre carries two values.
- **Disposition:** **Accepted with Modification** — repaired by withdrawal and replacement.
- **Exact affected section:** prior Definition 7.4, Corollary 3.2.
- **Exact repair:** **Definition 7.4** now names three separate conditions — *total for* `(C,b)`, *fibre-constant for* `(C,b)`, and *`C`-sufficient* (both). **Corollary 3.2 is withdrawn.** **Theorem 3.2′** replaces it under the explicit hypothesis of totality: non-fibre-constancy then forces `|𝒮_C(b,x)| ≥ 2` and denies factorisation. The non-totality branch is routed to `⊥_und` by Definition 5.3, not to a two-element set. Observation 3.2.1 records the withdrawal and reproduces the counterexample.
- **Mathematical justification:** the counterexample was reconstructed independently and holds. Under totality the original argument is valid, and that is exactly the hypothesis Theorem 3.2′ adds.
- **Effect on dependent definitions:** Definition 7.5 gains an explicit `⊥_und` branch for `r^{-1}(x) ∩ Ω^b_C = ∅`.
- **Effect on dependent theorems:** prior Observation 7.6, Limitation 14.6 and Rejection 16.11 **withdrawn**.
- **New assumptions introduced:** totality, as an explicit hypothesis of Theorem 3.2′.
- **Remaining proof obligation:** none.
- **Remediation verification status:** internally checkable.

## AV-011 — Quotient descent is not a well-defined theorem for a partial evaluator

- **Severity:** Blocking
- **Exact verified defect:** Theorem 4 declared neither totality nor a quotient domain. Under the total reading uniqueness fails — with `≈_C` equality, `𝒴 = {0,1}` and `δ_C` defined only at `(0,0)`, any total map may take arbitrary values on the other three quotient pairs. Under the partial reading, A8 does not require the raw domain to be saturated, so the pullback need not return `D_C`.
- **Disposition:** **Accepted with Modification** — repaired by withdrawal and replacement.
- **Exact affected section:** prior Theorem 4.
- **Exact repair:** **Theorem 4 is withdrawn.** **Theorem 4′ (Partial quotient descent)** replaces it: `δ̄_C` is declared **partial** with domain exactly `D̄_C := (p×p)(D_C)`; uniqueness is claimed **only on `D̄_C`**; and the pullback relation is stated exactly — `δ̄_C ∘ (p×p)` has domain `(p×p)^{-1}(D̄_C) ⊇ D_C` and agrees with `δ_C` on `D_C`, with the inclusion strict unless `D_C` is saturated under `≈_C × ≈_C`. Observation 4.0 records both counterexamples.
- **Mathematical justification:** every point of `D̄_C` has a defined representative pair, on which A8 forces the value — giving existence, well-definedness and uniqueness on `D̄_C` and nowhere else. The saturation clause is exactly the condition under which pullback returns `D_C`.
- **Effect on dependent definitions:** Definition 3.10's `≈_C` row; A8.
- **Effect on dependent theorems:** prior Observation 7.9 withdrawn; the theorem summary corrected.
- **New assumptions introduced:** the domain `D̄_C`; the saturation condition, stated but not assumed.
- **Remaining proof obligation:** none.
- **Remediation verification status:** internally checkable.

## AV-012 — Posterior and kernel hypotheses do not support the information theorem

- **Severity:** Major
- **Exact verified defect:** a kernel and prior determine an evidence marginal, but a regular conditional posterior need not exist on arbitrary measurable spaces; "the induced posterior family" had no type or measurability condition; integrability alone supplies neither the barycentre identity nor measurability of the random risk. The concavity argument is correct *once* a measurable regular posterior with the disintegration identity is assumed.
- **Disposition:** **Accepted**
- **Exact affected section:** prior Definition 3.20, Definition 8.4, Theorem 5(iii), OB-3.
- **Exact repair:** **Definition 3.14 (Regular evidence structure)** now bundles the kernel `K_b` with a **regular** conditional probability `Π_b`, the **barycentre identity** `∫ Π_b(·|e) λ_b(de) = μ_C`, and **measurability and λ_b-integrability** of `e ↦ 𝔯(Π_b(·|e))`. Definition 8.4 and Theorem 5(iii) are asserted only for such a structure. Observation 5.0 states the restriction. Observation 3.14.1 records why.
- **Mathematical justification:** with regularity, the barycentre identity and integrability supplied as hypotheses of the structure, Jensen's inequality for the concave functional `𝔯` applies exactly. Without them the integral in Definition 8.4 need not exist.
- **Effect on dependent definitions:** Definition 8.4.
- **Effect on dependent theorems:** Theorem 5(iii) narrowed; Theorem 6(ii)–(iii) declare a regular structure explicitly.
- **New assumptions introduced:** regularity, barycentre identity, risk measurability and integrability — all as hypotheses of Definition 3.14, not as background assumptions.
- **Remaining proof obligation:** **OB-3** — conditions guaranteeing that a regular evidence structure exists on given spaces.
- **Remediation verification status:** internally checkable; OB-3 open.

## AV-013 — Pairwise non-equivalence constructions omit decisive parameters

- **Severity:** Major
- **Exact verified defect:** the constructions declared no `ρ_C` despite Definition 8.1 making it primitive, and no `ε`; the displayed value `1` uses `ε = 0`, and for `ε ≥ 1` the strict decision ordering in part (i) disappears; in part (iii) the assertion that the effect is less than `1` depends on the unspecified location functional — a reduction returning `2` on the half-normal profile is compatible with the undefined term. Corollary 6.1 additionally relies on an undefined latent quantity.
- **Disposition:** **Accepted**
- **Exact affected section:** prior Definition 8.1, Theorem 6, Corollary 6.1.
- **Exact repair:** **Definition 3.12** now defines *location functional*: bounded between `inf supp` and `sup supp`, and equal to the atom on Dirac profiles. **Theorem 6** hypothesises `ρ_C = ℓ` the **mean**, `ε = 0` **with attainment**, and displays all three complete contexts. Part (iii) now computes `σ^eff(b₂) = 𝔼|θ₂| = s√(2/π)` exactly, with the range `s < √(π/2)` stated. **Corollary 6.1 is withdrawn** (Observation 6.1′).
- **Mathematical justification:** the mean is a location functional by Definition 3.12. With `ε = 0` and squared loss on `ℝ` the infimum is attained, so `𝒜*₀` is a singleton and the displayed values are forced. `𝔼|θ₂|` for `θ₂ ~ 𝒩(0,s²)` is `s√(2/π)`, which is `< 1` exactly when `s < √(π/2)`.
- **Effect on dependent definitions:** Definition 3.12 added; Definition 8.1 references it.
- **Effect on dependent theorems:** Theorem 5(i)'s proof now cites Definition 3.12 for `ℓ(ν) ≥ inf supp ν ≥ 0`; prior Rejection 16.5 withdrawn.
- **New assumptions introduced:** the support-bound and Dirac conditions on `ℓ`; `ε = 0` with attainment in Theorem 6.
- **Remaining proof obligation:** none. A common-latent-order claim would need a formal hypothesis on admissible measurement maps — not supplied, and Corollary 6.1 stays withdrawn.
- **Remediation verification status:** internally checkable.

## AV-014 — Additive context-free scalar theorem is false

- **Severity:** Blocking
- **Exact verified defect:** A4 supplies a null context in the global set `𝒞`, while the decomposition was required only on "the family considered"; the proof assumed without hypothesis that the A4 witness lies in that family. Countermodel: `𝔅 = {b}`, `𝒞 = {C₀,C₁}`, family `{C₁}`, `σ_{C₀}(b) = 0`, `S(b) = 1`, `β = 1`, `g_{C₁}(b) = 0`, `σ_{C₁}(b) = 1` — every hypothesis holds, the conclusion `S(b) = 0` fails.
- **Disposition:** **Accepted with Modification** — repaired by withdrawal and replacement.
- **Exact affected section:** prior Theorem 7.
- **Exact repair:** **Theorem 7 is withdrawn.** **Theorem 7′** replaces it with an explicit hypothesis (a): the family `𝒦` is **nullity-closed** — for every `b` there is `C ∈ 𝒦` with `σ_C(b) = 0` — alongside (b) the decomposition on every `C ∈ 𝒦`. Observation 7.0 records the countermodel.
- **Mathematical justification:** the countermodel was reconstructed independently and holds. Hypothesis (a) is precisely what the prior proof silently used; with it, the one-line argument is valid.
- **Effect on dependent definitions:** none.
- **Effect on dependent theorems:** prior Limitation 14.2 and Rejections 16.2 and 16.17's theorem-based clauses **withdrawn**. Rejection 16.17 is retained only as an inspection claim: no context-free ordering primitive is declared in the signature.
- **New assumptions introduced:** nullity-closure of the family.
- **Remaining proof obligation:** none.
- **Remediation verification status:** internally checkable.

## AV-015 — Mutual-information theorem is valid, but its epistemic corollary is false

- **Severity:** Major
- **Exact verified defect:** the two identities are correct; the corollary does not follow. Conditional redundancy given `R` is not absence of information for an observer receiving only `S`. Counterexample: `Z = R = S` a non-degenerate Bernoulli variable gives `I(Z;S|R) = 0` while `I(Z;S) = H(Z) > 0`.
- **Disposition:** **Accepted with Modification** — repaired by withdrawal.
- **Exact affected section:** prior Corollary 8.1.
- **Exact repair:** **Corollary 8.1 is withdrawn.** Theorem 8 is retained unchanged and renamed *Conditional information redundancy*. Observation 8.1′ states the exact surviving content: a derived summary adds no information **to an observer who already has `R`**.
- **Mathematical justification:** the counterexample was reconstructed independently and holds.
- **Effect on dependent definitions:** none.
- **Effect on dependent theorems:** prior Limitation 14.3 **withdrawn**; Rejection 16.3 **retained in narrowed form**, conditioned on simultaneous access to `R`; the epistemic clause of prior Rejection 16.17 withdrawn.
- **New assumptions introduced:** none.
- **Remaining proof obligation:** none.
- **Remediation verification status:** internally checkable.

## AV-016 — Normalisation theorem is valid, but both corollaries overreach

- **Severity:** Major
- **Exact verified defect:** Theorem 9's inequality and order preservation are correct, but they do not imply incomparability or absence of information; if denominators are known the original values are recoverable, and `ν^A(a) = ν^{A'}(b) = 1` informatively says both are arena maxima. Dimensionlessness prevents direct dimensional equality or addition, not calibration by a declared dimensioned scale `x ↦ Dx`.
- **Disposition:** **Accepted with Modification** — repaired by withdrawal.
- **Exact affected section:** prior Corollaries 9.1–9.2.
- **Exact repair:** **Both corollaries are withdrawn.** Theorem 9 retained unchanged with `A` nonempty stated. Observation 9.1′ states the exact surviving content: a normalised value depends on its arena's maximum, so comparing normalised values across arenas *without also declaring the denominators* is uninformative about `φ`.
- **Mathematical justification:** both counterexamples were reconstructed independently and hold.
- **Effect on dependent definitions:** none.
- **Effect on dependent theorems:** prior Rejection 16.4 **withdrawn**; prior Limitation 14.7 **narrowed** to the A7 stipulation in the absence of a declared transport.
- **New assumptions introduced:** `A` finite nonempty, stated explicitly.
- **Remaining proof obligation:** none.
- **Remediation verification status:** internally checkable.

## AV-017 — Universal-encodability proof assumes a measurable group operation

- **Severity:** Blocking
- **Exact verified defect:** class `W₂` is an ordered abelian group but Definition 3.12 did not make subtraction measurable, and measurable singletons do not imply it. Counterexample: `ℝ` with the countable–cocountable σ-algebra has all singletons measurable, yet the diagonal is not product-measurable, so subtraction is not measurable and the constructed `δ(y,y') = y'−y` violates Definition 3.14. Constant maps are measurable regardless, so that part of the proof was sound but the singleton hypothesis was doing no work.
- **Disposition:** **Accepted with Modification** — repaired by replacing the proof, not the theorem's existential content.
- **Exact affected section:** prior Theorem 10's proof.
- **Exact repair:** the evaluator is replaced by the **second projection** `δ_C(y,y') := y'`, which is product-measurable on any measurable space and requires **no algebraic structure at all**. Consequently Theorem 10′ drops the class-`W₂` hypothesis entirely and holds for **any** codomain with at least one element. A new codomain class **`W₂^m` (measurably signed)** is added to Definition 3.5 to record the distinction, and Observation 3.6 reproduces the countable–cocountable counterexample. No theorem uses subtraction unless it declares `W₂^m`.
- **Mathematical justification:** the counterexample was reconstructed independently and holds. The projection `(y,y') ↦ y'` is measurable with respect to `Σ_W ⊗ Σ_W` by definition of the product σ-algebra; constant maps `m ↦ f(b)` are measurable on any domain. Both facts are hypothesis-free.
- **Effect on dependent definitions:** Definition 3.5 gains class `W₂^m`; Observation 3.6 added.
- **Effect on dependent theorems:** Theorem 10′ is strictly stronger in reach and strictly weaker in claimed scope than prior Theorem 10.
- **New assumptions introduced:** none — one is removed.
- **Remaining proof obligation:** none.
- **Remediation verification status:** internally checkable.

## AV-018 — Universal encodability is restricted, and the no-empirical-content conclusion does not follow

- **Severity:** Blocking
- **Exact verified defect:** the theorem quantifies only over assignments into a `W₂` group and builds only a generic probability-coupled contrast valuation; it constructs no qualitative, interval, distributional, effect, decision, information, composition or diffusion form. Effect, decision and information significance are constrained non-negative by Theorem 5, so an assignment of `−1` as effect significance is excluded outright. The theorem concerns a single context, while joint assignments are further constrained by A3, A4 and A7. Corollary 10.2's exhaustiveness claim is also unproved.
- **Disposition:** **Accepted with Modification** — repaired by withdrawal and bounded replacement. **This is the most consequential adjudication in the record.**
- **Exact affected section:** prior Theorem 10's "Applies to" line, Corollaries 10.1–10.2, Observations 1.2 and 10.4, Limitation 14.9, Rejection 16.14, theorem summary.
- **Exact repair:** the **"applies to all forms" label is withdrawn**; Theorem 10′ is labelled *deterministic contrast form only, with a projection evaluator*, and explicitly **not** effect, decision, information or composition. **Corollary 10.1 — "the unrestricted framework has no empirical content whatever" — is withdrawn.** **Corollary 10.1′ (Bounded underdetermination)** replaces it: *within the deterministic contrast form with unrestricted evaluators, no single-context assignment is excluded by the axioms.* **Corollary 10.2 is withdrawn** for unproved exhaustiveness. Prior Limitation 14.9 and Rejection 16.14 are **withdrawn**; new Limitation 14.11 states only what Corollary 10.1′ supports. Observation 10.1.1 records the withdrawal and the three grounds. Observation 10.0.1 records that the witness evaluator is **degenerate** — it ignores the factual outcome — so the honest content is that the axioms do not exclude degenerate evaluators.
- **Mathematical justification:** all three grounds were checked. Theorem 5 does force non-negativity of the three named forms under its hypotheses, so `−1` is unreachable as an effect significance; Theorem 10′ constructs one context and says nothing about joint families; and no argument was offered for exhaustiveness in Corollary 10.2.
- **Effect on dependent definitions:** none.
- **Effect on dependent theorems:** the document's principal epistemic claim is removed. **No conclusion about the empirical content of the whole framework is drawn anywhere in the remediated document.**
- **New assumptions introduced:** none.
- **Remaining proof obligation:** none. A framework-wide empirical-content result would require constructing every form and handling the cross-context axioms — out of scope for bounded remediation, and not attempted.
- **Remediation verification status:** internally checkable.

## AV-019 — Composition has no defined carrier or endpoints

- **Severity:** Blocking
- **Exact verified defect:** `E` was never defined; a relation instance carried only a type and signature, so it had no source or target to match; `κ` determines the domain of a partial operation but not its output, so `⊙` cannot be *derived* from `κ`; empty-path semantics were absent; the diffusion product is total only once `E`, paths and finite weights exist.
- **Disposition:** **Accepted**
- **Exact affected section:** prior Definitions 10.1–10.6.
- **Exact repair:** **Definition 10.1** now declares a complete composition signature `(U, E, src, tgt, t, κ, ⊙, w)` with `src, tgt : E → U`, `κ` restricted to endpoint-compatible pairs, `⊙ : κ → E` **primitive** and endpoint-coherent, and `w : E → ℝ≥0`. **Definition 10.2** admits only nonempty paths, excluding the empty-path case explicitly. Observation 10.1.1 records that `⊙` is primitive because many operations share a domain.
- **Mathematical justification:** endpoint coherence `src(e⊙f) = src(e)`, `tgt(e⊙f) = tgt(f)` makes iterated composition along a path well formed. Making `⊙` primitive is forced by the verification's observation that `κ` underdetermines it.
- **Effect on dependent definitions:** Definitions 10.2, 10.3.
- **Effect on dependent theorems:** Theorems 11, 12′, 13′ now have a complete signature.
- **New assumptions introduced:** `U`, `src`, `tgt`, `⊙` as primitives; endpoint coherence.
- **Remaining proof obligation:** none.
- **Remediation verification status:** internally checkable.

## AV-020 — Non-associativity proof operates on types, not relation instances

- **Severity:** Blocking
- **Exact verified defect:** the proof supplied a table on `T` and then assumed instance compositions exist with the table's output type, giving no instances for intermediate results and no instance-level operation; its hypothesis was the circular phrase "a composition table as constructed". Corollary 12.2 converted an existential into the universal claim that a path does not determine its composite, which is false for one-edge paths and for associative operations. "Substructure" and "licensed path" were undefined, so Corollary 12.3 could not follow.
- **Disposition:** **Accepted with Modification** — repaired by reconstruction and withdrawal.
- **Exact affected section:** prior Theorem 12, Corollaries 12.1–12.3.
- **Exact repair:** **Theorem 12′** exhibits the full instance-level construction: `U = {u₀,…,u₃}`, `E = {e₁,e₂,e₃,a,q}` with stated endpoints, `κ = {(e₁,e₂),(e₂,e₃),(e₁,q)}`, and `⊙` given explicitly by `e₁⊙e₂ := a`, `e₂⊙e₃ := q`, `e₁⊙q := a`, each endpoint-coherent. Then `(e₁⊙e₂)⊙e₃` is undefined and `e₁⊙(e₂⊙e₃) = a` is defined. **Corollaries 12.2 and 12.3 are withdrawn.** Observation 12.1′ states the exact surviving content and records why the universal form is false.
- **Mathematical justification:** the construction is finite and checkable by inspection; the verification's objection that one-edge paths always determine their composite is correct, so only an existential claim is made.
- **Effect on dependent definitions:** none.
- **Effect on dependent theorems:** prior Limitation 14.5 and Rejection 16.9 **withdrawn**.
- **New assumptions introduced:** none.
- **Remaining proof obligation:** none.
- **Remediation verification status:** internally checkable.

## AV-021 — Semantic-separation example is underconstructed

- **Severity:** Major
- **Exact verified defect:** the products `1` and `1/100` are correct, but the proof used endpoints absent from Definition 10.1, assumed without a graph definition that exactly two paths exist, did not address convergence of general path sums, and left the output instance of a `κ`-pair unspecified.
- **Disposition:** **Accepted**
- **Exact affected section:** prior Theorem 13.
- **Exact repair:** **Theorem 13′** supplies the full signature: `U = {a,b,c,c',z}`, five instances with stated endpoints, and `⊙` defined on the single `κ`-pair with output `g`. Path finiteness is **established by inspection of the endpoint maps** rather than assumed, so the sums are finite and convergence is not at issue.
- **Mathematical justification:** with the endpoint maps fixed, enumerating paths from `a` to `z` and from `b` to `z` is a finite check; the sums are `1` and `1/100` respectively.
- **Effect on dependent definitions:** none.
- **Effect on dependent theorems:** Observation 13.1′ retains the narrow interpretive point and disclaims the invalidity reading.
- **New assumptions introduced:** none beyond Definition 10.1.
- **Remaining proof obligation:** none.
- **Remediation verification status:** internally checkable.

## AV-022 — Recognisability and prior-art assertions are unsupported and partly false

- **Severity:** Blocking
- **Exact verified defect:** `U`, `Q`, registers, guards, transition semantics and the reduction from `κ` were undefined; no finiteness was placed on `U` or `Q`, so finite `S` does not give a finite product (take `U` infinite, `S` a singleton); decidability needs an effective finite presentation, not a finite carrier, and an arbitrary `κ` can encode a non-computable membership relation; the state count is an upper bound before reachability minimisation, not an equality; and the universal claim that no invariant lies outside every existing typed, temporal or dimensional formalism had neither a quantified comparison class nor a proof or citation.
- **Disposition:** **Accepted with Modification** — repaired by withdrawal in full.
- **Exact affected section:** prior Observations 10.7–10.9, Limitation 14.10, Open Question 15.6's negative closure.
- **Exact repair:** **the entire recognisability subsection is withdrawn**, together with the state-count claim, the decidability claim, and the universal prior-art subsumption claim. Prior **Limitation 14.10 is withdrawn**. **Open Question 15.6 is reopened**, with its prior negative closure explicitly retracted. Observation 10.4′ records all of this. The narrower disclaimer — *no novelty is claimed* — is **retained**, since it requires no proof of universal subsumption.
- **Mathematical justification:** every one of the verification's five objections holds. In particular the infinite-`U` counterexample is decisive against the finite-product claim, and no comparison class was ever quantified for the subsumption claim.
- **Effect on dependent definitions:** none; the withdrawn material defined nothing that survives.
- **Effect on dependent theorems:** none. Theorems 11, 12′ and 13′ concern the composition signature, not its recognisability.
- **New assumptions introduced:** none.
- **Remaining proof obligation:** a formal automaton reduction with finiteness and effectiveness hypotheses would be required to reinstate any of this. Not attempted; out of scope.
- **Remediation verification status:** internally checkable. **Note:** this reverses a closure the author made in an earlier session on the strength of a prior-art document. The verification is right that a universal subsumption claim was never proved.

## AV-023 — Structural valuation is not context indexed and its theorem is tautological

- **Severity:** Major
- **Exact verified defect:** `φ` had no declared codomain and no fixed context although automorphisms were defined as `Aut(C)`, so "every automorphism" could range over incompatible context groups; once a fixed action is supplied Theorem 14 is exactly Definition 11.1 restated; Corollary 14.1's second clause ("depends on data outside an invariance class") is not a logical consequence of non-structurality; and an artefact morphism's claimed identity action was not reconciled with its non-identity relabelling.
- **Disposition:** **Accepted with Modification** — repaired by withdrawal and demotion.
- **Exact affected section:** prior Definitions 11.1–11.2, Theorem 14, Corollaries 14.1–14.2.
- **Exact repair:** prior **Definition 11.1 (structural valuation), Definition 11.2 (artefact morphism), Theorem 14 and Corollary 14.1 are withdrawn.** What survives is **Corollary 6.2**, stated for a **fixed** context `C`, a **fixed** group `Aut(C)` of Definition 6.1, and the declared codomain `Ŵ_C` — proved in one line from A3. The second clause of Corollary 14.1 is **withdrawn**. Rejection 16.13 is **narrowed** to morphisms in the declared universe.
- **Mathematical justification:** the verification is correct that orbit constancy is definitional once typed; presenting it as an independent all-forms theorem overstated it. The counterexample to the second clause — an arbitrary label-dependent function failing orbit constancy without depending on declared data — holds.
- **Effect on dependent definitions:** Definition 6.1 retained; 11.1–11.2 removed.
- **Effect on dependent theorems:** Proposition 11.1's A3 check is now the only place covariance is exercised.
- **New assumptions introduced:** none.
- **Remaining proof obligation:** none.
- **Remediation verification status:** internally checkable.

## AV-024 — The named consistency witness does not instantiate its claimed fragment

- **Severity:** Blocking
- **Exact verified defect:** each context supplied `μ_C` but no `𝔄_C`, so the claim that all eight components were supplied was false; the outcome σ-algebra was not written; A3 was checked only for the identity — which is vacuous — and then asserted for all relabellings "by Definition 3.22", which is not a satisfaction check because the context set was not shown closed under transports and Definition 3.22 was itself incomplete; and the decision problem on `C₁` instantiated no decision significance or `W₂`-valued context.
- **Disposition:** **Accepted with Modification** — repaired by withdrawal and reconstruction.
- **Exact affected section:** prior Proposition 12.1.
- **Exact repair:** **Proposition 12.1 is withdrawn.** **Proposition 11.1** replaces it with four specific corrections: (a) `𝔄_C` no longer exists, so all **seven** components are genuinely supplied; (b) the outcome σ-algebra is declared Borel on `ℝ`; (c) a **nontrivial** morphism universe `𝒢 = {id, ȷ}` is declared, with `ȷ` the coordinate-swap involution, and the A3 check is performed **for `ȷ`** with the transported components computed explicitly from Definition 3.17 — the check is therefore **not vacuous**; (d) the context set `𝒞 = {C₁, C₂, C₀}` is **proved closed** under `𝒢`, with `ȷ_*C₁ = C₂`, `ȷ_*C₂ = C₁` and `ȷ_*C₀ = C₀`. The fragment is restricted to the deterministic form with a `W₁` codomain, so no decision or `W₂` claim is made.
- **Mathematical justification:** the A3 computation is displayed in the proof: transporting `C₁` by `ȷ` yields outcome map `y` and operation `(x,y) ↦ (x+1,y+2)` for `ȷ_𝔅 b₁ = b₂`, giving contrast `2 = σ_{C₁}(b₁)` with `ȷ̂_W = id`. Closure makes every `ι_*C` an element of `𝒞`, which is what A3's quantifier requires over the declared universe.
- **Effect on dependent definitions:** none.
- **Effect on dependent theorems:** this is the document's only consistency result; it now supports exactly the deterministic fragment over `𝒢`.
- **New assumptions introduced:** the finite morphism universe `𝒢`.
- **Remaining proof obligation:** **OB-1** — consistency beyond this fragment, and A3 over *all* representation morphisms rather than `𝒢`. **Blocking.**
- **Remediation verification status:** internally checkable; OB-1 open and blocking.

## AV-025 — A4 is satisfied in the witness, but full-signature consistency is not presently a proposition

- **Severity:** Major
- **Exact verified defect:** A4 is genuinely satisfied by `C₀` for both bearers, A8 by equality and A10 by the identity map; A5 and A9 were only informally or vacuously checked because their predicates were undefined; A6 was vacuous. A broader witness cannot be certified without assigning meanings to `𝔄_C`, profile induction, transported bottoms, `E`, endpoints and the automaton objects — and assigning them would add structure not fixed by the candidate.
- **Disposition:** **Deferred Open Obligation**
- **Exact affected section:** prior Observation 12.2, OB-1.
- **Exact repair:** the undefined objects are now either **defined** (`Ŵ`, transported bottoms via Definition 3.16, `E` and endpoints via Definition 10.1) or **deleted** (`𝔄_C`, three profile classes, the automaton objects). A5, A9 and A10 are now formal predicates (AV-005), so their satisfaction is checkable — Proposition 11.1 checks them non-vacuously. **Observation 11.1.2** states the binding exclusion list for what the witness does **not** cover: codomain classes `W₂` and `W₂^m`; interval and bottom outputs; non-trivial `≈_C`; decision structure; evidence structure; non-atomic measures; the composition signature; and A3 over all morphisms. **OB-1 is retained as Blocking.**
- **Mathematical justification:** the verification's point that full consistency was "presently unaskable" is met in part — the signature is now complete enough for the question to be well posed — but the model exhibited covers only the deterministic fragment, so the answer remains unknown.
- **Effect on dependent definitions:** none.
- **Effect on dependent theorems:** no theorem claims full-signature consistency.
- **New assumptions introduced:** none.
- **Remaining proof obligation:** **OB-1**, Blocking.
- **Remediation verification status:** open by construction; explicitly not claimed resolved.

## AV-026 — Internal references, theorem summaries, and notation do not match the candidate

- **Severity:** Minor
- **Exact verified defect:** references to a nonexistent section 18 at lines 10, 22 and 456; a reference sending relation-instance composition to section 11 when it is in section 10; a theorem table labelling Theorems 3, 4, 6, 7, 10 and 12 as proved and overstating Theorem 10 as applying to all forms; `E`, `I(W_C)`, `U`, `Q`, `S` undefined; corollaries under Theorem 3 numbered 3.3, 3.1, 3.2, obscuring dependency order.
- **Disposition:** **Accepted**
- **Exact affected section:** prior §1, §2, §13 table, §16, and the corollary ordering in §7.
- **Exact repair:** all cross-references now resolve — the rejected-formulations section is §16 and is referenced as such; composition is referenced as §10. `E`, `U` are **defined** (Definition 10.1); `I(W)` is **defined** (Definition 3.7); `Q` and `S` are **removed** with the withdrawn recognisability subsection. The proven-results table (§12) is rebuilt from the post-remediation status and no longer lists Theorems 4, 7, 12 or prior 10; Theorem 10′ is labelled deterministic-form-only. Corollaries under Theorem 3 are ordered 3.0, 3.0.1, 3.3, 3.2′, with dependency order preserved.
- **Mathematical justification:** none required; these are reference and inventory corrections, made only after theorem status was resolved, as the verification instructed.
- **Effect on dependent definitions:** none.
- **Effect on dependent theorems:** none.
- **New assumptions introduced:** none.
- **Remaining proof obligation:** none.
- **Remediation verification status:** mechanically checked — cross-reference and delimiter audits pass.

## AV-027 — Multiple limitations and rejected formulations do not follow from their cited results

- **Severity:** Blocking
- **Exact verified defect:** Limitation 14.2 depends on false Theorem 7; 14.3 overstates Theorem 8; 14.9 depends on the overgeneralised encodability corollary; Rejection 16.7 is not implied by symmetry and conflicts with the context's own admissibility component; 16.8 omits Theorem 11's hypothesis; 16.12 unqualifiedly rejects cross-context comparison although A7 and Definition 8.10 expressly permit it under a declared transport; and 14.4's claim that distinct reductions always induce distinct orderings is false, since distinct positive rescalings induce the same ordering.
- **Disposition:** **Accepted**
- **Exact affected section:** prior Limitations 14.1–14.10, Rejections 16.1–16.19.
- **Exact repair:** the limitation and rejection sections are **rebuilt from the post-remediation dependency closure**. **Withdrawn limitations:** 14.1, 14.2, 14.3, 14.5, 14.6, 14.9, 14.10. **Retained:** 14.4 with its false second clause **removed**; 14.7 narrowed to the A7 stipulation *absent a declared transport*. **New:** 14.11 (bounded underdetermination), 14.12 (fragment-only consistency). **Withdrawn rejections:** 16.2, 16.4, 16.5, 16.7, 16.9, 16.11, 16.14. **Narrowed:** 16.1 re-grounded on the stipulation in Definition 5.3 rather than Theorem 1; 16.3 conditioned on simultaneous access to `R`; 16.8 conditioned on Theorem 11's hypothesis, with the type-determined case explicitly conceded; 16.12 conditioned on the absence of a declared transport; 16.13 restricted to the declared morphism universe; 16.17 reduced to an inspection claim. Every withdrawal is listed in §13 with its finding.
- **Mathematical justification:** each retained entry now names a verified result and matches its quantifiers. Each withdrawn entry depended on a statement that is false or withdrawn.
- **Effect on dependent definitions:** none.
- **Effect on dependent theorems:** none — this repair is downstream of the theorems.
- **New assumptions introduced:** none.
- **Remaining proof obligation:** none.
- **Remediation verification status:** internally checkable by comparing §12, §13, §14 and §16.

## AV-028 — Status, empirical boundary, and non-novelty disclaimer are accurately limited

- **Severity:** Observation
- **Exact verified defect:** none. The candidate status, non-freeze, non-validation and non-novelty disclaimers were found accurate and consistent with the repository research controls, which independently record `EH-0` and exclude this candidate from the Version 1 freeze. OB-2 and OB-3 were correctly recorded as genuine open obligations.
- **Disposition:** **Accepted** — no repair required to the disclaimer itself.
- **Exact affected section:** document control, scope, OB-2, OB-3.
- **Exact repair:** the disclaimers are **retained and strengthened**: the status table now additionally records that the prior candidate was independently verified NOT FORMALLY SOUND, and that no universal prior-art subsumption is claimed. OB-2 and OB-3 are carried forward unchanged in substance, OB-3 reworded to match the regular-evidence-structure repair of AV-012.
- **Mathematical justification:** none required.
- **Effect on dependent definitions:** none.
- **Effect on dependent theorems:** none.
- **New assumptions introduced:** none.
- **Remaining proof obligation:** OB-2, OB-3 — both non-blocking.
- **Remediation verification status:** carried forward; the verification's own assessment stands.

---

## Blocking-defect closure table

Every Blocking finding ends in exactly one of the four permitted outcomes.

| Finding | Outcome | Detail |
|---|---|---|
| AV-001 | 2 — withdrawn | `𝔄_C` and three profile classes deleted from the signature |
| AV-002 | 1 — repaired with proof | Extended action `ι̂_W` on all of `Ŵ`; all components transported |
| AV-004 | 2 + 3 — withdrawn and narrowed | Three profile classes deleted; Definition 5.3 case table exhaustive |
| AV-005 | 2 — withdrawn | A1, A6 demoted out of the formal system; A5, A9, A10 formalised |
| AV-009 | 2 — withdrawn | Corollary 3.1 withdrawn; no computability claim remains |
| AV-010 | 2 + 3 — withdrawn and narrowed | Corollary 3.2 withdrawn; Theorem 3.2′ under totality, with proof |
| AV-011 | 2 + 1 — withdrawn and replaced | Theorem 4 withdrawn; Theorem 4′ proved on `D̄_C` |
| AV-014 | 2 + 3 — withdrawn and narrowed | Theorem 7 withdrawn; Theorem 7′ on a nullity-closed family, with proof |
| AV-017 | 1 — repaired with proof | Projection evaluator; no algebraic hypothesis needed |
| AV-018 | 2 + 3 — withdrawn and narrowed | Corollaries 10.1, 10.2 withdrawn; Corollary 10.1′ bounded, with proof |
| AV-019 | 1 — repaired | Complete composition signature with primitive `⊙` |
| AV-020 | 2 + 1 — withdrawn and replaced | Corollaries 12.2, 12.3 withdrawn; Theorem 12′ instance-level, with proof |
| AV-022 | 2 — withdrawn | Recognisability subsection withdrawn in full; OQ 15.6 reopened |
| AV-024 | 2 + 1 — withdrawn and replaced | Proposition 12.1 withdrawn; Proposition 11.1 with non-vacuous A3 check |
| AV-027 | 2 + 3 — withdrawn and narrowed | Seven limitations and seven rejections withdrawn; six narrowed |

**No Blocking finding was relabelled non-blocking.** One Blocking obligation is **created and retained as blocking**: **OB-1**, full-signature consistency, arising from AV-024 and AV-025.
