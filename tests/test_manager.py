from __future__ import annotations
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import manage_skills as manager
from package_lib import SKILLS, ForgeError, inventory, no_links, relative_name, write_manifest


class ManagerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="forge-test-")
        self.base = Path(self.tmp.name)
        self.source = self.base / "source"
        self.target = self.base / "runtime" / "skills"
        self.make_source(self.source, "1.0.0")

    def tearDown(self):
        self.tmp.cleanup()

    def make_source(self, root, version):
        root.mkdir(parents=True)
        (root / "suite.json").write_text(json.dumps({"schema_version": 1, "package_id": "interface-forge", "version": version, "skills": list(SKILLS)}), encoding="utf-8")
        (root / "VERSION").write_text(version + "\n", encoding="utf-8")
        for name in SKILLS:
            p = root / "skills" / name
            (p / "references").mkdir(parents=True)
            (p / "SKILL.md").write_text(f"# {name}\n", encoding="utf-8")
            (p / "references" / "rules.md").write_text(f"Rules {version}\n", encoding="utf-8")
        write_manifest(root)

    def run_action(self, action, apply=False, backup_id=None, source=None):
        return manager.execute(action, self.target, source or self.source, apply, backup_id)

    def install(self):
        return self.run_action("install", True)

    def new_source(self, version="1.1.0"):
        root = self.base / ("next-" + version)
        self.make_source(root, version)
        return root

    def interrupted_update(self):
        self.install()
        old = manager.load_state(self.target)
        src = self.new_source()
        new = manager.package_state(src, self.target)
        root = manager.state_directory(self.target)
        ident = uuid.uuid4().hex
        backup = root / "backups" / ident
        for name in SKILLS:
            shutil.copytree(self.target / name, backup / "skills" / name)
        manager.atomic_json(backup / "backup.json", {"package_id": "interface-forge", "target": str(self.target), "snapshot": old})
        manager.atomic_json(root / "pending.json", {"package_id": "interface-forge", "backup_id": ident, "old": old, "new": new})
        shutil.rmtree(self.target / SKILLS[0])
        shutil.copytree(src / "skills" / SKILLS[0], self.target / SKILLS[0])
        return old

    def test_preview_does_not_create_target_or_state(self):
        before = inventory(self.base)
        result = self.run_action("install")
        self.assertFalse(result["changed"])
        self.assertEqual(before, inventory(self.base))
        self.assertFalse(self.target.exists())

    def test_status_absent_is_read_only(self):
        before = inventory(self.base)
        result = self.run_action("status")
        self.assertEqual(result["state"], "not-installed")
        self.assertEqual(before, inventory(self.base))

    def test_install_exactly_five_directories(self):
        result = self.install()
        self.assertTrue(result["changed"])
        self.assertEqual(set(p.name for p in self.target.iterdir()), set(SKILLS))
        self.assertEqual(self.run_action("status")["state"], "installed-pristine")
        for name in SKILLS:
            self.assertEqual(inventory(self.target / name), inventory(self.source / "skills" / name))

    def test_ignored_cache_not_silently_copied(self):
        cache = self.source / "skills" / SKILLS[0] / "__pycache__"
        cache.mkdir()
        (cache / "extra.pyc").write_bytes(b"not-part-of-release")
        with self.assertRaises(ForgeError):
            self.install()
        self.assertFalse(self.target.exists())

    def test_ignored_dist_not_silently_copied(self):
        extra = self.source / "skills" / SKILLS[0] / "dist"
        extra.mkdir()
        (extra / "unlisted.txt").write_text("not-part-of-release", encoding="utf-8")
        with self.assertRaises(ForgeError):
            self.install()
        self.assertFalse(self.target.exists())

    def test_install_is_idempotent(self):
        self.install()
        old_backups = self.run_action("backups")
        self.assertFalse(self.install()["changed"])
        self.assertEqual(old_backups, self.run_action("backups"))

    def test_other_skills_and_configuration_untouched(self):
        other = self.target / "other-skill"
        other.mkdir(parents=True)
        (other / "keep.txt").write_text("user", encoding="utf-8")
        config = self.target.parent / "config.toml"
        config.write_text("custom = true", encoding="utf-8")
        agents = self.target.parent / "AGENTS.md"
        agents.write_text("personal rules", encoding="utf-8")
        self.install()
        self.run_action("uninstall", True)
        self.assertEqual((other / "keep.txt").read_text(), "user")
        self.assertEqual(config.read_text(), "custom = true")
        self.assertEqual(agents.read_text(), "personal rules")

    def test_unknown_directory_collision_refused(self):
        p = self.target / SKILLS[0]
        p.mkdir(parents=True)
        (p / "keep.txt").write_text("do not lose")
        with self.assertRaises(ForgeError):
            self.install()
        self.assertEqual((p / "keep.txt").read_text(), "do not lose")
        self.assertFalse((self.target / SKILLS[1]).exists())

    def test_file_collision_refused(self):
        self.target.mkdir(parents=True)
        p = self.target / SKILLS[0]
        p.write_text("user file")
        with self.assertRaises(ForgeError):
            self.install()
        self.assertEqual(p.read_text(), "user file")

    def test_modified_file_prevents_update_and_uninstall(self):
        self.install()
        p = self.target / SKILLS[1] / "SKILL.md"
        p.write_text("local modification")
        for action in ("update", "uninstall"):
            with self.subTest(action=action), self.assertRaises(ForgeError):
                self.run_action(action, True)
        self.assertEqual(p.read_text(), "local modification")

    def test_added_file_is_preserved(self):
        self.install()
        p = self.target / SKILLS[0] / "custom.md"
        p.write_text("added file")
        with self.assertRaises(ForgeError):
            self.run_action("uninstall", True)
        self.assertTrue(p.exists())

    def test_added_empty_directory_is_drift(self):
        self.install()
        (self.target / SKILLS[0] / "custom-empty").mkdir()
        with self.assertRaises(ForgeError):
            self.run_action("uninstall", True)

    def test_missing_file_is_drift(self):
        self.install()
        (self.target / SKILLS[0] / "SKILL.md").unlink()
        self.assertEqual(self.run_action("status")["state"], "drift-or-collision")
        with self.assertRaises(ForgeError):
            self.run_action("update", True)

    def test_tampered_source_refused_before_writes(self):
        (self.source / "skills" / SKILLS[0] / "SKILL.md").write_text("tampered")
        with self.assertRaises(ForgeError):
            self.install()
        self.assertFalse(self.target.exists())

    def test_update_to_newer_version(self):
        self.install()
        result = self.run_action("update", True, source=self.new_source())
        self.assertEqual(result["from_version"], "1.0.0")
        self.assertEqual(result["to_version"], "1.1.0")
        self.assertEqual(self.run_action("status")["version"], "1.1.0")

    def test_same_version_changed_refused(self):
        self.install()
        (self.source / "skills" / SKILLS[0] / "SKILL.md").write_text("new content")
        write_manifest(self.source)
        with self.assertRaises(ForgeError):
            self.run_action("update", True)

    def test_downgrade_refused(self):
        self.install()
        with self.assertRaises(ForgeError):
            self.run_action("update", True, source=self.new_source("0.9.9"))

    def test_update_without_install_refused(self):
        with self.assertRaises(ForgeError):
            self.run_action("update", True)

    def test_install_different_version_requires_update(self):
        self.install()
        with self.assertRaises(ForgeError):
            self.run_action("install", True, source=self.new_source())

    def test_uninstall_absent_is_noop(self):
        result = self.run_action("uninstall", True)
        self.assertFalse(result["changed"])
        self.assertFalse(self.target.exists())

    def test_update_backup_can_restore_previous_version(self):
        self.install()
        updated = self.run_action("update", True, source=self.new_source())
        self.run_action("restore", True, updated["backup_id"])
        self.assertEqual(self.run_action("status")["version"], "1.0.0")

    def test_uninstall_snapshot_can_reinstall(self):
        self.install()
        removed = self.run_action("uninstall", True)
        self.assertEqual(self.run_action("status")["state"], "not-installed")
        self.run_action("restore", True, removed["backup_id"])
        self.assertEqual(self.run_action("status")["state"], "installed-pristine")

    def test_first_empty_snapshot_restores_absence(self):
        installed = self.install()
        self.run_action("restore", True, installed["backup_id"])
        self.assertEqual(self.run_action("status")["state"], "not-installed")

    def test_backup_outside_skill_discovery_tree(self):
        self.install()
        self.run_action("update", True, source=self.new_source())
        self.assertEqual(len(list(self.target.rglob("SKILL.md"))), 5)
        self.assertFalse(manager.state_directory(self.target).is_relative_to(self.target))

    def test_tampered_backup_refused(self):
        self.install()
        removed = self.run_action("uninstall", True)
        backup = manager.backup_path(manager.state_directory(self.target), removed["backup_id"])
        (backup / "skills" / SKILLS[0] / "SKILL.md").write_text("tampered")
        with self.assertRaises(ForgeError):
            self.run_action("restore", True, removed["backup_id"])
        self.assertEqual(self.run_action("status")["state"], "not-installed")

    def test_bad_backup_identifier_refused(self):
        with self.assertRaises(ForgeError):
            self.run_action("restore", True, "../../outside")

    def test_backup_target_identity_checked(self):
        self.install()
        removed = self.run_action("uninstall", True)
        path = manager.backup_path(manager.state_directory(self.target), removed["backup_id"]) / "backup.json"
        data = json.loads(path.read_text())
        data["target"] = str(self.base / "another-target")
        path.write_text(json.dumps(data))
        with self.assertRaises(ForgeError):
            self.run_action("restore", True, removed["backup_id"])

    def test_lock_refuses_concurrent_change(self):
        root = manager.state_directory(self.target)
        root.mkdir(parents=True)
        (root / "operation.lock").write_text("processo attivo")
        with self.assertRaises(ForgeError):
            self.install()
        self.assertFalse(self.target.exists())
        self.assertTrue((root / "operation.lock").exists())

    def test_exception_during_update_rolls_back(self):
        self.install()
        old = manager.load_state(self.target)
        real_replace = os.replace
        fired = False
        def fail_once(src, dst):
            nonlocal fired
            src = Path(src)
            if not fired and src.parent.name == "new" and src.name == SKILLS[1]:
                fired = True
                raise OSError("simulated error")
            return real_replace(src, dst)
        with mock.patch.object(manager.os, "replace", side_effect=fail_once):
            with self.assertRaises(OSError):
                self.run_action("update", True, source=self.new_source())
        self.assertTrue(fired)
        self.assertEqual(manager.load_state(self.target), old)
        self.assertEqual(self.run_action("status")["state"], "installed-pristine")
        self.assertFalse((manager.state_directory(self.target) / "pending.json").exists())

    def test_exception_during_first_install_restores_absence(self):
        real_replace = os.replace
        fired = False
        def fail_once(src, dst):
            nonlocal fired
            src = Path(src)
            if not fired and src.parent.name == "new" and src.name == SKILLS[1]:
                fired = True
                raise OSError("simulated error")
            return real_replace(src, dst)
        with mock.patch.object(manager.os, "replace", side_effect=fail_once):
            with self.assertRaises(OSError):
                self.install()
        self.assertTrue(fired)
        self.assertEqual(self.run_action("status")["state"], "not-installed")
        self.assertEqual(list(self.target.iterdir()), [])

    def test_journal_recovery_restores_snapshot(self):
        old = self.interrupted_update()
        self.assertTrue(self.run_action("status")["pending_transaction"])
        self.run_action("recover", True)
        self.assertEqual(manager.load_state(self.target), old)
        self.assertEqual(self.run_action("status")["state"], "installed-pristine")

    def test_recovery_does_not_delete_foreign_changes(self):
        self.interrupted_update()
        p = self.target / SKILLS[0] / "user-added.md"
        p.write_text("do not delete")
        with self.assertRaises(ForgeError):
            self.run_action("recover", True)
        self.assertEqual(p.read_text(), "do not delete")
        self.assertTrue(self.run_action("status")["pending_transaction"])

    def test_pending_transaction_blocks_new_operation(self):
        self.interrupted_update()
        with self.assertRaises(ForgeError):
            self.run_action("uninstall", True)

    def test_recovery_preview_is_read_only(self):
        self.interrupted_update()
        before = inventory(self.base)
        self.run_action("recover")
        self.assertEqual(before, inventory(self.base))

    def test_restore_preview_is_read_only(self):
        installed = self.install()
        before = inventory(self.base)
        self.run_action("restore", backup_id=installed["backup_id"])
        self.assertEqual(before, inventory(self.base))

    def test_invalid_target_root_or_home(self):
        for p in (Path(self.target.anchor), Path.home()):
            with self.subTest(path=p), self.assertRaises(ForgeError):
                manager.safe_target(p)

    def test_source_target_overlap_refused(self):
        with self.assertRaises(ForgeError):
            manager.execute("install", self.source / "runtime", self.source, True)

    def test_symlink_target_refused(self):
        actual = self.base / "actual"
        actual.mkdir()
        alias = self.base / "alias"
        try:
            alias.symlink_to(actual, target_is_directory=True)
        except OSError as exc:
            self.skipTest(f"Symlink unavailable in this environment: {exc}")
        with self.assertRaises(ForgeError):
            manager.execute("install", alias / "skills", self.source, True)
        self.assertEqual(list(actual.iterdir()), [])

    def test_source_symlink_refused(self):
        outside = self.base / "external.txt"
        outside.write_text("outside")
        alias = self.source / "skills" / SKILLS[0] / "alias.md"
        try:
            alias.symlink_to(outside)
        except OSError as exc:
            self.skipTest(f"Symlink unavailable: {exc}")
        with self.assertRaises(ForgeError):
            self.install()
        self.assertEqual(outside.read_text(), "outside")

    def test_portable_relative_paths(self):
        for value in ("../a", "/tmp/a", "a\\b", "C:a", "a//b", "CON.txt", "a/evil.", "a?.md", "a\x00b"):
            with self.subTest(value=value), self.assertRaises(ForgeError):
                relative_name(value)
        self.assertEqual(relative_name("references/core-contract.md"), "references/core-contract.md")

    def test_invalid_state_cannot_select_other_directories(self):
        self.install()
        path = manager.state_directory(self.target) / "installed.json"
        state = json.loads(path.read_text())
        state["trees"]["unrelated"] = state["trees"].pop(SKILLS[0])
        path.write_text(json.dumps(state))
        with self.assertRaises(ForgeError):
            self.run_action("uninstall", True)
        self.assertTrue((self.target / SKILLS[0]).exists())

    def test_real_package_cli_lifecycle(self):
        source = self.base / "full-source"
        shutil.copytree(ROOT, source, ignore=shutil.ignore_patterns("__pycache__", ".git", "*.pyc", "local"))
        write_manifest(source)
        script = source / "scripts" / "manage_skills.py"
        for action, extra in (("install", []), ("install", ["--apply"]), ("status", []), ("uninstall", ["--apply"])):
            result = subprocess.run([sys.executable, str(script), action, "--target", str(self.target), *extra], text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            if action == "status":
                self.assertEqual(payload["state"], "installed-pristine")

if __name__ == "__main__":
    unittest.main()
