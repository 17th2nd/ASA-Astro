# ASTRO-THEORY-0001 Independent Verification Report

## Document control

| Field | Value |
|---|---|
| Report identifier | `ASTRO-THEORY-0001-INDEPENDENT-VERIFICATION-REPORT` |
| Examination date | 2026-08-01 |
| Repository | `17th2nd/ASA-Astro` |
| Canonical path examined | `docs/theory/ASTRO-THEORY-0001.md` |
| Required and observed source blob | `08a2257aaea6e5f23b316682025022b62d834d68` |
| Required and observed baseline commit | `365b25301d7467139d68257f34a3a81cd7fe73ef` |
| Local `HEAD` before report mutation | `365b25301d7467139d68257f34a3a81cd7fe73ef` |
| Local `origin/main` after fetch | `365b25301d7467139d68257f34a3a81cd7fe73ef` |
| Ahead / behind before report mutation | `0 / 0` |
| Branch | `main` |
| Initial worktree and index | Clean; no staged files |
| Candidate mutation | None |
| Verification disposition | **ASTRO-THEORY-0001 NOT FORMALLY SOUND** |

## 1. Verification basis and independence

This examination used only the exact source blob identified above as the theory
candidate. `git fetch origin` completed before examination. `HEAD`,
`origin/main`, the required baseline, and the blob at the canonical path all
matched. No repository `AGENTS.md` or equivalent local instruction file was
present. The repository `README.md`, the frozen protocol
`ASTRO-EXP-0001@1.0`, the frozen claims register `ASTRO-CLAIMS-0001@1.0`, the
append-only results ledger `ASTRO-RESULTS-0001@1.0`, and the Version 1 research
controls freeze report were inspected for authority and status boundaries.

No earlier mathematical verification report, finding, reconstruction, change
map, or defect-resolution claim was used as evidence for a finding in this
report. The candidate's own provenance paragraph was read because it is part of
the required blob; the earlier findings it mentions were not adopted. The two
companion theory records were not used as a proof basis.

The research controls establish that this candidate is outside the Research
Controls Version 1 freeze. They record zero experiments, zero empirical results,
and evidence level `EH-0`. Nothing in this mathematical report changes those
states.

## 2. Executive determination

The candidate is readable as an informal mathematical proposal, but it is not a
complete formal theory and is not suitable for freeze. The failure is not one of
style. It is structural:

1. the context and transport signatures contain undefined and ill-typed
   objects;
2. several axioms are not formal predicates and therefore cannot be satisfied
   or falsified in a model;
3. Theorem 7 is false under its written hypotheses;
4. Corollary 3.2 is false because it suppresses the partiality branch built into
   its own definition of sufficiency;
5. the published proof of the load-bearing universal-encodability theorem uses
   measurability not supplied by its hypotheses, and its all-forms and
   no-empirical-content consequences are stronger than the theorem;
6. the composition and recognisability sections use an undefined carrier,
   undefined endpoints, undefined automaton components, and missing finiteness
   and effectiveness hypotheses;
7. the stated consistency witness does not supply every context component and
   does not verify A3 over a defined universe of morphisms.

No contradiction of the form `P` and `not P` was derived inside the
well-formed elementary fragment. That does not establish consistency. The full
candidate is not sufficiently defined for model-theoretic consistency to have a
determinate meaning.

## 3. Findings

### AV-001 — Incomplete context signature

- **Severity:** Blocking
- **Exact location:** Definition 3.14, lines 86–100; Definition 3.16, lines
  103–114.
- **Statement examined:** A context is an eight-component tuple containing an
  admissibility restriction `A_C`, and its reduction has domain a declared
  profile class `P_C` and may return an element of `I(W_C)`.
- **Defect or verification result:** `A_C` has no declared carrier, type, or map
  from which `mu_C` is determined. `P_C` is required to be declared but is not a
  component of the context tuple. `I(W_C)` is not defined. Consequently the
  tuple does not determine the `mu_C` and profile objects used by Definitions
  5.1–5.3, and the output type of `rho_C` is not a declared set.
- **Counterexample or proof:** Two distinct rules can map the same informal
  “admissibility restriction” to different probability measures; the tuple
  supplies no mathematical relation selecting one. Likewise two contexts can
  have the same eight displayed components while choosing different profile
  classes, because the class selector is absent from the tuple.
- **Consequence:** Context equality, contextual completeness, transported
  contexts, significance, and model satisfaction are not well defined.
- **Required resolution:** Define the type and semantics of `A_C`, include or
  uniquely derive the profile class, and define `I(W_C)` before the theory can be
  modelled.
- **Downstream impact:** A2; A3; Definitions 5.2–5.3; Theorems 1, 2, 5, 6, and
  10; Proposition 12.1; every claim applying to “all forms.”

### AV-002 — Representation transport and covariance are ill typed

- **Severity:** Blocking
- **Exact location:** Definitions 3.21–3.22, lines 126–134; A3, lines 144–145;
  Definition 8.10, lines 380–382.
- **Statement examined:** A representation morphism transports every context
  component and satisfies
  `sigma_(iota_*C)(iota_B b) = iota_W(sigma_C(b))`.
- **Defect or verification result:** Definition 3.22 transports `mu_C` but not
  the required `A_C`; it does not transport the profile-class declaration. The
  expression `(iota_W^{-1})_*` is standard for measures but is not defined for
  the finite-set and finite-multiset profile classes. `iota_W` is defined only on
  `W_C`, while `rho_C` and `sigma_C` may return an interval or any of three
  bottom symbols. The same output-type defect occurs in cross-context transport.
- **Counterexample or proof:** If `sigma_C(b)=bot_ind`, the right side of A3 is
  `iota_W(bot_ind)`, outside the domain of `iota_W`. If the profile is a finite
  multiset, no pushforward operation on multisets has been declared. Thus A3 is
  not a formula for allowed theory values.
- **Consequence:** Covariance cannot be evaluated for the complete stated
  codomain. Transported contexts need not be contexts in the sense of Definition
  3.14.
- **Required resolution:** Supply transports for every context component and
  every profile/output alternative, including explicit action on intervals and
  bottom symbols.
- **Downstream impact:** Theorem 2; Observation 3.23; Corollaries 14.2 and 16.13;
  the A3 check in Proposition 12.1.

### AV-003 — Optionality conflicts with contextual completeness

- **Severity:** Major
- **Exact location:** Definition 3.14, line 96; A2, line 142.
- **Statement examined:** `approx_C` is an optional enrichment, while any
  unsupplied component of the eight-component context makes a valuation
  `bot_und`.
- **Defect or verification result:** The candidate does not distinguish an
  intentionally absent optional component from an unsupplied required
  component. Under the literal tuple reading, an optional `approx_C` must still
  occupy a component; under the literal A2 reading, omitting it makes every such
  valuation undefined.
- **Counterexample or proof:** Take a context supplying every component except
  `approx_C`. Definition 3.14 permits that omission; A2 assigns `bot_und`. Both
  readings cannot govern the same object without an absence convention.
- **Consequence:** The domain of valid contexts and the reach of A2 are
  indeterminate.
- **Required resolution:** Declare a typed absent value or restrict A2 to
  required components.
- **Downstream impact:** Every construction that omits `approx_C`, including
  Theorem 10 as written.

### AV-004 — Profile construction and partial-function handling are incomplete

- **Severity:** Blocking
- **Exact location:** Definition 3.16, lines 103–114; Definitions 5.2–5.3,
  lines 172–176.
- **Statement examined:** A probability measure induces an element of any one of
  four profile classes, after which `rho_C` defines significance.
