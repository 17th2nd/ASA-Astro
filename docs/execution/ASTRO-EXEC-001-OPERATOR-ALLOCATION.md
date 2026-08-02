# ASTRO-EXEC-001 — Operator Allocation

Bounded component ownership enabling multiple AI operators to work independently. **Parallel development must not create parallel authority.** All accepted work converges continuously on GitHub `main`.

## 1. Binding rules

1. **`main` is the only authority.** No development branch, no worktree as an authoritative state, no temporary directory as a substitute, no local-only completed work, no uncommitted completed deliverable.
2. **No operator may consume another operator's unpublished work.** If you need an interface, it must already be on `main`. If it is not, you are blocked — report the block; do not assume a shape.
3. **One owner per file.** Two operators never edit the same file in the same package. Shared contracts are owned by Operator A exclusively.
4. **Interface before implementation.** A dependent component may begin only after its dependency's interface and contract tests are published and verified remotely.
5. **Publish small, publish often.** Each bounded unit is manufactured, validated, reviewed, committed, pushed, verified from the remote, and recorded before the next begins.
6. **No `UR` may be closed by an implementer.** Blocked code fails closed with `UnresolvedRequirement("UR-00n")`.

## 2. Allocation

### Operator A — Core Architecture and Contracts
**Owns:** `src/astro_exec/core/**`, all shared schemas, `estimator/interface.py`, repository-wide conventions.
**Delivers:** identifiers, canonical JSON, hashing, configuration model, provenance model, error taxonomy, logging, `LeakageGuard`, run lifecycle, module interface definitions.
**Depends on:** nothing. **Blocks:** everyone.
**Gate:** no other operator starts until A's Phase 2 contracts are published and verified on `main`.

### Operator B — Data and Evidence
**Owns:** `src/astro_exec/data/**`, `validation/fixtures/exec/data/**`.
**Delivers:** dataset registry, acquisition, hashing, cache, Gaia/DE440/SB441-N16 loaders, Horizons capture-replay, preprocessing, evidence records, eligibility, ordering.
**Depends on:** A. **Blocked by:** `UR-003`, `UR-004`, `UR-007`.

### Operator C — Orbital Core
**Owns:** `src/astro_exec/orbits/**`, `crates/astro_integrator/**`.
**Delivers:** force model with EIH, integrator crate and FFI, posterior construction, timescales, frames, streaming reduction.
**Depends on:** A for contracts; B for ephemeris loaders. **Blocked by:** `UR-005`, `UR-006`.
**Note:** the single highest-risk component. Numerical defects here are silent and corrupt every downstream number.

### Operator D — Experiment and Validation
**Owns:** `src/astro_exec/experiment/**`, `src/astro_exec/analysis/**`.
**Delivers:** controller, apparatus checks, LOO comparator, sealing, $\delta_t$, endpoint, metrics, statistics, validation, F-classification, claim comparator.
**Depends on:** A, C. **Blocked by:** `UR-010`.

### Operator E — Results and Interfaces
**Owns:** `src/astro_exec/results/**`, `src/astro_exec/cli/**`, `src/astro_exec/roles/**`.
**Delivers:** run package, artefact classification, reports, ledger candidate generator, CLI, read-only inspection API, visualisation export boundary, adapter specifications.
**Depends on:** A, D. **Blocked by:** `UR-009`.

## 3. Integration order

```
A (core contracts)
   ├─► B (data)  ─────┐
   ├─► C (orbits) ────┼─► D (experiment, validation) ─► E (results, CLI)
   └─────────────────┘
```

A must complete Phase 2 alone. B and C then proceed in parallel — they share only A's contracts and B's ephemeris loaders, which B publishes first. D integrates. E finishes.

## 4. Conflict prevention

| Mechanism | Rule |
|---|---|
| File ownership | Exactly one owner per path. Cross-package edits require an interface change request to A |
| Shared schemas | A owns all of them. No operator adds a field to a shared schema |
| Fixtures | Owned by the operator who owns the consuming module; shared reference fixtures owned by A |
| Tests | Each operator owns tests for their own package; integration tests spanning packages are owned by D |
| Commit boundary | One bounded unit per commit; never mix packages in one commit |
| Publication | Push and verify remotely before the next unit; no stacked unpublished work |
| Interface change | Any change to a published interface requires A's approval and a contract-test update in the same commit |

## 5. Handoff artefact

Every completed unit publishes a handoff record containing: unit id and owner; commit id verified on `origin/main`; interfaces added or changed; contract tests added; fixtures added; known limitations; open `UR` dependencies; what the next operator may now assume.

**The last line matters most.** It is the only thing a downstream operator is permitted to rely on. Anything not in a published handoff does not exist.

## 6. Acceptance authority

| Work | Accepted by |
|---|---|
| Interface and schema changes | Operator A |
| Scientific correctness of a numerical routine | Operator C plus an independent reviewer |
| Protocol conformance of any experiment behaviour | Operator D, citing the `ASTRO-EXP-0001` section |
| Ledger conformance | Operator E, citing the `ASTRO-RESULTS-0001` section |
| Phase completion | Human custodian, against the acceptance gates |
| Any `UR` closure | Human custodian only |

**No operator accepts their own scientific correctness.** A test written by the same operator who wrote the routine validates implementation behaviour; the acceptance criterion is frozen scientific intent, which requires a second reader citing the protocol.
