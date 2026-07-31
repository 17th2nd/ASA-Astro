# ASTRO-ONTOLOGY-0001 — Core Astronomy Validation Ontology

## Document control

| Field | Value |
|---|---|
| Status | Normative ASA-Astro domain ontology; not an ASA definition |
| Purpose | Define machine-mappable concepts for the proof-of-concept boundary |
| Depends on | `ASA-ASTRO-0001-foundational-definition.md` |
| Relationship vocabulary | `ASTRO-RELATIONSHIP-TAXONOMY-0001.md` |

## 1. Modelling conventions

Every record derived from this ontology MUST have a stable identifier, a schema
version, a lifecycle state, and a provenance link. Identifiers identify records,
not scientific truth. Records MAY be superseded but MUST remain auditable.

The classification field used below has these values:

- **Observed**: produced directly by an identified acquisition or detector
  process, while still being a representation rather than astronomical reality.
- **Inferred**: concluded from evidence through a named interpretive method.
- **Computed**: produced deterministically or statistically from declared
  inputs and a versioned policy or algorithm.
- **Externally supplied**: adopted from an identified catalogue, expert set,
  benchmark authority, or other source outside the run.

A concept can admit more than one classification, but an individual record MUST
state its actual classification. The same datum MUST NOT silently change class
as it moves through the pipeline.

## 2. Cross-cutting invariants

1. An Observation Source is not the astronomical reality it represents.
2. A Pixel, Detector Output, or Light Region is not an astronomical entity.
3. Candidate Entity and Resolved Entity are distinct lifecycle and epistemic
   states; candidate formation does not establish identity.
4. A relationship claim is always carried by a Relationship Assertion.
   Classification does not erase its evidence, confidence, or uncertainty.
5. Relationship strength and Confidence MUST be separate attributes.
6. Standing and Significance are separate computations and records.
7. Significance MUST reference exactly one declared Context version and MUST
   NOT be an intrinsic Candidate, Resolved, Composite, or System attribute.
8. Null-like states MUST distinguish `unknown`, `unavailable`, `not_applicable`,
   `withheld`, `contested`, `estimated`, and `bounded` where applicable.
9. Every derived value MUST be traceable through Provenance Records to source
   inputs.
10. Ground Truth is scoped reference authority, not absolute astronomical
    reality.

## 3. Entity and record terms

### 3.1 Observation

- **Precise definition:** A bounded acquisition event or externally documented
  acquisition record in which an instrument or observing process sampled a
  declared region, target, or signal under specified conditions.
- **Classification:** Observed when locally acquired; externally supplied when
  imported from an archive or catalogue.
- **Permitted attributes:** observation identifier; source identifier;
  acquisition start/end or epoch; instrument and configuration; observing band;
  sky region or target designation as supplied; coordinate/reference frame;
  exposure metadata; calibration references; environmental or quality flags;
  access/licence authority; Provenance Record links.
- **Prohibited conflations:** astronomical event; image file; Detector Output;
  resolved astronomical identity; Ground Truth; inference.
- **Lifecycle:** declared → acquired/imported → calibrated or quality-assessed →
  accepted, rejected, or superseded. Rejection does not delete the record.
- **Relations to other terms:** uses an Observation Source; produces or imports
  Detector Output; supports Evidence Records; is described by Provenance
  Records.
- **Astronomy example:** A documented telescope exposure in a named observing
  band, without asserting which astronomical objects appear in it.

### 3.2 Observation Source

- **Precise definition:** The immutable or version-identified physical or
  digital source representation from which an Observation or imported evidence
  is obtained.
- **Classification:** Observed for a local instrument stream; externally
  supplied for an archive image, table, or catalogue product.
- **Permitted attributes:** stable source identifier; provider; source URI or
  archive key; content digest where permitted; media type; dimensions; encoding;
  release/version; retrieval time; licence; supplied calibration metadata;
  integrity status.
- **Prohibited conflations:** astronomical reality; Observation event;
  Resolved Entity; Evidence Record; scientific authority merely because it is a
  file.
- **Lifecycle:** registered → integrity-checked → available, unavailable,
  quarantined, or superseded. Original bytes MUST remain unaltered when retained.
- **Relations to other terms:** is used by an Observation; is transformed into
  Detector Output; is cited by Provenance and Evidence Records; can be a source
  for Ground Truth only when separately authorised.
