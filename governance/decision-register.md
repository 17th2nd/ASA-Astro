# ASA-Astro Decision Register

## Purpose

This register preserves unresolved architectural, scientific, data, validation,
and integration questions. An open item is not permission for an operator to
choose a convenient answer. Formal components MUST either remain blocked by the
item or represent the uncertainty explicitly.

## Status vocabulary

- **Open:** no authorised decision exists.
- **Evidence gathering:** authorised investigation is in progress; no decision
  has been made.
- **Proposed:** a concrete option and evidence await the decision owner.
- **Decided:** the decision owner has supplied a dated decision and rationale.
- **Superseded:** a later decision record replaces the item without erasing it.

Only the named human decision owner, or an explicitly delegated authority, may
set an item to **Decided**. A decision MUST identify date, decision, rationale,
evidence, affected artefacts, implementation owner, and review trigger.

## Open decisions

### DR-0001 — ASA dependency identity and interface

- **Status:** Open
- **Question:** Which immutable ASA version or commit, distribution source, and
  standing/context/significance interface will ASA-Astro consume?
- **Why unresolved:** The repository began without a dependency lock or an
  authoritative interface selection. ASA-Astro has no authority to invent one.
- **Blocks:** Executable Standing or Significance integration; any ASA
  conformance claim.
- **Current constraint:** Adapters may be designed at a conceptual boundary only.
  No ASA canonical material may be copied into this repository.
- **Evidence required:** Upstream ASA release/commit identity, interface
  documentation, integrity mechanism, licence/access terms, and compatibility
  expectations.
- **Decision owner:** Human programme operator with ASA constitutional authority.

### DR-0002 — Operator B, C, and D ownership confirmation

- **Status:** Open
- **Question:** Are the collision-avoidance boundaries proposed in
  `REPOSITORY-STRUCTURE-0001` the authorised manufacturing assignments for
  Codex B, C, and D?
- **Why unresolved:** Only Codex A's role was explicitly assigned in the
  manufacturing instruction.
- **Blocks:** Creation of B/C/D implementation or validation files where
  ownership could overlap.
- **Current constraint:** Codex A owns only the requested non-implementation
  foundation. Other operators must not infer authority from the proposal.
- **Evidence required:** Human assignment identifying each operator's files,
  interfaces, and integration responsibilities.
- **Decision owner:** Human programme operator.

### DR-0003 — Initial illustrative image identity and use authority

- **Status:** Open
- **Question:** What exact source image will seed the proof of concept, and what
  are its provider, identifier, version, digest, licence, calibration state,
  observing band, instrument, epoch, and limitations?
- **Why unresolved:** No image or source manifest exists in the repository.
- **Blocks:** Source ingestion, detector fixtures derived from the image, and any
  image-specific demonstration.
- **Current constraint:** No object identity or scientific claim may be inferred
  from an unspecified image.
- **Evidence required:** Source archive record, original bytes or authorised
  retrieval method, metadata, digest, licence, and integrity check.
- **Decision owner:** Human programme operator, advised by a domain-qualified
  scientific reviewer.

### DR-0004 — Reference catalogue and Ground Truth sources

- **Status:** Open
- **Question:** Which catalogue releases, expert-labelled references, or
  controlled synthetic sources will serve as scoped Ground Truth for each
  benchmark proposition?
- **Why unresolved:** No reference corpus, licence, or independent adjudication
  protocol has been selected.
- **Blocks:** Formal benchmark execution and validation claims.
- **Current constraint:** The illustrative image is not Ground Truth. Model
  outputs cannot label themselves.
- **Evidence required:** Candidate source comparison covering scientific scope,
  uncertainty, selection effects, independence, versioning, licence, and
  machine access.
- **Decision owner:** Human programme operator with a domain-qualified scientific
  reviewer and validation operator.

### DR-0005 — First bounded scientific question and “primary galaxy” rule

- **Status:** Open
- **Question:** Which one or more Context questions will form the first
  benchmark, and how will any “primary galaxy” or system boundary be identified
  without using brightness, image size, or central placement as a shortcut?
