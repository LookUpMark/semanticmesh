"""Unit tests for src/extraction/triplet_extractor.py — UT-04"""

from __future__ import annotations

import json
from unittest.mock import MagicMock

from src.extraction.triplet_extractor import extract_all_triplets, extract_triplets
from src.models.schemas import Chunk

# ── Fixtures ───────────────────────────────────────────────────────────────────


def _make_chunk(text: str = "A Customer purchases Products.", index: int = 0) -> Chunk:
    return Chunk(
        text=text,
        chunk_index=index,
        metadata={"source": "test.pdf", "page": "1", "token_count": "10"},
    )


def _make_llm(triplets_payload: list[dict]) -> MagicMock:
    """Return a mock LLM that yields the given triplets as JSON."""
    llm = MagicMock()
    response = MagicMock()
    response.content = json.dumps({"triplets": triplets_payload})
    llm.invoke.return_value = response
    return llm


VALID_TRIPLET = {
    "subject": "Customer",
    "predicate": "purchases",
    "object": "Product",
    "provenance_text": "A Customer purchases Products.",
    "confidence": 0.95,
}


# ── extract_triplets ──────────────────────────────────────────────────────────


class TestExtractTriplets:
    def test_happy_path_returns_triplets(self) -> None:
        chunk = _make_chunk()
        llm = _make_llm([VALID_TRIPLET])
        result = extract_triplets(chunk, llm)
        assert len(result) == 1
        assert result[0].subject == "Customer"

    def test_source_chunk_index_set(self) -> None:
        chunk = _make_chunk(index=7)
        llm = _make_llm([VALID_TRIPLET])
        result = extract_triplets(chunk, llm)
        assert result[0].source_chunk_index == 7

    def test_empty_triplets_list_from_llm(self) -> None:
        chunk = _make_chunk()
        llm = _make_llm([])
        result = extract_triplets(chunk, llm)
        assert result == []

    def test_llm_error_returns_empty_list(self) -> None:
        chunk = _make_chunk()
        llm = MagicMock()
        llm.invoke.side_effect = RuntimeError("timeout")
        result = extract_triplets(chunk, llm)
        assert result == []

    def test_invalid_json_returns_empty_list(self) -> None:
        chunk = _make_chunk()
        llm = MagicMock()
        resp = MagicMock()
        resp.content = "I cannot extract triplets from this text."
        llm.invoke.return_value = resp
        result = extract_triplets(chunk, llm)
        assert result == []

    def test_pydantic_validation_error_returns_empty(self) -> None:
        """Confidence > 1.0 should fail Pydantic validation."""
        chunk = _make_chunk()
        bad_triplet = {**VALID_TRIPLET, "confidence": 2.5}  # invalid
        llm = _make_llm([bad_triplet])
        result = extract_triplets(chunk, llm)
        assert result == []

    def test_multiple_triplets_returned(self) -> None:
        triplet2 = {**VALID_TRIPLET, "subject": "Product", "predicate": "has", "object": "Price"}
        chunk = _make_chunk()
        llm = _make_llm([VALID_TRIPLET, triplet2])
        result = extract_triplets(chunk, llm)
        assert len(result) == 2


# ── extract_all_triplets ──────────────────────────────────────────────────────


class TestExtractAllTriplets:
    def test_empty_chunks_returns_empty(self) -> None:
        llm = _make_llm([])
        assert extract_all_triplets([], llm) == []

    def test_flattens_across_chunks(self) -> None:
        chunks = [_make_chunk(index=i, text=f"Fact {i}.") for i in range(3)]
        llm = _make_llm([VALID_TRIPLET])
        result = extract_all_triplets(chunks, llm)
        assert len(result) == 3  # 1 triplet per chunk × 3 chunks

    def test_one_failing_chunk_does_not_stop_others(self) -> None:
        chunks = [_make_chunk(index=i) for i in range(3)]

        call_count = 0

        def side_effect(messages):
            nonlocal call_count
            call_count += 1
            if call_count == 2:
                raise RuntimeError("timeout on chunk 1")
            resp = MagicMock()
            resp.content = json.dumps({"triplets": [VALID_TRIPLET]})
            return resp

        llm = MagicMock()
        llm.invoke.side_effect = side_effect
        result = extract_all_triplets(chunks, llm)
        # chunks 0 and 2 succeed → 2 triplets
        assert len(result) == 2

    def test_parallel_max_workers_override(self) -> None:
        """max_workers kwarg is accepted and results are still correct."""
        chunks = [_make_chunk(index=i, text=f"Fact {i}.") for i in range(5)]
        llm = _make_llm([VALID_TRIPLET])
        result = extract_all_triplets(chunks, llm, max_workers=3)
        assert len(result) == 5  # 1 triplet per chunk × 5 chunks

    def test_results_in_chunk_order(self) -> None:
        """Triplets are returned in chunk index order regardless of completion order."""
        import threading
        chunks = [_make_chunk(index=i, text=f"Fact {i}.") for i in range(4)]
        lock = threading.Lock()
        completion_order: list[int] = []

        def side_effect(messages):
            # Find chunk index from message content
            content = messages[1].content
            idx = next(
                (c.chunk_index for c in chunks if f"Fact {c.chunk_index}." in content),
                0,
            )
            with lock:
                completion_order.append(idx)
            resp = MagicMock()
            resp.content = json.dumps({"triplets": [
                {**VALID_TRIPLET, "subject": f"Entity{idx}"}
            ]})
            return resp

        llm = MagicMock()
        llm.invoke.side_effect = side_effect
        result = extract_all_triplets(chunks, llm, max_workers=4)
        # subjects should come out in chunk order: Entity0, Entity1, Entity2, Entity3
        subjects = [t.subject for t in result]
        assert subjects == ["Entity0", "Entity1", "Entity2", "Entity3"]
