---
type: context-pack
title: "Active Projects"
purpose: "Route an agent to current project state"
last_updated: 2026-07-13
stale_after: unknown
ownership: machine
status: seed
generated_by: setup
confidence: low
human_review_required: true
source_session_summaries: []
---

<div class="sb-card sb-project"><strong>ACTIVE PROJECTS</strong><br>Routing pack · replace seeds with verified project state.</div>

# Active Projects

## When to use

At the start of project work when no more specific brief is available.

## Compressed summary

- [[03_Projects/Example Project/README|Example Project]] is fictional setup content.
- Real active projects: unknown.

## Current state

No real project has been ingested.

## Key decisions

- External projects are read-only unless the user explicitly requests modification.

## Important files and commands

- [[12_Workflows/project-ingestion]]
- `python scripts/sb.py project-ingest <path>`

## Known issues

- Project list is a seed and may be stale.

## Next actions

- [ ] Ingest the first real project.
- [ ] Replace this seed with verified state.
