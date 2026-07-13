---
type: workflow
workflow_id: project-audit
status: active
owner: shared
generated_by: system-setup
machine_generated: true
human_review_required: true
confidence: high
tags: [workflow, project, audit]
---

<div class="sb-banner sb-banner-project">Assess current reality · cite evidence · prioritize safely</div>

# Project audit

> [!danger] Audit-only boundary
> An audit diagnoses and recommends. It does not modify the project, dependencies, infrastructure, or human-owned memory.

## Purpose
Evaluate a project snapshot for architecture, correctness risk, maintainability, security posture, tests, documentation, and memory consistency.

## Inputs
- Project path, exact revision, audit goals, exclusions, risk tolerance, and previous audit/context notes.

## Outputs
- Audit report in `08_Machine/Project-Audits/`.
- Optional contradiction/link reports and proposed context-pack refresh.

## Allowed folders
- Read: explicitly named project path and its vault memory/policies.
- Write: `08_Machine/Project-Audits/` and related machine-review folders.

## Forbidden actions
- Filling gaps by inference; missing facts remain `unknown` until evidence is supplied.
- Editing human-owned notes or immutable sources without explicit approval.
- Editing code, installing dependencies, running untrusted software, changing external services, or exploiting vulnerabilities.
- Treating static hints as confirmed runtime defects.
- Hiding scope limitations or inflating severity.

## Process
1. Record project path, revision, audit dimensions, excluded paths, available tests, and environment limitations.
2. Read project instructions, docs, manifests, architecture notes, recent decisions, and prior audits.
3. Inspect structure, entry points, boundaries, dependency/configuration patterns, tests, and deployment evidence.
4. Assess documentation/code consistency and candidates for stale, mock, generated, duplicate, or dead code.
5. For each finding, capture severity, confidence, exact evidence, impact, and safest verification/remedy.
6. Separate confirmed issues, risks, questions, and out-of-scope areas.
7. Compare with prior audit findings and project memory; report resolved/regressed/unknown status without editing history.
8. Prioritize a small remediation sequence and identify decisions requiring human approval.
9. Verify the project is unchanged and save the report using the project-audit template.

## Agent prompts
### Codex
> Read `AGENTS.md`; audit `<project>` at `<revision>` read-only for `<dimensions>`. Save an evidence-backed report in `08_Machine/Project-Audits/`; do not implement fixes.

### Claude
> Read `CLAUDE.md`; conduct the bounded project audit, calibrate severity/confidence, and distinguish confirmed findings from static-analysis hypotheses.

### Gemini
> Read `GEMINI.md`; compare the named project snapshot with its docs and memory. Report inconsistencies and prioritized next steps, preserving both code and original notes.

## Validation checklist
- [ ] Revision, audit dimensions, exclusions, and environment limitations are explicit.
- [ ] Every finding has evidence, impact, severity, confidence, and next verification/action.
- [ ] Confirmed issues, risks, questions, and scope gaps are separated.
- [ ] Prior audit history was preserved.
- [ ] Git/filesystem status confirms the project was not modified.
