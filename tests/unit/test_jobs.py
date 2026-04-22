"""Unit tests for src/api/jobs.py — thread-safe in-memory job store."""

from __future__ import annotations

import threading

import pytest

from src.api.jobs import (
    create_job,
    get_job,
    list_jobs,
    set_done,
    set_failed,
    set_running,
    set_step,
)


class TestJobsCRUD:
    def test_create_returns_hex_id(self) -> None:
        jid = create_job({"type": "unit"})
        assert len(jid) == 12
        assert all(c in "0123456789abcdef" for c in jid)

    def test_get_returns_none_for_unknown(self) -> None:
        assert get_job("doesnotexist") is None

    def test_full_lifecycle(self) -> None:
        jid = create_job({"info": "test"})
        assert get_job(jid)["status"] == "queued"
        set_running(jid)
        assert get_job(jid)["status"] == "running"
        set_step(jid, "step_1")
        assert get_job(jid)["current_step"] == "step_1"
        set_done(jid, {"result": "ok"})
        job = get_job(jid)
        assert job["status"] == "done"
        assert job["result"] == {"result": "ok"}
        assert job["current_step"] is None

    def test_set_failed_records_error(self) -> None:
        jid = create_job({"x": 1})
        set_failed(jid, "oops")
        job = get_job(jid)
        assert job["status"] == "failed"
        assert job["error"] == "oops"

    def test_list_includes_created_jobs(self) -> None:
        jid = create_job({"tag": "listme"})
        jobs = list_jobs()
        ids = [j["job_id"] for j in jobs]
        assert jid in ids

    def test_operations_on_nonexistent_id_are_safe(self) -> None:
        """set_* on unknown IDs should not raise."""
        set_running("ghost")
        set_step("ghost", "step")
        set_done("ghost", {})
        set_failed("ghost", "err")


class TestJobsThreadSafety:
    def test_concurrent_creates(self) -> None:
        ids: list[str] = []
        errors: list[Exception] = []

        def _create():
            try:
                jid = create_job({"thread": threading.current_thread().name})
                ids.append(jid)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=_create) for _ in range(50)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(errors) == 0
        assert len(set(ids)) == 50
