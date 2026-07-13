---
type: decision
title: "Keep Raw Sources Immutable"
date: 2026-07-13
decision_status: accepted
ownership: shared
status: example
generated_by: setup
confidence: high
human_review_required: true
related_projects: ["[[03_Projects/Example Project/README|Example Project]]"]
---

<div class="sb-banner sb-decision">DECISION · accepted after human review</div>

# Keep Raw Sources Immutable

## Context

The system needs durable evidence that cannot be silently rewritten during synthesis.

## Decision

Files accepted into `07_Sources/` are read-only to AI. Corrections and interpretations are stored separately and linked back to the source.

## Consequences

- Provenance remains inspectable.
- Derived claims can be rechecked.
- Updating source metadata requires explicit human action.

## Alternatives considered

- Let agents normalize source bodies in place — rejected because it erases evidence.
