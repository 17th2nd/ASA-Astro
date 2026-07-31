# Reviewer Guidance

## 1. Evidence precedence

Use this order when sources differ:

1. exact copied source artefact and generated result at source commit;
2. repository governance and decision records;
3. normative programme documents;
4. provisional model/implementation documents and schemas;
5. implementation and executable tests;
6. evidentiary reports and generated summaries;
7. packaging orientation prose.

This order is a reading discipline, not permission to ignore document authority
statements. Report conflicts rather than silently selecting a preferred source.

## 2. Terminology discipline

Preserve the source meanings of Observation, Evidence Record, Candidate Entity,
Relationship Assertion, Relationship Type, Standing, Context, Significance,
Explanation Trace, Ground Truth, Benchmark, and Validation Result.

Do not replace:

- Candidate Entity with astronomical object;
- image-space proximity with physical proximity;
- Relationship Assertion with established relationship;
- strength with Confidence;
- Standing with Significance;
- brightness or topology with significance;
- deterministic output with scientific truth;
- synthetic comparator with Ground Truth;
- open decision with implementation permission.

## 3. Review method

1. Verify `MANIFEST.json` and the package checksum before substantive review.
2. Read the model-specific prompt and `REVIEW-SCOPE.md`.
3. Use `SOURCE-INDEX.md` to follow the required reading and dependencies.
4. Trace each material claim from report to generated JSON, then to harness,
   implementation, schema, and test.
5. Attempt to falsify separation, provenance, Context, uncertainty, and
   non-brightness claims.
6. Compare ontology requirements with machine schemas and runtime behaviour.
7. Distinguish a defect in this implementation from an open research question
   and from a human-authority decision.
8. Propose only bounded remedies and tests.

The static explorer is an inspection aid. It is not an authoritative summary and
must not replace JSON, source, or report evidence.

## 4. Severity vocabulary

- **Critical:** permits invalid scientific/constitutional claims, corrupts the
  central reasoning boundary, or makes the principal conclusion unreliable.
- **Major:** materially weakens validity, traceability, reproducibility, or the
  ability to execute the next bounded experiment.
- **Moderate:** bounded defect or mismatch with limited impact and a local
  remedy.
- **Minor:** clarity, ergonomics, or low-risk consistency issue.
- **Observation:** relevant evidence that is not a defect.
- **Open research question:** cannot be resolved from current evidence and should
  not be mislabeled as a defect.

## 5. Required finding record

For every finding return:

| Field | Required content |
|---|---|
| Finding ID | Stable reviewer-local identifier |
| Severity | Critical, Major, Moderate, Minor, Observation, or Open research question |
| Classification | Defect, divergence, unsupported claim, governance gap, deferred research, or rejected concern |
| Evidence | Exact corpus paths and specific section/field/function/result/test |
| Observation | What the repository directly shows |
| Rationale | Why it matters within the bounded hypothesis |
| Impacted claim | Exact claim or decision affected |
| Remedy | Smallest bounded change or experiment; `none` for rejected concerns |
| Validation test | How the remedy or claim would be falsified/verified |
| Authority | Implementing operator, scientific reviewer, human programme authority, or ASA authority |

Do not merge multiple unrelated defects into one record merely because they
share a component.

## 6. Required review output

Return:

1. package integrity statement and source commit;
2. executive conclusion;
3. finding register in severity order;
4. ontology-to-schema-to-code divergence table;
5. conclusion-validity trace for **Insufficient evidence**;
6. rejected concerns and why they are not defects;
7. bounded Validation Programme v0.2 proposal;
8. human-authority decision list;
9. residual uncertainties and material not independently verifiable.

State clearly whether the package was sufficient for independent review without
conversation history. Do not claim that completing this review validates ASA,
ASA-Astro, or any astronomical interpretation.
