from __future__ import annotations
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / "skills/frontend-visual-qa/scripts"

def load(name):
    spec = importlib.util.spec_from_file_location(name, QA / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    previous = sys.dont_write_bytecode
    try:
        sys.dont_write_bytecode = True
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = previous
    return module
report = load("validate_report")
copycheck = load("check_copy")

class ReportTests(unittest.TestCase):
    def valid(self):
        return {"schema_version": 1, "project": "Synthetic test", "revision": "test-1", "scope": "Form on device",
                "requirements": [{"id": "iphone", "platform": "iphone", "description": "Keyboard", "allowed_methods": ["physical-device", "platform-simulator"]}],
                "results": [{"requirement_id": "iphone", "platform": "iphone", "status": "PASS", "method": "physical-device", "environment": "Synthetic unit-test environment, not real evidence", "evidence": ["proof.txt"], "reason": ""}]}

    def test_complete_report_ready(self):
        self.assertEqual(report.assess(self.valid())["state"], "READY_FOR_REVIEW")

    def test_failed_report_blocked(self):
        data = self.valid(); data["results"][0]["status"] = "FAIL"
        self.assertEqual(report.assess(data)["state"], "BLOCKED")

    def test_unrun_report_incomplete(self):
        data = self.valid(); data["results"][0].update(status="NOT_RUN", method=None, environment=None, evidence=[], reason="Environment unavailable")
        self.assertEqual(report.assess(data)["state"], "INCOMPLETE")

    def test_missing_result_incomplete(self):
        data = self.valid(); data["results"] = []
        self.assertEqual(report.assess(data)["state"], "INCOMPLETE")

    def test_not_applicable_requires_reason(self):
        data = self.valid(); data["results"][0].update(status="NOT_APPLICABLE", reason="")
        with self.assertRaises(report.ReportError): report.assess(data)
        data["results"][0]["reason"] = "Scope exclusion documented in fixture"
        self.assertEqual(report.assess(data)["state"], "READY_FOR_REVIEW")

    def test_emulation_cannot_satisfy_device_requirement(self):
        data = self.valid(); data["results"][0]["method"] = "browser-emulation"
        with self.assertRaises(report.ReportError): report.assess(data)

    def test_emulation_allowed_for_separate_layout_requirement(self):
        data = self.valid(); data["requirements"][0]["allowed_methods"] = ["browser-emulation"]
        data["results"][0]["method"] = "browser-emulation"
        self.assertEqual(report.assess(data)["state"], "READY_FOR_REVIEW")

    def test_platform_mismatch_rejected(self):
        data = self.valid(); data["results"][0]["platform"] = "desktop"
        with self.assertRaises(report.ReportError): report.assess(data)

    def test_pass_requires_evidence(self):
        data = self.valid(); data["results"][0]["evidence"] = []
        with self.assertRaises(report.ReportError): report.assess(data)

    def test_pass_requires_environment(self):
        data = self.valid(); data["results"][0]["environment"] = None
        with self.assertRaises(report.ReportError): report.assess(data)

    def test_duplicate_results_rejected(self):
        data = self.valid(); data["results"].append(copy.deepcopy(data["results"][0]))
        with self.assertRaises(report.ReportError): report.assess(data)

    def test_duplicate_requirements_rejected(self):
        data = self.valid(); data["requirements"].append(copy.deepcopy(data["requirements"][0]))
        with self.assertRaises(report.ReportError): report.assess(data)

    def test_unknown_result_rejected(self):
        data = self.valid(); data["results"][0]["requirement_id"] = "unknown-result"
        with self.assertRaises(report.ReportError): report.assess(data)

    def test_empty_requirements_rejected(self):
        data = self.valid(); data["requirements"] = []
        with self.assertRaises(report.ReportError): report.assess(data)

    def test_unknown_method_rejected(self):
        data = self.valid(); data["results"][0]["method"] = "magic"
        with self.assertRaises(report.ReportError): report.assess(data)

    def test_invalid_types_rejected(self):
        for field, value in (("schema_version", True), ("requirements", None), ("results", "pass"), ("project", [])):
            data = self.valid(); data[field] = value
            with self.subTest(field=field), self.assertRaises(report.ReportError): report.assess(data)

    def test_template_stays_incomplete(self):
        data = json.loads((ROOT / "skills/frontend-visual-qa/templates/qa-report.json").read_text())
        self.assertEqual(report.assess(data)["state"], "INCOMPLETE")

    def test_context_placeholder_blocks_readiness(self):
        data = self.valid(); data["project"] = "TO_FILL"
        self.assertEqual(report.assess(data)["state"], "INCOMPLETE")

    def test_local_evidence_existence(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            with self.assertRaises(report.ReportError): report.assess(self.valid(), root)
            (root / "proof.txt").write_text("fixture only")
            self.assertEqual(report.assess(self.valid(), root)["state"], "READY_FOR_REVIEW")

    def test_evidence_outside_root_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d); (base / "proof.txt").write_text("outside"); (base / "evidence").mkdir()
            data = self.valid(); data["results"][0]["evidence"] = ["../proof.txt"]
            with self.assertRaises(report.ReportError): report.assess(data, base / "evidence")

    def test_cli_exit_codes(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "report.json"
            data = self.valid()
            for expected in (0, 1, 2):
                if expected == 1:
                    data["results"] = []
                if expected == 2:
                    data["requirements"] = []
                p.write_text(json.dumps(data))
                run = subprocess.run([sys.executable, str(QA / "validate_report.py"), str(p)], capture_output=True, text=True)
                self.assertEqual(run.returncode, expected, run.stderr)

class CopyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.root = Path(self.tmp.name)
    def tearDown(self): self.tmp.cleanup()

    def test_clean_text(self):
        p = self.root / "copy.md"; p.write_text("Clean text - simple.\n", encoding="utf-8")
        result = copycheck.scan([p])
        self.assertEqual(result["files_checked"], 1); self.assertEqual(result["findings"], []); self.assertEqual(result["errors"], [])

    def test_finds_em_dash_without_mutating(self):
        p = self.root / "copy.md"; p.write_text("one " + chr(0x2014) + " two\n", encoding="utf-8")
        before = p.read_bytes(); result = copycheck.scan([p])
        self.assertEqual(result["findings"][0]["codepoint"], "U+2014")
        self.assertEqual(result["findings"][0]["column"], 5)
        self.assertEqual(p.read_bytes(), before)

    def test_optional_en_dash(self):
        p = self.root / "copy.md"; p.write_text("1" + chr(0x2013) + "3", encoding="utf-8")
        self.assertEqual(copycheck.scan([p])["findings"], [])
        self.assertEqual(len(copycheck.scan([p], True)["findings"]), 1)

    def test_invalid_encoding_is_not_false_pass(self):
        p = self.root / "copy.md"; p.write_bytes(b"\xff\xfe\xfa")
        result = copycheck.scan([p])
        self.assertTrue(result["errors"]); self.assertEqual(result["files_checked"], 0)

    def test_missing_file_is_error(self):
        self.assertTrue(copycheck.scan([self.root / "missing.md"])["errors"])

    def test_empty_directory_is_not_pass(self):
        self.assertTrue(copycheck.scan([self.root])["errors"])

    def test_dependency_directories_excluded(self):
        (self.root / "node_modules").mkdir()
        (self.root / "node_modules/bad.md").write_text(chr(0x2014), encoding="utf-8")
        (self.root / "good.md").write_text("clean")
        result = copycheck.scan([self.root])
        self.assertEqual(result["files_checked"], 1); self.assertEqual(result["findings"], [])

    def test_report_does_not_echo_line_content(self):
        p = self.root / "copy.md"; p.write_text("confidential data " + chr(0x2014), encoding="utf-8")
        result = json.dumps(copycheck.scan([p]), ensure_ascii=False)
        self.assertNotIn("confidential data", result)

    def test_duplicate_inputs_count_once(self):
        p = self.root / "copy.md"; p.write_text("clean")
        self.assertEqual(copycheck.scan([p, self.root])["files_checked"], 1)

    def test_symlink_is_not_followed(self):
        p = self.root / "outside.md"; p.write_text(chr(0x2014), encoding="utf-8")
        link = self.root / "alias.md"
        try: link.symlink_to(p)
        except OSError as exc: self.skipTest(str(exc))
        result = copycheck.scan([link])
        self.assertTrue(result["errors"]); self.assertEqual(result["files_checked"], 0)

if __name__ == "__main__":
    unittest.main()
