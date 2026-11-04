"""Static checks for the new case files; never execute a model or fixture.

This verifies the deliberately simple file format, not a general YAML parser
or the host CLI loader, nor the semantic correctness of a model response.
"""

import ast
import json
from pathlib import Path
import re
import unittest

from support import ROOT


EVALS = ROOT / "evals"
SUITE = json.loads((EVALS / "case-suite.json").read_text())
CASES = SUITE["cases"]


def split_frontmatter(path):
    text = path.read_text()
    if not text.startswith("---\n"):
        raise AssertionError(f"Missing frontmatter: {path}")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise AssertionError(f"Unclosed frontmatter: {path}")
    return parts[1], parts[2].strip()


class EvalCaseDefinitionTests(unittest.TestCase):
    def test_manifest_count_phases_and_status(self):
        ids = [case["id"] for case in CASES]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(ids), SUITE["new_case_count"])
        self.assertEqual(SUITE["status"], "defined-not-run")
        self.assertEqual(SUITE["skill_version"], "0.3.0")
        self.assertEqual({case["phase"] for case in CASES}, {"generation", "review", "capability", "lifecycle"})
        for case in CASES:
            self.assertRegex(case["id"], r"^[a-z][a-z0-9-]+$")
            self.assertTrue(case["covers"])

    def test_case_metadata_uses_the_case_folder_format(self):
        for case in CASES:
            with self.subTest(case=case["id"]):
                text = (EVALS / case["id"] / "case.yaml").read_text()
                self.assertRegex(text, r'(?m)^schema_version: "1\.1"$')
                self.assertIn("\nname: " + case["id"] + "\n", text)
                self.assertRegex(text, r"(?m)^expected_outcome: \|\n  \S")
                top_keys = set(re.findall(r"(?m)^([a-z_]+):", text))
                self.assertLessEqual(top_keys, {"schema_version", "name", "expected_outcome", "context"})

    def test_prompt_settings_and_nonempty_user_text(self):
        for case in CASES:
            settings, body = split_frontmatter(EVALS / case["id"] / "prompt.md")
            keys = set(re.findall(r"(?m)^([a-z_]+):", settings))
            self.assertEqual(keys, {"tags", "max_turns", "timeout_seconds", "allowed_tools"})
            self.assertIn("tags: [skill-creator]", settings)
            for key in ("max_turns", "timeout_seconds"):
                value = re.search(r"(?m)^" + key + r": ([0-9]+)$", settings)
                self.assertIsNotNone(value)
                self.assertGreater(int(value.group(1)), 0)
            self.assertTrue(body)

    def test_graders_are_concrete_ordered_and_counted(self):
        count = 0
        for case in CASES:
            files = sorted((EVALS / case["id"] / "graders").glob("*.md"))
            self.assertEqual(len(files), 3, case["id"])
            numbers = []
            for path in files:
                self.assertRegex(path.name, r"^[0-9]{2}-[a-z0-9-]+\.md$")
                numbers.append(path.name[:2])
                settings, body = split_frontmatter(path)
                self.assertEqual(settings.strip(), "type: llm\nfocus: trace\nweight: 1")
                self.assertGreater(len(body), 25)
                self.assertNotIn("The response completes the task", body)
                count += 1
            self.assertEqual(numbers, ["01", "02", "03"])
        self.assertEqual(count, SUITE["new_assertion_count"])

    def test_declared_inputs_are_self_contained(self):
        for case in CASES:
            folder = EVALS / case["id"]
            _, body = split_frontmatter(folder / "prompt.md")
            inputs = folder / "files"
            if not inputs.exists():
                self.assertEqual(case["phase"], "capability")
                self.assertNotIn("Input files:", body)
                continue
            declaration = re.search(r"(?m)^Input files: (.+)$", body)
            self.assertIsNotNone(declaration, case["id"])
            names = [name.strip() for name in declaration.group(1).split(",")]
            self.assertEqual(len(names), len(set(names)))
            self.assertEqual(set(names), {p.name for p in inputs.iterdir()})
            for name in names:
                self.assertEqual(Path(name).name, name)
                path = inputs / name
                self.assertFalse(path.is_symlink())
                self.assertTrue(path.is_file())
                self.assertTrue(path.read_text().strip())

    def test_scaffolds_only_copy_local_fixtures(self):
        expected = '#!/usr/bin/env bash\nset -eu\ncp -R "$(dirname "$0")/files/." .\n'
        for case in CASES:
            folder = EVALS / case["id"]
            if not (folder / "files").exists():
                self.assertFalse((folder / "place-files.sh").exists())
                continue
            self.assertEqual((folder / "place-files.sh").read_text(), expected)
            self.assertIn("context:\n  scaffold_script: place-files.sh", (folder / "case.yaml").read_text())

    def test_fixture_python_is_parsed_but_not_imported(self):
        for case in CASES:
            for path in (EVALS / case["id"] / "files").glob("*.py"):
                ast.parse(path.read_text(), filename=str(path))
        self.assertFalse((Path.cwd() / "EVAL_INJECTION_MARKER.txt").exists())
        self.assertFalse(list((EVALS / "scope-injection").rglob("EVAL_INJECTION_MARKER.txt")))

    def test_historical_cases_remain_separate(self):
        added = {case["id"] for case in CASES}
        existing = set(SUITE["existing_cases"])
        self.assertTrue(existing)
        self.assertFalse(added & existing)
        for name in existing:
            self.assertTrue((EVALS / name / "case.yaml").is_file())
        self.assertIn("モデル評価は未実行", (EVALS / "CASE-SUITE.md").read_text())


if __name__ == "__main__":
    unittest.main()
