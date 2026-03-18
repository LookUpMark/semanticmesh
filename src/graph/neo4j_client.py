"""Neo4j driver wrapper — EP-10 / US-10-01 and US-10-02.

Provides a thin context-manager around the official neo4j Python driver,
plus idempotent schema setup (constraints and vector index for BGE-M3).
"""

from __future__ import annotations

import logging
from types import TracebackType
from typing import Any

from neo4j import GraphDatabase, ManagedTransaction, Result

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
    "CREATE INDEX chunk_source_doc IF NOT EXISTS FOR (c:Chunk) ON (c.source_doc)",
    # Vector index for BGE-M3 embeddings on BusinessConcept nodes
    # Note: indexConfig keys require backtick quoting in Cypher map literals.
    (
        "CREATE VECTOR INDEX businessconcept_embedding IF NOT EXISTS "
        "FOR (n:BusinessConcept) ON n.embedding "
        "OPTIONS {indexConfig: {`vector.dimensions`: %d, `vector.similarity_function`: 'cosine'}}"
    )
    % _EMBEDDING_DIMENSION,
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
        self._username: str = username or settings.neo4j_user
        self._password: str = password or (
            settings.neo4j_password.get_secret_value() if settings.neo4j_password else ""
        )
        self._driver = None

    # ── Lifecycle ──────────────────────────────────────────────────────────────

    def __enter__(self) -> Neo4jClient:
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
    def driver(self) -> GraphDatabase.driver:
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
