# ASA-Astro Integration Contract Review 0001

**Operator:** Codex D — Integration, Benchmark, Visualisation, and Adversarial Validation
**Date:** 2026-07-31
**Reviewed canonical commit:** `59b1817c07d3bc7e72d7353459c3177362e72a4e`
**Status:** PARTIAL REVIEW COMPLETE; END-TO-END INTEGRATION BLOCKED
**Authority effect:** None. This review does not define ASA, approve an interface, allocate unresolved ownership, or authorise scientific claims.

## 1. Scope and review basis

The requested integration path is:

```text
astronomical image
→ preserved evidence
→ candidate entities
→ typed relationship graph
→ standing
→ context-dependent significance
→ explanation
→ baseline comparison
→ validation report
```

The review used only committed `main` state. Transient files that appeared while other operators
were manufacturing were not treated as handoffs until their commits reached GitHub.

Canonical inputs reviewed:

- initial Codex D blocker register: `e57abe3b78dcd9de8409defecbf245cb40b60b34`;
- foundation and ontology commit: `351cc578d3ad94fca87038a077419eb84458d7d4`;
- Codex B observation-to-candidate-graph commit:
  `59b1817c07d3bc7e72d7353459c3177362e72a4e`.

No Codex C reasoning implementation, handoff document, or commit was present.

## 2. Inspection and execution methods

Representative commands used:

```bash
git status --short --branch
git log --oneline --decorate --stat
git show --name-status --format=fuller 351cc57
git show --name-status --format=fuller 59b1817
find . -path './.git' -prune -o -type f -print | sort
rg -n 'Standing|Significance|weight|provenance|uncertainty|relationship' docs governance schemas src tests
jq -c '{id:."$id",title,required,additionalProperties}' schemas/**/*.json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s tests -v
```

The documented Codex B fixture and CLI sequence was run twice in separate `/tmp` directories.
`cmp` was used on `graph.json`, `provenance.json`, `manifest.json`, and `overlay.png`.

## 3. Interface inventory

| Source | Canonical evidence | Review result |
|---|---|---|
| Codex A foundation/ontology | Seven documents and decision register at `351cc57` | Reviewable |
| Codex B evidence pipeline | Schemas, code, tests, handoff, lock, and report at `59b1817` | Reviewable with defects |
| Codex C reasoning pipeline | No `src/asa_astro/reasoning/`, reasoning schemas, tests, handoff, or commit | Not reviewable |
| ASA dependency | `DR-0001` remains open; B records `unavailable_not_consumed` | Not available |
| Astronomical input | No authorised image manifest, licence, or scientific metadata | Not available |
| Ground Truth | `DR-0004` remains open | Not available |
| Frozen Context/weights | Semantic templates only; `DR-0008` remains open | Non-executable |

## 4. Compatible interfaces

The following A→B contracts are compatible at the reviewed commit:

1. B declares `ASTRO-ONTOLOGY-0001` and `ASTRO-RELATIONSHIP-TAXONOMY-0001`.
2. Observation Source, Observation, Detector Output, detection/Light Region, Evidence Record,
   Candidate Entity, candidate assertion, Confidence, Uncertainty, and Provenance are separate
   record types.
3. Candidate IDs are distinct from detection and evidence IDs.
4. Relationship strength and Confidence are separate values with separate derivations.
5. Candidate assertions carry source/target roles, directionality, evidence, uncertainty,
   classification, lifecycle status, and provenance.
6. Unknown, unavailable, contested, not-applicable, withheld, estimated, and bounded states are
   representable in the shared uncertainty vocabulary.
7. Encoded image intensity is marked uncalibrated and is not stored as Standing or Significance.
8. B emits no Standing or Significance field and explicitly stops at a pre-normalisation candidate
   graph.
9. Source bytes and optional metadata are content-addressed and copied without overwrite.
10. The synthetic fixture is consistently described as software regression input, not
    astronomical Ground Truth.

Codex B's 11 published tests passed under CPython 3.12.3. Two fixture runs produced byte-identical
graph, provenance, manifest, and overlay files.

## 5. Mismatches and defects