- **Astronomy example:** A versioned FITS image or catalogue table obtained from
  an identified archive.

### 3.3 Detector Output

- **Precise definition:** A detector-level or processing-level representation
  of measured signal, including raw samples, calibrated arrays, masks, or
  detection products, tied to an Observation.
- **Classification:** Observed for raw detector measurements; computed for
  calibrated, resampled, segmented, or otherwise transformed products.
- **Permitted attributes:** output identifier; Observation link; array or record
  shape; units; calibration state; detector geometry; masks; saturation and
  quality flags; processing method/version; uncertainty representation;
  Provenance Record link.
- **Prohibited conflations:** source image as reality; Pixel as entity;
  Light Region as object; Candidate Entity; astronomical measurement without
  units and calibration state.
- **Lifecycle:** produced → calibrated/processed → quality-assessed → accepted,
  rejected, or superseded.
- **Relations to other terms:** contains Pixels or detection records; may be
  segmented into Light Regions; supports Evidence Records and Candidate Entity
  formation.
- **Astronomy example:** A calibrated intensity array with a bad-pixel mask,
  without object labels.

### 3.4 Pixel

- **Precise definition:** One addressable sample element in a specific Detector
  Output, defined by its index and sampling geometry.
- **Classification:** Observed when it carries a detector sample; computed when
  resampled or synthesized by processing.
- **Permitted attributes:** parent Detector Output; index; coordinate mapping;
  value and units; uncertainty; mask/quality state; channel or band; provenance
  for computed pixels.
- **Prohibited conflations:** point in astronomical space; star, galaxy, or
  other entity; independent Observation; significance; a fixed physical scale
  without a declared transformation.
- **Lifecycle:** created with parent output → calibrated/masked or resampled →
  retained as immutable input to later products.
- **Relations to other terms:** belongs to one Detector Output; may contribute to
  zero or more Light Regions and Evidence Records; maps to coordinates only
  through a declared model.
- **Astronomy example:** One sample in an image plane that contributes measured
  intensity to a segmented region.

### 3.5 Light Region

- **Precise definition:** A bounded set of detector samples grouped by a named
  segmentation or detection rule because they exhibit a declared signal
  pattern.
- **Classification:** Computed.
- **Permitted attributes:** region identifier; member pixels or mask; detection
  method/version; threshold and parameters; band; aggregate measured features;
  background model; uncertainty; quality flags; parent Detector Output;
  Provenance Record.
- **Prohibited conflations:** astronomical object; visible matter as all matter;
  Resolved Entity; proof of physical association; intrinsic luminosity;
  significance.
- **Lifecycle:** proposed by detector → quality-assessed → retained, merged,
  split, rejected, or superseded; all transformations remain traceable.
- **Relations to other terms:** derives from Pixels/Detector Output; supports
  Candidate Entities and Evidence Records; may overlap other Light Regions
  across bands or methods.
- **Astronomy example:** A segmented patch of above-background signal that may
  later support one candidate, multiple candidates, or no entity candidate.

### 3.6 Candidate Entity

- **Precise definition:** A provisional record asserting that one or more
  evidence-bearing representations may correspond to an astronomical entity,
  while identity and boundaries remain unresolved.
- **Classification:** Inferred.
- **Permitted attributes:** candidate identifier; candidate kind vocabulary;
  supporting and contradicting Evidence Records; source representations;
  proposed coordinates with frame/epoch; boundary hypotheses; resolution state;
  Confidence and Uncertainty; alternative candidate links; Provenance Record.
- **Prohibited conflations:** Detector Output or Light Region; confirmed
  catalogue identity; Resolved Entity; scientific Ground Truth; Standing;
  Significance.
- **Lifecycle:** proposed → assessed → split, merged, matched, rejected,
  unresolved, or promoted to a Resolved Entity. Promotion preserves the
  candidate record and method.
- **Relations to other terms:** is supported by Light Regions and Evidence
  Records; may participate in provisional Relationship Assertions; may resolve
  to a Resolved Entity or contribute to a Composite Entity.
- **Astronomy example:** A source candidate generated from aligned detections in
  multiple bands before catalogue matching.

### 3.7 Resolved Entity

- **Precise definition:** An entity record for which a declared resolution
  policy has concluded that specified representations refer to the same bounded
  astronomical subject with an explicit confidence and provenance.
- **Classification:** Inferred, or externally supplied when imported from a
  catalogue and clearly labelled as such.
