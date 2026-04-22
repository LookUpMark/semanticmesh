"""Unit tests for src/api/auth.py — API key authentication."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from src.api.auth import require_api_key, _auth_attempts


@pytest.fixture(autouse=True)
def _clean_state(monkeypatch):
    _auth_attempts.clear()
    monkeypatch.delenv("API_KEY", raising=False)
    yield
    _auth_attempts.clear()


def _make_request(client_ip: str = "127.0.0.1") -> MagicMock:
    req = MagicMock()
    req.client = MagicMock()
    req.client.host = client_ip
    return req


class TestRequireApiKey:
    def test_no_key_configured_passes(self) -> None:
        result = require_api_key(request=_make_request(), api_key=None)
        assert result is None

    def test_missing_header_raises_401(self, monkeypatch) -> None:
        monkeypatch.setenv("API_KEY", "valid-key")
        with pytest.raises(HTTPException) as exc_info:
            require_api_key(request=_make_request(), api_key=None)
        assert exc_info.value.status_code == 401

    def test_wrong_key_raises_403(self, monkeypatch) -> None:
        monkeypatch.setenv("API_KEY", "correct")
        with pytest.raises(HTTPException) as exc_info:
            require_api_key(request=_make_request(), api_key="wrong")
        assert exc_info.value.status_code == 403

    def test_correct_key_passes(self, monkeypatch) -> None:
        monkeypatch.setenv("API_KEY", "my-key")
        result = require_api_key(request=_make_request(), api_key="my-key")
        assert result == "my-key"

    def test_rate_limit_after_failures(self, monkeypatch) -> None:
        monkeypatch.setenv("API_KEY", "real")
        req = _make_request("10.0.0.1")
        for _ in range(5):
            try:
                require_api_key(request=req, api_key="bad")
            except HTTPException:
                pass
        with pytest.raises(HTTPException) as exc_info:
            require_api_key(request=req, api_key="bad")
        assert exc_info.value.status_code == 429

    def test_different_ips_separate_limits(self, monkeypatch) -> None:
        monkeypatch.setenv("API_KEY", "real")
        req1 = _make_request("1.1.1.1")
        req2 = _make_request("2.2.2.2")
        for _ in range(5):
            try:
                require_api_key(request=req1, api_key="bad")
            except HTTPException:
                pass
        with pytest.raises(HTTPException) as exc_info:
            require_api_key(request=req2, api_key="bad")
        assert exc_info.value.status_code == 403  # 403, not 429

    def test_constant_time_comparison(self, monkeypatch) -> None:
        """Verify wrong key = 403 regardless of key length/content."""
        monkeypatch.setenv("API_KEY", "a" * 64)
        with pytest.raises(HTTPException) as exc_info:
            require_api_key(request=_make_request(), api_key="b" * 64)
        assert exc_info.value.status_code == 403
