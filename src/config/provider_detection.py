"""Provider auto-detection from model names.

This module provides utilities to infer the LLM provider from a model name string.

Detection rules (applied in order, first match wins):
  1. Named-provider prefix (``groq/``, ``mistral/``, ``ollama/``, etc.) → specific provider
  2. ``provider/model`` (any remaining ``/``) → **OpenRouter**
  3. Starts with ``gpt-``, ``o1-``, ``o4-`` etc. (no slash) → **OpenAI** direct
  4. Starts with ``claude-`` (no slash) → **Anthropic** direct
  5. Starts with ``gemini-`` or ``deepseek-`` etc. (prefix without ``/``) → named provider
  6. Anything else → **LM Studio** (local)

This means any LangChain-supported provider can be used by prefixing the model name with
``<provider>/``, e.g. ``ollama/llama3.1``, ``groq/llama3-70b-8192``,
``bedrock/anthropic.claude-3-sonnet``, ``google/gemini-2.0-flash``.

Constants
---------
_OPENROUTER_BASE_URL: Default OpenRouter API endpoint
_LMSTUDIO_DEFAULT_URL: Default LM Studio endpoint
_OPENAI_PREFIXES: Tuple of OpenAI model name prefixes (no slash needed)
_ANTHROPIC_PREFIXES: Tuple of Anthropic model name prefixes (no slash needed)
_PROVIDER_BASE_URLS: Default base URLs for OpenAI-compatible providers
_PROVIDER_ENV_KEY_MAP: Environment variable name for each provider's API key

Functions
---------
detect_provider(model: str) -> str: Infer provider from model name
_strip_free_suffix(model: str) -> str: Remove :free suffix from model name
_is_free_model(model: str) -> bool: Check if model name has :free suffix
"""

from __future__ import annotations

__all__ = [
    "detect_provider",
    "is_openai_reasoning_model",
    "_strip_free_suffix",
    "_is_free_model",
    "_OPENROUTER_BASE_URL",
    "_LMSTUDIO_DEFAULT_URL",
    "_OPENAI_PREFIXES",
    "_ANTHROPIC_PREFIXES",
    "_OPENAI_REASONING_PREFIXES",
    "_PROVIDER_BASE_URLS",
    "_PROVIDER_ENV_KEY_MAP",
]

# ── Constants ─────────────────────────────────────────────────────────────────

_OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
_LMSTUDIO_DEFAULT_URL = "http://localhost:1234/v1"

# Model name prefixes that map to direct provider APIs (no slash in the name)
_OPENAI_PREFIXES = ("gpt-", "o1-", "o2-", "o3-", "o4-", "text-")
_ANTHROPIC_PREFIXES = ("claude-",)

# OpenAI reasoning models: accept reasoning_effort=minimal/low/medium/high but NOT "none".
# Includes o-series and gpt-5* (which are all chain-of-thought reasoning models).
_OPENAI_REASONING_PREFIXES = ("o1-", "o2-", "o3-", "o4-", "gpt-5")

# Default base URLs for OpenAI-API-compatible third-party providers.
# These are used by _build_openai_compatible_chat() in model_builders.py as defaults
# when no PROVIDER_BASE_URL env var / provider_base_url kwarg is supplied.
_PROVIDER_BASE_URLS: dict[str, str] = {
    "groq": "https://api.groq.com/openai/v1",
    "together": "https://api.together.xyz/v1",
    "nvidia": "https://integrate.api.nvidia.com/v1",
    "deepseek": "https://api.deepseek.com/v1",
    "xai": "https://api.x.ai/v1",
    "cohere": "https://api.cohere.ai/compatibility/v1",
    # ollama exposes an OpenAI-compatible endpoint as well (fallback mode)
    "ollama": "http://localhost:11434/v1",
}

# Environment variable that holds the API key for each provider.
_PROVIDER_ENV_KEY_MAP: dict[str, str] = {
    "groq": "GROQ_API_KEY",
    "together": "TOGETHER_API_KEY",
    "nvidia": "NVIDIA_API_KEY",
    "deepseek": "DEEPSEEK_API_KEY",
    "xai": "XAI_API_KEY",
    "cohere": "COHERE_API_KEY",
    "google": "GOOGLE_API_KEY",
    "bedrock": "AWS_ACCESS_KEY_ID",
    "mistral": "MISTRAL_API_KEY",
    "huggingface": "HUGGINGFACEHUB_API_TOKEN",
    "azure": "AZURE_OPENAI_API_KEY",
    "ollama": "",  # no API key required for local Ollama
}

