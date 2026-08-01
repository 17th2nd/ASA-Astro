# ASTRO-CLAIMS-0001 — Canonical Scientific Claims Registry

| Registry field | Value |
|---|---|
| Registry identifier | `ASTRO-CLAIMS-0001` |
| Title | Canonical Scientific Claims Registry |
| Programme | Adaptive Significance Architecture — Astronomy Validation Programme |
| Version | `1.0` — Version 1 freeze |
| Status | Frozen Version 1 canonical claim-status register |
| Effective date | 2026-08-01 |
| Scope | Scientific, mathematical, empirical, and scientific-novelty claims within ASA-Astro |
| Authority boundary | Registration records claim identity and status; it does not establish empirical truth, validate ASA, or exercise authority over ASA generally. |
| Protocol dependency | [`ASTRO-EXP-0001@1.0`](../../validation/benchmarks/ASTRO-EXP-0001.md) |
| Results dependency | [`ASTRO-RESULTS-0001@1.0`](../../validation/results/ASTRO-RESULTS-0001.md) |
| Supersession state | Initial canonical claims register; incorporates and status-preserves claims from the cited research drafts |
| Canonical location | `docs/claims/ASTRO-CLAIMS-0001.md` |
| Verification status | Verified for Version 1 freeze by [`ASTRO-V1-RESEARCH-CONTROLS-FREEZE-REPORT`](../../reports/ASTRO-V1-RESEARCH-CONTROLS-FREEZE-REPORT.md) |
| Empirical state | Experiments executed: `0`; empirical results: `0`; evidence level: `EH-0` |
| Permitted statuses | `Retained`, `Rejected`, `Untested`, `Open`, `Withdrawn` |
| Admission rule | A scientific claim has no programme standing until assigned an identifier and complete record here. |
| Citation rule | Every future paper must cite the claim identifier and this registry revision for every scientific claim it asserts, tests, rejects, or withdraws. |
| Exclusivity rule | No scientific claim may be maintained in a paper, experiment, architecture document, or review outside this registry. Amend this registry first. |
| History rule | Rejected and withdrawn claims remain registered; identifiers are never reused or deleted. |
| Validation rule | Registration, retention, rejection, or withdrawal is not an empirical result. Only `ASTRO-RESULTS-0001` events can record empirical evidence. |
| Confidence rule | Numeric confidence values are epistemic audit assessments of the stated claim or status, not observed frequencies, calibrated predictive probabilities, p-values, or empirical evidence. |

## Status definitions

| Status | Definition |
|---|---|
| `Retained` | Supported strongly enough to remain assertable within its stated scope. |
| `Rejected` | False, formally defective, or defeated as a novelty claim by existing evidence or prior art. |
| `Untested` | Precisely testable, but no decisive result is held. |
| `Open` | Not resolved and not yet stated tightly enough, or not yet equipped, for a decisive test. |
| `Withdrawn` | Removed from the active programme because it was superseded, over-broad, out of scope, or voluntarily abandoned. Withdrawal does not erase its history. |

## Evidence register

