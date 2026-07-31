#!/usr/bin/env python3
"""Build deterministic, complete ASA-Astro Phase 01 review archives.

The source corpus is read from one immutable Git commit, not from mutable
working-tree files. Source bytes are copied without transformation.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = BUNDLE_ROOT.parents[1]
CONFIG_PATH = BUNDLE_ROOT / "tooling" / "PACKAGING-CONFIG.json"
CORPUS_ROOT = BUNDLE_ROOT / "corpus"
ARCHIVE_ROOT = BUNDLE_ROOT / "archives"
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)

OWNER_BY_COMMIT = {
    "e57abe3b78dcd9de8409defecbf245cb40b60b34": "Codex D",
    "351cc578d3ad94fca87038a077419eb84458d7d4": "Codex A",
    "59b1817c07d3bc7e72d7353459c3177362e72a4e": "Codex B",
    "e3476fc01b3743a320af580d9054fa1e8cfddc6f": "Codex D",
    "520f790a363660bbd97abf7f0f45f73cacc2d739": "Codex C",
    "7fc6e97c6aee4da076750f3f7082bbcd82e7291b": "Codex D",
}

EXACT_ROLES = {
    ".gitignore": "Repository hygiene exclusions for generated and machine-local files.",
    "README.md": "Current repository entry point and bounded executable quick start.",
    "docs/architecture/REPOSITORY-STRUCTURE-0001.md": "Proposed minimal repository structure and operator collision boundaries.",
    "docs/foundation/ASA-ASTRO-0001-foundational-definition.md": "Foundational identity, scope, ASA boundary, evidence obligations, and falsification conditions.",
    "docs/integration/INTEGRATION-CONTRACT-REVIEW-0001.md": "Historical and Phase II integration-contract review across A, B, C, and D interfaces.",
    "docs/models/ASTRO-CONTEXT-MODEL-0001.md": "Normative astronomy-domain Context declaration model and required fields.",
    "docs/models/ASTRO-SIGNIFICANCE-MODEL-0001.md": "Provisional executable Standing and Significance formulas, weights, recursion, and limitations.",
    "docs/ontology/ASTRO-ONTOLOGY-0001.md": "Core ontology and lifecycle/epistemic separations.",
    "docs/ontology/ASTRO-RELATIONSHIP-TAXONOMY-0001.md": "Relationship type semantics, evidence rules, directionality, and propagation limits.",
    "docs/pipeline/CODEX-B-HANDOFF-0001.md": "Codex B observation-to-candidate-graph interface and integration handoff.",
    "docs/pipeline/OBSERVATION-TO-GRAPH-PIPELINE-0001.md": "Observation/evidence pipeline contract, algorithms, outputs, and scientific limits.",
    "docs/reasoning/CODEX-C-HANDOFF-0001.md": "Codex C Standing/Significance interface and integration handoff.",
    "docs/reports/CODEX-B-MANUFACTURING-REPORT-0001.md": "Codex B manufacturing evidence, tests, limitations, and ownership.",
    "docs/reports/CODEX-C-MANUFACTURING-REPORT-0001.md": "Codex C manufacturing evidence, tests, limitations, and ownership.",
    "docs/validation/ASTRO-VALIDATION-FRAMEWORK-0001.md": "Normative benchmark, baseline, ablation, calibration, and falsification framework.",
    "examples/parameters.json": "Declared deterministic observation-pipeline parameters.",
    "governance/decision-register.md": "Open human-authority architectural, scientific, validation, and integration decisions.",
    "governance/integration-issues.md": "Current integration defect register with severity, evidence, remedy, and status.",
    "pyproject.toml": "Python package metadata, runtime range, dependencies, and entry point.",
    "reports/ASA-ASTRO-POC-VALIDATION-REPORT-0001.md": "Historical and Phase II POC evidence, falsification disposition, and Insufficient evidence conclusion.",
    "reports/CODEX-D-MANUFACTURING-REPORT-0001.md": "Codex D integration/validation manufacturing history, tests, and limitations.",
    "requirements.lock": "Exact tested Python dependency versions.",
    "tests/fixtures/README.md": "Synthetic-fixture status and non-Ground-Truth warning.",
    "tests/integration/test_phase2_validation.py": "Executable Phase II end-to-end, identity, failure-preservation, and archive-independent validation tests.",
    "tests/integration/test_pipeline.py": "Executable observation-pipeline integration and determinism tests.",
    "tests/reasoning/test_engine.py": "Executable Standing, Context, Significance, uncertainty, recursion, baseline, and trace tests.",
    "tests/unit/test_detection_and_relationships.py": "Executable detection and candidate-relationship unit tests.",
    "tests/unit/test_models_and_schemas.py": "Executable model and JSON Schema contract tests.",
    "validation/README.md": "Phase II harness execution, output, environment, and claim-boundary instructions.",
    "validation/run_phase2.py": "Executable Phase II integration, benchmark, adversarial, ablation, explorer, and manifest harness.",
    "validation/results/phase2/ablation-results.json": "Generated component-ablation evidence.",
    "validation/results/phase2/adversarial-results.json": "Generated adversarial case register with passes, failures, and limitation.",
    "validation/results/phase2/benchmark-results.json": "Generated Context, baseline, ranking, and stability comparisons.",
    "validation/results/phase2/explanation-validation.json": "Generated Explanation Trace linkage and completeness checks.",
    "validation/results/phase2/explorer.html": "Self-contained lightweight visual inspection explorer.",
    "validation/results/phase2/input-manifest.json": "Generated identity and provenance manifest for Phase II input.",
    "validation/results/phase2/manifest.json": "Root generated SHA-256 manifest for Phase II artefacts.",
    "validation/results/phase2/reproducibility.json": "Generated repeat-run byte-identity and resource observations.",
    "validation/results/phase2/validation-summary.json": "Generated compact Phase II result counts and Insufficient evidence conclusion.",
}

MUST_READ_EXACT = {
    "README.md",
    "docs/architecture/REPOSITORY-STRUCTURE-0001.md",
    "docs/foundation/ASA-ASTRO-0001-foundational-definition.md",
    "docs/integration/INTEGRATION-CONTRACT-REVIEW-0001.md",
    "docs/models/ASTRO-CONTEXT-MODEL-0001.md",
    "docs/models/ASTRO-SIGNIFICANCE-MODEL-0001.md",
    "docs/ontology/ASTRO-ONTOLOGY-0001.md",
    "docs/ontology/ASTRO-RELATIONSHIP-TAXONOMY-0001.md",
    "docs/pipeline/CODEX-B-HANDOFF-0001.md",
    "docs/pipeline/OBSERVATION-TO-GRAPH-PIPELINE-0001.md",
    "docs/reasoning/CODEX-C-HANDOFF-0001.md",
    "docs/reports/CODEX-B-MANUFACTURING-REPORT-0001.md",
    "docs/reports/CODEX-C-MANUFACTURING-REPORT-0001.md",
    "docs/validation/ASTRO-VALIDATION-FRAMEWORK-0001.md",
    "governance/decision-register.md",
    "governance/integration-issues.md",
    "pyproject.toml",
    "requirements.lock",
    "reports/ASA-ASTRO-POC-VALIDATION-REPORT-0001.md",
    "reports/CODEX-D-MANUFACTURING-REPORT-0001.md",
    "src/asa_astro/evidence/detection.py",
    "src/asa_astro/evidence/graph.py",
    "src/asa_astro/evidence/pipeline.py",
    "src/asa_astro/evidence/validation.py",
    "src/asa_astro/reasoning/engine.py",
    "src/asa_astro/reasoning/models.py",
    "src/asa_astro/reasoning/validation.py",
    "tests/integration/test_phase2_validation.py",
    "tests/integration/test_pipeline.py",
    "tests/reasoning/test_engine.py",
    "tests/unit/test_detection_and_relationships.py",
    "tests/unit/test_models_and_schemas.py",
    "validation/README.md",
    "validation/run_phase2.py",
    "validation/results/phase2/ablation-results.json",
    "validation/results/phase2/adversarial-results.json",
    "validation/results/phase2/benchmark-results.json",
    "validation/results/phase2/explanation-validation.json",
    "validation/results/phase2/manifest.json",
    "validation/results/phase2/reproducibility.json",
    "validation/results/phase2/validation-summary.json",
}


@dataclass(frozen=True)
class SourceEntry:
    source_path: str
    corpus_path: str
    git_blob: str
    size_bytes: int
    sha256: str
    category: str
    owner: str
    last_commit: str
    classifications: tuple[str, ...]
    role: str
    must_read: bool
    depends_on: str


def load_config() -> dict[str, Any]:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def git_bytes(*args: str) -> bytes:
    return subprocess.run(
        ["git", *args], cwd=REPO_ROOT, check=True, stdout=subprocess.PIPE
    ).stdout


def git_text(*args: str) -> str:
    return git_bytes(*args).decode("utf-8").strip()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def category_for(path: str) -> str:
    if path.startswith("docs/foundation/"):
        return "foundation"
    if path.startswith("docs/ontology/"):
        return "ontology"
    if path.startswith("docs/architecture/") or path in {"README.md", ".gitignore"}:
        return "architecture"
    if path.startswith("docs/models/"):
        return "models"
    if path.startswith("schemas/"):
        return "schemas"
    if path.startswith("docs/pipeline/") or path.startswith("src/asa_astro/evidence/") or path in {
        "src/asa_astro/__init__.py",
        "src/asa_astro/cli.py",
    }:
        return "pipeline"
    if path.startswith("docs/reasoning/") or path.startswith("src/asa_astro/reasoning/"):
        return "reasoning"
    if path.startswith("docs/integration/"):
        return "integration"
    if path.startswith("governance/"):
        return "governance"
    if path.startswith("docs/reports/") or path.startswith("reports/"):
        return "reports"
    if path.startswith("tests/"):
        return "tests"
    if path.startswith("docs/validation/") or path.startswith("validation/"):
        return "validation"
    if path in {"pyproject.toml", "requirements.lock"} or path.startswith("examples/"):
        return "environment"
    raise ValueError(f"unclassified source path: {path}")


def classifications_for(path: str) -> tuple[str, ...]:
    normative = {
        "docs/foundation/ASA-ASTRO-0001-foundational-definition.md",
        "docs/models/ASTRO-CONTEXT-MODEL-0001.md",
        "docs/ontology/ASTRO-ONTOLOGY-0001.md",
        "docs/ontology/ASTRO-RELATIONSHIP-TAXONOMY-0001.md",
        "docs/validation/ASTRO-VALIDATION-FRAMEWORK-0001.md",
        "governance/decision-register.md",
    }
    if path in normative:
        return ("normative",)
    if path == "docs/architecture/REPOSITORY-STRUCTURE-0001.md":
        return ("provisional",)
    if path == "docs/models/ASTRO-SIGNIFICANCE-MODEL-0001.md":
        return ("provisional", "executable specification")
    if path.startswith("schemas/"):
        return ("provisional", "executable contract")
    if path.startswith("src/") or path == "validation/run_phase2.py":
        return ("provisional", "executable")
    if path.startswith("tests/") or path.startswith("validation/fixtures/"):
        return ("provisional", "executable test evidence")
    if path.startswith("validation/results/"):
        return ("generated", "evidentiary")
    if path.startswith("reports/") or path.startswith("docs/reports/"):
        return ("evidentiary", "historical")
    if path.startswith("docs/integration/") or path == "governance/integration-issues.md":
        return ("evidentiary", "historical")
    if path.startswith("docs/pipeline/") or path.startswith("docs/reasoning/"):
        return ("provisional", "evidentiary")
    if path in {"pyproject.toml", "requirements.lock", "examples/parameters.json"}:
        return ("executable configuration",)
    if path == "validation/README.md":
        return ("executable guidance", "evidentiary")
    return ("historical",)


def role_for(path: str) -> str:
    if path in EXACT_ROLES:
        return EXACT_ROLES[path]
    name = PurePosixPath(path).name
    stem = name.rsplit(".", 1)[0].replace("-", " ").replace("_", " ")
    if path.startswith("schemas/"):
        return f"Machine-readable JSON Schema contract for {stem}."
    if path.startswith("src/asa_astro/evidence/"):
        return f"Executable Codex B evidence-pipeline module: {stem}."
    if path.startswith("src/asa_astro/reasoning/"):
        return f"Executable Codex C reasoning module: {stem}."
    if path.startswith("tests/fixtures/"):
        return f"Deterministic synthetic test fixture or fixture generator: {stem}."
    if path.startswith("tests/"):
        return f"Executable repository test support: {stem}."
    if path.startswith("validation/fixtures/contexts/"):
        return f"Frozen Phase II Context fixture: {stem}."
    if path == "validation/fixtures/manual-priority.json":
        return "Generator-informed synthetic manual-priority comparator fixture; not Ground Truth."
    if path.startswith("validation/results/phase2/contexts/"):
        return f"Generated preserved Context input: {stem}."
    if "/reasoning/" in path and path.startswith("validation/results/"):
        result_roles = {
            "analysis": "Complete generated Standing/Significance analysis bundle.",
            "baselines": "Generated comparator rankings for one Context.",
            "context": "Exact Context copied into one reasoning bundle.",
            "explanation-traces": "Generated Explanation Trace records for one Context.",
            "manifest": "Generated content-hash manifest for one reasoning bundle.",
            "ranked-results": "Generated Context-specific rank order.",
            "significance-results": "Generated Context-bound Significance records.",
            "standing-results": "Generated Context-independent Standing records.",
        }
        return result_roles.get(stem, f"Generated reasoning evidence: {stem}.")
    if path.startswith("validation/results/phase2/evidence/source/"):
        return "Content-addressed synthetic input or metadata copy retained in the evidence bundle."
    if path.startswith("validation/results/phase2/evidence/"):
        return f"Generated Codex B evidence-bundle artefact: {stem}."
    if path.startswith("validation/results/phase2/input/"):
        return "Synthetic Phase II input retained as the harness input; not astronomical Ground Truth."
    if path.startswith("validation/results/"):
        return f"Generated Phase II validation evidence: {stem}."
    if path == "validation/.gitattributes":
        return "Git attribute declaration for generated validation content."
    if path == "validation/__init__.py":
        return "Python package marker for the Phase II validation harness."
    return f"Repository source artefact: {stem}."


def dependencies_for(path: str) -> str:
    if path.startswith("docs/foundation/"):
        return "supplied ASA-Astro directive"
    if path.startswith("docs/ontology/"):
        return "foundational definition"
    if path == "docs/models/ASTRO-CONTEXT-MODEL-0001.md":
        return "foundation; ontology; relationship taxonomy"
    if path == "docs/models/ASTRO-SIGNIFICANCE-MODEL-0001.md":
        return "A models/taxonomy; B graph/provenance contracts; open ASA dependency"
    if path.startswith("schemas/observation/") or path.startswith("schemas/entity/") or path == "schemas/common.schema.json":
        return "A ontology/taxonomy; B pipeline contract"
    if path.startswith("schemas/reasoning/"):
        return "A ontology/Context; C significance model; B graph contract"
    if path.startswith("src/asa_astro/evidence/") or path in {"src/asa_astro/__init__.py", "src/asa_astro/cli.py"}:
        return "B schemas; parameters; dependency lock"
    if path.startswith("src/asa_astro/reasoning/"):
        return "B graph/provenance; C schemas and significance model"
    if path.startswith("tests/reasoning/") or path.startswith("tests/fixtures/reasoning/"):
        return "C reasoning implementation and schemas"
    if path.startswith("tests/"):
        return "B pipeline/schemas or D Phase II harness, according to test path"
    if path == "validation/run_phase2.py" or path.startswith("validation/fixtures/"):
        return "B and C public interfaces; A validation framework"
    if path.startswith("validation/results/"):
        return "validation/run_phase2.py; frozen fixtures; source commit 7fc6e97"
    if path.startswith("reports/") or path.startswith("docs/integration/") or path == "governance/integration-issues.md":
        return "A/B/C artefacts and generated validation evidence available at report revision"
    if path.startswith("docs/reports/") or path.startswith("docs/pipeline/") or path.startswith("docs/reasoning/"):
        return "owning operator's source, schemas, fixtures, tests, and upstream contracts"
    if path == "governance/decision-register.md":
        return "human authority for closure"
    return "repository source commit"


def must_read(path: str) -> bool:
    return path in MUST_READ_EXACT or path.startswith("schemas/")


def source_tree(config: dict[str, Any]) -> list[tuple[str, str, int]]:
    raw = git_bytes("ls-tree", "-r", "-z", "-l", config["source_commit"])
    records: list[tuple[str, str, int]] = []
    for item in raw.split(b"\0"):
        if not item:
            continue
        metadata, encoded_path = item.split(b"\t", 1)
        mode, object_type, blob, size = metadata.decode("ascii").split()
        path = encoded_path.decode("utf-8")
        if mode == "120000":
            raise ValueError(f"source symlink is not permitted: {path}")
        if object_type != "blob" or mode not in {"100644", "100755"}:
            raise ValueError(f"unsupported Git entry {mode} {object_type}: {path}")
        records.append((path, blob, int(size)))
    return sorted(records)


def source_entries(config: dict[str, Any]) -> list[SourceEntry]:
    entries: list[SourceEntry] = []
    for path, blob, git_size in source_tree(config):
        data = git_bytes("show", f"{config['source_commit']}:{path}")
        if len(data) != git_size:
            raise ValueError(f"Git size mismatch for {path}")
        last_commit = git_text("log", "-1", "--format=%H", config["source_commit"], "--", path)
        owner = OWNER_BY_COMMIT.get(last_commit, "Repository / human authority")
        category = category_for(path)
        entries.append(
            SourceEntry(
                source_path=path,
                corpus_path=f"corpus/{category}/{path}",
                git_blob=blob,
                size_bytes=len(data),
                sha256=sha256_bytes(data),
                category=category,
                owner=owner,
                last_commit=last_commit,
                classifications=classifications_for(path),
                role=role_for(path),
                must_read=must_read(path),
                depends_on=dependencies_for(path),
            )
        )
    return entries


def ensure_safe_bundle_root() -> None:
    if BUNDLE_ROOT.name != "phase-01-poc-review" or BUNDLE_ROOT.parent.name != "review-packages":
        raise RuntimeError(f"refusing to build outside expected bundle root: {BUNDLE_ROOT}")
    if REPO_ROOT.name != "ASA-Astro":
        raise RuntimeError(f"refusing to build outside ASA-Astro: {REPO_ROOT}")


def write_source_corpus(config: dict[str, Any], entries: list[SourceEntry]) -> None:
    ensure_safe_bundle_root()
    if CORPUS_ROOT.exists():
        shutil.rmtree(CORPUS_ROOT)
    for entry in entries:
        target = BUNDLE_ROOT / entry.corpus_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(git_bytes("show", f"{config['source_commit']}:{entry.source_path}"))


def escape_table(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def write_source_index(config: dict[str, Any], entries: list[SourceEntry]) -> None:
    lines = [
        "# Source Index",
        "",
        f"- Source repository: `{config['source_repository']}`",
        f"- Source commit: `{config['source_commit']}`",
        f"- Tracked source files included: **{len(entries)}**",
        f"- Tracked source bytes included: **{sum(item.size_bytes for item in entries)}**",
        "",
        "Every tracked source path appears exactly once under a role-based corpus directory. “Must read” is navigation guidance, not an authority downgrade for rows marked No.",
        "",
        "Status values preserve the distinction among normative, provisional, executable, evidentiary, generated, and historical material. Multiple values may apply.",
        "",
        "| Source path | Corpus path | Role | Owner | Status | Must read | Depends on |",
        "|---|---|---|---|---|---:|---|",
    ]
    for entry in entries:
        lines.append(
            "| `{}` | `{}` | {} | {} | {} | {} | {} |".format(
                escape_table(entry.source_path),
                escape_table(entry.corpus_path),
                escape_table(entry.role),
                escape_table(entry.owner),
                escape_table(", ".join(entry.classifications)),
                "Yes" if entry.must_read else "No",
                escape_table(entry.depends_on),
            )
        )
    lines.extend(
        [
            "",
            "## Known absent source artefact",
            "",
            "No standalone Codex A manufacturing report exists at the source commit. This absence is recorded by `governance/integration-issues.md` (`INT-0002`). It is not filled from conversation history. The A commit and all A-owned source artefacts are present in the corpus.",
            "",
        ]
    )
    (BUNDLE_ROOT / "SOURCE-INDEX.md").write_text("\n".join(lines), encoding="utf-8")


def write_large_evidence(entries: list[SourceEntry]) -> None:
    selected = [
        entry
        for entry in entries
        if entry.size_bytes >= 100_000 or PurePosixPath(entry.source_path).suffix.lower() in {".png", ".ppm"}
    ]
    lines = [
        "# Large and Binary Evidence",
        "",
        "This register lists every included source artefact of at least 100,000 bytes and every included PNG/PPM binary, with its review purpose and source SHA-256.",
        "",
        "| Source path | Bytes | SHA-256 | Purpose |",
        "|---|---:|---|---|",
    ]
    for entry in selected:
        lines.append(
            f"| `{escape_table(entry.source_path)}` | {entry.size_bytes} | `{entry.sha256}` | {escape_table(entry.role)} |"
        )
    lines.extend(
        [
            "",
            "The two PPM paths with identical hashes are distinct paths in the authoritative source commit: one is the harness input and the other is the content-addressed source preserved by the evidence bundle.",
            "",
        ]
    )
    (BUNDLE_ROOT / "LARGE-EVIDENCE.md").write_text("\n".join(lines), encoding="utf-8")


def file_manifest_entry(path: Path, relative: str, metadata: dict[str, Any]) -> dict[str, Any]:
    data = path.read_bytes()
    return {
        "path": relative,
        "size_bytes": len(data),
        "sha256": sha256_bytes(data),
        **metadata,
    }


def packaging_metadata(relative: str) -> dict[str, Any]:
    if relative.startswith("gemini/") or relative.startswith("claude/"):
        classification = ["generated packaging", "model-specific review prompt"]
        role = "Model-specific independent review instruction."
        must = True
    elif relative.startswith("tooling/"):
        classification = ["generated packaging", "executable packaging tool"]
        role = "Deterministic package build, configuration, or validation tooling."
        must = False
    elif relative == "SOURCE-INDEX.md":
        classification = ["generated packaging", "source index"]
        role = "Path-level ownership, status, dependency, and reading index."
        must = True
    elif relative == "LARGE-EVIDENCE.md":
        classification = ["generated packaging", "evidence index"]
        role = "Large/binary source purpose and checksum register."
        must = True
    else:
        classification = ["generated packaging", "orientation"]
        role = "Non-authoritative package orientation and review boundary."
        must = True
    return {
        "origin": "generated_packaging",
        "source_path": None,
        "source_commit": None,
        "owner": "Codex A — packaging only",
        "classifications": classification,
        "role": role,
        "must_read": must,
    }


def source_metadata(entry: SourceEntry, config: dict[str, Any]) -> dict[str, Any]:
    return {
        "origin": "copied_repository_source",
        "source_path": entry.source_path,
        "source_commit": config["source_commit"],
        "git_blob": entry.git_blob,
        "owner": entry.owner,
        "last_commit": entry.last_commit,
        "classifications": list(entry.classifications),
        "role": entry.role,
        "must_read": entry.must_read,
    }


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def master_payload(config: dict[str, Any], entries: list[SourceEntry]) -> list[dict[str, Any]]:
    source_by_corpus = {entry.corpus_path: entry for entry in entries}
    payload: list[dict[str, Any]] = []
    for path in sorted(BUNDLE_ROOT.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(BUNDLE_ROOT).as_posix()
        if relative == "MANIFEST.json" or relative.startswith("archives/") or "__pycache__" in path.parts:
            continue
        if relative in source_by_corpus:
            metadata = source_metadata(source_by_corpus[relative], config)
        else:
            metadata = packaging_metadata(relative)
        payload.append(file_manifest_entry(path, relative, metadata))
    return payload


def write_master_manifest(config: dict[str, Any], entries: list[SourceEntry]) -> None:
    payload = master_payload(config, entries)
    manifest = {
        "schema_version": "1.0.0",
        "manifest_scope": "committed shared review-package source tree excluding archives and this self-referential manifest",
        "package_id": config["package_id"],
        "source_repository": config["source_repository"],
        "source_commit": config["source_commit"],
        "source_file_count": len(entries),
        "source_bytes": sum(entry.size_bytes for entry in entries),
        "payload_file_count": len(payload),
        "manifest_self_hash": None,
        "manifest_self_hash_reason": "A manifest cannot contain its own stable cryptographic hash.",
        "entries": payload,
        "known_source_gaps": config["known_source_gaps"],
        "excluded_classes": config["excluded_classes"],
    }
    (BUNDLE_ROOT / "MANIFEST.json").write_bytes(json_bytes(manifest))


def archive_payload_paths(reviewer: str) -> list[str]:
    common = [
        "README.md",
        "SOURCE-INDEX.md",
        "REVIEW-SCOPE.md",
        "REVIEWER-GUIDANCE.md",
        "LARGE-EVIDENCE.md",
    ]
    common.extend(
        path.relative_to(BUNDLE_ROOT).as_posix()
        for path in sorted(CORPUS_ROOT.rglob("*"))
        if path.is_file()
    )
    common.extend(
        path.relative_to(BUNDLE_ROOT).as_posix()
        for path in sorted((BUNDLE_ROOT / "tooling").rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts
    )
    prompt = {
        "gemini": "gemini/GEMINI-INDEPENDENT-REVIEW-PROMPT.md",
        "claude": "claude/CLAUDE-INDEPENDENT-REVIEW-PROMPT.md",
    }[reviewer]
    return sorted(set(common + [prompt]))


def archive_manifest(
    config: dict[str, Any], entries: list[SourceEntry], reviewer: str, relative_paths: list[str]
) -> bytes:
    source_by_corpus = {entry.corpus_path: entry for entry in entries}
    payload = []
    for relative in relative_paths:
        path = BUNDLE_ROOT / relative
        metadata = source_metadata(source_by_corpus[relative], config) if relative in source_by_corpus else packaging_metadata(relative)
        payload.append(file_manifest_entry(path, relative, metadata))
    value = {
        "schema_version": "1.0.0",
        "manifest_scope": f"complete {reviewer} reviewer archive excluding this self-referential manifest",
        "package_id": f"{config['package_id']}-{reviewer}",
        "reviewer": reviewer,
        "source_repository": config["source_repository"],
        "source_commit": config["source_commit"],
        "source_file_count": len(entries),
        "source_bytes": sum(entry.size_bytes for entry in entries),
        "payload_file_count": len(payload),
        "manifest_self_hash": None,
        "manifest_self_hash_reason": "A manifest cannot contain its own stable cryptographic hash.",
        "entries": payload,
        "known_source_gaps": config["known_source_gaps"],
        "excluded_classes": config["excluded_classes"],
    }
    return json_bytes(value)


def zip_write_bytes(archive: zipfile.ZipFile, member: str, data: bytes) -> None:
    pure = PurePosixPath(member)
    if pure.is_absolute() or ".." in pure.parts or ".git" in pure.parts:
        raise ValueError(f"unsafe archive member: {member}")
    info = zipfile.ZipInfo(member, FIXED_ZIP_TIME)
    info.create_system = 3
    info.external_attr = 0o100644 << 16
    info.compress_type = zipfile.ZIP_STORED
    archive.writestr(info, data)


def build_archive(
    config: dict[str, Any], entries: list[SourceEntry], reviewer: str, target: Path
) -> None:
    relative_paths = archive_payload_paths(reviewer)
    root_name = f"ASA-Astro-POC-Review-Package-{reviewer.capitalize()}"
    manifest_data = archive_manifest(config, entries, reviewer, relative_paths)
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_STORED, strict_timestamps=True) as archive:
        zip_write_bytes(archive, f"{root_name}/MANIFEST.json", manifest_data)
        for relative in relative_paths:
            zip_write_bytes(archive, f"{root_name}/{relative}", (BUNDLE_ROOT / relative).read_bytes())


def verify_archive_determinism(
    config: dict[str, Any], entries: list[SourceEntry], reviewer: str, actual: Path
) -> None:
    with tempfile.TemporaryDirectory(prefix=f"asa-astro-{reviewer}-archive-") as temp_dir:
        repeated = Path(temp_dir) / actual.name
        build_archive(config, entries, reviewer, repeated)
        if actual.read_bytes() != repeated.read_bytes():
            raise RuntimeError(f"archive is not byte-deterministic: {actual.name}")


def build_archives(config: dict[str, Any], entries: list[SourceEntry]) -> None:
    ensure_safe_bundle_root()
    if ARCHIVE_ROOT.exists():
        shutil.rmtree(ARCHIVE_ROOT)
    ARCHIVE_ROOT.mkdir(parents=True)
    checksums = []
    for reviewer in ("gemini", "claude"):
        target = ARCHIVE_ROOT / config["archives"][reviewer]
        build_archive(config, entries, reviewer, target)
        verify_archive_determinism(config, entries, reviewer, target)
        checksums.append(f"{sha256_bytes(target.read_bytes())}  {target.name}")
    (ARCHIVE_ROOT / "SHA256SUMS").write_text("\n".join(checksums) + "\n", encoding="ascii")


def main() -> None:
    ensure_safe_bundle_root()
    config = load_config()
    actual_commit = git_text("rev-parse", "--verify", config["source_commit"])
    if actual_commit != config["source_commit"]:
        raise RuntimeError("configured source commit does not resolve exactly")
    entries = source_entries(config)
    write_source_corpus(config, entries)
    write_source_index(config, entries)
    write_large_evidence(entries)
    write_master_manifest(config, entries)
    build_archives(config, entries)
    print(f"Built {len(entries)} source files from {config['source_commit']}")
    for reviewer in ("gemini", "claude"):
        path = ARCHIVE_ROOT / config["archives"][reviewer]
        print(f"{path.name}: {path.stat().st_size} bytes {sha256_bytes(path.read_bytes())}")


if __name__ == "__main__":
    main()
