# ASTRO-RELATIONSHIP-TAXONOMY-0001 — Relationship Taxonomy

## Document control

| Field | Value |
|---|---|
| Status | Normative ASA-Astro astronomy-domain taxonomy |
| Purpose | Constrain relationship assertions and prevent untyped graph semantics |
| Depends on | `ASTRO-ONTOLOGY-0001.md` |

## 1. Taxonomy contract

A taxonomy entry defines permitted semantics; it does not assert that a
relationship exists. Every instance MUST be a Relationship Assertion with named
subjects, evidence, provenance, confidence, uncertainty, frame and epoch where
relevant, and a lifecycle state.

All types obey these rules:

1. Relationship magnitude or strength MUST be represented separately from
   Confidence.
2. `unknown`, `unavailable`, `contested`, and `not_applicable` MUST remain
   distinguishable from zero magnitude and false assertion.
3. Direction and roles MUST be encoded explicitly. Storage order MUST NOT imply
   scientific direction.
4. Symmetry MUST NOT be inferred from a visually symmetric representation.
5. Transitivity is prohibited unless a type-specific rule below permits it and
   the necessary frames, epochs, role semantics, and uncertainties are
   compatible.
6. Recursive propagation into Standing or Significance is prohibited by
   default. A permitted recursion rule MUST be versioned, bounded, cycle-safe,
   uncertainty-aware, and validated by ablation and negative control.
7. The same entity pair MAY carry multiple non-equivalent assertion types and
   competing assertions.
8. No assertion is upgraded to “established” merely by classification or graph
   insertion.

Confidence SHOULD use a calibrated numeric representation when calibration data
exist. Otherwise it MUST use a declared categorical vocabulary that includes an
uncalibrated state. A confidence value MUST identify its target proposition,
method, evidence set, and calibration scope.

## 2. Relationship types

### 2.1 Spatial

- **Definition:** A relation describing relative location, separation,
  orientation, adjacency, overlap, or alignment in a declared coordinate or
  reference frame.
- **Directionality:** Role-dependent. A displacement vector is directed from
  origin to target; separation is an unordered pair with an explicit symmetric
  subtype.
- **Symmetry:** Permitted only for symmetric subtypes such as scalar separation
  or overlap. Directional offsets and “in front of” are not symmetric.
- **Persistence:** Snapshot or interval scoped. It may change with epoch,
  observer, motion, frame, and measurement revision.
- **Expected units:** Angular units for sky-plane measures; length units for
  physical separation; dimensionless or angular units for alignment. Units,
  coordinate frame, epoch, and projection MUST be present.
- **Evidentiary basis:** Astrometric measurements, calibrated image geometry,
  catalogue coordinates, distance estimates, and declared transformations.
- **Confidence representation:** Confidence in the stated spatial proposition,
  separate from positional covariance or separation magnitude. Frame and
  cross-match uncertainty MUST be included.
- **Transitivity:** Generally prohibited. A limited directional ordering subtype
  MAY be transitive only within the same frame and epoch; proximity, adjacency,
  and overlap are not transitive.
- **Recursive propagation:** Prohibited by default. Spatial graph traversal MAY
  be used as an explicitly bounded feature, never as automatic significance.
- **Common failure modes:** Treating projected proximity as physical proximity;
  mixing frames or epochs; omitting distance uncertainty; converting image
  centrality into importance; assuming co-location establishes membership or
  causality.

### 2.2 Gravitational

- **Definition:** An evidence- or model-supported relation in which an estimated
  mass distribution contributes gravitational potential, acceleration, force,
  binding, lensing, or dynamical influence involving another subject.
- **Directionality:** Influence MUST state source mass/system and affected
  subject. Mutual interaction MAY be represented by two roles or a symmetric
  interaction subtype, but magnitudes need not be equal in the chosen measure.
- **Symmetry:** Physical interaction may be mutual; stored influence quantities
  such as acceleration are directional and not symmetric.
- **Persistence:** Time-, scale-, and model-dependent; valid only for a declared
  epoch/interval and mass model.
- **Expected units:** As appropriate to the asserted subtype: potential,
  acceleration, force, mass estimate, lensing angle, or dimensionless binding
  indicator. The subtype MUST constrain units.
- **Evidentiary basis:** Kinematics, dynamics, lensing observations, mass models,
  orbital evidence, or an identified external scientific reference. A visible
  image alone is insufficient.
