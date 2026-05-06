"""Gold Standard Loader — load and normalize QA pairs from dataset JSON files.

Handles the heterogeneous schemas across fixtures (DS01–DS07) and returns
a canonical ``(dataset_metadata, normalized_pairs)`` tuple.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Known wrapper keys that hold the QA-pair array.
_WRAPPER_KEYS = ("pairs", "qa_pairs", "questions")

# Field-name resolution priority (first match wins).
_ANSWER_KEYS = ("expected_answer", "answer", "ground_truth")
_SOURCES_KEYS = ("expected_sources", "entities", "concepts", "tables_involved", "relevant_tables")
_TYPE_KEYS = ("query_type", "category")
_DIFFICULTY_KEYS = ("difficulty", "complexity")


def load_gold_standard(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Load QA pairs from a gold-standard JSON, normalizing all field names.

    Supports:
      * Dict-wrapped formats: ``{"pairs": [...]}``, ``{"qa_pairs": [...]}``
      * Bare JSON arrays: ``[...]``
      * All field-name variants across DS01–DS07

    Returns:
        ``(dataset_metadata, normalized_pairs)``
    """
    with path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    # ── Extract the inner array ──────────────────────────────────────────────
    if isinstance(raw, list):
        pairs_raw: list[dict] = raw
        metadata: dict[str, Any] = {}
    elif isinstance(raw, dict):
        metadata = {k: v for k, v in raw.items() if k not in _WRAPPER_KEYS}
        pairs_raw = None
        for key in _WRAPPER_KEYS:
            if key in raw:
                pairs_raw = raw[key]
                break
        if pairs_raw is None:
            logger.warning("No recognized QA key (%s) in %s", _WRAPPER_KEYS, path)
            pairs_raw = []
    else:
        raise TypeError(f"Unexpected top-level type in {path}: {type(raw).__name__}")

    # ── Normalize each pair ──────────────────────────────────────────────────
    normalized: list[dict[str, Any]] = []
    for i, p in enumerate(pairs_raw):
        if not isinstance(p, dict):
            logger.warning("Skipping non-dict item at index %d in %s", i, path)
            continue
        norm = dict(p)
        # query_id
        if "query_id" not in norm:
            raw_id = p.get("id", f"Q{i + 1:03d}")
            norm["query_id"] = str(raw_id) if not isinstance(raw_id, str) else raw_id
        # expected_answer
        if "expected_answer" not in norm:
            norm["expected_answer"] = next((p.get(k) for k in _ANSWER_KEYS if p.get(k)), "")
        # expected_sources
        if "expected_sources" not in norm:
            norm["expected_sources"] = next((p.get(k) for k in _SOURCES_KEYS if p.get(k)), [])
        # query_type — normalize value to snake_case regardless of source field
        if "query_type" not in norm:
            norm["query_type"] = next((p.get(k) for k in _TYPE_KEYS if p.get(k)), "unknown")
        norm["query_type"] = norm["query_type"].lower().replace(" ", "_").replace("-", "_")
        # difficulty
        if "difficulty" not in norm:
            norm["difficulty"] = next((p.get(k) for k in _DIFFICULTY_KEYS if p.get(k)), "unknown")
        normalized.append(norm)

    return metadata, normalized
