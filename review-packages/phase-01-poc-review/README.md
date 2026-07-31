# ASA-Astro Phase 01 Proof-of-Concept Review Package

## Package identity

This is a packaging and orientation layer over the complete tracked snapshot of
`17th2nd/ASA-Astro` at source commit
`7fc6e97c6aee4da076750f3f7082bbcd82e7291b`.

The copied corpus is byte-for-byte source evidence. This README, the review
scope, reviewer guidance, source index, manifests, packaging tools, and
model-specific prompts are generated packaging artefacts. They do not amend,
summarise away, supersede, or reinterpret the source corpus. If packaging prose
and a copied source artefact differ, the copied source artefact and canonical
Git history control.

The source commit contains 141 tracked regular files. Every one is included
exactly once in each complete reviewer archive. No `.git` content, untracked
file, cache, virtual environment, secret, credential, or machine-local state is
included.

## Programme in one bounded statement

ASA-Astro is an astronomy-domain proof of concept intended to test Adaptive
Significance Architecture (ASA), not to redefine ASA. The implemented path is:

```text
Observation
→ Evidence
→ Candidate Graph
→ Standing
→ explicit Context
→ Significance
→ Explanation Trace
→ benchmark, adversarial, and ablation evidence
```

The source image used in Phase II is a deterministic synthetic software fixture,
not an astronomical observation or Ground Truth.

## Hypothesis tested

The bounded hypothesis was whether evidence-backed typed relationships, separate
Standing, explicit Context, represented uncertainty, and bounded recursive
propagation produce reasoning more defensible than naive visual prominence on
the available ASA-Astro material.

“More defensible” requires traceable evidence and transformations, isolated
Context effects, correct adverse-evidence behaviour, and an independent
reference capable of judging the ordering. Merely producing a different ranking
is not sufficient.

## Implemented architecture

- Codex A supplies the foundation, ontology, relationship taxonomy, Context
  model, validation framework, repository structure, and decision register.
- Codex B supplies the deterministic source-to-evidence-to-candidate-graph
  implementation, observation/entity schemas, fixtures, tests, and handoff.
- Codex C supplies a provisional Standing and context-specific Significance
  implementation, reasoning schemas, Explanation Traces, baselines, fixtures,
  tests, and handoff. It records the ASA dependency as
  `unavailable_not_consumed`.
- Codex D supplies integration review, the Phase II harness, five Context runs,
  benchmark comparisons, adversarial cases, ablations, reproducibility evidence,
  a static explorer, and the validation conclusion.

Operator descriptions identify manufacturing provenance; they do not resolve
the open human ownership decision.

## Evidence present

The corpus contains:

- normative and provisional programme definitions;
- all machine-readable schemas;
- the complete B and C implementations;
- unit, reasoning, integration, and Phase II tests;
- exact dependency declarations;
- the synthetic fixture and generated evidence bundle;
- five Context-specific reasoning bundles;
- baseline, adversarial, ablation, explanation, and reproducibility results;
- a content-addressed Phase II manifest and lightweight static explorer;
- integration findings, open decisions, manufacturing reports, and the bounded
  validation report.

The Phase II run reports 54 byte-identical files across two internal executions,
separate Standing across five Context runs, divergence from brightness, and
traceable component contributions.

## Material failures and limitations

The Phase II adversarial register records 13 passes, 5 failures, and 1 declared
limitation. The material failures are:

1. base Standing centrality reached its iteration cap without convergence;
2. the same evidence could be both supporting and contradicting without effect;
3. Relationship Assertion uncertainty could become `contested` without changing
   a score;
4. an unresolved inferred dark/occluding image-region hypothesis could receive
   excessive certainty without a hypothesis-specific guard;
5. Contexts with zero eligible relationship evidence emitted active non-zero
   rankings instead of abstaining or becoming indeterminate.

The structural Significance ranking diverged from brightness but remained highly
correlated with degree and eigenvector centrality. All numeric ablations retained
the same top subject. Only two distinct ranking orders emerged from five Context
declarations. No authorised astronomical source, catalogue, calibrated
Confidence, independent expected hierarchy, immutable ASA dependency, or
scientifically authorised weighting policy exists.

## Current conclusion

The authoritative report concludes **Insufficient evidence**.

The proof of concept demonstrates deterministic and traceable engineering
behaviour, including divergence from naive brightness. It does not demonstrate
that the combined reasoning is more scientifically defensible than topology or
manual priority because the only graph is synthetic, there is no independent
astronomical reference, several critical semantic behaviours fail, and the
result substantially tracks graph centrality.

## Validation Programme v0.2 review target

“Validation Programme v0.2” is a requested reviewer-proposal label, not an
adopted source-corpus programme or authorised repository decision. Reviewers are
asked to propose the smallest defensible next programme that investigates the
source report's eight next-experiment areas:

1. contradiction aggregation and Relationship Assertion uncertainty;
2. Context missingness and abstention;
3. Standing convergence and termination policy;
4. alignment between the full Context model and executable schema;
5. scientifically justified weights and predeclared falsification thresholds;
6. an authorised astronomical source and independent uncertainty-bearing
   reference data;
7. multiple graphs and held-out hierarchies where topology and the combined
   model make different predictions;
8. calibrated Confidence/uncertainty, or explicit retention of heuristic status.

Reviewer proposals must remain bounded remedies or experiments. They must not be
presented as adopted architecture, ASA amendment, scientific discovery, or
universal validation.

## Reading order

1. `REVIEW-SCOPE.md`
2. the prompt in the archive's `gemini/` or `claude/` directory
3. `REVIEWER-GUIDANCE.md`
4. `SOURCE-INDEX.md`, especially rows marked **Yes** under “Must read”
5. foundation, ontology, Context, and significance model
6. B and C handoffs plus implementation/schema/test evidence
7. D integration review, issue register, Phase II summary, adversarial and
   ablation results
8. the complete POC validation report and open decision register

## Archive and integrity verification

The repository stores two complete deterministic archives under `archives/`.
Each archive contains the shared corpus plus only its own model-specific prompt.
Archive checksums are in `archives/SHA256SUMS`.

From a clean checkout containing the packaging commit:

```bash
python3 review-packages/phase-01-poc-review/tooling/build_review_packages.py
python3 review-packages/phase-01-poc-review/tooling/validate_review_packages.py
cd review-packages/phase-01-poc-review/archives
sha256sum -c SHA256SUMS
```

The build uses only the Python standard library and Git. ZIP member timestamps,
permissions, ordering, compression settings, and JSON serialization are fixed.

## Source gaps preserved, not repaired

- No standalone Codex A manufacturing report exists at the source commit.
  `governance/integration-issues.md` records this as `INT-0002`. The Codex A
  commit and all A-owned artefacts are included; no report was reconstructed
  from conversation history.
- No immutable ASA dependency exists.
- No authorised astronomical input or independent Ground Truth exists.
- Human decisions in `governance/decision-register.md` remain open.

## Source-level duplicate bytes

The source commit itself stores identical synthetic PPM bytes at both the Phase
II input path and the content-addressed evidence/source path. It also stores
Context and result derivatives in multiple provenance roles. The package
preserves these distinct authoritative paths exactly. It introduces no duplicate
copy of any one source path; `MANIFEST.json` and `LARGE-EVIDENCE.md` disclose
their paths, roles, sizes, and hashes.
