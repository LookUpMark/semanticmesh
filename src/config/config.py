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

    Override via environment variables (see settings.py for names).
    Non-sensitive defaults are defined here for visibility.
    """

    # ── Neo4j ──────────────────────────────────────────────────────────────────
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"

    # ── LLM Providers ──────────────────────────────────────────────────────────
    lmstudio_base_url: str = "http://localhost:1234/v1"
    openrouter_base_url: str = "https://openrouter.ai/api/v1"

    # ── LLM Models ─────────────────────────────────────────────────────────────
    llm_model_reasoning: str = "gpt-5.4-nano-2026-03-17"
    llm_model_extraction: str = "gpt-5.4-nano-2026-03-17"

    # Temperature: extraction/reasoning at 0.0 for deterministic JSON, generation at 0.3 for fluency
    llm_temperature_extraction: float = 0.0
    llm_temperature_reasoning: float = 0.0
    llm_temperature_generation: float = 0.3

    llm_max_tokens_extraction: int = 8192
    llm_max_tokens_reasoning: int = 4096

    # ── Embeddings & Reranking ─────────────────────────────────────────────────
    embedding_model: str = "BAAI/bge-m3"
    embedding_dimensions: int = 1024
    reranker_model: str = "BAAI/bge-reranker-v2-m3"
    reranker_top_k: int = 12

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

    # ── Ablation Flags ─────────────────────────────────────────────────────────
    enable_schema_enrichment: bool = False
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

    # ── Logging ────────────────────────────────────────────────────────────────
    log_level: str = "INFO"

    # ── Debug Tracing ───────────────────────────────────────────────────────────
    enable_debug_trace: bool = False
    trace_output_dir: str = "notebooks/ablation/ablation_results/traces/debug"
    trace_compress_large_fields: bool = True
    trace_truncate_length: int = 500
    trace_max_items: int = 100


# Default configuration instance
DEFAULT_CONFIG = AppConfig()
