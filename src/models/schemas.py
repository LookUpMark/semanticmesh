"""All Pydantic v2 data models for the thesis pipeline.

Implemented in one file so imports are always unambiguous.
Never define models inline in node functions — always import from here.
"""

from __future__ import annotations

from datetime import datetime  # noqa: TC003
from typing import Any, Literal

from pydantic import BaseModel, Field

# ── Ingestion ──────────────────────────────────────────────────────────────────


class Document(BaseModel):
    """A raw page or section extracted from a PDF."""

    text: str
    metadata: dict[str, str] = Field(default_factory=dict)
    # metadata keys: source (filename), page (int)


class Chunk(BaseModel):
    """A text chunk produced by RecursiveCharacterTextSplitter."""

    text: str
    chunk_index: int
    metadata: dict[str, str] = Field(default_factory=dict)
    # metadata keys: source, page, token_count


# ── Extraction ─────────────────────────────────────────────────────────────────


class Triplet(BaseModel):
    """A (subject, predicate, object) semantic fact + provenance."""

    subject: str
    predicate: str
    object: str
    provenance_text: str  # verbatim sentence from the source chunk
    confidence: float = Field(ge=0.0, le=1.0)
    source_chunk_index: int | None = None


class TripletExtractionResponse(BaseModel):
    """SLM JSON-mode output schema for triplet extraction."""

    triplets: list[Triplet]


# ── Entity Resolution ──────────────────────────────────────────────────────────


class EntityCluster(BaseModel):
    """A group of near-duplicate entity strings produced by vector blocking."""

    canonical_candidate: str  # most frequent / longest form
    variants: list[str]  # all near-duplicate strings in the cluster
    avg_similarity: float  # mean pairwise cosine similarity


class CanonicalEntityDecision(BaseModel):
    """LLM judge decision for a single EntityCluster."""

    merge: bool
    canonical_name: str
    reasoning: str  # one sentence — logged only, not used downstream


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
    references: str | None = None  # "other_table.col"
    comment: str | None = None


class TableSchema(BaseModel):
    """Parsed DDL output for a single SQL table."""

    table_name: str
    schema_name: str | None = None
    columns: list[ColumnSchema]
    ddl_source: str  # raw DDL string for this table
    comment: str | None = None


class EnrichedColumn(BaseModel):
    """Enriched column metadata produced by the LLM Schema Enrichment node."""

    original_name: str  # e.g. "CUST_ID" — never changed
    enriched_name: str  # e.g. "Customer ID" — human-readable


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
    def from_table_schema(cls, table: TableSchema) -> EnrichedTableSchema:
        """Promote a TableSchema to EnrichedTableSchema with empty enrichment fields."""
        return cls(**table.model_dump())


# ── Mapping ────────────────────────────────────────────────────────────────────


class MappingProposal(BaseModel):
    """LLM proposal aligning a PhysicalTable to a BusinessConcept."""

    table_name: str
    mapped_concept: str | None  # null if no mapping found
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
    params: dict[str, Any] = Field(default_factory=dict)
    mapping_id: str  # "{table_name}__{concept_name}"


# ── Retrieval ──────────────────────────────────────────────────────────────────


class RetrievedChunk(BaseModel):
    """A context chunk returned by any retrieval method."""

    node_id: str
    node_type: str  # "BusinessConcept" | "PhysicalTable"
    text: str  # formatted as "name: definition"
    score: float
    source_type: Literal["vector", "bm25", "graph"]
    metadata: dict[str, Any] = Field(default_factory=dict)
    reranker_score: float | None = None


# ── Generation ────────────────────────────────────────────────────────────────


class GraderDecision(BaseModel):
    """Hallucination Grader verdict."""

    grounded: bool
    critique: str | None = None
    action: Literal["pass", "regenerate", "web_search"]
    timeout_occurred: bool = False
    parse_attempts: int = 1
    consistency_corrections: int = 0
    certainty: float = Field(default=0.5, ge=0.0, le=1.0)


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
    failed_samples: list[dict[str, Any]] = Field(default_factory=list)
