# Part 7 — `src/retrieval/hybrid_retriever.py`

## 1. Purpose & Context

**Epic:** EP-12 Hybrid Retrieval  
**US-12-01** — Dense Vector Retrieval, **US-12-02** — BM25 Keyword Retrieval, **US-12-03** — Graph Traversal, **US-12-04** — Result Merging

`hybrid_retriever` combines three complementary retrieval strategies to maximise recall before reranking:

| Strategy | Strength | Implementation |
|---|---|---|
| Dense (vector) | Semantic similarity, paraphrases | Neo4j vector index + BGE-M3 |
| BM25 | Exact keywords, rare tokens | `rank-bm25` on a node text index |
| Graph traversal | Relational context, JOIN partners | Cypher `MATCH (start)-[r*1..N]` |

Results are deduplicated by node name, keeping the highest score per node, then passed to the cross-encoder reranker.

---

## 2. Prerequisites

- `src/models/schemas.py` — `RetrievedChunk` (step 5)
- `src/graph/neo4j_client.py` — `Neo4jClient` (step 19)
- `src/retrieval/embeddings.py` — `embed_text` (step 23)
- `src/config/settings.py` — `retrieval_vector_top_k`, `retrieval_bm25_top_k`, `retrieval_graph_depth`
- `rank-bm25` package (`pip install rank-bm25`)

---

## 3. Public API

| Symbol | Signature | Description |
|---|---|---|
| `vector_search` | `(query, client, top_k, model) -> list[RetrievedChunk]` | Dense BGE-M3 + Neo4j vector index |
| `bm25_search` | `(query, all_nodes, top_k) -> list[RetrievedChunk]` | BM25Okapi keyword search on node dump |
| `graph_traversal` | `(seed_names, client, depth) -> list[RetrievedChunk]` | Cypher hop expansion |
| `merge_results` | `(vector, bm25, graph) -> list[RetrievedChunk]` | Dedup by name, keep max score |
| `build_node_index` | `(client) -> list[dict]` | Dump all BusinessConcept + PhysicalTable nodes |

---

## 4. Full Implementation

