---
type: workflow
workflow_id: context-pack-refresh
status: active
owner: shared
generated_by: system-setup
machine_generated: true
human_review_required: true
confidence: high
tags: [workflow, context-pack, memory]
---

<div class="sb-banner sb-banner-memory">Refresh from authoritative notes · retain the provenance chain</div>

# Context-pack refresh

> [!warning] Compression can hide disagreement
> Never resolve conflicting sources silently. Surface contradictions and retain links to the full notes.

## Purpose
Update a reusable context pack to a known date/revision while keeping it compact, sourced, and honest about uncertainty.

## Inputs
- Existing context pack, project/area scope, last-updated boundary, authoritative project/decision/session notes, and optional repository revision.

## Outputs
- Refreshed file in `08_Machine/Context-Packs/` or a replacement draft for review.
- Optional contradiction/staleness reports and downstream brief-refresh queue.

## Allowed folders
- Read: relevant project, episodic, knowledge, source, and machine notes after the previous source boundary.
- Write: `08_Machine/Context-Packs/`, `Contradictions/`, and `Reports/`.

## Forbidden actions
- Filling gaps by inference; missing facts remain `unknown` until evidence is supplied.
- Editing human-owned notes or immutable sources without explicit approval.
- Using the old pack as sole authority, deleting unresolved context, or overwriting human notes.
- Claiming “current” without a date/revision and inspected source list.
- Expanding the pack into a full project encyclopedia.

## Process
1. Record current date/timezone, repository revision if applicable, old pack version, and refresh reason.
2. Validate every old key claim against current authoritative notes; classify retain, update, remove-as-obsolete, or unresolved.
3. Read new decisions, session summaries, project changes, known issues, and next actions since the prior boundary.
4. Reconcile conflicts by reporting them, not choosing silently; reflect unresolved alternatives in the pack.
5. Rewrite the compressed summary, current state, decisions, files, commands, issues, and actions for the intended use case.
6. Preserve links to full notes and enumerate source session summaries used.
7. Set confidence and review status from source coverage; set freshness/valid-through honestly.
8. Compare size and utility with the old pack, then queue dependent briefs that are now stale.

## Agent prompts
### Codex
> Read `AGENTS.md`; refresh `<context pack>` through `<date/revision>` from authoritative project and session notes. Preserve unresolved conflicts and list every source used.

### Claude
> Read `CLAUDE.md`; validate the existing pack claim by claim, then produce a concise replacement draft with freshness, confidence, and full-note links.

### Gemini
> Read `GEMINI.md`; update the named context pack from changes after its last boundary. Do not treat the previous pack as authority or hide missing coverage.

## Validation checklist
- [ ] Refresh date/revision, old boundary, scope, and source list are explicit.
- [ ] Old claims were checked against current authoritative evidence.
- [ ] Contradictions/unknowns remain visible.
- [ ] Pack retains all required fields while staying materially compressed.
- [ ] Stale dependent briefs are identified, not silently left current.
