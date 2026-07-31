# ASTRO-CONTEXT-MODEL-0001 — Context Declaration Model

## Document control

| Field | Value |
|---|---|
| Status | Normative ASA-Astro profile for declaring contexts; no significance algorithm is defined here |
| Depends on | `ASA-ASTRO-0001-foundational-definition.md`, `ASTRO-ONTOLOGY-0001.md`, `ASTRO-RELATIONSHIP-TAXONOMY-0001.md` |
| ASA boundary | Context is an ASA-owned semantic role; this document defines only the astronomy-domain declaration supplied to a selected ASA version |

## 1. Purpose

A Context states the bounded question under which Significance is computed.
Without a complete, immutable Context declaration there is no valid ASA-Astro
Significance result.

The model exists to prevent hidden prompts, implicit observer assumptions,
undeclared weights, and permanent “importance” fields. It does not prescribe a
significance engine or amend ASA.

## 2. Context invariants

1. A Significance result MUST reference exactly one Context identifier and
   version.
2. A Context MUST be declared and frozen before its benchmark outputs are
   evaluated.
3. Context version, subjects, scope, eligible evidence, relationship policy,
   weighting policy, missingness policy, output semantics, and authority MUST be
   inspectable.
4. Standing MUST be supplied as a separate input record. A Context MUST NOT
   rewrite Standing to obtain a preferred result.
5. A Significance result MUST be stored as a derived result, never as an
   intrinsic entity attribute.
6. Scores or ranks from different Contexts MUST NOT be compared unless a
   predeclared cross-context normalisation explicitly permits it.
7. Apparent brightness, luminosity, proximity, image-plane position, pixel area,
   or visual dominance MUST NOT receive implicit relevance. If any is eligible,
   the Context MUST state why, how, and under what scientific limitations.
8. Unknown, unavailable, contested, and excluded inputs MUST remain distinct and
   appear in the Explanation Trace.
9. Context changes MUST create a new version. A used Context is immutable.
10. Context authority is not scientific truth; it is authority to ask and score
    a declared question.

## 3. Required declaration fields

The future machine-readable form MUST represent every field below. “Required”
means required either as a concrete value or as an explicit structured state
such as `not_applicable`; omission is not a valid default.

| Field | Requirement |
|---|---|
| `context_id` | Stable, non-semantic identifier. |
| `context_version` | Immutable version of the complete declaration. |
| `title` | Human-readable label; not used as computation input unless explicitly mapped. |
| `question` | Precise question the significance output answers. |
| `authority` | Person, governance record, or frozen Benchmark authorised to declare it. |
| `purpose_class` | One declared class such as structural, observational, evolutionary, or information-value. |
| `target_scope` | Eligible entity/system identifiers or a reproducible selector and its source version. |
| `reference_system` | The system boundary, if the question is system-relative. |
| `observer` | Observer/location/instrument perspective or `not_applicable`. |
| `coordinate_frame` | Frame and coordinate-system version or `not_applicable`. |
| `epoch_or_interval` | Evaluation time or validity interval. |
| `horizon` | Forecast/retrospective horizon or `not_applicable`. |
| `eligible_evidence` | Evidence kinds, quality/admissibility rules, and permitted sources. |
| `eligible_relationship_types` | Relationship Types and role/subtype constraints. |
| `relationship_policy` | Rules for direction, depth, contested assertions, confidence, and propagation. |
| `standing_policy` | Which Standing result/profile is required and how invalid/expired standing is treated. |
| `feature_policy` | Eligible derived features with units, transformations, and scientific rationale. |
| `weighting_policy_ref` | Immutable policy identifier; inline hidden weights are prohibited. |
| `normalisation_scope` | Population/reference against which rank or score semantics are defined. |
| `missingness_policy` | Behaviour for unknown, unavailable, withheld, contested, and not-applicable values. |
| `uncertainty_policy` | Propagation, sensitivity, and indeterminate-result rules. |
| `exclusions` | Explicitly ineligible data, relationships, entities, and leakage controls. |
| `output_semantics` | Rank/score/category meaning, direction, tie rule, and comparability limits. |
| `explanation_requirements` | Minimum trace fields and contribution/exception reporting. |
| `provenance_ref` | Context source, decision, and version lineage. |

An executable declaration MUST fail schema validation if a required field is
absent. A Context whose `weighting_policy_ref` or ASA dependency cannot be
resolved MUST be non-executable rather than silently defaulted.

## 4. Computation boundary

The context-to-significance interface is conceptually:

```text
inputs:
  subject record(s)
  active Evidence Records
  active Relationship Assertions / normalised Relationships
  separate Standing result
  frozen Context declaration
  selected ASA dependency and computation-policy versions

output:
  context-specific Significance result
  uncertainty and sensitivity information
  Explanation Trace
  Provenance Record
  valid | invalid | indeterminate status
```

