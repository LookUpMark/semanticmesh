# Part 5 — `src/mapping/rag_mapper.py`

## 1. Purpose & Context

**Epic:** EP-06 RAG Semantic Mapping  
**US-06-01** — Contextual Retrieval per Table, **US-06-02** — Mapping Proposal Generation

For each physical table, retrieves the most relevant business entities using a Map-Reduce RAG pattern (one retrieval + one LLM call per table), then produces a `MappingProposal`. Few-shot examples from the validated example bank are injected to guide the LLM toward the expected output format.

---

## 2. Prerequisites

- `src/models/schemas.py` — `TableSchema`, `EnrichedTableSchema`, `Entity`, `MappingProposal`, `MappingExample` (step 3)
- `src/prompts/templates.py` — `MAPPING_SYSTEM`, `MAPPING_USER` (step 7)
- `src/prompts/few_shot.py` — `load_mapping_examples`, `format_mapping_examples` (step 8)
- `src/config/logging.py` — `get_logger`, `NodeTimer`

---

## 3. Public API

| Symbol | Signature | Description |
|---|---|---|
| `build_retrieval_query` | `(table: EnrichedTableSchema) -> str` | Constructs a text query from enriched table metadata |
| `retrieve_top_entities` | `(query: str, entities: list[Entity], embeddings: Embeddings, top_k: int) -> list[Entity]` | Returns the `top_k` most similar entities to the query |
| `propose_mapping` | `(table: TableSchema, entities: list[Entity], llm: LLMProtocol, few_shot_examples: str) -> MappingProposal` | Calls LLM; returns `MappingProposal` |

---

## 4. Full Implementation

