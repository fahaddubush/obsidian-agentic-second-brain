---
type: workflow
workflow_id: agentic-memory-reconciliation
status: active
owner: shared
generated_by: system-setup
machine_generated: true
human_review_required: true
confidence: high
tags: [workflow, memory, reconciliation, automation]
---

# Agentic memory reconciliation

## Purpose

Turn private lifecycle events into verified, nonduplicative memory using model judgment, bounded subagents, deterministic receipts, and safe recovery.

Scheduled workers include `[second-brain-reconciliation-worker:v1]` in their prompt. The private runtime journals their evidence for audit but never queues their own completion as new memory work.

## Inputs

- Pending jobs from the private runtime database.
- Relevant repository state, current vault memory, and available task evidence.
- The `agentic-second-brain` skill and its memory contract.

## Process

1. Run `python scripts/brain_runtime.py doctor --repair --json`.
2. Claim up to twenty jobs with `python scripts/brain_runtime.py claim --limit 20 --json`.
3. Group jobs by session and project. Never merge away distinct evidence.
4. For multiple independent projects or evidence lanes, delegate read-only extraction to at most three `brain_researcher` agents.
5. Consolidate each task into one episodic record. Update project, semantic, procedural, working, temporal, context-pack, or brief memory only when durable evidence supports it.
6. Use a `brain_verifier` agent for batches, conflicts, weak evidence, or high-impact updates.
7. Run vault validation, instruction synchronization, source integrity, automated tests, style checks, and Git status review.
8. Record a receipt for every completed job. The receipt must name an existing vault note.
9. Mark failures through the runtime CLI so retries and dead-letter state remain truthful.

## Self-healing boundary

The worker may rebuild retrieval indexes, retry transient jobs, recover stale processing leases, refresh machine-owned integrity metadata, and regenerate derived briefs from verified memory. It must not silently rewrite human notes, immutable evidence, policies, accepted decisions, or semantic conflicts.

## Completion gate

- [ ] Every claimed job has a receipt or an explicit retry/dead-letter status.
- [ ] Memory claims link to source events, task evidence, or inspected repository artifacts.
- [ ] Duplicate and superseded facts preserve provenance and temporal history.
- [ ] No filler note was created for a turn without durable value.
- [ ] Validation passes and private outputs remain absent from public Git status.
