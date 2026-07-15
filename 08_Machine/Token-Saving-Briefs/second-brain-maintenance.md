---
type: token-saving-brief
title: "Second Brain Maintenance"
purpose: "Maintain the vault with minimum safe context"
last_updated: 2026-07-15
ownership: machine
status: seed
generated_by: setup
confidence: high
human_review_required: true
source_context_pack: "[[08_Machine/Context-Packs/obsidian-second-brain]]"
---

<div class="sb-brief">START HERE · VAULT MAINTENANCE</div>

# Second Brain Maintenance

Read [[10_Meta/agent-core]] and [[08_Machine/Context-Packs/obsidian-second-brain]]. Preserve raw sources and human notes. Global hooks append redacted evidence to `~/.codex/second-brain/brain.db`; the hourly worker reconciles queued jobs through the installed skill and bounded agents. Check runtime health with `python scripts/brain_runtime.py doctor --repair --json`. If shared rules change, update the canonical core first, synchronize all three adapters, run `python scripts/sb.py instruction-sync --write`, then validate and review the diff.
