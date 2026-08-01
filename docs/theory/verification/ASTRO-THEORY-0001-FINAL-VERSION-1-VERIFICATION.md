# ASTRO-THEORY-0001
## Final Version 1 Deterministic-Core Verification

## 1. Examination control

| Field | Verified value |
|---|---|
| Repository | `17th2nd/ASA-Astro` |
| Authoritative ref | `origin/main` after a fresh fetch |
| Branch before examination | `main` |
| `HEAD == origin/main` before examination | Yes |
| Ahead / behind before examination | `0 / 0` |
| Worktree before examination | Clean; no staged, modified, or untracked files |
| Examination date | 2026-08-01 (Australia/Brisbane) |
| Exact theory path | `docs/theory/ASTRO-THEORY-0001.md` |
| Theory edited | No |
| Part B edited | No |
| Theory frozen | No |

The required fetch completed successfully. The five required documents were then resolved and read in full from the freshly fetched `origin/main` Git object tree. The four prior verification and remediation records were treated as evidence of intended work only, not as proof.

No `AGENTS.md` exists in the repository. The repository `README.md` was inspected; it contains no additional instruction altering this examination. No frozen research control was modified.

A second fresh fetch during the examination again returned the same `origin/main` commit and the same five blobs, with `HEAD == origin/main`, zero divergence, and a clean worktree. The canonical source did not change during the mathematical examination.

## 2. Exact commit and blobs

| Object | Exact Git object |
|---|---|
| GitHub commit examined | `ba3ccc097a024b5354b58199094719e7b1f3e271` |
| `docs/theory/ASTRO-THEORY-0001.md` | `c20ca91fa18551f247dfa1c150dea3f9d9b510d5` |
| `docs/theory/verification/ASTRO-THEORY-0001-VERSION-1-DETERMINISTIC-CORE-VERIFICATION.md` | `400df7491539b153e6e9550ab0c267593e56337e` |
| `docs/theory/verification/ASTRO-THEORY-0001-DCV-ADJUDICATION.md` | `5b75ffca85191532096252a341d104d2472cb091` |
| `docs/theory/verification/ASTRO-THEORY-0001-SIGNATURE-COMPLETION-CHANGE-MAP.md` | `3712efa6164530b3b1f6387ee0eefec0ff9cd072` |
| `docs/theory/verification/ASTRO-THEORY-0001-SIGNATURE-COMPLETION-REPORT.md` | `a95437e629ed041f1e6bf36fbde9d4da187103ef` |

The working-copy theory independently hashes to the same theory blob, `c20ca91fa18551f247dfa1c150dea3f9d9b510d5`.

## 3. Verification scope

The proposed freeze object examined was exactly:

> ASTRO-THEORY-0001 — VERSION 1 DETERMINISTIC CORE

The mathematical scope was Part A only. Part B was inspected solely to test the dependency boundary, status declarations, and accidental-change control. No Part B theorem or enrichment was required to pass this examination.

The examination rechecked the complete Part A signature, definitions, formation rule, axioms, retained theorems and corollaries, consistency proposition, limitations, rejected formulations, open obligations, and Part A / Part B boundary. It did not assume that closure of DCV-001 or DCV-002 implied closure of the rest of Part A.

## 4. Method

1. Fetch `origin`; verify branch, equality, divergence, and worktree state.
2. Record the authoritative commit and all five required blob identities.
3. Read all five blobs in full from `origin/main`.
4. Enumerate every primitive and derived symbol used by Part A.
5. Type-check the homogeneous frame, morphism components, group laws, context transport, closure predicate, A3, and functoriality component by component.
6. Check supplied and absent branches of the representation component separately.
7. Re-prove every retained Part A theorem and corollary from its stated hypotheses.
8. Reconstruct all four witness contexts, both group elements, every transport, every contrast, profile, significance value, and axiom instance independently.
9. Check Part A references against Part B and compare the Part B byte region with the pre-remediation theory blob.
10. Check headings, declaration labels, cross-references, delimiters, braces, unfinished markers, status text, and malformed notation.
11. Fetch `origin` again and confirm that the canonical theory and verification basis remained unchanged.

