# ASTRO-THEORY-0001
## Final Independent Mathematical Re-Verification
### Version 1 Deterministic Core Freeze Assessment

## Examination control

| Field | Value |
|---|---|
| Repository | `17th2nd/ASA-Astro` |
| Authoritative ref | `origin/main` |
| Canonical commit examined | `26417eb4e7dad9bf09260b1d60d6b46ca78d759b` |
| Canonical candidate path | `docs/theory/ASTRO-THEORY-0001.md` |
| Canonical candidate blob | `0d64e4fd1fa8d6668ece38c6ec4f0fab73479210` |
| Worktree before examination | Clean; `HEAD == origin/main` |
| Prior candidate | Not examined as the current theory; no prior finding was adopted as proof |
| Examination scope | Deterministic core only |
| Determination | **DETERMINISTIC CORE REQUIRES BOUNDED REMEDIATION** |

## Scope of the deterministic core examined

The examined core consists of:

- Definitions 3.1–3.12 and 3.15–3.17;
- Axioms A2, A3, A4, A5, A7, A8, A9, and A10;
- Definitions 5.1–5.3 and Theorem 1;
- Definition 6.1 and Corollary 6.2;
- Definitions and results in §7 concerning factorisation, identified outputs,
  fibre constancy, and partial quotient descent;
- Theorem 7′ to the extent that it is a deterministic consequence of contextual
  nullity;
- Theorem 9 as a context-independent scalar normalisation result;
- Theorem 10′ and Corollary 10.1′ because they explicitly claim the
  deterministic contrast form;
- Proposition 11.1, its deterministic consistency witness, the deterministic
  entries in §12, the applicable limitations in §14, and the applicable rejected
  formulations in §16.

Definitions 3.13–3.14, decision and information significance, Theorems 5–6 and
8 insofar as they concern those enrichments, and the composition signature and
Theorems 11–13′ were not required for this determination. Definition 8.9 was
included because A7 directly depends on its cross-context transport object.

## Determinative findings

### FV-001 — The context family and morphism universe are absent from the signature

- **Severity:** Blocking.
- **Location:** Definition 3.10, lines 67–80; Definition 3.15, line 100; A3–A4,
  lines 130–132; Proposition 11.1, lines 392–418.
- **Verification:** The signature defines an individual context but never
  declares the set `C` used by A4 and Theorem 7′. It defines representation
  morphisms but does not declare a model component selecting an admissible
  morphism universe. A3 quantifies over **every** representation morphism.
  Proposition 11.1 instead announces a model-specific set `G={id,j}` and states
  that A3 is quantified over `G`. Nothing in Definitions 3.1–3.17 authorises
  that restriction.
- **Proof:** `mathcal C` first receives a value inside the proposed witness at
  line 404; it is used as a formal carrier at line 132 and line 288 before any
  definition. Likewise `mathcal G` is introduced only inside the witness, while
  A3 has already quantified over every morphism.
- **Consequence:** A4 is not a predicate over the declared signature, and the
  consistency proof does not verify A3 under its written quantifier.
- **Deterministic dependency:** Formal signature, contextual nullity,
  representation covariance, Theorem 7′, and Proposition 11.1.

### FV-002 — The profile of an almost-everywhere partial contrast is not formally defined

- **Severity:** Major.
- **Location:** Definitions 5.1–5.3, lines 150–166.
- **Verification:** Definition 5.2 writes the ordinary pushforward
  `(delta_C^b)_* mu_C` when `delta_C^b` is only a partial map with full-measure
  domain `Omega_C^b`. Ordinary pushforward notation requires a total measurable
  map. No extension off the null complement and no pushforward of the restricted
  measure is defined.
- **Proof:** When `mu_C(Omega_C^b)=1` but `Omega_C^b` is a proper subset of
  `M`, the expression in Definition 5.2 is not an instance of the pushforward
  operation declared anywhere in the candidate. Different total extensions
  yield the same measure, but existence and extension independence are not
  stated; the exact expression remains undefined.
