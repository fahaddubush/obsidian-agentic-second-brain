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

Codex discovers project hooks from the active Codex project root. If Codex opens `Project #3`, it will not discover this nested `.codex` directory by itself. This workspace therefore has a local adapter at `Project #3/.codex` that points back to this reviewed handler.

1. Close existing tasks that were opened before the adapter existed.
2. Restart Codex so project configuration is rescanned.
3. Open a new task using `C:\Users\slopp\Desktop\Projects\Project #3` as the project.
4. Run `python second-brain\scripts\sb.py hooks-check --project-root "."` from the parent project terminal.
5. Open Settings, then Hooks.
6. Review and trust the project-local definitions.
7. Start one more new task if Codex requests it after trust is granted.

Alternatively, add `C:\Users\slopp\Desktop\Projects\Project #3\second-brain` as its own Codex project and use the repository-local hook files directly.

Never use `--dangerously-bypass-hook-trust` for normal work.