Mechanical checks were used as integrity evidence only. They were not substituted for mathematical proof.

## 5. DCV-001 closure determination

**Determination: not fully closed.** The central homogeneous-carrier construction is mathematically viable, but the actual Part A text retains blocking typing and completeness defects.

### Elements that pass

- Definition 3.14.1 fixes one bearer set, one measurable model space, one measurable outcome space, and one ordered measurable codomain per frame.
- Definition 3.18 clause 3 requires every context in one instance to use exactly the frame's outcome and codomain carriers.
- Definition 3.15 gives explicit endomorphism types for the bearer, model, outcome, and codomain components.
- Subject to a fully declared codomain structure, the identity, componentwise composition, componentwise inverses, associativity, and unit laws are valid. Thus the intended automorphism set is a group, and an instance group may be a subgroup.
- The transported measure, outcome map, operation assignment, optional equivalence, contrast evaluator, fixed carriers, and reduction all have the intended types when the extended codomain action is read as an endomorphism of the fixed `W`.
- Direct componentwise calculation verifies
  \[
  \mathbf 1_*C=C,
  \qquad
  (\iota\circ\kappa)_*C=\iota_*(\kappa_*C).
  \]
  For measures this is functoriality of pushforward; for the reduction it uses
  `((\iota\circ\kappa)^{-1})_*=(\kappa^{-1})_*\circ(\iota^{-1})_*` and
  `\widehat{\iota_W\circ\kappa_W}=\widehat{\iota_W}\circ\widehat{\kappa_W}`.

### Blocking defects

