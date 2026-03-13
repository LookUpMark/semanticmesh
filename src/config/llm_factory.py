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

from src.config.llm_client import InstrumentedLLM, LLMProtocol
from src.config.settings import settings

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
) -> LLMProtocol:
    """Create an instrumented LLM, auto-detecting the provider from *model*.

    Provider detection
    ------------------
    - ``provider/model`` (contains ``/``) → OpenRouter
    - ``gpt-*``, ``o1-*``, ``o3-*`` (no slash) → OpenAI direct
    - ``claude-*`` (no slash) → Anthropic direct (requires ``langchain-anthropic``)
    - anything else → LM Studio local endpoint

    Examples
    --------
    >>> make_llm("openai/gpt-oss-120b:free")          # → OpenRouter
    >>> make_llm("gpt-4o")                            # → OpenAI
    >>> make_llm("claude-3-5-sonnet-20241022")        # → Anthropic
    >>> make_llm("local-model")                       # → LM Studio
    >>> make_llm("qwen3-8b-instruct")                 # → LM Studio
    """
    provider = detect_provider(model)

    if provider == "openrouter":
        _api_key = openrouter_api_key or settings.openrouter_api_key.get_secret_value()
        _base_url = openrouter_base_url or settings.openrouter_base_url
        chat = ChatOpenAI(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            base_url=_base_url,
            api_key=_api_key,
            **({"model_kwargs": extra_model_kwargs} if extra_model_kwargs else {}),
        )

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
            max_retries=settings.max_llm_retries,
        )

    else:  # lmstudio
        _base_url = lmstudio_base_url or settings.lmstudio_base_url
        _kwargs = extra_model_kwargs or {"chat_template_kwargs": {"enable_thinking": False}}
        chat = ChatOpenAI(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            base_url=_base_url,
            api_key="lm-studio",
            model_kwargs={"extra_body": _kwargs},
        )

    return InstrumentedLLM(chat, name=role, max_retries=settings.max_llm_retries)


# ── Cached pipeline factories ─────────────────────────────────────────────────

def reconfigure_from_env() -> None:
    """Clear all cached LLM instances so they re-read from ``settings`` on next call.

    Call this from the notebook after changing ``os.environ`` to pick up new
    model names or API keys without restarting the kernel.
    """
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
        model=settings.llm_model_reasoning,
        temperature=settings.llm_temperature_reasoning,
        max_tokens=settings.llm_max_tokens_reasoning,
        role="reasoning",
    )


@lru_cache(maxsize=1)
def get_extraction_llm() -> LLMProtocol:
    """Extraction SLM — LM Studio local model, T=0.0, JSON mode.

    Used for: triplet extraction from PDF chunks.

    Note: ``max_tokens=16384`` prevents truncated JSON.
    ``enable_thinking: false`` disables Qwen3 chain-of-thought; silently
    ignored by non-thinking models.
    """
    return InstrumentedLLM(
        ChatOpenAI(
            model=settings.llm_model_extraction,
            temperature=settings.llm_temperature_extraction,
            max_tokens=settings.llm_max_tokens_extraction,
            base_url=settings.lmstudio_base_url,
            api_key="lm-studio",  # LM Studio ignores auth
            model_kwargs={"extra_body": {"chat_template_kwargs": {"enable_thinking": False}}},
        ),
        name="extraction",
        max_retries=settings.max_llm_retries,
    )


@lru_cache(maxsize=1)
def get_generation_llm() -> LLMProtocol:
    """Generation LLM — OpenRouter, T=0.3.

    Same model as reasoning but higher temperature for answer fluency.
    Thinking is mandatory for this model; OpenRouter keeps it in a separate
    field so the content returned is always clean prose.
    """
    return make_llm(
        model=settings.llm_model_reasoning,
        temperature=settings.llm_temperature_generation,
        max_tokens=settings.llm_max_tokens_reasoning,
        role="generation",
    )
