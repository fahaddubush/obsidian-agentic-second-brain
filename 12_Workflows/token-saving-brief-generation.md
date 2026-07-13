---
type: workflow
workflow_id: token-saving-brief-generation
status: active
owner: shared
generated_by: system-setup
machine_generated: true
human_review_required: true
confidence: high
tags: [workflow, brief, memory]
---

<div class="sb-banner sb-banner-memory">Smallest useful context · clear expansion path</div>

# Token-saving brief generation

> [!note] A brief is a cache, not the source of truth
> Future agents should read the brief first, then its context pack, then full notes only as needed.

## Purpose
Create a purpose-specific startup brief containing only the context necessary for the next likely task.

## Inputs
- Intended use case, current reviewed context pack, authoritative next actions/constraints, and optional token/length target.

## Outputs
- Brief in `08_Machine/Token-Saving-Briefs/` linked to its context pack and source notes.

## Allowed folders
- Read: the named current context pack and only the authoritative notes needed to verify it.
- Write: `08_Machine/Token-Saving-Briefs/`.

## Forbidden actions
- Filling gaps by inference; missing facts remain `unknown` until evidence is supplied.
- Editing human-owned notes or immutable sources without explicit approval.
- Creating a generic all-purpose dump, omitting critical safety constraints, or inventing missing project state.
- Treating an unreviewed/stale context pack as current without warning.
- Copying secrets, long logs, transcripts, or easily discoverable background.

## Process
1. Define one use case: active-project startup, debugging continuation, audit/research continuation, application, study, or second-brain maintenance.
2. Verify source context-pack freshness, revision, confidence, and unresolved contradictions.
3. Select only objective, essential state, settled decisions, hard constraints, immediate actions, critical files/notes, and known unknowns.
4. Remove history that does not change the next action and commands that are not safe/current.
5. Include an expansion ladder: context pack, then specific full notes, then sources/sessions.
6. State generated/updated date, source pack, source notes, confidence, and human-review requirement.
7. Test the brief against the use case: an agent should know what to do next and what not to assume.

## Agent prompts
### Codex
> Read `AGENTS.md`; generate the shortest useful brief for `<use case>` from `<context pack>`. Include current objective, constraints, next actions, critical files, unknowns, and expansion links only.

### Claude
> Read `CLAUDE.md`; compress the reviewed context pack into a single-purpose continuation brief. Preserve safety-critical facts and explicitly warn if source context is stale.

### Gemini
> Read `GEMINI.md`; create a token-saving brief for `<use case>` with a clear brief → pack → full-notes expansion path. Do not add unsupported state.

## Validation checklist
- [ ] Brief has one explicit use case and known freshness/revision.
- [ ] All required immediate state and safety constraints are present.
- [ ] Historical/detail content that does not affect next action was removed.
- [ ] Unknowns and stale-source warnings are visible.
- [ ] Links to the context pack and specific expansion notes resolve.
