---
type: workflow
workflow_id: codebase-architecture-extraction
status: active
owner: shared
generated_by: system-setup
machine_generated: true
human_review_required: true
confidence: high
tags: [workflow, codebase, architecture]
---

<div class="sb-banner sb-banner-project">Trace behavior from evidence · keep diagrams honest</div>

# Codebase architecture extraction

> [!danger] Source code is read-only
> Architecture notes are derived machine artifacts. Do not “fix” the code while documenting it.

## Purpose
Derive a useful, evidence-linked architecture model from a bounded codebase snapshot.

## Inputs
- Project path and exact revision where available.
- README/docs, manifests, configuration, source tree, tests, and existing architecture notes.

## Outputs
- A proposed `03_Projects/<project>/architecture.md` update or separate machine draft.
- Supporting report in `08_Machine/Reports/` and link to the relevant context pack.

## Allowed folders
- Read: named project path and its vault project memory.
- Write: project documentation only when allowed; otherwise `08_Machine/Reports/` or `Synthesis/`.

## Forbidden actions
- Filling gaps by inference; missing facts remain `unknown` until evidence is supplied.
- Editing human-owned notes or immutable sources without explicit approval.
- Modifying or executing the codebase, installing dependencies, or probing external services.
- Inferring runtime behavior from filenames alone.
- Hiding contradictory documentation or uncertain component boundaries.

## Process
1. Fix the analysis boundary: revision, included paths, generated/vendor exclusions, and available runtime evidence.
2. Read declared architecture and build/runtime manifests; list claims to verify.
3. Locate entry points, composition roots, public interfaces, configuration sources, persistence, and integrations.
4. Trace representative flows from input to output through concrete symbols/files; avoid exhaustive low-value traversal.
5. Model components and dependencies with relative links and a small Mermaid diagram where it improves understanding.
6. Compare documentation, code, and tests; record disagreements without choosing silently.
7. Describe deployment/runtime topology only where configurations support it.
8. Record risks, unknowns, and follow-up verification steps.
9. Produce a reviewable architecture draft with source revision and freshness metadata.

## Agent prompts
### Codex
> Read `AGENTS.md`; extract architecture from `<project>` at `<revision>` in read-only mode. Trace entry points and representative flows with file evidence, then draft a review-required architecture note.

### Claude
> Read `CLAUDE.md`; reconcile declared and implemented architecture for the named scope. Use concise diagrams only where supported, and list contradictions and unknown boundaries.

### Gemini
> Read `GEMINI.md`; map components, interfaces, data flow, persistence, and external integrations from concrete files. Do not execute or edit the project.

## Validation checklist
- [ ] Revision and analyzed/excluded paths are explicit.
- [ ] Component and flow claims cite files, symbols, tests, or configuration.
- [ ] Declared versus observed architecture differences are visible.
- [ ] Diagrams do not imply unsupported runtime behavior.
- [ ] Original code and human notes were preserved.
