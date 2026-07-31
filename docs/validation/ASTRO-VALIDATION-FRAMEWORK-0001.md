# ASTRO-VALIDATION-FRAMEWORK-0001 — Validation Framework

## Document control

| Field | Value |
|---|---|
| Status | Normative validation design; no validation has yet been executed |
| Purpose | Define how ASA-Astro can support or falsify bounded claims about the tested ASA approach |
| Depends on | `ASA-ASTRO-0001-foundational-definition.md`, `ASTRO-ONTOLOGY-0001.md`, `ASTRO-CONTEXT-MODEL-0001.md`, `ASTRO-RELATIONSHIP-TAXONOMY-0001.md` |

## 1. Validation claim boundary

ASA-Astro MAY validate only a statement of this form:

> A specified ASA-Astro commit, using a specified immutable ASA dependency,
> data/reference versions, contexts, policies, models, schemas, and execution
> environment, met or failed predeclared criteria on a bounded benchmark.

It MUST NOT convert that result into universal ASA validity, astronomy-domain
correctness outside the benchmark, novelty, ratification, or scientific
discovery.

An execution that only emits outputs is a demonstration. An execution over a
frozen protocol is a benchmark run. It becomes a validation record only when
all protocol-integrity checks and predeclared comparisons are reported.

## 2. Validation units

The framework evaluates separable units so that a strong score at one stage
cannot hide a failed boundary at another.

| Unit | Tested question |
|---|---|
| Observation integrity | Are source identity, calibration, detector state, and provenance retained? |
| Candidate formation | Are detector representations kept separate from entity candidates, with supported recall and false-candidate control? |
| Entity resolution | Are representations matched or kept unresolved in agreement with reference labels and uncertainty? |
| Relationship recovery | Are supported relationship assertions recovered with correct type, roles, frame, units, confidence, and evidence? |
| Hierarchy/structure | Are selected known membership, containment, and structural patterns recovered without invalid transitivity? |
| Standing separation | Is Standing independently reproducible and free of hidden Context inputs? |
| Contextual significance | Do rankings/results agree with context-specific references better than declared baselines where claimed? |
| Explanation integrity | Can every output be traced to eligible inputs, rules, exclusions, uncertainty, and versions? |
| Scientific restraint | Are unknown, unavailable, contested, and unsupported claims preserved rather than forced into certainty? |

A critical integrity failure MAY invalidate the whole run even when aggregate
predictive metrics are high.

## 3. What counts as recovery of known structure

“Recovery” means agreement with a frozen, independently sourced reference for a
specified proposition set. It does not mean that the system rediscovered
astronomical reality from the image alone.

Successful recovery requires all applicable conditions:

1. benchmark subjects and reference propositions were not used to create hidden
   labels in the evaluation path;
2. entity mappings follow a predeclared matching/adjudication protocol;
3. relationship type, direction, roles, temporal/frame scope, and units agree
   with the reference within its uncertainty;
4. abstention or `indeterminate` is scored explicitly rather than silently
   removed;
5. contested Ground Truth is evaluated as contested, with acceptable alternatives
   or adjudication rules frozen in advance;
6. false extra relationships receive a penalty, including high-confidence false
   assertions and invalid transitive edges;
7. required hierarchy or structural motifs are recovered at the level declared
   by the benchmark, not inferred from visual similarity alone;
8. acceptance thresholds and critical failures were frozen before the held-out
   run.

Potential recovery metrics include per-type precision, recall, F-score,
precision-recall area, role/direction accuracy, entity-resolution accuracy,
hierarchy path agreement, graph edit components, and abstention-aware coverage.
The Benchmark MUST choose metrics appropriate to label balance and uncertainty;
this document does not choose numeric thresholds.

## 4. Reference data and Ground Truth

### 4.1 Acceptable reference sources

Ground Truth MAY be assembled from:

- an identified scientific catalogue release with licence and citation;
- an expert-labelled set produced under a documented annotation protocol;
- independently reviewed physical/model-derived quantities, when the benchmark
  explicitly tests agreement with that model rather than absolute reality;
- controlled synthetic data whose generating process is known, used only for
  the properties it actually controls;
- a versioned combination of sources with an explicit adjudication policy.

The initial illustrative image alone is never Ground Truth for identity,
physical relationship, causation, composition, development, or inferred dark
matter.

### 4.2 Reference manifest requirements

Every reference release MUST record:

- provider, release/version, immutable identifiers, retrieval date, and digest;
- licence or use authority;
- coordinate frame, epoch, units, band, and selection function as applicable;
- covered and excluded propositions;
- label/value uncertainty and confidence semantics;
- known limitations, disputed entries, and missingness;
- entity cross-match/adjudication method;
- independence or shared derivation relative to system inputs;
- train/tune/evaluation partition rules;
- corrections as new versions rather than in-place edits.

