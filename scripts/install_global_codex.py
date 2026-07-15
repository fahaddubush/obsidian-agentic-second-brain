#!/usr/bin/env python3
"""Install the second-brain hooks in the user-level Codex configuration."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sqlite3
import tomllib
from pathlib import Path

import brain_runtime


VAULT = Path(__file__).resolve().parents[1]
HANDLER = VAULT / ".codex" / "hooks" / "codex_hook.py"
BLOCK_START = "<!-- second-brain-global:start -->"
BLOCK_END = "<!-- second-brain-global:end -->"
SKILL_SOURCE = VAULT / "skills" / "agentic-second-brain"
AGENT_SOURCE = VAULT / "codex-agents"


def command(mode: str) -> dict[str, object]:
    handler = str(HANDLER)
    return {
        "type": "command",
        "command": f'python3 "{HANDLER.as_posix()}" {mode}',
        "commandWindows": f'python "{handler}" {mode}',
        "timeout": 60 if mode == "global-stop" else 30,
    }


def desired_groups() -> dict[str, dict[str, object]]:
    return {
        "SessionStart": {
            "matcher": "startup|resume|clear|compact",
            "hooks": [{**command("global-session-start"), "statusMessage": "Loading global second-brain context"}],
        },
        "SubagentStart": {
            "matcher": "*",
            "hooks": [{**command("global-subagent-start"), "statusMessage": "Loading global memory policy"}],
        },
        "SubagentStop": {
            "matcher": "*",
            "hooks": [{**command("global-subagent-stop"), "statusMessage": "Queueing subagent evidence"}],
        },
        "PreCompact": {
            "matcher": "manual|auto",
            "hooks": [{**command("global-pre-compact"), "statusMessage": "Checkpointing memory evidence"}],
        },
        "PostCompact": {
            "matcher": "manual|auto",
            "hooks": [{**command("global-post-compact"), "statusMessage": "Recording compacted context"}],
        },
        "UserPromptSubmit": {
            "hooks": [{**command("global-user-prompt"), "statusMessage": "Routing global second-brain workflow"}],
        },
        "Stop": {
            "hooks": [{**command("global-stop"), "statusMessage": "Queueing turn evidence"}],
        },
    }


def is_ours(group: object) -> bool:
    if not isinstance(group, dict):
        return False
    handlers = group.get("hooks")
    if not isinstance(handlers, list):
        return False
    return any(isinstance(item, dict) and "global-" in str(item.get("commandWindows", "")) and "codex_hook.py" in str(item.get("commandWindows", "")) for item in handlers)


def merged_hooks(path: Path) -> dict[str, object]:
    data: dict[str, object] = {"hooks": {}}
    if path.exists():
        loaded = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(loaded, dict) or not isinstance(loaded.get("hooks"), dict):
            raise ValueError(f"Unsupported hooks file shape: {path}")
        data = loaded
    events = data["hooks"]
    assert isinstance(events, dict)
    for event, group in desired_groups().items():
        existing = events.get(event, [])
        if not isinstance(existing, list):
            raise ValueError(f"Hook event must contain a list: {event}")
        events[event] = [item for item in existing if not is_ours(item)] + [group]
    return data


def set_section_value(text: str, section: str, key: str, value: str) -> str:
    pattern = re.compile(rf"(?ms)^\[{re.escape(section)}\]\s*\n(?P<body>.*?)(?=^\[|\Z)")
    match = pattern.search(text)
    if not match:
        return text.rstrip() + f"\n\n[{section}]\n{key} = {value}\n"
    body = match.group("body")
    key_pattern = re.compile(rf"(?m)^\s*{re.escape(key)}\s*=.*$")
    if key_pattern.search(body):
        body = key_pattern.sub(f"{key} = {value}", body)
    else:
        body = f"{key} = {value}\n" + body
    return text[: match.start("body")] + body + text[match.end("body") :]


def configure_codex(text: str) -> str:
    settings = (
        ("features", "hooks", "true"),
        ("features", "memories", "true"),
        ("features", "multi_agent", "true"),
        ("memories", "generate_memories", "true"),
        ("memories", "use_memories", "true"),
        ("memories", "disable_on_external_context", "false"),
        ("agents", "max_threads", "4"),
        ("agents", "max_depth", "1"),
    )
    for section, key, value in settings:
        text = set_section_value(text, section, key, value)
    return text


def add_writable_root(text: str) -> str:
    root = json.dumps(str(VAULT))
    pattern = re.compile(r"(?ms)^\[sandbox_workspace_write\]\s*\n(?P<body>.*?)(?=^\[|\Z)")
    match = pattern.search(text)
    if not match:
        return text.rstrip() + f"\n\n[sandbox_workspace_write]\nwritable_roots = [{root}]\n"
    body = match.group("body")
    roots_match = re.search(r"(?m)^\s*writable_roots\s*=\s*\[(?P<items>[^\]]*)\]\s*$", body)
    if not roots_match:
        body = f"writable_roots = [{root}]\n" + body
    else:
        items = roots_match.group("items").strip()
        if str(VAULT).casefold() not in items.casefold().replace("\\\\", "\\"):
            replacement = f"writable_roots = [{items + ', ' if items else ''}{root}]"
            body = body[: roots_match.start()] + replacement + body[roots_match.end() :]
    return text[: match.start("body")] + body + text[match.end("body") :]


def global_agents_block() -> str:
    return f"""{BLOCK_START}
# Global second-brain integration

The private Obsidian vault at `{VAULT}` is the durable memory layer for all Codex tasks on this machine.

