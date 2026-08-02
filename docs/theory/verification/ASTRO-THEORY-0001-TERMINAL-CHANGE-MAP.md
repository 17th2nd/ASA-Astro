# ASTRO-THEORY-0001
## Terminal Change Map

Every difference between theory blob `c20ca91fa18551f247dfa1c150dea3f9d9b510d5` (before) and `6fc866796b0a9c39d3f7384d4118fce8ee7ae5ac` (after). Nothing is changed silently.

| Measure | Before | After |
|---|---|---|
| Lines | 505 | 692 |
| Bytes | 52,108 | 85,798 |
| Words | 6,113 | 10,415 |
| Part A lines | 440 | 627 |
| Part B region SHA-256 | `05f1720f…4d5a6c3c` | `05f1720f…4d5a6c3c` — **identical** |
| Git diff | — | 1 file changed, 286 insertions(+), 99 deletions(-) |

**Part B is byte-identical.** Every change below lies in the preamble or Part A.

---

## 1. Preamble

| Item | Before | After | Ground |
|---|---|---|---|
| `Verification` row | "…re-verified as **DETERMINISTIC CORE REQUIRES BOUNDED REMEDIATION** (findings FV-001 – FV-006). This edition remediates those findings…" | Same determination, findings relabelled **TR-1 – TR-6** of the Final Version 1 Verification; "awaits final freeze verification" | NB-4 stale wording |
| `Prior edition` row | Blob `0d64e4fd…` | Blob `c20ca91f…`, pointing at this change map | NB-4 |
| "What changed in this pass" | Description of the FV-001 – FV-006 pass | Rewritten for this pass: TR-1 – TR-6, opening with "terminal formal closure only. No theory redesign, no new result, no novelty claim." | NB-4 |
| `Status`, `Structure`, `Empirical status`, `Novelty`, Freeze boundary | — | **Unchanged** | — |

---

## 2. Repair 1 — extended codomain action (TR-1)

| Location | Before | After |
|---|---|---|
| **Definition 3.16** | One sentence: `$\widehat{\iota_W}:\widehat{W}\to\widehat{W'}$ acts as $\iota_W$ on $W$, as $[u,v]\mapsto[\iota_Wu,\iota_Wv]$ on $\mathcal{I}(W)$, and as the identity on each bottom.` | Typed declaration `$\widehat{\iota_W}:\widehat W\to\widehat W$` with a three-row case table over the summands of Definition 3.8, and the explicit statement that **source and target are both $\widehat W$** and that the unbound $W'$ is removed |
| **Observation 3.16.1** | *did not exist* | **New.** Seven-part verification: (a) totality and case-disjointness; (b) well-definedness on intervals, proved from uniqueness of least and greatest elements; (c) values lie in the target, using (W-a); (d) identity; (e) composition; (f) inverse; (g) consequences for Corollary 6.2, the reduction transport and A3 |

**Undeclared $W'$: removed.** The only surviving occurrences of the symbol are (i) the sentence in Definition 3.16 recording its removal and (ii) the quoted text of the withdrawn Definition 8.9 in Observation 8.9.1, which is explicitly marked as prior-edition text.

**Rechecked, as required:** ordinary values (row 1), intervals (row 2), every bottom (row 3), identity (d), composition (e), inverse (f); transported reductions and A3 (g); Corollary 6.2 (proof rewritten, below); the witness (§7 below).

| Location | Before | After |
|---|---|---|
| **Definition 3.17**, carriers sentence | "$(W_{\iota_*C},\preceq,\Sigma)=(W,\preceq_W,\Sigma_W)$" | "$\mathbb{W}_{\iota_*C}=\mathbb{W}$ — the **whole codomain object, class datum included**", justified by (W-c) |
| **Observation 3.17.0** | "$\rho_{\iota_*C}:\Delta(W)\rightharpoonup\widehat W$" asserted | Same, now derived: pushforward along a measurable isomorphism, then $\rho_C$, then $\widehat{\iota_W}:\widehat W\to\widehat W$ per Definition 3.16 |
| **Corollary 6.2**, proof | "A3 gives $\sigma_{\pi_*C}(\pi_{\mathfrak{B}}b)=\widehat{\mathrm{id}}(\sigma_C(b))=\sigma_C(b)$" | $\widehat{\pi_W}=\mathrm{id}_{\widehat W}$ now **derived** from Observation 3.16.1(d), with both sides typed |
| **A3** | "an equation in $\widehat{W_{\iota_*C}}$" | "an equation **in $\widehat W$**", with each side's membership justified separately |

