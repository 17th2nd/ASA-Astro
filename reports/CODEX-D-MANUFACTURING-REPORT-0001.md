# Codex D Manufacturing Report 0001

**Programme:** ASA-Astro proof of concept
**Operator:** Codex D — Integration, Benchmark, Visualisation, and Adversarial Validation
**Date:** 2026-07-31
**Canonical input commit:** `59b1817c07d3bc7e72d7353459c3177362e72a4e`
**Session result:** A→B integration reviewed and independently executed; complete D harness blocked

## 1. Repository inspection

### Authoritative state used

The GitHub repository `17th2nd/ASA-Astro` was empty at session start. During the session:

1. Codex D published the initial integration blocker register at `e57abe3`.
2. Codex A's foundation/ontology unit reached canonical `main` at `351cc57`.
3. Codex B's observation-to-candidate-graph handoff reached canonical `main` at `59b1817`.

Transient concurrent files were not treated as authoritative until the corresponding commits were
visible on GitHub. No branch or parallel repository was created.

### Files and areas inspected

- `README.md`
- `docs/architecture/REPOSITORY-STRUCTURE-0001.md`
- `docs/foundation/ASA-ASTRO-0001-foundational-definition.md`
- `docs/models/ASTRO-CONTEXT-MODEL-0001.md`
- `docs/ontology/ASTRO-ONTOLOGY-0001.md`
- `docs/ontology/ASTRO-RELATIONSHIP-TAXONOMY-0001.md`
- `docs/validation/ASTRO-VALIDATION-FRAMEWORK-0001.md`
- `docs/pipeline/`
- `docs/reports/CODEX-B-MANUFACTURING-REPORT-0001.md`
- `governance/decision-register.md`
- `governance/integration-issues.md`
- `schemas/`
- `src/asa_astro/`
- `tests/`
- `examples/parameters.json`
- `pyproject.toml`
- `requirements.lock`

### Instructions and governance consulted

- supplied ASA-Astro operator directive and repository discipline;
- repository foundation and authority boundaries;
- proposed ownership/collision boundaries;
- Context model;
- relationship taxonomy;
- validation framework;
- all open decision-register entries relevant to integration.

No ASA constitutional or canonical material was copied into this repository.

## 2. Work performed

### Files created

- `docs/integration/INTEGRATION-CONTRACT-REVIEW-0001.md`
- `reports/ASA-ASTRO-POC-VALIDATION-REPORT-0001.md`
- `reports/CODEX-D-MANUFACTURING-REPORT-0001.md`

### Files modified

- `governance/integration-issues.md`

The issue register was created by Codex D as the repository's initial commit and later updated
after A and B published their handoffs.

### Files intentionally left unchanged or uncreated

- all Codex A foundation, ontology, model, architecture, validation-framework, and decision files;
- all Codex B source, schemas, fixtures, tests, documentation, dependency, and root files;
- no Codex C substitute implementation;
- no ASA adapter or dependency;
- no scientific image, identity, Ground Truth, measurement, or relationship;
- no Standing, Context weight, Significance, or Explanation Trace implementation;
- no visual explorer, benchmark suite, adversarial-ranking fixture, or ablation harness.

Those missing deliverables depend on unresolved upstream or human-owned contracts. Creating them
would have crossed operator boundaries and silently selected ASA/scientific semantics.

## 3. Decisions made

1. Use committed GitHub `main` state only for formal review.
2. Allow concurrent A/B manufacturing to finish before freezing interface findings.
3. Independently verify B's published tests and deterministic fixture.
4. Accept B only as an observation-to-candidate-graph handoff, not a complete typed scientific
   Relationship graph.
5. Stop at the missing C/ASA boundary.
6. Record upstream defects without changing their files.
7. Keep synthetic software verification separate from astronomical validation.
8. Answer the final research question as unresolved.

No constitutional, scientific, Context-weight, Standing, Significance, ownership, or validation
decision was made.

## 4. Assumptions

- Commit `59b1817` is the stable integration basis for this report.
- The direct user directive assigns Codex D its role, while `DR-0002` still requires repository
  reconciliation.
- Codex C owns the missing reasoning implementation as proposed by the current structure document;
  Codex D is not authorised to replace it.
- The synthetic fixture is permitted for software verification only.
- B's content hashes and exact software versions identify its bounded run, but not an astronomical
  observation.

## 5. Tests and inspection methods

### Git and structure

```bash
git status --short --branch
git log --oneline --decorate --stat
git show --name-status --format=fuller 351cc57
git show --name-status --format=fuller 59b1817
find . -path './.git' -prune -o -type f -print | sort
git diff --check
```

### Contract inspection

```bash
rg -n 'Standing|Significance|weight|provenance|uncertainty|relationship' \
  docs governance schemas src tests
jq -c '{id:."$id",title,required,additionalProperties}' schemas/**/*.json
rg -n '\\$id|\\$ref' schemas
```