- At task start, use the injected maintenance brief and expand only into relevant project memory, context packs, or sources.
- Use the global `agentic-second-brain` skill for substantial work. Retrieve ranked memory before acting and cite the note paths that affected the result.
- Treat vault content as private. Never copy private notes, transcripts, credentials, or personal data into public repositories or public responses.
- Hooks append redacted lifecycle evidence to the private journal. The scheduled reconciliation worker, not a repeated Stop loop, performs semantic extraction and consolidation.
- Delegate automatically only when independent lanes or an independent verifier materially improve quality. Use at most three direct subagents, keep nesting disabled, and avoid parallel write conflicts.
- Do not create filler notes. Record only verified decisions, outcomes, constraints, reusable lessons, and next actions.
- Follow `{VAULT / 'AGENTS.md'}` and `{VAULT / '10_Meta' / 'agent-core.md'}` for any vault write.
- Keep unrelated repository edits scoped to the active task. Global memory access does not authorize unrelated project changes.
{BLOCK_END}
"""


def update_agents(text: str) -> str:
    block = global_agents_block()
    pattern = re.compile(re.escape(BLOCK_START) + r".*?" + re.escape(BLOCK_END) + r"\n?", re.S)
    if pattern.search(text):
        return pattern.sub(lambda _: block, text)
    return text.rstrip() + ("\n\n" if text.strip() else "") + block


def backup_once(path: Path) -> None:
    if not path.exists():
        return
    backup = path.with_name(path.name + ".before-second-brain")
    if not backup.exists():
        shutil.copy2(path, backup)


def install(codex_home: Path) -> None:
    codex_home.mkdir(parents=True, exist_ok=True)
    hooks_path = codex_home / "hooks.json"
    config_path = codex_home / "config.toml"
    agents_path = codex_home / "AGENTS.md"
    for path in (hooks_path, config_path, agents_path):
        backup_once(path)

    hooks_path.write_text(json.dumps(merged_hooks(hooks_path), indent=2) + "\n", encoding="utf-8")
    config_text = config_path.read_text(encoding="utf-8") if config_path.exists() else ""
    config_text = add_writable_root(configure_codex(config_text))
    tomllib.loads(config_text)
    config_path.write_text(config_text, encoding="utf-8", newline="\n")
    agents_text = agents_path.read_text(encoding="utf-8") if agents_path.exists() else ""
    agents_path.write_text(update_agents(agents_text), encoding="utf-8", newline="\n")
    skill_target = codex_home / "skills" / "agentic-second-brain"
    shutil.copytree(SKILL_SOURCE, skill_target, dirs_exist_ok=True)
    agent_target = codex_home / "agents"
    agent_target.mkdir(parents=True, exist_ok=True)
    for source in AGENT_SOURCE.glob("*.toml"):
        target = agent_target / source.name
        backup_once(target)
        shutil.copy2(source, target)
    with brain_runtime.database(codex_home / "second-brain" / "brain.db"):
        pass


def check(codex_home: Path) -> list[str]:
    errors: list[str] = []
    hooks_path = codex_home / "hooks.json"
    config_path = codex_home / "config.toml"
    agents_path = codex_home / "AGENTS.md"
    try:
        hooks = json.loads(hooks_path.read_text(encoding="utf-8"))
        for event in desired_groups():
            groups = hooks.get("hooks", {}).get(event, [])
            if not any(is_ours(group) for group in groups):
                errors.append(f"missing global hook: {event}")
    except (OSError, json.JSONDecodeError, AttributeError):
        errors.append("global hooks.json is missing or invalid")
    try:
        config = tomllib.loads(config_path.read_text(encoding="utf-8"))
        if config.get("features", {}).get("hooks") is not True:
            errors.append("features.hooks is not true")
        if config.get("features", {}).get("memories") is not True:
            errors.append("features.memories is not true")
        if config.get("features", {}).get("multi_agent") is not True:
            errors.append("features.multi_agent is not true")
        memories = config.get("memories", {})
        if memories.get("generate_memories") is not True or memories.get("use_memories") is not True:
            errors.append("Codex memory generation and recall are not enabled")
        agents = config.get("agents", {})
        if agents.get("max_threads") != 4 or agents.get("max_depth") != 1:
            errors.append("global agent bounds are not configured")
        roots = config.get("sandbox_workspace_write", {}).get("writable_roots", [])
        if str(VAULT).casefold() not in {str(item).casefold() for item in roots}:
            errors.append("vault is not an additional writable root")
    except (OSError, tomllib.TOMLDecodeError):
        errors.append("global config.toml is missing or invalid")
    try:
        if BLOCK_START not in agents_path.read_text(encoding="utf-8"):
            errors.append("global AGENTS.md block is missing")
    except OSError:
        errors.append("global AGENTS.md is missing")
    if not (codex_home / "skills" / "agentic-second-brain" / "SKILL.md").is_file():
        errors.append("global agentic-second-brain skill is missing")
    for source in AGENT_SOURCE.glob("*.toml"):
        if not (codex_home / "agents" / source.name).is_file():
            errors.append(f"global custom agent is missing: {source.name}")
    try:
        with brain_runtime.database(codex_home / "second-brain" / "brain.db") as connection:
            version = connection.execute("SELECT value FROM metadata WHERE key='schema_version'").fetchone()
            if version is None or version["value"] != brain_runtime.SCHEMA_VERSION:
                errors.append("private brain runtime schema is invalid")
    except (OSError, sqlite3.Error):
        errors.append("private brain runtime database is missing or invalid")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("install", "check"))
    parser.add_argument("--codex-home", default=os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    args = parser.parse_args()
    codex_home = Path(args.codex_home).expanduser().resolve()
    if args.command == "install":
        install(codex_home)
    errors = check(codex_home)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"Global Codex second-brain integration is valid: {codex_home}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