---

## 3. Repair 2 — complete codomain structure (TR-2)

| Location | Before | After |
|---|---|---|
| **Definition 3.5** | "(Codomain) — primitive, **context-indexed**. A triple … It is of class $\mathsf{W}_1$ if it additionally carries $(\oplus,0_W)$…" | "(Codomain **carrier**) — primitive." The triple only, with "This triple carries **no** algebraic structure; additional structure is never implicit" |
| **Definition 3.6** | *number unused* | **New — Codomain object.** $\mathbb{W}=((W,\preceq_W,\Sigma_W),\mathsf{c})$ with class datum $\mathsf{c}$ exactly one of $\mathsf{W}_1(\oplus,0_W)$ — subject to laws **(M1)–(M5)** stated explicitly — or $\bot_{\mathrm{abs}}$ (class $\mathsf{W}_0$) |
| **Observation 3.6.1** | *did not exist* | **New.** Why selection is a datum: one carrier may admit many operations satisfying (M1)–(M5) and none canonically |
| **Observation 3.6.2** | *did not exist* | **New.** Which laws Part A actually uses — stated honestly: no proof discharges (M1)–(M5) abstractly; they are stated so the class is determinate |
| **Definition 3.5.1** | "(Point-separating **codomain**)… A codomain is point-separating…" | "(Point-separating **carrier**)", with the note that the property is carrier-only and independent of the class datum |
| **Definition 3.10** | 7th slot `$(W_C,\rho_C)$`, "codomain and reduction, context-indexed" | 7th slot `$(\mathbb{W}_C,\rho_C)$`, "codomain object (Definition 3.6) and reduction; fixed to the frame's codomain object by Definition 3.18 clause 3"; component names $W_C,\preceq_{W_C},\Sigma_{W_C},\mathsf{c}_C$ declared |
| **Definition 3.12** | "For $W_C$ realised as $(\mathbb{R}_{\ge0},+,0,\le)$ with the Borel $\sigma$-algebra" | "For $\mathbb{W}_C$ realised as the carrier $(\mathbb{R}_{\ge0},\le,\mathcal{B}(\mathbb{R}_{\ge0}))$ with class datum $\mathsf{c}_C=\mathsf{W}_1(+,0)$" |
| **Definition 3.12.1**, **Observation 3.12.2** | "point-separating **codomain**" | "point-separating **carrier**" |
| **Definition 3.14.1** (frame) | 4th component `$(W,\preceq_W,\Sigma_W)$`, "one codomain" | 4th component `$\mathbb{W}$`, "one **codomain object** … carrier **and** selected class datum"; homogeneity extended to "the frame's codomain object, class datum included" |
| **Definition 3.15**, $\iota_W$ row | Target "$(W,\preceq_W,\Sigma_W)$"; condition "isomorphism of **any declared** class-$\mathsf{W}_1$ structure" | Source and target `$\mathbb{W}$`; condition "automorphism of the codomain object, in the exact sense of (W-a)–(W-c)", where **(W-c)** preserves **exactly the selected** $\mathsf{c}$ — with an explicit branch for $\mathsf{c}=\bot_{\mathrm{abs}}$ imposing **no** condition |
| **Observation 3.15.1** | Closure under composition and inverse asserted for "codomain automorphisms" | Closure **proved** for (W-a), (W-b) and (W-c), with the $\oplus$ and $0_W$ computations shown for both composition and inverse, and the $\mathsf{W}_0$ branch noted |
| **Definition 3.18** clause 3 | "$(W_C,\preceq,\Sigma)=(W,\preceq_W,\Sigma_W)$" | "$\mathbb{W}_C=\mathbb{W}$ — the **whole codomain object, class datum $\mathsf{c}$ included**" |
| **Definition 3.18.3** table | Row `$(W,\preceq_W,\Sigma_W)$ \| codomain`; class-$\mathsf{W}_1$ structure **absent** | Row `$\mathbb{W}$ \| codomain object`, plus sub-rows for the **carrier** and the **class datum $\mathsf{c}$** (required, typed; role: **A4** ($0_W$), Definition 3.15 (W-c), Theorems 1, 7′, Proposition 11.1′) |
| **A4** | "there is $C\in\mathcal{C}$ with $W_C$ of class $\mathsf{W}_1$ and $\sigma_C(b)=0_{W_C}$" | Two-part: the instance class datum **is** $\mathsf{W}_1(\oplus,0_W)$; and for every $b$ there exists $C$ with $\sigma_C(b)=0_W$ |
| **Observation A.3.0** | *did not exist* | **New.** Proves the restatement is **equivalent** under clause 3, and states plainly that a class-$\mathsf{W}_0$ instance **does not satisfy A4** |
| **Theorem 1**, hypotheses | "$W=(\mathbb{R}_{\ge0},+,0,\le)$ Borel — class $\mathsf{W}_1$"; "$r$ not supplied" | Codomain object $\mathbb{W}=((\mathbb{R}_{\ge0},\le,\mathcal{B}),\mathsf{W}_1(+,0))$; "$\mathsf{r}=\bot_{\mathrm{abs}}$" |
| **Theorem 7′**, hypotheses | "A theory instance $\mathbb{T}$; …; $W=(\mathbb{R}_{\ge0},+,0,\le)$" | "A theory instance $\mathbb{T}=(\mathbb{F},\mathsf{r},\mathcal{C},\mathcal{G})$ whose codomain object is $\mathbb{W}=((\mathbb{R}_{\ge0},\le,\mathcal{B}),\mathsf{W}_1(+,0))$" |
| **Theorem 10″** | Hypothesis "a point-separating codomain" | Hypothesis a codomain object "with $\mathsf{c}$ **arbitrary** — either class"; "no algebraic structure is required **and none is used**" |

