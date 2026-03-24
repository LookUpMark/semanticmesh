"""Shared test fixtures: mock LLM, Neo4j container, settings override, sample data.

All fixtures available to unit, integration, and evaluation tests.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest
from testcontainers.neo4j import Neo4jContainer

from src.config.settings import Settings
from src.graph.neo4j_client import Neo4jClient


@pytest.fixture(scope="session")
def test_settings() -> Settings:
    """Override settings with test values — never reads from .env.

    This fixture provides safe test values that won't interfere with
    development or production configurations.
    """
    return Settings(
        neo4j_uri="bolt://localhost:7688",  # test port (different from dev 7687)
        neo4j_user="neo4j",
        neo4j_password="test_password_12345",
        openrouter_api_key="sk-or-test-key-for-testing",
        llm_model_reasoning="test-reasoning-model",
        llm_model_extraction="test-extraction-model",
        llm_model_generation="test-generation-model",
        embedding_model="test-embedding-model",
        reranker_model="test-reranker-model",
        chunk_size=512,
        chunk_overlap=64,
        er_blocking_top_k=5,
        er_similarity_threshold=0.85,
        confidence_threshold=0.90,
        max_reflection_attempts=3,
        max_cypher_healing_attempts=3,
        max_hallucination_retries=3,
        few_shot_cypher_examples=3,
        retrieval_vector_top_k=10,
        retrieval_bm25_top_k=10,
        retrieval_graph_depth=2,
        reranker_top_k=5,
        enable_schema_enrichment=True,
        enable_cypher_healing=True,
        enable_critic_validation=True,
        enable_reranker=True,
        enable_hallucination_grader=True,
        retrieval_mode="hybrid",
    )


@pytest.fixture(scope="session")
def neo4j_container(test_settings: Settings):
    """Spin up a real Neo4j Docker container for integration tests.

    This fixture uses testcontainers to spin up a Neo4j instance
    that is isolated from development/production databases.

    The container is started once per test session and shared across
    all integration tests for performance.
    """
    with Neo4jContainer(
        image="neo4j:5.18",
        username=test_settings.neo4j_user,
        password=test_settings.neo4j_password,
    ) as container:
        yield container


@pytest.fixture
def neo4j_client(neo4j_container: Neo4jContainer) -> Neo4jClient:
    """Provide a Neo4jClient connected to the test container.

    The client is created fresh for each test and automatically
    cleans up the database between tests.
    """
    uri = neo4j_container.get_connection_url()
    user = neo4j_container.username
    password = neo4j_container.password

    client = Neo4jClient(uri=uri, username=user, password=password)

    with client:
        client.execute_cypher("MATCH (n) DETACH DELETE n")

    yield client


def _load_mock_response(name: str) -> dict[str, Any]:
    """Load a mock LLM response from the fixtures directory."""
    path = Path(__file__).parent / "fixtures" / "00_legacy" / "mock_responses" / f"{name}.json"
    with open(path) as f:
        return json.load(f)


@pytest.fixture
def mock_llm():
    """Mock LLM that returns fixed JSON responses.

    By default, returns an empty response. Use .side_effect or .return_value
    to customize for specific tests.
    """
    llm = MagicMock()
    response = MagicMock()
    response.content = "{}"
    llm.invoke.return_value = response
    return llm


@pytest.fixture
def mock_llm_sequence():
    """Factory for creating a mock LLM that returns a sequence of responses.

    Example:
        responses = [
            '{"triplets": [...]}',  # First call
            '{"merge": true, ...}',  # Second call
        ]
        llm = mock_llm_sequence(responses)
    """

    def _create(responses: list[str]) -> MagicMock:
        llm = MagicMock()
        call_count = [0]

        def _invoke(*args, **kwargs):
            response = MagicMock()
            if call_count[0] < len(responses):
                response.content = responses[call_count[0]]
                call_count[0] += 1
            else:
                response.content = responses[-1]
            return response

        llm.invoke = _invoke
        return llm

    return _create


@pytest.fixture
def mock_extraction_response():
    """Mock LLM response for triplet extraction."""
    return _load_mock_response("extraction_response")


@pytest.fixture
def mock_mapping_response():
    """Mock LLM response for schema mapping."""
    return _load_mock_response("mapping_high_confidence")


@pytest.fixture
def mock_critic_approved():
    """Mock LLM response for critic approval."""
    return _load_mock_response("critic_approved")


@pytest.fixture
def mock_critic_rejected():
    """Mock LLM response for critic rejection."""
    return _load_mock_response("critic_rejected")


@pytest.fixture
def mock_grader_faithful():
    """Mock LLM response for faithful grader."""
    return _load_mock_response("grader_faithful")


@pytest.fixture
def mock_grader_hallucinated():
    """Mock LLM response for hallucinated grader."""
    return _load_mock_response("grader_hallucinated")


@pytest.fixture
def mock_embeddings():
    """Mock embeddings that return fixed 1024-dim vectors.

    Uses BGE-M3 dimensionality (1024). Returns deterministic vectors
    for testing purposes.
    """
    embedder = MagicMock()

    def _embed_documents(texts: list[str]) -> list[list[float]]:
        vectors = []
        for i in range(len(texts)):
            base = [0.1] * 1024
            base[0] = (i % 10) / 10.0
            vectors.append(base)
        return vectors

    embedder.embed_documents = _embed_documents

    def _embed_query(text: str) -> list[float]:
        return [0.5] * 1024

    embedder.embed_query = _embed_query

    return embedder


@pytest.fixture
def sample_simple_schema() -> Path:
    """Path to the simple schema DDL file."""
    return Path(__file__).parent / "fixtures" / "00_legacy" / "sample_ddl" / "simple_schema.sql"


@pytest.fixture
def sample_complex_schema() -> Path:
    """Path to the complex schema DDL file."""
    return Path(__file__).parent / "fixtures" / "00_legacy" / "sample_ddl" / "complex_schema.sql"


@pytest.fixture
def sample_business_glossary() -> Path:
    """Path to the business glossary text file."""
    return Path(__file__).parent / "fixtures" / "00_legacy" / "sample_docs" / "business_glossary.txt"


@pytest.fixture
def sample_data_dictionary() -> Path:
    """Path to the data dictionary text file."""
    return Path(__file__).parent / "fixtures" / "00_legacy" / "sample_docs" / "data_dictionary.txt"


@pytest.fixture
def get_graph_snapshot():
    """Factory function to capture Neo4j graph state for idempotency tests.

    Example:
        snapshot1 = get_graph_snapshot(neo4j_client)
        # ... run some operation ...
        snapshot2 = get_graph_snapshot(neo4j_client)
        assert snapshot1 == snapshot2
    """

    def _snapshot(client: Neo4jClient) -> dict[str, Any]:
        with client:
            result = client.execute_cypher("""
                MATCH (n)
                WITH count(DISTINCT n) as node_count
                MATCH ()-[r]->()
                WITH node_count, count(DISTINCT r) as edge_count
                MATCH (c:BusinessConcept)
                WITH node_count, edge_count, collect(c.name) as concepts
                MATCH (t:PhysicalTable)
                RETURN node_count, edge_count, concepts, collect(t.table_name) as tables
            """)
            if result:
                return {
                    "node_count": result[0].get("node_count", 0),
                    "edge_count": result[0].get("edge_count", 0),
                    "concepts": set(result[0].get("concepts", [])),
                    "tables": set(result[0].get("tables", [])),
                }
        return {"node_count": 0, "edge_count": 0, "concepts": set(), "tables": set()}

    return _snapshot
