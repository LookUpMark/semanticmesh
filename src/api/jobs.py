"""In-memory job store for background tasks.

Stores job state keyed by job_id (12-hex string).
All operations are thread-safe via a Lock.
"""

from __future__ import annotations

import copy
import time
import uuid
from threading import Lock
from typing import Any

_store: dict[str, dict[str, Any]] = {}
_lock = Lock()

# AUDIT-006 (RED): Hard cap on total jobs to prevent unbounded memory growth
# from rapid-fire API calls. When reached, oldest terminal-state jobs are evicted.
_MAX_JOBS = 1000

# AUDIT-006 (RED): Maximum size of the meta dict per job (~4KB worth of keys).
_MAX_META_KEYS = 50


def _get_max_jobs() -> int:
    from src.config.settings import get_settings

    return get_settings().api_max_concurrent_jobs


def _get_job_ttl() -> int:
    from src.config.settings import get_settings

    return get_settings().api_job_ttl_seconds


def _evict_stale_jobs() -> None:
    now = time.monotonic()
    ttl = _get_job_ttl()
    stale = [
        jid
        for jid, data in _store.items()
        if now - data.get("_created_at", now) > ttl and data.get("status") in ("done", "failed")
    ]
    for jid in stale:
        del _store[jid]


def _evict_oldest_terminal() -> None:
    """AUDIT-006 (RED): Remove oldest terminal-state jobs to make room."""
    terminal = [
        (jid, data.get("_created_at", 0.0))
        for jid, data in _store.items()
        if data.get("status") in ("done", "failed")
    ]
    terminal.sort(key=lambda x: x[1])
    # Evict oldest 10% of terminal jobs
    evict_count = max(1, len(terminal) // 10)
    for jid, _ in terminal[:evict_count]:
        del _store[jid]


def create_job(meta: dict[str, Any]) -> str:
    job_id = uuid.uuid4().hex[:12]
    with _lock:
        if len(_store) >= _MAX_JOBS:
            _evict_stale_jobs()
        # AUDIT-006 (RED): If still at limit after stale eviction, force-evict oldest
        if len(_store) >= _MAX_JOBS:
            _evict_oldest_terminal()
        # AUDIT-006 (RED): Cap meta dict size to prevent oversized metadata
        if len(meta) > _MAX_META_KEYS:
            meta = dict(list(meta.items())[:_MAX_META_KEYS])
        _store[job_id] = {
            "status": "queued",
            "meta": meta,
            "current_step": None,
            "_created_at": time.monotonic(),
        }
    return job_id


def set_running(job_id: str) -> None:
    with _lock:
        if job_id in _store:
            _store[job_id]["status"] = "running"


def set_step(job_id: str, step: str) -> None:
    """Update the current pipeline step name (e.g. 'extract_triplets')."""
    with _lock:
        if job_id in _store:
            _store[job_id]["current_step"] = step


def set_done(job_id: str, result: dict[str, Any]) -> None:
    with _lock:
        if job_id in _store:
            _store[job_id]["status"] = "done"
            _store[job_id]["result"] = result
            _store[job_id]["current_step"] = None


def set_failed(job_id: str, error: str) -> None:
    with _lock:
        if job_id in _store:
            _store[job_id].update({"status": "failed", "error": error, "current_step": None})


def get_job(job_id: str) -> dict[str, Any] | None:
    with _lock:
        return copy.deepcopy(_store[job_id]) if job_id in _store else None


def list_jobs() -> list[dict[str, Any]]:
    # AUDIT-057 (YELLOW): Use deepcopy so callers cannot mutate the internal store
    # through nested references in the returned dicts.
    with _lock:
        return [{"job_id": jid, **copy.deepcopy(data)} for jid, data in _store.items()]
