"""Argparse CLI for Phase 2 validation, dry-run manufacture, and replay."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from astro_exec import __version__
from astro_exec.core.canonical_json import canonical_text
from astro_exec.core.config import load_config
from astro_exec.core.errors import AstroExecError, ConfigurationError
from astro_exec.core.frozen import verify_frozen_artefacts
from astro_exec.core.replay import verify_run_package
from astro_exec.core.run_package import create_dry_run


def _config_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--config", type=Path, required=True, help="validated TOML configuration")


def _repository_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--repository-root", type=Path, default=Path.cwd(), help="repository containing declared artefacts")


def _dry_run_arguments(parser: argparse.ArgumentParser, *, require_flag: bool) -> None:
    if require_flag:
        parser.add_argument("--dry-run", action="store_true", help="required compatibility flag")
    _config_argument(parser)
    _repository_argument(parser)
    parser.add_argument("--output", type=Path, required=True, help="new run-package directory")
    parser.add_argument("--run-label", required=True, help="operational invocation label")


def build_parser() -> argparse.ArgumentParser:
    """Build the complete, non-scientific Phase 2 command contract."""

    parser = argparse.ArgumentParser(prog="astro-exec", description="ASA-Astro deterministic execution skeleton")
    subcommands = parser.add_subparsers(dest="command", required=True)
    subcommands.add_parser("version", help="report the astro_exec package version")

    validate_config = subcommands.add_parser("validate-config", help="validate and fingerprint configuration")
    _config_argument(validate_config)
    validate_frozen = subcommands.add_parser("validate-frozen", help="verify the declared frozen artefact set")
    _config_argument(validate_frozen)
    _repository_argument(validate_frozen)

    dry_run = subcommands.add_parser("dry-run", help="create a deterministic infrastructure-only package")
    _dry_run_arguments(dry_run, require_flag=False)
    run = subcommands.add_parser("run", help="compatibility alias for dry-run")
    _dry_run_arguments(run, require_flag=True)

    verify = subcommands.add_parser("verify", help="verify an existing dry-run package")
    verify.add_argument("package", type=Path, help="run-package directory")
    replay = subcommands.add_parser("replay", help="compatibility alias for verify")
    replay.add_argument("package", type=Path, help="run-package directory")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Execute the CLI and return zero on success or two on structured failure."""

    arguments = build_parser().parse_args(argv)
    try:
        if arguments.command == "version":
            print(canonical_text({"component": "astro_exec", "version": __version__}))
            return 0
        if arguments.command == "validate-config":
            config = load_config(arguments.config)
            print(canonical_text({"config_fingerprint": config.fingerprint, "schema_version": config.schema_version, "status": "valid"}))
            return 0
        if arguments.command == "validate-frozen":
            config = load_config(arguments.config)
            verified = verify_frozen_artefacts(config, arguments.repository_root)
            print(canonical_text({"artefact_count": len(verified), "status": "verified"}))
            return 0
        if arguments.command in {"dry-run", "run"}:
            if arguments.command == "run" and not arguments.dry_run:
                raise ConfigurationError("Phase 2 requires --dry-run")
            config = load_config(arguments.config)
            run_id = create_dry_run(
                arguments.output,
                config=config,
                repository_root=arguments.repository_root,
                run_label=arguments.run_label,
            )
            print(canonical_text({"output": str(arguments.output), "run_id": run_id, "status": "sealed"}))
            return 0
        report = verify_run_package(arguments.package)
        print(canonical_text(report.to_record()))
        return 0
    except (AstroExecError, OSError, ValueError) as exc:
        error = exc if isinstance(exc, AstroExecError) else ConfigurationError(str(exc))
        print(canonical_text(error.to_record()), file=sys.stderr)
        return 2
