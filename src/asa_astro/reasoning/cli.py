"""Minimal local interface for reproducible Codex C reasoning runs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import tempfile
from typing import Any

from .engine import analyze, analyze_counterfactual
from .models import ALGORITHM_VERSION, content_sha256
from .validation import load_json_object


def _write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_analysis(
    output_directory: Path,
    analysis: dict[str, Any],
    additional_artifacts: dict[str, Any] | None = None,
) -> None:
    """Write a new deterministic result bundle without overwriting prior evidence."""
    output_directory = output_directory.resolve()
    if output_directory.exists():
        raise FileExistsError(f"output path already exists; refusing overwrite: {output_directory}")
    output_directory.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{output_directory.name}.tmp-", dir=output_directory.parent))
    try:
        artefacts = {
            "analysis.json": analysis,
            "standing-results.json": analysis["standing_results"],
            "significance-results.json": analysis["significance_results"],
            "ranked-results.json": analysis["ranked_results"],
            "explanation-traces.json": analysis["explanation_traces"],
            "baselines.json": analysis["baselines"],
            "context.json": analysis["context"],
        }
        artefacts.update(additional_artifacts or {})
        for name, value in artefacts.items():
            _write_json(temporary / name, value)
        manifest = {
            "algorithm_version": ALGORITHM_VERSION,
            "input_graph_sha256": analysis["input_graph_sha256"],
            "input_provenance_sha256": analysis["input_provenance_sha256"],
            "context_sha256": analysis["context_sha256"],
            "artifacts": [
                {"path": name, "content_sha256": content_sha256(value)}
                for name, value in sorted(artefacts.items())
            ],
        }
        _write_json(temporary / "manifest.json", manifest)
        temporary.replace(output_directory)
    except Exception:
        shutil.rmtree(temporary, ignore_errors=True)
        raise


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compute provisional Standing and contextual Significance")
    parser.add_argument("--graph", type=Path, required=True, help="Codex B graph.json")
    parser.add_argument("--provenance", type=Path, required=True, help="Codex B provenance.json")
    parser.add_argument("--context", type=Path, required=True, help="Context JSON conforming to schemas/reasoning/context.schema.json")
    parser.add_argument("--output", type=Path, required=True, help="new output directory")
    parser.add_argument("--counterfactual", type=Path, help="optional bounded intervention JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    graph = load_json_object(arguments.graph)
    provenance = load_json_object(arguments.provenance)
    context = load_json_object(arguments.context)
    if arguments.counterfactual:
        output = analyze_counterfactual(graph, provenance, context, load_json_object(arguments.counterfactual))
        # Counterfactual output contains a complete reproducible analysis under each state.
        comparison = {
            "intervention": output["intervention"],
            "baseline": output["baseline"]["ranked_results"],
            "counterfactual": output["counterfactual"]["ranked_results"],
            "comparison": output["comparison"],
        }
        write_analysis(arguments.output, output["counterfactual"], {"counterfactual-comparison.json": comparison})
    else:
        write_analysis(arguments.output, analyze(graph, provenance, context))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
