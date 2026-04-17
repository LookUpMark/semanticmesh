"""Pydantic request/response models for both REST APIs."""

from __future__ import annotations

from typing import Any, Literal, TypeAlias

from pydantic import BaseModel, Field, model_validator

# ── Shared LLM override fields ────────────────────────────────────────────────

_LLM_REASONING_DESC = (
    "Reasoning / generation model name. When `provider` is set, the model name is passed\n"
    "directly to that provider — no prefix needed. With `provider=null` (auto-detect),\n"
    "the prefix determines the provider:\n"
    "  - `openai/gpt-oss-120b` (OpenRouter — any `/` without named prefix)\n"
    "  - `gpt-4.1` (OpenAI direct — bare gpt-* prefix)\n"
    "  - `claude-3-5-sonnet-20241022` (Anthropic direct)\n"
    "  - `ollama/llama3.1`, `groq/llama3-70b-8192`, etc. (named-prefix providers)\n"
    "Sets env var LLM_MODEL_REASONING."
)
_LLM_EXTRACTION_DESC = (
    "Extraction model for triplet extraction. Same name conventions as reasoning_model.\n"
    "Sets env var LLM_MODEL_EXTRACTION."
)
_LLM_MIDTIER_DESC = (
    "Mid-tier model for RAG mapping, Actor-Critic, hallucination grading.\n"
    "Sets env var LLM_MODEL_MIDTIER."
)
_LLM_BASE_URL_DESC = (
    "Override base URL for local / custom OpenAI-compatible endpoints "
    "(Ollama, LMStudio, self-hosted Groq proxy, etc.). "
    "Sets env var LMSTUDIO_BASE_URL."
)

_LLM_PROVIDER_DESC = (
    "Global LLM provider routing override. When set, all model names without an explicit "
    "provider prefix are routed through this provider. "
    "Possible values:\n"
    "  - `auto` — provider inferred from each model name prefix (default)\n"
    "  - `openrouter` — all models via OpenRouter (needs OPENROUTER_API_KEY)\n"
    "  - `openai` — all models via OpenAI API direct (needs OPENAI_API_KEY)\n"
    "  - `anthropic` — all models via Anthropic API (needs ANTHROPIC_API_KEY)\n"
    "  - `lmstudio` — all models via LM Studio local endpoint\n"
    "  - `ollama` — all models via Ollama local endpoint\n"
    "  - `groq` — all models via Groq (needs GROQ_API_KEY)\n"
    "  - `google` — all models via Google Gemini (needs GOOGLE_API_KEY)\n"
    "  - `mistral` — all models via Mistral AI (needs MISTRAL_API_KEY)\n"
    "  - `together` — all models via Together AI (needs TOGETHER_API_KEY)\n"
    "  - `bedrock` — all models via AWS Bedrock (needs AWS credentials)\n"
    "Sets env var LLM_PROVIDER."
)


