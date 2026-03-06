# Part 2 — `src/models/schemas.py`

## 1. Purpose & Context

**Epic:** EP-06 data models  
**US:** REQUIREMENTS.md §6 — Data Models & Schemas

Defines every Pydantic v2 model used across the entire pipeline. Implemented **all at once** (step 3 in the implementation order) so that every subsequent module can import types without circular dependencies. No LLM logic here — pure data modelling.

---

## 2. Prerequisites

- `pyproject.toml` with `pydantic>=2.7` installed (step 1)

---

## 3. Public API — Model Inventory

| Group | Model | Used by |
|---|---|---|
| Ingestion | `Document`, `Chunk` | `pdf_loader`, `triplet_extractor` |
| Extraction | `Triplet`, `TripletExtractionResponse` | `triplet_extractor` |
| Entity Resolution | `EntityCluster`, `CanonicalEntityDecision`, `Entity` | `blocking`, `llm_judge`, `entity_resolver` |
| Schema | `ColumnSchema`, `TableSchema`, `EnrichedColumn`, `EnrichedTableSchema` | `ddl_parser`, `schema_enricher` |
| Mapping | `MappingProposal`, `CriticDecision`, `MappingExample` | `rag_mapper`, `validator` |
| Cypher | `CypherExample`, `CypherStatement` | `cypher_generator` |
| Retrieval | `RetrievedChunk` | `hybrid_retriever`, `reranker` |
| Generation | `GraderDecision` | `hallucination_grader` |
| Evaluation | `EvaluationReport` | `ragas_runner` |

---

## 4. Full Implementation

```python
"""All Pydantic v2 data models for the thesis pipeline.

Implemented in one file so imports are always unambiguous.
Never define models inline in node functions — always import from here.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


# ── Ingestion ──────────────────────────────────────────────────────────────────

class Document(BaseModel):
    """A raw page or section extracted from a PDF."""
    text: str
    metadata: dict = Field(default_factory=dict)
    # metadata keys: source (filename), page (int)


class Chunk(BaseModel):
    """A text chunk produced by RecursiveCharacterTextSplitter."""
    text: str
    chunk_index: int
    metadata: dict = Field(default_factory=dict)
    # metadata keys: source, page, token_count


# ── Extraction ─────────────────────────────────────────────────────────────────

class Triplet(BaseModel):
    """A (subject, predicate, object) semantic fact + provenance."""
    subject: str
    predicate: str
    object: str
    provenance_text: str          # verbatim sentence from the source chunk
    confidence: float = Field(ge=0.0, le=1.0)
    source_chunk_index: int | None = None


class TripletExtractionResponse(BaseModel):
    """SLM JSON-mode output schema for triplet extraction."""
    triplets: list[Triplet]


# ── Entity Resolution ──────────────────────────────────────────────────────────

class EntityCluster(BaseModel):
    """A group of near-duplicate entity strings produced by vector blocking."""
    canonical_candidate: str      # most frequent / longest form
    variants: list[str]           # all near-duplicate strings in the cluster
    avg_similarity: float         # mean pairwise cosine similarity


class CanonicalEntityDecision(BaseModel):
    """LLM judge decision for a single EntityCluster."""
    merge: bool
    canonical_name: str
    reasoning: str                # one sentence — logged only, not used downstream


class Entity(BaseModel):
    """A resolved, canonical business concept ready for RAG Mapping."""
    name: str
    definition: str
    synonyms: list[str] = Field(default_factory=list)
    provenance_text: str
    source_doc: str
    embedding: list[float] | None = None


# ── Schema Parsing ─────────────────────────────────────────────────────────────

class ColumnSchema(BaseModel):
    """Metadata for a single DDL column."""
    name: str
    data_type: str
    is_primary_key: bool = False
    is_foreign_key: bool = False
    references: str | None = None   # "other_table.col"
    comment: str | None = None


class TableSchema(BaseModel):
    """Parsed DDL output for a single SQL table."""
    table_name: str
    schema_name: str | None = None
    columns: list[ColumnSchema]
    ddl_source: str                 # raw DDL string for this table
    comment: str | None = None


class EnrichedColumn(BaseModel):
    """Enriched column metadata produced by the LLM Schema Enrichment node."""
    original_name: str              # e.g. "CUST_ID" — never changed
    enriched_name: str              # e.g. "Customer ID" — human-readable


class EnrichedTableSchema(TableSchema):
    """TableSchema extended with LLM-generated human-readable names and description.

    Inherits all fields from ``TableSchema`` (table_name, schema_name, columns,
    ddl_source, comment) so it is Liskov-substitutable wherever TableSchema is
    expected — avoids mypy --strict errors at call sites that accept either type.
    """
    # Enrichment-only fields (TableSchema fields are inherited)
    enriched_table_name: str | None = None
    enriched_columns: list[EnrichedColumn] = Field(default_factory=list)
    table_description: str | None = None

    @classmethod
    def from_table_schema(cls, table: TableSchema) -> "EnrichedTableSchema":
        """Promote a TableSchema to EnrichedTableSchema with empty enrichment fields."""
        return cls(**table.model_dump())


# ── Mapping ────────────────────────────────────────────────────────────────────

class MappingProposal(BaseModel):
    """LLM proposal aligning a PhysicalTable to a BusinessConcept."""
    table_name: str
    mapped_concept: str | None        # null if no mapping found
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str
    alternative_concepts: list[str] = Field(default_factory=list)


class CriticDecision(BaseModel):
    """LLM critic verdict on a MappingProposal."""
    approved: bool
    critique: str | None = None
    suggested_correction: str | None = None


class MappingExample(BaseModel):
    """A few-shot mapping example injected into the MAPPING_USER prompt."""
    ddl_snippet: str
    concept_name: str
    concept_definition: str
    cypher: str


# ── Cypher ─────────────────────────────────────────────────────────────────────

class CypherExample(BaseModel):
    """A few-shot Cypher generation example injected into the CYPHER_USER prompt."""
    description: str
    ddl_snippet: str
    concept_name: str
    cypher: str


class CypherStatement(BaseModel):
    """A validated Cypher MERGE statement ready for Neo4j execution."""
    cypher: str
    params: dict = Field(default_factory=dict)
    mapping_id: str                    # "{table_name}__{concept_name}"


# ── Retrieval ──────────────────────────────────────────────────────────────────

class RetrievedChunk(BaseModel):
    """A context chunk returned by any retrieval method."""
    node_id: str
    node_type: str                     # "BusinessConcept" | "PhysicalTable"
    text: str                          # formatted as "name: definition"
    score: float
    source_type: Literal["vector", "bm25", "graph"]
    metadata: dict = Field(default_factory=dict)
    reranker_score: float | None = None


# ── Generation ────────────────────────────────────────────────────────────────

class GraderDecision(BaseModel):
    """Hallucination Grader verdict."""
    grounded: bool
    critique: str | None = None
    action: Literal["pass", "regenerate", "web_search"]


# ── Evaluation ────────────────────────────────────────────────────────────────

class EvaluationReport(BaseModel):
    """RAGAS + system-specific evaluation results for one run."""
    timestamp: datetime
    num_samples: int
    faithfulness: float
    context_precision: float
    context_recall: float
    answer_relevancy: float
    cypher_healing_rate: float
    hitl_confidence_agreement: float
    failed_samples: list[dict] = Field(default_factory=list)
```

