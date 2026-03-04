# Part 6 — `src/graph/cypher_healer.py`

## 1. Purpose & Context

**Epic:** EP-09 Cypher Generation & Healing  
**US-09-02** — Cypher Execution Test, **US-09-03** — Cypher Healing Loop

`cypher_healer` adds two layers of safety around every generated Cypher statement:

1. **`test_cypher`** — dry-runs the statement with Neo4j's `EXPLAIN` prefix (parses the query plan without executing any writes) to surface syntax errors.
2. **`fix_cypher`** — injects the Neo4j error back into `CYPHER_FIX_USER` (a Reflection Prompt variant) for LLM self-correction.
3. **`heal_cypher`** — orchestrates up to `settings.max_cypher_healing_attempts` (default 3) test→fix iterations. On exhaustion, logs `CRITICAL` and returns `None` so the builder graph can mark `cypher_failed=True` and continue.

---

## 2. Prerequisites

- `src/models/schemas.py` — `MappingProposal` (step 5)
- `src/prompts/templates.py` — `CYPHER_SYSTEM`, `CYPHER_FIX_USER` (step 7)
- `src/graph/cypher_generator.py` — `strip_cypher_fence` (step 20)
- `src/config/settings.py` — `get_settings()` for `max_cypher_healing_attempts` (step 2)
- `src/config/logging.py` — `get_logger`
- `neo4j` Python driver (official, ≥ 5.x)

---

## 3. Public API

| Symbol | Signature | Description |
|---|---|---|
| `test_cypher` | `(cypher: str, driver: neo4j.Driver) -> tuple[bool, str \| None]` | Dry-run via EXPLAIN; returns (True, None) or (False, error) |
| `fix_cypher` | `(cypher: str, error: str, mapping: MappingProposal, llm: LLMProtocol) -> str` | One-shot LLM fix via Reflection Prompt |
| `heal_cypher` | `(cypher: str, mapping: MappingProposal, driver, llm, max_attempts: int) -> str \| None` | Full retry loop; None on exhaustion |

---

## 4. Full Implementation

