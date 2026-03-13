# Part 7 — `src/retrieval/reranker.py`

## 1. Purpose & Context

**Epic:** EP-13 Cross-Encoder Reranking  
**US-13-01** — Cross-Encoder Reranking Node

After the hybrid retriever produces a merged candidate pool, the cross-encoder jointly scores every `(query, chunk)` pair using `BAAI/bge-reranker-large`. Unlike the bi-encoder used for retrieval, the cross-encoder reads both texts together and produces a single relevance score — substantially more accurate for identifying information-dense chunks.

The reranker is the last filter before the answer generator. Its output directly determines what the LLM sees.

---

## 2. Prerequisites

- `src/models/schemas.py` — `RetrievedChunk` (step 5)
- `FlagEmbedding` package — `FlagReranker` class (`pip install FlagEmbedding`)
- `src/config/settings.py` — `reranker_top_k`, `reranker_model` (step 2)
- `src/config/logging.py` — `get_logger`

---

## 3. Public API

| Symbol | Signature | Description |
|---|---|---|
| `get_reranker` | `() -> FlagReranker` | Cached singleton reranker loader |
| `rerank` | `(query: str, chunks: list[RetrievedChunk], reranker=None, top_k=None) -> list[RetrievedChunk]` | Score all pairs, sort, slice to top_k |

---

## 4. Full Implementation

```python
"""Cross-encoder reranker — BAAI/bge-reranker-large.

EP-13 / US-13-01: Jointly scores (query, chunk) pairs and returns the
top_k most relevant chunks for the answer generator.
"""

from __future__ import annotations

import logging
from functools import lru_cache

from src.config.logging import get_logger
from src.config.settings import get_settings
from src.models.schemas import RetrievedChunk

logger: logging.Logger = get_logger(__name__)


@lru_cache(maxsize=1)
def get_reranker():
    """Return the singleton FlagReranker instance, loaded on CPU.

    The model is loaded from ``settings.reranker_model`` (default
    ``"BAAI/bge-reranker-large"``).  Always runs on CPU regardless of GPU
    availability.

    **CUDA guard:** ``FlagReranker.__init__`` probes CUDA during initialization
    even when ``device="cpu"`` is specified, which triggers OOM errors when GPU
    VRAM is already occupied (e.g., by an LM Studio model loaded in the same
    session).  To prevent this, ``CUDA_VISIBLE_DEVICES`` is temporarily set to
    ``""`` (hiding all GPUs) for the duration of model initialization, then
    restored to its original value immediately afterward.

    Returns:
        A ``FlagEmbedding.FlagReranker`` instance ready for ``.compute_score()``.
    """
    import os

    try:
        from FlagEmbedding import FlagReranker
    except ImportError as exc:
        raise ImportError(
            "FlagEmbedding is not installed. Run: pip install FlagEmbedding"
        ) from exc

    settings = get_settings()
    model_name: str = settings.reranker_model
    logger.info("Loading reranker model '%s'...", model_name)

    old_cuda = os.environ.get("CUDA_VISIBLE_DEVICES")
    os.environ["CUDA_VISIBLE_DEVICES"] = ""
    try:
        model = FlagReranker(model_name, use_fp16=False, device="cpu")
    finally:
        if old_cuda is None:
            os.environ.pop("CUDA_VISIBLE_DEVICES", None)
        else:
            os.environ["CUDA_VISIBLE_DEVICES"] = old_cuda

    logger.info("Reranker model loaded.")
    return model


def rerank(
    query: str,
    chunks: list[RetrievedChunk],
    reranker=None,
    top_k: int | None = None,
) -> list[RetrievedChunk]:
    """Score and rerank retrieved chunks using the cross-encoder.

    Each ``(query, chunk.text)`` pair is scored jointly by `bge-reranker-large`.
    Scores are stored in ``chunk.metadata["reranker_score"]`` and the list is
    sorted descending.  The top ``top_k`` chunks are returned.

    If ``chunks`` is empty the function returns immediately without loading the
    model.  If the reranker call fails (e.g., OOM), a warning is logged and the
    input chunks are returned in their original order (graceful degradation).

    Args:
        query:    Natural language query string.
        chunks:   Merged candidate ``RetrievedChunk`` list from hybrid retriever.
        reranker: Optional pre-loaded ``FlagReranker``; if None, calls ``get_reranker()``.
        top_k:    Slice size; defaults to ``settings.reranker_top_k``.

    Returns:
        Reranked ``RetrievedChunk`` list (length ≤ ``top_k``), sorted by reranker score desc.
    """
    settings = get_settings()
    k: int = top_k if top_k is not None else settings.reranker_top_k

    if not chunks:
        return []

    if reranker is None:
        reranker = get_reranker()

    pairs: list[tuple[str, str]] = [(query, chunk.text) for chunk in chunks]

    try:
        scores: list[float] = reranker.compute_score(pairs, normalize=True)
    except Exception as exc:
        logger.warning(
            "Reranker scoring failed (%s) — returning chunks unranked.", exc
        )
        return chunks[:k]

    # Attach reranker_score to each chunk's metadata
    scored: list[RetrievedChunk] = []
    for chunk, score in zip(chunks, scores):
        updated_metadata = {**chunk.metadata, "reranker_score": float(score)}
        scored.append(chunk.model_copy(update={"metadata": updated_metadata, "score": float(score)}))

    reranked = sorted(scored, key=lambda c: c.score, reverse=True)[:k]
    logger.info(
        "rerank: top chunk '%s' score=%.4f (pool=%d, top_k=%d).",
        reranked[0].node_id if reranked else "N/A",
        reranked[0].score if reranked else 0.0,
        len(chunks), k,
    )
    return reranked
```

