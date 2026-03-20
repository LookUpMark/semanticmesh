"""Cross-encoder reranker — BAAI/bge-reranker-large.

EP-13 / US-13-01: Jointly scores (query, chunk) pairs and returns the
top_k most relevant chunks for the answer generator.
"""

from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING

from src.config.logging import get_logger
from src.config.settings import get_settings

if TYPE_CHECKING:
    import logging

    from src.models.schemas import RetrievedChunk

logger: logging.Logger = get_logger(__name__)


@lru_cache(maxsize=1)
def get_reranker():
    """Return the singleton FlagReranker instance.

    The model is loaded from ``settings.reranker_model`` (default
    ``"BAAI/bge-reranker-large"``).  Runs on CPU if no GPU is available.

    Returns:
        A ``FlagEmbedding.FlagReranker`` instance ready for ``.compute_score()``.

    Raises:
        ImportError: If ``FlagEmbedding`` is not installed.
    """
    try:
        from FlagEmbedding import FlagReranker
    except ImportError as exc:
        raise ImportError("FlagEmbedding is not installed. Run: pip install FlagEmbedding") from exc

    settings = get_settings()
    model_name: str = settings.reranker_model
    logger.info("Loading reranker model '%s'...", model_name)
    # Temporarily hide CUDA devices during init so PyTorch doesn't try to
    # allocate GPU memory even when device="cpu" is requested.
    import os as _os

    _saved = _os.environ.get("CUDA_VISIBLE_DEVICES")
    _os.environ["CUDA_VISIBLE_DEVICES"] = ""
    try:
        reranker = FlagReranker(model_name, use_fp16=False, device="cpu")
        # FlagEmbedding can still infer empty/CUDA targets in some environments.
        # Force a deterministic single CPU target to avoid multi-process zero-device bugs.
        reranker.target_devices = ["cpu"]
    finally:
        if _saved is None:
            _os.environ.pop("CUDA_VISIBLE_DEVICES", None)
        else:
            _os.environ["CUDA_VISIBLE_DEVICES"] = _saved
    logger.info("Reranker model loaded.")
    return reranker


def rerank(
    query: str,
    chunks: list[RetrievedChunk],
    reranker=None,
    top_k: int | None = None,
) -> list[RetrievedChunk]:
    """Score and rerank retrieved chunks using the cross-encoder.

    Each ``(query, chunk.text)`` pair is scored jointly by ``bge-reranker-large``.
    Scores are stored in ``chunk.metadata["reranker_score"]`` and the chunk
    ``.score`` field is updated.  The list is sorted descending and sliced to
    ``top_k``.

    If ``chunks`` is empty the function returns immediately without loading the
    model.  If the reranker call fails (e.g., OOM), a warning is logged and the
    input chunks are returned in their original order (graceful degradation).

    Args:
        query:    Natural language query string.
        chunks:   Merged candidate ``RetrievedChunk`` list from hybrid retriever.
        reranker: Optional pre-loaded ``FlagReranker``; if None, calls ``get_reranker()``.
        top_k:    Slice size; defaults to ``settings.reranker_top_k``.

    Returns:
        Reranked ``RetrievedChunk`` list (length <= ``top_k``), sorted by score desc.
    """
    settings = get_settings()
    k: int = top_k if top_k is not None else settings.reranker_top_k

    if not chunks:
        return []

    valid_chunks = [c for c in chunks if c.node_id.strip() and c.text.strip()]
    if not valid_chunks:
        logger.warning("rerank: all chunks dropped as invalid (empty node_id/text).")
        return []
    if len(valid_chunks) < len(chunks):
        logger.info(
            "rerank: dropped %d invalid chunks before scoring.",
            len(chunks) - len(valid_chunks),
        )

    if reranker is None:
        reranker = get_reranker()

    pairs: list[tuple[str, str]] = [(query, chunk.text) for chunk in valid_chunks]

    try:
        scores: list[float] = reranker.compute_score(pairs, normalize=True)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Reranker scoring failed (%s) — returning chunks unranked.", exc)
        return valid_chunks[:k]

    scored: list[RetrievedChunk] = []
    for chunk, score in zip(valid_chunks, scores, strict=False):
        updated_meta = {**chunk.metadata, "reranker_score": float(score)}
        scored.append(chunk.model_copy(update={"metadata": updated_meta, "score": float(score)}))

    reranked = sorted(scored, key=lambda c: c.score, reverse=True)[:k]
    logger.info(
        "rerank: top chunk '%s' score=%.4f (pool=%d, top_k=%d).",
        reranked[0].node_id if reranked else "N/A",
        reranked[0].score if reranked else 0.0,
        len(valid_chunks),
        k,
    )
    return reranked
