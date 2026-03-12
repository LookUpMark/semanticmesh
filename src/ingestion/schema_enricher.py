"""LLM Schema Enrichment node.

EP-05b: Expands abbreviated DDL identifiers into human-readable English names.
Called before the RAG Mapping step to reduce the lexical gap between
schema conventions and business glossary terminology.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import ValidationError

from src.config.logging import NodeTimer, get_logger
from src.models.schemas import EnrichedColumn, EnrichedTableSchema, TableSchema
from src.prompts.templates import ENRICHMENT_SYSTEM, ENRICHMENT_USER

if TYPE_CHECKING:
    import logging

    from src.config.llm_client import LLMProtocol

logger: logging.Logger = get_logger(__name__)


def _format_columns_text(table: TableSchema) -> str:
    """Format column list as a text block for the ENRICHMENT_USER prompt.

    Example output:
        CUST_ID INT (PK)
        FULL_NAME VARCHAR
        EMAIL VARCHAR
    """
    lines: list[str] = []
    for col in table.columns:
        flags: list[str] = []
        if col.is_primary_key:
            flags.append("PK")
        if col.is_foreign_key:
            ref = f"FK -> {col.references}" if col.references else "FK"
            flags.append(ref)
        flag_str = f" ({', '.join(flags)})" if flags else ""
        lines.append(f"{col.name} {col.data_type}{flag_str}")
    return "\n".join(lines)


def enrich_schema(table: TableSchema, llm: LLMProtocol) -> EnrichedTableSchema:
    """Call an LLM to enrich one TableSchema with human-readable names.

    The LLM receives ENRICHMENT_SYSTEM + ENRICHMENT_USER and returns a JSON
    object with ``enriched_table_name``, ``enriched_columns``, and
    ``table_description``.

    On any failure (LLM error, JSON parse error, Pydantic ``ValidationError``),
    the function logs a warning and returns an ``EnrichedTableSchema`` with
    enrichment fields left as ``None`` / empty -- the pipeline continues.

    Args:
        table: Parsed ``TableSchema`` from ``ddl_parser``.
        llm: Any ``LLMProtocol`` instance (use ``get_reasoning_llm()`` from factory).

    Returns:
        ``EnrichedTableSchema`` with enrichment fields populated (best-effort).
    """
    columns_text = _format_columns_text(table)
    user_prompt = ENRICHMENT_USER.format(
        table_name=table.table_name,
        columns_text=columns_text,
    )

    with NodeTimer() as timer:
        try:
            response = llm.invoke(
                [
                    SystemMessage(content=ENRICHMENT_SYSTEM),
                    HumanMessage(content=user_prompt),
                ]
            )
            # AIMessage.content can be str | list[str | dict[Any, Any]]
            # For enrichment, we expect plain JSON string
            content = response.content
            if not isinstance(content, str):
                logger.warning(
                    "LLM returned non-string content for table '%s' -- "
                    "returning unenriched schema.",
                    table.table_name,
                )
                return EnrichedTableSchema.from_table_schema(table)
            raw_json: str = content.strip()
        except Exception as exc:
            logger.warning(
                "LLM call failed for table '%s': %s -- returning unenriched schema.",
                table.table_name, exc,
            )
            return EnrichedTableSchema.from_table_schema(table)

    logger.debug(
        "Schema enrichment LLM call for '%s' completed in %.0f ms",
        table.table_name, timer.elapsed_ms,
    )

    # Parse JSON response
    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError as exc:
        logger.warning(
            "Non-JSON response for table '%s': %s -- returning unenriched schema.",
            table.table_name, exc,
        )
        return EnrichedTableSchema.from_table_schema(table)

    # Build enriched column list
    enriched_columns: list[EnrichedColumn] = []
    for entry in data.get("enriched_columns", []):
        try:
            enriched_columns.append(
                EnrichedColumn(
                    original_name=entry.get("original", ""),
                    enriched_name=entry.get("enriched", entry.get("original", "")),
                )
            )
        except (KeyError, TypeError, ValidationError):
            continue  # skip malformed column entries silently

    enriched = EnrichedTableSchema.from_table_schema(table)
    enriched.enriched_table_name = data.get("enriched_table_name")
    enriched.table_description = data.get("table_description")
    enriched.enriched_columns = enriched_columns

    logger.info(
        "Enriched table '%s' -> '%s' (%d columns enriched)",
        table.table_name,
        enriched.enriched_table_name or "(no enrichment)",
        len(enriched_columns),
    )
    return enriched


def enrich_all(
    tables: list[TableSchema],
    llm: LLMProtocol,
) -> list[EnrichedTableSchema]:
    """Enrich every table in the list; gracefully degrade on individual failures.

    Args:
        tables: List of ``TableSchema`` objects from ``ddl_parser``.
        llm: LLM instance to call for enrichment.

    Returns:
        List of ``EnrichedTableSchema`` with the same length as ``tables``.
        Tables that could not be enriched are returned with enrichment fields
        set to ``None`` / empty (never dropped).
    """
    results: list[EnrichedTableSchema] = []
    for table in tables:
        enriched = enrich_schema(table, llm)
        results.append(enriched)
    logger.info("Enriched %d/%d tables successfully.", len(results), len(tables))
    return results
