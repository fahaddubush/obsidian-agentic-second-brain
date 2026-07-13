---
type: workflow
workflow_id: link-suggestion
status: active
owner: shared
generated_by: system-setup
machine_generated: true
human_review_required: true
confidence: high
tags: [workflow, links]
---

<div class="sb-banner sb-banner-graph">Suggest edges · explain why · let humans accept</div>

# Link suggestion

> [!note] Suggestions are not edits
> All candidate links go to `08_Machine/Link-Suggestions/`; agents do not inject links into protected notes automatically.

## Purpose
Find high-value relationships among notes using titles, existing links, shared evidence, and semantic meaning.

## Inputs
- Explicit note/folder scope, relationship types of interest, and link-quality threshold.

## Outputs
- Link-suggestion report in `08_Machine/Link-Suggestions/`.
- Optional orphan/duplicate candidates with confidence and rationale.

## Allowed folders
- Read: named vault scope, excluding private or protected areas not granted.
- Write: `08_Machine/Link-Suggestions/` only.

## Forbidden actions
- Filling gaps by inference; missing facts remain `unknown` until evidence is supplied.
- Editing human-owned notes or immutable sources without explicit approval.
- Editing notes, creating links based only on shared tags/keywords, or inventing note targets.
- Scanning the entire vault when a bounded scope is supplied.
- Suggesting links to missing notes without labeling them as new-note candidates.

## Process
1. Inventory the scoped notes and resolve current links/aliases before proposing new ones.
2. Identify candidates based on explicit references, shared source evidence, dependency, sequence, contradiction, or strong conceptual relation.
3. Assign a relationship label such as supports, contradicts, implements, depends-on, example-of, or follows-from.
4. Explain the evidence and practical value of each bidirectional link.
5. Remove duplicates, self-links, already-linked pairs, and vague keyword matches.
6. Rank by confidence and benefit; mark uncertain targets or aliases.
7. Produce exact suggested wiki-link text and insertion location, but make no note edits.

## Agent prompts
### Codex
> Read `AGENTS.md`; find high-value links within `<scope>`. Write a ranked machine report with relationship, evidence, and exact insertion suggestion. Do not edit source or human notes.

### Claude
> Read `CLAUDE.md`; analyze the named notes for meaningful graph relationships, reject keyword-only matches, and keep all links as reviewable proposals.

### Gemini
> Read `GEMINI.md`; generate link suggestions for the supplied scope, resolve existing links first, and label missing targets or uncertain aliases.

## Validation checklist
- [ ] Scope and relationship criteria are explicit.
- [ ] Proposed target notes exist or are labeled creation candidates.
- [ ] Every link has evidence, relationship type, benefit, and confidence.
- [ ] Existing/self/duplicate/keyword-only links are excluded.
- [ ] No original note was modified.
