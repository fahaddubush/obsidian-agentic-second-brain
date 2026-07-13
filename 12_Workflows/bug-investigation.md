---
type: workflow
workflow_id: bug-investigation
status: active
owner: shared
generated_by: system-setup
machine_generated: true
human_review_required: true
confidence: high
tags: [workflow, debugging]
---

<div class="sb-banner sb-banner-code">Reproduce · isolate · test hypotheses · retain the trail</div>

# Bug investigation

> [!warning] Diagnosis before mutation
> This workflow produces an investigation record. Code fixes, destructive diagnostics, or production actions require separate authorization.

## Purpose
Investigate a defect systematically and preserve reusable evidence, hypotheses, experiments, and next steps.

## Inputs
- Project/revision, observed behavior, expected behavior, environment, reproduction steps, logs, and scope.

## Outputs
- Investigation report in `08_Machine/Reports/`.
- Optional work-session note and proposed update to project `bugs.md`.

## Allowed folders
- Read: named project path, project memory, relevant sessions, and supplied logs.
- Write: machine reports and new episodic memory; project bug index only with approval.

## Forbidden actions
- Filling gaps by inference; missing facts remain `unknown` until evidence is supplied.
- Editing human-owned notes or immutable sources without explicit approval.
- Changing code or production state unless explicitly requested.
- Running destructive, privileged, network, or data-mutating experiments without approval.
- Claiming root cause from correlation or suppressing failed hypotheses.

## Process
1. Capture expected versus observed behavior, revision, environment, frequency, impact, and evidence gaps.
2. Establish the smallest safe reproduction; redact secrets from logs and notes.
3. Trace the affected path through code/configuration and compare working versus failing cases.
4. Maintain a hypothesis table with supporting/contradicting evidence and confidence.
5. Run approved, reversible diagnostics one variable at a time and record commands plus results.
6. Narrow to root cause only when evidence discriminates alternatives; otherwise report the leading hypotheses.
7. Propose the smallest fix and regression test, but do not implement unless separately authorized.
8. Record unresolved risks, reproduction status, and the next discriminating test.

## Agent prompts
### Codex
> Read `AGENTS.md`; investigate bug `<id>` in `<project@revision>` without editing it. Build a reproducible evidence trail, test safe hypotheses, and report root cause only if demonstrated.

### Claude
> Read `CLAUDE.md`; analyze the supplied symptom and logs, separate observations from hypotheses, and produce a reviewable investigation with next discriminating tests.

### Gemini
> Read `GEMINI.md`; perform a bounded bug investigation using only approved diagnostics. Record environment and commands, redact secrets, and do not implement a fix.

## Validation checklist
- [ ] Expected/observed behavior, revision, and environment are captured.
- [ ] Reproduction and commands are safe, explicit, and results recorded.
- [ ] Hypotheses show both supporting and contradicting evidence.
- [ ] Root-cause confidence matches the evidence.
- [ ] No code, human note, or external state changed without approval.
