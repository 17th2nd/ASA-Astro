# ASA-Astro

ASA-Astro is a bounded astronomy validation domain for Adaptive Significance Architecture (ASA). This repository does not redefine ASA, contain ASA constitutional material, or claim that a single image supplies astronomical ground truth.

The first executable component is Codex B’s deterministic observation-to-candidate-graph pipeline. It registers an image without overwriting it, records source and processing provenance, detects provisional image regions, and emits evidence-backed image-space graph inputs. It does **not** compute standing or significance and does not assert astronomical identity, physical distance, gravity, orbit, cause, or evolution.

## Quick start

Requirements: CPython 3.12 and the exact packages in `requirements.lock`.

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.lock
.venv/bin/pip install --no-deps -e .
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v
```

Generate the synthetic regression fixture and process it:

```bash
PYTHONPATH=src python3 tests/fixtures/generate_fixture.py /tmp/asa-astro-synthetic.ppm
PYTHONPATH=src python3 -m asa_astro.cli \
  /tmp/asa-astro-synthetic.ppm \
  --metadata tests/fixtures/synthetic_observation.metadata.json \
  --parameters examples/parameters.json \
  --source-locator fixture:synthetic-observation-v1 \
  --output /tmp/asa-astro-run
```

The output directory must not exist. A successful run produces a content-addressed source copy, canonical JSON graph, provenance bundle, processing manifest, Markdown summary, GraphML exchange graph, and diagnostic PNG overlay.

## Permanent documentation

- Pipeline contract and scientific limits: `docs/pipeline/OBSERVATION-TO-GRAPH-PIPELINE-0001.md`
- Codex B integration handoff: `docs/pipeline/CODEX-B-HANDOFF-0001.md`
- Machine-readable contracts: `schemas/`
- Manufacturing report: `docs/reports/CODEX-B-MANUFACTURING-REPORT-0001.md`

No repository artefact declares ASA or ASA-Astro scientifically validated.