- **Defect or verification result:** Only the probability-coupled construction
  is defined. A probability measure does not canonically induce a finite
  multiset. Its range or support need not be a finite set, so it does not
  canonically induce the declared finite-set profile either. A pushforward is a
  finite measure, but the measure-valued and probability-coupled cases are not
  distinguished operationally. Definition 5.3 also omits the case in which
  `delta_C^b` is defined on a non-null set but not almost everywhere: the profile
  does not exist, yet none of its listed `bot_und` conditions applies.
- **Counterexample or proof:** Let `mu_C` be uniform on `[0,1]` and
  `delta_C^b(m)=m`. Its image is infinite, not a finite set or multiset. For the
  partiality gap, define the contrast only on `[0,1/2]`; it is neither nowhere
  defined nor defined almost everywhere.
- **Consequence:** Generic significance is not defined for two advertised
  profile classes and has an unclassified partial-domain branch.
- **Required resolution:** Define the profile-producing operation for each
  class and exhaustively type every partiality outcome.
- **Downstream impact:** A5; A9; Theorems 1, 5, 6, and 10; the full-signature
  consistency obligation.

### AV-005 — Several axioms are not mathematical predicates

- **Severity:** Blocking
- **Exact location:** A1–A10, especially A1, A5, A6, A9, and A10 at lines
  140–160.
- **Statement examined:** A1–A10 form an axiom system whose joint satisfiability
  is later asserted for a fragment.
- **Defect or verification result:** “Valuation of a comparison,” “available
  information,” “determined set,” “joint uncertainty,” “comparison set,” and
  “model class compatible with the evidence” are not objects or predicates in
  the signature. A5 mixes point, set, interval, and bottom outputs without a
  single typed codomain. A10 uses evidence compatibility although neither an
  evidence observation nor a compatibility relation is in the base signature.
- **Counterexample or proof:** There is no interpretation function in the
  candidate by which one can decide whether a given point is “fabricated” or a
  given set is “the determined set.” Therefore a purported model cannot be
  checked against these sentences.
- **Consequence:** Joint satisfiability and logical consequence from A1, A5, A6,
  A9, or A10 are not formally meaningful.
- **Required resolution:** Translate each axiom into predicates over declared
  carriers and functions, with one output type for each case.
- **Downstream impact:** Corollaries 3.1–3.2; Observation 4.1; Proposition 12.1;
  limitations and rejections relying on these axioms.

### AV-006 — Designation and filter contexts use an undefined structure

- **Severity:** Major
- **Exact location:** Definitions 6.1–6.3 and Theorem 2, lines 196–211.
- **Statement examined:** Contexts designate or filter relative to
  automorphisms of “the underlying structure,” and a filter cannot break a
  symmetry.
- **Defect or verification result:** No underlying structure, its carrier, or its
  automorphism group is defined. `Aut(C)` is defined using context morphisms,
  whereas Definitions 6.2–6.3 immediately switch to automorphisms of a different
  unnamed object. Theorem 2's displayed equality is a direct instance of A3 for
  `W_C`-valued outputs, not a theorem that designation is necessary.
- **Counterexample or proof:** Without a map from the unnamed underlying
  automorphisms to `Aut(C)`, a bearer orbit in Corollary 2.1 has no determined
  group action.
- **Consequence:** Designation, filter context, and “designation necessity” are
  undefined; only the conditional orbit-constancy equality survives.
- **Required resolution:** Fix the underlying object and group action, and state
  the relation between its automorphisms and context morphisms.
- **Downstream impact:** Corollaries 2.1–2.2; Definition 11.1; Limitations 14.8;
  Rejection 16.7.

### AV-007 — Order reversal has a valid numerical core but incomplete contexts

- **Severity:** Major
- **Exact location:** Theorem 1 and Corollaries 1.1–1.2, lines 180–190.
- **Statement examined:** Two contexts differing only in their outcome maps
  reverse the order of two bearers, and A4 is satisfiable.
- **Defect or verification result:** The numerical calculation `2>1` and `1<2`
  is correct. The proof does not supply the `A_C` component, a profile-class
  component in the tuple, or an absence value for optional `approx_C`.
  Corollary 1.1 is valid only for the constructed bearer set and context family;
  it does not prove that every theory instance has an order reversal.
  Corollary 1.2 exhibits a null contrast for an unspecified bearer assignment,
  not a complete model satisfying the universal A4 sentence.
- **Counterexample or proof:** A theory instance with `B={b_1,b_2}` and one
  `W_1` context having zero contrast for both bearers satisfies A4 and admits the
  constant context-free ordering. Theorem 1 shows that the framework permits
  reversal, not that every context family reverses.
- **Consequence:** Theorem 1 is a narrowed construction, not a complete
  all-context limitation.
- **Required resolution:** Complete the constructed contexts and restrict each
  corollary to the quantifiers proved.
- **Downstream impact:** Limitation 14.1; Rejection 16.1; the summary table at
  lines 515–530.

### AV-008 — Factorisation requires a precise quotient sigma-algebra and domain

- **Severity:** Major
- **Exact location:** Theorem 3 and Corollary 3.3, lines 223–243.
- **Statement examined:** A measurable function factors measurably through `r`
  iff it is fibre-constant.
- **Defect or verification result:** The set-theoretic factorisation on
  `r(M)` is correct. “The sigma-algebra induced by `r`” is not defined as a
  sigma-algebra on `R` or only on `r(M)`. The proof defines `h` only on `r(M)`,
  while the conclusion conventionally requires `h:R->W`. Its displayed
  measurability calculation is valid under the final/quotient sigma-algebra for
  saturated sets, but that convention is unstated. Corollary 3.3 applies the
  theorem with codomain `Y_C`, although Theorem 3 restricts `W` to a class in
  Definition 3.12 and an outcome space need not be such a codomain.
- **Counterexample or proof:** Under the final sigma-algebra
  `{A subset R : r^{-1}(A) is measurable}`, the core theorem can be completed by
  extending `h` outside `r(M)`. The published proof neither makes that choice
  nor states that convention.
- **Consequence:** Theorem 3 is valid only after narrowing its measurable-space
  semantics; Corollary 3.3 does not literally follow from the written theorem.
- **Required resolution:** Define the induced sigma-algebra, the domain of `h`,
  and a theorem codomain broad enough for Corollary 3.3.
- **Downstream impact:** Corollaries 3.1–3.3; Definitions 7.4–7.7; identification
  claims.

### AV-009 — Measurable factorisation does not imply computability

- **Severity:** Blocking
- **Exact location:** Corollary 3.1, lines 257–259.
- **Statement examined:** The contrast is computable from the representation iff
  `r` is sufficient.
- **Defect or verification result:** Theorem 3 proves existence of a measurable
  factor, not an algorithm. Computability is neither defined nor implied by
  measurability.
- **Counterexample or proof:** Let `M=R=N` with discrete sigma-algebras,
  `r=id`, and let `A subset N` be non-computable. Take a total contrast
  `delta_C^b(n)=1_A(n)`. It is measurable and constant on every singleton fibre,
  so `r` is sufficient and the factor exists. No algorithm computes the
  contrast from `r(n)`.
- **Consequence:** Corollary 3.1 is false under the ordinary meaning of
  computability and commits a category error.
- **Required resolution:** Withdraw the computability conclusion or supply an
  effective presentation and algorithmic hypotheses.
- **Downstream impact:** Open Question 15.2 and any claim that sufficiency is a
  computational criterion.

### AV-010 — Forced abstention theorem is false for partial contrasts

- **Severity:** Blocking
- **Exact location:** Definition 7.4 and Corollary 3.2, lines 255 and 261–269.
- **Statement examined:** If `r` is not sufficient, some nonempty fibre has at
  least two contrast values.
