"""Deterministic context distillation for query-time chunks.

The distiller rewrites noisy chunk texts into compact, citation-friendly
statements without introducing new facts. It only reformats information already
present in input chunks.
"""

from __future__ import annotations

import re

import tiktoken

from src.config.settings import get_settings
from src.models.schemas import RetrievedChunk

_TOKEN_RE = re.compile(r"[a-zA-Z0-9_]+")
_FK_RE = re.compile(
    r"The table\s+(?P<src>[A-Za-z0-9_]+)\s+references\s+(?P<tgt>[A-Za-z0-9_]+)"
    r"\s+via\s+a\s+foreign\s+key\s+\(column\s+(?P<fk>[A-Za-z0-9_]+)\s+→\s+"
    r"(?P<tgt2>[A-Za-z0-9_]+)\.(?P<ref>[A-Za-z0-9_]+)\)\.",
    re.IGNORECASE,
)
_NOISE_MARKERS = (
    "heuristic embedding mapping score=",
    "adjusted_confidence=",
    "best_candidate=",
)

# Shared tokenizer — same encoding used throughout the project (cl100k_base)
_TOKENIZER = tiktoken.get_encoding("cl100k_base")


def _distill_text(chunk: RetrievedChunk) -> str:
    text = chunk.text.strip()
    m = _FK_RE.search(text)
    if m:
        src = m.group("src")
        tgt = m.group("tgt")
        fk = m.group("fk")
        ref = m.group("ref")
        return f"Relationship: {src} references {tgt} via foreign key {fk} -> {tgt}.{ref}."

    lower = text.lower()
    if any(marker in lower for marker in _NOISE_MARKERS):
        return f"Entity hint: {chunk.node_id}."

    # Fix mid-sentence chunk starts: if text doesn't begin with a capital
    # letter or Markdown marker, trim up to the first sentence boundary.
    if text and text[0].islower():
        # Find first sentence-like boundary (. or newline followed by capital/marker)
        for i, ch in enumerate(text):
            if ch == "\n" and i + 1 < len(text):
                text = text[i + 1 :]
                break
        else:
            # No newline found, try period
            dot = text.find(". ")
            if dot != -1 and dot < 80:
                text = text[dot + 2 :]

    if ":" in text and len(text) > 800:
        head, body = text.split(":", 1)
        compact = " ".join(body.split())
        return f"{head.strip()}: {compact}"

    return " ".join(text.split())


def distill_context_chunks(
    query: str,
    chunks: list[RetrievedChunk],
    max_chunks: int | None = None,
    token_budget: int | None = None,
) -> list[RetrievedChunk]:
    """Return cleaned and de-duplicated chunk list for answer generation.

    Chunks are processed in their incoming order (preserving reranker ranking)
    and added until either *max_chunks* or *token_budget* (measured in
    cl100k_base tokens) is reached.

    Args:
        query:        Natural-language query string.
        chunks:       Retrieved and optionally reranked chunks (order preserved).
        max_chunks:   Hard upper bound on number of chunks returned.
                      Defaults to ``settings.generation_max_context_chunks``.
                      Pass ``0`` or a very large number to rely solely on the
                      token budget.
        token_budget: Soft upper bound on total context tokens.
                      Defaults to ``settings.generation_token_budget``.
                      A chunk that would push the total over budget is skipped
                      rather than truncated so every included chunk is verbatim.
    """
    if not chunks:
        return []

    settings = get_settings()
    effective_max_chunks = (
        max_chunks if max_chunks is not None else settings.generation_max_context_chunks
    )
    effective_token_budget = (
        token_budget if token_budget is not None else settings.generation_token_budget
    )

    out: list[RetrievedChunk] = []
    seen_text: set[str] = set()
    used_tokens: int = 0
    effective_max = effective_max_chunks if effective_max_chunks > 0 else len(chunks)
    for chunk in chunks:
        distilled_text = _distill_text(chunk)
        key = distilled_text.lower()
        if key in seen_text:
            continue
        chunk_tokens = len(_TOKENIZER.encode(distilled_text))
        if used_tokens + chunk_tokens > effective_token_budget:
            continue  # skip oversized chunks rather than truncating
        seen_text.add(key)
        out.append(
            chunk.model_copy(
                update={
                    "text": distilled_text,
                    "metadata": {**chunk.metadata, "distilled": True},
                }
            )
        )
        used_tokens += chunk_tokens
        if len(out) >= effective_max:
            break
    return out
