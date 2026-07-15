from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


HOOK_PATH = Path(__file__).resolve().parents[1] / ".codex" / "hooks" / "codex_hook.py"
SPEC = importlib.util.spec_from_file_location("second_brain_codex_hook", HOOK_PATH)
assert SPEC and SPEC.loader
hook = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(hook)


class CodexHooksTest(unittest.TestCase):
    def test_routes_required_workflows(self) -> None:
        self.assertIn("project-ingestion", hook.matched_workflows("Ingest this project without modifying it"))
        self.assertIn("llm-session-summary", hook.matched_workflows("Summarize this LLM session into memory"))
        self.assertIn("dreaming-nightly-synthesis", hook.matched_workflows("Run dreaming synthesis on the last 7 days"))
        full_ingestion = hook.matched_workflows("Ingest all available Codex tasks and chat history")
        self.assertIn("full-codex-task-ingestion", full_ingestion)
        self.assertIn("llm-session-summary", full_ingestion)
        self.assertIn("transcript-ingestion", full_ingestion)

    def test_blocks_secret_like_prompts(self) -> None:
        synthetic_key = "sk-" + ("a" * 22)
        self.assertIsNotNone(hook.prompt_secret_reason(f"my key is {synthetic_key}"))
        self.assertIsNone(hook.prompt_secret_reason("document how API keys should be protected"))

    def test_windows_commands_are_repository_portable(self) -> None:
        hook_config = json.loads((HOOK_PATH.parents[1] / "hooks.json").read_text(encoding="utf-8"))
        serialized = json.dumps(hook_config)
        personal_path_prefix = "C:" + "/Users/"
        self.assertNotIn(personal_path_prefix, serialized)
        for groups in hook_config["hooks"].values():
            for group in groups:
                for handler in group["hooks"]:
                    self.assertIn("git rev-parse --show-toplevel", handler["commandWindows"])

    def test_blocks_high_risk_shell_commands(self) -> None:
        self.assertIsNotNone(hook.destructive_reason("Bash", "git reset --hard HEAD~1"))
        self.assertIsNotNone(hook.destructive_reason("Bash", "Remove-Item -Recurse -Force .\\notes"))
        self.assertIsNone(hook.destructive_reason("Bash", "git status --short"))

    def test_protects_immutable_sources(self) -> None:
        patch = "*** Begin Patch\n*** Update File: 07_Sources/Articles/source.md\n@@\n-old\n+new\n*** End Patch"
        self.assertIsNotNone(hook.destructive_reason("apply_patch", patch))
        add = "*** Begin Patch\n*** Add File: 07_Sources/Articles/new-source.md\n+source\n*** End Patch"
        self.assertIsNone(hook.destructive_reason("apply_patch", add))

    def test_global_handler_uses_private_runtime(self) -> None:
        self.assertTrue(callable(hook.brain_runtime.record_hook_event))
        self.assertTrue(callable(hook.brain_runtime.search_memory))


if __name__ == "__main__":
    unittest.main()
