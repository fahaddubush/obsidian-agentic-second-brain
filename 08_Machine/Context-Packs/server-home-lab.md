---
type: context-pack
title: "Server and Home Lab"
purpose: "Resume infrastructure work without exposing secrets"
last_updated: 2026-07-13
stale_after: unknown
ownership: machine
status: seed
generated_by: setup
confidence: low
human_review_required: true
source_session_summaries: []
---

<div class="sb-card sb-infra"><strong>SERVER / HOME LAB</strong><br>Topology notes belong here; credentials do not.</div>

# Server and Home Lab

## When to use

Before maintenance, troubleshooting, upgrades, or architecture work.

## Compressed summary and current state

Hosts, networks, services, versions, and backups are unknown.

## Key decisions

- Store secret references, never secret values.
- Commands that alter infrastructure require explicit approval.

## Important files

- Procedures belong in `06_Procedural-Memory/`.
- Incident sessions belong in `05_Episodic-Memory/Work-Sessions/`.

## Known issues

- This seed is not an operational runbook.

## Next actions

- [ ] Document non-sensitive topology.
- [ ] Add a tested backup procedure.