- **Permitted attributes:** entity identifier; entity kind; resolution policy
  and version; contributing candidate/representation links; external identifiers
  with authority; coordinates and epochs; evidence; Confidence; Uncertainty;
  active/contested/superseded resolution state; Provenance Record.
- **Prohibited conflations:** certainty of physical nature; a single image or
  catalogue row; Composite Entity unless modelled as one; Ground Truth;
  intrinsic Standing or Significance.
- **Lifecycle:** resolved → reviewed → active, contested, split, merged, or
  superseded. A later disagreement MUST preserve prior identity assertions.
- **Relations to other terms:** resolves Candidate Entities; may be a member or
  component of Composite Entities or Astronomical Systems; participates in
  Relationship Assertions; receives separately computed Standing and
  context-specific Significance results.
- **Astronomy example:** Multiple observations matched under a declared policy
  to one catalogue-referenced source, with the match uncertainty retained.

### 3.8 Composite Entity

- **Precise definition:** A modelled entity whose identity explicitly comprises
  two or more component entities or unresolved components under a declared
  composition rule.
- **Classification:** Inferred or externally supplied.
- **Permitted attributes:** composite identifier; composite kind; component
  membership assertions; composition rule/version; hierarchy level; evidence;
  boundaries; Confidence; Uncertainty; temporal validity; Provenance Record.
- **Prohibited conflations:** arbitrary image grouping; Astronomical System by
  default; proof that all components are gravitationally bound; sum of component
  significance; permanent membership.
- **Lifecycle:** proposed → component-assessed → active, contested, revised,
  decomposed, merged, or superseded.
- **Relations to other terms:** contains or aggregates Candidate/Resolved
  Entities through explicit Relationship Assertions; may itself be a member of
  an Astronomical System; can receive its own Standing and Significance results.
- **Astronomy example:** A catalogue-supported multiple-star candidate modelled
  as a composite while component identities and binding evidence remain
  explicit.

### 3.9 Astronomical System

- **Precise definition:** A scientifically scoped collection or hierarchy of
  entities and relationships treated as a system under a declared boundary and
  system criterion.
- **Classification:** Inferred or externally supplied.
- **Permitted attributes:** system identifier; system kind; boundary definition;
  reference frame; epoch/validity interval; membership and containment
  assertions; system criterion; evidence; Confidence; Uncertainty; Provenance
  Record.
- **Prohibited conflations:** every spatial grouping; Composite Entity;
  observation field of view; visual centrality; a context; a guaranteed closed
  physical system.
- **Lifecycle:** proposed/imported → boundary and membership assessed → active,
  contested, revised, or superseded.
- **Relations to other terms:** contains or has members through Relationship
  Assertions; may be nested in another system; supplies structural inputs to
  Standing and contextual inputs to Significance.
- **Astronomy example:** A galaxy represented as a bounded system containing
  component structures and member candidates under an identified reference.

### 3.10 Relationship

- **Precise definition:** A typed semantic connection between identified
  subjects as represented by one or more active Relationship Assertions. It is
  the normalised relation view, not an evidence-free fact.
- **Classification:** Inferred, computed, or externally supplied according to
  the assertions that support it.
- **Permitted attributes:** relationship identifier; subject/object identifiers;
  Relationship Type; role labels; magnitude and units where applicable;
  temporal/reference-frame scope; active assertion identifiers; aggregated
  Confidence and Uncertainty method; lifecycle state.
- **Prohibited conflations:** Relationship Assertion; causal relation by default;
  edge weight as Confidence; transitivity; scientific establishment independent
  of supporting assertions.
- **Lifecycle:** assembled from assertions → classified/reviewed → active,
  contested, rejected, or superseded. Competing relationships MAY coexist.
- **Relations to other terms:** is supported by Relationship Assertions; uses a
  Relationship Type; may inform Standing and Significance through a declared
  policy; is explained by Evidence and Provenance Records.
- **Astronomy example:** A normalised `member_of` relation view backed by a
  catalogue assertion and an independent kinematic assertion.

### 3.11 Relationship Assertion

- **Precise definition:** A provenance-bearing claim by a named source or method
  that specified subjects have a specified Relationship Type under declared
  conditions.
- **Classification:** Inferred, computed, or externally supplied; never simply
  “observed” when physical interpretation is required.
