---
title: Visual Style Guide
type: style-guide
status: active
cssclasses: [second-brain]
---

# Visual Style Guide

The presentation layer makes dashboards scannable without becoming a second content format. Markdown carries meaning; CSS only enhances it.

## Principles

- Prefer headings, tables, lists, callouts, and wiki links.
- Use YAML `cssclasses: [second-brain]` on notes that need styled headings; add `sb-dashboard` only to navigational dashboards.
- Use small standalone HTML blocks. Never wrap Markdown sections in a `<div>`, because Obsidian may stop rendering the inner Markdown.
- Every HTML enhancement must leave nearby plain text that communicates the same meaning.
- Use theme variables, not hard-coded light/dark colors. Keep contrast, keyboard navigation, reduced motion, mobile width, and print output usable.
- Avoid emoji-heavy headings, decorative clutter, inline styles, JavaScript, remote fonts, and fragile theme-specific selectors.

## Reusable classes

```html
<div class="sb-banner sb-banner--blue"><strong>Message.</strong> Supporting text.</div>

<div class="sb-card-grid">
  <div class="sb-card"><strong>Title</strong><br>Short description.</div>
</div>

<span class="sb-badge sb-badge--review">Review required</span>
```

Available banner accents: `--blue`, `--green`, `--amber`, and `--red`. Badges support `--human`, `--machine`, and `--review`.

## Callout semantics

- `[!tip]`: next action or efficient path
- `[!info]`: context or provenance
- `[!warning]`: review or safety boundary
- `[!danger]`: destructive action, secret exposure, or external side effect

## Setup

Follow [[../.obsidian/README]]. The snippet is optional; never make a workflow depend on it.
