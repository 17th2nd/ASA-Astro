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

## Astro — Astronomy Execution Engine on ASA (CLAUDE-ASTRO-BUILD-001)

`src/astro/` is the Astro execution engine: a proving implementation of ASA on astronomy workloads.
Astro owns astronomy (entities, evidence, relationships, objectives, planning, scheduling, execution,
receipts); ASA — consumed at the pinned baseline in `config/asa-baseline.json` — owns identity,
relationship admission, provenance and replay. Significance is a **derived construct** computed by
Astro over ASA relational state under a declared Objective; it is never stored on an entity.

```bash
ASTRO_ASA_SOURCE=/path/to/ASA/clone python3 tools/asa_baseline.py   # materialise the pinned ASA kernel under .asa/ (omit the env var to clone from GitHub)
.venv/bin/pip install --no-deps -e .
astro version
astro demo context-switch      # one universe, four objectives, four different selections; universe and ASA state unchanged
astro demo evidence-arrival    # same objective, new evidence, different plan
astro evaluate --universe data/universe/slice1.json --objective data/objectives/A-exoplanet-transit-followup.json \
               --context data/contexts/night-2026-09-03.json --out /tmp/astro-run
astro explain --out /tmp/astro-run --universe data/universe/slice1.json --entity SYN-HOST-A
PYTHONPATH=src python3 -m unittest discover -s tests/astro -t .
```

Layout: `astro.domain` (entities, evidence, relationships, state, immutable Universe) · `astro.objectives`
(Objective, ObservingContext) · `astro.asa` (pinned-baseline locator, AstroAdapter, RelationalSnapshot) ·
`astro.significance` (feature library, evaluator, explanation) · `astro.execution` (plan, schedule,
simulated executor) · `astro.session` (evaluate → plan → schedule → execute → evidence → re-evaluate) ·
`astro.receipts` (AstroDecisionReceipt) · `registry/` (Astro relationship-type facet, validated by ASA) ·
`data/` (synthetic slice-1 universe, objectives, contexts — all labelled) · `temp/` (operator reports;
`temp/astro-asa-integration.md` records what Astro consumes from ASA and what it asks of it).

### Real catalogues and the persistent store

`astro catalogues fetch` pulls public catalogues into `data/catalogues/raw/` (gitignored; digests, retrieval time,
release, licence and citation recorded in `data/catalogues/manifest.json`): NASA Exoplanet Archive composite
parameters, Gaia DR3 for every host star, GCVS 5.1, OpenNGC (CC-BY-SA-4.0), Hunt & Reffert 2023 clusters, IAU MPC
observatory codes, ALeRCE ZTF supernova candidates. `astro store build --store var/astro-store --universe-out
var/universe-real.json` merges them by identity into one universe labelled `real` and loads it into a persistent
ASA kernel (≈95k entities, ≈103k evidence records, ≈870k events; `BUILD.json` is the receipt).
`astro evaluate … --store var/astro-store --universe var/universe-real.json --context data/contexts/siding-spring-2026-09-03.json`
then answers, for example, which known transiting planets transit tonight from Siding Spring.

### Knowledge frontier

`astro store build --frontier --as-of <UTC>` also derives what the store does *not* know and writes it into ASA:
missing expected evidence as `lacks-evidence` relationships (retired when evidence arrives), measurement claims as
`measures` relationships with `asa.core/contradicts` between disagreeing catalogues, geometry-derived `near`,
`member_of` and `hosted_transient` relationships (evidenced) and comparison-star candidates (deliberately
unevaluated), and 648 sky tiles with coverage gaps. `astro frontier --store … --universe …` summarises blank spaces,
semantic edges and disputes; objectives E (knowledge-gap reduction) and F (dispute adjudication) rank them.
`astro.catalogues.tess` fetches TESS light curves from MAST as `time_series` evidence.

Checks added 2026-09-04 after the first candidate findings were taken to the literature: cluster membership is
endorsed only when host and cluster proper motions agree to 3 km/s tangential velocity and the host's Gaia RUWE is
≤ 1.4 (position and parallax alone admitted GPX-1/Trumpler 2, which its discovery paper had already ruled out on
proper motion; 41 of 244 associations survive, and they are the known ones); `ephemeris_drift` treats a tabulated
period error above 1% of the period as an undetermined period, not drift. `tools/candidate_findings.py` reproduces
both candidate lists with these checks; `tools/cut_universe.py` cuts a cone of the real universe so the §18 benchmark
(`astro benchmark`, now with independent oracles for objectives E and F and a graded gain column) can run on real data.
Every universe load — store build, session cycle, benchmark bootstrap — records contradictions between registered
claims and retires a lacks-evidence gap whose evidence has arrived.

### Navigator and the debug scope

`astro ui --universe … --objective … --context … --findings … --out var/ui/astro-navigator.html` builds one
self-contained page (D3 from cdnjs, data embedded): a zoomable sky map sized by score under the chosen objective,
a relationship graph you travel through by clicking (edges styled by ASA stance: endorsed, unevaluated, retired,
contradicts; missing evidence and disputed claims drawn as ghost nodes), and a detail pane with feature
contributions, evidence, claims and candidate-finding verdicts. The debug scope is the solar neighbourhood,
`tools/cut_universe.py … --max-distance-pc 50` (Gaia parallax or catalogue distance): every object there has a
literature answer and Gaia is clean, so an Astro verdict can be checked in minutes.

All Astro data committed in this repository is **synthetic or simulated and labelled as such**; real catalogue rows are fetched, never committed, and every real record carries its source and licence. Nothing in Astro
touches the frozen scientific instruments below or claims empirical validation of ASA.

## Canonical programme state

| Instrument | State |
|---|---|
| `ASTRO-THEORY-0001` Part A | **Version 1 Deterministic Core — Frozen** |
| `ASTRO-THEORY-0001` Part B | **Candidate Enrichments — Not Frozen** |
| `ASTRO-EXP-0001` | Frozen, **not executed** |
| `ASTRO-CLAIMS-0001` | Frozen |
| `ASTRO-RESULTS-0001` | Frozen, evidence level `EH-0` |
| Empirical validation | **Not commenced** |

The Version 1 theory freeze records verification of a formal mathematical object. It claims no empirical validation, no novelty, and no proof of any Part B enrichment. Freeze record: `docs/theory/ASTRO-THEORY-0001-V1-FREEZE-RECORD.md`.

## Permanent documentation

- Canonical minimum validation protocol: `validation/benchmarks/ASTRO-EXP-0001.md`
- Canonical scientific claims register: `docs/claims/ASTRO-CLAIMS-0001.md`
- Permanent empirical results ledger: `validation/results/ASTRO-RESULTS-0001.md`
- Pipeline contract and scientific limits: `docs/pipeline/OBSERVATION-TO-GRAPH-PIPELINE-0001.md`
- Codex B integration handoff: `docs/pipeline/CODEX-B-HANDOFF-0001.md`
- Machine-readable contracts: `schemas/`
- Manufacturing report: `docs/reports/CODEX-B-MANUFACTURING-REPORT-0001.md`

No repository artefact declares ASA or ASA-Astro scientifically validated.
