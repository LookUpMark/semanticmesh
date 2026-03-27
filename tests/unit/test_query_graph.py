"""Unit tests for src/generation/query_graph.py — UT-23 (routing logic)."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from src.generation.nodes.generation_nodes import (
    _node_answer_generation,
    _compose_generation_chunks,
)
from src.generation.nodes.expansion_nodes import _node_context_distillation
from src.generation.query_graph import (
    _node_finalise,
    _node_retrieve,  # Renamed from _node_hybrid_retrieval
    _node_rerank,  # Renamed from _node_reranking
    _node_retrieval_quality_gate,
)
from src.generation.routing import (
    _route_after_grader,
    _route_after_retrieval_gate,
)
from src.models.schemas import GraderDecision, RetrievedChunk

# Helpers


def _state(action: str, grounded: bool = True) -> dict:
    return {"grader_decision": GraderDecision(grounded=grounded, critique=None, action=action)}


class TestRouteAfterGrader:
    def test_pass_routes_to_finalise(self) -> None:
        assert _route_after_grader(_state("pass")) == "finalise"

    def test_regenerate_routes_to_answer_generation(self) -> None:
        assert _route_after_grader(_state("regenerate", grounded=False)) == "answer_generation"

    def test_web_search_routes_to_finalise(self) -> None:
        assert _route_after_grader(_state("web_search", grounded=False)) == "finalise"

    def test_none_decision_routes_to_finalise(self) -> None:
        assert _route_after_grader({"grader_decision": None}) == "finalise"

    def test_missing_key_routes_to_finalise(self) -> None:
        assert _route_after_grader({}) == "finalise"

    def test_unknown_action_routes_to_finalise(self) -> None:
        mock_decision = MagicMock(action="unknown_action")
        assert _route_after_grader({"grader_decision": mock_decision}) == "finalise"


class TestRouteAfterRetrievalGate:
    def test_abstain_early_routes_to_finalise(self) -> None:
        assert (
            _route_after_retrieval_gate({"retrieval_gate_decision": "abstain_early"}) == "finalise"
        )

    def test_proceed_routes_to_context_distillation(self) -> None:
        assert (
            _route_after_retrieval_gate({"retrieval_gate_decision": "proceed"})
            == "context_distillation"
        )


class TestBuildQueryGraph:
    def test_graph_compiles(self) -> None:
        from src.generation.query_graph import build_query_graph

        with (
            patch("src.retrieval.embeddings.get_embeddings", return_value=MagicMock()),
            patch("src.config.llm_factory.get_reasoning_llm", return_value=MagicMock()),
            patch("src.graph.neo4j_client.Neo4jClient", MagicMock()),
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

    def test_keeps_all_valid_ranked_chunks(self) -> None:
        settings = MagicMock()
        settings.enable_reranker = True
        settings.reranker_top_k = 5

        with (
            patch("src.generation.nodes.retrieval_nodes.get_settings", return_value=settings),
            patch(
                "src.generation.nodes.retrieval_nodes.rerank",
                return_value=[self._chunk("A", 0.9), self._chunk("B", 0.2)],
            ),
        ):
            state = {"user_query": "q", "retrieved_chunks": [self._chunk("seed", 0.1)]}
            out = _node_rerank(state)
            assert [c.node_id for c in out["reranked_chunks"]] == ["A", "B"]
            assert out["retrieval_quality_score"] == 0.9
            assert out["retrieval_chunk_count"] == 2
            assert out["context_sufficiency"] == "adequate"
            assert out["retrieval_filtered_by_threshold"] is False

    def test_returns_empty_when_no_valid_chunks(self) -> None:
        settings = MagicMock()
        settings.enable_reranker = True
        settings.reranker_top_k = 5

        bad_chunk = RetrievedChunk(
            node_id="",
            node_type="BusinessConcept",
            text="",
            score=0.9,
            source_type="vector",
            metadata={},
        )

        with (
            patch("src.generation.nodes.retrieval_nodes.get_settings", return_value=settings),
            patch("src.generation.nodes.retrieval_nodes.rerank", return_value=[bad_chunk]),
        ):
            state = {"user_query": "q", "retrieved_chunks": [bad_chunk]}
            out = _node_rerank(state)
            assert out["reranked_chunks"] == []
            assert out["retrieval_filtered_by_threshold"] is False
            assert out["context_sufficiency"] == "insufficient"

    def test_prefilters_noisy_heuristic_chunks(self) -> None:
        settings = MagicMock()
        settings.enable_reranker = False
        settings.reranker_top_k = 5

        noisy = RetrievedChunk(
            node_id="Customers",
            node_type="BusinessConcept",
            text="Customers: Heuristic embedding mapping score=0.506, adjusted_confidence=0.753, best_candidate='Customers'.",
            score=0.8,
            source_type="graph",
            metadata={},
        )
        useful = RetrievedChunk(
            node_id="SALES_ORDER_HDR→CUSTOMER_MASTER",
            node_type="relationship",
            text="The table SALES_ORDER_HDR references CUSTOMER_MASTER via a foreign key.",
            score=0.2,
            source_type="graph",
            metadata={},
        )

        with patch("src.generation.nodes.retrieval_nodes.get_settings", return_value=settings):
            out = _node_rerank(
                {
                    "user_query": "How is customer linked to orders?",
                    "retrieved_chunks": [noisy, useful],
                }
            )

        assert len(out["reranked_chunks"]) == 1
        assert out["reranked_chunks"][0].node_id == "SALES_ORDER_HDR→CUSTOMER_MASTER"


class TestNodeHybridRetrievalLazyExpansion:
    def _chunk(self, name: str, score: float) -> RetrievedChunk:
        return RetrievedChunk(
            node_id=name,
            node_type="BusinessConcept",
            text=f"{name}: definition",
            score=score,
            source_type="vector",
            metadata={},
        )

    def test_triggers_lazy_expansion_when_top_score_low(self) -> None:
        settings = MagicMock(
            retrieval_mode="hybrid",
            retrieval_vector_top_k=3,
            retrieval_bm25_top_k=3,
            retrieval_graph_depth=1,
            enable_lazy_expansion=True,
            lazy_expansion_confidence_threshold=0.4,
        )

        vec = [self._chunk("A", 0.2)]
        bm = [self._chunk("B", 0.15)]
        trav = [self._chunk("C", 0.1)]
        concepts = []
        fks = []
        extra = [self._chunk("D", 0.35)]

        with (
            patch("src.generation.nodes.retrieval_nodes.get_settings", return_value=settings),
            patch("src.generation.nodes.retrieval_nodes.get_embeddings", return_value=MagicMock()),
            patch("src.generation.nodes.retrieval_nodes.Neo4jClient") as mock_client_cls,
            patch("src.generation.nodes.retrieval_nodes.build_node_index", return_value=[]),
            patch("src.generation.nodes.retrieval_nodes.vector_search", return_value=vec),
            patch("src.generation.nodes.retrieval_nodes.bm25_search", return_value=bm),
            patch(
                "src.generation.nodes.retrieval_nodes.graph_traversal", side_effect=[trav, extra]
            ) as mock_trav,
            patch("src.generation.nodes.retrieval_nodes.fetch_all_concepts", return_value=concepts),
            patch("src.generation.nodes.retrieval_nodes.fetch_fk_relationships", return_value=fks),
            patch(
                "src.generation.nodes.retrieval_nodes.merge_results",
                side_effect=[vec + bm + trav, vec + bm + trav + extra],
            ),
        ):
            mock_client = MagicMock()
            mock_client_cls.return_value.__enter__.return_value = mock_client
            out = _node_retrieve({"user_query": "How are customers and orders related?"})

        assert len(out["retrieved_chunks"]) == 4
        assert mock_trav.call_count == 2


class TestNodeRetrievalQualityGate:
    def test_sparse_structural_single_chunk_proceeds_with_warning(self) -> None:
        settings = MagicMock(enable_retrieval_quality_gate=True)
        rel_chunk = RetrievedChunk(
            node_id="SALES_ORDER_HDR→CUSTOMER_MASTER",
            node_type="relationship",
            text="Foreign key from SALES_ORDER_HDR to CUSTOMER_MASTER references CUST_ID.",
            score=0.02,
            source_type="graph",
            metadata={},
        )
        state = {
            "user_query": "How are orders linked to customers?",
            "retrieval_quality_score": 0.02,
            "retrieval_chunk_count": 1,
            "retrieval_filtered_by_threshold": False,
            "context_sufficiency": "sparse",
            "reranked_chunks": [rel_chunk],
        }

        with patch("src.generation.query_graph.get_settings", return_value=settings):
            out = _node_retrieval_quality_gate(state)

        assert out["retrieval_gate_decision"] == "proceed_with_warning"


class TestAnswerGenerationContextComposition:
    def _chunk(
        self, name: str, text: str, source: str = "graph", score: float = 0.4
    ) -> RetrievedChunk:
        return RetrievedChunk(
            node_id=name,
            node_type="BusinessConcept",
            text=text,
            score=score,
            source_type=source,
            metadata={},
        )

    def test_answer_generation_uses_balanced_subset(self) -> None:
        rel = self._chunk(
            "SALES_ORDER_HDR→CUSTOMER_MASTER",
            "The table SALES_ORDER_HDR references CUSTOMER_MASTER via a foreign key.",
            source="graph",
            score=0.8,
        )
        vec = self._chunk(
            "Customer",
            "Customer entity and profile information.",
            source="vector",
            score=0.7,
        )
        extras = [
            self._chunk(f"X{i}", f"Extra context {i}", source="graph", score=0.2 - i * 0.01)
            for i in range(12)
        ]
        state = {
            "user_query": "How is a customer linked to orders?",
            "reranked_chunks": [rel, vec] + extras,
            "context_sufficiency": "adequate",
            "iteration_count": 0,
        }

        with (
            patch(
                "src.generation.nodes.generation_nodes.get_reasoning_llm", return_value=MagicMock()
            ),
            patch(
                "src.generation.nodes.generation_nodes.generate_answer", return_value="ok"
            ) as mock_generate,
        ):
            out = _node_answer_generation(state)

        used_chunks = mock_generate.call_args.args[1]
        assert len(used_chunks) <= 12
        assert any(c.node_id == "SALES_ORDER_HDR→CUSTOMER_MASTER" for c in used_chunks)
        assert out["generation_chunks"] == used_chunks

    def test_finalise_prefers_generation_chunks_for_output_context(self) -> None:
        reranked = [self._chunk("A", "A: noisy", score=0.1)]
        generation = [self._chunk("B", "B: focused evidence", score=0.9)]
        state = {
            "current_answer": "answer",
            "retrieval_gate_decision": "proceed",
            "reranked_chunks": reranked,
            "generation_chunks": generation,
            "retrieval_quality_score": 0.9,
            "retrieval_chunk_count": 1,
            "retrieval_filtered_by_threshold": False,
            "context_sufficiency": "adequate",
        }

        out = _node_finalise(state)
        assert out["sources"] == ["B"]
        assert out["retrieved_contexts"] == ["B: focused evidence"]


class TestContextDistillationNode:
    def _chunk(
        self, name: str, text: str, source: str = "graph", score: float = 0.4
    ) -> RetrievedChunk:
        return RetrievedChunk(
            node_id=name,
            node_type="BusinessConcept",
            text=text,
            score=score,
            source_type=source,
            metadata={},
        )

    def test_distills_noisy_chunk_text(self) -> None:
        noisy = self._chunk(
            "Customers",
            "Customers: Heuristic embedding mapping score=0.506, adjusted_confidence=0.753, threshold=0.600, best_candidate='Customers'.",
            source="graph",
            score=0.5,
        )
        fk = self._chunk(
            "SALES_ORDER_HDR→CUSTOMER_MASTER",
            "The table SALES_ORDER_HDR references CUSTOMER_MASTER via a foreign key (column CUST_ID → CUSTOMER_MASTER.CUST_ID). This means each record in SALES_ORDER_HDR is linked to a record in CUSTOMER_MASTER.",
            source="graph",
            score=0.8,
        )
        state = {
            "user_query": "How is a customer linked to orders?",
            "reranked_chunks": [noisy, fk],
        }

        out = _node_context_distillation(state)
        texts = [c.text for c in out["generation_chunks"]]
        assert any(t.startswith("Relationship:") for t in texts)
        assert not any("heuristic embedding mapping score=" in t.lower() for t in texts)


class TestChannelBalancedComposition:
    def _chunk(self, name: str, source: str, score: float) -> RetrievedChunk:
        return RetrievedChunk(
            node_id=name,
            node_type="BusinessConcept",
            text=f"{name}: context",
            score=score,
            source_type=source,
            metadata={},
        )

    def test_limits_graph_dominance_when_other_channels_exist(self) -> None:
        chunks = []
        # Many graph chunks with higher scores
        chunks.extend([self._chunk(f"G{i}", "graph", 0.9 - i * 0.01) for i in range(12)])
        # Fewer vector and bm25 chunks
        chunks.extend([self._chunk(f"V{i}", "vector", 0.7 - i * 0.01) for i in range(3)])
        chunks.extend([self._chunk(f"B{i}", "bm25", 0.6 - i * 0.01) for i in range(3)])

        out = _compose_generation_chunks(
            "customer orders relationship", chunks, max_core=6, max_support=4
        )
        assert len(out) == 10
        graph_count = sum(1 for c in out if c.source_type == "graph")
        vector_count = sum(1 for c in out if c.source_type == "vector")
        bm25_count = sum(1 for c in out if c.source_type == "bm25")

        assert graph_count <= 5
        assert vector_count >= 1
        assert bm25_count >= 1
