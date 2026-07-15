#!/usr/bin/env python3
"""Private event journal and retrieval index for the global second brain."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys
from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Iterable


VAULT = Path(__file__).resolve().parents[1]
RUNTIME_HOME = Path(os.environ.get("SECOND_BRAIN_RUNTIME_HOME", Path.home() / ".codex" / "second-brain"))
DB_PATH = RUNTIME_HOME / "brain.db"
SCHEMA_VERSION = "1"
MAX_ATTEMPTS = 3
MAINTENANCE_MARKER = "[second-brain-reconciliation-worker:v1]"
MEMORY_ROOTS = (
    "01_Daily",
    "02_Working-Memory",
    "03_Projects",
    "04_Knowledge",
    "05_Episodic-Memory",
    "06_Procedural-Memory",
    "08_Machine/Context-Packs",
    "08_Machine/Token-Saving-Briefs",
)
SECRET_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----.*?-----END (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", re.S),
    re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password)\s*[:=]\s*[^\s,;]+"),
)


def now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def redact(text: str) -> str:
    result = text
    for pattern in SECRET_PATTERNS:
        result = pattern.sub("[REDACTED]", result)
    return result


def stable_hash(*parts: object) -> str:
    value = "\x1f".join(str(part) for part in parts)
    return hashlib.sha256(value.encode("utf-8", errors="replace")).hexdigest()


def connect(path: Path = DB_PATH) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path, timeout=30)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA journal_mode=WAL")
    connection.execute("PRAGMA synchronous=FULL")
    connection.execute("PRAGMA foreign_keys=ON")
    connection.execute("PRAGMA busy_timeout=30000")
    initialize(connection)
    return connection


@contextmanager
def database(path: Path = DB_PATH) -> Iterable[sqlite3.Connection]:
    connection = connect(path)
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def initialize(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS metadata (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_key TEXT NOT NULL UNIQUE,
            session_id TEXT NOT NULL,
            turn_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            cwd TEXT NOT NULL,
            project_key TEXT NOT NULL,
            content_json TEXT NOT NULL,
            content_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS events_session_turn ON events(session_id, turn_id, id);
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY,
            session_id TEXT NOT NULL,
            turn_id TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('pending', 'processing', 'completed', 'dead')),
            attempts INTEGER NOT NULL DEFAULT 0,
            next_retry_at TEXT,
            claimed_at TEXT,
            receipt_json TEXT,
            last_error TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS jobs_status_retry ON jobs(status, next_retry_at, created_at);
        CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(
            path UNINDEXED,
            title,
            body,
            scope UNINDEXED,
            sha256 UNINDEXED,
            modified_at UNINDEXED
        );
        """
    )
    connection.execute(
        "INSERT INTO metadata(key, value) VALUES('schema_version', ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (SCHEMA_VERSION,),
    )
    connection.commit()


def project_key(cwd: str) -> str:
    path = Path(cwd)
    return stable_hash(str(path.resolve() if path.exists() else path))[:16]


def event_content(payload: dict[str, Any], event_type: str) -> dict[str, Any]:
    content: dict[str, Any] = {
        "hook_event_name": str(payload.get("hook_event_name") or event_type),
        "model": str(payload.get("model") or "unknown"),
        "source": str(payload.get("source") or "unknown"),
    }
    field_map = {
        "prompt": "prompt",
        "last_assistant_message": "assistant_message",
        "agent_id": "agent_id",
        "agent_type": "agent_type",
        "trigger": "trigger",
    }
    for source, target in field_map.items():
        value = payload.get(source)
        if isinstance(value, str) and value.strip():
            content[target] = redact(value)
    return content


