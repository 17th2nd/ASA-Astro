# ASA-Astro POC Validation Report 0001

**Operator:** Codex D — Integration, Benchmark, Visualisation, and Adversarial Validation
**Date:** 2026-07-31
**Tested canonical commit:** `59b1817c07d3bc7e72d7353459c3177362e72a4e`
**Status:** PRE-VALIDATION PARTIAL RESULT — COMPLETE POC BLOCKED
**Claim boundary:** This report does not validate ASA, ASA-Astro, an astronomical interpretation,
or a significance-ranking hypothesis.

## 1. Research question

Does the integrated proof of concept provide evidence that typed relationships, Standing,
declared Context, and uncertainty produce a more defensible ranking than naive visual prominence,
with an auditable path from source evidence to explanation?

## 2. Hypothesis

For a frozen dataset, ASA dependency, Standing policy, Contexts, and Ground Truth, a system that
preserves typed relationships and uncertainty and computes Context-specific Significance will
produce rankings and explanations that are more defensible than brightness-only or other declared
naive baselines.

The hypothesis requires falsifiable ranking outcomes. A reproducible candidate graph alone is
insufficient.

## 3. System tested

### Present

- foundation, ontology, relationship taxonomy, Context model, and validation design from
  `351cc578d3ad94fca87038a077419eb84458d7d4`;
- Codex B deterministic observation-to-candidate-graph pipeline from
  `59b1817c07d3bc7e72d7353459c3177362e72a4e`;
- CPython 3.12.3;
- Pillow 10.2.0;
- jsonschema 4.10.3;
- the exact package versions in `requirements.lock`.

### Absent

- Codex C relationship/reasoning implementation;
- immutable ASA dependency;
- Standing computation;
- executable Context declarations and authorised weights;
- Significance computation;
- Explanation Trace output;
- baseline-ranking implementation;
- visual graph explorer;
- benchmark/adversarial/ablation harness;
- astronomical source and Ground Truth.

The tested system therefore ends at a typed candidate graph and is not the requested complete POC.

## 4. Datasets and fixtures

### Synthetic software fixture

`tests/fixtures/generate_fixture.py` deterministically generates an encoded RGB PPM containing
painted regions designed to exercise detector branches. Its source digest is:

```text
fb4fd2864605e49849543cab64de5eaa2c296555b8d4a3e0e5f4141d4b43891a
```

This fixture is suitable for software invariants only. Its internal variable names do not make its
regions astronomical entities or independent Ground Truth.

### Astronomical image-derived data

None. No authorised image, provider record, licence, instrument, band, epoch, calibration, or
reference catalogue was available.

## 5. Method

1. Inspect canonical `main` and the A/B handoff documents.
2. Run the complete published B unit/integration suite.
3. Generate the synthetic fixture and execute the documented CLI.
4. Repeat the run in a separate temporary directory.
5. Compare graph, provenance, manifest, and overlay bytes.
6. Review schemas against A's ontology and schema-readiness criteria.
7. Search for C/ASA/Standing/Context/Significance/Explanation artefacts.
8. Stop rather than invent the missing contracts.

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s tests -v

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src \
  python3 tests/fixtures/generate_fixture.py /tmp/asa-astro-synthetic.ppm

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m asa_astro.cli \
  /tmp/asa-astro-synthetic.ppm \
  --metadata tests/fixtures/synthetic_observation.metadata.json \
  --parameters examples/parameters.json \
  --source-locator fixture:synthetic-observation-v1 \
  --output /tmp/asa-astro-run
