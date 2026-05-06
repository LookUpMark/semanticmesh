"""Unit tests for src/mapping/rag_mapper.py — UT-07"""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import numpy as np

from src.mapping.rag_mapper import propose_mapping, propose_mapping_heuristic
from src.mapping.retrieval import build_retrieval_query, retrieve_top_entities
from src.models.schemas import (
    ColumnSchema,
    EnrichedColumn,
    EnrichedTableSchema,
    Entity,
    MappingProposal,
    TableSchema,
)


def _make_table(name: str = "TB_CST", ddl: str = "") -> TableSchema:
    if not ddl:
        ddl = f"CREATE TABLE {name} (ID INT PRIMARY KEY);"
    return TableSchema(
        table_name=name,
        columns=[ColumnSchema(name="ID", data_type="INT", is_primary_key=True)],
        ddl_source=ddl,
    )


def _make_enriched(name: str = "TB_CST") -> EnrichedTableSchema:
    base = _make_table(name)
    e = EnrichedTableSchema.from_table_schema(base)
    e.enriched_table_name = "Customer Table"
    e.table_description = "Stores customer records."
    e.enriched_columns = [EnrichedColumn(original_name="ID", enriched_name="Customer ID")]
    return e


def _make_entity(name: str, definition: str = "") -> Entity:
    return Entity(
        name=name,
        definition=definition,
        synonyms=[],
        provenance_text="",
        source_doc="test.pdf",
    )


def _make_llm_proposal(table_name: str, concept: str, confidence: float) -> MagicMock:
    llm = MagicMock()
    resp = MagicMock()
    resp.content = json.dumps(
        {
            "table_name": table_name,
            "mapped_concept": concept,
            "confidence": confidence,
            "reasoning": "test reasoning",
            "alternative_concepts": [],
        }
    )
    llm.invoke.return_value = resp
    return llm


class TestBuildRetrievalQuery:
    def test_uses_enriched_name_when_available(self) -> None:
        table = _make_enriched("TB_CST")
        query = build_retrieval_query(table)
        assert "Customer Table" in query
        assert "TB_CST" not in query

    def test_fallback_to_original_name(self) -> None:
        table = EnrichedTableSchema.from_table_schema(_make_table("TB_CST"))
        query = build_retrieval_query(table)
        assert "TB_CST" in query

    def test_includes_description(self) -> None:
        table = _make_enriched()
        query = build_retrieval_query(table)
        assert "Stores customer records" in query

    def test_includes_enriched_columns(self) -> None:
        table = _make_enriched()
        query = build_retrieval_query(table)
        assert "Customer ID" in query

    def test_caps_columns_at_10(self) -> None:
        table = _make_table("TB_MANY")
        enriched = EnrichedTableSchema.from_table_schema(table)
        enriched.enriched_columns = [
            EnrichedColumn(original_name=f"COL{i}", enriched_name=f"Column {i}") for i in range(15)
        ]
        query = build_retrieval_query(enriched)
        assert "Column 14" not in query
        assert "Column 0" in query


class TestRetrieveTopEntities:
    def _make_embeddings(self, query_vec: list, entity_vecs: list[list]) -> MagicMock:
        """Mock embedder: single-text calls → query_vec, multi-text calls → entity_vecs."""
        emb = MagicMock()

        def encode(texts: list, **kw: object) -> np.ndarray:
            if len(texts) == 1:
                return np.array([query_vec])
            return np.array(entity_vecs)

        emb.encode.side_effect = encode
        return emb

    def test_returns_top_k(self) -> None:
        entities = [_make_entity(f"E{i}") for i in range(5)]
        emb = self._make_embeddings([1, 0], [[1, 0]] * 5)
        result = retrieve_top_entities("query", entities, emb, top_k=3)
        assert len(result) == 3

    def test_empty_entities_returns_empty(self) -> None:
        emb = MagicMock()
        result = retrieve_top_entities("query", [], emb, top_k=5)
        assert result == []

    def test_most_similar_entity_is_first(self) -> None:
        entities = [
            _make_entity("Customer", "A person who buys"),
            _make_entity("Product", "An item for sale"),
        ]
        emb = self._make_embeddings([1, 0], [[1, 0], [0, 1]])
        result = retrieve_top_entities("query", entities, emb, top_k=2)
        assert result[0].name == "Customer"
        assert result[1].name == "Product"

    def test_uses_definition_when_available(self) -> None:
        entities = [
            _make_entity("Customer", "A person who buys things"),
            _make_entity("CUST", ""),
        ]
        query = "person who buys things"
        emb = self._make_embeddings([0.9, 0.1], [[0.9, 0.1], [0.5, 0.5]])
        result = retrieve_top_entities(query, entities, emb, top_k=1)
        assert result[0].name == "Customer"


