# ASTRO-V1 Research Controls Freeze Report

## Document control

| Field | Value |
|---|---|
| Report identifier | `ASTRO-V1-RESEARCH-CONTROLS-FREEZE-REPORT` |
| Date | 2026-08-01 |
| Repository | `17th2nd/ASA-Astro` |
| Authorised baseline | `6de6a446d2df2804e6b824ae01bba62ef37c5b69` |
| Publication branch | `main` |
| Freeze scope | ASA-Astro Research Controls Version 1 |
| Theory scope | `ASTRO-THEORY-0001` and its two supporting records excluded |
| Experiments executed | `0` |
| Empirical results | `0` |
| Evidence level | `EH-0` |
| Disposition | **ASA-ASTRO RESEARCH CONTROLS V1 FROZEN WITH RECORDED NON-BLOCKING ISSUES** |

## 1. Freeze unit

The coherent Version 1 freeze unit consists only of:

1. `09_Drafts/Codex/ASTRO-EXP-0001_Minimum-Validation-Programme.md`
2. `09_Drafts/Codex/2026-08-01_Codex_ASTRO-PRIOR-ART-0001.md`
3. `README.md`
4. `docs/claims/ASTRO-CLAIMS-0001.md`
5. `validation/benchmarks/ASTRO-EXP-0001.md`
6. `validation/results/ASTRO-RESULTS-0001.md`
7. `reports/ASTRO-V1-RESEARCH-CONTROLS-FREEZE-REPORT.md`

No directory-wide staging is authorised. No file under `docs/theory/` is part
of the freeze unit.

## 2. Canonical baseline preflight

Immediately before report creation, two independent live-remote checks and
two local checkpoints established:

- live `refs/heads/main`:
  `6de6a446d2df2804e6b824ae01bba62ef37c5b69`;
- local `HEAD`:
  `6de6a446d2df2804e6b824ae01bba62ef37c5b69`;
- local `origin/main`:
  `6de6a446d2df2804e6b824ae01bba62ef37c5b69`;
- branch: `main`;
- ahead/behind: `0/0`;
- staged files: `0`;
- the six pre-existing freeze-candidate files were present;
- the three theory records were tracked and clean;
- candidate and theory blob hashes were unchanged between the two local
  checkpoints;
- no concurrent canonical or local content mutation was detected during the
  audit interval.

The authorised baseline commit changed only:

- `docs/theory/ASTRO-THEORY-0001.md`;
- `docs/theory/ASTRO-THEORY-0001-FORMAL-DEFECT-RESOLUTION.md`;
- `docs/theory/ASTRO-THEORY-0001-CHANGE-MAP.md`.

## 3. Theory-impact determination

The three theory records do **not** materially alter a meaning, identifier,
dependency, or status used by `ASTRO-EXP-0001`, `ASTRO-CLAIMS-0001`, or
`ASTRO-RESULTS-0001`.

Evidence for that determination:

- none of the three research-control records references `ASTRO-THEORY-0001`
  or a path under `docs/theory/`;
- none of the theory records defines or changes an `ASTRO-CLM-*`,
  `ASTRO-EXP-*`, `ASTRO-RES-*`, `ASTRO-EVD-*`, or `AR1-E*` control identifier;
- the theory candidate declares itself not frozen, not Version 1, not
  empirically validated, and without a novelty claim;
- the theory candidate proves that its unrestricted framework has no empirical
  content and assigns predictive content only to independently constrained
  instantiations;
- the experiment protocol independently excludes mathematical novelty, graph
  novelty, composition rules, and general architectural validity from its
  tested scope;
- the claims registry and results ledger retain their own source, dependency,
  status, authority, and evidence rules without importing theory authority.

The baseline theory blobs audited and excluded were:

| File | Git blob |
|---|---|
| `docs/theory/ASTRO-THEORY-0001.md` | `08a2257aaea6e5f23b316682025022b62d834d68` |
| `docs/theory/ASTRO-THEORY-0001-FORMAL-DEFECT-RESOLUTION.md` | `f68b201d6277f2cc215b549289588943cfd19713` |
| `docs/theory/ASTRO-THEORY-0001-CHANGE-MAP.md` | `995874d650367124eb6e868ca31bf124a45419b6` |

`ASTRO-THEORY-0001` therefore remains a **Theory Candidate** outside the
Research Controls Version 1 freeze.

## 4. Preserved candidate identity

The previously audited freeze-candidate content did not change across the
rebaseline audit. Its pre-commit Git blobs were:

| File | Git blob |
|---|---|
| `09_Drafts/Codex/ASTRO-EXP-0001_Minimum-Validation-Programme.md` | `2b8ce547f3b7ff6d495e6c8e39efee0025f4cf95` |
| `README.md` | `b47f19d3293a586bff31ba7dd01d45bc97bbeb44` |
| `09_Drafts/Codex/2026-08-01_Codex_ASTRO-PRIOR-ART-0001.md` | `64fe1d288bd94c71ec9eb6bfcab79f98c33ad85d` |
| `docs/claims/ASTRO-CLAIMS-0001.md` | `f1b4d94527cec10c650358036a0009bd5e4e46cc` |
| `validation/benchmarks/ASTRO-EXP-0001.md` | `8b6606947421cfa96a572bb45726be4d4f3e51ce` |
| `validation/results/ASTRO-RESULTS-0001.md` | `c1a3739119bd56e5cdf745243970f78e0848848d` |

