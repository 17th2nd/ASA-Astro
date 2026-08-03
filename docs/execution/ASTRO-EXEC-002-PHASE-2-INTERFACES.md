# ASTRO-EXEC-002 — Phase 2 Interface Contract

**Status:** implementation contract for the deterministic execution skeleton.  Infrastructure only;
no scientific computation, datasets, orbit propagation, estimator logic, or astronomy mathematics.

## Public package surface

| Interface | Contract | Explicit non-responsibility |
|---|---|---|
| `astro_exec.core.canonical_json` | UTF-8, sorted-key, compact canonical JSON; rejects non-finite and non-JSON values | No scientific encoding |
| `astro_exec.core.hashing` | SHA-256 for bytes, streams, files, and canonical fingerprints | No dataset acquisition |
| `astro_exec.core.ids` | Full SHA-256 content-derived identifiers; never time-, host-, PID-, or random-derived | No scientific identity resolution |
| `astro_exec.core.config` | Strict TOML load, exact-key validation, frozen dataclasses, canonical snapshot and fingerprint | No scientific defaults; Phase 2 accepts `dry-run` only |
| `astro_exec.core.frozen` | Verify all configured frozen artefacts before package creation; mismatch aborts | Does not alter frozen material |
| `astro_exec.core.provenance` | Immutable content-addressed nodes, parent-complete DAG, deterministic export | Dry runs create no authoritative scientific provenance |
| `astro_exec.core.logging` | Canonical JSONL with deterministic sequence; no ambient timestamp | Logs cannot enter scientific outputs |
| `astro_exec.core.leakage_guard` | Resolve filesystem paths and enforce role-specific read/write roots; symlink escape fails closed | Does not grant capabilities dynamically |
| `astro_exec.core.lifecycle` | Closed Phase 2 state machine ending in `DRY_RUN_COMPLETE` or `ABORTED` | No experiment sequencing |
| `astro_exec.core.run_package` | Complete empty `EH-0` package with checksums, provenance, config, environment, frozen-artifact receipt and logs | Emits no scientific result |
| `astro_exec.core.replay` | Offline checksum, config-fingerprint, lifecycle, classification and run-id verification | No live network access |
| `astro_exec.core.determinism` | Compare two packages after normalising only their declared run ids | No numerical tolerance |
| `astro_exec.estimator.interface` | Opaque target envelope and `FrozenEstimator` protocol from ASTRO-EXEC-001 §5.9 | `UnresolvedEstimator` always raises `UR-001`; no estimator supplied |
| `astro_exec.roles` | Four role identities and deterministic dry-run entry-point result | No role performs protocol or scientific work |
| `astro_exec.cli` | `run --dry-run` and offline `replay` | No measurement or acquisition command |

Reserved namespaces `data`, `orbits`, `experiment`, `analysis`, and `results` contain package markers
only. Their later phase owners may not assume any unpublished interface.

## CLI

```bash
astro-exec run --dry-run \
  --config config/astro-exec-phase2.toml \
  --repository-root . \
  --run-label independent-review-a \
  --output /tmp/astro-run-a

astro-exec replay /tmp/astro-run-a
```

The output path must not exist. `run_label` contributes only to the content-derived run identifier.
It is not serialized elsewhere. A second run with another label must therefore be byte-identical
after replacing the run-id value and excluding the checksum inventory whose hashes necessarily cover
that value.

## Role capabilities

Capabilities are immutable repository-relative roots loaded from the checked-in configuration.
`LeakageGuard` resolves the requested path and every configured root before comparing them. This
rejects absolute escape, traversal and symlink escape. The Phase 2 ASA-laboratory role can read only
`inputs/estimator` and write only `selections/asa`; it cannot read `truth`.

## Frozen artefacts

`config/astro-exec-phase2.toml` pins SHA-256 digests for the theory, theory freeze record, experiment,
claims, results ledger, and research-controls freeze report. Verification happens before the output
directory is created. A mismatch raises `FrozenArtefactDrift`; there is no warning-and-continue path.

## Downstream assumptions

Operators B–E may rely only on the interfaces listed above after G1 is verified on GitHub `main`.
They must not import `asa_astro`, modify shared schemas, add scientific defaults, resolve an open `UR`,
or treat a dry-run artefact as empirical evidence.
