---
type: workflow
workflow_id: dreaming-nightly-synthesis
status: active
owner: shared
generated_by: system-setup
machine_generated: true
human_review_required: true
confidence: high
tags: [workflow, synthesis, dreaming]
---

<div class="sb-banner sb-banner-dream">Let recent memory meet · keep every insight reviewable</div>

# Dreaming / nightly synthesis

> [!warning] Manual or scheduled read-only review
> Scheduling may create machine reports, but it must never rewrite human notes, move captures, or enact project actions automatically.

## Purpose
Connect recent captures, daily notes, sessions, and project updates into tentative themes, links, contradictions, and next-action suggestions.

## Inputs
- Explicit time window (default suggestion: last seven days), timezone, project scope, and maximum notes.
- Recent inbox, daily, LLM/work sessions, project updates, and unresolved machine-review items.

## Outputs
- Dated dream report in `08_Machine/Dreams/`.
- Optional synthesis, contradiction, stale-note, and link-suggestion reports in their machine folders.

## Allowed folders
- Read: bounded recent notes in `00_Inbox/`, `01_Daily/`, `03_Projects/`, `05_Episodic-Memory/`, and relevant reviewed machine notes.
- Write: `08_Machine/Dreams/`, `Synthesis/`, `Contradictions/`, `Link-Suggestions/`, and `Reports/`.

## Forbidden actions
- Filling gaps by inference; missing facts remain `unknown` until evidence is supplied.
- Editing human-owned notes or immutable sources without explicit approval.
- Editing human/source/project notes, accepting suggestions, or starting project work.
- Treating repeated mentions as truth or importance without corroboration.
- Running unattended destructive hooks or scanning private/out-of-scope notes.

## Process
1. Record run time, timezone, date window, included folders, exclusions, and prior-run boundary.
2. Inventory notes and record coverage gaps; prefer summaries/briefs, opening full notes only when needed.
3. Extract explicit topics, events, decisions, open loops, and project changes with source links.
4. Cluster related items and describe repeated themes without converting frequency into fact.
5. Propose meaningful links, potential duplicates, and candidate evergreen lessons.
6. Run temporal/context checks for contradictions and staleness; create separate reports for substantive cases.
7. Suggest project next actions tied to explicit goals, labeling agent-generated priorities as proposals.
8. Create the dream report with facts, inferences, confidence, unknowns, and a short human review queue.
9. If scheduled, log success/failure only; never auto-apply the queue.

## Agent prompts
### Codex
> Read `AGENTS.md`; run dreaming synthesis for `<date range>` and `<scope>`. Create only machine-owned reports, link every theme to evidence, and do not edit or move original notes.

### Claude
> Read `CLAUDE.md`; synthesize recent inbox, daily, session, and project signals into reviewable themes, links, conflicts, and next-action proposals. Keep facts separate from interpretations.

### Gemini
> Read `GEMINI.md`; perform a bounded nightly review, preferring briefs before full notes. Produce a dated dream report and separate high-confidence issue reports; enact nothing.

## Validation checklist
- [ ] Run window, timezone, scope, exclusions, and coverage gaps are recorded.
- [ ] Themes, links, conflicts, and actions trace to exact notes.
- [ ] Repetition was not mistaken for correctness or priority.
- [ ] All output is machine-owned and human-review-required.
- [ ] No source/human note or external state changed.
