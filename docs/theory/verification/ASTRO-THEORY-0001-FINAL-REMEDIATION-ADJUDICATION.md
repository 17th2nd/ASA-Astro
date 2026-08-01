# ASTRO-THEORY-0001 — Final Deterministic-Core Remediation Adjudication

**Subject:** `docs/theory/ASTRO-THEORY-0001.md`
**Sole authoritative defect basis:** `docs/theory/verification/ASTRO-THEORY-0001-FINAL-INDEPENDENT-VERIFICATION.md`, determination **DETERMINISTIC CORE REQUIRES BOUNDED REMEDIATION**. Read in full. Not modified.
**Pre-remediation blob:** `0d64e4fd1fa8d6668ece38c6ec4f0fab73479210` — confirmed at `HEAD` and in the worktree before mutation.
**Baseline:** `HEAD = origin/main = 26417eb4e7dad9bf09260b1d60d6b46ca78d759b`, branch `main`, 0 ahead / 0 behind, worktree otherwise clean.
**Status after remediation:** Theory Candidate. Not frozen.

**Basis discipline.** Neither the V1–V20 findings nor the AV-001–AV-028 findings were used as a remediation basis. Where the final report carries an earlier concern forward it does so in its own words, and only that wording is cited.

**Provenance note.** At the time of this pass the final verification report is **present but untracked** in the worktree. Its content hash is recorded here so the basis is pinned regardless: the report is the file at the path above, 20 967 bytes, SHA-256 `98ec24bb2487b16e…`, examined commit `26417eb`, examined blob `0d64e4fd`. Per instruction, it is **not** staged by this pass and is **not** modified.

**Finding distribution:** Blocking 3 (FV-001, FV-003, FV-004) · Major 3 (FV-002, FV-005, FV-006) · **total 6**.
**Disposition distribution:** Accepted 2 · Accepted with Modification 3 · Withdrawn Statement 1 · Rejected with Proof 0.

**On the absence of rejections.** Each counterexample in the report was reconstructed independently before adjudication. All held. FV-004 in particular identifies a false componentwise equality that I asserted and did not check; the recomputation confirms the verifier.

---

## FV-001 — The context family and morphism universe are absent from the signature

- **Severity:** Blocking
- **Exact defect:** The signature defines an individual context but never declares the set $\mathcal{C}$ used by A4 and Theorem 7′, and declares no component selecting an admissible morphism universe. A3 quantifies over **every** representation morphism, while Proposition 11.1 announced a model-specific $\mathcal{G}=\{\mathrm{id},\jmath\}$ and quantified A3 over it. Nothing in Definitions 3.1–3.17 authorised that restriction. $\mathcal{C}$ first received a value inside the proposed witness while being used as a formal carrier by the axioms.
- **Exact affected section:** Definition 3.10; Definition 3.15; A3–A4; Proposition 11.1.
- **Disposition:** **Accepted**
- **Exact repair:** New **Definition 3.18 (Theory instance)** declares $\mathbb{T}=(\mathfrak{B},(\mathfrak{M},\mathcal{F}),\mathcal{C},\mathcal{G})$ with $\mathcal{C}$ a nonempty set of contexts, $\mathcal{G}$ a group of representation morphisms, and **closure of $\mathcal{C}$ under transport by $\mathcal{G}$ as a requirement on instances**. **A3** now quantifies over the declared $\mathcal{G}$; **A4** over the declared $\mathcal{C}$. Observation 3.18.1 records the change. Observation A.3.1 replaces the prior Observation 4.2.1 and states that A3 and A4 are now predicates over declared carriers.
- **Proof or counterexample:** No counterexample was required; the defect is one of undeclared carriers. With Definition 3.18 supplied, A3's quantifier ranges over a declared set and $\iota_*C\in\mathcal{C}$ makes the equation well formed; A4's existential ranges over a declared set.
- **Downstream effect:** Theorem 7′ now hypothesises a family $\mathcal{K}\subseteq\mathcal{C}$ of a declared instance. Corollary 6.2 uses $\mathrm{Aut}(C)\le\mathcal{G}$. Proposition 11.1′ must exhibit an instance, which means exhibiting closure rather than asserting it.
- **Fully closed:** **Yes.** The narrowing of A3 from *all* morphisms to a declared $\mathcal{G}$ is an explicit exercise of the permitted option "narrow the axiom", and is recorded as such rather than presented as no change.

