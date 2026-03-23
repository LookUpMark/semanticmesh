"""Deterministic context distillation for query-time chunks.

The distiller rewrites noisy chunk texts into compact, citation-friendly
statements without introducing new facts. It only reformats information already
present in input chunks.
"""

from __future__ import annotations

import re

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


def _query_terms(query: str) -> set[str]:
    stop = {
        "what",
        "which",
        "where",
        "when",
        "how",
        "does",
        "the",
        "this",
        "that",
        "with",
        "into",
        "from",
        "table",
        "database",
        "business",
        "concept",
        "information",
        "schema",
        "knowledge",
        "graph",
    }
    return {t.lower() for t in _TOKEN_RE.findall(query) if len(t) > 2 and t.lower() not in stop}


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

    if ":" in text and len(text) > 220:
        head, body = text.split(":", 1)
        compact = " ".join(body.split())
        return f"{head.strip()}: {compact[:220].rstrip()}"

    return " ".join(text.split())


def distill_context_chunks(
    query: str,
    chunks: list[RetrievedChunk],
    max_chunks: int = 10,
) -> list[RetrievedChunk]:
    """Return cleaned and de-duplicated chunk list for answer generation."""
    if not chunks:
        return []

    terms = _query_terms(query)

    def _priority(chunk: RetrievedChunk) -> tuple[int, int, float]:
        t = chunk.text.lower()
        n = chunk.node_id.lower()
        hits = int(any(term in t or term in n for term in terms))
        structural = int("→" in chunk.node_id or "foreign key" in t or "references" in t)
        return (hits, structural, float(chunk.score))

    ranked = sorted(chunks, key=_priority, reverse=True)
    out: list[RetrievedChunk] = []
    seen_text: set[str] = set()
    for chunk in ranked:
        distilled_text = _distill_text(chunk)
        key = distilled_text.lower()
        if key in seen_text:
            continue
        seen_text.add(key)
        out.append(
            chunk.model_copy(
                update={
                    "text": distilled_text,
                    "metadata": {**chunk.metadata, "distilled": True},
                }
            )
        )
        if len(out) >= max_chunks:
            break
    return out