- **Defect or verification result:** Definition 7.4 can fail because the contrast
  is not defined everywhere, not only because it is non-constant on a fibre.
  The proof silently discards that branch.
- **Counterexample or proof:** Let `M={0,1}`, `r=id`, `Y={0,1}`, `M_C=id`, and
  `tau=id`. Define `delta_C` only at `(1,1)`, with value `0`. Then
  `delta_C^b` is not defined everywhere, so `r` is not sufficient. Each fibre is
  a singleton. The identified output on the fibre over `1` is `{0}` and that on
  the fibre over `0` is `bot_und`; no fibre has two values. A measurable total
  factor can also agree with the contrast wherever the latter is defined.
- **Consequence:** The stated corollary, its proof, and the assertion that
  abstention follows in every non-sufficient case are false.
- **Required resolution:** Split failure of totality from failure of
  fibre-constancy and state conclusions separately.
- **Downstream impact:** Observation 7.6; Limitation 14.6; Rejection 16.11.

### AV-011 — Quotient descent is not a well-defined theorem for a partial evaluator

- **Severity:** Blocking
- **Exact location:** Theorem 4, lines 279–286.
- **Statement examined:** A8 yields a unique evaluator on the full quotient
  square wherever the partial raw evaluator is defined.
- **Defect or verification result:** The theorem does not say whether
  `bar_delta_C` is total or partial, and supplies no quotient domain. If total,
  uniqueness fails on quotient pairs with no defined representative. If partial
  and “descent” means equality of partial maps after quotient projection, A8 does
  not require the raw domain to be saturated under equivalence.
- **Counterexample or proof:** With equality as `approx_C`, `Y={0,1}`, and
  `delta_C` defined only at `(0,0)` with value `0`, A8 holds. Any total quotient
  map may take arbitrary values on the other three quotient pairs, so it is not
  unique. With universal equivalence and the same one-point domain, a quotient
  partial map defined on the sole class pair pulls back to all of `Y^2`, not to
  the raw partial domain.
- **Consequence:** Theorem 4 is false under the total reading and incomplete
  under the partial reading.
- **Required resolution:** Declare a partial quotient domain and the required
  domain-saturation condition, or weaken the claimed descent relation.
- **Downstream impact:** Observation 7.9; the theorem summary at line 520;
  quotient-level claims.

### AV-012 — Posterior and kernel hypotheses do not support the information theorem

- **Severity:** Major
- **Exact location:** Definition 3.20, line 122; Definition 8.4 and Theorem
  5(iii), lines 309–320; OB-3, line 560.
- **Statement examined:** A Markov kernel induces a random posterior whose
  barycentre is `mu_C`, permitting Jensen's inequality for Bayes risk.
- **Defect or verification result:** A kernel and prior determine an evidence
  marginal, but a regular conditional posterior need not exist on arbitrary
  measurable spaces. “The induced posterior family” has no type or measurability
  condition. Integrability alone does not supply the barycentre identity or
  measurability of the random risk. The concavity argument itself is correct once
  a measurable regular posterior with the disintegration identity is assumed.
- **Counterexample or proof:** The candidate ranges over arbitrary measurable
  model and evidence spaces, a class on which regular conditional probabilities
  are not guaranteed. Definition 3.20 may be read as supplying one, but then the
  properties used at line 320 still have to be axioms of that supplied object.
- **Consequence:** Theorem 5(iii) is a narrowed theorem, not established over the
  declared base signature.
- **Required resolution:** State posterior existence, regularity, barycentre,
  and risk measurability hypotheses explicitly.
- **Downstream impact:** Information significance; Theorem 6(ii)–(iii); the
  evidence-kernel portion of OB-1.

### AV-013 — Pairwise non-equivalence constructions omit decisive parameters

- **Severity:** Major
- **Exact location:** Theorem 6, lines 322–341.
- **Statement examined:** Three complete contexts make each pair of significance
  forms order two bearers differently.
- **Defect or verification result:** The constructions do not declare the
  reduction `rho_C` used for effect significance, despite Definition 8.1 making
  it primitive. They do not declare `epsilon` for decision significance. The
  exact values `1` in parts (i) and (ii) use `epsilon=0`; for `epsilon>=1`, the
  claimed strict decision ordering in part (i) disappears. In part (iii), the
  assertion that the effect of replacing a normal variable by its mean is less
  than `1` for small variance depends on the unspecified location functional.
  The examples also omit the complete context tuple.
- **Counterexample or proof:** A reduction that returns the atom for a Dirac
  profile and returns `2` on the half-normal profile is compatible with the
  undefined term “location functional” and lies within that profile's support.
  It gives effect `2`, not less than `1`, in part (iii). For part (i), the
  `epsilon`-optimal actions after a unit shift include `0` when `epsilon>=1`, so
  the decision significance becomes `0` rather than the claimed `1`.
- **Consequence:** The theorem's existential idea is plausible with extra
  choices, but the published proof does not instantiate the complete signature
  or prove its displayed values. Corollary 6.1 is additionally dependent on an
  undefined notion of a latent quantity and on order-preserving, rather than
  arbitrary, monotonic measurement maps.
- **Required resolution:** State complete contexts, a specific reduction, a
  specific `epsilon`, and a formal common-latent-order hypothesis.
- **Downstream impact:** Corollaries 6.1–6.2; Limitation/Rejection 16.5; Theorem
  summary line 522.

### AV-014 — Additive context-free scalar theorem is false

- **Severity:** Blocking
- **Exact location:** Theorem 7, lines 347–354.
- **Statement examined:** A4 forces `S` to be zero for a decomposition over a
  “family considered.”
- **Defect or verification result:** A4 supplies a null context in the global
  set `C`. The decomposition is required only on the family considered. The
  proof assumes without hypothesis that the A4 witness lies in that family.
- **Counterexample or proof:** Let `B={b}` and let the global context set contain
  `C_0,C_1`, both with codomain `R_{>=0}`. Let the family considered be
  `{C_1}`. Put `sigma_C0(b)=0`, satisfying A4; put `S(b)=1`, `beta=1`,
  `g_C1(b)=0`, and `sigma_C1(b)=1`, satisfying every family decomposition
  hypothesis. The conclusion `S(b)=0` is false.
- **Consequence:** Theorem 7 is false as written. The theory has not proved its
  claimed prohibition on an additive context-free component.
- **Required resolution:** Require the decomposition on every possible A4 null
  context for each bearer, or withdraw the conclusion.
- **Downstream impact:** Observation 7.1'; Limitation 14.2; Rejections 16.2 and
  16.17; theorem summary line 523.

### AV-015 — Mutual-information theorem is valid, but its epistemic corollary is false

- **Severity:** Major
- **Exact location:** Theorem 8 and Corollary 8.1, lines 356–363.
- **Statement examined:** If `S=f(R)`, then `S` adds no conditional mutual
  information, so a derived quantity cannot be justified epistemically.
- **Defect or verification result:** The two mutual-information identities are
  correct under the stated existence assumptions. The corollary does not
  follow. Conditional redundancy given access to `R` is not absence of
  information for an observer who receives only `S`, and it is not absence of
  epistemic justification.
- **Counterexample or proof:** Let `Z=R` be a non-degenerate Bernoulli variable
  and `S=R`. Then `I(Z;S|R)=0`, as the theorem says, while
  `I(Z;S)=H(Z)>0`. The derived summary is informative to an observer without
  `R`.
- **Consequence:** Theorem 8 is verified as an information identity; Corollary
  8.1 and the claimed “no epistemic role” are not mathematical consequences.
