"""In-memory job store for background tasks.

Stores job state keyed by job_id (12-hex string).
All operations are thread-safe via a Lock.
"""
from __future__ import annotations

import uuid
from threading import Lock
from typing import Any

_store: dict[str, dict[str, Any]] = {}
_lock = Lock()


def create_job(meta: dict[str, Any]) -> str:
    job_id = uuid.uuid4().hex[:12]
    with _lock:
        _store[job_id] = {"status": "queued", **meta}
    return job_id


def set_running(job_id: str) -> None:
    with _lock:
        if job_id in _store:
            _store[job_id]["status"] = "running"


def set_done(job_id: str, result: dict[str, Any]) -> None:
    with _lock:
        if job_id in _store:
            _store[job_id].update({"status": "done", **result})


def set_failed(job_id: str, error: str) -> None:
    with _lock:
        if job_id in _store:
            _store[job_id].update({"status": "failed", "error": error})


def get_job(job_id: str) -> dict[str, Any] | None:
    with _lock:
        return dict(_store[job_id]) if job_id in _store else None


def list_jobs() -> list[dict[str, Any]]:
    with _lock:
        return [{"job_id": jid, **data} for jid, data in _store.items()]