**W₁ is not required of theorems that do not use it.** Theorem 10″ explicitly admits either class; Theorem 3, Corollary 3.3, Theorem 4′, Theorem 9 and Corollary 6.2 are untouched in this respect.

---

## 4. Repair 3 — cross-context transport removed (TR-3)

**Option A adopted: removal.** See Terminal Adjudication §4.1 for the four grounds.

| Location | Before | After |
|---|---|---|
| **Definition 8.9** | "(Cross-context transport) — optional. A declared order-embedding $t:W_C\to W_{C'}$ with extended action $\widehat t$ per Definition 3.16…" | **Withdrawn.** Replaced in place by **Observation 8.9.1**, which quotes the withdrawn text verbatim and gives three numbered grounds plus the rejection of Option B |
| **A7 (Codomain confinement)** | "Values under $C$ lie in $\widehat{W_C}$; values under distinct contexts are related only through a declared transport (Definition 8.9)." | **Withdrawn.** Replaced by **Observation A.3.2**, recording that clause 1 is literally A5 under homogeneity and clause 2 was not a predicate over any declared component |
| **Observation A.3.1** | "A5, A7, A8, A9, A10 are predicates…"; "Satisfaction of A3–A10" | "A5, A8, A9 and A10…"; axioms of Version 1 stated as exactly **A3, A4, A5, A8, A9, A10**; labels A1, A2, A6, A7 recorded as not in use |
| **Definition 3.18.3** closing sentence | "A5 and A7 over $\widehat W$" | A7 clause removed; "**There is no axiom A7**" recorded, with pointer to Observation 8.9.1 |
| **Definition 3.18.3** table, codomain row | Role "values; A5, **A7**; Defs 3.7, 3.8, 3.11" | Role "values; A5; Defs 3.7, 3.8, 3.11, 3.16" |
| **Limitation 14.7** | "Absent a declared transport (Definition 8.9), values under distinct contexts are not compared. This is the A7 stipulation…" | **Replaced by 14.7′**: Version 1 supplies **no** cross-context comparison apparatus; what it lacks is any warrant for interpreting such a comparison; deferred as OB-A6 |
| **Rejected formulation 16.12** | "*Values under distinct contexts may be compared without a declared transport.* — A7 with Definition 8.9." | **Withdrawn**, under a new "Withdrawn in this pass — TR-3" heading, because its only stated warrant has been removed |
| **Observation 10.1.1** | "…constrained by A3 over $\mathcal{G}$, by A4 over $\mathcal{C}$, and by **A7**." | A7 reference removed; replaced by A5, A8, A9, A10 |
| **Proposition 11.1′** claim | "axioms A3, A4, A5, **A7**, A8, A9, A10 … and **8.9**" | "axioms **A3, A4, A5, A8, A9, A10**"; Definition 8.9 removed from the signature list; explicit note that neither is claimed |
| **Proposition 11.1′** satisfaction | "*A7* — all values lie in $\widehat W$; no cross-context comparison is performed." | **Line deleted** |
| **OB-A6** | *did not exist* | **New.** Records the deferral, its preconditions, and its dependency on OB-A5 |
| **A.11 closing** | "None of OB-A1 – OB-A5 blocks…" | "None of OB-A1 – OB-A6 blocks…" |