- **Required resolution:** Restrict the conclusion to incremental information
  conditional on simultaneous access to `R`.
- **Downstream impact:** Limitation 14.3; Rejection 16.3; the epistemic clause of
  Rejection 16.17.

### AV-016 — Normalisation theorem is valid, but both corollaries overreach

- **Severity:** Major
- **Exact location:** Theorem 9 and Corollaries 9.1–9.2, lines 367–382.
- **Statement examined:** Changing the arena changes normalized values, so
  cross-arena equality carries no information and calibration against a
  dimensioned quantity is impossible.
- **Defect or verification result:** Theorem 9's inequality and order-preservation
  calculation are correct. It does not imply incomparability or absence of
  information. Dimensionlessness prevents direct dimensional equality or
  addition, not calibration by an explicitly dimensioned scale. A7 itself
  permits comparison through a declared transport.
- **Counterexample or proof:** Let `A={a}`, `A'={a,b}`, `phi(a)=1`, and
  `phi(b)=2`. Then `nu^A(a)=nu^A'(b)=1`; that equality tells us both elements are
  arena maxima. If each denominator is known, the original values are
  recoverable. Also, for a declared dimensioned constant `D`, the calibration
  `x -> D x` maps a dimensionless normalized value to a dimensioned value.
- **Consequence:** Theorem 9 is verified, while Corollaries 9.1–9.2 and their
  rejection claims are unsupported.
- **Required resolution:** Limit the corollaries to denominator dependence and
  direct dimensionally homogeneous operations.
- **Downstream impact:** Rejection 16.4; Limitation 14.7; cross-context claims.

### AV-017 — Universal-encodability proof assumes a measurable group operation

- **Severity:** Blocking
- **Exact location:** Theorem 10, lines 392–397.
- **Statement examined:** For any measurable `W` in class `W_2` with measurable
  singletons and any function `f:B->W`, the displayed context realizes `f`.
- **Defect or verification result:** A class `W_2` object is an ordered abelian
  group, but Definition 3.12 does not make addition or subtraction measurable.
  Measurable singletons do not imply measurable subtraction. Therefore the
  proof's evaluator `delta(y,y')=y'-y` need not be measurable. Constant
  operations are measurable on every measurable domain, so that part of the
  proof is valid; the singleton hypothesis is not what makes them measurable.
- **Counterexample or proof:** Give `R` its usual ordered abelian-group structure
  and the countable–cocountable sigma-algebra. Every singleton is measurable. In
  the product sigma-algebra the diagonal is not measurable: any product-
  measurable set depends on countably many countable/cocountable generators,
  which cannot separate all uncountably many diagonal sections. Since the
  inverse image of `{0}` under subtraction is the diagonal, subtraction is not
  measurable. The context constructed in the proof violates Definition 3.14.
- **Consequence:** The published load-bearing proof is invalid under its exact
  hypotheses.
- **Required resolution:** Either assume a measurable group structure or use a
  separately justified measurable contrast.
- **Downstream impact:** Corollaries 10.1–10.2; Observations 1.2 and 10.4;
  Limitation 14.9; Rejection 16.14.

### AV-018 — Universal encodability is restricted, and the no-empirical-content conclusion does not follow

- **Severity:** Blocking
- **Exact location:** Theorem 10's “Applies to” line 395; Corollaries 10.1–10.2
  and Observations 10.3–10.4, lines 399–407; theorem summary line 526.
- **Statement examined:** Every value assignment is realized in all forms, so
  the unrestricted framework forbids no observation.
- **Defect or verification result:** The theorem quantifies only assignments into
  a `W_2` ordered abelian group and builds only a generic probability-coupled
  contrast valuation. It does not construct a qualitative, interval,
  distributional, effect, decision, information, composition, or diffusion
  form. In particular, effect, decision, and information significance are
  constrained to be non-negative under Theorem 5's hypotheses. The theorem also
  concerns a single context assignment, not joint observations constrained by
  A3, A4, or A7.
- **Counterexample or proof:** An assignment of `-1` as effect significance is
  excluded by Definition 8.1. A joint assignment that violates covariance under
  a representation morphism is excluded by A3. Neither is realized by Theorem
  10. Conversely, the narrow `W_2` existence conclusion has an independent
  set-theoretic realization using the measurable projection
  `delta(y,y')=y'`; thus the exact `W_2` conclusion need not be false even though
  the published proof and all-forms label fail.
- **Consequence:** “No empirical content whatever” is not proved for the full
  framework. Corollary 10.2's assertion that content can arise only by
  constraining four named components is also not exhaustive; restrictions on
  codomains, profiles, priors, context relations, or morphisms can exclude
  assignments.
- **Required resolution:** Restrict the encodability and empirical-content
  conclusions to the exact generic `W_2`, single-context assignment class proved.
- **Downstream impact:** The candidate's principal epistemic claim, its strongest
  limitation, and Rejections 16.14 and 16.16.

### AV-019 — Composition has no defined carrier or endpoints

- **Severity:** Blocking
- **Exact location:** Definitions 10.1–10.6, lines 411–423.
- **Statement examined:** Relation instances form a carrier `E`, compose on a
  compatibility domain, and form paths with matching endpoints.
- **Defect or verification result:** `E` is never defined. A relation instance
  contains only a type and signature, so it has no source or target endpoint to
  match. `kappa` determines the domain of a partial operation but not its output,
  so `odot` is not derived from `kappa`. The treatment of an empty path is not
  stated. The diffusion product is total only after `E`, paths, and finite
  weights are defined.
- **Counterexample or proof:** For a fixed nonempty compatibility relation there
  are generally many partial operations with the same domain and different
  outputs. Hence Definition 10.3 cannot be derived from Definition 10.2.
- **Consequence:** Paths and every theorem in section 10 lack a complete formal
  signature.
- **Required resolution:** Define `E`, endpoint maps, the primitive status and
  output law of composition, and empty-path semantics.
- **Downstream impact:** Theorems 11–13; Corollaries 12.1–12.3; recognisability;
  OB-1.

### AV-020 — Non-associativity proof operates on types, not relation instances

- **Severity:** Blocking
- **Exact location:** Theorem 12 and Corollaries 12.1–12.3, lines 432–445.
- **Statement examined:** A constructed instance-level partial composition is
  non-associative, every path requires bracketing, and licensed paths cannot form
  a substructure.
- **Defect or verification result:** The proof supplies a table on the type set
  `T`, then assumes instance compositions exist and have the table's output type.
  It gives no instances representing the intermediate results and no
  instance-level operation. The conclusion is existential, but its hypotheses
  are the circular phrase “a composition table as constructed.” Corollary 12.2
  changes “there exists a path with bracketing-dependent definedness” into the
  universal claim that a path does not determine its composite. “Substructure”
  and “licensed path” are not defined, so Corollary 12.3 cannot follow.
- **Counterexample or proof:** In any associative partial operation, and for any
  one-edge path even in a non-associative operation, the path does determine its
  composite. Theorem 12 at most supplies one counterexample path after a valid
  instance operation is constructed.
- **Consequence:** Theorem 12 is not proved; Corollaries 12.2–12.3 are false or
  undefined as written.
- **Required resolution:** Construct the operation on `E` and restrict the
  corollaries to the exhibited path and a formally defined path structure.
- **Downstream impact:** Limitation 14.5; Rejection 16.9; theorem summary line
  528.

### AV-021 — Semantic-separation example is underconstructed

- **Severity:** Major
- **Exact location:** Theorem 13 and Observations 13.1–13.2, lines 447–456.
- **Statement examined:** Diffusion order and compositional licensure can order
  two sources differently.
