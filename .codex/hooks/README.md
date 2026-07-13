# Codex hook handlers

## Purpose

Provide deterministic lifecycle glue between Codex and the vault workflows.

## What belongs here

Small standard-library Python handlers that consume Codex hook JSON from stdin and return documented JSON on stdout.

## What does not belong here

Network calls, model calls, transcript ingestion, secrets, destructive automation, or unattended edits to human/source notes.

## Writers

Human-governed. AI may modify handlers only under an explicit implementation request with tests and renewed hook trust.

## Examples

`codex_hook.py session-start` loads safe startup context; `codex_hook.py stop` runs deterministic validation.

## Runtime state

The handler stores only session identifiers, timestamps, routed workflow names, and dirty/validation flags under ignored `.codex/state/`. It never stores prompt bodies, assistant messages, tool output, or transcript contents.
