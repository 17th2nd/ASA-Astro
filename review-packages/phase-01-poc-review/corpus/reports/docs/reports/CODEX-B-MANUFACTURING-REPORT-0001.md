# Codex B Manufacturing Report 0001

**Programme:** ASA-Astro proof of concept
**Operator:** Codex B — Observation, Evidence, and Graph-Construction Manufacturer
**Date:** 2026-07-31
**Session result:** Bounded deterministic evidence-to-candidate-graph component manufactured and verified; no scientific validation or ratification claimed

## 1. Repository inspection

### Authoritative and local state used

- GitHub repository: `17th2nd/ASA-Astro`.
- Default and canonical branch: `main`.
- Initial GitHub state observed: empty repository, no commits, no files, no issues, and no pull requests.
- First integration-register commit observed during manufacturing: `e57abe3` (`governance: register missing integration inputs`).
- Foundation/ontology commit observed and used: `351cc57` (`docs: establish ASA-Astro foundation and ontology`).
- No feature, personal, experimental, or operator branch was created or used.

Concurrent operator work appeared in the shared checkout while this unit was in progress. Codex B left all Codex A and Codex D paths unchanged and relocated B implementation into the foundation-assigned evidence boundary.

### Instructions and governance consulted

- supplied ASA-Astro programme and Operator Directive 0001;
- `docs/foundation/ASA-ASTRO-0001-foundational-definition.md`;
- `docs/architecture/REPOSITORY-STRUCTURE-0001.md`;
- relevant Observation Source, Detector Output, Light Region, Candidate Entity, Relationship Assertion, Evidence, Provenance, Confidence, Uncertainty, lifecycle, and schema-readiness sections of `docs/ontology/ASTRO-ONTOLOGY-0001.md`;
- applicable spatial, containment, structural, observational, occlusion, taxonomy-contract, and classification-lifecycle sections of `docs/ontology/ASTRO-RELATIONSHIP-TAXONOMY-0001.md`;
- `governance/decision-register.md`;
- `governance/integration-issues.md`;
- Codex D’s untracked integration review and report files, used only to avoid overlap.

No ASA constitutional or canonical material was copied into this repository.

## 2. Work performed

### Files created by Codex B

Repository entry and reproducible environment:

- `.gitignore`
- `README.md`
- `pyproject.toml`
- `requirements.lock`
- `examples/parameters.json`

Machine contracts:

- `schemas/common.schema.json`
- `schemas/observation/observation-source.schema.json`
- `schemas/observation/observation.schema.json`
- `schemas/observation/source-image-metadata.schema.json`
- `schemas/observation/detector-output.schema.json`
- `schemas/observation/detection.schema.json`
- `schemas/observation/evidence-record.schema.json`
- `schemas/observation/provenance-record.schema.json`
- `schemas/observation/confidence.schema.json`
- `schemas/observation/uncertainty.schema.json`
- `schemas/entity/candidate-entity.schema.json`
- `schemas/observation/candidate-graph/candidate-relationship-assertion.schema.json`
- `schemas/observation/candidate-graph/candidate-graph-node.schema.json`
- `schemas/observation/candidate-graph/candidate-graph-edge.schema.json`
- `schemas/observation/candidate-graph/candidate-graph.schema.json`

Executable evidence component:

- `src/asa_astro/__init__.py`
- `src/asa_astro/cli.py`
- `src/asa_astro/evidence/__init__.py`
- `src/asa_astro/evidence/models.py`
- `src/asa_astro/evidence/detection.py`
- `src/asa_astro/evidence/graph.py`
- `src/asa_astro/evidence/pipeline.py`
- `src/asa_astro/evidence/validation.py`

Fixtures and tests:

- `tests/__init__.py`
- `tests/fixtures/__init__.py`
- `tests/fixtures/generate_fixture.py`
- `tests/fixtures/synthetic_observation.metadata.json`
- `tests/fixtures/expected_assertions.json`
- `tests/fixtures/README.md`
- `tests/integration/__init__.py`
- `tests/integration/test_pipeline.py`
- `tests/unit/__init__.py`
- `tests/unit/test_models_and_schemas.py`
- `tests/unit/test_detection_and_relationships.py`

Documentation and handoff:

- `docs/pipeline/OBSERVATION-TO-GRAPH-PIPELINE-0001.md`
- `docs/pipeline/CODEX-B-HANDOFF-0001.md`
- `docs/reports/CODEX-B-MANUFACTURING-REPORT-0001.md`

### Files modified

None of the tracked Codex A or Codex D files was modified by Codex B.

### Files intentionally left unchanged

- all committed foundation, architecture, ontology, context, validation-framework, and decision-register files owned by Codex A;
- `governance/integration-issues.md`, including the concurrent modification made by Codex D;
- untracked Codex D files under `docs/integration/` and `reports/`;
- any future Codex C reasoning, normalised relationship, Standing, Context, Significance, or Explanation Trace implementation;
- ASA dependency content, because no immutable ASA version has been authorised;
- astronomical source data and Ground Truth, because none has been authorised.

## 3. Manufactured capability