- **Defect or verification result:** The numerical products `1` and `1/100` are
  correct. The proof uses source and target endpoints absent from Definition
  10.1, assumes without a graph definition that exactly two paths exist, and
  does not address convergence of the general sums over paths. Membership in
  `kappa` makes a pair part of the domain but the output instance remains
  unspecified by the section's signature.
- **Counterexample or proof:** After adding four directed instances and choosing
  a partial operation output, the finite example can witness independence. Those
  data are not present in the exact theory.
- **Consequence:** The semantic-separation idea is not a theorem of the stated
  signature, although the finite arithmetic does not contain a contradiction.
- **Required resolution:** Supply the graph/path and partial-operation data and
  state finiteness or summability for path sums.
- **Downstream impact:** Theorem summary line 529; Observations 13.1–13.2;
  Rejection 16.10.

### AV-022 — Recognisability and prior-art assertions are unsupported and partly false

- **Severity:** Blocking
- **Exact location:** Observations 10.7–10.9, lines 458–467; Open Question 15.6,
  line 576.
- **Statement examined:** Licensed paths are a guarded register automaton on
  `U x Q x S`; finite `S` makes the product finite-state with decidable
  recognition and exactly `|U||Q||S|` states; all such machinery is established
  prior art and has no unexpressed invariant.
- **Defect or verification result:** `U`, `Q`, registers, guards, transition
  semantics, and the mapping from `kappa` to an automaton are undefined. No
  finiteness assumptions are placed on `U` or `Q`, so finite `S` does not imply a
  finite product. Decidability requires an effective finite presentation of
  transitions and guards, not merely a finite mathematical carrier. The exact
  state count is at most a raw product count before reachability minimisation,
  not necessarily equal. Arbitrary `kappa` can encode a non-computable
  membership relation. Finally, the universal statement that no invariant lies
  outside every existing typed, temporal, or dimensional formalism has neither
  a quantified comparison class nor a proof or citation in the candidate.
- **Counterexample or proof:** Let `U` be infinite and `S` a singleton. Then
  `U x Q x S` is infinite even for finite nonempty `Q`. Alternatively, let
  admissibility encode a non-computable subset of a countable instance carrier;
  bounded register content alone supplies no decision algorithm.
- **Consequence:** Recognisability and the negatively closed prior-art question
  are not verified. The narrower declaration “no novelty is claimed” is honest
  and does not require proving universal subsumption.
- **Required resolution:** Supply a formal automaton reduction with finiteness
  and effectiveness hypotheses, and withdraw or formally delimit the universal
  prior-art assertion.
- **Downstream impact:** Limitation 14.10; Theorem/observation summary; Rejection
  16.18 only insofar as it asserts more than non-claiming novelty.

### AV-023 — Structural valuation is not context indexed and its theorem is tautological

- **Severity:** Major
- **Exact location:** Definitions 11.1–11.2, Theorem 14, and Corollaries
  14.1–14.2, lines 471–492.
- **Statement examined:** A structural valuation is invariant under every
  automorphism and therefore constant on orbits; artefact morphisms leave
  significance unchanged.
- **Defect or verification result:** `varphi` has no declared codomain and no
  fixed context, although automorphisms are defined as `Aut(C)`. “Every
  automorphism” can therefore range over incompatible context groups. Once a
  fixed action is supplied, Theorem 14 is exactly Definition 11.1 restated and
  is valid as a definitional lemma. Corollary 14.1 proves non-structurality but
  not the additional causal statement that a value “depends on data outside” an
  invariance class. An artefact morphism's claimed identity action is also not
  reconciled with its non-identity relabelling of carriers.
- **Counterexample or proof:** A deliberately arbitrary, label-dependent
  function can fail orbit constancy without depending on any declared data at
  all; the second clause of Corollary 14.1 is not a logical consequence.
- **Consequence:** Orbit constancy is a tautology after typing, not an independent
  all-forms theorem. Artefact independence remains dependent on ill-typed A3.
- **Required resolution:** Fix the context, group action, and valuation codomain,
  and remove consequences not contained in invariance.
- **Downstream impact:** Corollary 14.2; Observations 11.3–11.4; Rejection 16.13.

### AV-024 — The named consistency witness does not instantiate its claimed fragment

- **Severity:** Blocking
- **Exact location:** Proposition 12.1 and its proof, lines 496–509.
- **Statement examined:** The displayed model supplies all eight context
  components and satisfies A1–A10 in the deterministic–decision fragment.
- **Defect or verification result:** Each context supplies `mu_C` but no
  admissibility object `A_C`, and Definition 3.14 gives no rule making those
  interchangeable. Thus the assertion that all eight components are supplied is
  false. The outcome sigma-algebra is not explicitly supplied. A3 is checked for
  the identity and then asserted for all relabellings “by Definition 3.22”; this
  is not a satisfaction check, because the declared context set
  `{C_1,C_2,C_0}` is not shown closed under transports and Definition 3.22 is
  itself incomplete and ill typed. The identity case is vacuous. The witness
  supplies a decision problem only on `C_1` but does not instantiate decision
  significance or a `W_2`-valued context.
- **Counterexample or proof:** A3 quantifies over every representation morphism.
  Checking only the identity verifies no nontrivial covariance. Defining a new
  context by transport can make covariance tautological, but that new context is
  not shown to be an element of the witness's `C`.
- **Consequence:** Proposition 12.1 does not prove fragment consistency. A3 is
  only vacuously checked for identity and definitionally asserted for objects not
  shown in the model.
- **Required resolution:** Supply every tuple component, a precise universe of
  morphisms and transported contexts, and a satisfaction argument for each
  formal axiom.
- **Downstream impact:** The only consistency result in the candidate; OB-1;
  freeze eligibility.

### AV-025 — A4 is satisfied in the witness, but full-signature consistency is not presently a proposition

- **Severity:** Major
- **Exact location:** A4, line 147; witness contexts at lines 501–507;
  Observation 12.2 and OB-1, lines 509 and 556.
- **Statement examined:** `C_0` supplies contextual nullity for every bearer;
  consistency beyond the named fragment remains open; a broader witness might
  be constructed without changing the theory.
- **Defect or verification result:** Under the natural reading of the displayed
  data, A4 is genuinely satisfied for both `b_1` and `b_2`: `C_0` leaves the
  `x` outcome unchanged and the absolute contrast is zero. A8 is also genuinely
  satisfied by equality, and A10 by the identity representation map. A5 and A9
  are only informally/vacuously checked because their predicates are undefined.
  A6 is vacuous in the absence of competing uncertainty objects. A broader
  formal witness cannot be certified without assigning meanings to `A_C`,
  profile induction, transported bottoms, `E`, endpoints, and the automaton
  objects. Assigning those meanings would add structure not fixed by the exact
  candidate.
- **Counterexample or proof:** Trivial singleton examples can be sketched for
  most optional codomain and path cases, showing no evident semantic
  contradiction. They are not models of the exact text because the satisfaction
  relation for the undefined objects and prose axioms is absent.
- **Consequence:** Full consistency is neither proved nor disproved. It is
  presently unaskable as a model-theoretic property of the exact document.
- **Required resolution:** Complete the signature and formalize the axioms before
  OB-1 can be discharged by any broader witness.
- **Downstream impact:** Consistency assessment and final freeze recommendation.

### AV-026 — Internal references, theorem summaries, and notation do not match the candidate

- **Severity:** Minor
- **Exact location:** Lines 10, 22, 66, 456, 515–530, and 584–622.
- **Statement examined:** Internal section references and the proven-statements
  table accurately identify the theory's dependencies and results.
