"""Integration tests for runtime settings management.

Verifies that settings reload, env-var overrides, and ablation study
configuration isolation work correctly.
"""

from __future__ import annotations

import pytest

from src.config.settings import get_settings, reload_settings

pytestmark = pytest.mark.integration


class TestSettingsReload:
    def test_get_settings_returns_same_instance(self) -> None:
        s1 = get_settings()
        s2 = get_settings()
        assert s1 is s2

    def test_reload_clears_cache(self) -> None:
        s1 = get_settings()
        reload_settings()
        s2 = get_settings()
        assert s1 is not s2

    def test_env_var_override_after_reload(self, monkeypatch) -> None:
        monkeypatch.setenv("CHUNK_SIZE", "1024")
        reload_settings()
        s = get_settings()
        assert s.chunk_size == 1024
        monkeypatch.delenv("CHUNK_SIZE", raising=False)
        reload_settings()

    def test_settings_has_expected_fields(self) -> None:
        s = get_settings()
        assert hasattr(s, "neo4j_uri")
        assert hasattr(s, "chunk_size")
        assert hasattr(s, "retrieval_mode")
        assert hasattr(s, "enable_reranker")
        assert hasattr(s, "enable_hallucination_grader")

    def test_ablation_settings_override_context(self) -> None:
        """Verify _settings_override from ablation_runner restores state."""
        from src.evaluation.ablation_runner import _settings_override

        reload_settings()
        original_chunk = get_settings().chunk_size

        with _settings_override({"CHUNK_SIZE": "2048"}):
            s = get_settings()
            assert s.chunk_size == 2048

        # After context exit, original value should be restored
        reload_settings()
        s = get_settings()
        assert s.chunk_size == original_chunk
