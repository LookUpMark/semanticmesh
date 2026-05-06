"""Cross-encoder reranker — BAAI/bge-reranker-v2-m3.

EP-13 / US-13-01: Jointly scores (query, chunk) pairs and returns the
top_k most relevant chunks for the answer generator.
"""

from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING

import numpy as np

from src.config.config import LMSTUDIO_PLACEHOLDER_KEY
from src.config.logging import get_logger
from src.config.settings import get_settings

if TYPE_CHECKING:
    import logging

    from src.models.schemas import RetrievedChunk

logger: logging.Logger = get_logger(__name__)


class _LMStudioReranker:
    """Cosine-similarity reranker that uses LM Studio's embedding endpoint.

    Scores each (query, doc) pair by computing the cosine similarity between
    their dense embeddings produced by the embedding model loaded in LM Studio.
    This is a bi-encoder approximation of cross-encoder reranking, suitable when
    the FlagReranker local model is unavailable.
    """

    def __init__(self, client, model: str) -> None:
        self._client = client
        self._model = model

    def _embed(self, texts: list[str], batch_size: int = 32) -> np.ndarray:
        results: list[list[float]] = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            resp = self._client.embeddings.create(input=batch, model=self._model)
            results.extend([e.embedding for e in resp.data])
        return np.array(results, dtype=np.float32)

    def compute_score(self, pairs: list[tuple[str, str]], **_kwargs) -> list[float]:
        queries = [p[0] for p in pairs]
        docs = [p[1] for p in pairs]
        q_embs = self._embed(queries)
        d_embs = self._embed(docs)
        q_norm = q_embs / (np.linalg.norm(q_embs, axis=1, keepdims=True) + 1e-9)
        d_norm = d_embs / (np.linalg.norm(d_embs, axis=1, keepdims=True) + 1e-9)
        return (q_norm * d_norm).sum(axis=1).tolist()


@lru_cache(maxsize=1)
def get_reranker():
    """Return the singleton reranker instance.

    Backend is determined by ``settings.reranker_model``:
    - ``lmstudio/<model>`` → :class:`_LMStudioReranker` (cosine-similarity via LM Studio)
    - everything else → ``FlagEmbedding.FlagReranker`` (cross-encoder, local PyTorch)

    Returns:
        An object with a ``.compute_score(pairs, ...)`` → list[float] interface.

    Raises:
        ImportError: If ``FlagEmbedding`` is not installed (local path only).
    """
    settings = get_settings()
    model_name: str = settings.reranker_model

    if model_name.startswith("lmstudio/"):
        from openai import OpenAI  # noqa: PLC0415

        # Use the embedding model name from settings (already stripped by _LMStudioEmbedder logic)
        emb_model = settings.embedding_model
        if emb_model.startswith("lmstudio/"):
            emb_model = emb_model[len("lmstudio/"):]
        base_url: str = settings.lmstudio_base_url
        logger.info("Using LM Studio reranker (cosine similarity via '%s').", emb_model)
        return _LMStudioReranker(client=OpenAI(api_key=LMSTUDIO_PLACEHOLDER_KEY, base_url=base_url), model=emb_model)

    try:
        from FlagEmbedding import FlagReranker
    except ImportError as exc:
        raise ImportError("FlagEmbedding is not installed. Run: pip install FlagEmbedding") from exc

    import torch  # noqa: PLC0415

    _cuda = torch.cuda.is_available()
    _device = "cuda:0" if _cuda else "cpu"
    _fp16 = _cuda
    logger.info("Loading reranker model '%s' on %s...", model_name, _device.upper())
    reranker = FlagReranker(model_name, use_fp16=_fp16, device=_device)
    reranker.target_devices = [_device]
    logger.info("Reranker model loaded.")
    return reranker


def _enrich_text_for_reranking(chunk: RetrievedChunk) -> str:
    """Enrich short chunk texts for better cross-encoder scoring.

    Short BC/graph chunks (e.g. "Customer Master: Primary record...")  get low
    reranker scores because there's not enough text. Prepend context info.
    """
    settings = get_settings()
    text = chunk.text
    if len(text) < settings.reranker_short_text_threshold and chunk.node_type not in ("ParentChunk", "Chunk"):
        prefix_parts: list[str] = []
        if chunk.node_type and chunk.node_type != "Unknown":
            prefix_parts.append(chunk.node_type)
        if chunk.node_id and chunk.node_id != text:
            prefix_parts.append(chunk.node_id)
        rel = chunk.metadata.get("rel_type") if chunk.metadata else None
        if rel:
            prefix_parts.append(f"relationship: {rel}")
        if prefix_parts:
            text = f"[{' | '.join(prefix_parts)}] {text}"
    return text


def rerank(
    query: str,
    chunks: list[RetrievedChunk],
    reranker=None,
    top_k: int | None = None,
) -> list[RetrievedChunk]:
    """Score and rerank retrieved chunks using the cross-encoder.

    Each ``(query, chunk.text)`` pair is scored jointly by ``bge-reranker-v2-m3``.
    Scores are stored in ``chunk.metadata["reranker_score"]`` and the chunk
    ``.score`` field is updated. The list is sorted descending and sliced to
    ``top_k``.

    If ``chunks`` is empty the function returns immediately without loading the
    model. If the reranker call fails, a warning is logged and the input chunks
    are returned in their original order (graceful degradation).

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

    pairs: list[tuple[str, str]] = [(query, _enrich_text_for_reranking(chunk)) for chunk in valid_chunks]

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

    # Rank-based confidence floor: the top chunk being #1 in a competitive pool
    # is itself strong evidence of relevance even when cross-encoder absolute
    # scores are low (common with short BC definitions or markdown tables).
    # Linear interpolation: pool=3 → floor 0.40, pool≥10 → floor 0.55.
    if len(valid_chunks) >= 3:
        pool_size = len(valid_chunks)
        settings = get_settings()
        w_rerank = settings.reranker_weight_rerank
        w_vector = settings.reranker_weight_vector
        w_bm25 = settings.reranker_weight_bm25
        w_graph = settings.reranker_weight_graph
        pool_floor = min(w_vector, w_rerank + (pool_size - 3) * (w_vector - w_rerank) / (10 - 3))
        for i, chunk in enumerate(reranked[:5]):
            floor = max(pool_floor - i * w_bm25, w_graph)
            if chunk.score < floor:
                reranked[i] = chunk.model_copy(
                    update={
                        "score": floor,
                        "metadata": {**chunk.metadata, "reranker_score": chunk.score, "score_floored_from": chunk.score},
                    },
                )

    logger.info(
        "rerank: top chunk '%s' score=%.4f (pool=%d, top_k=%d).",
        reranked[0].node_id if reranked else "N/A",
        reranked[0].score if reranked else 0.0,
        len(valid_chunks),
        k,
    )
    return reranked