- **Permitted attributes:** assertion identifier; claimant/method; subject and
  object; proposed type; direction/roles; magnitude and units; frame/epoch;
  supporting, contradicting, and contextual Evidence Records; Confidence;
  Uncertainty; validity interval; review and resolution state; Provenance Record.
- **Prohibited conflations:** established fact; Relationship normalisation;
  evidence itself; magnitude with Confidence; one assertion with independent
  corroboration.
- **Lifecycle:** proposed/imported → evidence-linked → classified → accepted for
  use, contested, rejected, or superseded. Rejected assertions remain auditable.
- **Relations to other terms:** asserts a Relationship Type between entities,
  systems, observations, or records; is aggregated into a Relationship only by
  an explicit method; feeds Explanation Traces.
- **Astronomy example:** A catalogue-derived claim that a source is a member of a
  galaxy, retaining the catalogue release and membership method.

### 3.12 Relationship Type

- **Precise definition:** A versioned vocabulary entry that defines the
  semantics, roles, directionality, units, evidence expectations, and permitted
  propagation behaviour of a relationship class.
- **Classification:** Externally supplied to a run as a versioned ASA-Astro
  taxonomy entry; computed only if a separately declared taxonomy-generation
  process produces it.
- **Permitted attributes:** stable type identifier; label; definition; domain and
  range constraints; directionality; symmetry; persistence; unit constraints;
  evidentiary requirements; confidence method; transitivity and recursive
  propagation rules; failure modes; taxonomy version.
- **Prohibited conflations:** an instance of a Relationship; proof an assertion
  is true; generic edge labels without semantics; automatic transitivity.
- **Lifecycle:** proposed → reviewed → active, deprecated, or superseded. Type
  semantics MUST NOT change in place after use.
- **Relations to other terms:** classifies Relationship Assertions and
  Relationships; is defined by `ASTRO-RELATIONSHIP-TAXONOMY-0001`.
- **Astronomy example:** The vocabulary entry for `orbital`, not a claim that a
  particular body orbits another.

### 3.13 Evidence Record

- **Precise definition:** A structured record that states how a specific source,
  measurement, reference, or derived analysis supports, contradicts, or
  contextualises a specific claim.
- **Classification:** Observed, inferred, computed, or externally supplied, as
  explicitly declared per record.
- **Permitted attributes:** evidence identifier; subject claim; evidence role;
  source; method; value and units; frame/epoch/band; quality flags; independence
  group; Confidence and Uncertainty where meaningful; Provenance Record;
  admissibility and invalidation state.
- **Prohibited conflations:** the supported claim; Provenance Record; duplicate
  derivations as independent evidence; absence of evidence as negative evidence
  without a detection model.
- **Lifecycle:** captured/imported → quality and provenance checked → admissible,
  limited, contested, invalid, or superseded.
- **Relations to other terms:** cites Observation Sources, Observations, Detector
  Outputs, external references, or computations; supports entity resolution,
  Relationship Assertions, Standing, Context inputs, Significance, Ground
  Truth, and Validation Results.
- **Astronomy example:** A position measurement with units and epoch used to
  support a candidate-to-catalogue match.

### 3.14 Provenance Record

- **Precise definition:** An immutable derivation or custody record connecting
  an output to its direct inputs, responsible process or source, versions,
  parameters, and integrity evidence.
- **Classification:** Computed for execution lineage; externally supplied for
  source custody metadata.
- **Permitted attributes:** provenance identifier; output identifier; ordered
  parent identifiers; activity/method; operator or executable; code/schema/model/
  policy versions; parameters; seed; timestamps; source and licence; content
  digests; environment identifier; warnings; manual intervention.
- **Prohibited conflations:** Evidence Record; correctness; scientific authority;
  narrative citation without machine-resolvable lineage.
- **Lifecycle:** created atomically with record → integrity-checked → retained;
  never edited in place. Corrections create a superseding record.
- **Relations to other terms:** is mandatory for every derived ontology record;
  chains Observation Sources through Evidence, assertions, computations,
  Explanation Traces, and Validation Results.
- **Astronomy example:** A lineage record showing that a calibrated array was
  derived from a source file using a named calibration and code version.

### 3.15 Confidence

- **Precise definition:** A declared, method-specific representation of how
  strongly available evidence supports a proposition or estimate, including its
  calibration scope.
