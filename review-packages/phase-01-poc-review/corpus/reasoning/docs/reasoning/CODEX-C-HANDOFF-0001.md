# CODEX-C-HANDOFF-0001 — Standing and Significance Computation

Status: manufactured proof-of-concept; not ratified and not scientifically validated

Starting canonical commit: `e3476fc01b3743a320af580d9054fa1e8cfddc6f`

## Delivered boundary

Codex C consumes the Codex B `graph.json` and companion `provenance.json`; it does not perform detection or change those inputs. It emits context-independent Standing records, Context-bound Significance records, separate Explanation Traces, ranked results, five baselines, and bounded counterfactual comparisons.

The public Python entry points are:

```python
from asa_astro.reasoning import analyze, analyze_counterfactual
```

The local CLI is:

```bash
PYTHONPATH=src python3 -m asa_astro.reasoning.cli \
  --graph GRAPH.json --provenance PROVENANCE.json \
  --context CONTEXT.json --output NEW_DIRECTORY
```

`--counterfactual INTERVENTION.json` accepts one of:

- `{"kind":"remove_node","node_id":"..."}`;
- `{"kind":"weaken_edge","edge_id":"...","factor":0.5}`;
- `{"kind":"drop_observational_confidence","node_id":"...","factor":0.5}`;
- `{"kind":"change_context","context":{...}}`.

The CLI refuses overwrite. Its manifest binds the graph hash, Context hash, algorithm version, and artifact hashes.

## Contracts consumed

- `ASTRO-ONTOLOGY-0001` for entity/representation, epistemic, lifecycle, evidence, confidence, uncertainty, provenance, Standing and Significance boundaries;
- `ASTRO-RELATIONSHIP-TAXONOMY-0001` for admitted Relationship Types and the strength/confidence distinction;
- `ASTRO-CONTEXT-MODEL-0001` for explicit Context identity, scope and eligibility;
- `ASTRO-VALIDATION-FRAMEWORK-0001` for provenance, uncertainty and falsification posture;
- Codex B Candidate Entity, graph, Relationship Assertion, Evidence Record, detection, confidence, uncertainty and provenance contracts.

The engine rejects unsupported physical claims and never treats image-space relationships as physical relationships. Candidate class and encoded brightness are excluded from core Standing and Significance. Candidate class is used only by the isolated manual-priority comparator.

## Produced contracts

- `schemas/reasoning/context.schema.json` — externally supplied Context configuration;
- `standing-result.schema.json` — Context-free computed Standing record;
- `significance-result.schema.json` — graph- and Context-bound result;
- `explanation-trace.schema.json` — decomposed reasoning trace.

All records use schema `0.1.0`, ontology `ASTRO-ONTOLOGY-0001`, taxonomy `ASTRO-RELATIONSHIP-TAXONOMY-0001`, and algorithm `asa-astro-reasoning-poc-0.1.0`.

## Provisional decisions

No constitutional decision was closed. The component weights, assertion-class factors, persistence factors, lifecycle factors, uncertainty mapping, normalization behavior, direct-neighbour mix, and propagation equation are replaceable hypotheses documented in `ASTRO-SIGNIFICANCE-MODEL-0001`. Results explicitly record `asa_dependency_status=unavailable_not_consumed`.

## Integration requirements for Codex D

Codex D can run the full repository suite and validate the CLI against a fresh Codex B bundle. It should verify:

1. graph/provenance/result hashes and all cited IDs resolve;
2. Context changes do not change Standing records;
3. no result is written into a Candidate Entity;
4. brightness, degree, centrality, centre distance, and class priority remain comparators only;
5. all top pathways are bounded by declared depth;
6. ASA conformance and scientific validity remain explicitly unclaimed.

Codex D-owned integration reports and governance files were inspected but intentionally left unchanged. Any formal integration finding belongs to Codex D or human authority.

## Known blockers and limitations

DR-0001, DR-0008, DR-0009, DR-0010, and DR-0012 remain open. The ASA dependency is unavailable. Codex B supplies uncalibrated single-image evidence with unavailable scientific ground truth. Current normalization is run-relative. Counterfactuals describe graph computation, not physical causality. Portability beyond the published graph contract has not been validated.

## Review answer

A reviewer can reproduce every implemented ranking from the versioned graph and provenance input, exact Context JSON, algorithm/policy versions, and Explanation Trace without conversational memory. That reproducibility is an engineering result only, not constitutional ratification or scientific validation.
