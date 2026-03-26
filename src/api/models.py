"""Pydantic request/response models for both REST APIs."""
from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


# ── Ablation API ──────────────────────────────────────────────────────────────

class AblationRunRequest(BaseModel):
    """Launch a custom ablation run with any combination of flags/hyperparameters."""

    dataset: str = Field(
        default="tests/fixtures/01_basics_ecommerce/gold_standard.json",
        description="Path to the gold_standard.json fixture to evaluate against.",
        examples=["tests/fixtures/02_intermediate_finance/gold_standard.json"],
    )
    study_id: str = Field(
        default="API-RUN",
        description="Output directory prefix under notebooks/ablation/ablation_results/.",
    )
    max_samples: int | None = Field(
        default=None, ge=1,
        description="Limit evaluation to the first N QA pairs (None = all).",
    )
    run_ragas: bool = Field(
        default=False,
        description="Enable RAGAS evaluation. Adds ~2-5 min per 15 samples.",
    )
    ragas_model: str = Field(
        default="gpt-4.1-mini",
        description="OpenAI model used as RAGAS evaluator.",
    )
    skip_builder: bool = Field(
        default=False,
        description="Skip Knowledge Graph build — reuse the existing Neo4j graph.",
    )
    lazy_extraction: bool = Field(
        default=False,
        description="Use rule-based heuristic extraction instead of LLM.",
    )

    # ── Ablation flags ────────────────────────────────────────────────────────
    retrieval_mode: Literal["hybrid", "vector", "bm25"] | None = Field(
        default=None, description="Retrieval channel combination. Default: hybrid.",
    )
    enable_reranker: bool | None = Field(
        default=None, description="Cross-encoder reranking (bge-reranker-v2-m3).",
    )
    reranker_top_k: int | None = Field(
        default=None, ge=1, le=50,
        description="Number of candidates kept after reranking.",
    )
    enable_hallucination_grader: bool | None = Field(
        default=None, description="Self-RAG hallucination grader.",
    )
    enable_cypher_healing: bool | None = Field(
        default=None, description="Cypher auto-fix loop on syntax errors.",
    )
    enable_critic_validation: bool | None = Field(
        default=None, description="Actor-Critic mapping validation.",
    )
    enable_schema_enrichment: bool | None = Field(
        default=None, description="LLM-based DDL acronym expansion.",
    )

    # ── Hyperparameters ───────────────────────────────────────────────────────
    chunk_size: int | None = Field(
        default=None, ge=64, le=2048,
        description="Child chunk token size for vector search.",
    )
    chunk_overlap: int | None = Field(
        default=None, ge=0, le=512,
        description="Child chunk overlap in tokens.",
    )
    parent_chunk_size: int | None = Field(
        default=None, ge=128, le=4096,
        description="Parent chunk token size returned verbatim to the LLM.",
    )
    er_similarity_threshold: float | None = Field(
        default=None, ge=0.0, le=1.0,
        description="Minimum cosine similarity for entity blocking.",
    )
    er_blocking_top_k: int | None = Field(
        default=None, ge=1, le=50,
        description="K-NN candidates per entity in ER blocking.",
    )
    confidence_threshold: float | None = Field(
        default=None, ge=0.0, le=1.0,
        description="Mapping confidence threshold below which HITL interrupt fires.",
    )
    retrieval_vector_top_k: int | None = Field(
        default=None, ge=1, le=100,
        description="Number of vector-search candidates before reranking.",
    )
    llm_max_tokens_extraction: int | None = Field(
        default=None, ge=512, le=32768,
        description="Max output tokens for the extraction LLM.",
    )


class AblationJobResponse(BaseModel):
    job_id: str
    status: Literal["queued", "running", "done", "failed"]
    study_id: str
    dataset: str


class AblationResultResponse(BaseModel):
    job_id: str
    status: Literal["queued", "running", "done", "failed"]
    study_id: str
    error: str | None = None
    summary: dict[str, Any] | None = Field(
        default=None,
        description="High-level metrics: questions, grounded, abstained, avg_score.",
    )
    ragas: dict[str, float] | None = Field(
        default=None,
        description="RAGAS metrics: faithfulness, answer_relevancy, context_precision, context_recall.",
    )
    per_question: list[dict[str, Any]] | None = None


