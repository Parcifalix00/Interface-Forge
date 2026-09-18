#!/usr/bin/env python3
"""Static validation of the Interface Forge package format, not model behavior."""
from __future__ import annotations
import argparse
import ast
import json
from pathlib import Path
import re
import sys
from typing import Any
from urllib.parse import unquote
from package_lib import SKILLS, ForgeError, package_files, suite, verify_manifest


def validate(root: Path, integrity: bool = False) -> dict[str, Any]:
    info = suite(root)
    files = package_files(root)
    errors: list[str] = []
    required = ["LICENSE", "THIRD_PARTY_NOTICES.md", "licenses/Higgsfield-MIT.txt", "README.md", "START_HERE.md",
                "docs/VALIDATION.md", "docs/EVALUATION_PLAN.md", "evals/routing-cases.json", "contracts/core-contract.md", "contracts/platform-baseline.md"]
    for name in required:
        if name not in files:
            errors.append(f"Required file missing: {name}")
    names = sorted(p.name for p in (root / "skills").iterdir() if p.is_dir())
    if names != sorted(SKILLS):
        errors.append("Skill directories do not match the expected registry.")
    if len({x.casefold() for x in files}) != len(files):
        errors.append("Collision between names that differ only by letter case.")
    for rel in files:
        p = root / rel
        if p.suffix.lower() in {".ttf", ".otf", ".woff", ".woff2", ".pem", ".key", ".pfx"} or p.name.startswith(".env"):
            errors.append(f"File type not allowed in this distribution: {rel}")
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeError:
            errors.append(f"Unexpected non-UTF-8 file in text package: {rel}")
            continue
        if chr(0x2014) in text or chr(0x2013) in text:
            errors.append(f"Forbidden typographic separator in authored package: {rel}")
        if p.suffix == ".py":
            try:
                ast.parse(text, filename=rel)
            except SyntaxError as exc:
                errors.append(f"Invalid Python: {rel}: {exc}")
        if p.suffix == ".json":
            try:
                json.loads(text)
            except ValueError as exc:
                errors.append(f"Invalid JSON: {rel}: {exc}")
        if p.suffix == ".md":
            for href in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
                if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", href) or href.startswith("#"):
                    continue
                target = unquote(href.split("#", 1)[0])
                if not target:
                    continue
                resolved = (p.parent / target).resolve()
                if not resolved.is_relative_to(root.resolve()) or not resolved.exists():
                    errors.append(f"Unresolved local link: {rel} -> {href}")
    for name in SKILLS:
        p = root / "skills" / name
        try:
            text = (p / "SKILL.md").read_text(encoding="utf-8")
            match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
            if not match:
                raise ValueError("Missing frontmatter")
            front = match.group(1)
            found_name = re.search(r"^name: ([a-z0-9]+(?:-[a-z0-9]+)*)$", front, re.M)
            desc = re.search(r"^description: (.+)$", front, re.M)
            if not found_name or found_name.group(1) != name or len(name) > 64:
                raise ValueError("name does not match directory/format")
            if not desc:
                raise ValueError("Missing description")
            description = json.loads(desc.group(1))
            if not isinstance(description, str) or not 1 <= len(description) <= 1024:
                raise ValueError("Invalid description")
            if f'  version: "{info["version"]}"' not in front or "license: MIT" not in front:
                raise ValueError("Version or license mismatch")
            if len(text.splitlines()) > 500:
                raise ValueError("SKILL.md exceeds 500 lines")
            metadata = (p / "agents" / "openai.yaml").read_text(encoding="utf-8")
            for key in ("interface:", "  display_name:", "  short_description:", "  default_prompt:", "policy:", "  allow_implicit_invocation: true"):
                if key not in metadata:
                    raise ValueError(f"Missing metadata: {key}")
            if "$" + name not in metadata:
                raise ValueError("default_prompt does not explicitly reference the skill name")
            for line in metadata.splitlines():
                if ': "' in line:
                    json.loads(line.split(": ", 1)[1])
            if (p / "references" / "core-contract.md").read_bytes() != (root / "contracts" / "core-contract.md").read_bytes():
                raise ValueError("Shared contract differs from canonical copy")
            if name in {"interface-forge", "product-ui-design", "frontend-visual-qa"}:
                if (p / "references" / "platform-baseline.md").read_bytes() != (root / "contracts" / "platform-baseline.md").read_bytes():
                    raise ValueError("Platform baseline differs from canonical copy")
            if (p / "LICENSE").read_bytes() != (root / "LICENSE").read_bytes():
                raise ValueError("Original license differs from canonical copy")
            if (p / "licenses" / "Higgsfield-MIT.txt").read_bytes() != (root / "licenses" / "Higgsfield-MIT.txt").read_bytes():
                raise ValueError("Upstream license differs from canonical copy")
        except (OSError, ValueError) as exc:
            errors.append(f"{name}: {exc}")
    try:
        cases = json.loads((root / "evals" / "routing-cases.json").read_text(encoding="utf-8"))["cases"]
        ids = [c["id"] for c in cases]
        if len(ids) != len(set(ids)) or len(cases) < 15:
            errors.append("Evaluation cases are duplicated or insufficient.")
        for case in cases:
            if not case["prompt"] or not case["required_behaviours"] or not case["forbidden_behaviours"]:
                errors.append(f"Incomplete evaluation case: {case['id']}")
            if any(s not in SKILLS for s in case["acceptable_entry_skills"]):
                errors.append(f"Unknown skill in evaluation case: {case['id']}")
    except (OSError, KeyError, ValueError, TypeError) as exc:
        errors.append(f"Invalid evaluation registry: {exc}")
    if integrity:
        try:
            verify_manifest(root)
        except ForgeError as exc:
            errors.append(str(exc))
    return {"status": "PASS" if not errors else "FAIL", "version": info["version"], "files_checked": len(files),
            "skills_checked": len(SKILLS), "integrity_checked": integrity, "errors": errors,
            "limitation": "Static checks for package-specific format, links, and contracts. Not a general YAML parser and not evidence of triggering or UI quality."}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--verify-integrity", action="store_true")
    args = parser.parse_args()
    try:
        result = validate(args.root, args.verify_integrity)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["status"] == "PASS" else 1
    except (ForgeError, OSError, ValueError) as exc:
        print(f"INVALID PACKAGE: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