class PipelineConfig(BaseModel):
    """Optional per-run configuration overrides.

    All fields are optional. When provided, they temporarily override the
    corresponding environment variable for the duration of the pipeline run
    (build + query). When omitted, the server's current settings are used.

    These overrides apply to Demo endpoints (build, query, pipeline) only.
    Ablation studies use their own matrix-driven configuration.
    """

    # ── LLM Provider Selection ──────────────────────────────────────────────
    provider: Literal[
        "auto", "openrouter", "openai", "anthropic", "lmstudio", "ollama",
        "groq", "google", "bedrock", "azure", "mistral", "together",
        "deepseek", "xai", "nvidia", "huggingface",
    ] | None = Field(
        default="openrouter",
        description=_LLM_PROVIDER_DESC,
        examples=["openrouter", "openai", "lmstudio"],
    )

    # ── LLM Model Selection ─────────────────────────────────────────────────
    reasoning_model: str | None = Field(
        default="openai/gpt-oss-120b",
        description=_LLM_REASONING_DESC,
        examples=["openai/gpt-oss-120b", "gpt-4.1", "groq/llama3-70b-8192"],
    )
    extraction_model: str | None = Field(
        default="openai/gpt-4.1-nano",
        description=_LLM_EXTRACTION_DESC,
        examples=["openai/gpt-4.1-nano", "gpt-4.1-nano"],
    )
    midtier_model: str | None = Field(
        default="openai/gpt-4.1-nano",
        description=_LLM_MIDTIER_DESC,
        examples=["openai/gpt-4.1-nano", "gpt-4.1-mini"],
    )
    lmstudio_base_url: str | None = Field(
        default=None,
        description=_LLM_BASE_URL_DESC,
        examples=["http://localhost:1234/v1", "http://192.168.1.50:1234/v1"],
    )

    # ── LLM Parameters ──────────────────────────────────────────────────────
    temperature_extraction: float | None = Field(
        default=0.0, ge=0.0, le=2.0,
        description="Temperature for extraction LLM (0.0 = deterministic JSON).",
    )
    temperature_reasoning: float | None = Field(
        default=0.0, ge=0.0, le=2.0,
        description="Temperature for reasoning/mapping LLM (0.0 = deterministic).",
    )
    temperature_generation: float | None = Field(
        default=0.3, ge=0.0, le=2.0,
        description="Temperature for answer generation LLM (0.3 for fluency).",
    )
    max_tokens_extraction: int | None = Field(
        default=8192, ge=256, le=32768,
        description="Max output tokens for extraction LLM.",
    )
    max_tokens_reasoning: int | None = Field(
        default=4096, ge=256, le=32768,
        description="Max output tokens for reasoning LLM.",
    )

    # ── Chunking ────────────────────────────────────────────────────────────
    chunk_size: int | None = Field(
        default=256, ge=64, le=2048,
        description=(
            "Child chunk token size. Must be greater than chunk_overlap."
        ),
    )
    chunk_overlap: int | None = Field(
        default=32, ge=0, le=1024,
        description=(
            "Child chunk overlap in tokens. Must be strictly less than chunk_size."
        ),
    )
    parent_chunk_size: int | None = Field(
        default=800, ge=128, le=4096,
        description=(
            "Parent chunk token size. "
            "Must be greater than parent_chunk_overlap and greater than chunk_size."
        ),
    )
    parent_chunk_overlap: int | None = Field(
        default=96, ge=0, le=2048,
        description=(
            "Parent chunk overlap in tokens. Must be strictly less than parent_chunk_size."
        ),
    )

    @model_validator(mode="after")
    def _validate_chunk_constraints(self) -> PipelineConfig:
        """Enforce overlap < size for both child and parent chunks."""
        if (
            self.chunk_size is not None
            and self.chunk_overlap is not None
            and self.chunk_overlap >= self.chunk_size
        ):
            raise ValueError(
                f"chunk_overlap ({self.chunk_overlap}) must be less than "
                f"chunk_size ({self.chunk_size})."
            )
        if (
            self.parent_chunk_size is not None
            and self.parent_chunk_overlap is not None
            and self.parent_chunk_overlap >= self.parent_chunk_size
        ):
            raise ValueError(
                f"parent_chunk_overlap ({self.parent_chunk_overlap}) must be less than "
                f"parent_chunk_size ({self.parent_chunk_size})."
            )
        if (
            self.chunk_size is not None
            and self.parent_chunk_size is not None
            and self.parent_chunk_size <= self.chunk_size
        ):
            raise ValueError(
                f"parent_chunk_size ({self.parent_chunk_size}) must be greater than "
                f"chunk_size ({self.chunk_size})."
            )
        return self

    # ── Retrieval ───────────────────────────────────────────────────────────
    retrieval_mode: Literal["hybrid", "vector", "bm25"] | None = Field(
        default="hybrid",
        description="Retrieval channel combination.",
    )
    retrieval_vector_top_k: int | None = Field(
        default=20, ge=1, le=100,
        description="Vector search candidates.",
    )
    retrieval_bm25_top_k: int | None = Field(
        default=10, ge=1, le=100,
        description="BM25 keyword candidates.",
    )
    enable_reranker: bool | None = Field(
        default=True,
        description="Enable cross-encoder reranking (bge-reranker-v2-m3).",
    )
    reranker_top_k: int | None = Field(
        default=12, ge=1, le=50,
        description="Candidates kept after reranking.",
    )

    # ── Entity Resolution ───────────────────────────────────────────────────
    er_similarity_threshold: float | None = Field(
        default=0.75, ge=0.0, le=1.0,
        description="Cosine similarity threshold for entity blocking.",
    )
    er_blocking_top_k: int | None = Field(
        default=10, ge=1, le=50,
        description="K-NN candidates per entity in blocking.",
    )

    # ── Mapping & Validation ────────────────────────────────────────────────
    confidence_threshold: float | None = Field(
        default=0.90, ge=0.0, le=1.0,
        description="Mapping confidence threshold for HITL interrupt.",
    )
    max_reflection_attempts: int | None = Field(
        default=3, ge=1, le=10,
        description="Max Actor-Critic reflection retries.",
    )
    max_cypher_healing_attempts: int | None = Field(
        default=3, ge=0, le=10,
        description="Max Cypher healing retries before deterministic fallback.",
    )
    max_hallucination_retries: int | None = Field(
        default=3, ge=0, le=10,
        description="Max hallucination regeneration retries.",
    )

    # ── Feature Flags ───────────────────────────────────────────────────────
    enable_schema_enrichment: bool | None = Field(
        default=True,
        description="LLM acronym expansion during schema enrichment.",
    )
    enable_cypher_healing: bool | None = Field(
        default=True,
        description="Auto-fix Cypher syntax errors via LLM reflection.",
    )
    enable_critic_validation: bool | None = Field(
        default=True,
        description="Actor-Critic mapping validation loop.",
    )
    enable_hallucination_grader: bool | None = Field(
        default=True,
        description="Self-RAG hallucination grading.",
    )
    enable_retrieval_quality_gate: bool | None = Field(
        default=True,
        description="Retrieval quality gate before generation.",
    )
    enable_grader_consistency_validator: bool | None = Field(
        default=True,
        description="Grader consistency check across iterations.",
    )
    enable_spacy_heuristics: bool | None = Field(
        default=True,
        description="spaCy-based heuristic extraction as fallback.",
    )
    enable_lazy_expansion: bool | None = Field(
        default=True,
        description="Lazy context expansion strategy.",
    )

    def to_env_overrides(self) -> dict[str, str]:
        """Convert non-None fields to env var overrides."""
        mapping: dict[str, Any] = {
            "LLM_PROVIDER": self.provider,
            "LLM_MODEL_REASONING": self.reasoning_model,
            "LLM_MODEL_EXTRACTION": self.extraction_model,
            "LLM_MODEL_MIDTIER": self.midtier_model,
            "LMSTUDIO_BASE_URL": self.lmstudio_base_url,
            "LLM_TEMPERATURE_EXTRACTION": self.temperature_extraction,
            "LLM_TEMPERATURE_REASONING": self.temperature_reasoning,
            "LLM_TEMPERATURE_GENERATION": self.temperature_generation,
            "LLM_MAX_TOKENS_EXTRACTION": self.max_tokens_extraction,
            "LLM_MAX_TOKENS_REASONING": self.max_tokens_reasoning,
            "CHUNK_SIZE": self.chunk_size,
            "CHUNK_OVERLAP": self.chunk_overlap,
            "PARENT_CHUNK_SIZE": self.parent_chunk_size,
            "PARENT_CHUNK_OVERLAP": self.parent_chunk_overlap,
            "RETRIEVAL_MODE": self.retrieval_mode,
            "RETRIEVAL_VECTOR_TOP_K": self.retrieval_vector_top_k,
            "RETRIEVAL_BM25_TOP_K": self.retrieval_bm25_top_k,
            "ENABLE_RERANKER": self.enable_reranker,
            "RERANKER_TOP_K": self.reranker_top_k,
            "ER_SIMILARITY_THRESHOLD": self.er_similarity_threshold,
            "ER_BLOCKING_TOP_K": self.er_blocking_top_k,
            "CONFIDENCE_THRESHOLD": self.confidence_threshold,
            "MAX_REFLECTION_ATTEMPTS": self.max_reflection_attempts,
            "MAX_CYPHER_HEALING_ATTEMPTS": self.max_cypher_healing_attempts,
            "MAX_HALLUCINATION_RETRIES": self.max_hallucination_retries,
            "ENABLE_SCHEMA_ENRICHMENT": self.enable_schema_enrichment,
            "ENABLE_CYPHER_HEALING": self.enable_cypher_healing,
            "ENABLE_CRITIC_VALIDATION": self.enable_critic_validation,
            "ENABLE_HALLUCINATION_GRADER": self.enable_hallucination_grader,
            "ENABLE_RETRIEVAL_QUALITY_GATE": self.enable_retrieval_quality_gate,
            "ENABLE_GRADER_CONSISTENCY_VALIDATOR": self.enable_grader_consistency_validator,
            "ENABLE_SPACY_HEURISTICS": self.enable_spacy_heuristics,
            "ENABLE_LAZY_EXPANSION": self.enable_lazy_expansion,
        }
        result: dict[str, str] = {}
        for env_key, value in mapping.items():
            if value is None:
                continue
            if isinstance(value, bool):
                result[env_key] = "true" if value else "false"
            else:
                result[env_key] = str(value)
        return result


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
        description="Output directory prefix under outputs/ablation/.",
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
    force_rebuild: bool = Field(
        default=False,
        description=(
            "Bypass the SHA-256 incremental check — re-ingest all files even if unchanged. "
            "Has no effect when clear_graph=True (full wipe always re-ingests everything)."
        ),
    )
    config: PipelineConfig | None = Field(
        default=None,
        description="Optional per-run configuration overrides (models, temperatures, feature flags, etc.).",
    )