---

## 5. Tests

**File:** `tests/unit/test_prompts.py` contains schema validation. Add a dedicated `test_schemas.py`:

```python
"""Unit tests for src/models/schemas.py"""

import pytest
from pydantic import ValidationError

from src.models.schemas import (
    CanonicalEntityDecision,
    Chunk,
    ColumnSchema,
    CriticDecision,
    Document,
    EnrichedTableSchema,
    Entity,
    EntityCluster,
    EvaluationReport,
    GraderDecision,
    MappingProposal,
    RetrievedChunk,
    TableSchema,
    Triplet,
    TripletExtractionResponse,
)


class TestTriplet:
    def test_valid_triplet(self) -> None:
        t = Triplet(
            subject="Customer",
            predicate="purchases",
            object="Product",
            provenance_text="A Customer purchases Products.",
            confidence=0.9,
        )
        assert t.confidence == 0.9

    def test_confidence_clamp_min(self) -> None:
        with pytest.raises(ValidationError):
            Triplet(subject="a", predicate="b", object="c",
                    provenance_text="x", confidence=-0.1)

    def test_confidence_clamp_max(self) -> None:
        with pytest.raises(ValidationError):
            Triplet(subject="a", predicate="b", object="c",
                    provenance_text="x", confidence=1.1)


class TestMappingProposal:
    def test_null_concept_allowed(self) -> None:
        p = MappingProposal(
            table_name="SYS_AUDIT_LOG",
            mapped_concept=None,
            confidence=0.0,
            reasoning="System table.",
        )
        assert p.mapped_concept is None

    def test_confidence_out_of_range(self) -> None:
        with pytest.raises(ValidationError):
            MappingProposal(
                table_name="T", mapped_concept="C", confidence=1.5, reasoning="x"
            )


class TestEnrichedTableSchema:
    def test_from_table_schema(self) -> None:
        ts = TableSchema(
            table_name="TB_CUST",
            columns=[ColumnSchema(name="CUST_ID", data_type="INT", is_primary_key=True)],
            ddl_source="CREATE TABLE TB_CUST (CUST_ID INT PRIMARY KEY);",
        )
        ets = EnrichedTableSchema.from_table_schema(ts)
        assert ets.table_name == "TB_CUST"
        assert ets.enriched_table_name is None
        assert ets.enriched_columns == []


class TestGraderDecision:
    def test_valid_actions(self) -> None:
        for action in ("pass", "regenerate", "web_search"):
            d = GraderDecision(grounded=action == "pass", action=action)  # type: ignore[arg-type]
            assert d.action == action

    def test_invalid_action(self) -> None:
        with pytest.raises(ValidationError):
            GraderDecision(grounded=False, action="retry")  # type: ignore[arg-type]


class TestRetrievedChunk:
    def test_valid_source_types(self) -> None:
        for src in ("vector", "bm25", "graph"):
            r = RetrievedChunk(
                node_id="1", node_type="BusinessConcept",
                text="hello", score=0.5, source_type=src,  # type: ignore[arg-type]
            )
            assert r.source_type == src
```

---

## 6. Smoke Test

```bash
python -c "
from src.models.schemas import Triplet, MappingProposal, GraderDecision, EnrichedTableSchema
print('All schema imports OK')
t = Triplet(subject='A', predicate='b', object='C', provenance_text='A b C.', confidence=0.9)
print(f'Triplet: {t.subject} {t.predicate} {t.object}')
"
```
