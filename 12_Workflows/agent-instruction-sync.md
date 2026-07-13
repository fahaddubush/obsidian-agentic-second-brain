---
type: workflow
workflow_id: agent-instruction-sync
status: active
owner: shared
generated_by: system-setup
machine_generated: true
human_review_required: true
confidence: high
tags: [workflow, agents, instructions]
---

<div class="sb-banner sb-banner-meta">One canonical core · thin adapters · drift made visible</div>

# Agent instruction synchronization

> [!danger] Rules affect every future agent
> Shared-rule changes require explicit human approval. Update `10_Meta/agent-core.md` first, then synchronize adapters without erasing agent-specific guidance.

## Purpose
Detect and safely resolve drift among the canonical rules and Codex, Claude Code, and Gemini CLI adapters.

## Inputs
- `10_Meta/agent-core.md`, root `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, and the proposed rule change or audit-only request.

## Outputs
- Drift report in `08_Machine/Reports/`.
- If explicitly approved: synchronized edits to the canonical file and three adapters.

## Allowed folders
- Read: the four instruction files and referenced `10_Meta/` policies.
- Write: `08_Machine/Reports/`; the four instruction files only with explicit approval for the described changes.

## Forbidden actions
- Filling gaps by inference; missing facts remain `unknown` until evidence is supplied.
- Editing human-owned notes or immutable sources without explicit approval.
- Changing shared policy in only one adapter.
- Copying adapter-specific details into the canonical core or deleting agent-specific guidance.
- Weakening safety rules, changing authority boundaries, or auto-syncing on a schedule without review.

## Process
1. Determine mode: audit-only or approved synchronization. Default to audit-only.
2. Parse the canonical shared-rule topics: purpose, folders, ownership, allowed/forbidden actions, YAML, naming, ingestion, sessions, sources, links/tags, review, safety, and validation.
3. Map each core topic to its mirrored/linked section in all three adapters.
4. Report missing, contradictory, stale, or agent-specific differences; distinguish harmless wording from behavioral drift.
5. For a shared rule change, draft the canonical `agent-core.md` change first and show its impact.
6. After approval, update all adapters in the same change set while preserving Codex-, Claude-, and Gemini-specific sections.
7. Re-run the semantic comparison and verify all canonical references/relative links.
8. Record files changed, date, reason, approver, and any intentional exceptions in a drift report.

## Agent prompts
### Codex
> Read `AGENTS.md`; audit `10_Meta/agent-core.md`, `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` for behavioral drift. Create a report only; do not synchronize until I approve the exact changes.

### Claude
> Read `CLAUDE.md`; compare all four instruction files against the canonical core. Separate shared-rule drift from valid adapter-specific guidance and propose one synchronized patch.

### Gemini
> Read `GEMINI.md`; check canonical coverage and contradictions across all adapters. Default to audit-only and preserve each tool’s specific notes.

## Validation checklist
- [ ] Mode and approval scope are explicit.
- [ ] All canonical rule topics were mapped across all three adapters.
- [ ] Shared changes start in `agent-core.md` and appear consistently in every adapter.
- [ ] Agent-specific sections are preserved and clearly separated.
- [ ] Post-change comparison, links, provenance, and change log were verified.
