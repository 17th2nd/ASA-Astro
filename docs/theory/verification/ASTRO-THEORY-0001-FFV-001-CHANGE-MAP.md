# ASTRO-THEORY-0001
## FFV-001 Change Map

Every difference between theory blob `6fc866796b0a9c39d3f7384d4118fce8ee7ae5ac` (before) and `69a7846614847f479962827557924a31b4b45b26` (after). Nothing is changed silently.

| Measure | Before | After |
|---|---|---|
| Lines | 692 | 709 |
| Bytes | 85,798 | 89,425 |
| Words | 10,415 | 10,954 |
| Part A lines | 627 | 644 |
| Part A Definition declarations | 30 | **29** |
| Part B region SHA-256 | `05f1720f…4d5a6c3c` | `05f1720f…4d5a6c3c` — **identical** |
| Git diff | — | 1 file changed, 28 insertions(+), 11 deletions(-) |

**Ten hunks, all listed below.** Part B is byte-identical.

---

## 1. The withdrawal — §A.6

| Location | Before | After |
|---|---|---|
| **Definition 7.7** | `**Definition 7.7 (Four distinct notions).** (i) sufficiency; (ii) minimal sufficiency relative to $\delta^{\,b}_C$; (iii) the distinguishability indicator on $\Omega^b_C\times\Omega^b_C$; (iv) the partition of $\Omega^b_C$ by equality of $\delta^{\,b}_C$. **No minimality is claimed anywhere.**` | **Withdrawn.** Replaced in place by **Observation 7.7.1**, which quotes the withdrawn declaration verbatim in a blockquote and gives four numbered grounds, a statement that nothing retained uses the withdrawn notions, and the reason completion was rejected |

Observation 7.7.1 records, per notion:

| Notion | Disposition recorded |
|---|---|
| (i) sufficiency | **Retained** — already complete in Definition 7.4; clause (i) added nothing; every use of "sufficient" in Part A refers to Definition 7.4 and to no other |
| (ii) minimal sufficiency | **Not part of Version 1.** Named no admissible class, comparison relation or minimality predicate |
| (iii) distinguishability indicator | **Not part of Version 1.** No symbol, codomain or value rule; occurs nowhere else in Part A |
| (iv) equality partition | **Not part of Version 1.** No symbol or quotient notation; expressly distinguished from Theorem 4′'s quotient by $\approx_C$, which is fully defined |

---

## 2. Propagation — every remaining reference

| Location | Before | After |
|---|---|---|
| **Observation 3.18.2**, supplied branch | "**Definitions 7.1, 7.4, 7.5 and 7.7**" | "**Definitions 7.1, 7.4 and 7.5**" |
| **Definition 3.18.3**, `$\mathsf{r}$` row | "A10; Defs 7.1, 7.4, 7.5, 7.7; Thm 3.2′; Prop 11.1′" | "A10; Defs 7.1, 7.4, 7.5; Thm 3.2′; Prop 11.1′" |
| **Proposition 11.1′**, claim | "…6.1, 7.1, 7.4, 7.5 and 7.7**. There is no axiom A7 and no Definition 8.9 in Version 1 (Observations A.3.2, 8.9.1), so neither is claimed." | "…6.1, 7.1, 7.4 and 7.5**. There is no axiom A7, no Definition 8.9 and no Definition 7.7 in Version 1 (Observations A.3.2, 8.9.1, 7.7.1), so none is claimed. **Every definition named above is complete**, and each is instantiated by the witness below." |
| **Proposition 11.1′**, representation paragraph | "A10, Theorem 3.2′ and Definitions 7.4, 7.5 and 7.7 are interpreted with this $r$" | "A10, Theorem 3.2′ and Definitions 7.4 and 7.5 are interpreted with this $r$" |
| **OB-A4** | "A10 and Definitions 7.1–7.7 do not mention $\mathcal{G}$" | "A10 and Definitions 7.1–7.5 do not mention $\mathcal{G}$" |

