---
type: workflow
workflow_id: contradiction-detection
status: active
owner: shared
generated_by: system-setup
machine_generated: true
human_review_required: true
confidence: high
tags: [workflow, contradiction]
---

<div class="sb-banner sb-banner-quality">Compare claims · normalize context · report, never erase</div>

# Contradiction detection

> [!warning] Contradictions are hypotheses
> Different dates, versions, scopes, or definitions often explain apparent conflicts. Preserve both notes until a human resolves them.

## Purpose
Identify and explain potentially incompatible claims while minimizing false positives and preserving historical context.

## Inputs
- Bounded note set, comparison date, and optional project/version/domain context.

## Outputs
- Reports in `08_Machine/Contradictions/`.
- Optional link suggestions and human questions.

## Allowed folders
- Read: the named note scope and directly linked evidence.
- Write: `08_Machine/Contradictions/` and `Link-Suggestions/`.

## Forbidden actions
- Filling gaps by inference; missing facts remain `unknown` until evidence is supplied.
- Editing human-owned notes or immutable sources without explicit approval.
- Editing either claim, choosing a winner without evidence, or deleting obsolete history.
- Comparing claims detached from their date, version, qualifiers, or source reliability.
- Reporting different opinions as factual contradictions.

## Process
1. Extract atomic claims with note path, section/location, date/version, qualifiers, and provenance.
2. Match only claims about the same subject, property, and compatible scope.
3. Test for temporal change, different environments, definitions, units, authority levels, or fact-versus-opinion.
4. Classify as direct contradiction, possible tension, supersession candidate, compatible, or insufficient evidence.
5. Create one report per meaningful conflict using the contradiction template.
6. Suggest clarifying language, source verification, or a decision note—never an automatic rewrite.
7. Link related reports and mark whether resolution would affect context packs or project memory.

## Agent prompts
### Codex
> Read `AGENTS.md`; compare claims within `<scope>` as of `<date/version>`. Create contradiction reports only after checking time, version, definition, and provenance. Do not edit the claims.

### Claude
> Read `CLAUDE.md`; identify genuine or possible contradictions in the named notes. Quote minimally, cite exact locations, and explain alternative reconciliations.

### Gemini
> Read `GEMINI.md`; run bounded contradiction detection and classify each pair with calibrated confidence. Preserve historical claims and propose human verification.

## Validation checklist
- [ ] Each pair concerns the same subject/property/scope.
- [ ] Date, version, units, definitions, and provenance were compared.
- [ ] Report classification and confidence match the evidence.
- [ ] Opinions and superseded facts are not misreported as direct contradictions.
- [ ] No source or human note was changed.
