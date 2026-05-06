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
        # Short BC chunks are enriched with [node_type | node_id] prefix
        assert call_args[0] == ("what is a customer?", "[BusinessConcept | Customer] Customer: some definition text")
        assert call_args[1] == ("what is a customer?", "[BusinessConcept | Product] Product: some definition text")

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
        assert call_args == [("query", "[BusinessConcept | Customer] Customer: some definition text")]

    def test_floor_large_pool_rank1_gets_055(self) -> None:
        """Pool ≥10 → rank #1 floor is 0.55 (max of linear interpolation)."""
        chunks = [_chunk(f"C{i}") for i in range(12)]
        # All get low scores (0.01..0.12) → floor should kick in
        reranker = _make_reranker([0.01 * (i + 1) for i in range(12)])
        result = rerank("query", chunks, reranker=reranker, top_k=5)
        # Rank #1 (highest raw = 0.12) should be floored to 0.55
        assert result[0].score == pytest.approx(0.55)
        # Rank #2 → 0.50
        assert result[1].score == pytest.approx(0.50)
        # Rank #5 → 0.35
        assert result[4].score == pytest.approx(0.35)

    def test_floor_small_pool_rank1_gets_040(self) -> None:
        """Pool=3 (minimum) → rank #1 floor is 0.40."""
        chunks = [_chunk(f"C{i}") for i in range(3)]
        reranker = _make_reranker([0.01, 0.02, 0.03])
        result = rerank("query", chunks, reranker=reranker, top_k=5)
        # Rank #1 floor = 0.40 (pool=3, min of interpolation)
        assert result[0].score == pytest.approx(0.40)
        # Rank #2 floor = 0.35
        assert result[1].score == pytest.approx(0.35)

    def test_floor_mid_pool_interpolated(self) -> None:
        """Pool=6 → floor interpolated between 0.40 and 0.55."""
        chunks = [_chunk(f"C{i}") for i in range(6)]
        reranker = _make_reranker([0.01] * 6)
        result = rerank("query", chunks, reranker=reranker, top_k=5)
        # pool=6: floor = 0.40 + (6-3)*(0.15/7) = 0.40 + 0.0643 ≈ 0.464
        expected_floor = 0.40 + (6 - 3) * 0.15 / 7
        assert result[0].score == pytest.approx(expected_floor, abs=0.001)

    def test_floor_not_applied_when_score_already_above(self) -> None:
        """Floor should not downgrade scores above the floor."""
        chunks = [_chunk(f"C{i}") for i in range(12)]
        reranker = _make_reranker([0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.05, 0.04, 0.03])
        result = rerank("query", chunks, reranker=reranker, top_k=5)
        # Top chunks already above floor, should keep original scores
        assert result[0].score == pytest.approx(0.9)
        assert result[1].score == pytest.approx(0.8)

    def test_floor_metadata_stores_original_score(self) -> None:
        """When floor is applied, original score stored in metadata."""
        chunks = [_chunk(f"C{i}") for i in range(12)]
        reranker = _make_reranker([0.01] * 12)
        result = rerank("query", chunks, reranker=reranker, top_k=5)
        assert "score_floored_from" in result[0].metadata
        assert result[0].metadata["score_floored_from"] == pytest.approx(0.01)


# ── TestGetReranker ───────────────────────────────────────────────────────────


class TestGetReranker:
    def test_import_error_raises_helpful_message(self) -> None:
        from src.retrieval import reranker as reranker_mod

        reranker_mod.get_reranker.cache_clear()
        with patch.dict(sys.modules, {"FlagEmbedding": None}):
            with pytest.raises(ImportError, match="FlagEmbedding"):
                reranker_mod.get_reranker()
        reranker_mod.get_reranker.cache_clear()
