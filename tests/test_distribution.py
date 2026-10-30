"""Exercise acceptance and rejection with disposable package fixtures."""
import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("distribution", ROOT / "scripts/validate_distribution.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="cleanup-package-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "repository"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(".git", "__pycache__", ".venv"))
        self.package = self.root / "skills/cleanup-worktree"
        self.skill = self.package / "SKILL.md"

    def assert_rejected(self, diagnostic):
        errors = validator.check_distribution(self.root)
        self.assertTrue(any(diagnostic in error for error in errors), errors)

    def append_link(self, link):
        with self.skill.open("a") as stream:
            stream.write("\n" + link + "\n")

    def test_current_package_is_valid(self):
        self.assertEqual(validator.check_distribution(self.root), [])

    def test_reference_within_package_is_valid(self):
        self.append_link("[Details](references/verification.md)")
        self.assertEqual(validator.check_distribution(self.root), [])

    def test_repository_documentation_can_link_to_package(self):
        with (self.root / "README.md").open("a") as stream:
            stream.write("\n[Skill](skills/cleanup-worktree/SKILL.md)\n")
        self.assertEqual(validator.check_distribution(self.root), [])

    def test_package_cannot_depend_on_repository_readme(self):
        self.append_link("[Required policy](../../README.md)")
        self.assert_rejected("Invalid relative link")

    def test_encoded_escape_is_rejected(self):
        self.append_link("[Required policy](%2e%2e/%2e%2e/README.md)")
        self.assert_rejected("Invalid relative link")

    def test_reference_style_escape_is_rejected(self):
        self.append_link("[Required policy][policy]\n\n[policy]: ../../README.md")
        self.assert_rejected("Invalid relative link")

    def test_angle_target_escape_is_rejected(self):
        self.append_link("[Required policy](<../../README.md>)")
        self.assert_rejected("Invalid relative link")

    def test_external_https_link_is_valid(self):
        self.append_link("[Git](https://git-scm.com/docs/git-worktree)")
        self.assertEqual(validator.check_distribution(self.root), [])

    def test_file_scheme_is_rejected(self):
        self.append_link("[Policy](file:///external-policy.md)")
        self.assert_rejected("Unsupported link")

    def test_missing_file_is_rejected(self):
        self.append_link("[Details](references/missing.md)")
        self.assert_rejected("Invalid relative link")

    def test_external_file_symlink_is_rejected(self):
        outside = Path(self.temporary.name) / "outside.md"
        outside.write_text("Fixture content\n")
        (self.package / "references/linked.md").symlink_to(outside)
        self.assert_rejected("Symbolic link is not distributable")

    def test_external_directory_symlink_is_rejected(self):
        outside = Path(self.temporary.name) / "outside"
        outside.mkdir()
        (outside / "policy.md").write_text("Fixture content\n")
        (self.package / "linked-directory").symlink_to(outside, target_is_directory=True)
        self.assert_rejected("Symbolic link is not distributable")

    def test_broken_symlink_is_rejected(self):
        (self.package / "broken.md").symlink_to("missing.md")
        self.assert_rejected("Symbolic link is not distributable")

    def test_internal_symlink_is_rejected(self):
        (self.package / "alias.md").symlink_to("SKILL.md")
        self.assert_rejected("Symbolic link is not distributable")

    def test_symlinked_package_directory_is_rejected(self):
        relocated = self.root / "relocated"
        self.package.rename(relocated)
        self.package.symlink_to(relocated, target_is_directory=True)
        self.assert_rejected("Symbolic link is not distributable")

    def test_frontmatter_sequence_is_rejected_without_traceback(self):
        self.skill.write_text("---\n- invalid\n---\nBody\n")
        self.assert_rejected("Expected YAML mapping")

    def test_nested_metadata_sequence_is_rejected_without_traceback(self):
        self.skill.write_text('---\nname: cleanup-worktree\nmetadata: [invalid]\n---\nBody\n')
        self.assert_rejected("Expected metadata mapping")

    def test_yaml_syntax_error_is_rejected(self):
        self.skill.write_text("---\nname: [\n---\nBody\n")
        self.assert_rejected("Invalid YAML")

    def test_body_version_mismatch_is_rejected(self):
        text = self.skill.read_text()
        self.skill.write_text(text.replace("## Version\n\n", "## Other\n\n"))
        self.assert_rejected("Body version differs")

    def test_readme_version_mismatch_is_rejected(self):
        path = self.root / "README.md"
        path.write_text(path.read_text().replace("Current version:", "Old version:"))
        self.assert_rejected("README version differs")

    def test_missing_release_notes_is_rejected(self):
        for path in (self.root / ".github").glob("RELEASE_NOTES_*.md"):
            path.unlink()
        self.assert_rejected("Versioned release notes missing")

    def test_optional_ui_metadata_can_be_absent(self):
        (self.package / "agents/openai.yaml").unlink()
        self.assertEqual(validator.check_distribution(self.root), [])

    def test_invalid_ui_metadata_is_rejected_without_traceback(self):
        (self.package / "agents/openai.yaml").write_text("interface: [invalid]\n")
        self.assert_rejected("Invalid UI short description")

    def test_missing_required_source_is_rejected_without_traceback(self):
        self.skill.unlink()
        self.assert_rejected("Cannot read")


if __name__ == "__main__":
    unittest.main()