class TestProposeMapping:
    def test_happy_path_returns_proposal(self) -> None:
        table = _make_table("TB_CST")
        entities = [_make_entity("Customer", "A person who buys things.")]
        llm = _make_llm_proposal("TB_CST", "Customer", 0.95)
        result = propose_mapping(table, entities, llm)
        assert isinstance(result, MappingProposal)
        assert result.mapped_concept == "Customer"
        assert result.confidence == 0.95

    def test_llm_error_returns_null_mapping(self) -> None:
        table = _make_table()
        llm = MagicMock()
        llm.invoke.side_effect = RuntimeError("server error")
        result = propose_mapping(table, [], llm)
        assert result.mapped_concept is None
        assert result.confidence == 0.0
        assert "LLM call failed" in result.reasoning

    def test_invalid_json_returns_null_mapping(self) -> None:
        table = _make_table()
        llm = MagicMock()
        resp = MagicMock()
        resp.content = "not json"
        llm.invoke.return_value = resp
        result = propose_mapping(table, [], llm)
        assert result.mapped_concept is None
        assert result.confidence == 0.0
        assert "JSON parse error" in result.reasoning

    def test_pydantic_validation_error_returns_null_mapping(self) -> None:
        table = _make_table()
        llm = MagicMock()
        resp = MagicMock()
        resp.content = json.dumps({"table_name": "TB_CST", "mapped_concept": "Customer"})
        llm.invoke.return_value = resp
        result = propose_mapping(table, [], llm)
        assert result.mapped_concept is None
        assert result.confidence == 0.0
        assert "Pydantic validation error" in result.reasoning

    def test_reflection_prompt_prepended_to_few_shot(self) -> None:
        table = _make_table()
        entities = [_make_entity("Customer")]
        llm = MagicMock()
        resp = MagicMock()
        resp.content = json.dumps(
            {
                "table_name": "TB_CST",
                "mapped_concept": "Customer",
                "confidence": 0.95,
                "reasoning": "test",
                "alternative_concepts": [],
            }
        )
        llm.invoke.return_value = resp

        few_shot = "Example few shot text"
        reflection = "Your previous attempt was wrong because..."

        propose_mapping(
            table, entities, llm, few_shot_examples=few_shot, reflection_prompt=reflection
        )

        call_args = llm.invoke.call_args
        user_message = call_args[0][0][1]
        assert "[REFLECTION CRITIQUE" in user_message.content
        assert reflection in user_message.content
        assert few_shot in user_message.content


class TestProposeMappingHeuristic:
    @patch("src.mapping.rag_mapper._embed_texts_batch")
    @patch("src.mapping.rag_mapper.embed_text")
    @patch("src.mapping.retrieval.retrieve_top_entities")
    @patch("src.mapping.rag_mapper.get_settings")
    def test_returns_mapped_concept_when_confidence_above_threshold(
        self,
        mock_get_settings,
        mock_retrieve_top,
        mock_embed_text,
        mock_embed_texts_batch,
    ) -> None:
        table = _make_enriched("TB_CST")
        entities = [_make_entity("Customer", "A person who buys things")]
        mock_get_settings.return_value = MagicMock(heuristic_mapping_confidence_threshold=0.60)
        mock_retrieve_top.return_value = entities
        mock_embed_text.return_value = [1.0, 0.0]
        mock_embed_texts_batch.return_value = [[1.0, 0.0]]

        out = propose_mapping_heuristic(table, entities, MagicMock())

        assert out.mapped_concept == "Customer"
        assert out.confidence >= 0.9

    @patch("src.mapping.rag_mapper._embed_texts_batch")
    @patch("src.mapping.rag_mapper.embed_text")
    @patch("src.mapping.retrieval.retrieve_top_entities")
    @patch("src.mapping.rag_mapper.get_settings")
    def test_penalizes_column_like_candidate_and_selects_concept(
        self,
        mock_get_settings,
        mock_retrieve_top,
        mock_embed_text,
        mock_embed_texts_batch,
    ) -> None:
        base = _make_table("TB_PRODUCT")
        base.columns.append(ColumnSchema(name="WEIGHT_KG", data_type="DECIMAL"))
        table = EnrichedTableSchema.from_table_schema(base)
        table.enriched_table_name = "Product"

        entities = [
            _make_entity("WEIGHT_KG", "A numeric value"),
            _make_entity("Product", "A tangible or digital item offered for sale"),
        ]
        mock_get_settings.return_value = MagicMock(heuristic_mapping_confidence_threshold=0.55)
        mock_retrieve_top.return_value = entities

        mock_embed_text.return_value = [1.0, 0.0]
        mock_embed_texts_batch.return_value = [[1.0, 0.0], [0.98, 0.02]]

        out = propose_mapping_heuristic(table, entities, MagicMock())

        assert out.mapped_concept == "Product"
        assert out.confidence >= 0.55

    @patch("src.mapping.rag_mapper._embed_texts_batch")
    @patch("src.mapping.rag_mapper.embed_text")
    @patch("src.mapping.retrieval.retrieve_top_entities")
    @patch("src.mapping.rag_mapper.get_settings")
    def test_falls_back_to_enriched_table_name_when_best_candidate_is_attribute_like(
        self,
        mock_get_settings,
        mock_retrieve_top,
        mock_embed_text,
        mock_embed_texts_batch,
    ) -> None:
        base = _make_table("TB_PRODUCT")
        base.columns.append(ColumnSchema(name="WEIGHT_KG", data_type="DECIMAL"))
        table = EnrichedTableSchema.from_table_schema(base)
        table.enriched_table_name = "Product"

        entities = [_make_entity("WEIGHT_KG", "Numeric weight")]
        mock_get_settings.return_value = MagicMock(heuristic_mapping_confidence_threshold=0.60)
        mock_retrieve_top.return_value = entities
        mock_embed_text.return_value = [1.0, 0.0]
        mock_embed_texts_batch.return_value = [[1.0, 0.0]]

        out = propose_mapping_heuristic(table, entities, MagicMock())

        assert out.mapped_concept == "Product"
        assert out.confidence >= 0.55

    @patch("src.mapping.retrieval.retrieve_top_entities")
    def test_returns_null_mapping_when_no_candidates(self, mock_retrieve_top) -> None:
        table = _make_enriched("TB_CST")
        mock_retrieve_top.return_value = []

        out = propose_mapping_heuristic(table, [], MagicMock())

        assert out.mapped_concept is None
        assert out.confidence == 0.0
