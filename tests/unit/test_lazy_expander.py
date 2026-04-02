"""Unit tests for lazy query-time expansion helpers."""

from src.generation.lazy_expander import (
    collect_seed_names_for_expansion,
    should_trigger_lazy_expansion,
)
from src.models.schemas import RetrievedChunk


def _chunk(node_id: str) -> RetrievedChunk:
    return RetrievedChunk(
        node_id=node_id,
        node_type="BusinessConcept",
        text=node_id,
        score=0.1,
        source_type="graph",
        metadata={},
    )


def test_should_trigger_for_empty_chunks() -> None:
    assert should_trigger_lazy_expansion(top_score=0.9, chunk_count=0, threshold=0.4)


def test_should_trigger_for_low_score() -> None:
    assert should_trigger_lazy_expansion(top_score=0.2, chunk_count=3, threshold=0.4)


def test_collect_seed_names_unique_and_limited() -> None:
    chunks = [_chunk("A"), _chunk("B"), _chunk("A"), _chunk("C")]
    seeds = collect_seed_names_for_expansion(chunks, limit=2)
    assert seeds == ["A", "B"]
