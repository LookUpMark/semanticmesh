"""Unit tests for TASK-29 (ragas_runner) and TASK-30 (custom_metrics)."""

from __future__ import annotations

import json
from pathlib import Path  # noqa: TC003
from unittest.mock import patch

import pytest

from src.evaluation.custom_metrics import (
    GoldMapping,
    HealingResult,
    _pearson,
    cypher_healing_rate,
    hitl_confidence_agreement,
)
from src.evaluation.ragas_runner import (
    _compute_ragas_metrics,
    _load_dataset,
    _run_pipeline_on_sample,
    run_ragas_evaluation,
)
from src.models.schemas import MappingProposal

# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────

_SAMPLE = {
    "question": "Which table stores customer data?",
    "ground_truth": "CUSTOMER_MASTER",
    "ground_truth_contexts": ["Customer maps to CUSTOMER_MASTER"],
    "query_type": "direct_mapping",
    "difficulty": "easy",
}


@pytest.fixture()
def gold_dataset(tmp_path: Path) -> Path:
    data = [_SAMPLE, {**_SAMPLE, "question": "What is a Product?"}]
    p = tmp_path / "gold.json"
    p.write_text(json.dumps(data))
    return p


# ─────────────────────────────────────────────────────────────────────────────
# _load_dataset
# ─────────────────────────────────────────────────────────────────────────────


class TestLoadDataset:
    def test_load_valid_json(self, gold_dataset: Path) -> None:
        data = _load_dataset(gold_dataset)
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["question"] == _SAMPLE["question"]

    def test_load_invalid_json_raises(self, tmp_path: Path) -> None:
        p = tmp_path / "bad.json"
        p.write_text(json.dumps({"not": "a list"}))
        with pytest.raises(ValueError, match="Expected a JSON array"):
            _load_dataset(p)


# ─────────────────────────────────────────────────────────────────────────────
# _run_pipeline_on_sample
# ─────────────────────────────────────────────────────────────────────────────

_PATCH_RUNQUERY = "src.evaluation.ragas_runner.run_query"


class TestRunPipelineOnSample:
    def test_returns_answer_and_contexts(self) -> None:
        with patch(_PATCH_RUNQUERY) as mock_rq:
            mock_rq.return_value = {
                "final_answer": "CUSTOMER_MASTER",
                "sources": ["node_1", "node_2"],
                "retrieved_contexts": ["customer record text", "master table text"],
            }
            result = _run_pipeline_on_sample(_SAMPLE)
        assert result["answer"] == "CUSTOMER_MASTER"
        assert result["contexts"] == ["customer record text", "master table text"]
        assert result["question"] == _SAMPLE["question"]
        assert result["ground_truth"] == _SAMPLE["ground_truth"]

    def test_empty_retrieved_contexts_fallback_to_gold_contexts(self) -> None:
        with patch(_PATCH_RUNQUERY) as mock_rq:
            mock_rq.return_value = {
                "final_answer": "ok",
                "sources": ["node_1"],
                "retrieved_contexts": [],
            }
            result = _run_pipeline_on_sample(_SAMPLE)
        assert result["contexts"] == _SAMPLE["ground_truth_contexts"]

    def test_query_failure_returns_empty_answer(self) -> None:
        with patch(_PATCH_RUNQUERY, side_effect=RuntimeError("Neo4j down")):
            result = _run_pipeline_on_sample(_SAMPLE)
        assert result["answer"] == ""
        assert result["contexts"] == _SAMPLE["ground_truth_contexts"]


# ─────────────────────────────────────────────────────────────────────────────
# _compute_ragas_metrics
# ─────────────────────────────────────────────────────────────────────────────


class TestComputeRagasMetrics:
    def test_returns_zeros_when_ragas_not_installed(self) -> None:
        import builtins

        real_import = builtins.__import__

        def block_ragas(name: str, *args, **kwargs):
            if name in ("ragas", "datasets"):
                raise ImportError(f"{name} not available")
            return real_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=block_ragas):
            result = _compute_ragas_metrics([])

        assert result == {
            "faithfulness": 0.0,
            "answer_relevancy": 0.0,
            "context_precision": 0.0,
            "context_recall": 0.0,
        }


# ─────────────────────────────────────────────────────────────────────────────
# run_ragas_evaluation
# ─────────────────────────────────────────────────────────────────────────────

_PATCH_COMPUTE = "src.evaluation.ragas_runner._compute_ragas_metrics"
_PATCH_PIPELINE = "src.evaluation.ragas_runner._run_pipeline_on_sample"
_ZERO_METRICS = {
    "faithfulness": 0.0,
    "answer_relevancy": 0.0,
    "context_precision": 0.0,
    "context_recall": 0.0,
}