### 4.3 Expert labels

Expert labels MUST use a written rubric, independent annotation where practical,
and disagreement retention. Inter-rater agreement MUST be reported with a metric
suited to label type. Consensus MUST NOT erase minority alternatives without an
adjudication record. Experts MUST identify when a proposition is not decidable
from the supplied evidence.

### 4.4 Catalogue-derived references

Catalogue inclusion is not automatically Ground Truth for every proposition.
The Benchmark MUST state exactly which fields and catalogue claims are accepted,
how cross-matches are performed, what quality flags are admissible, and how
catalogue uncertainty or disagreement is represented.

## 5. Benchmark protocol

Before any held-out evaluation, the Benchmark MUST freeze:

1. system commit and clean-build procedure;
2. ASA dependency identifier and interface;
3. source, reference, schema, model, calibration, and licence manifests;
4. partitioning and leakage controls;
5. Context declarations and weighting policies;
6. baseline and ablation definitions;
7. metrics, aggregation, uncertainty intervals, and multiple-comparison policy;
8. success thresholds, non-inferiority margins, and critical failure conditions;
9. deterministic seeds, environment, resource limits, and repeat count;
10. exclusions and protocol-violation handling;
11. Explanation Trace sampling/inspection procedure;
12. the claims that a positive result would and would not support.

Tune and evaluation partitions MUST be disjoint at the independence unit defined
by the reference source. Splitting representations of the same entity across
partitions is leakage unless the benchmark specifically tests cross-observation
resolution and accounts for that dependence.

## 6. Baseline models

At minimum the following baselines MUST be implemented where the relevant input
exists. They MUST consume no privileged labels unavailable to the tested system.

| Baseline | Purpose |
|---|---|
| Seeded random or prevalence baseline | Establish chance and class-imbalance behaviour. |
| Apparent-brightness-only | Test whether outputs reduce to visual brightness. |
| Pixel-area/visual-dominance-only | Test whether large regions dominate without scientific basis. |
| Image-centre or observer-proximity-only | Test proximity and framing confounds. |
| Detection-confidence-only | Test whether evidence confidence is being mistaken for significance. |
| Uncontextualised structural score | Test whether Context adds value beyond a global graph measure. |
| Standing-only | Test whether Significance is merely Standing renamed. |
| Context-only prior | Test whether subject evidence contributes beyond context population priors. |
| Simple domain heuristic | Provide a scientifically interpretable comparison chosen before evaluation. |

A catalogue lookup that directly exposes held-out reference labels is not a fair
baseline; it MAY be reported separately as an oracle or upper-anchor with that
status explicit.

The significance-first approach adds measured value only if it improves at
least one predeclared claimed outcome over the relevant baselines without
breaching critical integrity or non-inferiority criteria.

## 7. Ablation tests

Ablations MUST remove or neutralise one declared component while keeping other
inputs and evaluation conditions fixed as far as practical.

Required candidate ablations:

- replace the Context computation with the uncontextualised structural score;
- replace Significance with Standing;
- remove Standing while preserving Context inputs;
- remove each Relationship Type family claimed to contribute;
- remove relationship direction or role information;
- disallow recursive propagation where the tested policy permits it;
- remove uncertainty inputs while retaining a visible `uncertainty_disabled`
  marker;
- replace calibrated Confidence with an uncalibrated ordering;
- exclude contested evidence;
- replace context weights with equal weights or a predeclared neutral policy;
- remove observer-specific inputs from observer-dependent contexts;
- remove inferred dark-matter-mediated assertions from any context that admits
  them.

Provenance and entity/representation separation are safety invariants, not
optional performance features. An attempted “no provenance” or
“pixel-equals-entity” ablation MUST be rejected as invalid rather than scored as
a legitimate model.

An ablation supports a component's value only when degradation occurs in the
predeclared metric and is not explained by changed data access, leakage, or an
unfair baseline.

## 8. Negative controls

Negative controls MUST include applicable cases from this list:

- shuffle Ground Truth labels within an appropriate stratum;
- permute entity-to-relationship endpoints while preserving simple graph counts;
- swap Context labels while keeping declarations unchanged, which MUST have no
  effect because labels alone are non-computational;
- supply a materially different Context while falsely reusing the old context
  identifier, which integrity checks MUST reject;
- inject bright or central distractor Light Regions with no supporting entity or
  relationship evidence;
- remove or corrupt provenance links, which MUST invalidate affected outputs;
- replace unknown/unavailable values with sentinel zeros in a deliberately
  invalid fixture, which schema or semantic checks MUST reject;
