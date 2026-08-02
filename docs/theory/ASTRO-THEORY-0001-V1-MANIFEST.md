# ASTRO-THEORY-0001 — Version 1 Manifest

Reproducible from Git objects and exact hashes. Every value below was computed from the repository, not transcribed.

| Field | Value |
|---|---|
| Manifest for | `ASTRO-THEORY-0001` Version 1 — Deterministic Core |
| Freeze date | 2026-08-02 (Australia/Brisbane) |
| Repository | `17th2nd/ASA-Astro`, branch `main` |
| Pre-freeze commit | `994b6223535d60dced3c06198f2930de37fbc3c0` |

## 1. Canonical theory

| Field | Value |
|---|---|
| Canonical path | `docs/theory/ASTRO-THEORY-0001.md` |
| **Pre-freeze verified mathematical-source blob** | `69a7846614847f479962827557924a31b4b45b26` |
| **Post-freeze Git blob** | `f6b4337e617a426fe1b62528272bc11bb8bda28f` |
| Post-freeze file SHA-256 | `c1289b3e8f096a91c82ed1bc912be31e798a289df26cc64dace76a06d8c1d56c` |
| Post-freeze size | 90,920 bytes |
| Post-freeze line count | 718 |
| Pre-freeze size | 89,425 bytes |
| Pre-freeze line count | 709 |
| Status | Part A **FROZEN**; Part B **Candidate, not frozen** |

### 1.1 Why the two theory blobs differ

**The post-freeze blob differs from the verified blob only because freeze metadata changed.** No mathematical content was altered. The differences are confined to:

- the document-control table in the preamble — status, version, freeze date, verified commit, verified source blob, verdict reference, recorded non-blocking finding, canonical location, supersession rule, amendment rule, verification lineage;
- the freeze-boundary paragraph, recording that Part A is frozen and Part B is not;
- a paragraph stating what the freeze does **not** claim;
- the closing status line, which previously read "Not frozen. Not verified."

Measured: **9 lines removed, 18 added**, all within those metadata regions.

### 1.2 Mathematical-body digest — the integrity control

The **mathematical body** is defined as the byte range from the `# PART A` heading through the final mathematical line `**OB-B4.**` inclusive. It contains all Part A and all Part B mathematics and excludes only the preamble metadata and the closing status line.

| Measure | Pre-freeze (verified source) | Post-freeze | Result |
|---|---|---|---|
| **SHA-256** | `383a9a8bf1d1d19a230caa79b3febcf6abddf293b6d83ed697cdf0dcf20c16c1` | `383a9a8bf1d1d19a230caa79b3febcf6abddf293b6d83ed697cdf0dcf20c16c1` | **IDENTICAL** |
| Lines | 686 | 686 | Identical |
| Bytes | 86,944 | 86,944 | Identical |
| `cmp` byte comparison | — | — | **Zero differing bytes** |

**This proves the verified mathematics was not altered by the freeze.**

### 1.3 Part B sub-digest

| Region | Pre-freeze | Post-freeze | Result |
|---|---|---|---|
| Part B **mathematical** content (`# PART B` … `**OB-B4.**`) | `31cd88df1dcd55ebeecf120e2f62a7bc54206ddfebf7d911ea75cbba8aded640` | `31cd88df1dcd55ebeecf120e2f62a7bc54206ddfebf7d911ea75cbba8aded640` | **IDENTICAL** |
| Part B full region including the closing status line | `05f1720f10f0a1c2670db644373a832ad26f5fb74e184e1dc1e463fc4d5a6c3c` | changed | Status line only |

The full-region hash changed **only** because the document's closing status line sits physically after the `# PART B` heading and previously asserted "Not frozen. Not verified." Leaving it would have published a false status. **No Part B mathematical text changed**, as the sub-digest proves. Part B's own status declaration — "Candidate · non-frozen · outside the consistency claim · outside any Version 1 verification claim" — was already correct and was **not** edited.

## 2. Verification lineage

Blobs read from commit `994b6223535d60dced3c06198f2930de37fbc3c0`. Each was confirmed directly against the repository, independently of the values quoted in the verdict.