**No heterogeneous transport system was introduced.**

---

## 5. Repair 4 — complete instance tuple propagated (TR-4)

| Location | Before | After |
|---|---|---|
| **§A.3 axiom preamble** | `Fix a theory instance $\mathbb{T}=(\mathfrak{B},\mathfrak{M},\mathcal{C},\mathcal{G})$.` | **Replaced** by a *Ranging convention* displaying the complete tuple $\mathbb{T}=(\mathbb{F},\mathsf{r},\mathcal{C},\mathcal{G})$ with $\mathbb{F}$ and $\mathbb{W}$ expanded; "**Every axiom below ranges over this complete tuple**"; the four-component form declared **superseded and withdrawn**, and expressly **not** an abbreviation |
| **Definition 3.18** | Tuple displayed with 4th frame slot `$(W,\preceq_W,\Sigma_W)$` | 4th slot `$\mathbb{W}$`, expanded inline; a **Declared abbreviation** paragraph fixes $\mathbb{F}$ and $\mathbb{T}$ as abbreviations for the displayed components, with "no components other than the seven displayed" |
| **§A.3 homogeneity note** | *did not exist* | **New.** Records $\mathbb{W}_C=\mathbb{W}$, $W_C=W$, $\widehat{W_C}=\widehat W$, so the axioms may be stated in the frame's symbols |
| **Theorem 3.2′** | No applicability clause | **New *Applicability* clause**: supplied-$\mathsf{r}$ branch only; in the absent branch "neither its hypotheses nor its conclusion is a proposition, and **no vacuous truth is inferred**" |
| **Theorem 3.2′**, proof | "Failure of fibre-constancy under totality yields $x$…" | Same, with the intermediate step showing $r^{-1}(x)\cap\Omega^b_C\ne\emptyset$, so Definition 7.5 case 3 applies and the value **is** $\mathcal{S}_C(b,x)$ |
| **Observation 3.18.2** | Single paragraph; named A10 and Definitions 7.1, 7.4, 7.5, 7.7 | Restructured into *Supplied branch* / *Absent branch* / *Unaffected either way*; **Theorem 3.2′ added to both branches**; absent branch states $\mathrm{Id}^b_C$ is **not formed** |
| **Observation 3.2.1** | — | Sentence added: "Nothing is concluded for an instance with $\mathsf{r}=\bot_{\mathrm{abs}}$" |
| **Result register**, row 3.2′ | "Under totality, non-fibre-constancy forces a non-singleton identified set" | "… — **supplied-$\mathsf{r}$ branch only**" |

---

## 6. Repair 5 — identified output typed (TR-4)

