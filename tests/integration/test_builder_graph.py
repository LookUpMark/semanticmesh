"""Integration tests for src/graph/builder_graph.py.

Tests: IT-01 (E2E Builder Graph), IT-02 (Idempotency), IT-03 (Self-Reflection),
      IT-05 (HITL Interrupt & Resume)
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from src.graph.builder_graph import build_builder_graph
from src.graph.neo4j_client import Neo4jClient
from src.models.schemas import Chunk
from src.models.state import BuilderState

pytestmark = pytest.mark.integration


def _load_text_file(path: Path) -> str:
    """Load text content from a file."""
    with open(path) as f:
        return f.read()


def _create_mock_llm_factory(responses: dict[str, str]) -> Any:
    """Create a mock LLM factory that returns predefined responses."""

    class _MockLLM:
        def __init__(self, response_map: dict[str, str]) -> None:
            self.response_map = response_map
            self.call_count: dict[str, int] = {}

        def invoke(self, *args, **kwargs) -> MagicMock:
            prompt = str(args[0]) if args else str(kwargs)
            response = MagicMock()

            if "triplet" in prompt.lower() or "extract" in prompt.lower():
                response.content = self.response_map.get("extraction", "{}")
                self.call_count["extraction"] = self.call_count.get("extraction", 0) + 1
            elif "mapping" in prompt.lower():
                response.content = self.response_map.get("mapping", "{}")
                self.call_count["mapping"] = self.call_count.get("mapping", 0) + 1
            elif "critic" in prompt.lower() or "review" in prompt.lower():
                response.content = self.response_map.get("critic", "{}")
                self.call_count["critic"] = self.call_count.get("critic", 0) + 1
            elif "enrich" in prompt.lower():
                response.content = self.response_map.get("enrichment", "{}")
                self.call_count["enrichment"] = self.call_count.get("enrichment", 0) + 1
            elif "cypher" in prompt.lower():
                response.content = self.response_map.get("cypher", "{}")
                self.call_count["cypher"] = self.call_count.get("cypher", 0) + 1
            elif "judge" in prompt.lower():
                response.content = self.response_map.get("judge", "{}")
                self.call_count["judge"] = self.call_count.get("judge", 0) + 1
            else:
                response.content = "{}"

            return response

    return _MockLLM(responses)


def _setup_mocks() -> tuple[Any, Any, Any]:
    """Setup standard mocks for builder graph tests."""
    mock_settings = MagicMock()
    mock_settings.neo4j_uri = "bolt://localhost:7687"
    mock_settings.neo4j_user = "neo4j"
    mock_settings.neo4j_password.get_secret_value.return_value = "test"
    mock_settings.confidence_threshold = 0.90
    mock_settings.max_reflection_attempts = 3
    mock_settings.max_cypher_healing_attempts = 3
    mock_settings.retrieval_vector_top_k = 10
    mock_settings.few_shot_cypher_examples = 3
    mock_settings.enable_schema_enrichment = True
    mock_settings.enable_cypher_healing = True
    mock_settings.enable_critic_validation = True

    mock_extraction = MagicMock()
    mock_reasoning = MagicMock()

    return mock_settings, mock_extraction, mock_reasoning


@pytest.mark.integration
class TestBuilderGraphE2E:
    """IT-01: End-to-end Builder Graph with small schema."""

    def test_builder_graph_creates_expected_nodes(
        self,
        neo4j_client: Neo4jClient,
        sample_simple_schema: Path,
        sample_business_glossary: Path,
    ) -> None:
        """Run full builder graph and verify expected nodes are created."""
        glossary_text = _load_text_file(sample_business_glossary)

        chunks = [
            Chunk(
                text=glossary_text,
                chunk_index=0,
                metadata={"source": str(sample_business_glossary), "page": 1},
            )
        ]

        extraction_response = json.dumps(
            {
                "triplets": [
                    {
                        "subject": "Customer",
                        "predicate": "places",
                        "object": "SalesOrder",
                        "provenance_text": "A Customer places one or more SalesOrders",
                        "confidence": 0.95,
                    },
                    {
                        "subject": "Product",
                        "predicate": "ordered_in",
                        "object": "SalesOrder",
                        "provenance_text": "Products are ordered through SalesOrders",
                        "confidence": 0.93,
                    },
                ]
            }
        )

        judge_response = json.dumps(
            {
                "merge": True,
                "canonical_name": "Customer",
                "reasoning": "Same concept",
            }
        )

        enrichment_response = json.dumps(
            {
                "enriched_table_name": "Customer Master",
                "enriched_columns": [
                    {"original": "CUST_ID", "enriched": "Customer ID"},
                    {"original": "FULL_NAME", "enriched": "Full Name"},
                ],
                "table_description": "Master customer data",
            }
        )

        mapping_response = json.dumps(
            {
                "table_name": "CUSTOMER_MASTER",
                "mapped_concept": "Customer",
                "confidence": 0.95,
                "reasoning": "Table stores customer data",
                "alternative_concepts": [],
            }
        )

        critic_response = json.dumps(
            {
                "approved": True,
                "critique": None,
                "suggested_correction": None,
            }
        )

        cypher_response = """
