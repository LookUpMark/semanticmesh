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