- **Confidence representation:** Confidence in the gravitational interpretation,
  with measurement and model uncertainty separately recorded. Model-family
  dependence MUST be exposed.
- **Transitivity:** Prohibited. If A influences B and B influences C, a direct
  A–C gravitational assertion does not follow without computation and evidence.
- **Recursive propagation:** Prohibited by default. Multi-body or field
  propagation requires an explicit physical model, bounded numerical method,
  and validation; graph recursion is not a substitute.
- **Common failure modes:** Inferring mass from brightness without a stated
  model; treating correlation or membership as binding; ignoring reference
  frame and scale; confusing force, acceleration, potential, and confidence;
  asserting dark matter directly from an illustrative image.

### 2.3 Orbital

- **Definition:** A relation asserting that a subject follows, or is modelled as
  following, an orbit around a primary, barycentre, or system under a declared
  orbital model.
- **Directionality:** Directed from orbiting subject to primary/barycentre, with
  roles explicit. A mutual barycentric model MAY identify co-orbiting roles.
- **Symmetry:** Not symmetric; `orbits` and `is_orbited_by` are inverse roles.
- **Persistence:** Interval scoped and model-dependent. Orbital elements and
  bound status may be revised.
- **Expected units:** Time for period; length or angular units for axes; angle
  for orientation; dimensionless eccentricity; epoch and reference frame.
- **Evidentiary basis:** Time-series astrometry, radial velocity, timing,
  dynamics, or an identified catalogue/model. A single image is insufficient.
- **Confidence representation:** Confidence in orbital interpretation and, if
  separate, bound status; parameter posterior/intervals record element
  uncertainty.
- **Transitivity:** Prohibited. An object orbiting a component does not thereby
  orbit every containing system under the same semantics.
- **Recursive propagation:** Prohibited. Hierarchical orbital models MUST be
  explicit Composite/System structures with validated dynamics.
- **Common failure modes:** Treating apparent circular alignment as an orbit;
  confusing projected motion with bound motion; omitting barycentre or epoch;
  assuming membership implies orbit; collapsing parameter uncertainty into
  confidence.

### 2.4 Containment

- **Definition:** A directional boundary relation stating that one subject lies
  within the declared spatial, structural, or representational boundary of
  another.
- **Directionality:** Directed from contained subject to container; inverse role
  is `contains`.
- **Symmetry:** Not symmetric.
- **Persistence:** Depends on boundary kind. Representational containment may be
  fixed for a source; physical containment is epoch- and boundary-model scoped.
- **Expected units:** Usually none for the relation. Boundary geometry carries
  coordinate units, frame, epoch, and inclusion tolerance.
- **Evidentiary basis:** Explicit masks, catalogue/system boundaries, coordinate
  tests, structural models, or external references.
- **Confidence representation:** Confidence that the subject satisfies the
  declared boundary rule; boundary uncertainty remains separate.
- **Transitivity:** Permitted only when all links use compatible nested boundary
  semantics and frames. Image-region containment MUST NOT transitively imply
  astronomical-system containment.
- **Recursive propagation:** Structural ancestry MAY be traversed with a maximum
  depth and cycle detection. It MUST NOT automatically propagate Standing or
  Significance.
- **Common failure modes:** Mixing representation and physical containment;
  treating containment as membership or gravitational binding; using vague
  boundaries; assuming all nesting is transitive; double-counting nested
  components.

### 2.5 Membership

- **Definition:** A relation asserting that an entity participates as a member
  of an Astronomical System under a declared membership criterion.
- **Directionality:** Directed from member to system; inverse role is
  `has_member`.
- **Symmetry:** Not symmetric.
- **Persistence:** Criterion-, epoch-, and evidence-dependent; MAY be contested
  or probabilistic.
- **Expected units:** None for membership itself. Kinematic, positional, or
  other supporting values retain their own units.
- **Evidentiary basis:** Catalogue membership, kinematics, distance, chemistry,
  dynamics, or expert adjudication under an identified criterion.
- **Confidence representation:** Confidence or membership probability MUST name
  the criterion and calibration set; it is not relationship strength.
- **Transitivity:** Prohibited by default. Membership in a subsystem does not
  automatically establish membership in every enclosing system unless a
  versioned policy explicitly defines hierarchical inheritance.
- **Recursive propagation:** Prohibited by default. Bounded hierarchy traversal
  MAY be tested by ablation.
