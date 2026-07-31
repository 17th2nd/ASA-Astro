# ASA-Astro Integration Issue Register

**Register owner:** Codex D for integration findings only
**Date opened:** 2026-07-31
**Status:** Active working register
**Authority effect:** None. Entries record defects and required evidence; they do not allocate constitutional or architectural authority.

## Status Vocabulary

- `OPEN` — evidence or remedy is absent.
- `READY FOR VERIFICATION` — owner reports a remedy on `main`; Codex D has not verified it.
- `VERIFIED` — the stated verification method has passed against the cited commit.
- `CLOSED BY OPERATOR DECISION` — the human operator has explicitly dispositioned the issue.

## Issues

| ID | Source component | Severity | Evidence | Impact | Owner | Required remedy | Verification method | Status |
|---|---|---|---|---|---|---|---|---|
| INT-0001 | Repository baseline | BLOCKER | GitHub reports an empty Git repository; no commits or files exist on `main` | No inspectable project baseline or permanent upstream artefacts | Human operator / programme coordination | Establish the intended initial canonical history without creating parallel branches | GitHub `main` has a commit and repository instructions can be read | OPEN |
| INT-0002 | Codex A handoff | BLOCKER | No Codex A artefacts, ownership record, schemas, fixtures, or tests exist | Codex D cannot inspect or integrate A-owned interfaces | Codex A | Publish the already-designated A outputs with an ownership list, versions, provenance rules, fixtures, and tests | Paths exist on `main`; schemas/examples/tests pass; ownership is explicit | OPEN |
| INT-0003 | Codex B handoff | BLOCKER | No Codex B artefacts, ownership record, schemas, fixtures, or tests exist | Codex D cannot inspect or integrate B-owned interfaces | Codex B | Publish the already-designated B outputs with an ownership list, versions, provenance rules, fixtures, and tests | Paths exist on `main`; schemas/examples/tests pass; ownership is explicit | OPEN |
| INT-0004 | Codex C handoff | BLOCKER | No Codex C artefacts, ownership record, schemas, fixtures, or tests exist | Codex D cannot inspect or integrate C-owned interfaces | Codex C | Publish the already-designated C outputs with an ownership list, versions, provenance rules, fixtures, and tests | Paths exist on `main`; schemas/examples/tests pass; ownership is explicit | OPEN |
| INT-0005 | Operator ownership | BLOCKER | The directive names A/B/C outputs but does not map operators to components or paths | Specific remedies could create overlapping work or assign architecture without authority | Human operator / programme coordination | Record component and file ownership for A, B, C, and D | Ownership manifest is present and has no overlapping write ownership | OPEN |
| INT-0006 | ASA dependency | BLOCKER | No dependency manifest, ASA version, commit, tag, or import boundary exists | ASA-Astro could silently redefine or copy ASA | Human operator with responsible upstream operator | Declare an explicit, versioned dependency without copying constitutional material into ASA-Astro | Dependency resolves to the declared version and imported use is boundary-tested | OPEN |
| INT-0007 | Astronomy input | BLOCKER | No image, dataset, source identifier, licence, checksum, or acquisition provenance exists | Detection overlay and evidence preservation cannot be reproduced | Human operator / designated data owner | Provide or identify the approved illustrative input with licence and immutable checksum | Input manifest resolves and checksum matches | OPEN |
| INT-0008 | Scientific comparison | BLOCKER | No ground-truth source, catalogue reference, uncertainty limits, or comparison tolerance exists | Astronomical validation and uncertainty calibration cannot be claimed | Human operator / designated scientific owner | Identify versioned scientific comparison sources and permissible claims | Ground-truth manifest resolves; provenance and uncertainty are explicit | OPEN |
| INT-0009 | Environment and dependencies | BLOCKER | No executable code, environment specification, or lockfile exists | Clean-checkout reproduction cannot be tested | Owners of executable upstream components | Supply runtime requirements and locked dependencies with upstream implementation | Clean isolated installation and test command succeed | OPEN |
| INT-0010 | Expected outputs | BLOCKER | No fixture result, output schema, checksum manifest, or tolerance policy exists | Determinism and regression cannot be measured | Responsible upstream owners | Supply expected fixture outputs or formally bounded tolerances | Repeated clean runs match hashes or declared tolerances | OPEN |
| INT-0011 | Integration implementation | BLOCKER | INT-0002 through INT-0010 are open | Harness, visualisation, benchmark, adversarial and ablation work would require invented contracts | Codex D after upstream entry criteria pass | Implement only against reviewed contracts; do not silently cure upstream defects | Full pipeline and required checks pass from clean checkout | OPEN |
| INT-0012 | Validation conclusion | BLOCKER | No integrated execution has occurred | The final review question has no empirical answer | Codex D after INT-0011 | Run the approved benchmark and report failures and uncertainty | Validation report cites generated evidence and checksums | OPEN |

## Register Integrity

- No issue is marked verified without execution evidence.
- No issue allocates a new scientific identity, relationship, weight, or certainty.
- No issue treats brightness as significance.
- No issue treats synthetic success as astronomical confirmation.
- No issue authorises modification of ASA constitutional or canonical material.
