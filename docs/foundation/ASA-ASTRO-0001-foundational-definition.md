# ASA-ASTRO-0001 — Foundational Definition

## Document control

| Field | Value |
|---|---|
| Status | Foundational programme definition; not a validation result |
| Scope | ASA-Astro proof of concept |
| Authority | ASA-Astro repository governance, subordinate to an explicitly versioned ASA dependency |
| Audience | Implementers, reviewers, scientific advisers, and validation operators |
| Related records | `ASTRO-ONTOLOGY-0001`, `ASTRO-RELATIONSHIP-TAXONOMY-0001`, `ASTRO-CONTEXT-MODEL-0001`, `ASTRO-VALIDATION-FRAMEWORK-0001`, `REPOSITORY-STRUCTURE-0001`, `governance/decision-register.md` |

## 1. Normative language

The terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** state
requirements for ASA-Astro. They do not amend ASA. Descriptive scientific
examples are non-normative and do not assert facts about an unidentified input.

## 2. Constitutional identity

ASA-Astro is a bounded proof-of-concept validation domain for Adaptive
Significance Architecture (ASA). Astronomy is used because observations,
physical relationships, uncertainty, hierarchy, causality, and scale can be
compared with independently maintained scientific understanding.

ASA-Astro is:

- a consumer and tester of an explicitly versioned ASA interface;
- a producer of astronomy-domain evidence, relationship assertions, contextual
  reasoning outputs, and validation results;
- a falsifiable experiment, not evidence that ASA is correct before testing;
- an independent repository whose contents are specific to the validation
  domain.

ASA-Astro is not an ASA constitutional authority. It MUST NOT reproduce,
reinterpret, ratify, or supersede ASA constitutional or canonical material.
When ASA-Astro and its selected ASA dependency conflict, the conflict MUST be
recorded and implementation MUST stop at that boundary until an authorised
decision is made.

## 3. Purpose

The programme exists to determine whether a significance-first architecture can
produce useful, traceable, context-sensitive reasoning over astronomy-domain
evidence without collapsing observation, inference, structure, confidence,
standing, and significance into one score.

The proof of concept is intended to test whether the architecture can:

1. preserve the lineage from source material to every derived value;
2. recover selected, already-known structural relationships within declared
   benchmark bounds;
3. distinguish an observed representation from an astronomical entity;
4. represent unknown, unavailable, uncertain, and contested information;
5. compute different significance outcomes for the same entity under different
   declared contexts without contradiction;
6. explain which evidence, relationships, standing result, context declaration,
   policy, and computation produced an output;
7. fail visibly when evidence is insufficient or the tested ASA approach adds
   no measured value.

## 4. Scope

The initial scope is the smallest end-to-end path needed to evaluate the common
conceptual pipeline:

```text
Observation
→ Evidence Record
→ Candidate Entity
→ Relationship Assertion
→ Relationship Classification
→ Standing Computation
→ Context Declaration
→ Significance Computation
→ Reasoning Output
→ Validation Against Ground Truth
```

In scope:

- ingestion of a documented illustrative astronomical image and, where
  authorised, associated catalogue or expert reference data;
- preservation of source, detector, pixel, light-region, entity, and
  representation boundaries;
- candidate formation and explicit entity-resolution states;
- asserted and classified relationships from the bounded taxonomy;
- evidence-linked confidence and uncertainty;
- standing computation separated from contextual significance computation;
- explicit, versioned context declarations;
- deterministic reasoning outputs where inputs and policies permit;
- validation against versioned, licensed, provenance-bearing reference data;
- negative controls, baselines, ablations, and falsification reporting.

The initial image is only an illustrative starting input. It is not sufficient
scientific ground truth and MUST NOT, by itself, establish object identity,
distance, physical association, causation, composition, development, or
dark-matter mediation.

## 5. Non-scope

The programme MUST NOT become:

- a general astronomy application, sky survey, catalogue, or observatory
  control system;
- an image-classification novelty demonstration;
- a source of newly invented measurements, object identities, physical claims,
  or certainty;
- a replacement for scientific catalogues, peer review, expert adjudication,
  or domain-specific physical modelling;
