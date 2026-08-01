# ASTRO-RESULTS-0001 — Permanent Empirical Results Ledger

## Document control

| Field | Value |
|---|---|
| Identifier | `ASTRO-RESULTS-0001` |
| Title | Permanent Empirical Results Ledger |
| Version | `1.0` — Version 1 freeze |
| Status | Frozen Version 1 controls; active append-only empirical ledger |
| Effective date | 2026-08-01 |
| Scope | ASA-Astro empirical experiments, results, evidence, claims, replications, datasets, calibrations, and publications |
| Protocol dependency | [`ASTRO-EXP-0001@1.0`](../benchmarks/ASTRO-EXP-0001.md) |
| Claims dependency | [`ASTRO-CLAIMS-0001@1.0`](../../docs/claims/ASTRO-CLAIMS-0001.md); experiment claims `ASTRO-CLM-0070`, `ASTRO-CLM-0071`, and `ASTRO-CLM-0072` |
| Supersession state | Initial canonical ledger; supersedes no earlier results ledger |
| Canonical location | `validation/results/ASTRO-RESULTS-0001.md` |
| Verification status | Verified for Version 1 freeze by [`ASTRO-V1-RESEARCH-CONTROLS-FREEZE-REPORT`](../../reports/ASTRO-V1-RESEARCH-CONTROLS-FREEZE-REPORT.md) |
| Current empirical state at freeze | Experiments executed: `0`; empirical results: `0`; evidence level: `EH-0` |
| Record schema | `ASTRO-RESULTS-RECORD/1.0.0` |
| Authority boundary | Records evidence; does not grant ASA authority, establish scientific truth, or validate claims beyond a recorded experiment's scope |
| Mutation rule | Existing content is immutable after establishment; all later changes are new events appended to the event stream |

## 1. Purpose

This document is the permanent empirical memory of the ASA-Astro programme.
It records what was attempted, what occurred, what evidence exists, what did
not occur, which claims changed status, and whether another party repeated or
reproduced a result.

The ledger MUST preserve positive results, negative results, inconclusive
results, failed experiments, protocol violations, corrections, contradictory
replications, withdrawn claims, obsolete dataset versions, superseded
calibrations, and retracted publications with equal permanence.

This ledger MUST NOT:

- convert an unexecuted protocol into a result;
- treat absence of evidence as a negative result;
- treat a failed or invalid experiment as evidence for or against its scientific
  claim unless that failure was itself a predeclared endpoint;
- infer a cause from an association unless the experiment supports that causal
  interpretation;
- generalise beyond the population, data, intervention, outcome, implementation,
  and conditions recorded in the result;
- replace measured values with narrative judgements;
- delete or silently rewrite an inconvenient record.

## 2. Permanent ledger invariants

### INV-R01 — Append only

Every future record MUST be appended as a new event at the end of §19. Existing
events, headings, definitions, identifiers, wording, order, and values MUST NOT
be edited in place.

### INV-R02 — Nothing is deleted

No result, evidence record, failure, claim, withdrawal, replication, dataset
version, calibration event, publication event, correction, or contradiction may
be removed. An unavailable external artefact remains represented by its original
record and a later `EVIDENCE_UNAVAILABLE` event.

### INV-R03 — Identifiers are permanent

An identifier is assigned once and never reused. A corrected, repeated,
reanalysed, or superseding record receives a new identifier and links to the
earlier record.

### INV-R04 — Corrections do not overwrite

An error is corrected by a `CORRECTION` event containing the erroneous record
identifier, the exact field or statement affected, the original value, the
corrected value, the reason, and the evidence for the correction. The original
record remains authoritative as a historical statement but is marked as
corrected when the event stream is resolved.

### INV-R05 — Supersession preserves history

A later dataset, calibration, analysis, claim, or publication may supersede an
earlier one only through a new event. Supersession changes prospective use; it
does not retroactively change the inputs or conclusions of an earlier result.

### INV-R06 — Outcome classes never silently change

A positive, negative, inconclusive, failed, invalid, or not-run state may be
reclassified only by an appended `RECLASSIFICATION` event. The event MUST state
which new evidence permits the reclassification and MUST preserve both labels.

