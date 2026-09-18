#!/usr/bin/env python3
"""Install verified copies of the suite. Mutating operations require --apply.

State and backups remain OUTSIDE the Codex skill directory.
No network access, elevation, AGENTS.md modification, or model configuration changes.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
from typing import Any, Iterator
import uuid

from package_lib import (SKILLS, PACKAGE_ID, ForgeError, absolute, inventory,
                         no_links, read_json, validate_inventory, verify_manifest)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def state_directory(target: Path) -> Path:
    key = hashlib.sha256(os.path.normcase(str(target)).encode("utf-8")).hexdigest()[:12]
    return target.parent / ".interface-forge" / key


def safe_target(value: str | Path) -> Path:
    target = absolute(value)
    if target == Path(target.anchor) or target == absolute(Path.home()):
        raise ForgeError("The target must be a skill directory, not a filesystem root or the home directory.")
    no_links(target)
    no_links(state_directory(target))
    if target.exists() and not target.is_dir():
        raise ForgeError("The target exists but is not a directory.")
    return target


def atomic_json(path: Path, data: Any) -> None:
    no_links(path)
    temp = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
    try:
        with temp.open("x", encoding="utf-8", newline="\n") as stream:
            json.dump(data, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, path)
    finally:
        if temp.exists():
            temp.unlink()


def validate_state(data: Any, target: Path) -> dict[str, Any] | None:
    if data is None:
        return None
    if not isinstance(data, dict) or data.get("schema_version") != 1 or data.get("package_id") != PACKAGE_ID:
        raise ForgeError("Invalid installation state.")
    if data.get("target") != str(target) or not isinstance(data.get("trees"), dict) or set(data["trees"]) != set(SKILLS):
        raise ForgeError("State refers to a different target or suite.")
    if not isinstance(data.get("version"), str) or not re.fullmatch(r"\d+\.\d+\.\d+", data["version"]):
        raise ForgeError("Invalid state version.")
    for tree in data["trees"].values():
        validate_inventory(tree)
    return data


def load_state(target: Path) -> dict[str, Any] | None:
    p = state_directory(target) / "installed.json"
    return validate_state(read_json(p), target) if p.exists() else None


def check_current(target: Path, old: dict[str, Any] | None) -> None:
    for name in SKILLS:
        p = target / name
        no_links(p)
        if old is None:
            if p.exists():
                raise ForgeError(f"Collision: {p} exists but is not owned by this installation.")
        elif not p.is_dir() or inventory(p) != old["trees"][name]:
            raise ForgeError(f"Local modifications or missing files in {name}. Refusing overwrite; reconcile first.")


def package_state(source: Path, target: Path) -> dict[str, Any]:
    if source == target or source in target.parents or target in source.parents:
        raise ForgeError("Source and target must not overlap.")
    info = verify_manifest(source)
    manifest = read_json(source / "release-manifest.json")
    trees = {s: inventory(source / "skills" / s) for s in SKILLS}
    # The release excludes caches and working files, but copytree would copy them.
    # Rejecting undeclared files prevents payloads outside the manifest.
    for name, tree in trees.items():
        prefix = f"skills/{name}/"
        expected = {p[len(prefix):]: value for p, value in manifest["files"].items()
                    if p.startswith(prefix)}
        if tree["files"] != expected:
            raise ForgeError(f"Undeclared files in the {name} payload, possibly including caches. Use a clean release extraction.")
    return {"schema_version": 1, "package_id": PACKAGE_ID, "target": str(target),
            "version": info["version"], "trees": trees}


@contextmanager
def lock(root: Path) -> Iterator[None]:
    no_links(root)
    root.mkdir(parents=True, exist_ok=True)
    path = root / "operation.lock"
    try:
        with path.open("x", encoding="utf-8") as stream:
            json.dump({"pid": os.getpid(), "created_utc": stamp()}, stream)
    except FileExistsError as exc:
        raise ForgeError(f"Lock exists: {path}. Verify that no operation is active; the lock is not removed automatically.") from exc
    try:
        yield
    finally:
        path.unlink(missing_ok=True)


def backup_path(root: Path, identifier: str) -> Path:
    if not re.fullmatch(r"[0-9a-f]{32}", identifier):
        raise ForgeError("Invalid backup ID.")
    p = root / "backups" / identifier
    no_links(p)
    return p


def read_backup(target: Path, identifier: str) -> tuple[dict[str, Any] | None, Path]:
    p = backup_path(state_directory(target), identifier)
    data = read_json(p / "backup.json")
    if not isinstance(data, dict) or data.get("package_id") != PACKAGE_ID or data.get("target") != str(target):
        raise ForgeError("Backup is not valid for this target.")
    snap = validate_state(data.get("snapshot"), target)
    if "snapshot" not in data:
        raise ForgeError("Backup is missing its snapshot.")
    if snap:
        for name in SKILLS:
            if inventory(p / "skills" / name) != snap["trees"][name]:
                raise ForgeError(f"Backup was modified: {name}.")
    return snap, p / "skills"


def set_state(root: Path, state: dict[str, Any] | None) -> None:
    if state is None:
        (root / "installed.json").unlink(missing_ok=True)
    else:
        atomic_json(root / "installed.json", state)


def recover_transaction(target: Path) -> None:
    root = state_directory(target)
    pending = read_json(root / "pending.json")
    if not isinstance(pending, dict) or pending.get("package_id") != PACKAGE_ID:
        raise ForgeError("Invalid journal. Preserve backups and request review.")
    old, src = read_backup(target, pending.get("backup_id", ""))
    if old != validate_state(pending.get("old"), target):
        raise ForgeError("Journal and previous backup do not match.")
    new = validate_state(pending.get("new"), target)
    # Recovery does not remove unrelated changes. It accepts only the old state,
    # the new state, or an absent directory for each skill in the transaction.
    for name in SKILLS:
        p = target / name
        no_links(p)
        if p.exists():
            actual = inventory(p)
            allowed = [x["trees"][name] for x in (old, new) if x]
            if actual not in allowed:
                raise ForgeError(f"Recovery blocked: unrelated content exists in {name}; it will not be deleted.")
    recovery = root / "transactions" / ("recover-" + uuid.uuid4().hex)
    no_links(recovery)
    recovery.mkdir(parents=True)
    try:
        if old:
            for name in SKILLS:
                shutil.copytree(src / name, recovery / name)
                if inventory(recovery / name) != old["trees"][name]:
                    raise ForgeError("Recovery copy failed integrity verification.")
        target.mkdir(parents=True, exist_ok=True)
        for name in SKILLS:
            p = target / name
            if p.exists():
                shutil.rmtree(p)
            if old:
                os.replace(recovery / name, p)
        set_state(root, old)
        (root / "pending.json").unlink()
        original = root / "transactions" / pending["backup_id"]
        if original.exists():
            no_links(original)
            shutil.rmtree(original)
    finally:
        if recovery.exists():
            shutil.rmtree(recovery)


def change(target: Path, old: dict[str, Any] | None,
           new: dict[str, Any] | None, new_source: Path | None) -> str:
    root = state_directory(target)
    identifier = uuid.uuid4().hex
    backup = backup_path(root, identifier)
    work = root / "transactions" / identifier
    no_links(work)
    backup.mkdir(parents=True)
    work.mkdir(parents=True)
    try:
        if old:
            for name in SKILLS:
                shutil.copytree(target / name, backup / "skills" / name)
                if inventory(backup / "skills" / name) != old["trees"][name]:
                    raise ForgeError("Backup does not match the previous installation.")
        atomic_json(backup / "backup.json", {"package_id": PACKAGE_ID, "target": str(target),
                    "created_utc": stamp(), "snapshot": old})
        if new:
            if new_source is None:
                raise ForgeError("Source for the new installation is missing.")
            for name in SKILLS:
                shutil.copytree(new_source / name, work / "new" / name)
                if inventory(work / "new" / name) != new["trees"][name]:
                    raise ForgeError("Source changed during preparation.")
        check_current(target, old)
        atomic_json(root / "pending.json", {"package_id": PACKAGE_ID, "backup_id": identifier,
                                           "old": old, "new": new})
        target.mkdir(parents=True, exist_ok=True)
        (work / "old").mkdir()
        for name in SKILLS:
            p = target / name
            if p.exists():
                os.replace(p, work / "old" / name)
            if new:
                os.replace(work / "new" / name, p)
        set_state(root, new)
        (root / "pending.json").unlink()
    except BaseException:
        if (root / "pending.json").exists():
            try:
                recover_transaction(target)
            except BaseException as rollback_error:
                raise ForgeError(f"Operation interrupted; automatic recovery did not complete: {rollback_error}. Preserve state and backups, then use recover.") from rollback_error
        raise
    finally:
        if not (root / "pending.json").exists() and work.exists():
            shutil.rmtree(work)
    return identifier


def execute(action: str, target: Path, source: Path, apply: bool = False,
            backup_id: str | None = None) -> dict[str, Any]:
    target = safe_target(target)
    root = state_directory(target)
    pending = (root / "pending.json").exists()
    if action == "backups":
        entries = []
        location = root / "backups"
        if location.exists():
            no_links(location)
            for p in sorted(location.iterdir()):
                if p.is_dir() and (p / "backup.json").exists():
                    info = read_json(p / "backup.json")
                    snap = info.get("snapshot") or {}
                    entries.append({"id": p.name, "version": snap.get("version"), "created_utc": info.get("created_utc")})
        return {"target": str(target), "backups": entries}
    if action == "status":
        old = load_state(target)
        issue = None
        try:
            check_current(target, old)
        except ForgeError as exc:
            issue = str(exc)
        return {"target": str(target), "state_directory": str(root), "version": old["version"] if old else None,
                "state": "drift-or-collision" if issue else ("installed-pristine" if old else "not-installed"),
                "pending_transaction": pending, "lock_present": (root / "operation.lock").exists(), "issue": issue}
    if action == "recover":
        if not pending:
            return {"action": action, "changed": False, "message": "No transaction to recover."}
        if not apply:
            return {"action": action, "changed": False, "message": "Preview: restore the previous snapshot only if no unrelated modifications are present."}
        with lock(root):
            recover_transaction(target)
        return {"action": action, "changed": True, "message": "Previous snapshot restored."}
    if pending:
        raise ForgeError("An incomplete transaction exists. Run status and recover before other changes.")
    old = load_state(target)
    check_current(target, old)
    new_source = None
    if action in {"install", "update"}:
        new = package_state(absolute(source), target)
        new_source = absolute(source) / "skills"
        if action == "install" and old:
            if new == old:
                return {"action": action, "changed": False, "message": "The same version is already installed and identical."}
            raise ForgeError("The suite is already installed. Use update.")
        if action == "update" and not old:
            raise ForgeError("No managed installation exists to update. Use install.")
        if old and new == old:
            return {"action": action, "changed": False, "message": "No update is required."}
        if old and tuple(map(int, new["version"].split("."))) <= tuple(map(int, old["version"].split("."))):
            raise ForgeError("Changed content requires a higher version. Use restore to return to a previous version.")
    elif action == "uninstall":
        if not old:
            return {"action": action, "changed": False, "message": "Suite is not installed; no files were removed."}
        new = None
    elif action == "restore":
        if not backup_id:
            raise ForgeError("restore requires --backup-id.")
        new, new_source = read_backup(target, backup_id)
        if new == old:
            return {"action": action, "changed": False, "message": "The requested snapshot is already active."}
    else:
        raise ForgeError("Unknown operation.")
    plan = {"action": action, "target": str(target), "state_directory": str(root),
            "from_version": old["version"] if old else None, "to_version": new["version"] if new else None,
            "skills": list(SKILLS), "changed": False}
    if not apply:
        plan["message"] = "Preview. No writes performed. Add --apply to execute."
        return plan
    with lock(root):
        if (root / "pending.json").exists() or load_state(target) != old:
            raise ForgeError("State changed after preview. Run the check again.")
        check_current(target, old)
        identifier = change(target, old, new, new_source)
    plan.update(changed=True, backup_id=identifier, message="Operation completed. Restart Codex and verify the skills.")
    return plan


def main() -> int:
    if sys.version_info < (3, 10):
        print("Python 3.10 or newer is required.", file=sys.stderr)
        return 2
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["install", "update", "uninstall", "status", "backups", "restore", "recover"])
    parser.add_argument("--target", type=Path, default=Path.home() / ".agents" / "skills")
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--apply", action="store_true", help="Authorize writes; preview is the default.")
    parser.add_argument("--backup-id")
    args = parser.parse_args()
    try:
        result = execute(args.action, args.target, args.source, args.apply, args.backup_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if result.get("issue") or result.get("pending_transaction") else 0
    except (ForgeError, OSError, ValueError) as exc:
        print(f"STOP: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