## 5. Statistical audit

The completed statistical audit evidence is preserved:

- one-sided binomial alpha at 20 or more wins under
  $X\sim\operatorname{Binomial}(27,0.5)$:
  `0.0095786452293396`;
- power at a true material-win probability of `0.8`:
  `0.8444402928110182`;
- exhaustive enumeration found no qualifying sample-and-threshold pair with
  fewer than 27 targets;
- at 27 targets, threshold 19 fails the alpha bound, threshold 20 satisfies
  both bounds, and threshold 21 fails the power bound;
- 27 targets and a 20-win threshold are therefore the smallest integer pair
  meeting both declared bounds.

The exact rational power is

`251662818435137536 / 298023223876953125`

or `0.8444402928110168862359552...`. The frozen decimal differs at approximately
`1.3e-15`, consistent with floating-library evaluation, and does not affect the
declared power bound or design decision. This is recorded as non-blocking and
the already audited protocol text is unchanged.

## 6. Claims-registry audit

The claims registry contains:

- 72 headings of the form `ASTRO-CLM-NNNN`;
- 72 matching identifier fields;
- 72 unique identifiers forming the complete continuous range
  `ASTRO-CLM-0001` through `ASTRO-CLM-0072`;
- 72 status fields;
- no missing or duplicate claim identifier;
- no unresolved claim dependency reference;
- every required registry field in every claim record.

Status distribution:

| Status | Count |
|---|---:|
| Retained | 22 |
| Rejected | 15 |
| Untested | 9 |
| Open | 6 |
| Withdrawn | 20 |
| **Total** | **72** |

The experiment claims `ASTRO-CLM-0070`, `ASTRO-CLM-0071`, and
`ASTRO-CLM-0072` remain `Untested`.

## 7. Results-ledger audit

The append-only stream contains exactly three establishment events:

1. `AR1-E000001` — `LEDGER_ESTABLISHED`;
2. `AR1-E000002` — `EXPERIMENT_REGISTERED`;
3. `AR1-E000003` — `CLAIM_REGISTERED`.

All three YAML records parse, contain every mandatory event-envelope key, use
the declared schema version, and form a complete sequential
`previous_event_id` chain. No execution, result, evidence, dataset,
calibration, replication, reproduction, or publication event has been added.

The state at freeze remains:

- experiments executed: `0`;
- empirical results: `0`;
- evidence level: `EH-0`.

## 8. Link audit

After creation of this report, all 20 local Markdown links in the six source
records and the three baseline theory records resolve. The only three missing
local targets before report creation were the deliberate forward references to
this report from the protocol, claims registry, and results ledger.

The live external-link recheck covered 68 unique HTTP(S) targets:

| Result | Count |
|---|---:|
| HTTP 200 | 47 |
| HTTP 202 | 2 |
| HTTP 403 after redirect | 19 |
| HTTP 404 | 0 |
| Connection or DNS failure | 0 |
| **Total** | **68** |

The 19 HTTP 403 results are publisher or resolver access controls encountered
by the automated HEAD audit. They are recorded as non-blocking because the
targets responded and none returned 404 or failed resolution.

## 9. Content and scope checks

- `git diff --check` passed before report creation.
- The historical draft now delegates authority to the canonical protocol and
  retains no operative endpoint or claim.
- `README.md` identifies the canonical protocol, claims registry, and results
  ledger.
- The protocol has one hypothesis, one endpoint, no secondary endpoint, and
  one terminal programme rule.
- No empirical event is inferred from protocol or claim registration.
- No software result or pre-existing phase-2 artefact is treated as execution
  of the frozen protocol.
- No theory record belongs to the freeze unit.

## 10. Non-blocking issues

Two non-blocking audit observations are recorded:

1. the frozen power decimal reflects floating-library evaluation and differs
   from the exact rational expansion only beyond the precision material to the
   declared bound;
2. 19 external targets deny automated HEAD access with HTTP 403 after
   redirection, while returning no evidence of a missing target.

Neither changes an identifier, dependency, status, endpoint, threshold,
authority boundary, empirical state, or freeze decision.

## 11. Publication conditions

Publication is authorised only when all of the following hold immediately
before commit and push:

- live `origin/main`, local `origin/main`, and the commit parent remain
  `6de6a446d2df2804e6b824ae01bba62ef37c5b69`;
- staged scope equals exactly the seven files in §1;
- `git diff --cached --check` passes;
- no path under `docs/theory/` is staged;
- the push is a direct fast-forward of `main`;
- no branch is created.

Post-publication verification must establish that local `HEAD`, live
`origin/main`, and the published GitHub `main` ref are identical; the published
tree contains the seven intended paths with matching blobs; and no unrelated
or theory path appears in the freeze commit.
