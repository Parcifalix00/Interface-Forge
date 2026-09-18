from __future__ import annotations
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_package import validate
from package_lib import SKILLS, ForgeError, inventory, verify_manifest, write_manifest

class PackageTests(unittest.TestCase):
    def test_static_package_contract(self):
        result = validate(ROOT)
        self.assertEqual(result["status"], "PASS", result["errors"])

    def test_exact_five_skills(self):
        data = json.loads((ROOT / "suite.json").read_text())
        self.assertEqual(data["skills"], list(SKILLS))

    def test_canonical_contracts_identical(self):
        for name in SKILLS:
            self.assertEqual((ROOT / "contracts/core-contract.md").read_bytes(), (ROOT / "skills" / name / "references/core-contract.md").read_bytes())

    def test_focused_entrypoint_size(self):
        for name in SKILLS:
            with self.subTest(skill=name):
                self.assertLess(len((ROOT / "skills" / name / "SKILL.md").read_text().splitlines()), 200)

    def test_licenses_travel_with_each_skill(self):
        for name in SKILLS:
            self.assertTrue((ROOT / "skills" / name / "LICENSE").is_file())
            self.assertIn("Higgsfield AI", (ROOT / "skills" / name / "licenses/Higgsfield-MIT.txt").read_text())

    def test_evals_include_positive_negative_and_device_limits(self):
        data = json.loads((ROOT / "evals/routing-cases.json").read_text())
        cases = {c["id"]: c for c in data["cases"]}
        self.assertGreaterEqual(len(cases), 20)
        self.assertEqual(cases["negative-backend"]["acceptable_entry_skills"], [])
        self.assertEqual(cases["iphone-proof"]["execution_status"], "NOT_RUN")
        self.assertIn("cost-unknown", cases)

    def test_manifest_detects_new_changed_and_removed_file(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "package"
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns("__pycache__", ".git", "*.pyc", "local"))
            write_manifest(root)
            verify_manifest(root)
            p = root / "unexpected.txt"
            p.write_text("extra")
            with self.assertRaises(ForgeError):
                verify_manifest(root)
            p.unlink()
            original = (root / "README.md").read_bytes()
            (root / "README.md").write_text("changed")
            with self.assertRaises(ForgeError):
                verify_manifest(root)
            (root / "README.md").write_bytes(original)
            (root / "LICENSE").unlink()
            with self.assertRaises(ForgeError):
                verify_manifest(root)

    def test_inventory_includes_empty_directories(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "empty").mkdir()
            self.assertEqual(inventory(root)["directories"], ["empty"])

if __name__ == "__main__":
    unittest.main()
