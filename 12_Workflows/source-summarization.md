---
type: workflow
workflow_id: source-summarization
status: active
owner: shared
generated_by: system-setup
machine_generated: true
human_review_required: true
confidence: high
tags: [workflow, source, summarization]
---

<div class="sb-banner sb-banner-research">One source at a time · faithful before concise</div>

# Source summarization

> [!danger] Raw source is immutable
> Write the summary beside the knowledge process in `08_Machine/`, never into or over the source capture.

## Purpose
Create a faithful, useful summary of one inspected source with explicit provenance, limitations, and unknowns.

## Inputs
- One source note/file/URL, its metadata, the summary purpose, and desired length.

## Outputs
- Summary in `08_Machine/Summaries/` linked to its source.
- Optional concept/link suggestions in `08_Machine/Link-Suggestions/`.

## Allowed folders
- Read: the named `07_Sources/` item and narrowly relevant context.
- Write: `08_Machine/Summaries/` and `Link-Suggestions/`.

## Forbidden actions
- Filling gaps by inference; missing facts remain `unknown` until evidence is supplied.
- Editing human-owned notes or immutable sources without explicit approval.
- Editing the source, inventing metadata, or implying complete coverage when only an excerpt was available.
- Excessive quotation or copying copyrighted text.
- Adding external claims that the source does not support without clear separation.

## Process
1. Confirm source identity, access status, completeness, and the question the summary should serve.
2. Record metadata exactly as available; use `unknown` for missing creator/date/license.
3. Identify the source’s purpose, central claims, evidence/method, conclusions, and stated limitations.
4. Paraphrase concisely; use only short quotations when exact wording is essential.
5. Separate source claims from the summarizer’s interpretation and label confidence.
6. Note contradictions, ambiguities, dated information, and missing sections.
7. Link the output to the source and propose related concepts without modifying them.

## Agent prompts
### Codex
> Read `AGENTS.md`; summarize only `<source>` for `<purpose>`. Preserve the source, state coverage limits, paraphrase faithfully, and create a machine-owned summary with a direct source link.

### Claude
> Read `CLAUDE.md`; produce a structured source summary that separates the author’s claims, evidence, limitations, and your interpretation. Mark unavailable metadata unknown.

### Gemini
> Read `GEMINI.md`; summarize the named source without external supplementation. Record whether the full source or an excerpt was inspected and keep link suggestions reviewable.

## Validation checklist
- [ ] Exactly one source and its inspected coverage are identified.
- [ ] Claims, evidence, conclusions, and limitations are faithfully separated.
- [ ] Quotes are minimal and provenance is explicit.
- [ ] Missing data remains `unknown`.
- [ ] The raw source is byte-for-byte untouched.
