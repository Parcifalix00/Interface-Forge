#!/usr/bin/env python3
"""Validate a declarative QA report; does not certify the underlying evidence."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
from typing import Any

METHODS = {"static", "browser-emulation", "desktop-browser", "platform-simulator", "physical-device", "manual-assistive-tech"}
STATUSES = {"PASS", "FAIL", "NOT_RUN", "NOT_APPLICABLE"}

class ReportError(ValueError):
    pass


def nonempty(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ReportError(f"{field}: non-empty text is required.")
    return value


def assess(data: Any, evidence_root: Path | None = None) -> dict[str, Any]:
    if not isinstance(data, dict) or type(data.get("schema_version")) is not int or data["schema_version"] != 1:
        raise ReportError("schema_version must be integer 1.")
    missing: list[str] = []
    for field in ("project", "revision", "scope"):
        value = nonempty(data.get(field), field)
        if "TO_FILL" in value:
            missing.append(f"Context still needs to be completed: {field}")
    requirements, results = data.get("requirements"), data.get("results")
    if not isinstance(requirements, list) or not requirements or not isinstance(results, list):
        raise ReportError("requirements must be a non-empty list and results must be a list.")
    index: dict[str, dict[str, Any]] = {}
    for req in requirements:
        if not isinstance(req, dict):
            raise ReportError("Invalid requirement.")
        ident = nonempty(req.get("id"), "requirement.id")
        if ident in index:
            raise ReportError(f"Duplicate requirement: {ident}")
        nonempty(req.get("platform"), "requirement.platform")
        nonempty(req.get("description"), "requirement.description")
        allowed = req.get("allowed_methods")
        if not isinstance(allowed, list) or not allowed or any(not isinstance(x, str) or x not in METHODS for x in allowed):
            raise ReportError(f"Invalid allowed methods for {ident}.")
        if len(set(allowed)) != len(allowed):
            raise ReportError(f"Duplicate methods for {ident}.")
        index[ident] = req
    seen: set[str] = set()
    failed: list[str] = []
    counts = {s: 0 for s in sorted(STATUSES)}
    for item in results:
        if not isinstance(item, dict):
            raise ReportError("Invalid result.")
        ident = nonempty(item.get("requirement_id"), "result.requirement_id")
        if ident not in index or ident in seen:
            raise ReportError(f"Unknown or duplicate result: {ident}")
        seen.add(ident)
        req = index[ident]
        if item.get("platform") != req["platform"]:
            raise ReportError(f"Result platform differs from requirement: {ident}")
        status = item.get("status")
        if not isinstance(status, str) or status not in STATUSES:
            raise ReportError(f"Invalid status: {ident}")
        method = item.get("method")
        if method is not None and (not isinstance(method, str) or method not in METHODS):
            raise ReportError(f"Invalid method: {ident}")
        evidence = item.get("evidence", [])
        if not isinstance(evidence, list) or any(not isinstance(x, str) or not x.strip() for x in evidence):
            raise ReportError(f"Invalid evidence list: {ident}")
        if status in {"PASS", "FAIL"}:
            if method not in req["allowed_methods"]:
                raise ReportError(f"{ident}: the method does not satisfy the requirement; emulation and device evidence are not equivalent.")
            nonempty(item.get("environment"), f"{ident}.environment")
            if not evidence:
                raise ReportError(f"{ident}: evidence is required for {status}.")
            if evidence_root is not None:
                base = evidence_root.resolve()
                for name in evidence:
                    candidate = Path(name)
                    resolved = (base / candidate).resolve()
                    if candidate.is_absolute() or not resolved.is_relative_to(base) or not resolved.is_file():
                        raise ReportError(f"{ident}: local evidence is missing or outside the evidence root: {name}")
        else:
            nonempty(item.get("reason"), f"{ident}.reason")
        counts[status] += 1
        if status == "FAIL":
            failed.append(ident)
        elif status == "NOT_RUN":
            missing.append(ident)
    missing.extend(sorted(set(index) - seen))
    state = "BLOCKED" if failed else ("INCOMPLETE" if missing else "READY_FOR_REVIEW")
    return {"state": state, "counts": counts, "failed": failed, "missing": missing,
            "evidence_files_checked": evidence_root is not None,
            "limitation": "Structural and consistency validation only. It does not prove evidence truthfulness, observation, scope sufficiency, or complete compliance."}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("--evidence-root", type=Path, help="Also verify existence and confinement of local evidence files.")
    args = parser.parse_args()
    try:
        data = json.loads(args.report.read_text(encoding="utf-8"))
        result = assess(data, args.evidence_root)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["state"] == "READY_FOR_REVIEW" else 1
    except (OSError, ValueError) as exc:
        print(f"INVALID REPORT: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
