"""Shared, dependency-free helpers for the second-brain command line tools."""

from __future__ import annotations

import hashlib
import os
import re
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Iterable


WIKILINK_RE = re.compile(r"(?<!!)\[\[([^\]]+)\]\]")
FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
SECRET_RE = re.compile(
    r"(?i)(api[_-]?key|token|secret|password|authorization)\s*[:=]\s*([^\s,;]+)"
)


def vault_root(value: str | Path | None = None) -> Path:
    """Return a resolved vault root; by default, the parent of this script folder."""
    root = Path(value).expanduser() if value else Path(__file__).resolve().parents[1]
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f"Vault does not exist: {root}")
    return root


def confined(root: Path, relative: str | Path) -> Path:
    """Resolve *relative* under *root* and reject path traversal."""
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError(f"Path escapes vault: {relative}") from exc
    return candidate


def atomic_create(root: Path, relative: str | Path, content: str) -> Path:
    """Create a UTF-8 file exactly once; never overwrite an existing path."""
    path = confined(root, relative)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
    except FileExistsError as exc:
        raise FileExistsError(f"Refusing to overwrite: {path}") from exc
    return path


def atomic_replace(root: Path, relative: str | Path, content: str) -> Path:
    """Atomically replace a vault file. Callers must gate this behind explicit consent."""
    path = confined(root, relative)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
        os.replace(temp_name, path)
    except Exception:
        Path(temp_name).unlink(missing_ok=True)
        raise
    return path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", value.strip()).strip("-").lower()
    return slug or "untitled"


def yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def redact(value: str) -> str:
    return SECRET_RE.sub(lambda match: f"{match.group(1)}: [REDACTED]", value)


def markdown_files(root: Path, *, include_hidden: bool = False) -> Iterable[Path]:
    for path in root.rglob("*.md"):
        relative = path.relative_to(root)
        if not include_hidden and any(part.startswith(".") for part in relative.parts):
            continue
        if ".git" not in relative.parts:
            yield path


def wikilinks(path: Path) -> list[str]:
    text = FENCE_RE.sub("", path.read_text(encoding="utf-8", errors="replace"))
    targets: list[str] = []
    for match in WIKILINK_RE.finditer(text):
        target = match.group(1).split("|", 1)[0].split("#", 1)[0].strip()
        if target:
            targets.append(target.replace("\\", "/"))
    return targets


def frontmatter_keys(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---\n"):
        return set()
    end = text.find("\n---", 4)
    if end < 0:
        return set()
    keys: set[str] = set()
    for line in text[4:end].splitlines():
        if line and not line.startswith((" ", "-", "#")) and ":" in line:
            keys.add(line.split(":", 1)[0].strip())
    return keys


def note_catalog(root: Path) -> tuple[dict[str, list[Path]], dict[str, Path]]:
    """Return casefolded stem and vault-relative-path indexes."""
    by_stem: dict[str, list[Path]] = {}
    by_path: dict[str, Path] = {}
    for path in markdown_files(root):
        rel = path.relative_to(root).with_suffix("").as_posix()
        by_path[rel.casefold()] = path
        by_stem.setdefault(path.stem.casefold(), []).append(path)
    return by_stem, by_path


def resolve_link(target: str, by_stem: dict[str, list[Path]], by_path: dict[str, Path]) -> list[Path]:
    normalized = target.removesuffix(".md").strip("/").casefold()
    if normalized in by_path:
        return [by_path[normalized]]
    return by_stem.get(Path(normalized).name, [])