| Location | Before | After |
|---|---|---|
| **Definition 3.8** | "$\widehat{W}:=W\sqcup\mathcal{I}(W)\sqcup\{\bot_{\mathrm{ind}},\bot_{\mathrm{inc}},\bot_{\mathrm{und}}\}$, a disjoint union." | Same, plus: it is the carrier of deterministic significance "and of nothing else"; "**$\widehat W$ contains no subset of $W$ other than the order-intervals**", and is **not extended anywhere below** |
| **Definition 3.8.1** | *did not exist* | **New — Identified-output carrier.** $\widehat{W}^{\mathrm{id}}:=\mathcal{P}_{\neq\emptyset}(W)\sqcup\{\bot_{\mathrm{inc}},\bot_{\mathrm{und}}\}$ |
| **Observation 3.8.2** | *did not exist* | **New.** The two output carriers are distinct; neither is a subobject of the other; no identified output is placed in $\widehat W$ |
| **Definition 7.5** | One sentence, three unlabelled cases, **no symbol, no domain, no codomain**, returning a bare subset | Full declaration: *Applicability*; the function $\mathrm{Id}^b_C:\mathcal{R}\to\widehat{W}^{\mathrm{id}}$; domain, codomain and totality stated; three cases in a table |
| **Observation 7.5.1** | *did not exist* | **New.** (a) totality; (b) every value lies in the declared codomain; (c) **no carrier is overloaded**, with the reason a single-valued design was rejected; (d) $\mathrm{Id}^b_C$ and $\sigma_C$ are distinct functions; (e) no measurability is asserted or used |
| **A10** | "the identified output at $x$ is $\bot_{\mathrm{inc}}$" — prose, untyped | "$\mathrm{Id}^b_C(x)=\bot_{\mathrm{inc}}$", with the function's type displayed and $C$, $b$, $x$ explicitly quantified |
| **Theorem 3.2′**, conclusion | "$\lvert\mathcal{S}_C(b,x)\rvert\ge2$" | "$\mathrm{Id}^b_C(x)=\mathcal{S}_C(b,x)\in\mathcal{P}_{\neq\emptyset}(W)$ satisfying $\lvert\mathcal{S}_C(b,x)\rvert\ge2$" |
| **Definition 3.18.4** | *did not exist* | **New — Derived-object table.** Twelve derived objects with declared type, totality and formation condition, including $\widehat{\iota_W}$, $\sigma_C$ (total), $\mathcal{H}_r$ and $\mathrm{Id}^b_C$ |

---

## 7. Consistency proposition recomputed (TR-6)

| Location | Before | After |
|---|---|---|
| **Claim** | Axioms A3, A4, A5, A7, A8, A9, A10; Definitions "3.1–3.5, 3.5.1, 3.7–3.12, 3.12.1, 3.14.1, 3.15, 3.16, 3.17, 3.18, 3.18.3, 5.1–5.3, 6.1, 7.1, 7.4, 7.5, 7.7 and 8.9" | Axioms **A3, A4, A5, A8, A9, A10**; Definitions "3.1–3.5, 3.5.1, **3.6**, 3.7, 3.8, **3.8.1**, 3.9–3.12, 3.12.1, 3.14.1, 3.15, 3.16, 3.17, 3.18, 3.18.3, **3.18.4**, 5.1–5.3, 6.1, 7.1, 7.4, 7.5 and 7.7" — **exactly the 30 declared Definitions**, with 8.9 removed |
| **Proof opening** | "component by component" | Adds "**Every datum below is supplied through a declared slot of the tuple; no structure is introduced in prose.**" |
| **Frame** | "$(W,\preceq_W,\Sigma_W)=(\mathbb{R}_{\ge0},\le)$ … **carrying $(+,0)$ so that it is of class $\mathsf{W}_1$**" — prose | Codomain object supplied as the fourth frame slot: $\mathbb{W}=((\mathbb{R}_{\ge0},\le,\mathcal{B}),\ \mathsf{c})$ with $\mathsf{c}:=\mathsf{W}_1(+,0)$, and **(M1)–(M5) verified individually** |
| **Representation component** | — | Adds that the instance is in the supplied branch and $\mathrm{Id}^b_C$ is formed; Theorem 3.2′ added to the interpreted list |
| **Morphism group** | "$\jmath_W$ is an automorphism of $(W,\preceq_W,\Sigma_W)$ preserving $+$ and $0$" | "$\jmath_W$ is an automorphism of the **codomain object** $\mathbb{W}$", with **(W-a)**, **(W-b)**, **(W-c)** checked separately; a new *Extended action* paragraph derives $\widehat{\jmath_W}=\mathrm{id}_{\widehat W}$ from Observation 3.16.1(d) |
| **Shared context components** | "Every context uses the frame's $(\mathcal{Y},\mathcal{G}_{\mathcal{Y}})$ and $(W,\preceq_W,\Sigma_W)$" | "$\mathbb{W}_C=\mathbb{W}$ — **the whole codomain object, class datum included**"; $\rho^{\mathrm{at}}$ domain stated |
| **Contexts** | Four contexts, transports computed inline in prose | Restructured: two given outright, two defined as transports |
| **Transport recomputation** | *did not exist as a systematic check* | **New seven-row table** recomputing **every** slot — $\mu$, $M$, $T$, $\approx$, $\delta$, $\rho$, carriers — under Definition 3.17, followed by the five explicit $M$ and $T$ computations |
| **Closure** | "$\mathrm{id}_*C=C$" | "$\mathbf{1}_*C=C$" (notation aligned with Observation 3.15.1); otherwise unchanged, involutivity argument retained |
| **Significance values** | "All contrasts are total and all profiles are Dirac" | Adds the explicit route through Definition 5.3 row four ($\Omega^b_C=\mathfrak{M}$, $\mu_C(\Omega^b_C)=1$, $P^b_C\in\operatorname{dom}\rho^{\mathrm{at}}$) |
| **A3 check** | Six bullet lines, two collapsing $b_i$ | **Eight separately numbered equations**, each pair written out; identity case now justified by Observation 3.16.1(d) |
| **A4 check** | "$C_0\in\mathcal{C}$ has $W$ of class $\mathsf{W}_1$ and $\sigma_{C_0}(b_i)=0_W$" | **Both conjuncts** checked: the class datum is $\mathsf{W}_1(+,0)$ supplied in the frame slot; and $C_0$ gives $0_W$, the **selected** identity |
| **A7 check** | Present | **Deleted** |
| **A8, A9 checks** | "vacuous" / "every $\Omega^b_C\ne\emptyset$" | Restated as "antecedent false … A8 holds" / "antecedent false … A9 holds" |
| **A10 check** | "every fibre is a singleton and none is empty" | Adds that Definition 7.5 case 3 applies at every $x$, giving $\mathrm{Id}^b_C(x)=\{\delta^{\,b}_C(x)\}$, and states plainly that **A10 holds vacuously in this instance** |
| **Observation 11.1.3** | *did not exist* | **New.** Six-row table mapping every witness datum to the declared slot it arrives through, plus "**No structure is added in explanatory prose**" |
| **Observation 11.1.2** | "non-point-separating codomains, or codomains outside class $\mathsf{W}_1$" | "non-point-separating **carriers**, or codomain objects of class $\mathsf{W}_0$" |

