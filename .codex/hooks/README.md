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

Project validation flags remain under ignored `.codex/state/`. Global lifecycle evidence is redacted and appended to the private SQLite journal at `~/.codex/second-brain/brain.db`, outside the public repository. The handler queues idempotent work; semantic extraction is performed later by the reviewed reconciliation workflow.