class TestRunRagasEvaluation:
    def test_returns_four_float_metrics(self, gold_dataset: Path) -> None:
        mock_result = {
            "question": "q",
            "answer": "a",
            "contexts": ["c"],
            "ground_truth": "gt",
        }
        with (
            patch(_PATCH_PIPELINE, return_value=mock_result),
            patch(_PATCH_COMPUTE, return_value=_ZERO_METRICS) as mock_compute,
        ):
            metrics = run_ragas_evaluation(gold_dataset)

        assert set(metrics.keys()) == {
            "faithfulness",
            "answer_relevancy",
            "context_precision",
            "context_recall",
        }
        assert all(isinstance(v, float) for v in metrics.values())
        mock_compute.assert_called_once()

    def test_pipeline_failure_still_returns_metrics(self, gold_dataset: Path) -> None:
        with (
            patch(_PATCH_PIPELINE, side_effect=RuntimeError("crash")),
            patch(_PATCH_COMPUTE, return_value=_ZERO_METRICS),
        ):
            metrics = run_ragas_evaluation(gold_dataset)
        # _compute_ragas_metrics called with empty results list
        assert isinstance(metrics, dict)


# ─────────────────────────────────────────────────────────────────────────────
# cypher_healing_rate
# ─────────────────────────────────────────────────────────────────────────────


class TestCypherHealingRate:
    def test_empty_list(self) -> None:
        assert cypher_healing_rate([]) == 0.0

    def test_all_initial_success(self) -> None:
        results = [
            HealingResult(initial_success=True, final_success=True),
            HealingResult(initial_success=True, final_success=True),
        ]
        assert cypher_healing_rate(results) == 0.0

    def test_all_healed(self) -> None:
        results = [
            HealingResult(initial_success=False, final_success=True),
            HealingResult(initial_success=False, final_success=True),
            HealingResult(initial_success=False, final_success=True),
        ]
        assert cypher_healing_rate(results) == pytest.approx(1.0)

    def test_none_healed(self) -> None:
        results = [
            HealingResult(initial_success=False, final_success=False),
            HealingResult(initial_success=False, final_success=False),
        ]
        assert cypher_healing_rate(results) == pytest.approx(0.0)

    def test_mixed(self) -> None:
        results = [
            HealingResult(initial_success=True, final_success=True),  # no attempt
            HealingResult(initial_success=False, final_success=True),  # healed
            HealingResult(initial_success=False, final_success=True),  # healed
            HealingResult(initial_success=False, final_success=False),  # failed
        ]
        # healed=2, failed=1 → 2/3
        assert cypher_healing_rate(results) == pytest.approx(2 / 3)


# ─────────────────────────────────────────────────────────────────────────────
# hitl_confidence_agreement
# ─────────────────────────────────────────────────────────────────────────────


class TestHitlConfidenceAgreement:
    def test_no_matches_returns_zero(self) -> None:
        proposals = [
            MappingProposal(
                table_name="TBL_A",
                mapped_concept="Concept",
                confidence=0.9,
                reasoning="r",
            )
        ]
        gold = [GoldMapping(table_name="OTHER", correct_concept="Concept")]
        assert hitl_confidence_agreement(proposals, gold) == 0.0

    def test_single_match_returns_zero(self) -> None:
        proposals = [
            MappingProposal(
                table_name="TBL_A",
                mapped_concept="Concept",
                confidence=0.9,
                reasoning="r",
            )
        ]
        gold = [GoldMapping(table_name="TBL_A", correct_concept="Concept")]
        assert hitl_confidence_agreement(proposals, gold) == 0.0

    def test_perfect_positive_correlation(self) -> None:
        proposals = [
            MappingProposal(
                table_name="A", mapped_concept="Concept_A", confidence=0.9, reasoning="r"
            ),
            MappingProposal(
                table_name="B", mapped_concept="Concept_B", confidence=0.8, reasoning="r"
            ),
            MappingProposal(table_name="C", mapped_concept="WRONG", confidence=0.3, reasoning="r"),
        ]
        gold = [
            GoldMapping(table_name="A", correct_concept="Concept_A"),
            GoldMapping(table_name="B", correct_concept="Concept_B"),
            GoldMapping(table_name="C", correct_concept="Concept_C"),
        ]
        r = hitl_confidence_agreement(proposals, gold)
        # high confidence → correct, low confidence → wrong: positive correlation
        assert r > 0.5

    def test_zero_variance_confidence_returns_zero(self) -> None:
        proposals = [
            MappingProposal(table_name="A", mapped_concept="X", confidence=0.9, reasoning="r"),
            MappingProposal(table_name="B", mapped_concept="Y", confidence=0.9, reasoning="r"),
        ]
        gold = [
            GoldMapping(table_name="A", correct_concept="X"),
            GoldMapping(table_name="B", correct_concept="Z"),
        ]
        assert hitl_confidence_agreement(proposals, gold) == 0.0


# ─────────────────────────────────────────────────────────────────────────────
# _pearson
# ─────────────────────────────────────────────────────────────────────────────


class TestPearson:
    def test_perfect_positive(self) -> None:
        r = _pearson([1.0, 2.0, 3.0], [1.0, 2.0, 3.0])
        assert r == pytest.approx(1.0)

    def test_perfect_negative(self) -> None:
        r = _pearson([1.0, 2.0, 3.0], [3.0, 2.0, 1.0])
        assert r == pytest.approx(-1.0)

    def test_zero_variance_returns_zero(self) -> None:
        r = _pearson([1.0, 1.0, 1.0], [1.0, 2.0, 3.0])
        assert r == 0.0
