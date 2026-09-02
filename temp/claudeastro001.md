# claudeastro001 — Preflight report

Programme: CLAUDE-ASTRO-BUILD-001 · Operator: Claude · Date: 2026-09-03

## ASTRO CURRENT STATE

| Item | Value |
|---|---|
| Astro repo | `~/ASA-Astro` → `https://github.com/17th2nd/ASA-Astro.git` |
| Branch | `main` (repo rule: no branches, commit direct to main, push each session) |
| ASTRO_HEAD | `549ee742` "Publish complete Phase 2 G1 evidence" (2026-08-03) |
| origin/main | `549ee742` — identical, 0 ahead / 0 behind |
| Working tree | clean before this programme; `.venv/` created (gitignored) |
| Last activity | 2026-08-03. Nothing since. Archive drive not mounted; Desktop `ASTRO*` folders are PDF/HTML prints and flat-packed Gemini handoff copies of repo files (no unpublished work found; no Gemini review response found anywhere) |

Existing modules:

| Package | What it is | Status for this programme |
|---|---|---|
| `src/asa_astro/` | Image → candidate-graph POC (Codex B) + provisional Standing/Significance engine over image regions (Codex C). Declares itself non-conformant, `asa_dependency_status = unavailable_not_consumed`. | **OBSOLETE as engine**, retained untouched. Its context-declaration ideas are reused as doctrine, not code. |
| `src/astro_exec/` | ASTRO-EXEC-002 Phase 2 deterministic execution skeleton for the frozen perturber experiment `ASTRO-EXP-0001`: canonical JSON, SHA-256/git-blob digests, content-derived identities, frozen-artefact verification, provenance DAG, run lifecycle, leakage guard, run package + replay, CLI. 38 tests. | **EXISTS, reused** for receipts, digests, provenance, canonical JSON. Not modified. |
| `docs/theory`, `docs/claims`, `validation/benchmarks`, `validation/results` | Frozen scientific instruments (`config/frozen-artefacts-v1.json`, 6 artefacts, digest-verified). Evidence level `EH-0`. | **Frozen. Never modified.** This programme claims no empirical validation of anything. |
| `docs/ontology`, `docs/models` | ASTRO-ONTOLOGY-0001, RELATIONSHIP-TAXONOMY-0001, CONTEXT-MODEL-0001, SIGNIFICANCE-MODEL-0001 (image-benchmark profile) | **PARTIAL** — the context invariants (§2), required declaration fields (§3), falsification criteria (§8) are adopted as the objective/context contract; the image-benchmark profiles are not the target domain. |

Existing tests (all green in a fresh `.venv`, Python 3.12.3, `requirements.lock`):

| Suite | Count |
|---|---|
| `tests/exec` (Phase 2 skeleton) | 38 |
| `tests/unit` + `tests/reasoning` + `tests/integration` (legacy POC) | 63 |

CLI check: `astro-exec validate-frozen` → `{"artefact_count":6,"status":"verified"}`.

## ASA INTEGRATION STATE

| Item | Value |
|---|---|
| ASA repo | `~/ASA-canonical` → `https://github.com/17th2nd/ASA.git` (read from git objects only; that working tree belongs to the parallel operator and sits on a governance branch with `kernel/` untracked) |
| ASA origin/main | `e64e1e25` (2026-08-11) — **contains no kernel** |
| ASA kernel branch | `origin/kernel/v0.1-alpha` head **`b855d4c7`** (2026-08-31); reviewed head 4fec38a = tag `ASA-KERNEL-0.1.0-alpha10`, Codex review 008 APPROVE WITH BOUNDED NON-BLOCKING FINDINGS; PR #32 (draft) merge authorised by D-043 but not executed |
| **ASA_BASELINE** | **`b855d4c730dc2553db7a693d91c7d4d0cf25d03c`** (branch `kernel/v0.1-alpha`, kernel `0.1.0-alpha10`, status "ENGINEERING ALPHA — NOT RATIFIED") |

Interfaces Astro will consume (all from `asa_kernel.api` + `asa_kernel.identity`, the consumer contract the ASAW adapter is held to):

- `Kernel.bootstrap(storage, registry_facet, stream, policy, perspectives, domain_types, actor)` / `Kernel.open`
- `submit("register_entity" | "update_entity" | "propose" | "update_state" | "supersede" | "retire_uro" …)` → `Receipt(outcome, key, events, diagnostics, head, seq)`
- `query(uao)`, `relationships(ref)`, `uro(key)`, `provenance(ref)`, `project(perspective)`, `head()`, `replay()`, `digest()`, `verify()`
- `derive_uao_id(namespace, seed)`; registry composition via `kernel/tools/build_registry.py compose_domain`
- Facet format: types with roles `{name, kind, binds, min, max, identity}`, literals `{name, datatype ∈ string|boolean|integer|decimal, identity}`, `evidence ∈ definitional|supported`; `supported` types are `unevaluated` until an `asa.core/supports@1` URO (evidence UAO → assertion URO) endorses them. Decimal literals are restricted decimal **strings**; floats are forbidden in anything the kernel hashes.

