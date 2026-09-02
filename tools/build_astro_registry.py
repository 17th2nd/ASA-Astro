#!/usr/bin/env python3
"""Compose Astro's relationship-type facet from ``registry/domains/astro.candidate.json``.

Uses the pinned ASA kernel's own ``compose_domain`` (kernel/tools/build_registry.py) so the
facet is validated by ASA code, then writes it into Astro's ``registry/`` — the ASA tool only
writes into the ASA tree (recorded in temp/astro-asa-integration.md).

    python3 tools/build_astro_registry.py           # write registry/relationship_types.astro.candidate.json
    python3 tools/build_astro_registry.py --check   # verify byte-stability
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astro.asa.locator import ensure_importable  # noqa: E402

DOMAIN = ROOT / "registry" / "domains" / "astro.candidate.json"
OUT = ROOT / "registry" / "relationship_types.astro.candidate.json"


def compose() -> dict:
    kdir = ensure_importable()
    spec = importlib.util.spec_from_file_location("asa_build_registry", kdir / "tools" / "build_registry.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    doc, _asa_path = module.compose_domain(DOMAIN)
    from asa_kernel.registry import validate_registry_document

    diags = validate_registry_document(doc)
    if diags:
        raise SystemExit("registry facet rejected by ASA: " + "; ".join(str(d.to_dict()) for d in diags))
    return doc


def main(argv: list[str]) -> int:
    doc = compose()
    text = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
    if "--check" in argv:
        ok = OUT.exists() and OUT.read_text(encoding="utf-8") == text
        print(("astro facet byte-stable; " if ok else "astro facet NOT byte-stable; ") + "digest " + doc["digest"])
        return 0 if ok else 1
    OUT.write_text(text, encoding="utf-8")
    print("wrote", OUT.relative_to(ROOT), "records", len(doc["types"]), "digest", doc["digest"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
