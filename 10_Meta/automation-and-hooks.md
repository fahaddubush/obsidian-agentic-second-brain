---
title: Automation and Hook Policy
type: integration-policy
status: active
human_review_required: true
---

# Automation and Hook Integration

Codex lifecycle automation is active through the reviewed project-local configuration in `.codex/hooks.json`. Scheduled/background automation remains opt-in. Every hook is dependency-free, local, and designed to avoid transcripts, prompt bodies, assistant messages, or tool outputs in persistent state.

| Trigger | Integrated behavior | Status |
|---|---|---|
| Codex session/thread start | Load canonical startup context, validate the vault, and create only missing daily/working-memory scaffolds. | Active after hook trust |
| User prompt submission | Match prompt intent to up to three of the 24 workflow files and inject their paths as developer context. Block obvious credential/private-key patterns. | Active after hook trust |
| Before Bash/file edits | Deny selected irreversible Git/deletion commands and updates/deletes/moves to immutable sources. | Active guardrail |
| After Bash/file edits | Mark the local session as requiring validation; retain no prompt, transcript, command, or output content. | Active |
| Turn stop | If dirty, run vault validation, instruction synchronization, and source-integrity checks; continue Codex when a fixable check fails. | Active |
| Subagent start | Inject vault safety and workflow context. | Active |
| End of coding session | Use `llm-session-summary.md` when requested. Codex exposes turn-scoped `Stop`, not a distinct session-close event. | Routed, not inferred |
| Git post-commit | Run `git-diff` manually or add a separate reviewed Git hook later. | Manual |
| Weekly/monthly/nightly schedule | Use Codex scheduled tasks with explicit times and reviewed prompts. | Not scheduled |

## Activation and trust

Project hooks require a trusted project layer and one-time review of the exact hook definition. Start a new Codex task from the vault, open `/hooks` or the Hooks settings section, inspect `.codex/hooks.json`, and trust it. Any handler/config edit changes the trusted hash and requires review again.

Do not use `--dangerously-bypass-hook-trust` for routine work.

## Automation boundary

Hooks automate Codex lifecycle behavior, not calendar schedules. Daily startup can happen on first Codex start, but daily shutdown, weekly/monthly review, nightly dreaming, and inbox sweeps need Codex scheduled tasks. These are intentionally not created until the human chooses times, timezone, and whether the machine may be offline.

The `Stop` event occurs after each Codex turn. It cannot reliably identify window close or the true end of a session, so it validates but does not create a full session summary every turn.

## Approval gate for future automation

Before expanding a hook: inspect and pin its code; define input/output folders; prohibit source/human-note mutation; guarantee no-overwrite behavior; redact secrets; keep network access off by default; log only minimal metadata; test with synthetic payloads; document disable/recovery steps; and obtain explicit human approval.