- **Classification:** Computed, inferred, or externally supplied.
- **Permitted attributes:** confidence identifier/value; scale and semantics;
  target proposition; calibration method and dataset; uncertainty on confidence;
  evidence set; independence assumptions; valid domain; missing/uncalibrated
  state; Provenance Record.
- **Prohibited conflations:** relationship magnitude; probability without stated
  semantics; certainty; significance; data quality alone; count of sources.
- **Lifecycle:** estimated/imported → calibrated/assessed → active, uncalibrated,
  contested, or superseded.
- **Relations to other terms:** qualifies Candidate resolution, Relationship
  Assertions, Ground Truth labels, and computed results; is evaluated by
  uncertainty calibration in a Benchmark.
- **Astronomy example:** A calibrated probability that two source
  representations are the same entity, not their angular separation.

### 3.16 Uncertainty

- **Precise definition:** A structured representation of incomplete knowledge,
  variability, measurement error, model dependence, ambiguity, missingness, or
  disagreement affecting a value or proposition.
- **Classification:** Observed as reported measurement error, inferred or
  computed by a model, or externally supplied.
- **Permitted attributes:** uncertainty kind; target field or proposition;
  interval/distribution/covariance or categorical state; units; confidence/cover
  semantics; source components; correlation/dependency identifiers; method;
  assumptions; contested alternatives; Provenance Record.
- **Prohibited conflations:** Confidence; zero; false; unavailable; random error
  only; an excuse to omit method or units.
- **Lifecycle:** captured/estimated → propagated or combined by an explicit
  method → reviewed, contested, or superseded.
- **Relations to other terms:** qualifies observations, evidence, candidates,
  assertions, standing, significance, and Validation Results; uncertainty
  dependencies are explicit Relationship Assertions.
- **Astronomy example:** A positional covariance associated with a catalogue
  coordinate, or a contested set of alternative entity matches.

### 3.17 Standing

- **Precise definition:** The astronomy-domain record of the selected ASA
  standing computation for a subject, based on declared evidence and structural
  inputs, before and separate from any Context-specific significance
  computation.
- **Classification:** Computed.
- **Permitted attributes:** standing-result identifier; subject; ASA dependency
  version/interface; computation policy/version; eligible input identifiers;
  structural/evidentiary components; result and scale semantics; Uncertainty;
  validity time; Provenance Record; Explanation Trace link.
- **Prohibited conflations:** Significance; permanent object worth; brightness;
  confidence; entity identity; hidden Context weighting.
- **Lifecycle:** requested → computed → accepted, invalid, contested, expired, or
  superseded when inputs or policy change.
- **Relations to other terms:** consumes Evidence and Relationships under the
  selected ASA contract; is one input to Significance; is inspected in an
  Explanation Trace and Validation Result.
- **Astronomy example:** A computed structural/evidentiary standing for a
  candidate in a galaxy model before asking whether it matters to star
  formation or observational interpretation.

### 3.18 Context

- **Precise definition:** A complete, versioned declaration of the question,
  scope, perspective, eligible evidence, relationship relevance, weighting or
  decision policy, exclusions, and output semantics for one Significance
  computation.
- **Classification:** Externally supplied when authorised by an operator or
  benchmark; computed only when derived by a separately authorised context
  construction policy.
- **Permitted attributes:** context identifier/version; question; subject scope;
  observer/reference frame; epoch/horizon; eligible Relationship Types and
  evidence; inclusion/exclusion rules; weighting policy; uncertainty policy;
  output scale; tie/missingness rules; authority; Provenance Record.
- **Prohibited conflations:** Astronomical System; query string alone; hidden
  prompt; Significance; global truth; mutable runtime defaults.
- **Lifecycle:** drafted → authorised/frozen → used → retired or superseded.
  Contexts used in benchmarks MUST be immutable for that benchmark version.
- **Relations to other terms:** governs Significance computation; references
  entities, Relationships, Evidence, Standing, and an observer when relevant;
  is recorded in Explanation Traces and Benchmarks.
- **Astronomy example:** A declaration asking which represented structures are
  relevant to interpreting an observation, with explicit band, observer, and
  evidence rules.

### 3.19 Significance

- **Precise definition:** A derived, context-specific result expressing a
  subject's relevance under exactly one declared Context and the selected ASA
  computation contract.
