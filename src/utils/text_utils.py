"""Shared text manipulation utilities for the thesis project.

This module provides common text processing patterns used across the codebase,
including normalization, token extraction, sentence splitting, and pattern matching.
Functions are designed to be deterministic, efficient, and well-typed.

Typical usage:
    >>> from src.utils.text_utils import normalize_text, extract_tokens
    >>> text = "  The Customer table stores orders.  "
    >>> normalize_text(text)
    'the customer table stores orders.'
    >>> extract_tokens(text)
    {'customer', 'table', 'stores', 'orders'}
"""

from __future__ import annotations

import re
from typing import Final

# ─────────────────────────────────────────────────────────────────────────────
# Compiled Regular Expressions
# ─────────────────────────────────────────────────────────────────────────────

#: Matches alphanumeric tokens (letters, numbers, underscores).
#: Used for extracting meaningful words from text.
TOKEN_RE: Final[re.Pattern[str]] = re.compile(r"[a-zA-Z0-9_]+")

#: Splits text at sentence boundaries (period, exclamation, question mark).
#: Uses lookbehind to preserve the punctuation in the result.
SENTENCE_SPLIT_RE: Final[re.Pattern[str]] = re.compile(r"(?<=[.!?])\s+")

#: Normalizes whitespace sequences (spaces, tabs, newlines) to single spaces.
SPACES_RE: Final[re.Pattern[str]] = re.compile(r"\s+")

#: Matches tokens starting with alphanumeric character followed by 2+ alphanumeric/underscore.
#: Used in heuristic extraction for finding candidate entities.
ALPHANUMERIC_TOKEN_RE: Final[re.Pattern[str]] = re.compile(r"[A-Za-z][A-Za-z0-9_]{2,}")

#: Splits text on non-alphanumeric boundaries for tokenization.
NON_ALPHANUMERIC_RE: Final[re.Pattern[str]] = re.compile(r"[^a-zA-Z0-9]+")

