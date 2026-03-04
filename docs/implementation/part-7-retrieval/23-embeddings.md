# Part 7 — `src/retrieval/embeddings.py`

## 1. Purpose & Context

**Epic:** EP-12 Hybrid Retrieval  
**Supporting Infrastructure:** Shared embedding model singleton used across blocking, RAG mapping, and vector retrieval.

`embeddings.py` provides a single `@lru_cache`-memoised accessor that loads the `BAAI/bge-m3` (`FlagModel`) encoder exactly once per process. The model outputs 1024-dimensional dense vectors used for:

- Entity blocking cosine similarity (step 13)
- RAG mapper entity retrieval (step 16)
- Neo4j vector index population (step 19)
- Query-time dense retrieval (step 24)

---

## 2. Prerequisites

- `FlagEmbedding` package — `FlagModel` class (`pip install FlagEmbedding`)
- `src/config/settings.py` — `get_settings()` with `embedding_model` field (default `"BAAI/bge-m3"`) (step 2)
- `src/config/logging.py` — `get_logger`

---

## 3. Public API

| Symbol | Signature | Description |
|---|---|---|
| `get_embeddings` | `() -> FlagModel` | Cached singleton FlagModel loader |
| `embed_texts` | `(texts: list[str], model: FlagModel \| None) -> list[list[float]]` | Encode a list of strings → list of 1024-d vectors |
| `embed_text` | `(text: str, model: FlagModel \| None) -> list[float]` | Convenience wrapper for a single string |

---

## 4. Full Implementation

```python
"""Embedding model singleton — shared BGE-M3 encoder.

Loads BAAI/bge-m3 once via @lru_cache and exposes simple encode helpers.
Used across entity blocking, RAG mapping, vector indexing, and query retrieval.
"""

from __future__ import annotations

import logging
from functools import lru_cache

from src.config.logging import get_logger
from src.config.settings import get_settings

logger: logging.Logger = get_logger(__name__)


@lru_cache(maxsize=1)
def get_embeddings():
    """Return the singleton BGE-M3 FlagModel instance.

    The model is loaded from ``settings.embedding_model`` (default
    ``"BAAI/bge-m3"``).  Loading happens on the first call; subsequent calls
    return the cached object in O(1).

    Returns:
        A ``FlagEmbedding.FlagModel`` instance ready for ``.encode()``.
    """
    try:
        from FlagEmbedding import FlagModel
    except ImportError as exc:
        raise ImportError(
            "FlagEmbedding is not installed. Run: pip install FlagEmbedding"
        ) from exc

    settings = get_settings()
    model_name: str = settings.embedding_model
    logger.info("Loading embedding model '%s'...", model_name)
    model = FlagModel(
        model_name,
        use_fp16=True,        # halves VRAM usage; negligible accuracy loss
        query_instruction_for_retrieval="Represent this sentence for retrieval: ",
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
    """
    if not texts:
        return []
    if model is None:
        model = get_embeddings()
    embeddings = model.encode(texts, batch_size=32, show_progress_bar=False)
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
```

---

## 5. Tests

```python
"""Unit tests for src/retrieval/embeddings.py — UT-18"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest


class TestEmbedTexts:
    def _fake_model(self, dim: int = 1024) -> MagicMock:
        import numpy as np
        model = MagicMock()
        model.encode = MagicMock(
            side_effect=lambda texts, **kw: np.zeros((len(texts), dim), dtype="float32")
        )
        return model

    def test_returns_list_of_lists(self) -> None:
        from src.retrieval.embeddings import embed_texts
        model = self._fake_model()
        result = embed_texts(["hello", "world"], model=model)
        assert isinstance(result, list)
        assert len(result) == 2
        assert len(result[0]) == 1024

    def test_empty_input_returns_empty(self) -> None:
        from src.retrieval.embeddings import embed_texts
        result = embed_texts([], model=MagicMock())
        assert result == []

    def test_single_text(self) -> None:
        from src.retrieval.embeddings import embed_text
        model = self._fake_model()
        vec = embed_text("test sentence", model=model)
        assert isinstance(vec, list)
        assert len(vec) == 1024

    def test_calls_model_encode(self) -> None:
        from src.retrieval.embeddings import embed_texts
        model = self._fake_model()
        embed_texts(["a", "b", "c"], model=model)
        model.encode.assert_called_once()
        call_args = model.encode.call_args
        assert call_args[0][0] == ["a", "b", "c"]


class TestGetEmbeddings:
    def test_import_error_raises_helpful_message(self) -> None:
        import importlib
        import sys
        # Patch FlagEmbedding as unavailable
        with patch.dict(sys.modules, {"FlagEmbedding": None}):
            # Clear lru_cache
            from src.retrieval import embeddings as emb_mod
            emb_mod.get_embeddings.cache_clear()
            with pytest.raises(ImportError, match="FlagEmbedding"):
                emb_mod.get_embeddings()
            emb_mod.get_embeddings.cache_clear()
```

---

## 6. Smoke Test

```bash
python -c "
from src.retrieval.embeddings import embed_text
from unittest.mock import MagicMock
import numpy as np

# Mock model (avoids downloading BGE-M3 in CI)
model = MagicMock()
model.encode = lambda texts, **kw: np.zeros((len(texts), 1024), dtype='float32')

vec = embed_text('What is the customer table?', model=model)
print('Vector length:', len(vec))
print('Type:', type(vec[0]))
print('embed_text smoke test passed.')
"
```
