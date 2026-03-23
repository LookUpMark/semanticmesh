"""Provider auto-detection from model names.

This module provides utilities to infer the LLM provider from a model name string,
following these rules (in order):
  - ``provider/model`` (contains ``/``) → **OpenRouter**
  - Starts with ``gpt-``, ``o1-``, ``o3-``, ``o4-`` (no slash) → **OpenAI** (direct)
  - Starts with ``claude-`` (no slash) → **Anthropic** (direct)
  - Anything else → **LM Studio** (local)

Constants
---------
_OPENROUTER_BASE_URL: Default OpenRouter API endpoint
_LMSTUDIO_DEFAULT_URL: Default LM Studio endpoint
_OPENAI_PREFIXES: Tuple of OpenAI model name prefixes
_ANTHROPIC_PREFIXES: Tuple of Anthropic model name prefixes

Functions
---------
detect_provider(model: str) -> str: Infer provider from model name
_strip_free_suffix(model: str) -> str: Remove :free suffix from model name
_is_free_model(model: str) -> bool: Check if model name has :free suffix
"""

from __future__ import annotations

__all__ = [
    "detect_provider",
    "_strip_free_suffix",
    "_is_free_model",
    "_OPENROUTER_BASE_URL",
    "_LMSTUDIO_DEFAULT_URL",
    "_OPENAI_PREFIXES",
    "_ANTHROPIC_PREFIXES",
]

# ── Constants ─────────────────────────────────────────────────────────────────

_OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
_LMSTUDIO_DEFAULT_URL = "http://localhost:1234/v1"

# Model name prefixes that map to direct provider APIs (no slash in the name)
_OPENAI_PREFIXES = ("gpt-", "o1-", "o2-", "o3-", "o4-", "text-")
_ANTHROPIC_PREFIXES = ("claude-",)


# ── Provider detection ───────────────────────────────────────────────────────


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
