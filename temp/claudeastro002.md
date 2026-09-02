# claudeastro002 — Build report: Slice 1 and Slice 2

Programme: CLAUDE-ASTRO-BUILD-001 · Operator: Claude · Date: 2026-09-03

```
ASTRO_HEAD    = c373352bfdd6859523c5b225469ecc1b143649d9   (13 commits on 549ee742; this report is committed after it)
ASA_BASELINE  = b855d4c730dc2553db7a693d91c7d4d0cf25d03c   (17th2nd/ASA kernel/v0.1-alpha, kernel 0.1.0-alpha10)
```

## Outcome

The product success condition in the directive (§28) is met on synthetic data, end to end, deterministically,
and reproduced from a fresh clone:

| Step | Evidence |
|---|---|
| A fixed universe is presented | `data/universe/slice1.json` → `UNI-acd79bc7…` (14 entities, 16 evidence, 9 relationships, all labelled `synthetic`) |
| Only the objective changes | Objectives A/B/C/D evaluated against the same universe and context; ASA kernel digest `sha256:f602ff30…` identical before and after all four |
| ASA changes what is significant | Top target per objective: A → SYN-HOST-A · B → SYN-TR-2026a · C → SYN-VAR-D · D → SYN-STD-C |
| Astro changes what work it does | Plans: observe_transit HOST-A · classify_transient TR-2026a · time_series_block VAR-D, GIANT-F · observe_calibrator STD-C |
| Every decision traces to evidence and relationships | `AstroDecisionReceipt` carries objective, context, universe, kernel digest/head, registry digest, ASA baseline, Astro commit, candidate/evidence/relationship digests, per-target contributions, eligibility record, evidence ids, ASA relationship keys, explanations |
| New evidence changes the next decision | Corrected HOST-A ephemeris (supersedes) + refined HOST-B ephemeris → plan flips HOST-A → HOST-B; identities unchanged |
| Deterministic, inspectable | Fresh clone: receipt `RCPT-62f1ca80…` byte-identical to the local run; session ids identical across fresh kernels |

## What was built (all under `src/astro/`, Astro-owned)

| Package | Content |
|---|---|
| `astro.domain` | Entity (19 kinds; identity = kind + designation + catalogue ids), EvidenceRecord (11 kinds; status is lifecycle, not identity), RelationshipAssertion (10 typed, role-explicit, evidence-cited), EntityState, immutable digest-identified Universe with `with_evidence / with_relationships / with_states / supersede_evidence`. `IntrinsicSignificanceError` rejects any significance/priority/importance/rank/score field. |
| `astro.objectives` | Objective (content-identified declaration: purpose, question, authority, target kinds, required evidence, eligible relationship types + stance policy, features with weight and rationale, immutable `WPOL-` weighting ref, missingness, exclusions, plan policy), ObservingContext, JSON loaders. |
| `astro.asa` | Pinned-baseline locator; AstroAdapter (entities/evidence → UAOs; relationships → `supported` UROs endorsed by `asa.core/supports` from cited evidence; evidence-of / observed-with / observation-state → definitional UROs; status sync; reloads append nothing); RelationalSnapshot read model. Imports only `asa_kernel.api / identity / storage`. |
| `registry/` | Astro relationship-type facet (12 domain types + 5 core meta-types) composed and validated by ASA's own `compose_domain`; `--check` byte-stable, digest `sha256:52f78361…`. |
| `astro.significance` | 14 deterministic features, each returning value/status/trace; evaluator with eligibility rules, missingness policy, weighted score, rank, full contribution record; `explain()` renders recorded state only. |
| `astro.execution` | plan (budgets, `min_score`, `min_repeat_gap_hours` from ASA state, skip reasons), schedule (visibility intervals, no overlaps, transit-centred), SimulatedExecutor (facts about the observation only; labelled `simulated`). |
| `astro.session` | evaluate → plan → schedule → execute → new universe → re-evaluate; every cycle receipted; universes chained. |
| `astro.receipts`, `astro.pipeline`, `astro.cli` | receipts with canonical JSON + sha256; `astro version | evaluate | explain | session | demo {context-switch, evidence-arrival, session}`. |

## Tests

| Suite | Count | Fresh clone |
|---|---|---|
| `tests/astro` (domain 11, adapter 8, significance 15, execution 9) | 43 | 43 |
| `tests/exec` (unchanged Phase 2 skeleton) | 38 | 38 |
| legacy `tests/unit`, `tests/reasoning`, `tests/integration` | green | — |
| Frozen artefacts (`astro-exec validate-frozen`) | 6/6 verified | — |
| Pinned kernel self-test at baseline | 66 | — |