**No other occurrence of `7.7` existed.** After repair, every surviving occurrence is either the withdrawal record itself, the preamble note, the Proposition 11.1′ exclusion clause, or OB-A7 — none is a live use.

---

## 3. Open obligation added

| Location | Before | After |
|---|---|---|
| **OB-A7** | *did not exist* | **New.** Defers formal treatment of the three withdrawn notions, and states what any such treatment must supply: symbol, domain, codomain and complete rule for each, plus an admissible class, comparison relation and minimality predicate for minimal sufficiency. Records that none is consumed by any retained Part A statement, and restates that **no minimality result is claimed by Version 1** |
| **§A.11 closing** | "None of OB-A1 – OB-A6 blocks the deterministic core" | "None of OB-A1 – OB-A7 blocks the deterministic core" |

---

## 4. Preamble

| Item | Before | After |
|---|---|---|
| `Verification` row | "…independently verified as **DETERMINISTIC CORE REQUIRES BOUNDED REMEDIATION** (blocking findings TR-1 – TR-6…). This edition closes those findings and awaits final freeze verification." | Records the freeze examination and its determination **NOT READY FOR VERSION 1** on the single blocking defect **FFV-001**; notes that the examination established no contradiction, no failed witness, no theorem exceeding its proof and no Part B dependency; "This edition closes FFV-001 and awaits re-verification." |
| `Novelty` row | "No novelty is claimed. No universal prior-art subsumption is claimed." | Same, plus "**No minimality is claimed.**" |
| `Prior edition` row | Blob `c20ca91f…`, pointing at the terminal change map | Blob `6fc86679…`, pointing at this change map |
| "What changed in this pass" | Description of the TR-1 – TR-6 terminal-closure pass | Rewritten: micro-remediation of one defect; the withdrawal and its ground; sufficiency retained in Definition 7.4; the three notions deferred as OB-A7; an explicit statement that **nothing else changed** and that **FFV-NB-001 is deliberately not corrected** |
| `Status`, `Structure`, `Empirical status`, Freeze boundary | — | **Unchanged** |

---

## 5. What did not change

Verified by inspection of the ten diff hunks — none touches any of the following:

| Preserved unchanged | Evidence |
|---|---|
| All six axioms A3, A4, A5, A8, A9, A10 | No hunk falls in §A.3's axiom block |
| Every theorem, corollary and proposition **statement and proof** | No hunk falls in any theorem or proof |
| The consistency witness | Frame, codomain object, representation component, group, all four contexts, every transport, all six significance values, all eight A3 equations and every axiom check are byte-identical |
| Codomain structure (Definitions 3.5, 3.6, 3.8, 3.8.1) | Untouched |
| Transport and morphism rules (Definitions 3.15–3.17) | Untouched |
| Representation component (Definition 3.18 clause 2, Definitions 7.1, 7.4, 7.5) | Untouched — Definition 7.4 in particular is **byte-identical**, which is what preserves sufficiency |
| Result register, limitations, rejected formulations | Untouched — none referenced Definition 7.7 |
| Part B | Byte-identical; region SHA-256 unchanged |
| Theorem 1's surplus $\mathsf{r}=\bot_{\mathrm{abs}}$ hypothesis (FFV-NB-001) | **Deliberately untouched**, outside the authorised scope |

### Declaration-label changes

| Before | After | Reason |
|---|---|---|
| Definition 7.7 | *withdrawn; label not reused* | FFV-001 |
| *(new)* | Observation 7.7.1 | Withdrawal record, replacing Definition 7.7 in place |
| *(new)* | OB-A7 | Deferral of the three withdrawn notions |

**No existing declaration was renumbered or moved.** Part A Definition declarations fall from 30 to 29, and the Proposition 11.1′ signature list names exactly those 29 — verified in both directions with no declared-but-unclaimed and no claimed-but-undeclared entry.
