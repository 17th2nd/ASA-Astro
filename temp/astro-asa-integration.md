# Astro ↔ ASA integration note

Machine-readable-ish record of genuine cross-repository facts. Evidence first: nothing here is an
architectural demand on ASA main unless Astro has demonstrated it by implementation.

## Consumed baseline

| Field | Value |
|---|---|
| ASA repository | https://github.com/17th2nd/ASA.git |
| Branch | `kernel/v0.1-alpha` |
| ASA_BASELINE | `b855d4c730dc2553db7a693d91c7d4d0cf25d03c` |
| Kernel version | `0.1.0-alpha10` (ENGINEERING ALPHA — NOT RATIFIED) |
| Pinned by | `config/asa-baseline.json`; materialised at `.asa/ASA` by `tools/asa_baseline.py` |
| Kernel self-test at baseline (Astro venv, 2026-09-03) | 66/66 |

## Interfaces Astro consumes

- `asa_kernel.api.Kernel` — `bootstrap`, `open`, `submit`, `query`, `relationships`, `uro`, `provenance`, `project`, `head`, `replay`, `digest`, `verify`
- `asa_kernel.identity.derive_uao_id`
- `asa_kernel.storage.MemoryStorage` / `FileStorage`
- `asa_kernel.registry` (facet validation, via `kernel/tools/build_registry.compose_domain`)
- Registry facet format and admission policy v1 (`definitional` → endorsed; `supported` → endorsed on first `asa.core/supports@1`)

## Incompatibilities found

| Date | Finding | Astro handling |
|---|---|---|
| 2026-09-03 | `kernel/tools/build_registry.py --domain` writes the composed facet only into the ASA tree (`kernel/registry/relationship_types.<ns>.candidate.json`). | Astro imports `compose_domain()` and writes the returned document into its own `registry/`. Requested ASA change: an `--out PATH` option (or return-only mode). Non-blocking. |
| 2026-09-03 | Kernel has no significance evaluation (by design, programme §3/§21). | Astro implements significance as an Astro-owned derived construct over kernel relational state. See "candidate generic capability" below once demonstrated. |

## Temporary Astro adapters

| Adapter | Reason | Migration action |
|---|---|---|
| `src/astro/asa/locator.py` | Kernel is not pip-installable from the branch (no `pyproject` outside `kernel/dist`, which is untracked). | When ASA publishes an installable package with a version pin, replace path insertion with a dependency pin. |

## Candidate generic capabilities (recorded only after Astro demonstrated them)

| Date | Capability | Demonstrated by | Suggested ASA form |
|---|---|---|---|
| 2026-09-03 | **Enumeration query.** The consumer contract has `query(uao)`, `relationships(ref)`, `uro(key)` but no way to enumerate registered UAOs or UROs. Astro's `RelationalSnapshot` and duplicate-avoidance (`_find_uro`) read `Kernel.state.uaos` / `Kernel.state.uros` (a property on the API class, deep-copied projections) — outside the documented list. | `src/astro/asa/adapter.py` `snapshot()`, `_find_uro()`, `_rebuild_index()` | `Kernel.entities() -> list[str]`, `Kernel.uros(type_id=None) -> list[dict]`, and `Kernel.find_uro(type_id, bindings, literals) -> key | None` (identity-key lookup without proposing). Non-blocking. |
| 2026-09-03 | **Duplicate proposal is an event.** Re-proposing an identical URO appends `uro.proposed` + `governor.decision(merged)` + `uro.merged`, so an idempotent reload changes the digest. Correct per §11.6, but a consumer that wants "register if absent" must pre-check. | `tests/astro/test_asa_adapter.py::test_load_is_deterministic_and_idempotent` | Either the `find_uro` lookup above or a documented `submit("propose", ..., if_absent=True)` that returns the existing key without appending. |
| 2026-09-03 | **Derived-construct contract.** Astro's significance evaluation is a pure function of (kernel snapshot digest, objective declaration, context declaration, external value store bound by `record_digest`). ASA says significance is a Derived Construct evaluated at query time (programme §3/§21) but publishes no shape for one. | `src/astro/significance/evaluator.py` (`SignificanceEvaluation` scoped to kernel digest + head + registry digest + ASA baseline) | If ASA wants a generic shape: `DerivedConstruct{inputs: kernel_digest, registry_digest, declaration_id; output_id; scope}`. Astro will adopt it if published; not requested as a blocker. |
