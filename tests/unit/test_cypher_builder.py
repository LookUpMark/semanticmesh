"""Unit tests for src/graph/cypher_builder.py — build_fk_cypher."""

from __future__ import annotations

from src.graph.cypher_builder import build_fk_cypher, build_upsert_cypher
from src.models.schemas import ColumnSchema, EnrichedTableSchema, MappingProposal

# ── Helpers ───────────────────────────────────────────────────────────────────


def _make_table(
    name: str,
    columns: list[ColumnSchema],
) -> EnrichedTableSchema:
    return EnrichedTableSchema(
        table_name=name,
        schema_name=None,
        columns=columns,
        ddl_source="",
        enriched_name=name,
        column_descriptions={},
    )


def _col(name: str, is_fk: bool = False, references: str | None = None) -> ColumnSchema:
    return ColumnSchema(
        name=name,
        data_type="VARCHAR",
        is_primary_key=False,
        is_foreign_key=is_fk,
        references=references,
    )


def _proposal(concept: str = "Customer", confidence: float = 0.9) -> MappingProposal:
    return MappingProposal(
        table_name="T",
        mapped_concept=concept,
        confidence=confidence,
        reasoning="test",
    )


# ── build_fk_cypher ───────────────────────────────────────────────────────────


class TestBuildFkCypher:
    def test_no_fk_columns_returns_empty(self) -> None:
        table = _make_table("ORDERS", [_col("ID"), _col("NAME")])
        assert build_fk_cypher(table) == []

    def test_single_fk_returns_one_statement(self) -> None:
        table = _make_table(
            "ORDERS",
            [_col("CUST_ID", is_fk=True, references="CUSTOMERS.ID")],
        )
        stmts = build_fk_cypher(table)
        assert len(stmts) == 1
        cypher, params = stmts[0]
        assert "REFERENCES" in cypher
        assert "MERGE" in cypher
        assert params["src_table"] == "ORDERS"
        assert params["tgt_table"] == "CUSTOMERS"
        assert params["fk_column"] == "CUST_ID"
        assert params["ref_column"] == "ID"

    def test_multiple_fk_columns(self) -> None:
        table = _make_table(
            "LINE_ITEMS",
            [
                _col("ORDER_ID", is_fk=True, references="ORDERS.ID"),
                _col("PRODUCT_ID", is_fk=True, references="PRODUCTS.SKU"),
                _col("QTY"),
            ],
        )
        stmts = build_fk_cypher(table)
        assert len(stmts) == 2
        targets = {p["tgt_table"] for _, p in stmts}
        assert targets == {"ORDERS", "PRODUCTS"}

    def test_references_without_column_part(self) -> None:
        """references value without a dot should still produce a statement."""
        table = _make_table(
            "ORDERS",
            [_col("CUST_ID", is_fk=True, references="CUSTOMERS")],
        )
        stmts = build_fk_cypher(table)
        assert len(stmts) == 1
        _, params = stmts[0]
        assert params["tgt_table"] == "CUSTOMERS"
        assert params["ref_column"] == ""

    def test_fk_column_not_fk_is_ignored(self) -> None:
        """A column with is_foreign_key=False and references set is skipped."""
        col = ColumnSchema(
            name="CUST_ID",
            data_type="INT",
            is_primary_key=False,
            is_foreign_key=False,
            references="CUSTOMERS.ID",
        )
        table = _make_table("ORDERS", [col])
        assert build_fk_cypher(table) == []


# ── build_upsert_cypher (smoke test) ─────────────────────────────────────────


class TestBuildUpsertCypher:
    def test_returns_cypher_and_params(self) -> None:
        table = _make_table("CUST", [_col("ID"), _col("NAME")])
        cypher, params = build_upsert_cypher(_proposal(), table)
        assert "MERGE" in cypher
        assert params["concept_name"] == "Customer"
        assert params["table_name"] == "CUST"
        assert "ID" in params["column_names"]
