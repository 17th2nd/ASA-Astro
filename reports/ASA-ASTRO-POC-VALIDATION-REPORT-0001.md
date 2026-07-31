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
