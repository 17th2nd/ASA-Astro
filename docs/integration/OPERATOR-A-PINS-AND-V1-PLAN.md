# Operator A — ASA-Astro V1 pins + plan

Status: draft for ASA Chief. Does **not** modify ASA. Does **not** rewrite real-data-exp-0001. Does **not** touch Astro `main` manufacture.

## Exact pins (verified 2026-10-05, machine 17th2nd)

### ASA-Astro
| Item | Value |
|---|---|
| Repo | `https://github.com/17th2nd/ASA-Astro.git` |
| Local path | `/home/brock-gerand/ASA-Astro` |
| Base commit | `be2387f11efb065b5cb102ca00009de69d56d3eb` — `docs(real-data-exp-0001): failure note and claims hold` |
| Base branch | `housekeeping/real-data-exp-0001-failure-note` (= tip of that branch) |
| Integration branch | `grok/asa-astro-v1-application` — created from base pin (this work) |
| Prior local HEAD before branch | `preservation/local-handover-2026-09-26` @ `e154749` (left untouched) |
| `origin/main` | `cf20f04` — **do not manufacture on main** |

### ASA (dependency — read-only for Operator A)
| Item | Value |
|---|---|
| Canonical local | `/home/brock-gerand/ASA-canonical` |
| Required branch | `agent/asa-v1-rc0-final-falsification-remediation-133` |
| Required HEAD | **`c2ccd7d55e34d7ffe03fd21d8b633cde69c152d2`** — matches known `c2ccd7d…` |
| Tip message | `phase3: Founder 165C - barring follows the aftermath chain; decisions recorded (D-118)` |
| Tip date | 2026-10-05 21:40:46 +1000 |
| Nested checkout | `ASA-Astro/.asa/ASA` currently **detached at `b855d4c`** (stale vs remediation tip) |

## Stale integration (architecture map)

```
ASA-Astro (application)
  ├── src/asa_astro/     # Codex B observation→candidate-graph (schemas: asa_dependency unavailable_not_consumed)
  ├── src/astro/         # Astro execution engine (intends to consume ASA kernel)
  ├── config/asa-baseline.json  # CURRENT PIN (STALE for V1)
  │     ref: kernel/v0.1-alpha
  │     sha: b855d4c730dc2553db7a693d91c7d4d0cf25d03c
  │     kernel: 0.1.0-alpha10 ENGINEERING ALPHA — NOT RATIFIED
  ├── .asa/ASA           # materialised checkout of baseline (still at b855d4c)
  ├── registry/          # Astro relationship facet; validated by ASA compose_domain
  └── validation/real-data/ASTRO-REAL-DATA-EXP-0001  # FAILED experiment — hold claims; do not rewrite
```

### Consumed ASA surface (per `temp/astro-asa-integration.md`)
- `asa_kernel.api.Kernel` (bootstrap/open/submit/query/relationships/uro/provenance/project/head/replay/digest/verify)
- `asa_kernel.identity.derive_uao_id`
- `asa_kernel.storage.MemoryStorage` / `FileStorage`
- `asa_kernel.registry` + `tools/build_registry.compose_domain`

### Known incompatibilities / debt (non-blocking unless V1 says otherwise)
1. Registry compose writes into ASA tree — Astro already imports compose and writes own `registry/`
2. Kernel not pip-installable — path locator adapter
3. No significance in kernel — Astro-owned derived construct (Aug 2026 significance formula NOT earned for Phase-6 NPC; keep that lane separate)
4. Scale: full replay on open; supports O(n·m) governor; enumeration via undocumented `Kernel.state.*`
5. **Baseline drift:** Astro pinned to `b855d4c` / `kernel/v0.1-alpha`; V1 target is remediation-133 @ `c2ccd7d` — **re-pin is a deliberate recorded change**, not silent

### Stale / do-not-touch
- Do not amend `ASTRO-REAL-DATA-EXP-0001` failure narrative on this branch beyond citing it as hold
- Do not push manufacture to `main`
- Do not modify ASA repo contents (consume only)

## V1 application plan (proposed)

1. **Pin record** — update `config/asa-baseline.json` + `temp/astro-asa-integration.md` to remediation-133 @ `c2ccd7d…` *only after* kernel surface compatibility check (read-only against ASA-canonical checkout of that SHA).
2. **Materialise** — `tools/asa_baseline.py` against remediation tip into `.asa/ASA` (replace stale `b855d4c` checkout).
3. **Compat gate** — run Astro unit/adapter tests against new pin; list breaks without patching ASA; adapters stay in Astro.
4. **Application slice** — thin V1 path: pin → load synthetic/real slice → relational snapshot → one Objective evaluate → receipt. No claim upgrade of failed real-data exp.
5. **Claims discipline** — keep `asa_dependency_status` honest; no silent “ASA certified” from Astro UI; significance remains Astro-derived / on-trial where Programme says so.
6. **Idle Team** — Operator A owns pins+map; other operators take: (B) baseline re-pin PR text, (C) adapter/test green-up, (D) UI/navigator honesty labels — only after Chief accepts pins.

## Next action for Chief
Confirm: (a) create/push `grok/asa-astro-v1-application` from `be2387f` (done locally), (b) accept remediation-133 @ `c2ccd7d` as the ASA consume target for V1 re-pin, (c) Idle Team task split.


## Landed 2026-10-05 (Chief confirm)

- `config/asa-baseline-current-dev.json` — current-dev pin @ `c2ccd7d…`
- `config/asa-baseline.json` — historical, unchanged (`b855d4c`)
- `tools/asa_baseline.py` — `--config` supported; rematerialise detach
- `.asa/ASA` verified at `c2ccd7d55e34d7ffe03fd21d8b633cde69c152d2`