```python
"""RAG Semantic Mapping node.

EP-06: Map-Reduce RAG — for each physical table, retrieve relevant business
concepts via embedding similarity, then call the LLM to propose a mapping.
"""

from __future__ import annotations

import json
import logging

import numpy as np
from langchain_core.embeddings import Embeddings
from langchain_core.messages import HumanMessage, SystemMessage

from src.config.llm_client import LLMProtocol
from pydantic import ValidationError
from sklearn.metrics.pairwise import cosine_similarity

from src.config.logging import NodeTimer, get_logger
from src.config.settings import get_settings
from src.models.schemas import (
    Entity,
    EnrichedTableSchema,
    MappingExample,
    MappingProposal,
    TableSchema,
)
from src.prompts.templates import MAPPING_SYSTEM, MAPPING_USER

logger: logging.Logger = get_logger(__name__)
_settings = get_settings()


def build_retrieval_query(table: EnrichedTableSchema) -> str:
    """Construct a dense retrieval query from enriched table metadata.

    Priority order for metadata:
    1. enriched_table_name + table_description (if available)
    2. Fallback to original table_name + column names

    The richer this query, the better the embedding similarity with business
    concepts defined in natural language.

    Args:
        table: EnrichedTableSchema (may have enrichment fields as None if
               enrichment failed — graceful degradation).

    Returns:
        A plain-text query string for embedding.
    """
    parts: list[str] = []

    # Prefer enriched name + description
    if table.enriched_table_name:
        parts.append(table.enriched_table_name)
    else:
        parts.append(table.table_name)

    if table.table_description:
        parts.append(table.table_description)

    # Add enriched column names if available
    if table.enriched_columns:
        col_names = [ec.enriched_name for ec in table.enriched_columns]
    else:
        col_names = [c.name for c in table.columns if not c.is_primary_key]

    parts.append(", ".join(col_names[:10]))  # cap at 10 columns
    return " | ".join(parts)


def retrieve_top_entities(
    query: str,
    entities: list[Entity],
    embeddings: Embeddings,
    top_k: int | None = None,
) -> list[Entity]:
    """Retrieve the most semantically relevant entities for a given table query.

    Constructs embedding text for each entity as ``"{name}: {definition}"``.
    Uses cosine similarity against the query embedding.

    Args:
        query: Plain-text retrieval query (from ``build_retrieval_query``).
        entities: All canonical entities from entity resolution.
        embeddings: Embedding model (BGE-M3).
        top_k: Maximum number of entities to return.
               Defaults to ``settings.retrieval_vector_top_k``.

    Returns:
        Top-k most similar ``Entity`` objects, sorted by descending similarity.
    """
    k = top_k if top_k is not None else _settings.retrieval_vector_top_k
    if not entities:
        return []

    query_vec = np.array(embeddings.embed_query(query), dtype=np.float32).reshape(1, -1)

    entity_texts = [f"{e.name}: {e.definition}" if e.definition else e.name for e in entities]
    entity_vecs = np.array(embeddings.embed_documents(entity_texts), dtype=np.float32)

    sims = cosine_similarity(query_vec, entity_vecs)[0]
    top_indices = np.argsort(sims)[::-1][:k]

    return [entities[i] for i in top_indices]


def propose_mapping(
    table: TableSchema,
    entities: list[Entity],
    llm: LLMProtocol,
    few_shot_examples: str = "",
    reflection_prompt: str | None = None,
) -> MappingProposal:
    """Call the LLM to propose a semantic mapping for a single table.

    Args:
        table: The physical table (raw or enriched — both work).
        entities: The pre-retrieved subset of business entities (top-k).
        llm: Reasoning LLM (temperature=0.0).
        few_shot_examples: Formatted string from ``format_mapping_examples``
                           to inject into ``MAPPING_USER``.
        reflection_prompt: Optional Reflection Prompt critique from the validator;
                           prepended to ``few_shot_examples`` on retry calls.

    Returns:
        A validated ``MappingProposal``.  On any failure, returns a
        conservative ``MappingProposal`` with ``mapped_concept=None``
        and ``confidence=0.0`` — never crashes the pipeline.
    """
    entities_json = json.dumps(
        [
            {
                "name": e.name,
                "definition": e.definition,
                "synonyms": e.synonyms,
                "provenance_text": e.provenance_text[:300],
            }
            for e in entities
        ]
    )
    # Prepend reflection critique when this is a retry call
    effective_few_shot = (
        f"[REFLECTION CRITIQUE — correct the following error before generating]\n"
        f"{reflection_prompt}\n\n{few_shot_examples}"
        if reflection_prompt
        else few_shot_examples
    )
    user_prompt = MAPPING_USER.format(
        few_shot_examples=effective_few_shot,
        table_ddl=table.ddl_source,
        entities_json=entities_json,
    )

    with NodeTimer() as timer:
        try:
            response = llm.invoke(
                [
                    SystemMessage(content=MAPPING_SYSTEM),
                    HumanMessage(content=user_prompt),
                ]
            )
            raw_json: str = response.content.strip()
        except Exception as exc:
            logger.warning(
                "LLM mapping call failed for table '%s': %s — returning null mapping.",
                table.table_name, exc,
            )
            return MappingProposal(
                table_name=table.table_name,
                mapped_concept=None,
                confidence=0.0,
                reasoning=f"LLM call failed: {exc}",
            )

    logger.debug(
        "Mapping LLM call for '%s' completed in %.0f ms",
        table.table_name, timer.elapsed_ms,
    )

    # Parse and validate
    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError:
        logger.warning("Non-JSON mapping response for '%s'", table.table_name)
        return MappingProposal(
            table_name=table.table_name, mapped_concept=None, confidence=0.0,
            reasoning="JSON parse error.",
        )

    try:
        proposal = MappingProposal(**data)
    except ValidationError as exc:
        logger.warning("Pydantic validation error for mapping of '%s': %s", table.table_name, exc)
        return MappingProposal(
            table_name=table.table_name, mapped_concept=None, confidence=0.0,
            reasoning=f"Pydantic validation error: {exc}",
        )

    logger.info(
        "Proposed mapping: '%s' → '%s' (confidence=%.2f)",
        table.table_name, proposal.mapped_concept, proposal.confidence,
    )
    return proposal
```

---

## 5. Tests

