"""EP-01: LLM client factory.

Explicit per-tier configuration — each tier has its own provider, model,
endpoint, and reasoning effort set via environment variables::

    LLM_PROVIDER_REASONING=openai
    LLM_MODEL_REASONING=gpt-5.4-nano-2026-03-17
    LLM_ENDPOINT_REASONING=https://api.openai.com/v1
    LLM_EFFORT_REASONING=high

Fallback chain (backward compatible):
  1. Per-tier ``LLM_PROVIDER_<TIER>`` (new, explicit)
  2. Global ``LLM_PROVIDER`` (legacy override)
  3. ``detect_provider(model)`` (legacy auto-detection from model name prefix)

All callers import from here — no pipeline node constructs an LLM directly.
To swap providers, change the ``.env`` file; all nodes depend on ``LLMProtocol``.

Cached factory functions
------------------------
  * :func:`get_reasoning_llm()`  — mapping, validation, Cypher (T=0.0, effort=high)
  * :func:`get_extraction_llm()` — triplet extraction (T=0.0, effort=minimal)
  * :func:`get_generation_llm()` — answer generation (T=0.3, effort=none)
  * :func:`get_lightweight_llm()` — entity resolution, enrichment (T=0.0, effort=minimal)
  * :func:`get_midtier_llm()`    — RAG mapping, grading (T=0.0, effort=medium)
"""

from __future__ import annotations

from functools import lru_cache

from src.config.llm_client import FallbackLLM, InstrumentedLLM, LLMProtocol
from src.config.model_builders import (
    _build_anthropic_chat,
    _build_azure_chat,
    _build_bedrock_chat,
    _build_cohere_chat,
    _build_google_chat,
    _build_huggingface_chat,
    _build_lmstudio_chat,
    _build_mistral_chat,
    _build_ollama_chat,
    _build_openai_chat,
    _build_openai_compatible_chat,
    _build_openrouter_chat,
)
from src.config.provider_detection import (
    _is_free_model,
    _strip_free_suffix,
    detect_provider,
    is_openai_reasoning_model,
)
from src.config.settings import get_settings, reload_settings

__all__ = [
    "make_llm",
    "get_reasoning_llm",
    "get_extraction_llm",
    "get_generation_llm",
    "get_lightweight_llm",
    "get_midtier_llm",
    "reconfigure_from_env",
    "detect_provider",
    "LLMProtocol",
]


# ── Helpers ───────────────────────────────────────────────────────────────────


def _instrument(chat_like: LLMProtocol, role: str) -> LLMProtocol:
    """Wrap an LLM client with instrumentation and retry logic."""
    return InstrumentedLLM(chat_like, name=role, max_retries=get_settings().max_llm_retries)


def _resolve_provider(tier_provider: str, model: str) -> str:
    """Resolve LLM provider: explicit tier > global override > auto-detection."""
    if tier_provider:
        return tier_provider
    s = get_settings()
    if s.llm_provider and s.llm_provider != "auto":
        return s.llm_provider
    return detect_provider(model)


def _build_effort_kwargs(effort: str, provider: str) -> dict | None:
    """Build reasoning-effort keyword arguments for the given provider.

    Returns ``None`` when *effort* is empty/``"none"`` or the provider
    does not support reasoning-effort control.
    """
    if not effort or effort == "none":
        return None
    if provider == "openrouter":
        return {"reasoning": {"effort": effort}}
    if provider == "openai":
        return {"reasoning_effort": effort}
    return None


# ── Public factory function ───────────────────────────────────────────────────


