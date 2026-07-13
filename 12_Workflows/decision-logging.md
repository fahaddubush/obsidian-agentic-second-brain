---
type: workflow
workflow_id: decision-logging
status: active
owner: shared
generated_by: system-setup
machine_generated: true
human_review_required: true
confidence: high
tags: [workflow, decision]
---

<div class="sb-banner sb-banner-decision">Preserve the why · distinguish proposed from accepted</div>

# Decision logging

> [!note] Authority matters
> An agent may extract or draft a decision, but only an identified human or authoritative record can mark it accepted.

## Purpose
Record durable decisions with context, alternatives, evidence, consequences, and supersession history.

## Inputs
- Explicit decision statement or a named session/diff/document that contains it.
- Project, participants/deciders, date, constraints, and available alternatives.

## Outputs
- Decision note in `05_Episodic-Memory/Decisions/`.
- A link or proposed update in the related `03_Projects/<project>/decisions.md`.

## Allowed folders
- Read: named evidence in project, episodic, source, and machine folders.
- Write: `05_Episodic-Memory/Decisions/`; project index only with approval.

## Forbidden actions
- Filling gaps by inference; missing facts remain `unknown` until evidence is supplied.
- Editing human-owned notes or immutable sources without explicit approval.
- Converting a recommendation, discussion, or agent choice into an accepted human decision.
- Inventing deciders, dates, alternatives, rationale, or approval status.
- Rewriting or deleting superseded decision notes.

## Process
1. Identify the authoritative statement and whether status is proposed, accepted, rejected, superseded, or unknown.
2. Record exact date/deciders only when present; otherwise use `unknown`.
3. Summarize the context and constraints with links to source evidence.
4. Capture the chosen option and materially considered alternatives without reconstructing missing debate.
5. Record consequences, reversibility, risks, and follow-up checks.
6. Link related and superseded decisions bidirectionally without erasing history.
7. Create the decision note with human review if any field was inferred.
8. Propose updates to architecture/context/tasks when the decision changes them.

## Agent prompts
### Codex
> Read `AGENTS.md`; extract the decision from `<evidence>`. Create a decision note with status, rationale, alternatives, consequences, and source links. Do not mark it accepted unless the record explicitly does.

### Claude
> Read `CLAUDE.md`; log the named decision and preserve uncertainty about participants or rationale. Link superseded decisions without editing their history.

### Gemini
> Read `GEMINI.md`; draft a review-required decision record from supplied evidence. Separate the actual decision from agent recommendations and unknown discussion details.

## Validation checklist
- [ ] Status and authority are explicit and evidence-backed.
- [ ] Date/deciders/rationale are known or marked `unknown`.
- [ ] Alternatives and consequences are not invented.
- [ ] Supersession preserves prior history.
- [ ] Project update suggestions remain reviewable.
