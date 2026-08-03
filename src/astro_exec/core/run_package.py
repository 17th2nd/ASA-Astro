"""Complete empty run-package manufacture for Phase 2 dry runs."""

from __future__ import annotations

import platform
import sys
from pathlib import Path
from typing import Any

from astro_exec import __version__

from .canonical_json import canonical_bytes
from .config import ExecutionConfig
from .errors import ConfigurationError
from .frozen import verify_frozen_artefacts
from .hashing import sha256_file
from .ids import stable_identifier
from .lifecycle import RunLifecycle, RunState
from .logging import StructuredLogger
from .provenance import ProvenanceGraph, ProvenanceNode

_ARTEFACTS = {
    "config.snapshot.json": "diagnostic",
    "environment.json": "diagnostic",
    "frozen-artefacts.json": "diagnostic",
    "interfaces.json": "diagnostic",
    "logs/events.jsonl": "log",
    "manifest.json": "diagnostic",
    "provenance/graph.json": "diagnostic",
    "run.json": "diagnostic",
    "CHECKSUMS.sha256": "diagnostic",
}


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(value))


def _environment(repository_root: Path) -> dict[str, Any]:
    lock = repository_root / "requirements.lock"
    return {
        "astro_exec_version": __version__,
        "dependency_lock": {"path": "requirements.lock", "sha256": sha256_file(lock)},
        "implementation": platform.python_implementation(),
        "machine": platform.machine(),
        "python_version": platform.python_version(),
        "schema_version": "astro-exec-environment-v1",
        "system": platform.system(),
    }


def create_dry_run(
    output: str | Path,
    *,
    config: ExecutionConfig,
    repository_root: str | Path,
    run_label: str,
) -> str:
    """Verify inputs and create a complete non-scientific dry-run package.

    ``run_label`` contributes only to the content-derived run identifier and
    is not otherwise serialized, enabling G1 comparison after normalizing the
    run id. Existing output paths are never overwritten.
    """

    if not run_label:
        raise ConfigurationError("run_label must be non-empty")
    destination = Path(output)
    if destination.exists():
        raise ConfigurationError("run package path already exists", details={"path": str(destination)})
    root = Path(repository_root).resolve()
    run_id = stable_identifier("RUN", {"config_fingerprint": config.fingerprint, "run_label": run_label})
    lifecycle = RunLifecycle(run_id)
    lifecycle.transition(RunState.VERIFYING)
    verified = verify_frozen_artefacts(config, root)
    lifecycle.transition(RunState.VERIFIED)
    lifecycle.transition(RunState.MATERIALIZING)

    destination.mkdir(parents=True)
    logger = StructuredLogger(destination / "logs/events.jsonl", run_id)
    logger.emit("info", "dry-run-created", details={"state": RunState.CREATED.value})
    _write_json(destination / "config.snapshot.json", config.snapshot())
    _write_json(destination / "environment.json", _environment(root))
    _write_json(
        destination / "frozen-artefacts.json",
        {"artefacts": [item.to_record() for item in verified], "schema_version": "astro-exec-frozen-artefacts-v1"},
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
    config_node = ProvenanceNode.create("configuration", {"config_fingerprint": config.fingerprint})
    graph.add(config_node)
    artefact_nodes = []
    for item in verified:
        node = ProvenanceNode.create("frozen-artefact", item.to_record())
        graph.add(node)
        artefact_nodes.append(node)
    run_node = ProvenanceNode.create(
        "dry-run",
        {"evidence_level": "EH-0", "scientific_outputs": 0},
        tuple([config_node.node_id, *(node.node_id for node in artefact_nodes)]),
    )
    graph.add(run_node)
    _write_json(destination / "provenance/graph.json", graph.to_record())
    lifecycle.transition(RunState.DRY_RUN_COMPLETE)
    logger.emit("info", "dry-run-complete", details={"state": lifecycle.state.value})
    _write_json(
        destination / "run.json",
        {
            "artefacts": [{"classification": classification, "path": path} for path, classification in sorted(_ARTEFACTS.items())],
            "dry_run": True,
            "evidence_level": "EH-0",
            "run_id": run_id,
            "schema_version": "astro-exec-run-v1",
            "scientific_computation": False,
            "state": lifecycle.state.value,
        },
    )
    files = sorted(path for path in destination.rglob("*") if path.is_file() and path.name != "CHECKSUMS.sha256")
    checksums = "".join(f"{sha256_file(path)}  {path.relative_to(destination).as_posix()}\n" for path in files)
    (destination / "CHECKSUMS.sha256").write_text(checksums, encoding="ascii", newline="\n")
    return run_id