---

## FV-002 — The profile of an almost-everywhere partial contrast is not formally defined

- **Severity:** Major
- **Exact defect:** Definition 5.2 wrote the ordinary pushforward $(\delta^{\,b}_C)_*\mu_C$ where $\delta^{\,b}_C$ is a **partial** map with full-measure domain. Ordinary pushforward notation requires a total measurable map. No extension off the null complement and no pushforward of a restricted measure was defined, so the expression was not an instance of any declared operation.
- **Exact affected section:** Definitions 5.1–5.3.
- **Disposition:** **Accepted with Modification** — repaired by construction rather than by restriction.
- **Exact repair:** **Definition 5.2** now constructs the profile on the subspace: with $\Omega:=\Omega^b_C$ and $\mu_C(\Omega)=1$, give $\Omega$ the trace $\sigma$-algebra $\mathcal{F}|_\Omega$, restrict $\mu_C$ to a probability measure $\mu^\Omega_C$ on it, restrict $\delta^{\,b}_C$ to a **total measurable** $\delta^{b,\Omega}_C$, and set $P^b_C:=(\delta^{b,\Omega}_C)_*\mu^\Omega_C$. Observation 5.2.1 records the change. Definition 5.3's case table is reduced to four rows, since $\mu_C(\Omega)<1$ now covers both the empty and the partial branch uniformly.
- **Proof or counterexample:** $\mu_C(\Omega)=1$ makes $\mu^\Omega_C$ a probability measure on $(\Omega,\mathcal{F}|_\Omega)$; $\delta^{b,\Omega}_C$ is total on $\Omega$ by construction and measurable because $\delta^{\,b}_C$ is measurable on its domain and $\mathcal{F}|_\Omega$ is the trace $\sigma$-algebra. The pushforward is then the ordinary one, applied to a total map. **No extension is used, so extension-independence is not needed.**
- **Downstream effect:** Definition 5.3, A5, A9; every context with a contrast undefined only on a null set is now covered, including those the verifier noted were previously outside the definition.
- **Fully closed:** **Yes.**

---

## FV-003 — Theorem 10′ is false for an allowed measurable codomain

- **Severity:** Blocking
- **Exact defect:** Theorem 10′ claimed that for **every** nonempty codomain and every $f:\mathfrak{B}\to W$ some deterministic context realises $\sigma_C=f$. Counterexample: $W=\{0,1\}$ with the equality partial order and the trivial $\sigma$-algebra $\{\emptyset,W\}$ is a codomain under Definition 3.5; it carries exactly one probability measure, so $\delta_0=\delta_1$ as measures, every profile in $\Delta(W)$ is the same object, and the "Dirac-atom reduction" would have to return two different atoms for one input. It is therefore not a function. The second-projection evaluator is measurable but does not cure the collapse.
- **Exact affected section:** Theorem 10′; Corollary 10.1′; Observation 10.0.1; verified-results table; Limitation 14.11.
- **Disposition:** **Accepted with Modification** — narrowed with proof.
- **Exact repair:** New **Definition 3.5.1 (point-separating codomain)** and **Observation 3.5.2** proving point separation equivalent to injectivity of $x\mapsto\delta_x$. New **Definition 3.12.1 (atom reduction)**, defined only for point-separating codomains, with **Observation 3.12.2** recording that it is not a function otherwise. **Theorem 10″** replaces Theorem 10′ with point separation as an explicit hypothesis; the proof is otherwise unchanged and still requires no algebraic structure. **Corollary 10.1″** replaces Corollary 10.1′ with the same restriction. **Observation 10.0** reproduces the counterexample. **Observation 10.0.1** now says explicitly that no statement is made about non-point-separating codomains. **Limitation 14.11′** is narrowed. Theorem 1 and Proposition 11.1′ now declare point separation where they use $\rho^{\mathrm{at}}$ (Borel $\mathbb{R}_{\ge0}$ is point-separating).
- **Proof or counterexample:** The verifier's counterexample was reconstructed and holds: on $\{\emptyset,W\}$ every probability measure assigns $0$ to $\emptyset$ and $1$ to $W$, so $\Delta(W)$ is a singleton. Conversely Observation 3.5.2's equivalence is proved in both directions, so point separation is exactly what makes $\rho^{\mathrm{at}}$ well defined.
- **Downstream effect:** the encodability result and its underdetermination corollary now hold on a strictly smaller class. Every use of the atom reduction elsewhere is on Borel $\mathbb{R}_{\ge0}$, which satisfies the new hypothesis.
- **Fully closed:** **Yes.** Whether point separation is *necessary* as well as sufficient is recorded as **OB-A3**, non-blocking.

