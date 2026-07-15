---
title: Automation and Hook Policy
type: integration-policy
status: active
human_review_required: true
---

# Automation and Hook Integration

Codex lifecycle automation has two reviewed layers: project-local vault protection in `.codex/hooks.json`, plus user-level memory routing installed in `~/.codex/hooks.json`. Hooks write redacted lifecycle evidence to the private SQLite journal at `~/.codex/second-brain/brain.db`. Raw evidence never belongs in the public repository.

| Trigger | Integrated behavior | Status |
|---|---|---|
| Codex session/thread start | Load canonical startup context, validate the vault, and create only missing daily/working-memory scaffolds. | Active after hook trust |
| User prompt submission | Journal redacted evidence, retrieve ranked private memory, match intent to up to three of the 26 workflows, and block obvious credential/private-key patterns. | Active after hook trust |
| Before Bash/file edits | Deny selected irreversible Git/deletion commands and updates/deletes/moves to immutable sources. | Active guardrail |
| After Bash/file edits | Mark the local session as requiring validation; retain no prompt, transcript, command, or output content. | Active |
| Turn stop | If dirty, run vault validation, instruction synchronization, and source-integrity checks; continue Codex when a fixable check fails. | Active |
| Subagent lifecycle | Inject vault safety, then journal delegated evidence on completion. | Active after global hook trust |
| Context compaction | Checkpoint lifecycle evidence before and after compaction. | Active after global hook trust |
| Global turn stop | Journal the redacted assistant outcome and enqueue one idempotent reconciliation job. It never creates a continuation loop. | Active after global hook trust |
| Git post-commit | Run `git-diff` manually or add a separate reviewed Git hook later. | Manual |
| Memory reconciliation schedule | Claim queued jobs, consolidate typed memory, verify results, and record receipts or failures. | Scheduled locally |

## Activation and trust

Project hooks require a trusted project layer and one-time review of the exact hook definition. Start a new Codex task from the vault, open `/hooks` or the Hooks settings section, inspect `.codex/hooks.json`, and trust it. Any handler/config edit changes the trusted hash and requires review again.

Codex only discovers `.codex` configuration at the active project root. In this workspace the Codex project is commonly `Project #3`, while the Git repository and vault are nested under `second-brain`. A local adapter at `Project #3/.codex` exposes the nested reviewed handler. Restart Codex after creating or changing that adapter, then use a new task.

Verify discovery before troubleshooting the UI:

```powershell
cd "C:\Users\slopp\Desktop\Projects\Project #3"
python second-brain\scripts\sb.py hooks-check --project-root "."
```

Do not use `--dangerously-bypass-hook-trust` for routine work.

To make the agent available across every Codex project on this machine, install and verify the user-level layer:

```powershell
cd "C:\Users\slopp\Desktop\Projects\Project #3\second-brain"
python scripts\install_global_codex.py install
python scripts\install_global_codex.py check
```

The installer merges rather than replaces existing hooks, adds a marked block to the global `AGENTS.md`, enables hooks, native memories, and multi-agent support, installs the `agentic-second-brain` skill and three bounded agent roles, initializes the private journal, and adds the vault to `sandbox_workspace_write.writable_roots`. It creates `.before-second-brain` backups on first installation. Restart Codex, then review and trust the user-level hook definitions in Settings or `/hooks`. User hooks load independently of project trust.

The global layer does not add a global `PreToolUse` guard. Applying vault-only denials to unrelated repositories would break normal work. Project-local `PreToolUse` remains active whenever Codex works inside the vault project.

## Automation boundary

Hooks are fast evidence collectors, not autonomous model workers. The scheduled `Agentic Brain Reconciliation` task performs the slower semantic work: it claims durable jobs, groups related turns, retrieves supporting context, launches bounded specialist agents only when useful, writes typed memories, verifies the batch, and records a receipt or retry. Failed jobs are retried with backoff and eventually retained for diagnosis instead of silently disappearing.

The scheduled worker carries a versioned maintenance marker. Its lifecycle evidence remains auditable, but its own completion is not queued again. This prevents reconciliation from feeding itself.

The `Stop` event occurs after each Codex turn and cannot identify window close or the true end of a session. It only appends redacted evidence and queues an idempotent job. Native Codex memories provide an additional global context layer, but the private journal remains the auditable source for this vault integration.

Local Codex hooks cannot execute inside ordinary ChatGPT web conversations. They apply to Codex tasks and Codex surfaces that load the user-level configuration. ChatGPT Memory and Reference Chat History are separate account features. A remote authenticated MCP app can expose selected vault capabilities to ChatGPT, but it must be added explicitly and cannot silently capture every ChatGPT conversation.

## Repeatable full ingestion

Run all safe local maintenance checks with:

```powershell
python scripts/sb.py maintenance
```

To ingest Codex task history, open a Codex task from the vault and submit:

```text
Ingest all available Codex tasks from every Codex project into this local brain. Use transcript ingestion, LLM session memory, project memory, decisions, working memory, context packs, briefs, source integrity, and validation. Keep imported memory local and do not push it.
```

The project hook routes this wording to the relevant workflows. A standalone script cannot directly read Codex task history because that history is exposed through Codex app task tools. This prevents unattended local scripts from scraping private conversations.

Every full ingestion must create a manifest from `11_Templates/ingestion-manifest.json` and pass:

```powershell
python scripts/sb.py ingestion-audit "08_Machine/Reports/YYYY-MM-DD - Codex Ingestion Manifest.json"
```

## Approval gate for future automation

Before expanding a hook: inspect and pin its code; define input/output folders; prohibit source/human-note mutation; guarantee no-overwrite behavior; redact secrets; keep network access off by default; log only minimal metadata; test with synthetic payloads; document disable/recovery steps; and obtain explicit human approval.
