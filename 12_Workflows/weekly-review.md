---
type: workflow
workflow_id: weekly-review
status: active
owner: shared
generated_by: system-setup
machine_generated: true
human_review_required: true
confidence: high
tags: [workflow, review, weekly]
---

<div class="sb-banner sb-banner-review">See the week whole · promote lessons · choose deliberately</div>

# Weekly review

> [!note] Draft, then decide
> Agents assemble evidence and patterns; the human confirms priorities, project status, and archival decisions.

## Purpose
Consolidate one week of activity into verified outcomes, durable lessons, project health, and next-week focus.

## Inputs
- Daily notes and work/LLM sessions for an explicit seven-day period.
- Active projects, inbox state, decision notes, and machine-review backlog.

## Outputs
- A weekly review note in `05_Episodic-Memory/Timeline/` or another meta-approved review location.
- Review suggestions in `08_Machine/Reports/` and refreshed briefs where justified.

## Allowed folders
- Read: `00_Inbox/` through `08_Machine/` within the date/scope boundary, plus `10_Meta/`.
- Write: new review/episodic notes and machine outputs; shared/project notes only after approval.

## Forbidden actions
- Filling gaps by inference; missing facts remain `unknown` until evidence is supplied.
- Editing human-owned notes or immutable sources without explicit approval.
- Bulk-editing or archiving notes based only on age.
- Treating machine reports as verified evidence.
- Inventing a week’s goals or conclusions where daily/session coverage is incomplete.

## Process
1. State the period, timezone, included notes, and known coverage gaps.
2. Summarize verified outcomes, blockers, decisions, and unfinished commitments by project/area.
3. Review inbox backlog and machine-generated notes; propose disposition, do not enact it automatically.
4. Identify repeated lessons suitable for evergreen or procedural memory, with source links.
5. Check working-memory freshness and context-pack freshness; report stale candidates with reasons.
6. Surface contradictions and unresolved decisions as review items.
7. Draft next-week outcomes, risks, and a first action based on explicit active goals.
8. Have the human confirm changes before updating project status or shared knowledge.

## Agent prompts
### Codex
> Read `AGENTS.md`; review the specified week and draft a source-linked weekly review. Do not archive or change project status. Separate verified outcomes, inferred patterns, and missing coverage.

### Claude
> Read `CLAUDE.md`; synthesize the week’s daily and session evidence into outcomes, blockers, lessons, and proposed next-week focus. Keep all machine recommendations reviewable.

### Gemini
> Read `GEMINI.md`; run the weekly review for the named dates, cite the consulted notes, identify stale-context candidates, and label unsupported conclusions unknown.

## Validation checklist
- [ ] Period and evidence coverage are explicit.
- [ ] Facts, inferences, and proposals are distinguishable.
- [ ] No archival, status, or priority change occurred without approval.
- [ ] Durable lessons link to episodes that support them.
- [ ] Next-week proposals are concise and human-reviewed.
