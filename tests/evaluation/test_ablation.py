"""Unit tests for TASK-31: ablation_runner.py."""

from __future__ import annotations

import os
from unittest.mock import patch

import pytest

from src.evaluation.ablation_runner import (
    ABLATION_MATRIX,
    _settings_override,
    run_ablation,
)

_PATCH_RAGAS = "src.evaluation.ablation_runner.run_ragas_evaluation"
_PATCH_BUILDER = "src.graph.builder_graph.run_builder"
_ZERO_METRICS = {
    "faithfulness": 0.0,
    "answer_relevancy": 0.0,
    "context_precision": 0.0,
    "context_recall": 0.0,
}
# Immutable snapshot of the RAGAS-only keys (before any mutation by run_ablation)
_RAGAS_KEYS = tuple(_ZERO_METRICS)
_MOCK_BUILDER_STATE = {
    "triplets": [f"t{i}" for i in range(5)],
    "entities": [f"e{i}" for i in range(3)],
    "tables": ["tbl1", "tbl2"],
    "completed_tables": ["tbl1", "tbl2"],
    "cypher_failed": False,
}


# ─────────────────────────────────────────────────────────────────────────────
# ABLATION_MATRIX
# ─────────────────────────────────────────────────────────────────────────────


class TestAblationMatrix:
    def test_all_six_experiments_defined(self) -> None:
        for exp_id in ("AB-01", "AB-02", "AB-03", "AB-04", "AB-05", "AB-06"):
            assert exp_id in ABLATION_MATRIX

    def test_each_entry_has_required_fields(self) -> None:
        for exp_id, config in ABLATION_MATRIX.items():
            assert "description" in config, f"{exp_id} missing description"
            assert "env_overrides" in config, f"{exp_id} missing env_overrides"
            assert "primary_metric" in config, f"{exp_id} missing primary_metric"
            assert isinstance(config["env_overrides"], dict)


# ─────────────────────────────────────────────────────────────────────────────
# _settings_override context manager
# ─────────────────────────────────────────────────────────────────────────────


class TestSettingsOverride:
    def test_env_var_set_inside_block(self) -> None:
        os.environ.pop("_TEST_ABLATION_KEY", None)
        with _settings_override({"_TEST_ABLATION_KEY": "ablation_value"}):
            assert os.environ["_TEST_ABLATION_KEY"] == "ablation_value"

    def test_env_var_restored_after_block(self) -> None:
        os.environ.pop("_TEST_ABLATION_KEY", None)
        with _settings_override({"_TEST_ABLATION_KEY": "ablation_value"}):
            pass
        assert "_TEST_ABLATION_KEY" not in os.environ

    def test_original_value_preserved(self) -> None:
        os.environ["_TEST_ABLATION_KEY"] = "original"
        try:
            with _settings_override({"_TEST_ABLATION_KEY": "overridden"}):
                assert os.environ["_TEST_ABLATION_KEY"] == "overridden"
            assert os.environ["_TEST_ABLATION_KEY"] == "original"
        finally:
            os.environ.pop("_TEST_ABLATION_KEY", None)

    def test_cache_cleared_after_block(self) -> None:
        from src.config.settings import get_settings

        # Capture the instance before the block
        settings_before = get_settings()

        with _settings_override({"_TEST_ABLATION_KEY": "x"}):
            # On entry the cache was cleared + re-warmed — must be a new object
            settings_inside = get_settings()

        # On exit the cache was cleared + re-warmed again — another new object
        settings_after = get_settings()

        # cache_clear() resets miss counters to 0, so we verify cycle via
        # object identity: each phase must produce a distinct Settings instance
        assert settings_inside is not settings_before, (
            "_settings_override should create a new Settings on entry"
        )
        assert settings_after is not settings_inside, (
            "_settings_override should create a new Settings on exit"
        )


# ─────────────────────────────────────────────────────────────────────────────
# run_ablation
# ─────────────────────────────────────────────────────────────────────────────


class TestRunAblation:
    def test_invalid_experiment_id_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown experiment"):
            run_ablation("AB-99")

    def test_returns_dict_of_floats(self) -> None:
        # Use side_effect (not return_value) so run_ablation gets a fresh copy
        # each call — prevents _ZERO_METRICS from being mutated in-place.
        with patch(_PATCH_RAGAS, side_effect=lambda *a, **kw: dict(_ZERO_METRICS)):
            result = run_ablation("AB-06")
        assert isinstance(result, dict)
        # RAGAS metrics are floats; builder metrics are int/bool — all numeric
        assert all(isinstance(v, (int, float)) for v in result.values())
        # Core RAGAS keys must be present as floats (use pre-mutation snapshot)
        for key in _RAGAS_KEYS:
            assert key in result
            assert isinstance(result[key], float), f"{key!r} should be float"
        # Pipeline metrics must be present
        assert "triplets" in result
        assert "cypher_failed" in result

    def test_env_override_applied_during_run(self) -> None:
        captured: dict[str, str] = {}

        # run_ragas_evaluation is called as (dataset_path, run_ragas=bool)
        def capture_metrics(dataset_path=None, run_ragas=True, **kwargs):
            captured["ENABLE_HALLUCINATION_GRADER"] = os.environ.get(
                "ENABLE_HALLUCINATION_GRADER", "NOT_SET"
            )
            return dict(_ZERO_METRICS)

        # AB-20 sets ENABLE_HALLUCINATION_GRADER=false
        with patch(_PATCH_RAGAS, side_effect=capture_metrics), \
             patch(_PATCH_BUILDER, return_value=_MOCK_BUILDER_STATE):
            run_ablation("AB-20")

        assert captured["ENABLE_HALLUCINATION_GRADER"] == "false"

    def test_env_restored_after_run(self) -> None:
        # AB-20 sets ENABLE_HALLUCINATION_GRADER=false; verify it is restored after
        before = os.environ.get("ENABLE_HALLUCINATION_GRADER", "NOT_SET")
        with patch(_PATCH_RAGAS, side_effect=lambda *a, **kw: dict(_ZERO_METRICS)), \
             patch(_PATCH_BUILDER, return_value=_MOCK_BUILDER_STATE):
            run_ablation("AB-20")
        after = os.environ.get("ENABLE_HALLUCINATION_GRADER", "NOT_SET")
        assert before == after

    def test_all_experiments_run_without_error(self) -> None:
        # Mock both RAGAS and the builder so the test validates ablation_runner
        # routing logic for all 21 experiments without real LLM/Neo4j calls.
        with patch(_PATCH_RAGAS, side_effect=lambda *a, **kw: dict(_ZERO_METRICS)), \
             patch(_PATCH_BUILDER, return_value=_MOCK_BUILDER_STATE):
            for exp_id in ABLATION_MATRIX:
                result = run_ablation(exp_id)
                assert isinstance(result, dict), f"{exp_id} returned non-dict"
                for key in _RAGAS_KEYS:
                    assert key in result, f"{exp_id}: missing RAGAS key {key!r}"