- a reimplementation or local fork of ASA constitutional material;
- a claim of scientific discovery;
- a universal demonstration that ASA applies to all domains;
- an optimisation exercise in which a visually attractive output substitutes
  for a predeclared validation protocol.

Scientific discovery may be a future consequence of separately governed work,
but no ASA-Astro proof-of-concept output is a discovery merely because it is
unexpected.

## 6. Relation to ASA and concept ownership

### 6.1 Dependency rule

Any executable or formal dependency on ASA MUST identify an immutable ASA
version or commit, the consumed interface, compatibility expectations, and a
repeatable retrieval or vendoring method. ASA canonical content MUST NOT be
copied into this repository. Until the dependency is selected in the decision
register, an implementation MAY define an adapter boundary but MUST NOT claim
conformance to ASA.

### 6.2 ASA-owned semantic roles

Within this programme, the following roles belong to the ASA side of the
boundary and are only profiled, supplied with domain data, or tested here:

- **Standing** as a computation distinct from significance;
- **Context** as the mandatory declaration against which significance is
  computed;
- **Significance** as a context-dependent computation rather than an intrinsic
  object property.

Their authoritative definitions MUST come from the selected ASA dependency.
The local ontology states only the astronomy-domain contract ASA-Astro requires
in order to test them. A local profile MUST NOT silently widen or alter the ASA
meaning.

### 6.3 ASA-Astro-owned concepts

The following are owned by ASA-Astro because they are domain, adapter, or
validation concepts rather than amendments to ASA:

- Observation, Observation Source, Detector Output, Pixel, Light Region;
- Candidate Entity, Resolved Entity, Composite Entity, Astronomical System;
- astronomy Relationship, Relationship Assertion, and Relationship Type;
- astronomy Evidence Record and Provenance Record profiles;
- Confidence and Uncertainty representations used for astronomy evidence;
- Explanation Trace as the local inspectable record of an ASA-Astro run;
- Ground Truth, Benchmark, and Validation Result used by the validation harness;
- all astronomy-specific relationship classes and scientific evidence rules.

If a domain-independent abstraction appears reusable, it remains ASA-Astro
material until an ASA-governed process adopts it. Reusability does not grant
ASA-Astro authority over ASA.

## 7. Authority boundaries

| Subject | Authoritative source | ASA-Astro authority |
|---|---|---|
| ASA constitutional meaning | Selected upstream ASA version | Consume and test only |
| Astronomy source data | Identified provider and release | Preserve and cite; do not alter source claims |
| Catalogue facts | Identified catalogue release | Represent with provenance and uncertainty |
| Expert labels | Named, governed annotation set | Compare and record disagreement |
| Domain ontology and adapters | This repository | Define within the bounded proof of concept |
| Context declaration | Versioned ASA-Astro context artefact and authorised policy | Apply and test; never hide weights or assumptions |
| Validation conclusion | Versioned benchmark protocol plus observed results | Report within declared bounds only |
| Scientific discovery | Outside this proof of concept | No authority to declare |

An operator MUST NOT resolve a cross-boundary conflict by silently selecting the
most convenient claim. Conflicts belong in the decision register or validation
result.

## 8. Required conceptual separations

Every formal component MUST preserve these distinctions:

| Distinction | Required treatment |
|---|---|
| Source image / astronomical reality | The image is a provenance-bearing representation, not the object or total reality. |
| Pixel or detection / entity | Detector and segmentation outputs may support a candidate; they never establish identity alone. |
| Entity / representation | One entity may have multiple images, catalogue records, or model representations. |
| Observation / inference | Observed records state acquisition; inferences state method, premises, and uncertainty. |
| Assertion / established relationship | An assertion remains evidence-qualified and reviewable even when well supported. |
| Relationship strength / confidence | Estimated magnitude is about the relation; confidence is about support for the estimate or assertion. |
| Standing / significance | Standing is a separate computation; significance requires a declared context. |
| Global structure / contextual relevance | Structural position may inform significance but cannot determine it without context. |
| Visible matter / inferred structure | Visibility is not evidence of all matter; inferred structure must retain model dependence. |
| Model output / scientific ground truth | Outputs are hypotheses or computations until compared with an independent reference. |

## 9. Scientific integrity obligations

Every operator and component MUST:

1. identify which values are observed, externally supplied, inferred, or
   computed;