### INV-R07 — Evidence precedes interpretation

Every empirical statement MUST resolve to Evidence IDs. Every interpretation
MUST be either the direct application of a predeclared decision rule or be
labelled as an interpretation with its evidentiary limit.

### INV-R08 — Negative evidence has equal permanence

Negative, null, contradictory, and failed outcomes receive the same mandatory
record fields, evidence retention, publication-history tracking, and replication
eligibility as positive outcomes.

### INV-R09 — Chronology is explicit

Every event records its observation or occurrence time, its ledger-entry time,
and the immediately preceding event identifier. Late registration is permitted
but MUST be labelled `late_entry: true` with the delay explained.

### INV-R10 — Rules do not change retroactively

Changes to this record schema or evidence hierarchy are `SCHEMA_AMENDMENT`
events. Earlier events remain interpreted under the schema version active when
they were recorded.

### INV-R11 — No mutable current-state summary

The current state is derived by replaying the append-only event stream. No
manually maintained “latest result” table may replace or obscure the stream.

### INV-R12 — Restricted evidence is still registered

Evidence that cannot be distributed MUST retain an Evidence ID, provenance,
digest where lawful, custodian, access conditions, and reason for restriction.
Restricted access MUST NOT be described as independent verification.

## 3. Identifier namespaces

| Record | Identifier form |
|---|---|
| Ledger event | `AR1-E000001` |
| Experiment protocol | `ASTRO-EXP-NNNN@N.N` |
| Execution attempt | `ASTRO-RUN-NNNNNN` |
| Result | `ASTRO-RES-NNNNNN` |
| Evidence item | `ASTRO-EVD-NNNNNN` |
| Claim | `ASTRO-CLM-NNNN` |
| Dataset version | `ASTRO-DATA-NNNNNN` |
| Calibration event | `ASTRO-CAL-NNNNNN` |
| Replication or reproduction | `ASTRO-REP-NNNNNN` |
| Publication object | `ASTRO-PUB-NNNNNN` |

Sequence numbers express identity and ledger order only. They do not express
importance, quality, authority, or evidentiary strength.

## 4. Event envelope

Every event appended to §19 MUST contain:

```yaml
event_id: AR1-E......
event_type: ...
schema_version: ASTRO-RESULTS-RECORD/1.0.0
previous_event_id: ...
occurred_at: ISO-8601 timestamp or explicit unknown
recorded_at: ISO-8601 timestamp
late_entry: true | false
recorded_by:
  name_or_stable_id: ...
  role: ...
authority_or_basis: ...
subject_ids: [...]
evidence_ids: [...]
supersedes: []
corrects: []
event_statement: ...
limitations: [...]
```

Unknown values MUST be written as `unknown`. Inapplicable fields MUST be written
as `not_applicable`. Blank fields, omitted adverse facts, and sentinel values
that could be mistaken for measurements are prohibited.

Permitted event types are:

- `LEDGER_ESTABLISHED`
- `EXPERIMENT_REGISTERED`
- `EXECUTION_STARTED`
- `EXECUTION_COMPLETED`
- `EXECUTION_ABORTED`
- `RESULT_RECORDED`
- `EVIDENCE_REGISTERED`
- `EVIDENCE_RESTRICTED`
- `EVIDENCE_UNAVAILABLE`
- `CLAIM_REGISTERED`
- `CLAIM_WITHDRAWN`
- `CLAIM_SUPERSEDED`
- `REPLICATION_REGISTERED`
- `REPRODUCTION_REGISTERED`
- `DATASET_REGISTERED`
- `DATASET_SUPERSEDED`
- `CALIBRATION_RECORDED`
- `CALIBRATION_SUPERSEDED`
- `CALIBRATION_DRIFT_DETECTED`
- `PUBLICATION_RECORDED`
- `PUBLICATION_STATUS_CHANGED`
- `CORRECTION`
- `RECLASSIFICATION`
- `SCHEMA_AMENDMENT`
- `LEDGER_AUDIT`

## 5. Result recording

### 5.1 What counts as a result

A result exists only when:

1. an identified execution attempt reached a predeclared measurement point;
2. the relevant observations and derived values were preserved as evidence;
3. protocol-integrity status was determined;
4. the predeclared analysis and decision rule were applied or a deviation was
   explicitly recorded;
