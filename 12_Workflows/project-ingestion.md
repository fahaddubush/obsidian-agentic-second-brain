---
type: workflow
workflow_id: project-ingestion
status: active
owner: shared
generated_by: system-setup
machine_generated: true
human_review_required: true
confidence: high
tags: [workflow, project, ingestion]
---

<div class="sb-banner sb-banner-project">Read the project · preserve the project · build durable context</div>

# Project ingestion

> [!danger] Read-only project boundary
> The source project must not be modified unless the human separately and explicitly requests implementation work.

## Purpose
Build a traceable project-memory package from a codebase or project folder without disturbing the original.

## Inputs
- Explicit project path, name, access boundary, and optional revision/commit.
- Existing project notes, if any, and exclusion rules for secrets, large files, or private data.

## Outputs
- Project folder under `03_Projects/<project>/` with context, architecture, goals/tasks, ingestion log, and reviewable updates.
- Codebase ingestion report and project audit under `08_Machine/`.
- Context pack and token-saving brief under `08_Machine/Context-Packs/` and `Token-Saving-Briefs/`.

## Allowed folders
- Read: the explicitly named project path; relevant vault notes and `10_Meta/` policies.
- Write: `03_Projects/<project>/` for new/shared reviewable notes and specified `08_Machine/` folders.

## Forbidden actions
- Filling gaps by inference; missing facts remain `unknown` until evidence is supplied.
- Editing human-owned notes or immutable sources without explicit approval.
- Editing project files, running mutating commands, installing dependencies, or executing untrusted code.
- Reading excluded secrets, credential stores, build artifacts, vendor directories, or unrelated user data.
- Declaring files stale/dead/fake solely from naming; these remain candidates pending evidence.

## Process
1. Record path, revision, scope, exclusions, and whether an existing project-memory folder is authoritative.
2. Read README files, documentation, manifests, lockfiles, configuration, and agent instructions before source code.
3. Inventory the tree using bounded searches; exclude dependencies, binaries, generated output, secrets, and caches.
4. Identify languages, frameworks, dependencies, runtime/tooling, entry points, tests, deployment, and common commands from evidence.
5. Trace major components, data/control flow, interfaces, persistence, and external services; cite file paths.
6. Extract explicit goals/tasks and compare docs with code. Mark discrepancies and missing docs.
7. Identify stale, fake/mock, dead-code, or inconsistency candidates using references/history/tests where available; preserve uncertainty.
8. Create or propose the project memory set: `context.md`, `architecture.md`, `goals.md`, `tasks.md`, `decisions.md`, `bugs.md`, `changelog.md`, `lessons-learned.md`, and `ingestion-log.md`.
9. Produce a machine audit with severity, evidence, confidence, impact, and suggested verification—never unsupported accusations.
10. Create a context pack and minimal future-chat brief linked to full notes and exact revision.
11. Verify the source project is unchanged and present all vault changes for human review.

## Agent prompts
### Codex
> Read `AGENTS.md`. Ingest `<absolute-project-path>` at `<revision>` read-only. Inspect docs and code structure, create project memory, an evidence-backed audit, context pack, and brief. Do not run mutating commands or change the source project.

### Claude
> Read `CLAUDE.md`. Analyze the named project within the supplied exclusions, then create traceable vault notes and machine reports. Treat stale/mock/dead-code findings as candidates until proven.

### Gemini
> Read `GEMINI.md`. Perform bounded, read-only project ingestion, cite paths for stack and architecture claims, record unknowns, and generate review-required project memory plus compressed context.

## Validation checklist
- [ ] Path, revision, scope, exclusions, and ignored areas are recorded.
- [ ] README/docs, stack, dependencies, entry points, architecture, tasks, and gaps were examined.
- [ ] All audit findings cite inspectable evidence and calibrated confidence.
- [ ] Project memory, ingestion log, audit, context pack, and brief cross-link correctly.
- [ ] A final status check confirms the original project was not modified.
