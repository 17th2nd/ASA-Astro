# ASTRO-PRIOR-ART-0001 — Prior Art Laboratory: Elimination Report

**Programme:** Adaptive Significance Architecture (ASA)
**Target:** the surviving claims attributed to `ASTRO-RESEARCH-0003`, checked against `ASTRO-RESEARCH-0001`, `ASTRO-RESEARCH-0002`, and the graph-theoretic reduction preceding this report
**Author cell:** Codex (Prior Art Laboratory role)
**Date:** 2026-08-01
**Status:** DRAFT — adversarial prior-art review, not a patentability opinion, validation result, or architectural authority
**Repository:** ASA-Astro

---

## 0. Verdict

**No defensible mathematical novelty remains.**

ASA does not introduce a new graph class, graph invariant, path problem, centrality, intervention calculus, uncertainty calculus, query language, ontology formalism, learning architecture, decision rule, or theorem. Its surviving formal content reduces to a configuration of established objects:

\[
\boxed{
\text{ASA}
=
\text{typed attributed temporal graph}
+
\text{guarded path query}
+
\text{graph vitality functional}
+
\text{standard statistical controls}
+
\text{governance policy}
}
\]

Pure graph theory does **not** contain everything the ASA documents ask for. A graph alone does not supply empirical semantics, calibrated belief, observation models, utilities, causal intervention meaning, strategic incentives, or governance authority. That does not save ASA. Those missing pieces already belong to mature adjacent fields: knowledge representation, statistics, causal inference, database theory, decision theory, game theory, cryptography, and access-control theory. ASA combines them without adding a new mathematical solution.

The repository's explicit novelty claims N1–N5 all fail:

| Claim | Disposition | Decisive prior art |
|---|---|---|
| N1 — instance-level, physically conditioned path-composition gating | **Eliminated** | regular/data path queries, register automata, product automata, temporal/spatial/unit ontologies |
| N2 — standing/significance separation as a data-model invariant | **Eliminated** | normalized schemas, derived views/events, named graphs, provenance, validation schemas |
| N3 — abstention as a scored ranking output | **Eliminated exactly** | label ranking with partial abstention (2012), reject-option and selective-prediction theory |
| N4 — machine-enforced context preregistration | **Eliminated** | cryptographic commitments, trusted timestamps, registered reports, sealed holdouts |
| N5 — prohibition on fitting significance to the reasoning objective | **Eliminated** | experimental separation, holdout discipline, frozen scorers, dependency/provenance controls |

One proposition remains unresolved, but it is **not a novelty claim**:

> A particular frozen ASA estimator might outperform equal-information baselines on a held-out cross-context transfer benchmark.

That is an empirical performance hypothesis. It has no supporting result in the reviewed record. If it fails, ASA contributes neither novelty nor demonstrated utility. If it succeeds, the result would establish performance of one configured system, not invention of its constituent mathematics.

---

## 1. Scope and adverse assumptions

### 1.1 Missing target document

At the time of the initial adverse review, no file named `ASTRO-RESEARCH-0003` existed in the reviewed checkout. The report therefore reconstructed its target claims from:

1. the immediately preceding graph-theory review in this research sequence;
2. the explicit N1–N5 novelty register in `ASTRO-RESEARCH-0001`;
3. every architectural decision and revised hypothesis in `ASTRO-RESEARCH-0002`; and
4. the remaining empirical claim in the proposed minimum ASA disproof experiment.

This is a material provenance limitation. It is handled adversely to ASA: the review includes the broader Version 1 claim set rather than treating the absent document as permission to omit difficult claims.

**Version 1 freeze reconciliation, 2026-08-01.** `ASTRO-RESEARCH-0003` subsequently entered canonical `main`. It explicitly withdraws new graph mathematics, significance-before-reasoning as an architecture, and broad significance-first intelligence; it treats instance-level composition validity as an open empirical question rather than established novelty. Reinspection against that document changes no prior-art disposition. The canonical `ASTRO-EXP-0001@1.0` removes the composition track and leaves one bounded cross-context performance claim. The original chronology above remains recorded so the review sequence is not silently rewritten.

### 1.2 Standard of review

The test used here is not “can an ASA-specific phrase be found verbatim?” It is:

> After replacing ASA vocabulary by mathematical vocabulary, is the claimed object, operation, invariant, or experimental control already known?

Changing the domain predicates from `price` and `date` to `frame`, `epoch`, `band`, `unit`, and `model-family` does not create a new automaton. Calling node vitality “counterfactual significance” does not create a new graph functional. Combining known controls does not create a new theory unless the combination yields a new formally stated property with evidence or proof. No such property was found.

### 1.3 Confidence scale

| Label | Meaning |
|---|---|
| Very high | Exact mathematical subsumption or exact earlier formulation |
| High | Established construction with only application vocabulary changed |
| Medium | Strong analogue; exact system packaging may differ |
| Low | Literature coverage insufficient for a firm conclusion |

“Risk” means the risk that ASA would be overclaimed if the item were presented as novel.

---

## 2. Mathematical reduction

### 2.1 Data model

The most generous formalization of the ASA store is a typed, attributed, temporal, directed hypergraph

\[
G=(V,E,s,t,\lambda_V,\lambda_E,a_V,a_E,\tau,p),
\]