- **Classification:** Computed.
- **Permitted attributes:** significance-result identifier; subject; Context
  identifier/version; ASA dependency and computation policy versions; Standing
  input; eligible evidence and Relationship inputs; result/rank and scale
  semantics; Uncertainty; sensitivity information; validity time; Provenance
  Record; Explanation Trace.
- **Prohibited conflations:** intrinsic entity attribute; Standing; Confidence;
  brightness; proximity; visual dominance; importance for all purposes; truth.
- **Lifecycle:** requested with frozen Context → computed → validated or rejected
  for the run → expired/superseded when any input, context, or policy changes.
- **Relations to other terms:** consumes Context, Standing, Evidence, and
  Relationships; produces reasoning output; is audited by Explanation Trace and
  Validation Result. It MUST NOT be written onto an entity as permanent state.
- **Astronomy example:** The contextual relevance of a faint structural feature
  may differ between a structural-organisation context and an
  observer-interpretation context, with neither result claiming intrinsic
  importance.

### 3.20 Explanation Trace

- **Precise definition:** An inspectable, replay-oriented record showing how
  identified inputs, exclusions, policies, transformations, uncertainty rules,
  and intermediate results produced a specific reasoning output.
- **Classification:** Computed.
- **Permitted attributes:** trace identifier; output identifier; ordered or DAG
  steps; input/output record identifiers; Context and policy versions; rule or
  model identifiers; contribution values with semantics; excluded inputs and
  reasons; uncertainty propagation; warnings; stop conditions; Provenance
  Records.
- **Prohibited conflations:** post-hoc narrative; proof of correctness;
  provenance alone; model internals without input lineage; unsupported causal
  explanation.
- **Lifecycle:** generated atomically with output → completeness checked →
  retained, invalidated, or superseded with the output.
- **Relations to other terms:** connects Evidence, Relationships, Standing,
  Context, Significance, and Validation Results; supports reviewer inspection
  and repeatability.
- **Astronomy example:** A trace showing that a significance rank used specified
  membership and occlusion assertions, excluded an unavailable distance, and
  applied a frozen observational-interpretation context.

### 3.21 Ground Truth

- **Precise definition:** A versioned, scoped reference set accepted in advance
  for evaluating specified claims or outputs, with authority, limitations,
  uncertainty, and disagreement explicitly represented.
- **Classification:** Externally supplied, or computed only when a benchmark
  explicitly defines a derived reference procedure independent of the system
  under test.
- **Permitted attributes:** reference identifier/version; covered subjects and
  propositions; source authorities; label/value; units; Confidence and
  Uncertainty; adjudication method; temporal/frame scope; exclusions; licence;
  Evidence and Provenance Records.
- **Prohibited conflations:** astronomical reality in full; the illustrative
  image; system output; uncontested certainty; training data silently reused as
  held-out evaluation.
- **Lifecycle:** proposed → independently reviewed/adjudicated → frozen for a
  Benchmark → corrected only by a new version.
- **Relations to other terms:** supplies reference labels or values to a
  Benchmark; is compared with reasoning outputs to produce Validation Results;
  may contain contested alternatives.
- **Astronomy example:** A frozen set of catalogue-derived memberships and
  expert-reviewed relationship labels for a bounded sample and catalogue
  release.

### 3.22 Benchmark

- **Precise definition:** A frozen evaluation contract combining input set,
  Ground Truth, contexts, system/dependency versions, baselines, metrics,
  acceptance/falsification criteria, exclusions, and execution protocol.
- **Classification:** Externally supplied to the evaluated run as an authorised,
  frozen validation configuration.
- **Permitted attributes:** benchmark identifier/version; manifests and digests;
  train/tune/evaluation partitions; Ground Truth version; Context versions;
  baseline definitions; metrics; thresholds; seeds; run environment; ablations;
  negative controls; licences; Provenance Record.
- **Prohibited conflations:** dataset alone; demonstration; post-hoc metric
  selection; Validation Result; universal scientific test.
- **Lifecycle:** drafted → preregistered/frozen → executed without semantic
  changes → retired or superseded after results.
- **Relations to other terms:** binds Ground Truth, Context, inputs, baselines,
  and validation protocol; produces one or more Validation Results.
- **Astronomy example:** A held-out relationship-recovery and contextual-ranking
  evaluation over a versioned reference corpus.

### 3.23 Validation Result

- **Precise definition:** An immutable record of observed benchmark outcomes and
  whether a specific tested system version met each predeclared acceptance or
  falsification criterion.
