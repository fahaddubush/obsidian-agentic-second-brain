---
type: workflow
workflow_id: stale-note-detection
status: active
owner: shared
generated_by: system-setup
machine_generated: true
human_review_required: true
confidence: high
tags: [workflow, maintenance]
---

<div class="sb-banner sb-banner-quality">Age is a signal · inconsistency is evidence · humans decide</div>

# Stale-note detection

> [!warning] Never archive by age alone
> Old notes can remain valid; recent notes can already be obsolete. This workflow reports candidates only.

## Purpose
Find notes whose claims, status, links, or compressed context may no longer match current evidence.

## Inputs
- Folder/note scope, reference date, staleness rules, and current project/source evidence.

## Outputs
- Stale-note candidate report in `08_Machine/Reports/`.
- Optional contradiction reports and context-pack refresh queue.

## Allowed folders
- Read: named scope and the evidence needed to assess freshness.
- Write: `08_Machine/Reports/` and `Contradictions/`.

## Forbidden actions
- Filling gaps by inference; missing facts remain `unknown` until evidence is supplied.
- Editing human-owned notes or immutable sources without explicit approval.
- Editing timestamps to make notes appear fresh.
- Archiving, deleting, merging, or rewriting candidate notes.
- Marking immutable historical/source notes stale merely because their subject evolved.

## Process
1. Define freshness expectations by note type; exempt immutable sources and historical episodes from “obsolete” treatment.
2. Inventory `updated`, `valid_through`, project status, version/revision, and outbound links where present.
3. Compare claims/status/actions against newer authoritative notes, code revisions, decisions, or explicit deadlines.
4. Classify candidates: needs verification, superseded, broken link, abandoned working memory, stale context pack, or intentionally historical.
5. Cite the exact evidence that triggered each candidate; age alone is low-confidence context.
6. Recommend verify, refresh, link-to-successor, close, or archive-review, with an owner and safe next step.
7. Produce a report; route confirmed factual conflicts through contradiction detection.

## Agent prompts
### Codex
> Read `AGENTS.md`; detect stale-note candidates within `<scope>` as of `<date>`. Use content/version evidence, exempt immutable history, and produce a report without modifying notes.

### Claude
> Read `CLAUDE.md`; assess freshness using note-type rules and newer authoritative context. Explain each candidate and keep archival decisions human-owned.

### Gemini
> Read `GEMINI.md`; identify stale working memory, context packs, links, and status claims in the bounded scope. Do not use age as sole evidence.

## Validation checklist
- [ ] Scope, reference date, and per-type freshness rules are explicit.
- [ ] Source and episodic history were not mislabeled obsolete.
- [ ] Each candidate has current contrary evidence or a verification gap.
- [ ] Recommended action is reversible and human-reviewed.
- [ ] No timestamps, notes, or archive state were changed.