---

## FV-004 — The deterministic consistency witness is not closed under its declared morphism

- **Severity:** Blocking
- **Exact defect:** The witness asserted that $\{C_1,C_2,C_0\}$ is closed under $\mathcal{G}=\{\mathrm{id},\jmath\}$ and in particular that $\jmath_*C_0=C_0$. That is false. In $C_0$, $M(x,y)=x$ and both operations shift the second coordinate. Definition 3.17 gives $M_{\jmath_*C_0}(x,y)=y$ and both transported operations as $(x,y)\mapsto(x+1,y)$. These are the components of neither $C_0$ nor $C_1$ nor $C_2$. The statement that the $C_0$ case follows symmetrically established nothing.
- **Exact affected section:** Proposition 11.1 and its proof.
- **Disposition:** **Withdrawn Statement**, with replacement.
- **Exact repair:** **Proposition 11.1 is withdrawn.** **Proposition 11.1′** replaces it. $C_0':=\jmath_*C_0$ is computed explicitly — outcome map $y$, operations $(x,y)\mapsto(x+1,y)$ — and **added to the context set**, giving $\mathcal{C}=\{C_1,C_2,C_0,C_0'\}$. Closure is then **proved**, not asserted, using Observation 3.17.1 (functoriality) and involutivity of $\jmath$: $\jmath_*C_2=(\jmath\circ\jmath)_*C_1=C_1$ and $\jmath_*C_0'=C_0$. Observation 11.1.1 records the false equality and the repair.
- **Proof or counterexample:** The verifier's computation was reproduced independently and is correct. The replacement's closure argument is stated in the proof and rests only on functoriality and $\jmath\circ\jmath=\mathrm{id}$.
- **Downstream effect:** A3 is now checked over **eight** non-identity instances — two bearers for each of four contexts — all of which hold, and $\jmath\neq\mathrm{id}$, so the check is non-vacuous. A4 is satisfied by $C_0$, whose significance values are unchanged. The new context $C_0'$ also yields zero for both bearers.
- **Fully closed:** **Yes.**

---

## FV-005 — Proposition 11.1 does not name all definitions on which it depends

- **Severity:** Major
- **Exact defect:** The proposition declared its fragment as Definitions 3.1–3.12 and 3.15–3.17 plus "the deterministic contrast form", while its axioms and proof used $\delta^{\,b}_C$, $\Omega^b_C$, profiles and $\sigma_C$ — defined only in Definitions 5.1–5.3, which were not in the enumerated fragment. The formal boundary of the claimed fragment was therefore incomplete.
- **Exact affected section:** Proposition 11.1, claim line and satisfaction checks.
- **Disposition:** **Accepted**
- **Exact repair:** Proposition 11.1′ declares its fragment as **Definitions 3.1–3.5, 3.5.1, 3.7–3.12, 3.12.1, 3.15–3.18, 5.1–5.3, 6.1, 7.1, 7.4, 7.5, 7.7 and 8.9**, which is the closure of the objects its statement and proof use. Definitions 3.5.1, 3.12.1 and 3.18 are new in this pass and are included.
- **Proof or counterexample:** None required; the repair is an enumeration. It was checked by reading the proof and listing every defined object it names.
- **Downstream effect:** the Version 1 fragment identity is now closed under its own dependencies, which is what the freeze boundary requires.
- **Fully closed:** **Yes.**