2. retain units, reference frames, epochs, coordinate systems, and observation
   bands when scientifically relevant;
3. preserve null, unknown, unavailable, contested, and not-applicable states
   rather than coercing them to zero or false;
4. record model, catalogue, calibration, transformation, and policy versions;
5. avoid precision beyond the supporting evidence;
6. keep confidence separate from relationship magnitude and from significance;
7. make alternative or conflicting assertions co-representable;
8. expose assumptions and stop conditions in explanation traces;
9. use only licensed or otherwise authorised input and reference material;
10. avoid interpreting absence of visible light as absence of matter or
    structure.

No statement may be upgraded from candidate or inferred status because it makes
the output more coherent.

## 10. Evidence requirements

Every observation, assertion, resolution, derived value, standing result, and
significance result MUST be connected to at least one Evidence Record or to an
explicit `unavailable`/`unknown` evidence state. Each Evidence Record MUST:

- identify its subject and supported claim;
- identify the evidence kind and acquisition or derivation method;
- link to immutable or content-addressed source identity where practical;
- identify units, calibration, coordinate frame, epoch, and band when relevant;
- state quality flags, limitations, and uncertainty;
- link to a Provenance Record;
- state whether it supports, contradicts, or merely contextualises the claim;
- remain distinguishable from the claim itself.

Evidence quantity MUST NOT be treated as evidence quality. Repeated records
derived from the same source MUST NOT be counted as independent corroboration.

## 11. Provenance requirements

Every derived value MUST retain a traversable provenance chain to source inputs.
At minimum the chain MUST record:

- stable identifiers for inputs and outputs;
- source origin, licence or use authority, retrieval time, and source version;
- content digest where legally and technically possible;
- operator or executable identity;
- code, schema, model, calibration, policy, context, and dependency versions;
- transformation name, parameters, deterministic seed if used, and execution
  time;
- parent records in derivation order;
- warnings, missing dependencies, and manual interventions.

A derived record with a broken provenance link MUST be marked invalid for
validation. Provenance is not optional metadata and MUST NOT be reconstructed
from conversation history.

## 12. Uncertainty treatment

Uncertainty MUST be representable as structured data, not only prose. A record
MAY contain quantitative distributions, intervals, covariance, categorical
quality states, or contested alternatives, provided the method and semantics
are declared.

The following states MUST remain distinct:

- `unknown`: the value is not known;
- `unavailable`: a known source or method could not supply the value;
- `not_applicable`: the field does not apply;
- `withheld`: the value exists but is intentionally unavailable, with reason;
- `contested`: supported alternatives or authorities disagree;
- `estimated`: a method produced a value with declared uncertainty;
- `bounded`: only a limit or interval is supported.

Missing values MUST NOT default to zero. Confidence MUST NOT be manufactured
where calibration evidence is absent. Recursive uncertainty propagation MUST
be explicit, bounded, cycle-safe, and validated before use.

## 13. Standing and significance obligations

Standing and significance MUST be separately computed, stored, versioned, and
explained.

- Standing MAY summarise an entity's admissibility, evidence support, or
  structural position under the selected ASA contract. It MUST NOT encode a
  hidden context-specific priority.
- Significance MUST be computed for a declared Context and MUST identify the
  context version, computation policy, inputs, uncertainty, and explanation
  trace.
- Significance MUST be a derived result or event. It MUST NOT be stored as a
  timeless intrinsic property of an entity.
- A change in context MAY change significance without changing the entity or
  standing. This is expected behaviour, not inconsistency.

Luminosity, apparent brightness, proximity to the observer, proximity in the
image plane, size in pixels, central placement, contrast, and visual dominance
MUST NOT be used as synonyms or unqualified proxies for significance. They MAY
be evidence-bearing features only when a declared context and validated policy
make their relevance explicit. A bright or nearby object may be insignificant
to a context; a faint or invisible inferred structure may be significant, but
only to the extent supported by evidence and the context.

## 14. Expected proof-of-concept outputs

The proof of concept is expected to produce, as versioned and inspectable
artefacts:

1. source and observation manifests;
2. Evidence and Provenance Records;
3. detector or segmentation outputs clearly labelled as representations;
4. Candidate Entity records and explicit resolution outcomes;
5. Relationship Assertions and classifications with evidence and confidence;
6. Standing computation results;
7. Context declarations;
8. context-specific Significance results;
9. Explanation Traces that connect results to their inputs;
10. benchmark manifests, baseline results, ablation results, negative controls,
    and Validation Results;
11. a limitations and unresolved-decisions record.

Outputs MUST be deterministic for identical immutable inputs, versions,
parameters, and seeds, except where a documented nondeterministic dependency is
unavoidable. Any exception MUST be measured and reported.

## 15. Demonstration, benchmark, validation, and discovery

| Activity | Meaning in ASA-Astro | What it does not establish |
|---|---|---|
| Demonstration | Shows that a bounded path can execute and emit inspectable outputs. | Accuracy, comparative value, scientific validity, or generality. |
| Benchmark | Applies a frozen dataset, reference, protocol, metrics, and baselines. | Success unless acceptance criteria are met. |
| Validation | Reports whether a specified version satisfies predeclared criteria on a bounded benchmark. | Universal validity, ASA ratification, or scientific discovery. |
| Scientific discovery | A new scientific claim subjected to appropriate independent scientific methods and governance. | Nothing in this proof of concept may self-declare this status. |

A successful demonstration MUST NOT be described as a successful validation.
A benchmark result MUST include negative and failed findings. Validation language
MUST identify the tested versions and scope.

## 16. Success conditions

Success requires all of the following for a predeclared benchmark:

- reference data are independent, versioned, licensed, and provenance-bearing;
- known structure is recovered at or above acceptance thresholds fixed before
  evaluation;
- false relationships remain within the declared penalty bound;
- confidence or uncertainty is acceptably calibrated under the declared metric;
- context changes produce explainable, scientifically defensible ranking
  changes rather than brightness or proximity proxies;
- standing and significance remain demonstrably separate in data and code;
- explanation traces allow a reviewer to reproduce or reject each tested
  result;
- repeated runs satisfy the repeatability tolerance;
- the tested approach improves at least one predeclared outcome over relevant
  baselines without unacceptable regression on the others;
- all material failures, exclusions, and contested references are reported.

Numeric thresholds remain an authorised benchmark-design decision and MUST be
recorded before evaluation, not chosen after observing results.

## 17. Failure and falsification conditions

The significance-first approach is failed or unsupported for the tested scope
if any predeclared critical condition occurs, including:

- it cannot preserve provenance from output to source;
- it collapses detector output into asserted astronomical identity;
- it stores significance as an intrinsic permanent entity attribute;
- standing and significance are operationally indistinguishable;
- materially different contexts do not affect results when the reference model
  says they should, or context labels change results without traceable inputs;
- brightness, apparent proximity, or visual dominance explains the output as
  well as or better than the tested architecture;
- it produces excess unsupported relationships or hides contrary evidence;
- confidence is materially miscalibrated or missingness is converted to false
  certainty;
- results are not repeatable within the declared tolerance;
- explanation traces cannot account for rankings or derived values;
- performance does not exceed predeclared baselines on any claimed benefit;
- gains disappear under ablation, negative control, or held-out evaluation;
- benchmark leakage, post-hoc threshold selection, or reference dependence
  invalidates the comparison.

Failure MUST be reported as a Validation Result, not repaired through changed
meaning or unrecorded exclusions.

## 18. Foundational assumptions and open authority

This definition assumes only that an ASA interface capable of the required
standing, context, and significance roles can be selected. It does not assume a
particular ASA version, image, catalogue, object identity, metric threshold,
context weighting, or operator implementation. Those choices remain open in
`governance/decision-register.md`.

No scientific validation, ASA conformance, novelty, universal applicability, or
discovery is claimed by this document.

## 19. Document validation criteria

This foundation is internally acceptable only if reviewers can answer yes to
all of the following:

- Is ASA-Astro bounded as a validation consumer rather than an ASA authority?
- Are source, representation, entity, inference, standing, context, and
  significance separable in a future schema?
- Are evidence, provenance, uncertainty, and falsification mandatory?
- Are demonstration, benchmark, validation, and discovery non-interchangeable?
- Can an implementation fail without redefining the programme's goal?

A no answer falsifies this document's readiness and requires a recorded
revision before implementation depends on it.