- **Common failure modes:** Treating containment, proximity, or visual overlap as
  membership; using catalogue inclusion without release provenance; assuming
  permanence; transitive membership inflation; confusing membership probability
  with significance.

### 2.6 Structural

- **Definition:** A relation describing a subject's role, adjacency,
  connectivity, hierarchy, or participation in a declared astronomical
  structure.
- **Directionality:** Defined by subtype and roles; `part_of_structure` is
  directed, while some adjacency subtypes may be symmetric.
- **Symmetry:** Never assumed. Each subtype MUST declare it.
- **Persistence:** Scale-, method-, and epoch-dependent; structural models may
  change with evidence.
- **Expected units:** Often none. Geometric or network measures MUST declare
  units or dimensionless semantics and scale.
- **Evidentiary basis:** Morphology, kinematics, catalogue structure, simulations
  used as models, or expert-labelled references. Visual pattern alone supports
  at most a provisional assertion.
- **Confidence representation:** Confidence in classification/role, with
  structural strength or centrality kept separate and method-specific.
- **Transitivity:** Prohibited except for an explicit `part_of` subtype meeting
  compatible hierarchy rules. Adjacency and connectivity are not transitive.
- **Recursive propagation:** Bounded structural propagation MAY be permitted by
  a versioned computation policy with cycle detection, decay/normalisation,
  uncertainty handling, and negative controls.
- **Common failure modes:** Equating visual salience with structure; confusing
  topology with causation; unbounded centrality recursion; mixing scales;
  treating a modelled structure as observed fact.

### 2.7 Causal

- **Definition:** A claim that a source event, process, or state contributes to
  producing or changing a target event, process, or state under a specified
  causal model.
- **Directionality:** Directed from proposed cause/contributor to effect.
- **Symmetry:** Not symmetric.
- **Persistence:** Event- or interval-scoped; causal mechanisms and validity
  conditions MUST be declared.
- **Expected units:** None for the relation itself. Effect size and time lag
  carry declared units and model semantics.
- **Evidentiary basis:** Domain theory, temporal evidence, controlled or natural
  comparison where possible, mechanistic modelling, and external scientific
  references. Correlation alone is insufficient.
- **Confidence representation:** Confidence in the causal proposition, separate
  from effect size and model fit; alternative causal explanations MUST remain
  representable.
- **Transitivity:** Prohibited. A causes/contributes to B and B to C does not
  establish a direct A–C causal assertion.
- **Recursive propagation:** Prohibited by default. Causal-chain reasoning MUST
  use an explicit acyclic or cycle-aware causal model with bounded depth and
  uncertainty propagation.
- **Common failure modes:** Correlation-as-causation; post hoc narratives;
  omitted confounders; using temporal order as sufficient proof; treating model
  explanation as ground truth; multiplying confidence down a chain without a
  valid model.

### 2.8 Energetic

- **Definition:** A relation asserting transfer, storage, injection, loss, or
  balance of energy between or within subjects under a declared physical model.
- **Directionality:** Directed for source-to-sink transfer; storage or balance
  subtypes use explicit roles.
- **Symmetry:** Not generally symmetric.
- **Persistence:** Event-, interval-, band-, and model-scoped.
- **Expected units:** Energy, power, flux, energy density, or dimensionless ratio
  as constrained by subtype, with frame and integration bounds.
- **Evidentiary basis:** Calibrated measurements, spectra, light curves,
  dynamics, physical models, or external references.
- **Confidence representation:** Confidence in transfer/mechanism, separate from
  energy magnitude and measurement uncertainty.
- **Transitivity:** Prohibited. Energy transfer through an intermediate does not
  establish an equivalent direct transfer.
- **Recursive propagation:** Only through an explicit conservation/transfer
  model with bounded system boundaries and error accounting; otherwise
  prohibited.
- **Common failure modes:** Confusing brightness with emitted energy or
  significance; missing distance/band corrections; double-counting flows;
  ignoring system boundaries; interpreting correlation as transfer.

### 2.9 Radiative

- **Definition:** A relation involving emission, absorption, scattering,
  illumination, transmission, or radiative interaction between a source,
  medium, target, and/or observer.
- **Directionality:** Directed along source–medium–target/observer roles; inverse
  role labels MUST be explicit.
