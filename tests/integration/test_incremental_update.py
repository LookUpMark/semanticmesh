"""Integration tests for incremental delta updates.

Tests: IT-08 (Incremental Delta Update)
"""

from __future__ import annotations

import json
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from src.graph.builder_graph import build_builder_graph
from src.graph.neo4j_client import Neo4jClient
from src.models.schemas import Chunk
from src.models.state import BuilderState

pytestmark = pytest.mark.integration


def _make_builder_settings() -> MagicMock:
    settings = MagicMock()
    settings.confidence_threshold = 0.90
    settings.max_reflection_attempts = 3
    settings.max_cypher_healing_attempts = 3
    settings.retrieval_vector_top_k = 10
    settings.few_shot_cypher_examples = 3
    settings.enable_schema_enrichment = True
    settings.enable_cypher_healing = True
    settings.enable_critic_validation = True
    return settings


def _make_builder_state(chunk: Chunk, ddl_path: str, source_doc: str) -> BuilderState:
    return {
        "chunks": [chunk],
        "ddl_paths": [ddl_path],
        "source_doc": source_doc,
        "triplets": [],
        "entities": [],
        "tables": [],
        "enriched_tables": [],
        "pending_tables": [],
        "completed_tables": [],
    }


# ─────────────────────────────────────────────────────────────────────────────
# IT-08: Incremental Delta Update
# ─────────────────────────────────────────────────────────────────────────────


