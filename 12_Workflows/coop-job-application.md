---
type: workflow
workflow_id: coop-job-application
status: active
owner: shared
generated_by: system-setup
machine_generated: true
human_review_required: true
confidence: high
tags: [workflow, career, application]
---

<div class="sb-banner sb-banner-career">Match evidence to role · keep claims truthful · human sends</div>

# Co-op / job application

> [!danger] No autonomous submission
> Agents may research and draft, but must not apply, message, upload, schedule, or represent the human without explicit approval for that exact action.

## Purpose
Prepare a truthful, tailored application package and durable tracking context for a specific opportunity.

## Inputs
- Job posting/source URL, access date, company/role, deadline, location, eligibility, resume facts, portfolio evidence, and human preferences.

## Outputs
- Application working note under `02_Working-Memory/` or career project memory.
- Draft tailoring analysis and materials under `08_Machine/Reports/`.
- Optional future-chat brief under `08_Machine/Token-Saving-Briefs/`.

## Allowed folders
- Read: explicitly supplied career materials, source posting, and relevant project evidence.
- Write: new working/machine notes; human resume, cover letter, and trackers only with explicit approval.

## Forbidden actions
- Filling gaps by inference; missing facts remain `unknown` until evidence is supplied.
- Editing human-owned notes or immutable sources without explicit approval.
- Inventing experience, metrics, skills, dates, eligibility, contacts, or company facts.
- Sending/submitting anything, scraping restricted data, or exposing personal information.
- Optimizing for keywords at the expense of truth or readability.

## Process
1. Capture posting provenance, access date, deadline, location/work authorization, and unknowns.
2. Extract requirements and responsibilities, separating required, preferred, and ambiguous language.
3. Map each relevant requirement to verified resume/project evidence; leave unsupported items as gaps.
4. Research company/role only from inspected sources and date-stamp unstable facts.
5. Draft truthful resume bullets/cover-letter points without modifying canonical documents.
6. Identify questions, risks, portfolio links, and interview stories with evidence.
7. Create a human review checklist for accuracy, tone, privacy, formatting, and submission details.
8. Record status and next action only after the human confirms; create a concise continuation brief if useful.

## Agent prompts
### Codex
> Read `AGENTS.md`; analyze `<job posting>` against my supplied resume/project facts. Draft a truthful tailoring report and application checklist. Do not edit canonical files or submit anything.

### Claude
> Read `CLAUDE.md`; map the role’s requirements to verified evidence, highlight gaps, and draft concise application language with no invented metrics or experience.

### Gemini
> Read `GEMINI.md`; prepare a dated, source-linked application brief for `<role/company>`. Keep unstable facts time-stamped and all external actions human-approved.

## Validation checklist
- [ ] Posting URL/source, access date, deadline, and unknowns are recorded.
- [ ] Every candidate claim maps to verified human/project evidence.
- [ ] Drafts contain no invented experience, numbers, eligibility, or company claims.
- [ ] Personal data is minimized and protected.
- [ ] Nothing was sent, submitted, or changed externally.
