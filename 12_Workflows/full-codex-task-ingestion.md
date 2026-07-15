---
type: workflow
workflow_id: full-codex-task-ingestion
status: active
owner: shared
generated_by: system-setup
machine_generated: true
human_review_required: true
confidence: high
tags: [workflow, codex, ingestion, memory]
---

<div class="sb-banner sb-banner-memory">Discover everything, preserve evidence, prove completeness</div>

# Full Codex task ingestion

> [!danger] Completion is a tested claim
> Do not report a successful ingestion until the manifest reconciles exactly and `ingestion-audit` passes with zero errors.

## Purpose

Ingest every available Codex task for the authorized projects into useful, evidence-linked memory without skipping tasks, weakening notes, inventing missing details, or exposing private history through public Git.

## Required inputs

- Explicit authorization to read Codex task history.
- Authorized project paths or an explicit request for every available Codex project.
- Vault privacy boundary and publication restrictions.
- Current local date and timezone.

## Required outputs

- Machine-readable JSON ingestion manifest based on `11_Templates/ingestion-manifest.json`.
- Source catalog with every project, task ID, title, status, and exact turn count.
- One episodic session note per distinct task.
- Complete twelve-file project-memory package for every project.
- Working, semantic, and procedural memory when evidence supports them.
- Context pack and continuation brief for every project.
- Private session index and final ingestion report.

## Process

1. Read `AGENTS.md`, `10_Meta/agent-core.md`, this workflow, and every referenced template before writing.
2. List every authorized Codex project and every available task for each exact project path.
3. Read every task page until no older-turn cursor remains.
4. Build the manifest before synthesis. Reconcile project, task, and turn counts.
5. Record incomplete, interrupted, duplicated, overlapping, and active tasks without merging them away.
6. Redact credentials and unnecessary private data before any persistent write.
7. Create one task-specific episodic note using the LLM session template. Use the task ID as provenance.
8. Extract project goals, architecture, accepted decisions, proposals, tasks, bugs, metrics, changes, lessons, unknowns, and next actions into separate project notes.
9. Separate historical task state from current repository state. Do not claim present correctness without inspecting the current repository.
10. Create context packs and briefs only after project memory is complete.
11. Keep private imported outputs outside public Git tracking and verify this boundary.
12. Run `ingestion-audit`, vault validation, instruction synchronization, source-integrity checks, tests, style scanning, and Git status review.
13. Correct every error before reporting completion. Warnings must be explained or corrected.

## Quality requirements

- No empty headings, blank bullets, unexplained placeholders, or generic filler.
- Every material project claim links to inspected session evidence.
- Recommendations never become accepted decisions without human evidence.
- Metrics identify their historical session and require current-artifact verification.
- Incomplete tasks remain incomplete.
- Duplicate tasks remain separately traceable.
- Context packs state freshness and source coverage.
- Briefs contain one objective, constraints, immediate next actions, unknowns, and an expansion path.
- Generated text follows the repository style restrictions.

## Required validation command

```powershell
python scripts/sb.py ingestion-audit "08_Machine/Reports/YYYY-MM-DD - Codex Ingestion Manifest.json"
```

## Completion gate

- [ ] Manifest task count equals discovered task count.
- [ ] Manifest turn count equals the sum of every task turn count.
- [ ] Every manifest task has one existing episodic note containing its task ID.
- [ ] Every project has all twelve required project-memory files.
- [ ] Every project has a context pack and continuation brief.
- [ ] No empty sections, weak placeholders, secrets, emojis, or long dashes remain.
- [ ] Evidence links resolve.
- [ ] Imported private paths do not appear in public Git status.
- [ ] Vault validation and automated tests pass.