def make_llm(
    model: str,
    temperature: float = 0.0,
    max_tokens: int | None = None,
    role: str = "custom",
    *,
    openrouter_api_key: str | None = None,
    openrouter_base_url: str | None = None,
    openai_api_key: str | None = None,
    lmstudio_base_url: str | None = None,
    provider_base_url: str | None = None,
    provider: str | None = None,
    extra_model_kwargs: dict | None = None,
    enable_fallback: bool = True,
) -> LLMProtocol:
    """Create an instrumented LLM, auto-detecting the provider from *model*.

    Provider resolution
    -------------------
    When *provider* is given (and != ``"auto"``) it is used directly.
    Otherwise the provider is inferred from the model name prefix (see
    :func:`src.config.provider_detection.detect_provider`).

    The ``provider_base_url`` parameter is forwarded to the resolved builder
    so that any provider can be pointed at a custom endpoint.

    Automatic free→paid fallback
    ----------------------------
    If *enable_fallback* is True (default) and the model name ends with ``:free``,
    a FallbackLLM is created that automatically switches to the paid version when
    rate limits (HTTP 429) are encountered.
    """
    resolved_provider = (
        provider if (provider and provider != "auto") else None
    ) or detect_provider(model)
    is_free = _is_free_model(model)
    paid_model = _strip_free_suffix(model) if is_free else model

    if resolved_provider == "openrouter":
        if is_free and enable_fallback and model != paid_model:
            primary_chat = _build_openrouter_chat(
                model,
                temperature=temperature,
                max_tokens=max_tokens,
                openrouter_api_key=openrouter_api_key,
                openrouter_base_url=openrouter_base_url or provider_base_url,
                extra_model_kwargs=extra_model_kwargs,
            )
            fallback_chat = _build_openrouter_chat(
                paid_model,
                temperature=temperature,
                max_tokens=max_tokens,
                openrouter_api_key=openrouter_api_key,
                openrouter_base_url=openrouter_base_url or provider_base_url,
                extra_model_kwargs=extra_model_kwargs,
            )
            fallback_llm = FallbackLLM(
                primary=primary_chat,
                fallback=fallback_chat,
                name=role,
            )
            return _instrument(fallback_llm, role)

        chat = _build_openrouter_chat(
            model,
            temperature=temperature,
            max_tokens=max_tokens,
            openrouter_api_key=openrouter_api_key,
            openrouter_base_url=openrouter_base_url or provider_base_url,
            extra_model_kwargs=extra_model_kwargs,
        )
        return _instrument(chat, role)

    if resolved_provider == "openai":
        chat = _build_openai_chat(
            model,
            temperature=temperature,
            max_tokens=max_tokens,
            openai_api_key=openai_api_key,
            extra_model_kwargs=extra_model_kwargs,
            openai_base_url=provider_base_url,
        )
        return _instrument(chat, role)

    if resolved_provider == "anthropic":
        return _instrument(
            _build_anthropic_chat(
                model,
                temperature=temperature,
                max_tokens=max_tokens,
                base_url=provider_base_url,
            ),
            role,
        )

    if resolved_provider == "ollama":
        return _instrument(
            _build_ollama_chat(
                model,
                temperature=temperature,
                max_tokens=max_tokens,
                base_url=provider_base_url,
            ),
            role,
        )

    if resolved_provider == "google":
        return _instrument(
            _build_google_chat(
                model,
                temperature=temperature,
                max_tokens=max_tokens,
                base_url=provider_base_url,
            ),
            role,
        )

    if resolved_provider == "bedrock":
        return _instrument(
            _build_bedrock_chat(
                model,
                temperature=temperature,
                max_tokens=max_tokens,
                base_url=provider_base_url,
            ),
            role,
        )

    if resolved_provider == "azure":
        return _instrument(
            _build_azure_chat(
                model,
                temperature=temperature,
                max_tokens=max_tokens,
                base_url=provider_base_url,
            ),
            role,
        )

    if resolved_provider == "mistral":
        return _instrument(
            _build_mistral_chat(
                model,
                temperature=temperature,
                max_tokens=max_tokens,
                base_url=provider_base_url,
            ),
            role,
        )

    if resolved_provider == "huggingface":
        return _instrument(
            _build_huggingface_chat(
                model,
                temperature=temperature,
                max_tokens=max_tokens,
                base_url=provider_base_url,
            ),
            role,
        )

    if resolved_provider == "cohere":
        return _instrument(
            _build_cohere_chat(model, temperature=temperature, max_tokens=max_tokens),
            role,
        )

    if resolved_provider in ("groq", "together", "nvidia", "deepseek", "xai"):
        return _instrument(
            _build_openai_compatible_chat(
                model,
                provider=resolved_provider,
                temperature=temperature,
                max_tokens=max_tokens,
                base_url_override=provider_base_url,
                extra_model_kwargs=extra_model_kwargs,
            ),
            role,
        )

    effective_model = model
    if model.lower().startswith("lmstudio/"):
        effective_model = model[len("lmstudio/") :]
    effective_base_url = provider_base_url or lmstudio_base_url
    chat = _build_lmstudio_chat(
        effective_model,
        temperature=temperature,
        max_tokens=max_tokens,
        lmstudio_base_url=effective_base_url,
        extra_model_kwargs=extra_model_kwargs,
    )
    return _instrument(chat, role)


# ── Cached pipeline factories ─────────────────────────────────────────────────


def reconfigure_from_env() -> None:
    """Clear all cached instances so they re-read from ``os.environ`` on next call.

    Call this from the notebook after changing ``os.environ`` to pick up new
    model names or API keys without restarting the kernel.
    """
    reload_settings()
    get_reasoning_llm.cache_clear()
    get_extraction_llm.cache_clear()
    get_generation_llm.cache_clear()
    get_lightweight_llm.cache_clear()
    get_midtier_llm.cache_clear()


@lru_cache(maxsize=1)
def get_reasoning_llm() -> LLMProtocol:
    """Reasoning LLM — T=0.0, effort=high (default).

    Used for: schema mapping, Actor-Critic, LLM judge, hallucination grader,
    schema enrichment, Cypher generation/healing.

    Configuration (env vars):
      ``LLM_PROVIDER_REASONING``, ``LLM_MODEL_REASONING``,
      ``LLM_ENDPOINT_REASONING``, ``LLM_EFFORT_REASONING``.
    """
    s = get_settings()
    provider = _resolve_provider(s.llm_provider_reasoning, s.llm_model_reasoning)
    effort = s.llm_effort_reasoning or "high"
    effort_kwargs = _build_effort_kwargs(effort, provider)
    return make_llm(
        model=s.llm_model_reasoning,
        temperature=s.llm_temperature_reasoning,
        max_tokens=s.llm_max_tokens_reasoning,
        role="reasoning",
        provider=provider,
        provider_base_url=s.llm_endpoint_reasoning or None,
        extra_model_kwargs=effort_kwargs,
    )


