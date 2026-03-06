"""Unit tests for src/config/settings.py"""

import os
from unittest.mock import patch

from src.config.settings import Settings, get_settings


class TestSettingsDefaults:
    def test_default_neo4j_uri(self) -> None:
        s = Settings()
        assert s.neo4j_uri == "bolt://localhost:7687"

    def test_default_temperatures(self) -> None:
        s = Settings()
        assert s.llm_temperature_extraction == 0.0
        assert s.llm_temperature_reasoning == 0.0
        assert s.llm_temperature_generation == 0.3

    def test_default_thresholds_in_range(self) -> None:
        s = Settings()
        assert 0.0 <= s.confidence_threshold <= 1.0
        assert 0.0 <= s.er_similarity_threshold <= 1.0

    def test_default_loop_guards_positive(self) -> None:
        s = Settings()
        assert s.max_reflection_attempts > 0
        assert s.max_cypher_healing_attempts > 0
        assert s.max_hallucination_retries > 0

    def test_ablation_flags_default_true(self) -> None:
        s = Settings()
        assert s.enable_schema_enrichment is True
        assert s.enable_cypher_healing is True
        assert s.enable_reranker is True

    def test_secret_str_not_exposed(self) -> None:
        s = Settings()
        # SecretStr repr must not expose the value
        assert "neo4j" not in repr(s.neo4j_password)


class TestSettingsFromEnv:
    def test_override_via_env(self) -> None:
        with patch.dict(os.environ, {"NEO4J_URI": "bolt://myhost:7688"}):
            s = Settings()
            assert s.neo4j_uri == "bolt://myhost:7688"

    def test_override_confidence_threshold(self) -> None:
        with patch.dict(os.environ, {"CONFIDENCE_THRESHOLD": "0.80"}):
            s = Settings()
            assert s.confidence_threshold == 0.80

    def test_override_ablation_flag(self) -> None:
        with patch.dict(os.environ, {"ENABLE_SCHEMA_ENRICHMENT": "false"}):
            s = Settings()
            assert s.enable_schema_enrichment is False

    def test_secret_accessible_via_method(self) -> None:
        with patch.dict(os.environ, {"NEO4J_PASSWORD": "secret123"}):
            s = Settings()
            assert s.neo4j_password.get_secret_value() == "secret123"


class TestGetSettingsSingleton:
    def test_get_settings_returns_settings_instance(self) -> None:
        s = get_settings()
        assert isinstance(s, Settings)

    def test_singleton_same_object(self) -> None:
        # lru_cache ensures same object is returned
        s1 = get_settings()
        s2 = get_settings()
        assert s1 is s2
