"""Import-boundary and package-layout contracts for G1."""

from __future__ import annotations

import ast
import importlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "src/astro_exec"
FORBIDDEN_RENDERERS = {"bokeh", "godot", "matplotlib", "plotly", "pygame", "pyqt", "unity"}


class ArchitectureTests(unittest.TestCase):
    """Prove the new engine is independent from legacy and rendering packages."""

    def test_astro_exec_does_not_import_asa_astro_or_renderers(self) -> None:
        forbidden: list[tuple[str, str]] = []
        for path in PACKAGE.rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                names = [alias.name for alias in node.names] if isinstance(node, ast.Import) else [node.module or ""] if isinstance(node, ast.ImportFrom) else []
                for name in names:
                    root = name.split(".", 1)[0].lower()
                    if root == "asa_astro" or root in FORBIDDEN_RENDERERS:
                        forbidden.append((path.relative_to(ROOT).as_posix(), name))
        self.assertEqual(forbidden, [])

    def test_declared_package_namespaces_import(self) -> None:
        modules = (
            "astro_exec.analysis",
            "astro_exec.cli",
            "astro_exec.core",
            "astro_exec.data",
            "astro_exec.estimator",
            "astro_exec.experiment",
            "astro_exec.orbits",
            "astro_exec.results",
            "astro_exec.roles",
        )
        self.assertEqual([importlib.import_module(name).__name__ for name in modules], list(modules))


if __name__ == "__main__":
    unittest.main()
