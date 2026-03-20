"""LangGraph state schemas for builder_graph and query_graph.

Both use TypedDict (not Pydantic) so LangGraph can serialise them
with its built-in reducers. Use Optional / `| None` instead of
Field(default=...) here.
"""

from __future__ import annotations

from typing import TypedDict

from src.models.schemas import (
    Chunk,
    Document,
    EnrichedTableSchema,
    Entity,
    GraderDecision,
    MappingProposal,
    RetrievedChunk,
    TableSchema,
    Triplet,
)


class BuilderState(TypedDict, total=False):
    """Mutable state flowing through the Knowledge Graph Builder graph."""

    # Entry-point inputs
    ddl_paths: list[str]
    source_doc: str
    use_lazy_extraction: bool

    # Ingestion
    documents: list[Document]
    chunks: list[Chunk]

    # Extraction + Entity Resolution
    triplets: list[Triplet]
    entities: list[Entity]  # canonical, post-ER

    # Schema parsing
    tables: list[TableSchema]  # raw DDL output
    enriched_tables: list[EnrichedTableSchema]

    # Mapping (queue-based, one table at a time)
    pending_tables: list[EnrichedTableSchema]
    current_table: EnrichedTableSchema | None
    current_entities: list[Entity]
    mapping_proposal: MappingProposal | None
    best_proposal: MappingProposal | None  # highest-confidence proposal seen so far
    reflection_prompt: str | None
    reflection_attempts: int

    # Cypher
    current_cypher: str | None
    healing_attempts: int
    cypher_failed: bool

    # Control
    hitl_flag: bool
    skip_hitl: bool  # True in non-production runs — bypasses interrupt()
    failed_mappings: list[str]
    ingestion_errors: list[str]
    completed_tables: list[str]


class QueryState(TypedDict, total=False):
    """Mutable state flowing through the Query/Answer graph."""

    # Input (set once, never mutated)
    user_query: str

    # Retrieval
    retrieved_chunks: list[RetrievedChunk]
    reranked_chunks: list[RetrievedChunk]

    # Generation + grading
    current_answer: str
    last_critique: str | None
    grader_decision: GraderDecision | None
    generation_chunks: list[RetrievedChunk]

    # Output
    final_answer: str
    sources: list[str]
    retrieved_contexts: list[str]  # full texts of reranked chunks — used by RAGAS evaluation
    retrieval_quality_score: float
    retrieval_chunk_count: int
    retrieval_filtered_by_threshold: bool
    context_sufficiency: str  # "insufficient" | "sparse" | "adequate"
    retrieval_gate_decision: str  # "proceed" | "proceed_with_warning" | "abstain_early"
    semantic_verification_overlap: float
    semantic_verification_passed: bool
    semantic_verification_warning: str | None
    grader_consistency_valid: bool
    grader_rejection_count: int

    # Control
    iteration_count: int
