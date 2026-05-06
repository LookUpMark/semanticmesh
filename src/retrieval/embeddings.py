"""Embedding model singleton — shared encoder for entity blocking and retrieval.

Supports three backends:
- **OpenAI** (``text-embedding-3-large``, ``text-embedding-3-small``): cloud API,
  uses ``settings.openai_api_key``.  Dimension is controlled by
  ``settings.embedding_dimensions`` (default 1024, matches Neo4j vector index).
- **LM Studio** (``lmstudio/<model>``): OpenAI-compatible local server,
  uses ``settings.lmstudio_base_url``.
- **BGE-M3** (``BAAI/bge-m3``): local FlagEmbedding model. Uses GPU (``cuda:0``)
  if available, falls back to CPU automatically.

The active backend is auto-detected from ``settings.embedding_model``:
- starts with ``text-embedding-`` → OpenAI
- starts with ``lmstudio/`` → LM Studio (OpenAI-compatible)
- anything else → BGE-M3 (FlagEmbedding)
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

logger: logging.Logger = get_logger(__name__)


class _OpenAIEmbedder:
    """Thin wrapper around OpenAI Embeddings API matching the FlagModel `.encode()` interface."""

    def __init__(self, model_name: str, dimensions: int = 1024) -> None:
        from openai import OpenAI  # noqa: PLC0415

        api_key = get_settings().openai_api_key.get_secret_value()
        self._client = OpenAI(api_key=api_key)
        self._model = model_name
        self._dimensions = dimensions

    def encode(self, texts: list[str], batch_size: int = 32, **_kwargs) -> np.ndarray:
        """Embed *texts* in batches; returns (N, dimensions) float32 ndarray."""
        results: list[list[float]] = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            resp = self._client.embeddings.create(
                input=batch,
                model=self._model,
                dimensions=self._dimensions,
            )
            results.extend([e.embedding for e in resp.data])
        return np.array(results, dtype=np.float32)


class _LMStudioEmbedder:
    """OpenAI-compatible embedder forwarding requests to a local LM Studio server."""

    def __init__(self, model_name: str) -> None:
        from openai import OpenAI  # noqa: PLC0415

        base_url: str = get_settings().lmstudio_base_url
        self._client = OpenAI(api_key=LMSTUDIO_PLACEHOLDER_KEY, base_url=base_url)
        self._model = model_name

    def encode(self, texts: list[str], batch_size: int = 32, **_kwargs) -> np.ndarray:
        """Embed *texts* in batches via LM Studio; returns (N, dim) float32 ndarray."""
        results: list[list[float]] = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            resp = self._client.embeddings.create(input=batch, model=self._model)
            results.extend([e.embedding for e in resp.data])
        return np.array(results, dtype=np.float32)


@lru_cache(maxsize=1)
def get_embeddings():
    """Return the singleton embedder instance.

    Backend is determined by ``settings.embedding_model``:
    - ``text-embedding-*`` → :class:`_OpenAIEmbedder` (OpenAI Embeddings API)
    - everything else → ``FlagEmbedding.FlagModel`` (BGE-M3, CPU)

    Returns:
        An object with an ``.encode(texts, batch_size)`` → ndarray interface.
    """
    settings = get_settings()
    model_name: str = settings.embedding_model

    if model_name.startswith("text-embedding"):
        dims: int = getattr(settings, "embedding_dimensions", 1024)
        logger.info("Using OpenAI embedding model '%s' (dimensions=%d).", model_name, dims)
        return _OpenAIEmbedder(model_name, dimensions=dims)

    if model_name.startswith("lmstudio/"):
        bare = model_name[len("lmstudio/") :]
        logger.info("Using LM Studio embedding model '%s'.", bare)
        return _LMStudioEmbedder(bare)

    # Fallback: local BGE-M3
    try:
        from FlagEmbedding import FlagModel  # noqa: PLC0415
    except ImportError as exc:
        raise ImportError("FlagEmbedding is not installed. Run: pip install FlagEmbedding") from exc

    import torch  # noqa: PLC0415

    _cuda = torch.cuda.is_available()
    _device = "cuda:0" if _cuda else "cpu"
    _fp16 = _cuda
    logger.info("Loading embedding model '%s' on %s...", model_name, _device.upper())
    model = FlagModel(
        model_name,
        use_fp16=_fp16,
        query_instruction_for_retrieval="Represent this sentence for retrieval: ",
        devices=[_device],
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
        model: Optional pre-loaded embedder; if None, calls ``get_embeddings()``.

    Returns:
        A list of float vectors (one per input string).
    """
    if not texts:
        return []
    if model is None:
        model = get_embeddings()
    embeddings = model.encode(texts, batch_size=get_settings().embedding_batch_size)
    return embeddings.tolist()


def embed_text(text: str, model=None) -> list[float]:
    """Encode a single string into a dense vector.

    Args:
        text:  The string to embed.
        model: Optional pre-loaded model; if None, calls ``get_embeddings()``.

    Returns:
        A float list.
    """
    return embed_texts([text], model=model)[0]
