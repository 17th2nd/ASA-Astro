# ASTRO-RESEARCH-0001 — Scientific Foundation for the Astronomy Validation Programme

**Programme:** Adaptive Significance Architecture — Astronomy Validation Programme, Research Programme 001
**Author cell:** Claude (Principal Research Scientist role)
**Date:** 2026-08-01
**Status:** DRAFT — working document in `09_Drafts/`. No architectural authority. Not a validation result. Not a ratified ASA or ASA-Astro record.
**Repository:** ASA-Astro (sole repository for this concept)
**Depends on (read, not amended):** `ASA-ASTRO-0001`, `ASTRO-ONTOLOGY-0001`, `ASTRO-RELATIONSHIP-TAXONOMY-0001`, `ASTRO-CONTEXT-MODEL-0001`, `ASTRO-SIGNIFICANCE-MODEL-0001`, `ASTRO-VALIDATION-FRAMEWORK-0001`, `governance/decision-register.md`, `reports/ASA-ASTRO-POC-VALIDATION-REPORT-0001.md`

---

## Evidence classification used throughout

Every substantive claim in this report carries one of the following tags. They are never blurred.

| Tag | Meaning |
|---|---|
| **[ESTABLISHED]** | Established science or mathematics. Textbook or settled literature. |
| **[STRONG]** | Strong evidence. Well supported by multiple independent lines, but not settled. |
| **[HYPOTHESIS]** | Reasonable hypothesis. Coherent, testable, not yet tested here. |
| **[SPECULATION]** | Speculation. Plausible but without current evidentiary support. |
| **[UNKNOWN]** | Unknown. Cannot currently be resolved with available information. |

Where a claim is about ASA rather than about astronomy, the tag describes the epistemic status of the claim *about ASA*, not an endorsement of ASA.

---

# 1. Executive Summary

## 1.1 What was asked

Determine whether significance-first intelligence can be scientifically validated using astronomy; produce the scientific foundation for doing so; and answer, without vagueness, whether the proposed architecture actually differs from existing scientific and computational approaches.

## 1.2 The headline answers

**A. Can it be validated using astronomy? Partially, and only if "significance" is operationalised into measurable quantities.** [HYPOTHESIS]

Astronomy can supply rigorous, independent, versioned ground truth for the *lower* layers of the ASA pipeline — evidence, entity identification, relationship identification, relationship graph. It cannot supply a catalogue of "significance", because no such catalogue exists and no observation measures significance directly. The programme is therefore validatable only if significance is redefined as an *observable consequence* under a declared context. Section 9 identifies four such operationalisations, of which one — **counterfactual perturbation significance in solar-system dynamics** — provides exact, quantitative, non-circular, context-parameterised ground truth. That single reduction is, in my assessment, the difference between a validatable programme and an unfalsifiable one.

**B. Does the architecture differ from existing approaches? Not at the level of operations. Possibly at the level of constraints.** [STRONG]

Every computational layer ASA proposes already exists in mature form:

| ASA layer | Existing equivalent |
|---|---|
| Observation → Evidence | W3C PROV, IVOA ObsCore/Provenance DM, FITS/WCS metadata chains |
| Entity identification | Probabilistic record linkage (Fellegi–Sunter); Bayesian astronomical cross-identification (Budavári & Szalay 2008) |
| Relationship identification | Knowledge graphs, RDF/OWL, heterogeneous information networks |
| Relationship graph | Typed multi-relational graphs; property graphs; probabilistic/uncertain graphs |
| Standing | Eigenvector centrality, PageRank, HITS, Katz, betweenness; TrustRank; evidence-weighted centrality on uncertain graphs |
| Context | Topic-sensitive / personalised PageRank (Haveliwala 2002); random walk with restart; query-conditional ranking; metapath-based relevance (PathSim/HeteSim) |
| Dynamic significance | Decision-theoretic value of information (Howard 1966); Bayesian experimental design (Lindley 1956); learning-to-rank |
| Reasoning after significance | Attention mechanisms; focus-of-attention in expert systems; relevance-first retrieval-augmented inference |

**No individual ASA layer is novel.** Any claim that it is will not survive contact with a literature review. This must be stated plainly in every external-facing document, or the programme will lose credibility on first expert reading.

What is *not* obviously precedented is the **conjunction of prohibitions**: (i) reasoning may never feed back into significance; (ii) significance may never be stored as an entity attribute; (iii) path composition is forbidden per relationship type unless explicitly licensed with compatible units, frames, epochs and roles; (iv) abstention is a first-class output; (v) context must be frozen before evaluation. Items (i), (ii), (iv) and (v) have close analogues elsewhere (acyclic pipeline design, normalised data modelling, selective prediction, clinical-trial preregistration). Item (iii) — a *transitivity-gated typed path algebra with physical validity conditions* — is the one place where I could not find an existing equivalent. It is a modest novelty claim, and it is an engineering-discipline claim, not a mathematical one. Section 5.6 states it precisely.

**C. Two internal contradictions were found in the existing corpus.** [STRONG]

These are not stylistic objections. They are structural, and both must be resolved before any benchmark is meaningful.

1. **Standing reintroduces intrinsic significance.** `ASTRO-SIGNIFICANCE-MODEL-0001` §6 computes `Q_i* = β_S·S_i + β_D·D_i + β_G·G_i + β_I·I_i` with `S_i` context-independent. A context-independent additive term with positive weight is, by definition, a context-invariant component of significance attached to the entity. The primary hypothesis states "objects possess no intrinsic significance." The current model contradicts it. Section 6 gives the resolution: standing must be an **admissibility gate and evidential-support record**, not a scalar contributed to the significance sum.

2. **The standing formulation uses path-composition algorithms on a graph whose own taxonomy forbids path composition.** `ASTRO-SIGNIFICANCE-MODEL-0001` §5 includes eigenvector-like influence (power iteration) and Brandes betweenness over "supported topology." `ASTRO-RELATIONSHIP-TAXONOMY-0001` prohibits transitivity for 12 of its 17 types and permits it conditionally for the remaining 5. Eigenvector centrality and betweenness are *defined* by summation over paths; a path through a non-composable edge sequence has no semantics. The current standing score is therefore computing a quantity that the repository's own ontology says is meaningless. Section 7.4 gives the resolution.

**D. The primary hypothesis, as written, is not falsifiable.** [ESTABLISHED — as a matter of logic]

"Objects possess no intrinsic significance; significance emerges from evidence, relationships, standing and context" asserts that significance is a function of those four arguments. Every ranking system ever built satisfies that description. As stated, it is a definition, not a hypothesis, and cannot be tested. Section 8.2 supplies three sharpened forms that *are* falsifiable, of which the strongest is:

> **H1 (Context-Irreducibility).** There exists no single context-independent ranking function that matches context-specific reference rankings across a declared diverse context set, to within the accuracy achieved by a context-conditional function.

H1 is directly measurable: fit the best possible global ranking, measure its ceiling, compare. If a single global ranking matches every context's reference as well as a context-conditional one does, the architecture's central premise fails for that domain.

**E. The most likely falsification route is not exotic. It is a trivial physical baseline.** [STRONG]

For gravitational and dynamical contexts, `GM/r²` — a one-line formula with no graph, no standing, no context machinery — is an extremely strong predictor of which bodies matter. For radiative contexts, flux is similarly strong. If the ASA graph pipeline cannot beat these on their home turf, the correct conclusion is *no demonstrated added value*, and that outcome must be pre-accepted, not explained away. I estimate this is the single most probable experimental result. [HYPOTHESIS]

## 1.3 Recommendation

Proceed, with the scope reset described in Section 17. Specifically: abandon the single-illustrative-image path (which cannot produce ground truth for anything), adopt catalogue- and simulation-derived data, resolve DR-0004 in favour of the four ground-truth families in Section 9, and make Experiment E2 (counterfactual perturbation significance) the programme's first real test rather than its last. The programme's value is currently blocked not by implementation but by the absence of a measurable significance target.

---

# 2. Existing Scientific Landscape

## 2.1 Why astronomy was proposed, and where that reasoning holds

The proposal cites: objective observations, mature understanding, reproducible measurements, known relationships, independent ground truth, relational complexity, multi-scale structure, uncertainty, incompleteness, and independence from human language.

Assessment of each:

| Claimed property | Verdict | Notes |
|---|---|---|
| Objective observations | **Largely holds** [STRONG] | Photon counts, astrometric positions and timings are as observer-independent as empirical data gets. Calibration, however, is a modelled chain, not a raw fact. |
| Mature scientific understanding | **Holds** [ESTABLISHED] | Celestial mechanics, radiative transfer and stellar structure are among the best-tested theories in science. |
| Reproducible measurements | **Holds with caveats** [STRONG] | Archives are versioned and re-reducible. Re-reduction with a newer pipeline can change values materially; version pinning is mandatory, not optional. |
| Known relationships | **Holds** [ESTABLISHED] | Membership, orbit, containment and hierarchy have curated catalogue-level references. |
| Independent ground truth | **Holds for structure; fails for significance** [STRONG] | Central finding. See §9. |
| Enormous relational complexity | **Holds** [ESTABLISHED] | SIMBAD alone: ~19.5M objects, ~66M identifiers, ~44M object–paper citation links (Jan 2026). |
| Multi-scale structure | **Holds** [ESTABLISHED] | Satellite → planet → star → binary → cluster → galaxy → group → cluster → filament spans ~15 orders of magnitude in length. |
| Uncertainty | **Holds, and is exemplary** [ESTABLISHED] | Astronomy has unusually disciplined uncertainty reporting: covariances, posteriors, upper limits, quality flags. |
| Incomplete observations | **Holds — and is a hazard, not only an asset** [STRONG] | See §2.3. |
| **Independent of human language** | **Does not hold** [STRONG] | See §2.2. This claim should be withdrawn. |

## 2.2 The "no human language" claim is false and should be withdrawn

**[STRONG]** Astronomy reduces linguistic mediation; it does not eliminate it. Every element the programme would consume as ground truth is a linguistically and socially constituted artefact:

- SIMBAD object types are a curated taxonomy maintained by human editors reading papers. The classification `HII` versus `SFR` versus `Cl*` is a naming decision.
- "Open cluster membership" is not a physical predicate with a unique referent. Different published criteria (astrometric clustering, tidal-radius cuts, chemical tagging) select different member sets for the same cluster. A 2026 A&A study of the Gaia DR3 open-cluster census exists specifically because the census is method-dependent.
- "Galaxy", "group", "filament" are boundary conventions imposed on a continuous density field.
- The distinction between a "planet" and a "brown dwarf" is a definitional line drawn by committee.

The correct, defensible claim is: **astronomy allows the relational structure to be anchored in measurements whose acquisition is language-independent, while the entity and relationship *labels* remain human artefacts with declared provenance.** That is still a strong argument for astronomy. It is not the argument currently written down.

