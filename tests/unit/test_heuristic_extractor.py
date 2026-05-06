"""Unit tests for heuristic lazy triplet extraction."""

from types import SimpleNamespace

import src.extraction.heuristic_extractor as heuristic_extractor
from src.extraction.heuristic_extractor import extract_all_triplets_heuristic
from src.models.schemas import Chunk


def _chunk(text: str, idx: int = 0) -> Chunk:
    return Chunk(text=text, chunk_index=idx, metadata={"source": "test.txt", "page": "1"})


def test_extracts_pattern_based_triplets() -> None:
    chunks = [_chunk("Customer maps to CUSTOMER_MASTER. SALES_ORDER stores order data.", 3)]
    triplets = extract_all_triplets_heuristic(chunks)

    assert triplets
    assert any(t.predicate == "maps_to" for t in triplets)
    assert len(triplets) >= 2
    # Regex fallback extracts the full matched group (e.g. "order data"); spaCy would give "order"
    assert any("order" in t.object.lower() for t in triplets)
    assert all(t.source_chunk_index == 3 for t in triplets)


def test_fallback_relation_and_deduplication() -> None:
    chunks = [_chunk("Inventory metrics. Inventory metrics.", 1)]
    triplets = extract_all_triplets_heuristic(chunks)

    assert len(triplets) == 1
    assert triplets[0].predicate == "related_to"
    assert triplets[0].confidence <= 0.35


def test_spacy_path_extracts_dependency_triplet(monkeypatch) -> None:
    class FakeToken:
        def __init__(self, text: str, dep_: str, lemma_: str = "") -> None:
            self.text = text
            self.dep_ = dep_
            self.lemma_ = lemma_ or text.lower()

    class FakeSentence:
        def __init__(self) -> None:
            self.text = "Customers place orders"
            self._tokens = [
                FakeToken("Customers", "nsubj"),
                FakeToken("place", "ROOT", "store"),
                FakeToken("orders", "dobj"),
            ]

        def __iter__(self):
            return iter(self._tokens)

    class FakeDoc:
        def __init__(self) -> None:
            self.sents = [FakeSentence()]

    monkeypatch.setattr(
        heuristic_extractor,
        "_get_spacy_nlp",
        lambda: lambda _text: FakeDoc(),
    )

    chunks = [_chunk("Customers place orders.", 7)]
    triplets = extract_all_triplets_heuristic(chunks)

    assert len(triplets) == 1
    assert triplets[0].subject == "Customers"
    assert triplets[0].predicate == "store"
    assert triplets[0].object == "orders"
    assert triplets[0].confidence == 0.60
    assert triplets[0].source_chunk_index == 7


def test_spacy_missing_falls_back_to_regex(monkeypatch) -> None:
    monkeypatch.setattr(heuristic_extractor, "_get_spacy_nlp", lambda: None)
    monkeypatch.setattr(
        heuristic_extractor,
        "get_settings",
        lambda: SimpleNamespace(enable_spacy_heuristics=False, heuristic_extraction_confidence=0.55),
    )

    chunks = [_chunk("Customer maps to CUSTOMER_MASTER.", 2)]
    triplets = extract_all_triplets_heuristic(chunks)

    assert len(triplets) == 1
    assert triplets[0].predicate == "maps_to"