#: Common stop words for query term extraction.
#: Includes generic terms that add little semantic value.
QUERY_STOP_WORDS: Final[frozenset[str]] = frozenset(
    {
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
)

#: Tokens that indicate relational structure (foreign keys, joins).
RELATION_TOKENS: Final[tuple[str, ...]] = (
    "references",
    "foreign key",
    "fk ",
    " fk",
    "joins",
    "join ",
)

#: Priority structure tokens for chunk ranking.
PRIORITY_STRUCTURE_TOKENS: Final[tuple[str, ...]] = ("references", "foreign key")

#: Punctuation characters to strip from text ends.
TRAILING_PUNCTUATION: Final[str] = " ,.;:!? \t\n\r"


# ─────────────────────────────────────────────────────────────────────────────
# Normalization Functions
# ─────────────────────────────────────────────────────────────────────────────


def normalize_text(text: str) -> str:
    """Normalize text by lowercasing and stripping surrounding whitespace.

    This is a lightweight normalization suitable for comparisons and lookups.
    For more aggressive normalization (whitespace collapsing, punctuation removal),
    use ``normalize_whitespace`` or ``clean_text`` instead.

    Args:
        text: Input string to normalize.

    Returns:
        Lowercased string with leading/trailing whitespace removed.

    Example:
        >>> normalize_text("  Customer Orders  ")
        'customer orders'
    """
    return text.lower().strip()


def normalize_whitespace(text: str) -> str:
    """Collapse all whitespace sequences to single spaces and strip.

    Handles spaces, tabs, newlines, and other Unicode whitespace.

    Args:
        text: Input string with potentially irregular whitespace.

    Returns:
        String with normalized whitespace and trimmed ends.

    Example:
        >>> normalize_whitespace("Line1\\n\\n  Line2\\tLine3")
        'Line1 Line2 Line3'
    """
    return SPACES_RE.sub(" ", text).strip()


def clean_text(text: str) -> str:
    """Full text cleaning: normalize whitespace and remove trailing punctuation.

    Combines whitespace normalization with removal of common trailing
    punctuation marks. Suitable for preparing text for display or storage.

    Args:
        text: Input string to clean.

    Returns:
        Cleaned string with normalized whitespace and no trailing punctuation.

    Example:
        >>> clean_text("  Example text, with punctuation.  ")
        'Example text, with punctuation'
    """
    normalized = normalize_whitespace(text)
    return normalized.strip(TRAILING_PUNCTUATION)


#: Matches a camelCase or PascalCase transition (lowercase followed by uppercase).
_CAMEL_SPLIT_RE: Final[re.Pattern[str]] = re.compile(r"([a-z])([A-Z])")

#: English articles/determiners and common sentence-starter verbs to skip when
#: extracting a noun phrase from a sentence-like concept name.
_LEADING_SKIP_WORDS: Final[frozenset[str]] = frozenset({
    "a", "an", "the", "this", "that", "these", "those",
    "each", "every", "any", "some", "all",
    "it", "its", "they", "their",
    "is", "are", "was", "were", "be", "been",
    "represents", "contains", "stores", "holds", "describes",
    "indicates", "records", "defines", "specifies",
})

#: Regex to detect a sentence-like concept name: starts with a determiner/article
#: or has a subordinating clause marker.
_SENTENCE_MARKER_RE: Final[re.Pattern[str]] = re.compile(
    r"^(a|an|the|this|that|each|every)\s+", re.IGNORECASE
)


def normalize_concept_name(name: str) -> str:
    """Normalize a raw LLM-generated entity name to a short Title Case phrase.

    Handles the following input forms:
    - ``camelCase`` / ``PascalCase`` → splits on case boundary
    - ``SNAKE_CASE`` / ``ALL_CAPS`` → splits on underscores
    - Short noun phrase → collapses whitespace and applies Title Case
    - **Sentence-like description** (≥ 5 words or starts with an article) →
      extracts the core noun phrase using two strategies:

      1. **Title-Case run extraction**: scans the sentence for consecutive
         capitalised words (e.g. "Sales Order", "Product") and returns the
         longest run of ≥ 2 words, or the first single capitalised word.
      2. **Leading-word fallback**: strips leading articles/determiners and
         takes the first 3 content words.

    Args:
        name: Raw entity name string from the LLM.

    Returns:
        Normalised, title-cased concept name of at most ~4 words.

    Examples:
        >>> normalize_concept_name("customerOrder")
        'Customer Order'
        >>> normalize_concept_name("CUSTOMER_ORDER_DETAIL")
        'Customer Order Detail'
        >>> normalize_concept_name(
        ...     "a single line within a Sales Order specifying a Product"
        ... )
        'Sales Order'
    """
    if not name:
        return name

    # ── Step 1: split camelCase / PascalCase ──────────────────────────────────
    name = _CAMEL_SPLIT_RE.sub(r"\1 \2", name)
    # Replace underscores and dashes with spaces, strip punctuation
    name = name.replace("_", " ").replace("-", " ")
    name = SPACES_RE.sub(" ", name).strip().strip(".,;:!?\"'")

    words = name.split()

    # ── Step 2: if it's a short phrase (≤ 4 words), just Title-Case it ───────
    if len(words) <= 4 and not _SENTENCE_MARKER_RE.match(name):
        return name.title()

    # ── Step 3: sentence-like → extract noun phrase ───────────────────────────
    # Strategy A: find the longest run of consecutive Title-Case words
    # that appear in the middle of the sentence (skip the very first word
    # since it's always capitalised due to sentence start).
    # A word is considered "Title Case in context" if the original had it
    # capitalised (we peek at the raw words before .title()).
    raw_words = name.split()
    # Find runs of words that were originally capitalised (i.e. not all-lower)
    runs: list[list[str]] = []
    current_run: list[str] = []
    for i, w in enumerate(raw_words):
        clean_w = w.strip(".,;:!?\"'()")
        is_cap = clean_w and clean_w[0].isupper() and i > 0  # skip first word
        if is_cap and clean_w.lower() not in _LEADING_SKIP_WORDS:
            current_run.append(clean_w)
        else:
            if current_run:
                runs.append(current_run)
            current_run = []
    if current_run:
        runs.append(current_run)

    if runs:
        # Pick the longest run; if tied, pick the first
        best_run = max(runs, key=len)
        candidate = " ".join(best_run[:4])  # cap at 4 words
        if candidate:
            return candidate.title()

    # Strategy B: strip leading skip words and take first 3 content words
    content_words = []
    for w in raw_words:
        clean_w = w.strip(".,;:!?\"'()")
        if not content_words and clean_w.lower() in _LEADING_SKIP_WORDS:
            continue
        content_words.append(clean_w)
        if len(content_words) >= 3:
            break

    return " ".join(content_words).title() if content_words else name.title()


# ─────────────────────────────────────────────────────────────────────────────
# Token Extraction Functions
# ─────────────────────────────────────────────────────────────────────────────


def extract_tokens(text: str, *, min_length: int = 2) -> set[str]:
    """Extract alphanumeric tokens from text, normalized to lowercase.

    Tokens are sequences of letters, numbers, and underscores. Short tokens
    are filtered out to reduce noise.

    Args:
        text: Input string to tokenize.
        min_length: Minimum token length to include (default: 2).

    Returns:
        Set of unique, lowercase tokens meeting the length requirement.

    Example:
        >>> extract_tokens("Customer_ID stores Order_123")
        {'customer_id', 'stores', 'order_123'}
        >>> extract_tokens("a b c", min_length=2)
        set()
    """
    return {t.lower() for t in TOKEN_RE.findall(text) if len(t) >= min_length}


def extract_query_terms(query: str) -> set[str]:
    """Extract meaningful query terms, filtering stop words and short tokens.

    Designed for search/retrieval scenarios where common words should be
    ignored. Uses ``QUERY_STOP_WORDS`` to filter generic terms.

    Args:
        query: Search query or natural language question.

    Returns:
        Set of significant, lowercase query terms.

    Example:
        >>> extract_query_terms("What tables reference the Customer?")
        {'tables', 'reference', 'customer'}
    """
    return {
        t.lower()
        for t in TOKEN_RE.findall(query)
        if len(t) > 2 and t.lower() not in QUERY_STOP_WORDS
    }


def split_alphanumeric_tokens(text: str) -> list[str]:
    """Split text into alphanumeric tokens on non-alphanumeric boundaries.

    More aggressive than ``extract_tokens`` - splits on any non-alphanumeric
    character rather than matching token sequences.

    Args:
        text: Input string to tokenize.

    Returns:
        List of non-empty, lowercase alphanumeric tokens.

    Example:
        >>> split_alphanumeric_tokens("user_name@example.com")
        ['user', 'name', 'example', 'com']
    """
    return [t.lower() for t in NON_ALPHANUMERIC_RE.split(text) if t]


# ─────────────────────────────────────────────────────────────────────────────
# Sentence Splitting
# ─────────────────────────────────────────────────────────────────────────────


def split_sentences(text: str) -> list[str]:
    """Split text into sentence-like segments, cleaning each segment.

    Splits on period, exclamation, or question mark followed by whitespace.
    Empty segments are filtered out.

    Args:
        text: Input text to split.

    Returns:
        List of non-empty, cleaned sentence segments.

    Example:
        >>> split_sentences("First sentence. Second! Third?")
        ['First sentence', 'Second', 'Third']
        >>> split_sentences("  .  ")
        []
    """
    if not text.strip():
        return []
    return [clean_text(s) for s in SENTENCE_SPLIT_RE.split(text) if clean_text(s)]


# ─────────────────────────────────────────────────────────────────────────────
# Pattern Matching Functions
# ─────────────────────────────────────────────────────────────────────────────


def has_relation_tokens(text: str) -> bool:
    """Check if text contains relational structure tokens.

    Tests for indicators of foreign key relationships or joins.

    Args:
        text: Text to check.

    Returns:
        True if any relation token is found in the text.

    Example:
        >>> has_relation_tokens("Table A references Table B")
        True
        >>> has_relation_tokens("Simple data description")
        False
    """
    return any(token in text for token in RELATION_TOKENS)


def has_priority_structure_tokens(text: str) -> bool:
    """Check if text contains priority structure tokens (FK, references).

    More restrictive than ``has_relation_tokens`` - only checks for
    high-priority structural indicators.

    Args:
        text: Text to check.

    Returns:
        True if any priority structure token is found.

    Example:
        >>> has_priority_structure_tokens("foreign key column")
        True
        >>> has_priority_structure_tokens("table joins data")
        False
    """
    return any(token in text for token in PRIORITY_STRUCTURE_TOKENS)


def has_structural_evidence(node_id: str, text: str) -> bool:
    """Check if a chunk has structural relationship evidence.

    Looks for arrow symbols in node IDs or relation tokens in text.
    Used in retrieval quality assessment.

    Args:
        node_id: Node identifier string.
        text: Chunk text content.

    Returns:
        True if structural evidence is found.

    Example:
        >>> has_structural_evidence("A→B", "foreign key relationship")
        True
        >>> has_structural_evidence("Entity", "simple description")
        False
    """
    normalized_id = node_id.strip().lower()
    if "→" in normalized_id:
        return True
    normalized_text = text.strip().lower()
    return has_relation_tokens(normalized_text)


# ─────────────────────────────────────────────────────────────────────────────
# Name Normalization (for mapping/concept matching)
# ─────────────────────────────────────────────────────────────────────────────


def normalize_candidate_name(name: str) -> str:
    """Normalize a candidate concept name for comparison.

    Removes common prefixes and suffixes that add noise, such as:
    - Leading "The "
    - Trailing " business concept"
    - Extra spaces and punctuation

    Args:
        name: Raw candidate name to normalize.

    Returns:
        Cleaned name suitable for comparison.

    Example:
        >>> normalize_candidate_name("The Customer business concept.")
        'Customer business concept'
        >>> normalize_candidate_name("  Order Item  ")
        'Order Item'
    """
    cleaned = re.sub(r"^the\s+", "", name.strip(), flags=re.IGNORECASE)
    cleaned = re.sub(r"\s+business\s+concept$", "", cleaned, flags=re.IGNORECASE)
    cleaned = cleaned.strip(" .")
    return cleaned


def is_attribute_like(name: str, table_column_names: set[str] | None = None) -> bool:
    """Check if a name appears to be an attribute rather than a concept.

    Attributes are typically:
    - Matching table column names (if provided)
    - ALL_CAPS_WITH_UNDERSCORES (database column style)
    - Too long or too short (token count)
    - Generic noise tokens

    Args:
        name: Candidate name to evaluate.
        table_column_names: Optional set of table column names for comparison.

    Returns:
        True if the name appears to be an attribute.

    Example:
        >>> is_attribute_like("CUSTOMER_ID")
        True
        >>> is_attribute_like("Customer")
        False
    """
    generic_noise_tokens = {
        "business",
        "dictionary",
        "description",
        "decimal",
        "status",
        "examples",
        "contains",
        "provides",
        "usage",
        "multiple",
        "negative",
    }
    n = name.strip()
    n_tokens = split_alphanumeric_tokens(n)

    if table_column_names and n.upper() in table_column_names:
        return True
    if re.fullmatch(r"[A-Z0-9_]{4,}", n) and "_" in n:
        return True
    if len(n_tokens) == 0 or len(n_tokens) > 8:
        return True
    return n.lower() in generic_noise_tokens


# ─────────────────────────────────────────────────────────────────────────────
# Noise Detection
# ─────────────────────────────────────────────────────────────────────────────


NOISE_MARKERS: Final[tuple[str, ...]] = (
    "heuristic embedding mapping score=",
    "adjusted_confidence=",
    "best_candidate=",
)


def is_noise_chunk_text(text: str) -> bool:
    """Check if chunk text contains noise markers indicating low-quality content.

    Args:
        text: Chunk text to evaluate.

    Returns:
        True if noise markers are present.

    Example:
        >>> is_noise_chunk_text("heuristic embedding mapping score=0.5")
        True
        >>> is_noise_chunk_text("Entity: Customer")
        False
    """
    lower = text.lower()
    return any(marker in lower for marker in NOISE_MARKERS)


def is_short_noise_text(text: str, min_length: int = 18) -> bool:
    """Check if text is suspiciously short, likely indicating low quality.

    Args:
        text: Text to evaluate.
        min_length: Minimum length threshold (default: 18).

    Returns:
        True if text is shorter than threshold.

    Example:
        >>> is_short_noise_text("Entity")
        True
        >>> is_short_noise_text("Entity: Customer with full description")
        False
    """
    return len(text.strip()) < min_length


# ─────────────────────────────────────────────────────────────────────────────
# Distillation (for query-time chunk rewriting)
# ─────────────────────────────────────────────────────────────────────────────

_FOREIGN_KEY_RE: Final[re.Pattern[str]] = re.compile(
    r"The table\s+(?P<src>[A-Za-z0-9_]+)\s+references\s+(?P<tgt>[A-Za-z0-9_]+)"
    r"\s+via\s+a\s+foreign\s+key\s+\(column\s+(?P<fk>[A-Za-z0-9_]+)\s+→\s+"
    r"(?P<tgt2>[A-Za-z0-9_]+)\.(?P<ref>[A-Za-z0-9_]+)\)\.",
    re.IGNORECASE,
)


def distill_fk_relationship(text: str) -> str | None:
    """Extract and format foreign key relationship from verbose chunk text.

    Parses verbose FK descriptions into compact, standardized format.

    Args:
        text: Chunk text containing FK relationship description.

    Returns:
        Formatted FK string or None if pattern not found.

    Example:
        >>> distill_fk_relationship(
        ...     "The table orders references customers via a foreign key "
        ...     "(column customer_id → customers.id)."
        ... )
        'Relationship: orders references customers via foreign key customer_id -> customers.id.'
    """
    m = _FOREIGN_KEY_RE.search(text)
    if not m:
        return None
    src = m.group("src")
    tgt = m.group("tgt")
    fk = m.group("fk")
    ref = m.group("ref")
    return f"Relationship: {src} references {tgt} via foreign key {fk} -> {tgt}.{ref}."


def distill_chunk_text(text: str, node_id: str) -> str:
    """Distill chunk text into compact, citation-friendly format.

    Handles:
    - Foreign key relationship extraction
    - Noise marker filtering
    - Long text truncation at colon boundary

    Args:
        text: Raw chunk text.
        node_id: Node identifier for entity hints.

    Returns:
        Distilled text suitable for answer generation context.

    Example:
        >>> distill_chunk_text("heuristic embedding mapping score=0.5", "Entity")
        'Entity hint: Entity.'
        >>> distill_chunk_text("Customer: The customer entity stores data...", "Customer")
        'Customer: The customer entity stores data'
    """
    # FK relationship extraction
    fk_distilled = distill_fk_relationship(text)
    if fk_distilled:
        return fk_distilled

    # Noise marker filtering
    if is_noise_chunk_text(text):
        return f"Entity hint: {node_id}."

    # Long text truncation
    if ":" in text and len(text) > 220:
        head, body = text.split(":", 1)
        compact = " ".join(body.split())
        return f"{head.strip()}: {compact[:220].rstrip()}"

    # Default: normalize whitespace
    return normalize_whitespace(text)


# ─────────────────────────────────────────────────────────────────────────────
# CamelCase Normalization
# ─────────────────────────────────────────────────────────────────────────────

#: Splits on CamelCase boundaries: "SalesOrder" → "Sales Order"
_CAMEL_BOUNDARY_RE: re.Pattern[str] = re.compile(r"(?<=[a-z])(?=[A-Z])")


def normalize_source_name(name: str) -> str:
    """Normalize a source name for substring matching.

    Handles CamelCase → space-separated, underscores → spaces, then lowercases.
    Examples:
        "SalesOrder"      → "sales order"
        "OrderLineItem"   → "order line item"
        "CUSTOMER_MASTER" → "customer master"
        "Customer"        → "customer"
    """
    spaced = _CAMEL_BOUNDARY_RE.sub(" ", name)
    return spaced.replace("_", " ").lower().strip()
