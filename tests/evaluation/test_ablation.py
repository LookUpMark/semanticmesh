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
_ZERO_METRICS = {
    "faithfulness": 0.0,
    "answer_relevancy": 0.0,
    "context_precision": 0.0,
    "context_recall": 0.0,
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

        # Fill the cache
        _ = get_settings()
        with _settings_override({"_TEST_ABLATION_KEY": "x"}):
            pass
        # Cache should have been cleared (currsize==0 or a new call happened)
        cache_info_after = get_settings.cache_info()
        # After the block, cache was cleared, so currsize should be 0
        assert cache_info_after.currsize == 0


# ─────────────────────────────────────────────────────────────────────────────
# run_ablation
# ─────────────────────────────────────────────────────────────────────────────


class TestRunAblation:
    def test_invalid_experiment_id_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown experiment"):
            run_ablation("AB-99")

    def test_returns_dict_of_floats(self) -> None:
        with patch(_PATCH_RAGAS, return_value=_ZERO_METRICS):
            result = run_ablation("AB-06")
        assert isinstance(result, dict)
        assert all(isinstance(v, float) for v in result.values())

    def test_env_override_applied_during_run(self) -> None:
        captured: dict[str, str] = {}

        def capture_metrics(dataset_path=None):
            captured["ENABLE_HALLUCINATION_GRADER"] = os.environ.get(
                "ENABLE_HALLUCINATION_GRADER", "NOT_SET"
            )
            return _ZERO_METRICS

        with patch(_PATCH_RAGAS, side_effect=capture_metrics):
            run_ablation("AB-06")

        assert captured["ENABLE_HALLUCINATION_GRADER"] == "false"

    def test_env_restored_after_run(self) -> None:
        before = os.environ.get("ENABLE_HALLUCINATION_GRADER", "NOT_SET")
        with patch(_PATCH_RAGAS, return_value=_ZERO_METRICS):
            run_ablation("AB-06")
        after = os.environ.get("ENABLE_HALLUCINATION_GRADER", "NOT_SET")
        assert before == after

    def test_all_experiments_run_without_error(self) -> None:
        with patch(_PATCH_RAGAS, return_value=_ZERO_METRICS):
            for exp_id in ABLATION_MATRIX:
                result = run_ablation(exp_id)
                assert isinstance(result, dict), f"{exp_id} returned non-dict"
