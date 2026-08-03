"""Manifest-driven, fail-closed verification for frozen artefacts."""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from .config import ExecutionConfig
from .errors import DigestValidationError, FrozenArtefactDrift
from .hashing import GitBlobDigest, SHA256Digest, git_blob_digest, sha256_file

FROZEN_MANIFEST_SCHEMA = "astro-exec-frozen-manifest-v1"
_DOCUMENT_STATUSES = {"frozen", "mixed"}
_SECTION_STATUSES = {"frozen", "candidate-not-frozen"}


def _drift(message: str, drift_type: str, **details: Any) -> FrozenArtefactDrift:
    return FrozenArtefactDrift(message, details={"drift_type": drift_type, **details})


def _relative_path(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise _drift("frozen manifest path is invalid", "manifest-invalid", field=field)
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or "\\" in value or "$" in value:
        raise _drift("frozen manifest path escapes repository scope", "manifest-invalid", field=field, path=value)
    return path.as_posix()


def _exact_keys(value: Mapping[str, Any], expected: set[str], location: str) -> None:
    if set(value) != expected:
        raise _drift(
            "frozen manifest fields differ from contract",
            "manifest-invalid",
            actual=sorted(value),
            expected=sorted(expected),
            location=location,
        )


def _contains_symlink(root: Path, relative: str) -> bool:
    """Return whether any repository-relative path component is a symlink."""

    current = root
    for part in PurePosixPath(relative).parts:
        current = current / part
        if current.is_symlink():
            return True
    return False


@dataclass(frozen=True, slots=True)
class ArtefactSection:
    """Declared freeze status of one semantically bounded document section."""

    name: str
    status: str

    def to_record(self) -> dict[str, str]:
        """Return the section status without broadening its freeze boundary."""

        return {"name": self.name, "status": self.status}


@dataclass(frozen=True, slots=True)
class FrozenManifestEntry:
    """One integrity-pinned path and its accurately scoped status metadata."""

    path: str
    sha256: SHA256Digest
    git_blob: GitBlobDigest
    document_status: str
    sections: tuple[ArtefactSection, ...]

    def to_record(self) -> dict[str, Any]:
        """Return the canonical declared manifest entry."""

        return {
            "document_status": self.document_status,
            "git_blob": self.git_blob.to_record(),
            "path": self.path,
            "sections": [section.to_record() for section in self.sections],
            "sha256": self.sha256.to_record(),
        }


@dataclass(frozen=True, slots=True)
class FrozenManifest:
    """Immutable declared artefact set and directories closed to extra files."""

    schema_version: str
    closed_directories: tuple[str, ...]
    artefacts: tuple[FrozenManifestEntry, ...]

    def to_record(self) -> dict[str, Any]:
        """Return the complete normalized manifest record."""

        return {
            "artefacts": [item.to_record() for item in self.artefacts],
            "closed_directories": list(self.closed_directories),
            "schema_version": self.schema_version,
        }


@dataclass(frozen=True, slots=True)
class VerifiedArtefact:
    """An artefact whose current bytes and Git framing match the manifest."""

    path: str
    sha256: SHA256Digest
    git_blob: GitBlobDigest
    document_status: str
    sections: tuple[ArtefactSection, ...]

    def to_record(self) -> dict[str, Any]:
        """Return verification status separately from semantic freeze status."""

        return {
            "document_status": self.document_status,
            "git_blob": self.git_blob.to_record(),
            "path": self.path,
            "sections": [section.to_record() for section in self.sections],
            "sha256": self.sha256.to_record(),
            "verification_status": "verified",
        }


def manifest_from_mapping(data: Mapping[str, Any]) -> FrozenManifest:
    """Validate a decoded manifest and preserve its exact freeze boundaries."""

    _exact_keys(data, {"schema_version", "closed_directories", "artefacts"}, "$")
    if data["schema_version"] != FROZEN_MANIFEST_SCHEMA:
        raise _drift("unsupported frozen manifest schema", "manifest-invalid")
    raw_directories = data["closed_directories"]
    if not isinstance(raw_directories, list):
        raise _drift("closed_directories must be an array", "manifest-invalid")
    directories = tuple(sorted(_relative_path(item, "closed_directories") for item in raw_directories))
    if len(set(directories)) != len(directories):
        raise _drift("closed directory is declared more than once", "manifest-invalid")

    raw_artefacts = data["artefacts"]
    if not isinstance(raw_artefacts, list) or not raw_artefacts:
        raise _drift("frozen manifest artefacts must be a non-empty array", "manifest-invalid")
    artefacts: list[FrozenManifestEntry] = []
    for index, raw in enumerate(raw_artefacts):
        if not isinstance(raw, Mapping):
            raise _drift("frozen manifest artefact must be an object", "manifest-invalid", index=index)
        _exact_keys(raw, {"path", "sha256", "git_blob_sha1", "document_status", "sections"}, f"$.artefacts[{index}]")
        status = raw["document_status"]
        if status not in _DOCUMENT_STATUSES:
            raise _drift("invalid document freeze status", "manifest-invalid", index=index, status=status)
        raw_sections = raw["sections"]
        if not isinstance(raw_sections, list):
            raise _drift("artefact sections must be an array", "manifest-invalid", index=index)
        sections: list[ArtefactSection] = []
        for section_index, raw_section in enumerate(raw_sections):
            if not isinstance(raw_section, Mapping):
                raise _drift("artefact section must be an object", "manifest-invalid", index=index)
            _exact_keys(raw_section, {"name", "status"}, f"$.artefacts[{index}].sections[{section_index}]")
            if not isinstance(raw_section["name"], str) or not raw_section["name"] or raw_section["status"] not in _SECTION_STATUSES:
                raise _drift("invalid artefact section status", "manifest-invalid", index=index, section=section_index)
            sections.append(ArtefactSection(raw_section["name"], raw_section["status"]))
        if status == "mixed" and {item.status for item in sections} != {"frozen", "candidate-not-frozen"}:
            raise _drift("mixed document must declare frozen and candidate sections", "manifest-invalid", index=index)
        if status == "frozen" and sections:
            raise _drift("uniformly frozen document cannot carry mixed section statuses", "manifest-invalid", index=index)
        artefacts.append(
            FrozenManifestEntry(
                _relative_path(raw["path"], f"artefacts[{index}].path"),
                SHA256Digest(raw["sha256"]),
                GitBlobDigest(raw["git_blob_sha1"]),
                status,
                tuple(sections),
            )
        )
    ordered = tuple(sorted(artefacts, key=lambda item: item.path))
    if len({item.path for item in ordered}) != len(ordered):
        raise _drift("frozen artefact path is declared more than once", "manifest-invalid")
    return FrozenManifest(FROZEN_MANIFEST_SCHEMA, directories, ordered)


def load_frozen_manifest(path: str | Path) -> FrozenManifest:
    """Load a UTF-8 JSON frozen-artefact manifest without fallback discovery."""

    manifest_path = Path(path)
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise _drift("frozen manifest is unavailable or malformed", "manifest-invalid", path=str(manifest_path)) from exc
    if not isinstance(data, Mapping):
        raise _drift("frozen manifest root must be an object", "manifest-invalid")
    try:
        return manifest_from_mapping(data)
    except (DigestValidationError, TypeError, ValueError) as exc:
        raise _drift("frozen manifest contains an invalid typed digest", "manifest-invalid") from exc


def verify_frozen_artefacts(config: ExecutionConfig, repository_root: str | Path) -> tuple[VerifiedArtefact, ...]:
    """Verify the declared set and abort on missing, changed, substituted, or extra files."""

    root = Path(repository_root).resolve()
    unresolved_manifest = root / config.frozen_manifest
    if _contains_symlink(root, config.frozen_manifest):
        raise _drift("frozen manifest was substituted by a symlink", "substituted", path=config.frozen_manifest)
    manifest_path = unresolved_manifest.resolve()
    try:
        manifest_path.relative_to(root)
    except ValueError as exc:
        raise _drift("frozen manifest escapes repository root", "path-escape", path=config.frozen_manifest) from exc
    manifest = load_frozen_manifest(manifest_path)
    declared_paths = {item.path for item in manifest.artefacts}

    for directory in manifest.closed_directories:
        if _contains_symlink(root, directory):
            raise _drift("closed authoritative directory was substituted by a symlink", "substituted", path=directory)
        closed = (root / directory).resolve()
        try:
            closed.relative_to(root)
            actual = {
                item.relative_to(root).as_posix()
                for item in closed.iterdir()
                if item.is_file() or item.is_symlink()
            }
        except (OSError, ValueError) as exc:
            raise _drift("closed authoritative directory is unavailable", "missing", path=directory) from exc
        extras = sorted(actual - declared_paths)
        if extras:
            raise _drift("extra authoritative artefact detected", "extra", paths=extras)

    verified: list[VerifiedArtefact] = []
    for artefact in manifest.artefacts:
        unresolved = root / artefact.path
        if _contains_symlink(root, artefact.path):
            raise _drift("frozen artefact was substituted by a symlink", "substituted", path=artefact.path)
        candidate = unresolved.resolve()
        try:
            candidate.relative_to(root)
        except ValueError as exc:
            raise _drift("frozen artefact escapes repository root", "path-escape", path=artefact.path) from exc
        if not candidate.is_file():
            raise _drift("frozen artefact is missing", "missing", path=artefact.path)
        try:
            content = candidate.read_bytes()
        except OSError as exc:
            raise _drift("frozen artefact is unavailable", "missing", path=artefact.path) from exc
        actual_sha256 = SHA256Digest(sha256_file(candidate))
        actual_git_blob = git_blob_digest(content)
        if actual_sha256 != artefact.sha256 or actual_git_blob != artefact.git_blob:
            raise _drift(
                "frozen artefact digest mismatch",
                "changed",
                path=artefact.path,
                actual_sha256=actual_sha256.to_record(),
                expected_sha256=artefact.sha256.to_record(),
                actual_git_blob=actual_git_blob.to_record(),
                expected_git_blob=artefact.git_blob.to_record(),
            )
        verified.append(
            VerifiedArtefact(
                artefact.path,
                actual_sha256,
                actual_git_blob,
                artefact.document_status,
                artefact.sections,
            )
        )
    return tuple(verified)