```python
"""Hybrid retriever — dense vector + BM25 + graph traversal.

EP-12 / US-12-01 to US-12-04:
Retrieves candidate nodes from Neo4j for a given natural-language query,
then merges and deduplicates results before passing to the reranker.
"""

from __future__ import annotations

import logging
from typing import Any

from src.config.logging import get_logger
from src.config.settings import get_settings
from src.graph.neo4j_client import Neo4jClient
from src.models.schemas import RetrievedChunk
from src.retrieval.embeddings import embed_text

logger: logging.Logger = get_logger(__name__)


# ── Node Dump ──────────────────────────────────────────────────────────────────

def build_node_index(client: Neo4jClient) -> list[dict[str, Any]]:
    """Fetch all BusinessConcept and PhysicalTable nodes as plain dicts.

    This snapshot is kept in memory and used to build the BM25 token index at
    query-graph startup. It must be refreshed after each ingestion run.

    Args:
        client: Active ``Neo4jClient`` context.

    Returns:
        List of node property dicts with ``name``, ``node_type``, and other fields.
    """
    concept_records = client.execute_cypher(
        "MATCH (n:BusinessConcept) RETURN n.name AS name, "
        "n.definition AS definition, 'BusinessConcept' AS node_type, "
        "n.synonyms AS synonyms, n.source_doc AS source_doc"
    )
    table_records = client.execute_cypher(
        "MATCH (n:PhysicalTable) RETURN n.table_name AS name, "
        "'' AS definition, 'PhysicalTable' AS node_type, "
        "[] AS synonyms, n.source_doc AS source_doc, "
        "n.column_names AS column_names"
    )
    all_nodes = concept_records + table_records
    logger.debug("build_node_index: %d nodes fetched.", len(all_nodes))
    return all_nodes


# ── Dense Vector Search ────────────────────────────────────────────────────────

def vector_search(
    query: str,
    client: Neo4jClient,
    top_k: int | None = None,
    model=None,
) -> list[RetrievedChunk]:
    """Embed the query and run Neo4j vector index search on BusinessConcept nodes.

    Args:
        query:  Natural language query string.
        client: Active ``Neo4jClient``.
        top_k:  Number of results; defaults to ``settings.retrieval_vector_top_k``.
        model:  Optional pre-loaded FlagModel; passed to ``embed_text``.

    Returns:
        Sorted list of ``RetrievedChunk`` with ``source_type="vector"``.
    """
    settings = get_settings()
    k = top_k or settings.retrieval_vector_top_k
    query_vector: list[float] = embed_text(query, model=model)

    cypher = (
        "CALL db.index.vector.queryNodes('businessconcept_embedding', $k, $embedding) "
        "YIELD node, score "
        "RETURN node.name AS name, node.definition AS definition, "
        "score, 'BusinessConcept' AS node_type, "
        "node.source_doc AS source_doc, node.synonyms AS synonyms"
    )
    records = client.execute_cypher(cypher, {"k": k, "embedding": query_vector})

    chunks: list[RetrievedChunk] = []
    for rec in records:
        name = rec.get("name") or ""
        definition = rec.get("definition") or ""
        chunks.append(
            RetrievedChunk(
                node_id=name,
                node_type=rec.get("node_type", "BusinessConcept"),
                text=f"{name}: {definition}",
                score=float(rec.get("score", 0.0)),
                source_type="vector",
                metadata={k: v for k, v in rec.items() if k not in ("name", "definition", "score", "node_type")},
            )
        )
    logger.debug("vector_search: %d results for query '%s'.", len(chunks), query[:60])
    return chunks


# ── BM25 Keyword Search ────────────────────────────────────────────────────────

def _node_to_text(node: dict[str, Any]) -> str:
    """Flatten a node dict to a searchable string for BM25 tokenisation."""
    parts = [
        node.get("name") or "",
        node.get("definition") or "",
        " ".join(node.get("synonyms") or []),
        " ".join(node.get("column_names") or []),
    ]
    return " ".join(p for p in parts if p).lower()


def bm25_search(
    query: str,
    all_nodes: list[dict[str, Any]],
    top_k: int | None = None,
) -> list[RetrievedChunk]:
    """Keyword retrieval using BM25Okapi over a pre-built node text corpus.

    Args:
        query:     Natural language query string.
        all_nodes: Node dump from ``build_node_index``.
        top_k:     Number of results; defaults to ``settings.retrieval_bm25_top_k``.

    Returns:
        Sorted list of ``RetrievedChunk`` with ``source_type="bm25"``.
    """
    try:
        from rank_bm25 import BM25Okapi
    except ImportError as exc:
        raise ImportError("Install rank-bm25: pip install rank-bm25") from exc

    settings = get_settings()
    k = top_k or settings.retrieval_bm25_top_k

    if not all_nodes:
        return []

    corpus_texts: list[str] = [_node_to_text(n) for n in all_nodes]
    tokenised_corpus = [text.split() for text in corpus_texts]
    bm25 = BM25Okapi(tokenised_corpus)

    tokenised_query = query.lower().split()
    scores: list[float] = bm25.get_scores(tokenised_query).tolist()

    indexed = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:k]
    chunks: list[RetrievedChunk] = []
    for idx, score in indexed:
        node = all_nodes[idx]
        name = node.get("name") or ""
        definition = node.get("definition") or ""
        chunks.append(
            RetrievedChunk(
                node_id=name,
                node_type=node.get("node_type", "BusinessConcept"),
                text=f"{name}: {definition}",
                score=score,
                source_type="bm25",
                metadata={k: v for k, v in node.items() if k not in ("name", "definition")},
            )
        )
    logger.debug("bm25_search: %d results for query '%s'.", len(chunks), query[:60])
    return chunks


# ── Graph Traversal ────────────────────────────────────────────────────────────

def graph_traversal(
    seed_names: list[str],
    client: Neo4jClient,
    depth: int | None = None,
) -> list[RetrievedChunk]:
    """Expand seed node names to their graph neighbours via Cypher traversal.

    Args:
        seed_names: Node names to start traversal from.
        client:     Active ``Neo4jClient``.
        depth:      Hop depth; defaults to ``settings.retrieval_graph_depth`` (2).

    Returns:
        List of ``RetrievedChunk`` with ``source_type="graph"``.
    """
    settings = get_settings()
    d = depth or settings.retrieval_graph_depth

    if not seed_names:
        return []

    cypher = (
        f"MATCH (start)-[r*1..{d}]-(neighbor) "
        "WHERE start.name IN $seed_names "
        "RETURN neighbor.name AS name, "
        "COALESCE(neighbor.definition, neighbor.table_name, '') AS definition, "
        "labels(neighbor)[0] AS node_type, type(r[0]) AS rel_type "
        "LIMIT 20"
    )
    records = client.execute_cypher(cypher, {"seed_names": seed_names})

    seen: set[str] = set()
    chunks: list[RetrievedChunk] = []
    for rec in records:
        name = rec.get("name") or ""
        if name in seen or name in seed_names:
            continue
        seen.add(name)
        definition = rec.get("definition") or ""
        chunks.append(
            RetrievedChunk(
                node_id=name,
                node_type=rec.get("node_type", "Unknown"),
                text=f"{name}: {definition}",
                score=0.5,  # graph neighbours get a neutral baseline score
                source_type="graph",
                metadata={"rel_type": rec.get("rel_type")},
            )
        )
    logger.debug("graph_traversal: %d neighbours found.", len(chunks))
    return chunks


# ── Result Merging ─────────────────────────────────────────────────────────────

def merge_results(
    vector: list[RetrievedChunk],
    bm25: list[RetrievedChunk],
    graph: list[RetrievedChunk],
) -> list[RetrievedChunk]:
    """Deduplicate and merge retrieval results from all three strategies.

    Deduplication by ``node_id`` — keep the highest score per node across
    all sources. Graph traversal results are included even at lower scores.

    Args:
        vector: Results from ``vector_search``.
        bm25:   Results from ``bm25_search``.
        graph:  Results from ``graph_traversal``.

    Returns:
        Deduplicated list sorted by score descending.
    """
    best: dict[str, RetrievedChunk] = {}
    for chunk in vector + bm25 + graph:
        nid = chunk.node_id
        if nid not in best or chunk.score > best[nid].score:
            best[nid] = chunk
    merged = sorted(best.values(), key=lambda c: c.score, reverse=True)
    logger.debug("merge_results: %d unique nodes.", len(merged))
    return merged
```

