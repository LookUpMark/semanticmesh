"""Unit tests for src/retrieval/reranker.py — UT-13."""

from __future__ import annotations

import sys
from unittest.mock import MagicMock, patch

import pytest

from src.models.schemas import RetrievedChunk
from src.retrieval.reranker import rerank

# ── Helpers ────────────────────────────────────────────────────────────────────


def _chunk(name: str, score: float = 0.5) -> RetrievedChunk:
    return RetrievedChunk(
        node_id=name,
        node_type="BusinessConcept",
        text=f"{name}: some definition text",
        score=score,
        source_type="vector",
        metadata={},
    )


def _make_reranker(scores: list[float]) -> MagicMock:
    reranker = MagicMock()
    reranker.compute_score.return_value = scores
    return reranker


# ── TestRerank ────────────────────────────────────────────────────────────────


class TestRerank:
    def test_empty_chunks_returns_empty(self) -> None:
        result = rerank("query", [], reranker=MagicMock(), top_k=5)
        assert result == []

    def test_sorted_descending_by_score(self) -> None:
        chunks = [_chunk("A"), _chunk("B"), _chunk("C")]
        reranker = _make_reranker([0.3, 0.9, 0.6])
        result = rerank("query", chunks, reranker=reranker, top_k=3)
        assert result[0].node_id == "B"
        assert result[1].node_id == "C"
        assert result[2].node_id == "A"

    def test_top_k_slices_results(self) -> None:
        chunks = [_chunk(f"N{i}") for i in range(10)]
        scores = [float(i) / 10 for i in range(10)]
        reranker = _make_reranker(scores)
        result = rerank("query", chunks, reranker=reranker, top_k=3)
        assert len(result) == 3

    def test_reranker_score_stored_in_metadata(self) -> None:
        chunks = [_chunk("X"), _chunk("Y")]
        reranker = _make_reranker([0.8, 0.4])
        result = rerank("query", chunks, reranker=reranker, top_k=2)
        assert "reranker_score" in result[0].metadata
        assert result[0].metadata["reranker_score"] == pytest.approx(0.8)

    def test_reranker_failure_returns_unranked(self) -> None:
        chunks = [_chunk("A"), _chunk("B")]
        reranker = MagicMock()
        reranker.compute_score.side_effect = RuntimeError("OOM")
        result = rerank("query", chunks, reranker=reranker, top_k=5)
        assert len(result) == 2

    def test_score_field_updated_to_reranker_score(self) -> None:
        chunks = [_chunk("Z", score=0.1)]
        reranker = _make_reranker([0.99])
        result = rerank("query", chunks, reranker=reranker, top_k=1)
        assert result[0].score == pytest.approx(0.99)

    def test_pairs_passed_to_compute_score(self) -> None:
        chunks = [_chunk("Customer"), _chunk("Product")]
        reranker = _make_reranker([0.7, 0.5])
        rerank("what is a customer?", chunks, reranker=reranker, top_k=2)
        call_args = reranker.compute_score.call_args[0][0]
        assert call_args[0] == ("what is a customer?", "Customer: some definition text")
        assert call_args[1] == ("what is a customer?", "Product: some definition text")

    def test_invalid_chunks_are_dropped_before_scoring(self) -> None:
        valid = _chunk("Customer")
        invalid = RetrievedChunk(
            node_id="",
            node_type="BusinessConcept",
            text="",
            score=0.1,
            source_type="vector",
            metadata={},
        )
        reranker = _make_reranker([0.9])

        result = rerank("query", [invalid, valid], reranker=reranker, top_k=5)

        assert len(result) == 1
        assert result[0].node_id == "Customer"
        call_args = reranker.compute_score.call_args[0][0]
        assert call_args == [("query", "Customer: some definition text")]


# ── TestGetReranker ───────────────────────────────────────────────────────────


class TestGetReranker:
    def test_import_error_raises_helpful_message(self) -> None:
        from src.retrieval import reranker as reranker_mod

        reranker_mod.get_reranker.cache_clear()
        with patch.dict(sys.modules, {"FlagEmbedding": None}):
            with pytest.raises(ImportError, match="FlagEmbedding"):
                reranker_mod.get_reranker()
        reranker_mod.get_reranker.cache_clear()
