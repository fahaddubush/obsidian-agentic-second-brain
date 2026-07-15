---
type: context-pack
title: "Obsidian Second Brain"
purpose: "Maintain this vault safely"
last_updated: 2026-07-15
stale_after: 2026-08-13
ownership: machine
status: seed
generated_by: setup
confidence: high
human_review_required: true
source_session_summaries:
  - "[[05_Episodic-Memory/LLM-Sessions/Codex/2026/2026-07-13 - Built Agentic Second Brain]]"
---

<div class="sb-hero sb-meta"><span class="sb-kicker">VAULT CONTEXT</span><h1>Obsidian Second Brain</h1><p>Safe maintenance context in one screen.</p></div>

# Obsidian Second Brain

## When to use

Before changing vault structure, rules, adapters, templates, workflows, scripts, or visual styling.

## Compressed project summary

A local-first, Markdown-first LLM wiki with immutable sources, protected human notes, machine review outputs, episodic session memory, and compressed future-chat context.

## Current state

- Canonical rules: [[10_Meta/agent-core]]
- Adapters: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`
- Visual layer: `.obsidian/snippets/second-brain.css`
- Automation: project integrity hooks, seven user-level lifecycle hooks, private journal and queue, ranked retrieval, native Codex memories, bounded agents, and hourly reconciliation

## Key decisions

- Markdown is durable; HTML/CSS is optional presentation.
- Start with Obsidian core search and links.
- Use Local REST API/MCP only if live Obsidian control is needed.
- Keep model-driven consolidation asynchronous, receipt-backed, bounded to one delegation level, and unable to overwrite protected notes.

## Important files

- [[README]]
- [[10_Meta/tooling-research]]
- [[10_Meta/validation-checklist]]
- [[12_Workflows/agent-instruction-sync]]

## Common commands

- `python scripts/sb.py validate`
- `python scripts/sb.py instruction-sync`
- `python scripts/brain_runtime.py doctor --repair --json`
- `python scripts/brain_runtime.py search "query" --json`
- `python -m unittest discover -s tests -v`
- In Codex: `/hooks` to review, trust, inspect, or disable project hooks

## Known issues

- Changed hook definitions must be reviewed and trusted again after a Codex restart.
- Ordinary ChatGPT web does not execute local Codex hooks.

## Next actions

- [ ] Review the first scheduled reconciliation receipt.
- [ ] Measure missed retrievals and weak consolidations before tuning thresholds or prompts.
