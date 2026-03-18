"""Embedding model singleton — shared BGE-M3 encoder.

Loads BAAI/bge-m3 once via @lru_cache and exposes simple encode helpers.
Used across entity blocking, RAG mapping, vector indexing, and query retrieval.

Embedding dimension: 1024 (required by the Neo4j vector index).
"""

from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING

from src.config.logging import get_logger
from src.config.settings import get_settings

if TYPE_CHECKING:
    import logging

logger: logging.Logger = get_logger(__name__)


@lru_cache(maxsize=1)
def get_embeddings():
    """Return the singleton BGE-M3 FlagModel instance.

    The model is loaded from ``settings.embedding_model`` (default
    ``"BAAI/bge-m3"``).  Loading happens on the first call; subsequent calls
    return the cached object in O(1).

    Returns:
        A ``FlagEmbedding.FlagModel`` instance ready for ``.encode()``.

    Raises:
        ImportError: If ``FlagEmbedding`` is not installed.
    """
    try:
        from FlagEmbedding import FlagModel
    except ImportError as exc:
        raise ImportError("FlagEmbedding is not installed. Run: pip install FlagEmbedding") from exc

    settings = get_settings()
    model_name: str = settings.embedding_model
    logger.info("Loading embedding model '%s' on CPU...", model_name)
    model = FlagModel(
        model_name,
        use_fp16=False,  # fp16 requires CUDA; use fp32 on CPU
        query_instruction_for_retrieval="Represent this sentence for retrieval: ",
        devices=["cpu"],
    )
    logger.info("Embedding model loaded.")
    return model


def embed_texts(
    texts: list[str],
    model=None,
) -> list[list[float]]:
    """Encode a list of strings into dense vectors.

    Args:
        texts: Non-empty list of strings to embed.
        model: Optional pre-loaded ``FlagModel``; if None, calls ``get_embeddings()``.

    Returns:
        A list of 1024-dimensional float vectors (one per input string).
        Returns an empty list when ``texts`` is empty.
    """
    if not texts:
        return []
    if model is None:
        model = get_embeddings()
    embeddings = model.encode(texts, batch_size=32)
    return embeddings.tolist()


def embed_text(text: str, model=None) -> list[float]:
    """Encode a single string into a dense vector.

    Args:
        text:  The string to embed.
        model: Optional pre-loaded model; if None, calls ``get_embeddings()``.

    Returns:
        A 1024-dimensional float list.
    """
    return embed_texts([text], model=model)[0]