- **Defect or verification result:** The document ends at section 16, but lines
  10, 22, and 456 refer to nonexistent section 18. Line 66 sends relation-instance
  composition to section 11 although it is in section 10. The theorem table
  labels Theorems 3, 4, 6, 7, 10, and 12 as proved and overstates Theorem 10 as
  applying to all forms. `E`, `I(W_C)`, `U`, `Q`, and `S` remain undefined.
  Corollaries under Theorem 3 are numbered 3.3, 3.1, then 3.2; this is not a
  logical error but obscures dependency order. A delimiter scan found no line
  with an odd number of dollar delimiters; the principal notation failures are
  semantic/type failures rather than unbalanced TeX.
- **Counterexample or proof:** There is no section 18 or definition of the named
  symbols in the 628-line source blob.
- **Consequence:** The dependency record and internal navigation are unreliable.
- **Required resolution:** Correct the references and summary only after theorem
  status is resolved; define every symbol used in a formal claim.
- **Downstream impact:** Novelty boundary, rejected-formulation references, and
  the freeze inventory of proven results.

### AV-027 — Multiple limitations and rejected formulations do not follow from their cited results

- **Severity:** Blocking
- **Exact location:** Limitations 14.1–14.10, lines 534–554; Rejections
  16.1–16.19, lines 584–624.
- **Statement examined:** Each limitation and rejection is entailed by the named
  theorem, corollary, or axiom.
- **Defect or verification result:** The dependency audit below identifies the
  exact outcomes. In particular, Limitation 14.2 depends on false Theorem 7;
  Limitation 14.3 overstates Theorem 8; Limitation 14.9 depends on the
  overgeneralized universal-encodability corollary; Rejection 16.7 is not implied
  by symmetry and conflicts with the context's own admissibility-restriction
  component; Rejection 16.8 omits Theorem 11's hypothesis that compatibility is
  not type-level; and Rejection 16.12 unqualifiedly rejects cross-context
  comparison even though A7 and Definition 8.10 expressly permit it under a
  declared transport.
- **Counterexample or proof:** AV-014 supplies a model with a nonzero additive
  scalar satisfying the exact Theorem 7 hypotheses. AV-015 gives a derived
  summary with positive mutual information to an observer lacking `R`. A
  restriction can designate by selecting an asymmetric admissible subset, so
  Theorem 2 does not defeat every restriction-based context. If `kappa` is a
  function of types, exact type-level licensing is sound and complete, contrary
  to unqualified Rejection 16.8.
- **Consequence:** The negative conclusions described as load-bearing are not a
  valid dependency closure of the proved elementary results.
- **Required resolution:** Retain only limitations and rejections whose exact
  quantifiers follow from verified premises; withdraw the rest until their
  dependencies are proved.
- **Downstream impact:** Sections 1, 13, 14, 16, and the final theory status.

### AV-028 — Status, empirical boundary, and non-novelty disclaimer are accurately limited

- **Severity:** Observation
- **Exact location:** Document control and provenance, lines 3–14; scope lines
  28–36; OB-2 and OB-3, lines 558–560; final line 628.
- **Statement examined:** The document is a candidate, not frozen, not
  empirically validated, and makes no novelty claim; measurability and
  integrability gaps remain open.
- **Defect or verification result:** These status and empirical disclaimers are
  accurate and consistent with the repository research controls. OB-2 correctly
  records that measurability of the pointwise contrast is assumed rather than
  derived. OB-3 correctly records that integrability conditions are absent.
  These honest limitations do not cure the formal defects above.
- **Counterexample or proof:** The canonical controls independently record
  `EH-0` and exclude this candidate from their Version 1 freeze.
- **Consequence:** No unsupported empirical-validation claim or affirmative
  novelty claim was found.
- **Required resolution:** None for the disclaimer itself.
- **Downstream impact:** The candidate must retain candidate status; the
  mathematical disposition does not alter empirical controls.

## 4. Definition verification inventory

| Definition(s) | Result |
|---|---|
| 3.1–3.8 | Basic carriers, measurable operations, and the partial bearer assignment are coherent. Definition 3.6 is usable only in contexts that supply `r`. |
| 3.11 | Not formal: “acts on the specification of a model only” supplies no subtype predicate beyond the already declared endomap. |
| 3.12 | Algebraic distinctions are intelligible, but measurable structures are absent for general `W_0`–`W_3`; interval structure over a preorder is not uniquely specified. |
| 3.14–3.16 | Failed signature completeness; see AV-001 and AV-003. |
| 3.18 | The three bottom symbols are mutually distinguished, but transports and mixed output codomains are not defined. |
| 3.19 | Well typed for losses under `mu_C`; integrability under pushed or posterior measures is additional. |
| 3.20 | Incomplete posterior object; see AV-012. |
| 3.21–3.22 | Failed transport completeness and typing; see AV-002. |
| 5.1 | Well typed when its prerequisites and partial evaluator domain are supplied. |
| 5.2–5.3 | Incomplete outside probability-coupled profiles and non-exhaustive for partial domains; see AV-004. |
| 6.1–6.3 | `Aut(C)` is interpretable after transport is repaired; designation/filter definitions are not, because the underlying structure is absent. |
| 7.1–7.2 | Verified when optional `r` is supplied. |
| 7.4 | A precise sufficient condition, but its totality branch is mishandled by Corollary 3.2. |
| 7.5 | Set construction is clear on nonempty fibres; its overall codomain mixing sets and bottom symbols is not declared. |
| 7.7 | Items (i)–(iii) are intelligible; `ker delta_C^b` for a partial map requires a domain/undefinedness convention. No minimality theorem is claimed. |
| 8.1 | Requires a definition of “location functional.” |
| 8.2 | Epsilon-optimal sets are nonempty for positive `epsilon` when the risk infimum is finite; the zero case correctly requires attainment. |
| 8.4 | Depends on the missing posterior regularity in AV-012. |
| 8.5 | Verified for finite nonempty `A`; nonemptiness follows from the declared map to positive reals only if a function with that domain exists, but should be explicit. |
| 8.10 | Verified only for values actually in `W_C`; interval and bottom outputs are outside its declared domain. |
| 9.1 | Procedural independence is an informal methodological predicate, not a mathematical definition over the signature. |
| 10.1–10.6 | Failed as a complete composition signature; see AV-019. |
| 11.1–11.2 | Require a fixed context, group action, valuation type, and coherent identity-on-components convention; see AV-023. |

## 5. Axiom verification inventory

| Axiom | Result |
|---|---|
| A1 | Intelligible design principle, not a formal predicate because “valuation of a comparison” is undefined. |
| A2 | Conflicts with optional components and depends on the incomplete tuple; AV-003. |
| A3 | Ill typed for allowed outputs and incomplete transports; AV-002. |
| A4 | A precise existential schema once `sigma_C` is typed. The displayed `C_0` genuinely gives zero for both witness bearers. |
| A5 | Not formal and mixes output types; AV-005. |
| A6 | Not formal; no joint carrier, marginal operator, or conditional operator is declared. |
| A7 | The within-context codomain restriction is precise. The comparison rule is a stipulation, with the explicit transport exception in Definition 8.10. |
| A8 | Equality of values on pairs of defined representatives is precise under the natural two-pair reading; it does not by itself saturate the domain of a partial evaluator. |
| A9 | Not formal because comparison sets and quantified valuation operators are not declared. |
| A10 | The empty-fibre branch in Definition 7.5 is clear, but “compatible with evidence” is not defined in the base signature. |

No complete formal model was shown to satisfy all ten exact axioms because five
are not satisfaction-testable and A3 is not well typed.