```python
"""Cypher healing — dry-run test via EXPLAIN + LLM self-correction loop.

EP-09 / US-09-02 and US-09-03:
  * test_cypher   — validate without executing (EXPLAIN prefix)
  * fix_cypher    — inject Neo4j error into Reflection Prompt
  * heal_cypher   — up to max_attempts test→fix iterations
"""

from __future__ import annotations

import logging

import neo4j.exceptions
from langchain_core.messages import HumanMessage, SystemMessage

from src.config.llm_client import LLMProtocol
from neo4j import Driver

from src.config.logging import get_logger
from src.config.settings import get_settings
from src.graph.cypher_generator import strip_cypher_fence
from src.models.schemas import MappingProposal
from src.prompts.templates import CYPHER_FIX_USER, CYPHER_SYSTEM

logger: logging.Logger = get_logger(__name__)


# ── Dry-Run Validation ─────────────────────────────────────────────────────────

def test_cypher(cypher: str, driver: Driver) -> tuple[bool, str | None]:
    """Validate a Cypher statement without executing any writes.

    Uses Neo4j's ``EXPLAIN`` prefix which parses and plans the query but
    does not run it, so no data is written or read.

    Args:
        cypher: The generated Cypher string to validate.
        driver: An open ``neo4j.Driver`` instance.

    Returns:
        ``(True, None)`` if Neo4j accepts the query plan.
        ``(False, error_message)`` on ``CypherSyntaxError``, ``ClientError``,
        or any other driver exception. The ``error_message`` is injected into
        the Reflection Prompt verbatim.
    """
    explain_stmt = f"EXPLAIN {cypher}"
    try:
        with driver.session() as session:
            session.run(explain_stmt).consume()
        logger.debug("test_cypher: EXPLAIN passed.")
        return True, None
    except neo4j.exceptions.CypherSyntaxError as exc:
        logger.warning("Cypher syntax error: %s", exc)
        return False, str(exc)
    except neo4j.exceptions.ClientError as exc:
        logger.warning("Cypher client error: %s", exc)
        return False, str(exc)
    except Exception as exc:
        logger.warning("Cypher test unexpected error: %s", exc)
        return False, str(exc)


# ── One-Shot LLM Fix ──────────────────────────────────────────────────────────

def fix_cypher(
    cypher: str,
    error: str,
    mapping: MappingProposal,
    llm: LLMProtocol,
) -> str:
    """Ask the LLM to correct a Cypher statement given the Neo4j error.

    Uses ``CYPHER_FIX_USER`` — a Reflection Prompt variant that embeds the
    broken Cypher and the exact Neo4j error message.

    Args:
        cypher:  The failing Cypher string.
        error:   The raw Neo4j error string from ``test_cypher``.
        mapping: The ``MappingProposal`` that produced the Cypher (for context).
        llm:     Reasoning LLM (temperature=0.0).

    Returns:
        A corrected Cypher string (markdown fences stripped).

    Raises:
        RuntimeError: If the LLM call itself fails.
    """
    user_prompt = CYPHER_FIX_USER.format(
        broken_cypher=cypher,
        error_message=error,
    )
    response = llm.invoke(
        [
            SystemMessage(content=CYPHER_SYSTEM),
            HumanMessage(content=user_prompt),
        ]
    )
    fixed = strip_cypher_fence(response.content)
    logger.debug("fix_cypher: LLM returned %d-char fix.", len(fixed))
    return fixed


# ── Full Healing Loop ─────────────────────────────────────────────────────────

def heal_cypher(
    cypher: str,
    mapping: MappingProposal,
    driver: Driver,
    llm: LLMProtocol,
    max_attempts: int | None = None,
) -> str | None:
    """Iteratively test and fix a Cypher statement until it passes or is exhausted.

    Attempt sequence:
    1. ``test_cypher`` — if passes, return immediately.
    2. ``fix_cypher``  — inject error into LLM Reflection Prompt.
    3. Repeat up to ``max_attempts`` total test+fix cycles.

    On exhaustion after ``max_attempts`` failures the function returns ``None``
    and logs a CRITICAL warning.  The builder graph should then set
    ``cypher_failed=True`` for this mapping and continue with the next table.

    Args:
        cypher:       Initial Cypher string from ``generate_cypher``.
        mapping:      The ``MappingProposal`` that produced the Cypher.
        driver:       An open ``neo4j.Driver`` for ``test_cypher``.
        llm:          Reasoning LLM for ``fix_cypher``.
        max_attempts: Override ``settings.max_cypher_healing_attempts`` (default 3).

    Returns:
        A valid Cypher string, or ``None`` if all attempts failed.
    """
    settings = get_settings()
    limit: int = max_attempts if max_attempts is not None else settings.max_cypher_healing_attempts

    current: str = cypher
    for attempt in range(1, limit + 1):
        ok, error = test_cypher(current, driver)
        if ok:
            logger.info(
                "Cypher healed for '%s' after %d attempt(s).",
                mapping.table_name, attempt,
            )
            return current

        logger.warning(
            "Cypher attempt %d/%d failed for '%s': %s",
            attempt, limit, mapping.table_name, error,
        )

        if attempt == limit:
            logger.critical(
                "Cypher healing exhausted for table '%s'. Marking as failed.",
                mapping.table_name,
            )
            return None

        try:
            current = fix_cypher(current, error, mapping, llm)
        except Exception as exc:
            logger.error("fix_cypher LLM call failed: %s — aborting healing.", exc)
            return None

    # Should be unreachable; guard for static analysis
    return None
```

---

## 5. Tests

