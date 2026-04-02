"""Pydantic request/response models for both REST APIs."""

from __future__ import annotations

from typing import Any, Literal, TypeAlias

from pydantic import BaseModel, Field

# ── Shared LLM override fields ────────────────────────────────────────────────

_LLM_REASONING_DESC = (
    "Reasoning / generation model. Provider auto-detected from prefix:\n"
    "  - `openai/gpt-4.1` (OpenRouter) | `gpt-4.1` (OpenAI direct)\n"
    "  - `claude-3-5-sonnet-20241022` (Anthropic direct)\n"
    "  - `ollama/llama3.1` (Ollama — needs langchain-ollama or compat mode)\n"
    "  - `google/gemini-2.0-flash` or `gemini-2.0-flash` (Google Gemini)\n"
    "  - `bedrock/anthropic.claude-3-sonnet-20240229-v1:0` (AWS Bedrock)\n"
    "  - `groq/llama3-70b-8192` (Groq — OpenAI-compat, no extra package)\n"
    "  - `mistral/mistral-large-latest` (Mistral AI)\n"
    "  - `together/meta-llama/Llama-3-70b` (Together AI — OpenAI-compat)\n"
    "  - `deepseek/deepseek-chat` or `deepseek-chat` (DeepSeek)\n"
    "  - `xai/grok-2` or `grok-2` (xAI Grok — OpenAI-compat)\n"
    "  - `nvidia/meta/llama-3.1-70b-instruct` (Nvidia NIM — OpenAI-compat)\n"
    "Sets env var LLM_MODEL_REASONING for the pipeline run."
)
_LLM_EXTRACTION_DESC = (
    "Extraction model for triplet extraction. Same prefix conventions as reasoning_model. "
    "Sets env var LLM_MODEL_EXTRACTION."
)
_LLM_BASE_URL_DESC = (
    "Override base URL for local / custom OpenAI-compatible endpoints "
    "(Ollama, LMStudio, self-hosted Groq proxy, etc.). "
    "Sets env var PROVIDER_BASE_URL."
)


# ── Ablation API ──────────────────────────────────────────────────────────────


class CustomAblationRequest(BaseModel):
    """Launch a fully custom ablation run with any combination of flags/hyperparameters."""

    dataset: str = Field(
        default="tests/fixtures/01_basics_ecommerce/gold_standard.json",
        description="Path to the gold_standard.json fixture to evaluate against.",
        examples=["tests/fixtures/02_intermediate_finance/gold_standard.json"],
    )
    study_id: str = Field(
        default="custom-run",
        description="Output directory prefix under notebooks/ablation/ablation_results/.",
    )
    max_samples: int | None = Field(
        default=None,
        ge=1,
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
        default=None,
        description="Retrieval channel combination. Default: hybrid.",
    )
    enable_reranker: bool | None = Field(
        default=None,
        description="Cross-encoder reranking (bge-reranker-v2-m3).",
    )
    reranker_top_k: int | None = Field(
        default=None,
        ge=1,
        le=50,
        description="Number of candidates kept after reranking.",
    )
    enable_hallucination_grader: bool | None = Field(
        default=None,
        description="Self-RAG hallucination grader.",
    )
    enable_cypher_healing: bool | None = Field(
        default=None,
        description="Cypher auto-fix loop on syntax errors.",
    )
    enable_critic_validation: bool | None = Field(
        default=None,
        description="Actor-Critic mapping validation.",
    )
    enable_schema_enrichment: bool | None = Field(
        default=None,
        description="LLM-based DDL acronym expansion.",
    )

    # ── Hyperparameters ───────────────────────────────────────────────────────
    chunk_size: int | None = Field(
        default=None,
        ge=64,
        le=2048,
        description="Child chunk token size for vector search.",
    )
    chunk_overlap: int | None = Field(
        default=None,
        ge=0,
        le=512,
        description="Child chunk overlap in tokens.",
    )
    parent_chunk_size: int | None = Field(
        default=None,
        ge=128,
        le=4096,
        description="Parent chunk token size returned verbatim to the LLM.",
    )
    er_similarity_threshold: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Minimum cosine similarity for entity blocking.",
    )
    er_blocking_top_k: int | None = Field(
        default=None,
        ge=1,
        le=50,
        description="K-NN candidates per entity in ER blocking.",
    )
    confidence_threshold: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Mapping confidence threshold below which HITL interrupt fires.",
    )
    retrieval_vector_top_k: int | None = Field(
        default=None,
        ge=1,
        le=100,
        description="Number of vector-search candidates before reranking.",
    )
    llm_max_tokens_extraction: int | None = Field(
        default=16384,
        ge=512,
        le=32768,
        description="Max output tokens for the extraction LLM.",
    )

    # ── LLM model overrides ───────────────────────────────────────────────────
    reasoning_model: str | None = Field(
        default=None,
        description=_LLM_REASONING_DESC,
        examples=["groq/llama3-70b-8192", "gemini-2.0-flash", "ollama/llama3.1"],
    )
    extraction_model: str | None = Field(
        default=None,
        description=_LLM_EXTRACTION_DESC,
        examples=["groq/llama3-8b-8192", "ollama/qwen2.5-coder:7b"],
    )
    provider_base_url: str | None = Field(
        default=None,
        description=_LLM_BASE_URL_DESC,
        examples=["http://localhost:11434/v1", "http://localhost:1234/v1"],
    )


