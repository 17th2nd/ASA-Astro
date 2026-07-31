# Observation-to-Graph Pipeline 0001

**Version:** 0.1.0
**Operator:** Codex B
**Maturity:** Bounded proof of concept
**Validation claim:** None; synthetic regression success is not astronomical validation

## 1. Purpose and boundary

This pipeline converts a replaceable visual input and optional declared metadata into an auditable candidate graph. It preserves the distinction between the source image and astronomical reality, pixels and entities, observations and inferences, relationship assertions and established relationships, relationship strength and confidence, and graph inputs versus scientific ground truth.

It does not:

- redefine or embed ASA;
- identify an astronomical object;
- convert encoded brightness to luminosity;
- convert pixel distance to physical distance;
- infer gravitational, orbital, causal, or evolutionary relations;
- compute standing;
- declare a context or compute significance;
- treat a model output as scientific ground truth;
- claim that visible matter exhausts physical structure;
- claim scientific validation is complete.

## 2. Pipeline stages

```text
replaceable image + declared metadata
  → immutable content-addressed registration
  → separate Observation and decoded Detector Output records
  → decoded image metadata and encoded-luminance statistics
  → transparent threshold segmentations
  → pixel feature records with uncertainty
  → provisional candidate representations
  → evidence-backed image-space relationship assertions
  → schema validation and cross-record invariant checks
  → graph, provenance, manifest, summary, GraphML, and diagnostic overlay
```

This implements the common conceptual pipeline only through candidate relationship construction. Relationship classification is retained in each assertion. Standing, context, significance, reasoning, and external ground-truth validation are downstream and absent by design. The implementation resides under the foundation-assigned `src/asa_astro/evidence/` boundary.

## 3. Dependencies and environment

- CPython 3.12.3 in the verified environment;
- Pillow 10.2.0 for image decoding, local Gaussian background, and diagnostic rendering;
- jsonschema 4.10.3 for Draft 2020-12 contract validation;
- Python standard library for hashing, connected components, statistics, graph construction, JSON, XML text, and tests.

Exact direct and transitive versions used by this proof of concept are in `requirements.lock`. The processing run records Python, Pillow, pipeline version, and all parameters. There is no machine-learning component and no hidden model classification.

## 4. Input preservation and registration

`process_observation` requires a source image and a path for a new output directory. It refuses an existing output path. Source and optional metadata are read and SHA-256 hashed, never opened for writing, and copied byte-for-byte into the output bundle under content-addressed names. Copies are re-hashed before bundle publication.

The processing-run ID is derived from:

- source SHA-256;
- optional metadata SHA-256;
- every detector parameter;
- pipeline, Python, and Pillow versions;
- SHA-256 of the executable evidence-module source set and schema bundle.

This avoids nondeterministic timestamps. The source record stores the original filename and a caller-declared stable locator without embedding a machine-specific absolute path by default.

Pillow-captured width, height, format, source mode, and source channels are recorded. A separate Observation retains supplied or unavailable acquisition fields, and a separate computed Detector Output represents the RGB decode. Declared metadata is retained verbatim in the provenance bundle but does not silently drive physical conversions. Calibration and physical scale default to `unavailable`.

## 5. Detection and feature extraction

The detector uses deterministic integer Rec.709-weighted encoded luminance. This is a display-encoding measurement, not calibrated flux or physical luminosity.

### 5.1 Bright and extended regions

The global background is the image median. A robust scale estimate is `1.4826 × median absolute deviation`, bounded below by 1. The low and core thresholds are:

```text
background + max(configured minimum delta, configured sigma × robust scale)
```

Eight-connected pixels above each threshold become regions. Low-threshold regions support point-like, extended, diffuse, or unresolved image-morphology labels. A smaller high-threshold component nested in an extended low-threshold region becomes an internal-substructure candidate.

### 5.2 Dark or occluding candidates

A Gaussian-smoothed encoded-luminance image supplies a local comparison. Pixels whose local smooth value exceeds the original by `dark_local_delta`, within an already luminous local neighbourhood, form dark-deficit regions. The output calls these `dark_or_occluding_region` hypotheses and records that an intensity deficit does not establish dust, obscuration, absence of matter, or any physical cause.

### 5.3 Diffraction-spike contamination

A bright, low-fill component that is elongated or larger than the point-region limit receives `possible_diffraction_spike_contamination`. This flag lowers confidence and prevents promotion to a foreground-point hypothesis. It is a conservative morphology warning, not an optical-instrument diagnosis.

### 5.4 Features

Each region records, where computable:

