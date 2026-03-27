"""Builder functions for constructing LLM client instances.

This module provides low-level builder functions for creating ChatOpenAI,
ChatAnthropic, and other LLM client instances for different providers.

All builders are private (prefixed with ``_``) and should only be called
through :func:`src.config.llm_factory.make_llm`.

Provider coverage
-----------------
OpenAI-compatible (no extra packages):
  _build_openrouter_chat   — OpenRouter (cloud proxy)
  _build_openai_chat       — OpenAI direct
  _build_lmstudio_chat     — LM Studio local endpoint
  _build_openai_compatible_chat — Generic wrapper for any OpenAI-API-compatible
                               endpoint (Groq, Together, Nvidia, DeepSeek, xAI,
                               Cohere, Ollama in compat mode)

Provider-specific (lazy imports — require optional packages):
  _build_anthropic_chat    — Anthropic (langchain-anthropic)
  _build_ollama_chat       — Ollama (langchain-ollama)
  _build_google_chat       — Google Gemini / Vertex AI (langchain-google-genai)
  _build_bedrock_chat      — AWS Bedrock (langchain-aws)
  _build_azure_chat        — Azure OpenAI (langchain-openai, already installed)
  _build_mistral_chat      — Mistral AI (langchain-mistralai)
  _build_huggingface_chat  — HuggingFace Hub (langchain-huggingface)
  _build_cohere_chat       — Cohere (langchain-cohere)

Functions
---------
_optional_model_kwargs(extra_model_kwargs: dict | None) -> dict:
    Wrap extra_model_kwargs in the format expected by ChatOpenAI
"""

from __future__ import annotations