- **Symmetry:** Not symmetric.
- **Persistence:** Time-, wavelength-, geometry-, and observer-dependent.
- **Expected units:** Spectral or integrated flux, luminosity, intensity,
  optical depth, wavelength/frequency, or dimensionless transmission, as
  appropriate. Band and frame are mandatory when relevant.
- **Evidentiary basis:** Calibrated photometry/spectroscopy, radiative-transfer
  modelling, time series, or external references.
- **Confidence representation:** Confidence in the interaction or source
  attribution, separate from measured radiative magnitude and calibration
  uncertainty.
- **Transitivity:** Prohibited. Radiation passing through multiple media requires
  a transfer model, not graph transitivity.
- **Recursive propagation:** Permitted only inside an explicit bounded
  radiative-transfer computation with uncertainty and convergence criteria.
- **Common failure modes:** Treating apparent brightness as luminosity or
  significance; ignoring extinction, band, redshift, distance, or detector
  response; attributing emission to the wrong entity; inferring causation from
  co-visibility.

### 2.10 Compositional

- **Definition:** A relation asserting that a subject has a component,
  constituent, abundance, material phase, or substructure under a declared
  composition model.
- **Directionality:** Directed from whole to component/constituent for
  `has_component`, with an inverse `component_of`; abundance roles are explicit.
- **Symmetry:** Not symmetric.
- **Persistence:** Scale-, epoch-, phase-, and model-dependent.
- **Expected units:** Dimensionless fraction, mass/number fraction, abundance
  convention, mass, or count, with normalisation basis and uncertainty.
- **Evidentiary basis:** Spectroscopy, resolved observations, dynamical/model
  inference, catalogue values, or expert references.
- **Confidence representation:** Confidence in component identity or abundance
  model, separate from fraction/value uncertainty.
- **Transitivity:** `component_of` MAY be transitively traversed only for
  compatible part-whole semantics. Abundances and material properties MUST NOT
  be transitively inherited without a composition calculation.
- **Recursive propagation:** Bounded component aggregation MAY be permitted with
  conservation, overlap, and double-counting rules; automatic significance
  propagation is prohibited.
- **Common failure modes:** Inferring composition from colour alone; mixing mass
  and number fractions; double-counting nested components; treating visible
  matter as total composition; inheriting component properties to the whole.

### 2.11 Temporal

- **Definition:** A relation ordering or overlapping observations, events,
  states, or validity intervals in a declared time standard.
- **Directionality:** Directed for `before`, `after`, `starts`, or `ends`;
  symmetric for explicitly symmetric overlap/equality subtypes.
- **Symmetry:** Subtype-specific.
- **Persistence:** The historical ordering is stable if timestamps are stable;
  inferred event intervals may be revised.
- **Expected units:** Time, duration, epoch, and time standard; ordering-only
  relations may be unitless but MUST cite source timestamps.
- **Evidentiary basis:** Observation timestamps, time-series analysis,
  chronologies, model-derived event intervals, or external records.
- **Confidence representation:** Confidence in ordering/overlap separate from
  timestamp or interval uncertainty.
- **Transitivity:** Permitted for strict `before`/`after` within compatible time
  standards; not permitted for overlap, near-simultaneity, correlation, or
  inferred developmental sequence by default.
- **Recursive propagation:** Bounded ordering closure MAY be computed; it MUST
  preserve uncertainty and MUST NOT create causal assertions.
- **Common failure modes:** Mixed time standards; treating observation time as
  source-event time without propagation correction; overlap-as-causation;
  transitive “near” relations; ignoring interval uncertainty.

### 2.12 Developmental

- **Definition:** A model-dependent relation placing a subject, state, or event
  in an astronomical formation or evolution sequence.
- **Directionality:** Directed from predecessor/earlier state or process to
  successor/later state, with model roles explicit.
- **Symmetry:** Not symmetric.
- **Persistence:** Historical/model-scoped; classification may change with model
  or evidence even though the underlying history does not.
- **Expected units:** Time or age where supported; otherwise a declared ordinal
  stage vocabulary. Stage numbers MUST NOT imply interval scale.
- **Evidentiary basis:** Population models, spectra, ages, simulations as models,
  time series, morphology with caveats, and external scientific references.
- **Confidence representation:** Confidence in stage/transition interpretation,
  separate from estimated age and model uncertainty.
- **Transitivity:** Prohibited by default. Sequence reachability MAY be derived
  within one explicit model but does not establish direct developmental
  ancestry or causation.
