# Safe automation scripts

<div class="sb-card sb-machine"><strong>Deterministic helpers</strong><br>Local, dependency-free, reviewable, and conservative by default.</div>

## Purpose

This folder contains the vault's Python command line tools. Deterministic helpers protect integrity, while the private runtime supplies an auditable queue and retrieval index for scheduled agentic reconciliation.

## What belongs here

- `sb.py`: the unified command line entry point.
- `vaultlib.py`: shared path, hashing, Markdown-link, and atomic-write helpers.
- `install_global_codex.py`: idempotent user-level Codex hook and guidance installer.
- `brain_runtime.py`: private SQLite event journal, durable job queue, ranked Markdown retrieval, receipts, retries, and repair checks.
- Small deterministic utilities that follow [[10_Meta/safety-policy]].

## What does not belong here

- API keys, credentials, downloaded models, embedding databases, or transcripts.
- Self-modifying agent code or unreviewed background services.
- Tools that overwrite human notes or external projects.

## Writers

Humans own this folder. AI may propose or edit code only when explicitly asked, with tests and review.

## Quick start

Requires Python 3.10 or newer and no third-party packages.

```powershell
python scripts/sb.py --help
python scripts/sb.py validate
python scripts/sb.py instruction-sync
python scripts/sb.py daily
python scripts/sb.py daily --missing-only
python scripts/sb.py maintenance
python scripts/sb.py hooks-check --project-root ".."
python scripts/sb.py ingestion-audit "08_Machine/Reports/YYYY-MM-DD - Codex Ingestion Manifest.json"
python scripts/sb.py session --agent Codex --title "Implemented feature X"
python scripts/sb.py graph-audit
python scripts/sb.py sources --write
python scripts/sb.py project-ingest "C:\path\to\project"
python scripts/install_global_codex.py install
python scripts/install_global_codex.py check
python scripts/brain_runtime.py search "current project decisions" --json
python scripts/brain_runtime.py doctor --repair --json
python scripts/brain_runtime.py claim --limit 20 --json
```

## Examples

- Create-only planning notes: `python scripts/sb.py daily`
- Read-only vault health check: `python scripts/sb.py validate`
- Read-only project inventory with machine outputs: `python scripts/sb.py project-ingest "C:\work\my-project"`
- Full deterministic maintenance: `python scripts/sb.py maintenance`
- Hook discovery diagnostics for the parent Codex project: `python scripts/sb.py hooks-check --project-root ".."`
- Strict manifest reconciliation: `python scripts/sb.py ingestion-audit "08_Machine/Reports/YYYY-MM-DD - Codex Ingestion Manifest.json"`
- Global Codex integration: `python scripts/install_global_codex.py install`
- Global integration verification: `python scripts/install_global_codex.py check`
- Ranked private-memory retrieval: `python scripts/brain_runtime.py search "query" --json`
- Runtime reconciliation and safe repair: `python scripts/brain_runtime.py doctor --repair --json`

## Full Codex task ingestion

The maintenance command cannot read Codex task history by itself. Codex exposes task history through app tools available inside a Codex task, not through this standalone Python process.

Open a Codex task from this vault and submit this exact reusable request:

```text
Ingest all available Codex tasks from every Codex project into this local brain. Use transcript ingestion, LLM session memory, project memory, decisions, working memory, context packs, briefs, source integrity, and validation. Keep imported memory local and do not push it.
```

The trusted prompt hook routes this request to the ingestion and session workflows. This explicit request is the privacy boundary that authorizes Codex to read the task histories.

Before reporting completion, create the JSON manifest from `11_Templates/ingestion-manifest.json` and require `ingestion-audit` to pass with zero errors.

All create commands refuse to overwrite existing output. `instruction-sync --write` changes only adapter hash sentinels. `sources --write` changes only the ignored local manifest at `.codex/state/source-integrity.json`. A clean public checkout validates against `08_Machine/Reports/source-integrity.example.json` until a private manifest is created. Hook evidence and queue state live outside the repository at `~/.codex/second-brain/brain.db`. The reviewed recurring worker follows [[../12_Workflows/agentic-memory-reconciliation]] and never rewrites protected human or source notes.

## Validation

```powershell
python -m unittest discover -s tests -v
python -m py_compile scripts/vaultlib.py scripts/sb.py scripts/brain_runtime.py scripts/install_global_codex.py .codex/hooks/codex_hook.py
```
