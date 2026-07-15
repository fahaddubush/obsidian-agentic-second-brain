# 12_Workflows

**Purpose:** Human-readable, agent-neutral operating procedures.

**What belongs:** Inputs, outputs, allowed paths, safety constraints, steps, agent prompts, and validation.

**What does not belong:** Background daemons, hidden automation, or generated results.

**Writers:** Both; AI may propose changes, and humans approve risky automation.

**Examples:** `project-ingestion.md`, `agentic-memory-reconciliation.md`, `full-codex-task-ingestion.md`, `weekly-review.md`.

`agentic-memory-reconciliation.md` handles incremental jobs created by global lifecycle hooks. `full-codex-task-ingestion.md` is the separate, explicit historical backfill for all available Codex tasks. They are complementary and must not be merged into one ambiguous workflow.