- **Consequence:** Deterministic significance is fully defined for total
  contrasts, including every displayed deterministic witness, but not for every
  context admitted by the deterministic signature.
- **Deterministic dependency:** Definition 5.3, A3, and any deterministic context
  with a contrast undefined only on a null set.

### FV-003 — Theorem 10′ is false for an allowed measurable codomain

- **Severity:** Blocking.
- **Location:** Theorem 10′ and Corollary 10.1′, lines 319–340; verified-results
  table line 436; Limitation 14.11, line 482.
- **Statement:** For every nonempty codomain and every function `f:B->W`, one
  deterministic context realizes `sigma_C=f`.
- **Counterexample:** Let
  `W={0,1}` with the equality partial order and the trivial sigma-algebra
  `{empty,W}`. This is a nonempty codomain under Definition 3.5. Let
  `B={b_0,b_1}` and `f(b_i)=i`. There is exactly one probability measure on
  this measurable space, because every probability measure has the same values
  `0` on the empty set and `1` on `W`. In particular,
  `delta_0=delta_1` as measures. Therefore every defined profile in
  `Delta(W)` is the same object, and the function `rho_C` must return the same
  output for both bearers. It cannot return both `0` and `1`.
- **Verification result:** The proof's “Dirac-atom reduction” is not a function
  on this codomain: its single input measure would have to return two different
  atoms. Point separation by measurable sets is not a hypothesis of the
  theorem. The second-projection evaluator is measurable, but it does not cure
  the collapse of profiles in `Delta(W)`.
- **Consequence:** Theorem 10′, Corollary 10.1′, the corresponding verified-result
  entry, Observation 10.0.1's universal assertion, and Limitation 14.11 are
  false as written.
- **Deterministic dependency:** Bounded encodability and the claimed
  single-context underdetermination of deterministic significance.

### FV-004 — The deterministic consistency witness is not closed under its declared morphism

- **Severity:** Blocking.
- **Location:** Proposition 11.1, especially lines 398–408.
- **Statement:** The context set `{C_1,C_2,C_0}` is closed under
  `G={id,j}` and A3 is verified non-vacuously.
- **Counterexample:** In `C_0`, `M(x,y)=x` and both bearer operations shift the
  second coordinate: `T(b_i)(x,y)=(x,y+1)`. Under the declared coordinate-swap
  morphism `j`, Definition 3.17 gives
  `M_{j_*C_0}(x,y)=y` and gives both transported operations as
  `(x,y)->(x+1,y)`. These components are not those of `C_0`, whose outcome map
  is `x` and whose operations shift `y`. Nor are they the components of `C_1`
  or `C_2`.
- **Verification result:** The assertion `j_*C_0=C_0` at line 404 is false.
  Thus the displayed three-context set is not closed under `G`. The line 408
  statement that the `C_0` case follows symmetrically does not establish the
  claimed closure or satisfaction over the declared set.
- **Consequence:** The proof of Proposition 11.1 contains a false componentwise
  equality and does not prove the stated deterministic consistency result.
- **Deterministic dependency:** Consistency witness, contextual nullity under a
  transport-closed family, and representation covariance.

### FV-005 — Proposition 11.1 does not name all definitions on which it depends

- **Severity:** Major.
- **Location:** Proposition 11.1, line 392, and its satisfaction checks,
  lines 406–414.
- **Verification:** The proposition says the fragment comprises Definitions
  3.1–3.12 and 3.15–3.17 plus the deterministic contrast form. Its axioms and
  proof use `delta_C^b`, `Omega_C^b`, profiles, and `sigma_C`, which are defined
  only in Definitions 5.1–5.3. Those definitions are not included in the
  enumerated fragment.
- **Consequence:** The formal boundary of the claimed fragment is incomplete.
  The intended dependency is inferable from the phrase “deterministic contrast
  form,” but the exact proposition is not closed under its named definitions.
