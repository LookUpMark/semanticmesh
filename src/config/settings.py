"""EP-01: Application settings loaded from environment / .env file."""

from __future__ import annotations

from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        secrets_dir="/run/secrets",
        extra="ignore",
    )

    # ── Neo4j ──────────────────────────────────────────────────────────────────
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: SecretStr = SecretStr("neo4j")

    # ── LLM — thesis: OpenRouter Free Tier; architecture: any BaseChatModel ───
    # Swap llm_model_* values (and ChatOpenRouter in llm_factory.py) to route
    # to any provider: gpt-4o, claude-3-5-sonnet, llama via vLLM, etc.
    openrouter_api_key: SecretStr = SecretStr("")   # OPENROUTER_API_KEY env var
    llm_model_reasoning: str = "qwen/qwen3-coder:free"                    # reasoning + generation
    llm_model_extraction: str = "qwen/qwen3-next-80b-a3b-instruct:free"   # SLM extraction
    llm_temperature_extraction: float = 0.0
    llm_temperature_reasoning: float = 0.0
    llm_temperature_generation: float = 0.3

    # ── Embeddings & Reranking ─────────────────────────────────────────────────
    embedding_model: str = "BAAI/bge-m3"
    reranker_model: str = "BAAI/bge-reranker-large"
    reranker_top_k: int = 5

    # ── Entity Resolution ──────────────────────────────────────────────────────
    er_blocking_top_k: int = 10
    er_similarity_threshold: float = 0.85

    # ── Confidence & Loop Guards ───────────────────────────────────────────────
    confidence_threshold: float = 0.90
    max_reflection_attempts: int = 3
    max_cypher_healing_attempts: int = 3
    max_hallucination_retries: int = 3
    max_llm_retries: int = 3                # InstrumentedLLM retry attempts on rate-limit/timeout

    # ── Chunking ───────────────────────────────────────────────────────────────
    chunk_size: int = 512
    chunk_overlap: int = 64

    # ── Retrieval ──────────────────────────────────────────────────────────────
    retrieval_vector_top_k: int = 20
    retrieval_bm25_top_k: int = 10
    retrieval_graph_depth: int = 2

    # ── Few-Shot ───────────────────────────────────────────────────────────────
    few_shot_cypher_examples: int = 5

    # ── Ablation Flags ─────────────────────────────────────────────────────────
    enable_schema_enrichment: bool = True
    retrieval_mode: str = "hybrid"          # "hybrid" | "vector" | "bm25"
    enable_cypher_healing: bool = True
    enable_critic_validation: bool = True
    enable_reranker: bool = True
    enable_hallucination_grader: bool = True

    # ── Logging ────────────────────────────────────────────────────────────────
    log_level: str = "INFO"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the singleton Settings instance (cached after first call)."""
    return Settings()


# Module-level singleton — import with:
#   from src.config.settings import settings
settings: Settings = get_settings()
