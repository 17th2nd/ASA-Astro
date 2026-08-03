# ASTRO-EXEC-002 — Phase 2 Completion Report

## Outcome

The G1 deterministic execution skeleton is implemented, validated from GitHub, and bounded at
Phase 2. It remains non-scientific infrastructure at `EH-0`. No Phase 3 work began.

## Commit receipt

- Programme baseline: `5e8b0a567c7e8c95fdc4081c568b483eba022189`
- Expanded-directive actual starting SHA: `9cc9c60fccf624238962f122fe1c2c6e9bbb3a7e`
- Final tested implementation SHA: `5d4600b713eb5ebcb34698241e0050b660ba43ab`
- Evidence publication commit: the Git commit containing this report; verified and recorded in the
  post-publication Gemini handoff manifest and operator receipt
- Authoritative repository: `https://github.com/17th2nd/ASA-Astro`, branch `main`

Git cannot embed a commit's own SHA in that commit's contents. “Final tested implementation SHA” is
therefore the exact remote code/configuration commit exercised by the evidence. The following
evidence-only commit does not change runtime behavior.

## Complete changed-file inventory

Relative to the programme baseline, Phase 2 added or modified only these files:

```text
config/astro-exec-phase2.toml
config/frozen-artefacts-v1.json
docs/execution/ASTRO-EXEC-001-ACCEPTANCE-GATES.md
docs/execution/ASTRO-EXEC-002-PHASE-2-INTERFACES.md
docs/execution/ASTRO-EXEC-002-REQUIREMENTS-TRACEABILITY.md
pyproject.toml
reports/ASTRO-EXEC-002-COMPLETION-REPORT.md
reports/ASTRO-EXEC-002-G1-VALIDATION-REPORT.md
reports/ASTRO-EXEC-002-TEST-REPORT.md
review-packages/ASTRO-EXEC-002-GEMINI-REVIEW-PROMPT.md
src/astro_exec/__init__.py
src/astro_exec/analysis/__init__.py
src/astro_exec/cli/__init__.py
src/astro_exec/cli/main.py
src/astro_exec/contracts/astro-exec-config-v1.schema.json
src/astro_exec/core/__init__.py
src/astro_exec/core/canonical_json.py
src/astro_exec/core/config.py
src/astro_exec/core/determinism.py
src/astro_exec/core/errors.py
src/astro_exec/core/frozen.py
src/astro_exec/core/hashing.py
src/astro_exec/core/ids.py
src/astro_exec/core/leakage_guard.py
src/astro_exec/core/lifecycle.py
src/astro_exec/core/logging.py
src/astro_exec/core/provenance.py
src/astro_exec/core/replay.py
src/astro_exec/core/run_package.py
src/astro_exec/data/__init__.py
src/astro_exec/estimator/__init__.py
src/astro_exec/estimator/interface.py
src/astro_exec/experiment/__init__.py
src/astro_exec/orbits/__init__.py
src/astro_exec/results/__init__.py
src/astro_exec/roles/__init__.py
src/astro_exec/roles/contracts.py
tests/exec/__init__.py
tests/exec/core/__init__.py
tests/exec/core/test_config.py
tests/exec/core/test_integrity.py
tests/exec/core/test_lifecycle.py
tests/exec/core/test_logging.py
tests/exec/core/test_provenance.py
tests/exec/core/test_representation.py
tests/exec/core/test_run_package.py
tests/exec/test_architecture.py
tests/exec/test_interfaces_and_cli.py
```

## Module inventory

| Namespace | Modules | Phase 2 responsibility |
|---|---|---|
| `astro_exec.core` | `canonical_json`, `hashing`, `ids`, `config`, `provenance`, `frozen`, `leakage_guard`, `lifecycle`, `errors`, `logging`, `run_package`, `replay`, `determinism` | Shared deterministic contracts |
| `astro_exec.cli` | `main` | Infrastructure-only command surface |
| `astro_exec.estimator` | `interface` | ABI and explicit `UR-001` failure placeholder |
| `astro_exec.roles` | `contracts` | Four role identities and dry-run-only result |
| Reserved | `analysis`, `data`, `experiment`, `orbits`, `results` | Empty namespace markers only |

No module under `astro_exec` imports `asa_astro`.

## Public-interface inventory

- Canonical representation: `canonical_timestamp`, `canonical_text`, `canonical_bytes`.
- Digests: `DigestKind`, `SHA256Digest`, `GitBlobDigest`, byte/stream/file/object hash helpers and
  typed digest verification.
- Identities: `DeterministicIdentity`, `ArtefactIdentity`, `ConfigurationIdentity`, `RunIdentity`,
  `InvocationIdentity`, `ProvenanceRecordIdentity`, `TransformationIdentity`.
- Configuration: `RoleCapabilities`, `ExecutionConfig`, `configuration_schema`,
  `config_from_mapping`, `load_config`.
- Frozen integrity: `ArtefactSection`, `FrozenManifestEntry`, `FrozenManifest`,
  `VerifiedArtefact`, manifest load/validation/verification functions.
- Provenance: `SourceArtefact`, `DependencyEnvironment`, `DerivedArtefact`,
  `ProvenanceRelationship`, `ProvenanceNode`, `ProvenanceGraph`.
- Isolation/lifecycle: `LeakageGuard`, `RunState`, `LifecycleTransition`, `RunLifecycle`.
- Errors/logs: stable `AstroExecError` subclasses and `StructuredLogger`.
- Package/replay: `create_dry_run`, `ReplayReport`, `verify_run_package`, `DeterminismReport`,
  `compare_dry_runs`.
