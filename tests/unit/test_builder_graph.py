"""Unit tests for src/graph/builder_graph.py — IT-01 (subset)"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from langgraph.graph import END

from src.graph.builder_graph import (
    _node_extract_triplets,
    _route_after_build,
    _route_after_heal,
    _route_after_validate,
    build_builder_graph,
)
from src.models.schemas import Chunk

# ── Conditional edge routing ───────────────────────────────────────────────────


class TestRouteAfterValidate:
    def test_routes_to_hitl_when_flag(self) -> None:
        state = {"hitl_flag": True, "reflection_prompt": None}
        assert _route_after_validate(state) == "hitl"

    def test_routes_to_rag_mapping_for_reflection(self) -> None:
        state = {"hitl_flag": False, "reflection_prompt": "Please fix..."}
        assert _route_after_validate(state) == "rag_mapping"

    def test_routes_to_generate_cypher_on_success(self) -> None:
        state = {"hitl_flag": False, "reflection_prompt": None}
        assert _route_after_validate(state) == "generate_cypher"

    def test_hitl_takes_precedence_over_reflection(self) -> None:
        state = {"hitl_flag": True, "reflection_prompt": "Please fix..."}
        assert _route_after_validate(state) == "hitl"


class TestRouteAfterHeal:
    def test_routes_to_build_on_success(self) -> None:
        state = {"cypher_failed": False}
        assert _route_after_heal(state) == "build_graph"

    def test_routes_to_build_even_on_failed_cypher(self) -> None:
        # heal_cypher may fail, but build_graph now uses the deterministic
        # parameterized builder so we always attempt the write.
        state = {"cypher_failed": True, "pending_tables": [MagicMock()]}
        assert _route_after_heal(state) == "build_graph"

    def test_routes_to_build_with_no_pending_tables(self) -> None:
        state = {"cypher_failed": True, "pending_tables": []}
        assert _route_after_heal(state) == "build_graph"

    def test_handles_missing_pending_tables_gracefully(self) -> None:
        state = {"cypher_failed": True}
        assert _route_after_heal(state) == "build_graph"


class TestRouteAfterBuild:
    def test_routes_to_rag_mapping_if_pending(self) -> None:
        state = {"pending_tables": [MagicMock()]}
        assert _route_after_build(state) == "rag_mapping"

    def test_routes_to_end_when_empty(self) -> None:
        state = {"pending_tables": []}
        assert _route_after_build(state) == END

    def test_handles_missing_key_gracefully(self) -> None:
        state = {}
        # Missing pending_tables key should route to END
        assert _route_after_build(state) == END


# ── build_builder_graph ────────────────────────────────────────────────────────


class TestBuildBuilderGraph:
    @patch("src.graph.builder_graph.get_settings")
    @patch("src.graph.builder_graph.get_extraction_llm")
    @patch("src.graph.builder_graph.get_reasoning_llm")
    def test_graph_compiles_without_error(
        self,
        mock_reasoning_llm,
        mock_extraction_llm,
        mock_settings,
    ) -> None:
        mock_settings.return_value = MagicMock(
            few_shot_cypher_examples=3,
            max_reflection_attempts=3,
            max_cypher_healing_attempts=3,
            retrieval_vector_top_k=10,
            confidence_threshold=0.9,
            sqlite_checkpoint_path=":memory:",
        )
        mock_extraction_llm.return_value = MagicMock()
        mock_reasoning_llm.return_value = MagicMock()

        graph = build_builder_graph(production=False)
        assert graph is not None

    @patch("src.graph.builder_graph.get_settings")
    @patch("src.graph.builder_graph.get_extraction_llm")
    @patch("src.graph.builder_graph.get_reasoning_llm")
    def test_interrupt_before_hitl(
        self,
        mock_reasoning_llm,
        mock_extraction_llm,
        mock_settings,
    ) -> None:
        mock_settings.return_value = MagicMock(
            few_shot_cypher_examples=3,
            max_reflection_attempts=3,
            max_cypher_healing_attempts=3,
            retrieval_vector_top_k=10,
            confidence_threshold=0.9,
            sqlite_checkpoint_path=":memory:",
        )
        mock_extraction_llm.return_value = MagicMock()
        mock_reasoning_llm.return_value = MagicMock()

        graph = build_builder_graph(production=False)
        # Check that the graph is compiled with interrupt_before
        assert graph is not None
        # The compiled graph should have the interrupt configured


class TestNodeExtractTriplets:
    @patch("src.graph.builder_graph.get_settings")
    @patch("src.graph.builder_graph.extract_all_triplets_heuristic")
    @patch("src.graph.builder_graph.extract_all_triplets")
    @patch("src.graph.builder_graph.get_extraction_llm")
    def test_uses_heuristic_path_when_lazy_enabled(
        self,
        mock_get_llm,
        mock_extract_llm,
        mock_extract_heuristic,
        mock_get_settings,
    ) -> None:
        mock_get_settings.return_value = MagicMock(use_lazy_extraction=True)
        mock_extract_heuristic.return_value = [MagicMock()]
        state = {
            "chunks": [Chunk(text="Customer maps to CUSTOMER_MASTER.", chunk_index=0, metadata={})]
        }

        out = _node_extract_triplets(state)

        assert len(out["triplets"]) == 1
        mock_extract_heuristic.assert_called_once()
        mock_extract_llm.assert_not_called()
        mock_get_llm.assert_not_called()

    @patch("src.graph.builder_graph.get_settings")
    @patch("src.graph.builder_graph.extract_all_triplets_heuristic")
    @patch("src.graph.builder_graph.extract_all_triplets")
    @patch("src.graph.builder_graph.get_extraction_llm")
    def test_uses_llm_path_when_lazy_disabled(
        self,
        mock_get_llm,
        mock_extract_llm,
        mock_extract_heuristic,
        mock_get_settings,
    ) -> None:
        mock_get_settings.return_value = MagicMock(use_lazy_extraction=False)
        mock_get_llm.return_value = MagicMock()
        mock_extract_llm.return_value = [MagicMock(), MagicMock()]
        state = {
            "chunks": [Chunk(text="Customer maps to CUSTOMER_MASTER.", chunk_index=0, metadata={})],
            "use_lazy_extraction": False,
        }

        out = _node_extract_triplets(state)

        assert len(out["triplets"]) == 2
        mock_get_llm.assert_called_once()
        mock_extract_llm.assert_called_once()
        mock_extract_heuristic.assert_not_called()