- add unsupported transitive relationships, which taxonomy validation MUST
  reject or penalise;
- scramble observer, band, frame, or epoch metadata, which must not yield a
  confident observer-dependent result;
- present synthetic no-signal or detector-artifact inputs with documented
  expected abstention behaviour;
- expose a reference-only feature to a leakage detector and verify that the run
  is invalidated.

A control that performs materially better than chance or the predeclared null
expectation triggers investigation and may invalidate the benchmark.

## 9. Uncertainty and confidence calibration

Calibration is evaluated separately from ranking and relationship magnitude.
For probabilistic propositions, the Benchmark SHOULD use proper scoring rules
such as Brier score or log loss and SHOULD report a reliability analysis and an
expected calibration error with predeclared bins or an adaptive alternative.

For interval/distribution outputs, the Benchmark SHOULD report empirical
coverage at declared levels, interval width/sharpness, and distributional score
where justified. For categorical confidence, the Benchmark MUST report outcome
rates per category and MUST include `uncalibrated` rather than invent numeric
probability.

Calibration reports MUST:

- stratify by relationship type and relevant quality regime when sample sizes
  permit;
- retain abstentions and missing cases in coverage reporting;
- avoid interpreting calibrated confidence as scientific truth;
- state dependence assumptions and use grouped or hierarchical resampling when
  observations share entities or sources;
- distinguish measurement uncertainty, model uncertainty, reference
  uncertainty, and confidence in a proposition.

Material overconfidence, particularly for false physical or causal assertions,
is a critical failure candidate.

## 10. False relationship penalties

Relationship evaluation MUST penalise unsupported additions as well as missed
references. At minimum it MUST distinguish:

- wrong endpoint/entity resolution;
- wrong Relationship Type;
- reversed direction or incorrect roles;
- invalid unit, frame, epoch, or observer scope;
- unsupported transitive/recursive edge;
- asserted certainty where the reference is contested or indeterminate;
- high-confidence false assertion;
- physical/causal interpretation supported only by visual or projected
  proximity;
- duplicate assertions derived from one source counted as corroboration.

The Benchmark MUST predeclare a penalty matrix or cost function. Higher costs
SHOULD be considered for confident false causal, orbital, gravitational,
developmental, compositional, or dark-matter-mediated assertions than for an
appropriate abstention. The cost policy MUST NOT be tuned after viewing held-out
errors.

Precision and recall MUST both be reported; a system cannot claim recovery by
emitting every possible relationship or by emitting almost none.

## 11. Ranking agreement

Context-specific ranking MUST be compared only with a reference ranking or
graded relevance judgement produced for the same Context semantics.

Depending on the reference, the frozen Benchmark MAY use:

- Kendall's tau-b for ordinal rankings with ties;
- Spearman rank correlation for monotonic agreement where justified;
- normalised discounted cumulative gain for graded top-ranked relevance;
- top-k overlap/precision and recall for operational cut-offs;
- pairwise accuracy for expert comparative judgements;
- rank stability intervals under uncertainty and resampling.

The metric, tie rule, unranked/indeterminate treatment, and population scope MUST
be declared in advance. A high correlation with apparent brightness or visual
dominance is a confound indicator, not validation. Agreement MUST be accompanied
by comparison against brightness-, proximity-, Standing-, and context-free
baselines.

## 12. Explanation Trace inspection

Automated checks MUST verify for every scored result that the trace contains:

- exact subject, Context, Standing, ASA dependency, and policy versions;
- all contributing Evidence and Relationship identifiers;
- excluded, unknown, unavailable, and contested inputs with reasons;
- intermediate results and unit/normalisation semantics;
- uncertainty and confidence handling;
- bounded propagation depth and cycle outcome when applicable;
- output and Provenance Record linkage.

A blinded or preselected reviewer sample MUST also assess whether traces:

- answer the declared Context question;
- avoid post-hoc scientific narratives;
- distinguish evidence from inference;
- expose brightness/proximity contributions where eligible;
- make a false or surprising output diagnosable;
- are sufficient to reproduce or reject the result.

Trace readability does not prove correctness. Trace incompleteness is an
integrity failure even when the ranking is accurate.

## 13. Repeatability and reproducibility

### 13.1 Repeatability

Identical immutable inputs, versions, parameters, environment, and seeds MUST
produce byte-identical formal outputs where practical. If a dependency is
nondeterministic, the Benchmark MUST predeclare a tolerance and repeated-run
protocol, and the Validation Result MUST report observed variance.

### 13.2 Reproducibility