- **Why unresolved:** The context profiles are semantic templates, not a selected
  benchmark scope.
- **Blocks:** Context freezing, target selection, Ground Truth scope, and metric
  design.
- **Current constraint:** “Primary” must be supplied by an authorised reference
  or reproducible system rule with uncertainty.
- **Evidence required:** Scientific purpose, candidate system/reference set,
  system-boundary evidence, and feasibility of independent evaluation.
- **Decision owner:** Human programme operator with a domain-qualified scientific
  reviewer.

### DR-0006 — Entity-resolution policy

- **Status:** Open
- **Question:** Which matching evidence, catalogue identifiers, coordinate/epoch
  transformations, thresholds, contested-match representation, and review rules
  distinguish Candidate from Resolved Entity?
- **Why unresolved:** Resolution depends on the selected data and scientific
  sources.
- **Blocks:** Resolved Entity schemas, cross-observation joins, and relationship
  endpoint evaluation.
- **Current constraint:** Detector outputs and Light Regions may create
  candidates only. Unknown or multiple matches must remain representable.
- **Evidence required:** Data characteristics, catalogue uncertainty, matching
  literature/methods, positive and negative match fixtures, and calibration
  plan.
- **Decision owner:** Human programme operator with domain and evidence-pipeline
  reviewers.

### DR-0007 — Coordinate, epoch, time, unit, and band conventions

- **Status:** Open
- **Question:** Which canonical internal conventions and conversion libraries
  will be used for coordinates, reference frames, epochs/time standards, units,
  spectral bands, and redshift/distance representations?
- **Why unresolved:** The correct choice depends on source/reference data and
  implementation toolchain.
- **Blocks:** Machine schemas and cross-source comparison.
- **Current constraint:** Source values must retain original convention metadata;
  no implicit conversion or unitless scientific value is permitted.
- **Evidence required:** Selected source conventions, relevant scientific
  standards, conversion-library verification, and round-trip fixtures.
- **Decision owner:** Human programme operator with a domain-qualified scientific
  reviewer and implementing operator.

### DR-0008 — Context weighting policy and declaration authority

- **Status:** Open
- **Question:** Who may authorise Contexts, and what versioned weighting/rule
  policy will each first benchmark Context use?
- **Why unresolved:** Choosing weights is a scientific and programme decision,
  not a foundation-writing task.
- **Blocks:** Executable Context declarations and Significance computation.
- **Current constraint:** No hidden/default weights; contexts must be frozen
  before held-out evaluation and tested for sensitivity.
- **Evidence required:** Context purpose, eligible evidence/relationships,
  scientific rationale, baseline comparison, sensitivity design, and approval
  record.
- **Decision owner:** Human programme operator with domain and validation advice.

### DR-0009 — Standing contract and admissible inputs

- **Status:** Open
- **Question:** How does the selected ASA version define Standing, which
  astronomy-domain inputs are admissible, and how are invalid, contested, or
  expired Standing results represented?
- **Why unresolved:** Standing is ASA-owned and no ASA dependency is selected.
- **Blocks:** Standing schema/implementation and its interface to Significance.
- **Current constraint:** Standing must remain free of hidden Context weighting
  and cannot be replaced by brightness, confidence, or significance.
- **Evidence required:** Upstream ASA contract plus proposed domain mapping and
  falsification fixtures.
- **Decision owner:** Human programme operator with ASA authority.

### DR-0010 — Significance output semantics

- **Status:** Open
- **Question:** Will each Context output an ordering, graded rank, bounded score,
  category, set selection, or another ASA-compatible result, and what are tie,
  normalisation, comparability, and indeterminate semantics?
- **Why unresolved:** No ASA interface or first Benchmark has been selected.
- **Blocks:** Significance result schema, ranking metrics, and acceptance
  thresholds.
- **Current constraint:** Every result is Context-specific and may not be stored
  on the entity or compared across Contexts without explicit normalisation.
- **Evidence required:** ASA contract, intended user/reasoning question,
  reference-label form, baseline feasibility, and sensitivity implications.
