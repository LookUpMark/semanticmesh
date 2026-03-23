"""SLM Triplet Extraction node.

EP-03: Calls a Small Language Model in JSON mode to extract
(subject, predicate, object, provenance_text, confidence) triplets
from each text chunk. Validates with Pydantic; gracefully returns []
on any parsing failure.
"""

from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import TYPE_CHECKING

from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import ValidationError

from src.config.logging import NodeTimer, get_logger
from src.config.settings import get_settings
from src.models.schemas import Chunk, Triplet, TripletExtractionResponse
from src.prompts.templates import EXTRACTION_SYSTEM, EXTRACTION_USER
from src.utils.json_utils import ReflectionResult, clean_json, reflect_on_json

if TYPE_CHECKING:
    import logging

    from src.config.llm_client import LLMProtocol

logger: logging.Logger = get_logger(__name__)


def _reflect_on_json(
    raw_json: str,
    error: str,
    llm: LLMProtocol,
    truncated: bool = False,
) -> str:
    """Ask the LLM to self-correct a malformed JSON extraction output.

    Wraps the shared ``reflect_on_json`` utility with triplet-specific
    role and output format.

    Args:
        raw_json:  The original (broken) LLM output string.
        error:     The ``json.JSONDecodeError`` or ``ValidationError`` message.
        llm:       Extraction LLM instance.
        truncated: Set to True when raw_json is empty (cap hit on first call).

    Returns:
        Corrected raw JSON string from the LLM, or empty string on failure.
    """
    result: ReflectionResult = reflect_on_json(
        llm=llm,
        error=error,
        original_input=raw_json,
        role="strict information extraction engine",
        output_format='JSON object matching {"triplets": [...]}',
        truncated=truncated,
    )
    return result["content"] if result["success"] else ""


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
            raw_json: str = clean_json(content)
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
            raw_json = _reflect_on_json(raw_json, str(exc), llm, truncated=(raw_json == ""))

    if data is None:
        return []

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

    triplets = [
        t.model_copy(update={"source_chunk_index": chunk.chunk_index}) for t in parsed.triplets
    ]

    logger.info(
        "Chunk %d → %d triplets extracted (source=%s, page=%s)",
        chunk.chunk_index,
        len(triplets),
        chunk.metadata.get("source", "unknown"),
        chunk.metadata.get("page", "?"),
    )
    return triplets


def extract_all_triplets(
    chunks: list[Chunk],
    llm: LLMProtocol,
    max_workers: int | None = None,
) -> list[Triplet]:
    """Extract triplets from all chunks in parallel batches.

    Uses a ``ThreadPoolExecutor`` with ``max_workers`` concurrent LLM calls
    (defaults to ``settings.extraction_concurrency``).  Results are assembled
    in original chunk order regardless of completion order.

    Individual chunk failures are silently skipped (logged as warnings).

    Args:
        chunks:      All text chunks from the PDF/chunking pipeline.
        llm:         SLM instance (use ``get_extraction_llm()``).
        max_workers: Override for concurrent workers; falls back to
                     ``settings.extraction_concurrency`` (default 10).

    Returns:
        Flat list of all successfully extracted ``Triplet`` objects,
        in chunk order.
    """
    if not chunks:
        logger.info("Extracted 0 total triplets from 0 chunks.")
        return []

    settings = get_settings()
    workers = max_workers if max_workers is not None else settings.extraction_concurrency

    results: dict[int, list[Triplet]] = {}

    with ThreadPoolExecutor(max_workers=workers) as pool:
        future_to_idx = {
            pool.submit(extract_triplets, chunk, llm): chunk.chunk_index for chunk in chunks
        }
        for future in as_completed(future_to_idx):
            idx = future_to_idx[future]
            try:
                results[idx] = future.result()
            except Exception as exc:  # should not happen — extract_triplets never raises
                logger.warning("Unexpected error for chunk %d: %s", idx, exc)
                results[idx] = []

    all_triplets: list[Triplet] = []
    for chunk in chunks:
        all_triplets.extend(results.get(chunk.chunk_index, []))

    logger.info(
        "Extracted %d total triplets from %d chunks.",
        len(all_triplets),
        len(chunks),
    )
    return all_triplets
