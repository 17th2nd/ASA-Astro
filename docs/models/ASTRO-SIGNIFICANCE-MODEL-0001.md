# ASTRO-SIGNIFICANCE-MODEL-0001 — Proof-of-Concept Computation Model

Status: provisional, non-canonical implementation hypothesis

Algorithm version: `asa-astro-reasoning-poc-0.1.0`

Schema version: `0.1.0`

Consumes: `ASTRO-ONTOLOGY-0001`, `ASTRO-RELATIONSHIP-TAXONOMY-0001`, `ASTRO-CONTEXT-MODEL-0001`, and Codex B candidate-graph/provenance schemas

Decision dependencies: DR-0001, DR-0008, DR-0009, DR-0010, DR-0012

## 1. Authority and scientific boundary

This document specifies a transparent ASA-Astro proof-of-concept. It does not define ASA, ratify Standing or Significance semantics, close a decision-register item, or claim scientific validation. The unavailable ASA dependency is explicitly recorded as `unavailable_not_consumed` in every result.

Codex B supplies image-space Candidate Entities and Relationship Assertions. They are representations supported by encoded image evidence, not confirmed astronomical objects or established gravitational, orbital, causal, evolutionary, or lineage relationships. The engine preserves that boundary. It neither promotes a B assertion nor uses a provisional candidate label in its core scoring functions.

All numeric values below are test hypotheses. They are versioned, replaceable configuration or algorithm constants and must be empirically challenged.

## 2. Terms

**Standing** is a context-independent, relatively persistent structural score computed for a Candidate Entity from the admitted graph, evidence support, confidence, persistence hypotheses, and uncertainty. It is a computed record, not an intrinsic entity property.

**Context** is an immutable-for-one-run, externally supplied configuration declaring an identifier, version, objective, eligible and excluded Relationship Types, weights, propagation policy, depth bound, uncertainty tolerance, normalization method, explanation requirements, and baseline policy. Its canonical JSON SHA-256 is carried by each Significance result.

**Significance** is a runtime score expressing relative relevance of a Candidate Entity to one declared Context and one graph version. It is never written into a Candidate Entity.

**Relationship vector** is the decomposed tuple

\[
R_e=(t_e,s_e,c_e,q_e,k_e,p_e,u_e)
\]

where \(t\) is the published Relationship Type, \(s\) relationship strength, \(c\) assertion confidence, \(q\) evidence quality, \(k\) assertion-class support factor, \(p\) persistence hypothesis, and \(u\) uncertainty burden. Strength and confidence remain distinct trace fields.

**Confidence** is bounded heuristic support for a proposition. It is not probability unless a future calibrated contract says otherwise. Codex B values remain labelled uncalibrated.

**Evidence quality** is the mean lifecycle- and uncertainty-adjusted support of cited Evidence Records. It preserves Evidence Record identifiers in the output.

**Persistence** is a provisional expectation that a relationship kind remains structurally relevant between computations. It is not measured astronomical duration.

**Influence** is the eigenvector-like component induced by supported neighbouring connectivity. **Dependency** is incident supported containment/structural reliance. **Information value** is the admitted quality of the node's supporting evidence, not novelty or scientific importance.

**Propagation** is bounded traversal of Context-eligible typed assertions. **Decay** is the Context factor reducing each added path step. **Normalization** maps scores within the current candidate set; therefore scores are relative to that run and cannot be compared across graphs without a separate calibration contract.

**Recursive effects** are neighbour contributions reached beyond depth one. They terminate at the Context `maximum_depth` (schema maximum eight), never revisit a node in one path, and therefore do not require an unbounded convergence claim.

**Uncertainty penalty** reduces a computed result according to explicit uncertainty state and Context tolerance. **Unsupported-inference penalty** is represented by the assertion-class factor and zero contribution from unavailable or inadmissible evidence; no unsupported physical edge may enter the engine.

## 3. Admission and rejection

The engine first validates the Codex B graph schema and then requires:

- graph and provenance processing-run identity;
- unique node and edge identifiers;
- resolvable detections, Evidence Records, and Provenance Records;
- bounded strength and confidence;
- taxonomy-recognized Relationship Types;
- `physical_claim=false` and no forbidden physical type;
- no intrinsic `standing` or `significance` candidate field;
- a schema-valid, provisional Context with disjoint eligible/excluded types and component weights summing to one.

Unknown, unavailable, contested, and uncalibrated states remain represented. Rejection is preferable to silent imputation.

## 4. Evidence-backed edge support

For evidence record \(j\), lifecycle factor \(l_j\) and uncertainty burden \(u_j\):

\[
q_e={1\over n}\sum_{j=1}^{n}l_j(1-0.5u_j)
\]

The supported edge weight is:

\[
w_e=s_ec_eq_ek_e
\]

Provisional assertion-class factors are `image_space_derived=0.70`, `hypothesis=0.35`, and `dependency=0.90`. Provisional persistence factors are `spatial=0.35`, `containment=0.75`, `structural=0.70`, `observational=0.95`, and `occlusion=0.40`. These values are hypotheses, not taxonomy definitions.

## 5. Standing formulation

Only Candidate Entity-to-Candidate Entity edges form Standing topology; the Observation Source does not become a structurally prestigious entity. Encoded brightness, pixel area, image-centre distance, candidate class, and active Context are excluded.

For node \(i\), eight raw components are computed and max-normalized across the current candidate set:

1. typed degree: count of distinct incident Relationship Types;
2. weighted connectivity: \(\sum w_e\);
3. eigenvector-like influence: bounded power iteration over \(w_ep_e\), at most 64 iterations with tolerance \(10^{-12}\);
4. betweenness: deterministic Brandes centrality over supported topology;
5. containment hierarchy: supported incident containment weight;
6. relationship persistence: \(\sum w_ep_e\);
7. evidence support: candidate confidence times supporting-evidence quality;
8. structural dependency: supported structural and containment weight.