```python
"""Unit tests for src/mapping/rag_mapper.py — UT-07"""

from __future__ import annotations

import json
from unittest.mock import MagicMock

import numpy as np
import pytest

from src.mapping.rag_mapper import (
    build_retrieval_query,
    propose_mapping,
    retrieve_top_entities,
)
from src.models.schemas import (
    ColumnSchema,
    EnrichedColumn,
    EnrichedTableSchema,
    Entity,
    MappingProposal,
    TableSchema,
)


def _make_table(name: str = "TB_CST") -> TableSchema:
    return TableSchema(
        table_name=name,
        columns=[ColumnSchema(name="ID", data_type="INT", is_primary_key=True)],
        ddl_source=f"CREATE TABLE {name} (ID INT PRIMARY KEY);",
    )


def _make_enriched(name: str = "TB_CST") -> EnrichedTableSchema:
    base = _make_table(name)
    e = EnrichedTableSchema.from_table_schema(base)
    e.enriched_table_name = "Customer Table"
    e.table_description = "Stores customer records."
    e.enriched_columns = [EnrichedColumn(original_name="ID", enriched_name="Customer ID")]
    return e


def _make_entity(name: str, definition: str = "") -> Entity:
    return Entity(
        name=name, definition=definition, synonyms=[],
        provenance_text="", source_doc="test.pdf",
    )


def _make_llm_proposal(table_name: str, concept: str, confidence: float) -> MagicMock:
    llm = MagicMock()
    resp = MagicMock()
    resp.content = json.dumps({
        "table_name": table_name,
        "mapped_concept": concept,
        "confidence": confidence,
        "reasoning": "test reasoning",
        "alternative_concepts": [],
    })
    llm.invoke.return_value = resp
    return llm


# ── build_retrieval_query ──────────────────────────────────────────────────────

class TestBuildRetrievalQuery:
    def test_uses_enriched_name_when_available(self) -> None:
        table = _make_enriched("TB_CST")
        query = build_retrieval_query(table)
        assert "Customer Table" in query

    def test_fallback_to_original_name(self) -> None:
        table = EnrichedTableSchema.from_table_schema(_make_table("TB_CST"))
        query = build_retrieval_query(table)
        assert "TB_CST" in query

    def test_includes_description(self) -> None:
        table = _make_enriched()
        query = build_retrieval_query(table)
        assert "Stores customer records" in query


# ── retrieve_top_entities ──────────────────────────────────────────────────────

class TestRetrieveTopEntities:
    def _make_embeddings(self, query_vec: list, entity_vecs: list[list]) -> MagicMock:
        emb = MagicMock()
        emb.embed_query.return_value = query_vec
        emb.embed_documents.return_value = entity_vecs
        return emb

    def test_returns_top_k(self) -> None:
        entities = [_make_entity(f"E{i}") for i in range(5)]
        emb = self._make_embeddings([1, 0], [[1, 0]] * 5)
        result = retrieve_top_entities("query", entities, emb, top_k=3)
        assert len(result) == 3

    def test_empty_entities_returns_empty(self) -> None:
        emb = MagicMock()
        result = retrieve_top_entities("query", [], emb, top_k=5)
        assert result == []

    def test_most_similar_entity_is_first(self) -> None:
        entities = [
            _make_entity("Customer"),   # vec [1,0] → sim=1.0
            _make_entity("Product"),    # vec [0,1] → sim=0.0
        ]
        emb = self._make_embeddings([1, 0], [[1, 0], [0, 1]])
        result = retrieve_top_entities("query", entities, emb, top_k=2)
        assert result[0].name == "Customer"


# ── propose_mapping ───────────────────────────────────────────────────────────

class TestProposeMapping:
    def test_happy_path_returns_proposal(self) -> None:
        table = _make_table("TB_CST")
        entities = [_make_entity("Customer", "A person who buys things.")]
        llm = _make_llm_proposal("TB_CST", "Customer", 0.95)
        result = propose_mapping(table, entities, llm)
        assert isinstance(result, MappingProposal)
        assert result.mapped_concept == "Customer"
        assert result.confidence == 0.95

    def test_llm_error_returns_null_mapping(self) -> None:
        table = _make_table()
        llm = MagicMock()
        llm.invoke.side_effect = RuntimeError("server error")
        result = propose_mapping(table, [], llm)
        assert result.mapped_concept is None
        assert result.confidence == 0.0

    def test_invalid_json_returns_null_mapping(self) -> None:
        table = _make_table()
        llm = MagicMock()
        resp = MagicMock()
        resp.content = "not json"
        llm.invoke.return_value = resp
        result = propose_mapping(table, [], llm)
        assert result.mapped_concept is None
```

---

## 6. Smoke Test

```bash
python -c "
from src.mapping.rag_mapper import build_retrieval_query
from src.models.schemas import EnrichedTableSchema, ColumnSchema, TableSchema

ts = TableSchema(
    table_name='CUSTOMER_MASTER',
    columns=[ColumnSchema(name='CUST_ID', data_type='INT', is_primary_key=True)],
    ddl_source='CREATE TABLE CUSTOMER_MASTER (CUST_ID INT PRIMARY KEY);'
)
ets = EnrichedTableSchema.from_table_schema(ts)
ets.enriched_table_name = 'Customer Master'
ets.table_description = 'Stores customer identity data.'
print('Query:', build_retrieval_query(ets))
"
```
