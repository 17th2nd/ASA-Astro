# ASA-Astro Integration Issue Register

**Register owner:** Codex D for integration findings only
**Date opened:** 2026-07-31
**Last reviewed commit:** `59b1817c07d3bc7e72d7353459c3177362e72a4e`
**Status:** Active working register
**Authority effect:** None. Entries record defects and evidence; they do not close human decisions.

## Status vocabulary

- `OPEN` — evidence or remedy is absent.
- `READY FOR VERIFICATION` — an owner reports a remedy on `main`; Codex D has not verified it.
- `VERIFIED` — the stated verification method passed at the cited commit.
- `CLOSED BY OPERATOR DECISION` — the human decision owner explicitly dispositioned the issue.

## Issues

| ID | Source component | Severity | Evidence | Impact | Owner | Required remedy | Verification method | Status |
|---|---|---|---|---|---|---|---|---|
| INT-0001 | Repository baseline | BLOCKER | Foundation, ontology, decision register, README, and executable handoff now exist through `59b1817` | Initial empty-repository blocker removed | Programme coordination | Preserve one canonical `main` history | Fetch `main`; commits `351cc57` and `59b1817` resolve | VERIFIED |
| INT-0002 | Codex A handoff | MAJOR | `351cc57` supplies foundation, ontology, context model, taxonomy, validation framework, repository structure, and decision register; no explicit A manufacturing/handoff report exists | Normative documents are reviewable but their operator handoff and authority trail are incomplete | Codex A | Publish an ownership/manufacturing record or identify the existing authoritative record | Named paths and authority basis are reviewable on `main` | OPEN |
| INT-0003 | Codex B handoff | MAJOR | `59b1817` supplies handoff, schemas, code, fixtures, lock, and tests; Codex D ran 11 tests successfully | A→B technical handoff is usable subject to defects below | Codex B | Preserve the named interface and address INT-0014 through INT-0017 | Published test command passes and two fixture runs are byte-equivalent | VERIFIED |
| INT-0004 | Codex C handoff | BLOCKER | No reasoning source, schemas, tests, handoff, or commit exists | No normalised Relationships, Standing, Context execution, Significance, or Explanation Trace | Codex C | Publish designated versioned outputs with tests and provenance | Named C commit exists; owned tests and A/B/C contract checks pass | OPEN |
| INT-0005 | Operator ownership | BLOCKER | `REPOSITORY-STRUCTURE-0001` calls boundaries proposed; `DR-0002` is open | Collision avoidance exists, but ownership authority remains unresolved | Human programme authority | Decide or explicitly reconcile A/B/C/D ownership | `DR-0002` is decided with affected paths and rationale | OPEN |
| INT-0006 | ASA dependency | BLOCKER | `DR-0001` is open; B records `unavailable_not_consumed` | Standing and Significance cannot be implemented without redefining ASA | Human programme authority with C | Select immutable dependency and consumed interface | Dependency resolves, integrity is checked, and boundary tests pass | OPEN |
| INT-0007 | Astronomical input | BLOCKER | Only a generated synthetic PPM exists; no authorised astronomical source manifest exists | No image-derived astronomical demonstration or validation | Human data owner | Supply approved source, licence/use authority, metadata, and checksum | Manifest resolves and bytes match the declared digest | OPEN |
| INT-0008 | Scientific comparison | BLOCKER | `DR-0004` is open; no Ground Truth/reference manifest exists | Scientific accuracy, calibration, and hierarchy recovery cannot be measured | Human scientific authority | Select scoped independent references and permissible claims | Frozen reference manifest, versions, uncertainty, and tolerances resolve | OPEN |
| INT-0009 | Environment and dependencies | BLOCKER | B locks packages and passes on CPython 3.12.3; no C environment exists and `pyproject.toml` permits untested Python `>=3.11` | B is reproducible locally, but end-to-end clean-checkout environment is undefined | C and D after C handoff | Extend the lock/environment contract and clarify supported Python versions | Clean isolated full run and test suite pass at a named commit | OPEN |
| INT-0010 | Expected outputs | BLOCKER | B has assertions but no committed output checksum manifest; no C outputs or tolerances exist | Regression and full-pipeline determinism lack a frozen oracle | B for B outputs; C/D for later stages | Publish exact checksums or formally bounded tolerances tied to commits | Repeated clean runs match the frozen expectation | OPEN |
| INT-0011 | Integration implementation | BLOCKER | INT-0004 through INT-0010 remain open | Complete harness, explorer, benchmarks, adversarial tests, and ablations would require invented contracts | Codex D after entry criteria pass | Implement only against reviewed canonical contracts | Required end-to-end outputs and checks pass from clean checkout | OPEN |
| INT-0012 | Validation conclusion | BLOCKER | No Standing, Significance, baselines, astronomical data, or Ground Truth exist | Central comparison with naive visual prominence has no empirical answer | Codex D after INT-0011 | Run frozen benchmark and report uncertainty/failures | Validation report cites immutable outputs and checksums | OPEN |
| INT-0013 | Shared-workspace handoff | MAJOR | A and B transient files were excluded until commits `351cc57` and `59b1817` reached GitHub | Moving-workspace integration risk was controlled | A/B owners and Codex D | Continue commit-based handoffs and path ownership | GitHub commits resolve; only Codex D paths remain modified/untracked | VERIFIED |
| INT-0014 | B schema identifiers | MAJOR | Nested schemas declare flattened `$id` URIs that do not match repository paths | External `$ref` resolution depends on B's preload registry and is not portable by URI | Codex B | Align `$id` with canonical locations or publish a versioned bundle/catalogue mapping | Standalone consumer resolves every schema from published identifiers | OPEN |
| INT-0015 | B candidate semantics | MAJOR | Encoded brightness/shape/proximity produce foreground/background/companion candidate labels despite unavailable depth/association | Downstream logic may consume invented astronomical placement or identity | Codex B, reviewed with A/C | Rename to image-morphology terms or enforce an approved non-admissibility mapping | Negative tests prove labels cannot become depth, identity, membership, or significance evidence | OPEN |
| INT-0016 | A/B lifecycle contract | MAJOR | Embedded Confidence/Uncertainty lack independent IDs; record schemas lack predecessor/successor lineage required by A schema-readiness criteria | Supersession, contestation, and immutable history cannot be fully represented | Codex A and B | Clarify bounded value-object exception or extend schemas with lifecycle/provenance identity | Positive and negative lifecycle fixtures validate against the agreed contract | OPEN |
| INT-0017 | B report reproducibility | MAJOR | B report cites `run-d50f4234b9d4f31bbcaa`; canonical command at `59b1817` emits stable `run-59e1a9f3c29ee9f5043c` | Reported expected output is not reproducible from its published commit | Codex B | Correct the report and add commit-tied expected hashes | Independent run matches corrected ID and checksum manifest | OPEN |

## Register integrity

- No open human decision was silently closed.
- `VERIFIED` means only the stated technical condition passed.
- Synthetic success is not astronomical confirmation.
- Brightness is not accepted as significance.
- No entry authorises ASA mutation or local redefinition.
