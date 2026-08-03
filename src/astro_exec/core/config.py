"""Strict TOML configuration loading, validation, freezing, and fingerprinting."""

from __future__ import annotations

import tomllib
from collections.abc import Mapping
from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path, PurePosixPath
from typing import Any

from jsonschema import Draft202012Validator

from .errors import ConfigurationError
from .hashing import fingerprint

CONFIG_SCHEMA_VERSION = "astro-exec-config-v1"
PHASE_2_MODE = "dry-run"
ROLE_NAMES = ("asalab", "custodian", "statistician", "truthlab")
DEFAULT_POLICY = "no-implicit-defaults"


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
    default_policy: str
    mode: str
    frozen_manifest: str
    roles: tuple[RoleCapabilities, ...]

    def to_record(self) -> dict[str, Any]:
        """Return the fingerprint input in declared canonical order."""

        return {
            "defaults": {"applied": [], "policy": self.default_policy},
            "execution": {"frozen_manifest": self.frozen_manifest, "mode": self.mode},
            "roles": {item.role: {"read_roots": list(item.read_roots), "write_roots": list(item.write_roots)} for item in self.roles},
            "schema_version": self.schema_version,
        }

    @property
    def fingerprint(self) -> str:
        """Return the immutable canonical configuration fingerprint."""

        return fingerprint(self.to_record())

    @property
    def identity(self) -> "ConfigurationIdentity":
        """Return the typed identity of this complete validated configuration."""

        from .ids import ConfigurationIdentity

        return ConfigurationIdentity.derive(self.to_record())

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

    errors = sorted(
        Draft202012Validator(configuration_schema()).iter_errors(data),
        key=lambda error: tuple(str(part) for part in error.absolute_path),
    )
    if errors:
        error = errors[0]
        location = "$" + "".join(f"[{part}]" for part in error.absolute_path)
        raise ConfigurationError(
            "configuration does not match its versioned schema",
            details={"location": location, "validation": error.message},
        )

    _keys(data, {"schema_version", "defaults", "execution", "roles"}, "$")
    if data["schema_version"] != CONFIG_SCHEMA_VERSION:
        raise ConfigurationError("unsupported configuration schema version")

    defaults = data["defaults"]
    if not isinstance(defaults, Mapping):
        raise ConfigurationError("defaults must be a table")
    _keys(defaults, {"policy", "applied"}, "$.defaults")
    if defaults["policy"] != DEFAULT_POLICY or defaults["applied"] != []:
        raise ConfigurationError("Phase 2 does not permit implicit or applied defaults")

    execution = data["execution"]
    if not isinstance(execution, Mapping):
        raise ConfigurationError("execution must be a table")
    _keys(execution, {"mode", "frozen_manifest"}, "$.execution")
    if execution["mode"] != PHASE_2_MODE:
        raise ConfigurationError("Phase 2 permits dry-run mode only")
    frozen_manifest = _relative_path(execution["frozen_manifest"], "$.execution.frozen_manifest")

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
        default_policy=DEFAULT_POLICY,
        mode=PHASE_2_MODE,
        frozen_manifest=frozen_manifest,
        roles=tuple(roles),
    )


def configuration_schema() -> dict[str, Any]:
    """Load the packaged JSON Schema for the current configuration version."""

    import json

    resource = files("astro_exec").joinpath("contracts/astro-exec-config-v1.schema.json")
    try:
        schema = json.loads(resource.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
    except (OSError, ValueError, TypeError) as exc:
        raise ConfigurationError("packaged configuration schema is unavailable or invalid") from exc
    return schema


def load_config(path: str | Path) -> ExecutionConfig:
    """Load UTF-8 TOML from ``path`` and return a validated frozen config."""

    config_path = Path(path)
    try:
        with config_path.open("rb") as stream:
            data = tomllib.load(stream)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise ConfigurationError("configuration could not be loaded", details={"path": str(config_path)}) from exc
    return config_from_mapping(data)
