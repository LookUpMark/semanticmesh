# Part 8 — `src/generation/hallucination_grader.py`

## 1. Purpose & Context

**Epic:** EP-14 Answer Generation & Hallucination Grader  
**US-14-02** — Hallucination Grader Node

The Hallucination Grader is an adversarial LLM node that reads the generated answer, the user's query, and the context chunks, then decides if any claims in the answer are unsupported.

Three possible verdicts:
- `"pass"` — answer is fully grounded; send to user.
- `"regenerate"` — specific unsupported claims found; inject critique and retry generation.
- `"web_search"` — context is entirely irrelevant; fall back to external search.

A `QueryState.iteration_count` guard in the Query Graph prevents infinite regeneration loops.

---

## 2. Prerequisites

- `src/models/schemas.py` — `RetrievedChunk`, `GraderDecision` (step 5)
- `src/prompts/templates.py` — `GRADER_SYSTEM`, `GRADER_USER` (step 7)
- `src/config/logging.py` — `get_logger`

---

## 3. Public API

| Symbol | Signature | Description |
|---|---|---|
| `grade_answer` | `(query, answer, chunks, llm) -> GraderDecision` | LLM grader verdict with critique on failure |

---

## 4. Full Implementation

```python
"""Hallucination grader — adversarial LLM audit of generated answers.

EP-14 / US-14-02:
Determines if the generated answer is grounded in the retrieved context.
Returns a GraderDecision driving the Query Graph routing.
"""

from __future__ import annotations

import json
import logging

from langchain_core.messages import HumanMessage, SystemMessage

from src.config.llm_client import LLMProtocol
from pydantic import ValidationError

from src.config.logging import get_logger
from src.generation.answer_generator import format_context
from src.models.schemas import GraderDecision, RetrievedChunk
from src.prompts.templates import GRADER_SYSTEM, GRADER_USER

logger: logging.Logger = get_logger(__name__)


def grade_answer(
    query: str,
    answer: str,
    chunks: list[RetrievedChunk],
    llm: LLMProtocol,
) -> GraderDecision:
    """Audit a generated answer for unsupported claims against the context chunks.

    The grader LLM receives:
    - The user's original question.
    - The generated answer to audit.
    - All context chunks in numbered format (same representation as the generator).

    It must return a JSON object matching ``GraderDecision``.  On any parse or
    validation error the grader defaults to ``grounded=True, action="pass"``
    to avoid blocking the pipeline on grader malfunction.

    Args:
        query:   The user's natural-language question.
        answer:  The generated answer to audit.
        chunks:  Reranked context chunks used during generation.
        llm:     Reasoning LLM — temperature MUST be 0.0 (deterministic audit).

    Returns:
        ``GraderDecision`` with ``grounded``, ``critique``, and ``action`` fields.
    """
    context_block = format_context(chunks)
    user_prompt = GRADER_USER.format(
        context=context_block,
        question=query,
        answer=answer,
    )

    try:
        response = llm.invoke(
            [
                SystemMessage(content=GRADER_SYSTEM),
                HumanMessage(content=user_prompt),
            ]
        )
        raw_json: str = response.content.strip()
    except Exception as exc:
        logger.warning(
            "Grader LLM call failed (%s) — defaulting to pass.", exc
        )
        return GraderDecision(grounded=True, critique=None, action="pass")

    try:
        data: dict = json.loads(raw_json)
        decision = GraderDecision(**data)
    except (json.JSONDecodeError, ValidationError) as exc:
        logger.warning(
            "Grader response parse error (%s) — defaulting to pass.", exc
        )
        return GraderDecision(grounded=True, critique=None, action="pass")

    # Consistency check: grounded=True must have action="pass"
    if decision.grounded and decision.action != "pass":
        logger.warning(
            "Grader inconsistency (grounded=True but action=%s) — forcing pass.",
            decision.action,
        )
        return GraderDecision(grounded=True, critique=None, action="pass")

    logger.info(
        "Grader verdict: grounded=%s, action=%s, critique=%r.",
        decision.grounded, decision.action,
        (decision.critique or "")[:120],
    )
    return decision
```

---

## 5. Tests

