"""Command-line entry point for the observation-to-graph pipeline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .evidence.models import DetectionParameters
from .evidence.pipeline import process_observation


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="asa-astro-observe",
        description="Register one image immutably and emit an auditable image-space candidate graph.",
    )
    parser.add_argument("input", type=Path, help="replaceable source image; never modified")
    parser.add_argument("--output", required=True, type=Path, help="new output directory; must not exist")
    parser.add_argument("--parameters", type=Path, help="JSON object overriding documented detector defaults")
    parser.add_argument("--metadata", type=Path, help="optional declared JSON metadata copied into the bundle")
    parser.add_argument(
        "--source-locator",
        help="stable source locator recorded in provenance; defaults to file:<input filename>",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    parameter_values = None
    if args.parameters:
        with args.parameters.open("r", encoding="utf-8") as source:
            parameter_values = json.load(source)
        if not isinstance(parameter_values, dict):
            raise ValueError("parameter file must contain a JSON object")
    parameters = DetectionParameters.from_mapping(parameter_values)
    result = process_observation(
        args.input,
        args.output,
        parameters=parameters,
        metadata_path=args.metadata,
        source_locator=args.source_locator,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
