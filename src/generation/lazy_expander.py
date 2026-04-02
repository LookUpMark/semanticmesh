"""Lazy query-time expansion helpers.

This module augments retrieval only when initial confidence is low,
keeping the default path fast for high-confidence queries.
"""

from __future__ import annotations

from src.models.schemas import RetrievedChunk


def should_trigger_lazy_expansion(
    top_score: float,
    chunk_count: int,
    threshold: float,
) -> bool:
    """Return True when retrieval looks too weak and expansion is justified."""
    if chunk_count <= 0:
        return True
    return float(top_score) < float(threshold)


def collect_seed_names_for_expansion(chunks: list[RetrievedChunk], limit: int = 8) -> list[str]:
    """Collect unique node IDs used as traversal seeds for expansion."""
    seeds: list[str] = []
    seen: set[str] = set()
    for chunk in chunks:
        node_id = (chunk.node_id or "").strip()
        if not node_id or node_id in seen:
            continue
        seen.add(node_id)
        seeds.append(node_id)
        if len(seeds) >= limit:
            break
    return seeds