This interface says what must be supplied and retained. It intentionally does
not choose a formula, feature set, weight values, propagation depth, score
range, or ranking algorithm. Those remain separately authorised decisions and
must be testable against baselines.

## 5. Context profiles for the proof of concept

The profiles below are semantic templates, not executable configurations. Each
requires a frozen dataset, policy, and decision record before use.

### 5.1 Structural organisation of the primary galaxy

- **Question:** Which represented entities or structures are most relevant to
  describing the declared organisation of the benchmark's primary galaxy?
- **Required scope:** A resolved reference system and an explicit rule for what
  “primary” means. The largest or brightest image region MUST NOT be assumed to
  be primary.
- **Potentially eligible relationships:** containment, membership,
  compositional, structural, spatial, lineage/shared-origin, and uncertainty
  dependency.
- **Potentially eligible evidence:** catalogue structure, kinematics, calibrated
  imaging used with projection caveats, and expert-labelled structure.
- **Mandatory exclusions:** visual dominance as structure; unsupported physical
  membership; context-free graph centrality.
- **Output meaning:** relevance to the declared structural description, not
  global importance or luminosity.

### 5.2 Star-formation relevance

- **Question:** Which subjects are relevant to evaluating star-formation
  evidence or hypotheses within the declared system, epoch, and observational
  bands?
- **Required scope:** An authorised scientific operationalisation of
  star-formation relevance and admissible proxies.
- **Potentially eligible relationships:** developmental, compositional,
  energetic, radiative, causal (only with sufficient basis), containment,
  spatial, and uncertainty dependency.
- **Potentially eligible evidence:** appropriately calibrated band-specific
  observations, spectra, externally supplied classifications, and model outputs
  clearly marked inferred.
- **Mandatory exclusions:** brightness alone; colour alone without a declared
  calibrated method; generic proximity as causation.
- **Output meaning:** relevance to the declared star-formation question, not a
  claim that star formation is present or caused by a ranked subject.

### 5.3 Gravitational influence

- **Question:** Which subjects or inferred structures are relevant to the
  declared gravitational behaviour of a system or target under a specified
  physical model?
- **Required scope:** Reference frame, mass/dynamical model, scale, epoch, and
  target behaviour.
- **Potentially eligible relationships:** gravitational, orbital, spatial,
  containment, membership, structural, compositional, inferred
  dark-matter-mediated, and uncertainty dependency.
- **Potentially eligible evidence:** kinematics, lensing, distance and mass
  estimates, or external model/reference data with uncertainty.
- **Mandatory exclusions:** brightness-as-mass without a declared model;
  image-plane proximity as binding; invisible-region-as-dark-matter inference.
- **Output meaning:** model-scoped relevance to gravitational behaviour, not an
  intrinsic ranking or proof of the selected mass model.

### 5.4 Observational interpretation

- **Question:** Which subjects, representations, and effects are relevant to
  interpreting what the declared observer/instrument recorded?
- **Required scope:** Observation, instrument, band, calibration, observer,
  field geometry, and processing version.
- **Potentially eligible relationships:** observational, occlusion, radiative,
  spatial, temporal, containment (representational), and uncertainty dependency.
- **Potentially eligible evidence:** detector/calibration metadata, masks,
  point-spread information, multi-band data, and source provenance.
- **Mandatory exclusions:** treating artefacts as entities; treating apparent
  brightness as significance; translating detector absence directly to
  astronomical absence.
- **Output meaning:** relevance to explaining the observation, which may give an
  artefact or foreground medium high contextual relevance without treating it
  as a significant astronomical object in other contexts.

### 5.5 Long-term system evolution

- **Question:** Which subjects and relationships are relevant to a declared
  model of system evolution over a specified horizon?
- **Required scope:** System boundary, initial epoch, forecast/retrospective
  horizon, model family, and permitted causal/developmental claims.
- **Potentially eligible relationships:** temporal, developmental, causal,
  gravitational, orbital, energetic, compositional, lineage/shared-origin, and
  uncertainty dependency.
- **Potentially eligible evidence:** time series, population evidence, dynamics,
  externally supplied models, and reference histories.
- **Mandatory exclusions:** morphology-as-destiny; extrapolation beyond model
  validity; unbounded recursive causal propagation.
- **Output meaning:** relevance under one evolution model and horizon, not a
  certain prediction.

### 5.6 Relationship to the observer

- **Question:** Which subjects or effects are relevant because of their declared
  geometric, temporal, radiative, or observational relationship to the
  observer?
- **Required scope:** Observer identity/location, reference frame, epoch,
  instrument, band, and question-specific distance semantics.
