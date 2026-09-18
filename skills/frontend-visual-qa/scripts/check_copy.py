#!/usr/bin/env python3
"""Read-only U+2014 scan of selected files; performs no automatic replacement."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any

EXTENSIONS = {".md", ".txt", ".html", ".htm", ".css", ".scss", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".json", ".yaml", ".yml", ".py", ".ps1", ".xml", ".swift", ".kt", ".dart", ".csv"}
SKIP = {".git", "node_modules", "__pycache__", "dist", "build", ".next", ".venv", "venv"}


def is_link(p: Path) -> bool:
    data = p.lstat()
    return stat.S_ISLNK(data.st_mode) or bool(getattr(data, "st_file_attributes", 0) & 0x400)


def scan(paths: list[Path], include_en_dash: bool = False) -> dict[str, Any]:
    selected: set[Path] = set()
    errors: list[str] = []
    for entry in paths:
        try:
            if is_link(entry):
                errors.append(f"Link not followed: {entry}")
            elif entry.is_file():
                selected.add(entry.absolute())
            elif entry.is_dir():
                for current, dirs, files in os.walk(entry, followlinks=False):
                    base = Path(current)
                    valid_dirs = []
                    for name in sorted(dirs):
                        if name in SKIP:
                            continue
                        if is_link(base / name):
                            errors.append(f"Link not followed: {base / name}")
                        else:
                            valid_dirs.append(name)
                    dirs[:] = valid_dirs
                    for name in files:
                        p = base / name
                        if p.suffix.lower() not in EXTENSIONS:
                            continue
                        if is_link(p):
                            errors.append(f"Link not followed: {p}")
                        else:
                            selected.add(p.absolute())
            else:
                errors.append(f"Path is not a regular file or directory: {entry}")
        except OSError as exc:
            errors.append(f"{entry}: {exc}")
    findings = []
    checked = 0
    forbidden = {chr(0x2014)}
    if include_en_dash:
        forbidden.add(chr(0x2013))
    for path in sorted(selected):
        try:
            text = path.read_text(encoding="utf-8-sig")
            checked += 1
            for number, line in enumerate(text.splitlines(), 1):
                for column, char in enumerate(line, 1):
                    if char in forbidden:
                        findings.append({"path": str(path), "line": number, "column": column, "codepoint": f"U+{ord(char):04X}"})
        except (OSError, UnicodeError) as exc:
            errors.append(f"File not checked {path}: {exc}")
    if not checked:
        errors.append("No text files were checked.")
    return {"files_checked": checked, "findings": findings, "errors": errors,
            "limitation": "Conservative file scan, not DOM analysis. Quotations, data, and ranges may require documented exceptions."}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--include-en-dash", action="store_true", help="Also report U+2013, including legitimate ranges that may require review.")
    args = parser.parse_args()
    result = scan(args.paths, args.include_en_dash)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if result["errors"] else (1 if result["findings"] else 0)

if __name__ == "__main__":
    raise SystemExit(main())
