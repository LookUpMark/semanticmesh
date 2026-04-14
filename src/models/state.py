"""LangGraph state schemas for builder_graph and query_graph."""

from __future__ import annotations

from typing import Annotated, Any, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

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

    ddl_paths: list[str]
    source_doc: str
    use_lazy_extraction: bool
    documents: list[Document]
    chunks: list[Chunk]
    triplets: list[Triplet]
    entities: list[Entity]
    tables: list[TableSchema]
    enriched_tables: list[EnrichedTableSchema]
    pending_tables: list[EnrichedTableSchema]
    current_table: EnrichedTableSchema | None
    current_entities: list[Entity]
    mapping_proposal: MappingProposal | None
    best_proposal: MappingProposal | None
    reflection_prompt: str | None
    reflection_attempts: int
    current_cypher: str | None
    healing_attempts: int
    cypher_failed: bool
    hitl_flag: bool
    skip_hitl: bool
    failed_mappings: list[str]
    ingestion_errors: list[str]
    completed_tables: list[str]
    skipped_files: list[str]

    # Debug tracing fields (use Any to avoid circular imports)
    trace_enabled: bool
    builder_trace: Any  # BuilderTrace | None at runtime
    trace_output_dir: str


class QueryState(TypedDict, total=False):
    """Mutable state flowing through the Query/Answer graph."""

    # ── Conversation memory (LangGraph-native: add_messages reducer) ─────────
    # Accumulates across checkpoints keyed by thread_id (= session_id).
    # Each turn appends HumanMessage (initial state) + AIMessage (_node_finalise).
    messages: Annotated[list[BaseMessage], add_messages]

    user_query: str
    retrieved_chunks: list[RetrievedChunk]
    reranked_chunks: list[RetrievedChunk]
    generation_chunks: list[RetrievedChunk]
    current_answer: str
    last_critique: str | None
    grader_decision: GraderDecision | None
    final_answer: str
    sources: list[str]
    entity_names: list[str]
    retrieved_contexts: list[str]
    retrieval_quality_score: float
    retrieval_chunk_count: int
    retrieval_filtered_by_threshold: bool
    context_sufficiency: str
    retrieval_gate_decision: str
    grader_consistency_valid: bool
    grader_rejection_count: int
    iteration_count: int

    # Debug tracing fields (use Any to avoid circular imports)
    query_trace_enabled: bool
    query_trace: Any  # QueryTrace | None at runtime
    query_index: int
    builder_trace_id: str
