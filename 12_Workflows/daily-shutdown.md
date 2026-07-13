---
type: workflow
workflow_id: daily-shutdown
status: active
owner: shared
generated_by: system-setup
machine_generated: true
human_review_required: true
confidence: high
tags: [workflow, daily]
---

<div class="sb-banner sb-banner-daily">Close loops · record evidence · make tomorrow easy</div>

# Daily shutdown

> [!warning] No invented progress
> Completion, blockers, and decisions must come from today’s notes, diffs, session summaries, or explicit human input.

## Purpose
Capture today’s verified outcomes, preserve unresolved context, and prepare a clean handoff for the next session.

## Inputs
- Today’s daily note and working-memory notes.
- Today’s work/LLM sessions, project changes, and explicit human corrections.

## Outputs
- A reviewed end-of-day section in `01_Daily/` or a proposed update in `08_Machine/Reports/`.
- Session summaries in `05_Episodic-Memory/` where missing.
- Optional brief/context-pack refreshes under `08_Machine/`.

## Allowed folders
- Read: today’s `01_Daily/`, `02_Working-Memory/`, relevant `03_Projects/`, and recent `05_Episodic-Memory/`.
- Write: new episodic notes and machine outputs; existing daily/project notes only with approval.

## Forbidden actions
- Filling gaps by inference; missing facts remain `unknown` until evidence is supplied.
- Editing human-owned notes or immutable sources without explicit approval.
- Marking tasks complete without evidence.
- Deleting temporary notes or carrying private data into machine summaries.
- Rewriting project state or human reflection without approval.

## Process
1. Establish the day’s exact scope and list notes/sessions reviewed.
2. Compare morning outcomes with evidence of work; record completed, partial, blocked, deferred, or unknown.
3. Extract decisions and notable events into episodic memory when they deserve durable context.
4. Create any missing meaningful LLM session summaries via `llm-session-summary.md`.
5. List unresolved issues with the smallest executable next action and necessary context.
6. Draft the end-of-day reflection and carry-forward list; keep subjective reflection for the human.
7. Close or mark working-memory notes stale only after approval; otherwise report candidates.
8. Refresh a brief only if the underlying state materially changed, preserving source links.

## Agent prompts
### Codex
> Read `AGENTS.md` and summarize today from supplied notes and repository evidence. Draft a shutdown report, create missing session memory, and leave human/project notes unchanged unless I approve edits.

### Claude
> Read `CLAUDE.md`; reconcile today’s intended outcomes with verifiable work. Record unresolved context and propose tomorrow’s first action without inventing completion.

### Gemini
> Read `GEMINI.md`; produce a review-required daily shutdown using today’s note, sessions, and named project evidence. Label gaps unknown and suggest any brief refresh.

## Validation checklist
- [ ] Outcomes are supported by explicit evidence.
- [ ] Unresolved work has owner/status/next action or is marked unknown.
- [ ] Meaningful LLM sessions have traceable summaries.
- [ ] No human reflection or source content was overwritten.
- [ ] Refreshed machine context cites current source notes.
