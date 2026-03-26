"""Builder functions for constructing LLM client instances.

This module provides low-level builder functions for creating ChatOpenAI,
ChatAnthropic, and other LLM client instances for different providers.

All builders are private (prefixed with ``_``) and should only be called
through :func:`src.config.llm_factory.make_llm`.

Functions
---------
_optional_model_kwargs(extra_model_kwargs: dict | None) -> dict:
    Wrap extra_model_kwargs in the format expected by ChatOpenAI
_build_openrouter_chat(...): Build a ChatOpenAI instance for OpenRouter
_build_openai_chat(...): Build a ChatOpenAI instance for OpenAI direct API
_build_anthropic_chat(...): Build a ChatAnthropic instance for Anthropic direct API
_build_lmstudio_chat(...): Build a ChatOpenAI instance for LM Studio local endpoint
"""

from __future__ import annotations

__all__ = [
    "_optional_model_kwargs",
    "_build_openrouter_chat",
    "_build_openai_chat",
    "_build_anthropic_chat",
    "_build_lmstudio_chat",
]

from typing import TYPE_CHECKING

from langchain_openai import ChatOpenAI

from src.config.settings import get_settings

if TYPE_CHECKING:
    from src.config.llm_client import LLMProtocol


# ── Helper functions ─────────────────────────────────────────────────────────


def _optional_model_kwargs(extra_model_kwargs: dict | None) -> dict:
    """Wrap extra_model_kwargs in the format expected by ChatOpenAI."""
    return {"model_kwargs": extra_model_kwargs} if extra_model_kwargs else {}


# ── Provider-specific builders ───────────────────────────────────────────────


def _build_openrouter_chat(
    model_name: str,
    *,
    temperature: float,
    max_tokens: int | None,
    openrouter_api_key: str | None,
    openrouter_base_url: str | None,
    extra_model_kwargs: dict | None,
) -> ChatOpenAI:
    """Build a ChatOpenAI instance configured for OpenRouter."""
    api_key = openrouter_api_key or get_settings().openrouter_api_key.get_secret_value()
    base_url = openrouter_base_url or get_settings().openrouter_base_url
    return ChatOpenAI(
        model=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        base_url=base_url,
        api_key=api_key,
        **_optional_model_kwargs(extra_model_kwargs),
    )


def _build_openai_chat(
    model: str,
    *,
    temperature: float,
    max_tokens: int | None,
    openai_api_key: str | None,
    extra_model_kwargs: dict | None,
) -> ChatOpenAI:
    """Build a ChatOpenAI instance for OpenAI direct API.

    ``reasoning_effort`` is extracted from *extra_model_kwargs* and passed as a
    top-level ChatOpenAI parameter (not via ``model_kwargs``) to avoid the
    LangChain UserWarning about explicit parameters.
    """
    import os

    api_key = (
        openai_api_key
        or os.environ.get("OPENAI_API_KEY")
        or get_settings().openai_api_key.get_secret_value()
    )
    mkwargs: dict = dict(extra_model_kwargs) if extra_model_kwargs else {}
    reasoning_effort: str | None = mkwargs.pop("reasoning_effort", None)
    chat_kwargs: dict = {
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "api_key": api_key,
    }
    if mkwargs:
        chat_kwargs["model_kwargs"] = mkwargs
    if reasoning_effort is not None:
        chat_kwargs["reasoning_effort"] = reasoning_effort
    return ChatOpenAI(**chat_kwargs)


def _build_anthropic_chat(
    model: str,
    *,
    temperature: float,
    max_tokens: int | None,
) -> LLMProtocol:
    """Build a ChatAnthropic instance for Anthropic direct API.

    Raises:
        ImportError: If langchain-anthropic is not installed.
    """
    try:
        from langchain_anthropic import ChatAnthropic  # type: ignore[import]
    except ImportError as exc:  # pragma: no cover
        raise ImportError(
            "Install langchain-anthropic to use Anthropic models directly: "
            "pip install langchain-anthropic"
        ) from exc

    import os

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    return ChatAnthropic(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens or 4096,
        api_key=api_key,
    )


def _build_lmstudio_chat(
    model: str,
    *,
    temperature: float,
    max_tokens: int | None,
    lmstudio_base_url: str | None,
    extra_model_kwargs: dict | None,
) -> ChatOpenAI:
    """Build a ChatOpenAI instance for LM Studio local endpoint."""
    base_url = lmstudio_base_url or get_settings().lmstudio_base_url
    kwargs = extra_model_kwargs or {"chat_template_kwargs": {"enable_thinking": False}}
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        base_url=base_url,
        api_key="lm-studio",
        model_kwargs={"extra_body": kwargs},
    )