**Numerical results are unchanged.** All four contexts, both group elements, every transport, every contrast, every profile, all six significance values and all eight non-identity A3 equations recompute to exactly the values recorded in the final verification report §11.

---

## 8. Repair 6 — encodability narrowed (TR-5)

| Location | Before | After |
|---|---|---|
| **Theorem 10″**, conclusion | "There is a context $C$ with $W_C=W$ and $\sigma_C(b)=f(b)$" | "There are a **frame** $\mathbb{F}_f$ and a **single** context $C$ over $\mathbb{F}_f$ with $\mathbb{W}_C=\mathbb{W}$ and $\sigma_C(b)=f(b)$" — frame made explicit |
| **Observation 10.0.2** | *did not exist* | **New.** Theorem 10″ constructs a context, **not** a theory instance; **no axiom is asserted or checked**; A4 could not be satisfied at all when $\mathsf{c}=\bot_{\mathrm{abs}}$ |
| **Corollary 10.1″** | "…no single-context assignment $f:\mathfrak{B}\to W$ is **excluded by the axioms**." | "…the single-context construction of Theorem 10″ **realises** $f$, so no assignment $f$ is excluded by **the requirement that it be realised by some context of the deterministic contrast form**." |
| **Observation 10.1.0** | *did not exist* | **New.** Records that the prior conclusion **exceeded its proof and is withdrawn**; gives the A4 + homogeneity obstruction; records that **Option B** was adopted and why A and C were rejected; states that the phrase "the axioms exclude no assignment" does not occur in Version 1 |
| **Observation 10.0.1** | "the axioms therefore do not exclude degenerate evaluators" | "the **deterministic contrast form** therefore does not itself exclude degenerate evaluators"; adds "**No claim is made that the axioms fail to exclude such an assignment**" |
| **Observation 10.1.1** | "concerns one context, one form, and point-separating codomains only" | Adds "and speaks of **realisability by a construction** rather than of consistency with the axioms"; lists A5, A8, A9, A10 as unverified by Theorem 10″ |
| **Limitation 14.11′** | "no single-context assignment is excluded (Corollary 10.1″)" | "every single-context assignment is **realised by the construction**"; adds "**Nothing follows about exclusion by the axioms**" and the class-$\mathsf{W}_0$ counter-case |
| **Result register**, row 10″ | "Encodability on point-separating codomains" | "Encodability on point-separating carriers — **context-existence only; no axiom is verified**" |
| **§A.10.2.1** | "The assignment $\sigma_C(b)=0$ … satisfies A4" | Qualified: "In an instance whose codomain object is of class $\mathsf{W}_1$ — as A4 requires (Observation A.3.0) — the assignment $\sigma_C(b)=0_W$ …" |
| **Observation 10.0** | "$W=\{0,1\}$ … is a **codomain** under Definition 3.5" | "… is a **codomain carrier** under Definition 3.5" |

