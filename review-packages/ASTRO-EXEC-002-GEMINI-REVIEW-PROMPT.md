# Gemini Independent Review — ASTRO-EXEC-002 Phase 2

You are the independent reviewer for `ASTRO-EXEC-002`, Phase 2 — Execution Skeleton, in
`17th2nd/ASA-Astro`.

## Authority and evidence

GitHub `main` is authoritative. The flat-packed directory is a disconnected convenience copy only.
Use `GEMINI-HANDOFF-MANIFEST.md` to map every flattened filename back to its repository path and to
verify its Git blob SHA or SHA-256 digest. Report any missing file, duplicate flattened name, digest
mismatch, stale commit, or unmanifested file as a blocking evidence defect.

## Review objective

Determine whether the verified commit satisfies exactly G1 in
`docs/execution/ASTRO-EXEC-001-ACCEPTANCE-GATES.md` and remains strictly within Phase 2 of
`docs/execution/ASTRO-EXEC-001-MANUFACTURING-ROADMAP.md`.

Review all implementation, tests, configuration, interface documentation, validation evidence,
requirements traceability, risk controls, unresolved requirements, dependency manifests and the
completion report supplied in the bundle.

## Required review questions

1. Does `astro_exec.core` supply canonical JSON, deterministic identifiers and hashing, immutable
   validated configuration and fingerprints, provenance primitives, structured errors and logging,
   frozen-artefact verification, and `LeakageGuard` without scientific behavior?
2. Is canonical serialization deterministic for every admitted JSON value and fail-closed for values
   outside the contract?
3. Can any content identifier, configuration fingerprint, provenance identifier, lifecycle output or
   run package depend on wall clock, hostname, PID, memory address, random state, map insertion order,
   or filesystem enumeration order?
4. Does frozen-artefact verification happen before output creation and abort on a missing, escaped or
   changed artefact?
5. Can the ASA-laboratory role read truth-laboratory outputs through direct paths, absolute paths,
   traversal, symlinks, undeclared roots, or a mutable capability object?
6. Are two dry runs byte-equivalent after replacing only their declared run identifiers and excluding
   the checksum inventory whose hashes cover those identifiers?
7. Does offline replay detect file addition, deletion, mutation, malformed checksums, configuration
   fingerprint drift, invalid run state, or an authoritative-scientific classification?
8. Does any module under `src/astro_exec/` import `asa_astro`, a renderer, or another forbidden or
   unpinned dependency?
9. Is `UR-001` preserved as unresolved, with no estimator algorithm or selection heuristic hidden in
   the interface skeleton?
10. Does any implementation cross into Phase 3 or later by adding datasets, acquisition, context
    values, orbit propagation, estimator logic, experiment comparison, statistics, claims, ledger
    mutation, rendering, astronomy mathematics, or scientific constants?
11. Are every public interface and downstream assumption documented sufficiently for Operators B–E
    to proceed without private conversation context?
12. Do tests validate all public modules, security boundaries, malformed inputs, drift, deterministic
    replay, CLI behavior, role isolation and import boundaries? Identify any tautological test.
13. Is the fresh-clone evidence sufficient, reproducible from the included manifests and consistent
    with the verified commit?
14. Were any frozen scientific artefact, historical `src/asa_astro/` file, result ledger, claim,
    experiment protocol, theory file or legacy fixture modified?
15. Do the open unresolved requirements remain open, correctly scoped, and fail closed where Phase 2
    touches them?

## Required method

- Recompute all supplied file digests before substantive review.
- Trace each G1 checkbox to implementation, tests and published validation evidence.
- Inspect implementation directly; do not accept the completion report as proof by assertion.
- Distinguish a software defect from a missing custodian ruling.
- Do not propose or implement scientific defaults for an unresolved requirement.
- Treat any Phase 3+ behavior, hidden legacy import, leakage path, nondeterministic identifier, drift
  warning-and-continue path, or unverified local evidence as blocking.

## Required output

Return:

1. verified commit and bundle-integrity verdict;
2. G1 criterion-by-criterion matrix with `PASS`, `FAIL`, or `INSUFFICIENT EVIDENCE`;
3. findings ordered by severity, each with flat filename, original repository path, line reference,
   violated contract, impact, and minimum remediation;
4. confirmation of Phase 2 scope containment;
5. unresolved-requirements assessment;
6. test and determinism assessment;
7. security and LeakageGuard assessment;
8. final verdict: `G1 PASS`, `G1 PASS WITH NON-BLOCKING FINDINGS`, or `G1 FAIL`.

Do not infer acceptance authority from this bundle. The human custodian retains formal gate authority.