Known integration risk:

1. **The kernel has no significance formula by design** ("Significance is a Derived Construct evaluated at query time and does not enter Kernel v0.1", programme §3/§21; `04_Significance/` on main is a placeholder). Astro therefore implements significance as an Astro-owned *derived construct* over kernel relational state, parameterised by an Objective. The generic contract that emerges is recorded as a candidate ASA requirement in `temp/astro-asa-integration.md`, not built into ASA.
2. Kernel is on a branch, not main; the parallel operator may merge or move it. Astro pins the exact SHA in `config/asa-baseline.json`; every receipt carries it; a moved baseline is a deliberate re-pin.
3. `build_registry.py --domain` writes only into the ASA tree. Astro calls its `compose_domain` and writes the result into Astro's own `registry/`; an `--out` option is the requested ASA change.
4. JCS forbids floats. Astro's kernel attributes carry numbers as decimal strings; the Astro domain layer keeps native precision separately and digests both.

## SPECIFICATION COVERAGE (directive §4–§19 vs corpus)

| Requirement | Class | Note |
|---|---|---|
| §4 No intrinsic significance; identity/evidence/relationships/state | EXISTS (doctrine) / ABSENT (code) | Ontology + context model state it; no domain code implements it |
| §5 R_v → S_v → Plan → Schedule → Execute → Evidence → Update | ABSENT | Nothing in repo plans or executes |
| §6 Astronomy domain model (entities, identity, evidence, relationships, state) | ABSENT | Legacy POC models image regions only |
| §7 Objective/Context model, objectives A–E | PARTIAL | Context model §3 gives the declaration contract; no executable objective exists |
| §8 Context-switch and evidence-arrival demonstrations as regression tests | ABSENT | |
| §9 Execution engine (plan/schedule/execute/feedback) | ABSENT | `astro_exec` is an apparatus for one frozen experiment, not a planner |
| §10 Data-first, deterministic core, no LLM | EXISTS (principle) | Whole corpus is deterministic; keep it so |
| §11 Provenance + `AstroDecisionReceipt` | PARTIAL | `astro_exec.core` supplies digests, identities, provenance DAG; receipt type absent |
| §12 Explainability from decision state | PARTIAL | Legacy explanation traces exist for image graphs; not reusable |
| §13–14 Visual demo, relationship graph | ABSENT | (Slice 4; not before the core is proven) |
| §15 Scientific integrity, labelled synthetic data | EXISTS (doctrine) | Foundation §9–§12; adopted |
| §16 Vertical slices | ABSENT | |
| §17 Tests (identity invariance, no intrinsic significance, context/evidence/relationship sensitivity, determinism, provenance, boundary) | ABSENT | |
| §18 Benchmarks vs FIFO/random/static | ABSENT | (Slice 5) |
| §19 Asteroseismology readiness (time series, cadence) | ABSENT | Domain model carries time-series evidence and cadence from the start |
| ASTRO-EXP-0001 perturber experiment (Phases 3–10) | CONFLICTING (scope) | A different product: one frozen experiment blocked on custodian rulings UR-001..010. Left exactly as is. Not resumed by this programme; not contradicted by it. Nothing built here is evidence for it. |

## FIRST VERTICAL SLICE

Executable path, in this order, each step a narrow commit with tests:

```
data/universe/slice1.json  (synthetic, labelled)
  → astro.domain   (Entity, EvidenceRecord, RelationshipAssertion, EntityState, Universe digest)
  → astro.asa      (AstroAdapter: universe → kernel UAO/URO/supports; pinned ASA baseline)
  → astro.objectives (Objective A exoplanet transit follow-up, B transient follow-up, D calibration; Context)
  → astro.significance (derived construct: eligibility gate + declared features + immutable weight policy → ranked, explained)
  → astro.execution (plan from ranking)
  → astro.receipts (AstroDecisionReceipt via astro_exec.core canonical JSON/digests)
  → astro.cli      (evaluate / explain / demo context-switch)
```

Proof for Phase C: same universe digest, objective A vs objective B → different ranking, kernel digest and universe digest unchanged. Then evidence arrival → re-evaluation changes the plan. Both become tests.

Repository layout decisions: new package `src/astro/` (Astro-owned); `src/astro_exec/` and `src/asa_astro/` untouched; ASA checkout at `.asa/` (gitignored, pinned, verified); Astro registry facet under `registry/`; reports in `temp/`.
