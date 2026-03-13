# Part 4 — `src/extraction/triplet_extractor.py`

## 1. Purpose & Context

**Epic:** EP-03 SLM Triplet Extraction  
**US-03-01** — Triplet Extraction Node

Uses a Small Language Model (SLM) in JSON mode to extract `(subject, predicate, object, provenance_text, confidence)` triplets from each text chunk. The SLM is called per-chunk at `temperature=0.0`. On JSON parse failure or Pydantic `ValidationError`, the extractor triggers a self-reflection retry via `REFLECTION_TEMPLATE` (PT-05) up to `max_reflection_attempts` times (default 3) before returning `[]` — never crashing the pipeline.

---

## 2. Prerequisites

- `src/models/schemas.py` — `Chunk`, `Triplet`, `TripletExtractionResponse` (step 3)
- `src/prompts/templates.py` — `EXTRACTION_SYSTEM`, `EXTRACTION_USER`, `REFLECTION_TEMPLATE` (step 7)
- `src/config/llm_factory.py` — `get_extraction_llm` (step 4)
- `src/config/logging.py` — `get_logger`, `NodeTimer`
- `src/config/settings.py` — `get_settings`

---

## 3. Public API

| Symbol | Signature | Description |
|---|---|---|
| `extract_triplets` | `(chunk: Chunk, llm: LLMProtocol) -> list[Triplet]` | Extract triplets from a single chunk; returns `[]` on failure |
| `extract_all_triplets` | `(chunks: list[Chunk], llm: LLMProtocol) -> list[Triplet]` | Batch extraction across all chunks |

---

## 4. Full Implementation