The component:

1. hashes and content-addresses a replaceable source image and optional declared metadata;
2. refuses pre-existing output paths and never opens source inputs for writing;
3. records separate Observation Source, Observation, decoded Detector Output, Light Region/detection, Evidence, Candidate Entity, and Provenance records;
4. extracts encoded-image features without calling them calibrated flux or luminosity;
5. detects bright point-like, extended, diffuse-capable, local dark-deficit, internal-core, and possible diffraction-contaminated regions through transparent heuristics;
6. emits provisional and unresolved candidate representations with structured uncalibrated confidence and uncertainty;
7. creates candidate-graph assertions using canonical taxonomy types plus explicit image-space subtypes, roles, directionality, frame/missingness, strength, separate confidence, evidence, lifecycle, and provenance;
8. rejects gravitational, orbital, causal, evolutionary, and physical-distance edge vocabulary;
9. emits canonical JSON, provenance JSON, a SHA-256 manifest, Markdown summary, GraphML, diagnostic overlay, and immutable source copies;
10. validates every formal record against Draft 2020-12 JSON Schemas and cross-record invariants before publishing a bundle.

The component does not compute or store Standing or Significance.

## 4. Decisions made within the assigned implementation scope

1. Use CPython 3.12, Pillow, JSON Schema, and the standard library for the smallest transparent implementation with no hidden model.
2. Use exact dependency versions and record Python, Pillow, pipeline, code-tree, and schema-bundle digests in each run.
3. Use canonical JSON SHA-256 identifiers and omit nondeterministic clock time; execution time is explicitly represented as `unavailable`, pending a trusted run-authority contract.
4. Represent confidence as an explicitly `uncalibrated` bounded heuristic support score with a target proposition, method, evidence set, and inherited provenance—not as an implied probability.
5. Represent the detector output and candidate separately. Candidate resolution state remains `unresolved`.
6. Treat `primary_extended_object` only as the largest segmented extended image region under the run’s reproducible rule. It is not a galaxy identity, system centre, standing, or significance claim.
7. Place candidate-graph assertion contracts below `schemas/observation/candidate-graph/` and implementation below `src/asa_astro/evidence/`. This makes them Codex B’s pre-normalisation handoff and avoids occupying Codex C’s `src/asa_astro/reasoning/` boundary.
8. Use a small deterministic synthetic PPM generated from repository code for software regression only. It is not the initiating astronomical image and not Ground Truth.

These choices implement the current proof-of-concept unit. They do not close any human-owned decision-register item.

## 5. Assumptions

- The direct human directive assigning Codex B observation, evidence, and candidate-graph construction supplies session authority despite `DR-0002` still recording ownership confirmation as open. The register remains unchanged and requires owner reconciliation.
- A generated synthetic image with explicit unavailable scientific metadata is permissible as a unit/integration fixture under the assigned “small fixtures” boundary.
- Generic encoded RGB input is a replaceable representation; no physical calibration, observation band, epoch, sky coordinate, object identity, or source catalogue can be inferred from it.
- Candidate-graph assertions are evidence-stage inputs. Codex C remains responsible for any later normalised Relationship view and all Standing/Context/Significance reasoning under an authorised ASA dependency.
- Exact package versions plus code/schema digests are sufficient for this implementation trial, but they do not close the programme’s formal reproducibility-environment decision.

## 6. Tests and verification performed

### Repository-environment suite

Command:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Result: **11 tests passed**.

Coverage includes:

- Draft 2020-12 validity for all schemas;
- negative Candidate schema fixture with missing evidence;
- canonical identifiers and unknown/invalid parameter rejection;
- bright/extended, dark-deficit, and diffraction-contamination paths;
- required measurements and uncalibrated flags;
- positive orientation-alignment assertion;
- negative physical-relationship assertion;
- source hash and byte-identical source-copy preservation;
- Observation/Detector/Evidence/Candidate/edge cross-record links;
- at least one extended candidate;
- bright point candidates never becoming system-central;
- every edge citing evidence and setting `physical_claim: false`;
- pixel distances remaining uncalibrated image-space values;
- refusal to overwrite existing output;
- byte-for-byte equivalence across repeat runs.

### Clean isolated installation

An isolated temporary virtual environment installed the exact versions from `requirements.lock`, installed the package editable without dependency substitution, and ran the same suite.

Result: **11 tests passed**.

### Deterministic CLI fixture execution

The final inspected fixture run produced:

- processing run ID: `run-d50f4234b9d4f31bbcaa`;
- source SHA-256: `fb4fd2864605e49849543cab64de5eaa2c296555b8d4a3e0e5f4141d4b43891a`;
- 1 Observation;
- 1 Detector Output;
- 11 detections;
- 11 Evidence Records;
- 11 Candidate Entities;
- 43 Relationship Assertions;
- 7 manifest-listed generated/source artefacts, excluding the manifest’s own recursive digest.

Observed candidate types included primary extended, possible companion, background extended, internal substructure, likely foreground point, dark/occluding hypothesis, and unknown/possible-contamination regions.

