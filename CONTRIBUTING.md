# Contributing

Thank you for helping improve Agentic Second Brain.

## Before opening a change

1. Read `AGENTS.md` and `10_Meta/agent-core.md`.
2. Keep raw source payloads under `07_Sources/` immutable.
3. Do not include personal notes, credentials, transcripts, local certificates, or machine-specific paths.
4. Put generated analysis in `08_Machine/` and label provenance and review requirements.
5. Keep the durable layer compatible with ordinary Markdown and Obsidian.

## Development

Python 3.11 or newer is recommended; there are no runtime package dependencies.

```bash
python -m py_compile scripts/vaultlib.py scripts/sb.py .codex/hooks/codex_hook.py
python -m unittest discover -s tests -v
python scripts/sb.py validate
python scripts/sb.py instruction-sync
python scripts/sb.py sources
```

## Pull requests

- Keep each pull request focused and explain the user-facing outcome.
- Add regression tests for behavior changes.
- Preserve no-overwrite and path-confinement guarantees.
- Update documentation when a command, hook, schema, template, or workflow changes.
- Do not weaken source protection, secret handling, or human-review boundaries.
- Confirm that no private vault content is present in the diff.

By contributing, you agree that your contribution is licensed under the MIT License.
