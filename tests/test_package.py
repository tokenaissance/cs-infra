import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestPackage(unittest.TestCase):
    def test_manifest_identity(self):
        manifest = json.loads((ROOT / "manifest.json").read_text())
        self.assertEqual(manifest["name"], "cs-infra")
        self.assertEqual(manifest["version"], "0.1.0")

    def test_skill_frontmatter(self):
        text = (ROOT / "SKILL.md").read_text()
        self.assertTrue(text.startswith("---\n"))
        self.assertIn("\nname: cs-infra\n", text)
        self.assertIn("description:", text)

    def test_references_exist(self):
        for name in ("checklist.md", "rust-api.md", "sources.md"):
            self.assertTrue((ROOT / "references" / name).is_file(), name)

    def test_checklist_sections(self):
        text = (ROOT / "references" / "checklist.md").read_text()
        for section in ("## A.", "## B.", "## C.", "## D.", "## E.", "## F.", "## G.", "## H.", "## I.", "## J.", "## K."):
            self.assertIn(section, text)

    def test_bilingual_readmes(self):
        en = (ROOT / "README.md").read_text()
        zh = (ROOT / "docs" / "README.zh-CN.md").read_text()
        self.assertIn("docs/README.zh-CN.md", en)
        self.assertIn("../README.md", zh)
        self.assertIn("## License", en)
        self.assertIn("## License", zh)

    def test_trigger_cases(self):
        cases = json.loads((ROOT / "evals" / "trigger_cases.json").read_text())
        self.assertTrue(cases["should_trigger"])
        self.assertTrue(cases["should_not_trigger"])
        self.assertTrue(cases["near_neighbor"])


if __name__ == "__main__":
    unittest.main()
