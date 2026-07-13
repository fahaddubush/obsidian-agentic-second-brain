---
type: workflow
workflow_id: exam-course-study
status: active
owner: shared
generated_by: system-setup
machine_generated: true
human_review_required: true
confidence: high
tags: [workflow, university, study]
---

<div class="sb-banner sb-banner-study">Study from the syllabus · practice recall · expose weak spots</div>

# Exam / course study

> [!note] Course truth comes from supplied materials
> Agents must not invent exam coverage, deadlines, grading rules, or instructor expectations.

## Purpose
Build a source-grounded study plan and active-recall materials while preserving course notes and academic integrity.

## Inputs
- Course/exam name, date if known, syllabus/scope, lectures, readings, assignments, past feedback, and available study time.

## Outputs
- Working study plan in `02_Working-Memory/`.
- Concept/procedure drafts or machine summaries and practice sets under `08_Machine/`.
- Study-session episodes in `05_Episodic-Memory/Work-Sessions/`.

## Allowed folders
- Read: supplied course project/source notes and relevant prior study sessions.
- Write: new working-memory, episodic, and machine notes; existing human course notes only with approval.

## Forbidden actions
- Filling gaps by inference; missing facts remain `unknown` until evidence is supplied.
- Editing human-owned notes or immutable sources without explicit approval.
- Completing prohibited graded work, evading academic rules, or fabricating course requirements.
- Rewriting instructor/source notes or treating agent-generated answers as authoritative.
- Generating a plan that ignores the actual time budget or unknown exam scope.

## Process
1. Confirm exam date, allowed materials, integrity constraints, syllabus topics, and available time; mark unknowns.
2. Inventory source coverage by topic and distinguish required, optional, and inferred material.
3. Diagnose knowledge using recall questions or supplied assessment evidence, not note volume.
4. Rank topics by course weight (if known), weakness, prerequisites, and remaining time.
5. Create a spaced plan with bounded sessions, active recall, problem practice, and review checkpoints.
6. Generate practice questions from supplied sources; keep answer keys separate and cite the source topic.
7. Log misconceptions and promote stable explanations only after checking course evidence.
8. At each checkpoint, update the plan from demonstrated recall and record gaps honestly.

## Agent prompts
### Codex
> Read `AGENTS.md`; use the supplied syllabus and course notes to create a study plan for `<exam/date>`. Mark unknown coverage, emphasize active recall, and do not alter source notes.

### Claude
> Read `CLAUDE.md`; diagnose topic gaps from the named materials and create source-linked practice questions plus a realistic schedule within `<hours>`.

### Gemini
> Read `GEMINI.md`; prepare a review-required course study pack from supplied sources only. Respect the stated academic-integrity rules and separate questions from answers.

## Validation checklist
- [ ] Exam date/scope/rules/time budget are sourced or marked unknown.
- [ ] Plan reflects prerequisites, weakness, and realistic session limits.
- [ ] Practice material traces to supplied course evidence.
- [ ] No prohibited graded work or fabricated requirement is included.
- [ ] Human/source notes remain unchanged.