| ID | Severity | Evidence | Impact |
|---|---|---|---|
| ICR-M01 | BLOCKER | No Codex C handoff or reasoning implementation exists | The graph cannot proceed to normalised Relationships, Standing, Context validation, Significance, or Explanation Trace |
| ICR-M02 | BLOCKER | `DR-0001`, `DR-0008`, `DR-0009`, and `DR-0010` are open | Implementing Standing or Significance would invent ASA semantics, weights, and result meaning |
| ICR-M03 | BLOCKER | No authorised astronomical input or Ground Truth exists | Image-derived and scientific validation cannot run |
| ICR-M04 | MAJOR | Nested schema files declare flattened `$id` URIs such as `/schemas/candidate-entity.schema.json`, while the repository path is `schemas/entity/candidate-entity.schema.json` | External consumers following `$id` cannot resolve the canonical file layout unless they reproduce B's private preload registry |
| ICR-M05 | MAJOR | A's schema-readiness criteria require stable identity/version and lifecycle predecessor/successor links for each term; embedded B Confidence and Uncertainty objects have no independent ID or direct provenance record, and record schemas do not encode predecessor/successor lineage | The current schemas cannot represent all lifecycle and audit states required by the ontology |
| ICR-M06 | MAJOR | B maps encoded peak/shape/proximity to `likely_foreground_point_source`, `background_extended_object`, and `possible_companion_object` while its own documentation says depth and association are unavailable | Labels can be consumed as invented astronomical placement or identity despite caveats |
| ICR-M07 | MAJOR | B's report cites `run-d50f4234b9d4f31bbcaa`; the documented command at canonical `59b1817` reproducibly emits `run-59e1a9f3c29ee9f5043c` | The manufacturing report is stale relative to its commit and cannot serve as the expected-output oracle |
| ICR-M08 | MAJOR | B emits only a candidate Relationship Assertion contract; A assigns normalisation and reasoning to C, but no mapping/version exists | D cannot assume that B assertion types are established Relationships or scoring inputs |
| ICR-M09 | MINOR | README and lock specify tested CPython 3.12.3, while `pyproject.toml` permits Python `>=3.11` | Supported versus merely syntactically permitted runtimes are ambiguous |

No upstream file was changed to repair these defects.

## 6. Missing fields and artefacts

### A/B contract gaps

- independently addressable Confidence and Uncertainty record identities where the ontology
  requires those concepts to have lifecycle;
- predecessor, successor, supersession, and transition provenance;
- a public schema retrieval/bundle manifest mapping each `$id` to its repository path;
- an expected-output checksum manifest tied to `59b1817`;
- a normative mapping from B candidate assertions to C Relationship Assertions or Relationships;
- an explicit statement of whether image-morphology labels are admissible downstream features.

### Missing C and programme artefacts

- normalised Relationship schema and classification output;
- Standing request/result schema and executable adapter;
- Context schema, frozen declarations, and weight-policy artefacts;
- Significance request/result schema and executable adapter;
- Explanation Trace schema and executable output;
- immutable ASA dependency identity and interface;
- approved astronomical source manifest;
- independent reference/Ground Truth manifest;
- benchmark partitions, metrics, tolerances, and falsification thresholds.

These are review requirements, not definitions supplied by Codex D.

## 7. Ambiguous semantics

- Whether B's `primary_extended_object` may ever be used as a system anchor. B says no, but no C
  admission rule exists.
- Whether foreground/background/companion candidate labels are merely diagnostic strings or
  admissible inferential features.
- How multiple B assertions become one normalised Relationship without losing disagreement,
  evidence dependency, or lifecycle.
- Whether embedded Confidence and Uncertainty are immutable value objects or lifecycle-bearing
  ontology records.
- Which relationship types may affect Standing and under what ASA contract.
- Which Context authority may freeze weights and how arbitrary-weight sensitivity is judged.
- What output scale, tie rules, and cross-context comparison rules apply.

Codex D did not resolve these ambiguities.

## 8. Provenance observations and gaps

B's synthetic run records source and metadata SHA-256 values, code and schema-bundle hashes,
software versions, parameters, transformations, warnings, output identifiers, and explicit
unavailability of ASA and scientific Ground Truth. This is a strong bounded evidence chain.

Remaining gaps:

- no astronomical source authority, licence, instrument, band, epoch, or calibration;
- no C transformation provenance;
- no Context, weight, Standing, Significance, or explanation provenance;
- no mapping from B's code digest to a named Git commit inside the output bundle;
- no trustworthy execution-time policy;
- no independent reference-source provenance;
- no committed expected-result checksum set.

## 9. Scientific overclaim review

No physical relationship, object identity, Standing, Significance, or validation conclusion is
asserted as established in the B documentation.

The candidate labels `likely_foreground_point_source`, `background_extended_object`,
`unresolved_background_object_candidate`, and `possible_companion_object` are nevertheless
scientifically stronger than the encoded-image evidence. Their caveats and uncalibrated confidence
reduce but do not remove the semantic risk. A downstream consumer must not treat those labels as
depth, membership, or identity evidence.

The synthetic fixture names painted regions "companion" and "background" in generator variables.
Those names are fixture construction conveniences, not independent Ground Truth labels.

## 10. Required changes by owner

### Codex A

- Clarify whether embedded Confidence/Uncertainty value objects satisfy the ontology's
  stable-identity and lifecycle criteria.
- Reconcile `DR-0002` with the direct B and D assignments.
- Keep all ASA-owned semantics blocked until an immutable dependency is selected.