- **Classification:** Computed, with externally supplied review status where
  applicable.
- **Permitted attributes:** result identifier; Benchmark version; tested commit,
  ASA dependency, data/schema/model/policy/context versions; environment; metric
  values with uncertainty; baseline comparisons; per-criterion pass/fail/
  indeterminate; exclusions; failures; trace references; reviewer status;
  Provenance Record.
- **Prohibited conflations:** scientific discovery; universal validation;
  programme ratification; demonstration success; only favourable metrics;
  conversational summary.
- **Lifecycle:** produced by frozen run → integrity checked → reviewed → accepted
  as a record, rejected for protocol violation, or superseded by a new run.
- **Relations to other terms:** evaluates outputs and Explanation Traces against
  a Benchmark and Ground Truth; may falsify a claimed benefit without altering
  source records.
- **Astronomy example:** A report that records relationship precision, ranking
  agreement, calibration, repeatability, and failed criteria for one exact run.

## 4. Classification summary and ownership

| Concept | Allowed epistemic class | Programme ownership |
|---|---|---|
| Observation | Observed / externally supplied | ASA-Astro |
| Observation Source | Observed / externally supplied | ASA-Astro |
| Detector Output | Observed / computed | ASA-Astro |
| Pixel | Observed / computed | ASA-Astro |
| Light Region | Computed | ASA-Astro |
| Candidate Entity | Inferred | ASA-Astro |
| Resolved Entity | Inferred / externally supplied | ASA-Astro |
| Composite Entity | Inferred / externally supplied | ASA-Astro |
| Astronomical System | Inferred / externally supplied | ASA-Astro |
| Relationship | Inferred / computed / externally supplied | ASA-Astro |
| Relationship Assertion | Inferred / computed / externally supplied | ASA-Astro |
| Relationship Type | Externally supplied to a run / computed if generated | ASA-Astro |
| Evidence Record | Any, explicitly declared | ASA-Astro profile |
| Provenance Record | Computed / externally supplied | ASA-Astro profile |
| Confidence | Computed / inferred / externally supplied | ASA-Astro profile |
| Uncertainty | Any, explicitly declared | ASA-Astro profile |
| Standing | Computed | ASA-owned role; ASA-Astro result profile |
| Context | Externally supplied / authorised computed | ASA-owned role; ASA-Astro declaration profile |
| Significance | Computed | ASA-owned role; ASA-Astro result profile |
| Explanation Trace | Computed | ASA-Astro adapter/validation artefact |
| Ground Truth | Externally supplied / independent derived reference | ASA-Astro validation harness |
| Benchmark | Externally supplied authorised configuration | ASA-Astro validation harness |
| Validation Result | Computed / externally reviewed | ASA-Astro validation harness |

The phrase “ASA-owned role” is a boundary marker, not a local definition of ASA.
The selected ASA dependency remains authoritative.

## 5. Lifecycle compatibility rules

- Lifecycle transitions MUST be events or immutable successor records; scientific
  history MUST NOT be overwritten.
- A rejected Candidate Entity MUST NOT become a negative observation unless the
  detector's sensitivity and rejection reason support that interpretation.
- A contested Resolved Entity or Relationship Assertion MUST remain usable only
  under policies that explicitly permit contested inputs.
- A superseded Context invalidates reuse of its Significance results as current,
  but the prior results remain reproducible history.
- A Validation Result whose Benchmark, Ground Truth, or provenance becomes
  invalid MUST be marked invalid for decision use; it MUST NOT be deleted.

## 6. Schema-readiness and falsification criteria

Each term is schema-ready only if a machine-readable representation can encode:

- its stable identity and version;
- epistemic classification;
- lifecycle state and predecessor/successor links;
- evidence, provenance, confidence, and uncertainty references as applicable;
- explicit missingness states;
- units, frame, epoch, and band where relevant;
- the prohibited separations expressed by distinct types or fields.

This ontology fails review if a proposed schema requires any of the following:

- storing Significance on an entity without a Context reference;
- using one field for relationship magnitude and Confidence;
- representing Candidate and Resolved Entity with no distinguishable state or
  resolution provenance;
- treating Pixels or Light Regions as entities by identifier reuse;
- emitting a derived numeric value without a Provenance Record;
- representing contested alternatives only by choosing one value;
- treating Ground Truth as unscoped absolute reality.
