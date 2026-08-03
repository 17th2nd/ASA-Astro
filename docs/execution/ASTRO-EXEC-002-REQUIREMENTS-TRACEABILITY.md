# ASTRO-EXEC-002 — Phase 2 Requirements Traceability

**Package:** ASTRO-EXEC-002 · **Gate:** G1 only · **Evidence level:** EH-0

Every test under `tests/exec/` cites `G1` or its originating `R-*` requirement in the test docstring.
No unresolved scientific requirement is closed by this matrix.

| Phase 2 requirement | Implementation | Contract evidence | Outcome |
|---|---|---|---|
| Package separate from legacy `asa_astro` | `src/astro_exec/` | `test_astro_exec_does_not_import_asa_astro_or_renderers` | PASS |
| Canonical UTF-8 JSON and timestamps | `core/canonical_json.py` | canonical known-answer, ordering, scalar/timestamp, unsupported-value tests | PASS |
| SHA-256 and distinct Git blob identity | `core/hashing.py` | SHA-256/Git known-answer, typed substitution, mismatch tests | PASS |
| Deterministic domain identifiers | `core/ids.py` | canonical-content and domain-type tests | PASS |
| Schema-backed immutable configuration | `core/config.py`, packaged JSON Schema | schema, unknown field, unsafe path, immutability, fingerprint tests | PASS |
| Explicit defaults; no scientific default | required `[defaults]` table with empty `applied` | configuration snapshot test | PASS |
| Generic provenance primitives and DAG | `core/provenance.py` | complete source/derived record, missing input, parent integrity tests | PASS |
| Frozen-artefact run-start verification (`R-061`) | `core/frozen.py`, explicit manifest | repository receipt; missing, changed, substituted, extra and pre-output abort tests | PASS |
| Part A frozen; Part B Candidate | mixed-status theory manifest entry | exact section-status contract test | PASS |
| Default-deny four-role capability boundary (`R-029`) | `core/leakage_guard.py`, TOML capabilities | allowed, cross-role denied, traversal and symlink tests | PASS |
| Required deterministic lifecycle | `core/lifecycle.py` | legal path, illegal transition, failed/sealed and provenance tests | PASS |
| Structured stable errors and diagnostic logs | `core/errors.py`, `core/logging.py` | error record and logging context/classification tests | PASS |
| Infrastructure-only CLI | `cli/main.py` | version/config/frozen/dry-run/verify/failure-output tests | PASS |
| Deterministic run identity and invocation separation | `core/run_package.py`, typed identities | two-label authoritative equivalence and sibling invocation tests | PASS |
| Replay framework | `core/replay.py`, `core/determinism.py` | checksum tamper, identity, lifecycle and byte-comparison tests | PASS |
| Software/environment/config/frozen/provenance/lifecycle package contents | dry-run package schema v1 | package content and replay tests | PASS |
| Exact pinned clean installation | `pyproject.toml`, `requirements.lock` | metadata-lock contract plus fresh-clone wheel install | PASS |
| Public interfaces documented for later operators | public docstrings and Phase 2 interface contract | AST public-docstring audit | PASS |
| No scientific execution and no evidence elevation | `scientific_computation: false`, `evidence_level: EH-0` | package classification tests and fresh-clone receipt | PASS |

## G1 acceptance mapping

| Binding G1 criterion | Published evidence |
|---|---|
| `astro_exec.core` published | GitHub `main`; 38 installed Phase 2 contracts |
| Contract tests green on a fresh clone | `reports/ASTRO-EXEC-002-TEST-REPORT.md` |
| Frozen drift aborts | `tests/exec/core/test_integrity.py`, `test_frozen_artefact_drift_aborts_before_output_creation` |
| Two dry runs byte-identical except run id | Stronger result: same run ID and byte-identical authoritative content; invocation is outside the package |
| No `asa_astro` import | AST import-boundary test over all `src/astro_exec/**/*.py` |
| Interfaces documented without chat history | `ASTRO-EXEC-002-PHASE-2-INTERFACES.md` and public docstrings |

## Unresolved requirements

`UR-001` through `UR-010` remain exactly as recorded in
`ASTRO-EXEC-001-UNRESOLVED-REQUIREMENTS.md`. No status, resolution route, or scientific requirement
was modified or closed in Phase 2.