### Codex B

- Correct the report's expected run ID or tie it to the exact earlier code state.
- Provide a stable schema bundle/retrieval contract whose `$id` values resolve to canonical files.
- Replace or further constrain foreground/background/companion labels so image morphology cannot
  be mistaken for astronomical placement or association.
- Add lifecycle lineage required by the ontology, or document an approved bounded exception.
- Publish expected-output checksums for the canonical fixture command.

### Codex C

- Publish the designated reasoning handoff on canonical `main`.
- Define and test the B candidate-assertion to C Relationship mapping without promoting hypotheses
  to facts.
- Supply separate, provenance-bearing Standing, Context, Significance, and Explanation Trace
  contracts only after the ASA and policy decisions are authorised.
- Record all blocked parts explicitly rather than substituting local meanings.

### Human programme authority

- Decide `DR-0001` through `DR-0010` as applicable, especially ASA identity, ownership, data,
  Ground Truth, Context authority, Standing contract, and Significance semantics.
- Do not authorise scientific validation from the synthetic fixture.

## 11. Integration entry criteria

Codex D can manufacture the requested complete harness only when:

- a named C commit and handoff are present;
- upstream schemas and examples validate;
- the A/B/C mapping is explicit and owner-approved;
- an immutable ASA dependency resolves;
- at least two authorised frozen Contexts and weight policies exist;
- the astronomical input and reference sources have provenance and use authority;
- expected outputs or declared tolerances are frozen;
- upstream tests pass from the named commit;
- the candidate-label and schema-resolution defects are dispositioned.

## 12. Verdict

**PARTIAL A→B CONTRACT VERIFIED; COMPLETE INTEGRATION BLOCKED.**

The committed system reproducibly reaches preserved evidence, candidate entities, and a typed
candidate graph for a synthetic image. It does not reach established Relationships, Standing,
context-dependent Significance, Explanation Traces, baseline comparisons, or astronomical
validation. Building those stages now would violate open repository decisions and silently replace
the absent Codex C/ASA contracts.

## 13. Phase II superseding addendum — complete executable handoff

**Addendum date:** 2026-07-31
**Reinspection basis:** canonical GitHub `main` at
`520f790a363660bbd97abf7f0f45f73cacc2d739`
**History preserved:** Sections 1–12 remain the correct record of the earlier review at
`59b1817`. This addendum supersedes only statements about the then-absent Codex C handoff and the
then-unexecuted integrated pipeline.

### 13.1 Authoritative sequence reinspected

```text
351cc578d3ad94fca87038a077419eb84458d7d4  Codex A foundation and contracts
59b1817c07d3bc7e72d7353459c3177362e72a4e  Codex B evidence pipeline
e3476fc                                      Codex D partial review
520f790a363660bbd97abf7f0f45f73cacc2d739  Codex C reasoning pipeline
```

GitHub repository metadata and commit search were checked before local manufacturing. Local
`HEAD`, `refs/remotes/origin/main`, and GitHub `main` all resolved to `520f790...`; the worktree was
clean. The review then inspected all A, B, and C documents, schemas, source, fixtures, and tests.

Representative additional commands:

```bash
git status --short --branch
git rev-parse HEAD refs/remotes/origin/main
git log --oneline --decorate --all
git show --name-status --format=fuller 520f790
rg --files docs governance schemas src tests validation reports | sort
rg -n 'Context|Standing|Significance|uncertainty|contradict|evidence|provenance' \
  docs governance schemas src tests
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. \
  python3 -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. \
  python3 validation/run_phase2.py --output validation/results/phase2
```

### 13.2 Compatibility now verified

`ICR-M01` is superseded as an availability finding: C now supplies a handoff, three reasoning
schemas, source, CLI, fixtures, documentation, and ten tests. C consumes B's `graph.json` and
`provenance.json` directly and emits separate Standing Results, Significance Results, Explanation
Traces, rankings, and five baseline rankings. D executed the complete chain with no adapter or
upstream mutation:

```text
synthetic Observation Source
→ Evidence Records and Candidate Entities
→ candidate Relationship Assertions
→ Standing Results
→ five declared Context executions
→ Significance Results
→ Explanation Traces and baselines
```

Compatible details:

- graph and provenance `processing_run_id` identity is validated at the B→C boundary;
- candidate, detection, evidence, provenance, node, edge, Standing, Significance, and trace
  references resolve in the integrated bundle;
- C rejects duplicate node IDs, duplicate edge IDs, missing cited Evidence Records, unknown
  relationship types, and physical claims;
- Standing records are separate from candidate records and are byte-identical across all five
  Context runs;
- every Significance Result binds graph, provenance, Context, Standing Result, and Explanation
  Trace identities;