| Artefact | Path | Git blob | SHA-256 | Bytes | Lines |
|---|---|---|---|---|---|
| **Final verdict** | `docs/theory/verification/ASTRO-THEORY-0001-FINAL-BINARY-FREEZE-VERDICT.md` | `680f0f31fe0ced20c3f73c35927f7441a7b4d787` | `5fc74efc5aa5489f47f112291f9ff01c5191a4b759897a9f300dd163528e7d30` | 14,887 | 176 |
| FFV-001 adjudication | `docs/theory/verification/ASTRO-THEORY-0001-FFV-001-ADJUDICATION.md` | `0cd476829e8ecf4c0b18d9677df25b4932f6772d` | `f3320fd6a2cc9fecc9a93667337254211a2b69bc3b718da9184df6fd3c23f433` | 8,974 | 117 |
| FFV-001 change map | `docs/theory/verification/ASTRO-THEORY-0001-FFV-001-CHANGE-MAP.md` | `2e5f12bd8f26e39f4248d7527bf02ca424b9b014` | `19aef20eb23a05d815d877c4cbac539bee9f13809c2c4839d2688979fd9f9b8e` | 7,103 | 96 |
| FFV-001 remediation report | `docs/theory/verification/ASTRO-THEORY-0001-FFV-001-REMEDIATION-REPORT.md` | `95b86bf8f7b0a509ad1c839db03b6de7b55e81c9` | `3be84edda2afffcc5fdde3e7c9691a2c186445c07b0a483075c01f54eafd74ab` | 11,766 | 237 |

**Status of each: preserved historical evidence. None was modified by this freeze.** Twelve further verification and remediation records from earlier rounds remain under `docs/theory/verification/`, likewise unmodified.

## 3. Freeze artefacts created

| Artefact | Path | Purpose | Status |
|---|---|---|---|
| Freeze record | `docs/theory/ASTRO-THEORY-0001-V1-FREEZE-RECORD.md` | Concise canonical statement of what is frozen and on what authority | Created by this freeze |
| Manifest | `docs/theory/ASTRO-THEORY-0001-V1-MANIFEST.md` | This document: exact hashes and integrity proof | Created by this freeze |
| Freeze report | `reports/ASTRO-THEORY-0001-V1-FREEZE-REPORT.md` | Full operational and constitutional record of the freeze action | Created by this freeze |

Digests for these three, and for the modified `README.md`, are recorded in the freeze report §14 after commit, since a file cannot contain its own hash.

## 4. Files modified by this freeze

| Path | Nature of change |
|---|---|
| `docs/theory/ASTRO-THEORY-0001.md` | Freeze metadata and boundary declarations only; mathematical body byte-identical |
| `README.md` | Additive canonical-programme-state section only; no existing statement altered |

## 5. Files explicitly excluded

No file below was staged or modified:

`docs/theory/verification/` (all 16 records) · `validation/benchmarks/ASTRO-EXP-0001.md` · `docs/claims/ASTRO-CLAIMS-0001.md` · `validation/results/ASTRO-RESULTS-0001.md` · `reports/ASTRO-V1-RESEARCH-CONTROLS-FREEZE-REPORT.md` · `docs/theory/ASTRO-THEORY-0001-CHANGE-MAP.md` · `docs/theory/ASTRO-THEORY-0001-FORMAL-DEFECT-RESOLUTION.md` · `src/` · `tests/` · `schemas/` · `examples/` · `governance/` · `09_Drafts/`

## 6. Duplicate-copy control

There is **exactly one** canonical copy of the theory, at `docs/theory/ASTRO-THEORY-0001.md`. Neither the freeze record, the manifest, nor the freeze report reproduces the theory text. No duplicate, mirror, or archival copy was created by this freeze.

## 7. Reproducing these values

```bash
git rev-parse 994b6223535d60dced3c06198f2930de37fbc3c0:docs/theory/ASTRO-THEORY-0001.md   # verified source blob
git hash-object docs/theory/ASTRO-THEORY-0001.md                                          # post-freeze blob

# mathematical-body digest, pre and post
A=$(grep -n '^# PART A' FILE | cut -d: -f1); L=$(grep -n '^\*\*OB-B4\.\*\*' FILE | cut -d: -f1)
sed -n "${A},${L}p" FILE | sha256sum
```
