---
title: Tag Taxonomy
type: schema
status: active
---

# Tag Taxonomy

Use few, controlled, lowercase hierarchical tags. Prefer front matter arrays.

| Family | Allowed examples | Purpose |
|---|---|---|
| `type/` | `concept`, `project`, `decision`, `session`, `source`, `procedure`, `report`, `brief` | What the note is |
| `status/` | `inbox`, `active`, `blocked`, `draft`, `review`, `complete`, `archived` | Workflow state |
| `area/` | `coding`, `university`, `research`, `career`, `homelab`, `personal` | Durable responsibility |
| `source/` | `article`, `book`, `pdf`, `transcript`, `video`, `web`, `codebase` | Source medium |
| `review/` | `human-required`, `verified`, `rejected` | Review state |

Do not encode projects as ad-hoc tags when a `project` property and wiki link are clearer. Add a taxonomy value only after repeated need; document it here first.
