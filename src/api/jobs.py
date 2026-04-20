"""In-memory job store for background tasks.

Stores job state keyed by job_id (12-hex string).
All operations are thread-safe via a Lock.
"""

from __future__ import annotations

import time
import uuid
from threading import Lock
from typing import Any

_store: dict[str, dict[str, Any]] = {}
_lock = Lock()
_MAX_JOBS = 200
_JOB_TTL_SECONDS = 3600  # 1 hour


def _evict_stale_jobs() -> None:
    now = time.monotonic()
    stale = [
        jid for jid, data in _store.items()
        if now - data.get("_created_at", now) > _JOB_TTL_SECONDS
        and data.get("status") in ("done", "failed")
    ]
    for jid in stale:
        del _store[jid]


def create_job(meta: dict[str, Any]) -> str:
    job_id = uuid.uuid4().hex[:12]
    with _lock:
        if len(_store) >= _MAX_JOBS:
            _evict_stale_jobs()
        _store[job_id] = {"status": "queued", "meta": meta, "current_step": None, "_created_at": time.monotonic()}
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
        return dict(_store[job_id]) if job_id in _store else None


def list_jobs() -> list[dict[str, Any]]:
    with _lock:
        return [{"job_id": jid, **data} for jid, data in _store.items()]



