---
type: workflow
workflow_id: research-digestion
status: active
owner: shared
generated_by: system-setup
machine_generated: true
human_review_required: true
confidence: high
tags: [workflow, research]
---

<div class="sb-banner sb-banner-research">Preserve sources · compare claims · compound understanding</div>

# Research digestion

> [!warning] Citation integrity
> Never cite a source that was not inspected. Derived synthesis must distinguish author claims, observed facts, and agent inference.

## Purpose
Convert a bounded research set into traceable source notes, concept links, open questions, and reviewable synthesis.

## Inputs
- Research question, inclusion boundary, source files/URLs, date accessed, and desired depth.
- Existing related concepts and previous synthesis notes.

## Outputs
- Immutable source captures under `07_Sources/` where authorized.
- Machine summaries/synthesis under `08_Machine/`.
- Suggested concept links or draft evergreen updates for review.

## Allowed folders
- Read: supplied sources plus relevant `04_Knowledge/`, `07_Sources/`, and policies.
- Write: new source records and `08_Machine/Summaries/`, `Synthesis/`, `Contradictions/`, `Link-Suggestions/`.

## Forbidden actions
- Filling gaps by inference; missing facts remain `unknown` until evidence is supplied.
- Editing human-owned notes or immutable sources without explicit approval.
- Altering raw captures, fabricating citations, or presenting snippets/search results as full-source review.
- Silently merging synthesis into human-owned concept notes.
- Concealing inaccessible, paywalled, outdated, or methodologically weak evidence.

## Process
1. Define the research question, scope, freshness needs, and acceptance criteria.
2. Inventory sources with creator/title/date/URL or path/access status; mark missing metadata unknown.
3. Read each accessible source and capture its claims, evidence, method, limitations, and context separately.
4. Create source-linked summaries that use paraphrase and respect copyright/licensing constraints.
5. Compare sources for agreement, disagreement, chronology, and incompatible definitions.
6. Build a synthesis that labels facts, source claims, and new inferences with confidence.
7. Propose links to concepts/projects and new questions; do not edit human notes automatically.
8. Record excluded/inaccessible sources and the date beyond which freshness should be rechecked.

## Agent prompts
### Codex
> Read `AGENTS.md`; digest the supplied research set for `<question>`. Preserve raw sources, create per-source summaries and a cross-source synthesis with direct provenance, and flag inaccessible evidence.

### Claude
> Read `CLAUDE.md`; analyze only the named sources, distinguish claims from inference, compare methods and limitations, and save all derived text as review-required machine notes.

### Gemini
> Read `GEMINI.md`; create traceable research digestion for the specified question and date boundary. Do not invent citations or merge into human concepts.

## Validation checklist
- [ ] Scope, access date, source list, and inaccessible items are explicit.
- [ ] Every substantive claim traces to an inspected source or is labeled inference.
- [ ] Raw source material remains unchanged.
- [ ] Conflicts, definitions, limitations, and freshness are addressed.
- [ ] Derived notes have machine provenance and review status.