- **Deterministic dependency:** Version 1 fragment identity and consistency.

### FV-006 — Two retained deterministic limitations or rejections overstate verified results

- **Severity:** Major.
- **Location:** Limitation 14.11, line 482; Rejections 16.1 and 16.13, lines
  520 and 532.
- **Verification:** Limitation 14.11 depends on false Theorem 10′. Rejection
  16.1 says intrinsic significance is rejected by Definition 5.3 because
  significance is written as a function of `(C,b)`. A two-argument function may
  be constant in its first argument; Definition 5.3 does not exclude that case,
  and DP-1 is expressly unavailable to proofs. A4 is compatible with the
  intrinsic zero valuation. Rejection 16.13 invokes “artefact relabelling” and a
  “declared universe,” neither of which is defined in the remediated signature;
  Corollary 6.2 proves only fixed-context orbit constancy for `Aut(C)`.
- **Counterexample:** Set `sigma_C(b)=0` for every context and bearer. This is
  independent of context, is compatible with A4, and is not excluded merely by
  writing the function with two arguments.
- **Consequence:** The deterministic core retains unsupported universal or
  categorical statements despite withdrawing their earlier forms.
- **Deterministic dependency:** Explicit limitations and rejected formulations.

## Definitions Verified

The following definitions are mathematically coherent within the deterministic
boundary:

- Definitions 3.1–3.4: bearer set, measurable model space, optional
  representation map, and measurable model operations;
- Definitions 3.5–3.9: ordered measurable codomains, the measurably signed
  subclass, order intervals, disjoint output codomain, and typed optional
  absence;
- Definition 3.10 as the type of an **individual** fully supplied context;
- Definition 3.11 for probability-measure profiles;
- Definition 3.12 on its declared `R_{>=0}` Borel carrier;
- Definitions 3.15–3.17 as transports of individual contexts, including the
  extended action on intervals and bottom values;
- Definition 5.1, including measurability of `Omega_C^b`, because the pair map
  formed from `M_C` and `M_C o tau` is measurable and `D_C` is measurable;
- the case partition in Definition 5.3 once a profile exists;
- Definition 6.1;
- Definition 7.1, Definitions 7.4–7.5, and Definition 7.7 on
  `Omega_C^b`;
- Definition 8.9 as the transport object directly required by A7.

No circular definition was found among these objects. The transport reduction
in Definition 3.17 is defined from the source reduction, and significance is
then evaluated from the transported tuple; it does not define the source value
in terms of itself.

## Definitions Rejected

The following are not accepted as complete Version 1 deterministic definitions:

1. the undeclared context family `mathcal C` used by A4 and Theorem 7′;
2. the undeclared admissible morphism universe implicitly used to replace A3's
   universal quantifier by `mathcal G` in Proposition 11.1;
3. Definition 5.2 for a partial contrast defined almost everywhere but not
   everywhere;
4. the “Dirac-atom reduction” in Theorem 10′ for arbitrary measurable
   codomains, because a Dirac measure need not identify a unique point.

## Axioms Verified

- **A5:** Correctly confines Definition 5.3 outputs to the disjoint output
  codomain.
- **A7:** Correctly types within-context values and makes cross-context relation
  conditional on Definition 8.9.
- **A8:** Correctly states congruence on pairs lying in the partial evaluator's
  domain.
- **A9:** Correctly types the empty pointwise-contrast domain and agrees with
  Definition 5.3.
- **A10:** Correctly types an empty representation fibre and agrees with
  Definition 7.5.

A2 is coherent as a formation rule: a seven-tuple missing a required component
is not a context for which significance is defined. It is not a substantive
axiom over the class of contexts, because Definition 3.10 already requires all
seven components.

## Axioms Not Verified

- **A3:** Its equation is type-correct after Definitions 3.16–3.17, but its
  quantifier is not matched by the witness. The signature says every
  representation morphism; the proof checks only an undeclared selected
  universe `G`.
