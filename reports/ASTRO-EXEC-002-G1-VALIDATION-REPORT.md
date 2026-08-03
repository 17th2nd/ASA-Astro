# ASTRO-EXEC-002 — G1 Validation Report

| Field | Value |
|---|---|
| Package | ASTRO-EXEC-002 Phase 2 — Execution Skeleton |
| Operator | Codex Operator A |
| Authoritative repository | `https://github.com/17th2nd/ASA-Astro`, branch `main` |
| Programme baseline | `5e8b0a567c7e8c95fdc4081c568b483eba022189` |
| Expanded-directive starting SHA | `9cc9c60fccf624238962f122fe1c2c6e9bbb3a7e` |
| Final tested implementation SHA | `5d4600b713eb5ebcb34698241e0050b660ba43ab` |
| Verification date | 2026-08-03 |
| Evidence level | `EH-0`; no scientific experiment executed |

The final tested implementation SHA is the exact code/configuration state retrieved from GitHub and
validated below. The subsequent evidence-only commit is identified by the containing Git commit of
this report and by the post-publication Gemini manifest; a Git commit cannot contain its own SHA.

## Scope boundary

The delivery is deterministic infrastructure only. It implements no astronomy, physics, datasets,
orbit determination or propagation, estimator logic, experiment selection, truth comparison,
metrics, statistics, claims evaluation, rendering, or ledger mutation. `src/asa_astro/`, legacy
schemas and fixtures, historical records, and frozen scientific artefacts were intentionally
unchanged. No `UR` entry was closed.

## Published bounded units

Every row was validated, committed, pushed directly to `main`, fetched back, and matched against
`origin/main` before the next unit began.

| Unit | Verified GitHub commit |
|---|---|
| Initial canonical representation | `df7296193e799609c4748148fc46a4add178542b` |
| Initial integrity/capability foundation | `be2366d2bac5392ac484623c9ade13ac509dccb4` |
| Initial lifecycle/interfaces | `b9f16c8471ba2454bf5cfb6f779904a77f6b1bde` |
| Initial G1 reports | `93eae8178ef8cb692d95eb94bfd59309bae06651` |
| Gemini review prompt | `9cc9c60fccf624238962f122fe1c2c6e9bbb3a7e` |
| Canonical timestamps, typed digests and identities | `3868ec85820d32163075cff5fa0ee45a9edde545` |
| Schema-backed config and complete provenance | `d777d3b3ca4856809c6cafceee693ab14027a525` |
| Frozen manifest and LeakageGuard | `eeafebafb4e310669300e53098b04e104fff9a38` |
| Required lifecycle, structured logs and CLI | `375588596f7bbed716c8428fd32bdf728285537b` |
| Authoritative/invocation separation and replay | `0b81776d9013f69709fb50ccc72ce98aac0838ee` |
| Exact clean-install dependency graph | `5d4600b713eb5ebcb34698241e0050b660ba43ab` |

No published commit was amended, rebased, or force-pushed.

## G1 acceptance evidence

| Criterion | Objective evidence | Outcome |
|---|---|---|
| `astro_exec.core` published | Complete modules installed from GitHub wheel; public API inventory published | PASS |
| Canonical JSON, identifiers, hashing, config, provenance, errors, logging, LeakageGuard | Focused known-answer, validation, completeness and negative tests | PASS |
| Contract tests green on fresh clone | 38/38 installed Phase 2 tests in a new virtual environment | PASS |
| Complete existing Python validation preserved | 25/25 repository-native legacy tests in the same fresh clone | PASS |
| Frozen verification aborts on drift | Missing/changed/substituted/extra tests plus output-noncreation assertion | PASS |
| Two dry runs byte-identical except run id | Stronger: same authoritative run ID and digest; zero differing authoritative files | PASS |
| No `asa_astro` import | AST import-graph test across every `src/astro_exec/**/*.py` | PASS |
| Interfaces documented without conversation context | Phase 2 interface document plus zero-missing public-docstring audit | PASS |

Detailed test receipt: `reports/ASTRO-EXEC-002-TEST-REPORT.md`.
Requirements mapping: `docs/execution/ASTRO-EXEC-002-REQUIREMENTS-TRACEABILITY.md`.

## Deterministic replay evidence

The installed CLI generated two packages from identical authoritative inputs and different explicit
invocation labels:

```text
run id: RUN-ca9998d7ff3795ef2104fbcc2697a7d3dd779d32b7dbe96287a1525e1e85a7ac
authoritative digest: c63d67203fe528b104e79cd5994baf67cf7dc72af26a85aeaa22886735c59bb4
package one replay: verified
package two replay: verified
authoritative_equivalent: true
differing_files: []
```

The invocation labels are contained only in separate sibling diagnostic records. Package logs are
explicitly `diagnostic-not-scientific-evidence` and excluded from authoritative content.

## Frozen-artefact evidence

`config/frozen-artefacts-v1.json` pins SHA-256 and Git blob SHA-1 for all six required artefacts.
The guard verifies the exact manifest before creating a run directory and reports an exact drift
type. The theory entry is `mixed`: Part A is frozen; Part B is Candidate and not frozen.

## LeakageGuard evidence

Capabilities are explicit and immutable for custodian, truth laboratory, ASA laboratory and
statistician. Access is denied by default. Tests prove allowed reads work while cross-role truth
reads, `..` traversal and symlink escape fail with `LeakageViolation`.

## Import and installation evidence

- Installed runtime/build dependencies match `requirements.lock` exactly.
- Packaged config schema loads from the distribution, not ancestor discovery.
- No `astro_exec` module imports `asa_astro` or a renderer.
- No workstation absolute path, sibling repository fallback, environment-variable access path, or
  implicit ancestor scan exists in `astro_exec`.

## Unresolved requirements and later gates

`UR-001` through `UR-010` remain unchanged. `UnresolvedEstimator.select()` still raises
`UnresolvedRequirement("UR-001")`. G2 and every later gate remain unmarked and unimplemented.

## Gate result

**G1 IS OBJECTIVELY SATISFIED AT THE TESTED IMPLEMENTATION SHA.** The repository-published evidence
remains engineering validation at `EH-0`. Programme authority retains the acceptance ruling.
