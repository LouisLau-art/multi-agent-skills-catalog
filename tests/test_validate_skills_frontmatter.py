from __future__ import annotations

import tempfile
import textwrap
import unittest
from pathlib import Path

from scripts.validate_skills_frontmatter import (
    RepairResult,
    sanitize_frontmatter_text,
    validate_skill_file,
    validate_skill_tree,
)


class SanitizeFrontmatterTextTests(unittest.TestCase):
    def test_valid_frontmatter_is_unchanged(self) -> None:
        original = textwrap.dedent(
            """\
            ---
            name: example-skill
            description: Safe short description
            license: MIT
            ---
            """
        )

        result = sanitize_frontmatter_text(original)

        self.assertFalse(result.changed)
        self.assertEqual(result.content, original)
        self.assertEqual(result.repairs, [])

    def test_repairs_indented_keywords_block(self) -> None:
        original = textwrap.dedent(
            """\
            ---
            name: example-skill
            description: Example description

              Keywords: alpha, beta,
              gamma, delta
            license: MIT
            ---
            """
        )

        result = sanitize_frontmatter_text(original)

        self.assertTrue(result.changed)
        self.assertIn("keywords_block", result.repairs)
        self.assertIn("keywords: >", result.content)
        self.assertNotIn("  Keywords:", result.content)

    def test_repairs_yaml_breaking_description_scalar(self) -> None:
        original = textwrap.dedent(
            """\
            ---
            name: modal-skill
            description: Modal integration patterns. Activate for: API routes, webhooks. Provides: examples.
            ---
            """
        )

        result = sanitize_frontmatter_text(original)

        self.assertTrue(result.changed)
        self.assertIn("description_folded_scalar", result.repairs)
        self.assertIn("description: >", result.content)


class ValidateSkillFileTests(unittest.TestCase):
    def test_validate_skill_file_fixes_known_yaml_issue(self) -> None:
        content = textwrap.dedent(
            """\
            ---
            name: example-skill
            description: Example description

              Keywords: alpha, beta,
              gamma
            license: MIT
            ---

            # Example
            """
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            skill_path = Path(tmp_dir) / "SKILL.md"
            skill_path.write_text(content, encoding="utf-8")

            result = validate_skill_file(skill_path, check_only=False)

            self.assertEqual(result.status, "fixed")
            self.assertIn("keywords_block", result.repairs)
            saved = skill_path.read_text(encoding="utf-8")
            self.assertIn("keywords: >", saved)

    def test_validate_skill_file_reports_still_invalid_in_check_only_mode(self) -> None:
        content = textwrap.dedent(
            """\
            ---
            name: broken-skill
            description:
              [unterminated
            ---
            """
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            skill_path = Path(tmp_dir) / "SKILL.md"
            skill_path.write_text(content, encoding="utf-8")

            result = validate_skill_file(skill_path, check_only=True)

            self.assertEqual(result.status, "invalid")
            self.assertTrue(result.error)
            self.assertEqual(result.repairs, [])


class ValidateSkillTreeTests(unittest.TestCase):
    def test_ignores_hidden_directories_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            visible = root / "visible-skill"
            hidden = root / ".system"
            visible.mkdir()
            hidden.mkdir()
            (visible / "SKILL.md").write_text(
                "---\nname: visible\ndescription: ok\n---\n",
                encoding="utf-8",
            )

            summary = validate_skill_tree(root, check_only=True)

            self.assertEqual(summary.checked, 1)
            self.assertEqual(summary.valid, 1)
            self.assertEqual(summary.missing, 0)


if __name__ == "__main__":
    unittest.main()
