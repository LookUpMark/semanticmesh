# Part 6 — `src/graph/neo4j_client.py`

## 1. Purpose & Context

**Epic:** EP-09 Property-Graph Persistence  
**US-10-01** — Neo4j Python Driver Wrapper, **US-10-02** — Index and Constraint Setup

`Neo4jClient` wraps the official `neo4j` Python driver with:

- Context-manager lifecycle (`__enter__` / `__exit__`) so connections close properly.
- `execute_cypher` for single-statement reads/writes with parameter support.
- `execute_batch` for write-heavy bulk inserts via an explicit transaction.
- `setup_schema` for idempotent schema initialisation (constraints + vector index).

All Cypher statements executed by the ingestion pipeline flow through this client.

---

## 2. Prerequisites

- `neo4j` Python package (official driver ≥ 5.x).
- `src/config/settings.py` — `get_settings()` with `neo4j_uri`, `neo4j_username`, `neo4j_password` (step 2).
- `src/config/logging.py` — `get_logger` (step 3).

---

## 3. Public API

| Symbol | Signature | Description |
|---|---|---|
| `Neo4jClient` | class | Context-manager wrapper around GraphDatabase.driver |
| `.execute_cypher` | `(cypher: str, params: dict | None) -> list[dict]` | Run one statement, return records as dicts |
| `.execute_batch` | `(statements: list[tuple[str, dict]]) -> None` | Execute many statements in one explicit transaction |
| `.driver` | `@property -> neo4j.Driver` | Exposes the underlying driver for modules that need it (e.g., `cypher_healer`) |
| `setup_schema` | `(client: Neo4jClient) -> None` | Idempotent CREATE CONSTRAINT + CREATE VECTOR INDEX |

---

## 4. Full Implementation