class BuildResultResponse(BaseModel):
    job_id: str
    status: Literal["queued", "running", "done", "failed"]
    error: str | None = None
    current_step: str | None = Field(
        default=None,
        description="Name of the pipeline node currently executing (null when done/failed).",
    )
    triplets_extracted: int | None = None
    entities_resolved: int | None = None
    tables_parsed: int | None = None
    tables_completed: int | None = None
    parent_chunks: int | None = None
    child_chunks: int | None = None
    skipped_files: list[str] | None = Field(
        default=None,
        description="Files skipped because their SHA-256 hash was unchanged since last build.",
    )


# ── KG Snapshot models ────────────────────────────────────────────────────────

class KGSnapshotMeta(BaseModel):
    """Metadata for a saved Knowledge Graph snapshot."""

    id: str = Field(description="UUID of the snapshot.")
    name: str = Field(description="Human-readable snapshot name.")
    description: str = Field(default="", description="Optional description.")
    created_at: str = Field(description="ISO-8601 UTC creation timestamp.")
    node_count: int = Field(description="Number of nodes in the snapshot.")
    edge_count: int = Field(description="Number of edges in the snapshot.")
    is_active: bool = Field(description="Whether this snapshot is currently loaded in Neo4j.")


class SaveSnapshotRequest(BaseModel):
    """Request to save the current KG as a named snapshot."""

    name: str = Field(
        description="Human-readable name for this snapshot.",
        examples=["E-Commerce v1", "Finance schema — April 2026"],
    )
    description: str = Field(
        default="",
        description="Optional longer description.",
    )