---

## FV-006 — Two retained deterministic limitations or rejections overstate verified results

- **Severity:** Major
- **Exact defect:** Three items. **(i)** Limitation 14.11 depended on the false Theorem 10′. **(ii)** Rejection 16.1 claimed intrinsic significance is rejected because Definition 5.3 writes significance as a function of $(C,b)$ — but a two-argument function may be constant in its first argument, Definition 5.3 does not exclude that, DP-1 is unavailable to proofs, and A4 is compatible with the intrinsic zero valuation. Counterexample: $\sigma_C(b)=0$ for every context and bearer. **(iii)** Rejection 16.13 invoked "artefact relabelling" and a "declared universe", neither defined in the signature; Corollary 6.2 proves only fixed-context orbit constancy for $\mathrm{Aut}(C)$.
- **Exact affected section:** Limitation 14.11; Rejections 16.1 and 16.13.
- **Disposition:** **Accepted with Modification** — one narrowing, two withdrawals.
- **Exact repair:**
 **(i)** Limitation **14.11′** narrowed to point-separating codomains, single context, deterministic form, with explicit "nothing follows for" clauses. Limitation **14.12′** likewise narrowed to the exact instance of Proposition 11.1′.
 **(ii)** Rejection **16.1 is withdrawn.** New **§A.10.2.1** states plainly that **the deterministic core does not exclude intrinsic significance**, reproduces the $\sigma\equiv0$ counterexample, and records that no Part A result replaces the withdrawn rejection. Rejection 16.17 is annotated so it is not read as doing so: it is a claim about the *signature* only.
 **(iii)** Rejection **16.13 is withdrawn as stated**, with the note that what survives is exactly Corollary 6.2 and nothing more.
- **Proof or counterexample:** The $\sigma\equiv0$ assignment is context-independent; it satisfies A4 because $0_W$ is the required null value in a class $\mathsf{W}_1$ codomain; and no Part A axiom excludes it. Verified by checking each of A3, A4, A5, A7, A8, A9, A10 against it.
- **Downstream effect:** §A.10.2 is a new subsection enumerating what the core does **not** establish, so that the withdrawals are visible rather than merely absent.
- **Fully closed:** **Yes.**

---

## Blocking-defect closure

| Finding | Outcome | Detail |
|---|---|---|
| FV-001 | Repaired with proof, axiom narrowed | Definition 3.18 declares $\mathcal{C}$ and $\mathcal{G}$; A3 quantifies over $\mathcal{G}$; closure is an instance requirement |
| FV-003 | Scope narrowed with proof | Theorem 10″ on point-separating codomains; Observation 3.5.2 proves the equivalence that makes $\rho^{\mathrm{at}}$ a function |
| FV-004 | Affected proposition withdrawn and replaced | Proposition 11.1′ adds $C_0'$ and **proves** closure by functoriality and involutivity |

**No Blocking finding was relabelled non-blocking.** No new blocking obligation is created by this pass: OB-A1, OB-A2 and OB-A3 are non-blocking and unused by any Part A theorem.

---

## Effect on the earlier OB register

| Obligation | Status after this pass |
|---|---|
| **OB-1** (full-signature consistency) | **Split.** Its deterministic portion — A3 over the morphism universe — is **discharged** for the core by Definition 3.18 and Proposition 11.1′, which check A3 over the declared $\mathcal{G}$ non-vacuously. Its enrichment portion becomes **OB-B3** and is Candidate, outside the Version 1 claim. |
| **OB-2** (measurability of $\delta^{\,b}_C$) | Superseded for the core: Definition 5.1 now proves $\Omega^b_C\in\mathcal{F}$ and Definition 5.2 gives a measurable restriction. Residual wider-setting question retained as **OB-A2**, non-blocking. |
| **OB-3** (regular evidence structure) | Moved wholly to Part B as **OB-B2**. Not part of the core. |
| **OB-4** (formalise DP-1, DP-2) | Moved wholly to Part B as **OB-B1**. The verifier confirms it does not block the core, since DP-1 and DP-2 are non-formal and unused. |