---

## 5. Tests

```python
"""Unit tests for src/retrieval/hybrid_retriever.py — UT-19"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from src.models.schemas import RetrievedChunk
from src.retrieval.hybrid_retriever import (
    _node_to_text,
    bm25_search,
    graph_traversal,
    merge_results,
    vector_search,
)


# ── Helpers ────────────────────────────────────────────────────────────────────

def _chunk(name: str, score: float, source: str = "vector") -> RetrievedChunk:
    return RetrievedChunk(
        node_id=name, node_type="BusinessConcept",
        text=f"{name}: definition",
        score=score, source_type=source, metadata={},
    )


def _make_client(records: list[dict]) -> MagicMock:
    client = MagicMock()
    client.execute_cypher.return_value = records
    return client


# ── _node_to_text ──────────────────────────────────────────────────────────────

class TestNodeToText:
    def test_joins_fields(self) -> None:
        node = {"name": "Customer", "definition": "A buyer", "synonyms": ["Client"], "column_names": ["ID"]}
        text = _node_to_text(node)
        assert "customer" in text
        assert "buyer" in text
        assert "client" in text
        assert "id" in text

    def test_handles_missing_fields(self) -> None:
        node = {"name": "X"}
        text = _node_to_text(node)
        assert "x" in text


# ── vector_search ──────────────────────────────────────────────────────────────

class TestVectorSearch:
    def test_returns_retrieved_chunks(self) -> None:
        import numpy as np
        model = MagicMock()
        model.encode = MagicMock(return_value=np.zeros((1, 1024), dtype="float32"))
        client = _make_client([
            {"name": "Customer", "definition": "A buyer", "score": 0.95, "node_type": "BusinessConcept", "source_doc": "x.pdf", "synonyms": ["Client"]},
        ])
        results = vector_search("customer", client, top_k=5, model=model)
        assert len(results) == 1
        assert results[0].source_type == "vector"
        assert results[0].score == pytest.approx(0.95)

    def test_empty_results(self) -> None:
        import numpy as np
        model = MagicMock()
        model.encode = MagicMock(return_value=np.zeros((1, 1024), dtype="float32"))
        client = _make_client([])
        results = vector_search("nothing", client, top_k=5, model=model)
        assert results == []


# ── bm25_search ───────────────────────────────────────────────────────────────

class TestBm25Search:
    def _nodes(self) -> list[dict]:
        return [
            {"name": "Customer", "definition": "A person who buys goods", "synonyms": [], "column_names": [], "node_type": "BusinessConcept"},
            {"name": "Product",  "definition": "A sellable item in the inventory", "synonyms": ["Item"], "column_names": [], "node_type": "BusinessConcept"},
            {"name": "Order",    "definition": "A purchase transaction",            "synonyms": [], "column_names": [], "node_type": "BusinessConcept"},
        ]

    def test_top_result_is_most_relevant(self) -> None:
        results = bm25_search("customer buying goods", self._nodes(), top_k=3)
        assert results[0].node_id == "Customer"

    def test_returns_source_type_bm25(self) -> None:
        results = bm25_search("product", self._nodes(), top_k=1)
        assert results[0].source_type == "bm25"

    def test_empty_nodes_returns_empty(self) -> None:
        assert bm25_search("query", [], top_k=5) == []

    def test_top_k_respected(self) -> None:
        results = bm25_search("purchase", self._nodes(), top_k=1)
        assert len(results) <= 1


# ── graph_traversal ───────────────────────────────────────────────────────────

class TestGraphTraversal:
    def test_returns_neighbours(self) -> None:
        client = _make_client([
            {"name": "Order", "definition": "A purchase", "node_type": "BusinessConcept", "rel_type": "RELATED_TO"},
        ])
        results = graph_traversal(["Customer"], client, depth=2)
        assert len(results) == 1
        assert results[0].source_type == "graph"

    def test_empty_seeds_returns_empty(self) -> None:
        client = _make_client([])
        assert graph_traversal([], client) == []

    def test_excludes_seed_names_from_results(self) -> None:
        client = _make_client([
            {"name": "Customer", "definition": "loop node", "node_type": "BC", "rel_type": "SELF"},
        ])
        results = graph_traversal(["Customer"], client, depth=1)
        assert all(r.node_id != "Customer" for r in results)


# ── merge_results ──────────────────────────────────────────────────────────────

class TestMergeResults:
    def test_deduplicates_by_node_id(self) -> None:
        v = [_chunk("Customer", 0.9, "vector")]
        b = [_chunk("Customer", 0.7, "bm25")]
        g = [_chunk("Order", 0.5, "graph")]
        merged = merge_results(v, b, g)
        names = [c.node_id for c in merged]
        assert names.count("Customer") == 1

    def test_keeps_highest_score(self) -> None:
        v = [_chunk("Customer", 0.9, "vector")]
        b = [_chunk("Customer", 0.7, "bm25")]
        merged = merge_results(v, b, [])
        assert merged[0].score == pytest.approx(0.9)

    def test_sorted_descending(self) -> None:
        v = [_chunk("B", 0.6), _chunk("A", 0.9)]
        merged = merge_results(v, [], [])
        assert merged[0].node_id == "A"

    def test_empty_inputs(self) -> None:
        assert merge_results([], [], []) == []
```

---

## 6. Smoke Test

```bash
python -c "
from src.retrieval.hybrid_retriever import bm25_search, merge_results

nodes = [
    {'name': 'Customer', 'definition': 'A person who buys goods', 'synonyms': [], 'column_names': [], 'node_type': 'BusinessConcept'},
    {'name': 'Product',  'definition': 'An item for sale',         'synonyms': ['Item'], 'column_names': [], 'node_type': 'BusinessConcept'},
]
results = bm25_search('customer purchase', nodes, top_k=2)
print('BM25 top result:', results[0].node_id if results else 'none')

merged = merge_results(results, [], [])
print('Merged count:', len(merged))
print('hybrid_retriever smoke test passed.')
"
```