With normalized component \(z_{ik}\) and provisional weights

\[
\alpha=(.12,.18,.14,.12,.10,.10,.14,.10),\quad \sum_k\alpha_k=1,
\]

the pre-adjustment Standing is

\[
S_i^*=\sum_k\alpha_kz_{ik}.
\]

Candidate confidence \(c_i\), uncertainty burden \(u_i\), and provisional penalty weight \(\lambda=.35\) produce

\[
S_i=S_i^*c_i(1-\lambda u_i).
\]

Every \(z\), weight, contribution, adjustment, termination condition, and provenance reference is emitted. A reviewer can recompute the score without a hidden model.

## 6. Contextual Significance formulation

For Context \(C\), only eligible, non-excluded types contribute. Its relationship-type weight is \(r_C(t)\). A direct contribution from edge \(e:i\rightarrow j\) is

\[
d_{ie}=w_er_C(t_e)(0.5+0.5S_j).
\]

The constant half-weight permits an Observation Source dependency to contribute without assigning Standing to the source. It is provisional and explicitly traceable.

For a simple path \(P=(e_1,\ldots,e_m)\), \(2\le m\le D_C\):

\[
g_{iP}=S_{terminal(P)}\prod_{h=1}^{m}\left[w_{e_h}r_C(t_{e_h})\delta_C^h\right].
\]

Traversal is cycle-free per path and bounded by \(D_C\). Direct totals \(D_i\), propagated totals \(G_i\), and evidence information \(I_i\) are normalized using the declared method. With Context component weights \(\beta\), summing to one:

\[
Q_i^*=\beta_SS_i+\beta_DD_i+\beta_GG_i+\beta_II_i.
\]

With Context uncertainty tolerance \(\tau_C\):

\[
Q_i=Q_i^*c_i[1-u_i(1-\tau_C)].
\]

`Q` is a relative proof-of-concept score, not a probability. Ties are resolved by stable subject identifier. Context changes may change `Q` and rank; they cannot change Standing.

## 7. Explanation Trace

Each result points to a separate trace containing the complete Context, final score, Standing result and contribution, every eligible direct edge contribution, all bounded propagated paths, confidence adjustment, uncertainty penalty, excluded evidence and reason, warnings, top pathways, and provenance references. The result additionally carries graph hash, companion provenance-bundle hash, Context hash, algorithm version, schema/ontology/taxonomy versions, and dependency status.

## 8. Baselines

The engine emits comparators that never feed Significance:

- encoded peak intensity (called `brightness`, explicitly not luminosity);
- candidate-candidate node degree;
- eigenvector-like centrality;
- inverse normalized pixel distance to image centre;
- manually supplied candidate-class priority from the Context.

The manual baseline is the only class-aware calculation. It is isolated precisely because Codex B candidate labels are provisional. Different ranking orders falsify equivalence to these baselines; matching orders in one graph do not establish equivalence.

## 9. Counterfactuals

The bounded interface supports candidate removal, edge-strength weakening, candidate confidence reduction, and complete Context replacement. It returns before/after score and rank deltas while retaining both full analyses. It does not claim real-world causal effect: these are computational interventions on a representation.

## 10. Synthetic scenarios and falsification criteria

The deterministic Codex B synthetic observation fixture plus controlled mutations tests:

- A — a bright, provisionally foreground point-like region must not be ranked by brightness alone;
- B — a dimmer structurally supported candidate can outrank a brighter weakly connected candidate;
- C — a bridge candidate receives a decomposed betweenness term;
- D — reducing confidence or marking uncertainty contested lowers a highly connected candidate;
- E — structural, observational, and star-formation-question Contexts preserve Standing but can change Significance ranks;
- F — a spatial proximity assertion reduced to confidence `0.001` contributes less than `0.001` and cannot dominate merely by proximity.

Tests also require byte-equivalent repeated computation, bounded propagation, resolvable provenance, malformed input rejection, complete traces, counterfactual deltas, and CLI overwrite refusal. A failure of any criterion falsifies this implementation unit. Scientific validation still requires independent ground truth and human resolution of the open decisions.

## 11. Reproduction

Given Codex B `graph.json`, companion `provenance.json`, and a versioned Context:

```bash
PYTHONPATH=src python3 -m asa_astro.reasoning.cli \
  --graph path/to/graph.json \
  --provenance path/to/provenance.json \
  --context tests/fixtures/reasoning/structural-context.json \
  --output path/to/new-reasoning-output
```

The CLI refuses an existing output directory and emits the complete analysis, separate results/traces/baselines, the exact Context, and a content-hash manifest.

## 12. Known limitations and reserved authority

- No published, versioned ASA dependency is available; ASA conformance is not tested or claimed.
- Standing, Significance, Context policy, and propagation semantics remain reserved under DR-0009, DR-0010, DR-0008, and DR-0012.
- Codex B evidence is a single illustrative, uncalibrated image-space source with unavailable scientific ground truth.
- Max normalization makes results graph-relative and sensitive to candidate-set changes.
- Centrality and betweenness are demonstration measures, not proof that these measures belong in ASA Standing.
- Counterfactuals operate on graph representation only and must not be read as astronomical causality.
- Portability outside this input contract has not been demonstrated.

The final review question is satisfied computationally: every ranking is reproducible from the versioned graph/provenance bundle, immutable Context content, algorithm version, provisional policy, and Explanation Trace. It is not yet satisfied as an ASA constitutional or scientific validation claim.
