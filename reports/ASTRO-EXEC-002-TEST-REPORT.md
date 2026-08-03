# ASTRO-EXEC-002 — Phase 2 Test Report

| Field | Value |
|---|---|
| Authoritative repository | `https://github.com/17th2nd/ASA-Astro`, branch `main` |
| Verified implementation commit | `5d4600b713eb5ebcb34698241e0050b660ba43ab` |
| Verification date | 2026-08-03 |
| Environment | Fresh GitHub clone, new Python 3.12 virtual environment, installed wheel |
| Outcome | **PASS** |
| Evidence classification | Engineering validation, `EH-0`; not scientific evidence |

## Clean installation

The fresh clone resolved to the verified commit with `HEAD...origin/main = 0 0` and a clean tree.
`python -m pip install .` built and installed the wheel with the exact declared lock:

```text
asa-astro==0.1.0
attrs==23.2.0
jsonschema==4.10.3
Pillow==10.2.0
pyrsistent==0.20.0
```

The packaged configuration JSON Schema was available through the installed distribution; no
ancestor scan or implicit source checkout was used by `astro_exec`.

## Automated suites

| Suite and exact command | Result |
|---|---|
| Installed Phase 2: `venv/bin/python -m unittest discover -s tests/exec -t . -v` | 38 tests, PASS |
| Legacy unit, repository-native: `PYTHONPATH=src venv/bin/python -m unittest discover -s tests/unit -t . -v` | 8 tests, PASS |
| Legacy reasoning, repository-native: `PYTHONPATH=src venv/bin/python -m unittest discover -s tests/reasoning -t . -v` | 10 tests, PASS |
| Legacy integration/harness, repository-native: `PYTHONPATH=src venv/bin/python -m unittest discover -s tests/integration -t . -v` | 7 tests in 49.354s, PASS |

Total: **63/63 tests passed**. Legacy tests use their established source-checkout mode because the
legacy POC resolves its schemas and code receipt from repository paths. Phase 2 clean-install tests
exercise the installed `astro_exec` wheel.

## Installed CLI acceptance

Commands executed from the verified fresh clone:

```text
astro-exec version
astro-exec validate-config --config config/astro-exec-phase2.toml
astro-exec validate-frozen --config config/astro-exec-phase2.toml --repository-root .
astro-exec dry-run ... --output /tmp/.../dry-one --run-label invocation-one
astro-exec dry-run ... --output /tmp/.../dry-two --run-label invocation-two
astro-exec verify /tmp/.../dry-one
astro-exec verify /tmp/.../dry-two
compare_dry_runs(dry-one, dry-two)
```

Observed receipt:

```text
configuration: valid
frozen artefacts: 6 verified
run id (both): RUN-ca9998d7ff3795ef2104fbcc2697a7d3dd779d32b7dbe96287a1525e1e85a7ac
authoritative digest (both): c63d67203fe528b104e79cd5994baf67cf7dc72af26a85aeaa22886735c59bb4
replay status (both): verified
authoritative_equivalent: true
differing_files: []
```

The different invocation labels produced distinct sibling invocation records. They did not change
run identity, package files, or `AUTHORITATIVE-CONTENT.sha256`.

## Negative and security contracts

Automated evidence passed for:

- unsupported canonical values and naive timestamps;
- invalid and mismatched typed digests;
- unknown configuration fields and path escape;
- incomplete provenance and missing parent records;
- missing, changed, symlink-substituted and prohibited extra frozen artefacts;
- accurate frozen Part A versus Candidate Part B status;
- denied cross-role reads, parent traversal and symlink escape;
- illegal lifecycle transitions;
- structured CLI failure output;
- package overwrite refusal and checksum tampering;
- absence of legacy `asa_astro` and renderer imports.

## Static validation

```text
python -m compileall -q src/astro_exec tests/exec — PASS
public class/function docstring audit — PASS; 0 undocumented
contract test citation audit — PASS; 0 uncited
git diff --check — PASS
fresh clone HEAD == origin/main — PASS
fresh clone ahead/behind — 0/0
fresh clone working tree — clean before validation-generated ignored caches
```

No scientific execution, dataset acquisition, network acquisition command, estimator, astronomy
mathematics, or empirical-ledger mutation occurred during this validation.