- **Recursive propagation:** Prohibited except in a bounded versioned state-
  transition model validated against reference sequences.
- **Common failure modes:** Treating visual morphology as an evolutionary fact;
  mixing incompatible models; assuming all systems follow one sequence;
  converting correlation into development; hiding model dependence.

### 2.13 Lineage or shared-origin

- **Definition:** A relation asserting derivation from, descent from, or a
  hypothesised common origin with another subject under a declared formation or
  provenance model.
- **Directionality:** `derived_from` is directed; `shares_origin_with` is
  symmetric. The subtype MUST be explicit.
- **Symmetry:** Subtype-specific.
- **Persistence:** Historical but epistemically revisable as evidence or origin
  models change.
- **Expected units:** Usually none. Age, chemical-distance, kinematic-distance,
  or model parameters retain their own units and semantics.
- **Evidentiary basis:** Chemical abundance patterns, kinematics, ages,
  simulations as models, provenance/custody for representations, and external
  references.
- **Confidence representation:** Confidence in the lineage/common-origin
  proposition, separate from similarity measures and parameter uncertainty.
- **Transitivity:** `derived_from` MAY be transitively traversed only within a
  declared lineage model. `shares_origin_with` is not automatically transitive.
- **Recursive propagation:** Bounded ancestry traversal MAY be permitted with
  cycle prohibition. It MUST NOT propagate properties or significance by
  inheritance.
- **Common failure modes:** Similarity-as-origin; shared location-as-lineage;
  confusing data provenance with astronomical origin; transitive clustering of
  weak similarities; treating simulations as observed history.

### 2.14 Observational

- **Definition:** A relation connecting an Observation, Observation Source,
  Detector Output, representation, instrument, observer, or entity candidate in
  the acquisition and representation chain.
- **Directionality:** Directed for `observed_by`, `produced_from`,
  `represented_in`, or `detected_in`; co-observation is explicitly symmetric.
- **Symmetry:** Subtype-specific; never inferred.
- **Persistence:** Usually fixed for an acquisition or derivation, while
  interpretation links may be revised.
- **Expected units:** None for lineage links. Acquisition values retain their
  own units, epoch, band, geometry, and calibration.
- **Evidentiary basis:** Source manifests, detector metadata, execution
  provenance, calibration records, and entity-resolution evidence.
- **Confidence representation:** Deterministic custody links use integrity
  status rather than artificial probability; interpretive `represented_in`
  links use calibrated or categorical Confidence.
- **Transitivity:** Only provenance-like `produced_from` paths may be traversed
  transitively. `detected_in`, `represented_in`, and co-observed relations are
  not transitive.
- **Recursive propagation:** Provenance traversal is permitted with cycle checks;
  scientific property or significance propagation is prohibited.
- **Common failure modes:** Entity/representation conflation; treating
  co-observation as physical association; losing calibration lineage; assigning
  certainty to a cross-match; confusing source custody with scientific support.

### 2.15 Occlusion

- **Definition:** An observer- and geometry-dependent relation asserting that a
  foreground subject or medium blocks, attenuates, or overlaps the line of sight
  to a background subject or signal.
- **Directionality:** Directed from occluding subject/medium to occluded target,
  with observer and line of sight explicit.
- **Symmetry:** Not symmetric.
- **Persistence:** Observer-, wavelength-, geometry-, and epoch-dependent.
- **Expected units:** Optical depth, attenuation/extinction, covering fraction,
  angular overlap, or no units for categorical occlusion; band is required when
  relevant.
- **Evidentiary basis:** Imaging geometry, multi-band observations, spectroscopy,
  extinction models, distance ordering, or external references.
- **Confidence representation:** Confidence in foreground/background ordering
  and occlusion interpretation, separate from attenuation magnitude.
- **Transitivity:** Prohibited. A occludes B and B occludes C does not establish a
  direct or equivalent A–C relation.
- **Recursive propagation:** Permitted only in an explicit bounded line-of-sight
  or radiative-transfer model; otherwise prohibited.
- **Common failure modes:** Interpreting low brightness as intrinsic faintness;
  missing observer or band; projected overlap as physical contact; assuming
  complete occlusion; confusing mask artefacts with astronomical occlusion.

### 2.16 Uncertainty dependency

- **Definition:** A relation stating that uncertainty, missingness, covariance,
  or contested status in one record affects the uncertainty of another declared
  value or proposition.
