# Codex project integration

## Purpose

Connect this vault's policies and workflows to Codex lifecycle hooks.

## What belongs here

- `config.toml`: project-local Codex feature settings.
- `hooks.json`: reviewed hook event definitions.
- `hooks/`: deterministic, dependency-free handlers and their tests.

## What does not belong here

Hook trust records, transcripts, prompts, credentials, API keys, or runtime state. `.codex/state/` is local and ignored by Git.

## Writers

Humans govern this integration. AI may update it only when explicitly requested; any changed hook must be reviewed and trusted again in Codex.

## Examples

- `SessionStart` loads the maintenance brief and creates only missing daily scaffolds.
- `UserPromptSubmit` routes matching requests to files in `12_Workflows/`.
- `Stop` validates the vault after a turn that used write-capable tools.

## Activate

1. Start a new Codex task from this vault root.
2. Open `/hooks` or the Hooks section in Codex settings.
3. Review the project-local definitions and trust them.
4. Confirm the project itself is trusted; untrusted projects do not load local hooks.

Never use `--dangerously-bypass-hook-trust` for normal work.