class RenameSnapshotRequest(BaseModel):
    """Request to rename/update an existing KG snapshot."""

    name: str = Field(description="New human-readable name for the snapshot.")
    description: str | None = Field(
        default=None,
        description="New description. If omitted, the existing description is preserved.",
    )


# ── Conversation models ────────────────────────────────────────────────────────

class ConversationMessage(BaseModel):
    """A single chat message stored in a conversation."""

    role: str = Field(description='"user" or "assistant".')
    content: str = Field(description="Message text content.")
    metadata: dict[str, Any] | None = Field(
        default=None,
        description="Optional QueryResponse metadata attached to assistant messages.",
    )


class ConversationMeta(BaseModel):
    """Metadata for a saved conversation (no messages)."""

    id: str = Field(description="UUID of the conversation.")
    title: str = Field(description="Human-readable title.")
    session_id: str = Field(description="LangGraph thread_id tied to this conversation.")
    preview: str = Field(description="First user question (truncated to 80 chars).")
    message_count: int = Field(description="Total number of messages.")
    active_snapshot_id: str | None = Field(
        default=None,
        description="KG snapshot that was active when the conversation was saved.",
    )
    created_at: str = Field(description="ISO-8601 UTC creation timestamp.")
    updated_at: str = Field(description="ISO-8601 UTC last-update timestamp.")


class ConversationDetail(ConversationMeta):
    """Full conversation including all messages."""

    messages: list[ConversationMessage] = Field(description="Ordered list of chat messages.")


class SaveConversationRequest(BaseModel):
    """Request to persist a conversation."""

    session_id: str = Field(description="Client session UUID (LangGraph thread_id).")
    title: str = Field(
        description="Human-readable title (defaults to first user message if empty).",
        default="",
    )
    messages: list[ConversationMessage] = Field(description="Full message list to persist.")
    active_snapshot_id: str | None = Field(
        default=None,
        description="ID of the KG snapshot that was active during this conversation.",
    )


class RenameConversationRequest(BaseModel):
    """Request to rename a conversation."""

    title: str = Field(description="New title for the conversation.")


class QueryRequest(BaseModel):
    """Query the Knowledge Graph with a natural-language question."""

    question: str = Field(
        description="Natural language question to answer from the Knowledge Graph.",
        examples=[
            "What information is stored for each customer?",
            "How are products and orders related?",
        ],
    )
    config: PipelineConfig | None = Field(
        default=None,
        description="Optional per-run configuration overrides (models, temperatures, feature flags, etc.).",
    )
    session_id: str | None = Field(
        default=None,
        description="Client-generated session UUID. The server uses it as LangGraph thread_id "
                    "so the MemorySaver checkpoint carries the full conversation history "
                    "server-side — no need to replay history in the request body.",
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
    session_id: str | None = Field(
        default=None,
        description="Echo of the request session_id for client-side correlation.",
    )


class PipelineRequest(BaseModel):
    """Run a complete E2E pipeline: build KG then answer questions."""

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
    config: PipelineConfig | None = Field(
        default=None,
        description="Optional per-run configuration overrides (models, temperatures, feature flags, etc.).",
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
    child_of_edges: int
    references_edges: int
    total_nodes: int
    total_relationships: int