5. the result was entered through a `RESULT_RECORDED` event.

A plan, protocol, simulation design, expected outcome, software test, informal
observation, unpublished recollection, or statement that an experiment “should”
work is not an empirical result unless it was itself the declared subject of an
experiment.

### 5.2 Mandatory result record

Every `ASTRO-RES-*` record MUST contain:

```yaml
result_id: ASTRO-RES-......
experiment_protocol_id: ASTRO-EXP-....@...
execution_ids: [...]
result_status: POSITIVE | NEGATIVE | INCONCLUSIVE | FAILED_EXPERIMENT | INVALID
protocol_integrity: VALID | VALID_WITH_DECLARED_DEVIATIONS | INVALID | UNDETERMINED
preregistration:
  locator: ...
  committed_at: ...
  integrity_identifier: ...
system_identity:
  repository_commit: ...
  executable_or_model_identity: ...
  dependency_versions: [...]
execution_environment: ...
dataset_version_ids: [...]
calibration_ids: [...]
population_and_sample:
  target_population: ...
  sampling_rule: ...
  sample_size_planned: ...
  sample_size_observed: ...
  exclusions: [...]
primary_endpoints:
  - endpoint: ...
    unit: ...
    observed_value: ...
    uncertainty: ...
    decision_threshold: ...
    decision: ...
secondary_endpoints: [...]
missing_or_censored_observations: [...]
protocol_deviations: [...]
analysis_identity: ...
evidence_ids: [...]
claim_ids_addressed: [...]
claim_impact: ...
evidence_level: EH-...
scope_limit: ...
interpretation: ...
independent_review: ...
```

The `interpretation` field MUST contain no statement broader than the recorded
claim impact and scope limit. If the decision rule supplies the only supported
interpretation, it MUST be quoted rather than paraphrased expansively.

## 6. Evidence recording

### 6.1 Evidence identity

Every evidence object receives one `ASTRO-EVD-*` identifier. Evidence includes
raw observations, source manifests, transformed data, logs, model outputs,
analysis outputs, environment captures, decisions, exclusions, protocol
deviations, reviewer attestations, and publication artefacts.

### 6.2 Mandatory evidence fields

```yaml
evidence_id: ASTRO-EVD-......
evidence_type: RAW | DERIVED | PROCEDURAL | DOCUMENTARY | REVIEW | PUBLICATION
title: ...
created_at: ...
created_by: ...
source_or_parent_evidence_ids: [...]
derivation_or_capture_method: ...
content_locator: ...
media_type_or_format: ...
byte_size: ...
content_digest:
  algorithm: ...
  value: ...
custodian: ...
access_status: PUBLIC | RESTRICTED | UNAVAILABLE
licence_or_use_authority: ...
independence_from_tested_system: ...
known_limitations: [...]
related_run_ids: [...]
related_result_ids: [...]
```

### 6.3 Evidence derivation

Derived evidence MUST name every source Evidence ID and the exact transformation
identity. A figure, table, summary statistic, or exported dataset is not a
substitute for its source evidence.

### 6.4 Missing and lost evidence

Missing evidence is recorded as missing, never inferred. If evidence is lost,
corrupted, access-revoked, or found to have a digest mismatch, a new event MUST
record the condition. Results dependent on it remain visible and may receive a
later reclassification; they are not erased.

## 7. Outcome classes

### 7.1 Positive result

`POSITIVE` means that a protocol-valid experiment met every predeclared
condition required for its bounded positive outcome. It does not mean that ASA
is true, generally valid, novel, useful elsewhere, or causally responsible for
the outcome unless those propositions were separately tested.

The record MUST include the observed effect, uncertainty, comparator, decision
threshold, protocol deviations, and exact bounded claim supported.

### 7.2 Negative result

`NEGATIVE` means that a protocol-valid experiment met its predeclared negative
decision rule or failed its predeclared positive rule where the protocol defines
that failure as a negative result.

A negative result MUST NOT be translated into proof of no effect unless the
design and uncertainty support the specified equivalence or non-inferiority
claim. A negative result remains negative even if later work is positive.

### 7.3 Inconclusive result