## 6. Theorem and proof inventory

| Result | Verification | Proper logical status under the exact candidate |
|---|---|---|
| Theorem 1 | Numerical construction verified; context signature incomplete and corollary quantifiers overstate it | Narrowed theorem |
| Theorem 2 | Equality follows immediately from A3 for typed `W_C` values | Lemma/corollary of A3, not a designation theorem |
| Theorem 3 | Set-theoretic core verified under a final/quotient sigma-algebra and an extension of `h`; exact statement under-specified | Narrowed theorem |
| Theorem 4 | Total reading false; partial reading lacks its domain and saturation semantics | Failed theorem |
| Theorem 5(i) | Valid if “preserving the support bound” is formally defined | Narrowed theorem |
| Theorem 5(ii) | Verified, including positive-epsilon non-attainment handling | Verified theorem |
| Theorem 5(iii) | Concavity/Jensen argument valid only with a measurable regular posterior and barycentre identity | Narrowed theorem |
| Theorem 6 | Examples omit `rho_C`, `epsilon`, and complete contexts; displayed values are not proved | Unresolved theorem/proof failure |
| Theorem 7 | Explicit countermodel in AV-014 | Failed theorem |
| Theorem 8 | Both mutual-information identities verified | Verified lemma; epistemic corollary failed |
| Theorem 9 | Inequality and within-arena order preservation verified | Verified theorem; corollaries failed |
| Theorem 10 | Published proof invalid; narrow `W_2` existence conclusion independently holds with a measurable projection; all-forms label and corollaries fail | Narrowed theorem with invalid published proof |
| Theorem 11 | Binary-predicate dichotomy is logically correct after `E` and the type projection are defined | Narrowed elementary lemma |
| Theorem 12 | Type table does not construct the claimed instance operation | Unresolved theorem/proof failure |
| Theorem 13 | Arithmetic core is correct; graph, endpoints, operation, and sums are not supplied | Unresolved theorem/proof failure |
| Theorem 14 | Orbit constancy is exactly the definition of structural valuation once typed | Definitional lemma |
| Proposition 12.1 | Does not supply all context components or a non-vacuous A3 satisfaction argument | Failed consistency proof |

### Verified theorems

- Theorem 5(ii), on its stated finite-risk and nonempty-selection conditions.
- Theorem 8's two mutual-information identities.
- Theorem 9's arena-dependence inequality and within-arena order statement.
- The elementary logical core of Theorem 11, conditional on a completed
  instance/type signature.

### Failed theorems

- Theorem 4, as a unique total quotient evaluator and as an unspecified partial
  descent.
- Theorem 7, by the countermodel in AV-014.
- Proposition 12.1, as a proof that its displayed object is a complete model of
  the named fragment.

### Narrowed or unresolved theorems

- Theorems 1, 2, 3, 5(i), 5(iii), 6, 10, 11, 12, 13, and 14 require the
  restrictions stated in the inventory and findings above.

## 7. Corollary, observation, limitation, and rejection dependency audit

### Corollaries

| Corollary | Result |
|---|---|
| 1.1 | Valid only for the two contexts exhibited by Theorem 1; not universal over every theory instance. |
| 1.2 | A null construction is plausible but not a complete A4 model proof. |
| 2.1–2.2 | Conditional orbit statement is valid only after designation and the group action are defined. |
| 3.3 | Set-theoretic statement is valid on the image with induced-domain measurability, but it is not a literal instance of Theorem 3's codomain hypothesis. |
| 3.1 | False as a computability statement; AV-009. |
| 3.2 | False because non-sufficiency includes lack of totality; AV-010. |
| 6.1 | Not established without a formal common latent order and a complete Theorem 6 construction. |
| 6.2 | Reasonable ambiguity observation, not a consequence that identifies all uses of the word. |
| 8.1 | False as an epistemic conclusion; AV-015. |
| 9.1–9.2 | Do not follow; AV-016. |
| 10.1–10.2 | Stronger than Theorem 10; AV-018. |
| 12.1 | True of a defined partial binary operation; the candidate has not defined one. |
| 12.2–12.3 | Universal/undefined overreach; AV-020. |
| 14.1 | First clause follows from orbit invariance; “depends on data outside” does not. |
| 14.2 | Conditional instance of A3 only after transport typing is repaired. |

### Observations

The following observations are verified within their stated limited sense:
3.9, 3.13, 3.17, 5.4, 6.4, 7.8, 8.0.1, 8.3, 10.3, 11.3, and the scope
disclaimer in 12.2. Observation 3.10 is correct except for its stale section
reference.

The following are conditional or overstate unresolved results: 1.1–1.2, 2.1–2.2,
3.23, 4.1, 7.3, 3.4, 7.6, 7.9, 7.1', 8.11, 10.4, 13.1–13.2,
10.7–10.9, and 11.4. In particular, 7.6 depends on false Corollary 3.2;
10.4 depends on the overgeneralized Corollary 10.1; and 10.7–10.8 fail the
finiteness/effectiveness checks in AV-022.

### Limitations 14.1–14.10

| Limitation | Result |
|---|---|
| 14.1 | Demonstrated for the constructed reversal family, not for every possible context family. |
| 14.2 | Unsupported because Theorem 7 is false under its exact hypotheses. |
| 14.3 | Unsupported; Theorem 8 establishes only conditional information redundancy. |
| 14.4 | The reduction is indeed primitive. The further claim that distinct reductions induce distinct orderings whenever a profile is asymmetric is false: distinct positive rescalings can induce the same ordering. |
| 14.5 | A path may fail to have an intrinsic unbracketed composite; the universal wording inherited from Corollary 12.2 is false. |
| 14.6 | Non-identification is possible, but Corollary 3.2 does not characterize every non-sufficient case. |
| 14.7 | Valid as the A7 stipulation only in the absence of a declared transport. |
| 14.8 | Exogeneity follows from absence of a selection rule, not from Theorem 2 alone; necessity is question- and orbit-conditional. |
| 14.9 | Not established for the full framework; AV-017–AV-018. |
| 14.10 | Not established until the automaton and effectiveness conditions are defined. |

### Rejections 16.1–16.19

| Rejection | Result |
|---|---|
| 16.1 | A1 stipulates non-intrinsic valuation; Theorem 1 only shows that context reversal is permitted. |
| 16.2 | Not proved because Theorem 7 is false as stated. |
| 16.3 | Valid only as “no additional mutual information conditional on `R`,” not as a general epistemic rejection. |
| 16.4 | Not implied: Theorem 9 describes arena dependence but does not make arena-relative rank mathematically invalid. |
| 16.5 | Not established by the incomplete Theorem 6 proof or undefined latent-quantity premise. |
| 16.6 | “Emerges from structure” is not a formal proposition and cannot be rejected by A2 without an attempted tuple. |
| 16.7 | Not implied. A restriction can break symmetry, and `A_C` is itself described as an admissibility restriction. |
| 16.8 | Valid only when Theorem 11's non-type-level hypothesis holds; false when compatibility is exactly type-determined. |
| 16.9 | Too strong; some paths and some operations have bracketing-independent values. |
| 16.10 | The narrow statement that non-transitivity alone does not invalidate a declared diffusion product is correct. |
| 16.11 | Depends on false Corollary 3.2 and nonformal A5. |
| 16.12 | Contradicts the express transport exception in A7 and Definition 8.10 unless read as “without a declared transport.” |
| 16.13 | Corollary 14.2 covers only artefact morphisms, not every possible encoding change. |
| 16.14 | Not established for the full framework; AV-018. |
| 16.15 | Verified as a statement about the candidate's primitives: no context-discovery construction is supplied. |
| 16.16 | The evaluator is indeed primitive, but Theorem 10 realizes value assignments, not “any evaluator whatever.” |
| 16.17 | Absence of a context-free-order primitive is verified by inspection; the claimed theorem-based prohibitions are not. |
| 16.18 | Verified only as a non-novelty disclaimer. Universal prior-art subsumption is unproved. |
| 16.19 | Verified as out of scope: the phrase is absent from the formal signature. |