```python
"""Unit tests for src/generation/hallucination_grader.py — UT-22"""

from __future__ import annotations

import json
from unittest.mock import MagicMock

import pytest

from src.generation.hallucination_grader import grade_answer
from src.models.schemas import GraderDecision, RetrievedChunk


# ── Helpers ────────────────────────────────────────────────────────────────────

def _chunk(name: str) -> RetrievedChunk:
    return RetrievedChunk(
        node_id=name, node_type="BusinessConcept",
        text=f"{name}: definition text", score=0.85,
        source_type="vector", metadata={},
    )

def _make_llm(decision: dict) -> MagicMock:
    llm = MagicMock()
    resp = MagicMock()
    resp.content = json.dumps(decision)
    llm.invoke.return_value = resp
    return llm


# ── grade_answer ──────────────────────────────────────────────────────────────

class TestGradeAnswer:
    def test_pass_verdict(self) -> None:
        llm = _make_llm({"grounded": True, "critique": None, "action": "pass"})
        decision = grade_answer("Query?", "Answer.", [_chunk("X")], llm)
        assert decision.grounded is True
        assert decision.action == "pass"
        assert decision.critique is None

    def test_regenerate_verdict(self) -> None:
        llm = _make_llm({
            "grounded": False,
            "critique": "TB_ORDERS is not in any retrieved chunk.",
            "action": "regenerate",
        })
        decision = grade_answer("Query?", "TB_ORDERS stores orders.", [_chunk("Customer")], llm)
        assert decision.grounded is False
        assert decision.action == "regenerate"
        assert "TB_ORDERS" in decision.critique

    def test_web_search_verdict(self) -> None:
        llm = _make_llm({"grounded": False, "critique": "No relevant context.", "action": "web_search"})
        decision = grade_answer("Obscure query?", "I don't know.", [], llm)
        assert decision.action == "web_search"

    def test_llm_failure_defaults_to_pass(self) -> None:
        llm = MagicMock()
        llm.invoke.side_effect = RuntimeError("LLM unavailable")
        decision = grade_answer("?", "Answer.", [], llm)
        assert decision.action == "pass"
        assert decision.grounded is True

    def test_bad_json_defaults_to_pass(self) -> None:
        llm = MagicMock()
        resp = MagicMock()
        resp.content = "not json"
        llm.invoke.return_value = resp
        decision = grade_answer("?", "Answer.", [], llm)
        assert decision.action == "pass"

    def test_inconsistent_grounded_true_with_non_pass_is_corrected(self) -> None:
        llm = _make_llm({"grounded": True, "critique": None, "action": "regenerate"})
        decision = grade_answer("?", "Answer.", [_chunk("X")], llm)
        assert decision.action == "pass"

    def test_context_injected_in_prompt(self) -> None:
        llm = _make_llm({"grounded": True, "critique": None, "action": "pass"})
        grade_answer("What is Customer?", "Customer buys goods.", [_chunk("Customer")], llm)
        call_args = llm.invoke.call_args[0][0]
        human_content = call_args[1].content
        assert "Customer" in human_content

    def test_answer_injected_in_prompt(self) -> None:
        llm = _make_llm({"grounded": True, "critique": None, "action": "pass"})
        grade_answer("Q?", "My special answer text.", [_chunk("X")], llm)
        call_args = llm.invoke.call_args[0][0]
        human_content = call_args[1].content
        assert "My special answer text." in human_content
```

---

## 6. Smoke Test

```bash
python -c "
from src.generation.hallucination_grader import grade_answer
from src.models.schemas import GraderDecision, RetrievedChunk
from unittest.mock import MagicMock
import json

llm = MagicMock()
resp = MagicMock()
resp.content = json.dumps({'grounded': True, 'critique': None, 'action': 'pass'})
llm.invoke.return_value = resp

chunk = RetrievedChunk(node_id='Customer', node_type='BusinessConcept', text='Customer: buys goods', score=0.9, source_type='vector', metadata={})
decision = grade_answer('Who buys things?', 'The Customer entity represents buyers.', [chunk], llm)
print('Grader verdict:', decision.action)
print('hallucination_grader smoke test passed.')
"
```
