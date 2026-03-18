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
"""

from __future__ import annotations

from functools import lru_cache

from langchain_openai import ChatOpenAI

from src.config.llm_client import FallbackLLM, InstrumentedLLM, LLMProtocol
from src.config.settings import get_settings, reload_settings

# ── Provider auto-detection ────────────────────────────────────────────────────

_OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
_LMSTUDIO_DEFAULT_URL = "http://localhost:1234/v1"

# Model name prefixes that map to direct provider APIs (no slash in the name)
_OPENAI_PREFIXES = ("gpt-", "o1-", "o2-", "o3-", "o4-", "text-")
_ANTHROPIC_PREFIXES = ("claude-",)


def detect_provider(model: str) -> str:
    """Infer the LLM provider from the model name string.

    Rules (in order):
    - ``provider/model`` (contains ``/``) → **OpenRouter**
      e.g. ``openai/gpt-oss-120b:free``, ``anthropic/claude-3.5-sonnet``,
           ``meta-llama/llama-3.3-70b-instruct:free``
    - Starts with ``gpt-``, ``o1-``, ``o3-``, ``o4-`` (no slash) → **openai** (direct)
    - Starts with ``claude-`` (no slash) → **anthropic** (direct)
    - Anything else → **lmstudio** (local)
    """
    if "/" in model:
        return "openrouter"
    m = model.lower()
    if m.startswith(_OPENAI_PREFIXES):
        return "openai"
    if m.startswith(_ANTHROPIC_PREFIXES):
        return "anthropic"
    return "lmstudio"


def _strip_free_suffix(model: str) -> str:
    """Remove the :free suffix from a model name if present.

    Examples:
        >>> _strip_free_suffix("openai/gpt-oss-120b:free")
        "openai/gpt-oss-120b"
        >>> _strip_free_suffix("meta-llama/llama-3.3-70b-instruct:free")
        "meta-llama/llama-3.3-70b-instruct"
        >>> _strip_free_suffix("openai/gpt-oss-120b")
        "openai/gpt-oss-120b"
    """
    if model.endswith(":free"):
        return model[:-5]
    return model


def _is_free_model(model: str) -> bool:
    """Check if a model name has the :free suffix."""
    return model.endswith(":free")


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
    extra_model_kwargs: dict | None = None,
    enable_fallback: bool = True,
) -> LLMProtocol:
    """Create an instrumented LLM, auto-detecting the provider from *model*.

    Provider detection
    ------------------
    - ``provider/model`` (contains ``/``) → OpenRouter
    - ``gpt-*``, ``o1-*``, ``o3-*`` (no slash) → OpenAI direct
    - ``claude-*`` (no slash) → Anthropic direct (requires ``langchain-anthropic``)
    - anything else → LM Studio local endpoint

    Automatic free→paid fallback
    ----------------------------
    If *enable_fallback* is True (default) and the model name ends with ``:free``,
    a FallbackLLM is created that automatically switches to the paid version when
    rate limits (HTTP 429) are encountered. This provides seamless operation without
    manual intervention.

    Examples
    --------
    >>> make_llm("openai/gpt-oss-120b:free")          # → FallbackLLM (free→paid)
    >>> make_llm("gpt-4o")                            # → InstrumentedLLM (OpenAI)
    >>> make_llm("claude-3-5-sonnet-20241022")        # → InstrumentedLLM (Anthropic)
    >>> make_llm("local-model")                       # → InstrumentedLLM (LM Studio)
    >>> make_llm("openai/gpt-oss-120b:free", enable_fallback=False)  # → No fallback
    """
    provider = detect_provider(model)
    is_free = _is_free_model(model)
    paid_model = _strip_free_suffix(model) if is_free else model

    # Helper to create a ChatOpenAI instance for OpenRouter
    def _create_openrouter_chat(model_name: str) -> ChatOpenAI:
        _api_key = openrouter_api_key or get_settings().openrouter_api_key.get_secret_value()
        _base_url = openrouter_base_url or get_settings().openrouter_base_url
        return ChatOpenAI(
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            base_url=_base_url,
            api_key=_api_key,
            **({"model_kwargs": extra_model_kwargs} if extra_model_kwargs else {}),
        )

    if provider == "openrouter":
        # Create fallback pair for free models
        if is_free and enable_fallback and model != paid_model:
            primary_chat = _create_openrouter_chat(model)
            fallback_chat = _create_openrouter_chat(paid_model)
            fallback_llm = FallbackLLM(
                primary=primary_chat,
                fallback=fallback_chat,
                name=role,
            )
            # Instrument the fallback wrapper too, so all nodes get the same wrapper type.
            return InstrumentedLLM(
                fallback_llm,
                name=role,
                max_retries=get_settings().max_llm_retries,
            )
        # Single model (non-free or fallback disabled)
        chat = _create_openrouter_chat(model)
        return InstrumentedLLM(chat, name=role, max_retries=get_settings().max_llm_retries)

    elif provider == "openai":
        import os

        _api_key = openai_api_key or os.environ.get("OPENAI_API_KEY", "")
        chat = ChatOpenAI(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=_api_key,
            **({"model_kwargs": extra_model_kwargs} if extra_model_kwargs else {}),
        )
        return InstrumentedLLM(chat, name=role, max_retries=get_settings().max_llm_retries)

    elif provider == "anthropic":
        try:
            from langchain_anthropic import ChatAnthropic  # type: ignore[import]
        except ImportError as exc:  # pragma: no cover
            raise ImportError(
                "Install langchain-anthropic to use Anthropic models directly: "
                "pip install langchain-anthropic"
            ) from exc
        import os

        _api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        return InstrumentedLLM(
            ChatAnthropic(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens or 4096,
                api_key=_api_key,
            ),
            name=role,
            max_retries=get_settings().max_llm_retries,
        )

    else:  # lmstudio
        _base_url = lmstudio_base_url or get_settings().lmstudio_base_url
        _kwargs = extra_model_kwargs or {"chat_template_kwargs": {"enable_thinking": False}}
        chat = ChatOpenAI(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            base_url=_base_url,
            api_key="lm-studio",
            model_kwargs={"extra_body": _kwargs},
        )
        return InstrumentedLLM(chat, name=role, max_retries=get_settings().max_llm_retries)


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


@lru_cache(maxsize=1)
def get_reasoning_llm() -> LLMProtocol:
    """Reasoning LLM — OpenRouter, T=0.0.

    Used for: schema mapping, Actor-Critic, LLM judge, hallucination grader,
    schema enrichment, Cypher generation/healing.

    Note: ``openai/gpt-oss-120b:free`` has mandatory thinking on OpenRouter.
    Thinking tokens are isolated in the ``reasoning`` field by OpenRouter;
    the ``content`` field always contains the clean response (no leakage).
    ``max_tokens`` caps combined thinking+output to avoid empty content on
    very long thinking runs.
    """
    return make_llm(
        model=get_settings().llm_model_reasoning,
        temperature=get_settings().llm_temperature_reasoning,
        max_tokens=get_settings().llm_max_tokens_reasoning,
        role="reasoning",
    )


@lru_cache(maxsize=1)
def get_extraction_llm() -> LLMProtocol:
    """Extraction SLM — provider auto-detected from model name, T=0.0.

    Used for: triplet extraction from PDF chunks.

    - LM Studio local models (e.g. ``local-model``, ``qwen3-8b``): JSON mode,
      ``enable_thinking: false`` to disable Qwen3 chain-of-thought.
    - OpenRouter models (e.g. ``openai/gpt-oss-20b:free``): routed to OpenRouter.
    - OpenAI direct (e.g. ``gpt-4o-mini``): routed to OpenAI.
    """
    s = get_settings()
    provider = detect_provider(s.llm_model_extraction)

    if provider == "lmstudio":
        # Local model: pass LM Studio-specific chat template kwargs
        return InstrumentedLLM(
            ChatOpenAI(
                model=s.llm_model_extraction,
                temperature=s.llm_temperature_extraction,
                max_tokens=s.llm_max_tokens_extraction,
                base_url=s.lmstudio_base_url,
                api_key="lm-studio",
                model_kwargs={"extra_body": {"chat_template_kwargs": {"enable_thinking": False}}},
            ),
            name="extraction",
            max_retries=s.max_llm_retries,
        )

    # Cloud model (OpenRouter, OpenAI, Anthropic): use make_llm for provider routing
    return make_llm(
        model=s.llm_model_extraction,
        temperature=s.llm_temperature_extraction,
        max_tokens=s.llm_max_tokens_extraction,
        role="extraction",
    )


@lru_cache(maxsize=1)
def get_generation_llm() -> LLMProtocol:
    """Generation LLM — OpenRouter, T=0.3.

    Same model as reasoning but higher temperature for answer fluency.
    Thinking is mandatory for this model; OpenRouter keeps it in a separate
    field so the content returned is always clean prose.
    """
    return make_llm(
        model=get_settings().llm_model_reasoning,
        temperature=get_settings().llm_temperature_generation,
        max_tokens=get_settings().llm_max_tokens_reasoning,
        role="generation",
    )
