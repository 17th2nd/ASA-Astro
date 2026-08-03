"""Deterministic infrastructure-only run-package manufacture for Phase 2."""

from __future__ import annotations

import platform
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from astro_exec import __version__

from .canonical_json import canonical_bytes
from .config import ExecutionConfig
from .errors import ConfigurationError
from .frozen import verify_frozen_artefacts
from .hashing import sha256_file
from .ids import InvocationIdentity, RunIdentity
from .lifecycle import RunLifecycle, RunState
from .logging import StructuredLogger
from .provenance import ProvenanceGraph, ProvenanceNode

PACKAGE_SCHEMA_VERSION = "astro-exec-dry-run-package-v1"
_FULL_GIT_SHA = re.compile(r"^[0-9a-f]{40}$")
_ARTEFACTS: dict[str, tuple[str, bool]] = {
    "AUTHORITATIVE-CONTENT.sha256": ("diagnostic", False),
    "CHECKSUMS.sha256": ("diagnostic", False),
    "VERIFY.md": ("human-report", True),
    "config.snapshot.json": ("diagnostic", True),
    "environment.json": ("diagnostic", True),
    "frozen-artefacts.json": ("diagnostic", True),
    "interfaces.json": ("diagnostic", True),
    "lifecycle.json": ("diagnostic", True),
    "logs/events.jsonl": ("log", False),
    "manifest.json": ("diagnostic", True),
    "provenance/graph.json": ("diagnostic", True),
    "run.json": ("diagnostic", True),
}


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(value))