- intensity-weighted centroid in pixels;
- axis-aligned pixel bounding box;
- segmented area;
- raw integrated encoded luminance;
- local-background-adjusted encoded intensity;
- peak or dark-deficit intensity;
- three-pixel-ring local background median;
- mean encoded RGB channels;
- bounding-box extent/fill;
- covariance-derived orientation and elongation;
- local candidate density in image space;
- centroid distance from the provisional major extended region in pixels;
- segmentation confidence and explicit uncertainty notes.

Every numeric feature records a unit, derivation, and calibration flag where applicable. Missing major-structure distance remains JSON `null`. Brightness never becomes significance.

## 6. Provisional hierarchical grouping

The detector emits image regions; grouping emits candidate representations. These are not confirmed entities.

| Candidate label | Bounded inference basis |
|---|---|
| `primary_extended_object` | Largest segmented extended image region, not system centrality |
| `internal_substructure` | High-threshold core inside an extended segmentation |
| `likely_foreground_point_source` | Compact high-peak morphology; depth unavailable and confidence capped |
| `possible_companion_object` | Separate extended region near the major region in image pixels; physical association not established |
| `background_extended_object` | Separate extended morphology; background depth not established |
| `unresolved_background_object_candidate` | Unresolved morphology with explicitly hypothetical depth label |
| `diffuse_or_uncertain_region` | Low-contrast extended segmentation retained without identity |
| `dark_or_occluding_region` | Local intensity deficit with alternative explanations retained |
| `unknown_image_region` | Evidence does not support a narrower bounded label or contamination is possible |

Hypothesis confidence cannot exceed `maximum_hypothesis_confidence`, default 0.45.

## 7. Relationship construction

Each candidate has an `observational` / `observational_dependency` edge to the source. Candidate pairs may receive these canonical-type/subtype combinations:

- `spatial` / `proximity` from centroid separation under a parameterized image-space radius;
- `spatial` / `overlap` from axis-aligned bounding-box intersection over union;
- `containment` / `containment` from at least 90% bounding-box containment;
- `spatial` / `orientation_alignment` from elongated components with major-axis angles within tolerance;
- `structural` / `morphological_association` from shared provisional morphology and image proximity;
- `occlusion` / `occlusion` as a low-confidence hypothesis when a dark deficit overlaps luminous structure;
- `structural` / `shared_structural_region` as a hypothesis when a centroid lies inside the major-region bounding box.

Every edge includes source and target nodes, explicit roles and directionality, taxonomy and subtype, image-pixel coordinate space, explicit unavailable epoch/band/observer states, status, a relationship-specific strength measurement, separate structured uncalibrated confidence and uncertainty, lifecycle, provenance, explicit inference basis, and one or more evidence IDs. `physical_claim` is always `false` and cross-record validation rejects forbidden physical relation types.

## 8. Outputs

| Artefact | Purpose |
|---|---|
| `graph.json` | Canonical typed nodes and edges, schema validated |
| `provenance.json` | Complete observation/evidence/detection/transformation/assertion trace |
| `manifest.json` | Run and software identity plus path, role, media type, bytes, and SHA-256 for generated artefacts |
| `summary.md` | Human-readable candidates, assertions, and limitations |
| `graph.graphml` | Optional exchange representation emitted by default |
| `overlay.png` | Diagnostic bounding boxes and identifiers; not a scientific annotation product |
| `source/…` | Content-addressed source and optional metadata copies |

The manifest does not hash itself because that would be recursively defined; the exclusion is explicit.

## 9. Parameters

Defaults are declared in the frozen `DetectionParameters` model and reproduced in `examples/parameters.json`. Unknown parameter names are rejected.

| Parameter | Default | Effect |
|---|---:|---|
| `bright_sigma` | 2.5 | Robust bright threshold scale |
| `bright_min_delta` | 18 | Minimum encoded-luminance bright contrast |
| `core_sigma` | 5.0 | Robust high/core threshold scale |
| `core_min_delta` | 42 | Minimum encoded-luminance core contrast |
| `dark_local_delta` | 16 | Local dark-deficit threshold |
| `background_blur_radius` | 5.0 | Gaussian local-background radius in pixels |
| `min_component_pixels` | 3 | Minimum luminous region area |
| `dark_min_component_pixels` | 4 | Minimum dark-deficit area |
| `point_max_pixels` | 24 | Maximum point-like segmentation area |
| `extended_min_pixels` | 45 | Minimum extended segmentation area |
| `diffuse_min_pixels` | 80 | Minimum diffuse candidate area |
| `proximity_radius_pixels` | 16.0 | Base relationship radius |
| `local_density_radius_pixels` | 24.0 | Feature-density radius |
| `orientation_alignment_degrees` | 15.0 | Image-plane orientation tolerance |
| `diffraction_elongation_min` | 5.0 | Thin-component warning threshold |
| `diffraction_fill_ratio_max` | 0.45 | Low-fill warning threshold |
| `foreground_peak_min` | 220 | Encoded peak required for foreground-point hypothesis |
| `maximum_hypothesis_confidence` | 0.45 | Confidence cap for identity/depth/association hypotheses |
| `maximum_components_per_pass` | 128 | Bounded work and output size per segmentation pass |