@lru_cache(maxsize=1)
def get_extraction_llm() -> LLMProtocol:
    """Extraction SLM — T=0.0, effort=minimal (default).

    Used for: triplet extraction from PDF chunks.

    Configuration (env vars):
      ``LLM_PROVIDER_EXTRACTION``, ``LLM_MODEL_EXTRACTION``,
      ``LLM_ENDPOINT_EXTRACTION``, ``LLM_EFFORT_EXTRACTION``.
    """
    s = get_settings()
    provider = _resolve_provider(s.llm_provider_extraction, s.llm_model_extraction)
    effort = s.llm_effort_extraction
    if not effort:
        effort = "minimal" if provider in ("openai", "openrouter") and is_openai_reasoning_model(
            s.llm_model_extraction
        ) else ""
    effort_kwargs = _build_effort_kwargs(effort, provider) if effort else None
    return make_llm(
        model=s.llm_model_extraction,
        temperature=s.llm_temperature_extraction,
        max_tokens=s.llm_max_tokens_extraction,
        role="extraction",
        provider=provider,
        provider_base_url=s.llm_endpoint_extraction or None,
        extra_model_kwargs=effort_kwargs,
    )


@lru_cache(maxsize=1)
def get_generation_llm() -> LLMProtocol:
    """Generation LLM — T=0.3.

    Uses the reasoning model by default (or ``LLM_MODEL_GENERATION`` if set).

    Configuration (env vars):
      ``LLM_PROVIDER_GENERATION``, ``LLM_MODEL_GENERATION``,
      ``LLM_ENDPOINT_GENERATION``, ``LLM_EFFORT_GENERATION``.
    """
    s = get_settings()
    model = s.llm_model_generation or s.llm_model_reasoning
    provider = _resolve_provider(s.llm_provider_generation, model)
    effort_kwargs = (
        _build_effort_kwargs(s.llm_effort_generation, provider)
        if s.llm_effort_generation
        else None
    )
    return make_llm(
        model=model,
        temperature=s.llm_temperature_generation,
        max_tokens=s.llm_max_tokens_reasoning,
        role="generation",
        provider=provider,
        provider_base_url=s.llm_endpoint_generation or None,
        extra_model_kwargs=effort_kwargs,
    )


@lru_cache(maxsize=1)
def get_lightweight_llm() -> LLMProtocol:
    """Lightweight LLM — reuses extraction model, T=0.0, effort=minimal (default).

    Used for: entity resolution judge, schema enrichment.

    Configuration (env vars):
      Reuses ``LLM_PROVIDER_EXTRACTION``, ``LLM_MODEL_EXTRACTION``,
      ``LLM_ENDPOINT_EXTRACTION``, ``LLM_EFFORT_EXTRACTION``.
    """
    s = get_settings()
    provider = _resolve_provider(s.llm_provider_extraction, s.llm_model_extraction)
    effort = s.llm_effort_extraction
    if not effort:
        effort = "minimal" if provider in ("openai", "openrouter") and is_openai_reasoning_model(
            s.llm_model_extraction
        ) else ""
    effort_kwargs = _build_effort_kwargs(effort, provider) if effort else None
    return make_llm(
        model=s.llm_model_extraction,
        temperature=s.llm_temperature_extraction,
        max_tokens=s.llm_max_tokens_extraction,
        role="lightweight",
        provider=provider,
        provider_base_url=s.llm_endpoint_extraction or None,
        extra_model_kwargs=effort_kwargs,
    )


@lru_cache(maxsize=1)
def get_midtier_llm() -> LLMProtocol:
    """Mid-tier LLM — T=0.0, effort=medium (default).

    Used for: RAG semantic mapping, Actor-Critic validation, hallucination grading.

    Configuration (env vars):
      ``LLM_PROVIDER_MIDTIER``, ``LLM_MODEL_MIDTIER``,
      ``LLM_ENDPOINT_MIDTIER``, ``LLM_EFFORT_MIDTIER``.
    """
    s = get_settings()
    provider = _resolve_provider(s.llm_provider_midtier, s.llm_model_midtier)
    effort = s.llm_effort_midtier or "medium"
    effort_kwargs = _build_effort_kwargs(effort, provider)
    return make_llm(
        model=s.llm_model_midtier,
        temperature=s.llm_temperature_reasoning,
        max_tokens=s.llm_max_tokens_reasoning,
        role="midtier",
        provider=provider,
        provider_base_url=s.llm_endpoint_midtier or None,
        extra_model_kwargs=effort_kwargs,
    )
