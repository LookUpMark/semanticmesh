"""Unit tests for src.mapping.retrieval."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from src.mapping.retrieval import build_retrieval_query, retrieve_top_entities
from src.models.schemas import ColumnSchema, EnrichedTableSchema, Entity, TableSchema


def _make_table(name: str, enriched_name: str | None = None) -> EnrichedTableSchema:
    base = TableSchema(
        table_name=name,
        columns=[
            ColumnSchema(name="id", data_type="INTEGER", is_primary_key=True),
            ColumnSchema(name="name", data_type="VARCHAR"),
        ],
        ddl_source=f"CREATE TABLE {name} (id INT, name VARCHAR);",
        source_file="schema.sql",
    )
    table = EnrichedTableSchema.from_table_schema(base)
    if enriched_name:
        table.enriched_table_name = enriched_name
    return table


def _make_entity(name: str, definition: str = "") -> Entity:
    return Entity(
        name=name, definition=definition, synonyms=[],
        provenance_text="test", source_doc="test.txt",
    )


class TestBuildRetrievalQuery:
    def test_uses_enriched_name_when_available(self) -> None:
        table = _make_table("TB_CST", enriched_name="Customer")
        table.table_description = "A buyer of products"
        query = build_retrieval_query(table)
        assert "Customer" in query
        assert "buyer" in query

    def test_falls_back_to_table_name(self) -> None:
        table = _make_table("TB_ORD")
        query = build_retrieval_query(table)
        assert "TB_ORD" in query

    def test_includes_column_names(self) -> None:
        table = _make_table("TB_PRD")
        query = build_retrieval_query(table)
        assert "name" in query


class TestRetrieveTopEntities:
    @patch("src.mapping.retrieval.embed_texts")
    @patch("src.mapping.retrieval.embed_text")
    def test_returns_top_k_entities(self, mock_embed_text, mock_embed_texts) -> None:
        # Query vector
        mock_embed_text.return_value = [1.0, 0.0, 0.0]
        # Entity vectors — first is most similar to query
        mock_embed_texts.return_value = [
            [1.0, 0.0, 0.0],   # identical to query
            [0.0, 1.0, 0.0],   # orthogonal
            [0.7, 0.7, 0.0],   # partially similar
        ]

        entities = [
            _make_entity("Order", "A purchase transaction"),
            _make_entity("Product", "An item for sale"),
            _make_entity("Customer", "A buyer"),
        ]

        result = retrieve_top_entities("Order purchase", entities, MagicMock(), top_k=2)
        assert len(result) == 2
        assert result[0].name == "Order"  # highest similarity

    @patch("src.mapping.retrieval.embed_texts")
    @patch("src.mapping.retrieval.embed_text")
    def test_returns_empty_for_no_entities(self, mock_embed_text, mock_embed_texts) -> None:
        result = retrieve_top_entities("query", [], MagicMock(), top_k=5)
        assert result == []
        mock_embed_text.assert_not_called()

    @patch("src.mapping.retrieval.embed_texts")
    @patch("src.mapping.retrieval.embed_text")
    def test_respects_top_k(self, mock_embed_text, mock_embed_texts) -> None:
        mock_embed_text.return_value = [1.0, 0.0]
        mock_embed_texts.return_value = [[1.0, 0.0], [0.5, 0.5], [0.0, 1.0]]
        entities = [_make_entity(f"E{i}") for i in range(3)]

        result = retrieve_top_entities("test", entities, MagicMock(), top_k=1)
        assert len(result) == 1