| Evidence identifier | Record |
|---|---|
| `SRC-001` | [ASTRO-RESEARCH-0001](../../09_Drafts/Claude/2026-08-01_Claude_Astronomy-Validation-Programme-Research-Report.md) |
| `SRC-002` | [ASTRO-RESEARCH-0002](../../09_Drafts/Claude/2026-08-01_Claude_ASTRO-RESEARCH-0002-Architectural-Revision.md) |
| `SRC-003` | [ASTRO-RESEARCH-0003](../../09_Drafts/Claude/2026-08-01_Claude_ASTRO-RESEARCH-0003-Convergence-Architecture.md) |
| `SRC-004` | [ASTRO-PRIOR-ART-0001](../../09_Drafts/Codex/2026-08-01_Codex_ASTRO-PRIOR-ART-0001.md) |
| `SRC-005` | [ASTRO-EXP-0001@1.0](../../validation/benchmarks/ASTRO-EXP-0001.md) |
| `SRC-006` | [Historical Minimum ASA Disproof Experiment](../../09_Drafts/Codex/2026-08-01_Codex_Minimum-ASA-Disproof-Experiment.md) |
| `SRC-007` | [ASTRO-RESULTS-0001@1.0](../../validation/results/ASTRO-RESULTS-0001.md) |
| `PA-001` | Angles et al., [*Foundations of Modern Query Languages for Graph Databases*](https://doi.org/10.1145/3104031); Ehrig et al., [typed attributed graph transformation](https://journals.sagepub.com/doi/10.3233/FUN-2006-74103) |
| `PA-002` | Gallo et al., [directed hypergraphs](https://doi.org/10.1016/0166-218X%2893%2990045-P); W3C, [n-ary relations](https://www.w3.org/TR/swbp-n-aryRelations/) |
| `PA-003` | Mendelzon and Wood, [regular paths](https://doi.org/10.1137/S009753979122370X); Libkin and Vrgoč, [regular path queries on graphs with data](https://homepages.inf.ed.ac.uk/libkin/papers/icdt12b.pdf); Libkin, Tan, and Vrgoč, [binding over data paths](https://www.research.ed.ac.uk/en/publications/regular-expressions-with-binding-over-data-words-for-querying-gra/) |
| `PA-004` | W3C [RDF](https://www.w3.org/TR/rdf12-concepts/), [OWL 2](https://www.w3.org/TR/owl2-direct-semantics/), [SHACL](https://www.w3.org/TR/shacl/), [PROV-O](https://www.w3.org/TR/prov-o/), and [OWL-Time](https://www.w3.org/TR/owl-time/); OGC [GeoSPARQL](https://www.ogc.org/standards/geosparql/); [QUDT](https://www.qudt.org/pages/QUDToverviewPage.html) |
| `PA-005` | Corley and Chang, [most vital nodes](https://doi.org/10.1287/mnsc.21.3.362); Everett and Borgatti, [vitality centrality](https://doi.org/10.1016/j.socnet.2010.06.004); Skibski, [vitality indices](https://www.ijcai.org/proceedings/2021/0056.pdf); Cook, [deletion influence](https://doi.org/10.1080/00401706.1977.10489493) |
| `PA-006` | Cheng et al., [label ranking with partial abstention](https://papers.neurips.cc/paper_files/paper/2012/hash/fe2d010308a6b3799a3d9c728ee74244-Abstract.html); Chow, [reject option](https://doi.org/10.1109/TIT.1970.1054406); El-Yaniv and Wiener, [selective classification](https://jmlr.org/papers/v11/el-yaniv10a.html) |
| `PA-007` | Haveliwala, [topic-sensitive PageRank](https://doi.org/10.1145/511446.511513); Jeh and Widom, [personalized PageRank](https://www.ra.ethz.ch/CDstore/www2003/papers/refereed/p185/html/p185-jeh.html) |
| `PA-008` | Veličković et al., [Graph Attention Networks](https://arxiv.org/abs/1710.10903); Xu et al., [message-passing GNN expressiveness](https://arxiv.org/abs/1810.00826) |
| `PA-009` | Horvitz and Thompson, [unequal-probability sampling](https://doi.org/10.1080/01621459.1952.10483446); Rubin, [missing data](https://www.ets.org/research/policy_research_reports/publications/article/1976/itce.html); Heckman, [sample selection](https://doi.org/10.2307/1912352); Brier, [forecast calibration](https://doi.org/10.1175/1520-0493%281950%29078%3C0001:VOFEIT%3E2.0.CO;2) |
| `PA-010` | Pearl, [interventions and causal diagrams](https://doi.org/10.1093/biomet/82.4.669); Howard, [information value theory](https://doi.org/10.1109/TSSC.1966.300074); Buckingham, [dimensional analysis](https://doi.org/10.1103/PhysRev.4.345) |
| `PA-011` | Naor, [bit commitment](https://research.ibm.com/publications/bit-commitment-using-pseudorandomness); IETF [RFC 3161](https://datatracker.ietf.org/doc/rfc3161/); Dwork et al., [reusable holdout](https://doi.org/10.1126/science.aaa9375) |
| `PA-012` | Spivak, [functorial data migration](https://arxiv.org/abs/1009.1166) |
| `PA-013` | Snodgrass and Ahn, [time in databases](https://doi.org/10.1145/318898.318921); Green, Karvounarakis, and Tannen, [provenance semirings](https://web.cs.ucdavis.edu/~green/papers/pods07.pdf) |
| `PA-014` | Lamport, [distributed time](https://doi.org/10.1145/359545.359563); Preguiça, Baquero, and Shapiro, [CRDTs](https://arxiv.org/abs/1805.06358); NIST, [role-based access control](https://www.nist.gov/publications/nist-model-role-based-access-control-towards-unified-standard) |

## Retained

### ASTRO-CLM-0001

- **Identifier:** `ASTRO-CLM-0001`
- **Claim:** No defensible mathematical novelty remains in ASA as reviewed.
- **Supporting evidence:** `SRC-004`; exact reductions in `PA-001`–`PA-014` cover every reviewed graph, query, vitality, abstention, selection, decision, commitment, and governance constituent.
- **Contradicting evidence:** No new graph object, invariant, calculus, algorithm, complexity result, universal property, or theorem is stated in `SRC-001`–`SRC-003`.
- **Current status:** `Retained`
- **Confidence:** Very high (`0.98`).
- **Dependencies:** `ASTRO-CLM-0002`, `ASTRO-CLM-0004`–`ASTRO-CLM-0008`, `ASTRO-CLM-0024`–`ASTRO-CLM-0028`.
- **Future experiment:** None required for the present corpus; repeat prior-art review only after a new formal claim is registered.
- **Possible falsifier:** A precise ASA theorem, algorithm, or mathematical object with a proved property not subsumed by the cited prior art.
- **Possible confirmation:** Independent formal review reproduces every reduction and finds no residual formal claim.

### ASTRO-CLM-0002

- **Identifier:** `ASTRO-CLM-0002`
- **Claim:** The reviewed ASA formal core reduces to a typed attributed temporal graph, a guarded data-path query, a vitality or perturbation functional, standard statistical controls, and governance policy.
- **Supporting evidence:** `SRC-004`; `PA-001`, `PA-003`, `PA-005`, `PA-009`, `PA-011`, `PA-014`.
- **Contradicting evidence:** The exact ASA field bundle may be document-specific, but no extra mathematical operator has been identified.
- **Current status:** `Retained`
- **Confidence:** Very high (`0.98`).
- **Dependencies:** `ASTRO-CLM-0004`–`ASTRO-CLM-0006`.
- **Future experiment:** Formalize any future ASA revision and construct an explicit semantics-preserving translation into or out of this reduction.
- **Possible falsifier:** A required ASA operation that cannot be expressed by the reduction and is formally defined in the registry.
- **Possible confirmation:** A bidirectional encoding preserving all registered ASA observables and decisions.

### ASTRO-CLM-0003

- **Identifier:** `ASTRO-CLM-0003`
- **Claim:** Pure graph theory does not determine empirical meaning, calibrated belief, observation mechanisms, utilities, causal intervention semantics, strategic incentives, governance authority, or distributed merge policy; established adjacent fields already address those requirements.
- **Supporting evidence:** `SRC-004` §§3 and 6; `PA-004`, `PA-009`, `PA-010`, `PA-011`, `PA-014`.
- **Contradicting evidence:** Graph-labelled formalisms can encode outputs from these fields, but encoding does not derive their semantics or assumptions from adjacency alone.
- **Current status:** `Retained`
- **Confidence:** Very high (`0.97`).
- **Dependencies:** None.
- **Future experiment:** State an alleged graph-only derivation and test it on two isomorphic graphs assigned different empirical interpretations, utilities, or observation models.
- **Possible falsifier:** A graph-theoretic construction that uniquely derives one of these external quantities from graph structure without added interpretation or assumptions.
- **Possible confirmation:** Isomorphic graphs support incompatible valid empirical interpretations or decision utilities while every graph invariant remains unchanged.

### ASTRO-CLM-0004

- **Identifier:** `ASTRO-CLM-0004`
- **Claim:** ASA entities, assertions, evidence, provenance, attributes, types, and validity intervals are representable by established property graphs, temporal knowledge graphs, or reified directed hypergraphs.
- **Supporting evidence:** `PA-001`, `PA-002`, `PA-004`, `PA-013`; `SRC-004` §2.1.
- **Contradicting evidence:** No ASA data item requiring greater representational expressivity is registered.
- **Current status:** `Retained`
- **Confidence:** Very high (`0.99`).
- **Dependencies:** None.
- **Future experiment:** Encode the complete ASA schema in each of the three established representations and verify lossless round trips.
- **Possible falsifier:** A registered ASA assertion whose arity, attributes, time, provenance, or role structure cannot be represented losslessly.
- **Possible confirmation:** Lossless translations preserve all registered queries and constraints.

### ASTRO-CLM-0005

- **Identifier:** `ASTRO-CLM-0005`
- **Claim:** Instance-level path licensing by relation type, frame, epoch, interval, unit, model family, role, calibration, and evidence dependence is an established guarded data-path or register-automaton problem over a product state space.
- **Supporting evidence:** `PA-003`, `PA-004`; `SRC-004` §§2.2 and 4 N1.
- **Contradicting evidence:** ASA selects a particular register and guard bundle, but states no new expressiveness, closure, complexity, or algorithmic result.
- **Current status:** `Retained`
- **Confidence:** Very high (`0.98`).
- **Dependencies:** `ASTRO-CLM-0004`.
- **Future experiment:** Compile the frozen ASA licence into a register automaton and compare accepted paths and terminal states exhaustively on a finite fixture.
- **Possible falsifier:** A licensed ASA traversal whose acceptance requires an operation outside the expressiveness of the stated guarded-path model.
- **Possible confirmation:** Equality of accepted path languages and composed signatures on exhaustive fixtures.

### ASTRO-CLM-0006

- **Identifier:** `ASTRO-CLM-0006`
- **Claim:** A score of the form \(d(F(G),F(W_v(G)))\) is graph vitality, deletion influence, perturbation response, or an intervention effect, not a new ASA significance calculus.
- **Supporting evidence:** `PA-005`, `PA-010`; `SRC-004` §2.3.
- **Contradicting evidence:** ASA supplies context-specific choices of \(F\), \(d\), and \(W_v\), but those choices specify an application rather than a new mathematical form.
- **Current status:** `Retained`
- **Confidence:** Very high (`0.99`).
- **Dependencies:** None.
- **Future experiment:** Map every registered ASA counterfactual score to its corresponding vitality, sensitivity, influence, or causal-intervention formulation.
- **Possible falsifier:** A registered ASA counterfactual operator with semantics not expressible as a factual–counterfactual functional comparison.
- **Possible confirmation:** Exact equality between the ASA score and an established vitality or response functional for all admissible inputs.

### ASTRO-CLM-0007

- **Identifier:** `ASTRO-CLM-0007`
- **Claim:** Physical-effect significance, decision significance, and information significance are distinct estimands and are not interchangeable measurements of one latent scalar.
- **Supporting evidence:** `SRC-003` C-03; `PA-005` and `PA-010` give different mathematical targets for perturbation effect, regret or utility, and value of information.
- **Contradicting evidence:** A particular decision model may relate them, but only through declared utilities, priors, actions, and observation costs.
- **Current status:** `Retained`
- **Confidence:** High (`0.96`).
- **Dependencies:** `ASTRO-CLM-0003`.
- **Future experiment:** For a frozen system, vary utility and evidence cost while holding physical effect fixed, then test whether the three rankings diverge.
- **Possible falsifier:** A theorem proving universal order-equivalence of all three quantities without additional assumptions.
- **Possible confirmation:** A single controlled counterexample in which two quantities rank the same entities differently.

### ASTRO-CLM-0008

- **Identifier:** `ASTRO-CLM-0008`
- **Claim:** Within the retained programme, significance is a context-declared valuation of a factual–counterfactual contrast, not a context-free graph property.
- **Supporting evidence:** `SRC-003` C-04; `PA-005`, `PA-010`.
- **Contradicting evidence:** A context may select a conventional graph invariant as its outcome, but that selection is itself external context.
- **Current status:** `Retained`
- **Confidence:** High (`0.95`).
- **Dependencies:** `ASTRO-CLM-0006`, `ASTRO-CLM-0007`.
- **Future experiment:** Hold the graph fixed while changing the declared outcome, intervention, or utility; compare resulting valuations.
- **Possible falsifier:** A unique significance value derivable from graph structure alone for every admissible context.
- **Possible confirmation:** Two admissible contexts over the same graph yield different entity valuations.

### ASTRO-CLM-0009

- **Identifier:** `ASTRO-CLM-0009`
- **Claim:** Context is mathematically necessary whenever the target valuation distinguishes graph-automorphic entities or changes while the observed graph is fixed.
- **Supporting evidence:** `SRC-001` §6.1; permutation-invariant graph functions assign identical values to nodes in the same automorphism orbit unless extra information breaks the symmetry.
- **Contradicting evidence:** Context is unnecessary for a target that is itself invariant under the same automorphisms.
- **Current status:** `Retained`
- **Confidence:** Very high (`0.98`).
- **Dependencies:** `ASTRO-CLM-0008`.
- **Future experiment:** Construct automorphic node pairs and preregister contexts that do and do not distinguish them.
- **Possible falsifier:** A context-free isomorphism-invariant function that separates nodes within one automorphism orbit.
- **Possible confirmation:** Proof by invariance, plus a context-dependent target assigning different values to the pair.

### ASTRO-CLM-0010

- **Identifier:** `ASTRO-CLM-0010`
- **Claim:** A deterministic Standing value computed only from the same graph cannot add epistemic information beyond that graph.
- **Supporting evidence:** `SRC-001` §5.4; `SRC-003` C-01; deterministic post-processing cannot increase information about an external target beyond its input.
- **Contradicting evidence:** Standing may add information if it imports independent observations, labels, priors, or human judgements, in which case the information is not graph-derived.
- **Current status:** `Retained`
- **Confidence:** Very high (`0.98`).
- **Dependencies:** None.
- **Future experiment:** Compare predictive information conditional on the full graph with and without a graph-deterministic Standing field.
- **Possible falsifier:** Positive conditional mutual information from a genuinely deterministic Standing field after conditioning on its complete graph input.
- **Possible confirmation:** Conditional information is zero, while gains appear only after adding external inputs.

### ASTRO-CLM-0011

- **Identifier:** `ASTRO-CLM-0011`
- **Claim:** Non-transitivity of an edge relation does not by itself make random walks, PageRank, betweenness, or other path-based graph measures mathematically or scientifically invalid when traversal is declared as diffusion, search, or exposure rather than logical composition.
- **Supporting evidence:** `SRC-003` C-02 and RJ-1; random-walk and centrality theory routinely operates on non-transitive social and interaction relations.
- **Contradicting evidence:** Such measures remain scientifically uninterpretable when no traversal semantics is declared.
- **Current status:** `Retained`
- **Confidence:** Very high (`0.98`).
- **Dependencies:** `ASTRO-CLM-0012`.
- **Future experiment:** Compare diffusion predictions from a non-transitive network against observed propagation while separately testing invalid logical inferences.
- **Possible falsifier:** A proof that every meaningful path measure requires the underlying relation to be transitive.
- **Possible confirmation:** A validated diffusion model over a non-transitive relation.

### ASTRO-CLM-0012

- **Identifier:** `ASTRO-CLM-0012`
- **Claim:** A path measure with undeclared traversal semantics is scientifically underdetermined even when it is mathematically well defined.
- **Supporting evidence:** `SRC-003` C-02; `ASTRO-CLM-0003`.
- **Contradicting evidence:** A declared observable or generative process can supply the missing interpretation.
- **Current status:** `Retained`
- **Confidence:** High (`0.96`).
- **Dependencies:** `ASTRO-CLM-0003`.
- **Future experiment:** Apply the same path statistic to two plausible semantics with different observable consequences.
- **Possible falsifier:** A unique empirical interpretation entailed by the bare statistic and adjacency structure.
- **Possible confirmation:** Two incompatible empirical models induce the same graph statistic.

### ASTRO-CLM-0013

- **Identifier:** `ASTRO-CLM-0013`
- **Claim:** Physical composition validity requires supplied predicates about frames, epochs, dimensions, models, roles, calibration, and evidence dependence; graph topology alone cannot infer those predicates.
- **Supporting evidence:** `SRC-003` C-02; `PA-004`, `PA-010`.
- **Contradicting evidence:** Once supplied as attributes and rules, established graph-query and validation systems can evaluate them.
- **Current status:** `Retained`
- **Confidence:** Very high (`0.97`).
- **Dependencies:** `ASTRO-CLM-0003`, `ASTRO-CLM-0005`.
- **Future experiment:** Hold topology fixed and vary one physical-compatibility attribute; verify that admissibility changes only through the supplied predicate.
- **Possible falsifier:** Correct physical admissibility recovered uniquely from topology after all physical metadata is removed.
- **Possible confirmation:** Isomorphic attributed structures with different frame or unit assignments require different admissibility decisions.

### ASTRO-CLM-0014

- **Identifier:** `ASTRO-CLM-0014`
- **Claim:** A counterfactual effect intended for scientific calibration must retain the dimension of its declared outcome; within-run rank or max normalization destroys absolute calibration and cross-run comparability.
- **Supporting evidence:** `SRC-002` AD-10; `SRC-003` C-07; `PA-010`.
- **Contradicting evidence:** Dimensionless normalization may be valid when the estimand itself is a declared dimensionless ratio and the denominator is fixed independently.
- **Current status:** `Retained`
- **Confidence:** High (`0.96`).
- **Dependencies:** `ASTRO-CLM-0008`.
- **Future experiment:** Compare calibration and cross-run error under dimensioned effects and within-run normalized ranks.
- **Possible falsifier:** A reconstruction theorem recovering every absolute effect from normalized ranks without retained scale information.
- **Possible confirmation:** Two runs with identical normalized ranks but materially different absolute effects.

### ASTRO-CLM-0015

- **Identifier:** `ASTRO-CLM-0015`
- **Claim:** Non-random observation or inclusion can distort graph topology, learned relationships, and significance estimates; correction requires a selection model or a scope-limiting declaration.
- **Supporting evidence:** `SRC-001` §§2.3 and 8.3; `SRC-002` AD-17–AD-19; `PA-009`.
- **Contradicting evidence:** The claim does not apply to a fixed, complete candidate set supplied identically to all methods, such as the registered Track A comparator set.
- **Current status:** `Retained`
- **Confidence:** Very high (`0.98`).
- **Dependencies:** None.
- **Future experiment:** Apply known censoring to simulated complete graphs and test bias before and after valid propensity correction.
- **Possible falsifier:** An estimator proved invariant to every selection mechanism in its declared class without modeling or assumptions.
- **Possible confirmation:** Controlled censoring changes topology-derived rankings and valid correction reduces the error.

### ASTRO-CLM-0016

- **Identifier:** `ASTRO-CLM-0016`
- **Claim:** Evidence adequacy thresholds depend on context-specific costs of false admission and false rejection and therefore are not generally context-free.
- **Supporting evidence:** `SRC-003` C-01; decision and reject-option theory in `PA-006` and `PA-010`.
- **Contradicting evidence:** Context-free well-formedness checks can reject malformed inputs independently of decision costs.
- **Current status:** `Retained`
- **Confidence:** High (`0.96`).
- **Dependencies:** `ASTRO-CLM-0007`.
- **Future experiment:** Hold evidence constant while varying preregistered error costs and calculate the Bayes-optimal admission threshold.
- **Possible falsifier:** A universally optimal threshold independent of all admissible loss functions.
- **Possible confirmation:** Different loss ratios yield different optimal decisions for the same posterior evidence.

### ASTRO-CLM-0017

- **Identifier:** `ASTRO-CLM-0017`
- **Claim:** Computing importance weights before downstream reasoning is not distinctive to ASA; graph attention already performs learned neighbour weighting before aggregation.
- **Supporting evidence:** `PA-008`; `SRC-001` §3.5; `SRC-002` AD-24; `SRC-003` C-09.
- **Contradicting evidence:** ASA may freeze or constrain weights differently, but that is a training and governance restriction rather than novelty in forward ordering.
- **Current status:** `Retained`
- **Confidence:** Very high (`0.99`).
- **Dependencies:** None.
- **Future experiment:** None; compare computational graphs and dependency order formally.
- **Possible falsifier:** A materially different registered ordering property absent from attention architectures.
- **Possible confirmation:** Direct mapping of the claimed order to an attention forward pass.

### ASTRO-CLM-0018

- **Identifier:** `ASTRO-CLM-0018`
- **Claim:** Query-, topic-, or designation-conditioned graph ranking predates ASA in personalized and topic-sensitive PageRank.
- **Supporting evidence:** `PA-007`; `SRC-004` §3.3.
- **Contradicting evidence:** PageRank does not by itself estimate a calibrated counterfactual effect, correct selection, or implement a declared abstention policy.
- **Current status:** `Retained`
- **Confidence:** Very high (`0.99`).
- **Dependencies:** None.
- **Future experiment:** Derive the ASA degenerate configuration and compare it numerically with personalized PageRank.
- **Possible falsifier:** A registered context-conditioning operation not expressible as or reducible to any known personalized graph query, together with a proved new property.
- **Possible confirmation:** Equality of scores under the permissive licence and PageRank-compatible transition policy.

### ASTRO-CLM-0019

- **Identifier:** `ASTRO-CLM-0019`
- **Claim:** Freezing a scoring rule against objective feedback is established experimental separation, holdout, provenance, and information-flow discipline, not new learning theory.
- **Supporting evidence:** `SRC-002` AD-24; `SRC-003` C-09; `SRC-004` N5; `PA-011`, `PA-013`.
- **Contradicting evidence:** A particular enforcement mechanism may be stronger or weaker, but no ASA generalization bound or new hypothesis class follows from the prohibition.
- **Current status:** `Retained`
- **Confidence:** Very high (`0.97`).
- **Dependencies:** None.
- **Future experiment:** Audit dependency graphs and sealed evaluation to test whether any objective-derived value reaches the scorer.
- **Possible falsifier:** A new formal learning result whose assumptions and conclusion arise uniquely from the ASA prohibition.
- **Possible confirmation:** Reduction of every ASA rule to known holdout, provenance, or noninterference controls.

### ASTRO-CLM-0020

- **Identifier:** `ASTRO-CLM-0020`
- **Claim:** A claimed incremental scientific contribution requires comparison with the strongest established equal-information method for the task; beating a straw baseline does not establish added value.
- **Supporting evidence:** `SRC-003` C-10; `SRC-005`; `SRC-006`.
- **Contradicting evidence:** A weak baseline may remain diagnostic, but cannot support the incremental claim.
- **Current status:** `Retained`
- **Confidence:** High (`0.95`).
- **Dependencies:** None.
- **Future experiment:** Run the frozen method against both weak and practitioner-grade comparators under identical inputs and cost.
- **Possible falsifier:** A valid inference rule showing that dominance over a strictly weaker comparator entails dominance over the strongest comparator.
- **Possible confirmation:** A method beats weak baselines but ties or loses to the practitioner-grade method.

### ASTRO-CLM-0021

- **Identifier:** `ASTRO-CLM-0021`
- **Claim:** Counterfactual ground truth produced by a declared scientific model is exact only within that model and does not establish truth about nature outside its assumptions.
- **Supporting evidence:** `SRC-005` Ground truth; `SRC-006`; `PA-010`.
- **Contradicting evidence:** Independent observational validation can support the model's external adequacy, but cannot convert conditional model truth into assumption-free truth.
- **Current status:** `Retained`
- **Confidence:** Very high (`0.98`).
- **Dependencies:** None.
- **Future experiment:** Validate the model against held-out observations and repeat the counterfactual under plausible alternative models.
- **Possible falsifier:** Proof that the declared model is complete and exact for nature over the claimed domain.
- **Possible confirmation:** Counterfactual effects change under observationally plausible alternative model specifications.

### ASTRO-CLM-0023

- **Identifier:** `ASTRO-CLM-0023`
- **Claim:** A finite matched-case corpus can demonstrate a concrete error class but cannot prove universal non-expressibility by an extensible standards stack.
- **Supporting evidence:** `SRC-003` Track B history; standard model-theoretic distinction between a counterexample to one configuration and a proof over all configurations.
- **Contradicting evidence:** A separate formal expressiveness proof could establish non-expressibility; the proposed finite experiment is not such a proof.
- **Current status:** `Retained`
- **Confidence:** Very high (`0.99`).
- **Dependencies:** `ASTRO-CLM-0040` as historical context only.
- **Future experiment:** Pair the empirical corpus with a formal expressiveness and reduction analysis of the frozen comparison language.
- **Possible falsifier:** A valid theorem showing that the finite corpus alone entails non-expressibility for every allowed extension.
- **Possible confirmation:** An ordinary added constraint eliminates the observed difference without changing the standards formalism.

## Rejected

### ASTRO-CLM-0024

- **Identifier:** `ASTRO-CLM-0024`
- **Claim:** N1 — instance-level physically conditioned path-composition gating is a novel ASA mathematical or graph-theoretic contribution.
- **Supporting evidence:** `SRC-001` reported an incomplete search and framed N1 as its narrowest candidate novelty.
- **Contradicting evidence:** `SRC-004` N1; guarded data paths, register automata, product automata, temporal and unit ontologies, and validation languages in `PA-003`–`PA-004` subsume the construction.
- **Current status:** `Rejected`
- **Confidence:** Very high (`0.98`).
- **Dependencies:** `ASTRO-CLM-0005`.
- **Future experiment:** None; reopening requires a formal property not expressible by the cited models.
- **Possible falsifier:** A prior-art-resistant formal operator, theorem, or complexity result unique to N1.
- **Possible confirmation:** Independent database-theory review maps every N1 operation to existing guarded-path machinery.

### ASTRO-CLM-0025

- **Identifier:** `ASTRO-CLM-0025`
- **Claim:** N2 — separation of Standing and significance as a data-model invariant is novel and makes Standing structurally incapable of ranking.
- **Supporting evidence:** `SRC-001` presented the separation as part of a claimed conjunction.
- **Contradicting evidence:** `SRC-004` N2; normalization, derived views, events, named graphs, provenance, and SHACL already provide the separation; finite or countable Standing records admit mappings to \(\mathbb R\).
- **Current status:** `Rejected`
- **Confidence:** Very high (`0.98`).
- **Dependencies:** `ASTRO-CLM-0010`, `ASTRO-CLM-0034`.
- **Future experiment:** None; any renewed claim must state a formal invariant and prove it is not policy alone.
- **Possible falsifier:** A proven representation theorem showing an ASA store prevents every ranking map while established stores cannot.
- **Possible confirmation:** Construction of a ranking from the supposedly non-orderable Standing record and a standard normalized-schema encoding.

### ASTRO-CLM-0026

- **Identifier:** `ASTRO-CLM-0026`
- **Claim:** N3 — abstention as a first-class ranking output is novel to ASA.
- **Supporting evidence:** `SRC-001` included it in the proposed novelty conjunction.
- **Contradicting evidence:** `SRC-004` N3; partial ranking with abstention is explicit in Cheng et al. 2012, with older reject-option and selective-prediction theory in `PA-006`.
- **Current status:** `Rejected`
- **Confidence:** Very high (`0.999`).
- **Dependencies:** None.
- **Future experiment:** None; novelty can be reopened only for a materially different formal output or guarantee.
- **Possible falsifier:** Evidence that the cited systems cannot express the registered ASA abstention type or decision rule.
- **Possible confirmation:** Exact encoding of ASA outputs as partial rankings or tagged reject options.

### ASTRO-CLM-0027

- **Identifier:** `ASTRO-CLM-0027`
- **Claim:** N4 — machine-enforced context preregistration is novel to ASA.
- **Supporting evidence:** `SRC-001` included it in the proposed novelty conjunction.
- **Contradicting evidence:** `SRC-004` N4; commitments, trusted timestamps, registered reports, and sealed holdouts in `PA-011` predate ASA and generally provide stronger guarantees.
- **Current status:** `Rejected`
- **Confidence:** Very high (`0.98`).
- **Dependencies:** None.
- **Future experiment:** None; compare guarantees of any proposed mechanism with commitment and trusted-time security definitions.
- **Possible falsifier:** A new preregistration security property achieved by ASA and absent from prior art.
- **Possible confirmation:** Formal reduction of ASA freezing to a weaker commitment or timestamp protocol.

### ASTRO-CLM-0028

- **Identifier:** `ASTRO-CLM-0028`
- **Claim:** N5 — prohibiting significance from being fitted to the reasoning objective is a novel learning-theoretic contribution.
- **Supporting evidence:** `SRC-001` identified this as the residue after conceding attention prior art.
- **Contradicting evidence:** `SRC-004` N5; frozen scorers, experimental separation, holdouts, provenance DAGs, and information-flow restrictions precede ASA; no new bound or hypothesis class is stated.
- **Current status:** `Rejected`
- **Confidence:** High (`0.97`).
- **Dependencies:** `ASTRO-CLM-0019`.
- **Future experiment:** None; reopening requires a new theorem or empirically distinctive guarantee.
- **Possible falsifier:** A registered learning result depending uniquely on the ASA restriction and not obtainable from standard sample separation.
- **Possible confirmation:** Every restriction translates to established holdout, provenance, or noninterference rules.

### ASTRO-CLM-0029

- **Identifier:** `ASTRO-CLM-0029`
- **Claim:** The exact conjunction N1–N5 establishes scientific or mathematical novelty even though each constituent is prior art.
- **Supporting evidence:** `SRC-001` proposed novelty in the conjunction of prohibitions.
- **Contradicting evidence:** `SRC-004` S2 and §9; no new emergent property, theorem, unexpected result, or independently replicated effect follows from the conjunction.
- **Current status:** `Rejected`
- **Confidence:** High (`0.96`).
- **Dependencies:** `ASTRO-CLM-0024`–`ASTRO-CLM-0028`.
- **Future experiment:** State and test a non-additive property of the conjunction against all proper-subset ablations.
- **Possible falsifier:** A proved or replicated effect that arises from the conjunction and cannot be obtained from the constituent prior art.
- **Possible confirmation:** Full and subset ablations show no unique conjunction effect, or the conjunction is a straightforward integration profile.

### ASTRO-CLM-0030

- **Identifier:** `ASTRO-CLM-0030`
- **Claim:** ASA introduces a new graph class, invariant, path problem, centrality, query language, category-theoretic object, or theorem.
- **Supporting evidence:** No precise object or theorem is stated in the reviewed sources.
- **Contradicting evidence:** `SRC-004` §§2–5; `PA-001`–`PA-005`, `PA-012`.
- **Current status:** `Rejected`
- **Confidence:** Very high (`0.99`).
- **Dependencies:** `ASTRO-CLM-0001`, `ASTRO-CLM-0002`.
- **Future experiment:** None until a candidate formal statement is registered.
- **Possible falsifier:** A peer-verifiable ASA definition and theorem not reducible to prior art.
- **Possible confirmation:** Complete translation of all ASA formal operations to cited constructions.

### ASTRO-CLM-0031

- **Identifier:** `ASTRO-CLM-0031`
- **Claim:** Graph theory alone already contains everything ASA requires.
- **Supporting evidence:** Graph theory contains the topology, walks, centralities, automorphisms, flows, and vitality operations.
- **Contradicting evidence:** `ASTRO-CLM-0003`; semantics, belief, selection, utility, intervention meaning, incentives, authority, and merge policy require external structures and assumptions.
- **Current status:** `Rejected`
- **Confidence:** Very high (`0.98`).
- **Dependencies:** `ASTRO-CLM-0003`.
- **Future experiment:** Attempt a graph-only derivation for each listed external quantity under isomorphic reinterpretations.
- **Possible falsifier:** A complete graph-theoretic semantics deriving every listed quantity without external assumptions.
- **Possible confirmation:** Any pair of isomorphic graphs with different valid empirical meanings, utilities, or observation processes.

### ASTRO-CLM-0032

- **Identifier:** `ASTRO-CLM-0032`
- **Claim:** ASA supplies a novel mathematical solution to the semantic, probabilistic, causal, decision, strategic, governance, or distributed-systems gaps left by pure graph theory.
- **Supporting evidence:** ASA documents name policies and fields touching these gaps.
- **Contradicting evidence:** `SRC-004` §6; `PA-004`, `PA-009`–`PA-014`; ASA states no new semantics, inference rule, identification theorem, equilibrium concept, authorization model, or merge algorithm.
- **Current status:** `Rejected`
- **Confidence:** Very high (`0.97`).
- **Dependencies:** `ASTRO-CLM-0003`.
- **Future experiment:** Register a precise gap-specific theorem or algorithm and compare it with the relevant field's prior art.
- **Possible falsifier:** A demonstrably new solution with a proved property or replicated advantage.
- **Possible confirmation:** Every ASA field delegates the substantive operation to an established external method or leaves it unspecified.

### ASTRO-CLM-0033

- **Identifier:** `ASTRO-CLM-0033`
- **Claim:** The paths accepted by an instance-state-dependent ASA licence generally form an ordinary subgraph \(G_C\) of the original graph.
- **Supporting evidence:** `SRC-002` AD-08 used licensed-subgraph notation.
- **Contradicting evidence:** `SRC-004` §2.2; acceptance may depend on automaton and register history, so the established object is a product graph or accepting run, not an edge-induced subgraph of the original graph.
- **Current status:** `Rejected`
- **Confidence:** Very high (`0.98`).
- **Dependencies:** `ASTRO-CLM-0005`.
- **Future experiment:** Construct two visits to the same edge under different register states and compare admissibility.
- **Possible falsifier:** Proof that every ASA guard is memoryless and depends only on the current edge and context.
- **Possible confirmation:** One edge is admissible after one prefix and inadmissible after another.

### ASTRO-CLM-0034

- **Identifier:** `ASTRO-CLM-0034`
- **Claim:** A Standing representation can be made structurally incapable of supporting any ranking.
- **Supporting evidence:** `SRC-002` AD-01 intended Standing to be unordered.
- **Contradicting evidence:** `SRC-004` N2; any finite or countable record can be mapped into an order, and support cardinality alone can rank many records. Non-ranking is policy, not structural impossibility.
- **Current status:** `Rejected`
- **Confidence:** Very high (`0.99`).
- **Dependencies:** None.
- **Future experiment:** Explicitly construct ranking maps over every proposed Standing record type.
- **Possible falsifier:** A formal type with a proof that no nonconstant map to any ordered set exists under the allowed operations.
- **Possible confirmation:** A permitted program computes a nonconstant scalar or ordering from the record.

### ASTRO-CLM-0035

- **Identifier:** `ASTRO-CLM-0035`
- **Claim:** Counterfactual significance is a new ASA graph functional.
- **Supporting evidence:** Earlier ASA framing named the functional as a distinctive layer.
- **Contradicting evidence:** `ASTRO-CLM-0006`; `PA-005`, `PA-010` establish vitality, influence, response, and intervention forms.
- **Current status:** `Rejected`
- **Confidence:** Very high (`0.99`).
- **Dependencies:** `ASTRO-CLM-0006`.
- **Future experiment:** None unless a different functional is registered.
- **Possible falsifier:** A counterfactual-significance operation not representable as established vitality, influence, sensitivity, or intervention response.
- **Possible confirmation:** Algebraic identity with a cited prior-art functional.

### ASTRO-CLM-0036

- **Identifier:** `ASTRO-CLM-0036`
- **Claim:** Path-based centrality is semantically invalid on every graph whose relations are mostly non-transitive.
- **Supporting evidence:** `SRC-001` §5.5 and `SRC-002` INV-08 asserted the over-broad form.
- **Contradicting evidence:** `SRC-003` C-02 and RJ-1; diffusion, exposure, and search semantics remain meaningful over non-transitive relations.
- **Current status:** `Rejected`
- **Confidence:** Very high (`0.99`).
- **Dependencies:** `ASTRO-CLM-0011`, `ASTRO-CLM-0012`.
- **Future experiment:** Validate a diffusion outcome over a non-transitive graph while showing that logical composition remains invalid.
- **Possible falsifier:** Proof that non-transitivity invalidates every possible traversal semantics.
- **Possible confirmation:** One empirically validated non-transitive diffusion or search network.

### ASTRO-CLM-0037

- **Identifier:** `ASTRO-CLM-0037`
- **Claim:** Version 1 contained no remaining internal contradiction.
- **Supporting evidence:** `SRC-002` §8.10 asserted closure of the identified contradictions.
- **Contradicting evidence:** `SRC-003` C-01 and RJ-9 identify a missed contradiction: an admissibility gate cannot generally be context-free when admission costs differ by context.
- **Current status:** `Rejected`
- **Confidence:** High (`0.96`).
- **Dependencies:** `ASTRO-CLM-0016`.
- **Future experiment:** Formal consistency audit of every future architecture revision against the registry.
- **Possible falsifier:** A formal model showing the Version 1 gate remains context-free under every admitted context and loss function.
- **Possible confirmation:** One fixed evidence state is admissible under one allowed context and inadmissible under another.

### ASTRO-CLM-0038

- **Identifier:** `ASTRO-CLM-0038`
- **Claim:** The general definition of significance is counterfactual physical effect alone.
- **Supporting evidence:** `SRC-002` AD-09 adopted this definition for Version 1.
- **Contradicting evidence:** `SRC-003` C-03; decision regret and value of information are distinct significance quantities with different mathematical inputs and outputs.
- **Current status:** `Rejected`
- **Confidence:** High (`0.96`).
- **Dependencies:** `ASTRO-CLM-0007`.
- **Future experiment:** Hold physical effect fixed while changing action utility or evidence cost.
- **Possible falsifier:** Universal order-equivalence of physical effect, regret, and information value.
- **Possible confirmation:** A controlled case in which the three quantities diverge.

## Untested

### ASTRO-CLM-0041

- **Identifier:** `ASTRO-CLM-0041`
- **Claim:** H1′ — no context-independent estimator matches a context-conditional estimator across a declared diverse context family within the preregistered noninferiority margin.
- **Supporting evidence:** `SRC-002` §6; `SRC-004` §7 identifies a valid empirical comparison.
- **Contradicting evidence:** Context-free estimators may suffice where all target valuations are invariant; no benchmark result is held.
- **Current status:** `Untested`
- **Confidence:** Medium (`0.55`).
- **Dependencies:** A diverse context family, equal model capacity and information, frozen reference outcomes, preregistered margin.
- **Future experiment:** Compare the best context-free and context-conditional estimators under nested cross-validation across held-out contexts.
- **Possible falsifier:** Context-free performance lies within the noninferiority margin in every registered context.
- **Possible confirmation:** Context conditioning yields preregistered improvements that replicate on held-out context families.

### ASTRO-CLM-0042

- **Identifier:** `ASTRO-CLM-0042`
- **Claim:** H2′ — a licensed relational estimator can estimate a declared counterfactual effect with calibrated uncertainty and approach the task-specific physical or simulation anchor.
- **Supporting evidence:** `SRC-002` §6 defines the test; counterfactual and calibration theory make it coherent.
- **Contradicting evidence:** No result is held; a simple intrinsic-attribute or supervised estimator may match or exceed it.
- **Current status:** `Untested`
- **Confidence:** Low-medium (`0.40`).
- **Dependencies:** Identifiable counterfactual, valid anchor, joint uncertainty model, frozen licence, equal-information baselines.
- **Future experiment:** Evaluate effect error, interval coverage, and ablations against the exact or simulation anchor.
- **Possible falsifier:** Persistent miscalibration, failure to approach the anchor, or equal performance from an attribute-only baseline.
- **Possible confirmation:** Replicated calibrated predictions materially closer to the anchor than equal-information simpler baselines.

### ASTRO-CLM-0043

- **Identifier:** `ASTRO-CLM-0043`
- **Claim:** H3′ — licensed relational constraints improve held-out cross-context transfer relative to an unconstrained equal-information estimator.
- **Supporting evidence:** `SRC-002` §6 and AD-25; `SRC-004` S1 recognizes this as an unresolved empirical performance hypothesis.
- **Contradicting evidence:** Domain-adaptation and invariant-prediction prior art already addresses the problem; no ASA result is held, and a supervised regressor may transfer equally well.
- **Current status:** `Untested`
- **Confidence:** Low (`0.30`) that a practically important ASA advantage will be confirmed.
- **Dependencies:** Multiple truly held-out contexts, equal information and capacity, frozen constraint set, supervised upper anchor, preregistered transfer metric.
- **Future experiment:** Train or configure on source contexts and evaluate once on sealed target contexts with constraint ablations.
- **Possible falsifier:** The unconstrained estimator is noninferior, or licence ablation causes no preregistered degradation.
- **Possible confirmation:** Repeated held-out-context advantage survives ablation, calibration, and independent replication.

### ASTRO-CLM-0044

- **Identifier:** `ASTRO-CLM-0044`
- **Claim:** A relational representation provides measurable benefit for at least one of physical-effect, decision, or information significance beyond equal-information non-relational estimators.
- **Supporting evidence:** `SRC-003` research question 3; relational structure can encode dependencies not present in isolated feature vectors.
- **Contradicting evidence:** No comparative result is held; equivalent relational features may be supplied to conventional estimators.
- **Current status:** `Untested`
- **Confidence:** Medium (`0.45`).
- **Dependencies:** `ASTRO-CLM-0007`; separate estimands, equal-information baselines, task-specific outcomes.
- **Future experiment:** Run separate ablations for each significance kind using relational, flattened equal-information, and task-specific estimators.
- **Possible falsifier:** No relational model materially exceeds the best equal-information alternative for any of the three estimands.
- **Possible confirmation:** A replicated task-specific improvement survives representation and capacity controls.

### ASTRO-CLM-0045

- **Identifier:** `ASTRO-CLM-0045`
- **Claim:** Typed abstention with declared costs can improve risk calibration or expected decision value over forced prediction in tasks where abstention is permitted.
- **Supporting evidence:** `PA-006`, `PA-010`; `SRC-002` AD-20–AD-22.
- **Contradicting evidence:** The benefit is task- and cost-dependent; abstention is failure under a hard allocation budget such as `ASTRO-CLM-0070`.
- **Current status:** `Untested`
- **Confidence:** Medium-high (`0.70`) in general, low confidence that ASA adds beyond prior art.
- **Dependencies:** Declared reject cost, complete outcome labels for neutrality tests, admissible abstention policy.
- **Future experiment:** Compare risk-coverage and expected utility curves with and without typed reasons under frozen costs.
- **Possible falsifier:** Forced prediction weakly dominates at every admissible coverage and cost, or abstention merely selects unlabeled hard cases.
- **Possible confirmation:** Preregistered utility or calibration gains persist at matched coverage and on fully labeled outcomes.

### ASTRO-CLM-0046

- **Identifier:** `ASTRO-CLM-0046`
- **Claim:** Generic frozen context contracts materially reduce context-answer leakage and post hoc target tailoring.
- **Supporting evidence:** `SRC-002` AD-14–AD-16; `SRC-003` C-08; `PA-011` supports commitment and sealed evaluation.
- **Contradicting evidence:** A context designer can encode domain knowledge correlated with the answer before freezing; hashing proves immutability, not neutrality.
- **Current status:** `Untested`
- **Confidence:** Medium (`0.55`).
- **Dependencies:** Independent authorship or audit, family-level instantiation, sealed outcomes, leakage diagnostics.
- **Future experiment:** Compare predictive leakage and post hoc flexibility under per-case, generic frozen, and independently authored contexts.
- **Possible falsifier:** Generic frozen contexts leak or overfit as strongly as bespoke contexts after equal-information controls.
- **Possible confirmation:** Predeclared leakage metrics fall materially and replicate under independent context authorship.

### ASTRO-CLM-0070

- **Identifier:** `ASTRO-CLM-0070`
- **Claim:** A single ASA estimator frozen after calibration on 27 Gaia DR3 main-belt asteroids transfers to 27 disjoint Gaia DR3 near-Earth deployment asteroids and achieves at least 20 material wins, where a material win satisfies \(E_{ASA}(t)+\delta_t\leq0.80E_{LOO}(t)\) against direct leave-one-perturber-out four-term selection over the frozen 20-year model.
- **Supporting evidence:** `SRC-005` Version 1 defines one computable endpoint, one strong comparator, one deployment rule, and one success threshold; `SRC-007` records no execution and no result.
- **Contradicting evidence:** No empirical outcome is held; prior-art review supplies no performance evidence for ASA, and the comparator measures the declared candidate effects directly.
- **Current status:** `Untested`
- **Confidence:** Low (`0.20`) that the positive claim will be confirmed; this is an epistemic assessment, not an empirical probability.
- **Dependencies:** `ASTRO-CLM-0043`; `ASTRO-EXP-0001@1.0`; 27 apparatus-valid independent deployment targets; frozen estimator; sealed outcomes; valid posterior and numerical-resolution construction.
- **Future experiment:** Execute `SRC-005` exactly once and record the outcome in `SRC-007`.
- **Possible falsifier:** A protocol-valid first run with \(W\leq19\); F0 or F1 terminates the programme without scientifically falsifying the estimator comparison.
- **Possible confirmation:** A protocol-valid first run with \(W\geq20\); the stronger replicated wording requires a second independent protocol-valid run with \(W\geq20\).

### ASTRO-CLM-0071

- **Identifier:** `ASTRO-CLM-0071`
- **Claim:** H0 — in the declared deployment population, the probability that the frozen ASA estimator produces a material win against direct leave-one-perturber-out selection is at most one half.
- **Supporting evidence:** `SRC-005` defines the null, the material-win event, and the exact one-sided binomial test; `SRC-007` records no execution or result.
- **Contradicting evidence:** No deployment observations are held. A protocol-valid \(W\geq20\) would reject this null at one-sided alpha `0.0095786452293396` but would not prove a universal ASA advantage.
- **Current status:** `Untested`
- **Confidence:** Low-medium (`0.40`) that H0 describes the deployment population; this is an epistemic assessment, not the null parameter or a result.
- **Dependencies:** `ASTRO-CLM-0070`; `ASTRO-EXP-0001@1.0`; target independence and the registered material-win definition.
- **Future experiment:** Execute `SRC-005` exactly once and apply its exact binomial rule.
- **Possible falsifier:** A protocol-valid first run with \(W\geq20\), which rejects H0 at the preregistered one-sided threshold.
- **Possible confirmation:** The planned test cannot confirm \(p\leq0.5\) merely by failing to reject it; confirmation would require a separately registered equivalence or upper-bound design.

### ASTRO-CLM-0072

- **Identifier:** `ASTRO-CLM-0072`
- **Claim:** After any terminal outcome under `ASTRO-EXP-0001@1.0`, the maximum negative statement is: “ASTRO-EXP-0001 did not demonstrate a material cross-context advantage for ASA. The remaining ASA utility claim is terminated.”
- **Supporting evidence:** `SRC-005` fixes F0–F3, prohibits rescue analyses, and supplies this exact bounded language; `SRC-007` records no terminal outcome.
- **Contradicting evidence:** A protocol-valid first run with \(W\geq20\) is not a terminal negative outcome and permits only the bounded positive claim in `ASTRO-CLM-0070`; it does not validate ASA generally.
- **Current status:** `Untested`
- **Confidence:** High (`0.95`) that the conditional wording correctly bounds a future terminal outcome; no empirical outcome probability is asserted.
- **Dependencies:** `ASTRO-CLM-0070`, `ASTRO-CLM-0071`; `ASTRO-EXP-0001@1.0`; a recorded F0, F1, F2, or F3 event in `ASTRO-RESULTS-0001`.
- **Future experiment:** Execute `SRC-005`; if a terminal class occurs, append the class and exact statement to `SRC-007`.
- **Possible falsifier:** Use of this statement after a non-terminal valid first-run success, or wording that asserts equivalence, universal failure, or truth outside the frozen experiment.
- **Possible confirmation:** A properly classified terminal event is recorded and the published interpretation matches the quoted statement exactly.

## Open

### ASTRO-CLM-0047

- **Identifier:** `ASTRO-CLM-0047`
- **Claim:** The exact ASA specification may be an original integration profile despite containing no novel scientific or mathematical constituent.
- **Supporting evidence:** `SRC-004` S2; no identical profile is held.
- **Contradicting evidence:** No exhaustive document-identity search was performed; arbitrary conjunction and vocabulary identity do not establish scientific novelty.
- **Current status:** `Open`
- **Confidence:** Medium (`0.50`) for textual originality; very low (`0.05`) for scientific significance.
- **Dependencies:** Stable complete specification and exhaustive comparison corpus.
- **Future experiment:** Conduct a specification-level prior-art and document-similarity search, separate from mathematical novelty review.
- **Possible falsifier:** An earlier materially identical integration profile.
- **Possible confirmation:** Exhaustive search finds no materially identical profile; confirmation remains limited to document originality.

### ASTRO-CLM-0048

- **Identifier:** `ASTRO-CLM-0048`
- **Claim:** Contextual evidence adequacy has substantive content beyond ordinary decision-theoretic thresholding and schema or provenance validation.
- **Supporting evidence:** `SRC-003` C-01 gives it a distinct architectural name.
- **Contradicting evidence:** `SRC-003` U-8 and `SRC-004` reduce the mechanism to validation plus context-dependent reject costs.
- **Current status:** `Open`
- **Confidence:** Low (`0.20`) that distinct content exists.
- **Dependencies:** `ASTRO-CLM-0016`; a precise operator and comparator.
- **Future experiment:** Formalize the operator and prove or test an output unavailable from Bayes decision rules plus ordinary validation.
- **Possible falsifier:** Exact reduction to schema/provenance checks and a context-specific decision threshold.
- **Possible confirmation:** A formally specified residual operation with a distinct guarantee or replicated benefit.

### ASTRO-CLM-0049

- **Identifier:** `ASTRO-CLM-0049`
- **Claim:** Diffusion or search traversal can be separated from physical or logical composition by a formal data-independent criterion rather than analyst declaration.
- **Supporting evidence:** `SRC-003` research question 4 identifies a potentially formal distinction.
- **Contradicting evidence:** The same graph walk can represent diffusion in one model and inference in another; semantics may be irreducibly model-declared.
- **Current status:** `Open`
- **Confidence:** Low (`0.25`) that a universal criterion exists.
- **Dependencies:** `ASTRO-CLM-0011`, `ASTRO-CLM-0012`.
- **Future experiment:** Formalize both semantics over identical path languages and search for an invariant that separates them across models.
- **Possible falsifier:** One path language admits both valid interpretations under different external semantics.
- **Possible confirmation:** A proved necessary-and-sufficient criterion over declared graph and operator structure.

### ASTRO-CLM-0050

- **Identifier:** `ASTRO-CLM-0050`
- **Claim:** There exists a scientifically important domain with computable counterfactuals and heterogeneous relational evidence in which no purpose-built sensitivity or decision method already supplies the required estimate.
- **Supporting evidence:** `SRC-003` research question 6 states the required use case.
- **Contradicting evidence:** `SRC-004` finds mature task-specific methods across the reviewed mathematical components; no qualifying domain is registered.
- **Current status:** `Open`
- **Confidence:** Low-medium (`0.35`).
- **Dependencies:** A precise domain, outcome, counterfactual, and strongest practitioner baseline.
- **Future experiment:** Systematic domain survey followed by one preregistered equal-information comparison.
- **Possible falsifier:** Every candidate domain has an established method matching the claimed ASA function.
- **Possible confirmation:** A domain expert validates the gap and ASA fills it with replicated practical benefit.

### ASTRO-CLM-0053

- **Identifier:** `ASTRO-CLM-0053`
- **Claim:** The enumerated withdrawal operations are complete enough for every retained significance estimand in the intended operating envelope.
- **Supporting evidence:** `SRC-002` AD-13 and `SRC-003` C-05 require a fixed declaration.
- **Contradicting evidence:** `SRC-002` residual risk B7; no completeness theorem or exhaustive domain audit is held.
- **Current status:** `Open`
- **Confidence:** Low (`0.30`).
- **Dependencies:** Fixed operating envelope and one enumeration per significance kind.
- **Future experiment:** Domain-expert enumeration audit followed by adversarial construction of unrepresented interventions.
- **Possible falsifier:** One scientifically required intervention cannot be represented without changing the enumeration.
- **Possible confirmation:** Closure or completeness proof over the declared operating envelope.

### ASTRO-CLM-0054

- **Identifier:** `ASTRO-CLM-0054`
- **Claim:** A single-operator hash or repository commit provides sufficiently independent evidence of preregistration for high-stakes evaluation.
- **Supporting evidence:** Content hashes can detect later changes when the earlier digest is reliably known.
- **Contradicting evidence:** `SRC-003` U-2; `PA-011` provides stronger independent commitment and trusted-time mechanisms. One operator can replace both content and claimed history before external observation.
- **Current status:** `Open`
- **Confidence:** Low (`0.20`).
- **Dependencies:** Threat model, independent witness, trusted timestamp, custody log.
- **Future experiment:** Formal threat-model analysis and third-party verification drill.
- **Possible falsifier:** A feasible undetectable rewrite under the declared single-operator process.
- **Possible confirmation:** An independently witnessed commitment and audit trail meeting the declared security property.

## Withdrawn

### ASTRO-CLM-0022

- **Identifier:** `ASTRO-CLM-0022`
- **Claim:** Under eight independent Bernoulli comparisons with equal win probability, observing eight wins in one direction has two-sided exact sign-test probability \(2/2^8=0.0078125\).
- **Supporting evidence:** `SRC-006`; exact binomial enumeration. The mathematical calculation remains correct for its assumptions.
- **Contradicting evidence:** `SRC-005` supersedes the eight-target design with a 27-target one-sided binomial rule; the calculation also fails if targets are dependent, the null win probability differs from one half, ties are treated differently, or direction is selected after observation.
- **Current status:** `Withdrawn`
- **Confidence:** Very high (`0.999`) that the historical arithmetic is correct; it has no operative role in Version 1.
- **Dependencies:** Superseded experimental design `ASTRO-CLM-0039`; replacement `ASTRO-CLM-0070`.
- **Future experiment:** None under Version 1; use the independently verified 27-target calculation in `SRC-005`.
- **Possible falsifier:** An arithmetic error in \(2/2^8\) or violation of the historical assumptions.
- **Possible confirmation:** Exact enumeration of all \(2^8\) historical sign patterns.

### ASTRO-CLM-0039

- **Identifier:** `ASTRO-CLM-0039`
- **Claim:** Under equal information, equal retained-force budget, and no greater selection cost, the frozen ASA selector produces materially lower reduced-model trajectory error than tangent-linear variational sensitivity on all eight preregistered targets, with median error ratio at most `0.80`.
- **Supporting evidence:** `SRC-006` defined the historical eight-target endpoint; no execution or outcome is held.
- **Contradicting evidence:** `SRC-005` replaces the target count, comparator, endpoint, cost rule, population split, and success threshold; `SRC-004` supplies no empirical ASA advantage.
- **Current status:** `Withdrawn`
- **Confidence:** Very high (`0.99`) that this exact claim is superseded and untested.
- **Dependencies:** Superseded by `ASTRO-CLM-0070`.
- **Future experiment:** None; the historical experiment must not be executed or used to interpret Version 1.
- **Possible falsifier:** Evidence that `SRC-005` did not supersede the eight-target protocol.
- **Possible confirmation:** Canonical execution and reporting use only `ASTRO-CLM-0070` and the 27-target protocol.

### ASTRO-CLM-0040

- **Identifier:** `ASTRO-CLM-0040`
- **Claim:** ASA's instance-level composition discipline correctly distinguishes every valid and invalid matched inference chain and rejects at least one invalid chain that a fully and fairly specified temporal RDF, OWL, SHACL, units, and provenance standards stack admits.
- **Supporting evidence:** `SRC-003` preserved Track B as an unresolved historical proposal; no experiment or outcome is held.
- **Contradicting evidence:** `SRC-004` N1 eliminates the composition-novelty basis by reduction to ordinary guarded paths and constraints; `SRC-005` contains no Track B experiment.
- **Current status:** `Withdrawn`
- **Confidence:** Very high (`0.98`) that no active Track B claim or experiment remains.
- **Dependencies:** Prior-art rejection `ASTRO-CLM-0024`; retained formal limit `ASTRO-CLM-0023`.
- **Future experiment:** None within Version 1; any new empirical error-prevention claim requires a new identifier and prior-art-resistant rationale.
- **Possible falsifier:** A new formal non-expressibility result or independently motivated claim registered after Version 1.
- **Possible confirmation:** Canonical protocol, results ledger, and publications contain no Track B execution or active composition-novelty claim.

### ASTRO-CLM-0051

- **Identifier:** `ASTRO-CLM-0051`
- **Claim:** The `8/8` Track A terminal rule has adequate power for every practically meaningful effect size and supports more than the bounded conclusion “no advantage demonstrated at this power” after failure.
- **Supporting evidence:** The historical rule had high specificity and a simple exact test.
- **Contradicting evidence:** `SRC-003` U-5 gives power \(0.8^8\approx0.168\) at an 80% win probability; `SRC-005` replaces the rule with 27 targets and a 20-win threshold.
- **Current status:** `Withdrawn`
- **Confidence:** Very high (`0.99`) that the historical power claim is not operative and was inadequately supported.
- **Dependencies:** Superseded by `ASTRO-CLM-0070` and the statistical rule in `SRC-005`.
- **Future experiment:** None; Version 1 uses independently recomputed one-sided alpha `0.0095786452293396` and power `0.8444402928110182` at \(p=0.8\).
- **Possible falsifier:** A valid power calculation showing the historical 8/8 design met the claimed power across the stated meaningful range.
- **Possible confirmation:** The historical 8/8 power remains below the declared threshold and all Version 1 analyses use 27 targets.

### ASTRO-CLM-0052

- **Identifier:** `ASTRO-CLM-0052`
- **Claim:** The standards comparator in Track B can be specified completely enough that a finite ASA advantage is attributable to non-expressibility rather than omitted rules, metadata, or expertise.
- **Supporting evidence:** `SRC-003` recorded the historical Track B question.
- **Contradicting evidence:** `SRC-004` finds ordinary expressibility prior art; extensible SHACL, SPARQL, OWL, unit, temporal, and provenance constraints have no natural “strongest combination”; `SRC-005` eliminates Track B.
- **Current status:** `Withdrawn`
- **Confidence:** Very high (`0.98`) that no active Track B comparator claim remains.
- **Dependencies:** `ASTRO-CLM-0023`, `ASTRO-CLM-0024`, `ASTRO-CLM-0040`.
- **Future experiment:** None within Version 1.
- **Possible falsifier:** A new registered formal language boundary with a non-expressibility proof and independent scientific motivation.
- **Possible confirmation:** All Version 1 controls exclude Track B and retain the prior-art rejection.

### ASTRO-CLM-0055

- **Identifier:** `ASTRO-CLM-0055`
- **Claim:** Astronomy validation is independent of human language or removes human interpretation.
- **Supporting evidence:** Physical acquisition processes do not depend on natural-language labels.
- **Contradicting evidence:** `SRC-001` §2.2 and `SRC-003` RJ-10; catalogue classes, entity boundaries, membership rules, relationship labels, and model choices are human artefacts.
- **Current status:** `Withdrawn`
- **Confidence:** Very high (`0.99`) that the broad claim is false.
- **Dependencies:** None.
- **Future experiment:** None for the broad claim; provenance audits may quantify human dependence.
- **Possible falsifier:** A complete validation pipeline whose entities, categories, relations, contexts, and decisions are fixed without human conventions.
- **Possible confirmation:** The retained narrower statement is confirmed when measurements are instrument-anchored and all human labels carry provenance.

### ASTRO-CLM-0056

- **Identifier:** `ASTRO-CLM-0056`
- **Claim:** Standing is a permanent, context-free architectural layer distinct from ordinary well-formedness and contextual evidence adequacy.
- **Supporting evidence:** `SRC-001` and `SRC-002` retained Standing as a named layer, latterly on probation.
- **Contradicting evidence:** `SRC-003` C-01 deletes the layer after analytic reduction to validation and context-dependent decision thresholds.
- **Current status:** `Withdrawn`
- **Confidence:** High (`0.97`) that no distinct retained layer is justified.
- **Dependencies:** `ASTRO-CLM-0010`, `ASTRO-CLM-0016`, `ASTRO-CLM-0048`.
- **Future experiment:** Reopen only if `ASTRO-CLM-0048` produces a distinct operator and benefit.
- **Possible falsifier:** A formal Standing operation not reducible to validation, external evidence, or contextual thresholding.
- **Possible confirmation:** Complete reduction of all Standing outputs to those three sources.

### ASTRO-CLM-0057

- **Identifier:** `ASTRO-CLM-0057`
- **Claim:** A context-free scalar Standing term should enter the significance aggregate.
- **Supporting evidence:** The pre-revision model used an additive positive Standing term.
- **Contradicting evidence:** `SRC-001` §§5.2–5.4; `SRC-002` AD-02; it reintroduces context-invariant importance and cannot add information when graph-derived.
- **Current status:** `Withdrawn`
- **Confidence:** Very high (`0.99`).
- **Dependencies:** `ASTRO-CLM-0010`.
- **Future experiment:** None unless an external, independently measured variable and scoped estimand are registered.
- **Possible falsifier:** A context-free additive term shown to improve calibrated target estimation after conditioning on all inputs without contradicting contextual nullity.
- **Possible confirmation:** Ablation shows no conditional information gain or exposes context-invariant bias.

### ASTRO-CLM-0058

- **Identifier:** `ASTRO-CLM-0058`
- **Claim:** “Significance emerges from evidence, relationships, standing, and context” is a falsifiable scientific hypothesis.
- **Supporting evidence:** It was the original programme framing.
- **Contradicting evidence:** `SRC-001` §§1.2 and 8.1; the statement merely defines significance as an unspecified function of named inputs and supplies no failure condition.
- **Current status:** `Withdrawn`
- **Confidence:** Very high (`0.99`) that the statement is not falsifiable as written.
- **Dependencies:** None.
- **Future experiment:** None; replace with a registered estimand, comparator, margin, and failure rule.
- **Possible falsifier:** A logically possible observation entailed by the statement to count as failure.
- **Possible confirmation:** No observation can distinguish the statement from an arbitrary input-dependent scoring rule.

### ASTRO-CLM-0059

- **Identifier:** `ASTRO-CLM-0059`
- **Claim:** Significance-before-reasoning is an ASA architectural novelty.
- **Supporting evidence:** Original ASA public framing emphasized the order.
- **Contradicting evidence:** `ASTRO-CLM-0017`; `PA-008`; `SRC-002` AD-24 and `SRC-003` C-09 explicitly withdraw it.
- **Current status:** `Withdrawn`
- **Confidence:** Very high (`0.99`) that the novelty claim is false.
- **Dependencies:** `ASTRO-CLM-0017`.
- **Future experiment:** None.
- **Possible falsifier:** A registered ordering property materially absent from prior attention and staged-ranking systems.
- **Possible confirmation:** Direct forward-pass equivalence to graph attention or other pre-aggregation weighting.

### ASTRO-CLM-0060

- **Identifier:** `ASTRO-CLM-0060`
- **Claim:** ASA establishes a broad significance-first theory of intelligence.
- **Supporting evidence:** Original programme framing.
- **Contradicting evidence:** `SRC-003` §2 and AC-8; no operational intelligence definition, theorem, broad benchmark, or evidence supports the claim.
- **Current status:** `Withdrawn`
- **Confidence:** Very high (`0.99`) that the claim is unsupported.
- **Dependencies:** None.
- **Future experiment:** None within the astronomy programme; any revival requires a new registry claim and independent research programme.
- **Possible falsifier:** Failure of ASA on any indispensable component of the claimed general theory under a complete formalization.
- **Possible confirmation:** A precise theory with risky predictions and broad independent replication, none currently held.

### ASTRO-CLM-0061

- **Identifier:** `ASTRO-CLM-0061`
- **Claim:** ASA should outperform exact physics or a correct closed-form physical calculation on physical-effect significance.
- **Supporting evidence:** Earlier competitive framing risked treating physics as a baseline to beat.
- **Contradicting evidence:** `SRC-001` A6; `SRC-002` AD-09 and §9; `SRC-003` C-10. Exact physics is the anchor or truth generator within its domain.
- **Current status:** `Withdrawn`
- **Confidence:** Very high (`0.99`) that the broad superiority claim is false or incoherent.
- **Dependencies:** `ASTRO-CLM-0021`.
- **Future experiment:** None; compare approximation quality and operational allocation only where exact evaluation is withheld or costly.
- **Possible falsifier:** A declared regime where the alleged “exact” calculation is misspecified and ASA uses valid additional information; this would change the claim.
- **Possible confirmation:** Correct exact calculation attains zero within-model estimation error while ASA can only match or approximate it.

### ASTRO-CLM-0062

- **Identifier:** `ASTRO-CLM-0062`
- **Claim:** ASA claims general superiority over personalized PageRank on rank correlation.
- **Supporting evidence:** Early comparisons treated PageRank as a principal competitor.
- **Contradicting evidence:** `SRC-002` AD-26 explicitly disclaims rank-correlation superiority; `SRC-003` C-10 limits PPR to contexts without a stronger purpose-built method.
- **Current status:** `Withdrawn`
- **Confidence:** Very high (`0.99`) that no active claim remains.
- **Dependencies:** `ASTRO-CLM-0018`.
- **Future experiment:** None for the broad claim; any task-specific comparison must be newly registered.
- **Possible falsifier:** A current programme document asserting the broad superiority claim with a frozen supporting result.
- **Possible confirmation:** Registry and future papers make no such assertion.

### ASTRO-CLM-0063

- **Identifier:** `ASTRO-CLM-0063`
- **Claim:** Typed abstention must be available in every context.
- **Supporting evidence:** `SRC-002` AD-20 and INV-20 generalized abstention.
- **Contradicting evidence:** `SRC-003` C-06 and `SRC-005` Experiment A; abstention is task failure under a hard allocation budget.
- **Current status:** `Withdrawn`
- **Confidence:** Very high (`0.98`) that the universal claim is false.
- **Dependencies:** `ASTRO-CLM-0045`.
- **Future experiment:** Evaluate abstention only in contexts whose action set permits refusal.
- **Possible falsifier:** A proof that every admissible decision problem includes a reject action at finite cost.
- **Possible confirmation:** One valid hard-budget task in which refusal fails the task.

### ASTRO-CLM-0064

- **Identifier:** `ASTRO-CLM-0064`
- **Claim:** Detectability, selection models, correction, and observability diagnostics are mandatory in every ASA context.
- **Supporting evidence:** `SRC-002` AD-17–AD-19 made the machinery universal.
- **Contradicting evidence:** `SRC-003` C-11; a fixed complete candidate set supplied identically to both selectors has no catalogue inclusion mechanism to correct.
- **Current status:** `Withdrawn`
- **Confidence:** High (`0.97`) that the universal claim is false.
- **Dependencies:** `ASTRO-CLM-0015`.
- **Future experiment:** Scope selection controls by an explicit observation or inclusion mechanism.
- **Possible falsifier:** Proof that selection bias necessarily exists even for a complete fixed candidate set with identical access.
- **Possible confirmation:** A valid experiment whose result is unchanged by adding vacuous selection machinery.

### ASTRO-CLM-0065

- **Identifier:** `ASTRO-CLM-0065`
- **Claim:** Personalized PageRank is the mandatory strongest baseline in every ASA context.
- **Supporting evidence:** `SRC-002` INV-26 made PPR universal.
- **Contradicting evidence:** `SRC-003` C-10 and RJ-5; purpose-built physical, statistical, or decision methods can be strictly more relevant and stronger.
- **Current status:** `Withdrawn`
- **Confidence:** Very high (`0.98`) that the universal claim is false.
- **Dependencies:** `ASTRO-CLM-0018`, `ASTRO-CLM-0020`.
- **Future experiment:** Select comparators by task-specific expert review before evaluation.
- **Possible falsifier:** Proof that every relevant task reduces to personalized stationary graph ranking.
- **Possible confirmation:** One task where a practitioner-grade method answers the estimand directly and PPR does not.

### ASTRO-CLM-0066

- **Identifier:** `ASTRO-CLM-0066`
- **Claim:** Original H1 — a context-independent ranking cannot match context-specific reference rankings across every declared context.
- **Supporting evidence:** `SRC-001` §8.2 gave a testable context-irreducibility form.
- **Contradicting evidence:** The quantifiers and noninferiority margin were under-specified; `SRC-002` replaced it with H1′ and `SRC-003` reduced the active programme to two bounded tracks.
- **Current status:** `Withdrawn`
- **Confidence:** High (`0.95`) that this exact formulation is superseded, not that every scoped version is false.
- **Dependencies:** Superseded by `ASTRO-CLM-0041`.
- **Future experiment:** Test only the registered H1′ formulation.
- **Possible falsifier:** A context-free estimator matches the conditional estimator in the declared context family.
- **Possible confirmation:** Preregistered held-out results confirm `ASTRO-CLM-0041`.

### ASTRO-CLM-0067

- **Identifier:** `ASTRO-CLM-0067`
- **Claim:** Original H2 — relational structure alone is sufficient to recover significance.
- **Supporting evidence:** `SRC-001` §8.2 proposed relational sufficiency.
- **Contradicting evidence:** `ASTRO-CLM-0003`, `ASTRO-CLM-0008`, and `SRC-002` replace the undefined target with a declared counterfactual estimand, anchor, uncertainty model, and context.
- **Current status:** `Withdrawn`
- **Confidence:** Very high (`0.98`) that the broad formulation is false or under-specified.
- **Dependencies:** Superseded by `ASTRO-CLM-0042`.
- **Future experiment:** Test only the registered calibrated counterfactual-estimability claim.
- **Possible falsifier:** Two empirically different systems with identical relational structure require different significance values.
- **Possible confirmation:** Preregistered results confirm `ASTRO-CLM-0042`; this would not restore the broad “alone” claim.

### ASTRO-CLM-0068

- **Identifier:** `ASTRO-CLM-0068`
- **Claim:** Original H3 — separating significance from reasoning has value without specifying transfer, comparator, outcome, or feedback mechanism.
- **Supporting evidence:** `SRC-001` §8.2 proposed separation value.
- **Contradicting evidence:** `SRC-002` AD-24–AD-25 separates the prior-art governance rule from the empirical transfer wager and supplies measurable conditions.
- **Current status:** `Withdrawn`
- **Confidence:** Very high (`0.97`) that the original formulation is under-specified.
- **Dependencies:** Superseded by `ASTRO-CLM-0043`; constrained by `ASTRO-CLM-0019`.
- **Future experiment:** Test only the registered cross-context constraint-value claim.
- **Possible falsifier:** Equal-information unconstrained or supervised estimators match or exceed the separated architecture.
- **Possible confirmation:** Preregistered results confirm `ASTRO-CLM-0043`; this confirms a scoped performance claim only.

### ASTRO-CLM-0069

- **Identifier:** `ASTRO-CLM-0069`
- **Claim:** Significance universally “emerges” as one scalar that can aggregate physical effect, decision value, information value, attention, and centrality.
- **Supporting evidence:** Broad early programme language treated these quantities as one construct.
- **Contradicting evidence:** `ASTRO-CLM-0007`, `ASTRO-CLM-0008`; `SRC-003` C-03 prohibits collapsing or comparing the three retained significance kinds.
- **Current status:** `Withdrawn`
- **Confidence:** Very high (`0.98`) that the universal scalar claim is invalid.
- **Dependencies:** `ASTRO-CLM-0007`.
- **Future experiment:** None; any aggregation must register an explicit decision model and utility.
- **Possible falsifier:** A universal measurement model proving invariance and comparability across all listed constructs.
- **Possible confirmation:** A counterexample where physical effect, decision regret, information value, attention, and centrality rank entities differently.

## Registry closure

| Closure field | Value |
|---|---|
| Highest assigned claim identifier | `ASTRO-CLM-0072` |
| Retained | 22 |
| Rejected | 15 |
| Untested | 9 |
| Open | 6 |
| Withdrawn | 20 |
| Total registered claims | 72 |
| Unregistered scientific claims permitted | 0 |