§17 coverage: identity invariance · no intrinsic significance · context sensitivity · evidence sensitivity ·
relationship sensitivity (endorsed changes rank; unevaluated does not) · determinism · provenance · boundary
compliance (AST scan: no `asa_astro`, kernel only via the adapter, no renderer imports) · dataset stability.

## Defects found by the build and fixed (not hidden)

1. **Objectives re-observed the same target every cycle.** Nothing declared when work stops being worth doing.
   Fix: objective plan policy `min_score` and `min_repeat_gap_hours`, enforced from ASA-registered state and recorded as skip reasons.
2. **A transit not observable tonight ranked first** because `transit_window_proximity` graded near-misses over a 36 h horizon.
   Fix: strictly in-window by default; a horizon must be declared.
3. **Evidence status was part of evidence identity**, so a refined ephemeris could not supersede an old one.
   Fix: status is lifecycle; `supersede_evidence`; adapter syncs the URO status literal.
4. **Idempotent reload changed the kernel digest**: in ASA a duplicate proposal is a governed `merged` event.
   Fix: adapter checks for an existing URO before proposing. Recorded as an ASA request (below).
5. Circular import between pipeline and execution when the session loop lived inside `astro.execution` → moved to `astro.session`.

## ASA integration (see `temp/astro-asa-integration.md`)

Consumed: `Kernel.bootstrap/open/submit/query/relationships/uro/provenance/project/head/replay/digest/verify`,
`derive_uao_id`, storage backends, registry composition. Demonstrated non-blocking requests to ASA main:
enumeration query (`entities()`, `uros()`), `find_uro(type, bindings, literals)` or `propose(..., if_absent)`,
and — only if ASA wants one — a generic derived-construct shape. Astro reads `Kernel.state` for enumeration
until then. No ASA code was modified; `~/ASA-canonical`'s working tree was never touched.

## Scientific integrity

All data is synthetic or simulated and labelled by `data_class` on every record. The simulated executor never
fabricates a measurement or classification. Visibility is geometric altitude only (no refraction, twilight,
Moon) and says so in its trace. Brightness enters only as a declared instrument-feasibility feature; proximity
only as a declared calibration feature. Nothing here is evidence for `ASTRO-EXP-0001`, `ASTRO-THEORY-0001`
or any ASA claim; evidence level of the frozen instruments remains `EH-0`.

## Next

Slice 3 — catalogue adapters with provenance (Gaia DR3 / NASA Exoplanet Archive, DR-frozen, read-only, cached with digests) and real coordinates/ephemerides.
Slice 4 — the three-pane visual (universe | objective & context | significance & plan) on top of `evaluate`/`session` JSON.
Slice 5 — benchmark harness: ASA-guided session vs FIFO, random, static priority, brute force; report negative findings as such.
Also: relationship-status sync in the adapter (evidence status is synced; relationship status is not yet), `astro explain` for entities not in the receipt's explanation set, README quick-start on a clean machine with GitHub clone of ASA (network).

## Benchmark (§18) — added after the first push

`astro benchmark` runs every strategy through the same session loop, scheduler and simulated executor; only
selection differs. Baselines (fifo, random, static priority = brightest first) see the objective's kind filter
and budgets only. `oracle` selects with the ground-truth scorer and is an upper bound. Useful = the action
satisfied the objective's question per the universe's own records at the time.

| Objective | fifo | random | static priority | **asa** | oracle |
|---|---|---|---|---|---|
| A transit follow-up | 1/3 useful, 360 min wasted | 0/3, 540 | 0/2, 360 | **1/1, 0** | 1/1, 0 |
| B transient follow-up | 1/1, 0 | 1/1, 0 | 1/1, 0 | **1/1, 0** | 1/1, 0 |
| C stellar variability | 0/3, 540 | 1/3, 360 | 1/2, 180 | **2/2, 0** | 2/2, 0 |
| D calibration | 1/5, 80 | 1/5, 80 | 1/5, 80 | **1/1, 0** | 1/1, 0 |

Read honestly: a smoke benchmark on 14 hand-built entities whose objectives and oracle were written by the
same operator. It shows the harness works and the engine does what its declarations say; it is not evidence
that ASA improves astronomy. Objective B has no discriminating power (one eligible transient; every strategy
ties — recorded as a test). Baseline waste is partly the absence of a stop rule. All strategies reproduce
exactly; the engine never imports the oracle (tested). Next: larger populations, baselines with stop rules,
an oracle not written by the objective's author.
