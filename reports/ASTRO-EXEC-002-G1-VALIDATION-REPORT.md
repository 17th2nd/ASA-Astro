# ASTRO-EXEC-002 — G1 Validation Report

| Field | Value |
|---|---|
| Package | `ASTRO-EXEC-002` Phase 2 — Execution Skeleton |
| Operator | Operator A |
| Authoritative repository | `https://github.com/17th2nd/ASA-Astro` |
| Baseline | `5e8b0a567c7e8c95fdc4081c568b483eba022189` |
| Implementation tip verified from GitHub | `b9f16c8471ba2454bf5cfb6f779904a77f6b1bde` |
| Verification date | 2026-08-03 |
| Evidence level | `EH-0`; no scientific experiment executed |

## Scope boundary

The delivered package is infrastructure only. It contains no scientific computation, orbit
propagation, estimator implementation, datasets, astronomy mathematics, empirical result, ledger
candidate, or authoritative-scientific output. `src/asa_astro/` and all frozen scientific artefacts
are unchanged.

## Published bounded units

| Unit | Commit verified on GitHub `main` | Evidence |
|---|---|---|
| A1 — canonical representation, hashing, identifiers, errors | `df7296193e799609c4748148fc46a4add178542b` | Canonical JSON, SHA-256, content ids and structured-error tests green |
| A2 — configuration, provenance, logging, frozen artefacts, LeakageGuard | `be2366d2bac5392ac484623c9ade13ac509dccb4` | Config fingerprint, six artefact digests, provenance, logging and isolation tests green |
| A3 — lifecycle, run package, replay, roles, estimator ABI and CLI | `b9f16c8471ba2454bf5cfb6f779904a77f6b1bde` | Dry-run, replay, import graph and public CLI tests green |

Each unit was tested, committed to `main`, pushed, and independently verified with
`git ls-remote origin refs/heads/main` before the next unit began.

## G1 acceptance evidence

| Criterion | Evidence | Outcome |
|---|---|---|
| `astro_exec.core` published | Installed from a new GitHub clone; 25 package modules import | **PASS** |
| Canonical JSON, identifiers, hashing, config, provenance, errors, logging, `LeakageGuard` | 16 focused core-contract tests plus interface documentation | **PASS** |
| Contract tests green on fresh clone in clean environment | New `/tmp` clone and new `venv`; wheel built and installed; 24/24 `tests/exec` tests pass | **PASS** |
| Frozen-artefact drift aborts | Direct mismatch test and run-level test prove output is not created after drift | **PASS** |
| Two dry runs byte-identical except run id | `compare_dry_runs`: `differing_files=[]`, `equivalent_except_run_id=True` | **PASS** |
| No import of `asa_astro` | AST import-graph test over every `src/astro_exec/**/*.py`; runtime clean import test | **PASS** |
| Interfaces documented for B–E | `ASTRO-EXEC-002-PHASE-2-INTERFACES.md` plus complete public docstrings | **PASS** |

## Tests executed

### Fresh GitHub clone and isolated environment

```text
python -m unittest discover -s tests/exec -p 'test*.py' -v
Ran 24 tests in 0.020s — OK

astro-exec run --dry-run ... --run-label fresh-clone-a
status: DRY_RUN_COMPLETE

astro-exec run --dry-run ... --run-label fresh-clone-b
status: DRY_RUN_COMPLETE

astro-exec replay run-a
status: verified; 8 files

astro-exec replay run-b
status: verified; 8 files

compare_dry_runs(run-a, run-b)
{'differing_files': [], 'equivalent_except_run_id': True}
```

The cloned repository resolved to `b9f16c8471ba2454bf5cfb6f779904a77f6b1bde` and reported
`main...origin/main` with no changes.

### Retained pre-Phase-2 suites

```text
Legacy schema, evidence and pipeline: 11 tests — OK
Legacy reasoning: 10 tests — OK
Legacy Phase-2 validation harness: 4 tests in 48.370s — OK
```

### Static validation

```text
python3 -m py_compile src/astro_exec/**/*.py tests/exec/**/*.py — PASS
git diff --check — PASS
Public interface docstring audit — PASS (25 imported modules)
Forbidden asa_astro/rendering import audit — PASS
```

## Frozen-artefact receipt

The checked-in configuration pins and verifies these SHA-256 values before any output directory is
created:

| Path | SHA-256 |
|---|---|
| `docs/claims/ASTRO-CLAIMS-0001.md` | `44282ba8c92aa5f40b495982b50192a49f8aeb1ba5910895ea7c09136010c50b` |
| `docs/theory/ASTRO-THEORY-0001-V1-FREEZE-RECORD.md` | `b9fd57bb29750c3efe97ca18d8e4741f8afd08ae9e192b6dcf1e7fecc88cc6bc` |
| `docs/theory/ASTRO-THEORY-0001.md` | `c1289b3e8f096a91c82ed1bc912be31e798a289df26cc64dace76a06d8c1d56c` |
| `reports/ASTRO-V1-RESEARCH-CONTROLS-FREEZE-REPORT.md` | `43bf27049c640dd6467c2284a84eb37b5072aef4e8612815b7ab592ca2871fc1` |
| `validation/benchmarks/ASTRO-EXP-0001.md` | `a38796892e1d7d68c3a40b35b0a39175d07948f8ef9df73fee26daf4943a7316` |
| `validation/results/ASTRO-RESULTS-0001.md` | `434e4d417141ad69dcf45b23a5c89df644f01b6af3e9837bf5169db5fabf27a7` |

## Result

**G1 IMPLEMENTATION EVIDENCE SATISFIED.** Operators B–E may rely only on the published interfaces
after the custodian accepts this gate. Phase 3 has not begun.
