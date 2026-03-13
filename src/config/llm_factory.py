"""EP-01: LLM client factory.

Builds InstrumentedLLM-wrapped ChatOpenAI instances pointed at a local
LM Studio endpoint (OpenAI-compatible API).
All callers import from here — no pipeline node constructs an LLM object directly.

Architecture: replace `ChatOpenAI` with any LangChain BaseChatModel subclass
(ChatOpenRouter, ChatAnthropic, ChatOllama, …) to switch provider.
Only this file changes — all pipeline nodes depend on LLMProtocol.

Thesis: ChatOpenAI → LM Studio @ http://localhost:1234/v1 (local model).
Set LMSTUDIO_BASE_URL, LLM_MODEL_REASONING, LLM_MODEL_EXTRACTION via env/.env
to customise the endpoint and model names.
"""

from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING

from langchain_openai import ChatOpenAI

from src.config.llm_client import InstrumentedLLM, LLMProtocol
from src.config.settings import settings

if TYPE_CHECKING:
    from langchain_core.embeddings import Embeddings


@lru_cache(maxsize=1)
def get_reasoning_llm() -> LLMProtocol:
    """Return a cached LLM for reasoning tasks (mapping, Cypher, grading).

    Thesis   : ChatOpenAI → LM Studio, T=0.0
    Swap to  : ChatOpenRouter | ChatAnthropic | ChatOllama
    """
    return InstrumentedLLM(
        ChatOpenAI(
            model=settings.llm_model_reasoning,
            temperature=settings.llm_temperature_reasoning,
            base_url=settings.lmstudio_base_url,
            api_key="lm-studio",  # LM Studio ignores auth; any non-empty string works
        ),
        name="reasoning",
        max_retries=settings.max_llm_retries,
    )


@lru_cache(maxsize=1)
def get_extraction_llm() -> LLMProtocol:
    """Return a cached SLM for JSON-mode extraction.

    Thesis   : ChatOpenAI → LM Studio, T=0.0, max_tokens=16384
    Originally designed for NuExtract (local GPU); any instruction-tuned
    model with JSON-mode support is a valid drop-in.

    Note: ``max_tokens`` is set high (16k) to prevent JSON truncation.
    ``chat_template_kwargs: {enable_thinking: false}`` disables chain-of-thought
    on Qwen3-style thinking models in LM Studio; silently ignored by non-thinking models.
    """
    return InstrumentedLLM(
        ChatOpenAI(
            model=settings.llm_model_extraction,
            temperature=settings.llm_temperature_extraction,
            max_tokens=settings.llm_max_tokens_extraction,
            base_url=settings.lmstudio_base_url,
            api_key="lm-studio",
            model_kwargs={"extra_body": {"chat_template_kwargs": {"enable_thinking": False}}},
        ),
        name="extraction",
        max_retries=settings.max_llm_retries,
    )


@lru_cache(maxsize=1)
def get_generation_llm() -> LLMProtocol:
    """Return a cached LLM for natural-language answer generation.

    Thesis   : ChatOpenAI → LM Studio, T=0.3
    Same model as reasoning but higher temperature for fluency.
    """
    return InstrumentedLLM(
        ChatOpenAI(
            model=settings.llm_model_reasoning,
            temperature=settings.llm_temperature_generation,
            base_url=settings.lmstudio_base_url,
            api_key="lm-studio",
        ),
        name="generation",
        max_retries=settings.max_llm_retries,
    )


@lru_cache(maxsize=1)
def get_embeddings() -> Embeddings:  # type: ignore[name-defined]
    """Return a cached embedding model (stub for TASK-23).

    This is a minimal stub implementation that provides dummy 1024-dim vectors
    (matching BGE-M3 dimensionality). Will be replaced with proper FlagEmbedding
    implementation in TASK-23.

    Returns:
        LangChain Embeddings protocol instance with dummy vectors.
    """
    from langchain_core.embeddings import Embeddings

    class _StubEmbeddings(Embeddings):
        """Stub embeddings returning zero vectors (1024-dim for BGE-M3 compatibility)."""

        def embed_documents(self, texts: list[str]) -> list[list[float]]:
            """Return dummy 1024-dim vectors for each text."""
            return [[0.0] * 1024 for _ in texts]

        def embed_query(self, text: str) -> list[float]:
            """Return dummy 1024-dim vector for query."""
            return [0.0] * 1024

    return _StubEmbeddings()



@lru_cache(maxsize=1)
def get_embeddings() -> Embeddings:  # type: ignore[name-defined]
    """Return a cached embedding model (stub for TASK-23).

    This is a minimal stub implementation that provides dummy 1024-dim vectors
    (matching BGE-M3 dimensionality). Will be replaced with proper FlagEmbedding
    implementation in TASK-23.

    Returns:
        LangChain Embeddings protocol instance with dummy vectors.
    """
    from langchain_core.embeddings import Embeddings

    class _StubEmbeddings(Embeddings):
        """Stub embeddings returning zero vectors (1024-dim for BGE-M3 compatibility)."""

        def embed_documents(self, texts: list[str]) -> list[list[float]]:
            """Return dummy 1024-dim vectors for each text."""
            return [[0.0] * 1024 for _ in texts]

        def embed_query(self, text: str) -> list[float]:
            """Return dummy 1024-dim vector for query."""
            return [0.0] * 1024

    return _StubEmbeddings()
