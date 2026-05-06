"""Unit tests for src.retrieval.bm25_retriever."""

from __future__ import annotations

import pytest

from src.retrieval.bm25_retriever import (
    _expand_query_tokens,
    bm25_search,
    invalidate_bm25_cache,
)


@pytest.fixture(autouse=True)
def _reset_cache():
    """Ensure clean BM25 cache for each test."""
    invalidate_bm25_cache()
    yield
    invalidate_bm25_cache()


def _make_nodes() -> list[dict]:
    return [
        {"name": "Customer", "definition": "A person who buys products", "node_type": "BusinessConcept"},
        {"name": "Order", "definition": "A purchase transaction placed by a customer", "node_type": "BusinessConcept"},
        {"name": "Product", "definition": "An item available for sale in the store", "node_type": "BusinessConcept"},
        {"text": "Customers place orders for products", "node_type": "ParentChunk", "chunk_index": 0, "source_doc": "doc1"},
    ]


class TestBm25Search:
    def test_returns_results_for_matching_query(self) -> None:
        nodes = _make_nodes()
        results = bm25_search("customer purchase", nodes, top_k=3)
        assert len(results) > 0
        assert all(r.source_type == "bm25" for r in results)

    def test_respects_top_k(self) -> None:
        nodes = _make_nodes()
        results = bm25_search("customer order product", nodes, top_k=2)
        assert len(results) <= 2

    def test_empty_nodes_returns_empty(self) -> None:
        results = bm25_search("anything", [], top_k=5)
        assert results == []

    def test_parent_chunk_nodes_included(self) -> None:
        nodes = _make_nodes()
        results = bm25_search("customers place orders", nodes, top_k=5)
        parent_results = [r for r in results if r.node_type == "ParentChunk"]
        assert len(parent_results) >= 1
        assert parent_results[0].source_type == "bm25"

    def test_results_sorted_by_score_descending(self) -> None:
        nodes = _make_nodes()
        results = bm25_search("customer order", nodes, top_k=5)
        scores = [r.score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_cache_reuse(self) -> None:
        """Second call with same node list reuses cached BM25 object."""
        nodes = _make_nodes()
        r1 = bm25_search("customer", nodes, top_k=2)
        r2 = bm25_search("product", nodes, top_k=2)
        # Both should work without error (cache hit on second call)
        assert len(r1) > 0
        assert len(r2) > 0


class TestExpandQueryTokens:
    def test_expands_status_keyword(self) -> None:
        tokens = ["what", "status", "values"]
        expanded = _expand_query_tokens(tokens)
        assert "status_code" in expanded
        assert "check" in expanded

    def test_no_expansion_for_unknown_tokens(self) -> None:
        tokens = ["hello", "world"]
        expanded = _expand_query_tokens(tokens)
        assert expanded == ["hello", "world"]

    def test_handles_punctuation(self) -> None:
        tokens = ["status?", "constraint."]
        expanded = _expand_query_tokens(tokens)
        assert "status_code" in expanded
        assert "unique" in expanded
