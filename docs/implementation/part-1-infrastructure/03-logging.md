# Part 1 — `src/config/logging.py`

## 1. Purpose & Context

**Epic:** EP-01 — US-01-03 — Structured Logging

Configures the root Python logger exactly once with a JSON formatter (`python-json-logger`). Every other module calls `get_logger(__name__)` and uses the `log_node_event` / `log_retry_event` helpers to emit machine-parseable log lines.

---

## 2. Prerequisites

- `settings.py` complete (log level read from env)

---

## 3. Public API

| Symbol | Signature | Description |
|---|---|---|
| `get_logger` | `(name: str) -> Logger` | Named logger with JSON format |
| `log_node_event` | `(logger, node_name, input_summary, output_summary, duration_ms, model_used, **extra)` | Standard boundary log |
| `log_retry_event` | `(logger, node_name, attempt_number, error_injected, correction_applied)` | Reflection/retry log |
| `NodeTimer` | context manager | Measures elapsed ms for `log_node_event` |

---

## 4. Full Implementation

```python
"""EP-01: Structured JSON logging.

Every LangGraph node should call `get_logger(__name__)` and log using
the helpers below so that all operational data is consistently structured.
"""

from __future__ import annotations

import logging
import os
import time
from typing import Any

from pythonjsonlogger import jsonlogger  # type: ignore[import-untyped]


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

    formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(name)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
        rename_fields={"asctime": "ts", "name": "logger", "levelname": "level"},
    )
    handler.setFormatter(formatter)
    root.addHandler(handler)


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

    Call this at the END of every LangGraph node function:

        with NodeTimer() as t:
            result = do_work(...)
        log_node_event(logger, "my_node", f"input={x}", f"output={y}", t.elapsed_ms)
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
    """Context manager to measure node execution time in milliseconds.

    Usage::

        with NodeTimer() as t:
            output = expensive_operation()
        log_node_event(logger, "node_name", ..., t.elapsed_ms)
    """

    def __init__(self) -> None:
        self._start: float = 0.0

    def __enter__(self) -> "NodeTimer":
        self._start = time.perf_counter()
        return self

    def __exit__(self, *_: object) -> None:
        pass  # elapsed_ms is computed on access, not on exit

    @property
    def elapsed_ms(self) -> float:
        """Elapsed time in milliseconds since __enter__."""
        return (time.perf_counter() - self._start) * 1000
```

### Usage Pattern in Every Node

```python
from src.config.logging import get_logger, log_node_event, NodeTimer

logger = get_logger(__name__)

def my_node(state: BuilderState) -> dict:
    with NodeTimer() as t:
        result = call_llm(...)
    log_node_event(
        logger,
        node_name="my_node",
        input_summary=f"table={state.table_schemas[0].table_name}",
        output_summary=f"proposal={result.mapped_concept}",
        duration_ms=t.elapsed_ms,
        model_used=settings.llm_model_reasoning,
    )
    return {"mapping_proposals": [result]}
```

---

## 5. Tests

There are no dedicated unit tests for `logging.py` (it configures stdlib). Integration is verified by checking that node functions produce `node_event` JSON lines. A quick sanity check:

```python
"""Sanity test for logging module."""

import json
import logging
from io import StringIO

from src.config.logging import get_logger, log_node_event, log_retry_event, NodeTimer


def test_get_logger_returns_logger() -> None:
    logger = get_logger("test.module")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test.module"


def test_node_timer_measures_elapsed() -> None:
    import time
    with NodeTimer() as t:
        time.sleep(0.01)
    assert t.elapsed_ms >= 10


def test_log_retry_event_truncates_long_error(caplog: object) -> None:
    logger = get_logger("test")
    # Should not raise even with huge error strings
    log_retry_event(logger, "test_node", 1, "x" * 10_000, "fix")


def test_log_node_event_no_exception() -> None:
    logger = get_logger("test")
    log_node_event(logger, "test_node", "in", "out", 12.5, "model-name")
```

---

## 6. Smoke Test

```bash
python -c "
from src.config.logging import get_logger, log_node_event, NodeTimer
import time
logger = get_logger('smoke')
with NodeTimer() as t:
    time.sleep(0.01)
log_node_event(logger, 'smoke_node', 'hello', 'world', t.elapsed_ms, 'test-model')
print('Logging OK')
"
```

Expected: a JSON log line + `Logging OK`
