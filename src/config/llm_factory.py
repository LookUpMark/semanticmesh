"""EP-01: LLM client factory.

Split-routing architecture:
  * Reasoning + Generation → OpenRouter (cloud, ``openai/gpt-oss-120b:free``)
  * Extraction SLM         → LM Studio  (local, ``qwen3.5-35b-a3b``)

All callers import from here — no pipeline node constructs an LLM directly.
To swap providers, only this file changes; all nodes depend on ``LLMProtocol``.

Environment variables:
  OPENROUTER_API_KEY   — required for reasoning/generation
  LMSTUDIO_BASE_URL    — LM Studio endpoint (default: http://localhost:1234/v1)
  LLM_MODEL_REASONING  — override reasoning model (default: openai/gpt-oss-120b:free)
  LLM_MODEL_EXTRACTION — override extraction model (default: local-model)

Provider auto-detection
-----------------------
Provider detection logic is in :mod:`src.config.provider_detection`.
Model builders are in :mod:`src.config.model_builders`.

Cached factory functions
------------------------
  * :func:`get_reasoning_llm()` — OpenRouter, T=0.0 (mapping, validation, Cypher)
  * :func:`get_extraction_llm()` — Auto-detected, T=0.0 (triplet extraction)
  * :func:`get_generation_llm()` — OpenRouter, T=0.3 (answer generation)
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


# ── Public factory function ───────────────────────────────────────────────────


def _instrument(chat_like: LLMProtocol, role: str) -> LLMProtocol:
    """Wrap an LLM client with instrumentation and retry logic."""
    return InstrumentedLLM(chat_like, name=role, max_retries=get_settings().max_llm_retries)


def make_llm(
    model: str,
    temperature: float = 0.0,
    max_tokens: int | None = None,
    role: str = "custom",
    *,
    # Provider overrides (auto-detected from model name if not given)
    openrouter_api_key: str | None = None,
    openrouter_base_url: str | None = None,
    openai_api_key: str | None = None,
    lmstudio_base_url: str | None = None,
    # Generic base URL override — forwarded to any OpenAI-compatible provider
    # (Ollama, LMStudio, Groq self-hosted, custom proxy, etc.)
    provider_base_url: str | None = None,
    # Optional explicit provider override — if set (and != "auto"), skips
    # detect_provider() and uses this string directly.
    provider: str | None = None,
    extra_model_kwargs: dict | None = None,
    enable_fallback: bool = True,
) -> LLMProtocol:
    """Create an instrumented LLM, auto-detecting the provider from *model*.

    Provider detection
    ------------------
    Provider is inferred from the model name prefix (see
    :func:`src.config.provider_detection.detect_provider`):

    - ``ollama/<model>``    → Ollama (requires ``langchain-ollama``, falls back to compat)
    - ``google/<model>``    → Google Gemini (requires ``langchain-google-genai``)
    - ``bedrock/<model>``   → AWS Bedrock (requires ``langchain-aws``)
    - ``azure/<model>``     → Azure OpenAI (already in ``langchain-openai``)
    - ``groq/<model>``      → Groq API (OpenAI-compat, no extra package)
    - ``mistral/<model>``   → Mistral AI (requires ``langchain-mistralai``)
    - ``together/<model>``  → Together AI (OpenAI-compat, no extra package)
    - ``huggingface/<model>`` / ``hf/<model>`` → HuggingFace Hub
      (requires ``langchain-huggingface``)
    - ``cohere/<model>``    → Cohere (requires ``langchain-cohere``, falls back to compat)
    - ``nvidia/<model>``    → Nvidia NIM (OpenAI-compat, no extra package)
    - ``deepseek/<model>``  → DeepSeek (OpenAI-compat, no extra package)
    - ``xai/<model>``       → xAI Grok (OpenAI-compat, no extra package)
    - ``<provider>/<model>`` (any other slash) → OpenRouter
    - ``gpt-*``, ``o1-*``, ``o4-*`` (no slash) → OpenAI direct
    - ``claude-*`` (no slash) → Anthropic direct
    - ``gemini-*``, ``mistral-*``, ``deepseek-*``, ``grok-*`` → respective provider
    - anything else → LM Studio local endpoint

    Automatic free→paid fallback
    ----------------------------
    If *enable_fallback* is True (default) and the model name ends with ``:free``,
    a FallbackLLM is created that automatically switches to the paid version when
    rate limits (HTTP 429) are encountered.

    Examples
    --------
    >>> make_llm("openai/gpt-oss-120b:free")          # → FallbackLLM (free→paid)
    >>> make_llm("gpt-4o")                            # → InstrumentedLLM (OpenAI)
    >>> make_llm("claude-3-5-sonnet-20241022")        # → InstrumentedLLM (Anthropic)
    >>> make_llm("ollama/llama3.1")                   # → InstrumentedLLM (Ollama)
    >>> make_llm("groq/llama3-70b-8192")              # → InstrumentedLLM (Groq)
    >>> make_llm("gemini-2.0-flash")                  # → InstrumentedLLM (Google)
    >>> make_llm("local-model")                       # → InstrumentedLLM (LM Studio)
    """
    # Resolve provider: explicit override > auto-detection from model name
    resolved_provider = (provider if (provider and provider != "auto") else None) or detect_provider(model)
    is_free = _is_free_model(model)
    paid_model = _strip_free_suffix(model) if is_free else model

    if resolved_provider == "openrouter":
        if is_free and enable_fallback and model != paid_model:
            primary_chat = _build_openrouter_chat(
                model,
                temperature=temperature,
                max_tokens=max_tokens,
                openrouter_api_key=openrouter_api_key,
                openrouter_base_url=openrouter_base_url,
                extra_model_kwargs=extra_model_kwargs,
            )
            fallback_chat = _build_openrouter_chat(
                paid_model,
                temperature=temperature,
                max_tokens=max_tokens,
                openrouter_api_key=openrouter_api_key,
                openrouter_base_url=openrouter_base_url,
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
            openrouter_base_url=openrouter_base_url,
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
        )
        return _instrument(chat, role)

    if resolved_provider == "anthropic":
        return _instrument(
            _build_anthropic_chat(model, temperature=temperature, max_tokens=max_tokens),
            role,
        )

    if resolved_provider == "ollama":
        return _instrument(
            _build_ollama_chat(
                model, temperature=temperature, max_tokens=max_tokens, base_url=provider_base_url
            ),
            role,
        )

    if resolved_provider == "google":
        return _instrument(
            _build_google_chat(model, temperature=temperature, max_tokens=max_tokens), role
        )

    if resolved_provider == "bedrock":
        return _instrument(
            _build_bedrock_chat(model, temperature=temperature, max_tokens=max_tokens), role
        )

    if resolved_provider == "azure":
        return _instrument(
            _build_azure_chat(model, temperature=temperature, max_tokens=max_tokens), role
        )

    if resolved_provider == "mistral":
        return _instrument(
            _build_mistral_chat(model, temperature=temperature, max_tokens=max_tokens), role
        )

    if resolved_provider == "huggingface":
        return _instrument(
            _build_huggingface_chat(model, temperature=temperature, max_tokens=max_tokens), role
        )

    if resolved_provider == "cohere":
        return _instrument(
            _build_cohere_chat(model, temperature=temperature, max_tokens=max_tokens), role
        )

    # OpenAI-compatible providers: groq, together, nvidia, deepseek, xai
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

    # Default: LM Studio local endpoint
    # Strip explicit "lmstudio/" prefix so the model name matches what LM Studio serves
    effective_model = model
    if model.lower().startswith("lmstudio/"):
        effective_model = model[len("lmstudio/"):]
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
    reload_settings()  # re-reads os.environ into a fresh Settings object
    get_reasoning_llm.cache_clear()
    get_extraction_llm.cache_clear()
    get_generation_llm.cache_clear()
    get_lightweight_llm.cache_clear()
    get_midtier_llm.cache_clear()


@lru_cache(maxsize=1)
def get_reasoning_llm() -> LLMProtocol:
    """Reasoning LLM — T=0.0.

    Used for: schema mapping, Actor-Critic, LLM judge, hallucination grader,
    schema enrichment, Cypher generation/healing.

    ``reasoning_effort=medium`` (OpenAI) / ``reasoning.effort=medium`` (OpenRouter)
    gives the model sufficient thinking budget for multi-hop synthesis across chunks.
    """
    s = get_settings()
    provider_override = s.llm_provider if s.llm_provider != "auto" else None
    effective_provider = provider_override or detect_provider(s.llm_model_reasoning)
    if effective_provider == "openrouter":
        low_reasoning: dict | None = {"reasoning": {"effort": "medium"}}
    elif effective_provider == "openai":
        low_reasoning = {"reasoning_effort": "medium"}
    else:
        low_reasoning = None
    return make_llm(
        model=s.llm_model_reasoning,
        temperature=s.llm_temperature_reasoning,
        max_tokens=s.llm_max_tokens_reasoning,
        role="reasoning",
        provider=provider_override,
        extra_model_kwargs=low_reasoning,
    )


@lru_cache(maxsize=1)
def get_extraction_llm() -> LLMProtocol:
    """Extraction SLM — provider auto-detected from model name (or from settings.llm_provider), T=0.0.

    Used for: triplet extraction from PDF chunks.

    - LM Studio local models (e.g. ``local-model``, ``qwen3-8b``): JSON mode,
      ``enable_thinking: false`` to disable Qwen3 chain-of-thought.
    - OpenRouter models (e.g. ``openai/gpt-oss-20b:free``): routed to OpenRouter.
    - OpenAI direct (e.g. ``gpt-4o-mini``): routed to OpenAI.
    """
    s = get_settings()
    provider_override = s.llm_provider if s.llm_provider != "auto" else None
    effective_provider = provider_override or detect_provider(s.llm_model_extraction)

    if effective_provider == "lmstudio":
        return _instrument(
            make_llm(
                model=s.llm_model_extraction,
                temperature=s.llm_temperature_extraction,
                max_tokens=s.llm_max_tokens_extraction,
                role="extraction",
                provider="lmstudio",
            ),
            "extraction",
        )

    # Cloud model (OpenRouter, OpenAI, Anthropic): use make_llm for provider routing
    # For OpenAI reasoning models (o-series, gpt-5*): use minimal reasoning effort.
    # reasoning_effort="none" is not supported; "minimal" is the lowest valid value.
    # Standard chat models (gpt-4o*) don't accept reasoning_effort at all → pass None.
    # Note: OpenRouter models have mandatory reasoning that cannot be overridden here.
    no_reasoning: dict | None = None
    if effective_provider == "openai" and is_openai_reasoning_model(s.llm_model_extraction):
        no_reasoning = {"reasoning_effort": "minimal"}
    return make_llm(
        model=s.llm_model_extraction,
        temperature=s.llm_temperature_extraction,
        max_tokens=s.llm_max_tokens_extraction,
        role="extraction",
        provider=provider_override,
        extra_model_kwargs=no_reasoning,
    )


@lru_cache(maxsize=1)
def get_generation_llm() -> LLMProtocol:
    """Generation LLM — OpenRouter, T=0.3.

    Same model as reasoning but higher temperature for answer fluency.
    Thinking is mandatory for this model; OpenRouter keeps it in a separate
    field so the content returned is always clean prose.
    """
    s = get_settings()
    provider_override = s.llm_provider if s.llm_provider != "auto" else None
    return make_llm(
        model=s.llm_model_reasoning,
        temperature=s.llm_temperature_generation,
        max_tokens=s.llm_max_tokens_reasoning,
        role="generation",
        provider=provider_override,
    )


@lru_cache(maxsize=1)
def get_lightweight_llm() -> LLMProtocol:
    """Lightweight LLM — nano model with reasoning disabled, T=0.0.

    Used for simple classification tasks: entity resolution judge,
    schema enrichment. Uses the extraction model (nano) with
    ``reasoning_effort=minimal`` (lowest valid value for gpt-5* models).
    """
    s = get_settings()
    provider_override = s.llm_provider if s.llm_provider != "auto" else None
    no_reasoning: dict | None = None
    if is_openai_reasoning_model(s.llm_model_extraction):
        no_reasoning = {"reasoning_effort": "minimal"}
    return make_llm(
        model=s.llm_model_extraction,
        temperature=s.llm_temperature_extraction,
        max_tokens=s.llm_max_tokens_extraction,
        role="lightweight",
        provider=provider_override,
        extra_model_kwargs=no_reasoning,
    )


@lru_cache(maxsize=1)
def get_midtier_llm() -> LLMProtocol:
    """Mid-tier LLM — mini model with low reasoning, T=0.0.

    Used for tasks requiring moderate intelligence: RAG semantic mapping,
    Actor-Critic validation, hallucination grading. Faster and cheaper
    than the full reasoning model while still providing good accuracy.
    """
    s = get_settings()
    provider_override = s.llm_provider if s.llm_provider != "auto" else None
    effective_provider = provider_override or detect_provider(s.llm_model_midtier)
    if effective_provider == "openrouter":
        low_reasoning: dict | None = {"reasoning": {"effort": "low"}}
    elif effective_provider == "openai":
        low_reasoning = {"reasoning_effort": "low"}
    else:
        low_reasoning = None
    return make_llm(
        model=s.llm_model_midtier,
        temperature=s.llm_temperature_reasoning,
        max_tokens=s.llm_max_tokens_reasoning,
        role="midtier",
        provider=provider_override,
        extra_model_kwargs=low_reasoning,
    )
