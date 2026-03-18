"""Unit tests for src/generation/query_graph.py — UT-23 (routing logic)."""

from __future__ import annotations

from unittest.mock import MagicMock

from src.generation.query_graph import _route_after_grader
from src.models.schemas import GraderDecision

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
        from src.generation.query_graph import build_query_graph

        graph = build_query_graph()
        assert graph is not None
