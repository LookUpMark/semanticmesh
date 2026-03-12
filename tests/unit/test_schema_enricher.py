"""Unit tests for src/ingestion/schema_enricher.py -- UT-17"""

from __future__ import annotations

import json
from unittest.mock import MagicMock

from src.ingestion.schema_enricher import enrich_all, enrich_schema
from src.models.schemas import ColumnSchema, EnrichedTableSchema, TableSchema

# ---- Fixtures ----


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


# ---- enrich_schema ----


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
        table = _make_table("TB_ORD", num_cols=2)
        llm = MagicMock()
        response = MagicMock()
        # Missing enriched_columns key -- should still not crash
        response.content = json.dumps({"enriched_table_name": "Order Table"})
        llm.invoke.return_value = response
        result = enrich_schema(table, llm)
        assert result.enriched_table_name == "Order Table"
        assert result.enriched_columns == []


# ---- enrich_all ----


class TestEnrichAll:
    def test_returns_same_count_as_input(self) -> None:
        tables = [_make_table(f"T{i}") for i in range(5)]
        llm = _make_llm_response("T", num_cols=3)
        results = enrich_all(tables, llm)
        assert len(results) == 5

    def test_one_llm_error_does_not_stop_others(self) -> None:
        tables = [_make_table("T_GOOD"), _make_table("T_BAD"), _make_table("T_GOOD2")]

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