**Recommendation:** amend programme framing. Overclaiming here is exactly the kind of thing an expert reviewer will find in the first paragraph.

## 2.3 Selection functions: the largest scientific threat to the programme

**[ESTABLISHED]** Every astronomical catalogue is censored. Objects enter it only if they were bright enough, in the right part of the sky, observed at the right time, in the right band, and matched by the right algorithm. This censoring is not random; it is strongly correlated with exactly the quantities (brightness, proximity, size) that ASA insists must not be treated as significance.

The consequence for a graph architecture is severe and, as far as I can determine, unaddressed in the current corpus:

> **A centrality score computed on a censored graph measures the selection function as much as it measures the structure.** [ESTABLISHED]

A nearby bright star has more catalogue entries, more cross-identifications, more literature links, and more measured relationships than a distant faint one — not because it is more structurally central in the universe, but because it is easier to observe. Degree centrality on an astronomical knowledge graph is very close to a brightness proxy in disguise. This means the architecture's own prohibited confound (brightness) can enter through the graph topology while every explicit brightness feature is correctly excluded.

**This is the most important scientific risk in the programme.** It is not a data-quality nuisance; it is a mechanism by which the system can pass its own negative controls while still being a brightness ranker. Section 12.4 specifies the control required.

## 2.4 Astronomy is non-interventional, which limits causal validation

**[ESTABLISHED]** Astronomy is an observational science. We cannot perturb a galaxy and observe the result. The Pearl causal hierarchy's intervention rung is unavailable for real observations.

Consequences:

- The `causal` relationship type in `ASTRO-RELATIONSHIP-TAXONOMY-0001` §2.7 **cannot be validated against real astronomical ground truth**. There is no astronomical dataset in which causal edges are known to be true by intervention.
- The `developmental` type has the same problem: evolutionary sequences are inferred from population statistics across objects, not observed within an object.
- Simulations *do* permit intervention. In a cosmological or N-body simulation, one can rerun with a component removed. This makes simulation the only viable venue for causal-type validation. [STRONG]

**Recommendation:** either scope causal and developmental types out of the first validation programme, or validate them exclusively in simulation with the model-dependence explicitly declared. Do not attempt to validate causal claims against observational catalogues; the result would be uninterpretable.

## 2.5 What astronomy is genuinely excellent for

Stripped of overclaiming, astronomy remains a strong choice for four specific reasons: [STRONG]

1. **Exact counterfactual ground truth exists in one sub-domain.** Solar-system dynamics permits leave-one-out integration: remove a perturbing body, re-integrate, measure the change in a target's ephemeris. This yields a *measured, quantitative, context-dependent significance value* with no human judgement involved. Nothing comparable exists in most domains.
2. **Relationship types are physically distinguishable.** The difference between "gravitationally bound" and "projected nearby" is not a matter of opinion; it is decidable with parallax and kinematics. This makes false-relationship penalties meaningful.
3. **Uncertainty is natively reported.** ASA's demand for structured uncertainty is met by the data, not imposed on it.
4. **Context-dependence is already a lived practice.** Astronomers routinely say an object "matters for" one question and not another. Target-selection documents make this explicit and machine-readable.

## 2.6 Current state of the relevant data landscape (as of 2026-08)

| Source | Status | Relevance |
|---|---|---|
| **Gaia DR3** | Available since 2022 | Present workhorse: astrometry, photometry, non-single-star solutions, variability. |
| **Gaia DR4** | Scheduled 2 December 2026; first principal release; 5.5 yr time series, ~2.8 billion sources, ~142 billion detections, 130+ data products | Major. Epoch-level data enables temporal and orbital relationship work not previously possible. Do **not** build a benchmark that DR4 will invalidate in December; either freeze on DR3 explicitly or plan a DR4 refresh. |
| **Rubin / LSST** | LSST began 30 June 2026. Alerts streaming since Feb 2026 to nine community brokers. DR1 **cancelled**; first annual release (DRY1) now expected ~June 2028. DP2 released ~Jul/Aug 2026. | Alert-broker filters are the best available real-world analogue of ASA "context declarations". Not usable as a static catalogue benchmark before 2028. |
| **DESI DR1 / DR2** | DR1 released; DR2 spectra and redshifts not yet public (cosmology products only) as of the sources reviewed | Target-selection cartons (BGS/LRG/ELG/QSO) are declared, versioned relevance criteria — usable as context proxies. |
| **SDSS** | Mature, fully public through recent releases; SDSS-V ongoing | Group/cluster catalogues, Galaxy Zoo morphology labels. |
| **SIMBAD** | ~19.5M objects, ~66M identifiers, ~439k references, ~44M object–paper citations (Jan 2026) | The object–paper link table is a revealed-relevance corpus of exactly the kind the programme needs. |
| **NED** | Mature extragalactic equivalent | Cross-identification and redshift-independent distances. |
| **NASA ADS** | Mature | Literature graph; citation and co-mention structure. |
| **JPL SSD / Horizons, DE440/DE441** | Stable, public. DE440 integrates Sun, planetary barycentres, Moon, Pluto barycentre, **343 asteroids**, plus 30 KBOs and a KBO ring | **The key asset for E2.** The perturber-inclusion decision is itself a documented significance judgement with measurable consequences. |
| **Hunt & Reffert (2023) open cluster catalogue** | Public: 7,167 clusters, >700,000 member stars with membership probabilities, Gaia DR3-based | Best available membership ground truth with probabilistic labels. |
| **Minor Planet Center** | Public | Satellite systems, orbit classes, containment hierarchies. |
| **NASA Exoplanet Archive** | Public, versioned | Host–planet containment/orbital hierarchy with uncertainty. |
| **IllustrisTNG / EAGLE** | Public simulation data with merger trees | Full formation history known; supports causal and developmental validation and permits intervention. |

**Judgement:** the programme currently owns *zero* astronomical data (DR-0003 and DR-0004 both open; the POC validation report records "Astronomical image-derived data: None"). That is the actual blocker, and it is a data-acquisition problem, not an architecture problem.

---

# 3. Prior Art Review

This section exists to establish, before any novelty claim is made, exactly what already exists. It is deliberately unflattering.

## 3.1 Graph-structural ranking

**[ESTABLISHED]**

- **PageRank** (Brin & Page 1998): stationary distribution of a damped random walk. Context-free global prestige.
- **Personalised / Topic-Sensitive PageRank** (Haveliwala 2002): the teleport vector is biased toward a topic or seed set. **This is already "context-dependent significance over a graph".** It is the closest single prior art to ASA's significance layer and it is 24 years old.
- **Random Walk with Restart / Personalised relevance**: query-conditional node relevance, standard in recommendation and biological network analysis.
- **HITS** (Kleinberg 1999): dual hub/authority scores — a precedent for separating two kinds of structural standing.
- **Eigenvector, Katz, closeness, betweenness centrality**: classical.
- **TrustRank / anti-spam propagation**: seed-based trust propagation with provenance-like weighting — precedent for evidence-weighted standing.

**Implication for ASA:** the pair (standing = PageRank-like global score, significance = personalised PageRank with a context teleport vector) is a textbook construction. If ASA's significance layer reduces to this, it is not new. The programme must be able to state precisely what it does that personalised PageRank does not. My assessment of that answer is in §5.6.

## 3.2 Heterogeneous / typed networks

**[ESTABLISHED]**

- **Heterogeneous Information Networks** (Sun, Han et al.): typed nodes and edges with *metapaths* — declared type sequences along which similarity may be computed. **PathSim** and **HeteSim** compute relevance restricted to semantically meaningful metapaths.
- This directly anticipates ASA's core insight that untyped path traversal is meaningless. The metapath literature exists precisely because someone noticed that `author → paper → venue → paper → author` means something different from `author → paper → author`.
- **Knowledge graph embeddings** (TransE, RotatE, ComplEx) and confidence-aware variants (CKRL) handle typed relations with uncertainty.
- **RDF/OWL, SPARQL property paths**: typed graph query with formal semantics; OWL has property characteristics including `TransitiveProperty` — i.e., **per-relation transitivity declarations already exist as a W3C standard.**

**Implication for ASA:** the claim "we type our edges and restrict traversal by type" is prior art. OWL has had per-property transitivity flags since 2004. ASA's taxonomy is more physically detailed, but the *mechanism* is standard.

## 3.3 Uncertainty and probabilistic structure

**[ESTABLISHED]**

- **Bayesian networks / probabilistic graphical models** (Pearl, Koller & Friedman): joint distributions factorised over a DAG; exact and approximate inference; d-separation determines relevance.
- **Causal graphs / SCMs** (Pearl 2009; Spirtes, Glymour & Scheines): do-calculus, identifiability, confounding.
- **Uncertain / probabilistic graphs**: possible-worlds semantics, reliability, expected centrality.
- **Probabilistic databases** (Dalvi & Suciu): deferred resolution and query answering over uncertain tuples — precedent for ASA's "candidate entity that is never forced to resolve".
- **Probabilistic soft logic / Markov logic networks**: weighted first-order rules over relational data with uncertainty.

**Implication for ASA:** "represent unknown/contested/unavailable separately from zero" is standard in probabilistic databases and in three-valued and four-valued logics (Belnap 1977). ASA's uncertainty vocabulary (`unknown`, `unavailable`, `not_applicable`, `withheld`, `contested`, `estimated`, `bounded`) is a good engineering vocabulary but is not a new epistemology.

## 3.4 Decision theory and value of information

**[ESTABLISHED]**

- **Expected Value of Information** (Howard 1966): the value of an observation is the expected improvement in decision quality — *inherently* dependent on the decision at hand. This is "significance is context-dependent", formalised, sixty years ago.
- **Bayesian experimental design** (Lindley 1956): expected information gain determines which experiment to run.
- **Bayesian optimal experimental design in astronomy**: routinely used for survey and follow-up strategy.

**Implication for ASA:** ASA's "Scientific information value" context profile (`ASTRO-CONTEXT-MODEL-0001` §5.7) is expected-information-gain under a different name. This is not a criticism of the profile — it is well specified — but it must be cited as EVOI, and its performance must be compared to a proper EVOI baseline, which is a strong competitor.

## 3.5 Learned relevance

**[ESTABLISHED]**

- **Graph neural networks** (GCN, GraphSAGE, GAT): learned node representations by neighbourhood aggregation. **Graph Attention Networks compute per-edge relevance weights and then aggregate** — architecturally, "significance then reasoning".
- **Transformer attention**: computes a relevance distribution over inputs, then aggregates. Again: significance precedes aggregation.
- **Learning to rank**: query-conditional ordering; the query is the context.
- **Retrieval-augmented generation**: retrieve by relevance, then reason.

**This is the most uncomfortable prior art and must be confronted directly.** The claim "reasoning must never determine significance; reasoning occurs only after significance has already emerged" describes the *forward pass* of every attention-based model. The genuine difference is in the *backward pass*: in a learned model, the significance weights are determined by gradients from the reasoning objective, so over training, reasoning does determine significance. In ASA, significance is determined by declared context and evidence structure, and is never fitted to the downstream reasoning outcome.

