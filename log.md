---
title: Vault Change Log
type: log
cssclasses: [second-brain]
---

# Vault Change Log

Record material schema, policy, tooling, and structural changes here. Routine note edits belong in Git history or the note’s own history.

## 2026-07-13

- Created the initial agentic second-brain structure, governance layer, adapters, workflows, templates, and visual presentation layer.
- Established `10_Meta/agent-core.md` as the canonical shared instruction source.
- Chose a conservative baseline: Markdown, Obsidian core features, Git, and direct filesystem access; optional agent/search layers remain opt-in.
- Added a portable HTML/CSS presentation layer with dashboards, cards, banners, semantic memory colors, and token-brief badges; Markdown remains the durable layer.
- Added dependency-free validation, instruction-sync, daily/session, graph, source-integrity, project-ingestion, and Git-review commands plus tests.
- Added all required examples, project memory, context packs, briefs, current-year session folders, and the LLM session index.
- Initialized a local Git repository on branch `main`; no remote, hook, scheduler, plugin, or autonomous writer was installed.
- Added reviewed project-local Codex lifecycle hooks for startup context, workflow routing, safety guardrails, dirty tracking, subagent context, and stop-time validation. Calendar schedules and Git hooks remain unconfigured.