```

Codex D used fresh randomized `/tmp` paths to avoid overwriting existing output.

## 6. Baselines

No ranking baseline was executable because there is no Standing or Significance output.

Required but unrun baselines:

- brightness only;
- topology only;
- Confidence only;
- Standing only;
- context-free/equal-weight;
- proximity or image-centre heuristic where scientifically relevant as a negative control.

The absence of baselines is a blocker, not a zero score.

## 7. Results

### 7.1 B software verification

| Check | Result |
|---|---|
| Published unit/integration suite | PASS — 11 tests |
| Source-copy preservation | PASS |
| Existing-output overwrite refusal | PASS |
| Schema validation | PASS within B's preload registry |
| Evidence/candidate/assertion referential integrity | PASS |
| Strength and Confidence separation | PASS |
| Forbidden physical-relationship emission | PASS |
| Repeat-run byte equivalence | PASS |

The reviewed run emitted:

- processing run ID `run-59e1a9f3c29ee9f5043c`;
- 1 Observation;
- 1 Detector Output;
- 11 detections;
- 11 Evidence Records;
- 11 Candidate Entities;
- 43 candidate Relationship Assertions;
- graph JSON, provenance JSON, GraphML, overlay PNG, summary, manifest, and source copies.

### 7.2 Generated-result checksums

These checksums are Codex D's independent run at `59b1817`; they are evidence in this report, not a
ratified release oracle:

| Artefact | SHA-256 |
|---|---|
| `graph.json` | `4d76306bb3afe153ec938c31d9947f9c31ef2d15d3d08e22304afdeaf1839af2` |
| `provenance.json` | `31d6327892ac0c134267c2af7625ccf82286db46e2cc9769277fdb2f4daa1a03` |
| `overlay.png` | `5fd1b2e8c1d342c30092aa945923194ebe763665315ea14169ceeda57b82e5c2` |
| `manifest.json` | `5d474529fc7a3e6ffe8956cbced3a3bb4ae45041702c33e128d625ed51b53070` |

### 7.3 Central hypothesis

No ranking, Context sensitivity, brightness divergence, hierarchy recovery, calibration,
explanation completeness, or computational scaling result was produced. The central hypothesis
was not tested.

## 8. Failures and blocked checks

| Required evaluation | Outcome | Reason |
|---|---|---|
| Recovery of expected hierarchy | NOT RUN | No C/Standing contract or Ground Truth |
| Ranking stability | NOT RUN | No ranking implementation |
| Context sensitivity | NOT RUN | Contexts are non-executable semantic templates |
| Uncertainty calibration | NOT RUN | Synthetic heuristic confidence is explicitly uncalibrated |
| False-edge resilience | NOT RUN | No downstream reasoning/ranking consumer |
| Divergence from brightness | NOT RUN | No Significance output |
| Explanation completeness | NOT RUN | No Explanation Trace |
| Computational cost scaling | NOT RUN | No integrated pipeline |
| Astronomical comparison | NOT RUN | No authorised image/reference |

The B report's stated processing run ID,
`run-d50f4234b9d4f31bbcaa`, was not reproduced. The canonical commit repeatedly emitted
`run-59e1a9f3c29ee9f5043c`. This is a documentation/reproducibility defect returned to B.

## 9. Adversarial tests

The required D adversarial suite was not manufactured because the scoring contracts and admissible
semantics are absent. In particular, tests involving arbitrary Context weights or recursive
propagation cannot be defined before those policies exist.

B's own tests cover only bounded upstream negatives:

- physical relationship vocabulary is rejected;
- a bright point candidate is not made system-central;
- output paths are not overwritten;
- relationship strength and Confidence remain distinct.

These do not substitute for D's requested adversarial ranking tests.

## 10. Ablation studies

No ablation was run. The required variants—without Standing, relationship typing, uncertainty
penalties, recursive propagation, contextual weighting, and the brightness/topology/Confidence
baselines—require a reference implementation and frozen expected outcomes. Creating surrogate
formulae would silently manufacture the missing C/ASA design.

## 11. Uncertainty

- B confidence values are bounded but uncalibrated heuristic support values.
- The synthetic fixture provides no estimate of astronomical completeness, purity, identity
  accuracy, or relationship correctness.
- Candidate depth/association labels are not supported by an independent observation.
- The absence of C outputs is certain at the tested commit; the eventual implementation may change
  compatibility findings.
- No sampling uncertainty or statistical interval is meaningful because no benchmark population
  was evaluated.

## 12. Limitations

- Only an encoded synthetic image was processed.
- No FITS calibration, astrometry, catalogue matching, or resolved entity exists.
- No ASA dependency is present.
- No Standing, Significance, or Context-specific result exists.
- No visual explorer, baseline, benchmark, adversarial suite, or ablation exists.
- Schema validation currently relies on preloading flattened `$id` values.
- Several candidate labels semantically outrun their image-only evidence.
- The recorded checksums depend on the exact reviewed source and environment.

## 13. Reproducibility

The B stage is reproducible with the command in Section 5 and the dependency versions in
`requirements.lock`. Codex D observed byte equivalence across two independent temporary runs.

The complete POC is not reproducible because it does not exist. A clean checkout cannot produce
Standing ranking, multiple Context-specific rankings, baseline comparisons, explanation traces, or
a scientific validation result.

## 14. Falsification findings

| Bounded proposition | Finding |
|---|---|
| The B stage preserves source bytes and auditable derived records | Supported for the synthetic fixture |
| The B stage separates detection, evidence, candidate, and assertion records | Supported by tests and schema inspection |
| The B stage separates relationship strength from Confidence | Supported |
| The B stage is deterministic in the tested environment | Supported by two byte-equivalent runs |
| The published B report identifies the canonical fixture run | Weakened; cited run ID did not reproduce |
| Candidate labels never imply unavailable astronomical placement | Weakened; foreground/background/companion terminology remains |
| Typed relationships improve ranking over brightness | Unresolved; no ranking exists |
| Standing adds value | Unresolved; no Standing exists |
| Context changes Significance defensibly | Unresolved; no executable Context or Significance exists |
| Uncertainty is calibrated | Not supported; B explicitly reports uncalibrated values |
| ASA is validated | Not assessed and not an allowed conclusion |

## 15. Claim disposition

| Stated programme claim | Disposition |
|---|---|
| Provenance can be retained through an observation-to-candidate graph stage | Bounded support from synthetic execution |
| Typed candidate assertions can be represented without physical claims | Bounded support from schema/tests |
| Standing and Significance remain separate | Structurally respected by omission; not computationally tested |
| Significance is Context-dependent | Documented requirement only; not tested |
| Brightness is not Significance | No Significance exists; no comparison possible |
| Unknown and unavailable states remain representable | Partial support in B records |
| The integrated model beats naive visual prominence | Unresolved |
| ASA works in astronomy | Unresolved and outside this partial result |

## 16. Recommended next experiments

After the blockers are resolved:

1. Verify a named C handoff against B's candidate graph.
2. Freeze an ASA dependency and at least two authorised Context/weight policies.
3. Add schema-valid positive and negative synthetic reasoning fixtures.
4. Run the required adversarial and ablation matrix with predeclared expected outcomes.
5. Add one authorised astronomical input and independent reference manifest.
6. Freeze metrics, tolerances, partitions, and failure rules before evaluation.
7. Compare Context-specific outputs against brightness, topology, Confidence, Standing-only, and
   equal-weight baselines.
8. Inspect every explanation path for evidence, exclusions, uncertainty, and policy provenance.

## 17. Final review answer

**Unresolved.** The current repository supports a narrow claim that source evidence can be carried
reproducibly into a typed candidate graph for a synthetic fixture. It supplies no evidence yet that
typed relationships, Standing, Context, and uncertainty produce a more defensible ranking than
naive visual prominence.

## 18. Phase II superseding validation addendum

**Addendum date:** 2026-07-31
**Executable integration basis:** canonical upstream commit
`520f790a363660bbd97abf7f0f45f73cacc2d739`
**Addendum status:** COMPLETE SYNTHETIC ENGINEERING EXECUTION; SCIENTIFIC VALIDATION UNAVAILABLE
**Historical treatment:** Sections 1–17 are retained as the correct pre-C record. This addendum
supersedes only the earlier statements that the C pipeline and D execution artefacts did not exist.

### 18.1 Research question and bounded hypothesis

The executed question is whether this POC supplies evidence that evidence-backed typed
relationships, separate Standing, explicit Context, represented uncertainty, and bounded recursive
propagation yield reasoning more defensible than naive visual prominence on the available
ASA-Astro material.

“More defensible” requires more than a different ordering: inputs and transformations must be
traceable, Context changes must be isolated, adverse evidence must affect the result correctly,
and a reference capable of judging the ordering must exist. The test does not address whether ASA
is correct, complete, domain-independent, or scientifically validated.

### 18.2 System and datasets tested

The complete repository-native B→C path was run without an adapter:

```text
Observation → Evidence → Candidate Graph → Standing → Context
→ Significance → Explanation Trace
```

The run produced 11 Candidate Entities and 43 Relationship Assertions of types `containment`,
`observational`, `occlusion`, `spatial`, and `structural`. It used C's provisional algorithm and
its explicit `unavailable_not_consumed` ASA dependency state.

The only input remains the deterministic generated PPM with SHA-256
`fb4fd2864605e49849543cab64de5eaa2c296555b8d4a3e0e5f4141d4b43891a`. No authorised
astronomical image, catalogue, instrument metadata, calibrated measurement, or independent Ground
Truth was added. The frozen manual priority is a generator-informed synthetic comparator, not an
astronomical truth label.

### 18.3 Method and reproducibility package

The D harness is `validation/run_phase2.py`; clean-run instructions and environment commands are
in `validation/README.md`; exact dependencies remain in `requirements.lock`. A new output directory
is mandatory, so existing evidence cannot be overwritten.

The committed package includes:

- source and input manifest;
- B evidence bundle, overlay, graph JSON/GraphML, provenance, summary, and manifest;
- five frozen Context inputs;
- five C analysis bundles containing Standing, Significance, rankings, explanations, baselines,
  and manifests;
- benchmark, adversarial, ablation, explanation-validation, and reproducibility results;
- self-contained local `explorer.html`;
- a root SHA-256 artifact manifest.

Two internal independent executions compared 54 input/evidence/Context/reasoning files. All 54
were byte-identical. Stable identities were:

| Artefact | SHA-256 |
|---|---|
| graph | `0ff9dc94c797cb8701db73b8495634b5312b69f5593a9b5db75c588c9b201471` |
| provenance | `81336e2fc1259d3934ebb6949608b5072d5a8d7d95aced90c58ecc4de639a687` |
| overlay | `5fd1b2e8c1d342c30092aa945923194ebe763665315ea14169ceeda57b82e5c2` |
| D root manifest | `1aa75c8b75ebefe919643c450645a960707a41cafeae97e83d715f9711850ca7` |
| validation summary | `e4a6bb907bad8630bb9a123b31d6e16c4b670b0cf6768e3412c9812f995a6a13` |

Graph identity, artifact identity, Context hashes, result IDs, and Explanation Trace IDs were
stable. Standing outputs were identical across Context runs. On the manufacturing environment the
final harness run took 47.46 seconds and reached 80,968 KiB maximum resident memory; those
wall-clock/resource observations are environment-specific, not deterministic expectations. The
deterministic cost proxies were 1,682 structural propagated paths, 642 observational paths, and
zero paths in the other three Contexts.

### 18.4 Baseline results

For structural organisation, Significance and brightness had different top subjects, 35 of 55
pair orders disagreed, and Spearman rho was `-0.509090909091`. Brightness therefore does not merely
reappear as Significance in this run.

| Comparator | Same top as Significance | Pair disagreements / 55 | Spearman rho |
|---|---:|---:|---:|
| Brightness | No | 35 | -0.509090909091 |
| Image centre | No | 12 | 0.745454545455 |
| Degree centrality | Yes | 6 | 0.881818181818 |
| Eigenvector centrality | Yes | 5 | 0.936363636364 |
| Frozen manual priority | Yes | 6 | 0.890909090909 |

The result strongly diverges from visual brightness, but closely resembles topology. In the
absence of Ground Truth, that similarity cannot establish that the combined ranking is better than
degree/eigenvector centrality or the synthetic manual comparator. Multiplying all relationship
confidence values by `0.999` preserved the complete order (`rho=1.0`) and changed aggregate scores
by `0.000001125503`; this is one local stability check, not general robustness or calibration.

### 18.5 Context switching

Five Context declarations were evaluated against the identical graph and provenance:

| Context | Eligible input edges | Ranking observation |
|---|---:|---|
| Structural organisation | 31 | Distinct structural order |
| Observational interpretation | 32 | Same order as the three rows below |
| Scientific information value | 11 | Same order as observational interpretation |
| Star formation | 0 | Improper active non-zero order |
| Gravitational organisation | 0 | Improper active non-zero order |

Standing remained byte-identical in all five runs, so Context did not contaminate Standing.
Significance records and Context identities changed reproducibly, but only two distinct ordering
sequences emerged. More importantly, the two evidence-absent Contexts produced 11 non-zero results
with top score `0.052` rather than abstaining. Context isolation is supported; defensible
missing-evidence behaviour is not.

### 18.6 Adversarial results

Nineteen cases yielded 13 passes, 5 failures, and 1 declared limitation.

Bounded passes:

- a foreground point source changed to encoded brightness `1,000,000` became the brightness leader
  without changing any Significance score;
- moving the same foreground detection to the image centre changed only the image-centre baseline;
- a dim three-node bridge ranked first while contributing positive betweenness;
- contesting the leading candidate and its evidence reduced its score from `0.386631898042` to
  `0.113150853482`;
- disconnected and cyclic graphs terminated at their declared path bounds;
- eight distinct strength-`0.12` edges did not outrank the best endpoint of a single
  strength-`0.95` edge under the frozen adversarial Context;
- a 55-edge complete candidate graph emitted all 11 results, 990 bounded paths, converged in that
  scenario, and repeated byte-identically;
- duplicate node IDs, duplicate edge IDs, missing cited evidence, and unsupported relationship
  types were rejected;
- confidence `0.001` suppressed a false-proximity edge to maximum direct contribution
  `0.000030125937`.

Failures:

1. Base Standing centrality was deterministic but did not converge before its 64-iteration cap.
2. Putting the same evidence in supporting and contradicting lists was accepted and left every
   score unchanged.
3. Changing Relationship Assertion uncertainty to `contested` left every score unchanged.
4. An unresolved inferred dark/occluding image-region hypothesis accepted confidence `1.0` and
   `not_applicable` uncertainty, raising its score from `0.100958528681` to `0.719228201857`
   without a classification-specific warning. No dark-matter identity is asserted.
5. Evidence-absent star-formation and gravitational Contexts emitted active results instead of an
   indeterminate/abstaining state.

Extreme Context component weights selected two different top subjects. This is recorded as a
limitation because all weights are visible and schema-valid, but the repository supplies no
authorised scientific basis for choosing them.

### 18.7 Ablation results

| Ablation | Pair-order changes / 55 | Score L1 delta | Top changed | Interpretation |
|---|---:|---:|---:|---|
| Standing contribution removed | 1 | 0.228380453714 | No | Standing affects values and one pair, but is not decisive for the leader here |
| Context removed | n/a | n/a | n/a | Rejected because Context is required |
| Uncertainty penalties removed | 2 | 0.792943910784 | No | Largest numeric effect, modest order effect on this fixture |
| Relationship typing collapsed | 4 | 0.067294325673 | No | Typing affects ordering, but not the leader |
| Recursive propagation removed | 3 | 0.195795203323 | No | Propagation affects ordering and values, but not the leader |
| Contextual weight differentiation removed | 3 | 0.370927112939 | No | Weighting affects ordering and values, but not the leader |
| Explanation Trace removed | 0 | 0 | No | Numeric ranks survive, but all 11 result-to-explanation references become unresolved |

The ablations show that the declared components affect behaviour. They do not establish that any
component makes the ranking scientifically better: every numeric ablation retained the same top
subject, and no independent expected astronomical ordering exists.

### 18.8 Explanation and visual inspection

All 55 result traces identify their Standing contribution, propagated contribution, Context
adjustment, confidence effect, uncertainty penalty, excluded edges/evidence, graph/provenance
hashes, and result identity. Direct and propagated Evidence Records are resolvable through edge IDs
in the hash-bound graph. Included direct contributions do not carry Evidence IDs themselves, so a
detached trace is incomplete and is rejected as an adequate standalone explanation.

The static explorer displays the source image, detection overlay, graph nodes, typed edges,
Standing, selected-Context Significance, brightness-rank differences, confidence, uncertainty,
Evidence Records, exclusions, and top explanatory paths. It is an inspection instrument, not a UI
or scientific result.

### 18.9 Uncertainty, limitations, and falsification

- All image evidence, confidence, candidate labels, manual priority, and expected cases are
  synthetic or heuristic and explicitly uncalibrated.
- No astronomical image-derived graph or independent expected hierarchy exists.
- The sole fixture cannot estimate population robustness, scientific error, calibration, or
  generality.
- Context and model weights are provisional and not backed by an immutable ASA dependency.
- The high correlation with topology prevents attributing the structural ordering specifically to
  the combined architecture.
- Nonconvergent Standing centrality and the three semantic failures involving contradictions,
  assertion uncertainty, and evidence absence directly weaken the claimed defensibility.
- Component-scoped artifact identity is unstable because B's run ID incorporates downstream schema
  files.

Falsification disposition:

| Bounded claim | Disposition |
|---|---|
| Brightness is not simply reused as Significance | Supported on the synthetic fixture |
| Image-centre position is not directly reused as Significance | Supported on the synthetic fixture |
| Standing is Context-independent | Supported for the five executions |
| Context can change ordering | Supported narrowly: two orders from five declarations |
| Uncertainty can reduce candidate scores | Supported for candidate/evidence uncertainty |
| Relationship Assertion uncertainty affects reasoning | Not supported |
| Contradictory evidence affects reasoning | Not supported |
| Evidence absence remains representable without invented relevance | Not supported by output behaviour |
| Recursive propagation affects results | Supported behaviourally by ablation |
| The combined ranking is more correct/defensible than topology or manual priority | Unresolved without independent reference evidence |
| ASA is validated | Not assessed; prohibited conclusion |

### 18.10 Remaining questions and next experiments

1. Define and test contradiction aggregation and Relationship Assertion uncertainty semantics.
2. Add an explicit Context missingness/abstention contract.
3. Diagnose Standing centrality nonconvergence and freeze an acceptable termination rule.
4. Reconcile A's full Context model with C's executable schema.
5. Freeze scientifically justified weights and falsification thresholds before further evaluation.
6. Supply an authorised astronomical source plus independent, uncertainty-bearing reference data.
7. Test multiple graphs and held-out expected hierarchies, including cases where topology and the
   combined model predict different leaders.
8. Calibrate Confidence and uncertainty or keep all conclusions explicitly heuristic.

### 18.11 Phase II final review answer

**Insufficient evidence.** The POC now demonstrates deterministic, traceable divergence from naive
brightness and bounded behavioural contributions from typed relationships, Standing, Context,
uncertainty, and propagation. It does not demonstrate that the resulting reasoning is more
defensible within an astronomy validation domain because the only graph is synthetic, no
independent astronomical reference exists, the result largely tracks topology, centrality did not
converge, and contradiction, assertion uncertainty, and missing-evidence behaviour fail.
