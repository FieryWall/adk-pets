"""
SQLite-backed Memory Service

Provides an async-friendly, lightweight persistent memory store backed by SQLite.
This implements two methods compatible with the ADK memory usage in this repo:
 - add_session_to_memory(session): store session messages
 - search_memory(query, top_k): perform a simple substring search over stored entries

The implementation uses `asyncio.to_thread` to avoid blocking the event loop.
"""
import sqlite3
import json
import datetime
import asyncio
import os
from typing import List


class _Res:
    def __init__(self, text: str):
        self.text = text


class SQLiteMemoryService:
    """Simple SQLite persistence for ADK memory.

    This implementation is intentionally minimal and self-contained. It stores
    each message from a session as a separate entry and provides a basic
    substring search. For production use you may want to replace this with an
    FTS-backed implementation (FTS5) for better relevance and performance.
    """

    def __init__(self, db_path: str = None):
        # default to a file inside the repo so it's persistent between runs
        if db_path is None:
            db_path = os.path.join(os.getcwd(), ".adk_memory.db")
        self.db_path = db_path
        self._ensure_db()

    def _get_conn(self):
        # Use check_same_thread=False because we may call sqlite from threads
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def _ensure_db(self):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                entry_index INTEGER,
                content TEXT,
                FOREIGN KEY(session_id) REFERENCES sessions(id)
            )
            """
        )
        conn.commit()
        conn.close()

    def _add_session_sync(self, session) -> int:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO sessions (created_at) VALUES (?)",
            (datetime.datetime.now(datetime.timezone.utc).isoformat(),),
        )
        session_id = cur.lastrowid

        messages = getattr(session, "messages", []) or []
        for idx, m in enumerate(messages):
            # Support message objects with 'text' attribute or raw strings
            text = getattr(m, "text", None) if not isinstance(m, str) else m
            if text is None:
                text = str(m)
            cur.execute(
                "INSERT INTO entries (session_id, entry_index, content) VALUES (?, ?, ?)",
                (session_id, idx, text),
            )

        conn.commit()
        conn.close()
        return session_id

    async def add_session_to_memory(self, session) -> int:
        """Persist a session's messages into SQLite.

        Returns the inserted session id.
        """
        return await asyncio.to_thread(self._add_session_sync, session)

    def _search_sync(self, query: str, top_k: int = 5) -> List[_Res]:
        conn = self._get_conn()
        cur = conn.cursor()
        # basic case-insensitive LIKE search
        pattern = f"%{query}%"
        cur.execute(
            "SELECT content FROM entries WHERE content LIKE ? COLLATE NOCASE ORDER BY id DESC LIMIT ?",
            (pattern, top_k),
        )
        rows = cur.fetchall()
        conn.close()
        return [_Res(r[0]) for r in rows]

    async def search_memory(self, query: str, top_k: int = 5) -> List[_Res]:
        """Search stored entries for the given query string.

        Returns a list of objects with a `text` attribute (for compatibility with the
        existing retrieval tooling in this repo).
        """
        if not query:
            return []
        return await asyncio.to_thread(self._search_sync, query, top_k)

    def close(self):
        # nothing to close, connections are per-call
        pass


class InMemoryMemoryService:
    """Very small in-memory memory service used as a fallback for tests and
    when persistence is not required. Provides the same async methods as the
    SQLiteMemoryService: `add_session_to_memory` and `search_memory`.
    """

    def __init__(self):
        self._sessions = []
        self._entries = []
        self._next_session_id = 1

    async def add_session_to_memory(self, session) -> int:
        session_id = self._next_session_id
        self._next_session_id += 1

        messages = getattr(session, "messages", []) or []
        for idx, m in enumerate(messages):
            text = getattr(m, "text", None) if not isinstance(m, str) else m
            if text is None:
                text = str(m)
            self._entries.append({"session_id": session_id, "entry_index": idx, "content": text})

        self._sessions.append({"id": session_id})
        return session_id

    async def search_memory(self, query: str, top_k: int = 5) -> List[_Res]:
        if not query:
            return []
        q = query.lower()
        results: List[_Res] = []
        for e in reversed(self._entries):
            if q in (e.get("content") or "").lower():
                results.append(_Res(e.get("content")))
                if len(results) >= top_k:
                    break
        return results
        
def get_memory_service(kind: str = "sqlite", db_path: str | None = None):
    """
    Factory helper to obtain a memory service implementation.

    Args:
        kind: 'sqlite' to use the SQLite persistence, or 'memory' to use the
            in-memory implementation.
        db_path: Path to SQLite DB file when using sqlite kind.

    Returns:
        An object implementing `add_session_to_memory` and `search_memory`.
    """
    kind = (kind or "sqlite").lower()
    if kind in ("sqlite", "file"):
        return SQLiteMemoryService(db_path=db_path)
    if kind in ("memory", "inmemory", "in_memory"):
        return InMemoryMemoryService()
    raise ValueError(f"Unknown memory service kind: {kind}")

        
