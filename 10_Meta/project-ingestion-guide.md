---
title: Project Ingestion Guide
type: procedure
status: active
---

# Project Ingestion Guide

Project ingestion builds memory about a project; it does not change the project.

## Required inspection

- Record source path, repository URL, branch, and commit/ref when available.
- Read README and documentation; map directories without indexing dependencies or build artifacts.
- Identify language, frameworks, dependency manifests, entry points, runtime, tests, deployment, and data stores.
- Trace evidence for architecture and active work.
- Flag stale, dead, fake, mock, duplicated, inconsistent, or undocumented material as candidates with confidence, not fact, unless verified.

## Required outputs

Create/update `03_Projects/<project>/` with context, goals, architecture, decisions, tasks, bugs, changelog, lessons, ingestion log, machine summaries, and audits. Also create a dated project audit, context pack, and token-saving brief in their `08_Machine` folders.

## Boundary

Do not run the project, install dependencies, change files, alter Git, or execute project scripts unless the human separately authorizes it. See [[../12_Workflows/project-ingestion]].
