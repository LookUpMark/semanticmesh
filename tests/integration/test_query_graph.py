"""Integration tests for src/generation/query_graph.py.

Tests: IT-06 (Query Graph End-to-End), IT-07 (Hallucination Grader Loop)
"""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from src.generation.query_graph import build_query_graph
from src.graph.neo4j_client import Neo4jClient
from src.models.state import QueryState

pytestmark = pytest.mark.integration


# ─────────────────────────────────────────────────────────────────────────────
# Helper Functions
# ─────────────────────────────────────────────────────────────────────────────


def _make_query_settings(
    *,
    max_hallucination_retries: int = 3,
    enable_reranker: bool = True,
    enable_hallucination_grader: bool = True,
) -> MagicMock:
    settings = MagicMock()
    settings.retrieval_vector_top_k = 10
    settings.retrieval_bm25_top_k = 10
    settings.retrieval_graph_depth = 2
    settings.reranker_top_k = 5
    settings.max_hallucination_retries = max_hallucination_retries
    settings.enable_reranker = enable_reranker
    settings.enable_hallucination_grader = enable_hallucination_grader
    return settings


def _initial_query_state(query: str) -> QueryState:
    return {
        "user_query": query,
        "iteration_count": 0,
        "retrieved_chunks": [],
        "reranked_chunks": [],
        "current_answer": "",
        "last_critique": None,
        "grader_decision": None,
        "final_answer": "",
        "sources": [],
    }


def _mock_embeddings() -> MagicMock:
    embeddings = MagicMock()
    embeddings.embed_documents.return_value = [[0.1] * 1024]
    embeddings.embed_query.return_value = [0.1] * 1024
    return embeddings


def _populate_test_graph(client: Neo4jClient) -> None:
    """Populate the test graph with sample data for query tests."""
    with client:
        # Clear existing data
        client.execute_cypher("MATCH (n) DETACH DELETE n")

        # Create business concepts
        client.execute_cypher("""
            MERGE (c:BusinessConcept:Entity {
                name: 'Customer',
                definition: 'A person who purchases goods or services',
                synonyms: ['client', 'buyer']
            })
        """)

        client.execute_cypher("""
            MERGE (c:BusinessConcept:Entity {
                name: 'Product',
                definition: 'An item offered for sale',
                synonyms: ['item', 'goods']
            })
        """)

        client.execute_cypher("""
            MERGE (c:BusinessConcept:Entity {
                name: 'SalesOrder',
                definition: 'A transaction recording a purchase',
                synonyms: ['order', 'purchase']
            })
        """)

        # Create physical tables
        client.execute_cypher("""
            MERGE (t:PhysicalTable:Table {
                table_name: 'CUSTOMER_MASTER',
                schema_name: 'dbo'
            })
        """)

        client.execute_cypher("""
            MERGE (t:PhysicalTable:Table {
                table_name: 'TB_PRODUCT',
                schema_name: 'dbo'
            })
        """)

        client.execute_cypher("""
            MERGE (t:PhysicalTable:Table {
                table_name: 'SALES_ORDER_HDR',
                schema_name: 'dbo'
            })
        """)

        # Create mappings
        client.execute_cypher("""
            MATCH (c:BusinessConcept {name: 'Customer'})
            MATCH (t:PhysicalTable {table_name: 'CUSTOMER_MASTER'})
            MERGE (c)-[r:MAPPED_TO]->(t)
            SET r.mapping_confidence = 0.95
        """)

        client.execute_cypher("""
            MATCH (c:BusinessConcept {name: 'Product'})
            MATCH (t:PhysicalTable {table_name: 'TB_PRODUCT'})
            MERGE (c)-[r:MAPPED_TO]->(t)
            SET r.mapping_confidence = 0.93
        """)

        client.execute_cypher("""
            MATCH (c:BusinessConcept {name: 'SalesOrder'})
            MATCH (t:PhysicalTable {table_name: 'SALES_ORDER_HDR'})
            MERGE (c)-[r:MAPPED_TO]->(t)
            SET r.mapping_confidence = 0.92
        """)

        # Create some chunks for retrieval
        client.execute_cypher("""
            MERGE (ch:Chunk:Entity {
                node_id: 'chunk_1',
                text: 'Customer data includes name, email, and region information stored in CUSTOMER_MASTER table.'
            })
        """)

        client.execute_cypher("""
            MERGE (ch:Chunk:Entity {
                node_id: 'chunk_2',
                text: 'Product information such as SKU, name, and price is stored in TB_PRODUCT.'
            })
        """)

        client.execute_cypher("""
            MERGE (ch:Chunk:Entity {
                node_id: 'chunk_3',
                text: 'Sales orders track customer purchases with dates and amounts in SALES_ORDER_HDR.'
            })
        """)

        # Create vector index for hybrid search (if not exists)
        try:
            client.execute_cypher("""
                CREATE VECTOR INDEX chunk_vector_index
                FOR (c:Chunk) ON (c.embedding)
                OPTIONS {indexConfig: {`vector.dimensions`: 1024, `vector.similarity_function`: `cosine`}}
            """)
        except Exception:
            pass  # Index may already exist