`INCONCLUSIVE` means that a valid execution produced interpretable measurements
but the predeclared rule did not support either the bounded positive or bounded
negative claim. Inconclusive is not a synonym for negative, failed, or zero.

### 7.4 Failed experiment

`FAILED_EXPERIMENT` means that an execution attempt did not produce a valid test
of its scientific claim because the apparatus, data, procedure, integrity,
analysis, or required evidence failed.

The failure record MUST state:

- the stage at which failure occurred;
- the first known invalid condition;
- whether execution stopped or continued diagnostically;
- all measurements obtained before and after the failure;
- whether any endpoint remains interpretable;
- affected claims;
- evidence preserved;
- whether a later attempt is a technical rerun or a new experiment.

Unless a reliability or feasibility failure was a predeclared endpoint, a failed
experiment supplies no positive or negative evidence about the scientific claim.

### 7.5 Invalid result

`INVALID` means that a result was recorded but later found not to satisfy the
minimum conditions for interpretation. Invalidity is appended through a
`RECLASSIFICATION` event. The original result and the reason it was initially
accepted remain visible.

### 7.6 Not run

`NOT_RUN` is an experiment state, not a result class. It records that no
execution reached a measurement point. It MUST NOT receive an `ASTRO-RES-*`
identifier.

## 8. Claim recording and withdrawn claims

### 8.1 Claim record

Every claim addressed by an experiment MUST have an immutable `ASTRO-CLM-*`
record containing:

- exact claim text;
- claim type: descriptive, comparative, predictive, causal, equivalence,
  non-inferiority, feasibility, reliability, or other declared type;
- population, conditions, intervention or exposure, comparator, outcome, and
  time horizon;
- permitted and prohibited interpretations;
- evidence required to support or reject it;
- origin document and date;
- status at registration.

### 8.2 Claim status

The canonical claim-status vocabulary is exactly `Retained`, `Rejected`,
`Untested`, `Open`, and `Withdrawn`, as defined by `ASTRO-CLAIMS-0001@1.0`.
Ledger claim events record the prior status, new status, evidence basis, and
effective time. The Claims Registry displays current status; the event stream
preserves the transition history. `CLAIM_SUPERSEDED` records a relationship, not
a sixth claim status: the superseded claim becomes `Withdrawn` and names its
replacement Claim ID.

### 8.3 Withdrawal

A `CLAIM_WITHDRAWN` event MUST preserve:

- the exact original wording;
- the original source and scope;
- the withdrawing authority;
- the effective date;
- the reason category: evidence, contradiction, ambiguity, scope error,
  prior-art error, ethical constraint, governance decision, or other stated
  reason;
- every evidence and result identifier cited;
- whether the withdrawal is evidentiary or precautionary;
- any replacement claim under a new Claim ID.

Withdrawal is not deletion and is not automatically evidence that the opposite
claim is true. A withdrawn Claim ID is never reactivated. A later proposition
receives a new Claim ID and links back to it.

## 9. Replications and independent reproductions

### 9.1 Technical repeat

A technical repeat reruns the same protocol, implementation, dataset version,
calibration, and analysis to test execution stability. It is linked to the
original result but does not establish independence or generalisation.

### 9.2 Internal replication

An internal replication is initiated by the same programme but uses the
predeclared replication unit: new targets, observations, seeds, times, or another
declared sample. Shared people, code, infrastructure, and prior knowledge MUST be
recorded.

### 9.3 Independent reproduction

An independent reproduction is performed by an operator not involved in the
original execution or analysis, using the same released protocol and ordinarily
the same dataset and implementation. It tests whether the recorded procedure
and artefacts can reproduce the result.

The record MUST declare organizational, financial, code, data, and personnel
dependencies. Merely assigning a different operator name inside the same process
does not establish independence.

### 9.4 Independent replication

An independent replication uses an independently executed protocol and a new
eligible sample or dataset version. Shared conceptual assumptions and shared
upstream data MUST remain visible.

### 9.5 Replication outcome

Each `ASTRO-REP-*` record MUST be classified as `CONSISTENT`,
`PARTIALLY_CONSISTENT`, `INCONSISTENT`, `INCONCLUSIVE`, or `FAILED_EXPERIMENT`
under criteria frozen before its result is known.

