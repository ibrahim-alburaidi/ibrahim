"""Regression checks for audit gaps; all mutations affect temporary copies only."""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ValidationRegressionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name) / "badil"
        shutil.copytree(ROOT, self.project, ignore=shutil.ignore_patterns(
            ".git", "__pycache__", "local-results", "private-inputs"))

    def run_check(self):
        return subprocess.run([sys.executable, str(self.project / "scripts/validate_project.py")],
                              capture_output=True, text=True, encoding="utf-8")

    def rejected(self, phrase):
        result = self.run_check()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(phrase, result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_valid_project(self):
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_changed_deadline_in_both_outputs(self):
        for name in ("outputs/tasks.json", "outputs/handover.md"):
            path = self.project / name
            path.write_text(path.read_text(encoding="utf-8").replace("2026-10-05", "2026-10-09"), encoding="utf-8")
        self.rejected("Known deadline changed: T03")

    def test_trainee_table_mismatch(self):
        path = self.project / "README.md"
        path.write_text(path.read_text(encoding="utf-8").replace("**ibrahim abdullah alburaidi**", "**Wrong Name**"), encoding="utf-8")
        self.rejected("Course table mismatch: README.md/Trainee")

    def test_numeric_task_text(self):
        path = self.project / "outputs/tasks.json"
        tasks = json.loads(path.read_text(encoding="utf-8"))
        tasks[0]["task"] = 123
        path.write_text(json.dumps(tasks, ensure_ascii=False), encoding="utf-8")
        self.rejected("Task field must be a non-empty string: task")

    def test_unknown_evidence(self):
        path = self.project / "outputs/tasks.json"
        tasks = json.loads(path.read_text(encoding="utf-8"))
        tasks[0]["sources"] = ["M99"]
        path.write_text(json.dumps(tasks, ensure_ascii=False), encoding="utf-8")
        self.rejected("Unknown evidence in T01")

    def test_wrong_demo_duration(self):
        path = self.project / "docs/demo-guide.md"
        path.write_text(path.read_text(encoding="utf-8").replace("آلية العمل — 60 ثانية", "آلية العمل — 75 ثانية"), encoding="utf-8")
        self.rejected("Demo duration must be 300 seconds")


if __name__ == "__main__":
    unittest.main(verbosity=2)
