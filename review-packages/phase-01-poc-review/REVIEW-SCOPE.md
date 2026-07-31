# ASA-Astro Independent Review Scope

## 1. Review authority and boundary

Review the complete tracked ASA-Astro proof of concept at commit
`7fc6e97c6aee4da076750f3f7082bbcd82e7291b`.

The review may identify defects, inconsistencies, unsupported claims, risks,
bounded remedies, and experiments. It must not rewrite the repository, redefine
ASA, close human decisions, upgrade synthetic output to astronomical evidence,
claim universal applicability, or treat a proposed remedy as adopted authority.

The current source conclusion is **Insufficient evidence**. Review whether that
conclusion follows from the evidence; do not assume it is correct merely because
it is cautious.

## 2. Architectural review

Examine the integrity of:

```text
Observation → Evidence → Candidate Graph → Standing
→ Context → Significance → Explanation → Validation
```

Determine:

- whether source image, detector output, Light Region, Candidate Entity,
  representation, and astronomical reality remain distinct;
- whether Relationship Assertions remain evidence-qualified instead of becoming
  established physical Relationships by graph insertion;
- whether Standing is genuinely independent of Context and materially distinct
  from Significance in ontology, schema, implementation, and outputs;
- whether Context is explicit, immutable, versioned, complete, and controlled,
  including missingness, abstention, output semantics, and authority;
- whether provenance, Confidence, uncertainty, contradiction, and evidence
  absence affect computation rather than appearing only in records;
- whether relationship typing changes meaningful reasoning or merely partitions
  standard topology;
- whether Explanation Traces support audit and falsification rather than only
  narrating the produced score;
- whether bounded recursion adds defensible information or graph amplification.

## 3. Scientific review

Determine:

- whether the astronomy framing is scientifically defensible for a validation
  domain rather than a novelty image demonstration;
- whether any candidate labels, image-plane relations, inferred dark/occluding
  regions, foreground/background language, or synthetic expectations overrun
  available evidence;
- whether apparent brightness, pixel area, central placement, proximity, or
  graph topology re-enter Significance under another name;
- whether synthetic fixtures and generator-informed manual priority are kept
  separate from astronomical Ground Truth;
- what authorised astronomical observations, catalogue releases, expert labels,
  physical models, uncertainty metadata, and held-out reference structures could
  support a legitimate next experiment;
- which first bounded astronomy question can be answered without inventing an
  object identity, relationship, measurement, or causal claim;
- what result would genuinely falsify the tested significance-first hypothesis.

## 4. Computational review

Inspect:

- centrality convergence, termination, numerical tolerance, and the meaning of a
  deterministic nonconverged truncation;
- max normalisation, candidate-set dependence, cross-graph comparability, and
  sensitivity to graph size/composition;
- provisional component, relationship-type, persistence, assertion-class,
  uncertainty, propagation, and Context weights;
- same-evidence support/contradiction handling and alternative assertion
  coexistence;
- Relationship Assertion uncertainty and Confidence calibration;
- zero-eligible-evidence behaviour, abstention, and indeterminate outputs;
- recursion depth, decay, cycle handling, path multiplicity, double-counting,
  complexity, and topology dominance;
- baseline fairness and whether degree/eigenvector/manual-priority comparisons
  are sufficient;
- ablation power, especially when all ablations retain the same leader;
- adversarial coverage and whether critical scientific misuse cases are missing;
- source, graph, Context, result, trace, and component identity stability;
- reproducibility claims, package locks, and environment scope.

## 5. Governance review

Review:

- every open human decision and whether implementation has provisionally crossed
  its boundary without adequate visibility;
- claim discipline across normative documents, handoffs, implementation,
  generated summaries, explorer, and reports;
- evidence traceability from conclusion to generated record to code/test/source;
- separation of engineering repeatability from scientific validation;
- the appropriateness and exact logical basis of **Insufficient evidence**;
- the absence of an explicit Codex A manufacturing report and whether the
  remaining commit/ownership evidence is adequate for review;
- whether issue severities, owners, remedies, and verification methods are
  proportionate and complete;
- which matters must remain under human, scientific, or ASA constitutional
  authority.

## 6. Validation Programme v0.2 proposal boundary

Propose the smallest defensible next validation programme. Treat “v0.2” as a
review deliverable label only. The proposal must include:

- the precise bounded scientific question and non-claims;
- source observations and independent Ground Truth candidates, with versions,
  licences, uncertainty, selection effects, and leakage controls;
- hypotheses and predeclared falsification criteria;
- remedies/tests for contradiction, assertion uncertainty, evidence absence,
  Context completeness, and Standing convergence;
- at least one held-out case where topology and the combined architecture make
  meaningfully different predictions;
- baselines, ablations, adversarial controls, calibration metrics, ranking
  metrics, false-relationship costs, and repeatability checks;
- minimum sample/graph diversity and independence units;
- decision gates requiring human or scientific authority;
- stop conditions that preserve an honest negative result.

Do not propose a broad application, production platform, new ASA constitution,
general astronomy system, or research programme larger than needed to test the
failed and unresolved claims.

## 7. Evidence standard for findings

Every finding must cite at least one exact corpus path and, where applicable, a
schema field, function, test, JSON result, issue ID, or report section. Distinguish:

- observed repository fact;
- interpretation or inference;
- open research question;
- human-authority decision;
- proposed remedy;
- validation test for the remedy.

An absence must be evidenced by the manifest/source index or a source register,
not by assuming the reviewer received an incomplete package.