Contradictory replications MUST be recorded individually. They MUST NOT be
deleted, averaged away, or replaced by a consensus statement. Any synthesis is
a new result with its own method, evidence, and uncertainty.

## 10. Dataset versions

Every dataset used by an execution MUST have an immutable `ASTRO-DATA-*` record:

```yaml
dataset_version_id: ASTRO-DATA-......
provider: ...
dataset_name: ...
provider_release_or_query_version: ...
retrieved_at: ...
source_locator: ...
manifest_evidence_id: ASTRO-EVD-......
content_digest_or_snapshot_identity: ...
licence_or_use_authority: ...
selection_and_eligibility_rules: ...
included_units: ...
excluded_units: ...
schema_and_units: ...
known_missingness: ...
known_corrections_and_limitations: ...
derivation_parent_dataset_ids: [...]
partition_identity: ...
```

A provider update, corrected record, changed query, changed cross-match,
different partition, transformed representation, or changed exclusion rule
creates a new Dataset Version ID. “Latest” is prohibited as a dataset identity.

An earlier dataset is never rewritten or described as though a later correction
had been available to an earlier experiment.

## 11. Calibration history

Every calibration used in an experiment MUST have an `ASTRO-CAL-*` record
containing:

- calibrated quantity and unit;
- calibration target or reference;
- calibration dataset version and partition;
- method and software identity;
- fitted parameters and uncertainty;
- validity interval and operating range;
- pre-calibration and post-calibration diagnostics;
- known failure regions;
- operator and date;
- evidence identifiers;
- results authorized to consume the calibration.

Recalibration produces a new Calibration ID. It does not alter an old
calibration or any result that consumed it. Applying a new calibration to old
observations is a new reanalysis and therefore a new Result ID.

Calibration drift, failed calibration, and calibration discovered to have used
evaluation data MUST be appended explicitly. They may trigger later result
reclassification but never deletion.

## 12. Publication history

Every public dissemination that states or implies an empirical result MUST have
an `ASTRO-PUB-*` record. This includes preprints, papers, reports, registered
reports, conference outputs, public datasets, formal presentations, and material
public corrections.

The publication record MUST contain:

- title, authors, venue, and publication type;
- version, date, persistent identifier, and locator;
- linked Result, Evidence, Claim, Dataset, and Calibration IDs;
- exact claims communicated;
- peer-review status;
- disclosure of negative, failed, and contradictory results relevant to those
  claims;
- conflicts, funding, and access limitations;
- publication status.

Publication statuses are `DRAFT`, `SUBMITTED`, `POSTED`, `ACCEPTED`,
`PUBLISHED`, `CORRECTED`, `EXPRESSION_OF_CONCERN`, `RETRACTED`, and
`WITHDRAWN_BEFORE_PUBLICATION`.

Status changes are appended. Retraction or withdrawal never removes the
publication record, its earlier claims, or the evidence showing what was
communicated. Publication and peer review do not raise an empirical result's
evidence level by themselves.

## 13. Evidence hierarchy

Evidence level applies to a specific claim under a specific scope. It is not a
global score for ASA, a result, a publication, or an institution.

| Level | Minimum condition | What it does not establish |
|---|---|---|
| `EH-0` | No empirical execution, or only plans and assertions | Any empirical support or contradiction |
| `EH-1` | Execution artefacts exist, but protocol integrity or evidence completeness is unverified | A valid scientific result |
| `EH-2` | One bounded, protocol-valid result with complete evidence and declared uncertainty | Repeatability, independence, transfer, or generality |
| `EH-3` | `EH-2` plus a consistent technical repeat or internal replication | Independent reproducibility |
| `EH-4` | `EH-2` plus an independent reproduction from the released protocol and evidence | New-data replication or generality |
| `EH-5` | Independent replication on a new eligible sample or dataset under predeclared criteria | Universality outside the replicated scopes |
| `EH-6` | Multiple independent replications across materially different datasets, implementations, or protocols, synthesised by a registered method | Final truth, unrestricted causality, or validity in untested regimes |

