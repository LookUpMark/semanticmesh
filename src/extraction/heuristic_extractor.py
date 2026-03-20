"""Heuristic triplet extraction for lazy graph ingestion.

This module provides a low-cost, non-LLM extraction path that can be enabled
through ``USE_LAZY_EXTRACTION``. It favors precision and determinism over
coverage, and is intended as the first migration step before query-time
expansion logic is introduced.
"""

from __future__ import annotations

from functools import lru_cache
import re

from src.config.logging import get_logger
from src.config.settings import get_settings
from src.models.schemas import Chunk, Triplet

logger = get_logger(__name__)

_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
_SPACES_RE = re.compile(r"\s+")

_MAPPING_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"(?P<subj>[A-Za-z0-9_ ]+?)\s+maps\s+to\s+(?P<obj>[A-Za-z0-9_ ]+)"), "maps_to"),
    (re.compile(r"(?P<subj>[A-Za-z0-9_ ]+?)\s+is\s+(?P<obj>[A-Za-z0-9_ ]+)"), "is"),
    (
        re.compile(r"(?P<subj>[A-Za-z0-9_ ]+?)\s+stores?\s+(?P<obj>[A-Za-z0-9_ ]+)"),
        "stores",
    ),
    (
        re.compile(r"(?P<subj>[A-Za-z0-9_ ]+?)\s+contains?\s+(?P<obj>[A-Za-z0-9_ ]+)"),
        "contains",
    ),
]


@lru_cache(maxsize=1)
def _get_spacy_nlp():
    """Return a cached spaCy nlp pipeline or None when unavailable."""
    settings = get_settings()
    if not getattr(settings, "enable_spacy_heuristics", True):
        return None

    try:
        spacy = __import__("spacy")
    except ImportError:
        logger.warning("spaCy not installed; using regex heuristic extraction fallback.")
        return None

    model_name = getattr(settings, "spacy_model_name", "en_core_web_sm")
    try:
        return spacy.load(model_name)
    except Exception as exc:  # noqa: BLE001
        logger.warning(
            "spaCy model '%s' unavailable (%s); using regex heuristic extraction fallback.",
            model_name,
            exc,
        )
        return None


def _clean(text: str) -> str:
    """Normalize whitespace and trim trailing punctuation."""
    normalized = _SPACES_RE.sub(" ", text).strip()
    return normalized.strip(" ,.;:\t\n\r")


def _split_sentences(text: str) -> list[str]:
    """Return non-empty sentence-like segments from chunk text."""
    if not text.strip():
        return []
    return [_clean(s) for s in _SENTENCE_SPLIT_RE.split(text) if _clean(s)]


def _extract_from_sentence(sentence: str, chunk_index: int) -> list[Triplet]:
    """Extract zero or more deterministic triplets from one sentence."""
    triplets: list[Triplet] = []
    lowered = sentence.lower()

    for pattern, predicate in _MAPPING_PATTERNS:
        match = pattern.search(lowered)
        if not match:
            continue

        start_subj, end_subj = match.span("subj")
        start_obj, end_obj = match.span("obj")
        subject = _clean(sentence[start_subj:end_subj])
        obj = _clean(sentence[start_obj:end_obj])

        if len(subject) < 2 or len(obj) < 2:
            continue

        triplets.append(
            Triplet(
                subject=subject,
                predicate=predicate,
                object=obj,
                provenance_text=sentence,
                confidence=0.55,
                source_chunk_index=chunk_index,
            )
        )

    if not triplets:
        tokens = [t for t in re.findall(r"[A-Za-z][A-Za-z0-9_]{2,}", sentence) if len(t) > 2]
        if len(tokens) >= 2:
            triplets.append(
                Triplet(
                    subject=tokens[0],
                    predicate="related_to",
                    object=tokens[1],
                    provenance_text=sentence,
                    confidence=0.35,
                    source_chunk_index=chunk_index,
                )
            )

    return triplets


def _extract_from_spacy_sentence(sent, chunk_index: int) -> list[Triplet]:
    """Extract triplets from one spaCy sentence span with dependency hints."""
    sentence = _clean(sent.text)
    if not sentence:
        return []

    subject = None
    obj = None
    predicate = None

    for token in sent:
        dep = getattr(token, "dep_", "")
        if subject is None and dep in {"nsubj", "nsubjpass"}:
            subject = _clean(token.text)
        if obj is None and dep in {"dobj", "pobj", "obj", "attr", "dative"}:
            obj = _clean(token.text)
        if predicate is None and dep == "ROOT":
            predicate = _clean(getattr(token, "lemma_", "") or token.text).lower()

    if subject and obj and predicate and len(subject) > 1 and len(obj) > 1 and len(predicate) > 1:
        return [
            Triplet(
                subject=subject,
                predicate=predicate,
                object=obj,
                provenance_text=sentence,
                confidence=0.60,
                source_chunk_index=chunk_index,
            )
        ]

    return _extract_from_sentence(sentence, chunk_index)


def extract_all_triplets_heuristic(chunks: list[Chunk]) -> list[Triplet]:
    """Extract triplets from chunks without calling an LLM."""
    extracted: list[Triplet] = []
    seen: set[tuple[str, str, str, int | None]] = set()
    nlp = _get_spacy_nlp()

    for chunk in chunks:
        if nlp is not None:
            doc = nlp(chunk.text)
            sentence_triplets: list[Triplet] = []
            for sent in doc.sents:
                sentence_triplets.extend(_extract_from_spacy_sentence(sent, chunk.chunk_index))
        else:
            sentence_triplets = []
            for sentence in _split_sentences(chunk.text):
                sentence_triplets.extend(_extract_from_sentence(sentence, chunk.chunk_index))

        for triplet in sentence_triplets:
                key = (
                    triplet.subject.lower(),
                    triplet.predicate.lower(),
                    triplet.object.lower(),
                    triplet.source_chunk_index,
                )
                if key in seen:
                    continue
                seen.add(key)
                extracted.append(triplet)

    return extracted
