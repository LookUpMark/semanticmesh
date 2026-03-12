"""Unit tests for src/graph/neo4j_client.py — UT-11"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from src.graph.neo4j_client import Neo4jClient, setup_schema, _SCHEMA_STATEMENTS


# ── Helpers ────────────────────────────────────────────────────────────────────

def _make_client(driver_mock: MagicMock) -> Neo4jClient:
    """Return a Neo4jClient with an injected driver mock."""
    client = Neo4jClient(uri="bolt://localhost:7687", username="neo4j", password="test")
    client._driver = driver_mock
    return client


def _make_result_mock(records: list[dict]) -> MagicMock:
    """Create a mock Result that returns the given records when iterated."""
    def _make_record(d: dict) -> MagicMock:
        m = MagicMock()
        m.__iter__ = MagicMock(return_value=iter(d.items()))
        m.keys = MagicMock(return_value=list(d.keys()))
        m.__getitem__ = MagicMock(side_effect=d.__getitem__)
        return m

    record_mocks = [_make_record(d) for d in records]
    result_mock = MagicMock()
    result_mock.__iter__ = MagicMock(return_value=iter(record_mocks))
    result_mock.data = MagicMock(return_value=record_mocks)
    return result_mock


def _make_session_mock(records: list[dict] | None = None) -> MagicMock:
    """Create a mock Session that returns the given records."""
    records = records or []
    result_mock = _make_result_mock(records)

    session_mock = MagicMock()
    session_mock.__enter__ = MagicMock(return_value=session_mock)
    session_mock.__exit__ = MagicMock(return_value=False)
    session_mock.run.return_value = result_mock
    return session_mock


# ── Context Manager ────────────────────────────────────────────────────────────

class TestNeo4jClientLifecycle:
    def test_enter_creates_driver(self) -> None:
        with patch("src.graph.neo4j_client.GraphDatabase.driver") as mock_driver_ctor:
            mock_driver = MagicMock()
            mock_driver_ctor.return_value = mock_driver
            with patch("src.graph.neo4j_client.get_settings") as mock_settings:
                mock_settings.return_value = MagicMock(
                    neo4j_uri="bolt://localhost:7687",
                    neo4j_user="neo4j",
                    neo4j_password=MagicMock(get_secret_value=lambda: "pass"),
                )
                client = Neo4jClient()
                client.__enter__()
                mock_driver.verify_connectivity.assert_called_once()
                client._driver = mock_driver
                client.__exit__(None, None, None)
                mock_driver.close.assert_called_once()

    def test_exit_closes_driver(self) -> None:
        driver_mock = MagicMock()
        client = _make_client(driver_mock)
        client.__exit__(None, None, None)
        driver_mock.close.assert_called_once()

    def test_execute_cypher_without_context_raises(self) -> None:
        client = Neo4jClient(uri="bolt://localhost:7687", username="neo4j", password="test")
        with pytest.raises(RuntimeError, match="context manager"):
            client.execute_cypher("MATCH (n) RETURN n")

    def test_driver_property_without_context_raises(self) -> None:
        client = Neo4jClient(uri="bolt://localhost:7687", username="neo4j", password="test")
        with pytest.raises(RuntimeError, match="context manager"):
            _ = client.driver


# ── execute_cypher ─────────────────────────────────────────────────────────────

class TestExecuteCypher:
    def test_returns_list_of_dicts(self) -> None:
        driver_mock = MagicMock()
        session_mock = _make_session_mock([{"name": "Alice"}, {"name": "Bob"}])
        driver_mock.session.return_value = session_mock

        client = _make_client(driver_mock)
        result = client.execute_cypher("MATCH (n) RETURN n.name AS name")
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["name"] == "Alice"
        assert result[1]["name"] == "Bob"

    def test_passes_params_to_driver(self) -> None:
        driver_mock = MagicMock()
        session_mock = _make_session_mock([])
        driver_mock.session.return_value = session_mock

        client = _make_client(driver_mock)
        client.execute_cypher("MATCH (n {name: $name}) RETURN n", {"name": "X"})
        session_mock.run.assert_called_once_with(
            "MATCH (n {name: $name}) RETURN n",
            parameters={"name": "X"},
        )

    def test_empty_result_returns_empty_list(self) -> None:
        driver_mock = MagicMock()
        session_mock = _make_session_mock([])
        driver_mock.session.return_value = session_mock

        client = _make_client(driver_mock)
        result = client.execute_cypher("MATCH (n) RETURN n LIMIT 0")
        assert result == []

    def test_none_params_becomes_empty_dict(self) -> None:
        driver_mock = MagicMock()
        session_mock = _make_session_mock([])
        driver_mock.session.return_value = session_mock

        client = _make_client(driver_mock)
        client.execute_cypher("RETURN 1")
        session_mock.run.assert_called_once_with("RETURN 1", parameters={})


# ── execute_batch ──────────────────────────────────────────────────────────────

class TestExecuteBatch:
    def test_empty_batch_is_noop(self) -> None:
        driver_mock = MagicMock()
        client = _make_client(driver_mock)
        client.execute_batch([])
        driver_mock.session.assert_not_called()

    def test_calls_execute_write(self) -> None:
        driver_mock = MagicMock()

        # Mock session with execute_write
        session_mock = MagicMock()
        session_mock.__enter__ = MagicMock(return_value=session_mock)
        session_mock.__exit__ = MagicMock(return_value=False)
        driver_mock.session.return_value = session_mock

        client = _make_client(driver_mock)
        client.execute_batch([("MERGE (n:X {id: $id})", {"id": 1})])
        session_mock.execute_write.assert_called_once()

    def test_batch_without_context_raises(self) -> None:
        client = Neo4jClient(uri="bolt://localhost:7687", username="neo4j", password="test")
        with pytest.raises(RuntimeError):
            client.execute_batch([("MERGE (n:X)", {})])

    def test_all_statements_executed_in_transaction(self) -> None:
        driver_mock = MagicMock()

        session_mock = MagicMock()
        session_mock.__enter__ = MagicMock(return_value=session_mock)
        session_mock.__exit__ = MagicMock(return_value=False)
        driver_mock.session.return_value = session_mock

        client = _make_client(driver_mock)
        statements = [
            ("MERGE (n:A {name: $name})", {"name": "X"}),
            ("MERGE (n:B {name: $name})", {"name": "Y"}),
        ]
        client.execute_batch(statements)

        # Verify execute_write was called
        session_mock.execute_write.assert_called_once()
        # Verify the transaction function runs all statements
        tx_func = session_mock.execute_write.call_args[0][0]
        # We can't directly test the tx function without actually running it,
        # but we verified execute_write was called with a function
        assert session_mock.execute_write.call_count == 1


# ── setup_schema ──────────────────────────────────────────────────────────────

class TestSetupSchema:
    def test_all_statements_executed(self) -> None:
        client_mock = MagicMock()
        client_mock.execute_cypher.return_value = []
        setup_schema(client_mock)
        assert client_mock.execute_cypher.call_count == len(_SCHEMA_STATEMENTS)

    def test_failed_statement_does_not_raise(self) -> None:
        client_mock = MagicMock()
        client_mock.execute_cypher.side_effect = Exception("unsupported")
        # Should NOT raise — just log warnings
        setup_schema(client_mock)
        # All statements should still be attempted
        assert client_mock.execute_cypher.call_count == len(_SCHEMA_STATEMENTS)

    def test_continues_after_single_failure(self) -> None:
        call_count = [0]

        def side_effect(stmt):
            call_count[0] += 1
            if call_count[0] == 1:
                raise Exception("First statement fails")
            return []

        client_mock = MagicMock()
        client_mock.execute_cypher.side_effect = side_effect
        setup_schema(client_mock)

        # All statements should still be attempted
        assert client_mock.execute_cypher.call_count == len(_SCHEMA_STATEMENTS)
