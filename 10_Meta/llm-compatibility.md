---
title: LLM CLI Compatibility
type: architecture
status: active
---

# LLM CLI Compatibility

`10_Meta/agent-core.md` is agent-neutral and canonical.

| Tool | Root file | Loading approach |
|---|---|---|
| Codex/general agents | `AGENTS.md` | Critical rules are mirrored; read core directly. |
| Claude Code | `CLAUDE.md` | Uses Claude’s `@path` import for the core. |
| Gemini CLI | `GEMINI.md` | Uses Gemini’s `@path` import for the core. |
| Future agents | Their documented root context file | Point to core and mirror safety rules if imports are unsupported. |

Shared-rule changes begin in core and update all three adapters together. Tool-only behavior remains in its adapter. Keep adapters concise to avoid consuming context, and use the brief → pack → full-note loading order.

Do not assume a CLI automatically discovers files outside its documented scope. Confirm the tool’s effective instructions before risky work.
