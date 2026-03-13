"""Application configuration defaults.

Non-sensitive configuration values are defined here as a dataclass.
Sensitive values (API keys, passwords) should be set via environment variables
or .env file and are loaded in settings.py.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    """Default application configuration.

    These values can be overridden by environment variables. See settings.py
    for the environment variable names.

    Non-sensitive defaults are defined here for visibility and easy modification.
    """

    # ── Neo4j ──────────────────────────────────────────────────────────────────
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"

    # ── LLM Providers ──────────────────────────────────────────────────────────
    # LM Studio — local endpoint for extraction SLM
    lmstudio_base_url: str = "http://localhost:1234/v1"
    # OpenRouter — cloud endpoint for reasoning/generation LLM
    openrouter_base_url: str = "https://openrouter.ai/api/v1"

    # ── LLM Models ─────────────────────────────────────────────────────────────
    # Reasoning + generation: OpenRouter (override via LLM_MODEL_REASONING)
    llm_model_reasoning: str = "openai/gpt-oss-120b:free"
    # Extraction SLM: LM Studio local model (override via LLM_MODEL_EXTRACTION)
    llm_model_extraction: str = "local-model"

    # Temperature settings
    llm_temperature_extraction: float = 0.0
    llm_temperature_reasoning: float = 0.0
    llm_temperature_generation: float = 0.3

    # Max output tokens for extraction (16k to avoid truncated JSON)
    llm_max_tokens_extraction: int = 16384

    # Max output tokens for reasoning LLM (caps thinking+output; JSON payloads rarely need >4k)
    llm_max_tokens_reasoning: int = 16384

    # ── Embeddings & Reranking ─────────────────────────────────────────────────
    embedding_model: str = "BAAI/bge-m3"
    reranker_model: str = "BAAI/bge-reranker-large"
    reranker_top_k: int = 5

    # ── Entity Resolution ──────────────────────────────────────────────────────
    er_blocking_top_k: int = 10
    er_similarity_threshold: float = 0.75

    # ── Confidence & Loop Guards ───────────────────────────────────────────────
    confidence_threshold: float = 0.90
    max_reflection_attempts: int = 3
    max_cypher_healing_attempts: int = 3
    max_hallucination_retries: int = 3
    max_llm_retries: int = 3

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
    retrieval_mode: str = "hybrid"  # "hybrid" | "vector" | "bm25"
    enable_cypher_healing: bool = True
    enable_critic_validation: bool = True
    enable_reranker: bool = True
    enable_hallucination_grader: bool = True

    # ── Logging ────────────────────────────────────────────────────────────────
    log_level: str = "INFO"


# Default configuration instance
DEFAULT_CONFIG = AppConfig()
