"""EP-01: Application settings loaded from environment / .env file.

Sensitive values (API keys, passwords) are loaded from environment variables.
Non-sensitive defaults are defined in config.py and can be overridden via env vars.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.config.config import DEFAULT_CONFIG


class Settings(BaseSettings):
    """Application settings with environment variable override support.

    All non-sensitive defaults come from config.py and can be overridden.
    Sensitive values (API keys, passwords) must be set via environment variables.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        secrets_dir="/run/secrets",
        extra="ignore",
    )

    # ── Neo4j ──────────────────────────────────────────────────────────────────
    neo4j_uri: str = DEFAULT_CONFIG.neo4j_uri
    neo4j_user: str = DEFAULT_CONFIG.neo4j_user
    neo4j_password: SecretStr = SecretStr("")

    # ── LLM ─────────────────────────────────────────────────────────────────────
    lmstudio_base_url: str = DEFAULT_CONFIG.lmstudio_base_url
    openrouter_base_url: str = DEFAULT_CONFIG.openrouter_base_url
    groq_base_url: str = DEFAULT_CONFIG.groq_base_url
    together_base_url: str = DEFAULT_CONFIG.together_base_url
    nvidia_base_url: str = DEFAULT_CONFIG.nvidia_base_url
    deepseek_base_url: str = DEFAULT_CONFIG.deepseek_base_url
    xai_base_url: str = DEFAULT_CONFIG.xai_base_url
    cohere_base_url: str = DEFAULT_CONFIG.cohere_base_url
    ollama_base_url: str = DEFAULT_CONFIG.ollama_base_url
    openrouter_api_key: SecretStr = SecretStr("")
    openai_api_key: SecretStr = SecretStr("")
    llm_provider: str = DEFAULT_CONFIG.llm_provider
    llm_model_reasoning: str = DEFAULT_CONFIG.llm_model_reasoning
    llm_model_extraction: str = DEFAULT_CONFIG.llm_model_extraction
    llm_model_midtier: str = DEFAULT_CONFIG.llm_model_midtier
    llm_temperature_extraction: float = DEFAULT_CONFIG.llm_temperature_extraction
    llm_temperature_reasoning: float = DEFAULT_CONFIG.llm_temperature_reasoning
    llm_temperature_generation: float = DEFAULT_CONFIG.llm_temperature_generation
    llm_max_tokens_extraction: int = DEFAULT_CONFIG.llm_max_tokens_extraction
    llm_max_tokens_reasoning: int = DEFAULT_CONFIG.llm_max_tokens_reasoning
    llm_request_timeout: int = DEFAULT_CONFIG.llm_request_timeout

    # ── Embeddings & Reranking ─────────────────────────────────────────────────
    embedding_model: str = DEFAULT_CONFIG.embedding_model
    embedding_dimensions: int = DEFAULT_CONFIG.embedding_dimensions
    embedding_batch_size: int = DEFAULT_CONFIG.embedding_batch_size
    reranker_model: str = DEFAULT_CONFIG.reranker_model
    reranker_top_k: int = DEFAULT_CONFIG.reranker_top_k
    reranker_weight_rerank: float = DEFAULT_CONFIG.reranker_weight_rerank
    reranker_weight_vector: float = DEFAULT_CONFIG.reranker_weight_vector
    reranker_weight_bm25: float = DEFAULT_CONFIG.reranker_weight_bm25
    reranker_weight_graph: float = DEFAULT_CONFIG.reranker_weight_graph
    reranker_short_text_threshold: int = DEFAULT_CONFIG.reranker_short_text_threshold

    # ── Entity Resolution ──────────────────────────────────────────────────────
    er_blocking_top_k: int = DEFAULT_CONFIG.er_blocking_top_k
    er_similarity_threshold: float = DEFAULT_CONFIG.er_similarity_threshold
    er_max_cluster_size: int = DEFAULT_CONFIG.er_max_cluster_size
    er_threshold_step: float = DEFAULT_CONFIG.er_threshold_step
    er_recluster_max_iterations: int = DEFAULT_CONFIG.er_recluster_max_iterations

    # ── API Server ──────────────────────────────────────────────────────────────
    api_server_host: str = DEFAULT_CONFIG.api_server_host
    api_server_port: int = DEFAULT_CONFIG.api_server_port
    api_max_upload_bytes: int = DEFAULT_CONFIG.api_max_upload_bytes
    api_max_concurrent_jobs: int = DEFAULT_CONFIG.api_max_concurrent_jobs
    api_job_ttl_seconds: int = DEFAULT_CONFIG.api_job_ttl_seconds
    api_rate_limit_max_attempts: int = DEFAULT_CONFIG.api_rate_limit_max_attempts
    api_rate_limit_window_seconds: int = DEFAULT_CONFIG.api_rate_limit_window_seconds
    api_polling_interval: float = DEFAULT_CONFIG.api_polling_interval

    # ── Confidence & Loop Guards ───────────────────────────────────────────────
    confidence_threshold: float = DEFAULT_CONFIG.confidence_threshold
    max_reflection_attempts: int = DEFAULT_CONFIG.max_reflection_attempts
    max_cypher_healing_attempts: int = DEFAULT_CONFIG.max_cypher_healing_attempts
    max_hallucination_retries: int = DEFAULT_CONFIG.max_hallucination_retries
    max_llm_retries: int = DEFAULT_CONFIG.max_llm_retries

    # ── Chunking ───────────────────────────────────────────────────────────────
    parent_chunk_size: int = DEFAULT_CONFIG.parent_chunk_size
    parent_chunk_overlap: int = DEFAULT_CONFIG.parent_chunk_overlap
    chunk_size: int = DEFAULT_CONFIG.chunk_size
    chunk_overlap: int = DEFAULT_CONFIG.chunk_overlap
    extraction_concurrency: int = DEFAULT_CONFIG.extraction_concurrency

    # ── Retrieval ──────────────────────────────────────────────────────────────
    retrieval_vector_top_k: int = DEFAULT_CONFIG.retrieval_vector_top_k
    retrieval_bm25_top_k: int = DEFAULT_CONFIG.retrieval_bm25_top_k
    retrieval_attribute_top_k: int = DEFAULT_CONFIG.retrieval_attribute_top_k
    retrieval_graph_depth: int = DEFAULT_CONFIG.retrieval_graph_depth
    retrieval_graph_traversal_limit: int = DEFAULT_CONFIG.retrieval_graph_traversal_limit
    retrieval_min_score: float = DEFAULT_CONFIG.retrieval_min_score
    retrieval_min_score_ratio: float = DEFAULT_CONFIG.retrieval_min_score_ratio
    retrieval_salvage_min_score: float = DEFAULT_CONFIG.retrieval_salvage_min_score
    retrieval_rrf_constant: int = DEFAULT_CONFIG.retrieval_rrf_constant
    retrieval_context_score_gate: float = DEFAULT_CONFIG.retrieval_context_score_gate
    bm25_cache_ttl_seconds: int = DEFAULT_CONFIG.bm25_cache_ttl_seconds

    # ── Few-Shot ───────────────────────────────────────────────────────────────
    few_shot_cypher_examples: int = DEFAULT_CONFIG.few_shot_cypher_examples

    # ── Ablation Flags ─────────────────────────────────────────────────────────
    enable_schema_enrichment: bool = DEFAULT_CONFIG.enable_schema_enrichment
    retrieval_mode: str = DEFAULT_CONFIG.retrieval_mode
    enable_cypher_healing: bool = DEFAULT_CONFIG.enable_cypher_healing
    enable_critic_validation: bool = DEFAULT_CONFIG.enable_critic_validation
    enable_reranker: bool = DEFAULT_CONFIG.enable_reranker
    enable_hallucination_grader: bool = DEFAULT_CONFIG.enable_hallucination_grader
    enable_retrieval_quality_gate: bool = DEFAULT_CONFIG.enable_retrieval_quality_gate
    enable_grader_consistency_validator: bool = DEFAULT_CONFIG.enable_grader_consistency_validator
    grader_timeout_seconds: float = DEFAULT_CONFIG.grader_timeout_seconds
    use_lazy_extraction: bool = DEFAULT_CONFIG.use_lazy_extraction
    enable_spacy_heuristics: bool = DEFAULT_CONFIG.enable_spacy_heuristics
    spacy_model_name: str = DEFAULT_CONFIG.spacy_model_name
    er_judge_threshold: float = DEFAULT_CONFIG.er_judge_threshold
    heuristic_mapping_confidence_threshold: float = (
        DEFAULT_CONFIG.heuristic_mapping_confidence_threshold
    )
    heuristic_extraction_confidence: float = DEFAULT_CONFIG.heuristic_extraction_confidence
    heuristic_spacy_confidence: float = DEFAULT_CONFIG.heuristic_spacy_confidence
    enable_lazy_expansion: bool = DEFAULT_CONFIG.enable_lazy_expansion
    lazy_expansion_confidence_threshold: float = DEFAULT_CONFIG.lazy_expansion_confidence_threshold
    enable_post_rerank_expansion: bool = DEFAULT_CONFIG.enable_post_rerank_expansion
    # ── Retrieval Quality Gate Thresholds ──────────────────────────────────────
    retrieval_gate_proceed_threshold: float = DEFAULT_CONFIG.retrieval_gate_proceed_threshold
    retrieval_gate_abstain_threshold: float = DEFAULT_CONFIG.retrieval_gate_abstain_threshold
    retrieval_gate_structural_threshold: float = DEFAULT_CONFIG.retrieval_gate_structural_threshold
    # ── Reranking / Diversity ──────────────────────────────────────────────────
    diversity_inject_score: float = DEFAULT_CONFIG.diversity_inject_score
    diversity_boost_min_score: float = DEFAULT_CONFIG.diversity_boost_min_score
    pool_confidence_min_size: int = DEFAULT_CONFIG.pool_confidence_min_size
    pool_confidence_floor: float = DEFAULT_CONFIG.pool_confidence_floor
    pool_confidence_ceiling: float = DEFAULT_CONFIG.pool_confidence_ceiling
    sparse_sufficiency_threshold: float = DEFAULT_CONFIG.sparse_sufficiency_threshold
    post_rerank_expansion_score: float = DEFAULT_CONFIG.post_rerank_expansion_score
    # ── Generation Context ─────────────────────────────────────────────────────
    generation_max_context_chunks: int = DEFAULT_CONFIG.generation_max_context_chunks
    generation_token_budget: int = DEFAULT_CONFIG.generation_token_budget
    generation_max_core_chunks: int = DEFAULT_CONFIG.generation_max_core_chunks
    generation_max_support_chunks: int = DEFAULT_CONFIG.generation_max_support_chunks
    partial_abstention_score_threshold: float = DEFAULT_CONFIG.partial_abstention_score_threshold
    # ── Mapping Scoring ────────────────────────────────────────────────────────
    mapping_column_name_penalty: float = DEFAULT_CONFIG.mapping_column_name_penalty
    mapping_code_pattern_penalty: float = DEFAULT_CONFIG.mapping_code_pattern_penalty
    mapping_noise_token_penalty: float = DEFAULT_CONFIG.mapping_noise_token_penalty
    mapping_token_count_penalty: float = DEFAULT_CONFIG.mapping_token_count_penalty
    mapping_overlap_bonus_max: float = DEFAULT_CONFIG.mapping_overlap_bonus_max
    mapping_overlap_bonus_per_token: float = DEFAULT_CONFIG.mapping_overlap_bonus_per_token
    # ── Extraction ─────────────────────────────────────────────────────────────
    heuristic_fallback_confidence: float = DEFAULT_CONFIG.heuristic_fallback_confidence
    # ── Graph ──────────────────────────────────────────────────────────────────
    provenance_max_chars: int = DEFAULT_CONFIG.provenance_max_chars
    # ── Performance / Cost Optimisation ────────────────────────────────────────
    enable_singleton_llm_definitions: bool = DEFAULT_CONFIG.enable_singleton_llm_definitions
    critic_confidence_gate: float = DEFAULT_CONFIG.critic_confidence_gate
    max_reflection_attempts_reasoning: int = DEFAULT_CONFIG.max_reflection_attempts_reasoning
    # ── Logging ────────────────────────────────────────────────────────────────
    log_level: str = DEFAULT_CONFIG.log_level

    # ── Debug Tracing ───────────────────────────────────────────────────────────
    enable_debug_trace: bool = DEFAULT_CONFIG.enable_debug_trace
    trace_output_dir: str = DEFAULT_CONFIG.trace_output_dir
    trace_compress_large_fields: bool = DEFAULT_CONFIG.trace_compress_large_fields
    trace_truncate_length: int = DEFAULT_CONFIG.trace_truncate_length
    trace_max_items: int = DEFAULT_CONFIG.trace_max_items

    # ── Checkpointing ───────────────────────────────────────────────────────────
    sqlite_checkpoint_path: str = DEFAULT_CONFIG.sqlite_checkpoint_path

    # ── Azure OpenAI ────────────────────────────────────────────────────────────
    azure_openai_api_version: str = DEFAULT_CONFIG.azure_openai_api_version


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the singleton Settings instance (cached after first call)."""
    return Settings()


def reload_settings() -> Settings:
    """Clear the settings cache and return a fresh Settings instance.

    Call this after changing ``os.environ`` in notebooks or tests.
    Updates the module-level ``settings`` singleton in-place.
    """
    get_settings.cache_clear()
    new = get_settings()
    import src.config.settings as _self  # noqa: PLC0415

    _self.settings = new
    return new


# Module-level singleton
settings: Settings = get_settings()