__all__ = [
    "_optional_model_kwargs",
    "_build_openrouter_chat",
    "_build_openai_chat",
    "_build_anthropic_chat",
    "_build_lmstudio_chat",
    "_build_openai_compatible_chat",
    "_build_ollama_chat",
    "_build_google_chat",
    "_build_bedrock_chat",
    "_build_azure_chat",
    "_build_mistral_chat",
    "_build_huggingface_chat",
    "_build_cohere_chat",
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
        from langchain_anthropic import ChatAnthropic  # type: ignore[import-not-found]
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


# ── OpenAI-compatible generic builder ────────────────────────────────────────


def _build_openai_compatible_chat(
    model: str,
    *,
    provider: str,
    temperature: float,
    max_tokens: int | None,
    base_url_override: str | None = None,
    extra_model_kwargs: dict | None = None,
) -> ChatOpenAI:
    """Build a ChatOpenAI instance for any OpenAI-API-compatible third-party endpoint.

    Used for providers that implement the OpenAI REST API without requiring a
    dedicated LangChain integration package: Groq, Together AI, Nvidia NIM,
    DeepSeek, xAI Grok, Cohere Compatibility API, and Ollama (compat mode).

    The *model* string is forwarded as-is after stripping the ``<provider>/``
    prefix so the underlying HTTP call uses the provider's native model id.
    E.g. ``"groq/llama3-70b-8192"`` → model id sent to Groq: ``"llama3-70b-8192"``.

    Args:
        model: Full model string including provider prefix (e.g. ``"groq/llama3-70b-8192"``).
        provider: Provider string as returned by ``detect_provider()``.
        temperature: Sampling temperature.
        max_tokens: Maximum output tokens.
        base_url_override: If given, overrides the default base URL for this provider.
        extra_model_kwargs: Extra keyword arguments forwarded to ChatOpenAI.
    """
    import os

    from src.config.provider_detection import _PROVIDER_BASE_URLS, _PROVIDER_ENV_KEY_MAP

    # Strip the "<provider>/" prefix so we send the native model id
    prefix = f"{provider}/"
    native_model = model[len(prefix):] if model.lower().startswith(prefix) else model

    base_url = (
        base_url_override
        or os.environ.get("PROVIDER_BASE_URL")
        or _PROVIDER_BASE_URLS.get(provider, "")
    )
    env_key = _PROVIDER_ENV_KEY_MAP.get(provider, "")
    api_key = os.environ.get(env_key, "no-key") if env_key else "no-key"

    return ChatOpenAI(
        model=native_model,
        temperature=temperature,
        max_tokens=max_tokens,
        base_url=base_url,
        api_key=api_key,
        **_optional_model_kwargs(extra_model_kwargs),
    )


# ── Provider-specific builders (lazy imports) ────────────────────────────────
# Each builder imports its LangChain integration package lazily — only when
# actually called. If the package is not installed, a clear ImportError is raised
# with a ``pip install`` hint. This ensures missing optional dependencies do not
# crash the application at import time.


def _build_ollama_chat(
    model: str,
    *,
    temperature: float,
    max_tokens: int | None,
    base_url: str | None = None,
) -> LLMProtocol:
    """Build a ChatOllama instance for a locally-running Ollama server.

    Requires: ``pip install langchain-ollama``

    If *langchain-ollama* is not installed, falls back to ``_build_openai_compatible_chat``
    using Ollama's OpenAI-compatible endpoint (``/v1``) automatically.

    The ``ollama/`` prefix is stripped from *model* before passing to ChatOllama.
    """
    import os

    from src.config.provider_detection import _PROVIDER_BASE_URLS

    # Strip provider prefix
    native_model = model[len("ollama/"):] if model.lower().startswith("ollama/") else model
    ollama_base = base_url or os.environ.get("OLLAMA_BASE_URL") or _PROVIDER_BASE_URLS["ollama"]

    try:
        from langchain_ollama import ChatOllama  # type: ignore[import-not-found]
    except ImportError:
        # Graceful degradation: Ollama also supports the OpenAI API at /v1
        return _build_openai_compatible_chat(
            model,
            provider="ollama",
            temperature=temperature,
            max_tokens=max_tokens,
            base_url_override=ollama_base,
        )

    # Strip the trailing /v1 if present (ChatOllama does not use the /v1 suffix)
    host = ollama_base.rstrip("/")
    if host.endswith("/v1"):
        host = host[: -len("/v1")]

    return ChatOllama(  # type: ignore[no-any-return]
        model=native_model,
        temperature=temperature,
        num_predict=max_tokens,
        base_url=host,
    )


def _build_google_chat(
    model: str,
    *,
    temperature: float,
    max_tokens: int | None,
) -> LLMProtocol:
    """Build a ChatGoogleGenerativeAI instance for Google Gemini / Vertex AI.

    Requires: ``pip install langchain-google-genai``

    The ``google/`` prefix is stripped from *model* before passing to the client.
    """
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI  # type: ignore[import-not-found]
    except ImportError as exc:
        raise ImportError(
            "Install langchain-google-genai to use Google models: "
            "pip install langchain-google-genai"
        ) from exc

    # Strip provider prefix(es)
    for prefix in ("google/", "vertex_ai/"):
        if model.lower().startswith(prefix):
            model = model[len(prefix):]
            break

    return ChatGoogleGenerativeAI(  # type: ignore[no-any-return]
        model=model, temperature=temperature, max_output_tokens=max_tokens
    )


def _build_bedrock_chat(
    model: str,
    *,
    temperature: float,
    max_tokens: int | None,
) -> LLMProtocol:
    """Build a ChatBedrock instance for AWS Bedrock.

    Requires: ``pip install langchain-aws``

    Authentication uses the standard AWS credential chain (env vars, ~/.aws/credentials,
    IAM role). The ``bedrock/`` prefix is stripped from *model*.
    """
    try:
        from langchain_aws import ChatBedrock  # type: ignore[import-not-found]
    except ImportError as exc:
        raise ImportError(
            "Install langchain-aws to use AWS Bedrock models: pip install langchain-aws"
        ) from exc

    native_model = model[len("bedrock/"):] if model.lower().startswith("bedrock/") else model
    return ChatBedrock(  # type: ignore[no-any-return]
        model_id=native_model,
        model_kwargs={"temperature": temperature, "max_tokens": max_tokens},
    )


def _build_azure_chat(
    model: str,
    *,
    temperature: float,
    max_tokens: int | None,
) -> LLMProtocol:
    """Build an AzureChatOpenAI instance for Azure OpenAI Service.

    Requires: ``langchain-openai`` (already installed).

    Environment variables expected:
      AZURE_OPENAI_API_KEY      — Azure subscription key
      AZURE_OPENAI_ENDPOINT     — e.g. https://my-resource.openai.azure.com/
      AZURE_OPENAI_API_VERSION  — e.g. 2024-02-01 (default used if not set)

    The ``azure/`` or ``azure_openai/`` prefix is stripped from *model* to get
    the deployment name.
    """
    import os

    from langchain_openai import AzureChatOpenAI

    for prefix in ("azure_openai/", "azure/"):
        if model.lower().startswith(prefix):
            model = model[len(prefix):]
            break

    return AzureChatOpenAI(
        azure_deployment=model,
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT", ""),
        api_key=os.environ.get("AZURE_OPENAI_API_KEY", ""),  # type: ignore[arg-type]
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-11-01-preview"),
        temperature=temperature,
        max_tokens=max_tokens,
    )


def _build_mistral_chat(
    model: str,
    *,
    temperature: float,
    max_tokens: int | None,
) -> LLMProtocol:
    """Build a ChatMistralAI instance for Mistral AI.

    Requires: ``pip install langchain-mistralai``

    The ``mistral/`` prefix is stripped from *model*.
    """
    try:
        from langchain_mistralai import ChatMistralAI  # type: ignore[import-not-found]
    except ImportError as exc:
        raise ImportError(
            "Install langchain-mistralai to use Mistral models: "
            "pip install langchain-mistralai"
        ) from exc

    for prefix in ("mistral/",):
        if model.lower().startswith(prefix):
            model = model[len(prefix):]
            break

    return ChatMistralAI(model=model, temperature=temperature, max_tokens=max_tokens)  # type: ignore[no-any-return]


def _build_huggingface_chat(
    model: str,
    *,
    temperature: float,
    max_tokens: int | None,
) -> LLMProtocol:
    """Build a ChatHuggingFace instance for the HuggingFace Hub inference API.

    Requires: ``pip install langchain-huggingface``

    The ``hf/`` or ``huggingface/`` prefix is stripped from *model*.
    """
    try:
        from langchain_huggingface import (  # type: ignore[import-not-found]
            ChatHuggingFace,
            HuggingFaceEndpoint,
        )
    except ImportError as exc:
        raise ImportError(
            "Install langchain-huggingface to use HuggingFace models: "
            "pip install langchain-huggingface"
        ) from exc

    for prefix in ("huggingface/", "hf/"):
        if model.lower().startswith(prefix):
            model = model[len(prefix):]
            break

    endpoint = HuggingFaceEndpoint(
        repo_id=model, temperature=temperature, max_new_tokens=max_tokens
    )
    return ChatHuggingFace(llm=endpoint)  # type: ignore[no-any-return]


def _build_cohere_chat(
    model: str,
    *,
    temperature: float,
    max_tokens: int | None,
) -> LLMProtocol:
    """Build a ChatCohere instance for Cohere's native API.

    Requires: ``pip install langchain-cohere``

    The ``cohere/`` prefix is stripped from *model*.
    Note: if *langchain-cohere* is not installed, falls back to
    ``_build_openai_compatible_chat`` using Cohere's OpenAI-compatible endpoint.
    """
    for prefix in ("cohere/",):
        if model.lower().startswith(prefix):
            model = model[len(prefix):]
            break

    try:
        from langchain_cohere import ChatCohere  # type: ignore[import-not-found]
    except ImportError:
        # Graceful degradation: Cohere exposes an OpenAI-compatible endpoint
        return _build_openai_compatible_chat(
            f"cohere/{model}",
            provider="cohere",
            temperature=temperature,
            max_tokens=max_tokens,
        )

    return ChatCohere(model=model, temperature=temperature, max_tokens=max_tokens)  # type: ignore[no-any-return]
