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

## Candidate generic capabilities (record only after Astro demonstrates them)

- (none yet)