```python
"""SLM Triplet Extraction node.

EP-03: Calls a Small Language Model in JSON mode to extract
(subject, predicate, object, provenance_text, confidence) triplets
from each text chunk. Validates with Pydantic; gracefully returns []
on any parsing failure.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import ValidationError

from src.config.logging import NodeTimer, get_logger
from src.config.settings import get_settings
from src.models.schemas import Chunk, Triplet, TripletExtractionResponse
from src.prompts.templates import EXTRACTION_SYSTEM, EXTRACTION_USER, REFLECTION_TEMPLATE

if TYPE_CHECKING:
    import logging

    from src.config.llm_client import LLMProtocol

logger: logging.Logger = get_logger(__name__)


def _reflect_on_json(
    raw_json: str,
    error: str,
    llm: "LLMProtocol",
) -> str:
    """Ask the LLM to self-correct a malformed JSON extraction output.

    Uses ``REFLECTION_TEMPLATE`` (PT-05) to inject the original raw response
    and the parse/validation error, requesting a corrected JSON string.

    Args:
        raw_json: The original (broken) LLM output string.
        error:    The ``json.JSONDecodeError`` or ``ValidationError`` message.
        llm:      Extraction LLM instance.

    Returns:
        Corrected raw JSON string from the LLM.
    """
    reflection_prompt = REFLECTION_TEMPLATE.format(
        role="strict information extraction engine",
        output_format="JSON object matching {\"triplets\": [...]}",
        error_or_critique=error,
        original_input=raw_json,
    )
    response = llm.invoke([HumanMessage(content=reflection_prompt)])
    content = response.content
    return content.strip() if isinstance(content, str) else ""


def extract_triplets(chunk: Chunk, llm: LLMProtocol) -> list[Triplet]:
    """Extract semantic triplets from a single text chunk using the SLM.

    Args:
        chunk: A ``Chunk`` object from the PDF/chunking pipeline.
        llm: A LLMProtocol instance configured for extraction (temperature=0.0).
             Use ``get_extraction_llm()`` from the factory.

    Returns:
        List of validated ``Triplet`` objects.  Empty list on any failure
        (LLM error, JSON decode error, Pydantic ValidationError).
    """
    user_prompt = EXTRACTION_USER.format(chunk_text=chunk.text)

    with NodeTimer() as timer:
        try:
            response = llm.invoke(
                [
                    SystemMessage(content=EXTRACTION_SYSTEM),
                    HumanMessage(content=user_prompt),
                ]
            )
            # AIMessage.content can be str | list[str | dict[Any, Any]]
            content = response.content
            if not isinstance(content, str):
                logger.warning(
                    "LLM returned non-string content for chunk %d — returning empty triplet list.",
                    chunk.chunk_index,
                )
                return []
            raw_json: str = content.strip()
        except Exception as exc:
            logger.warning(
                "LLM call failed for chunk %d (source=%s): %s — returning empty triplet list.",
                chunk.chunk_index,
                chunk.metadata.get("source", "unknown"),
                exc,
            )
            return []

    logger.debug(
        "Extraction LLM call for chunk %d completed in %.0f ms",
        chunk.chunk_index,
        timer.elapsed_ms,
    )

    settings = get_settings()
    max_attempts: int = settings.max_reflection_attempts

    # Step 1: JSON parse (with self-reflection on failure)
    data: dict | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            data = json.loads(raw_json)
            break
        except json.JSONDecodeError as exc:
            logger.warning(
                "Non-JSON response for chunk %d (attempt %d/%d): %s. Raw response: %r",
                chunk.chunk_index,
                attempt,
                max_attempts,
                exc,
                raw_json[:200],
            )
            if attempt == max_attempts:
                return []
            raw_json = _reflect_on_json(raw_json, str(exc), llm)

    if data is None:
        return []

    # Step 2: Pydantic validation (with self-reflection on failure)
    parsed: TripletExtractionResponse | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            parsed = TripletExtractionResponse(**data)
            break
        except ValidationError as exc:
            logger.warning(
                "Pydantic validation failed for chunk %d (attempt %d/%d): %s",
                chunk.chunk_index,
                attempt,
                max_attempts,
                exc,
            )
            if attempt == max_attempts:
                return []
            raw_json = _reflect_on_json(json.dumps(data), str(exc), llm)
            try:
                data = json.loads(raw_json)
            except json.JSONDecodeError:
                return []

    if parsed is None:
        return []

    # Attach source chunk index to each triplet
    triplets = [
        t.model_copy(update={"source_chunk_index": chunk.chunk_index})
        for t in parsed.triplets
    ]

    logger.info(
        "Chunk %d → %d triplets extracted (source=%s, page=%s)",
        chunk.chunk_index,
        len(triplets),
        chunk.metadata.get("source", "unknown"),
        chunk.metadata.get("page", "?"),
    )
    return triplets


def extract_all_triplets(chunks: list[Chunk], llm: LLMProtocol) -> list[Triplet]:
    """Extract triplets from all chunks and flatten into a single list.

    Individual chunk failures are silently skipped (logged as warnings).

    Args:
        chunks: All text chunks from the PDF/chunking pipeline.
        llm: SLM instance (use ``get_extraction_llm()``).

    Returns:
        Flat list of all successfully extracted ``Triplet`` objects.
    """
    all_triplets: list[Triplet] = []
    for chunk in chunks:
        all_triplets.extend(extract_triplets(chunk, llm))

    logger.info(
        "Extracted %d total triplets from %d chunks.",
        len(all_triplets),
        len(chunks),
    )
    return all_triplets
```

---

## 5. Tests

```python
"""Unit tests for src/extraction/triplet_extractor.py — UT-04"""

from __future__ import annotations

import json
from unittest.mock import MagicMock

import pytest

from src.extraction.triplet_extractor import extract_all_triplets, extract_triplets
from src.models.schemas import Chunk, Triplet

# ── Fixtures ───────────────────────────────────────────────────────────────────

def _make_chunk(text: str = "A Customer purchases Products.", index: int = 0) -> Chunk:
    return Chunk(
        text=text,
        chunk_index=index,
        metadata={"source": "test.pdf", "page": 1, "token_count": 10},
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
```

---

## 6. Smoke Test

```bash
python -c "
from src.extraction.triplet_extractor import extract_triplets
from src.config.llm_factory import get_extraction_llm
from src.models.schemas import Chunk

llm = get_extraction_llm()
chunk = Chunk(
    text='A Customer is any individual who has purchased at least one product from the company.',
    chunk_index=0,
    metadata={'source': 'smoke_test', 'page': 1}
)
triplets = extract_triplets(chunk, llm)
for t in triplets:
    print(f'  ({t.subject}) --[{t.predicate}]--> ({t.object}) [{t.confidence:.2f}]')
"
```
