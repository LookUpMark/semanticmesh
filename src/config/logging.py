"""EP-01: Structured JSON logging.

Every LangGraph node should call `get_logger(__name__)` and log using
the helpers below so that all operational data is consistently structured.
"""

from __future__ import annotations

import logging
import os
import time
from typing import Any

from pythonjsonlogger import jsonlogger


def _configure_root_logger() -> None:
    """Configure the root logger with a JSON formatter exactly once."""
    root = logging.getLogger()
    if root.handlers:
        return  # already configured — avoids duplicate handlers in tests

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

    # Suppress Neo4j driver schema notifications (verbose GqlStatusObject spam).
    # These are INFO-level "constraint already exists" messages with no actionable info.
    logging.getLogger("neo4j.notifications").setLevel(logging.WARNING)


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

    Call at the START of each retry iteration before sending the Reflection Prompt.
    """
    logger.warning(
        "retry_event",
        extra={
            "node_name": node_name,
            "attempt_number": attempt_number,
            "error_injected": error_injected[:500],   # cap to avoid log bloat
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
        pass  # elapsed_ms is computed on access, not on exit

    @property
    def elapsed_ms(self) -> float:
        """Elapsed time in milliseconds since __enter__."""
        return (time.perf_counter() - self._start) * 1000
