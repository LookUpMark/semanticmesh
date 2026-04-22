"""Neo4j driver wrapper — EP-10 / US-10-01 and US-10-02.

Provides a thin context-manager around the official neo4j Python driver,
plus idempotent schema setup (constraints and vector index for BGE-M3).
"""

from __future__ import annotations

import logging
from threading import Lock
from types import TracebackType
from typing import Any

from neo4j import GraphDatabase, ManagedTransaction, Result

from src.config.logging import get_logger
from src.config.settings import get_settings

logger: logging.Logger = get_logger(__name__)

_EMBEDDING_DIMENSION: int = 1024

# Singleton driver — reused across all Neo4jClient instances.
_driver_lock = Lock()
_singleton_driver = None
_singleton_uri: str | None = None
_singleton_auth: tuple[str, str] | None = None


def _get_shared_driver(uri: str, auth: tuple[str, str]):
    """Return a singleton Neo4j driver, creating it if needed."""
    global _singleton_driver, _singleton_uri, _singleton_auth
    with _driver_lock:
        if _singleton_driver is not None and _singleton_uri == uri and _singleton_auth == auth:
            return _singleton_driver
        # Close old driver if URI/auth changed
        if _singleton_driver is not None:
            try:
                _singleton_driver.close()
            except Exception:
                logger.debug("Old driver close failed", exc_info=True)
        _singleton_driver = GraphDatabase.driver(uri, auth=auth)
        _singleton_driver.verify_connectivity()
        _singleton_uri = uri
        _singleton_auth = auth
        logger.debug("Neo4j shared driver connected to %s.", uri)
        return _singleton_driver


def close_shared_driver() -> None:
    """Close the singleton driver. Call on shutdown or settings reload."""
    global _singleton_driver, _singleton_uri, _singleton_auth
    with _driver_lock:
        if _singleton_driver is not None:
            _singleton_driver.close()
            logger.debug("Neo4j shared driver closed.")
        _singleton_driver = None
        _singleton_uri = None
        _singleton_auth = None

_SCHEMA_STATEMENTS: list[str] = [
    "CREATE CONSTRAINT businessconcept_name_unique IF NOT EXISTS "
    "FOR (n:BusinessConcept) REQUIRE n.name IS UNIQUE",
    "CREATE CONSTRAINT physicaltable_name_unique IF NOT EXISTS "
    "FOR (n:PhysicalTable) REQUIRE n.table_name IS UNIQUE",
    # SourceFile registry — one node per ingested file, keyed by canonical path.
    # Stores SHA-256 of file contents to enable incremental re-ingestion.
    "CREATE CONSTRAINT sourcefile_path_unique IF NOT EXISTS "
    "FOR (n:SourceFile) REQUIRE n.path IS UNIQUE",
    "CREATE INDEX chunk_source_doc IF NOT EXISTS FOR (c:Chunk) ON (c.source_doc)",
    "CREATE INDEX parentchunk_source_doc IF NOT EXISTS FOR (pc:ParentChunk) ON (pc.source_doc)",
    (
        "CREATE VECTOR INDEX businessconcept_embedding IF NOT EXISTS "
        "FOR (n:BusinessConcept) ON n.embedding "
        "OPTIONS {indexConfig: {`vector.dimensions`: %d, `vector.similarity_function`: 'cosine'}}"
    )
    % _EMBEDDING_DIMENSION,
    (
        "CREATE VECTOR INDEX chunk_embedding IF NOT EXISTS "
        "FOR (c:Chunk) ON c.embedding "
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

    def __enter__(self) -> Neo4jClient:
        self._driver = _get_shared_driver(self._uri, (self._username, self._password))
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        # Driver is shared — do NOT close it here. close_shared_driver() on shutdown.
        return None

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
            logger.warning("Schema statement failed (skipping): %s", exc)
    logger.info("Schema setup complete.")