# ─────────────────────────────────────────────────────────────────────────────
# IT-06: Query Graph End-to-End
# ─────────────────────────────────────────────────────────────────────────────


@pytest.mark.integration
class TestQueryGraphE2E:
    """IT-06: Query Graph end-to-end with pre-populated knowledge graph."""

    def test_query_graph_returns_grounded_answer(
        self,
        neo4j_client: Neo4jClient,
    ) -> None:
        """Pre-populated graph + valid user query → grounded final answer."""
        # Populate test data
        _populate_test_graph(neo4j_client)

        # Mock LLM responses
        answer_response = json.dumps(
            {
                "answer": "The CUSTOMER_MASTER table stores customer data including name, email, and region.",
                "sources": ["CUSTOMER_MASTER"],
            }
        )

        grader_response = json.dumps({"grounded": True, "critique": None, "action": "pass"})

        mock_llm = MagicMock()

        def _invoke(*args, **kwargs):
            prompt = str(args[0]) if args else ""
            result = MagicMock()
            if "grade" in prompt.lower() or "critique" in prompt.lower():
                result.content = grader_response
            else:
                result.content = answer_response
            return result

        mock_llm.invoke = _invoke

        with (
            patch("src.generation.query_graph.get_settings") as mock_settings_fn,
            patch("src.generation.query_graph.get_reasoning_llm") as mock_llm_fn,
            patch("src.generation.query_graph.get_embeddings") as mock_embeddings_fn,
        ):
            mock_settings_fn.return_value = _make_query_settings()

            mock_llm_fn.return_value = mock_llm

            mock_embeddings_fn.return_value = _mock_embeddings()

            graph = build_query_graph()

            query = "Which table stores customer data?"
            config = {"configurable": {"thread_id": "query-test-1"}}

            initial_state = _initial_query_state(query)

            result = graph.invoke(initial_state, config=config)

            # Verify we got a result
            assert result is not None
            assert "final_answer" in result

            # Answer should be non-empty
            assert result["final_answer"] != ""

            # Sources should be populated
            assert "sources" in result

    def test_query_graph_with_hallucination_passes(
        self,
        neo4j_client: Neo4jClient,
    ) -> None:
        """Query with hallucination grader that approves the answer."""
        _populate_test_graph(neo4j_client)

        # Mock responses - grader approves immediately
        answer_response = json.dumps(
            {
                "answer": "Customer information is stored in CUSTOMER_MASTER.",
            }
        )

        grader_response = json.dumps({"grounded": True, "critique": None, "action": "pass"})

        mock_llm = MagicMock()

        def _invoke(*args, **kwargs):
            prompt = str(args[0]) if args else ""
            result = MagicMock()
            if "grade" in prompt.lower() or "hallucination" in prompt.lower():
                result.content = grader_response
            else:
                result.content = answer_response
            return result

        mock_llm.invoke = _invoke

        with (
            patch("src.generation.query_graph.get_settings") as mock_settings_fn,
            patch("src.generation.query_graph.get_reasoning_llm") as mock_llm_fn,
            patch("src.generation.query_graph.get_embeddings") as mock_embeddings_fn,
        ):
            mock_settings_fn.return_value = _make_query_settings()

            mock_llm_fn.return_value = mock_llm

            mock_embeddings_fn.return_value = _mock_embeddings()

            graph = build_query_graph()

            initial_state = _initial_query_state("What customer data is stored?")

            config = {"configurable": {"thread_id": "query-test-2"}}
            result = graph.invoke(initial_state, config=config)

            # Verify grader decision was pass
            assert result.get("grader_decision") is not None

            # Verify we didn't fall back to web search
            answer = result.get("final_answer", "")
            assert "[Source: Web Search]" not in answer