## 8. Mandatory-domain coverage

| Domain | Determination |
|---:|---|
| 1. Formal signature completeness | Failed: AV-001, AV-004, AV-019. |
| 2. Type correctness | Failed: AV-002, AV-004, AV-011. |
| 3. Domain/codomain consistency | Failed for reduction, transport, partial quotient, and composition outputs. |
| 4. Partial-function handling | Failed: AV-004, AV-010, AV-011. |
| 5. Empty-set/empty-domain behaviour | Bottom symbols are distinguished, but the partially-defined-not-a.e. branch and empty path are absent. A9 is nonformal. |
| 6. Context indexing | Partial: base maps are indexed; profile class, structural valuation, and some optional structures are not consistently indexed. |
| 7. Cross-context comparison restrictions | A7 supplies a restriction and transport exception; Rejection 16.12 overstates it. |
| 8. Quotient/congruence conditions | Failed for partial descent: AV-011. |
| 9. Representation morphisms | Failed: AV-002 and AV-023. |
| 10. Measurability | Failed in Theorem 10; under-specified in Theorems 3 and 5(iii). |
| 11. Integrability | Explicitly assumed for written expectations; posterior-risk measurability/existence remains open. |
| 12. Kernel existence | Not guaranteed on arbitrary measurable spaces; AV-012. |
| 13. Optimiser/infimum assumptions | Positive-`epsilon` definition and zero-`epsilon` attainment rule are valid; Theorem 6 does not declare which case it uses. |
| 14. Identifiability | Definitions 7.4–7.5 are usable after typing; Corollaries 3.1–3.2 fail. |
| 15. Factorisation | Core valid only under the narrowed measurable quotient reading in AV-008. |
| 16. Consistency witness | Failed as a proof: AV-024–AV-025. |
| 17. Universal encodability | Published proof invalid and conclusion overgeneralized: AV-017–AV-018. |
| 18. Contextual nullity | A4 is satisfiable in the displayed `C_0` construction; Theorem 7 misuses its quantifier. |
| 19. Pairwise non-equivalence | Unresolved due omitted reduction, epsilon, and context components: AV-013. |
| 20. Additive context-free scalar | False under exact hypotheses: AV-014. |
| 21. Mutual information | Theorem 8 verified; its epistemic corollary failed. |
| 22. Normalisation | Theorem 9 verified; both corollaries failed. |
| 23. Composition definitions | Failed: AV-019. |
| 24. Non-associativity | Instance-level proof absent and corollaries overgeneralized: AV-020. |
| 25. Path language/recognisability | Failed: AV-022. |
| 26. Prior-art boundary | No novelty claim is made; universal subsumption/closed-question claim is unsupported. |
| 27. Empirical-content limitation | Not proved for the full framework: AV-018. |
| 28. Theorem numbering/dependencies | Theorems 1–14 are numerically continuous; corollary order and dependency table are unreliable. |
| 29. Internal references | Nonexistent section 18 and wrong section 11 reference: AV-026. |
| 30. LaTeX/notation integrity | Dollar delimiters are balanced; undefined symbols and mixed domains prevent semantic integrity. |

## 9. Consistency assessment

### 9.1 Named deterministic–decision fragment

The displayed arithmetic and deterministic contrasts are mutually compatible.
`C_0` gives zero contrast for both bearers, so A4 is satisfied for every bearer
in the witness. Equality makes the intended congruence condition true. The
identity representation map makes each fibre nonempty.

The claimed fragment witness nevertheless fails:

- `A_C` is missing from every context;
- the outcome measurable space is not fully written;
- A3 is verified only for identity, which is vacuous, and then asserted for
  transported objects not shown to belong to the context set;
- A5, A6, and A9 do not have formal satisfaction predicates;
- the object is not a complete context under Definition 3.14.

Accordingly A3 is not meaningfully verified. The identity case is vacuous, and
the non-identity case is made true by an incomplete transport definition rather
than checked over the witness model.

### 9.2 Complete signature

No logical contradiction was found in the coherent elementary sublanguage.
There is also no proof of consistency of the complete signature. The exact full
signature has undefined sorts, functions, domains, and predicates, so a model
and satisfaction relation cannot be formed. It is therefore impossible to prove
or disprove formal consistency of the complete candidate without first changing
the mathematical specification by supplying missing meanings.

### 9.3 Broader witness

A broader informal construction using singleton carriers, identity/equality
maps, zero contrasts, Dirac measures, and a finite acyclic path structure appears
possible. It is not a witness of the exact candidate: choosing definitions for
`A_C`, profile induction, bottom transports, endpoints, register states, and the
prose axioms would add hypotheses and objects not stated in the theory. No
broader formal witness can therefore be certified without changing the theory.

## 10. Universal-encodability assessment

- **Distinguished zero:** Exists for every `W_2` object by definition.
- **Constant-operation measurability:** Valid; constant maps are measurable
  without requiring measurable singletons.
- **Contrast measurability:** Not valid from the stated hypotheses; subtraction
  need not be measurable. AV-017 gives a counterexample.
- **Reduction:** Returning the atom can be a partial reduction on Dirac
  probability profiles, but the complete reduction/profile context remains
  under-specified.
- **Signed codomains:** Covered only at the generic `W_2` level.
- **Qualitative, magnitude, interval, and distributional codomains:** Not covered
  by the theorem.
- **Effect, decision, information, composition, and diffusion forms:** Not
  constructed. “Applies to all forms” is false.
- **Narrow conclusion:** For a fixed measurable pointed carrier, the intended
  arbitrary assignment can be realized by a measurable projection evaluator;
  this shows that the narrow existential idea is not refuted by the published
  proof defect.
- **Empirical conclusion:** A single-context `W_2` realization theorem does not
  show that the whole framework forbids no observation. Cross-context axioms and
  form-specific restrictions still exclude assignments.

The load-bearing conclusion “no empirical content unrestricted” is therefore
not established exactly.

## 11. Unresolved proof obligations

1. A formal context signature and satisfaction relation.
2. Exhaustive semantics for partial contrasts and every profile class.
3. Typed representation transports for all values and bottom cases.
4. A correct partial quotient descent theorem.
5. Effective rather than merely measurable representation recovery if
   computability is claimed.
6. Posterior existence, measurability, and barycentre conditions.
7. Complete pairwise non-equivalence contexts.
8. A corrected additive-scalar theorem or withdrawal of its conclusion.
9. A valid published proof and exact scope for universal encodability.
10. A complete composition/path signature and instance-level examples.
11. A formal automaton reduction with finite/effective hypotheses.
12. A non-vacuous model satisfying every exact axiom.

OB-2 and OB-3 in the candidate are genuine open obligations. OB-1 is not yet a
proof-ready obligation because the full formal signature is incomplete.

## 12. Freeze recommendation

The candidate is not syntactically complete as a formal theory, is not fully well
typed, contains a false theorem and false corollaries, and has no valid
consistency witness for even its named fragment. Its strongest epistemic
limitation is not proved for the advertised scope. These are freeze-blocking
mathematical defects, not editorial matters.

**Final disposition: ASTRO-THEORY-0001 NOT FORMALLY SOUND**