```python
"""Neo4j driver wrapper — EP-09 / US-10-01 and US-10-02.

Provides a thin context-manager around the official neo4j Python driver,
plus idempotent schema setup (constraints and vector index for BGE-M3).
"""

from __future__ import annotations

import logging
from types import TracebackType
from typing import Any

from neo4j import GraphDatabase, ManagedTransaction, Result, Session

from src.config.logging import get_logger
from src.config.settings import get_settings

logger: logging.Logger = get_logger(__name__)

# ── Vector index dimensions for BGE-M3 ────────────────────────────────────────
_EMBEDDING_DIMENSION: int = 1024

# ── Schema DDL run once at startup ────────────────────────────────────────────
_SCHEMA_STATEMENTS: list[str] = [
    # Uniqueness constraint on BusinessConcept name
    "CREATE CONSTRAINT businessconcept_name_unique IF NOT EXISTS "
    "FOR (n:BusinessConcept) REQUIRE n.name IS UNIQUE",

    # Uniqueness constraint on DataTable qualified name
    "CREATE CONSTRAINT datatable_qualified_unique IF NOT EXISTS "
    "FOR (n:DataTable) REQUIRE n.qualified_name IS UNIQUE",

    # Index for fast Chunk look-up by source document
    "CREATE INDEX chunk_source_doc IF NOT EXISTS "
    "FOR (c:Chunk) ON (c.source_doc)",

    # Vector index for BGE-M3 embeddings on BusinessConcept nodes
    (
        "CREATE VECTOR INDEX businessconcept_embedding IF NOT EXISTS "
        "FOR (n:BusinessConcept) ON n.embedding "
        "OPTIONS {indexConfig: {"
        "'vector.dimensions': %d, "
        "'vector.similarity_function': 'cosine'"
        "}}"
    ) % _EMBEDDING_DIMENSION,
]


class Neo4jClient:
    """Thread-safe, context-managed Neo4j driver wrapper.

    Usage::

        with Neo4jClient() as client:
            records = client.execute_cypher("MATCH (n) RETURN n.name LIMIT 5")
            client.execute_batch([
                ("MERGE (n:BusinessConcept {name: $name})", {"name": "Customer"}),
            ])

    The driver is created lazily on ``__enter__`` and closed on ``__exit__``.
    """

    def __init__(
        self,
        uri: str | None = None,
        username: str | None = None,
        password: str | None = None,
    ) -> None:
        settings = get_settings()
        self._uri: str = uri or settings.neo4j_uri
        self._username: str = username or settings.neo4j_username
        self._password: str = (
            password
            or (settings.neo4j_password.get_secret_value() if settings.neo4j_password else "")
        )
        self._driver = None

    # ── Lifecycle ──────────────────────────────────────────────────────────────

    def __enter__(self) -> "Neo4jClient":
        self._driver = GraphDatabase.driver(
            self._uri,
            auth=(self._username, self._password),
        )
        self._driver.verify_connectivity()
        logger.debug("Neo4j driver connected to %s.", self._uri)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self._driver is not None:
            self._driver.close()
            logger.debug("Neo4j driver closed.")

    # ── Driver Property ────────────────────────────────────────────────────────

    @property
    def driver(self) -> "neo4j.Driver":
        """Expose the underlying neo4j.Driver for callers that need raw access.

        Used by ``cypher_healer.test_cypher`` which requires the driver directly
        to run ``EXPLAIN`` statements outside the standard execute_cypher path.

        Raises:
            RuntimeError: If accessed before the context manager is entered.
        """
        if self._driver is None:
            raise RuntimeError("Neo4jClient must be used as a context manager.")
        return self._driver

    # ── Single Statement ───────────────────────────────────────────────────────

    def execute_cypher(
        self,
        cypher: str,
        params: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Execute a single Cypher statement and return all records as dicts.

        Args:
            cypher: A Cypher query string, optionally parameterised with ``$name`` placeholders.
            params: Optional parameter dict matching the ``$name`` placeholders.

        Returns:
            A list of ``{key: value}`` dicts, one per result record.
            Empty list for write statements that return nothing.

        Raises:
            RuntimeError: If the driver has not been initialised (not used as context manager).
        """
        if self._driver is None:
            raise RuntimeError("Neo4jClient must be used as a context manager.")
        params = params or {}

        with self._driver.session() as session:
            result: Result = session.run(cypher, parameters=params)
            records: list[dict[str, Any]] = [dict(r) for r in result]
            logger.debug("execute_cypher: %d record(s) returned.", len(records))
            return records

    # ── Batch Write ────────────────────────────────────────────────────────────

    def execute_batch(
        self,
        statements: list[tuple[str, dict[str, Any]]],
    ) -> None:
        """Execute multiple Cypher write statements in a single explicit transaction.

        All statements succeed or the entire transaction is rolled back.

        Args:
            statements: A list of ``(cypher_string, params_dict)`` tuples.
        """
        if self._driver is None:
            raise RuntimeError("Neo4jClient must be used as a context manager.")
        if not statements:
            return

        def _run_tx(tx: ManagedTransaction) -> None:
            for cypher, params in statements:
                tx.run(cypher, parameters=params)

        with self._driver.session() as session:
            session.execute_write(_run_tx)
            logger.debug("execute_batch: %d statement(s) committed.", len(statements))


# ── Schema Initialisation ─────────────────────────────────────────────────────

def setup_schema(client: Neo4jClient) -> None:
    """Create constraints and vector index if they do not already exist.

    Idempotent — safe to call multiple times. Must be called once on startup
    before any ingestion writes.

    Args:
        client: An active ``Neo4jClient`` context.
    """
    logger.info("Running schema setup (%d statements)...", len(_SCHEMA_STATEMENTS))
    for stmt in _SCHEMA_STATEMENTS:
        try:
            client.execute_cypher(stmt)
            logger.debug("Schema OK: %.60s...", stmt)
        except Exception as exc:
            # Some older community editions don't support VECTOR INDEX; log and continue.
            logger.warning("Schema statement failed (skipping): %s", exc)
    logger.info("Schema setup complete.")
```

---

## 5. Tests