- **Decision owner:** Human programme operator with ASA and validation reviewers.

### DR-0011 — Confidence vocabulary and uncertainty calibration

- **Status:** Open
- **Question:** Which propositions receive calibrated probabilities, which use
  categorical confidence, which uncertainty forms are required, and which
  calibration datasets and metrics are acceptable?
- **Why unresolved:** Calibration feasibility depends on reference sample size,
  dependency structure, and output semantics.
- **Blocks:** Final Evidence, Candidate, Relationship, Standing, and Significance
  schemas; calibration acceptance criteria.
- **Current constraint:** `uncalibrated` must be representable; confidence cannot
  equal magnitude, significance, or source count.
- **Evidence required:** Label availability, sample-size analysis, uncertainty
  sources, dependency model, candidate scoring/calibration methods, and domain
  review.
- **Decision owner:** Human programme operator with scientific and validation
  reviewers.

### DR-0012 — Permitted relationship propagation

- **Status:** Open
- **Question:** Which taxonomy subtypes, if any, may use bounded transitive or
  recursive propagation in Standing or Significance, at what depth, with what
  decay/normalisation and uncertainty rules?
- **Why unresolved:** The taxonomy permits only narrow type-specific candidates;
  no computation or benchmark justifies a policy yet.
- **Blocks:** Propagating relationship engine features.
- **Current constraint:** Propagation is off by default. Any implementation must
  be bounded, cycle-safe, uncertainty-aware, and ablated.
- **Evidence required:** Scientific rationale, formal rule, termination proof or
  bound, error analysis, fixtures, negative controls, and benchmark plan.
- **Decision owner:** Human programme operator with reasoning and validation
  reviewers.

### DR-0013 — Admission of inferred dark-matter-mediated assertions

- **Status:** Open
- **Question:** Will the first proof of concept admit inferred
  dark-matter-mediated assertions, and if so which independent evidence,
  physical models, alternative hypotheses, and confidence rules are mandatory?
- **Why unresolved:** An illustrative image cannot support the claim, and the
  required scientific reference/model scope is unspecified.
- **Blocks:** Production use of that Relationship Type and any associated
  Context feature.
- **Current constraint:** The type may exist in the ontology, but assertions are
  inadmissible until this decision is made. Invisibility is not dark-matter
  evidence.
- **Evidence required:** Domain-reviewed model/evidence protocol, alternative
  model treatment, calibration method, and negative controls.
- **Decision owner:** Human programme operator with a domain-qualified scientific
  reviewer.

### DR-0014 — Benchmark partitions, metrics, and numeric thresholds

- **Status:** Open
- **Question:** What independence unit, train/tune/evaluation partition, metric
  set, uncertainty interval, success threshold, non-inferiority margin, false-
  relationship penalty, and critical-failure rule will the first Benchmark use?
- **Why unresolved:** These choices require selected data, references, contexts,
  and claimed outcomes.
- **Blocks:** Frozen Benchmark and any validation conclusion.
- **Current constraint:** Values must be fixed before held-out evaluation and may
  not be chosen from observed test results.
- **Evidence required:** Dataset/reference characteristics, sample-size and
  dependence analysis, cost rationale, baseline pilot restricted to tuning data,
  and validation review.
- **Decision owner:** Human programme operator with independent validation and
  scientific reviewers.

### DR-0015 — Implementation language, serialization, and toolchain

- **Status:** Open
- **Question:** Which language, package/build system, machine-record
  serialization, schema technology, astronomy libraries, and supported runtime
  will be used?
- **Why unresolved:** The foundation is language-independent and no implementing
  operator assignment or dependency analysis exists.
- **Blocks:** Executable scaffolding, formal schema files, and environment lock.
- **Current constraint:** No speculative scaffolding or placeholder architecture;
  the choice must support deterministic tests, scientific units/coordinates,
  and record/provenance integrity.
- **Evidence required:** Minimal option comparison, library maintenance and
  scientific fitness, deterministic/reproducible build support, licensing, and
  operator capability.