# Backward-compat alias — code that imports AblationRunRequest still works
AblationRunRequest: TypeAlias = CustomAblationRequest


class PresetAblationRequest(BaseModel):
    """Launch a predefined AB-XX ablation study.

    The study configuration (env overrides, feature flags) is automatically loaded
    from the ablation matrix — no need to specify individual flags.

    Use ``GET /ablation/matrix`` to browse all 21 predefined studies.
    """

    study_id: str = Field(
        description="Ablation study ID to run (e.g. 'AB-00', 'AB-03', 'AB-15').",
        examples=["AB-00", "AB-03", "AB-15"],
    )
    dataset: str = Field(
        default="tests/fixtures/01_basics_ecommerce/gold_standard.json",
        description="Path to the gold_standard.json fixture to evaluate against.",
        examples=["tests/fixtures/02_intermediate_finance/gold_standard.json"],
    )
    max_samples: int | None = Field(
        default=None,
        ge=1,
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

    # ── LLM model overrides (win over matrix defaults) ───────────────────────
    reasoning_model: str | None = Field(
        default=None,
        description=_LLM_REASONING_DESC,
        examples=["groq/llama3-70b-8192", "gemini-2.0-flash", "ollama/llama3.1"],
    )
    extraction_model: str | None = Field(
        default=None,
        description=_LLM_EXTRACTION_DESC,
        examples=["groq/llama3-8b-8192", "ollama/qwen2.5-coder:7b"],
    )
    provider_base_url: str | None = Field(
        default=None,
        description=_LLM_BASE_URL_DESC,
        examples=["http://localhost:11434/v1", "http://localhost:1234/v1"],
    )


class AblationJobResponse(BaseModel):
    job_id: str
    status: Literal["queued", "running", "done", "failed"]
    study_id: str
    dataset: str


class PresetAblationJobResponse(AblationJobResponse):
    """Extended job response for preset runs — includes matrix metadata."""

    description: str
    applied_env_overrides: dict[str, str]


class AblationResultResponse(BaseModel):
    job_id: str
    status: Literal["queued", "running", "done", "failed"]
    study_id: str
    error: str | None = None
    summary: dict[str, Any] | None = Field(
        default=None,
        description=(
            "Builder + query summary: triplets_extracted, entities_resolved, "
            "tables_parsed, tables_completed, cypher_failed, total_questions, "
            "grounded_count, grounded_rate, abstained_count, avg_gt_coverage, avg_top_score."
        ),
    )
    ragas: dict[str, float] | None = Field(
        default=None,
        description=(
            "RAGAS metrics: faithfulness, answer_relevancy, context_precision, context_recall."
        ),
    )
    per_question: list[dict[str, Any]] | None = Field(
        default=None,
        description="Per-question detailed results including answer, grounding, retrieval scores.",
    )
    bundle_path: str | None = Field(
        default=None,
        description="Path to the evaluation_bundle.json file for AI-as-Judge analysis.",
    )


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
        examples=[
            [
                "tests/fixtures/01_basics_ecommerce/business_glossary.txt",
                "tests/fixtures/01_basics_ecommerce/data_dictionary.txt",
            ]
        ],
    )
    ddl_paths: list[str] = Field(
        description="Paths to DDL SQL files to map onto the ontology.",
        examples=[["tests/fixtures/01_basics_ecommerce/schema.sql"]],
    )
    clear_graph: bool = Field(
        default=True,
        description="Wipe all Neo4j nodes/edges before building (recommended for clean runs).",
    )
    study_id: str = Field(
        default="demo",
        description="Run identifier used for logging and trace output.",
    )
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
        examples=[
            "What information is stored for each customer?",
            "How are products and orders related?",
        ],
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
        examples=[
            [
                "tests/fixtures/01_basics_ecommerce/business_glossary.txt",
                "tests/fixtures/01_basics_ecommerce/data_dictionary.txt",
            ]
        ],
    )
    ddl_paths: list[str] = Field(
        description="Paths to DDL SQL files.",
        examples=[["tests/fixtures/01_basics_ecommerce/schema.sql"]],
    )
    questions: list[str] = Field(
        min_length=1,
        description="One or more natural-language questions to answer after build.",
        examples=[
            [
                "What information is stored for each customer?",
                "How are products and orders related?",
            ]
        ],
    )
    clear_graph: bool = Field(
        default=True,
        description="Wipe all Neo4j nodes/edges before building (recommended for clean runs).",
    )
    lazy_extraction: bool = Field(
        default=False,
        description="Use heuristic rule-based extraction instead of LLM (faster, less accurate).",
    )
    run_ragas: bool = Field(
        default=False,
        description="Compute RAGAS faithfulness/AR/CP/CR after answering (requires expected answers in the fixture).",
    )
    study_id: str = Field(
        default="demo",
        description="Run identifier used for logging and trace output.",
    )


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