- **Directionality:** Directed from uncertainty source to dependent target.
- **Symmetry:** Not symmetric, although correlated records MAY use paired
  directional roles or a separate symmetric covariance representation.
- **Persistence:** Valid for specified model/input versions and invalidated when
  dependencies change.
- **Expected units:** None for dependency itself; sensitivity coefficients,
  covariance, or propagated uncertainty retain declared units.
- **Evidentiary basis:** Derivation graph, statistical model, calibration model,
  sensitivity analysis, or explicit expert dependency declaration.
- **Confidence representation:** Confidence in the dependency structure is
  separate from the magnitude of propagated uncertainty. Unvalidated dependency
  models MUST be marked uncalibrated.
- **Transitivity:** Not asserted as a scientific relation. Indirect dependency
  MAY be computed through an explicit derivation graph with correlation rules.
- **Recursive propagation:** Permitted only when bounded, cycle-safe, versioned,
  and validated. Cycles require a convergent joint model or MUST stop with an
  indeterminate result.
- **Common failure modes:** Assuming independence; double-counting correlated
  errors; multiplying confidence scores; unbounded cycles; converting unknown
  to zero; losing dependency links in aggregation.

### 2.17 Inferred dark-matter-mediated

- **Definition:** A model-dependent assertion that an observed or inferred
  relationship is mediated or materially explained by an inferred dark-matter
  mass distribution, while preserving that the mediator is inferred rather
  than directly established by visible light.
- **Directionality:** Subtype-specific. A mass-distribution-to-dynamical-effect
  assertion is directed; a shared-field relation MUST declare participant
  roles.
- **Symmetry:** Not assumed. The underlying gravitational interaction and the
  explanatory mediation assertion have distinct semantics.
- **Persistence:** Model-, scale-, epoch-, and dataset-dependent; always
  epistemically revisable.
- **Expected units:** The mediation relation itself may be unitless. Supporting
  mass density, potential, acceleration, lensing, or kinematic residuals retain
  their scientific units, frames, and uncertainty.
- **Evidentiary basis:** Independently sourced dynamics, lensing, mass modelling,
  or other scientifically accepted inference methods with explicit alternative
  models. The illustrative image alone is never sufficient.
- **Confidence representation:** Confidence MUST target the mediation hypothesis
  and identify model comparison/calibration. Measurement uncertainty,
  mass-model uncertainty, and alternative explanations remain separate.
- **Transitivity:** Prohibited. Two relations attributed to a modelled mass
  distribution do not establish a new mediated relation between their subjects.
- **Recursive propagation:** Prohibited by default. A validated physical field or
  probabilistic model MAY compute indirect effects; graph recursion MUST NOT
  manufacture hidden structure or significance.
- **Common failure modes:** Claiming direct dark-matter observation from light;
  using unexplained residuals as proof; suppressing baryonic or instrumental
  alternatives; treating a model as Ground Truth; equating invisibility with
  dark matter; propagating speculative mediation through a graph.

## 3. Relationship classification lifecycle

```text
proposed assertion
→ evidence and provenance linked
→ candidate type checked against domain/range and units
→ frame, epoch, roles, and uncertainty checked
→ classified for bounded use | contested | rejected | indeterminate
→ normalised Relationship view (optional)
→ standing/context/significance eligibility decision
→ validation and possible supersession
```

Classification MUST be reproducible from an assertion and taxonomy version.
Classification MAY yield `indeterminate`; it MUST NOT select the nearest type to
avoid a missing value.

## 4. Taxonomy validation and falsification criteria

An executable classifier or schema implementing this taxonomy MUST include:

- positive fixtures for every type and supported subtype;
- negative fixtures for every prohibited conflation;
- unit, frame, epoch, direction, and role validation;
- explicit tests that magnitude and Confidence cannot share one field;
- transitivity tests that reject forbidden derived edges;
- cycle and maximum-depth tests for any permitted recursion;
- round-trip tests that preserve evidence, provenance, uncertainty, and
  contested alternatives;
- a failure result for unsupported or ambiguous classifications.

The taxonomy is falsified as implementation-ready if two types cannot be
distinguished without hidden conventions, if a permitted propagation rule can
produce unbounded or evidence-free assertions, or if an illustrative image can
be used alone to establish a physical, causal, orbital, compositional,
developmental, lineage, or dark-matter-mediated relation.