- **A4:** The nullity formula is coherent after a context family is supplied,
  and the displayed `C_0` gives zero for both bearers. The exact axiom is not a
  predicate over the declared signature because `mathcal C` is absent.

## Theorems Verified

### Theorem 1 — Order reversal exists

Verified. Both contexts supply the individual-context components used in the
proof; every operation and outcome map is measurable; the contrast is total;
the Dirac profiles are point-separating in the Borel codomain; and the computed
values `2,1` and `1,2` follow. The existential scope in Observation 1.1′ is
correct.

### Corollary 6.2 — Fixed-context orbit constancy

Verified conditional on A3. It is exactly the A3 equation for an automorphism
fixing the context and codomain.

### Theorem 3 — Measurable factorisation

Verified. The final sigma-algebra is a sigma-algebra, the extension of `h` off
`r(M)` is total because the target is nonempty, fibre constancy gives
well-definedness, and the final-sigma-algebra definition proves measurability.
No computability, minimality, or uniqueness off the image is inferred.

### Corollary 3.3 — Induced outcome map

Verified when the outcome carrier is equipped with the stated final
sigma-algebra. The composite `M_C o tau` is measurable for that sigma-algebra,
so it is a valid instance of Theorem 3.

### Theorem 3.2′ — Non-constancy under totality

Verified. Totality makes the pointwise contrast a total measurable function;
failure of fibre constancy supplies two distinct values on one nonempty fibre;
Theorem 3 rules out factorisation.

### Theorem 4′ — Partial quotient descent

Verified. A8 makes values independent of the chosen defined representative;
the domain `bar D_C` gives existence and uniqueness; and the pullback domain is
exactly the saturation stated in the conclusion.

### Theorem 7′ — Additive scalar on a nullity-closed family

Verified once `mathcal C` and `mathcal K` are supplied. Hypothesis (a) places
the null witness in the same family on which hypothesis (b) supplies the
nonnegative decomposition, so the proof follows.

### Theorem 9 — Arena dependence

Verified. Finiteness, nonemptiness, strict positivity, and a strictly larger
maximum are all explicit and sufficient.

## Theorems Requiring Narrowing

### Theorem 10′ — Bounded encodability

Rejected under its current universal codomain hypothesis by FV-003. The theorem
is valid on point-separating measurable codomains for which distinct desired
values induce distinct Dirac profiles; it is false for the full class declared
at line 320.

### Proposition 11.1 — Consistency of the deterministic fragment

The existential consistency conclusion is not contradicted: trivial and
singleton deterministic structures indicate no inherent contradiction among
the coherent axioms. The published proof is not verified because:

- its morphism quantifier differs from A3;
- its asserted closure fails on `C_0`;
- its fragment declaration omits Definitions 5.1–5.3;
- `mathcal C` and the admissible morphism universe are not signature objects.

It therefore cannot serve as the Version 1 consistency proof in its current
form.

## Corollaries, observations, limitations, and rejections

Verified within the deterministic boundary:

- Observations 3.6, 3.10.1, 3.11.1, 3.12.1, 3.17.1, 5.3.1, 1.1′,
  3.0, 3.0.1, 3.4, 3.2.1, 3.1.1, 7.8, 4.0, 7.0, 7.1′, and 9.1′;
- Limitation 14.4;
- Limitation 14.7, with its express declared-transport exception;
- Rejections 16.12, 16.16, 16.17, 16.18, and 16.19 as statements about what
  the signature does or does not declare.

Not verified within the deterministic boundary:

- Observation 4.2.1, because A4 is not over a declared carrier and A2 is a
  formation rule rather than a substantive model predicate;
- Observations 10.0, 10.0.1, and Corollary 10.1′ to the extent that they retain
  Theorem 10′'s universal codomain claim;
- Observations 11.1.1–11.1.2 where they state that closure and A3 satisfaction
  have been proved;