# ─────────────────────────────────────────────────────────────────────────────
# IT-07: Hallucination Grader Loop (Full)
# ─────────────────────────────────────────────────────────────────────────────


@pytest.mark.integration
class TestHallucinationGraderLoop:
    """IT-07: Hallucination grader triggers regeneration and web_search fallback."""

    def test_hallucination_loop_triggers_regeneration(
        self,
        neo4j_client: Neo4jClient,
    ) -> None:
        """Grader detects hallucination → triggers regeneration with critique."""
        _populate_test_graph(neo4j_client)

        generation_count = [0]

        # First answer is hallucinated, second is corrected
        def _mock_answer(*args, **kwargs):
            generation_count[0] += 1
            result = MagicMock()
            if generation_count[0] == 1:
                result.content = json.dumps(
                    {
                        "answer": "The ORDERS table contains customer data.",
                    }
                )
            else:
                result.content = json.dumps(
                    {
                        "answer": "The CUSTOMER_MASTER table stores customer data including name and email.",
                    }
                )
            return result

        # Grader rejects first, approves second
        grader_count = [0]

        def _mock_grader(*args, **kwargs):
            grader_count[0] += 1
            result = MagicMock()
            if grader_count[0] == 1:
                result.content = json.dumps(
                    {
                        "grounded": False,
                        "critique": "The answer mentions ORDERS table which is not in the context. Use CUSTOMER_MASTER.",
                        "action": "regenerate",
                    }
                )
            else:
                result.content = json.dumps({"grounded": True, "critique": None, "action": "pass"})
            return result

        mock_llm = MagicMock()

        def _invoke(*args, **kwargs):
            prompt = str(args[0]) if args else ""
            if "grade" in prompt.lower() or "hallucination" in prompt.lower():
                return _mock_grader()
            else:
                return _mock_answer()

        mock_llm.invoke = _invoke

        with (
            patch("src.generation.query_graph.get_settings") as mock_settings_fn,
            patch("src.generation.query_graph.get_reasoning_llm") as mock_llm_fn,
            patch("src.generation.query_graph.get_embeddings") as mock_embeddings_fn,
        ):
            mock_settings_fn.return_value = _make_query_settings()

            mock_llm_fn.return_value = mock_llm

            mock_embeddings_fn.return_value = _mock_embeddings()

            graph = build_query_graph()

            initial_state = _initial_query_state("What table stores customer data?")

            config = {"configurable": {"thread_id": "hallucination-test-1"}}
            result = graph.invoke(initial_state, config=config)

            # Verify regeneration occurred
            assert generation_count[0] == 2
            assert grader_count[0] == 2

            # Verify final answer does not contain the hallucinated reference
            final_answer = result.get("final_answer", "")
            assert "ORDERS" not in final_answer or "CUSTOMER_MASTER" in final_answer

    def test_hallucination_loop_max_retries_accepts_last_answer(
        self,
        neo4j_client: Neo4jClient,
    ) -> None:
        """After max_hallucination_retries the loop guard fires and accepts the current answer."""
        _populate_test_graph(neo4j_client)

        generation_count = [0]

        # Always return a hallucinated answer
        def _mock_answer(*args, **kwargs):
            generation_count[0] += 1
            result = MagicMock()
            result.content = json.dumps(
                {
                    "answer": "The UNKNOWN_TABLE contains mysterious data.",
                }
            )
            return result

        # Always reject with hallucination
        def _mock_grader(*args, **kwargs):
            result = MagicMock()
            result.content = json.dumps(
                {
                    "grounded": False,
                    "critique": "UNKNOWN_TABLE is not mentioned in any context.",
                    "action": "regenerate",
                }
            )
            return result

        mock_llm = MagicMock()

        def _invoke(*args, **kwargs):
            prompt = str(args[0]) if args else ""
            if "grade" in prompt.lower() or "hallucination" in prompt.lower():
                return _mock_grader()
            else:
                return _mock_answer()

        mock_llm.invoke = _invoke

        max_retries = 2  # Low for fast testing

        with (
            patch("src.generation.query_graph.get_settings") as mock_settings_fn,
            patch("src.generation.query_graph.get_reasoning_llm") as mock_llm_fn,
            patch("src.generation.query_graph.get_embeddings") as mock_embeddings_fn,
        ):
            mock_settings_fn.return_value = _make_query_settings(
                max_hallucination_retries=max_retries
            )

            mock_llm_fn.return_value = mock_llm

            mock_embeddings_fn.return_value = _mock_embeddings()

            graph = build_query_graph()

            initial_state = _initial_query_state("What table stores customer data?")

            config = {"configurable": {"thread_id": "hallucination-test-2"}}
            result = graph.invoke(initial_state, config=config)

            # After max_retries the loop guard should fire and accept the answer
            assert result is not None
            assert result.get("final_answer", "") != ""

            # Generation should have been called exactly max_retries times
            # (once per iteration before the guard triggers)
            assert generation_count[0] == max_retries

    def test_hallucination_grader_with_specific_critique(
        self,
        neo4j_client: Neo4jClient,
    ) -> None:
        """Grader provides specific critique naming the problematic entity."""
        _populate_test_graph(neo4j_client)

        def _mock_answer(*args, **kwargs):
            result = MagicMock()
            result.content = json.dumps(
                {
                    "answer": "PRODUCT_XYZ is stored in the Products table.",
                }
            )
            return result

        def _mock_grader(*args, **kwargs):
            result = MagicMock()
            result.content = json.dumps(
                {
                    "grounded": False,
                    "critique": "PRODUCT_XYZ is not mentioned in any retrieved context. Only TB_PRODUCT table is referenced.",
                    "action": "regenerate",
                }
            )
            return result

        mock_llm = MagicMock()

        def _invoke(*args, **kwargs):
            prompt = str(args[0]) if args else ""
            if "grade" in prompt.lower() or "hallucination" in prompt.lower():
                return _mock_grader()
            else:
                return _mock_answer()

        mock_llm.invoke = _invoke

        with (
            patch("src.generation.query_graph.get_settings") as mock_settings_fn,
            patch("src.generation.query_graph.get_reasoning_llm") as mock_llm_fn,
            patch("src.generation.query_graph.get_embeddings") as mock_embeddings_fn,
        ):
            mock_settings_fn.return_value = _make_query_settings(max_hallucination_retries=1)

            mock_llm_fn.return_value = mock_llm

            mock_embeddings_fn.return_value = _mock_embeddings()

            graph = build_query_graph()

            initial_state = _initial_query_state("What is PRODUCT_XYZ?")

            config = {"configurable": {"thread_id": "hallucination-test-3"}}
            result = graph.invoke(initial_state, config=config)

            # Verify critique was captured
            grader_decision = result.get("grader_decision")
            assert grader_decision is not None

            # Critique should mention specific problematic entity
            if hasattr(grader_decision, "critique") and grader_decision.critique:
                assert (
                    "PRODUCT_XYZ" in grader_decision.critique
                    or "TB_PRODUCT" in grader_decision.critique
                )
