# REPOSITORY-STRUCTURE-0001 — Minimal Information Architecture

## Document control

| Field | Value |
|---|---|
| Status | Proposed minimal repository structure and collision-avoidance boundary |
| Purpose | Give every proof-of-concept artefact one durable destination without speculative scaffolding |
| Authority limit | Does not assign ASA authority or preselect an implementation language |

## 1. Design constraints

The repository structure MUST:

- serve one ASA-Astro proof of concept in this repository only;
- keep ASA constitutional and canonical material outside the repository;
- make the ASA dependency explicit and immutable;
- keep domain meaning separate from implementation and run results;
- make source, evidence, entity, relationship, computation, and validation
  artefacts traceable;
- prevent overlapping operator ownership;
- add directories only when a real, reviewed artefact exists;
- avoid framework, service, deployment, and enterprise layers not required by
  the proof of concept;
- support deterministic tests and reconstruction from repository truth.

Empty directories, placeholder modules, duplicate “v2” documents, personal
workspaces, notebooks containing authoritative logic, and copied ASA material
are prohibited.

## 2. Current minimal structure

The foundation stage needs only the following files:

```text
ASA-Astro/
├── docs/
│   ├── architecture/
│   │   └── REPOSITORY-STRUCTURE-0001.md
│   ├── foundation/
│   │   └── ASA-ASTRO-0001-foundational-definition.md
│   ├── models/
│   │   └── ASTRO-CONTEXT-MODEL-0001.md
│   ├── ontology/
│   │   ├── ASTRO-ONTOLOGY-0001.md
│   │   └── ASTRO-RELATIONSHIP-TAXONOMY-0001.md
│   └── validation/
│       └── ASTRO-VALIDATION-FRAMEWORK-0001.md
└── governance/
    └── decision-register.md
```

No implementation, sample data, schema, dependency lock, or benchmark is
authorised merely because this document names a future destination.

## 3. Smallest defensible growth structure

Directories below MUST be created just in time, with their first substantive
artefact. Bracketed annotations explain responsibility and are not directory
names.

```text
ASA-Astro/
├── README.md                         [entry point once authorised]
├── docs/                             [durable meaning and operator guidance]
│   ├── architecture/
│   ├── foundation/
│   ├── models/
│   ├── ontology/
│   └── validation/
├── governance/                       [decision and authority records]
├── dependencies/
│   └── asa-dependency.lock           [exact upstream ASA identity/interface]
├── schemas/                          [machine-readable record contracts]
│   ├── observation/
│   ├── entity/
│   ├── relationship/
│   ├── reasoning/
│   └── validation/
├── src/
│   └── asa_astro/
│       ├── evidence/                 [source through Candidate Entity]
│       └── reasoning/                [relationships through Explanation Trace]
├── tests/
│   ├── contract/                     [cross-component and schema invariants]
│   ├── integration/                  [bounded pipeline tests]
│   └── unit/                         [mirrors owned executable modules]
└── validation/
    ├── benchmarks/                   [frozen protocols and context manifests]
    ├── datasets/                     [manifests/digests, not uncontrolled data]
    ├── fixtures/                     [small licensed or synthetic test fixtures]
    ├── ground-truth/                 [versioned reference manifests/labels]
    └── results/                      [immutable formal Validation Results]
```

The `asa-dependency.lock` filename is a logical destination; its serialization
and verification mechanism remain an open decision. It MUST eventually identify
an immutable ASA version/commit, source URI, integrity digest, consumed
interface, and compatibility rule. It MUST NOT contain copied constitutional
text.

The language-specific package and build files needed by an authorised
implementation MAY be added at repository root. The implementation language and
toolchain are intentionally not selected here.

## 4. Directory responsibilities

### 4.1 `docs/`

Contains stable human-readable definitions, contracts, and validation logic.
Documents MUST have distinct purposes and stable identifiers. Existing documents
SHOULD be revised with recorded changes instead of copied into parallel editions.

### 4.2 `governance/`

Contains repository-local decisions and unresolved authority questions. It MUST
NOT contain copied ASA constitutional material. The decision register records
questions; it does not grant an operator authority to resolve them.

### 4.3 `dependencies/`

Contains machine-verifiable external dependency identities and compatibility
information. It MUST NOT vendor ASA by default. Any vendoring exception requires
licence, integrity, update, and non-authority rules recorded by human decision.

### 4.4 `schemas/`

Contains machine-readable contracts mapping the ontology to representations.
Each schema MUST identify its owning concept/document version and MUST have
positive and negative fixtures or tests. Schemas MUST preserve provenance,
uncertainty, lifecycle, and conceptual separations.

### 4.5 `src/asa_astro/evidence/`

Contains the bounded path from source manifests through detector/representation
records, Evidence and Provenance Records, Light Regions, and Candidate Entity
formation/resolution adapters. It MUST NOT implement Significance.

### 4.6 `src/asa_astro/reasoning/`

Contains Relationship Assertion/classification, Standing adapter/computation,
Context validation, Significance adapter/computation, and Explanation Trace
generation under the locked ASA dependency. Source-ingestion logic MUST NOT be
duplicated here.

### 4.7 `tests/`

