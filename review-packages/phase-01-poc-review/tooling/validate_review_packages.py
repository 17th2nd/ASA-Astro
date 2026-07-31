#!/usr/bin/env python3
"""Validate corpus identity, manifests, archive extraction safety, and secrets."""

from __future__ import annotations

import hashlib
import json
import re
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

import build_review_packages as build


SECRET_PATTERNS = {
    "private key": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    "AWS access key": re.compile(rb"\bAKIA[0-9A-Z]{16}\b"),
    "GitHub token": re.compile(rb"\bgh(?:p|o|u|s|r)_[A-Za-z0-9]{30,}\b"),
    "OpenAI-style token": re.compile(rb"\bsk-[A-Za-z0-9_-]{24,}\b"),
    "credential-bearing URL": re.compile(rb"[a-zA-Z][a-zA-Z0-9+.-]*://[^\s/@:]+:[^\s/@]+@"),
    "assigned password": re.compile(rb"(?i)\bpassword\s*[:=]\s*['\"][^'\"\r\n]{4,}['\"]"),
}

FORBIDDEN_NAMES = {
    ".env",
    "credentials.json",
    "id_rsa",
    "id_ed25519",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def scan_secret(path: PurePosixPath, data: bytes) -> None:
    lower_name = path.name.lower()
    if lower_name in FORBIDDEN_NAMES or lower_name.endswith((".pem", ".p12", ".pfx")):
        raise AssertionError(f"forbidden credential-like filename: {path}")
    for label, pattern in SECRET_PATTERNS.items():
        if pattern.search(data):
            raise AssertionError(f"possible {label} in {path}")


def validate_source_corpus(config: dict, entries: list[build.SourceEntry]) -> None:
    expected_paths = {entry.corpus_path for entry in entries}
    actual_paths = {
        path.relative_to(build.BUNDLE_ROOT).as_posix()
        for path in build.CORPUS_ROOT.rglob("*")
        if path.is_file()
    }
    if actual_paths != expected_paths:
        raise AssertionError(
            f"corpus path mismatch; missing={sorted(expected_paths - actual_paths)} extra={sorted(actual_paths - expected_paths)}"
        )
    source_paths = set()
    for entry in entries:
        if entry.source_path in source_paths:
            raise AssertionError(f"source included more than once: {entry.source_path}")
        source_paths.add(entry.source_path)
        packaged = (build.BUNDLE_ROOT / entry.corpus_path).read_bytes()
        source = build.git_bytes("show", f"{config['source_commit']}:{entry.source_path}")
        if packaged != source:
            raise AssertionError(f"source bytes transformed: {entry.source_path}")
        if len(packaged) != entry.size_bytes or sha256(packaged) != entry.sha256:
            raise AssertionError(f"source metadata mismatch: {entry.source_path}")
        scan_secret(PurePosixPath(entry.corpus_path), packaged)


def validate_manifest_file(path: Path, expected_source_commit: str) -> dict:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if manifest["source_commit"] != expected_source_commit:
        raise AssertionError(f"wrong source commit in {path}")
    seen = set()
    for entry in manifest["entries"]:
        relative = entry["path"]
        if relative in seen:
            raise AssertionError(f"duplicate manifest path: {relative}")
        seen.add(relative)
        pure = PurePosixPath(relative)
        if pure.is_absolute() or ".." in pure.parts or ".git" in pure.parts:
            raise AssertionError(f"unsafe manifest path: {relative}")
        target = path.parent / relative
        if not target.is_file():
            raise AssertionError(f"manifest path unavailable: {relative}")
        data = target.read_bytes()
        if len(data) != entry["size_bytes"] or sha256(data) != entry["sha256"]:
            raise AssertionError(f"manifest digest mismatch: {relative}")
    if len(seen) != manifest["payload_file_count"]:
        raise AssertionError(f"manifest count mismatch: {path}")
    return manifest


def expected_master_payload() -> set[str]:
    paths = set()
    for path in build.BUNDLE_ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(build.BUNDLE_ROOT).as_posix()
        if relative == "MANIFEST.json" or relative.startswith("archives/") or "__pycache__" in path.parts:
            continue
        paths.add(relative)
    return paths


def parse_checksum_file(path: Path) -> dict[str, str]:
    values = {}
    for line in path.read_text(encoding="ascii").splitlines():
        digest, name = line.split("  ", 1)
        values[name] = digest
    return values


def validate_archive(config: dict, reviewer: str, expected_digest: str) -> None:
    archive_path = build.ARCHIVE_ROOT / config["archives"][reviewer]
    data = archive_path.read_bytes()
    if sha256(data) != expected_digest:
        raise AssertionError(f"archive checksum mismatch: {archive_path.name}")
    expected_root = f"ASA-Astro-POC-Review-Package-{reviewer.capitalize()}"
    expected_prompt = {
        "gemini": "gemini/GEMINI-INDEPENDENT-REVIEW-PROMPT.md",
        "claude": "claude/CLAUDE-INDEPENDENT-REVIEW-PROMPT.md",
    }[reviewer]
    other_prompt_dir = "claude" if reviewer == "gemini" else "gemini"
    with zipfile.ZipFile(archive_path, "r") as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise AssertionError(f"duplicate ZIP member in {archive_path.name}")
        for info in archive.infolist():
            pure = PurePosixPath(info.filename)
            if pure.is_absolute() or ".." in pure.parts or ".git" in pure.parts:
                raise AssertionError(f"unsafe ZIP member: {info.filename}")
            if not pure.parts or pure.parts[0] != expected_root:
                raise AssertionError(f"unexpected ZIP root: {info.filename}")
            file_type = (info.external_attr >> 16) & 0o170000
            if file_type == 0o120000:
                raise AssertionError(f"symlink ZIP member: {info.filename}")
        prompt_member = f"{expected_root}/{expected_prompt}"
        if prompt_member not in names:
            raise AssertionError(f"model prompt missing from {archive_path.name}")
        if any(name.startswith(f"{expected_root}/{other_prompt_dir}/") for name in names):
            raise AssertionError(f"other model prompt present in {archive_path.name}")
        required = {
            f"{expected_root}/README.md",
            f"{expected_root}/SOURCE-INDEX.md",
            f"{expected_root}/REVIEW-SCOPE.md",
            f"{expected_root}/REVIEWER-GUIDANCE.md",
            f"{expected_root}/LARGE-EVIDENCE.md",
            f"{expected_root}/MANIFEST.json",
        }
        if not required.issubset(names):
            raise AssertionError(f"required archive orientation missing: {sorted(required - set(names))}")
        with tempfile.TemporaryDirectory(prefix=f"asa-astro-{reviewer}-extract-") as temp_dir:
            extract_root = Path(temp_dir).resolve()
            for info in archive.infolist():
                relative = PurePosixPath(info.filename)
                target = extract_root.joinpath(*relative.parts).resolve()
                if extract_root not in target.parents:
                    raise AssertionError(f"archive member escapes extraction root: {info.filename}")
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(archive.read(info.filename))
            package_root = extract_root / expected_root
            manifest_path = package_root / "MANIFEST.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            if manifest["source_commit"] != config["source_commit"] or manifest["reviewer"] != reviewer:
                raise AssertionError(f"archive manifest identity mismatch: {archive_path.name}")
            manifest_paths = set()
            for entry in manifest["entries"]:
                relative = entry["path"]
                manifest_paths.add(relative)
                target = package_root / relative
                if not target.is_file():
                    raise AssertionError(f"archive manifest path missing: {relative}")
                payload = target.read_bytes()
                if len(payload) != entry["size_bytes"] or sha256(payload) != entry["sha256"]:
                    raise AssertionError(f"archive payload digest mismatch: {relative}")
                scan_secret(PurePosixPath(relative), payload)
            extracted_payload = {
                path.relative_to(package_root).as_posix()
                for path in package_root.rglob("*")
                if path.is_file() and path.name != "MANIFEST.json"
            }
            if extracted_payload != manifest_paths:
                raise AssertionError(
                    f"archive payload coverage mismatch: missing={sorted(manifest_paths - extracted_payload)} extra={sorted(extracted_payload - manifest_paths)}"
                )
            if manifest["source_file_count"] != 141:
                raise AssertionError("archive source count is not the frozen 141-file corpus")


def main() -> None:
    build.ensure_safe_bundle_root()
    config = build.load_config()
    entries = build.source_entries(config)
    if len(entries) != 141:
        raise AssertionError(f"unexpected source-file count: {len(entries)}")
    validate_source_corpus(config, entries)
    master = validate_manifest_file(build.BUNDLE_ROOT / "MANIFEST.json", config["source_commit"])
    manifest_paths = {entry["path"] for entry in master["entries"]}
    expected_paths = expected_master_payload()
    if manifest_paths != expected_paths:
        raise AssertionError(
            f"master manifest coverage mismatch; missing={sorted(expected_paths - manifest_paths)} extra={sorted(manifest_paths - expected_paths)}"
        )
    if master["source_file_count"] != len(entries):
        raise AssertionError("master manifest source count mismatch")
    checksums = parse_checksum_file(build.ARCHIVE_ROOT / "SHA256SUMS")
    if set(checksums) != set(config["archives"].values()):
        raise AssertionError("archive checksum-file coverage mismatch")
    for reviewer in ("gemini", "claude"):
        validate_archive(config, reviewer, checksums[config["archives"][reviewer]])
    print(f"PASS: {len(entries)} source paths and both complete reviewer archives validated")


if __name__ == "__main__":
    main()