- Limitation 14.11, which depends on false Theorem 10′;
- Limitation 14.12, because the displayed consistency proof is invalid;
- Rejections 16.1 and 16.13 for the reasons in FV-006.

The withdrawn-results table in §13 accurately marks those entries as no longer
asserted. No withdrawn statement was used to reject the deterministic core.

## Consistency Assessment

No contradiction was derived among the correctly typed deterministic objects.
The individual contexts in Theorem 1 are coherent. The null context `C_0`
genuinely gives zero significance to both bearers. A simple zero-valued
deterministic structure also indicates that A3 and A4 are not intrinsically
incompatible.

The exact candidate nevertheless lacks a valid proof of its claimed
deterministic consistency proposition. The witness's nontrivial transport check
for `C_1` and `C_2` is correct, but the asserted closure fails for `C_0`, and the
scope of A3 has been changed from every morphism to `G` without a signature
rule. Hence the candidate establishes plausibility of consistency, not the
published Proposition 11.1.

Contextual nullity itself is not the source of inconsistency. The blocking issue
is the relation among null contexts, the undeclared context family, and the
unmatched covariance quantifier.

## Boundary Assessment

The deterministic objects do not depend on decision significance, information
significance, a regular evidence structure, or the composition enrichment.
Those sections can remain Candidate without logically preventing a separately
defined deterministic fragment.

The current candidate, however, does not yet present a closed deterministic
Version 1 boundary. Its own Proposition 11.1 depends on unnamed Definitions
5.1–5.3, an undeclared `mathcal C`, and an undeclared restricted morphism
universe. The deterministic Theorem 10′ is independently false under its stated
codomain class. These defects lie wholly inside the requested deterministic
boundary and therefore cannot be deferred to a Version 2 enrichment programme.

## Deterministic Core Status

The deterministic core is separable in principle but is not presently
freezeable. The blockers are bounded to:

1. the formal context and morphism quantifier boundary;
2. the almost-everywhere partial-profile definition;
3. the universal codomain hypothesis of Theorem 10′ and its dependants;
4. the false closure claim and incomplete dependency list in Proposition 11.1;
5. the retained deterministic limitation and rejection overstatements identified
   in FV-006.

The determination is therefore bounded remediation rather than a conclusion
that contextual difference or deterministic significance is mathematically
incoherent.

## Remaining Candidate Extensions

The following remain outside this verification and retain Candidate status:

- formal versions of DP-1 and DP-2;
- general class `W_2` and measurably signed `W_2^m` uses;
- non-Dirac and non-atomic probabilistic extensions beyond what the deterministic
  definitions require;
- effect, decision, and information significance;
- regular evidence structures;
- interval- and bottom-valued examples beyond their output typing;
- nontrivial contextual congruence examples;
- composition, diffusion, non-associativity, and path enrichments;
- consistency beyond the exact deterministic fragment;
- novelty, recognisability, and prior-art questions.

No result about these extensions is necessary for the present negative freeze
determination.

## Remaining Proof Obligations

1. A declared context family supporting A4 and Theorem 7′.
2. A declared covariance quantifier matching A3 and the consistency witness.
3. A formal profile for an almost-everywhere-defined partial contrast.
4. A true deterministic encodability theorem over its exact codomain class, or
   withdrawal of Theorem 10′ and its dependants from the deterministic core.
5. A valid deterministic consistency proof whose context set is actually closed
   under its stated morphisms and whose fragment lists every definition used.
6. Removal or proof of the retained deterministic overstatements in FV-006.

OB-1 intersects this deterministic examination because A3 over all
representation morphisms is an axiom of the proposed core, not merely a future
decision, information, or composition enrichment. OB-3 and the enrichment
portion of OB-1 do not block this determination. OB-4 does not block the core
because DP-1 and DP-2 are explicitly non-formal and unused in proofs.

## Final Determination

ASTRO-THEORY-0001

DETERMINISTIC CORE REQUIRES BOUNDED REMEDIATION