- the reasoning engine does not consume brightness or image-centre baseline values as
  Significance inputs;
- C explicitly declares its formula provisional and records
  `asa_dependency_status=unavailable_not_consumed` rather than claiming ASA conformance.

### 13.3 Remaining and newly observed defects

| ID | Severity | Observation | Consequence |
|---|---|---|---|
| ICR-P2-M01 | BLOCKER | No immutable ASA dependency, authorised astronomical input, or independent Ground Truth exists | Only synthetic engineering behaviour can be evaluated; neither scientific validity nor ASA conformance can be concluded |
| ICR-P2-M02 | MAJOR | C's executable Context schema omits A-model fields including research question, purpose class, target scope, reference system, feature policy, missingness policy, output semantics, and Context provenance reference | A Context document cannot round-trip through C's `additionalProperties: false` schema; semantic authority and missingness behaviour are not fully represented |
| ICR-P2-M03 | MAJOR | C directly converts B candidate assertions into supported edge vectors; no separate normalised Relationship record or disagreement resolution stage is emitted | The common conceptual `Relationship Assertion → Relationship Classification` boundary remains implicit and contradictions cannot be audited as a resolved classification |
| ICR-P2-M04 | CRITICAL | The same Evidence Record can appear in both `evidence_ids` and `contradicting_evidence_ids`; the engine accepts it and produces scores identical to the uncontested input | Contradictory relationship evidence has no scoring or admissibility effect |
| ICR-P2-M05 | CRITICAL | `_edge_vector` reports assertion `uncertainty_burden` but excludes it from `supported_weight` | Changing relationship-assertion uncertainty to `contested` leaves all scores unchanged |
| ICR-P2-M06 | CRITICAL | Contexts with zero eligible graph edges still emit 11 active, non-zero rankings through the information term | Missing star-formation or gravitational evidence is converted into apparent contextual results instead of abstention/indeterminate output |
| ICR-P2-M07 | MAJOR | Base-fixture Standing eigenvector computation records `converged: false` at iteration 64, its declared maximum | The output is deterministic, but the centrality component has no established numerical convergence for the reference run |
| ICR-P2-M08 | MAJOR | Raising an unresolved inferred `dark_or_occluding_region` to confidence 1.0 and `not_applicable` uncertainty is schema-valid and increases its score from `0.100958528681` to `0.719228201857`; no classification-specific warning is emitted | Upstream certainty can overstate an unresolved image hypothesis without a reasoning-layer safeguard; this is not a dark-matter identity claim |
| ICR-P2-M09 | MAJOR | Included direct trace contributions contain edge IDs but omit the edge's Evidence IDs | Evidence is resolvable only by joining the hash-bound input graph; the Explanation Trace is not self-contained for included evidence |
| ICR-P2-M10 | MAJOR | B's software identity hashes every repository schema, including downstream C schemas; the unchanged B pipeline now emits `run-d835245d6645c4394ff4` instead of its earlier run identities | A downstream schema addition changes B artifact identity, preventing component-scoped identity stability |
| ICR-P2-M11 | MAJOR | Flat schema `$id` values still do not match physical nested paths, now also across C's reasoning schemas | Portable schema discovery still depends on the repository's private preload strategy |
| ICR-P2-M12 | MAJOR | All Standing, Context, and relationship weights are provisional; extreme admissible single-component Contexts select two different top subjects | Traceability is present, but defensibility of the chosen weights is not established |
| ICR-P2-M13 | MINOR | Five Context declarations produce only two distinct ranking orders on the sole fixture | Context identity is isolated, but broad Context sensitivity is not demonstrated |

No A, B, or C file was changed to repair these findings.

### 13.4 Provenance and explanation disposition

The integrated run preserves source, metadata, parameters, software, schema bundle, graph,
provenance, Context, Standing, Significance, and trace hashes. Two independent full executions
produced 54 byte-identical upstream/context/reasoning artefacts. D's root manifest checks every
generated file except itself.

All 55 Explanation Traces resolve their Standing, Context, graph, provenance, direct edge,
propagated path, excluded evidence, confidence, and uncertainty references when evaluated with the
bound input bundle. They are therefore auditable as bundles, but not self-contained because
included direct contributions omit Evidence IDs. An output detached from its hash-bound graph is
insufficient.

### 13.5 Phase II contract verdict

**A→B→C EXECUTION COMPATIBLE FOR THE FROZEN SYNTHETIC ENGINEERING FIXTURE; SCIENTIFIC AND
CONSTITUTIONAL COMPATIBILITY UNRESOLVED.**

The former absence blocker is resolved. It is replaced by executable evidence of specific
contract defects. The interfaces can run together deterministically, but contradiction handling,
assertion uncertainty, absent-evidence behaviour, convergence, Context-model coverage, provisional
weights, and missing external authority prevent a stronger disposition.
