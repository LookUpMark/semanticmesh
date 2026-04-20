"""Shared query processing utilities."""

from __future__ import annotations

import re

_TOKEN_RE = re.compile(r"[A-Za-z0-9]+(?:[-_][A-Za-z0-9]+)*")

_STOP_WORDS = frozenset({
    "what", "which", "where", "when", "how", "does",
    "the", "this", "that", "with", "into", "from",
    "each", "for", "and", "are",
    "table", "database", "business", "concept",
    "information", "schema", "knowledge", "graph",
})


def query_terms(query: str) -> set[str]:
    """Extract meaningful keywords from a query, stripping stop words."""
    return {t.lower() for t in _TOKEN_RE.findall(query) if len(t) > 2 and t.lower() not in _STOP_WORDS}
