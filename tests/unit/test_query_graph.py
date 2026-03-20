"""Unit tests for src/generation/query_graph.py — UT-23 (routing logic)."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from src.generation.query_graph import _node_reranking, _route_after_grader
from src.models.schemas import GraderDecision, RetrievedChunk

# ── Helpers ───────────────────────────────────────────────────────────────────


def _state(action: str, grounded: bool = True) -> dict:
    return {"grader_decision": GraderDecision(grounded=grounded, critique=None, action=action)}


# ── _route_after_grader ───────────────────────────────────────────────────────


class TestRouteAfterGrader:
    def test_pass_routes_to_finalise(self) -> None:
        assert _route_after_grader(_state("pass")) == "finalise"

    def test_regenerate_routes_to_answer_generation(self) -> None:
        assert _route_after_grader(_state("regenerate", grounded=False)) == "answer_generation"

    def test_web_search_routes_to_finalise(self) -> None:
        # web_search action no longer exists; unknown actions fall through to finalise
        assert _route_after_grader(_state("web_search", grounded=False)) == "finalise"

    def test_none_decision_routes_to_finalise(self) -> None:
        assert _route_after_grader({"grader_decision": None}) == "finalise"

    def test_missing_key_routes_to_finalise(self) -> None:
        assert _route_after_grader({}) == "finalise"

    def test_unknown_action_routes_to_finalise(self) -> None:
        mock_decision = MagicMock(action="unknown_action")
        assert _route_after_grader({"grader_decision": mock_decision}) == "finalise"


# ── build_query_graph ─────────────────────────────────────────────────────────


class TestBuildQueryGraph:
    def test_graph_compiles(self) -> None:
        from unittest.mock import MagicMock, patch

        from src.generation.query_graph import build_query_graph

        with (
            patch("src.generation.query_graph.get_embeddings", return_value=MagicMock()),
            patch("src.generation.query_graph.get_reasoning_llm", return_value=MagicMock()),
            patch("src.generation.query_graph.Neo4jClient", MagicMock()),
        ):
            graph = build_query_graph()
            assert graph is not None


class TestNodeReranking:
    def _chunk(self, name: str, score: float) -> RetrievedChunk:
        return RetrievedChunk(
            node_id=name,
            node_type="BusinessConcept",
            text=f"{name}: definition",
            score=score,
            source_type="vector",
            metadata={},
        )

    def test_applies_min_score_filter(self) -> None:
        settings = MagicMock()
        settings.enable_reranker = True
        settings.reranker_top_k = 5
        settings.retrieval_min_score = 0.5
        settings.retrieval_min_score_ratio = 0.0

        with (
            patch("src.generation.query_graph.get_settings", return_value=settings),
            patch(
                "src.generation.query_graph.rerank",
                return_value=[self._chunk("A", 0.9), self._chunk("B", 0.2)],
            ),
        ):
            state = {"user_query": "q", "retrieved_chunks": [self._chunk("seed", 0.1)]}
            out = _node_reranking(state)
            assert [c.node_id for c in out["reranked_chunks"]] == ["A"]
            assert out["retrieval_quality_score"] == 0.9
            assert out["retrieval_chunk_count"] == 1
            assert out["context_sufficiency"] == "adequate"

    def test_returns_empty_when_top_score_below_min_score(self) -> None:
        settings = MagicMock()
        settings.enable_reranker = True
        settings.reranker_top_k = 5
        settings.retrieval_min_score = 0.95
        settings.retrieval_min_score_ratio = 0.0

        with (
            patch("src.generation.query_graph.get_settings", return_value=settings),
            patch(
                "src.generation.query_graph.rerank",
                return_value=[self._chunk("A", 0.9), self._chunk("B", 0.2)],
            ),
        ):
            state = {"user_query": "q", "retrieved_chunks": [self._chunk("seed", 0.1)]}
            out = _node_reranking(state)
            assert out["reranked_chunks"] == []
            assert out["retrieval_filtered_by_threshold"] is True
            assert out["context_sufficiency"] == "insufficient"

    def test_applies_relative_threshold_from_top_score(self) -> None:
        settings = MagicMock()
        settings.enable_reranker = True
        settings.reranker_top_k = 5
        settings.retrieval_min_score = 0.1
        settings.retrieval_min_score_ratio = 0.6

        with (
            patch("src.generation.query_graph.get_settings", return_value=settings),
            patch(
                "src.generation.query_graph.rerank",
                return_value=[
                    self._chunk("A", 0.9),
                    self._chunk("B", 0.62),
                    self._chunk("C", 0.52),
                ],
            ),
        ):
            state = {"user_query": "q", "retrieved_chunks": [self._chunk("seed", 0.1)]}
            out = _node_reranking(state)
            assert [c.node_id for c in out["reranked_chunks"]] == ["A", "B"]
            assert out["retrieval_chunk_count"] == 2
