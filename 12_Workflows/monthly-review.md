---
type: workflow
workflow_id: monthly-review
status: active
owner: shared
generated_by: system-setup
machine_generated: true
human_review_required: true
confidence: high
tags: [workflow, review, monthly]
---

<div class="sb-banner sb-banner-review">Measure change · strengthen memory · prune by consent</div>

# Monthly review

> [!warning] Strategic choices remain human
> Agents may show trends and candidates; they may not close projects, delete notes, or redefine goals autonomously.

## Purpose
Assess a calendar month across projects and areas, promote mature learning, and evaluate second-brain health.

## Inputs
- Weekly reviews, daily/session coverage, project notes, decisions, machine outputs, and previous monthly goals.
- Explicit month, timezone, and exclusions.

## Outputs
- A monthly review note in `05_Episodic-Memory/Timeline/`.
- Optional synthesis, contradiction, or maintenance reports under `08_Machine/`.

## Allowed folders
- Read: relevant dated notes across `01_Daily/`–`08_Machine/` and policies in `10_Meta/`.
- Write: new timeline and machine notes; no changes to human/project state without approval.

## Forbidden actions
- Filling gaps by inference; missing facts remain `unknown` until evidence is supplied.
- Editing human-owned notes or immutable sources without explicit approval.
- Inferring performance from note volume alone.
- Treating missing records as evidence that no work occurred.
- Auto-archiving, deleting, or merging notes.

## Process
1. Confirm month boundaries and inventory available weekly reviews and missing periods.
2. Compare explicit monthly goals with verified outcomes and link evidence.
3. Summarize project movement, important decisions, recurring blockers, and paused work.
4. Identify concepts/procedures that matured and propose evergreen updates separately.
5. Analyze cross-week patterns, clearly labeling inference and confidence.
6. Audit machine-review backlog, instruction drift status, context freshness, and source integrity.
7. Propose projects to continue, pause, audit, or archive; require human decisions.
8. Draft next-month priorities, stop-doing candidates, risks, and bounded experiments.

## Agent prompts
### Codex
> Read `AGENTS.md`; create a review-required monthly synthesis for the named month from weekly reviews and project evidence. Identify coverage gaps and do not change project status.

### Claude
> Read `CLAUDE.md`; compare explicit goals with sourced outcomes, extract cross-week lessons, and propose next-month priorities while keeping strategic decisions human-owned.

### Gemini
> Read `GEMINI.md`; draft the monthly review and system-health checks. Mark missing periods unknown and place all cleanup or archival ideas in a machine report.

## Validation checklist
- [ ] Month, timezone, exclusions, and missing coverage are stated.
- [ ] Outcomes link to evidence; absence of notes was not treated as failure.
- [ ] Trends carry confidence and are labeled as inference.
- [ ] No strategic or destructive change was made automatically.
- [ ] System-health findings are reviewable and actionable.
