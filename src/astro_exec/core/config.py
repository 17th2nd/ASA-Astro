"""Strict TOML configuration loading, validation, freezing, and fingerprinting."""

from __future__ import annotations

import re
import tomllib
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from .errors import ConfigurationError
from .hashing import fingerprint

CONFIG_SCHEMA_VERSION = "astro-exec-config-v1"
PHASE_2_MODE = "dry-run"
ROLE_NAMES = ("asalab", "custodian", "statistician", "truthlab")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")


def _keys(value: Mapping[str, Any], expected: set[str], location: str) -> None:
    actual = set(value)
    if actual != expected:
        raise ConfigurationError(
            "configuration keys do not match the frozen contract",
            details={"actual": sorted(actual), "expected": sorted(expected), "location": location},
        )


def _relative_path(value: Any, location: str) -> str:
    if not isinstance(value, str) or not value:
        raise ConfigurationError("path must be a non-empty string", details={"location": location})
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or "$" in value or "\\" in value:
        raise ConfigurationError("unsafe repository-relative path", details={"location": location, "path": value})
    return path.as_posix()


@dataclass(frozen=True, slots=True)
class FrozenArtefact:
    """Repository-relative path and expected SHA-256 for a frozen artefact."""

    path: str
    sha256: str

    def to_record(self) -> dict[str, str]:
        """Return the canonical configuration record."""

        return {"path": self.path, "sha256": self.sha256}


@dataclass(frozen=True, slots=True)
class RoleCapabilities:
    """Immutable filesystem capabilities assigned to one protocol role."""

    role: str
    read_roots: tuple[str, ...]
    write_roots: tuple[str, ...]

    def to_record(self) -> dict[str, Any]:
        """Return the canonical capability record."""

        return {
            "read_roots": list(self.read_roots),
            "role": self.role,
            "write_roots": list(self.write_roots),
        }


@dataclass(frozen=True, slots=True)
class ExecutionConfig:
    """Fully validated immutable Phase 2 execution configuration."""

    schema_version: str
    mode: str
    frozen_artefacts: tuple[FrozenArtefact, ...]
    roles: tuple[RoleCapabilities, ...]

    def to_record(self) -> dict[str, Any]:
        """Return the fingerprint input in declared canonical order."""

        return {
            "execution": {"mode": self.mode},
            "frozen_artefacts": [item.to_record() for item in self.frozen_artefacts],
            "roles": {item.role: {"read_roots": list(item.read_roots), "write_roots": list(item.write_roots)} for item in self.roles},
            "schema_version": self.schema_version,
        }

    @property
    def fingerprint(self) -> str:
        """Return the immutable canonical configuration fingerprint."""

        return fingerprint(self.to_record())

    def snapshot(self) -> dict[str, Any]:
        """Return the canonical record plus its self-verifiable fingerprint."""

        record = self.to_record()
        return {**record, "config_fingerprint": self.fingerprint}

    def capabilities_for(self, role: str) -> RoleCapabilities:
        """Return one role's capabilities or fail closed for an unknown role."""

        for capabilities in self.roles:
            if capabilities.role == role:
                return capabilities
        raise ConfigurationError("unknown execution role", details={"role": role})


def config_from_mapping(data: Mapping[str, Any]) -> ExecutionConfig:
    """Validate an in-memory mapping against the frozen Phase 2 contract."""

    _keys(data, {"schema_version", "execution", "frozen_artefacts", "roles"}, "$")
    if data["schema_version"] != CONFIG_SCHEMA_VERSION:
        raise ConfigurationError("unsupported configuration schema version")

    execution = data["execution"]
    if not isinstance(execution, Mapping):
        raise ConfigurationError("execution must be a table")
    _keys(execution, {"mode"}, "$.execution")
    if execution["mode"] != PHASE_2_MODE:
        raise ConfigurationError("Phase 2 permits dry-run mode only")

    raw_artefacts = data["frozen_artefacts"]
    if not isinstance(raw_artefacts, list) or not raw_artefacts:
        raise ConfigurationError("frozen_artefacts must be a non-empty array")
    artefacts: list[FrozenArtefact] = []
    for index, item in enumerate(raw_artefacts):
        if not isinstance(item, Mapping):
            raise ConfigurationError("frozen artefact must be a table", details={"index": index})
        _keys(item, {"path", "sha256"}, f"$.frozen_artefacts[{index}]")
        digest = item["sha256"]
        if not isinstance(digest, str) or not _SHA256.fullmatch(digest):
            raise ConfigurationError("invalid SHA-256 digest", details={"index": index})
        artefacts.append(FrozenArtefact(_relative_path(item["path"], f"$.frozen_artefacts[{index}].path"), digest))
    if len({item.path for item in artefacts}) != len(artefacts):
        raise ConfigurationError("duplicate frozen artefact path")

    raw_roles = data["roles"]
    if not isinstance(raw_roles, Mapping):
        raise ConfigurationError("roles must be a table")
    _keys(raw_roles, set(ROLE_NAMES), "$.roles")
    roles: list[RoleCapabilities] = []
    for role in ROLE_NAMES:
        item = raw_roles[role]
        if not isinstance(item, Mapping):
            raise ConfigurationError("role capabilities must be a table", details={"role": role})
        _keys(item, {"read_roots", "write_roots"}, f"$.roles.{role}")
        roots: dict[str, tuple[str, ...]] = {}
        for access in ("read_roots", "write_roots"):
            values = item[access]
            if not isinstance(values, list) or not all(isinstance(value, str) for value in values):
                raise ConfigurationError("capability roots must be a string array", details={"role": role, "access": access})
            roots[access] = tuple(_relative_path(value, f"$.roles.{role}.{access}") for value in values)
        roles.append(RoleCapabilities(role, roots["read_roots"], roots["write_roots"]))

    return ExecutionConfig(
        schema_version=CONFIG_SCHEMA_VERSION,
        mode=PHASE_2_MODE,
        frozen_artefacts=tuple(sorted(artefacts, key=lambda item: item.path)),
        roles=tuple(roles),
    )


def load_config(path: str | Path) -> ExecutionConfig:
    """Load UTF-8 TOML from ``path`` and return a validated frozen config."""

    config_path = Path(path)
    try:
        with config_path.open("rb") as stream:
            data = tomllib.load(stream)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise ConfigurationError("configuration could not be loaded", details={"path": str(config_path)}) from exc
    return config_from_mapping(data)
