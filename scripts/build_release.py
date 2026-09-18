#!/usr/bin/env python3
"""Build a local release after checks and tests; does not publish anything."""
from __future__ import annotations
import argparse
from datetime import date
import hashlib
from pathlib import Path
import subprocess
import sys
import zipfile
from package_lib import ForgeError, package_files, suite, write_manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="ZIP path outside the project root.")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    output = args.output.expanduser().absolute()
    try:
        if output.is_relative_to(root):
            raise ForgeError("The output ZIP must be outside the source directory.")
        if output.exists() or output.with_suffix(output.suffix + ".sha256").exists():
            raise ForgeError("Output already exists. Choose a new name or deliberately remove the previous build.")
        subprocess.run([sys.executable, "-B", str(root / "scripts" / "check_package.py")], cwd=root, check=True)
        subprocess.run([sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=root, check=True)
        info = suite(root)
        day = date.fromisoformat(info["release_date"])
        write_manifest(root)
        files = sorted([*package_files(root), "release-manifest.json"])
        output.parent.mkdir(parents=True, exist_ok=True)
        temp = output.with_name(output.name + ".part")
        if temp.exists():
            raise ForgeError("A .part file already exists. Inspect the previous build first.")
        try:
            with zipfile.ZipFile(temp, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
                for rel in files:
                    record = zipfile.ZipInfo("Interface-Forge/" + rel, (day.year, day.month, day.day, 0, 0, 0))
                    record.compress_type = zipfile.ZIP_DEFLATED
                    record.external_attr = 0o100644 << 16
                    archive.writestr(record, (root / rel).read_bytes())
            temp.replace(output)
        finally:
            if temp.exists():
                temp.unlink()
        digest = hashlib.sha256(output.read_bytes()).hexdigest()
        output.with_suffix(output.suffix + ".sha256").write_text(f"{digest}  {output.name}\n", encoding="ascii")
        print(f"Release: {output}\nFile: {len(files)}\nSHA-256: {digest}")
        return 0
    except (ForgeError, OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"BUILD STOPPED: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
