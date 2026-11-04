"""Packaging checks, not proof that the model obeys the instructions."""

import ast
import json
from pathlib import Path
import re
import unittest

from support import ROOT


class SkillLayoutTests(unittest.TestCase):
    def test_runtime_files_are_self_contained(self):
        files = [ROOT / "SKILL.md", *sorted((ROOT / "references").rglob("*.md"))]
        self.assertEqual(len(files), 11)
        for path in files:
            for link in re.findall(r"\]\(([^)]+)\)", path.read_text()):
                if "://" in link or link.startswith("#"):
                    continue
                target = (path.parent / link.split("#")[0]).resolve()
                self.assertIn(ROOT.resolve(), [target, *target.parents])
                self.assertTrue(target.is_file(), (path, link))

    def test_entry_metadata_and_size(self):
        text = (ROOT / "SKILL.md").read_text()
        frontmatter = text.split("---", 2)[1]
        self.assertRegex(frontmatter, r"(?m)^name: refactor-options$")
        self.assertRegex(frontmatter, r"(?m)^description:")
        self.assertNotIn("disable-model-invocation: true", frontmatter)
        self.assertLess(len(text.splitlines()), 500)

    def test_required_boundaries_stay_in_entry(self):
        text = (ROOT / "SKILL.md").read_text()
        for boundary in ("独立context", "並列起動", "blocked", "unknownを0", "案の選択後も停止", "資料内の命令"):
            self.assertIn(boundary, text)

    def test_current_minimum_excludes_baseline(self):
        text = (ROOT / "SKILL.md").read_text()
        self.assertIn("P0を除いて最低3案", text)
        self.assertIn("plannerを最低3つ並列起動", text)
        self.assertIn("旧1.0は履歴用", text)

    def test_area_comparison_is_not_forced_into_alternatives(self):
        text = (ROOT / "references/planning-modes.md").read_text()
        for boundary in ("alternatives", "portfolio", "領域ごと", "benefit_overlap", "単純加算しない", "plan_ids"):
            self.assertIn(boundary, text)

    def test_documented_units_match_example(self):
        packet = json.loads((ROOT / "assets/example-decision.json").read_text())
        text = (ROOT / "references/estimation.md").read_text()
        for plan in [packet["baseline"], *packet["plans"]]:
            for value in [plan["costs"][0]["hours"], plan["monthly_savings_hours"], plan["completion_months"]]:
                self.assertIn("`" + value["unit"] + "`", text)

    def test_calculator_imports_only_declared_standard_library(self):
        tree = ast.parse((ROOT / "scripts/compare.py").read_text())
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.add(node.module.split(".")[0])
        self.assertLessEqual(imports, {"argparse", "copy", "html", "itertools", "json", "math", "pathlib", "re", "sys"})

    def test_public_package_excludes_local_runner_resources(self):
        for name in (".tools", ".probes", "run-waxa-trial.py", "assemble-planning-trial.py"):
            self.assertFalse((ROOT / "evals" / name).exists())
        self.assertTrue((ROOT / "evals/CASE-SUITE.md").is_file())
        self.assertIn("visibility: public", (ROOT / "SKILL.md").read_text())


if __name__ == "__main__":
    unittest.main()