1. **Definition 3.16 has an unbound target.** It declares
   \[
   \widehat{\iota_W}:\widehat W\longrightarrow\widehat{W'}
   \]
   although Definition 3.15 types `\iota_W` as an automorphism `W\to W` and no `W'` is declared. The only type induced by Definition 3.15 is `\widehat W\to\widehat W`. As written, the reduction transport and the right side of A3 still depend on an undeclared codomain. This is exactly the kind of remaining untyped reference that the examination instruction makes blocking.

2. **The frame does not contain every algebraic structure used by the core.** Definition 3.5 defines a codomain as the triple `(W,\preceq_W,\Sigma_W)` and says class `\mathsf W_1` additionally carries `(\oplus,0_W)`. Definition 3.14.1 and the displayed theory-instance tuple carry only the triple. Nevertheless Definition 3.15 requires morphisms to preserve any declared class-`\mathsf W_1` structure, A4 uses `0_W`, and the witness uses `+` and `0`. No chosen `\oplus` or `0_W` appears in the frame or primitive-completeness table. The same carrier triple could therefore be paired with different additional structures without the instance selecting which one A4 and the morphism condition mean.

3. **Definition 8.9 retains an undeclared and potentially heterogeneous transport.** It introduces an optional `t:W_C\to W_{C'}` but does not make a transport family, a supplied `t`, or typed absence a component of the theory instance. It also does not state that `C` and `C'` belong to the same homogeneous instance, so its displayed source and target retain the heterogeneous notation that Observation 3.14.2 says was removed from Version 1. Its extended action is referred back to the already malformed Definition 3.16.

4. **The homogeneous restriction changes the valid scope of a retained corollary.** This is detailed in the theorem audit. In brief, A4 requires a class-`\mathsf W_1` context for every bearer, while homogeneity forces every context in an instance to use the same `W`. On a point-separating codomain that is not class `\mathsf W_1`, no homogeneous instance can satisfy A4. Corollary 10.1″ nevertheless quantifies over every point-separating codomain and says no assignment is excluded by the axioms. Theorem 10″ constructs one context only and does not prove that assertion. Before homogeneity, a separate context with a different class-`\mathsf W_1` codomain could satisfy A4; after homogeneity that route is unavailable.

The bearer, model, and outcome automorphism laws themselves pass. These four defects prevent the claimed complete DCV-001 closure.

## 6. DCV-002 closure determination

**Determination: the principal tuple repair is valid, but DCV-002 is not fully closed throughout Part A.**

### Elements that pass

- Definition 3.18 clause 2 makes `\mathsf r` exactly one of a supplied pair `(r,(\mathcal R,\mathcal H))`, with `r:\mathfrak M\to\mathcal R` total and measurable, or typed absence `\bot_{\mathrm{abs}}`.
- When supplied, the declared domain, codomain, and sigma-algebra make Definition 7.1 and the fibre expressions in Definitions 7.4 and 7.5 meaningful.
- A10 explicitly refers to the instance component.
- Proposition 11.1′ supplies `\mathsf r=(\mathrm{id}_{\mathfrak M},(\mathfrak M,\mathcal F))` as instance data rather than as an external witness datum.
- When `\mathsf r` is absent, Observation 3.18.2 states that A10 and Definitions 7.1, 7.4, 7.5, and 7.7 are inapplicable, not vacuously true. This supplied/absent distinction is correct.

### Blocking defects

1. Immediately after the repaired Definition 3.18, the axiom section says:
   \[
   \text{Fix a theory instance }\mathbb T=(\mathfrak B,\mathfrak M,\mathcal C,\mathcal G).
   \]
   This is the superseded four-component tuple that omitted the outcome space, codomain, and representation component. It is stated as an equality, not as an explicitly declared abbreviation. A10 later refers to a representation component that is not recoverable from this displayed `\mathbb T`. The complete tuple repair is therefore not carried consistently into the formal axiom section.

2. Theorem 3.2′ uses the instance-dependent predicates “`r` total for `(C,b)`” and “fibre-constant,” as well as `\mathcal S_C(b,x)`, but its statement does not restrict itself to the supplied-`\mathsf r` branch. Observation 3.18.2 expressly exempts Theorem 3 and Corollary 3.3 because they quantify over their own maps; it does not do so for Theorem 3.2′. In an absent-`\mathsf r` instance the hypotheses and conclusion of Theorem 3.2′ have no interpretation. Its proof is correct in the supplied branch, but the theorem's applicability is not fully typed.

3. Definition 7.5 does not declare a symbol, domain, or common output carrier for “the identified output.” Its cases return either `\bot_{\mathrm{inc}}`, `\bot_{\mathrm{und}}`, or a subset `\mathcal S_C(b,x)\subseteq W`; arbitrary subsets need not be elements of `\widehat W`. A10 consequently refers in prose to an output whose function type is not declared. The individual empty-fibre value is intelligible, but the identified-output definition is not formally complete to the standard required here.

Thus the representation datum is now present in the main tuple and the witness, but the full Part A use of that datum is not yet uniformly typed.

## 7. Primitive-completeness audit

The table in Definition 3.18.3 correctly records the frame carriers, `\mathsf r`, context family, morphism group, measure, outcome map, operation assignment, optional equivalence, contrast evaluator, and reduction. It is not complete against the actual Part A text.

| Primitive or datum used by Part A | Actual status | Determination |
|---|---|---|
| `\mathfrak B`, `(\mathfrak M,\mathcal F)`, `(\mathcal Y,\mathcal G_{\mathcal Y})`, `(W,\preceq_W,\Sigma_W)` | In the frame | Pass |
| `\mathsf r` supplied or absent | In Definition 3.18 clause 2 | Pass at the main tuple |
| `\mathcal C`, `\mathcal G` | In Definition 3.18 | Pass |
| `\mu_C,M_C,T_C,\approx_C,\delta_C,\rho_C` | In each context | Pass |
| Class-`\mathsf W_1` operation `\oplus` and identity `0_W` | Used by Definition 3.15, A4, Theorem 7′, and the witness; absent from the frame and table | **Blocking omission** |
| Optional cross-context transport `t` or its typed absence | Used by Definition 8.9 and A7; absent from the instance and table | **Blocking omission** |
| Identified-output function and carrier | Used by A10 and Theorem 3.2′; no typed function is declared | **Blocking omission** |
| `\bot_{\mathrm{abs}}` | Globally declared in Definition 3.9 but omitted from the table | Table incompleteness; the global symbol itself is intelligible |

Locally quantified theorem data—such as `g`, `h`, `S`, `\beta`, `\mathcal K`, `f`, `\varphi`, and the quotient projection—do not have to be instance components because their theorem statements declare them. Derived objects `\Omega_C^b`, `P_C^b`, `\sigma_C`, `\mathcal H_r`, and `\mathrm{Aut}(C)` are likewise recoverable once their inputs are fully declared.

The primitive-completeness table's assertion that no Part A axiom depends on absent data is false because A4 uses the undeclared chosen class-`\mathsf W_1` structure and A7 refers to undeclared optional transports.

## 8. Definition audit

| Definition group | Result |
|---|---|
| 3.1–3.4 | Pass, subject to the supplied/absent integration findings above |
| 3.5, 3.5.1, 3.7–3.12.1 | Set-level definitions pass; class-`\mathsf W_1` structure is not carried by the instance |
| 3.14.1 | Pass for the four displayed carriers; incomplete for additional algebraic structure |
| 3.15 and group laws | Component sources and targets pass for the displayed carriers; structure preservation has no selected structure in the frame |
| 3.16 | **Fail:** `W'` is unbound |
| 3.17 | The six transported context components are well typed if 3.16 is read with target `\widehat W`; as written the reduction output inherits 3.16's defect |
| 3.18 | Main tuple and homogeneity clauses pass; later superseded tuple and omitted data prevent full signature completeness |
| 5.1 | Pass: `\Omega_C^b` is measurable and the partial contrast is measurable on its trace domain |
| 5.2 | Pass: restriction to a full-measure trace space makes the contrast total before pushforward |
| 5.3 | The four cases are disjoint and exhaustive. Therefore `\sigma_C(b)` is total on valid `(C,b)`, despite the heading calling it “partial” |
| 6.1 | The stabiliser/kernel intersection is a subgroup once the action is fully typed |
| 7.1, 7.4, 7.7 | Pass in the supplied-`\mathsf r` branch; inapplicable in the absent branch |
| 7.5 | **Fail formal completeness:** no identified-output function type or common carrier is declared |
| 8.9 | **Fail:** optional transport data are outside the instance and the homogeneous source/target condition is unstated |

The atom reduction is well defined exactly on point-separating codomains. The almost-everywhere profile construction is valid and uses no extension across a null complement. The deterministic-significance cases correctly send undefined operations, non-full contrast domains, and reductions outside their domains to `\bot_{\mathrm{und}}`.

## 9. Axiom audit

| Item | General statement | Witness calculation |
|---|---|---|
| FR-1 | Pass | All seven context slots supplied; `\approx=\bot_{\mathrm{abs}}` |
| A3 | **Blocked by Definition 3.16 and the incomplete codomain structure** | All identity and eight non-identity equations pass |
| A4 | **Blocked as an exact instance predicate because the chosen `\mathsf W_1` structure is absent from the tuple** | Numerically passes using the prose-supplied `+` and `0` |
| A5 | Pass; Definition 5.3 always returns an element of `\widehat W` | All values lie in `W\subseteq\widehat W` |
| A7 | **Not a testable predicate over the declared tuple because optional transports are not instance data** | No comparison is performed, but that does not complete the general signature |
| A8 | Pass; it is restricted to defined pairs | Vacuous because every equivalence is absent |
| A9 | Pass; it agrees with row two of Definition 5.3 whenever `\Omega_C^b` is defined and empty | Antecedent false for every witness pair |
| A10 | Empty-fibre case has the intended value when `\mathsf r` is supplied; absent branch is correctly inapplicable. Full output typing remains incomplete | Passes vacuously because `r=\mathrm{id}` has no empty fibre |

A5, A7, A8, and A9 use implicit free `C,b` variables rather than explicit universal quantifiers. Their intended schema reading is clear, but explicit quantification would be preferable for a frozen formal presentation.

## 10. Theorem audit

| Result | Determination |
|---|---|
| Theorem 1 — order reversal | **Pass.** The two contexts differ only in `M`; the profiles are `\delta_2,\delta_1` and `\delta_1,\delta_2`. The conclusion is existential. |
| Corollary 6.2 — orbit constancy | The one-line proof is correct from a well-typed A3 action. **Current freeze is blocked by DCV-001.** |
| Theorem 3 — measurable factorisation | **Pass.** Fibre constancy gives a well-defined extension and the final sigma-algebra makes it measurable. |
| Corollary 3.3 — induced outcome map | **Pass.** It is Theorem 3 with `r=M_C` and `g=M_C\circ\tau`; the context guarantees a nonempty outcome space. |
| Theorem 3.2′ — non-constancy under totality | Proof **passes in the supplied-`\mathsf r` branch**. Its absent-branch applicability is not stated and therefore does not pass uniform typing. |
| Theorem 4′ — partial quotient descent | **Pass.** A8 gives representative independence on exactly `(p\times p)(D_C)`; the pullback domain is the saturation of `D_C`. |
| Theorem 7′ — additive scalar | **Pass.** The null context lies in the same `\mathcal K`; nonnegative summands and `\beta>0` force `S(b)=0`. |
| Theorem 9 — normalisation | **Pass.** The larger positive denominator strictly lowers every old-arena value and preserves order. |
| Theorem 10″ — point-separating encodability | **Pass as a context-existence theorem.** Constant operations and the second projection are measurable; atom reduction returns `f(b)`. |
| Corollary 10.1″ — bounded underdetermination | **Fail.** Its statement exceeds Theorem 10″ after homogeneity. A point-separating `W` need not be class `\mathsf W_1`; then no homogeneous instance over `W` can satisfy A4, so assignments on that `W` are excluded by the full axioms. |
| Proposition 11.1′ — deterministic consistency | The displayed four-context model and every numerical axiom check pass. **The claim that it instantiates the exact general signature fails** because the required `\mathsf W_1` structure is supplied only in prose and Definition 8.9's optional datum has no slot or typed absence. |

The associated non-conclusions for Theorems 1, 3, 3.2′, 4′, 7′, and 9 are accurate. Observation 10.1.1 itself acknowledges that assignments are additionally constrained by A4, which confirms that Corollary 10.1″ cannot follow solely from the single-context construction over every point-separating codomain. Limitations 14.11′ and Observation 10.0.1 repeat the same overbroad “axioms do not exclude” claim and therefore fail with the corollary.

No retained proof relies on Part B. No existential theorem other than Corollary 10.1″ is presented as a stronger universal instance claim. Theorem 10″ itself remains valid in its narrow context-existence form.

## 11. Full witness reconstruction

### Frame and representation component

The witness declares:

- `\mathfrak B=\{b_1,b_2\}`;
- `(\mathfrak M,\mathcal F)=(\mathbb R^2,\mathcal B(\mathbb R^2))`;
- `(\mathcal Y,\mathcal G_{\mathcal Y})=(\mathbb R,\mathcal B(\mathbb R))`;
- `(W,\preceq_W,\Sigma_W)=(\mathbb R_{\ge0},\le,\mathcal B(\mathbb R_{\ge0}))`;
- in prose, the additional class-`\mathsf W_1` structure `(+ ,0)`;
- `\mathsf r=(r,(\mathcal R,\mathcal H))` with `(\mathcal R,\mathcal H)=(\mathfrak M,\mathcal F)` and `r=\mathrm{id}_{\mathfrak M}`.

The carrier is homogeneous and point-separating. The supplied representation component is total and measurable, and `\mathcal H_r=\mathcal F`.

### Morphism group

The identity is
\[
\mathbf1=(\mathrm{id}_{\mathfrak B},\mathrm{id}_{\mathfrak M},
\mathrm{id}_{\mathcal Y},\mathrm{id}_W).
\]

The nontrivial element is
\[
\jmath_{\mathfrak B}(b_1)=b_2,
\quad \jmath_{\mathfrak B}(b_2)=b_1,
\quad \jmath_{\mathfrak M}(x,y)=(y,x),
\quad \jmath_{\mathcal Y}=\mathrm{id},
\quad \jmath_W=\mathrm{id}.
\]

Each component is an automorphism of its displayed carrier, `\jmath^2=\mathbf1`, and `\mathcal G=\{\mathbf1,\jmath\}` is a group of order two. The identity codomain map preserves the prose-supplied `+` and `0`.

### Shared context components

Every context has:

- `\mu=\delta_{(0,0)}`;
- `\approx=\bot_{\mathrm{abs}}`;
- `\delta(u,v)=|u-v|` with domain `\mathbb R^2`;
- the frame outcome and codomain carriers;
- `\rho=\rho^{\mathrm{at}}` with domain the Dirac measures.

The evaluator is total and Borel measurable. Point separation makes atom reduction a function.

### Contexts and transported contexts

| Context | Outcome map | `T(b_1)` | `T(b_2)` |
|---|---|---|---|
| `C_1` | `M(x,y)=x` | `(x,y)\mapsto(x+2,y+1)` | `(x,y)\mapsto(x+1,y+2)` |
| `C_2=\jmath_*C_1` | `M(x,y)=y` | `(x,y)\mapsto(x+2,y+1)` | `(x,y)\mapsto(x+1,y+2)` |
| `C_0` | `M(x,y)=x` | `(x,y)\mapsto(x,y+1)` | `(x,y)\mapsto(x,y+1)` |
| `C_0'=\jmath_*C_0` | `M(x,y)=y` | `(x,y)\mapsto(x+1,y)` | `(x,y)\mapsto(x+1,y)` |

For every transport by `\jmath`:

- `(\jmath_{\mathfrak M})_*\delta_{(0,0)}=\delta_{(0,0)}`;
- the outcome maps and operations are exactly those in the table;
- absent equivalence transports to absent equivalence;
- `\delta` is unchanged because both outcome and codomain components are identities there;
- the outcome and codomain carriers remain the fixed frame carriers;
- `\rho` is unchanged because `\jmath_W=\mathrm{id}`.

Direct calculation gives
\[
\jmath_*C_1=C_2,
\quad \jmath_*C_2=C_1,
\quad \jmath_*C_0=C_0',
\quad \jmath_*C_0'=C_0.
\]

Together with the identity action, `\mathcal C=\{C_1,C_2,C_0,C_0'\}` is closed under `\mathcal G`. Involutivity is used only after the first two transports have been explicitly computed.

### Contrasts, profiles, and significance

Every operation is total, every `\Omega_C^b=\mathfrak M`, and every pointwise contrast is constant:

| Context | Bearer | `\delta_C^b(m)` for every `m` | Profile | Significance |
|---|---|---:|---|---:|
| `C_1` | `b_1` | `2` | `\delta_2` | `2` |
| `C_1` | `b_2` | `1` | `\delta_1` | `1` |
| `C_2` | `b_1` | `1` | `\delta_1` | `1` |
| `C_2` | `b_2` | `2` | `\delta_2` | `2` |
| `C_0` | `b_1` | `0` | `\delta_0` | `0` |
| `C_0` | `b_2` | `0` | `\delta_0` | `0` |
| `C_0'` | `b_1` | `0` | `\delta_0` | `0` |
| `C_0'` | `b_2` | `0` | `\delta_0` | `0` |

### All non-identity A3 equations

Since `\widehat{\jmath_W}` is intended to be the identity:

1. `\sigma_{C_2}(b_2)=2=\sigma_{C_1}(b_1)`.
2. `\sigma_{C_2}(b_1)=1=\sigma_{C_1}(b_2)`.
3. `\sigma_{C_1}(b_2)=1=\sigma_{C_2}(b_1)`.
4. `\sigma_{C_1}(b_1)=2=\sigma_{C_2}(b_2)`.
5. `\sigma_{C_0'}(b_2)=0=\sigma_{C_0}(b_1)`.
6. `\sigma_{C_0'}(b_1)=0=\sigma_{C_0}(b_2)`.
7. `\sigma_{C_0}(b_2)=0=\sigma_{C_0'}(b_1)`.
8. `\sigma_{C_0}(b_1)=0=\sigma_{C_0'}(b_2)`.

All eight hold and `\jmath\ne\mathbf1`, so the numerical covariance check is non-vacuous.

### Remaining witness checks

- **FR-1:** all seven context components are supplied.
- **A4:** `C_0` gives zero for both bearers; `C_0'` does as well.
- **A5:** all values are in `W\subseteq\widehat W` and arise from row four of Definition 5.3.
- **A7:** no cross-context comparison is made.
- **A8:** inapplicable antecedent because every equivalence is absent.
- **A9:** every contrast domain is the nonempty whole model space.
- **A10:** `r=\mathrm{id}` has singleton fibres and no empty fibre.

The representation component now comes from the declared main tuple. The witness nevertheless does **not** instantiate the exact written general signature without external prose: the class-`\mathsf W_1` operation and zero used by A4 and morphism preservation are not components of the frame tuple, and the claimed signature includes optional Definition 8.9 without a transport slot or typed absence.

## 12. Part A / Part B dependency audit

- No Part A proof cites a Part B definition, theorem, design principle, or obligation.
- References to Part B within Part A are boundary and deferral statements only.
- Part B is consistently labelled Candidate, non-frozen, outside Proposition 11.1′, and outside the Version 1 verification claim.
- The Part B region is byte-identical to the pre-remediation theory blob `ad86bb978dc2d9a215af9f90d3a8cf9771f48d69`. Both regions have SHA-256 `05f1720f10f0a1c2670db644373a832ad26f5fb74e184e1dc1e463fc4d5a6c3c`.

**Dependency determination: pass.** Part A does not depend on Part B. The blockers found in this report are internal to Part A.

## 13. Open-obligation assessment

| Obligation | Assessment |
|---|---|
| OB-A1 | Not used by any retained proof; non-blocking research question |
| OB-A2 | Not needed in the current measurable setting; non-blocking |
| OB-A3 | Not needed for Theorem 10″ as stated; non-blocking research question |
| OB-A4 | Equivariance of `\mathsf r` with `\mathcal G` is not used by any retained Part A statement; non-blocking |
| OB-A5 | Part B placement is not needed to prove homogeneous results. It does not cure the remaining Part A occurrence in Definition 8.9 |
| OB-B1–OB-B4 | Entirely outside this verification |

No open obligation supplies a missing hypothesis for a theorem that otherwise passed. OB-A4 and OB-A5 do not repair the blocking written-signature defects identified above.

## 14. Mechanical-integrity results

| Check | Result |
|---|---|
| Theory size | 505 lines; 6,113 words; 52,108 bytes |
| Markdown heading hierarchy | Balanced Part A and Part B hierarchy; no skipped structural level |
| Display-math delimiters | 22 `$$` delimiters; balanced |
| Remaining dollar delimiters | 1,330 delimiter characters after display delimiters; every source line has even parity |
| Braces | 692 opening and 692 closing |
| Code fences | 0 |
| Duplicate numbered declaration headings | None detected |
| Unfinished markers | No `TODO`, `TBD`, `FIXME`, `XXX`, `???`, or unchecked-box marker |
| Status declarations | Consistently Candidate, not frozen, awaiting verification |
| Accidental Part B changes | None; byte-region hash matches the pre-remediation blob |

The theorem and corollary labels in the result register resolve to declarations. Cross-references to withdrawn formulations are explicitly historical. There are, however, three mechanical defects relevant to freeze:

1. Definition 3.16's undeclared `W'` is malformed notation and a mathematical type error.
2. The four-component `\mathbb T=(\mathfrak B,\mathfrak M,\mathcal C,\mathcal G)` line is superseded text retained after Definition 3.18 was repaired.
3. The local sequence `Observation 3.18.2`, `Definition 3.18.3`, `Observation 3.18.1` is non-monotone, though all three labels are unique and cross-references resolve.

The heading of Definition 5.3 calls deterministic significance “partial,” while its four exhaustive cases assign a value to every valid `(C,b)`. This is a non-blocking terminology inconsistency because the case definition and A5 unambiguously make the resulting output total.

## 15. Remaining blocking findings

1. **DCV-001 remains open:** Definition 3.16 has undeclared target `W'`, so extended action, reduction transport, and A3 are not fully typed as written.
2. **The homogeneous frame is structurally incomplete:** the selected class-`\mathsf W_1` operation and zero used by A4 and morphism preservation are not frame or instance components.
3. **Primitive completeness fails:** optional cross-context transport and its typed absence are not instance data, so A7 and Definition 8.9 are not predicates over the declared tuple; Definition 8.9 also retains an unconstrained heterogeneous source/target form.
4. **DCV-002 remains incompletely propagated:** the axiom section reinstates the old four-component theory-instance equality, Theorem 3.2′ is not gated to the supplied branch, and the identified-output function has no declared type.
5. **A retained corollary exceeds its proof:** Corollary 10.1″, Observation 10.0.1, and limitation 14.11′ claim axiom-level encodability for every point-separating codomain, but homogeneity plus A4 excludes all instances whose fixed point-separating codomain is not class `\mathsf W_1`.
6. **The consistency proposition does not instantiate the exact written general signature:** its calculations are correct, but its `\mathsf W_1` structure is extra-tuple prose data and its claimed optional transport signature has no supplied/absent slot.

Each finding is bounded. Together they prevent formal completeness, uniform well-typedness, passage of every retained theorem, and the required exact-signature witness claim.

## 16. Remaining non-blocking findings

- Definition 5.3 is labelled partial although its exhaustive bottom-valued cases make `\sigma_C` total.
- A5, A7, A8, and A9 would benefit from explicit universal quantifiers over their free context and bearer variables.
- The 3.18.x declaration order is non-monotone but references remain resolvable.
- OB-A1 through OB-A5 remain genuine research or placement questions and are not used by passed proofs.
- All numerical witness values, transported contexts, group equations, and non-identity A3 equalities are correct.
- Part A is independent of Part B, and Part B is unchanged.

## 17. Freeze recommendation

Do **not** freeze Part A at theory blob `c20ca91fa18551f247dfa1c150dea3f9d9b510d5` as `ASTRO-THEORY-0001 VERSION 1 — DETERMINISTIC CORE`.

The correct recommendation is bounded remediation, not rejection of the deterministic construction. The homogeneous automorphism design and optional representation slot are viable, the scalar and factorisation theorems largely pass, and the four-context witness is numerically sound. Freeze is blocked by the remaining exact-signature, typing, and corollary-scope defects listed above. This verification operation makes no repair and creates no freeze.

## 18. Final determination

ASTRO-THEORY-0001
DETERMINISTIC CORE REQUIRES BOUNDED REMEDIATION