So the honest formulation of ASA's distinction is:

> **ASA forbids the significance function from being fitted to the reasoning objective.** [This is the real claim, and it is defensible.]

That is a constraint on *learning*, not on *architecture*. It has close relatives: causal-invariance learning, anti-leakage discipline, and the general principle that a feature selector must not see the test labels. But as an architectural invariant enforced at the data-model level, I did not find a direct equivalent.

## 3.6 Astronomical ontologies and knowledge graphs

**[ESTABLISHED]**

- **IVOA** standards: UCDs (Unified Content Descriptors), vocabularies, ObsCore, Provenance Data Model, VOTable. A 2007 IVOA working draft on an "Ontology of Astronomical Object Types" exists.
- **CosmOntology** and SIMBAD-derived ontology work: ontology layers built over SIMBAD's object-type standardisation, used for query construction and classification validation.
- **LLM-constructed astronomy knowledge graphs** (2024–): concept extraction from literature with citation-derived interconnection strength.
- **CDS cross-identification services** (X-Match), **Budavári & Szalay (2008)** Bayesian cross-identification: principled probabilistic entity resolution across catalogues.

**Implication for ASA:** an astronomy knowledge graph with typed relations and provenance is not a new idea. The IVOA Provenance Data Model already mandates much of what `ASA-ASTRO-0001` §11 requires. **ASA-Astro should adopt IVOA ProvDM rather than invent a parallel provenance schema** — inventing one guarantees the programme will be dismissed by the astronomical community as not-invented-here. This is a concrete recommendation with governance consequences (see DR-0007, DR-0017).

## 3.7 Prior-art summary table

| ASA element | Nearest prior art | Distance |
|---|---|---|
| Evidence records with provenance | W3C PROV, IVOA ProvDM | **Zero** — adopt, don't reinvent |
| Candidate vs resolved entity | Probabilistic databases; Bayesian cross-ID | **Zero** |
| Typed relationship taxonomy | HINs, OWL object properties, IVOA vocabularies | **Small** — ASA's physical detail is finer |
| Per-type transitivity rules | OWL `TransitiveProperty` | **Small** |
| Per-type unit/frame/epoch validity gating on composition | *No direct equivalent found* | **Genuine gap** — see §5.6 |
| Standing | PageRank / eigenvector / Katz / TrustRank | **Zero** |
| Context declaration | Personalised PageRank teleport; query specification; EVOI decision context | **Zero** as concept; **small** as a frozen, versioned, auditable artefact |
| Dynamic significance | Personalised PageRank; metapath relevance; EVOI | **Zero** |
| Significance never stored on entity | Database normalisation; event sourcing | **Zero** as principle; **small** as an enforced invariant in a scientific graph |
| Abstention / indeterminate as first-class | Selective prediction / classification with reject option (Chow 1970) | **Zero** as concept; **small** in ranking rather than classification |
| Reasoning must not fit significance | Anti-leakage discipline; causal invariance | **Small** — the enforcement mechanism differs |
| Context frozen before evaluation | Clinical-trial preregistration; ML held-out protocol | **Zero** as method; **small** as machine-enforced artefact |

**Aggregate verdict:** [STRONG] The architecture is a *recomposition of existing components under an unusual set of prohibitions*. Its potential contribution is in the discipline, not the mathematics. Documents should say this. The programme will be stronger, not weaker, for saying it first.

---

# 4. Relationship Taxonomy

## 4.1 Assessment of the existing taxonomy

`ASTRO-RELATIONSHIP-TAXONOMY-0001` defines 17 types. Measured against the types named in the research brief:

| Brief's requested type | Covered by existing taxonomy | Adequacy |
|---|---|---|
| gravitational | §2.2 Gravitational | **Good** |
| orbital | §2.3 Orbital | **Good** |
| membership | §2.5 Membership | **Good** |
| containment | §2.4 Containment | **Good** |
| causal | §2.7 Causal | **Good spec; unvalidatable observationally** (§2.4) |
| energetic | §2.8 Energetic | **Good** |
| radiative | §2.9 Radiative | **Good** |
| chemical | §2.10 Compositional (partly) | **Partial** — see 4.2 |
| temporal | §2.11 Temporal | **Good** |
| developmental | §2.12 Developmental | **Good spec; simulation-only validation** |
| hierarchical | §2.4 + §2.6 (split) | **Partial** — hierarchy is implicit, not a first-class type |
| observational | §2.14 Observational | **Good** |
| uncertainty | §2.16 Uncertainty dependency | **Good** |
| measurement | §2.14 (partly) | **Gap** — see 4.2 |
| derived | §2.14 `produced_from` (partly) | **Partial** |

The existing taxonomy is, on inspection, **better than most published astronomical ontologies** on three specific points: it separates magnitude from confidence; it declares transitivity per type; and it names failure modes explicitly. Those three properties should be preserved through any revision. [STRONG]

## 4.2 Identified gaps — proposed additional types

Seven gaps. Each is justified by a concrete failure that would occur without it.

### G1 — **Identity / cross-identification** (`same_as`, `possibly_same_as`, `distinct_from`)

**Why required:** The single most common relationship in real astronomy is "catalogue record A and catalogue record B refer to the same object." SIMBAD's ~66M identifiers for ~19.5M objects means the identity relation outnumbers all others roughly 3:1. The current taxonomy handles this inside entity resolution, not as a graph edge — which means cross-match uncertainty cannot propagate through the graph.

**Critical property:** `same_as` is the *only* type that should be transitive-and-symmetric (an equivalence relation) — and even then only at a declared confidence threshold, because probabilistic identity is notoriously non-transitive (A matches B at 0.9, B matches C at 0.9, A matches C at 0.4). **This non-transitivity of probabilistic identity is a well-known trap** [ESTABLISHED] and must be tested with a negative fixture.

### G2 — **Classification / typing** (`is_of_type`, `type_supersedes`)

**Why required:** "This object is a Type Ia supernova" is a relationship between an entity and a taxonomy node, carrying evidence, confidence, and a revision history. Currently it would be smuggled in as an entity attribute — which violates the same principle that forbids storing significance as an attribute. Classification is contested, revisable and evidence-dependent; it belongs in the graph.

### G3 — **Statistical association** (`correlates_with`, `co_occurs_with`)

**Why required:** Without an honest home for "these two quantities are correlated and we do not claim causation", every correlation will be forced into either `causal` (overclaim) or nothing (information loss). This type is the pressure valve that makes the strict `causal` type survivable. It must be explicitly non-transitive and must carry the estimator, sample, and confounding-control declaration.

### G4 — **Selection / censoring dependency** (`observability_limited_by`, `included_by_criterion`)

**Why required — this is the most important addition.** Per §2.3, selection effects are the primary confound. If the selection function is not represented *in the graph as edges*, it cannot be reasoned about, controlled for, or ablated. Making censoring a first-class relationship allows the benchmark to ask: "does this significance ranking change when the selection edges are ablated?" — which is the only direct test of the brightness-through-topology leak.

**Assessment: without G4, I do not believe the programme can rule out that it has built a brightness ranker.** [STRONG]

### G5 — **Calibration dependency** (`calibrated_against`, `depends_on_calibration`)

**Why required:** Astronomical values are calibrated against standards (flux standards, astrometric reference frames, radial-velocity standards). Two measurements sharing a calibrator are *not independent*. The existing `uncertainty dependency` type (§2.16) can express this, but it does not distinguish shared-calibrator correlation — which is precisely the case where naive independence assumptions produce false corroboration. `ASA-ASTRO-0001` §10 already forbids counting same-source records as independent corroboration; G5 makes that machine-checkable.

### G6 — **Contradiction / competing claim** (`contradicts`, `supersedes`, `revises`)

**Why required:** The corpus mandates that contested alternatives be co-representable (`ASTRO-RELATIONSHIP-TAXONOMY-0001` §1.7) but provides no edge type to *link* the alternatives. Two assertions that disagree should be connected by an edge, not merely both present. Without it, a reasoner cannot tell "two independent supporting claims" from "one claim and its refutation."

### G7 — **Derivation** (`derived_from_value`, `model_input_to`)

**Why required:** Distinct from `produced_from` (data custody). A mass estimate derived from a velocity dispersion under a virial assumption has a *scientific* derivation dependency, not merely a file-lineage one. Changing the assumed model invalidates the derived value. The current taxonomy conflates these under Observational §2.14, whose transitivity rule ("only provenance-like `produced_from` paths may be traversed transitively") would incorrectly license traversal across a model boundary.

## 4.3 The missing layer: a composition algebra