def _software_commit(repository_root: Path, declared: str | None) -> str:
    if declared is not None:
        if not _FULL_GIT_SHA.fullmatch(declared):
            raise ConfigurationError("software commit must be a full lowercase Git SHA-1")
        return declared
    try:
        result = subprocess.run(
            ["git", "-C", str(repository_root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise ConfigurationError(
            "software commit could not be resolved at the explicit repository root",
            details={"repository_root": str(repository_root)},
        ) from exc
    commit = result.stdout.strip()
    if not _FULL_GIT_SHA.fullmatch(commit):
        raise ConfigurationError("resolved software commit is not a full Git SHA-1")
    return commit


def _environment(repository_root: Path, software_commit: str) -> dict[str, Any]:
    lock = repository_root / "requirements.lock"
    return {
        "astro_exec_version": __version__,
        "dependency_lock": {"path": "requirements.lock", "sha256": sha256_file(lock)},
        "implementation": platform.python_implementation(),
        "machine": platform.machine(),
        "python_version": platform.python_version(),
        "schema_version": "astro-exec-environment-v1",
        "software_commit": software_commit,
        "system": platform.system(),
    }


def _checksum_inventory(root: Path, relative_paths: list[str]) -> str:
    return "".join(f"{sha256_file(root / path)}  {path}\n" for path in sorted(relative_paths))


def create_dry_run(
    output: str | Path,
    *,
    config: ExecutionConfig,
    repository_root: str | Path,
    run_label: str,
    software_commit: str | None = None,
) -> str:
    """Create a verified, deterministic, non-scientific dry-run package.

    The operational ``run_label`` is serialized only to a sibling
    ``<output>.invocation.json`` diagnostic record. It cannot influence run
    identity, authoritative bytes, or their checksum inventory. Existing
    package and invocation paths are never overwritten.
    """

    if not run_label:
        raise ConfigurationError("run_label must be non-empty")
    destination = Path(output)
    invocation_path = destination.with_name(destination.name + ".invocation.json")
    if destination.exists() or invocation_path.exists():
        raise ConfigurationError(
            "run package or invocation record path already exists",
            details={"invocation_path": str(invocation_path), "path": str(destination)},
        )
    root = Path(repository_root).resolve()

    verified = verify_frozen_artefacts(config, root)
    commit = _software_commit(root, software_commit)
    environment = _environment(root, commit)
    manifest_digest = sha256_file(root / config.frozen_manifest)
    identity_inputs = {
        "config_fingerprint": config.fingerprint,
        "environment": environment,
        "frozen_artefact_manifest_sha256": manifest_digest,
        "frozen_artefacts": [item.to_record() for item in verified],
        "package_schema_version": PACKAGE_SCHEMA_VERSION,
        "software_commit": commit,
    }
    run_id = str(RunIdentity.derive(identity_inputs))
    invocation = InvocationIdentity.derive({"label": run_label, "run_id": run_id})
    lifecycle = RunLifecycle(run_id)
    lifecycle.transition(RunState.VALIDATING)
    lifecycle.transition(RunState.READY)
    lifecycle.transition(RunState.EXECUTING)

    destination.mkdir(parents=True)
    _write_json(destination / "config.snapshot.json", config.snapshot())
    _write_json(destination / "environment.json", environment)
    _write_json(
        destination / "frozen-artefacts.json",
        {
            "artefacts": [item.to_record() for item in verified],
            "manifest_path": config.frozen_manifest,
            "manifest_sha256": manifest_digest,
            "schema_version": "astro-exec-frozen-verification-v1",
            "verification_status": "verified",
        },
    )
    _write_json(
        destination / "interfaces.json",
        {
            "estimator": {"implementation": "unresolved", "requirement": "UR-001"},
            "roles": [item.to_record() for item in config.roles],
            "schema_version": "astro-exec-interfaces-v1",
        },
    )
    _write_json(
        destination / "manifest.json",
        {
            "datasets": [],
            "dry_run": True,
            "posterior_states": [],
            "run_id": run_id,
            "schema_version": "astro-exec-manifest-v1",
            "sobol_points": [],
        },
    )

    graph = ProvenanceGraph()
    config_node = ProvenanceNode.create(
        "configuration",
        {"config_fingerprint": config.fingerprint, "configuration_id": str(config.identity)},
    )
    graph.add(config_node)
    environment_node = ProvenanceNode.create("dependency-environment", environment)
    graph.add(environment_node)
    artefact_nodes = []
    for item in verified:
        node = ProvenanceNode.create("frozen-artefact", item.to_record())
        graph.add(node)
        artefact_nodes.append(node)
    run_node = ProvenanceNode.create(
        "dry-run",
        {
            "evidence_level": "EH-0",
            "package_schema_version": PACKAGE_SCHEMA_VERSION,
            "run_id": run_id,
            "scientific_outputs": 0,
            "software_commit": commit,
        },
        tuple(sorted([config_node.node_id, environment_node.node_id, *(node.node_id for node in artefact_nodes)])),
    )
    graph.add(run_node)
    _write_json(destination / "provenance/graph.json", graph.to_record())

    lifecycle.transition(RunState.COMPLETED)
    lifecycle.seal()
    _write_json(destination / "lifecycle.json", lifecycle.to_record())
    logger = StructuredLogger(destination / "logs/events.jsonl", run_id, "run-package")
    logger.emit(
        "info",
        "dry-run-sealed",
        details={"scientific_computation": False, "state": lifecycle.state.value},
        provenance_id=run_node.node_id,
    )
    (destination / "VERIFY.md").write_text(
        "# ASTRO-EXEC Phase 2 dry-run verification\n\n"
        "Run `astro-exec verify <package-directory>` in the pinned dependency environment.\n"
        "Verification is offline and performs no scientific execution.\n",
        encoding="utf-8",
        newline="\n",
    )
    _write_json(
        destination / "run.json",
        {
            "artefacts": [
                {"authoritative_content": authoritative, "classification": classification, "path": path}
                for path, (classification, authoritative) in sorted(_ARTEFACTS.items())
            ],
            "diagnostic_logs": {
                "classification": "diagnostic-not-scientific-evidence",
                "path": "logs/events.jsonl",
            },
            "dry_run": True,
            "evidence_level": "EH-0",
            "run_id": run_id,
            "run_identity_inputs": identity_inputs,
            "schema_version": PACKAGE_SCHEMA_VERSION,
            "scientific_computation": False,
            "software_commit": commit,
            "state": lifecycle.state.value,
        },
    )

    authoritative_paths = [
        path
        for path, (_, authoritative) in _ARTEFACTS.items()
        if authoritative and path not in {"AUTHORITATIVE-CONTENT.sha256", "CHECKSUMS.sha256"}
    ]
    (destination / "AUTHORITATIVE-CONTENT.sha256").write_text(
        _checksum_inventory(destination, authoritative_paths),
        encoding="ascii",
        newline="\n",
    )
    complete_paths = [path.relative_to(destination).as_posix() for path in destination.rglob("*") if path.is_file()]
    (destination / "CHECKSUMS.sha256").write_text(
        _checksum_inventory(destination, complete_paths),
        encoding="ascii",
        newline="\n",
    )
    _write_json(
        invocation_path,
        {
            **invocation.to_record(),
            "label": run_label,
            "run_id": run_id,
            "schema_version": "astro-exec-invocation-v1",
        },
    )
    return run_id
