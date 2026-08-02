# ASTRO-EXEC-001 — Technology Decision

Assessment against the workload `ASTRO-EXP-0001` actually defines, not against a hypothetical future one. The governing instruction is: **prefer the smallest technology stack capable of executing Version 1 correctly.**

## 1. The workload, sized

| Quantity | Value |
|---|---|
| Propagations, deployment | 27 targets × 32 draws × (1 full + 16 deletions + 2 selected) = **16,416** |
| Plus calibration, convergence repeats, apparatus checks | ≈20,000 total (matches EXP §Cost and duration) |
| Horizon / output | 20 years, daily → 7,306 epochs each |
| Bodies | 26 (Sun, Moon, 8 planets, Pluto, 16 asteroids) + test particle |
| Physics | Newtonian point-mass + EIH 1PN, $\beta=\gamma=1$ |
| Naive full-trajectory storage | ~3 TB — **rejected**, see §5 |
| Actual storage after streaming reduction | ~200 MB |

Two properties dominate every choice: **this is compute-bound**, and **the result must be bit-reproducible**.

## 2. Language assessment

| Candidate | Determinism | Numerics | Performance | Maintainability | AI-assisted dev | Verdict |
|---|---|---|---|---|---|---|
| **Python 3.12** | Good at language level; poor control under threaded BLAS | Excellent ecosystem — `erfa`, `jplephem`, `scipy` | Inadequate for 20,000 propagations in pure form | Excellent | Excellent | **Selected — orchestration, data, analysis, CLI** |
| **Rust** | Excellent — no UB, explicit FP, `Cargo.lock` reproducible | Adequate; hand-written integrator is small and auditable | Excellent | Good | Good | **Selected — integrator crate only** |
| **C++** | Achievable but requires discipline; compiler FP defaults hostile | Excellent | Excellent | Moderate | Moderate | Rejected — weakest dependency reproducibility of the three |
| Julia | Good | Excellent | Excellent | Moderate | Weaker tooling maturity here | Rejected — adds a third ecosystem for no decisive gain |

**Decision: Python primary, Rust for one bounded crate.**

Honest statement of the cost: two languages means an FFI boundary, two toolchains and two test runners. That is real complexity and it is accepted for one specific reason — **a pure-Python integrator cannot deliver both the throughput and the floating-point control this experiment requires**, and the numerical kernel is the one place where a defect silently corrupts every downstream number. The FFI surface is deliberately tiny: one function taking initial state, epoch grid, body set and tolerance, returning a trajectory or a streamed maximum. Everything else stays Python.

A pure-Rust engine was considered and rejected: it would discard the Gaia/JPL Python ecosystem and the repository's existing Python conventions for a gain confined to code already isolated in the crate.

## 3. Storage assessment

| Candidate | Verdict |
|---|---|
| **Parquet** | **Selected** for trajectories and tabular outputs. Columnar, typed, compressed, portable, deterministic with pinned writer version and fixed row order |
| **SQLite** | **Selected** for the run index and provenance lookup. Single file, zero-config, transactional, ubiquitous |
| **Canonical JSON** | **Selected** for manifests, context, selections, results, ledger candidates — anything a human or reviewer must read and digest-compare |
| DuckDB | Rejected — an analytical engine for a dataset that fits comfortably in memory. Adds a dependency for no decisive benefit at this scale |
| Apache Arrow as storage | Rejected — Arrow is an in-memory format; Parquet is the on-disk answer. Arrow may appear transitively via the Parquet writer, which is acceptable |
| Neo4j / graph DB | **Rejected** — the "graph" is 27 targets × 16 candidates. A graph database here is unjustified infrastructure |
| NetworkX | **Rejected** — same reason. The provenance DAG is traversed with a few dozen lines of typed Python |
| HDF5 | Rejected — heavier dependency, weaker determinism guarantees than pinned Parquet |
| GraphML | Rejected for the engine. It exists in the legacy image pipeline; `ASTRO-EXP-0001` requires no graph exchange format |

## 4. Rendering integration

**Godot and Unity: assessed, not adopted for Version 1.** Neither has any role in executing `ASTRO-EXP-0001`. The engine exposes read-only run packages; any renderer is a downstream consumer. Adapter specifications are Phase 9 work and are deliberately deferred until the data model has stabilised — specifying an adapter against an unstable schema produces churn, not capability.

The binding constraint is architectural and is testable now: **no engine module may import a rendering library** (`test_no_rendering_imports`).

## 5. The decisive engineering choice — streaming reduction

Storing every propagation would need ~3 TB. But the endpoint needs only

$$E_m(t)=\operatorname{median}_q\ \max_k\ \|\mathbf r_{full,q}(t_k)-\mathbf r^{(4)}_{m,q}(t_k)\|$$

so a reduced-model run needs the full trajectory **only to difference against it**. Therefore:

- store full trajectories once per (target, draw): 27 × 32 × 7306 × 3 × 8 B ≈ **151 MB**;
- stream every reduced and single-deletion propagation against the stored full trajectory, accumulating $\max_k$ on the fly;
- persist only the scalar $L_j$ and $E_m(t)$ values, plus per-target diagnostics.

This turns a storage-prohibitive problem into a modest one and removes any need for a distributed store. It is recorded here because it is the single choice that most shapes the stack: **it is why no big-data technology is required.**

## 6. Selected stack

| Layer | Selection | Pinning |
|---|---|---|
| Primary language | Python 3.12 | `.python-version`, `uv.lock` |
| Secondary language | Rust (stable, pinned) | `rust-toolchain.toml`, `Cargo.lock` |
| Numerical kernel | `crates/astro_integrator` — EIH N-body, strict FP | pinned toolchain + codegen flags |
| Ephemeris | DE440 via `jplephem`, SB441-N16 kernels | dataset digests |
| Time / frames | `erfa` (IAU SOFA) | version pinned |
| Tabular | Parquet via `pyarrow`, pinned writer version | dependency lock |
| Run index | SQLite (stdlib `sqlite3`) | — |
| Documents | Canonical JSON | in-house serializer, contract-tested |
| Config | TOML in → canonical JSON snapshot out | fingerprinted |
| Tests | `pytest`, `cargo test` | lock |
| CLI | stdlib `argparse` | — |
| Packaging | `pyproject.toml` + maturin for the crate | lock |

**Explicitly forbidden in the engine:** any web framework, ORM, plotting library, rendering library, `-ffast-math` or FMA contraction in the crate, threaded BLAS in any authoritative numerical path, and any dependency not present in the lock.

## 7. Floating-point policy (binding)

- IEEE-754 binary64 everywhere; no `f32` in any scientific path.
- Rust crate compiled without fast-math; FMA contraction disabled; no reassociation.
- Force accumulation uses Neumaier compensated summation in fixed body-index order.
- $\max_k$ and $\operatorname{median}_q$ evaluated in fixed index order. Median of 32 is the mean of sorted elements 16 and 17.
- Parallelism only across independent (target, draw) units; merged in canonical order; **no parallel reduction into a shared accumulator**.
- Byte-identical guaranteed on the pinned reference platform. Cross-platform contract: identical selections and identical $W$; $E_m(t)$ equal within the registered $\delta_t$.

## 8. Open technology dependencies

The integrator scheme, tolerance pair and "integration floor" are **not** engineering choices — they are outcome-relevant and blocked on **`UR-005`**. The Sobol direction numbers are blocked on **`UR-006`**. This document does not select them.
