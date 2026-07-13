#!/usr/bin/env python3
"""Safe command line companion for the Markdown second brain."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from datetime import date, datetime
from pathlib import Path

from vaultlib import (
    atomic_create,
    atomic_replace,
    confined,
    frontmatter_keys,
    iso_now,
    markdown_files,
    note_catalog,
    redact,
    resolve_link,
    sha256,
    slugify,
    vault_root,
    wikilinks,
    yaml_quote,
)


REQUIRED_DIRS = [
    "00_Inbox", "01_Daily", "02_Working-Memory", "03_Projects", "04_Knowledge",
    "05_Episodic-Memory/LLM-Sessions", "06_Procedural-Memory", "07_Sources",
    "08_Machine/Context-Packs", "08_Machine/Token-Saving-Briefs", "09_Archive",
    "10_Meta", "11_Templates", "12_Workflows",
]
REQUIRED_FILES = [
    "AGENTS.md", "CLAUDE.md", "GEMINI.md", "README.md", "index.md", "log.md",
    "10_Meta/agent-core.md", "10_Meta/safety-policy.md", "10_Meta/validation-checklist.md",
    "05_Episodic-Memory/LLM-Sessions/index.md",
]
MACHINE_FIELDS = {"generated_by", "confidence", "human_review_required"}
ADAPTERS = ("AGENTS.md", "CLAUDE.md", "GEMINI.md")
RUNTIME_README_EXCLUSIONS = (
    (".git",),
    (".github",),
    (".obsidian", "cache"),
    (".obsidian", "plugins"),
    (".obsidian", "themes"),
    (".codex", "state"),
)


def readme_required(relative: Path) -> bool:
    """Return false for application-managed/runtime directories."""
    parts = relative.parts
    if "__pycache__" in parts:
        return False
    return not any(parts[: len(prefix)] == prefix for prefix in RUNTIME_README_EXCLUSIONS)


def render_yaml(
    kind: str,
    title: str,
    ownership: str = "machine",
    extra: dict[str, object] | None = None,
) -> str:
    now = iso_now()
    text = (
        "---\n"
        f"type: {kind}\n"
        f"title: {yaml_quote(title)}\n"
        f"created: {yaml_quote(now)}\n"
        f"updated: {yaml_quote(now)}\n"
        f"ownership: {ownership}\n"
        "status: draft\n"
        "generated_by: second-brain-cli\n"
        "confidence: low\n"
        "human_review_required: true\n"
    )
    for key, value in (extra or {}).items():
        if isinstance(value, bool):
            rendered = str(value).lower()
        elif isinstance(value, list):
            rendered = "[]" if not value else "[" + ", ".join(yaml_quote(str(item)) for item in value) + "]"
        else:
            rendered = yaml_quote(str(value))
        text += f"{key}: {rendered}\n"
    return text + "---\n"


def command_validate(args: argparse.Namespace) -> int:
    root = vault_root(args.vault)
    errors: list[str] = []
    warnings: list[str] = []
    for relative in REQUIRED_DIRS:
        if not confined(root, relative).is_dir():
            errors.append(f"missing directory: {relative}")
    for relative in REQUIRED_FILES:
        if not confined(root, relative).is_file():
            errors.append(f"missing file: {relative}")

    for directory in root.rglob("*"):
        if not directory.is_dir():
            continue
        rel = directory.relative_to(root)
        if not readme_required(rel):
            continue
        if not (directory / "README.md").is_file():
            errors.append(f"folder lacks README.md: {rel.as_posix()}")

    for path in markdown_files(root):
        rel = path.relative_to(root).as_posix()
        if rel.startswith("08_Machine/") and path.name != "README.md":
            missing = MACHINE_FIELDS - frontmatter_keys(path)
            if missing:
                errors.append(f"machine note lacks {sorted(missing)}: {rel}")

    by_stem, by_path = note_catalog(root)
    for stem, paths in by_stem.items():
        if len(paths) > 1 and stem not in {"readme", "index"}:
            roots = {path.relative_to(root).parts[0] for path in paths}
            # A workflow and its note template intentionally share a task name.
            # All vault links to these files should use their full folder path.
            if roots == {"11_Templates", "12_Workflows"}:
                continue
            warnings.append(
                f"ambiguous title '{stem}': " + ", ".join(p.relative_to(root).as_posix() for p in paths)
            )
    for path in markdown_files(root):
        for target in wikilinks(path):
            if not resolve_link(target, by_stem, by_path):
                warnings.append(f"broken link in {path.relative_to(root).as_posix()}: [[{target}]]")

    payload = {"vault": str(root), "errors": errors, "warnings": warnings}
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"Vault: {root}")
        for item in errors:
            print(f"ERROR: {item}")
        for item in warnings:
            print(f"WARN: {item}")
        print(f"Result: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


def command_sync(args: argparse.Namespace) -> int:
    root = vault_root(args.vault)
    core = confined(root, "10_Meta/agent-core.md")
    expected = sha256(core)
    problems: list[str] = []
    pattern = re.compile(r"(?m)^core_sha256:\s*[^\n]*$")
    for adapter in ADAPTERS:
        path = confined(root, adapter)
        text = path.read_text(encoding="utf-8")
        match = pattern.search(text)
        current = match.group(0).split(":", 1)[1].strip().strip('"\'') if match else None
        if current != expected:
            problems.append(f"{adapter}: {current or 'missing'} != {expected}")
            if args.write:
                replacement = f"core_sha256: {expected}"
                updated = pattern.sub(replacement, text, count=1) if match else text.replace("---\n", f"---\n{replacement}\n", 1)
                atomic_replace(root, adapter, updated)
    if problems:
        print("Instruction drift detected:")
        print("\n".join(f"- {problem}" for problem in problems))
        if args.write:
            print("Adapter hashes updated. Shared prose was not rewritten.")
            return 0
        print("Re-run with --write only after reviewing agent-core.md.")
        return 1
    print(f"Instruction adapters match agent-core.md ({expected}).")
    return 0


def command_daily(args: argparse.Namespace) -> int:
    root = vault_root(args.vault)
    day = args.date or date.today().isoformat()
    daily = render_yaml("daily-note", day, "human") + f"\n<div class=\"sb-banner sb-daily\">Daily focus · {day}</div>\n\n# {day}\n\n## Focus\n\n- \n\n## Schedule\n\n- \n\n## Notes\n\n- \n\n## Shutdown\n\n- Wins: \n- Open loops: \n- Tomorrow: \n"
    working_title = f"{day} - Working Memory"
    working = render_yaml("working-memory", working_title, "human") + f"\n<div class=\"sb-banner sb-working\">Active context · {day}</div>\n\n# {working_title}\n\n## Current goal\n\n## Active tasks\n\n- [ ] \n\n## Decisions pending\n\n## Bugs and blockers\n\n## Context to preserve\n\n## Next action\n"
    planned = [
        (f"01_Daily/{day}.md", daily),
        (f"02_Working-Memory/{working_title}.md", working),
    ]
    existing = [relative for relative, _ in planned if confined(root, relative).exists()]
    if existing and not args.missing_only:
        raise FileExistsError("Refusing partial/overwrite daily creation; existing: " + ", ".join(existing))
    paths = [
        atomic_create(root, relative, content)
        for relative, content in planned
        if not confined(root, relative).exists()
    ]
    if not paths:
        print("Daily and working-memory notes already exist; nothing changed.")
        return 0
    print("Created:")
    for path in paths:
        print(f"- {path.relative_to(root).as_posix()}")
    return 0


def command_session(args: argparse.Namespace) -> int:
    root = vault_root(args.vault)
    day = args.date or date.today().isoformat()
    title = args.title.strip()
    agent_key = args.agent.casefold()
    folder = {"codex": "Codex", "claude": "Claude", "gemini": "Gemini"}.get(agent_key, "Other")
    relative = f"05_Episodic-Memory/LLM-Sessions/{folder}/{day[:4]}/{day} - {title}.md"
    content = render_yaml(
        "llm-session-summary",
        title,
        extra={"agent": args.agent, "model": args.model or "unknown", "project": args.project or "unknown"},
    ) + (
        "\n<div class=\"sb-banner sb-session\">LLM session memory · review required</div>\n"
        f"\n# {title}\n\n## Original user request\n\nunknown\n\n## Session goal\n\nunknown\n\n"
        "## Final outcome\n\nunknown\n\n## Files inspected\n\n- unknown\n\n## Files modified\n\n- unknown\n\n"
        "## Commands run\n\n- unknown\n\n## Important decisions\n\n- unknown\n\n## Assumptions made\n\n- unknown\n\n"
        "## Errors and fixes\n\n- unknown\n\n## Unresolved issues\n\n- unknown\n\n## Next actions\n\n- [ ] unknown\n\n"
        "## Reusable context for future chats\n\nunknown\n\n## Related notes and projects\n\n- unknown\n"
    )
    path = atomic_create(root, relative, content)
    index = confined(root, "05_Episodic-Memory/LLM-Sessions/index.md")
    link = f"- [[{Path(relative).with_suffix('').as_posix()}|{day} · {args.agent} · {title}]]\n"
    index_text = index.read_text(encoding="utf-8")
    if link not in index_text:
        atomic_replace(root, index.relative_to(root), index_text.rstrip() + "\n" + link)
    print(f"Created {path.relative_to(root).as_posix()}")
    print("Unknown fields were deliberately left unknown for evidence-based completion.")
    return 0


def graph_findings(root: Path) -> dict[str, object]:
    by_stem, by_path = note_catalog(root)
    incoming: Counter[Path] = Counter()
    broken: list[dict[str, str]] = []
    ambiguous: list[dict[str, object]] = []
    for source in markdown_files(root):
        for target in wikilinks(source):
            matches = resolve_link(target, by_stem, by_path)
            if not matches:
                broken.append({"source": source.relative_to(root).as_posix(), "target": target})
            elif len(matches) > 1:
                ambiguous.append({"source": source.relative_to(root).as_posix(), "target": target, "matches": [p.relative_to(root).as_posix() for p in matches]})
            else:
                incoming[matches[0]] += 1
    orphans = [p.relative_to(root).as_posix() for p in markdown_files(root) if p.name != "README.md" and incoming[p] == 0]
    return {"broken": broken, "ambiguous": ambiguous, "orphans": sorted(orphans)}


def command_graph(args: argparse.Namespace) -> int:
    root = vault_root(args.vault)
    findings = graph_findings(root)
    stamp = datetime.now().astimezone().strftime("%Y-%m-%d %H%M%S")
    title = f"{stamp} - Graph Audit"
    body = render_yaml("graph-audit", title) + f"\n# {title}\n\nThis report is read-only analysis; it does not insert or repair links.\n\n"
    for heading, key in (("Broken links", "broken"), ("Ambiguous links", "ambiguous"), ("Orphan notes", "orphans")):
        body += f"## {heading}\n\n"
        values = findings[key]
        body += "\n".join(f"- `{redact(json.dumps(item, ensure_ascii=False))}`" for item in values) if values else "- None detected"
        body += "\n\n"
    path = atomic_create(root, f"08_Machine/Link-Suggestions/{title}.md", body)
    print(f"Created {path.relative_to(root).as_posix()}")
    return 0


def source_hashes(root: Path) -> dict[str, str]:
    source_root = confined(root, "07_Sources")
    return {
        path.relative_to(root).as_posix(): sha256(path)
        for path in source_root.rglob("*")
        if path.is_file() and path.name != "README.md"
    }


def command_sources(args: argparse.Namespace) -> int:
    root = vault_root(args.vault)
    manifest_path = confined(root, "08_Machine/Reports/source-integrity.json")
    current = source_hashes(root)
    if args.write:
        content = json.dumps({"generated_at": iso_now(), "algorithm": "sha256", "files": current}, indent=2) + "\n"
        if manifest_path.exists():
            atomic_replace(root, manifest_path.relative_to(root), content)
        else:
            atomic_create(root, manifest_path.relative_to(root), content)
        print(f"Wrote {manifest_path.relative_to(root).as_posix()} ({len(current)} source files).")
        return 0
    if not manifest_path.exists():
        print("No manifest. Run `sources --write` after accepting raw sources.")
        return 1
    expected = json.loads(manifest_path.read_text(encoding="utf-8")).get("files", {})
    changed = sorted(key for key in set(expected) & set(current) if expected[key] != current[key])
    added = sorted(set(current) - set(expected))
    missing = sorted(set(expected) - set(current))
    for label, values in (("CHANGED", changed), ("ADDED", added), ("MISSING", missing)):
        for value in values:
            print(f"{label}: {value}")
    print(f"Result: {len(changed)} changed, {len(added)} added, {len(missing)} missing.")
    return 1 if changed or missing else 0


STACK_MARKERS = {
    "package.json": "Node.js/JavaScript", "pyproject.toml": "Python", "requirements.txt": "Python",
    "Cargo.toml": "Rust", "go.mod": "Go", "pom.xml": "Java/Maven", "build.gradle": "Java/Gradle",
    "*.sln": ".NET", "*.csproj": ".NET", "Dockerfile": "Docker",
}


def project_inventory(project: Path) -> tuple[list[str], list[str], list[str]]:
    files: list[str] = []
    ignored = {".git", "node_modules", ".venv", "venv", "dist", "build", "__pycache__"}
    for path in project.rglob("*"):
        if any(part in ignored for part in path.relative_to(project).parts):
            continue
        if path.is_file():
            files.append(path.relative_to(project).as_posix())
        if len(files) >= 5000:
            break
    stacks = sorted({stack for marker, stack in STACK_MARKERS.items() if any(Path(item).match(marker) for item in files)})
    entrypoints = [item for item in files if Path(item).name.casefold() in {"main.py", "app.py", "index.js", "index.ts", "main.rs", "main.go", "program.cs", "manage.py"}]
    return files, stacks, entrypoints


def command_ingest(args: argparse.Namespace) -> int:
    root = vault_root(args.vault)
    project = Path(args.project_path).expanduser().resolve()
    if not project.is_dir():
        raise ValueError(f"Project does not exist: {project}")
    if root == project or root in project.parents:
        raise ValueError("Refusing to ingest the vault as an external project")
    files, stacks, entrypoints = project_inventory(project)
    name = args.name or project.name
    slug = slugify(name)
    stamp = datetime.now().astimezone().strftime("%Y-%m-%d %H%M%S")
    top = sorted({item.split("/", 1)[0] for item in files})
    audit_title = f"{stamp} - {name} Project Audit"
    audit = render_yaml("project-audit", audit_title, extra={"project": name, "source_path": str(project)}) + (
        f"\n# {audit_title}\n\n> [!warning] Review required\n> This deterministic inventory does not claim semantic understanding of the code.\n\n"
        f"## Detected stack\n\n{chr(10).join('- ' + s for s in stacks) or '- unknown'}\n\n"
        f"## Candidate entry points\n\n{chr(10).join('- `' + e + '`' for e in entrypoints) or '- unknown'}\n\n"
        f"## Top-level structure\n\n{chr(10).join('- `' + e + '`' for e in top)}\n\n"
        f"## Inventory\n\n- Files observed: {len(files)}{' (scan capped)' if len(files) >= 5000 else ''}\n"
        "- Dependencies, architecture, stale code, mocks, and inconsistencies require agent review.\n\n## Required follow-up\n\n- [ ] Read README and documentation.\n- [ ] Inspect dependency manifests.\n- [ ] Trace entry points and architecture.\n- [ ] Search for stale, mock, fake, or dead code with evidence.\n- [ ] Record decisions and missing documentation.\n"
    )
    audit_path = atomic_create(root, f"08_Machine/Project-Audits/{audit_title}.md", audit)
    context_title = f"{name} Context Pack"
    context = render_yaml(
        "context-pack",
        context_title,
        extra={"project": name, "last_updated": iso_now(), "stale_after": "unknown", "source_session_summaries": []},
    ) + f"\n# {context_title}\n\n## Purpose\n\nStart or resume work on {name}.\n\n## Compressed summary\n\nDeterministic first-pass ingestion only; semantic review remains pending.\n\n## Current state\n\n- Stack signals: {', '.join(stacks) or 'unknown'}\n- Candidate entry points: {', '.join(entrypoints) or 'unknown'}\n\n## Key decisions\n\n- unknown\n\n## Important files\n\n- See [[{audit_path.relative_to(root).with_suffix('').as_posix()}]]\n\n## Common commands\n\n- unknown\n\n## Known issues\n\n- unknown\n\n## Next actions\n\n- [ ] Complete semantic project audit.\n"
    context_path = atomic_create(root, f"08_Machine/Context-Packs/{slug} - context-pack - {stamp}.md", context)
    brief_title = f"{name} Startup Brief"
    brief = render_yaml(
        "token-saving-brief",
        brief_title,
        extra={"project": name, "source_context_pack": context_path.relative_to(root).as_posix()},
    ) + f"\n# {brief_title}\n\nRead [[{context_path.relative_to(root).with_suffix('').as_posix()}]] before full notes. First pass only: verify README, stack, entry points, architecture, tasks, and decisions. Do not modify `{project}` unless explicitly asked.\n"
    brief_path = atomic_create(root, f"08_Machine/Token-Saving-Briefs/{slug} - startup - {stamp}.md", brief)
    print("Created read-only ingestion outputs:")
    for path in (audit_path, context_path, brief_path):
        print(f"- {path.relative_to(root).as_posix()}")
    return 0


def run_git(project: Path, *arguments: str) -> str:
    result = subprocess.run(["git", "-C", str(project), *arguments], check=True, capture_output=True, text=True, timeout=30)
    return redact(result.stdout.strip())


def command_git_diff(args: argparse.Namespace) -> int:
    root = vault_root(args.vault)
    project = Path(args.project_path).expanduser().resolve()
    name = args.name or project.name
    status = run_git(project, "status", "--short") or "clean"
    names = run_git(project, "diff", "--name-status", args.base) or "none"
    stat = run_git(project, "diff", "--stat", args.base) or "none"
    stamp = datetime.now().astimezone().strftime("%Y-%m-%d %H%M%S")
    title = f"{stamp} - {name} Git Diff Review"
    body = render_yaml("git-diff-review", title, extra={"project": name, "base": args.base}) + f"\n# {title}\n\nThis captures metadata, not full diff content. Review for secrets before sharing.\n\n## Working tree\n\n```text\n{status}\n```\n\n## Changed paths\n\n```text\n{names}\n```\n\n## Diff stat\n\n```text\n{stat}\n```\n\n## Review\n\n- [ ] Explain intent.\n- [ ] Check tests and docs.\n- [ ] Check secrets and generated artifacts.\n- [ ] Record decisions or unresolved issues.\n"
    path = atomic_create(root, f"08_Machine/Reports/{title}.md", body)
    print(f"Created {path.relative_to(root).as_posix()}")
    return 0


def parser() -> argparse.ArgumentParser:
    root_parser = argparse.ArgumentParser(description=__doc__)
    root_parser.add_argument("--vault", help="Vault root (defaults to the parent of scripts/)")
    sub = root_parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="Read-only structural and link validation")
    validate.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    validate.set_defaults(func=command_validate)

    sync = sub.add_parser("instruction-sync", help="Check canonical instruction hash in adapters")
    sync.add_argument("--write", action="store_true", help="Update adapter hash sentinels after review")
    sync.set_defaults(func=command_sync)

    daily = sub.add_parser("daily", help="Create today's daily and working-memory notes without overwrite")
    daily.add_argument("--date", help="ISO date (default: local today)")
    daily.add_argument(
        "--missing-only",
        action="store_true",
        help="Create only missing notes; never replace an existing daily or working-memory note",
    )
    daily.set_defaults(func=command_daily)

    session = sub.add_parser("session", help="Create an evidence-safe LLM session summary scaffold")
    session.add_argument("--agent", required=True, help="Codex, Claude, Gemini, or another tool")
    session.add_argument("--title", required=True)
    session.add_argument("--model")
    session.add_argument("--project")
    session.add_argument("--date", help="ISO date (default: local today)")
    session.set_defaults(func=command_session)

    graph = sub.add_parser("graph-audit", help="Create a read-only broken-link/orphan report")
    graph.set_defaults(func=command_graph)

    sources = sub.add_parser("sources", help="Check or explicitly refresh raw-source SHA-256 manifest")
    sources.add_argument("--write", action="store_true", help="Create/update the machine-owned manifest")
    sources.set_defaults(func=command_sources)

    ingest = sub.add_parser("project-ingest", help="Inventory an external project without modifying it")
    ingest.add_argument("project_path")
    ingest.add_argument("--name")
    ingest.set_defaults(func=command_ingest)

    diff = sub.add_parser("git-diff", help="Capture safe Git change metadata into a review note")
    diff.add_argument("project_path")
    diff.add_argument("--name")
    diff.add_argument("--base", default="HEAD", help="Git revision to compare (default: HEAD)")
    diff.set_defaults(func=command_git_diff)
    return root_parser


def main() -> int:
    args = parser().parse_args()
    try:
        return int(args.func(args))
    except (ValueError, FileExistsError, subprocess.SubprocessError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
