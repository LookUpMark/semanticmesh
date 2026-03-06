"""EP-01: LLM client factory.

Builds InstrumentedLLM-wrapped ChatOpenRouter instances from settings.
All callers import from here — no pipeline node constructs an LLM object directly.

Architecture: replace `ChatOpenRouter` with any LangChain BaseChatModel subclass
(ChatOpenAI, ChatAnthropic, ChatOllama, ChatHuggingFace, …) to switch provider.
Only this file changes — all pipeline nodes depend on LLMProtocol.

Thesis: ChatOpenRouter @ OpenRouter Free Tier.  OPENROUTER_API_KEY must be set.
"""

from __future__ import annotations

from functools import lru_cache

from langchain_openrouter import ChatOpenRouter

from src.config.llm_client import InstrumentedLLM, LLMProtocol
from src.config.settings import settings


@lru_cache(maxsize=1)
def get_reasoning_llm() -> LLMProtocol:
    """Return a cached LLM for reasoning tasks (mapping, Cypher, grading).

    Thesis   : ChatOpenRouter @ qwen/qwen3-coder:free, T=0.0
    Swap to  : ChatOpenAI(model="gpt-4o") | ChatAnthropic(model="claude-3-5-sonnet-20241022")
    """
    return InstrumentedLLM(
        ChatOpenRouter(
            model=settings.llm_model_reasoning,
            temperature=settings.llm_temperature_reasoning,
        ),
        name="reasoning",
        max_retries=settings.max_llm_retries,
    )


@lru_cache(maxsize=1)
def get_extraction_llm() -> LLMProtocol:
    """Return a cached SLM for JSON-mode extraction.

    Thesis   : ChatOpenRouter @ qwen/qwen3-next-80b-a3b-instruct:free, T=0.0
    Originally designed for NuExtract (local GPU); any instruction-tuned
    model with JSON-mode support is a valid drop-in.
    """
    return InstrumentedLLM(
        ChatOpenRouter(
            model=settings.llm_model_extraction,
            temperature=settings.llm_temperature_extraction,
        ),
        name="extraction",
        max_retries=settings.max_llm_retries,
    )


@lru_cache(maxsize=1)
def get_generation_llm() -> LLMProtocol:
    """Return a cached LLM for natural-language answer generation.

    Thesis   : ChatOpenRouter @ qwen/qwen3-coder:free, T=0.3
    Same model as reasoning but higher temperature for fluency.
    """
    return InstrumentedLLM(
        ChatOpenRouter(
            model=settings.llm_model_reasoning,
            temperature=settings.llm_temperature_generation,
        ),
        name="generation",
        max_retries=settings.max_llm_retries,
    )