- **Potentially eligible relationships:** spatial, temporal, radiative,
  observational, occlusion, and uncertainty dependency.
- **Potentially eligible evidence:** astrometry, distance estimates, observation
  geometry, timing, detector response, and calibration.
- **Mandatory exclusions:** proximity as universal significance; apparent size
  or brightness as intrinsic value; observer relation without a named observer.
- **Output meaning:** observer-relative relevance only.

### 5.7 Scientific information value

- **Question:** Which observations, entities, assertions, or uncertainties are
  relevant to reducing uncertainty or discriminating among the benchmark's
  declared scientific alternatives?
- **Required scope:** A finite question set, current evidence state, candidate
  alternatives, permitted information-value measure, and decision horizon.
- **Potentially eligible relationships:** uncertainty dependency,
  observational, causal, spatial, temporal, compositional, and any domain type
  directly tied to the declared alternatives.
- **Potentially eligible evidence:** uncertainty models, disagreement records,
  coverage gaps, benchmark labels, and prospective observation models.
- **Mandatory exclusions:** novelty-as-value; low confidence automatically
  meaning high value; selecting known Ground Truth labels through leakage.
- **Output meaning:** expected or measured information value for the declared
  question, not scientific importance in general.

## 6. Same entity, different contexts

The following is a synthetic reasoning example only. `E-example` is not a real
object and no measurement or identity is asserted.

Assume the frozen input records say:

- `E-example` has one Standing result `S-example`;
- a structural membership assertion is well supported;
- a radiative interpretation is contested;
- an occlusion relation is supported for one observer and band;
- a mass estimate is unavailable;
- all of these states and their provenance remain unchanged across runs.

| Context | Illustrative outcome for the unchanged entity | Why no contradiction exists |
|---|---|---|
| Structural organisation | Eligible and ranked toward the more relevant part of this context's population because the supported membership/structural input is eligible. | The output answers a structural question only. |
| Star-formation relevance | Indeterminate because the required radiative interpretation is contested and the context forbids substituting brightness. | Indeterminate is not low significance and does not reject the entity. |
| Gravitational influence | Indeterminate because the required mass evidence is unavailable. | Structural standing does not manufacture a mass estimate. |
| Observational interpretation | Eligible and potentially ranked more relevant because the observer-specific occlusion affects interpretation. | Observer-specific relevance does not make the entity intrinsically important. |
| Long-term system evolution | Excluded or indeterminate if no admissible developmental/dynamical model covers it. | Context eligibility differs without changing identity or Standing. |
| Relationship to the observer | Relevant only for the named observer, band, and epoch. | The relation is perspective-bound and cannot be globalised. |
| Scientific information value | Potentially relevant if resolving the contested radiative assertion discriminates among predeclared alternatives. | Uncertainty can be informative without making the uncertain claim true. |

No row changes `E-example` or `S-example`. Each result has different semantics
and MUST NOT be compared numerically across Contexts unless an authorised
cross-context normalisation exists.

## 7. Context weighting and sensitivity

Weighting MAY be numeric, ordinal, rule-based, constrained optimisation, or
another ASA-compatible policy, but it MUST be:

- immutable and content/version identified;
- scientifically justified for the Context;
- inspectable independently of outputs;
- evaluated against simple baselines;
- accompanied by uncertainty and missingness behaviour;
- tested for sensitivity to plausible perturbations;
- incapable of silently converting visual features into significance;
- fixed before held-out evaluation.

Sensitivity reporting MUST identify whether ranking or category changes result
from evidence changes, Standing changes, Context changes, policy changes, or
numerical instability. These causes MUST NOT be collapsed into one “confidence”
field.

## 8. Validation and falsification criteria

Any formal schema or executable implementation of this model MUST test that:

1. a Significance request without a Context or with an unresolved Context
   dependency is rejected;
2. identical immutable inputs and seeds reproduce the same result within the
   declared tolerance;
3. Context version changes invalidate reuse of old Significance as current;
4. Significance cannot be serialised as an entity's intrinsic property;
5. changing an ineligible field does not affect a result;
6. changing an eligible input produces the traceable effect specified by the
   policy or an explicit indeterminate outcome;
7. a brightness-only and proximity-only negative control cannot masquerade as
   the Context computation;
8. Standing remains unchanged when only the Context changes;
9. missing and contested inputs follow the declared policy and appear in the
   Explanation Trace;
10. results from different Contexts are rejected as directly comparable unless
    a frozen normalisation explicitly authorises comparison.

The model is falsified as implementation-ready if any required field needs a
hidden default, if an operator cannot explain why the same entity changes rank
across contexts, or if Context labels can be changed without changing the
declared computation contract while still changing outputs.