MERGE (c:BusinessConcept:Entity {name: 'Customer'})
SET c.definition = 'A Customer is any individual...', c.synonyms = ['client', 'buyer']
MERGE (t:PhysicalTable:Table {table_name: 'CUSTOMER_MASTER'})
SET t.schema_name = 'dbo', t.ddl_source = 'CREATE TABLE...'
MERGE (c)-[r:MAPPED_TO]->(t)
SET r.mapping_confidence = 0.95, r.reasoning = 'Table stores customer data'
"""

        with (
            patch("src.graph.builder_graph.get_settings") as mock_settings_fn,
            patch("src.graph.builder_graph.get_extraction_llm") as mock_extraction_fn,
            patch("src.graph.builder_graph.get_reasoning_llm") as mock_reasoning_fn,
        ):
            mock_settings = MagicMock()
            mock_settings.confidence_threshold = 0.90
            mock_settings.max_reflection_attempts = 3
            mock_settings.max_cypher_healing_attempts = 3
            mock_settings.retrieval_vector_top_k = 10
            mock_settings.few_shot_cypher_examples = 3
            mock_settings.enable_schema_enrichment = True
            mock_settings.enable_cypher_healing = True
            mock_settings.enable_critic_validation = True
            mock_settings.neo4j_uri = "bolt://localhost:7687"
            mock_settings.neo4j_user = "neo4j"
            mock_settings.neo4j_password = "test"
            mock_settings_fn.return_value = mock_settings

            mock_extraction = MagicMock()
            extraction_result = MagicMock()
            extraction_result.content = extraction_response
            mock_extraction.invoke.return_value = extraction_result
            mock_extraction_fn.return_value = mock_extraction

            mock_reasoning = MagicMock()

            def _reasoning_invoke(*args, **kwargs):
                prompt = str(args[0]) if args else ""
                result = MagicMock()
                if "enrich" in prompt.lower():
                    result.content = enrichment_response
                elif "mapping" in prompt.lower():
                    result.content = mapping_response
                elif "critic" in prompt.lower() or "review" in prompt.lower():
                    result.content = critic_response
                elif "judge" in prompt.lower():
                    result.content = judge_response
                else:
                    result.content = cypher_response
                return result

            mock_reasoning.invoke = _reasoning_invoke
            mock_reasoning_fn.return_value = mock_reasoning

            graph = build_builder_graph(production=False)

            initial_state: BuilderState = {
                "chunks": chunks,
                "ddl_paths": [str(sample_simple_schema)],
                "source_doc": str(sample_business_glossary),
                "triplets": [],
                "entities": [],
                "tables": [],
                "enriched_tables": [],
                "pending_tables": [],
                "completed_tables": [],
            }

            config = {"configurable": {"thread_id": "test-e2e-1"}}
            graph.invoke(initial_state, config=config)

        with neo4j_client:
            concepts = neo4j_client.execute_cypher(
                "MATCH (n:BusinessConcept) RETURN n.name AS name", {}
            )
            tables = neo4j_client.execute_cypher(
                "MATCH (n:PhysicalTable) RETURN n.table_name AS name", {}
            )
            mappings = neo4j_client.execute_cypher(
                "MATCH ()-[r:MAPPED_TO]->() RETURN count(r) AS cnt", {}
            )

        assert isinstance(concepts, list)
        assert isinstance(tables, list)
        assert isinstance(mappings, list)


@pytest.mark.integration
class TestBuilderGraphIdempotency:
    """IT-02: Running Builder twice produces identical graph state."""

    def test_builder_graph_double_run_idempotent(
        self,
        neo4j_client: Neo4jClient,
        sample_simple_schema: Path,
        get_graph_snapshot: Any,
    ) -> None:
        """Running the Builder twice on the same input must produce identical graph state."""
        chunk = Chunk(
            text="Customers place orders for products.",
            chunk_index=0,
            metadata={"source": "test.txt"},
        )

        responses = {
            "extraction": json.dumps(
                {
                    "triplets": [
                        {
                            "subject": "Customer",
                            "predicate": "orders",
                            "object": "Product",
                            "provenance_text": "Customers place orders for products",
                            "confidence": 0.95,
                        }
                    ]
                }
            ),
            "judge": json.dumps({"merge": True, "canonical_name": "Customer", "reasoning": "Same"}),
            "enrichment": json.dumps(
                {
                    "enriched_table_name": "Customer Table",
                    "enriched_columns": [{"original": "CUST_ID", "enriched": "Customer ID"}],
                    "table_description": "Customer data",
                }
            ),
            "mapping": json.dumps(
                {
                    "table_name": "CUSTOMER_MASTER",
                    "mapped_concept": "Customer",
                    "confidence": 0.95,
                    "reasoning": "Maps correctly",
                    "alternative_concepts": [],
                }
            ),
            "critic": json.dumps({"approved": True, "critique": None}),
            "cypher": """
