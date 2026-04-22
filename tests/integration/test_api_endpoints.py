"""Integration tests for the FastAPI REST API layer.

Covers: Health, Auth, Config, Demo endpoints, Graph operations, Ablation reference.
Uses TestClient (synchronous ASGI transport) — no Docker needed for API-level tests.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.integration


@pytest.fixture(autouse=True)
def _clean_api_key_env(monkeypatch):
    monkeypatch.delenv("API_KEY", raising=False)


@pytest.fixture()
def client() -> TestClient:
    from src.api.app import app

    return TestClient(app)


@pytest.fixture()
def authed_client(monkeypatch) -> TestClient:
    monkeypatch.setenv("API_KEY", "test-secret-key-12345")
    from src.api.app import app

    c = TestClient(app)
    c.headers.update({"X-API-Key": "test-secret-key-12345"})
    return c


# ===========================================================================
# Health endpoint
# ===========================================================================


class TestHealthEndpoint:
    def test_health_returns_ok(self, client: TestClient) -> None:
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}

    def test_health_no_auth_required(self, monkeypatch) -> None:
        monkeypatch.setenv("API_KEY", "secret")
        from src.api.app import app

        c = TestClient(app)
        resp = c.get("/health")
        assert resp.status_code == 200


# ===========================================================================
# Auth
# ===========================================================================


class TestAuth:
    def test_no_key_configured_allows_all(self, client: TestClient) -> None:
        resp = client.get("/api/v1/config")
        assert resp.status_code == 200

    def test_missing_header_returns_401(self, monkeypatch) -> None:
        monkeypatch.setenv("API_KEY", "secret123")
        from src.api.app import app

        c = TestClient(app, raise_server_exceptions=False)
        resp = c.get("/api/v1/config")
        assert resp.status_code == 401

    def test_wrong_key_returns_403(self, monkeypatch) -> None:
        monkeypatch.setenv("API_KEY", "correct-key")
        from src.api import auth

        auth._auth_attempts.clear()
        from src.api.app import app

        c = TestClient(app, raise_server_exceptions=False)
        resp = c.get("/api/v1/config", headers={"X-API-Key": "wrong-key"})
        assert resp.status_code == 403

    def test_correct_key_returns_200(self, authed_client: TestClient) -> None:
        resp = authed_client.get("/api/v1/config")
        assert resp.status_code == 200

    def test_rate_limiting_after_too_many_failures(self, monkeypatch) -> None:
        monkeypatch.setenv("API_KEY", "real-key")
        from src.api import auth

        auth._auth_attempts.clear()
        from src.api.app import app

        c = TestClient(app, raise_server_exceptions=False)
        for _ in range(5):
            c.get("/api/v1/config", headers={"X-API-Key": "bad"})
        resp = c.get("/api/v1/config", headers={"X-API-Key": "bad"})
        assert resp.status_code == 429
        auth._auth_attempts.clear()


# ===========================================================================
# Config endpoints
# ===========================================================================


class TestConfigEndpoints:
    def test_get_config_returns_runtime_values(self, client: TestClient) -> None:
        resp = client.get("/api/v1/config")
        assert resp.status_code == 200
        data = resp.json()
        assert "CHUNK_SIZE" in data
        assert "LLM_MODEL_REASONING" in data
        assert "OPENROUTER_API_KEY" not in data
        assert "NEO4J_PASSWORD" not in data

    def test_post_config_applies_overrides(self, client: TestClient) -> None:
        resp = client.post("/api/v1/config", json={"overrides": {"CHUNK_SIZE": "1024"}})
        assert resp.status_code == 200
        body = resp.json()
        assert "CHUNK_SIZE" in body["applied"]

    def test_post_config_blocks_sensitive_keys(self, client: TestClient) -> None:
        resp = client.post(
            "/api/v1/config",
            json={
                "overrides": {
                    "NEO4J_PASSWORD": "hacked",
                    "OPENROUTER_API_KEY": "stolen",
                }
            },
        )
        assert resp.status_code == 200
        body = resp.json()
        assert "NEO4J_PASSWORD" in body["blocked"]
        assert "OPENROUTER_API_KEY" in body["blocked"]
        assert body["applied"] == []


# ===========================================================================
# Demo: Query endpoint (sync — mocks run_query)
# ===========================================================================


class TestQueryEndpoint:
    @patch("src.generation.query_graph.run_query")
    def test_query_returns_answer(self, mock_run_query, client: TestClient) -> None:
        mock_run_query.return_value = {
            "final_answer": "Each customer has an ID, name, email, region.",
            "sources": ["Customer", "CUSTOMER_MASTER"],
            "retrieval_quality_score": 0.85,
            "retrieval_chunk_count": 5,
            "gate_decision": "accept",
            "grounded": True,
            "context_previews": [],
        }
        resp = client.post(
            "/api/v1/demo/query",
            json={"question": "What information is stored for each customer?"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "customer" in data["answer"].lower()


# ===========================================================================
# Jobs store
# ===========================================================================


class TestJobStore:
    def test_create_and_get_job(self) -> None:
        from src.api import jobs

        jid = jobs.create_job({"type": "test"})
        assert len(jid) == 12
        job = jobs.get_job(jid)
        assert job is not None
        assert job["status"] == "queued"

    def test_job_lifecycle(self) -> None:
        from src.api import jobs

        jid = jobs.create_job({"type": "lifecycle"})
        jobs.set_running(jid)
        assert jobs.get_job(jid)["status"] == "running"
        jobs.set_step(jid, "extract_triplets")
        assert jobs.get_job(jid)["current_step"] == "extract_triplets"
        jobs.set_done(jid, {"entities": 10})
        job = jobs.get_job(jid)
        assert job["status"] == "done"
        assert job["result"]["entities"] == 10

    def test_set_failed(self) -> None:
        from src.api import jobs

        jid = jobs.create_job({"type": "fail"})
        jobs.set_failed(jid, "Something went wrong")
        job = jobs.get_job(jid)
        assert job["status"] == "failed"

    def test_get_nonexistent_returns_none(self) -> None:
        from src.api import jobs

        assert jobs.get_job("nonexistent123") is None


# ===========================================================================
# Pydantic model validation
# ===========================================================================


class TestPipelineConfigValidation:
    def test_valid_config(self) -> None:
        from src.api.models import PipelineConfig

        cfg = PipelineConfig(
            chunk_size=512,
            chunk_overlap=64,
            parent_chunk_size=1024,
            parent_chunk_overlap=128,
        )
        assert cfg.chunk_size == 512

    def test_overlap_ge_size_raises(self) -> None:
        from src.api.models import PipelineConfig

        with pytest.raises(ValueError, match="chunk_overlap.*must be less than"):
            PipelineConfig(chunk_size=256, chunk_overlap=256)

    def test_parent_smaller_than_child_raises(self) -> None:
        from src.api.models import PipelineConfig

        with pytest.raises(ValueError, match="parent_chunk_size.*must be greater"):
            PipelineConfig(chunk_size=512, parent_chunk_size=256)

    def test_parent_overlap_ge_parent_size_raises(self) -> None:
        from src.api.models import PipelineConfig

        with pytest.raises(ValueError, match="parent_chunk_overlap.*must be less than"):
            PipelineConfig(parent_chunk_size=800, parent_chunk_overlap=800)


# ===========================================================================
# Ablation router: matrix + datasets (read-only, no side-effects)
# ===========================================================================


class TestAblationReference:
    def test_get_matrix(self, client: TestClient) -> None:
        resp = client.get("/api/v1/ablation/matrix")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        study_ids = [entry["study_id"] for entry in data]
        assert "AB-00" in study_ids
        assert "AB-BEST" in study_ids

    def test_get_datasets(self, client: TestClient) -> None:
        resp = client.get("/api/v1/ablation/datasets")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        # datasets endpoint returns list[str] of relative paths
        if len(data) > 0:
            assert isinstance(data[0], str)