An independent operator SHOULD be able to reconstruct the run from repository
instructions and versioned external manifests without conversation history.
The run record MUST include environment and dependency locks, data digests,
commands, seeds, resource settings, and expected output digests or metric
tolerances.

Unexplained variation that changes an acceptance outcome is a critical failure.

## 14. Sensitivity to Context weighting

The validation run MUST evaluate a predeclared neighbourhood of plausible
weight/policy alternatives without using held-out labels to select the preferred
policy. It MUST report:

- rank/result stability and the subjects most affected;
- whether conclusions depend on one narrow weight choice;
- monotonic or invariance constraints expected by the policy;
- effects of removing each eligible feature family;
- effects of changing missingness and contested-evidence rules;
- comparison with equal-weight and context-free alternatives;
- whether brightness, visual size, or proximity becomes a dominant proxy.

Sensitivity is not a search for the weights that best fit Ground Truth after the
fact. Material instability MAY be an honest uncertainty result; hiding it is a
validation failure.

## 15. Required statistical reporting

Results MUST report point estimates with uncertainty appropriate to the sampling
and dependency structure. Entity, observation, and source dependence MUST be
accounted for in resampling or modelling. Sample sizes and exclusions MUST be
shown. Multiple contexts, types, or metrics MUST not be selectively reported.

Statistical significance alone is insufficient. Effect size, uncertainty,
baseline difference, practical criterion, and failure costs MUST be reported.
No post-hoc subgroup may be presented as confirmatory without a new frozen
Benchmark.

## 16. Success, no-added-value, and failure decisions

### 16.1 Bounded success

A run supports bounded validation only if:

- every protocol-integrity check passes;
- all critical criteria pass;
- known-structure recovery and false-relationship criteria meet their frozen
  thresholds;
- calibration and repeatability meet their frozen thresholds;
- context-specific ranking meets the declared agreement/non-inferiority rules;
- the approach improves at least one predeclared claimed benefit over relevant
  baselines without unacceptable regression elsewhere;
- ablations and controls behave consistently with the claimed mechanism;
- traces are complete and reviewer-inspectable;
- failures and indeterminate results are included.

### 16.2 Added no demonstrated value

The tested significance-first approach has added no demonstrated value on the
Benchmark when it fails to improve any predeclared claimed outcome over the
relevant simple baselines, or when any gain is within the frozen no-effect/
non-inferiority margin. This result MUST be reported even if the demonstration
looks plausible.

### 16.3 Falsification or invalidation

The tested approach is falsified for a claimed mechanism, or the run is invalid,
if any applicable condition occurs:

- brightness-, area-, centre-, proximity-, Confidence-, or Standing-only
  baselines match or exceed claimed context behaviour;
- context declarations can be exchanged without traceable semantic effects, or
  labels alone change results;
- false physical relationships exceed the penalty bound;
- uncertainty is materially miscalibrated or unknowns become certainty;
- entity/representation, assertion/relationship, Standing/Significance, or
  model/Ground Truth boundaries collapse;
- gains vanish under held-out evaluation or the relevant ablation;
- negative controls yield meaningful-looking structure or confident results;
- output provenance or Explanation Traces are incomplete;
- benchmark leakage, post-hoc threshold selection, selective reporting, or
  reference circularity is found;
- repeatability fails the frozen tolerance;
- the selected ASA dependency cannot be identified or reproduced.

Failure of one benchmark does not prove ASA universally false; it rejects the
bounded claim for the tested versions and conditions. Repeated failure MUST NOT
be repaired by redefining Significance or Ground Truth after evaluation.

## 17. Validation Result minimum record

Every run MUST emit a Validation Result containing:

- run and Benchmark identifiers;
- tested commit and dependency/data/schema/model/context/policy versions;
- environment, commands, seeds, start/end times, and input/output digests;
- integrity-check outcomes;
- all predeclared metrics with uncertainty and raw result references;
- baseline, ablation, negative-control, sensitivity, and repeatability results;
- false-relationship error breakdown;
- trace inspection findings;
- exclusions, protocol deviations, and data/reference limitations;
- criterion-by-criterion `pass`, `fail`, `indeterminate`, or `invalid` status;
- the exact bounded conclusion and prohibited broader interpretations;
- Provenance Record and reviewer/adjudication status.

## 18. Framework validation criteria

Before an executable benchmark adopts this framework, reviewers MUST verify that
another operator can identify:

- the independent reference and its limitations;
- the frozen inputs and leakage boundary;
- every baseline, ablation, control, metric, and threshold;
- how abstention, missingness, and contested truth are scored;
- which failures invalidate the run and which falsify a claimed benefit;
- how to reproduce the outputs without conversational knowledge.

If any answer depends on an unstated choice, the Benchmark is not ready to run.
