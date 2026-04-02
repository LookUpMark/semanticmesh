"""Shared utility functions for the thesis project."""

__all__ = [
    "clean_json",
    "ReflectionResult",
    "reflect_on_json",
    # Text utilities
    "normalize_text",
    "normalize_whitespace",
    "clean_text",
    "extract_tokens",
    "extract_query_terms",
    "split_alphanumeric_tokens",
    "split_sentences",
    "has_relation_tokens",
    "has_priority_structure_tokens",
    "has_structural_evidence",
    "normalize_candidate_name",
    "is_attribute_like",
    "is_noise_chunk_text",
    "is_short_noise_text",
    "distill_fk_relationship",
    "distill_chunk_text",
]

from src.utils.json_utils import ReflectionResult, clean_json, reflect_on_json
from src.utils.text_utils import (
    clean_text,
    distill_chunk_text,
    distill_fk_relationship,
    extract_query_terms,
    extract_tokens,
    has_priority_structure_tokens,
    has_relation_tokens,
    has_structural_evidence,
    is_attribute_like,
    is_noise_chunk_text,
    is_short_noise_text,
    normalize_candidate_name,
    normalize_text,
    normalize_whitespace,
    split_alphanumeric_tokens,
    split_sentences,
)
