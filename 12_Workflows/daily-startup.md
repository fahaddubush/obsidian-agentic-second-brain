---
type: workflow
workflow_id: daily-startup
status: active
owner: shared
generated_by: system-setup
machine_generated: true
human_review_required: true
confidence: high
tags: [workflow, daily]
---

<div class="sb-banner sb-banner-daily">Start with evidence · choose a small set of outcomes</div>

# Daily startup

> [!note] Human ownership
> An agent may draft today’s plan, but priorities and commitments become authoritative only after human review.

## Purpose
Create a focused daily note and short-lived working context from current commitments, not from guessed priorities.

## Inputs
- Current date and timezone.
- The latest daily note, active working-memory notes, project tasks, calendar information if supplied, and unresolved session actions.

## Outputs
- Today’s note in `01_Daily/`.
- Optional focused note in `02_Working-Memory/`.
- Optional stale-context suggestions in `08_Machine/Reports/`.

## Allowed folders
- Read: `01_Daily/`, `02_Working-Memory/`, active `03_Projects/`, recent `05_Episodic-Memory/`, and relevant context packs.
- Write: today’s new `01_Daily/` note, a new `02_Working-Memory/` note, and `08_Machine/Reports/`.

## Forbidden actions
- Filling gaps by inference; missing facts remain `unknown` until evidence is supplied.
- Editing human-owned notes or immutable sources without explicit approval.
- Overwriting an existing daily note or changing project priorities without approval.
- Claiming calendar commitments, deadlines, or completed work not present in inputs.
- Loading the entire vault when recent briefs provide sufficient context.

## Process
1. Confirm local date and timezone; if unavailable, record them as unknown rather than guessing.
2. Open the latest relevant token-saving briefs, then context packs only as needed.
3. Read yesterday’s carry-forward items, active working memory, and explicit project next actions.
4. Identify conflicts, stale tasks, and missing evidence; do not silently resolve them.
5. Draft at most three outcome-oriented priorities and distinguish commitments from suggestions.
6. Create today’s daily note from the template, or append a clearly delimited machine suggestion if the note already exists and editing was approved.
7. Create or refresh a focused working-memory note with objective, constraints, open questions, and exit criteria.
8. Link the daily note to the consulted project/session notes and record the source scope.

## Agent prompts
### Codex
> Read `AGENTS.md` and the latest relevant briefs. Draft today’s daily and working-memory notes from explicit open actions only. Preserve any existing daily note and flag conflicts for review.

### Claude
> Read `CLAUDE.md`; prepare a concise startup plan using yesterday’s carry-forward items and active project context. Separate known commitments from proposed priorities.

### Gemini
> Read `GEMINI.md`; create a review-required daily startup draft with no more than three outcomes, source links, constraints, and unknowns. Do not overwrite existing notes.

## Validation checklist
- [ ] Date and timezone are correct or explicitly unknown.
- [ ] Priorities trace to supplied notes or are labeled suggestions.
- [ ] Existing human content was preserved.
- [ ] Working memory has an objective, open questions, next action, and exit criteria.
- [ ] Context loading followed brief → context pack → full notes.