- **Decision owner:** Human programme operator advised by implementing operators.

### DR-0016 — Determinism and reproducibility environment

- **Status:** Open
- **Question:** What build/runtime lock, hardware/precision policy, random-seed
  policy, output canonicalisation, nondeterminism tolerance, and run-manifest
  format will define repeatability?
- **Why unresolved:** It depends on the toolchain and algorithms.
- **Blocks:** Determinism contract tests and formal benchmark execution.
- **Current constraint:** All randomness must be seeded and recorded; unexplained
  output-changing nondeterminism is unacceptable.
- **Evidence required:** Toolchain decision, reproducibility trials, numeric
  stability analysis, environment-capture method, and independent replay.
- **Decision owner:** Human programme operator with implementing and validation
  operators.

### DR-0017 — Scientific data storage and retrieval policy

- **Status:** Open
- **Question:** Which source/reference/fixture data may be committed, which must
  remain external, and how will retrieval, integrity, licence, availability,
  caching, and retirement be managed?
- **Why unresolved:** No data or licence is selected.
- **Blocks:** Dataset manifests and repository data additions.
- **Current constraint:** No uncontrolled large or restricted data; external data
  must be versioned and digest-verified; conversation links are insufficient.
- **Evidence required:** Dataset inventory, sizes, licences, availability/SLA,
  archival stability, integrity mechanism, and minimal fixture needs.
- **Decision owner:** Human programme operator with repository and scientific
  data reviewers.

### DR-0018 — Expert annotation and adjudication protocol

- **Status:** Open
- **Question:** If expert labels are used, who is qualified, what evidence will
  annotators receive, what rubric and blinding apply, how many independent
  judgements are required, and how will disagreement be retained/adjudicated?
- **Why unresolved:** No expert panel, task, or reference corpus exists.
- **Blocks:** Expert-derived Ground Truth.
- **Current constraint:** `indeterminate` and disagreement must be allowed;
  consensus cannot erase minority alternatives without a record.
- **Evidence required:** Annotation task design, conflict-of-interest and
  independence plan, rubric pilot, agreement metric, and adjudication authority.
- **Decision owner:** Human programme operator with a domain-qualified scientific
  and independent validation reviewer.

### DR-0019 — Ground Truth correction and contested-reference policy

- **Status:** Open
- **Question:** How will corrected, superseded, or contested catalogue/expert
  references affect prior Benchmarks and Validation Results?
- **Why unresolved:** No reference versioning or release policy exists.
- **Blocks:** Long-term interpretation of validation history.
- **Current constraint:** References and prior results must remain immutable;
  correction creates a new version and must not silently rewrite outcomes.
- **Evidence required:** Reference-source correction practices, result
  invalidation/re-evaluation policy, and traceability requirements.
- **Decision owner:** Human programme operator with governance and validation
  reviewers.

### DR-0020 — Repository review, release, and change authority

- **Status:** Open
- **Question:** What review evidence, human approval, commit signing, release
  tagging, and change-control process governs movement from foundation to
  implementation and from demonstration to formal Benchmark?
- **Why unresolved:** The repository began empty and contains no local release or
  review policy beyond the supplied single-main directive.
- **Blocks:** Claims of an authorised release, frozen Benchmark, or approved
  validation result.
- **Current constraint:** Work remains on the canonical `main` stream; no operator
  may ratify, merge, declare scientific validation complete, or create a release
  status without human authority.
- **Evidence required:** Human governance instruction defining reviewers,
  approvals, protected operations, release identifiers, and exception handling.
- **Decision owner:** Human programme operator.

## Register validation criteria

The register is complete enough for the foundation stage only if:

- every implementation-blocking unknown found in the foundation documents maps
  to an open item;
- operators can tell which work may proceed and which must stop;
- no item implies that silence is consent;
- closure requires evidence and an identified human authority;
- decided items will remain auditable rather than being deleted.

An operator discovering another unresolved architectural or scientific question
MUST add it before depending on an assumed answer.
