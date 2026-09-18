#!/usr/bin/env python3
"""Local package and path primitives; no network or external dependencies."""
from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from pathlib import Path, PurePosixPath
from typing import Any

SKILLS = (
    "interface-forge", "product-ui-design", "visual-brand-system",
    "frontend-visual-qa", "creative-assets",
)
PACKAGE_ID = "interface-forge"
IGNORE_DIRS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "dist"}


class ForgeError(Exception):
    """Verifiable error: the operation must stop without forcing changes."""


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def absolute(path: str | Path) -> Path:
    return Path(os.path.abspath(os.path.expanduser(str(path))))


def no_links(path: Path) -> None:
    """Reject symlinks, junctions, and reparse points in existing ancestors too."""
    p = absolute(path)
    for part in (*reversed(p.parents), p):
        try:
            data = part.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(data.st_mode) or getattr(data, "st_file_attributes", 0) & 0x400:
            raise ForgeError(f"Unsupported path containing a link/reparse point: {part}")


def relative_name(value: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value or ":" in value:
        raise ForgeError("Invalid relative filename in manifest.")
    p = PurePosixPath(value)
    if p.is_absolute() or str(p) != value or any(x in {"", ".", ".."} for x in p.parts):
        raise ForgeError(f"Unsafe relative path: {value!r}")
    reserved = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}
    for x in p.parts:
        if x.endswith((" ", ".")) or x.split(".")[0].upper() in reserved or any(ord(c) < 32 or c in '<>"|?*' for c in x):
            raise ForgeError(f"Filename is not portable to Windows: {value!r}")
    return value


def inventory(root: Path) -> dict[str, Any]:
    no_links(root)
    if not root.is_dir():
        raise ForgeError(f"Missing directory: {root}")
    files: dict[str, str] = {}
    directories: list[str] = []
    for current, dirs, names in os.walk(root, followlinks=False):
        base = Path(current)
        for name in sorted(dirs):
            p = base / name
            no_links(p)
            directories.append(relative_name(p.relative_to(root).as_posix()))
        for name in sorted(names):
            p = base / name
            no_links(p)
            if not p.is_file():
                raise ForgeError(f"Special file not allowed: {p}")
            files[relative_name(p.relative_to(root).as_posix())] = digest(p)
    return {"files": dict(sorted(files.items())), "directories": sorted(directories)}


def validate_inventory(data: Any) -> None:
    if not isinstance(data, dict) or set(data) != {"files", "directories"}:
        raise ForgeError("Invalid inventory.")
    if not isinstance(data["files"], dict) or not isinstance(data["directories"], list):
        raise ForgeError("Invalid inventory types.")
    for name, value in data["files"].items():
        relative_name(name)
        if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
            raise ForgeError("Invalid SHA-256 in inventory.")
    for name in data["directories"]:
        relative_name(name)
    if len(set(data["directories"])) != len(data["directories"]):
        raise ForgeError("Duplicate directories in inventory.")


def read_json(path: Path) -> Any:
    no_links(path)
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ForgeError(f"Unreadable JSON: {path}: {exc}") from exc


def suite(root: Path) -> dict[str, Any]:
    data = read_json(root / "suite.json")
    if not isinstance(data, dict) or data.get("schema_version") != 1 or data.get("package_id") != PACKAGE_ID:
        raise ForgeError("Invalid package identity.")
    if data.get("skills") != list(SKILLS):
        raise ForgeError("The package must contain exactly the five expected skills.")
    if not isinstance(data.get("version"), str) or not re.fullmatch(r"\d+\.\d+\.\d+", data["version"]):
        raise ForgeError("Invalid package version.")
    if (root / "VERSION").read_text(encoding="utf-8").strip() != data["version"]:
        raise ForgeError("VERSION and suite.json do not match.")
    return data


def package_files(root: Path) -> dict[str, str]:
    no_links(root)
    files: dict[str, str] = {}
    for current, dirs, names in os.walk(root, followlinks=False):
        base = Path(current)
        dirs[:] = sorted(d for d in dirs if d not in IGNORE_DIRS and not (base == root / "qa" and d == "local"))
        for name in dirs:
            no_links(base / name)
        for name in sorted(names):
            p = base / name
            rel = p.relative_to(root).as_posix()
            if rel == "release-manifest.json" or name.endswith((".pyc", ".pyo")):
                continue
            no_links(p)
            if not p.is_file():
                raise ForgeError(f"Special file in package: {p}")
            files[relative_name(rel)] = digest(p)
    return dict(sorted(files.items()))


def write_manifest(root: Path) -> dict[str, Any]:
    metadata = suite(root)
    data = {"schema_version": 1, "package_id": PACKAGE_ID, "version": metadata["version"], "files": package_files(root)}
    (root / "release-manifest.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return data


def verify_manifest(root: Path) -> dict[str, Any]:
    metadata = suite(root)
    data = read_json(root / "release-manifest.json")
    if not isinstance(data, dict) or data.get("schema_version") != 1 or data.get("package_id") != PACKAGE_ID or data.get("version") != metadata["version"]:
        raise ForgeError("Release manifest does not match package metadata.")
    expected = data.get("files")
    if not isinstance(expected, dict):
        raise ForgeError("Invalid file list in release manifest.")
    for name, value in expected.items():
        relative_name(name)
        if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
            raise ForgeError("Invalid hash in release manifest.")
    actual = package_files(root)
    if actual != expected:
        changes = sorted(k for k in set(actual) | set(expected) if actual.get(k) != expected.get(k))
        raise ForgeError("Release integrity could not be confirmed: " + ", ".join(changes[:12]))
    return metadata
