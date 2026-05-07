"""Observability integration: LangSmith + Langfuse.

Provides a unified callback handler list that pipeline nodes inject into LLM calls.
Both platforms are opt-in via environment variables.

LangSmith (automatic with LangChain)
-------------------------------------
Set these env vars and LangChain/LangGraph traces automatically:
  LANGCHAIN_TRACING_V2=true
  LANGCHAIN_API_KEY=ls-...
  LANGCHAIN_PROJECT=semanticmesh  (optional, defaults to "default")

Langfuse
--------
Set these env vars to enable:
  LANGFUSE_PUBLIC_KEY=pk-lf-...
  LANGFUSE_SECRET_KEY=sk-lf-...
  LANGFUSE_HOST=https://cloud.langfuse.com  (or self-hosted URL)

Usage::

    from src.config.observability import get_observability_callbacks

    callbacks = get_observability_callbacks()
    # Pass to LLM invocations:
    response = llm.invoke(messages, config={"callbacks": callbacks})
"""

from __future__ import annotations

import logging
import os
from functools import lru_cache
from typing import Any

_logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def _get_langfuse_handler() -> Any | None:
    """Create and cache the Langfuse callback handler (or None if not configured)."""
    public_key = os.environ.get("LANGFUSE_PUBLIC_KEY", "").strip()
    secret_key = os.environ.get("LANGFUSE_SECRET_KEY", "").strip()

    if not public_key or not secret_key:
        return None

    try:
        from langfuse.langchain import CallbackHandler

        handler = CallbackHandler()
        _logger.info(
            "Langfuse observability enabled (host=%s)",
            os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com"),
        )
        return handler
    except ImportError:
        _logger.warning(
            "LANGFUSE_PUBLIC_KEY is set but 'langfuse' package is not installed. "
            "Install with: pip install langfuse"
        )
        return None
    except Exception as exc:  # noqa: BLE001
        _logger.warning("Failed to initialize Langfuse: %s", exc)
        return None


def is_langsmith_enabled() -> bool:
    """Check if LangSmith tracing is enabled via env vars."""
    return os.environ.get("LANGCHAIN_TRACING_V2", "").lower() == "true" and bool(
        os.environ.get("LANGCHAIN_API_KEY", "").strip()
    )


def is_langfuse_enabled() -> bool:
    """Check if Langfuse is configured via env vars."""
    return bool(
        os.environ.get("LANGFUSE_PUBLIC_KEY", "").strip()
        and os.environ.get("LANGFUSE_SECRET_KEY", "").strip()
    )


def get_observability_callbacks() -> list[Any]:
    """Return the list of active observability callback handlers.

    LangSmith callbacks are NOT included here — LangChain injects them
    automatically when LANGCHAIN_TRACING_V2=true. This function only
    returns callbacks that must be explicitly passed (e.g., Langfuse).
    """
    callbacks: list[Any] = []

    langfuse_handler = _get_langfuse_handler()
    if langfuse_handler is not None:
        callbacks.append(langfuse_handler)

    return callbacks


def flush_observability() -> None:
    """Flush pending observability data (call on shutdown)."""
    handler = _get_langfuse_handler()
    if handler is not None:
        try:
            handler.flush()
        except Exception:  # noqa: BLE001
            pass


def reset_observability() -> None:
    """Clear cached handlers (call after env var changes)."""
    _get_langfuse_handler.cache_clear()
