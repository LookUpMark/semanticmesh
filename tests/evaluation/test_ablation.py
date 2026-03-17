"""Unit tests for TASK-31: ablation_runner.py."""

from __future__ import annotations

import json
import os
from pathlib import Path  # noqa: TC003
from unittest.mock import patch

import pytest

from src.evaluation.ablation_runner import (
    ABLATION_MATRIX,
    _settings_override,
    main,
    run_ablation,
    run_all_ablations,
    save_ablation_report,
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


# ─────────────────────────────────────────────────────────────────────────────
# run_all_ablations
# ─────────────────────────────────────────────────────────────────────────────

class TestRunAllAblations:
    def test_returns_dict_with_all_experiment_ids(self) -> None:
        with patch(_PATCH_RAGAS, return_value=_ZERO_METRICS):
            results = run_all_ablations()
        assert set(results.keys()) == set(ABLATION_MATRIX.keys())

    def test_each_value_is_dict_of_floats(self) -> None:
        with patch(_PATCH_RAGAS, return_value=_ZERO_METRICS):
            results = run_all_ablations()
        for exp_id, metrics in results.items():
            assert isinstance(metrics, dict), f"{exp_id} result is not a dict"
            assert all(isinstance(v, float) for v in metrics.values()), (
                f"{exp_id}: non-float metric value"
            )

    def test_ragas_called_once_per_experiment(self) -> None:
        with patch(_PATCH_RAGAS, return_value=_ZERO_METRICS) as mock_ragas:
            run_all_ablations()
        assert mock_ragas.call_count == len(ABLATION_MATRIX)


# ─────────────────────────────────────────────────────────────────────────────
# save_ablation_report
# ─────────────────────────────────────────────────────────────────────────────

_SAMPLE_RESULTS: dict[str, dict[str, float]] = {
    "AB-05": {"faithfulness": 0.7, "context_precision": 0.6},
    "AB-06": {"faithfulness": 0.8, "context_precision": 0.75},
}


class TestSaveAblationReport:
    def test_creates_file(self, tmp_path: Path) -> None:
        path = save_ablation_report(_SAMPLE_RESULTS, output_dir=tmp_path)
        assert path.exists()

    def test_file_has_json_extension(self, tmp_path: Path) -> None:
        path = save_ablation_report(_SAMPLE_RESULTS, output_dir=tmp_path)
        assert path.suffix == ".json"

    def test_file_contains_experiments_key(self, tmp_path: Path) -> None:
        path = save_ablation_report(_SAMPLE_RESULTS, output_dir=tmp_path)
        data = json.loads(path.read_text())
        assert "experiments" in data
        assert "AB-05" in data["experiments"]
        assert "AB-06" in data["experiments"]

    def test_output_dir_created_if_missing(self, tmp_path: Path) -> None:
        nested = tmp_path / "reports" / "ablation"
        assert not nested.exists()
        save_ablation_report(_SAMPLE_RESULTS, output_dir=nested)
        assert nested.exists()

    def test_metrics_values_preserved(self, tmp_path: Path) -> None:
        path = save_ablation_report(_SAMPLE_RESULTS, output_dir=tmp_path)
        data = json.loads(path.read_text())
        assert data["experiments"]["AB-05"]["faithfulness"] == pytest.approx(0.7)


# ─────────────────────────────────────────────────────────────────────────────
# main (CLI entry point)
# ─────────────────────────────────────────────────────────────────────────────

_PATCH_RUN_ABLATION = "src.evaluation.ablation_runner.run_ablation"
_PATCH_RUN_ALL = "src.evaluation.ablation_runner.run_all_ablations"
_PATCH_SAVE_REPORT = "src.evaluation.ablation_runner.save_ablation_report"


class TestAblationMain:
    def test_main_all_calls_run_all_ablations(self, tmp_path: Path) -> None:
        with (
            patch(_PATCH_RUN_ALL, return_value=_SAMPLE_RESULTS) as mock_all,
            patch(_PATCH_SAVE_REPORT, return_value=tmp_path / "report.json"),
            patch("sys.argv", ["ablation_runner", "--ablation", "all", "--output", str(tmp_path)]),
        ):
            main()
        mock_all.assert_called_once()

    def test_main_specific_id_calls_run_ablation(self, tmp_path: Path) -> None:
        with (
            patch(_PATCH_RUN_ABLATION, return_value=_ZERO_METRICS) as mock_run,
            patch(_PATCH_SAVE_REPORT, return_value=tmp_path / "report.json"),
            patch(
                "sys.argv",
                ["ablation_runner", "--ablation", "AB-05", "--output", str(tmp_path)],
            ),
        ):
            main()
        mock_run.assert_called_once_with("AB-05", dataset_path=None)

    def test_main_saves_report(self, tmp_path: Path) -> None:
        with (
            patch(_PATCH_RUN_ALL, return_value=_SAMPLE_RESULTS),
            patch(_PATCH_SAVE_REPORT, return_value=tmp_path / "report.json") as mock_save,
            patch("sys.argv", ["ablation_runner", "--output", str(tmp_path)]),
        ):
            main()
        mock_save.assert_called_once()

    def test_main_ab05_env_override(self) -> None:
        """AB-05 (reranker disabled) env var is correctly applied during main()."""
        captured: dict[str, str] = {}

        def capture_env(dataset_path=None):
            captured["ENABLE_RERANKER"] = os.environ.get("ENABLE_RERANKER", "NOT_SET")
            return _ZERO_METRICS

        with (
            patch(_PATCH_RAGAS, side_effect=capture_env),
            patch("sys.argv", ["ablation_runner", "--ablation", "AB-05"]),
        ):
            main()

        assert captured["ENABLE_RERANKER"] == "false"
