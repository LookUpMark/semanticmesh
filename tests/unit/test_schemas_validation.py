"""Unit tests for Pydantic model validation — mutation-style edge case coverage.

Boundary values, type coercion, missing fields, and invalid combinations.
"""

from __future__ import annotations

import pytest

from src.models.schemas import (
    Chunk,
    Document,
    Triplet,
    TripletExtractionResponse,
    GraderDecision,
    RetrievedChunk,
)


class TestDocument:
    def test_minimal_document(self) -> None:
        doc = Document(text="hello", metadata={"source": "a.pdf", "page": "1"})
        assert doc.text == "hello"

    def test_empty_text_allowed(self) -> None:
        doc = Document(text="", metadata={})
        assert doc.text == ""

    def test_metadata_is_dict(self) -> None:
        doc = Document(text="x", metadata={"key": "val"})
        assert doc.metadata["key"] == "val"


class TestChunk:
    def test_chunk_with_parent_index(self) -> None:
        c = Chunk(text="chunk", chunk_index=0, parent_chunk_index=5, metadata={})
        assert c.parent_chunk_index == 5

    def test_chunk_without_parent_index(self) -> None:
        c = Chunk(text="chunk", chunk_index=0, metadata={})
        assert c.parent_chunk_index is None

    def test_chunk_index_preserved(self) -> None:
        c = Chunk(text="t", chunk_index=42, metadata={})
        assert c.chunk_index == 42


class TestTriplet:
    def test_fields(self) -> None:
        t = Triplet(
            subject="Customer",
            predicate="has",
            object="Email",
            provenance_text="Customers have emails.",
            confidence=0.9,
        )
        assert t.subject == "Customer"
        assert t.predicate == "has"
        assert t.object == "Email"

    def test_extraction_response(self) -> None:
        t = Triplet(
            subject="A", predicate="r", object="B",
            provenance_text="A relates to B.",
            confidence=0.8,
        )
        resp = TripletExtractionResponse(triplets=[t])
        assert len(resp.triplets) == 1

    def test_confidence_bounds(self) -> None:
        with pytest.raises(ValueError):
            Triplet(
                subject="X", predicate="y", object="Z",
                provenance_text="text", confidence=1.5,
            )
        with pytest.raises(ValueError):
            Triplet(
                subject="X", predicate="y", object="Z",
                provenance_text="text", confidence=-0.1,
            )


class TestGraderDecision:
    def test_accept(self) -> None:
        d = GraderDecision(grounded=True, action="pass")
        assert d.grounded is True
        assert d.action == "pass"

    def test_reject(self) -> None:
        d = GraderDecision(grounded=False, action="regenerate", critique="hallucinated")
        assert d.grounded is False
        assert d.action == "regenerate"

    def test_invalid_action_raises(self) -> None:
        with pytest.raises(ValueError):
            GraderDecision(grounded=True, action="invalid")


class TestRetrievedChunk:
    def test_score(self) -> None:
        rc = RetrievedChunk(
            node_id="n1",
            node_type="Chunk",
            text="data",
            score=0.95,
            source_type="vector",
            metadata={"source": "doc.pdf"},
        )
        assert rc.score == 0.95
        assert rc.node_id == "n1"

    def test_invalid_source_type_raises(self) -> None:
        with pytest.raises(ValueError):
            RetrievedChunk(
                node_id="n1",
                node_type="Chunk",
                text="data",
                score=0.5,
                source_type="invalid",
            )


class TestApiModelsValidation:
    """Mutation-style validation for API request/response models."""

    def test_defaults(self) -> None:
        from src.api.models import PipelineConfig

        cfg = PipelineConfig()
        assert cfg.chunk_size == 256
        assert cfg.retrieval_mode == "hybrid"

    def test_temperature_upper_bound(self) -> None:
        from src.api.models import PipelineConfig

        cfg = PipelineConfig(temperature_extraction=2.0)
        assert cfg.temperature_extraction == 2.0
        with pytest.raises(ValueError):
            PipelineConfig(temperature_extraction=2.1)

    def test_temperature_negative(self) -> None:
        from src.api.models import PipelineConfig

        with pytest.raises(ValueError):
            PipelineConfig(temperature_extraction=-0.1)

    def test_max_tokens_below_min(self) -> None:
        from src.api.models import PipelineConfig

        with pytest.raises(ValueError):
            PipelineConfig(max_tokens_extraction=100)

    def test_max_tokens_above_max(self) -> None:
        from src.api.models import PipelineConfig

        with pytest.raises(ValueError):
            PipelineConfig(max_tokens_extraction=99999)

    def test_invalid_retrieval_mode(self) -> None:
        from src.api.models import PipelineConfig

        with pytest.raises(ValueError):
            PipelineConfig(retrieval_mode="invalid_mode")

    def test_vector_top_k_bounds(self) -> None:
        from src.api.models import PipelineConfig

        with pytest.raises(ValueError):
            PipelineConfig(retrieval_vector_top_k=0)
        with pytest.raises(ValueError):
            PipelineConfig(retrieval_vector_top_k=200)
