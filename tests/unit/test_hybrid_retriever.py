"""Unit tests for src/retrieval/embeddings.py — UT-12 (BGE-M3 embedder)."""

from __future__ import annotations

import sys
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

# ── Helpers ───────────────────────────────────────────────────────────────────


def _fake_model(dim: int = 1024) -> MagicMock:
    """Return a mock FlagModel whose encode() returns zero vectors."""
    model = MagicMock()
    model.encode = MagicMock(
        side_effect=lambda texts, **kw: np.zeros((len(texts), dim), dtype="float32")
    )
    return model


# ── TestEmbedTexts ────────────────────────────────────────────────────────────


class TestEmbedTexts:
    def test_returns_list_of_lists(self) -> None:
        from src.retrieval.embeddings import embed_texts

        result = embed_texts(["hello", "world"], model=_fake_model())
        assert isinstance(result, list)
        assert len(result) == 2
        assert isinstance(result[0], list)
        assert len(result[0]) == 1024

    def test_empty_input_returns_empty(self) -> None:
        from src.retrieval.embeddings import embed_texts

        result = embed_texts([], model=MagicMock())
        assert result == []

    def test_single_text(self) -> None:
        from src.retrieval.embeddings import embed_text

        vec = embed_text("test sentence", model=_fake_model())
        assert isinstance(vec, list)
        assert len(vec) == 1024

    def test_calls_model_encode_with_texts(self) -> None:
        from src.retrieval.embeddings import embed_texts

        model = _fake_model()
        embed_texts(["a", "b", "c"], model=model)
        model.encode.assert_called_once()
        call_args = model.encode.call_args
        # First positional arg is the texts list
        assert call_args[0][0] == ["a", "b", "c"]

    def test_uses_singleton_when_no_model_passed(self) -> None:
        from src.retrieval import embeddings as emb_mod

        fake = _fake_model()
        with patch.object(emb_mod, "get_embeddings", return_value=fake) as mock_get:
            emb_mod.embed_texts(["query"], model=None)
            mock_get.assert_called_once()

    def test_all_vectors_have_correct_dimension(self) -> None:
        from src.retrieval.embeddings import embed_texts

        texts = ["alpha", "beta", "gamma", "delta"]
        result = embed_texts(texts, model=_fake_model())
        assert all(len(v) == 1024 for v in result)

    def test_returns_list_of_floats(self) -> None:
        from src.retrieval.embeddings import embed_texts

        result = embed_texts(["check"], model=_fake_model())
        assert all(isinstance(x, float) for x in result[0])


# ── TestGetEmbeddings ─────────────────────────────────────────────────────────


class TestGetEmbeddings:
    def test_import_error_raises_helpful_message(self) -> None:
        from src.retrieval import embeddings as emb_mod

        # Clear lru_cache before patching so the function runs fresh
        emb_mod.get_embeddings.cache_clear()
        with patch.dict(sys.modules, {"FlagEmbedding": None}):
            with pytest.raises(ImportError, match="FlagEmbedding"):
                emb_mod.get_embeddings()
        # Always restore cache after test
        emb_mod.get_embeddings.cache_clear()


# ═══════════════════════════════════════════════════════════════════════════════
# TASK-24 — hybrid_retriever tests (UT-12 continued)
# ═══════════════════════════════════════════════════════════════════════════════

from src.models.schemas import RetrievedChunk  # noqa: E402
from src.retrieval.hybrid_retriever import (  # noqa: E402
    _node_to_text,
    bm25_search,
    graph_traversal,
    merge_results,
    vector_search,
)

# ── Helpers ────────────────────────────────────────────────────────────────────


def _chunk(name: str, score: float, source: str = "vector") -> RetrievedChunk:
    return RetrievedChunk(
        node_id=name,
        node_type="BusinessConcept",
        text=f"{name}: definition",
        score=score,
        source_type=source,  # type: ignore[arg-type]
        metadata={},
    )


def _make_client(records: list[dict]) -> MagicMock:
    client = MagicMock()
    client.execute_cypher.return_value = records
    return client


# ── TestNodeToText ─────────────────────────────────────────────────────────────


class TestNodeToText:
    def test_joins_all_fields(self) -> None:
        node = {
            "name": "Customer",
            "definition": "A buyer",
            "synonyms": ["Client"],
            "column_names": ["ID"],
        }
        text = _node_to_text(node)
        assert "customer" in text
        assert "buyer" in text
        assert "client" in text
        assert "id" in text

    def test_handles_missing_fields(self) -> None:
        node = {"name": "X"}
        text = _node_to_text(node)
        assert "x" in text


