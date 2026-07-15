from __future__ import annotations

import argparse
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import sb  # noqa: E402
import install_global_codex  # noqa: E402
import brain_runtime  # noqa: E402
from vaultlib import atomic_create, confined, sha256, vault_root  # noqa: E402


class VaultHelpersTest(unittest.TestCase):
    def test_runtime_directories_do_not_require_readmes(self) -> None:
        self.assertFalse(sb.readme_required(Path(".github")))
        self.assertFalse(sb.readme_required(Path(".github/workflows")))
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
    def test_source_integrity_fails_when_a_source_is_unmanifested(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "07_Sources" / "Transcripts" / "new.md"
            source.parent.mkdir(parents=True)
            source.write_text("private source", encoding="utf-8")
            manifest = root / ".codex" / "state" / "source-integrity.json"
            manifest.parent.mkdir(parents=True)
            manifest.write_text('{"files": {}}\n', encoding="utf-8")
            args = argparse.Namespace(vault=str(root), write=False)
            self.assertEqual(sb.command_sources(args), 1)

    def test_private_runtime_is_idempotent_and_claims_jobs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "brain.db"
            payload = {
                "session_id": "session-1",
                "turn_id": "turn-1",
                "cwd": str(Path(directory) / "project"),
                "hook_event_name": "Stop",
                "last_assistant_message": "Implemented the verified change.",
            }
            first = brain_runtime.record_hook_event(payload, "stop", enqueue=True, path=database)
            second = brain_runtime.record_hook_event(payload, "stop", enqueue=True, path=database)
            self.assertEqual(first, second)
            with brain_runtime.database(database) as connection:
                self.assertEqual(connection.execute("SELECT COUNT(*) FROM events").fetchone()[0], 1)
                self.assertEqual(connection.execute("SELECT COUNT(*) FROM jobs").fetchone()[0], 1)
            claimed = brain_runtime.claim_jobs(path=database)
            self.assertEqual(len(claimed), 1)
            self.assertEqual(claimed[0]["id"], first["job_id"])
            self.assertEqual(claimed[0]["events"][0]["content"]["assistant_message"], "Implemented the verified change.")

    def test_private_runtime_retrieves_ranked_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            note = root / "03_Projects" / "Demo" / "architecture.md"
            note.parent.mkdir(parents=True)
            note.write_text("# Demo architecture\n\nThe system uses a temporal event journal and receipt validation.\n", encoding="utf-8")
            database = root / "runtime" / "brain.db"
            results = brain_runtime.search_memory("temporal event journal", path=database, root=root)
            self.assertEqual(results[0]["path"], "03_Projects/Demo/architecture.md")

    def test_reconciliation_worker_does_not_enqueue_itself(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "brain.db"
            prompt = {
                "session_id": "worker-session",
                "turn_id": "turn-1",
                "cwd": str(Path(directory) / "project"),
                "prompt": f"{brain_runtime.MAINTENANCE_MARKER} Process pending jobs.",
            }
            stop = {
                "session_id": "worker-session",
                "turn_id": "turn-1",
                "cwd": str(Path(directory) / "project"),
                "last_assistant_message": "Reconciled the batch.",
            }
            brain_runtime.record_hook_event(prompt, "user_prompt", path=database)
            receipt = brain_runtime.record_hook_event(stop, "stop", enqueue=True, path=database)
            self.assertIsNone(receipt["job_id"])
            with brain_runtime.database(database) as connection:
                self.assertEqual(connection.execute("SELECT COUNT(*) FROM jobs").fetchone()[0], 0)

    def test_global_codex_installer_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            (home / "config.toml").write_text("[features]\njs_repl = false\n", encoding="utf-8")
            (home / "AGENTS.md").write_text("# Existing guidance\n", encoding="utf-8")
            install_global_codex.install(home)
            install_global_codex.install(home)
            self.assertEqual(install_global_codex.check(home), [])
            hooks = json.loads((home / "hooks.json").read_text(encoding="utf-8"))
            for event in install_global_codex.desired_groups():
                groups = hooks["hooks"][event]
                self.assertEqual(sum(install_global_codex.is_ours(group) for group in groups), 1)
            self.assertEqual((home / "AGENTS.md").read_text(encoding="utf-8").count(install_global_codex.BLOCK_START), 1)

    def test_empty_level_two_headings_ignores_populated_sections(self) -> None:
        text = "# Note\n\n## Empty\n\n## Parent\n\n### Child\n\nUseful detail.\n"
        self.assertEqual(sb.empty_level_two_headings(text), ["Empty"])

    def test_ingestion_audit_reconciles_manifest_and_required_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "03_Projects" / "Demo"
            for relative in sb.PROJECT_MEMORY_FILES:
                path = project / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                body = "# Demo\n"
                if path.name != "README.md" and "audits" not in path.parts and "machine-summaries" not in path.parts:
                    body += "\n## Evidence\n\n- [[Session]]\n"
                path.write_text(body, encoding="utf-8")
            session = root / "05_Episodic-Memory" / "LLM-Sessions" / "Codex" / "2026" / "Session.md"
            session.parent.mkdir(parents=True)
            session.write_text(
                "---\ntype: llm-session-summary\ntitle: Session\nstatus: complete\n"
                "generated_by: Codex\nconfidence: high\nhuman_review_required: true\n"
                "agent: Codex\nproject: Demo\nsession_id: task-1\n---\n\n# Session\n\n## Outcome\n\nCompleted.\n",
                encoding="utf-8",
            )
            outputs = {
                "source_catalog": "07_Sources/Transcripts/Catalog.md",
                "working_memory": "02_Working-Memory/Working.md",
                "procedure": "06_Procedural-Memory/Procedure.md",
                "ingestion_report": "08_Machine/Reports/Report.md",
                "private_index": "05_Episodic-Memory/LLM-Sessions/private-index.md",
            }
            contents = {
                outputs["source_catalog"]: "# Catalog\n\n| Task | ID | Turns |\n|---|---|---:|\n| Demo | `task-1` | 2 |\n",
                outputs["working_memory"]: "# Working\n",
                outputs["procedure"]: "# Procedure\n",
                outputs["ingestion_report"]: "# Report\n\nTasks: 1\nTurns: 2\n",
                outputs["private_index"]: "# Private sessions\n\n- [[Session]]\n",
                "08_Machine/Context-Packs/demo.md": "# Pack\n\n## Purpose\n\nResume.\n\n## Compressed summary\n\nState.\n\n## Next action\n\n- Continue.\n\n## Expansion\n\n- [[Session]]\n",
                "08_Machine/Token-Saving-Briefs/demo-continuation.md": "# Brief\n\n## Objective\n\nContinue.\n\n## Essential state\n\n- State.\n\n## Expand only if needed\n\n- [[Session]]\n",
            }
            for relative, content in contents.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            manifest = {
                "expected_task_count": 1,
                "expected_turn_count": 2,
                **outputs,
                "projects": [{
                    "name": "Demo", "memory_dir": "03_Projects/Demo", "slug": "demo",
                    "tasks": [{"id": "task-1", "turns": 2, "session_note": session.relative_to(root).as_posix()}],
                }],
            }
            self.assertEqual(sb.ingestion_findings(root, manifest)["errors"], [])
            manifest["expected_turn_count"] = 3
            self.assertTrue(any("turn reconciliation failed" in item for item in sb.ingestion_findings(root, manifest)["errors"]))

    def test_hooks_check_accepts_complete_project_configuration(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            codex = root / ".codex"
            (codex / "hooks").mkdir(parents=True)
            (codex / "config.toml").write_text("[features]\nhooks = true\n", encoding="utf-8")
            events = {name: [] for name in ("SessionStart", "UserPromptSubmit", "PreToolUse", "PostToolUse", "Stop")}
            (codex / "hooks.json").write_text(json.dumps({"hooks": events}), encoding="utf-8")
            (codex / "hooks" / "codex_hook.py").write_text("# handler\n", encoding="utf-8")
            args = argparse.Namespace(vault=str(root), project_root=str(root))
            self.assertEqual(sb.command_hooks_check(args), 0)

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