Observed relationship type/subtype pairs included containment/containment, observational/observational-dependency, occlusion/occlusion, spatial/overlap, spatial/proximity, structural/morphological-association, and structural/shared-structural-region. Spatial/orientation-alignment is covered by its dedicated positive unit fixture.

### Integrity checks

- `git diff --check` — passed.
- JSON parsing for every schema — passed through the schema-loader test.
- Repeat output comparison — passed byte-for-byte.
- Existing-output sentinel preservation — passed.
- No hidden ML or network lookup is used during processing.

## 7. Known limitations

- The detector is a generic encoded-image threshold baseline, not an astronomy source-extraction system.
- Confidence is uncalibrated and cannot be interpreted as probability.
- One image cannot establish foreground/background depth, companionship, system membership, astronomical identity, occlusion cause, or physical association.
- Axis-aligned bounding geometry can overstate irregular-region overlap and containment.
- Dark-deficit detection can confuse absorption, masks, edges, colour mapping, or processing artefacts.
- Encoded RGB can be nonlinear, stretched, composite, or non-photometric.
- The current implementation does not apply EXIF orientation or astronomy-specific FITS calibration.
- Pixel lists and Python flood fill are not intended for production-scale survey images.
- Schema discovery assumes a source checkout; a standalone wheel data-layout contract is not yet manufactured.
- Execution time is unavailable in deterministic output until a trusted, reproducible timestamp policy is authorised.
- Synthetic success establishes software invariants only. Completeness, purity, scientific accuracy, and uncertainty calibration are unmeasured.

## 8. Integration requirements

1. Codex C must consume schema/versioned candidate graph records without converting provisional image labels into established relationships, and must preserve B evidence/provenance identifiers.
2. Any Codex C normalised Relationship schema must distinguish its semantic record from B’s `candidate-relationship-assertion` handoff and record a mapping/version.
3. Codex D should verify a named stable commit from a clean worktree after all concurrent operator files are published; local transient files are not an integration handoff.
4. The human operator must reconcile the direct Codex B assignment with `DR-0002` and the integration issue register without retroactively treating silence as approval.
5. A versioned ASA dependency is required before Standing, Context, Significance, or ASA-conformance work.
6. An approved astronomical image needs provider, identity, version, licence/use authority, checksum, instrument, band, epoch, calibration, and limitations before an image-specific demonstration.
7. Independent scientific comparison sources, uncertainty rules, and frozen tolerances are required before benchmark or validation claims.
8. Formal coordinate, epoch, band, confidence-calibration, and runtime-reproducibility policies remain downstream integration requirements.

## 9. Repository integrity check

| Question | Result |
|---|---|
| Duplicate work introduced? | No duplicate implementation was found. Candidate assertions are explicitly B pre-normalisation records, not Codex C reasoning records. |
| Repository structure preserved? | Yes. B code is under `src/asa_astro/evidence/`; B schemas are under observation/entity boundaries. |
| Governance followed? | The committed foundation and ontology were integrated after appearing during the session. Open human decisions remain open. |
| Interfaces preserved? | No pre-existing executable interface existed. Codex A and D files were not modified. |
| Scientific boundaries preserved? | Yes. No identity, physical distance, physical relationship, standing, significance, Ground Truth, or validation conclusion is asserted. |
| ASA/ASA-Astro boundary preserved? | Yes. No ASA material was copied and no ASA dependency is claimed. |
| Outstanding conflicts? | Direct B assignment versus open register ownership confirmation; candidate assertion handoff requires explicit Codex C mapping. |

## 10. Blockers requiring operator decision

- `DR-0001`: immutable ASA dependency and consumed interface;
- `DR-0002`: repository ownership/register reconciliation for B/C/D;
- `DR-0003`: approved illustrative astronomical image and use authority;
- `DR-0004`: catalogue and scoped Ground Truth selection;
- `DR-0005`: authorised “primary galaxy”/system rule for any scientific context—the B image-region label is not such a rule;
- `DR-0006`: entity-resolution policy;
- `DR-0007`: scientific coordinate, epoch, time, unit, and band conventions;
- `DR-0011`: confidence vocabulary and calibration datasets;
- `DR-0015`: formal implementation/toolchain selection beyond this bounded trial;
- `DR-0016`: formal determinism and run-environment contract;
- `DR-0017`: scientific data storage and retrieval policy;
- `DR-0020`: review, release, and change authority.

No blocker was silently resolved, and no blocker prevented the bounded synthetic software component explicitly assigned in this session from being manufactured and tested.

## 11. Final review question

**Can the emitted graph be audited back to individual observations, parameters, and transformations without relying on conversational memory?**

**Yes for this bounded implementation contract and synthetic regression fixture.** Every graph assertion cites Evidence Records; those identify subject, claim, role, source, Detector Output, measurements, image frame, missing epoch/band, limitations, uncertainty, and Provenance. Provenance records the run, input digests, ordered parents, code/schema/software versions, parameters, transformations, warnings, and immutable source identity.

This is an auditability result, not a finding that the image-derived candidates or relationships are scientifically correct and not a declaration that ASA or ASA-Astro has been validated.
