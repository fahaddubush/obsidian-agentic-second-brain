---
type: workflow
workflow_id: llm-session-summary
status: active
owner: shared
generated_by: system-setup
machine_generated: true
human_review_required: true
confidence: high
tags: [workflow, llm-session, memory]
---

<div class="sb-banner sb-banner-memory">End the chat with a handoff future agents can trust</div>

# LLM session summary

> [!warning] Never reconstruct missing chat history
> Summarize the available transcript/current context. Any unavailable command, file, model, result, or rationale remains `unknown`.

## Purpose
Convert a meaningful Codex, Claude, Gemini, or other agent session into traceable episodic memory and minimal future context.

## Inputs
- Available session transcript/current context, agent/tool, date/timezone, project, and optional repository status/diff.

## Outputs
- `05_Episodic-Memory/LLM-Sessions/<Agent>/<YYYY>/<YYYY-MM-DD - Title>.md`.
- Updated LLM-session index and proposed related project-memory updates.
- Optional context pack and token-saving brief in `08_Machine/`.

## Allowed folders
- Read: current session evidence, named project/repository, relevant project memory, and prior briefs.
- Write: new LLM session note and machine context; indexes/project notes only if shared-write policy allows and changes are reviewable.

## Forbidden actions
- Filling gaps by inference; missing facts remain `unknown` until evidence is supplied.
- Editing human-owned notes or immutable sources without explicit approval.
- Inventing absent transcript details, commands, modified files, decisions, errors, outcomes, or model identity.
- Copying secrets, full sensitive transcripts, or unnecessary private content.
- Claiming an index/project update succeeded unless it was actually written and verified.

## Process
1. Identify agent/tool as Codex, Claude, Gemini, or Other; record model/session ID only if known.
2. Confirm local date/timezone, project/area, original request, and session goal from available evidence.
3. Summarize the final outcome, distinguishing completed, attempted, blocked, declined, and unknown work.
4. Inventory files inspected/modified and commands run from tool records or verified repository state; do not reconstruct from memory.
5. Capture important decisions, assumptions, errors/fixes, unresolved issues, and next actions with evidence.
6. Write reusable context that is concise, excludes secrets, and links to full project/source notes.
7. Create the note in the correct agent/year path using the session template; use `unknown` for missing fields.
8. Add a relative link to the session index and propose/update relevant project context without overwriting human prose.
9. Refresh a context pack only when durable state changed; create a shorter brief for the most likely next-session use case.
10. Reopen all written files and validate links, YAML, provenance, and consistency against the current session.

## Agent prompts
### Codex
> Read `AGENTS.md`; summarize this Codex session into the correct year folder. Use only current transcript/tool evidence, record files and commands exactly, update the session index, and create the shortest useful continuation brief.

### Claude
> Read `CLAUDE.md`; save this Claude Code session as episodic memory. Mark unavailable details unknown, preserve unresolved issues, and update related context through reviewable changes.

### Gemini
> Read `GEMINI.md`; create this Gemini CLI session summary with verified outcome, files, commands, decisions, errors/fixes, and next actions. Then create a source-linked future-chat brief.

## Validation checklist
- [ ] Agent/year path, date, title, project, goal, and original request are correct.
- [ ] Outcome, files, commands, decisions, assumptions, errors, and fixes match available evidence.
- [ ] Unknown details remain `unknown`; secrets/raw transcript excess are excluded.
- [ ] Session index and related project links resolve and were actually updated or clearly proposed.
- [ ] Context pack/brief are shorter than full memory and cite their source session.