def record_hook_event(
    payload: dict[str, Any],
    event_type: str,
    *,
    enqueue: bool = False,
    path: Path = DB_PATH,
) -> dict[str, Any]:
    session_id = str(payload.get("session_id") or "unknown")
    turn_id = str(payload.get("turn_id") or "none")
    cwd = str(payload.get("cwd") or "unknown")
    content = event_content(payload, event_type)
    serialized = json.dumps(content, sort_keys=True, ensure_ascii=False)
    content_hash = stable_hash(serialized)
    event_key = stable_hash(session_id, turn_id, event_type, content_hash)
    created = now()
    job_id = stable_hash(session_id, turn_id, str(content.get("agent_id") or "root"))[:24]
    enqueued_job_id: str | None = None
    with database(path) as connection:
        connection.execute(
            """
            INSERT OR IGNORE INTO events(
                event_key, session_id, turn_id, event_type, cwd, project_key, content_json, content_hash, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (event_key, session_id, turn_id, event_type, cwd, project_key(cwd), serialized, content_hash, created),
        )
        maintenance_session = connection.execute(
            "SELECT 1 FROM events WHERE session_id=? AND event_type='user_prompt' AND content_json LIKE ? LIMIT 1",
            (session_id, f"%{MAINTENANCE_MARKER}%"),
        ).fetchone()
        if enqueue and not maintenance_session and (content.get("assistant_message") or event_type == "pre_compact"):
            connection.execute(
                """
                INSERT INTO jobs(id, session_id, turn_id, status, created_at, updated_at)
                VALUES (?, ?, ?, 'pending', ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    status=CASE WHEN jobs.status='completed' THEN jobs.status ELSE 'pending' END,
                    updated_at=excluded.updated_at
                """,
                (job_id, session_id, turn_id, created, created),
            )
            enqueued_job_id = job_id
    return {"event_key": event_key, "job_id": enqueued_job_id}


def markdown_files(root: Path | None = None) -> Iterable[Path]:
    root = root or VAULT
    for relative in MEMORY_ROOTS:
        base = root / relative
        if not base.exists():
            continue
        for path in base.rglob("*.md"):
            if path.is_file() and path.stat().st_size <= 1_000_000:
                yield path


def note_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip() or fallback
    return fallback


def note_scope(relative: str) -> str:
    if relative.startswith("03_Projects/"):
        return "project"
    if relative.startswith("04_Knowledge/"):
        return "semantic"
    if relative.startswith("05_Episodic-Memory/"):
        return "episodic"
    if relative.startswith("06_Procedural-Memory/"):
        return "procedural"
    if relative.startswith("08_Machine/Context-Packs/"):
        return "context-pack"
    if relative.startswith("08_Machine/Token-Saving-Briefs/"):
        return "brief"
    if relative.startswith("02_Working-Memory/"):
        return "working"
    return "daily"


def sync_index(connection: sqlite3.Connection, root: Path | None = None) -> dict[str, int]:
    root = root or VAULT
    existing = {row["path"]: row["sha256"] for row in connection.execute("SELECT path, sha256 FROM memory_fts")}
    seen: set[str] = set()
    changed = 0
    for path in markdown_files(root):
        relative = path.relative_to(root).as_posix()
        seen.add(relative)
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        if existing.get(relative) == digest:
            continue
        text = data.decode("utf-8", errors="replace")
        connection.execute("DELETE FROM memory_fts WHERE path = ?", (relative,))
        connection.execute(
            "INSERT INTO memory_fts(path, title, body, scope, sha256, modified_at) VALUES (?, ?, ?, ?, ?, ?)",
            (relative, note_title(text, path.stem), text, note_scope(relative), digest, datetime.fromtimestamp(path.stat().st_mtime).astimezone().isoformat(timespec="seconds")),
        )
        changed += 1
    removed = 0
    for relative in set(existing) - seen:
        connection.execute("DELETE FROM memory_fts WHERE path = ?", (relative,))
        removed += 1
    connection.execute(
        "INSERT INTO metadata(key, value) VALUES('last_index_sync', ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (now(),),
    )
    connection.commit()
    return {"indexed": len(seen), "changed": changed, "removed": removed}


def search_memory(
    query: str,
    limit: int = 6,
    path: Path = DB_PATH,
    root: Path | None = None,
) -> list[dict[str, Any]]:
    terms = [term.casefold() for term in re.findall(r"[A-Za-z0-9][A-Za-z0-9_-]{1,}", query)]
    terms = list(dict.fromkeys(terms))[:16]
    if not terms:
        return []
    fts_query = " OR ".join(f'"{term}"*' for term in terms)
    with database(path) as connection:
        sync_index(connection, root)
        rows = connection.execute(
            """
            SELECT path, title, scope, modified_at,
                   snippet(memory_fts, 2, '', '', ' ... ', 28) AS snippet,
                   bm25(memory_fts, 1.0, 2.0, 1.0) AS rank
            FROM memory_fts
            WHERE memory_fts MATCH ?
            ORDER BY rank
            LIMIT ?
            """,
            (fts_query, max(1, min(limit, 20))),
        ).fetchall()
    return [dict(row) for row in rows]


def job_payload(connection: sqlite3.Connection, row: sqlite3.Row) -> dict[str, Any]:
    events = [
        {**dict(event), "content": json.loads(event["content_json"])}
        for event in connection.execute(
            "SELECT id, event_type, cwd, project_key, content_json, content_hash, created_at FROM events WHERE session_id=? AND turn_id=? ORDER BY id",
            (row["session_id"], row["turn_id"]),
        )
    ]
    for event in events:
        event.pop("content_json", None)
    return {**dict(row), "events": events}


def claim_jobs(limit: int = 10, path: Path = DB_PATH) -> list[dict[str, Any]]:
    claimed: list[dict[str, Any]] = []
    timestamp = now()
    with database(path) as connection:
        connection.execute("BEGIN IMMEDIATE")
        rows = connection.execute(
            """
            SELECT * FROM jobs
            WHERE status='pending' AND (next_retry_at IS NULL OR next_retry_at <= ?)
            ORDER BY created_at
            LIMIT ?
            """,
            (timestamp, max(1, min(limit, 50))),
        ).fetchall()
        for row in rows:
            connection.execute(
                "UPDATE jobs SET status='processing', attempts=attempts+1, claimed_at=?, updated_at=? WHERE id=?",
                (timestamp, timestamp, row["id"]),
            )
        connection.commit()
        for row in rows:
            updated = connection.execute("SELECT * FROM jobs WHERE id=?", (row["id"],)).fetchone()
            assert updated is not None
            claimed.append(job_payload(connection, updated))
    return claimed


def complete_job(job_id: str, notes: list[str], path: Path = DB_PATH) -> dict[str, Any]:
    verified: list[str] = []
    for value in notes:
        note = (VAULT / value).resolve() if not Path(value).is_absolute() else Path(value).resolve()
        try:
            relative = note.relative_to(VAULT)
        except ValueError as exc:
            raise ValueError(f"Receipt path is outside the vault: {value}") from exc
        if not note.is_file():
            raise ValueError(f"Receipt note does not exist: {value}")
        verified.append(relative.as_posix())
    receipt = {"notes": verified, "validated_at": now()}
    with database(path) as connection:
        updated = connection.execute(
            "UPDATE jobs SET status='completed', receipt_json=?, last_error=NULL, updated_at=? WHERE id=? AND status='processing'",
            (json.dumps(receipt, sort_keys=True), now(), job_id),
        ).rowcount
    if updated != 1:
        raise ValueError(f"Job is not processing or does not exist: {job_id}")
    return receipt


def fail_job(job_id: str, error: str, path: Path = DB_PATH) -> str:
    with database(path) as connection:
        row = connection.execute("SELECT attempts FROM jobs WHERE id=?", (job_id,)).fetchone()
        if row is None:
            raise ValueError(f"Unknown job: {job_id}")
        attempts = int(row["attempts"])
        if attempts >= MAX_ATTEMPTS:
            status = "dead"
            retry_at = None
        else:
            status = "pending"
            retry_at = (datetime.now().astimezone() + timedelta(minutes=2 ** attempts)).isoformat(timespec="seconds")
        connection.execute(
            "UPDATE jobs SET status=?, next_retry_at=?, last_error=?, updated_at=? WHERE id=?",
            (status, retry_at, redact(error)[:2000], now(), job_id),
        )
    return status


def doctor(repair: bool = False, path: Path = DB_PATH) -> dict[str, Any]:
    with database(path) as connection:
        index = sync_index(connection)
        repaired = 0
        if repair:
            cutoff = (datetime.now().astimezone() - timedelta(hours=2)).isoformat(timespec="seconds")
            repaired = connection.execute(
                """
                UPDATE jobs SET status='pending', claimed_at=NULL, next_retry_at=NULL,
                    last_error='Recovered stale processing lease', updated_at=?
                WHERE status='processing' AND claimed_at < ? AND attempts < ?
                """,
                (now(), cutoff, MAX_ATTEMPTS),
            ).rowcount
            connection.commit()
        counts = {row["status"]: row["count"] for row in connection.execute("SELECT status, COUNT(*) AS count FROM jobs GROUP BY status")}
        last_sync = connection.execute("SELECT value FROM metadata WHERE key='last_index_sync'").fetchone()
    return {"database": str(path), "schema_version": SCHEMA_VERSION, "jobs": counts, "index": index, "last_index_sync": last_sync["value"] if last_sync else None, "repaired": repaired}


def output(value: object, as_json: bool) -> None:
    if as_json:
        print(json.dumps(value, indent=2, ensure_ascii=False))
    else:
        if isinstance(value, list):
            for item in value:
                print(json.dumps(item, ensure_ascii=False))
        else:
            print(json.dumps(value, indent=2, ensure_ascii=False))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=str(DB_PATH), help="Private runtime database path")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    search = sub.add_parser("search")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=6)
    search.add_argument("--json", action="store_true")
    claim = sub.add_parser("claim")
    claim.add_argument("--limit", type=int, default=10)
    claim.add_argument("--json", action="store_true")
    receipt = sub.add_parser("receipt")
    receipt.add_argument("job_id")
    receipt.add_argument("--note", action="append", default=[])
    receipt.add_argument("--json", action="store_true")
    failed = sub.add_parser("fail")
    failed.add_argument("job_id")
    failed.add_argument("error")
    failed.add_argument("--json", action="store_true")
    health = sub.add_parser("doctor")
    health.add_argument("--repair", action="store_true")
    health.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    path = Path(args.db).expanduser().resolve()
    if args.command == "init":
        with database(path):
            pass
        output({"database": str(path), "schema_version": SCHEMA_VERSION}, True)
    elif args.command == "search":
        output(search_memory(args.query, args.limit, path), args.json)
    elif args.command == "claim":
        output(claim_jobs(args.limit, path), args.json)
    elif args.command == "receipt":
        output(complete_job(args.job_id, args.note, path), args.json)
    elif args.command == "fail":
        output({"job_id": args.job_id, "status": fail_job(args.job_id, args.error, path)}, args.json)
    elif args.command == "doctor":
        output(doctor(args.repair, path), args.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