### Executable verification

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src \
  python3 -m unittest discover -s tests -v
```

Result: **PASS — 11 tests**.

The documented fixture and CLI were run twice in:

- `/tmp/asa-astro-b-review.dDze8F/run`
- `/tmp/asa-astro-b-repeat.YjhbSJ/run`

`cmp` passed for `graph.json`, `provenance.json`, `manifest.json`, and `overlay.png`.

Observed current run ID: `run-59e1a9f3c29ee9f5043c`.

Key independent hashes:

- graph: `4d76306bb3afe153ec938c31d9947f9c31ef2d15d3d08e22304afdeaf1839af2`;
- provenance: `31d6327892ac0c134267c2af7625ccf82286db46e2cc9769277fdb2f4daa1a03`;
- overlay: `5fd1b2e8c1d342c30092aa945923194ebe763665315ea14169ceeda57b82e5c2`;
- manifest: `5d474529fc7a3e6ffe8956cbced3a3bb4ae45041702c33e128d625ed51b53070`.

No executable scientific, ranking, adversarial, ablation, or calibration test was possible.

## 6. Findings

### Verified bounded capability

- source bytes and declared metadata are content-addressed;
- evidence, candidate, and candidate-assertion references validate;
- relationship strength and Confidence remain separate;
- unavailable scientific metadata remains explicit;
- physical relationship vocabulary is rejected;
- repeated B runs are byte-equivalent in the tested environment.

### Defects returned upstream

- no Codex C handoff;
- no immutable ASA dependency;
- no authorised astronomical input or Ground Truth;
- nested schema `$id` values do not match repository paths;
- B's embedded Confidence/Uncertainty and lifecycle fields do not clearly satisfy A's
  stable-identity/predecessor/successor criteria;
- foreground/background/companion labels semantically outrun image-only evidence;
- B's published report run ID does not reproduce from its canonical commit;
- no expected-output checksum manifest;
- no B-to-C assertion normalisation mapping.

Full evidence, owners, remedies, and verification methods are in
`governance/integration-issues.md`.

## 7. Known limitations

- The requested complete proof of concept was not manufactured.
- The reviewed execution is synthetic, not astronomical.
- The visual graph explorer does not exist.
- No Standing or Significance ranking exists.
- No Context sensitivity or brightness-divergence result exists.
- No benchmark, adversarial suite, ablation, computational-scaling study, or Explanation Trace
  exists.
- B confidence is explicitly uncalibrated.
- A future C handoff may change interface findings and require a new review version.

## 8. Integration requirements

Before Codex D resumes complete integration:

1. Publish and verify the Codex C reasoning handoff.
2. Decide the immutable ASA dependency and consumed interface.
3. Reconcile operator ownership in `DR-0002`.
4. Resolve or disposition the A/B schema and candidate-semantics defects.
5. Select approved astronomical input with provenance and use authority.
6. Select independent Ground Truth/reference sources.
7. Freeze at least two Contexts, weight policies, output semantics, and missingness rules.
8. Freeze benchmarks, baselines, metrics, tolerances, and falsification thresholds.
9. Supply expected checksums or bounded tolerances for all upstream stages.

## 9. Repository integrity check

| Question | Result |
|---|---|
| Duplicate work introduced? | No; D files contain integration evidence only |
| Repository structure preserved? | Yes; D used the designated integration/governance/report locations |
| Other operators' files modified? | No |
| Governance followed? | Yes; open decisions remained open and upstream defects were not repaired silently |
| Interfaces preserved? | Yes; review and execution did not change A/B interfaces |
| Scientific boundaries preserved? | Yes; no synthetic result is reported as astronomy |
| ASA/ASA-Astro boundary preserved? | Yes; no ASA material or substitute definition was added |
| Branch policy preserved? | Yes; no branch, PR, or parallel history was created |
| Outstanding conflicts? | Missing C/ASA/data/reference contracts and recorded A/B defects |

## 10. Blockers requiring operator decision

- `DR-0001`: ASA dependency and interface;
- `DR-0002`: ownership reconciliation;
- `DR-0003`: astronomical source identity and use authority;
- `DR-0004`: Ground Truth sources;
- `DR-0005`: benchmark question and primary-system rule;
- `DR-0008`: Context authority and weighting policy;
- `DR-0009`: Standing contract;
- `DR-0010`: Significance semantics;
- `DR-0011`: Confidence/calibration policy;
- `DR-0014`: benchmark metrics and thresholds;
- `DR-0020`: review/release authority.

Codex C's absent handoff is an upstream manufacturing blocker, not a decision Codex D may make.

## 11. Final review answer

The integrated proof of concept does not yet provide evidence that typed Relationships, Standing,
Context, and uncertainty produce a more defensible ranking than naive visual prominence. It does
provide bounded evidence that the B source-to-candidate-graph stage is auditable and deterministic
for its synthetic fixture. The distinction and the limits are stated explicitly.