# Named prefixes (with slash) that map to a specific provider rather than OpenRouter.
# Order matters — more specific entries must come before generic ones.
# The value is the provider string returned by detect_provider().
_NAMED_PREFIX_MAP: dict[str, str] = {
    "ollama/": "ollama",
    "google/": "google",
    "vertex_ai/": "google",
    "bedrock/": "bedrock",
    "azure/": "azure",
    "azure_openai/": "azure",
    "groq/": "groq",
    "mistral/": "mistral",
    "together/": "together",
    "hf/": "huggingface",
    "huggingface/": "huggingface",
    "cohere/": "cohere",
    "nvidia/": "nvidia",
    "deepseek/": "deepseek",
    "xai/": "xai",
}

# Bare (no-slash) model name prefixes that identify a provider without a slash prefix.
_BARE_PREFIX_MAP: tuple[tuple[str, str], ...] = (
    ("gemini-", "google"),
    ("mistral-", "mistral"),
    ("command-", "cohere"),
    ("deepseek-", "deepseek"),
    ("grok-", "xai"),
)


# ── Provider detection ───────────────────────────────────────────────────────


def detect_provider(model: str) -> str:
    """Infer the LLM provider from the model name string.

    Rules (applied in order, first match wins):

    1. Named-provider slash prefix (e.g. ``ollama/``, ``groq/``, ``bedrock/``) →
       the named provider (see ``_NAMED_PREFIX_MAP``).
    2. Any remaining ``/`` → **openrouter**
       (e.g. ``openai/gpt-4.1:free``, ``meta-llama/llama-3.3-70b-instruct:free``)
    3. Bare OpenAI prefixes (``gpt-``, ``o1-``, etc.) → **openai** (direct)
    4. Bare Anthropic prefix (``claude-``) → **anthropic** (direct)
    5. Bare provider-specific prefixes (``gemini-``, ``mistral-``, etc.) →
       named provider (see ``_BARE_PREFIX_MAP``).
    6. Anything else → **lmstudio** (local)

    Examples
    --------
    >>> detect_provider("ollama/llama3.1")
    'ollama'
    >>> detect_provider("groq/llama3-70b-8192")
    'groq'
    >>> detect_provider("openai/gpt-4.1:free")
    'openrouter'
    >>> detect_provider("gpt-4.1")
    'openai'
    >>> detect_provider("gemini-2.0-flash")
    'google'
    >>> detect_provider("local-model")
    'lmstudio'
    """
    m = model.lower()

    # Rule 1: named provider slash prefix
    for prefix, provider in _NAMED_PREFIX_MAP.items():
        if m.startswith(prefix):
            return provider

    # Rule 2: any remaining slash → OpenRouter
    if "/" in m:
        return "openrouter"

    # Rule 3: bare OpenAI prefixes
    if m.startswith(_OPENAI_PREFIXES):
        return "openai"

    # Rule 4: bare Anthropic prefix
    if m.startswith(_ANTHROPIC_PREFIXES):
        return "anthropic"

    # Rule 5: bare provider-specific prefixes
    for prefix, provider in _BARE_PREFIX_MAP:
        if m.startswith(prefix):
            return provider

    # Rule 6: fallback → local LM Studio
    return "lmstudio"


def is_openai_reasoning_model(model: str) -> bool:
    """Return True if *model* is an OpenAI reasoning model (o-series or gpt-5*).

    Reasoning models accept ``reasoning_effort`` values ``"minimal"``,
    ``"low"``, ``"medium"``, and ``"high"``, but **not** ``"none"``.
    Standard chat models (e.g. ``gpt-4o``, ``gpt-4o-mini``) do not accept
    the ``reasoning_effort`` parameter at all.

    Examples
    --------
    >>> is_openai_reasoning_model("o3-mini")
    True
    >>> is_openai_reasoning_model("gpt-5-nano-2025-08-07")
    True
    >>> is_openai_reasoning_model("gpt-5.4-mini")
    True
    >>> is_openai_reasoning_model("gpt-4o-mini")
    False
    """
    return model.lower().startswith(_OPENAI_REASONING_PREFIXES)


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