@pytest.mark.integration
class TestIncrementalUpdate:
    """IT-08: Delta update adds new tables without duplicating existing ones."""

    def test_delta_update_adds_without_replacing(
        self,
        neo4j_client: Neo4jClient,
        get_graph_snapshot: Any,
    ) -> None:
        """After initial ingestion, adding a new table DDL must:
        - Add the new table node
        - Not delete or duplicate existing nodes
        """
        # Create a temporary DDL file for TABLE_A
        import os
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", suffix=".sql", delete=False) as f:
            table_a_ddl = f.name
            f.write("""
                CREATE TABLE TABLE_A (
                    ID INT PRIMARY KEY,
                    NAME VARCHAR(100)
                );
            """)

        with tempfile.NamedTemporaryFile(mode="w", suffix=".sql", delete=False) as f:
            table_b_ddl = f.name
            f.write("""
                CREATE TABLE TABLE_B (
                    ID INT PRIMARY KEY,
                    VALUE VARCHAR(100)
                );
            """)

        try:
            # Setup mock responses for TABLE_A
            chunk_a = Chunk(
                text="Table A stores ID and Name",
                chunk_index=0,
                metadata={"source": "test_a"},
            )

            responses_a = {
                "extraction": json.dumps(
                    {
                        "triplets": [
                            {
                                "subject": "TableA",
                                "predicate": "stores",
                                "object": "Data",
                                "provenance_text": "Table A stores data",
                                "confidence": 0.95,
                            }
                        ]
                    }
                ),
                "judge": json.dumps(
                    {"merge": True, "canonical_name": "TableA", "reasoning": "Same"}
                ),
                "enrichment": json.dumps(
                    {
                        "enriched_table_name": "Table A",
                        "enriched_columns": [{"original": "ID", "enriched": "Identifier"}],
                        "table_description": "First table",
                    }
                ),
                "mapping": json.dumps(
                    {
                        "table_name": "TABLE_A",
                        "mapped_concept": "TableA",
                        "confidence": 0.95,
                        "reasoning": "Direct mapping",
                        "alternative_concepts": [],
                    }
                ),
                "critic": json.dumps({"approved": True, "critique": None}),
                "cypher": """
MERGE (c:BusinessConcept {name: 'TableA'})
SET c.definition = 'A data storage table'
MERGE (t:PhysicalTable {table_name: 'TABLE_A'})
SET t.schema_name = 'dbo'
MERGE (c)-[r:MAPPED_TO]->(t)
SET r.mapping_confidence = 0.95
""",
            }

            mock_llm_a = self._create_mock_llm(responses_a)

            with (
                patch("src.graph.builder_graph.get_settings") as mock_settings_fn,
                patch("src.graph.builder_graph.get_extraction_llm") as mock_extraction_fn,
                patch("src.graph.builder_graph.get_reasoning_llm") as mock_reasoning_fn,
            ):
                mock_settings_fn.return_value = _make_builder_settings()
                mock_extraction_fn.return_value = mock_llm_a
                mock_reasoning_fn.return_value = mock_llm_a

                graph = build_builder_graph(production=False)

                # Initial run: TABLE_A only
                initial_state = _make_builder_state(chunk_a, table_a_ddl, "test_a")

                config = {"configurable": {"thread_id": "incremental-test"}}
                graph.invoke(initial_state, config=config)

                # Count nodes after initial run
                count_before = get_graph_snapshot(neo4j_client)

            # Setup mock responses for TABLE_B (delta update)
            chunk_b = Chunk(
                text="Table B stores ID and Value",
                chunk_index=0,
                metadata={"source": "test_b"},
            )

            responses_b = {
                "extraction": json.dumps(
                    {
                        "triplets": [
                            {
                                "subject": "TableB",
                                "predicate": "stores",
                                "object": "Value",
                                "provenance_text": "Table B stores value",
                                "confidence": 0.95,
                            }
                        ]
                    }
                ),
                "judge": json.dumps(
                    {"merge": True, "canonical_name": "TableB", "reasoning": "Same"}
                ),
                "enrichment": json.dumps(
                    {
                        "enriched_table_name": "Table B",
                        "enriched_columns": [{"original": "ID", "enriched": "Identifier"}],
                        "table_description": "Second table",
                    }
                ),
                "mapping": json.dumps(
                    {
                        "table_name": "TABLE_B",
                        "mapped_concept": "TableB",
                        "confidence": 0.95,
                        "reasoning": "Direct mapping",
                        "alternative_concepts": [],
                    }
                ),
                "critic": json.dumps({"approved": True, "critique": None}),
                "cypher": """
MERGE (c:BusinessConcept {name: 'TableB'})
SET c.definition = 'A value storage table'
MERGE (t:PhysicalTable {table_name: 'TABLE_B'})
SET t.schema_name = 'dbo'
MERGE (c)-[r:MAPPED_TO]->(t)
SET r.mapping_confidence = 0.95
""",
            }

            mock_llm_b = self._create_mock_llm(responses_b)

            with (
                patch("src.graph.builder_graph.get_settings") as mock_settings_fn,
                patch("src.graph.builder_graph.get_extraction_llm") as mock_extraction_fn,
                patch("src.graph.builder_graph.get_reasoning_llm") as mock_reasoning_fn,
            ):
                mock_settings_fn.return_value = _make_builder_settings()
                mock_extraction_fn.return_value = mock_llm_b
                mock_reasoning_fn.return_value = mock_llm_b

                graph = build_builder_graph(production=False)

                # Delta run: TABLE_B only
                delta_state = _make_builder_state(chunk_b, table_b_ddl, "test_b")

                config = {"configurable": {"thread_id": "incremental-test-2"}}
                graph.invoke(delta_state, config=config)

                # Count nodes after delta run
                count_after = get_graph_snapshot(neo4j_client)

            # Verify: new node added, original not deleted
            assert count_after["node_count"] > count_before["node_count"], (
                f"Expected more nodes after delta update: before={count_before['node_count']}, after={count_after['node_count']}"
            )

            # Verify TABLE_A still exists
            with neo4j_client:
                table_a_exists = neo4j_client.execute_cypher(
                    "MATCH (t:PhysicalTable {table_name: 'TABLE_A'}) RETURN count(t) AS cnt", {}
                )
                assert table_a_exists[0]["cnt"] > 0, "TABLE_A should still exist after delta update"

            # Verify TABLE_B was added
            with neo4j_client:
                table_b_exists = neo4j_client.execute_cypher(
                    "MATCH (t:PhysicalTable {table_name: 'TABLE_B'}) RETURN count(t) AS cnt", {}
                )
                assert table_b_exists[0]["cnt"] > 0, "TABLE_B should be added by delta update"

        finally:
            # Cleanup temp files
            if os.path.exists(table_a_ddl):
                os.unlink(table_a_ddl)
            if os.path.exists(table_b_ddl):
                os.unlink(table_b_ddl)

    def test_incremental_update_is_idempotent(
        self,
        neo4j_client: Neo4jClient,
    ) -> None:
        """Running the same delta update twice should not create duplicates."""
        import os
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", suffix=".sql", delete=False) as f:
            table_c_ddl = f.name
            f.write("""
                CREATE TABLE TABLE_C (
                    ID INT PRIMARY KEY,
                    DESCRIPTION VARCHAR(200)
                );
            """)

        try:
            chunk = Chunk(
                text="Table C stores descriptions",
                chunk_index=0,
                metadata={"source": "test_c"},
            )

            responses = {
                "extraction": json.dumps(
                    {
                        "triplets": [
                            {
                                "subject": "TableC",
                                "predicate": "stores",
                                "object": "Description",
                                "provenance_text": "Table C stores descriptions",
                                "confidence": 0.95,
                            }
                        ]
                    }
                ),
                "judge": json.dumps(
                    {"merge": True, "canonical_name": "TableC", "reasoning": "Same"}
                ),
                "enrichment": json.dumps(
                    {
                        "enriched_table_name": "Table C",
                        "enriched_columns": [{"original": "ID", "enriched": "Identifier"}],
                        "table_description": "Third table",
                    }
                ),
                "mapping": json.dumps(
                    {
                        "table_name": "TABLE_C",
                        "mapped_concept": "TableC",
                        "confidence": 0.95,
                        "reasoning": "Direct mapping",
                        "alternative_concepts": [],
                    }
                ),
                "critic": json.dumps({"approved": True, "critique": None}),
                "cypher": """
MERGE (c:BusinessConcept {name: 'TableC'})
SET c.definition = 'A description storage table'
MERGE (t:PhysicalTable {table_name: 'TABLE_C'})
SET t.schema_name = 'dbo'
MERGE (c)-[r:MAPPED_TO]->(t)
SET r.mapping_confidence = 0.95
""",
            }

            mock_llm = self._create_mock_llm(responses)

            with (
                patch("src.graph.builder_graph.get_settings") as mock_settings_fn,
                patch("src.graph.builder_graph.get_extraction_llm") as mock_extraction_fn,
                patch("src.graph.builder_graph.get_reasoning_llm") as mock_reasoning_fn,
            ):
                mock_settings_fn.return_value = _make_builder_settings()
                mock_extraction_fn.return_value = mock_llm
                mock_reasoning_fn.return_value = mock_llm

                graph = build_builder_graph(production=False)

                state = _make_builder_state(chunk, table_c_ddl, "test_c")

                # First run
                config = {"configurable": {"thread_id": "idempotent-test-1"}}
                graph.invoke(state, config=config)

                with neo4j_client:
                    count_1 = neo4j_client.execute_cypher(
                        "MATCH (t:PhysicalTable {table_name: 'TABLE_C'}) RETURN count(t) AS cnt", {}
                    )[0]["cnt"]

                # Second run (same input)
                config = {"configurable": {"thread_id": "idempotent-test-2"}}
                graph.invoke(state, config=config)

                with neo4j_client:
                    count_2 = neo4j_client.execute_cypher(
                        "MATCH (t:PhysicalTable {table_name: 'TABLE_C'}) RETURN count(t) AS cnt", {}
                    )[0]["cnt"]

                # Verify no duplicates (MERGE ensures idempotency)
                assert count_1 == count_2, (
                    f"Expected same count after duplicate run: first={count_1}, second={count_2}"
                )

        finally:
            if os.path.exists(table_c_ddl):
                os.unlink(table_c_ddl)

    # ─────────────────────────────────────────────────────────────────────────
    # Helper Methods
    # ─────────────────────────────────────────────────────────────────────────

    def _create_mock_llm(self, responses: dict[str, str]) -> MagicMock:
        """Create a mock LLM that returns predefined responses."""

        class _MockLLM:
            def __init__(self, response_map: dict[str, str]) -> None:
                self.response_map = response_map

            def invoke(self, *args, **kwargs) -> MagicMock:
                prompt = str(args[0]) if args else ""
                result = MagicMock()

                if "triplet" in prompt.lower() or "extract" in prompt.lower():
                    result.content = self.response_map.get("extraction", "{}")
                elif "mapping" in prompt.lower():
                    result.content = self.response_map.get("mapping", "{}")
                elif "critic" in prompt.lower() or "review" in prompt.lower():
                    result.content = self.response_map.get("critic", "{}")
                elif "enrich" in prompt.lower():
                    result.content = self.response_map.get("enrichment", "{}")
                elif "cypher" in prompt.lower():
                    result.content = self.response_map.get("cypher", "{}")
                elif "judge" in prompt.lower():
                    result.content = self.response_map.get("judge", "{}")
                else:
                    result.content = "{}"

                return result

        return _MockLLM(responses)