- Interfaces: `TargetInputs`, `FrozenEstimator`, `UnresolvedEstimator`, `Role`, `RoleResult`,
  `DryRunRole`.
- CLI: `build_parser`, `main`.

Every public interface has a docstring. Full behavioral details are in
`docs/execution/ASTRO-EXEC-002-PHASE-2-INTERFACES.md`.

## Validation and exact commands

The final tested implementation was cloned from GitHub and installed into a new virtual environment.
Core commands were:

```text
git clone --branch main --single-branch https://github.com/17th2nd/ASA-Astro.git <fresh>/ASA-Astro
python3 -m venv <fresh>/venv
<fresh>/venv/bin/python -m pip install .
<fresh>/venv/bin/python -m unittest discover -s tests/exec -t . -v
PYTHONPATH=src <fresh>/venv/bin/python -m unittest discover -s tests/unit -t . -v
PYTHONPATH=src <fresh>/venv/bin/python -m unittest discover -s tests/reasoning -t . -v
PYTHONPATH=src <fresh>/venv/bin/python -m unittest discover -s tests/integration -t . -v
<fresh>/venv/bin/astro-exec version
<fresh>/venv/bin/astro-exec validate-config --config config/astro-exec-phase2.toml
<fresh>/venv/bin/astro-exec validate-frozen --config config/astro-exec-phase2.toml --repository-root .
<fresh>/venv/bin/astro-exec dry-run --config config/astro-exec-phase2.toml --repository-root . --output <run-one> --run-label invocation-one
<fresh>/venv/bin/astro-exec dry-run --config config/astro-exec-phase2.toml --repository-root . --output <run-two> --run-label invocation-two
<fresh>/venv/bin/astro-exec verify <run-one>
<fresh>/venv/bin/astro-exec verify <run-two>
compare_dry_runs(<run-one>, <run-two>)
<fresh>/venv/bin/python -m compileall -q src/astro_exec tests/exec
```

Results: **38/38 Phase 2 tests and 25/25 retained legacy tests passed**. Both dry runs replayed;
their authoritative run ID and digest matched and `differing_files` was empty. See
`reports/ASTRO-EXEC-002-TEST-REPORT.md` for the exact receipt.

## Requirements and acceptance

- G1 traceability: `docs/execution/ASTRO-EXEC-002-REQUIREMENTS-TRACEABILITY.md`.
- G1 validation: `reports/ASTRO-EXEC-002-G1-VALIDATION-REPORT.md`.
- Only G1 checkboxes were marked complete. G2 and later remain open.
- No unresolved requirement was closed.
- No scientific execution occurred; all package evidence remains `EH-0`.

## Files intentionally unchanged

- Every frozen scientific artefact listed by `config/frozen-artefacts-v1.json`.
- `src/asa_astro/**` and all legacy scientific/POC behavior.
- `schemas/**` legacy observation and reasoning contracts.
- `tests/fixtures/**`, `examples/**`, and all existing fixture data.
- `validation/results/**`, the empirical ledger, historical reports and historical review packages.
- All ASTRO-EXEC-001 blueprint companions except the G1 acceptance checklist.
- G2–G10 acceptance state.

## Security impact statement

Security and experimental isolation are strengthened. Frozen verification is fail-closed and checks
two explicitly typed identities; symlink substitution, path escape, missing/changed files and closed
set extras are rejected before run creation. `LeakageGuard` denies undeclared role paths and rejects
traversal and symlink escape. Configuration rejects unknown fields and has no hidden defaults.
Invocation diagnostics and logs cannot enter authoritative replay identity. No fallback repository,
environment-variable access path, network acquisition command, scanner weakening, secret handling,
or credential-bearing output was added.

## Runtime behavior preservation

Legacy `asa_astro` code and tests are unchanged and 25/25 remain green. Phase 2 adds a separate
namespace and CLI. It performs validation and manufactures only empty infrastructure packages; it
cannot execute scientific paths. Determinism is stronger than the original G1 wording: identical
authoritative inputs produce the same run identity and bytes, while explicit invocation metadata is
outside the package.

## Expected integration order

The ASTRO-EXEC-001 manufacturing roadmap remains authoritative: G1 precedes the separately owned
data, context, orbit, experiment, analysis and results phases. This report does not authorize or
begin those phases and does not instruct another operator to start.

## Unresolved items and human rulings

- Programme/custodian acceptance of G1 remains a human ruling.
- `UR-001` remains the Phase 10 estimator-specification blocker.
- `UR-003`, `UR-004` and `UR-007` remain Phase 3/5 data-policy blockers.
- `UR-005` and `UR-006` remain Phase 5 numerical/Sobol blockers.
- `UR-002` and `UR-008` retain their recorded scope/programme status.
- `UR-009` and `UR-010` remain later-phase governance/ordering blockers.
- There is no technical blocker to the G1 interfaces themselves.

## Rollback procedure

Rollback is recoverable and non-rewriting: use `git revert` on `main`, newest Phase 2 commit first,
for the published commits listed in the G1 validation report, then push the revert commits normally.
Do not reset, rebase, amend or force-push. Re-run the complete pre-Phase-2 suites after the revert.
The Gemini desktop bundle is non-authoritative and may be archived or rebuilt from the resulting
verified remote commit.

## Stop condition

G1 implementation and evidence are complete. Operator A stops at Phase 2.
