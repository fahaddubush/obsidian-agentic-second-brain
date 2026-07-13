---
type: workflow
workflow_id: git-diff-review
status: active
owner: shared
generated_by: system-setup
machine_generated: true
human_review_required: true
confidence: high
tags: [workflow, git, review]
---

<div class="sb-banner sb-banner-code">Review the change · cite the line · never alter the evidence</div>

# Git diff review

> [!warning] Review is non-mutating
> Do not stage, commit, checkout, reset, amend, or edit files. A review reports issues; it does not silently fix them.

## Purpose
Review a precise Git diff for correctness, safety, regressions, tests, documentation, and memory implications.

## Inputs
- Repository path and an explicit diff range or working-tree scope.
- Relevant project context, requirements, tests, and review focus.

## Outputs
- Dated review report in `08_Machine/Reports/` or project `audits/`.
- Optional decision/session links and suggested project-memory updates.

## Allowed folders
- Read: named repository, relevant `03_Projects/`, `05_Episodic-Memory/`, and `10_Meta/`.
- Write: machine review folders only.

## Forbidden actions
- Filling gaps by inference; missing facts remain `unknown` until evidence is supplied.
- Editing human-owned notes or immutable sources without explicit approval.
- Any Git or filesystem mutation, including staging and formatting.
- Reviewing outside the named diff unless required context is clearly identified.
- Reporting hypothetical style preferences as correctness defects.

## Process
1. Record repository, base/head or working-tree scope, current revision, and whether untracked files are included.
2. Read the diff, affected tests, nearby contracts, and project instructions; do not rely on patch fragments alone.
3. Trace behavior changes across callers, data shapes, error paths, security boundaries, and concurrency/state.
4. Check tests and docs for changed behavior; run only approved, non-mutating checks if requested.
5. List actionable findings ordered by severity. Each includes path/location, evidence, impact, and a focused remedy.
6. Separate blockers, non-blocking risks, questions, and optional improvements.
7. Note changed decisions or architecture that should enter project/episodic memory.
8. If no actionable defect is found, say so and list residual test/coverage uncertainty.

## Agent prompts
### Codex
> Read `AGENTS.md`; review repository `<path>` for diff `<range>` without changing it. Prioritize correctness and regression findings, cite exact locations, and save a review-required report.

### Claude
> Read `CLAUDE.md`; perform a non-mutating review of the specified diff with surrounding context. Separate proven defects from questions and stylistic suggestions.

### Gemini
> Read `GEMINI.md`; inspect the named Git diff and related tests/contracts. Report evidence-backed issues by severity and state residual uncertainty if no defects are found.

## Validation checklist
- [ ] Repository, revision, and diff boundary are unambiguous.
- [ ] Findings are actionable, prioritized, and tied to exact evidence.
- [ ] Facts are separated from hypotheses and style preferences.
- [ ] Relevant tests/docs and cross-file effects were considered.
- [ ] Git status and project files remain unchanged.
