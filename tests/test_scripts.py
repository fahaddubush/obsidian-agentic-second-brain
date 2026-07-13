from __future__ import annotations

import argparse
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import sb  # noqa: E402
from vaultlib import atomic_create, confined, sha256, vault_root  # noqa: E402


class VaultHelpersTest(unittest.TestCase):
    def test_runtime_directories_do_not_require_readmes(self) -> None:
        self.assertFalse(sb.readme_required(Path(".obsidian/themes/Retroma")))
        self.assertFalse(sb.readme_required(Path(".obsidian/plugins/example")))
        self.assertFalse(sb.readme_required(Path(".codex/state")))
        self.assertTrue(sb.readme_required(Path("03_Projects/Real Project")))

    def test_confined_rejects_parent_escape(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            with self.assertRaises(ValueError):
                confined(root, "../outside.md")

    def test_atomic_create_never_clobbers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = atomic_create(root, "nested/note.md", "first")
            with self.assertRaises(FileExistsError):
                atomic_create(root, "nested/note.md", "second")
            self.assertEqual(path.read_text(encoding="utf-8"), "first")

    def test_vault_root_rejects_missing_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "missing"
            with self.assertRaises(ValueError):
                vault_root(missing)


class CommandsTest(unittest.TestCase):
    def test_daily_creates_two_notes_and_then_refuses_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            args = argparse.Namespace(vault=str(root), date="2026-07-13", missing_only=False)
            self.assertEqual(sb.command_daily(args), 0)
            daily = root / "01_Daily" / "2026-07-13.md"
            working = root / "02_Working-Memory" / "2026-07-13 - Working Memory.md"
            self.assertTrue(daily.is_file())
            self.assertTrue(working.is_file())
            original = sha256(daily)
            with self.assertRaises(FileExistsError):
                sb.command_daily(args)
            self.assertEqual(sha256(daily), original)

    def test_daily_missing_only_fills_gap_without_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            daily = root / "01_Daily" / "2026-07-13.md"
            daily.parent.mkdir(parents=True)
            daily.write_text("human text", encoding="utf-8")
            args = argparse.Namespace(vault=str(root), date="2026-07-13", missing_only=True)
            self.assertEqual(sb.command_daily(args), 0)
            self.assertEqual(daily.read_text(encoding="utf-8"), "human text")
            self.assertTrue((root / "02_Working-Memory" / "2026-07-13 - Working Memory.md").exists())

    def test_project_inventory_ignores_dependency_and_git_folders(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "package.json").write_text("{}", encoding="utf-8")
            (project / "index.js").write_text("", encoding="utf-8")
            (project / "node_modules").mkdir()
            (project / "node_modules" / "ignored.js").write_text("", encoding="utf-8")
            (project / ".git").mkdir()
            (project / ".git" / "config").write_text("secret", encoding="utf-8")
            files, stacks, entrypoints = sb.project_inventory(project)
            self.assertNotIn("node_modules/ignored.js", files)
            self.assertNotIn(".git/config", files)
            self.assertIn("Node.js/JavaScript", stacks)
            self.assertIn("index.js", entrypoints)

    def test_session_scaffold_updates_index_without_inventing_details(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            index = root / "05_Episodic-Memory" / "LLM-Sessions" / "index.md"
            index.parent.mkdir(parents=True)
            index.write_text("# Sessions\n", encoding="utf-8")
            args = argparse.Namespace(
                vault=str(root),
                date="2026-07-13",
                title="Test Session",
                agent="Codex",
                model=None,
                project=None,
            )
            self.assertEqual(sb.command_session(args), 0)
            note = root / "05_Episodic-Memory" / "LLM-Sessions" / "Codex" / "2026" / "2026-07-13 - Test Session.md"
            self.assertTrue(note.exists())
            self.assertIn("unknown", note.read_text(encoding="utf-8"))
            self.assertIn("Test Session", index.read_text(encoding="utf-8"))

    def test_graph_findings_reports_broken_link(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            atomic_create(root, "A.md", "# A\n\n[[Missing]]\n")
            atomic_create(root, "B.md", "# B\n")
            findings = sb.graph_findings(root)
            self.assertEqual(findings["broken"][0]["target"], "Missing")
            self.assertIn("B.md", findings["orphans"])

    def test_render_yaml_includes_machine_provenance(self) -> None:
        rendered = sb.render_yaml("test", "A title", extra={"agent": "Codex"})
        self.assertIn("generated_by: second-brain-cli", rendered)
        self.assertIn("human_review_required: true", rendered)
        self.assertIn('agent: "Codex"', rendered)


if __name__ == "__main__":
    unittest.main()