where vertices and edges have types, arbitrary attributes, validity time, and provenance. An n-ary assertion can be represented either as a hyperedge or as an assertion vertex connected by role-labelled incidence edges. The latter is the standard incidence/reification construction. Hypergraphs and their incidence bipartite graphs are classically equivalent representations; directed hypergraphs were already formalized for path and optimization problems by [Gallo et al. (1993)](https://doi.org/10.1016/0166-218X%2893%2990045-P). RDF n-ary relations prescribe the same reification pattern in a knowledge-representation setting ([W3C n-ary relations](https://www.w3.org/TR/swbp-n-aryRelations/)).

Property graphs already formalize labelled nodes and edges with properties ([Angles et al.](https://doi.org/10.1145/3104031)); typed attributed graphs and their transformations predate ASA by decades ([Ehrig et al.](https://journals.sagepub.com/doi/10.3233/FUN-2006-74103)). Nothing in the ASA entity/assertion/evidence distinction requires a new graph object.

### 2.2 Licensed traversal

Let each edge carry a label \(\lambda(e)\) and data signature \(\nu(e)\). ASA's licence is a transition system

\[
(q,r) \xrightarrow{e} (q',r')
\]

defined only when:

1. the relationship label is accepted by a finite automaton; and
2. a guard \(P(r,\nu(e))\) over stored values succeeds.

The register \(r\) can retain the previous edge signature or a composed signature. A graph search then runs on the product state space

\[
V \times Q \times R.
\]

This is a guarded/register automaton over a data path. Regular path queries were already standard graph-database theory; regular path queries with comparisons over values stored along a path were formalized by [Libkin and Vrgoč](https://homepages.inf.ed.ac.uk/libkin/papers/icdt12b.pdf), and binding/register formalisms were developed explicitly for graph databases by [Libkin, Tan, and Vrgoč](https://www.research.ed.ac.uk/en/publications/regular-expressions-with-binding-over-data-words-for-querying-gra/). The older regular-path foundation appears in [Mendelzon and Wood](https://doi.org/10.1137/S009753979122370X).

The important correction is that an accepted-path language is generally **not an ordinary subgraph** \(G_C\). Whether an edge is allowed can depend on automaton/register state. The established object is the product graph or automaton run. ASA's `G_C` notation hides this state dependence; it does not create a new graph.

Frames, intervals, coordinate systems, and dimensions merely instantiate the guards. Their representational prior art includes [OWL-Time](https://www.w3.org/TR/owl-time/), [OGC GeoSPARQL](https://www.ogc.org/standards/geosparql/), [QUDT](https://www.qudt.org/pages/QUDToverviewPage.html), and the [Ontology of Units of Measure](https://research.wur.nl/en/publications/ontology-of-units-of-measure-and-related-concepts/). Dimensional compatibility itself is much older than graph databases ([Buckingham, 1914](https://doi.org/10.1103/PhysRev.4.345)).

### 2.3 “Counterfactual significance”

For a declared graph functional \(F_C\), metric \(d_C\), and withdrawal operator \(W_{C,v}\), ASA defines

\[
\sigma_C(v)=d_C\!\left(F_C(G),F_C(W_{C,v}(G))\right).
\]

This is exactly a **vitality index**: node importance is the change in a graph invariant or functional caused by removal. The most-vital-node problem was formalized for flow networks by [Corley and Chang (1974)](https://doi.org/10.1287/mnsc.21.3.362). The general definition—deleting a node or edge and measuring change in a graph invariant—is explicit in induced/vitality centrality ([Everett and Borgatti, 2010](https://doi.org/10.1016/j.socnet.2010.06.004)). The equivalence between vitality indices and induced Shapley-style game-theoretic centralities was proved by [Skibski (2021)](https://www.ijcai.org/proceedings/2021/0056.pdf).

Outside graph theory, the same operation is leave-one-out influence or perturbation analysis. Cook's distance measures the effect of deleting an observation ([Cook, 1977](https://doi.org/10.1080/00401706.1977.10489493)); influence functions trace a prediction to influential training points ([Koh and Liang, 2017](https://proceedings.mlr.press/v70/koh17a.html)); linear response measures change under perturbation in physics ([Kubo, 1957](https://staff.ulsu.ru/moliver/ref/kubo/kubo57.pdf)); and interventions/counterfactuals have established causal semantics ([Pearl, 1995](https://doi.org/10.1093/biomet/82.4.669)).

The choice of \(F_C\), \(d_C\), and \(W_{C,v}\) is application specification. It can make the output meaningful, but it does not make the mathematical construction novel.

### 2.4 Abstention

An ASA output has the type

\[
Y \;\sqcup\;
\{\text{evidence},\text{licence},\text{selection}\}
\]

possibly with a reason record. This is a tagged sum type or reject option. It is not a new number and not a new logic. Partial functions returning “undefined” are classical; strong Kleene logic was designed around undefined values, and modern verification work uses it directly for partial functions ([Chechik et al.](https://www.cs.toronto.edu/~chechik/pubs/cvc04abstract.html)).

More decisively, ranking with abstention predates ASA exactly. [Cheng et al. (2012)](https://papers.neurips.cc/paper_files/paper/2012/hash/fe2d010308a6b3799a3d9c728ee74244-Abstract.html) allow a label ranker to abstain on uncertain pairwise comparisons and return a partial rather than total order. Reject cost and risk/coverage trade-offs originate at least with [Chow (1970)](https://doi.org/10.1109/TIT.1970.1054406) and selective classification is given a full risk/coverage treatment by [El-Yaniv and Wiener (2010)](https://jmlr.org/papers/v11/el-yaniv10a.html).

### 2.5 Selection, uncertainty, and transfer

The remaining quantitative machinery is standard statistics:

- unequal observation propensities and inverse-probability correction: [Horvitz and Thompson (1952)](https://doi.org/10.1080/01621459.1952.10483446);
- missingness mechanisms: [Rubin (1976)](https://www.ets.org/research/policy_research_reports/publications/article/1976/itce.html);
- non-random sample selection: [Heckman (1979)](https://doi.org/10.2307/1912352);
- propensity adjustment: [Rosenbaum and Rubin (1983)](https://dash.harvard.edu/entities/publication/73120378-852d-6bd4-e053-0100007fdf3b);
- calibration of probabilistic forecasts: [Brier (1950)](https://doi.org/10.1175/1520-0493%281950%29078%3C0001:VOFEIT%3E2.0.CO;2) and [Dawid (1982)](https://doi.org/10.1080/01621459.1982.10477856);
- distribution shift and domain adaptation: [Shimodaira (2000)](https://doi.org/10.1016/S0378-3758%2800%2900115-4) and [Ben-David et al.](https://research.google/pubs/analysis-of-representations-for-domain-adaptation/);
- invariance across environments: [Peters, Bühlmann, and Meinshausen (2016)](https://doi.org/10.1111/rssb.12167).

ASA neither strengthens these results nor relaxes their assumptions.

---

## 3. Requested field-by-field review

| Field | What existing work already supplies | What it definitely does not supply by itself | ASA result |
|---|---|---|---|
| Graph theory | paths, walks, reachability, centralities, automorphisms, cuts, flow, vitality under deletion | empirical meaning of labels; utilities; truth; observation mechanism | Core topology and deletion score are prior art |
| Property graphs | typed/labeled vertices and edges, arbitrary properties, graph schemas and queries | open-world semantics or justified belief | ASA storage model is an ordinary profile |
| Heterogeneous graphs | node/edge types, metapaths, type-specific transition patterns ([PathSim, 2011](https://www.vldb.org/pvldb/vol4/p992-sun.pdf)) | instance truth and physical validity without supplied predicates | ASA's schema-level licence is a metapath/regular-language restriction |
| Hypergraphs | n-ary relationships and incidence representations | endorsement, evidence quality, causation | ASA assertions can be hyperedges or reified nodes; no new expressivity |
| Temporal graphs/databases | time-indexed edges, temporal paths, valid time, transaction time, intervals | which clock/frame is scientifically correct | ASA validity intervals are bitemporal/temporal attributes ([Snodgrass and Ahn, 1985](https://doi.org/10.1145/318898.318921)) |
| Knowledge graphs | entity–relation representation, schema, identity, provenance, named contexts | automatic truth, calibrated confidence, strategic intent | ASA's evidence graph is a knowledge graph profile |
| RDF | triples, datasets/named graphs, reification/RDF-star-style assertion terms | closed-world validation and nonmonotonic acceptance by itself | Assertion/evidence separation is already representable |
| OWL | model-theoretic semantics, property chains, transitivity, disjointness, cardinality, keys | probabilistic calibration, closed-world data validation, defeasible belief | ASA type algebra does not exceed OWL plus external guards |
| SHACL | closed-world graph validation, node/property shapes, severities, reports, property paths | empirical correctness | “Standing” is substantially a SHACL-style validation result |
| Category theory | typed composition, functors, schemas-as-categories, data migration | domain truth, statistics, utilities | ASA states no new category, functor, universal property, or theorem |
| Random walks | diffusion, visitation, hitting/commute measures ([Aldous and Fill](https://www.stat.berkeley.edu/~aldous/RWG/book.html)) | semantic validity or causal meaning | Available baseline machinery only |
| PageRank/PPR | global, personalized, and topic-sensitive stationary rankings | calibrated counterfactual effect size | ASA's context anchor contains PPR as an acknowledged special case |
| GNNs | learned permutation-equivariant aggregation and graph representations | semantics, causal identification, reliable uncertainty without assumptions | ASA adds policy constraints, not a new GNN |
| Graph Attention | learned neighbor weighting before downstream aggregation | objective-independent meaning or calibrated significance | “significance before reasoning” is not distinctive |
| Argumentation/TMS | support, attack, justification, retraction, competing claims | direct access to world truth | ASA's support/contradiction layer is prior art |
| Database theory | normalization, constraints, views, provenance, regular data-path queries, temporal validity | physical interpretation of stored values | N1 and N2 collapse here |
| Physics | perturbation, response, sensitivity, dimensional analysis | choice of human objective in a multi-objective decision | ASA's withdrawal effect is finite perturbation/response |
| Decision theory | utility, expected value of information, action under uncertainty, reject costs | utility without a decision maker | ASA's context and actionable abstention import these constructs |
| Game theory | signaling, strategic communication, persuasion, reputation incentives | payoffs and priors absent from the model | ASA has no new deception or trust solution |

### 3.1 Category-theory claim specifically

Category theory is more general than ASA's typed composition. Database schemas have been modeled as categories, instances as functors, and migrations as functorial constructions by [Spivak](https://arxiv.org/abs/1009.1166). This can organize ASA's types and transformations, but ASA supplies no categorical result. Merely having partially composable typed arrows is not a novelty claim; it is the starting vocabulary of categories, semicategories, relations, and partial algebras.

### 3.2 GNN and GAT claim specifically

Graph neural networks learn functions of graph structure and attributes. Their message-passing expressiveness is bounded in known ways ([Xu et al.](https://arxiv.org/abs/1810.00826)). Graph Attention Networks learn neighbor weights as part of the downstream objective ([Veličković et al.](https://arxiv.org/abs/1710.10903)). ASA's prohibition on that fitting path is a design restriction, not a new learning architecture. A fixed, rule-based edge mask can be placed in front of any graph learner.

### 3.3 PageRank claim specifically

Personalization is not an ASA contribution. Topic-sensitive PageRank computes biased PageRank vectors and uses query context to produce query-specific importance ([Haveliwala, 2002](https://doi.org/10.1145/511446.511513)). Fully personalized PageRank was formalized and scaled by [Jeh and Widom (2003)](https://www.ra.ethz.ch/CDstore/www2003/papers/refereed/p185/html/p185-jeh.html). ASA can distinguish itself from PPR only by adding an externally declared estimand, selection model, and abstention policy. All three come from other prior art.

---

## 4. Destruction of the explicit novelty claims

### N1 — Instance-level, physically conditioned path-composition gating

**Existing work.** Regular path queries constrain edge-label sequences. Data-path queries and register automata additionally compare values stored at multiple positions along a graph path. Weighted automata/transducers carry and transform accumulated state. OWL-Time represents intervals and temporal relations; GeoSPARQL represents geometries and reference systems; QUDT/OM represent dimensions and units. SHACL evaluates instance-level predicates and produces validation results.

**Difference.** ASA chooses a particular register containing frame, epoch interval, band, model family, roles, dimension, and uncertainty. Those are domain fields supplied to established guards. The left-to-right evaluation order and monotone penalty are policy selections. No new closure result, expressiveness result, complexity result, or algorithm is stated.

**Evidence.** [Regular path queries on graphs with data](https://homepages.inf.ed.ac.uk/libkin/papers/icdt12b.pdf); [regular expressions with binding over data words](https://www.research.ed.ac.uk/en/publications/regular-expressions-with-binding-over-data-words-for-querying-gra/); [OWL-Time](https://www.w3.org/TR/owl-time/); [GeoSPARQL](https://www.ogc.org/standards/geosparql/); [OM units ontology](https://research.wur.nl/en/publications/ontology-of-units-of-measure-and-related-concepts/).

**Confidence.** Very high.

**Risk.** Critical. Continuing to call N1 a mathematical or graph-theoretic novelty is readily falsifiable by database-theory reviewers. At most, the exact field bundle could be described as an application profile.

**Verdict.** **Eliminated.**

### N2 — Standing/significance separation as a data-model invariant

**Existing work.** Relational normalization distinguishes base facts from derived views ([Codd, 1970](https://doi.org/10.1145/362384.362685)). RDF datasets and named graphs attach context to assertions; PROV-O represents entities, activities, derivations, agents, roles, and time ([W3C PROV-O](https://www.w3.org/TR/prov-o/)). SHACL emits validation results instead of mutating a resource into its validation score. Database provenance can annotate derivations algebraically ([Green, Karvounarakis, and Tannen, 2007](https://web.cs.ucdavis.edu/~green/papers/pods07.pdf)).

**Difference.** ASA prohibits an intrinsic `significance` column and permits a context-hashed derived event. That is an ordinary schema constraint and provenance convention. It creates no information-theoretic or database-theoretic property not already available.

**Evidence.** [Codd's relational model](https://doi.org/10.1145/362384.362685); [Named Graphs](https://doi.org/10.1145/1060745.1060835); [PROV-O](https://www.w3.org/TR/prov-o/); [provenance semirings](https://web.cs.ucdavis.edu/~green/papers/pods07.pdf); [SHACL](https://www.w3.org/TR/shacl/).

**Confidence.** Very high.

**Risk.** High. The claimed “structural incapability” of ranking is also mathematically false if interpreted literally. For finite or countable standing records, mappings into \(\mathbb R\) exist; support cardinality alone gives a ranking. The no-ranking rule is governance, not representational impossibility.

**Verdict.** **Eliminated.** “Standing” should be renamed validation status or removed if redundant.

### N3 — Abstention as a first-class ranking output

**Existing work.** Chow's reject rule prices abstention; selective prediction formalizes risk/coverage; Cheng et al. produce partial rankings by abstaining on uncertain pairwise comparisons.

**Difference.** ASA uses three reason codes and scores them in its benchmark. Reason codes are a tagged union; benchmark scoring is experimental design.

**Evidence.** [Chow (1970)](https://doi.org/10.1109/TIT.1970.1054406); [El-Yaniv and Wiener (2010)](https://jmlr.org/papers/v11/el-yaniv10a.html); [Cheng et al. (2012), *Label Ranking with Partial Abstention*](https://papers.neurips.cc/paper_files/paper/2012/hash/fe2d010308a6b3799a3d9c728ee74244-Abstract.html); [Mao, Mohri, and Zhong, *Ranking with Abstention*](https://arxiv.org/abs/2307.02035).

**Confidence.** Very high; the ranking-specific precedent is exact.

**Risk.** Critical if described as even a “small novelty.” It was published explicitly before ASA.

**Verdict.** **Eliminated exactly.**

### N4 — Machine-enforced context preregistration

**Existing work.** Registered Reports lock hypotheses and analyses before results ([Chambers, 2013](https://doi.org/10.1016/j.cortex.2012.12.016)). Cryptographic commitments provide binding commit–reveal ([Naor, 1991](https://research.ibm.com/publications/bit-commitment-using-pseudorandomness)). RFC 3161 time-stamps a collision-resistant hash to prove a datum existed before a time ([IETF RFC 3161](https://datatracker.ietf.org/doc/rfc3161/)). Reusable holdouts formally control adaptive analysis ([Dwork et al., 2015](https://doi.org/10.1126/science.aaa9375)).

**Difference.** ASA hashes a context record, stores the commitment, and copies its identifier into results. This is a direct composition of preregistration, commitment, timestamp, and provenance.

**Evidence.** The four sources above state every mechanism needed by N4.

**Confidence.** Very high.

**Risk.** High. A repository commit controlled by one operator is weaker than the cited cryptographic/trusted-time constructions. ASA's version is not only non-novel; without an independent witness it provides a weaker guarantee.

**Verdict.** **Eliminated.**

### N5 — Prohibition of fitting significance to the reasoning objective

**Existing work.** Train/test separation, frozen holdouts, preregistered analysis, causal design before outcome inspection, provenance, and access-control separation all restrict information flow. Dwork et al. formalize protection against adaptive holdout reuse. PROV-O records derivation and responsibility. NIST RBAC formalizes role and constraint-based authorization ([Sandhu, Ferraiolo, and Kuhn](https://www.nist.gov/publications/nist-model-role-based-access-control-towards-unified-standard)).

**Difference.** ASA forbids one edge in the computational dependency graph: downstream objective data may not update the significance parameters. That may be a useful audit rule, but a negative dependency constraint is not a new learner or theorem.

**Evidence.** [Reusable holdout](https://doi.org/10.1126/science.aaa9375); [PROV-O](https://www.w3.org/TR/prov-o/); [NIST RBAC](https://www.nist.gov/publications/nist-model-role-based-access-control-towards-unified-standard); Rubin's design-first argument ([2008 preprint](https://arxiv.org/abs/0811.1640)).

**Confidence.** High.

**Risk.** High if presented as learning-theoretic novelty. No bound, optimality result, or new hypothesis class follows from the prohibition.

**Verdict.** **Eliminated.** Retain only as an audit policy if operationally useful.

---

## 5. Complete Version 1 claim ledger

This table maps every architectural decision in `ASTRO-RESEARCH-0002`, including decisions never promoted to N1–N5.

| ASA item | Prior-art reduction | Novelty result |
|---|---|---|
| AD-01 standing is a three-state non-ordering gate | SHACL validation result + evidence set; three-valued/partial logic | None; “cannot be ranked” is policy, not structure |
| AD-02 no pre-context aggregate | absence of a materialized view; query-time computation | Negative restriction only |
| AD-03 probation/deletion criterion | feature ablation and model simplification | Experimental discipline, not theory |
| AD-04 validity signature | attributed temporal edge with spatial/unit/model metadata | Standard data model |
| AD-05 two-level partial composition | regular/data path query + register automaton + guards | N1 eliminated |
| AD-06 unlicensed composition gives \(\bot\), not zero | partial function totalized by an undefined/reject value | Classical |
| AD-07 frozen licence plus permissive/random controls | preregistration, negative/placebo control, ablation | Standard experimental design |
| AD-08 measures only on accepted paths | product-graph/automaton-constrained path computation | Established graph-query construction |
| AD-09′ identity, type, association, selection, calibration, contradiction, derivation | OWL/RDF/PROV, statistical and argumentation vocabularies | Vocabulary profile only |
| AD-09 counterfactual significance | graph vitality / leave-one-out influence / intervention response | Exact prior art |
| AD-10 dimensioned absolute output | dimensional analysis and quantity calculus | Standard scientific validity |
| AD-11 nonempty designation | query parameter / personalization vector / task definition | Standard contextual query |
| AD-12 designation-anchored paths | PPR/topic-sensitive PageRank/goal-directed reachability | Standard |
| AD-13 enumerated withdrawal semantics | intervention model and treatment-version specification | Necessary declaration, not new calculus |
| AD-17 detectability on entities/assertions | inclusion propensity / missingness metadata | Survey-statistics prior art |
| AD-18 selection correction or declared bias | Horvitz–Thompson, Heckman, propensity weighting, sensitivity analysis | Standard |
| AD-19 observability-only baseline and self-invalidation | negative control, confounding diagnostic, prespecified validity gate | Standard |
| AD-14 sealed context predictions | preregistration + commitment + timestamp + provenance | N4 eliminated |
| AD-15 one contract over many designations | parameterized query/template and out-of-sample validation | Standard generalization test |
| AD-16 external contexts, counter-contexts, expected failures | external validation, negative controls, adversarial/placebo benchmarks | Standard benchmark design |
| AD-20 typed abstentions | tagged union/reason-coded reject option | N3 eliminated |
| AD-21 abstention cost, budget, neutrality | selective risk/coverage + selection-bias diagnostics | Standard combination |
| AD-22 actionable abstention | expected value of information and active learning | Exact decision-theory precedent |
| AD-24 parameter provenance/no feedback | provenance DAG + information-flow restriction + frozen evaluation | N5 eliminated |
| AD-26 PPR as degenerate case | personalized/topic-sensitive PageRank | Correct containment, no novelty |
| AD-25 cross-context transfer and supervised anchor | domain adaptation, covariate shift, invariant prediction | Mature ML/statistics problem |
| AD-29 ground-truth tiers and anchor/oracle labels | validation-study design and measurement hierarchy | Terminology/policy |
| AD-27 operating envelope | model applicability domain and declared assumptions | Scientific reporting norm |
| AD-28 knob inventory, simple baseline, simplify on failure | model selection, ablation, parsimony | Scientific discipline |

### 5.1 Relationship taxonomy

The seven proposed “missing” relationships also have direct precedents:

| ASA relationship | Existing representation |
|---|---|
| identity / possible identity / distinction | OWL identity/difference, probabilistic entity resolution |
| classification / typing | RDF `rdf:type`, RDFS/OWL class membership |
| statistical association | ordinary attributed relation with estimator/provenance metadata |
| selection / censoring dependency | causal/selection diagrams and missing-data models |
| calibration dependency | PROV derivation/activity or a domain ontology property |
| contradiction / revision / supersession | abstract argumentation, bipolar support/attack, truth-maintenance systems, PROV revision |
| derivation / model input | PROV-O derivation and provenance semirings |

The underlying distinction between “a proposition exists” and “the proposition is accepted” is standard. RDF reification permits statements about a proposition without asserting it as an unqualified fact ([RDF 1.2 Concepts](https://www.w3.org/TR/rdf12-concepts/)). Truth-maintenance systems track justifications and revise dependent beliefs ([Doyle, 1979](https://doi.org/10.1016/0004-3702%2879%2990008-0)). Dung's argumentation framework formalizes attacks and acceptability ([Dung, 1995](https://doi.org/10.1016/0004-3702%2894%2900041-X)).

---

## 6. Where graph theory definitely does not solve the problem

These are real gaps in **pure graph theory**. They are not ASA novelties because established non-graph theories already formalize them.

### 6.1 Semantic interpretation

Let \(G\) be a labelled graph and let an interpretation be

\[
I=(D,\{R_\ell\}_{\ell\in L},\{f_a\}_{a\in A}),
\]

mapping labels to relations and attributes to quantities in a domain \(D\). The same syntactic graph can admit multiple non-isomorphic interpretations \(I_1,I_2\). No graph invariant chooses the empirically correct interpretation.

**Existing solution family:** RDF model theory, OWL direct semantics, description logics, domain ontologies.
**ASA difference:** supplies a domain vocabulary and guards; no new semantics.

### 6.2 Belief and calibration

A belief state requires at least a probability or evidence model, for example

\[
P(\theta\mid D) \propto P(D\mid\theta)P(\theta),
\]

or an alternative evidence calculus. Topology alone does not specify the prior, likelihood, dependence assumptions, or scoring rule.

**Existing solution family:** Bayesian inference, Dempster–Shafer theory, subjective logic, probabilistic graphical models, calibration theory. Subjective logic explicitly includes belief fusion, trust networks, and subjective Bayesian networks ([Jøsang, 2016](https://doi.org/10.1007/978-3-319-42337-1)).
**ASA difference:** none; uncertainty fields without an update rule are representation, not inference.

### 6.3 Truth, endorsement, and evidential access

Let \(w\) be a possible world and \(K_a(w)\) the worlds compatible with agent \(a\)'s evidence. A proposition \(\varphi\) can be stored as a node while any of the following differ:

\[
w\models\varphi,\qquad
K_a(w)\models\varphi,\qquad
a\text{ endorses }\varphi.
\]

Graph incidence does not collapse truth, knowledge, and endorsement into one relation. If two worlds induce the same accessible evidence graph but disagree on \(\varphi\), truth is not identifiable from that graph.

**Existing solution family:** model-theoretic semantics, epistemic logic, RDF assertion/reification, provenance, truth-maintenance systems, and formal argumentation.
**ASA difference:** it can record claims, sources, supports, and attacks, but provides no new truth criterion or access semantics.

### 6.4 Observation and selection

Let an unobserved target graph be \(G^*\), and let the observed graph satisfy

\[
G_{obs}\sim S(\,\cdot\mid G^*,Z).
\]

If inclusion probabilities are unknown, or are zero on part of the target population, distinct \(G^*\) can induce the same distribution of \(G_{obs}\). The inverse problem is then non-identifiable. No centrality corrects this automatically.

**Existing solution family:** sampling theory, missing-data mechanisms, sample-selection models, causal selection diagrams.
**ASA difference:** requires these models but does not derive or identify them.

### 6.5 Significance

An importance statement requires exogenous structure

\[
(C,F_C,d_C,W_C,U_C),
\]

where \(C\) names the task, \(F_C\) an outcome, \(d_C\) a discrepancy, \(W_C\) an intervention, and possibly \(U_C\) a utility. Without these, “importance” is underdetermined. Automorphic vertices cannot be distinguished by an isomorphism-invariant graph functional unless context breaks the symmetry.

**Existing solution family:** vitality indices, influence functions, sensitivity/response theory, causal inference, utility theory, value of information.
**ASA difference:** packages their arguments in a context contract.

### 6.6 Strategic deception and intent

A strategic communication model needs types, priors, messages, actions, utilities, and an equilibrium concept:

\[
\Gamma=(\Theta_S,\Theta_R,M,A,P,u_S,u_R).
\]

The communication graph does not determine these objects. Reliability estimated from past edges is not a solution to adversarial signaling.

**Existing solution family:** signaling and cheap-talk games ([Crawford and Sobel, 1982](https://doi.org/10.2307/1913390)), Bayesian persuasion ([Kamenica and Gentzkow, 2011](https://www.aeaweb.org/articles?id=10.1257%2Faer.101.6.2590)), trust/reputation systems.
**ASA difference:** no payoff, equilibrium, incentive, or adversarial-identifiability result is supplied.

### 6.7 Authority and governance

Authorization is a policy predicate

\[
\operatorname{permit}(actor,role,operation,object,state),
\]

not a topological fact. An edge can record an authorization, but topology cannot make it legitimate.

**Existing solution family:** RBAC, integrity models, policy languages. W3C ODRL represents permissions, prohibitions, duties, parties, assets, and constraints ([ODRL 2.2](https://www.w3.org/TR/odrl-model/)).
**ASA difference:** governance choices only.

### 6.8 Distributed time and merge

Replicated evidence needs a happens-before relation and a convergence/conflict rule. A typical state-based convergence condition uses a join-semilattice

\[
(S,\sqsubseteq,\sqcup), \qquad x\leftarrow x\sqcup y.
\]

A stored graph does not choose the partial order or merge policy.

**Existing solution family:** Lamport event order ([Lamport, 1978](https://doi.org/10.1145/359545.359563)), bitemporal databases, CRDTs ([Preguiça, Baquero, and Shapiro](https://arxiv.org/abs/1805.06358)).
**ASA difference:** none unless it states a new merge algebra, which the reviewed documents do not.

---

## 7. Revised hypotheses are not novelty claims

### H1′ — Context irreducibility

The mathematical core is elementary symmetry: an isomorphism-equivariant or invariant graph procedure assigns identical outputs to vertices in the same automorphism orbit unless extra data breaks the symmetry. Context-dependent PageRank and personalized search already add such extra data. H1′ may be empirically true for a selected benchmark, but it is not a new theorem as stated.

**Disposition:** prior art at the formal level; unresolved only as benchmark performance.

### H2′ — Relational counterfactual estimability

Once the target is \(d(F(G),F(W_v(G)))\), estimating it from graph features is an ordinary statistical learning/function-approximation problem. Vitality gives the exact graph form; influence and causal methods give approximation tools. Calibration is separately mature.

**Disposition:** no novelty. Whether a specific estimator is accurate is empirical.

### H3′ — Constraint value under transfer

This is a domain-generalization hypothesis: a constrained hypothesis class may transfer better than an unconstrained fitted class. Domain adaptation provides generalization bounds; invariant prediction tests stability across environments. No ASA bound, consistency theorem, or impossibility result is given.

**Disposition:** no novelty. This is the one material empirical wager still open.

---

## 8. Surviving claims

No mathematical novelty claim survives. Two narrower statements require precise treatment so they are not accidentally promoted into novelty.

### S1 — Frozen ASA may outperform baselines under cross-context transfer

**Existing work.** Domain adaptation, invariant prediction, covariate-shift correction, graph vitality, supervised counterfactual estimation, and constrained model classes.

**Difference.** A particular ASA policy bundle—licensed paths, declared withdrawal, selection correction, and typed abstention—would be evaluated together against equal-information baselines on a held-out context family. The exact frozen bundle may not previously have been evaluated.

**Evidence.** No result was found in the repository. `ASTRO-RESEARCH-0002` itself concedes that a supervised regressor will probably win in-distribution and may transfer equally well. The proposed disproof experiment is a preregistration, not evidence.

**Confidence.** Medium confidence that the proposition is genuinely unresolved; low confidence that ASA will obtain a practically important advantage.

**Risk.** Critical. A positive result could be misreported as architectural novelty. It would show only that this configured estimator performed better under the frozen protocol. A negative or tied result removes ASA's remaining utility claim.

**Classification.** **Survives only as an empirical hypothesis, not as prior-art-resistant novelty.**

### S2 — The exact ASA specification may be an unpublished integration profile

**Existing work.** Every constituent and every interface pattern is covered above.

**Difference.** The exact conjunction of field names, prohibitions, reason codes, and benchmark gates may be unique as a document identity.

**Evidence.** No earlier source with the identical ASA vocabulary was sought or required. Novelty of arbitrary conjunction is not established by absence of an identical document.

**Confidence.** Medium that the exact textual/profile combination is unique; very high that this does not establish mathematical novelty.

**Risk.** High. “No identical package found” is especially vulnerable to combination-of-prior-art and obviousness criticism and should not be advertised as research novelty.

**Classification.** **Possible specification originality only. No scientific novelty claim.**

---

## 9. Elimination decision

The prior-art search reaches the result the ASA programme was instructed to permit:

> **ASA contributes nothing beyond existing mathematics and disciplinary prior art at the conceptual level reviewed here.**

Its graph component is a typed attributed temporal graph queried by a guarded automaton. Its significance component is graph vitality or perturbation response. Its uncertainty, selection, calibration, abstention, transfer, provenance, preregistration, and governance components are imported intact from older fields. The remaining conjunction is an architecture profile, not a theory.

Accordingly:

1. Withdraw N1–N5 as novelty claims.
2. Do not replace them with “novel combination” language absent a new theorem or independently replicated result.
3. Delete “standing” as a conceptual layer unless it rejects something ordinary schema/provenance validation cannot reject.
4. Describe the composition mechanism as a guarded regular data-path query, not an ASA algebra.
5. Describe significance as a context-parameterized vitality/sensitivity estimate, not a new kind of significance.
6. Treat the cross-context benchmark as the sole remaining go/no-go test of utility.
7. If that test does not beat strong equal-information baselines, terminate the claim that ASA adds value.

This report does not preserve ASA. It reduces ASA to prior art plus one untested empirical wager.

---

## 10. Primary and authoritative evidence index

### Graphs, paths, and databases

- [Angles et al., *Foundations of Modern Query Languages for Graph Databases*](https://doi.org/10.1145/3104031)
- [Mendelzon and Wood, *Finding Regular Simple Paths in Graph Databases*](https://doi.org/10.1137/S009753979122370X)
- [Libkin and Vrgoč, *Regular Path Queries on Graphs with Data*](https://homepages.inf.ed.ac.uk/libkin/papers/icdt12b.pdf)
- [Libkin, Tan, and Vrgoč, *Regular Expressions with Binding over Data Words for Querying Graph Databases*](https://www.research.ed.ac.uk/en/publications/regular-expressions-with-binding-over-data-words-for-querying-gra/)
- [Green, Karvounarakis, and Tannen, *Provenance Semirings*](https://web.cs.ucdavis.edu/~green/papers/pods07.pdf)
- [Codd, *A Relational Model of Data for Large Shared Data Banks*](https://doi.org/10.1145/362384.362685)
- [Snodgrass and Ahn, *A Taxonomy of Time in Databases*](https://doi.org/10.1145/318898.318921)

### Semantic web and ontology

- [RDF 1.2 Concepts and Abstract Syntax](https://www.w3.org/TR/rdf12-concepts/)
- [OWL 2 Direct Semantics](https://www.w3.org/TR/owl2-direct-semantics/)
- [SHACL](https://www.w3.org/TR/shacl/)
- [PROV-O](https://www.w3.org/TR/prov-o/)
- [OWL-Time](https://www.w3.org/TR/owl-time/)
- [OGC GeoSPARQL](https://www.ogc.org/standards/geosparql/)
- [ODRL 2.2](https://www.w3.org/TR/odrl-model/)

### Vitality, influence, physics, and causality

- [Corley and Chang, *Finding the n Most Vital Nodes in a Flow Network*](https://doi.org/10.1287/mnsc.21.3.362)
- [Everett and Borgatti, *Induced, Endogenous and Exogenous Centrality*](https://doi.org/10.1016/j.socnet.2010.06.004)
- [Skibski, *Vitality Indices are Equivalent to Induced Game-Theoretic Centralities*](https://www.ijcai.org/proceedings/2021/0056.pdf)
- [Cook, *Detection of Influential Observation in Linear Regression*](https://doi.org/10.1080/00401706.1977.10489493)
- [Koh and Liang, *Understanding Black-box Predictions via Influence Functions*](https://proceedings.mlr.press/v70/koh17a.html)
- [Kubo, *Statistical-Mechanical Theory of Irreversible Processes I*](https://staff.ulsu.ru/moliver/ref/kubo/kubo57.pdf)
- [Pearl, *Causal Diagrams for Empirical Research*](https://doi.org/10.1093/biomet/82.4.669)
- [Buckingham, *On Physically Similar Systems*](https://doi.org/10.1103/PhysRev.4.345)

### Selection, calibration, abstention, and decisions

- [Horvitz and Thompson, unequal-probability sampling](https://doi.org/10.1080/01621459.1952.10483446)
- [Rubin, *Inference and Missing Data*](https://www.ets.org/research/policy_research_reports/publications/article/1976/itce.html)
- [Heckman, *Sample Selection Bias as a Specification Error*](https://doi.org/10.2307/1912352)
- [Brier, probability-forecast verification](https://doi.org/10.1175/1520-0493%281950%29078%3C0001:VOFEIT%3E2.0.CO;2)
- [Chow, *On Optimum Recognition Error and Reject Tradeoff*](https://doi.org/10.1109/TIT.1970.1054406)
- [Cheng et al., *Label Ranking with Partial Abstention*](https://papers.neurips.cc/paper_files/paper/2012/hash/fe2d010308a6b3799a3d9c728ee74244-Abstract.html)
- [Howard, *Information Value Theory*](https://doi.org/10.1109/TSSC.1966.300074)
- [Peters, Bühlmann, and Meinshausen, invariant prediction](https://doi.org/10.1111/rssb.12167)

### Governance, commitment, and distributed state

- [Naor, *Bit Commitment Using Pseudorandomness*](https://research.ibm.com/publications/bit-commitment-using-pseudorandomness)
- [IETF RFC 3161 Time-Stamp Protocol](https://datatracker.ietf.org/doc/rfc3161/)
- [Dwork et al., *The Reusable Holdout*](https://doi.org/10.1126/science.aaa9375)
- [NIST Role-Based Access Control Model](https://www.nist.gov/publications/nist-model-role-based-access-control-towards-unified-standard)
- [Lamport, *Time, Clocks, and the Ordering of Events in a Distributed System*](https://doi.org/10.1145/359545.359563)
- [Preguiça, Baquero, and Shapiro, *Conflict-free Replicated Data Types*](https://arxiv.org/abs/1805.06358)

---

*End of ASTRO-PRIOR-ART-0001. No reviewed ASA novelty claim survives. One empirical performance hypothesis remains untested.*
