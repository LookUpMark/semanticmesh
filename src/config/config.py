"""Application configuration defaults.

Non-sensitive configuration values are defined here as a dataclass.
Sensitive values (API keys, passwords) should be set via environment variables
or .env file and are loaded in settings.py.
"""

from __future__ import annotations

from dataclasses import dataclass

# Placeholder API key for local LM Studio (localhost-only, not a real secret).
LMSTUDIO_PLACEHOLDER_KEY = "lm-studio"


@dataclass(frozen=True)
class AppConfig:
    """Default application configuration.

    Override via environment variables (see settings.py for names).
    Non-sensitive defaults are defined here for visibility.
    """

    # ── Neo4j ──────────────────────────────────────────────────────────────────
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"

    # ── LLM Providers ──────────────────────────────────────────────────────────
    lmstudio_base_url: str = "http://localhost:1234/v1"
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    groq_base_url: str = "https://api.groq.com/openai/v1"
    together_base_url: str = "https://api.together.xyz/v1"
    nvidia_base_url: str = "https://integrate.api.nvidia.com/v1"
    deepseek_base_url: str = "https://api.deepseek.com/v1"
    xai_base_url: str = "https://api.x.ai/v1"
    cohere_base_url: str = "https://api.cohere.ai/compatibility/v1"
    ollama_base_url: str = "http://localhost:11434/v1"
    # Global provider routing override: "auto" = infer from model name prefix.
    # Other values: "openrouter", "openai", "anthropic", "lmstudio", "ollama",
    # "google", "bedrock", "azure", "groq", "mistral", "together", "deepseek",
    # "xai", "nvidia", "huggingface".
    llm_provider: str = "auto"

    # ── LLM Models ─────────────────────────────────────────────────────────────
    llm_model_reasoning: str = "gpt-5.4-2026-03-05"
    llm_model_extraction: str = "gpt-5.4-nano-2026-03-17"
    llm_model_midtier: str = "gpt-5.4-mini-2026-03-17"
    azure_openai_api_version: str = "2024-11-01-preview"

    # Temperature: extraction/reasoning at 0.0 for deterministic JSON, generation at 0.3 for fluency
    llm_temperature_extraction: float = 0.0
    llm_temperature_reasoning: float = 0.0
    llm_temperature_generation: float = 0.3

    llm_max_tokens_extraction: int = 8192
    llm_max_tokens_reasoning: int = 8192
    llm_request_timeout: int = 120

    # ── Embeddings & Reranking ─────────────────────────────────────────────────
    embedding_model: str = "BAAI/bge-m3"
    embedding_dimensions: int = 1024
    reranker_model: str = "BAAI/bge-reranker-v2-m3"
    reranker_top_k: int = 12

    # ── Entity Resolution ──────────────────────────────────────────────────────
    er_blocking_top_k: int = 10
    er_similarity_threshold: float = 0.75
    er_max_cluster_size: int = 10

    # ── Confidence & Loop Guards ───────────────────────────────────────────────
    confidence_threshold: float = 0.90
    max_reflection_attempts: int = 3
    max_cypher_healing_attempts: int = 3
    max_hallucination_retries: int = 3
    max_llm_retries: int = 3

    # ── Chunking ───────────────────────────────────────────────────────────────
    # Parent chunks: full-context nodes returned to the LLM (no embedding)
    parent_chunk_size: int = 800
    parent_chunk_overlap: int = 96
    # Child chunks: small nodes used for precise vector search (with embedding)
    chunk_size: int = 256
    chunk_overlap: int = 32
    extraction_concurrency: int = 10

    # ── Retrieval ──────────────────────────────────────────────────────────────
    retrieval_vector_top_k: int = 20
    retrieval_bm25_top_k: int = 10
    retrieval_graph_depth: int = 2
    retrieval_min_score: float = 0.05
    retrieval_min_score_ratio: float = 0.35
    retrieval_salvage_min_score: float = 0.07

    # ── Few-Shot ───────────────────────────────────────────────────────────────
    few_shot_cypher_examples: int = 5

    # ── API Server ──────────────────────────────────────────────────────────────
    api_server_host: str = "127.0.0.1"
    api_server_port: int = 8000
    api_max_upload_bytes: int = 100 * 1024 * 1024  # 100 MB
    api_max_concurrent_jobs: int = 200
    api_job_ttl_seconds: int = 3600
    api_rate_limit_max_attempts: int = 5
    api_rate_limit_window_seconds: int = 60

    # ── Ablation Flags ─────────────────────────────────────────────────────────
    enable_schema_enrichment: bool = True
    retrieval_mode: str = "hybrid"
    enable_cypher_healing: bool = True
    enable_critic_validation: bool = True
    enable_reranker: bool = True
    enable_hallucination_grader: bool = True
    enable_retrieval_quality_gate: bool = True
    enable_grader_consistency_validator: bool = True
    grader_timeout_seconds: float = 12.0
    use_lazy_extraction: bool = False
    enable_spacy_heuristics: bool = True
    spacy_model_name: str = "en_core_web_sm"
    er_judge_threshold: float = 0.80
    heuristic_mapping_confidence_threshold: float = 0.60
    enable_lazy_expansion: bool = True
    lazy_expansion_confidence_threshold: float = 0.40

    # ── Performance / Cost Optimisation ───────────────────────────────────────
    # When True, singleton entity definitions are derived directly from their
    # provenance text instead of calling the LLM — saves many lightweight calls.
    enable_singleton_llm_definitions: bool = False
    # Critic is skipped when the mapping confidence already exceeds this gate.
    # Setting to 1.0 disables this gate (always run critic when enabled).
    critic_confidence_gate: float = 0.85
    # Max reflection retries for expensive reasoning-tier calls (mapping, ER judge).
    # Cheaper extraction-tier retries use max_reflection_attempts unchanged.
    max_reflection_attempts_reasoning: int = 2

    # ── Logging ────────────────────────────────────────────────────────────────
    log_level: str = "INFO"

    # ── Debug Tracing ───────────────────────────────────────────────────────────
    enable_debug_trace: bool = False
    trace_output_dir: str = "outputs/ablation/traces/debug"
    trace_compress_large_fields: bool = True
    trace_truncate_length: int = 500
    trace_max_items: int = 100

    # ── Checkpointing ────────────────────────────────────────────────────────────
    sqlite_checkpoint_path: str = ":memory:"


# Default configuration instance
DEFAULT_CONFIG = AppConfig()
