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
