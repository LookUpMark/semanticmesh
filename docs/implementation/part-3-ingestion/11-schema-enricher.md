# Part 3 — `src/ingestion/schema_enricher.py`

## 1. Purpose & Context

**Epic:** EP-05b LLM Schema Enrichment  
**US-05b-01** — Schema Enrichment Node

Expands abbreviated DDL identifiers (`TB_CST`, `CUST_ADDR`, `ORD_DT`) into human-readable English names using an LLM and generates a brief business-purpose description for each table. This resolves the **Lexical Gap**: without enrichment, the embedding distance between `TB_CST` and `Customer` can block a correct mapping. See ADR-15.

Original identifiers are **never modified** — enriched names are additive metadata stored in new fields.

---

## 2. Prerequisites

- `src/models/schemas.py` — `TableSchema`, `EnrichedColumn`, `EnrichedTableSchema` (step 3)
- `src/prompts/templates.py` — `ENRICHMENT_SYSTEM`, `ENRICHMENT_USER` (step 7)
- `src/config/logging.py` — `get_logger`, `NodeTimer`
- LLM arg: caller passes `LLMProtocol` from `src/config/llm_client` (see step 4b)

---

## 3. Public API

| Symbol | Signature | Description |
|---|---|---|
| `enrich_schema` | `(table: TableSchema, llm: LLMProtocol) -> EnrichedTableSchema` | Calls LLM once per table to produce human-readable names and a description |
| `enrich_all` | `(tables: list[TableSchema], llm: LLMProtocol) -> list[EnrichedTableSchema]` | Enriches every table in the list; gracefully degrades on individual failures |

---

## 4. Full Implementation

```python
"""LLM Schema Enrichment node.

EP-05b: Expands abbreviated DDL identifiers into human-readable English names.
Called before the RAG Mapping step to reduce the lexical gap between
schema conventions and business glossary terminology.
"""

from __future__ import annotations

import json
import logging

from langchain_core.messages import HumanMessage, SystemMessage

from src.config.llm_client import LLMProtocol
from pydantic import ValidationError

from src.config.logging import NodeTimer, get_logger
from src.models.schemas import EnrichedColumn, EnrichedTableSchema, TableSchema
from src.prompts.templates import ENRICHMENT_SYSTEM, ENRICHMENT_USER

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
            ref = f"FK → {col.references}" if col.references else "FK"
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
    enrichment fields left as ``None`` / empty — the pipeline continues.

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
            raw_json: str = response.content.strip()
        except Exception as exc:
            logger.warning(
                "LLM call failed for table '%s': %s — returning unenriched schema.",
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
            "Non-JSON response for table '%s': %s — returning unenriched schema.",
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
        "Enriched table '%s' → '%s' (%d columns enriched)",
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
```

---

## 5. Tests