**[HYPOTHESIS — and this is the programme's most defensible novelty claim]**

The taxonomy declares transitivity *per type*. It does not declare **composition across types**. But real traversal is cross-type: `star --member_of--> cluster --contained_in--> galaxy`. Is `star --?--> galaxy` derivable? Under what semantics? With what units?

I propose the taxonomy be extended with a **composition table**: a partial function

```
compose : Type × Type × ValidityConditions → Type ∪ {⊥}
```

where `⊥` means "no valid composite relation exists; traversal must stop." Validity conditions include compatible coordinate frame, compatible epoch or overlapping validity interval, compatible role semantics, compatible units under a declared dimensional rule, and compatible model family.

Examples of entries:

| Left | Right | Composite | Condition |
|---|---|---|---|
| `contained_in` | `contained_in` | `contained_in` | Same boundary semantics, nested, same frame |
| `member_of` | `contained_in` | **⊥** | Membership is a criterion, containment is a boundary. Composition is a category error. |
| `orbits` | `orbits` | **⊥** | Hierarchical orbits require an explicit dynamical model, not composition. |
| `same_as` | *anything* | *anything* | Identity is the composition identity element, above a declared threshold |
| `observed_by` | `calibrated_against` | `depends_on_calibration` | Same instrument and epoch |
| `before` | `before` | `before` | Same time standard |
| `emits` | `occludes` | **⊥** | Requires radiative transfer, not graph composition |

**Why this is the novelty claim:** OWL gives per-property transitivity. HIN metapaths give permitted type sequences. Neither carries *physical validity conditions* (frame, epoch, units, model family) as gating predicates on composition. A metapath in the HIN literature is valid or invalid by schema; here it would be valid or invalid **per instance**, depending on whether the two edges share a compatible frame and epoch. I did not find prior art for instance-level, physically-conditioned path composition gating.

**Honest caveat:** this may exist in the scientific-workflow or units-aware-computing literature under a name I did not search. Before publishing any novelty claim, a formal prior-art search should be commissioned specifically on: dimensional analysis in graph query languages; validity-time semantics in temporal RDF; and frame-aware spatial reasoning calculi (RCC-8 and successors). [UNKNOWN — pending that search]

## 4.4 Proposed consolidated taxonomy (24 types)

Existing 17 (unchanged in semantics, revised only for composition-table entries) plus G1–G7.

Grouping for analytical use:

- **Physical** (composition sometimes licensed under a model): gravitational, orbital, energetic, radiative, compositional, occlusion, dark-matter-mediated
- **Structural** (composition often licensed): containment, membership, structural, hierarchical
- **Historical** (composition licensed within one model): temporal, developmental, lineage
- **Epistemic** (composition governed by derivation semantics): observational, measurement, derivation, uncertainty dependency, calibration dependency, contradiction, classification
- **Identity** (equivalence, threshold-gated): identity/cross-identification
- **Methodological** (never composed; used only for control): selection/censoring, statistical association

**Recommendation:** this grouping should determine which types are eligible for path-based standing computation at all. Only **Structural** and threshold-gated **Identity** types should be traversable by default. Everything else is depth-1 unless a validated model licenses more.

---

# 5. Standing Analysis

## 5.1 What standing is supposed to be

Per `ASA-ASTRO-0001` §13: "Standing MAY summarise an entity's admissibility, evidence support, or structural position under the selected ASA contract. It MUST NOT encode a hidden context-specific priority."

Note this definition already contains **three different things**: admissibility (a predicate), evidence support (an epistemic quantity), and structural position (a topological quantity). These have different mathematical types and must not be one scalar.

## 5.2 How standing differs from significance, mathematically

Let `G` be the evidence-bearing typed graph, `v` an entity, `C` a context drawn from a context space `𝒞`.

- **Significance** is a family of functions indexed by context: `σ : V × 𝒞 → ℝ`, or equivalently a function `σ_C : V → ℝ` for each `C`.
- **Standing** is a single function: `S : V → X` for some codomain `X`, with no dependence on `C`.

That is the whole formal difference: **standing is context-free, significance is context-indexed.** Everything else is interpretation.

The critical question is what standing *is* relative to the significance family. There are exactly three coherent readings, and they are mutually exclusive:

**Reading A — Standing as prior-averaged significance.**
`S(v) = E_{C ~ π}[σ(v, C)]` for some prior π over contexts.
- Mathematically clean.
- **Fatal to the primary hypothesis.** If standing is an expectation of significance over contexts, it *is* an intrinsic property of the object relative to π — a context-independent number attached to the entity, exactly what "objects possess no intrinsic significance" denies. Under Reading A, ASA has intrinsic significance and calls it standing.

**Reading B — Standing as an admissibility gate.**
`S : V → {admissible, inadmissible, indeterminate} × EvidenceSupportRecord`
- Standing is a *predicate plus a record*, not a score. It answers "does this entity have sufficient evidentiary support to be scored at all, and what is that support?" — never "how important is it?"
- Compatible with the primary hypothesis. Contributes no ordering.
- Significance then reads standing as a **filter and an input record**, not as an additive term.

**Reading C — Standing as a structural summary statistic.**
`S(v) = ` some topological descriptor vector (degree profile by type, evidence counts, hierarchy depth).
- A compression of the graph.
- Compatible with the hypothesis only if it is a *vector of descriptors* consumed contextually, not a scalar with an intrinsic ordering.

## 5.3 Finding: the current model implements Reading A and thereby contradicts the primary hypothesis

**[STRONG]**

`ASTRO-SIGNIFICANCE-MODEL-0001` §5 produces a scalar `S_i ∈ ℝ` and §6 uses it as `Q_i* = β_S·S_i + ...`.

A scalar, context-independent, ordered quantity attached to an entity and contributing positively to every significance computation **is an intrinsic importance score**. The name is different; the mathematics is not. Furthermore, §6 uses `S_j` again inside the edge contribution `d_ie = w_e·r_C(t_e)·(0.5 + 0.5·S_j)` — so standing enters twice, once directly and once through neighbours.

Consequence: if standing dominates (large `β_S`, or high variance in `S` relative to the context-dependent terms), significance rankings will be near-invariant across contexts, and the architecture reduces to a single global score — the exact outcome `ASA-ASTRO-0001` §3 says the programme exists to avoid.

**This is directly measurable and should be Experiment E0:** compute `corr(σ_C, S)` across all contexts. If the mean rank correlation between significance and standing exceeds a predeclared threshold, the architecture has collapsed into a single score.

**Recommendation (falsifiable, and I state it as my professional judgement):** adopt **Reading B**. Standing becomes a gate and an evidence record. Remove `β_S·S_i` from the significance sum. If the programme is unwilling to do this, it must abandon the claim that objects possess no intrinsic significance, because it does not hold in the implementation.

## 5.4 Finding: standing cannot add information

**[ESTABLISHED — this is the data-processing inequality]**

Standing `S(v)` is computed deterministically from `G`. Significance is computed from `(S, C, G)`. Since `S = f(G)`, conditioning on `S` given `G` adds nothing:

```
I(target ; S, G | C) = I(target ; G | C)
```

**Therefore standing can never increase the information available for computing significance.** It can only:

1. **Constrain** the hypothesis class (an inductive bias — helpful if the bias is correct, harmful if not);
2. **Cache** an expensive computation (an efficiency gain);
3. **Audit** — provide a stable, inspectable intermediate that reviewers can check (a governance gain);
4. **Lose** information through compression (a cost).

**Implication:** the justification for a standing layer must be stated as *computational, governance, or inductive-bias* justification. It must never be stated as an epistemic justification ("standing tells us something the graph does not"), because that is provably false. The current corpus does not state which justification it intends. It should.

**This is testable:** the ablation "remove Standing while preserving Context inputs" is already required by `ASTRO-VALIDATION-FRAMEWORK-0001` §7. If removing standing and computing significance directly from the graph performs *equally or better*, standing is not earning its place and should be demoted to Reading B or removed. I consider this a likely outcome. [HYPOTHESIS]

## 5.5 Finding: path-based standing measures are semantically invalid on this graph

**[STRONG]** — Second internal contradiction.

Eigenvector centrality is defined by `x = (1/λ)·A·x`, i.e. `x_i ∝ Σ_j A_ij x_j`, whose expansion is a sum over **walks of all lengths**. Betweenness counts **shortest paths**. Both presuppose that a sequence of edges constitutes a meaningful composite relation.

`ASTRO-RELATIONSHIP-TAXONOMY-0001` states transitivity is **prohibited** for: gravitational, orbital, membership (default), causal, energetic, radiative, developmental (default), occlusion, dark-matter-mediated — and prohibited-except-conditionally for spatial, containment, structural, compositional, temporal, lineage, observational, uncertainty dependency.

So the taxonomy says most edge sequences do not compose — and the standing model then sums over all of them.

**A walk `A --occludes--> B --member_of--> C` has no referent.** Yet power iteration will propagate weight along it, and Brandes will count it in shortest paths.

**Resolution options (in order of my preference):**

1. **Restrict the topology.** Compute path-based measures only on the sub-graph induced by composition-licensed type sequences (per §4.3). This makes centrality well defined and is implementable.
2. **Use depth-1 aggregation only** for non-composable types, reserving path measures for the structural/identity subgraph.
3. **Abandon path-based standing entirely** and use only typed-degree and evidence-support components.

Option 1 is the scientifically defensible one and is also the concrete embodiment of the composition-algebra novelty claim in §4.3. It turns a defect into the programme's distinctive contribution.

## 5.6 Where the architecture is genuinely novel — precise statement

Consolidating §3 and §5.5, here is my precise, defensible novelty claim. It is deliberately narrow.

**N1 — Instance-level, physically-conditioned path-composition gating.** [HYPOTHESIS — no prior art found, pending the formal search in §4.3]
Traversal between two edges is licensed or refused based on the *instances'* coordinate frames, epochs, units, roles and model families, not merely their types. Existing work (OWL, HINs, metapaths) gates at the schema level.

**N2 — Standing/significance separation enforced as a data-model invariant.** [SPECULATION as to novelty; the principle is standard]
Significance is representable only as a derived event carrying a context hash; the schema makes an intrinsic significance attribute unrepresentable. Precedent exists in event-sourced and normalised data design, but I found no instance of it applied to scientific relevance ranking.

**N3 — Abstention as a first-class ranking output.** [Small novelty]
`indeterminate` is a valid, scored outcome distinct from "ranked last". Selective classification (Chow 1970) has the reject option for classifiers; ranking systems almost universally force a total order. Making `indeterminate` scoreable in a *ranking* benchmark is unusual and useful.

**N4 — Machine-enforced context preregistration.** [Small novelty]
The context declaration is content-hashed and frozen before evaluation, with the hash carried in every result. Preregistration is standard in clinical trials; cryptographic enforcement inside the computation is not standard in either field.

**N5 — Prohibition of fitting significance to the reasoning objective.** [HYPOTHESIS]
Per §3.5, this is the real distinction from attention-based architectures. It is a learning constraint enforced architecturally.

**Everything else in the architecture is prior art.** I recommend the programme claim exactly N1–N5, in these words, and claim nothing more.

---

# 6. Context Analysis

## 6.1 When is context provably necessary?

**Result R1 (Automorphism Bound).** [ESTABLISHED — elementary graph theory, applied]

Let `Aut(G)` be the automorphism group of the typed, attributed graph `G`. Any significance function computed from graph structure alone is necessarily constant on automorphism orbits:

> For all `π ∈ Aut(G)` and all `v ∈ V`: `σ_structural(v) = σ_structural(π(v))`.

Therefore:

> **If a question's correct answer distinguishes two automorphic nodes, no structure-only function can answer it. Context is necessary — not merely helpful.**

**Concrete astronomical instances where this bites:**

- **Target-relative questions.** "Which bodies materially perturb *Bennu*?" Two dynamically equivalent asteroids in a symmetric configuration have identical structural position; only naming the target breaks the symmetry. **Context is provably required.**
- **Observer-relative questions.** "Which foreground structures affect what *this* telescope, in *this* band, at *this* epoch recorded?" Occlusion relations are observer-indexed; the graph without an observer designation cannot distinguish them.
- **Frame- and epoch-relative questions.** Proper motion changes projected proximity; a question scoped to epoch J2000 has a different answer than one scoped to J2026.
- **Utility-asymmetric questions.** "Which alerts should we spend 8 metres of telescope aperture on tonight?" is a decision problem with an explicit loss function. Structure carries no loss function.

**Conversely, where context is NOT necessary:** genuinely automorphism-invariant structural questions — "is this system hierarchical?", "how many members does this cluster have?", "is X in the same bound system as Y?". These are structural facts. The architecture should not pretend they need context, and the benchmark should include them precisely to show where the context machinery is *unnecessary overhead*. An architecture that claims context is always needed is overclaiming.

## 6.2 What context must contain, minimally

Distilled from R1, context must supply at least the symmetry-breaking information:

1. **Designation** — which entities/questions are targets (breaks automorphism)
2. **Observer / frame / epoch** — which perspective (breaks observer symmetry)
3. **Admissible evidence and relationship types** — which subgraph is in play
4. **Utility or objective** — what a good answer optimises (supplies the loss function)
5. **Horizon** — over what interval or scale
6. **Missingness and abstention policy** — what to do with unknowns

`ASTRO-CONTEXT-MODEL-0001` §3's 25-field declaration covers all six and more. **My assessment is that it is over-specified for a first benchmark.** 25 required fields with no defaults means every experiment carries substantial declaration overhead, and fields declared as `not_applicable` en masse become noise rather than discipline. Recommend a **minimal core profile** of the six above, with the remaining fields optional-but-recorded, for the first experiment programme. This is a working-efficiency judgement, not a principle change.

## 6.3 The context space is the hidden degree of freedom

**[STRONG] — a serious methodological warning.**

If contexts are chosen by the same people who designed the architecture, and chosen *after* seeing which contexts the architecture handles well, the entire validation is invalid. This is the ranking-benchmark equivalent of post-hoc subgroup selection.

**Required control:** the context set must be (a) frozen before any result is seen, (b) drawn from an *external* source where possible — real proposal science cases, real broker filters, real target-selection cartons — rather than invented, and (c) include contexts the architecture is expected to handle *badly*, declared in advance as such.

If every context in the benchmark is one ASA handles well, the benchmark measures nothing.

## 6.4 Context and significance: what "emergence" can defensibly mean

The brief says significance "emerges" from evidence, relationships, standing and context. "Emergence" is doing no work here and should be dropped from scientific documents. [STRONG]

The defensible statement is: **significance is a computed function of (evidence, graph, context) with no free parameters fitted to the reasoning outcome.** That is precise, testable, and does not invite the objection that "emergence" is being used to avoid specifying a mechanism.

---

# 7. Significance Analysis

## 7.1 Can significance emerge from graph structure alone?

**No.** [ESTABLISHED, via R1 in §6.1]

Structure-only significance is automorphism-invariant. Most operationally interesting astronomical questions are target-, observer-, frame- or epoch-relative and therefore not automorphism-invariant. Structure alone is provably insufficient for these.

Structure alone *is* sufficient for automorphism-invariant structural questions. The programme should say exactly this: **structure suffices for structural questions and provably fails for indexed questions.** That is a clean, defensible, non-vague answer to Research Objective 8.

## 7.2 Where existing graph theory ends

Research Objective 7. Six specific boundaries, each with the reason it is a boundary rather than a gap someone forgot to fill:

**B1 — Dimensional semantics.** Graph theory is dimensionless. Astronomical edge weights carry units (arcsec, km/s, M☉, magnitudes, dimensionless probabilities). `w_e = s_e·c_e·q_e·k_e` in the current model multiplies a "relationship strength" of unstated dimension by three dimensionless factors. **What are the units of `w_e`?** If strengths of different types have different dimensions, summing them (`Σ w_e` in standing component 2) is dimensionally invalid. This is not pedantry; it is the reason the score cannot be interpreted physically. [ESTABLISHED]

**B2 — Validity conditions.** An edge is true only within a frame, epoch, band, and model family. Graph theory has no notion of an edge that exists conditionally. Temporal RDF and validity-time databases address part of this; the multi-dimensional (frame × epoch × band × model) case is not standard. [STRONG]

**B3 — Composition semantics.** §5.5. Path-based algorithms presuppose composability. Astronomical relations mostly do not compose. [STRONG]

**B4 — Censoring.** Graph algorithms assume the graph is the graph. Astronomical graphs are severely and non-randomly censored (§2.3). There is no standard correction for centrality under a known selection function. **This is a genuine open research problem and, in my view, the most scientifically interesting one the programme touches.** [UNKNOWN — genuinely open]

**B5 — Assertion versus fact.** Knowledge graph edges conflate "X relates to Y" with "someone claims X relates to Y with this evidence." Reification and RDF-star address the representation; no standard ranking algorithm consumes it correctly. [STRONG]

**B6 — Non-independence of evidence.** Two edges derived from the same observation or the same calibrator are not independent, yet every centrality measure treats edges as independent contributions. This is the graph-theoretic version of pseudo-replication. [ESTABLISHED as a statistical problem; not addressed in graph ranking]

**Assessment:** B1, B2, B3 and B6 are addressable with engineering discipline — and that discipline is essentially what ASA proposes. B4 is a real open problem. B5 is representable today.

## 7.3 What significance must be, formally, for this programme to be testable

For validation to be possible, `σ(v, C)` must have an **independently observable referent**. Three candidate definitions, in decreasing rigour:

**D1 — Counterfactual effect (strongest).**
`σ(v, C) := ‖M_C(G) − M_C(G \ v)‖`
where `M_C` is a declared measurable outcome under context `C`. Significance is the magnitude of the change in the outcome when the entity is removed. This is *measurable*, *quantitative*, *non-circular* and *context-parameterised* by the choice of `M_C`.

In solar-system dynamics, `M_C` is a target's ephemeris over a horizon, and `σ` is computed by leave-one-out integration. **This is exact ground truth.** [ESTABLISHED — this is standard perturbation analysis]

**D2 — Revealed relevance (medium).**
`σ(v, C) := ` the observed rate at which human experts, operating under a declared context, selected `v` for attention (follow-up, target inclusion, literature citation).
Measurable but confounded by observability, fashion, and historical priority. Usable with careful confound controls. [STRONG as a proxy; not ground truth]

**D3 — Elicited judgement (weakest).**
Expert-assigned graded relevance under a written rubric.
Expensive, subjective, low inter-rater agreement expected on ranking tasks. Usable only as a supplement. [HYPOTHESIS]

**Recommendation:** the programme's primary validation must rest on **D1**. D2 provides breadth and realism. D3 provides interpretability. Any claim resting on D3 alone should not be made.

## 7.4 The relationship between the three layers, restated

Putting §5, §6, §7 together, the defensible architecture is:

```
Evidence graph G  (typed, provenance-bearing, censoring-annotated)
      │
      ├──► Standing S(v)  =  ⟨admissible?, evidence-support record, structural descriptors⟩
      │                       — a GATE and a RECORD, not a score
      │                       — computed only on the composition-licensed subgraph
      │
Context C (frozen, hashed, externally sourced)
      │
      ▼
Significance σ(v, C)  — computed from G restricted by C, gated by S,
                        never fitted to the reasoning objective,
                        stored as an event with C's hash,
                        may return `indeterminate`
      │
      ▼
Reasoning  — consumes σ; may never write back to σ
```

This differs from the current `ASTRO-SIGNIFICANCE-MODEL-0001` in exactly two ways: standing is a gate rather than an additive scalar, and path measures are restricted to the licensed subgraph. Both changes are consequences of findings in §5.

---

# 8. Falsification Analysis

The brief says: do not try to prove ASA correct; attempt to falsify it. This section is that attempt, conducted seriously.

## 8.1 Attack 1 — The hypothesis is a definition

**Attack:** "Objects possess no intrinsic significance; significance emerges from evidence, relationships, standing and context" is unfalsifiable as written (§1.2 D).

**Does ASA survive?** Not in this form. The statement must be replaced.

**Survival requires** the sharpened forms in §8.2.

## 8.2 Sharpened, falsifiable hypotheses

**H1 — Context-Irreducibility.**
No context-independent ranking function matches context-specific reference rankings as well as a context-conditional function does, across a declared diverse context set.
*Falsified if:* the best global ranking achieves reference agreement within the predeclared non-inferiority margin of the context-conditional ranking, across contexts.
*Measurable:* yes. Directly.

**H2 — Relational Sufficiency.**
Significance computed from typed relational structure plus context predicts the counterfactual-effect ground truth (D1) better than intrinsic-attribute baselines (mass, flux, distance, size).
*Falsified if:* `GM/r²`, or flux, or any single intrinsic attribute, matches or beats the relational computation.
*Measurable:* yes. **I expect this to be the hardest test to pass.** [HYPOTHESIS]

**H3 — Separation Value.**
Enforcing the architectural separations (standing/significance, magnitude/confidence, assertion/fact, composition gating) yields measurably better calibration, better abstention behaviour, or better cross-context transfer than an unseparated model of equal capacity.
*Falsified if:* an unconstrained model matches or beats it on all three.
*Measurable:* yes.

**These three are the programme's actual scientific content.** Everything else is engineering.

## 8.3 Attack 2 — The architecture is a brightness ranker in disguise

**Attack:** Per §2.3, catalogue degree correlates strongly with observability, which correlates strongly with apparent brightness. A graph-degree-driven significance score may reproduce a brightness ranking while passing every explicit brightness negative control, because the brightness enters through topology rather than through a feature.

**Does ASA survive?** **Unknown, and currently untested.** The existing negative controls (`ASTRO-VALIDATION-FRAMEWORK-0001` §8) test brightness-only baselines but do not test brightness-through-topology.

**Survival requires:** the G4 selection/censoring relationship type (§4.2), plus a specific control: compute the correlation between the significance ranking and a *pure selection-function model* of the field. If they correlate above a predeclared threshold, the run is invalid. **This control does not currently exist in the framework and must be added.**

## 8.4 Attack 3 — Standing is intrinsic significance renamed

**Attack:** §5.3. Under the current model, this attack succeeds.

**Does ASA survive?** Only if standing is redefined per Reading B. Otherwise the primary hypothesis is contradicted by the implementation.

## 8.5 Attack 4 — Path measures are meaningless on this graph

**Attack:** §5.5. Under the current model, this attack succeeds.

**Does ASA survive?** Only with composition-licensed subgraph restriction.

## 8.6 Attack 5 — Contexts are chosen to flatter

**Attack:** §6.3.

**Does ASA survive?** Only with externally sourced, pre-frozen contexts including expected-failure contexts.

## 8.7 Attack 6 — A one-line physical formula wins

**Attack:** For gravitational contexts, `GM/r²` is the physics. It requires no graph, no ontology, no context declaration, and it is exactly right. Any graph-based approximation of gravitational significance is strictly worse than computing the actual gravity.

**Does ASA survive?** **This attack largely succeeds for single-physics contexts, and the programme should concede it.**

The honest position: ASA is not a competitor to physics where the physics is known and computable. Its claimed value is in **multi-relational, multi-scale, partially-observed settings where no single closed-form quantity applies** — for example, deciding which of thousands of alerts to follow up given heterogeneous evidence of many types. Where a closed form exists, use the closed form.

**Consequence for the experiment programme:** E2 (solar-system perturbation) must be run *not* to show ASA beats `GM/r²` — it will not — but as a **calibration experiment**: does the architecture *recover* the known physical answer from relational evidence alone, without being told the physics? Recovering the right answer from the wrong-looking inputs is a strong result. Claiming to beat gravity is not.

This reframing is important and I want it recorded explicitly: **E2's success criterion is agreement with physics, not superiority over physics.**

## 8.8 Attack 7 — It reproduces personalised PageRank

**Attack:** §3.1. Standing = PageRank, context = teleport vector, significance = personalised PageRank. Twenty-four years old.

**Does ASA survive?** Partially. The distinguishing elements are N1 (instance-level composition gating), N3 (abstention), and the provenance/uncertainty machinery. Personalised PageRank has none of these. But the *ranking mechanism* is the same, and personalised PageRank must be implemented as a **primary baseline**. If ASA cannot beat personalised PageRank with a well-chosen teleport vector, the added machinery is unjustified.

**This baseline is not currently in `ASTRO-VALIDATION-FRAMEWORK-0001` §6 and must be added.** It is the single most important missing baseline.

## 8.9 Attack 8 — Attention already does significance-before-reasoning

**Attack:** §3.5.

**Does ASA survive?** Yes, but only on the narrowed claim N5: significance is not *fitted* to the reasoning objective. The forward-pass ordering claim is not distinctive and should be dropped from the framing. The diagram at the head of the brief, which presents the ordering as the innovation, is the weakest part of the programme's public case.

## 8.10 Falsification summary

| Attack | Outcome under current corpus | Survivable? |
|---|---|---|
| A1 Unfalsifiable hypothesis | **Succeeds** | Yes — restate as H1/H2/H3 |
| A2 Brightness via topology | **Untested** | Unknown — needs G4 + new control |
| A3 Standing = intrinsic significance | **Succeeds** | Yes — adopt Reading B |
| A4 Meaningless path measures | **Succeeds** | Yes — restrict to licensed subgraph |
| A5 Flattering contexts | **Untested** | Yes — external, pre-frozen contexts |
| A6 Physics wins | **Succeeds for single-physics contexts** | Yes — concede and reframe E2 |
| A7 = personalised PageRank | **Partially succeeds** | Yes — narrow claim to N1/N3/N5, add baseline |
| A8 = attention | **Succeeds on the ordering claim** | Yes — narrow claim to N5 |

**Overall verdict:** [STRONG] Four of eight attacks succeed against the corpus as it currently stands. All four are repairable, and the repairs are specified above. None of them is fatal to the *idea*; all are fatal to the *current formulation*. The architecture survives falsification only in the amended form described in §5.6, §6, §7.4 and §8.2.

**If the programme is unwilling to make these amendments, my assessment is that the Astronomy Validation Programme should not proceed, because it would be testing a formulation already known to be internally contradictory.**

---

# 9. Ground Truth Strategy

## 9.1 The core problem

**There is no catalogue of significance.** No telescope measures it. This is the single hardest problem in the programme and the reason DR-0004 must not be resolved casually.

Four families of ground truth are viable. They are complementary and should all be used, with their different epistemic statuses kept strictly distinct.

## 9.2 GT-A — Structural ground truth (validates the lower pipeline)

**What it validates:** entity identification, relationship identification, relationship type/direction/roles, hierarchy recovery, false-relationship control. **Not significance.**

| Source | Propositions it grounds | Strength |
|---|---|---|
| **Hunt & Reffert (2023)** Gaia DR3 open clusters: 7,167 clusters, >700k members with probabilities | `member_of` with calibrated probability | **Strong.** Probabilistic labels suit ASA's confidence model. A 2026 A&A selection-function analysis exists for this census — use it for G4 edges. |
| **Gaia DR3 non-single-star solutions** | `orbits`, binarity, orbital elements with covariance | **Strong.** Real orbital ground truth with uncertainty. |
| **NASA Exoplanet Archive** | host–planet `contains`/`orbits` hierarchy | **Strong.** Versioned, curated. |
| **Minor Planet Center** | satellite systems, dynamical class containment | **Strong.** |
| **Galaxy group/cluster catalogues** (SDSS-based) | `member_of` at extragalactic scale | **Medium** — group-finding is method-dependent; treat as contested reference. |
| **SIMBAD/NED cross-identifications** | `same_as` (G1) with identifier provenance | **Strong** for the identity relation; note the non-transitivity trap (§4.2 G1). |
| **Galaxy Zoo** | morphological `is_of_type` (G2) with inter-rater distributions | **Strong** — includes native disagreement, exactly what ASA's contested state needs. |

**Circularity check:** none of these are derived from ASA. All are independently maintained, versioned, licensed and citable. GT-A is clean.

## 9.3 GT-B — Counterfactual physical significance (validates significance itself)

**This is the programme's most valuable asset and should be its centrepiece.**

**Construction:**

1. Declare a context `C = ⟨target body, observable (e.g. heliocentric position), horizon (e.g. 100 yr), tolerance (e.g. 1 km)⟩`.
2. Integrate the target's trajectory with the full perturber set (DE440-class: Sun, planets, Moon, Pluto barycentre, 343 asteroids, 30 KBOs + ring).
3. For each perturber `p`, re-integrate with `p` removed.
4. `σ_true(p, C) := ` the resulting positional deviation at horizon.

**Properties — and this is why it matters:**

- **Exact.** No human judgement. [ESTABLISHED]
- **Quantitative and continuous.** Gives graded relevance, not binary labels.
- **Genuinely context-dependent.** Change the target, and the ranking of perturbers changes completely. Change the horizon, and it changes again. **This directly instantiates "the same object has different significance under different contexts" with measurable proof.**
- **Non-circular.** Derived from physics, not from any relevance judgement.
- **Already an operational decision in real astronomy.** JPL's choice of which asteroids to include as perturbers is exactly a significance decision with documented consequences.
- **Supports abstention testing.** For distant perturbers, the effect falls below numerical noise — the correct answer is `indeterminate`, not `zero`.

**The test:** can the ASA pipeline, given *only* relational evidence (masses, orbits, encounter geometry, temporal relations — but not the integration itself), rank perturbers in agreement with `σ_true`, better than degree centrality, better than personalised PageRank, and comparably to `GM/r²`?

**Success criterion, per §8.7: agreement with physics, not superiority over it.**

**Extension to other domains where counterfactual ground truth exists:** cosmological simulation merger trees (which progenitors materially determined a halo's final state — leave-one-out is computationally expensive but tractable on small samples), and gravitational lens modelling (which line-of-sight structures materially change the model).

## 9.4 GT-C — Revealed human significance (validates realism)

**What it validates:** whether the architecture's rankings correspond to what practising astronomers actually treat as relevant under declared contexts.

| Source | Context declaration | Significance signal | Confounds |
|---|---|---|---|
| **SIMBAD object–paper links** (~44M citations) | Paper topic / keyword classification | Object mentioned in papers of that topic | **Severe:** brightness, historical priority, catalogue availability. Must be controlled with a selection model. |
| **Telescope proposal target lists** (HST/JWST/ESO archives, with abstracts) | The proposal's declared science case — a *literal, human-written context declaration* | Object selected as a target | Medium: proposal success bias, PI networks. |
| **DESI / SDSS-V target cartons** | Machine-readable, versioned selection criteria (BGS/LRG/ELG/QSO) | Target selection flags | **Low — this is the cleanest of GT-C.** Criteria are published, versioned, and explicitly context-like. |
| **Alert broker filters** (ALeRCE, ANTARES, Fink, Lasair, and the other Rubin brokers) | Community-written science filters — **the closest existing real-world analogue to an ASA context declaration** | Which alerts pass which filter; which get follow-up | Medium. Live from Feb 2026; ~7M alerts/night from LSST. |

**Assessment of the broker analogy:** [STRONG] Nine brokers ingesting a 7-million-alert nightly stream, each applying community-authored filters to decide "is this an object I want to follow up?", is *exactly* the ASA problem statement, running in production, today, with real consequences. If ASA has operational value anywhere in astronomy, it is here. I recommend this become the programme's eventual applied target (§18).

**Circularity warning:** GT-C is human judgement, and human judgement is influenced by brightness and observability. GT-C can validate *realism*; it cannot validate *correctness*. Never present a GT-C result as scientific ground truth.

## 9.5 GT-D — Simulation ground truth (validates causal and developmental types)

Cosmological simulations (IllustrisTNG, EAGLE) publish merger trees: complete formation histories with every progenitor known.

**What it uniquely enables:** [STRONG]

- **Causal and developmental relationship validation** — impossible observationally (§2.4), possible here because the generating process is known and interventions can be run.
- **Known selection function** — one can apply a synthetic survey selection to simulated data and compare the censored graph's centrality to the true graph's centrality. **This is the only way to directly measure the B4/A2 censoring bias.** It should be done early.

**Limitation:** validates agreement with the simulation's physics, not with reality. Must always be reported as such.

## 9.6 Ground truth strategy summary

| Family | Validates | Rigour | Priority |
|---|---|---|---|
| GT-A structural | Lower pipeline: entities, relationships, hierarchy | High | 1st — required to trust anything above it |
| GT-B counterfactual | **Significance itself** | **Highest** | 1st — the programme's core test |
| GT-D simulation | Causal/developmental types; **censoring bias** | High (within-model) | 2nd |
| GT-C revealed | Operational realism | Proxy only | 3rd |

**Recommendation for DR-0004:** resolve as GT-A + GT-B for the first benchmark; GT-D for the censoring control; GT-C reserved for a later applied phase. Explicitly record that GT-C is not ground truth.

---

# 10. Dataset Recommendations

Concrete, in priority order, with the reason each is chosen and its principal hazard.

**Tier 1 — first benchmark (freeze these)**

1. **JPL DE440/DE441 + Horizons + Small-Body Database.** For GT-B. Public, stable, exactly documented, and the perturber-inclusion decision is itself the object of study. *Hazard:* requires an N-body integrator — but only as a ground-truth generator, not as part of ASA.
2. **Gaia DR3** (explicitly, *not* DR4 yet). Astrometry, photometry, NSS solutions. *Hazard:* DR4 lands 2 December 2026 with 5.5 yr time series and 130+ products; any DR3-based benchmark must declare itself DR3-frozen and plan a DR4 refresh, or it will look obsolete within months.
3. **Hunt & Reffert (2023) open cluster catalogue + its 2026 selection-function analysis.** For GT-A membership and for G4 censoring edges. *Hazard:* HDBSCAN-derived membership is method-dependent; treat as one reference among possible alternatives, not as truth.
4. **NASA Exoplanet Archive.** For GT-A hierarchy. *Hazard:* heterogeneous provenance across discovery methods; version-pin.

**Tier 2 — censoring and causal controls**

5. **IllustrisTNG (public data release) merger trees.** For GT-D. *Hazard:* model-dependence must be declared in every result.
6. **SDSS group/cluster catalogues + Galaxy Zoo.** Extragalactic structure and disagreement-bearing classification. *Hazard:* group finders disagree; use as contested reference deliberately.

**Tier 3 — identity, literature, and realism**

7. **SIMBAD + NED + CDS X-Match.** For G1 identity edges and GT-C literature relevance. *Hazard:* the object–paper link is heavily confounded; only usable with an explicit selection model.
8. **NASA ADS.** Literature graph. *Hazard:* citation dynamics are sociological.

**Tier 4 — future applied phase**

9. **Rubin/LSST alert stream via a community broker.** For the applied programme (§18). *Not available as a static release before ~June 2028 (DRY1); DR1 was cancelled.* Alerts and DP2 are available now for prototyping.
10. **DESI / SDSS-V target cartons.** Machine-readable context declarations. *Hazard:* DR2 spectra not yet public as of review.

**Explicitly recommended against for the first benchmark:**

- **A single illustrative image** (the current DR-0003 path). It cannot supply ground truth for identity, physical relationship, causation, composition, development, or significance. The POC validation report already records this. Continuing down this path spends effort on a route that cannot reach a validation result. **Recommend DR-0003 be closed as "not pursued for validation purposes; retained for pipeline smoke-testing only."**
- **JWST/HST imaging as a primary source.** Beautiful, but same problem: images do not carry relationship ground truth. Use catalogues.

---

# 11. Validation Methodology

This section amends rather than replaces `ASTRO-VALIDATION-FRAMEWORK-0001`, which is already strong. The amendments are the ones falsification analysis showed to be missing.

## 11.1 Amendments required to the existing framework

**M1 — Add personalised PageRank as a primary baseline.** (§8.8) Currently absent. Without it, the programme cannot claim its context mechanism does anything a 2002 algorithm does not.

**M2 — Add a selection-function baseline and control.** (§8.3, §2.3) Compute a pure selection/observability model of the field and correlate it with the significance ranking. Predeclare the threshold above which the run is invalid.

**M3 — Add a closed-form physics baseline where applicable.** (§8.7) For gravitational contexts, `GM/r²`. Report it as an *anchor*, and define success as agreement with it, not superiority.

**M4 — Add the standing-collapse test (E0).** (§5.3) Mean rank correlation between `σ_C` and `S` across contexts. Predeclared ceiling; exceeding it means the architecture has collapsed to a single score.

**M5 — Add composition-validity tests.** (§5.5) Negative fixtures asserting that path measures refuse to traverse non-licensed type sequences, with frame/epoch/unit mismatches as separate cases.

**M6 — Add dimensional-consistency tests.** (§7.2 B1) Every aggregated quantity must declare its dimension; summing incommensurable strengths must fail validation.

**M7 — Require external context sourcing.** (§6.3) At least half the benchmark contexts must derive from external artefacts (target cartons, broker filters, proposal abstracts), and at least one must be predeclared as an expected-failure context.

**M8 — Score abstention explicitly.** (§5.6 N3) `indeterminate` must have a defined cost, distinct from a wrong ranking and distinct from a correct one. Without this, abstention is free and the system will abstain its way to a good score.

## 11.2 Metric selection for GT-B

Since GT-B yields a continuous graded ground truth, the appropriate metrics are:

- **Spearman ρ and Kendall τ-b** against `σ_true` — overall ordering agreement
- **nDCG@k** with gain derived from `σ_true` magnitude — top-of-ranking accuracy, which is what matters operationally
- **Top-k set recall** at the operationally meaningful `k` (e.g. "the 16 perturbers you must include for 1 km accuracy")
- **Calibration of the abstention region** — for perturbers below the tolerance, does the system correctly return `indeterminate`?
- **Cross-context rank instability** — how much does the ranking change when the target changes? A system whose ranking barely moves across targets has failed H1.

That last metric is the direct measurement of the central hypothesis, and I want it named as the programme's headline number.

## 11.3 Leakage controls specific to this programme

- The ASA pipeline must never receive the integrator's output, the perturber list, or `GM/r²` as a feature.
- Masses may be supplied (they are catalogue facts) but the inverse-square law must not be encoded in the relationship weights, or the test is circular.
- **This is a hard boundary and the most likely place for accidental leakage.** An independent reviewer should audit the feature set specifically for implicit gravitational law encoding before the run.

---

# 12. Experiment Programme

Seven experiments. Each states its falsification condition in advance.

## E0 — Standing collapse test
**Question:** Does significance reduce to standing?
**Method:** compute `σ_C` for all benchmark contexts; report mean and distribution of `corr(σ_C, S)`.
**Falsifies:** if mean rank correlation exceeds the predeclared ceiling, the architecture is a single score with context decoration. **Run this first; it is cheap and it is decisive.**

## E1 — Structural recovery (GT-A)
**Question:** Can the pipeline recover known membership, orbital and containment relationships with correct type, direction, roles, units, frame and epoch?
**Data:** Hunt & Reffert clusters; Gaia DR3 NSS; Exoplanet Archive.
**Metrics:** per-type precision/recall, direction accuracy, invalid-transitivity rate, abstention-aware coverage.
**Falsifies:** recovery below the frozen threshold, or transitive edges generated that the taxonomy forbids.
**Note:** this validates the *lower pipeline only*. Passing E1 says nothing about significance.

## E2 — Counterfactual perturbation significance (GT-B) — **the centrepiece**
**Question:** Given only relational evidence, does ASA's context-specific significance ranking agree with measured counterfactual perturbation effect?
**Contexts:** ≥20, varying target body, observable, horizon and tolerance.
**Baselines:** random; mass-only; inverse-distance-only; degree centrality; personalised PageRank; `GM/r²` (as anchor, not competitor).
**Metrics:** §11.2, headline = cross-context rank instability.
**Falsifies:** ranking agreement no better than degree centrality or personalised PageRank; **or** ranking barely changes across targets (H1 fails); **or** `GM/r²` agreement is not approached at all.
**Success:** ranking approaches the physics anchor while beating all graph baselines, and moves substantially across contexts.

## E3 — Censoring bias measurement (GT-D)
**Question:** How much of the significance score is explained by the selection function?
**Method:** in simulation, compute significance on the true graph and on a synthetically censored graph; measure divergence. Separately, correlate real-data significance with a selection model.
**Falsifies:** if censored-graph significance correlates with the selection model above the predeclared threshold, the system is a observability ranker. **This is the experiment that answers Attack A2, and I regard it as the second most important.**

## E4 — Context ablation and swap
**Question:** Does context do work, and only through declared inputs?
**Method:** the ablations and negative controls already specified in `ASTRO-VALIDATION-FRAMEWORK-0001` §§7–8, plus M1–M8.
**Falsifies:** context label swaps change results (labels are computational — an integrity failure); or removing context inputs does not degrade performance.

## E5 — Composition gating validity
**Question:** Does the composition algebra prevent meaningless traversal without preventing meaningful traversal?
**Method:** positive and negative fixtures per §11.1 M5; measure whether restricting to licensed subgraphs changes (and ideally improves) E2 results.
**Falsifies:** gating makes no measurable difference — in which case N1, the primary novelty claim, is not doing anything.
**This experiment tests the novelty claim directly and should be reported prominently whichever way it goes.**

## E6 — Calibration and abstention
**Question:** Is confidence calibrated, and is abstention used correctly?
**Method:** reliability diagrams, ECE, coverage at declared levels, stratified by relationship type; abstention cost per M8.
**Falsifies:** material miscalibration, especially overconfidence on false physical assertions; or abstention used to avoid hard cases without cost.

## E7 — Revealed-relevance realism (GT-C)
**Question:** Do rankings correspond to what astronomers actually prioritise under matched contexts?
**Method:** DESI/SDSS-V target cartons and broker filters as contexts; selection as signal; explicit confound model for brightness and observability.
**Falsifies:** nothing — this is a *realism probe*, not a validation. Its result must never be reported as validation of correctness.

## Sequencing

```
E0 (cheap, decisive)
 └─► E1 (lower pipeline trust)
      └─► E2 (core significance test) ──┬─► E5 (novelty claim test)
           └─► E3 (censoring bias)      └─► E6 (calibration)
                └─► E4 (context integrity)
                     └─► E7 (realism, last)
```

**E0 before anything else.** If E0 fails, no other experiment is worth running until standing is redefined.

---

# 13. Failure Conditions

Beyond those already frozen in `ASA-ASTRO-0001` §17 and `ASTRO-VALIDATION-FRAMEWORK-0001` §16.3, this research adds:

**F1** — Mean `corr(σ_C, S)` exceeds the predeclared ceiling (E0). *Architecture has collapsed to a single score.*
**F2** — Significance ranking correlates with a pure selection/observability model above threshold (E3). *System is an observability ranker.*
**F3** — Personalised PageRank with a comparable teleport vector matches or beats ASA significance (E2). *The added machinery is unjustified.*
**F4** — Cross-context rank instability is below the predeclared floor (E2). *H1 fails; context is decorative.*
**F5** — Composition gating produces no measurable difference (E5). *N1, the primary novelty claim, is empty.*
**F6** — Path-based standing components are retained on non-licensed subgraphs. *Known semantic invalidity; run is invalid, not merely failed.*
**F7** — Any context is added, removed or modified after results are seen. *Benchmark invalid.*
**F8** — The gravitational law is found encoded in the relational feature set during audit (E2). *Circular; run invalid.*
**F9** — Abstention is unpriced and abstention rate exceeds the predeclared bound. *Score is inflated by silence.*

**F1, F6, F7 and F8 are *invalidating*, not merely failing.** A run exhibiting them produces no result at all.

---

# 14. Success Conditions

A bounded success requires **all** of:

1. All conditions in `ASTRO-VALIDATION-FRAMEWORK-0001` §16.1 met.
2. **E0 passes:** significance is demonstrably not standing.
3. **E1 passes:** structural recovery meets frozen thresholds with forbidden-transitivity rate at zero.
4. **E2 passes:** significance ranking approaches the physics anchor, beats all graph baselines including personalised PageRank, and shows substantial cross-context rank movement.
5. **E3 passes:** selection-function correlation below threshold.
6. **E4 passes:** context has traceable effect; label swaps have none.
7. **E6 passes:** calibration within frozen bounds; abstention priced and within bounds.
8. Every result carries a complete explanation trace, a frozen context hash, and resolvable provenance.
9. All negative and invalidating results reported.

**What a success would and would not establish:**

*Would:* that on a bounded astronomy benchmark, a significance-first architecture with the stated separations produces context-sensitive rankings that agree with measured counterfactual physical effect better than standard graph-ranking baselines, with calibrated uncertainty and auditable provenance.

*Would not:* that ASA is correct; that significance-first intelligence is validated; that the approach generalises beyond the benchmark; that anything has been discovered. These prohibitions are already in `ASA-ASTRO-0001` §15 and should be repeated verbatim in any result document.

---

# 15. Research Risks

| # | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | No astronomical data acquired; programme stalls at synthetic fixtures | **High — this is the current state** | Fatal | Resolve DR-0003/DR-0004 immediately per §10. Close the single-image path. |
| R2 | Selection function drives results undetected | **High** | Fatal to credibility | G4 edges; E3; M2 control |
| R3 | Standing dominates; architecture collapses to one score | **High under current model** | Fatal to the hypothesis | Reading B; E0 first |
| R4 | Trivial physical baseline wins | **High** | Reframing, not fatal | Concede per §8.7; success = agreement with physics |
| R5 | Contexts selected to flatter | Medium | Fatal to validity | External sourcing; pre-freeze; expected-failure context |
| R6 | Gaia DR4 (Dec 2026) obsoletes a DR3-frozen benchmark | **Certain** | Presentational | Declare DR3-frozen explicitly; plan DR4 refresh |
| R7 | Novelty claim collapses under a proper prior-art search | Medium | Reputational | Commission the §4.3 search *before* any external claim |
| R8 | Over-specified context model (25 required fields) makes experiments impractically expensive | Medium | Schedule | Minimal core profile per §6.2 |
| R9 | Parallel provenance schema rejected by astronomical community | Medium | Adoption | Adopt IVOA ProvDM per §3.6 |
| R10 | Causal/developmental types validated observationally, producing uninterpretable results | Medium | Scientific error | Restrict to GT-D simulation or scope out |
| R11 | Twenty open decisions block every experiment | **Certain under current register** | Schedule | Prioritise DR-0003, DR-0004, DR-0009, DR-0010, DR-0012, DR-0014; defer the rest |
| R12 | ASA dependency (DR-0001) never resolves, so nothing can claim conformance | High | Scope | Proceed as an independent architecture study; state plainly that ASA conformance is untested |

---

# 16. Open Questions

Genuinely open — I could not resolve these from available information.

**Q1** — Is there a correction for centrality bias under a known selection function? [UNKNOWN] This is a real open research problem (§7.2 B4). If the programme solved it, that would be a publishable contribution *independent of ASA*.

**Q2** — Does instance-level, physically-conditioned path composition gating exist in the literature under another name? [UNKNOWN] Search: dimensional analysis in graph query languages; validity-time temporal RDF; frame-aware qualitative spatial calculi. Must be answered before any novelty claim.

**Q3** — What is the correct dimensional treatment of a "relationship strength" that spans incommensurable physical quantities? [UNKNOWN] Options: per-type dimensionless normalisation against a declared scale; refusal to aggregate across types; or a type-indexed vector score rather than a scalar. I lean to the third; it is untested.

**Q4** — Is there a principled prior π over contexts, or is the context space unbounded? [UNKNOWN] Matters because Reading A's coherence depends on it, and because "diverse context set" needs a definition of diversity.

**Q5** — How should contested ground truth be scored when references disagree? [Partially addressed in `ASTRO-VALIDATION-FRAMEWORK-0001` §4.3, DR-0019 open] Group catalogues and cluster membership will disagree; the adjudication rule must be frozen in advance and is not yet specified.

**Q6** — Can significance be defined without a decision? [UNKNOWN] D1 requires a declared outcome measure `M_C`; D2 requires a declared human decision. If significance always requires a decision, then ASA is decision theory with a graph, and should say so.

**Q7** — Does the architecture's value survive when relationships must be *inferred* rather than looked up? [UNKNOWN] All GT-A sources supply relationships directly. Real deployment requires inferring them. The programme currently tests the easy half.

---

# 17. Recommended Research Roadmap

## Phase 0 — Corrections (before any experiment)

1. **Adopt Reading B for standing** (§5.3). Amend `ASTRO-SIGNIFICANCE-MODEL-0001`.
2. **Restrict path measures to composition-licensed subgraphs** (§5.5). Amend the same document.
3. **Replace the primary hypothesis with H1/H2/H3** (§8.2). Amend `ASA-ASTRO-0001` §3.
4. **Withdraw the "independent of human language" claim** (§2.2).
5. **Add relationship types G1–G7 and the composition table** (§4.2–4.3). Amend `ASTRO-RELATIONSHIP-TAXONOMY-0001`.
6. **Add framework amendments M1–M8** (§11.1). Amend `ASTRO-VALIDATION-FRAMEWORK-0001`.
7. **Commission the Q2 prior-art search.** Before any external novelty claim.

## Phase 1 — Data acquisition (the actual blocker)

8. Close DR-0003 (single image not pursued for validation).
9. Resolve DR-0004 as GT-A + GT-B per §9.6.
10. Acquire and version-pin: DE440/Horizons/SBDB; Gaia DR3 subset; Hunt & Reffert; Exoplanet Archive. Record licences, digests, retrieval dates per `ASA-ASTRO-0001` §11.
11. Adopt IVOA ProvDM as the provenance model (§3.6); amend DR-0017.

## Phase 2 — First real experiments

12. **E0** — standing collapse. Decisive, cheap, run first.
13. **E1** — structural recovery on GT-A.
14. **E2** — counterfactual perturbation significance. The programme's core test.

## Phase 3 — Confounds and novelty

15. **E3** — censoring bias, using GT-D simulation.
16. **E5** — composition gating: does the novelty claim do anything?
17. **E4**, **E6** — context integrity, calibration.

## Phase 4 — Realism and reporting

18. **E7** — revealed relevance, reported explicitly as a realism probe.
19. Validation Result per `ASTRO-VALIDATION-FRAMEWORK-0001` §17, including every negative finding.
20. Gaia DR4 refresh assessment (post 2 December 2026).

**Critical path:** Phase 0 items 1, 2 and 3 gate everything. Phase 1 item 10 gates every experiment. Nothing else is on the critical path, and considerable effort in the current corpus is not.

---

# 18. Future Validation Programme

Beyond astronomy, if the programme survives.

**Stage 2 — Applied astronomy: alert triage.** [The strongest applied target]
Rubin/LSST produces ~7 million alerts nightly to nine community brokers, each applying community-written science filters to decide what to follow up. This is the ASA problem statement in production. A context declaration *is* a broker filter. Significance *is* follow-up priority. Ground truth *is* whether follow-up confirmed something. It is measurable, competitive, consequential, and has an existing baseline (the brokers' own ML classifiers). If ASA has operational value, this is where it will show. Available for prototyping now; mature for benchmarking from ~2028.

**Stage 3 — Cross-domain transfer.** The architecture's claimed generality is untested by a single domain. A second domain with counterfactual ground truth is required. Candidates with the same "leave-one-out measurable effect" property: power-grid contingency analysis; epidemiological contact networks in simulation; supply-chain dependency criticality. Each has the two required properties — multi-relational structure and a computable counterfactual outcome.

**Stage 4 — The censoring problem as independent research.** Q1 is a genuine open problem in network science, larger than ASA. If the programme develops a principled correction for centrality under a known selection function, that is a contribution to network science regardless of ASA's fate. I would rate this the highest-expected-value spin-off.

**Stage 5 — ASA conformance.** Only when DR-0001 resolves. Until then, no conformance claim of any kind.

---

# 19. Assessment for the record

Asked to falsify rather than confirm, here is my summary judgement, stated plainly.

**The architecture, as currently written, contains two internal contradictions** (standing as intrinsic significance; path measures on a non-composable graph) **and one unfalsifiable central claim.** All three are repairable, and Section 17 Phase 0 specifies the repairs. Until they are made, running experiments would test a formulation already known to be inconsistent.

**The architecture is not novel at the level of operations.** Every layer has mature prior art, and the closest single precedent — topic-sensitive PageRank — is twenty-four years old. Claims of novelty should be narrowed to N1–N5 and defended only there.

**Astronomy is a good but oversold validation domain.** Its genuine strengths are counterfactual ground truth in dynamics, physically decidable relationship types, native uncertainty reporting, and existing context-like artefacts. Its genuine weaknesses — severe non-random censoring, non-interventionality, and the absence of any significance catalogue — are not currently acknowledged in the corpus and are more dangerous than its strengths are helpful.

**The programme's actual blocker is data, not architecture.** Nine documents, four schemas directories, a working pipeline, and zero astronomical observations. The single most valuable action available is to acquire DE440 plus a Gaia DR3 subset and run E0 and E2.

**And the single most valuable idea in this report is E2:** counterfactual perturbation significance converts "significance" from a philosophical position into a measured quantity with exact ground truth and genuine context-dependence. If the architecture cannot be tested against that, it cannot be tested at all. If it can, then the primary hypothesis becomes a real scientific claim with a real chance of being wrong — which is the only condition under which it is worth defending.

---

## Sources

- [Gaia Data Release 4 — ESA Cosmos](https://www.cosmos.esa.int/web/gaia/data-release-4)
- [Gaia DR4 content — ESA Cosmos](https://www.cosmos.esa.int/web/gaia/dr4)
- [Gaia Data Release Scenario — ESA Cosmos](https://www.cosmos.esa.int/web/gaia/release)
- [Rubin Observatory — Alerts and brokers](https://rubinobservatory.org/for-scientists/data-products/alerts-and-brokers)
- [Rubin Observatory — Early Science Program](https://rubinobservatory.org/for-scientists/resources/early-science)
- [Rubin Observatory Plans for an Early Data Release (RTN-011)](https://rtn-011.lsst.io/RTN-011.pdf)
- [Vera C. Rubin Observatory Data Preview 1](https://dp1.lsst.io/)
- [ANTARES broker](https://antares.noirlab.edu/)
- [Park et al. (2021), The JPL Planetary and Lunar Ephemerides DE440 and DE441](https://ssd.jpl.nasa.gov/doc/Park.2021.AJ.DE440.pdf)
- [SIMBAD Astronomical Database — CDS Strasbourg](http://simbad.u-strasbg.fr/)
- [SIMBAD: The Contents of SIMBAD](https://simbad.u-strasbg.fr/Pages/guide/ch15.htx)
- [Hunt & Reffert (2023), Improving the open cluster census II](https://arxiv.org/abs/2303.13424)
- [The selection function of the Gaia DR3 open cluster census (A&A 2026)](https://www.aanda.org/articles/aa/full_html/2026/02/aa57781-25/aa57781-25.html)
- [The different methods to calculate cluster membership probabilities](https://arxiv.org/html/2607.13711)
- [DESI Data Releases](https://data.desi.lbl.gov/doc/releases/)
- [DESI Data Release 1](https://arxiv.org/pdf/2503.14745)
- [IVOA Ontology of Astronomical Object Types (WD 2007)](https://www.ivoa.net/documents/WD/Semantics/AstrObjectOntology-20070219.html)
- [CosmOntology: Creating an Ontology of the Cosmos](https://ceur-ws.org/Vol-3342/paper-10.pdf)
- [Knowledge Graph in Astronomical Research with Large Language Models](https://arxiv.org/pdf/2406.01391)
- [Enabling science from the Rubin alert stream with Lasair](https://academic.oup.com/rasti/article/3/1/362/7712474)
- [Early Identification of Optical Tidal Disruption Events: a Fink science module](https://arxiv.org/pdf/2507.17499)

---

*End of ASTRO-RESEARCH-0001. Draft status. No architectural authority. Nothing in this document validates ASA, ASA-Astro, or any astronomical claim.*