---

## 5. Tests

```python
"""Unit tests for src/retrieval/reranker.py — UT-20"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from src.models.schemas import RetrievedChunk
from src.retrieval.reranker import rerank


# ── Helpers ────────────────────────────────────────────────────────────────────

def _chunk(name: str, score: float = 0.5) -> RetrievedChunk:
    return RetrievedChunk(
        node_id=name, node_type="BusinessConcept",
        text=f"{name}: some definition text",
        score=score, source_type="vector", metadata={},
    )


def _make_reranker(scores: list[float]) -> MagicMock:
    reranker = MagicMock()
    reranker.compute_score.return_value = scores
    return reranker


# ── rerank ────────────────────────────────────────────────────────────────────

class TestRerank:
    def test_empty_chunks_returns_empty(self) -> None:
        result = rerank("query", [], reranker=MagicMock(), top_k=5)
        assert result == []

    def test_sorted_descending_by_score(self) -> None:
        chunks = [_chunk("A"), _chunk("B"), _chunk("C")]
        reranker = _make_reranker([0.3, 0.9, 0.6])
        result = rerank("query", chunks, reranker=reranker, top_k=3)
        assert result[0].node_id == "B"
        assert result[1].node_id == "C"
        assert result[2].node_id == "A"

    def test_top_k_slices_results(self) -> None:
        chunks = [_chunk(f"N{i}") for i in range(10)]
        scores = [float(i) / 10 for i in range(10)]
        reranker = _make_reranker(scores)
        result = rerank("query", chunks, reranker=reranker, top_k=3)
        assert len(result) == 3

    def test_reranker_score_stored_in_metadata(self) -> None:
        chunks = [_chunk("X"), _chunk("Y")]
        reranker = _make_reranker([0.8, 0.4])
        result = rerank("query", chunks, reranker=reranker, top_k=2)
        assert "reranker_score" in result[0].metadata
        assert result[0].metadata["reranker_score"] == pytest.approx(0.8)

    def test_reranker_failure_returns_unranked(self) -> None:
        chunks = [_chunk("A"), _chunk("B")]
        reranker = MagicMock()
        reranker.compute_score.side_effect = RuntimeError("OOM")
        result = rerank("query", chunks, reranker=reranker, top_k=5)
        # Should not raise; returns original order
        assert len(result) == 2

    def test_scores_attached_as_new_score(self) -> None:
        chunks = [_chunk("Z", score=0.1)]
        reranker = _make_reranker([0.99])
        result = rerank("query", chunks, reranker=reranker, top_k=1)
        # score field is updated to reranker score
        assert result[0].score == pytest.approx(0.99)

    def test_pairs_passed_to_compute_score(self) -> None:
        chunks = [_chunk("Customer"), _chunk("Product")]
        reranker = _make_reranker([0.7, 0.5])
        rerank("what is a customer?", chunks, reranker=reranker, top_k=2)
        call_args = reranker.compute_score.call_args[0][0]
        assert call_args[0] == ("what is a customer?", "Customer: some definition text")
        assert call_args[1] == ("what is a customer?", "Product: some definition text")
```

---

## 6. Smoke Test

```bash
python -c "
from src.retrieval.reranker import rerank
from src.models.schemas import RetrievedChunk
from unittest.mock import MagicMock

chunks = [
    RetrievedChunk(node_id='Customer', node_type='BusinessConcept', text='Customer: buys products', score=0.5, source_type='vector', metadata={}),
    RetrievedChunk(node_id='Product',  node_type='BusinessConcept', text='Product: sellable item',  score=0.6, source_type='bm25',   metadata={}),
]
reranker = MagicMock()
reranker.compute_score.return_value = [0.95, 0.40]

result = rerank('who are our customers?', chunks, reranker=reranker, top_k=2)
print('Top chunk:', result[0].node_id, 'score:', result[0].score)
print('reranker smoke test passed.')
"
```