```python
"""Unit tests for src/ingestion/schema_enricher.py — UT-17"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from src.ingestion.schema_enricher import enrich_all, enrich_schema
from src.models.schemas import ColumnSchema, EnrichedTableSchema, TableSchema

# ── Fixtures ───────────────────────────────────────────────────────────────────

def _make_table(name: str = "TB_CST", num_cols: int = 3) -> TableSchema:
    cols = [
        ColumnSchema(name=f"COL_{i}", data_type="VARCHAR", is_primary_key=(i == 0))
        for i in range(num_cols)
    ]
    return TableSchema(
        table_name=name,
        columns=cols,
        ddl_source=f"CREATE TABLE {name} (COL_0 INT PRIMARY KEY);",
    )


def _make_llm_response(table_name: str, num_cols: int) -> MagicMock:
    """Return a mock LLM that produces valid enrichment JSON."""
    import json

    enriched_cols = [
        {"original": f"COL_{i}", "enriched": f"Column {i}"} for i in range(num_cols)
    ]
    payload = {
        "enriched_table_name": "Customer Table",
        "enriched_columns": enriched_cols,
        "table_description": "Stores customer identity data.",
    }
    llm = MagicMock()
    response = MagicMock()
    response.content = json.dumps(payload)
    llm.invoke.return_value = response
    return llm


# ── enrich_schema ─────────────────────────────────────────────────────────────

class TestEnrichSchema:
    def test_returns_enriched_table_schema(self) -> None:
        table = _make_table("TB_CST", num_cols=2)
        llm = _make_llm_response("TB_CST", num_cols=2)
        result = enrich_schema(table, llm)
        assert isinstance(result, EnrichedTableSchema)
        assert result.enriched_table_name == "Customer Table"

    def test_original_table_name_unchanged(self) -> None:
        table = _make_table("TB_CST", num_cols=2)
        llm = _make_llm_response("TB_CST", num_cols=2)
        result = enrich_schema(table, llm)
        assert result.table_name == "TB_CST"

    def test_enriched_columns_populated(self) -> None:
        table = _make_table("TB_CST", num_cols=3)
        llm = _make_llm_response("TB_CST", num_cols=3)
        result = enrich_schema(table, llm)
        assert len(result.enriched_columns) == 3
        assert result.enriched_columns[0].enriched_name == "Column 0"

    def test_llm_error_returns_unenriched_gracefully(self) -> None:
        table = _make_table()
        llm = MagicMock()
        llm.invoke.side_effect = RuntimeError("LLM timeout")
        result = enrich_schema(table, llm)
        assert isinstance(result, EnrichedTableSchema)
        assert result.enriched_table_name is None
        assert result.enriched_columns == []

    def test_bad_json_response_returns_unenriched(self) -> None:
        table = _make_table()
        llm = MagicMock()
        response = MagicMock()
        response.content = "This is not JSON at all"
        llm.invoke.return_value = response
        result = enrich_schema(table, llm)
        assert result.enriched_table_name is None

    def test_partial_json_graceful_degradation(self) -> None:
        import json
        table = _make_table("TB_ORD", num_cols=2)
        llm = MagicMock()
        response = MagicMock()
        # Missing enriched_columns key — should still not crash
        response.content = json.dumps({"enriched_table_name": "Order Table"})
        llm.invoke.return_value = response
        result = enrich_schema(table, llm)
        assert result.enriched_table_name == "Order Table"
        assert result.enriched_columns == []


# ── enrich_all ────────────────────────────────────────────────────────────────

class TestEnrichAll:
    def test_returns_same_count_as_input(self) -> None:
        tables = [_make_table(f"T{i}") for i in range(5)]
        llm = _make_llm_response("T", num_cols=3)
        results = enrich_all(tables, llm)
        assert len(results) == 5

    def test_one_llm_error_does_not_stop_others(self) -> None:
        tables = [_make_table("T_GOOD"), _make_table("T_BAD"), _make_table("T_GOOD2")]
        import json

        call_count = 0

        def side_effect(messages):
            nonlocal call_count
            call_count += 1
            if call_count == 2:
                raise RuntimeError("simulated failure")
            resp = MagicMock()
            resp.content = json.dumps({
                "enriched_table_name": "Good Table",
                "enriched_columns": [],
                "table_description": "desc",
            })
            return resp

        llm = MagicMock()
        llm.invoke.side_effect = side_effect

        results = enrich_all(tables, llm)
        assert len(results) == 3
        assert results[1].enriched_table_name is None  # degraded gracefully
```

---

## 6. Smoke Test

```bash
python -c "
from src.ingestion.ddl_parser import parse_ddl_file
from src.ingestion.schema_enricher import enrich_schema
from src.config.llm_factory import get_reasoning_llm
from pathlib import Path

tables = parse_ddl_file(Path('tests/fixtures/sample_ddl/simple_schema.sql'))
llm = get_reasoning_llm()
enriched = enrich_schema(tables[0], llm)
print('Original:', enriched.table_name)
print('Enriched:', enriched.enriched_table_name)
print('Description:', enriched.table_description)
"
```
