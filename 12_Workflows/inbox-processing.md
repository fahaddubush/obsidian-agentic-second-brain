---
type: workflow
workflow_id: inbox-processing
status: active
owner: shared
generated_by: system-setup
machine_generated: true
human_review_required: true
confidence: high
tags: [workflow, inbox]
---

<div class="sb-banner sb-banner-inbox">Capture freely · classify carefully · preserve the original</div>

# Inbox processing

> [!warning] Review boundary
> Inbox captures are human-owned evidence. Agents may propose destinations and derived notes, but must not rewrite, move, or delete captures without explicit approval.

## Purpose
Turn unstructured captures into a reviewable triage plan and useful derived memory without losing provenance.

## Inputs
- Selected notes in `00_Inbox/`.
- Optional project, source, and taxonomy context.
- A processing date and explicit scope.

## Outputs
- A triage report in `08_Machine/Reports/` listing each capture and proposed action.
- Optional summaries in `08_Machine/Summaries/` and link suggestions in `08_Machine/Link-Suggestions/`.
- Human-approved follow-up tasks in `02_Working-Memory/`.

## Allowed folders
- Read: `00_Inbox/`, relevant `03_Projects/`, `04_Knowledge/`, `07_Sources/`, and `10_Meta/`.
- Write: `08_Machine/Reports/`, `08_Machine/Summaries/`, `08_Machine/Link-Suggestions/`; `02_Working-Memory/` only with approval.

## Forbidden actions
- Filling gaps by inference; missing facts remain `unknown` until evidence is supplied.
- Editing human-owned notes or immutable sources without explicit approval.
- Editing, moving, renaming, or deleting inbox captures without approval.
- Inventing capture dates, authors, destinations, or project relationships.
- Copying secrets into derived notes or treating a suggestion as accepted fact.

## Process
1. Read `10_Meta/agent-core.md`, `vault-rules.md`, `source-policy.md`, and the current tag taxonomy.
2. Record the exact input note list; skip binary, private, or out-of-scope material.
3. For each capture, classify it as task, project, source, concept, event, procedure, reference, or `unknown`.
4. Extract only explicit facts; preserve a link back to the original capture.
5. Detect duplicates and related notes by title, links, and meaning; label all inferred relationships.
6. Propose one action per capture: keep, derive, route, defer, archive candidate, or needs human decision.
7. Create derived machine notes only when they add value, with source links and review-required provenance.
8. Write a triage table with confidence, destination, reason, and any unanswered question.
9. Ask for approval before any operation on the original capture; after approval, record what changed.

## Agent prompts
### Codex
> Read `AGENTS.md`, then process only the named `00_Inbox/` notes. Create a dated triage report; do not modify originals. Mark unknown classifications as unknown and show proposed destinations with evidence.

### Claude
> Read `CLAUDE.md`, then review the selected inbox captures in read-only mode. Produce machine-owned triage and link suggestions, preserving provenance and separating facts from inferences.

### Gemini
> Read `GEMINI.md`, inspect only the supplied inbox scope, and create a reviewable triage report. Do not move or rewrite captures; list questions where evidence is missing.

## Validation checklist
- [ ] Every processed capture links back to its original path.
- [ ] No original capture changed without explicit approval.
- [ ] Each proposal has a destination, reason, confidence, and review status.
- [ ] Unknown data remains `unknown`; no source or relationship was invented.
- [ ] Machine-created notes declare provenance and require human review.
