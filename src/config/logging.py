"""Structured JSON logging for LangGraph pipeline observability."""

from __future__ import annotations

import logging
import os
import time
import warnings
from typing import Any

from pythonjsonlogger import jsonlogger

# Suppress third-party warnings at import time
warnings.filterwarnings("ignore", message="IProgress not found", category=UserWarning)
warnings.filterwarnings("ignore", message="directory.*does not exist", category=UserWarning)


# ── Notebook formatter ─────────────────────────────────────────────────────────


class _NotebookFormatter(logging.Formatter):
    """Compact human-readable formatter for Jupyter notebook output.

    Output format:
        HH:MM:SS  logger.name                     message
        HH:MM:SS  [WARN] logger.name              warning message
    """

    def format(self, record: logging.LogRecord) -> str:  # noqa: A003
        ts = self.formatTime(record, "%H:%M:%S")
        parts = record.name.split(".")
        short = ".".join(parts[-2:]) if len(parts) > 1 else record.name
        msg = record.getMessage()
        if record.levelno >= logging.WARNING:
            tag = f"[{record.levelname[:4]}]"
            return f"{ts}  {tag:<7}  {short:<32}  {msg}"
        return f"{ts}  {short:<32}  {msg}"


def setup_notebook_logging() -> None:
    """Replace JSON formatter with human-readable output for Jupyter notebooks.

    Suppresses noisy third-party loggers and keeps src.* at INFO level.
    Call once after reconfigure_from_env().
    """
    root = logging.getLogger()

    for h in root.handlers[:]:
        root.removeHandler(h)

    handler = logging.StreamHandler()
    handler.setFormatter(_NotebookFormatter())
    root.addHandler(handler)
    root.setLevel(logging.INFO)
    _SILENT = (
        "httpx",
        "httpcore",
        "urllib3",
        "requests",
        "pydantic_settings",
        "pydantic",
        "LiteLLM",
        "openai",
        "anthropic",
    )
    for name in _SILENT:
        logging.getLogger(name).setLevel(logging.WARNING)

    logging.getLogger("src.graph.neo4j_client").setLevel(logging.WARNING)
    logging.getLogger("neo4j.notifications").setLevel(logging.WARNING)
    logging.getLogger("langgraph.checkpoint.serde.jsonplus").setLevel(logging.ERROR)
    try:
        import transformers  # type: ignore[import]

        transformers.logging.set_verbosity_error()
    except ImportError:
        pass


def _configure_root_logger() -> None:
    """Configure the root logger with a JSON formatter exactly once."""
    root = logging.getLogger()
    if root.handlers:
        return

    level_name = os.environ.get("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    root.setLevel(level)

    handler = logging.StreamHandler()
    handler.setLevel(level)

    formatter = jsonlogger.JsonFormatter(  # type: ignore[attr-defined]
        fmt="%(asctime)s %(name)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
        rename_fields={"asctime": "ts", "name": "logger", "levelname": "level"},
    )
    handler.setFormatter(formatter)
    root.addHandler(handler)

    logging.getLogger("neo4j.notifications").setLevel(logging.WARNING)
    logging.getLogger("langgraph.checkpoint.serde.jsonplus").setLevel(logging.ERROR)


# Configure root logger at module import time
_configure_root_logger()


def get_logger(name: str) -> logging.Logger:
    """Return a named logger inheriting the root JSON configuration."""
    return logging.getLogger(name)


def log_node_event(
    logger: logging.Logger,
    node_name: str,
    input_summary: str,
    output_summary: str,
    duration_ms: float,
    model_used: str = "",
    **extra: Any,
) -> None:
    """Log a standardised node-boundary event.

    Call this at the END of every LangGraph node function.
    """
    logger.info(
        "node_event",
        extra={
            "node_name": node_name,
            "input_summary": input_summary,
            "output_summary": output_summary,
            "duration_ms": round(duration_ms, 2),
            "model_used": model_used,
            **extra,
        },
    )


def log_retry_event(
    logger: logging.Logger,
    node_name: str,
    attempt_number: int,
    error_injected: str,
    correction_applied: str = "",
) -> None:
    """Log a reflection/retry event (Actor-Critic or Cypher Healing).

    Call at the START of each retry iteration.
    """
    logger.warning(
        "retry_event",
        extra={
            "node_name": node_name,
            "attempt_number": attempt_number,
            "error_injected": error_injected[:500],  # cap to avoid log bloat
            "correction_applied": correction_applied[:200],
        },
    )


class NodeTimer:
    """Context manager to measure node execution time in milliseconds."""

    def __init__(self) -> None:
        self._start: float = 0.0

    def __enter__(self) -> NodeTimer:
        self._start = time.perf_counter()
        return self

    def __exit__(self, *_: object) -> None:
        pass

    @property
    def elapsed_ms(self) -> float:
        """Elapsed time in milliseconds since __enter__."""
        return (time.perf_counter() - self._start) * 1000