Positive and negative results use the same hierarchy. A negative `EH-5` result
is not weaker merely because it is negative. A positive published result does
not exceed `EH-2` without the required replication evidence.

Evidence levels are not mechanically additive. Two dependent `EH-2` results do
not automatically become `EH-3`, and multiple reproductions using the same
defective source do not establish `EH-5`.

## 14. Interpretation limits

Every result record MUST separate:

1. **Observed:** directly recorded values and events.
2. **Derived:** quantities produced by a named analysis from recorded evidence.
3. **Decision:** mechanical application of the predeclared rule.
4. **Interpretation:** the narrow statement licensed by the first three.
5. **Not supported:** plausible statements the evidence does not establish.

The following transformations are prohibited unless separately tested:

- benchmark success → general architectural validity;
- benchmark failure → universal architectural impossibility;
- association → causation;
- statistical significance → practical importance;
- failure to reject → proof of no effect;
- absence or missingness → zero;
- failed experiment → negative scientific result;
- replication disagreement → permission to select the preferred run;
- publication → evidence of correctness;
- explanation quality → predictive validity;
- reproducibility → external validity;
- model-relative truth → unrestricted physical truth.

## 15. Corrections, supersession, and contradiction

A correction MUST be as visible and specific as the corrected statement. It may
correct transcription, metadata, calculation, classification, attribution, or
interpretation, but it MUST NOT conceal the original record.

A superseding result MUST state why it supersedes prospective interpretation:
new data, corrected analysis, improved protocol, discovered invalidity, changed
calibration, or another recorded reason. It MUST also state what remains valid
in the earlier result.

Contradictory valid results coexist. Declaring one authoritative requires a new,
registered synthesis or adjudication result. Chronology, prestige, sample size,
or publication status alone does not erase contradiction.

## 16. Minimum evidence package for a valid empirical result

A result cannot receive `EH-2` unless its evidence resolves to all applicable
items below:

1. frozen experiment protocol and decision rule;
2. execution start and completion records;
3. immutable system and dependency identities;
4. dataset and partition versions;
5. calibration identities;
6. raw or source observations;
7. exclusions, missingness, and failure logs;
8. primary and secondary output artefacts;
9. analysis code or exact analysis specification;
10. environment and resource record;
11. protocol-integrity assessment;
12. result record with uncertainty and scope;
13. reviewer or verifier identity and conflicts;
14. content digests or equivalent immutable source identities.

An incomplete package remains at `EH-1` even if its numerical outcome is
favourable.

## 17. Append procedure

For every future empirical action:

1. allocate permanent identifiers without reusing abandoned numbers;
2. register the protocol, claim, datasets, and calibrations before execution
   where the protocol requires preregistration;
3. append `EXECUTION_STARTED` before or at the start of measurement;
4. preserve evidence whether execution completes, aborts, or violates protocol;
5. append the execution outcome;
6. append a result only if the result definition in §5.1 is met;
7. append all later corrections, withdrawals, reproductions, replications, and
   publications as separate events;
8. never edit a preceding event to make the stream appear cleaner.

Identifier allocation is serialized against canonical `origin/main`:

1. fetch canonical `main` and read the final event identifier and
   `previous_event_id` chain;
2. allocate exactly the next six-digit event number and set
   `previous_event_id` to the canonical tip;
3. validate the complete chain and attempt one fast-forward publication;
4. if publication is rejected because canonical `main` advanced, do not merge,
   rebase, force, or publish the colliding event; fetch again, allocate the next
   number after the new canonical tip, update the uncommitted event's
   `previous_event_id`, revalidate, and retry as a new fast-forward operation;
5. if two conflicting identifiers were already published outside canonical
   `main`, canonical `main` keeps the first accepted event and a later
   `CORRECTION` event records the collision, assigns replacement subject IDs,
   and preserves locators and digests for both external records.

No published canonical event is renumbered or edited. An uncommitted candidate
event has no ledger standing.

## 18. State at establishment

As of 2026-08-01:

- frozen experiment protocols registered: **1** (`ASTRO-EXP-0001@1.0`);
- canonical claim records linked: **3** (`ASTRO-CLM-0070`, `ASTRO-CLM-0071`, `ASTRO-CLM-0072`);
- executed empirical experiments recorded in this ledger: **0**;
- positive empirical results: **0**;
- negative empirical results: **0**;
- inconclusive empirical results: **0**;
- failed empirical experiments: **0**;
- invalid empirical results: **0**;
- replications: **0**;
- independent reproductions: **0**;
- empirical dataset versions registered: **0**;
- empirical calibration events registered: **0**;
- empirical publications registered: **0**;
- empirical claims adjudicated by result: **0**;
- evidence level: **`EH-0`**.

Existing research drafts, proposed experiment documents, software checks, and
anticipated outcomes do not alter this state. They become ledger evidence only
through future append events and become empirical results only by satisfying
§5.1.

## 19. Append-only event stream

### AR1-E000001 — Ledger established

```yaml
event_id: AR1-E000001
event_type: LEDGER_ESTABLISHED
schema_version: ASTRO-RESULTS-RECORD/1.0.0
previous_event_id: none
occurred_at: 2026-08-01
recorded_at: 2026-08-01
late_entry: false
recorded_by:
  name_or_stable_id: Codex
  role: Results Architect
authority_or_basis: User instruction to manufacture ASTRO-RESULTS-0001
subject_ids:
  - ASTRO-RESULTS-0001
evidence_ids: []
supersedes: []
corrects: []
event_statement: >-
  ASTRO-RESULTS-0001 was established as the permanent append-only empirical
  results ledger. No experiment had been executed and no empirical result,
  dataset version, calibration, replication, reproduction, or publication was
  registered at establishment.
limitations:
  - This event records ledger establishment, not empirical evidence.
  - No scientific claim is supported or contradicted by this event.
```

### AR1-E000002 — Canonical protocol registered

```yaml
event_id: AR1-E000002
event_type: EXPERIMENT_REGISTERED
schema_version: ASTRO-RESULTS-RECORD/1.0.0
previous_event_id: AR1-E000001
occurred_at: 2026-08-01
recorded_at: 2026-08-01
late_entry: false
recorded_by:
  name_or_stable_id: Codex
  role: Canonical Research Controls Custodian
authority_or_basis: User instruction to freeze ASA-Astro research controls Version 1
subject_ids:
  - ASTRO-EXP-0001@1.0
evidence_ids: []
supersedes: []
corrects: []
event_statement: >-
  ASTRO-EXP-0001@1.0 was registered as the frozen, not-yet-executed canonical
  protocol for ASTRO-CLM-0070, its statistical null ASTRO-CLM-0071, and its
  terminal reporting claim ASTRO-CLM-0072. Registration is not execution and
  creates no empirical result.
limitations:
  - Execution attempts recorded: 0.
  - Result identifiers allocated: 0.
  - Evidence level remains EH-0.
```

### AR1-E000003 — Canonical experiment claims registered

```yaml
event_id: AR1-E000003
event_type: CLAIM_REGISTERED
schema_version: ASTRO-RESULTS-RECORD/1.0.0
previous_event_id: AR1-E000002
occurred_at: 2026-08-01
recorded_at: 2026-08-01
late_entry: false
recorded_by:
  name_or_stable_id: Codex
  role: Canonical Research Controls Custodian
authority_or_basis: User instruction to freeze ASA-Astro research controls Version 1
subject_ids:
  - ASTRO-CLM-0070
  - ASTRO-CLM-0071
  - ASTRO-CLM-0072
evidence_ids: []
supersedes:
  - ASTRO-CLM-0039
corrects: []
event_statement: >-
  ASTRO-CLM-0070, ASTRO-CLM-0071, and ASTRO-CLM-0072 were registered as the
  exact bounded positive claim, statistical null, and terminal-negative claim
  for ASTRO-EXP-0001@1.0. All three remain Untested. The earlier eight-target
  claim ASTRO-CLM-0039 is Withdrawn and superseded, and the Track B claim
  ASTRO-CLM-0040 is Withdrawn without an experiment.
limitations:
  - Claim registration is not empirical evidence.
  - No claim is supported or contradicted by this event.
  - Evidence level remains EH-0.
```

<!-- Append every future event after this comment. Do not edit, delete, reorder,
or insert content into any preceding part of ASTRO-RESULTS-0001. -->
