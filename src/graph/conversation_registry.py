"""Conversation persistence registry.

Stores user chat conversations to SQLite so they can be listed, loaded,
renamed, and deleted from the UI — independently of LangGraph's internal
SqliteSaver checkpoints.

Storage::

    data/memory/conversations_registry.db  ← SQLite with conversation metadata + messages

Message JSON schema::

    [
        {"role": "user",      "content": "..."},
        {"role": "assistant", "content": "...", "metadata": {QueryResponse fields}},
        ...
    ]
"""

from __future__ import annotations

import json
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from src.config.logging import get_logger

logger = get_logger(__name__)

_DATA_DIR = Path(__file__).parent.parent.parent / "data" / "memory"
_REGISTRY_DB = _DATA_DIR / "conversations_registry.db"

_MAX_PREVIEW_CHARS = 80


# ─────────────────────────────────────────────────────────────────────────────
# DB bootstrap
# ─────────────────────────────────────────────────────────────────────────────

def _ensure_dirs() -> None:
    _DATA_DIR.mkdir(parents=True, exist_ok=True)


@contextmanager
def _db():
    _ensure_dirs()
    conn = sqlite3.connect(str(_REGISTRY_DB))
    conn.row_factory = sqlite3.Row
    try:
        _bootstrap(conn)
        yield conn
        conn.commit()
    finally:
        conn.close()


def _bootstrap(conn: sqlite3.Connection) -> None:
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS conversations (
            id                  TEXT PRIMARY KEY,
            title               TEXT NOT NULL DEFAULT '',
            session_id          TEXT NOT NULL,
            preview             TEXT NOT NULL DEFAULT '',
            message_count       INTEGER NOT NULL DEFAULT 0,
            active_snapshot_id  TEXT,
            created_at          TEXT NOT NULL,
            updated_at          TEXT NOT NULL,
            messages_json       TEXT NOT NULL DEFAULT '[]'
        );
    """)


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

def list_conversations() -> list[dict[str, Any]]:
    """Return all saved conversations — metadata only, no messages."""
    with _db() as conn:
        rows = conn.execute(
            "SELECT id, title, session_id, preview, message_count, "
            "active_snapshot_id, created_at, updated_at "
            "FROM conversations ORDER BY updated_at DESC"
        ).fetchall()
    return [
        {
            "id": r["id"],
            "title": r["title"],
            "session_id": r["session_id"],
            "preview": r["preview"],
            "message_count": r["message_count"],
            "active_snapshot_id": r["active_snapshot_id"],
            "created_at": r["created_at"],
            "updated_at": r["updated_at"],
        }
        for r in rows
    ]


def get_conversation(conversation_id: str) -> dict[str, Any]:
    """Return full conversation including messages.

    Raises:
        ValueError: If not found.
    """
    with _db() as conn:
        row = conn.execute(
            "SELECT * FROM conversations WHERE id = ?",
            (conversation_id,),
        ).fetchone()
    if row is None:
        raise ValueError(f"Conversation '{conversation_id}' not found.")
    messages = json.loads(row["messages_json"] or "[]")
    return {
        "id": row["id"],
        "title": row["title"],
        "session_id": row["session_id"],
        "preview": row["preview"],
        "message_count": row["message_count"],
        "active_snapshot_id": row["active_snapshot_id"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
        "messages": messages,
    }


def save_conversation(
    session_id: str,
    title: str,
    messages: list[dict[str, Any]],
    active_snapshot_id: str | None = None,
) -> dict[str, Any]:
    """Persist a conversation.

    If ``title`` is empty, the first user message (truncated) is used.
    Returns the conversation metadata dict.
    """
    conv_id = str(uuid.uuid4())
    now = datetime.now(UTC).isoformat()

    # Auto-title from first user message
    if not title.strip():
        first_user = next((m["content"] for m in messages if m.get("role") == "user"), "")
        title = first_user[:_MAX_PREVIEW_CHARS].strip() or "Untitled conversation"

    preview = title[:_MAX_PREVIEW_CHARS]
    count = len(messages)

    with _db() as conn:
        conn.execute(
            "INSERT INTO conversations "
            "(id, title, session_id, preview, message_count, active_snapshot_id, "
            "created_at, updated_at, messages_json) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                conv_id,
                title,
                session_id,
                preview,
                count,
                active_snapshot_id,
                now,
                now,
                json.dumps(messages, default=str),
            ),
        )

    logger.info("Conversation '%s' saved (%d messages).", title, count)
    return {
        "id": conv_id,
        "title": title,
        "session_id": session_id,
        "preview": preview,
        "message_count": count,
        "active_snapshot_id": active_snapshot_id,
        "created_at": now,
        "updated_at": now,
    }


def rename_conversation(conversation_id: str, title: str) -> dict[str, Any]:
    """Rename an existing conversation.

    Raises:
        ValueError: If not found.
    """
    now = datetime.now(UTC).isoformat()
    with _db() as conn:
        row = conn.execute(
            "SELECT id, session_id, preview, message_count, active_snapshot_id, created_at "
            "FROM conversations WHERE id = ?",
            (conversation_id,),
        ).fetchone()
        if row is None:
            raise ValueError(f"Conversation '{conversation_id}' not found.")
        conn.execute(
            "UPDATE conversations SET title = ?, updated_at = ? WHERE id = ?",
            (title, now, conversation_id),
        )
    logger.info("Conversation '%s' renamed to '%s'.", conversation_id, title)
    return {
        "id": conversation_id,
        "title": title,
        "session_id": row["session_id"],
        "preview": row["preview"],
        "message_count": row["message_count"],
        "active_snapshot_id": row["active_snapshot_id"],
        "created_at": row["created_at"],
        "updated_at": now,
    }


def delete_conversation(conversation_id: str) -> None:
    """Delete a conversation permanently.

    Raises:
        ValueError: If not found.
    """
    with _db() as conn:
        row = conn.execute(
            "SELECT id FROM conversations WHERE id = ?", (conversation_id,)
        ).fetchone()
        if row is None:
            raise ValueError(f"Conversation '{conversation_id}' not found.")
        conn.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
    logger.info("Conversation '%s' deleted.", conversation_id)
