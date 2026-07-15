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

## 2026-07-15

- Added a machine-readable ingestion-manifest template and the `ingestion-audit` quality gate.
- Added exact task and turn reconciliation, complete project-schema checks, session provenance checks, evidence-link checks, compressed-memory checks, empty-section and placeholder detection, secret and style scanning, and local-only Git privacy validation.
- Added the full Codex task-ingestion workflow and updated hook routing to select it for complete history requests.
- Added `hooks-check` diagnostics and documented active-project-root discovery requirements.
- Added a local parent-project adapter so Codex tasks opened from `Project #3` can discover the nested second-brain lifecycle hooks.
- Kept the full pre-tool safety guard limited to tasks opened directly from the `second-brain` project root.
- Added a private SQLite evidence journal, durable reconciliation queue, ranked Markdown retrieval, receipts, retry handling, lease recovery, and rebuildable indexes.
- Added and globally installed the `agentic-second-brain` skill plus bounded researcher, curator, and verifier roles.
- Enabled native Codex memories and bounded multi-agent settings in the user configuration.
- Replaced the repeated global Stop closeout design with idempotent event capture and an hourly local reconciliation worker.
- Added the incremental agentic-memory workflow and kept full task-history ingestion as a distinct explicit backfill workflow.
- Removed obsolete global closeout state, documented workflow boundaries, and confirmed there are no exact duplicate scripts or workflows.
- Moved the live source-integrity manifest out of the public Git surface while retaining a safe example.
