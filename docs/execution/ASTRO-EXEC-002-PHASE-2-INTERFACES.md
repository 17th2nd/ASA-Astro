# ASTRO-EXEC-002 — Phase 2 Interface Contract

**Status:** G1 implementation contract for deterministic execution infrastructure. This package
performs no astronomy, scientific computation, dataset acquisition, orbit propagation, estimator
logic, experiment selection, statistics, rendering, or empirical-ledger mutation.

## Package boundary

`astro_exec` is separate from the legacy `asa_astro` proof of concept. No module under
`src/astro_exec/` may import `asa_astro` or a renderer. `tests/exec/test_architecture.py` enforces
that boundary over the Python AST.

Reserved namespaces `analysis`, `data`, `experiment`, `orbits`, and `results` are empty package
markers for later phases. Their presence does not authorize later-phase implementation.

## Public package surface

| Interface | Contract | Explicit non-responsibility |
|---|---|---|
| `astro_exec.core.canonical_json` | Canonical UTF-8 JSON: sorted keys, compact whitespace, shortest round-trip finite floats, declared array order, fixed UTC timestamp form, fail-closed unsupported values | No scientific encoding |
| `astro_exec.core.hashing` | SHA-256 bytes/stream/file/object hashing, typed `SHA256Digest`, typed Git SHA-1 `GitBlobDigest`, validation and mismatch failure | Never substitutes Git identity for content identity |
| `astro_exec.core.ids` | Separate artefact, configuration, run, invocation, provenance, and transformation identity types derived from canonical authoritative inputs | No wall-clock, random, hostname, PID, or scientific identity resolution |
| `astro_exec.core.config` | Packaged versioned JSON Schema validates TOML; unknown fields rejected; immutable dataclasses; canonical snapshot and fingerprint; explicit no-defaults policy | No scientific defaults; Phase 2 accepts `dry-run` only |
| `astro_exec.core.frozen` | Loads the explicit repository manifest; checks SHA-256 and Git blob identity; rejects missing, changed, symlink-substituted, escaping, or prohibited extra artefacts | Never alters or discovers frozen material implicitly |
| `astro_exec.core.provenance` | Typed source, environment, derived artefact, transformation and relationship records; immutable content-addressed DAG | Dry runs create no scientific result provenance |
| `astro_exec.core.logging` | Canonical JSONL with severity, component, run, provenance, sequence, and diagnostic-only classification | Timestamps and logs cannot influence replay identity or scientific evidence |
| `astro_exec.core.leakage_guard` | Default-deny role capabilities; resolved repository-relative reads/writes; traversal and symlink escape rejected | Does not expand capabilities dynamically |
| `astro_exec.core.lifecycle` | `proposed → validating → ready → executing → completed/failed → sealed`; legal transitions carry content-addressed provenance | No experiment sequencing or mutable global state |
| `astro_exec.core.run_package` | Sealed `EH-0` infrastructure package with software commit, config, environment, drift receipt, provenance, lifecycle, verification instructions, and checksums | Emits no dataset or authoritative-scientific value |
| `astro_exec.core.replay` | Offline file-set, checksum, configuration, run-identity, lifecycle and classification verification | No network, acquisition, or scientific re-execution |
| `astro_exec.core.determinism` | Byte-compares the declared authoritative-content inventories of two packages | Invocation diagnostics and logs are outside authoritative equivalence |
| `astro_exec.estimator.interface` | Opaque target envelope and `FrozenEstimator` protocol | `UnresolvedEstimator` raises `UR-001`; no estimator is supplied |
| `astro_exec.roles` | Four role identities and infrastructure-only dry-run result | No role performs protocol or scientific work |
| `astro_exec.cli` | `version`, `validate-config`, `validate-frozen`, `dry-run`, and `verify`; compatibility aliases `run --dry-run` and `replay` | No acquisition, dataset, estimator, measurement, or scientific command |

Every public class and function has a docstring. The public-interface AST audit is part of G1
validation.

## Configuration contract

`config/astro-exec-phase2.toml` explicitly declares:

- schema version `astro-exec-config-v1`;
- no implicit or applied defaults;
- `dry-run` execution mode;
- `config/frozen-artefacts-v1.json` as the sole frozen-manifest path;
- immutable read/write capability roots for custodian, truth laboratory, ASA laboratory, and
  statistician.

The JSON Schema is packaged at
`src/astro_exec/contracts/astro-exec-config-v1.schema.json`; installation therefore does not depend
on ancestor discovery or an implicit source checkout.

## Frozen boundary

The frozen manifest records both content SHA-256 and Git blob SHA-1 for six artefacts. The theory
document has `document_status: mixed`: **Part A — Version 1 Deterministic Core** is `frozen`, while
**Part B — Candidate Enrichments** is `candidate-not-frozen`. Whole-file byte integrity protects the
record without broadening Part B's semantic status.

Verification finishes before the output directory is created. Any drift raises
`FrozenArtefactDrift` with an exact `drift_type`; there is no warning-and-continue route.

## Deterministic package and invocation boundary

```bash
astro-exec dry-run \
  --config config/astro-exec-phase2.toml \
  --repository-root . \
  --run-label independent-review-a \
  --output /tmp/astro-run-a

astro-exec verify /tmp/astro-run-a
```

The output path must not exist. Run identity derives only from the validated configuration,
verified frozen-artefact receipt and manifest digest, dependency environment, package schema, and
full software commit. `run_label` derives an `InvocationIdentity` and is written only to the sibling
`/tmp/astro-run-a.invocation.json`, classified `diagnostic-non-authoritative`. It does not occur in
the package or `AUTHORITATIVE-CONTENT.sha256`.

Identical authoritative inputs therefore produce the same run ID and byte-identical authoritative
files. `logs/events.jsonl` and the sibling invocation record are diagnostic and cannot be cited as
scientific evidence. All dry-run packages remain `EH-0` and contain no
`authoritative-scientific` classification.

## Downstream constraints

Later operators may rely only on these published interfaces after programme acceptance of G1. They
must not infer a scientific implementation from a reserved namespace, import `asa_astro`, modify a
frozen artefact, add a scientific default, close an unresolved requirement, or treat Phase 2 output
as empirical evidence.