class AblationMatrixEntry(BaseModel):
    study_id: str
    description: str
    env_overrides: dict[str, str]
    run_ragas: bool


# ── Demo / E2E API ────────────────────────────────────────────────────────────

class BuildRequest(BaseModel):
    """Trigger the Builder pipeline to ingest docs and populate the Knowledge Graph."""

    doc_paths: list[str] = Field(
        description="Paths to business documentation files (PDF, MD, TXT).",
        examples=[["tests/fixtures/01_basics_ecommerce/business_glossary.md",
                   "tests/fixtures/01_basics_ecommerce/data_dictionary.md"]],
    )
    ddl_paths: list[str] = Field(
        description="Paths to DDL SQL files to map onto the ontology.",
        examples=[["tests/fixtures/01_basics_ecommerce/schema.sql"]],
    )
    clear_graph: bool = Field(
        default=True,
        description="Wipe all Neo4j nodes/edges before building (recommended for clean runs).",
    )
    study_id: str = Field(default="demo")
    lazy_extraction: bool = Field(
        default=False,
        description="Use heuristic rule-based extraction instead of LLM (faster, less accurate).",
    )


class BuildResultResponse(BaseModel):
    job_id: str
    status: Literal["queued", "running", "done", "failed"]
    error: str | None = None
    triplets_extracted: int | None = None
    entities_resolved: int | None = None
    tables_parsed: int | None = None
    tables_completed: int | None = None
    parent_chunks: int | None = None
    child_chunks: int | None = None


class QueryRequest(BaseModel):
    """Query the Knowledge Graph with a natural-language question."""

    question: str = Field(
        description="Natural language question to answer from the Knowledge Graph.",
        examples=["What information is stored for each customer?",
                  "How are products and orders related?"],
    )


class QueryResponse(BaseModel):
    answer: str = Field(description="Generated answer grounded in the KG context.")
    sources: list[str] = Field(description="Node IDs of retrieved context chunks.")
    retrieval_quality_score: float = Field(description="Top reranker score (0-1).")
    retrieval_chunk_count: int = Field(description="Number of context chunks used.")
    gate_decision: str = Field(description="Retrieval gate decision: proceed | abstain_early.")
    grounded: bool = Field(description="Whether the answer is verifiably grounded in context.")
    context_previews: list[str] = Field(
        description="First 3 context chunks (first 300 chars each).",
    )


class PipelineRequest(BaseModel):
    """Run the complete E2E pipeline: build KG then answer questions."""

    doc_paths: list[str] = Field(
        description="Paths to business documentation files.",
        examples=[["tests/fixtures/01_basics_ecommerce/business_glossary.md"]],
    )
    ddl_paths: list[str] = Field(
        description="Paths to DDL SQL files.",
        examples=[["tests/fixtures/01_basics_ecommerce/schema.sql"]],
    )
    questions: list[str] = Field(
        min_length=1,
        description="One or more natural-language questions to answer after build.",
        examples=[["What information is stored for each customer?",
                   "How are products and orders related?"]],
    )
    clear_graph: bool = Field(default=True)
    lazy_extraction: bool = Field(default=False)
    run_ragas: bool = Field(
        default=False,
        description="Compute RAGAS faithfulness/AR/CP/CR (requires expected answers).",
    )
    study_id: str = Field(default="demo")


class PipelineJobResponse(BaseModel):
    job_id: str
    status: Literal["queued", "running", "done", "failed"]
    num_questions: int


class PipelineResultResponse(BaseModel):
    job_id: str
    status: Literal["queued", "running", "done", "failed"]
    error: str | None = None
    builder: BuildResultResponse | None = None
    answers: list[QueryResponse] | None = None
    ragas: dict[str, float] | None = None


class GraphStatsResponse(BaseModel):
    """Node and relationship counts for the current Neo4j Knowledge Graph."""

    business_concepts: int
    physical_tables: int
    parent_chunks: int
    child_chunks: int
    mentions_edges: int
    maps_to_edges: int
    total_nodes: int
    total_relationships: int
