"""Argparse CLI for Phase 2 dry-run manufacture and offline replay."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from astro_exec.core.canonical_json import canonical_text
from astro_exec.core.config import load_config
from astro_exec.core.errors import AstroExecError, ConfigurationError
from astro_exec.core.replay import verify_run_package
from astro_exec.core.run_package import create_dry_run


def build_parser() -> argparse.ArgumentParser:
    """Build the stable Phase 2 command-line contract."""

    parser = argparse.ArgumentParser(prog="astro-exec", description="ASA-Astro deterministic execution skeleton")
    subcommands = parser.add_subparsers(dest="command", required=True)
    run = subcommands.add_parser("run", help="create a deterministic run package")
    run.add_argument("--dry-run", action="store_true", help="required Phase 2 non-scientific mode")
    run.add_argument("--config", type=Path, required=True, help="validated TOML configuration")
    run.add_argument("--repository-root", type=Path, default=Path.cwd(), help="repository containing frozen artefacts")
    run.add_argument("--output", type=Path, required=True, help="new run-package directory")
    run.add_argument("--run-label", required=True, help="external label used only to derive the run id")
    replay = subcommands.add_parser("replay", help="verify a completed run package offline")
    replay.add_argument("package", type=Path, help="run-package directory")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Execute the CLI and return zero on success or two on a structured failure."""

    arguments = build_parser().parse_args(argv)
    try:
        if arguments.command == "run":
            if not arguments.dry_run:
                raise ConfigurationError("Phase 2 requires --dry-run")
            config = load_config(arguments.config)
            run_id = create_dry_run(
                arguments.output,
                config=config,
                repository_root=arguments.repository_root,
                run_label=arguments.run_label,
            )
            print(canonical_text({"output": str(arguments.output), "run_id": run_id, "status": "DRY_RUN_COMPLETE"}))
            return 0
        report = verify_run_package(arguments.package)
        print(canonical_text(report.to_record()))
        return 0
    except (AstroExecError, OSError, ValueError) as exc:
        error = exc if isinstance(exc, AstroExecError) else ConfigurationError(str(exc))
        print(canonical_text(error.to_record()), file=sys.stderr)
        return 2