```python
"""Unit tests for src/graph/neo4j_client.py — UT-15"""

from __future__ import annotations

from unittest.mock import MagicMock, call, patch

import pytest

from src.graph.neo4j_client import Neo4jClient, setup_schema


# ── Helpers ────────────────────────────────────────────────────────────────────

def _make_client(driver_mock: MagicMock) -> Neo4jClient:
    """Return a Neo4jClient with an injected driver mock."""
    client = Neo4jClient(uri="bolt://localhost:7687", username="neo4j", password="test")
    client._driver = driver_mock
    return client


def _make_session_mock(records: list[dict]) -> MagicMock:
    record_mocks = [MagicMock(**{"__iter__": lambda s: iter(d.items()), "keys": lambda: d.keys(), **{k: v for k, v in d.items()}}) for d in records]
    result_mock = MagicMock()
    result_mock.__iter__ = MagicMock(return_value=iter(record_mocks))

    # Make dict(r) work for each record by returning itself as __iter__
    def _make_record(d: dict) -> MagicMock:
        m = MagicMock()
        m.__iter__ = MagicMock(return_value=iter(d.items()))
        m.keys = MagicMock(return_value=list(d.keys()))
        m.__getitem__ = MagicMock(side_effect=d.__getitem__)
        return m

    real_records = [_make_record(d) for d in records]
    result_mock.__iter__ = MagicMock(return_value=iter(real_records))

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
                    neo4j_username="neo4j",
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


# ── execute_cypher ─────────────────────────────────────────────────────────────

class TestExecuteCypher:
    def test_returns_list_of_dicts(self) -> None:
        driver_mock = MagicMock()
        session_mock = MagicMock()
        session_mock.__enter__ = MagicMock(return_value=session_mock)
        session_mock.__exit__ = MagicMock(return_value=False)

        record = MagicMock()
        record.__iter__ = MagicMock(return_value=iter([("name", "Alice")]))
        session_mock.run.return_value = [record]
        driver_mock.session.return_value = session_mock

        client = _make_client(driver_mock)
        result = client.execute_cypher("MATCH (n) RETURN n.name AS name")
        assert isinstance(result, list)

    def test_passes_params_to_driver(self) -> None:
        driver_mock = MagicMock()
        session_mock = MagicMock()
        session_mock.__enter__ = MagicMock(return_value=session_mock)
        session_mock.__exit__ = MagicMock(return_value=False)
        session_mock.run.return_value = []
        driver_mock.session.return_value = session_mock

        client = _make_client(driver_mock)
        client.execute_cypher("MATCH (n {name: $name}) RETURN n", {"name": "X"})
        session_mock.run.assert_called_once_with(
            "MATCH (n {name: $name}) RETURN n",
            parameters={"name": "X"},
        )


# ── execute_batch ──────────────────────────────────────────────────────────────

class TestExecuteBatch:
    def test_empty_batch_is_noop(self) -> None:
        driver_mock = MagicMock()
        client = _make_client(driver_mock)
        client.execute_batch([])
        driver_mock.session.assert_not_called()

    def test_calls_execute_write(self) -> None:
        driver_mock = MagicMock()
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


# ── setup_schema ──────────────────────────────────────────────────────────────

class TestSetupSchema:
    def test_all_statements_executed(self) -> None:
        from src.graph.neo4j_client import _SCHEMA_STATEMENTS
        client_mock = MagicMock()
        client_mock.execute_cypher.return_value = []
        setup_schema(client_mock)
        assert client_mock.execute_cypher.call_count == len(_SCHEMA_STATEMENTS)

    def test_failed_statement_does_not_raise(self) -> None:
        client_mock = MagicMock()
        client_mock.execute_cypher.side_effect = Exception("unsupported")
        # Should NOT raise — just log warnings
        setup_schema(client_mock)
```

---

## 6. Smoke Test

```bash
python -c "
from src.graph.neo4j_client import Neo4jClient, setup_schema

# Requires a running Neo4j instance. Set env vars first:
# NEO4J_URI=bolt://localhost:7687
# NEO4J_USERNAME=neo4j
# NEO4J_PASSWORD=password

with Neo4jClient() as client:
    setup_schema(client)
    result = client.execute_cypher('RETURN 1 AS ping')
    print('Ping result:', result)
    print('Neo4jClient context manager OK.')
"
```
