# Codex B Observation-to-Graph Handoff 0001

**Interface version:** 0.1.0
**Operator:** Codex B — Observation, Evidence, and Graph-Construction Manufacturer
**Status:** Proof-of-concept handoff; not ratified and not scientific validation
**Authority effect:** None beyond the supplied Codex B manufacturing directive

## 1. Owned manufacturing scope

The operator directive assigns Codex B the path from replaceable image input through provenance-preserving candidate graph output. It explicitly excludes final standing and significance computation.

Files manufactured by Codex B in this unit are:

- `.gitignore`
- `README.md`
- `pyproject.toml`
- `requirements.lock`
- `examples/parameters.json`
- `schemas/**/*.schema.json`
- `src/asa_astro/evidence/**` plus the thin `src/asa_astro/cli.py` entry point
- `tests/**`
- `docs/pipeline/OBSERVATION-TO-GRAPH-PIPELINE-0001.md`
- `docs/pipeline/CODEX-B-HANDOFF-0001.md`
- `docs/reports/CODEX-B-MANUFACTURING-REPORT-0001.md`

The root configuration files are shared integration surfaces manufactured because the empty repository had no executable environment. Their presence does not allocate future constitutional ownership. Codex B did not modify Codex D’s files under `docs/integration/`, `governance/`, or `reports/`.

## 2. Input contract

The executable accepts:

1. one readable image file;
2. a new output-directory path that does not already exist;
3. optional declared JSON metadata;
4. optional explicit detector parameters;
5. an optional stable source locator.

Input bytes are hashed before processing and copied under their SHA-256 name into the output bundle. The input and metadata paths are never opened for writing. Separate Observation Source, Observation, decoded Detector Output, Light Region/detection, Evidence, and Candidate records prevent representation/entity collapse. Calibration and physical scale default to `unavailable` and do not become available merely because metadata is present.

## 3. Output contract

| Path | Interface role |
|---|---|
| `graph.json` | Canonical schema-validated candidate graph for downstream consumers such as Codex C |
| `provenance.json` | Observation, image metadata, detections, evidence, transformations, software, parameters, and relationship assertions |
| `manifest.json` | Run ID and SHA-256/size/media type for every generated artefact except the self-referential manifest digest |
| `summary.md` | Human-readable bounded interpretation of graph content |
| `graph.graphml` | Exchange representation of the same nodes and assertions |
| `overlay.png` | Diagnostic image-space bounding boxes and stable candidate ordering |
| `source/<sha256>.<ext>` | Byte-identical content-addressed source copy |
| `source/metadata-<sha256>.json` | Optional byte-identical declared metadata copy |

Output records carry schema version `0.1.0`. Processing run IDs and record IDs are deterministic hashes of declared inputs. No wall-clock time is embedded in deterministic output.

## 4. Downstream invariants

Consumers may rely on these tested invariants:

- each detection resolves to one evidence record and one decoded Detector Output;
- each candidate cites detection and evidence identifiers;
- each graph edge cites resolvable evidence;
- each edge sets `physical_claim` to `false`;
- relationship strength and relationship confidence are distinct fields with distinct derivations;
- confidence is a structured `uncalibrated` heuristic support score, never an implied probability;
- ontology version, schema version, epistemic classification, lifecycle state, and provenance link accompany every derived ontology record;
- all reported geometry and distance use image pixels;
- encoded pixel intensity is explicitly uncalibrated;
- no field represents standing or significance;
- no candidate is classified as system-central from brightness;
- pre-existing output paths are not overwritten;
- identical input bytes, metadata, parameters, Python, and Pillow versions yield byte-equivalent bundles.

## 5. Provisional semantics

Candidate labels are bounded representations of image morphology. `likely_foreground_point_source`, `possible_companion_object`, `background_extended_object`, and `unresolved_background_object_candidate` are hypotheses with capped confidence, not depth measurements or object identities. `primary_extended_object` means only the largest segmented extended image region in the run; it is not a dynamical or significance centre.

Canonical relationship types are limited to the applicable `spatial`, `containment`, `structural`, `observational`, and `occlusion` entries from `ASTRO-RELATIONSHIP-TAXONOMY-0001`. Each also carries one candidate-graph subtype from `proximity`, `overlap`, `containment`, `orientation_alignment`, `morphological_association`, `occlusion`, `shared_structural_region`, or `observational_dependency`. `occlusion`, morphological association, and shared-region assertions remain hypotheses. No physical relationship vocabulary is accepted.

## 6. Validation command

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

The synthetic fixture is generated from repository code and is not astronomical ground truth. An approved astronomical input, ASA dependency version, and external ground-truth source remain programme-level integration requirements.
