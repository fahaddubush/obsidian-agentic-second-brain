---
title: Codex Hook Integration Validation
type: validation-report
date: 2026-07-13
status: passed
ownership: machine
generated_by: Codex
confidence: high
human_review_required: true
---

# Codex Hook Integration Validation

## Outcome

The project-local integration under `.codex/` matches the current Codex hook schema and passed local regression and synthetic lifecycle checks. Execution remains pending the required one-time human trust action in Codex.

## Integrated events

- `SessionStart`: creates only missing daily scaffolds, validates the vault, and injects the maintenance brief.
- `SubagentStart`: injects vault safety and workflow context.
- `UserPromptSubmit`: blocks obvious credentials and routes matching requests to reviewed workflows.
- `PreToolUse`: denies selected destructive commands and protected-source mutations.
- `PostToolUse`: records a minimal dirty flag without prompt, transcript, command, or output content.
- `Stop`: validates structure, instruction synchronization, and source integrity after write-capable tools.

## Evidence

- `python scripts/sb.py validate`: 0 errors, 0 warnings.
- `python -m unittest discover -s tests -v`: 16 tests passed.
- `python scripts/sb.py instruction-sync`: adapters match the canonical hash.
- `python scripts/sb.py sources`: 0 changed, 0 added, 0 missing.
- `.codex/hooks.json`: valid JSON and current event/matcher names.
- Synthetic hook payloads: startup context injected, project ingestion routed, secret-like prompt blocked, destructive Git command denied, and stop-time validation passed.

## Activation

Start a new Codex task from the vault root, open Settings → Hooks or `/hooks`, review the project-local definition, and trust it. Any later hook-definition change requires review again.

## Known boundary

`PreToolUse` is a guardrail, not a complete security boundary. `Stop` runs at turn scope rather than on a distinct session-close event. Calendar-based work therefore belongs in separately reviewed Codex scheduled tasks.

## Related

- [[10_Meta/automation-and-hooks]]
- [[08_Machine/Context-Packs/obsidian-second-brain]]
- [[05_Episodic-Memory/LLM-Sessions/Codex/2026/2026-07-13 - Built Agentic Second Brain]]
