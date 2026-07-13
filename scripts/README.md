# Safe automation scripts

<div class="sb-card sb-machine"><strong>Deterministic helpers</strong><br>Local, dependency-free, reviewable, and conservative by default.</div>

## Purpose

This folder contains the vault's optional Python command line tools. They reduce repetitive bookkeeping without turning the vault into an unattended autonomous system.

## What belongs here

- `sb.py`: the unified command line entry point.
- `vaultlib.py`: shared path, hashing, Markdown-link, and atomic-write helpers.
- Small deterministic utilities that follow [[10_Meta/safety-policy]].

## What does not belong here

- API keys, credentials, downloaded models, embedding databases, or transcripts.
- Background daemons, silently installed schedulers, or self-modifying agent code.
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
python scripts/sb.py session --agent Codex --title "Implemented feature X"
python scripts/sb.py graph-audit
python scripts/sb.py sources --write
python scripts/sb.py project-ingest "C:\path\to\project"
```

## Examples

- Create-only planning notes: `python scripts/sb.py daily`
- Read-only vault health check: `python scripts/sb.py validate`
- Read-only project inventory with machine outputs: `python scripts/sb.py project-ingest "C:\work\my-project"`

All create commands refuse to overwrite existing output. `instruction-sync --write` changes only adapter hash sentinels. `sources --write` changes only the machine-owned integrity manifest. Hooks and schedulers are proposals in [[10_Meta/automation-and-hooks]] and are not installed.

## Validation

```powershell
python -m unittest discover -s tests -v
python -m py_compile scripts/vaultlib.py scripts/sb.py
```
