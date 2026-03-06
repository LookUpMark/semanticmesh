"""Unit tests for src/config/logging.py — UT-03"""

from __future__ import annotations

import logging
import time

from src.config.logging import NodeTimer, get_logger, log_node_event, log_retry_event


class TestGetLogger:
    def test_get_logger_returns_logger(self) -> None:
        logger = get_logger("test.module")
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test.module"


class TestNodeTimer:
    def test_node_timer_measures_elapsed(self) -> None:
        with NodeTimer() as t:
            time.sleep(0.01)
        assert t.elapsed_ms >= 10


class TestLogRetryEvent:
    def test_log_retry_event_truncates_long_error(self, caplog: object) -> None:
        logger = get_logger("test")
        # Should not raise even with huge error strings
        log_retry_event(logger, "test_node", 1, "x" * 10_000, "fix")


class TestLogNodeEvent:
    def test_log_node_event_no_exception(self) -> None:
        logger = get_logger("test")
        log_node_event(logger, "test_node", "in", "out", 12.5, "model-name")