---

## 9. Non-blocking cleanup

| № | Location | Before | After |
|---|---|---|---|
| NB-1 | **Definition 5.3** heading | "derived, **partial**" | "derived, **total**"; declares $\sigma_C:\mathfrak{B}\to\widehat W$ total |
| NB-1 | **Definition 5.3** closing | "The four cases partition every possibility and agree with A9." | A **Totality** paragraph proving mutual exclusivity and exhaustiveness, recording that the prior label was a terminology error, and locating A9's antecedent in case 2 |
| NB-2 | **A5** | "$\sigma_C(b)\in\widehat{W_C}$" | "For every $C\in\mathcal{C}$ and every $b\in\mathfrak{B}$: $\sigma_C(b)\in\widehat W$" |
| NB-2 | **A8** | "If $\approx_C\neq\bot_{\mathrm{abs}}$, then for $(y,y')\dots$" | "For every $C\in\mathcal{C}$: if … then **for all** $(y,y')\dots$" |
| NB-2 | **A9** | "If $\Omega^b_C=\emptyset$ then …" | "For every $C\in\mathcal{C}$ and every $b\in\mathfrak{B}$ with $T_C(b)$ defined: if …" |
| NB-2 | **A10** | Implicit $C$, $b$ | "for every $C\in\mathcal{C}$, every $b\in\mathfrak{B}$ with $T_C(b)$ defined, and every $x\in\mathcal{R}$" |
| NB-2 | **A7** | Implicit $C$, $b$ | Withdrawn; no quantifier owed |
| NB-3 | **§A.2.5 order** | Observation 3.18.2 → Definition 3.18.3 → Observation 3.18.1 | Observation 3.18.1 → Observation 3.18.2 → Definition 3.18.3 → Definition 3.18.4 |
| NB-4 | **Definition 6.1** | "$\pi_W=\mathrm{id}_{W_C}$" | "$\pi_W=\mathrm{id}_W$" |
| NB-4 | **Definition 3.18.3** | $\bot_{\mathrm{abs}}$ omitted from the table | Row added: symbol (Def 3.9), required, global; role "typed absence of $\mathsf{c}$, $\mathsf{r}$, $\approx_C$; FR-1" |
| NB-4 | **§A.10.4 heading** | "Withdrawn in this pass — FV-006." | "Withdrawn in the **prior** pass — FV-006", with a new "Withdrawn in this pass — TR-3" heading for 16.12 |

### Declaration-label changes

| Before | After | Reason |
|---|---|---|
| *(new)* | Definition 3.6, Observations 3.6.1, 3.6.2 | Repair 2; number 3.6 was an unused gap |
| *(new)* | Definition 3.8.1, Observation 3.8.2 | Repair 5 |
| *(new)* | Observation 3.16.1 | Repair 1 |
| *(new)* | Definition 3.18.4 | Repair 5 |
| *(new)* | Observations A.3.0, A.3.2 | Repairs 2 and 3; numbered so §A.3 reads monotonically with A.3.1 unchanged |
| *(new)* | Observation 7.5.1 | Repair 5 |
| *(new)* | Observation 8.9.1 | Repair 3, replacing Definition 8.9 in place |
| *(new)* | Observations 10.0.2, 10.1.0 | Repair 6 |
| *(new)* | Observation 11.1.3 | Consistency proposition |
| *(new)* | OB-A6 | Repair 3 deferral |
| Definition 8.9 | *withdrawn; label not reused* | Repair 3 |
| A7 | *withdrawn; label not reused* | Repair 3 |
| 16.12 | *withdrawn* | Repair 3 consequence |
| 14.7 | 14.7′ | Repair 3 consequence |

**No existing declaration was renumbered.** Every label present in the prior edition either survives with its number or is explicitly withdrawn above. Observations 10.0.1, 10.1.1 and 11.1.2 were **moved** so that their sections read in ascending order; their labels and content-identity are preserved.