These defaults are engineering heuristics for a proof of concept, not astronomical calibration constants.

## 10. Determinism and audit trail

For identical input bytes, declared metadata, parameters, Python, Pillow, and pipeline versions:

- IDs are canonical-JSON SHA-256 derivations;
- component traversal and output ordering are stable;
- no current timestamp or absolute output path enters graph content;
- the source copy is byte-identical;
- every JSON output is key-sorted;
- the integration test compares every output file byte-for-byte across two runs.

An auditor can follow a graph edge’s evidence IDs to evidence measurements, then to the provenance record, run parameters, software versions, and source SHA-256. Each derived ontology record also carries schema version, ontology version, epistemic classification, lifecycle state, and a provenance link. This trace does not require conversational memory.

## 11. Tests, validation, and falsification criteria

Run:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

The suite validates all schemas, stable identifiers, parameter rejection, extended/dark/contamination segmentation paths, feature presence, orientation relationships, immutable source hashing, manifest source copies, edge evidence, absence of physical claims, uncalibrated pixel distance, overwrite refusal, and byte-equivalent reruns.

This component fails its bounded contract if any of these occur:

- source bytes change;
- a copied input hash differs;
- a detection, candidate, or edge cites missing evidence;
- graph or source hashes disagree;
- a physical relationship type or `physical_claim: true` appears;
- pixel distance is marked calibrated without an implemented calibration transformation;
- a point-like bright candidate becomes system-central;
- relationship strength is collapsed into confidence;
- unknown parameters are silently accepted;
- reruns in the recorded environment differ byte-for-byte;
- outputs overwrite an existing path.

## 12. Failure modes and scientific limitations

- Generic thresholding is sensitive to background gradients, saturation, compression, colour mapping, mosaics, masks, point-spread functions, and detector artefacts.
- Eight-connected segmentation can merge nearby sources or split one structure at a dark lane.
- Axis-aligned bounding boxes overstate irregular-region overlap and containment.
- Local Gaussian deficits can confuse real absorption, processing artefacts, image edges, and colour-map effects.
- The foreground/background and companion labels cannot be depth-confirmed from one image and remain hypotheses.
- Orientation estimates are unstable for near-circular or tiny components.
- Confidence values are structured, bounded, explicitly `uncalibrated` heuristic support scores, not catalogue-calibrated probabilities.
- Trusted execution time is recorded as `unavailable` rather than introducing a nondeterministic local clock value; a future run-authority contract must decide deterministic time capture.
- Encoded RGB may be nonlinear, composite, stretched, or non-photometric.
- A synthetic fixture establishes software invariants only, not detection completeness, purity, or scientific accuracy.
- The source decoder currently records but does not apply EXIF orientation or astronomy-specific FITS calibration.
- Schema discovery currently assumes a source checkout; wheel packaging is not yet an integration target.
- Large images use Python lists and flood-fill components and may be slow or memory-heavy.

## 13. Future external catalogue augmentation

An external catalogue may later augment—but must not rewrite—the observation graph. A future integration should:

1. identify catalogue name, release/version, query, licence, access time, and record checksum;
2. keep catalogue evidence records separate from image-derived evidence;
3. express cross-matches as assertions with angular uncertainty and competing candidates;
4. retain unavailable, contested, and non-matches explicitly;
5. require calibration metadata before pixel-to-sky or physical conversion;
6. preserve catalogue claims as externally sourced, not image-observed facts;
7. version any ASA dependency explicitly without copying ASA constitutional material;
8. validate against declared scientific ground truth separately from synthetic software tests.

No catalogue is selected by this manufacturing unit.

## 14. Unresolved programme decisions

- approved illustrative astronomical input, licence, and checksum;
- versioned ASA dependency and import boundary;
- scientific catalogue/ground-truth source and acceptable comparison tolerances;
- calibration and FITS support requirements;
- downstream Codex C relationship normalisation, standing, and significance contract;
- ownership/register reconciliation for the direct Codex B assignment against open `DR-0002`;
- whether GraphML is retained as a permanent integration format;
- packaging requirements beyond source-checkout execution.

## 15. Final review answer

**For this bounded pipeline: yes.** Every emitted candidate-graph assertion can be followed to evidence IDs, pixel measurements, a provenance record, the complete parameter set, software versions, processing-run ID, and immutable source hash without relying on conversational memory.

That answer is an auditability result for the software contract and synthetic fixture. It is not evidence that the candidate classifications or relationships are astronomically correct, and it does not declare ASA or ASA-Astro validated.