```python
"""Unit tests for src/graph/cypher_healer.py — UT-17"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from src.graph.cypher_healer import fix_cypher, heal_cypher, test_cypher
from src.models.schemas import MappingProposal


# ── Helpers ────────────────────────────────────────────────────────────────────

GOOD_CYPHER = "MERGE (bc:BusinessConcept {name: $name})"
BAD_CYPHER = "MERGE (bc:BusinessConcept name: $name)"  # missing braces


def _mapping(table: str = "TB_CST") -> MappingProposal:
    return MappingProposal(
        table_name=table,
        mapped_concept="Customer",
        confidence=0.97,
        reasoning="Test.",
        alternative_concepts=[],
    )


def _make_driver(*, should_fail: bool = False, error_msg: str = "syntax error") -> MagicMock:
    import neo4j.exceptions

    driver = MagicMock()
    session = MagicMock()
    session.__enter__ = MagicMock(return_value=session)
    session.__exit__ = MagicMock(return_value=False)

    if should_fail:
        result = MagicMock()
        result.consume.side_effect = neo4j.exceptions.CypherSyntaxError(error_msg)
        session.run.return_value = result
    else:
        result = MagicMock()
        result.consume.return_value = None
        session.run.return_value = result

    driver.session.return_value = session
    return driver


def _make_llm(fixed_cypher: str) -> MagicMock:
    llm = MagicMock()
    resp = MagicMock()
    resp.content = fixed_cypher
    llm.invoke.return_value = resp
    return llm


# ── test_cypher ────────────────────────────────────────────────────────────────

class TestTestCypher:
    def test_valid_cypher_returns_true(self) -> None:
        driver = _make_driver(should_fail=False)
        ok, err = test_cypher(GOOD_CYPHER, driver)
        assert ok is True
        assert err is None

    def test_invalid_cypher_returns_false_with_error(self) -> None:
        driver = _make_driver(should_fail=True, error_msg="Invalid syntax near 'name'")
        ok, err = test_cypher(BAD_CYPHER, driver)
        assert ok is False
        assert err is not None
        assert len(err) > 0

    def test_explain_prefix_added(self) -> None:
        driver = _make_driver(should_fail=False)
        session = driver.session.return_value
        test_cypher(GOOD_CYPHER, driver)
        call_arg = session.run.call_args[0][0]
        assert call_arg.startswith("EXPLAIN ")

    def test_generic_exception_returns_false(self) -> None:
        driver = MagicMock()
        session = MagicMock()
        session.__enter__ = MagicMock(return_value=session)
        session.__exit__ = MagicMock(return_value=False)
        result = MagicMock()
        result.consume.side_effect = Exception("network error")
        session.run.return_value = result
        driver.session.return_value = session
        ok, err = test_cypher(GOOD_CYPHER, driver)
        assert ok is False
        assert "network error" in err


# ── fix_cypher ────────────────────────────────────────────────────────────────

class TestFixCypher:
    def test_returns_stripped_cypher(self) -> None:
        llm = _make_llm("```cypher\n" + GOOD_CYPHER + "\n```")
        result = fix_cypher(BAD_CYPHER, "syntax error", _mapping(), llm)
        assert "```" not in result
        assert "MERGE" in result

    def test_error_injected_in_prompt(self) -> None:
        llm = _make_llm(GOOD_CYPHER)
        fix_cypher(BAD_CYPHER, "CypherSyntaxError: expected { near name", _mapping(), llm)
        call = llm.invoke.call_args[0][0]
        human_content = call[1].content
        assert "CypherSyntaxError" in human_content

    def test_llm_failure_propagates(self) -> None:
        llm = MagicMock()
        llm.invoke.side_effect = RuntimeError("LLM down")
        with pytest.raises(RuntimeError):
            fix_cypher(BAD_CYPHER, "error", _mapping(), llm)


# ── heal_cypher ───────────────────────────────────────────────────────────────

class TestHealCypher:
    def test_passes_on_first_try(self) -> None:
        driver = _make_driver(should_fail=False)
        llm = MagicMock()
        result = heal_cypher(GOOD_CYPHER, _mapping(), driver, llm, max_attempts=3)
        assert result == GOOD_CYPHER
        llm.invoke.assert_not_called()

    def test_heals_on_second_attempt(self) -> None:
        import neo4j.exceptions

        call_count = 0

        def _side_effect(stmt):
            nonlocal call_count
            call_count += 1
            mock_result = MagicMock()
            if call_count == 1:
                mock_result.consume.side_effect = neo4j.exceptions.CypherSyntaxError("bad")
            else:
                mock_result.consume.return_value = None
            return mock_result

        driver = MagicMock()
        session = MagicMock()
        session.__enter__ = MagicMock(return_value=session)
        session.__exit__ = MagicMock(return_value=False)
        session.run.side_effect = _side_effect
        driver.session.return_value = session

        llm = _make_llm(GOOD_CYPHER)
        result = heal_cypher(BAD_CYPHER, _mapping(), driver, llm, max_attempts=3)
        assert result == GOOD_CYPHER

    def test_exhaustion_returns_none(self) -> None:
        driver = _make_driver(should_fail=True)
        llm = _make_llm(BAD_CYPHER)  # LLM keeps returning bad Cypher
        result = heal_cypher(BAD_CYPHER, _mapping(), driver, llm, max_attempts=3)
        assert result is None

    def test_max_attempts_respected(self) -> None:
        driver = _make_driver(should_fail=True)
        llm = _make_llm(BAD_CYPHER)
        heal_cypher(BAD_CYPHER, _mapping(), driver, llm, max_attempts=2)
        # test called 2 times, fix called 1 time (no fix on last attempt)
        assert llm.invoke.call_count == 1

    def test_fix_llm_failure_returns_none(self) -> None:
        driver = _make_driver(should_fail=True)
        llm = MagicMock()
        llm.invoke.side_effect = RuntimeError("LLM error")
        result = heal_cypher(BAD_CYPHER, _mapping(), driver, llm, max_attempts=3)
        assert result is None
```

---

## 6. Smoke Test

```bash
python -c "
from src.graph.cypher_healer import test_cypher
from unittest.mock import MagicMock

# Simulate a passing EXPLAIN without a real Neo4j instance
driver = MagicMock()
session = MagicMock()
session.__enter__ = lambda s: s
session.__exit__ = lambda *a: False
session.run.return_value = MagicMock(consume=MagicMock(return_value=None))
driver.session.return_value = session

ok, err = test_cypher('MERGE (n:BusinessConcept {name: \$name})', driver)
print('test_cypher passed:', ok, err)
"
```
