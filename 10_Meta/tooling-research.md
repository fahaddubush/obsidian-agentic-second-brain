---
title: Verified Tooling Research
type: research
status: active
researched_on: 2026-07-13
human_review_required: true
---

# Verified Tooling Research

This is a dated evaluation, not an installation manifest. Re-check releases, permissions, and documentation before enabling anything.

## Recommended baseline

Use Obsidian, its core Search/Backlinks/Outgoing Links/Graph View, a private Git repository, and direct filesystem access from Codex, Claude Code, and Gemini CLI. Add one retrieval or agent layer only after the plain wiki shows a measured need.

## Real and dependable

| Tool | Classification | Fit and boundary |
|---|---|---|
| [Karpathy’s LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) | Architecture source | Defines raw sources + maintained Markdown wiki + schema/instructions. It is a pattern, not an installable product. |
| Obsidian [Search](https://obsidian.md/help/plugins/search), [Backlinks](https://obsidian.md/help/plugins/backlinks), [Outgoing Links](https://obsidian.md/help/plugins/outgoing-links), [Graph View](https://obsidian.md/help/plugins/graph) | Stable baseline | Local, built-in retrieval and link traversal; use before embeddings. Graph View visualizes links and is not a reasoning engine. |
| [Local REST API](https://github.com/coddingtonbear/obsidian-local-rest-api) | Mature optional integration | REST plus a built-in Streamable HTTP MCP endpoint, live metadata/state, search, file actions, and commands. Enable only for live Obsidian access; keep loopback-only and protect its bearer token. |
| [QMD](https://github.com/tobi/qmd) | Mature optional phase-two search | Cross-CLI local BM25, embeddings, expansion, reranking, CLI, and MCP. Portable across agents, but unnecessary until vault scale defeats curated indexes/core search. |
| [Smart Connections](https://github.com/brianpetro/obsidian-smart-connections) | Established optional discovery | Useful for in-Obsidian related-note suggestions. Treat rankings as discovery aids, not durable memory or truth. |
| [Obsidian Copilot](https://github.com/logancyang/obsidian-copilot) | Established chat/search; agent mode separate | Suitable if in-vault chat is desired. Evaluate new autonomous agent capabilities separately and confirm configured providers/privacy. |

## Real but experimental for this vault

| Tool | Why defer |
|---|---|
| [Local REST API Second Brain MCP Extension](https://community.obsidian.md/plugins/local-rest-api-second-brain-mcp-extension) | Real local embeddings plus semantic-root selection and BFS over links/backlinks, but young. Pilot on a test vault; prefer the pure-JavaScript build initially. |
| [Vault Operator](https://github.com/pssah4/vault-operator) (formerly “Obsilo Agent”) | Capable agent loop with retrieval, MCP, approvals, shadow-Git checkpoints, and protected paths, but broad permissions and fast-moving behavior. Its [privacy policy](https://github.com/pssah4/vault-operator/blob/main/PRIVACY.md) notes provider data flow and possible plaintext setting fallback. |
| [obsidian-second-brain](https://github.com/eugeniughelbur/obsidian-second-brain) | Genuine cross-CLI framework for Codex, Claude, Gemini, and others, but its scheduled reconciliation/self-rewriting conflicts with protected human notes. Borrow patterns, not the full automation, initially. Review its [security policy](https://github.com/eugeniughelbur/obsidian-second-brain/blob/main/SECURITY.md). |
| [Second Brain community plugin](https://community.obsidian.md/plugins/second-brain) | Implements raw-to-wiki compilation and semantic chat but is young and would compete with this vault’s schema/generated folders. |

## Avoid in the initial setup

- Old REST-to-MCP proxy wrappers: Local REST API now includes MCP directly.
- Multiple simultaneous embedding/indexing plugins: duplicated caches, compute, storage, and inconsistent rankings.
- Cloud “second brain” services as another source of truth for a local-first vault.
- Autonomous nightly rewriting of human notes or automatic contradiction resolution.
- Unpinned `curl | bash` or `npx ...@latest` production installs.
- Any REST/MCP endpoint exposed beyond `127.0.0.1`.

## Metaphors, not tools

- Episodic, semantic, procedural, working, and long-term “memory” are folder/workflow classifications.
- “Dreaming” is a scheduled synthesis report in `08_Machine`, not background learning.
- “The agent learns the vault” means Markdown/index/state changes, not model-weight training.
- Obsidian Graph View is link visualization, not a typed knowledge graph or logical inference engine.
- Embeddings estimate similarity; they do not provide provenance, truth, or understanding.
- “Autonomous” means repeated model/tool steps, not correctness or safe unattended operation.

## Security gates

Imported notes and code are untrusted prompt-injection surfaces. Local plugins may still transmit note text to cloud model/embedding providers. Generated databases and model files stay untracked. REST/MCP delete, overwrite, move, and command tools require explicit approval. Git provides audit/recovery, not secret removal.

## Adoption sequence

1. Plain vault + Obsidian core + Git + direct filesystem agents.
2. Local REST API built-in MCP only if live app state/commands are needed.
3. QMD **or** one semantic discovery layer after a measured retrieval problem.
4. Autonomous agent plugins only in a test copy with approvals, protected paths, backups, and a privacy review.