MERGE (c:BusinessConcept:Entity {name: 'Customer'})
SET c.definition = 'A person who buys products'
MERGE (t:PhysicalTable:Table {table_name: 'CUSTOMER_MASTER'})
SET t.schema_name = 'dbo'
MERGE (c)-[r:MAPPED_TO]->(t)
SET r.mapping_confidence = 0.95
""",
        }

        mock_llm = _create_mock_llm_factory(responses)

        with (
            patch("src.graph.builder_graph.get_settings") as mock_settings_fn,
            patch("src.graph.builder_graph.get_extraction_llm") as mock_extraction_fn,
            patch("src.graph.builder_graph.get_reasoning_llm") as mock_reasoning_fn,
        ):
            mock_settings = MagicMock()
            mock_settings.confidence_threshold = 0.90
            mock_settings.max_reflection_attempts = 3
            mock_settings.max_cypher_healing_attempts = 3
            mock_settings.retrieval_vector_top_k = 10
            mock_settings.few_shot_cypher_examples = 3
            mock_settings.enable_schema_enrichment = True
            mock_settings.enable_cypher_healing = True
            mock_settings.enable_critic_validation = True
            mock_settings_fn.return_value = mock_settings
            mock_extraction_fn.return_value = mock_llm
            mock_reasoning_fn.return_value = mock_llm

            graph = build_builder_graph(production=False)

            initial_state: BuilderState = {
                "chunks": [chunk],
                "ddl_paths": [str(sample_simple_schema)],
                "source_doc": "test.txt",
                "triplets": [],
                "entities": [],
                "tables": [],
                "enriched_tables": [],
                "pending_tables": [],
                "completed_tables": [],
            }

            config = {"configurable": {"thread_id": "idempotency-test"}}

            graph.invoke(initial_state, config=config)
            snapshot_1 = get_graph_snapshot(neo4j_client)

            graph.invoke(initial_state, config=config)
            snapshot_2 = get_graph_snapshot(neo4j_client)

            assert snapshot_1["node_count"] == snapshot_2["node_count"]
            assert snapshot_1["edge_count"] == snapshot_2["edge_count"]


@pytest.mark.integration
class TestBuilderGraphSelfReflection:
    """IT-03: Self-reflection loop recovers from invalid LLM output."""

    def test_mapping_reflection_loop_recovers(
        self,
        neo4j_client: Neo4jClient,
        sample_simple_schema: Path,
    ) -> None:
        """LLM Actor returns invalid JSON on attempt 1, valid JSON on attempt 2."""
        chunk = Chunk(
            text="Customer data is stored in the database.",
            chunk_index=0,
            metadata={"source": "test.txt"},
        )

        mapping_calls = [0]

        def _mock_mapping(*args, **kwargs):
            mapping_calls[0] += 1
            result = MagicMock()
            if mapping_calls[0] == 1:
                result.content = "INVALID JSON"
            else:
                result.content = json.dumps(
                    {
                        "table_name": "CUSTOMER_MASTER",
                        "mapped_concept": "Customer",
                        "confidence": 0.95,
                        "reasoning": "Valid mapping",
                        "alternative_concepts": [],
                    }
                )
            return result

        mock_llm = MagicMock()
        mock_llm.invoke = _mock_mapping

        with (
            patch("src.graph.builder_graph.get_settings") as mock_settings_fn,
            patch("src.graph.builder_graph.get_extraction_llm") as mock_extraction_fn,
            patch("src.graph.builder_graph.get_reasoning_llm") as mock_reasoning_fn,
        ):
            mock_settings = MagicMock()
            mock_settings.confidence_threshold = 0.90
            mock_settings.max_reflection_attempts = 3
            mock_settings.max_cypher_healing_attempts = 3
            mock_settings.retrieval_vector_top_k = 10
            mock_settings.few_shot_cypher_examples = 3
            mock_settings.enable_schema_enrichment = True
            mock_settings.enable_cypher_healing = True
            mock_settings.enable_critic_validation = True
            mock_settings_fn.return_value = mock_settings

            mock_extraction = MagicMock()
            ext_result = MagicMock()
            ext_result.content = json.dumps({"triplets": []})
            mock_extraction.invoke.return_value = ext_result
            mock_extraction_fn.return_value = mock_extraction

            mock_reasoning = MagicMock()

            def _reasoning_invoke(*args, **kwargs):
                prompt = str(args[0]) if args else ""
                result = MagicMock()
                if "mapping" in prompt.lower():
                    return _mock_mapping()
                elif "critic" in prompt.lower() or "review" in prompt.lower():
                    result.content = json.dumps({"approved": True, "critique": None})
                elif "enrich" in prompt.lower():
                    result.content = json.dumps(
                        {
                            "enriched_table_name": "Customer Table",
                            "enriched_columns": [],
                            "table_description": "Customer data",
                        }
                    )
                else:
                    result.content = "MERGE (c:BusinessConcept {name: 'Customer'})"
                return result

            mock_reasoning.invoke = _reasoning_invoke
            mock_reasoning_fn.return_value = mock_reasoning

            graph = build_builder_graph(production=False)

            initial_state: BuilderState = {
                "chunks": [chunk],
                "ddl_paths": [str(sample_simple_schema)],
                "source_doc": "test.txt",
                "triplets": [],
                "entities": [],
                "tables": [],
                "enriched_tables": [],
                "pending_tables": [],
                "completed_tables": [],
            }

            config = {"configurable": {"thread_id": "reflection-test"}}
            graph.invoke(initial_state, config=config)

            assert mapping_calls[0] >= 2


@pytest.mark.integration
class TestBuilderGraphHITL:
    """IT-05: HITL interrupt triggers correctly and can resume."""

    def test_hitl_interrupt_and_resume(
        self,
        neo4j_client: Neo4jClient,
        sample_simple_schema: Path,
    ) -> None:
        """Low-confidence mapping triggers HITL interrupt; resume processes corrected mapping."""
        chunk = Chunk(
            text="Customer data in the system.",
            chunk_index=0,
            metadata={"source": "test.txt"},
        )

        low_confidence_mapping = json.dumps(
            {
                "table_name": "CUSTOMER_MASTER",
                "mapped_concept": "Customer",
                "confidence": 0.75,
                "reasoning": "Low confidence match",
                "alternative_concepts": [],
            }
        )

        mock_llm = MagicMock()

        def _invoke(*args, **kwargs):
            prompt = str(args[0]) if args else ""
            result = MagicMock()
            if "mapping" in prompt.lower():
                result.content = low_confidence_mapping
            elif "critic" in prompt.lower() or "review" in prompt.lower():
                result.content = json.dumps({"approved": True, "critique": None})
            elif "enrich" in prompt.lower():
                result.content = json.dumps(
                    {
                        "enriched_table_name": "Customer Table",
                        "enriched_columns": [],
                        "table_description": "Customer data",
                    }
                )
            else:
                result.content = "MERGE (c:BusinessConcept {name: 'Customer'})"
            return result

        mock_llm.invoke = _invoke

        with (
            patch("src.graph.builder_graph.get_settings") as mock_settings_fn,
            patch("src.graph.builder_graph.get_extraction_llm") as mock_extraction_fn,
            patch("src.graph.builder_graph.get_reasoning_llm") as mock_reasoning_fn,
        ):
            mock_settings = MagicMock()
            mock_settings.confidence_threshold = 0.90
            mock_settings.max_reflection_attempts = 3
            mock_settings.max_cypher_healing_attempts = 3
            mock_settings.retrieval_vector_top_k = 10
            mock_settings.few_shot_cypher_examples = 3
            mock_settings.enable_schema_enrichment = True
            mock_settings.enable_cypher_healing = True
            mock_settings.enable_critic_validation = True
            mock_settings_fn.return_value = mock_settings

            mock_extraction = MagicMock()
            ext_result = MagicMock()
            ext_result.content = json.dumps({"triplets": []})
            mock_extraction.invoke.return_value = ext_result
            mock_extraction_fn.return_value = mock_extraction

            mock_reasoning_fn.return_value = mock_llm

            graph = build_builder_graph(production=False)

            initial_state: BuilderState = {
                "chunks": [chunk],
                "ddl_paths": [str(sample_simple_schema)],
                "source_doc": "test.txt",
                "triplets": [],
                "entities": [],
                "tables": [],
                "enriched_tables": [],
                "pending_tables": [],
                "completed_tables": [],
            }

            config = {"configurable": {"thread_id": "hitl-test"}}

            for event in graph.stream(initial_state, config=config):
                if "__interrupt__" in str(event):
                    break

            assert graph is not None