# ── TestVectorSearch ───────────────────────────────────────────────────────────


class TestVectorSearch:
    def _model(self) -> MagicMock:
        model = MagicMock()
        model.encode = MagicMock(return_value=np.zeros((1, 1024), dtype="float32"))
        return model

    def test_returns_retrieved_chunks(self) -> None:
        client = _make_client(
            [
                {
                    "name": "Customer",
                    "definition": "A buyer",
                    "score": 0.95,
                    "node_type": "BusinessConcept",
                    "source_doc": "x.pdf",
                    "synonyms": ["Client"],
                }
            ]
        )
        results = vector_search("customer", client, top_k=5, model=self._model())
        assert len(results) == 1
        assert results[0].source_type == "vector"
        assert results[0].score == pytest.approx(0.95)

    def test_empty_neo4j_result_returns_empty(self) -> None:
        client = _make_client([])
        results = vector_search("nothing", client, top_k=5, model=self._model())
        assert results == []


# ── TestBm25Search ─────────────────────────────────────────────────────────────


class TestBm25Search:
    def _nodes(self) -> list[dict]:
        return [
            {
                "name": "Customer",
                "definition": "A person who buys goods",
                "synonyms": [],
                "column_names": [],
                "node_type": "BusinessConcept",
            },
            {
                "name": "Product",
                "definition": "A sellable item in the inventory",
                "synonyms": ["Item"],
                "column_names": [],
                "node_type": "BusinessConcept",
            },
            {
                "name": "Order",
                "definition": "A purchase transaction",
                "synonyms": [],
                "column_names": [],
                "node_type": "BusinessConcept",
            },
        ]

    def test_top_result_is_most_relevant(self) -> None:
        results = bm25_search("customer buying goods", self._nodes(), top_k=3)
        assert results[0].node_id == "Customer"

    def test_source_type_is_bm25(self) -> None:
        results = bm25_search("product", self._nodes(), top_k=1)
        assert results[0].source_type == "bm25"

    def test_empty_nodes_returns_empty(self) -> None:
        assert bm25_search("query", [], top_k=5) == []

    def test_top_k_limits_results(self) -> None:
        results = bm25_search("purchase", self._nodes(), top_k=1)
        assert len(results) <= 1


# ── TestGraphTraversal ─────────────────────────────────────────────────────────


class TestGraphTraversal:
    def test_returns_neighbours(self) -> None:
        client = _make_client(
            [
                {
                    "name": "Order",
                    "definition": "A purchase",
                    "node_type": "BusinessConcept",
                    "rel_type": "RELATED_TO",
                },
            ]
        )
        results = graph_traversal(["Customer"], client, depth=2)
        assert len(results) == 1
        assert results[0].source_type == "graph"

    def test_empty_seeds_returns_empty(self) -> None:
        assert graph_traversal([], _make_client([]), depth=2) == []

    def test_excludes_seed_names_from_results(self) -> None:
        client = _make_client(
            [
                {
                    "name": "Customer",
                    "definition": "loop node",
                    "node_type": "BC",
                    "rel_type": "SELF",
                },
            ]
        )
        results = graph_traversal(["Customer"], client, depth=1)
        assert all(r.node_id != "Customer" for r in results)


# ── TestMergeResults ───────────────────────────────────────────────────────────


class TestMergeResults:
    def test_deduplicates_by_node_id(self) -> None:
        v = [_chunk("Customer", 0.9, "vector")]
        b = [_chunk("Customer", 0.7, "bm25")]
        g = [_chunk("Order", 0.5, "graph")]
        merged = merge_results(v, b, g)
        names = [c.node_id for c in merged]
        assert names.count("Customer") == 1

    def test_keeps_highest_score(self) -> None:
        v = [_chunk("Customer", 0.9, "vector")]
        b = [_chunk("Customer", 0.7, "bm25")]
        merged = merge_results(v, b, [])
        assert merged[0].score == pytest.approx(0.9)

    def test_sorted_descending(self) -> None:
        v = [_chunk("B", 0.6), _chunk("A", 0.9)]
        merged = merge_results(v, [], [])
        assert merged[0].node_id == "A"

    def test_empty_inputs_returns_empty(self) -> None:
        assert merge_results([], [], []) == []
