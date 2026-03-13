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

    Environment variables:
        NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
        LMSTUDIO_BASE_URL (default: http://localhost:1234/v1)
        LLM_MODEL_REASONING, LLM_MODEL_EXTRACTION
        LLM_TEMPERATURE_EXTRACTION, LLM_TEMPERATURE_REASONING, LLM_TEMPERATURE_GENERATION
        LLM_MAX_TOKENS_EXTRACTION (default: 16384)
        EMBEDDING_MODEL, RERANKER_MODEL
        ER_BLOCKING_TOP_K, ER_SIMILARITY_THRESHOLD
        CONFIDENCE_THRESHOLD, MAX_REFLECTION_ATTEMPTS, MAX_CYPHER_HEALING_ATTEMPTS
        CHUNK_SIZE, CHUNK_OVERLAP
        RETRIEVAL_VECTOR_TOP_K, RETRIEVAL_BM25_TOP_K, RETRIEVAL_GRAPH_DEPTH
        FEW_SHOT_CYPHER_EXAMPLES
        ENABLE_SCHEMA_ENRICHMENT, RETRIEVAL_MODE
        ENABLE_CYPHER_HEALING, ENABLE_CRITIC_VALIDATION, ENABLE_RERANKER, ENABLE_HALLUCINATION_GRADER
        LOG_LEVEL
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
    neo4j_password: SecretStr = SecretStr("neo4j")  # Override via NEO4J_PASSWORD

    # ── LLM ─────────────────────────────────────────────────────────────────────
    lmstudio_base_url: str = DEFAULT_CONFIG.lmstudio_base_url
    openrouter_base_url: str = DEFAULT_CONFIG.openrouter_base_url
    openrouter_api_key: SecretStr = SecretStr("")  # Override via OPENROUTER_API_KEY
    llm_model_reasoning: str = DEFAULT_CONFIG.llm_model_reasoning
    llm_model_extraction: str = DEFAULT_CONFIG.llm_model_extraction
    llm_temperature_extraction: float = DEFAULT_CONFIG.llm_temperature_extraction
    llm_temperature_reasoning: float = DEFAULT_CONFIG.llm_temperature_reasoning
    llm_temperature_generation: float = DEFAULT_CONFIG.llm_temperature_generation
    llm_max_tokens_extraction: int = DEFAULT_CONFIG.llm_max_tokens_extraction
    llm_max_tokens_reasoning: int = DEFAULT_CONFIG.llm_max_tokens_reasoning

    # ── Embeddings & Reranking ─────────────────────────────────────────────────
    embedding_model: str = DEFAULT_CONFIG.embedding_model
    reranker_model: str = DEFAULT_CONFIG.reranker_model
    reranker_top_k: int = DEFAULT_CONFIG.reranker_top_k

    # ── Entity Resolution ──────────────────────────────────────────────────────
    er_blocking_top_k: int = DEFAULT_CONFIG.er_blocking_top_k
    er_similarity_threshold: float = DEFAULT_CONFIG.er_similarity_threshold

    # ── Confidence & Loop Guards ───────────────────────────────────────────────
    confidence_threshold: float = DEFAULT_CONFIG.confidence_threshold
    max_reflection_attempts: int = DEFAULT_CONFIG.max_reflection_attempts
    max_cypher_healing_attempts: int = DEFAULT_CONFIG.max_cypher_healing_attempts
    max_hallucination_retries: int = DEFAULT_CONFIG.max_hallucination_retries
    max_llm_retries: int = DEFAULT_CONFIG.max_llm_retries

    # ── Chunking ───────────────────────────────────────────────────────────────
    chunk_size: int = DEFAULT_CONFIG.chunk_size
    chunk_overlap: int = DEFAULT_CONFIG.chunk_overlap

    # ── Retrieval ──────────────────────────────────────────────────────────────
    retrieval_vector_top_k: int = DEFAULT_CONFIG.retrieval_vector_top_k
    retrieval_bm25_top_k: int = DEFAULT_CONFIG.retrieval_bm25_top_k
    retrieval_graph_depth: int = DEFAULT_CONFIG.retrieval_graph_depth

    # ── Few-Shot ───────────────────────────────────────────────────────────────
    few_shot_cypher_examples: int = DEFAULT_CONFIG.few_shot_cypher_examples

    # ── Ablation Flags ─────────────────────────────────────────────────────────
    enable_schema_enrichment: bool = DEFAULT_CONFIG.enable_schema_enrichment
    retrieval_mode: str = DEFAULT_CONFIG.retrieval_mode
    enable_cypher_healing: bool = DEFAULT_CONFIG.enable_cypher_healing
    enable_critic_validation: bool = DEFAULT_CONFIG.enable_critic_validation
    enable_reranker: bool = DEFAULT_CONFIG.enable_reranker
    enable_hallucination_grader: bool = DEFAULT_CONFIG.enable_hallucination_grader

    # ── Logging ────────────────────────────────────────────────────────────────
    log_level: str = DEFAULT_CONFIG.log_level


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the singleton Settings instance (cached after first call)."""
    return Settings()


# Module-level singleton — import with:
#   from src.config.settings import settings
settings: Settings = get_settings()