Contains executable verification. Each operator owns unit and schema tests for
their artefacts; end-to-end validation ownership does not transfer local test
responsibility. Tests MUST include falsification cases, not only successful
examples.

### 4.8 `validation/`

Contains frozen benchmark contracts and immutable results. Large or licensed
scientific data SHOULD remain in an authoritative external store referenced by
manifest and digest. A local dataset is permitted only when its licence,
provenance, size, and reason for repository storage are explicit.

## 5. Operator ownership boundaries

These are proposed manufacturing boundaries for collision avoidance. They do
not authorise unresolved scientific or ASA decisions. Human confirmation is
recorded as an open decision.

| Operator | Primary owned outputs | Must not manufacture |
|---|---|---|
| Codex A — Foundation and ontology | `docs/foundation/`, `docs/ontology/`, `docs/models/`, `docs/architecture/`, the framework definition in `docs/validation/`, and curation of open questions in `governance/decision-register.md` | Image-processing code, significance-engine code, scientific labels, benchmark results, or unilateral closure of authority decisions |
| Codex B — Observation and evidence contracts | Observation/source/detector/evidence/entity schemas; `src/asa_astro/evidence/`; owned unit/contract tests and small fixtures | Redefining ontology meaning, implementing Significance, selecting Ground Truth, or editing Codex C/D owned files without an integration record |
| Codex C — Relationship and reasoning implementation | Relationship/reasoning schemas; `src/asa_astro/reasoning/`; ASA adapter; Standing, Context, Significance, and Explanation Trace implementation; owned unit/contract tests | Changing ASA meaning, collapsing Standing into Significance, source-ingestion duplication, or declaring validation success |
| Codex D — Benchmark and independent validation | `validation/` benchmark/reference manifests, held-out protocols, formal results, integration tests, and result reports | Tuning implementation against held-out labels, redefining Context after results, implementing production logic to improve a score, or declaring scientific discovery |

Shared files MUST have one session owner. Integration changes to another
operator's file require: a stated necessity, minimal diff, tests, and a report
naming the owner-facing impact. `governance/decision-register.md` is curated by
Codex A but only the authorised human decision owner may close authority items.

## 6. Interface boundaries

The minimum component interfaces are immutable record bundles, not implicit
in-process state:

```text
Evidence boundary:
  Observation Source / Observation / Detector Output
  → Evidence + Provenance + Candidate/Resolution records

Reasoning boundary:
  versioned entity/evidence bundle
  → Relationship Assertions and classifications
  → separate Standing result
  → frozen Context + selected ASA dependency
  → Significance result + Explanation Trace + Provenance

Validation boundary:
  frozen Benchmark + Ground Truth + formal outputs
  → immutable Validation Result
```

Serialization is undecided, but every boundary MUST support stable identifiers,
schema versions, explicit missingness, units/frame/epoch as applicable,
provenance links, and content integrity checks.

No component may query hidden conversation state, mutable notebooks, or
unversioned personal files to complete a formal run.

## 7. Naming and versioning

- Durable normative documents use stable uppercase identifiers and a numeric
  series, as established by the initial foundation documents.
- A document correction SHOULD update the existing file and repository history;
  a new identifier is justified only by a new contract, not by editing
  convenience.
- Schemas and formal record types MUST carry semantic versions independent of
  filenames and MUST identify the governing ontology version.
- Benchmark and result directories MUST use stable identifiers, not “latest”,
  “final”, operator names, or conversational labels.
- Generated output MUST be reproducible and either ignored as build material or
  committed as an explicitly authoritative Validation Result; ambiguous output
  MUST NOT accumulate.

## 8. Repository hygiene and integration gates

Before adding a file or directory, an operator MUST establish:

1. its unique responsibility and owner;
2. the existing artefact it depends on or improves;
3. why it is not duplicate or speculative;
4. its evidence/provenance obligations;
5. its tests, validation criteria, or falsification criteria;
6. its integration consumer;
7. the decision record for any unresolved authority.

Before integration, changes MUST pass applicable checks:

- repository remains on the canonical development line;
- no unexpected untracked or overlapping operator files exist;
- links and stable identifiers resolve;
- schemas validate positive and negative fixtures;
- executable components pass unit, contract, and determinism tests;
- no ASA canonical content is present;
- dependency and data provenance are explicit;
- no Significance field is intrinsic to an entity;
- the manufacturing report records files, decisions, assumptions, tests,
  limitations, requirements, and blockers.

## 9. Explicit non-structure

The proof of concept does not presently justify microservices, databases,
message buses, plugin systems, web/mobile applications, deployment clusters,
model registries, broad astronomy catalogues, multiple packages, or separate
repositories. If a future requirement genuinely needs one, it requires a
decision supported by evidence and an integration plan; it MUST NOT be added as
anticipatory scaffolding.

## 10. Structure validation criteria

This proposal is acceptable only if:

- every requested and foreseeable first-implementation artefact has one clear
  destination;
- no destination duplicates another operator's responsibility;
- the foundation can remain valid if implementation language changes;
- external data and ASA remain explicit dependencies rather than copied truth;
- future directories can be added just in time without reorganising the
  foundation.

It is falsified if operators need parallel repositories, private authoritative
workspaces, duplicated domain definitions, or hidden cross-component state to
implement the bounded pipeline.
