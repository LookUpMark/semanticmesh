# Part 8 — `src/generation/answer_generator.py`

## 1. Purpose & Context

**Epic:** EP-14 Answer Generation & Hallucination Grader  
**US-14-01** — Answer Generation Node, **US-14-03** — Web Search Fallback

`answer_generator` takes the top-K reranked chunks and a user query, then produces a grounded natural-language answer. A second call path (`with_critique`) injects the Hallucination Grader's critique back into the prompt for self-correction.

When all graph context is irrelevant, `web_search_fallback` retrieves an external summary via DuckDuckGo or Tavily and prefixes the result with `"[Source: Web Search]"`.

---

## 2. Prerequisites

- `src/models/schemas.py` — `RetrievedChunk` (step 5)
- `src/prompts/templates.py` — `ANSWER_SYSTEM`, `ANSWER_USER`, `ANSWER_WITH_CRITIQUE_USER` (step 7)
- `src/config/settings.py` — `llm_model_reasoning`, `llm_temperature_generation` (step 2)
- `src/config/logging.py` — `get_logger`
- `langchain-community` — `DuckDuckGoSearchRun` / `TavilySearchResults`

---

## 3. Public API

| Symbol | Signature | Description |
|---|---|---|
| `format_context` | `(chunks: list[RetrievedChunk]) -> str` | Numbered context block for the prompt |
| `generate_answer` | `(query, chunks, llm, critique=None) -> str` | Generate grounded answer; inject critique if provided |
| `web_search_fallback` | `(query: str) -> str` | DuckDuckGo/Tavily search; returns `"[Source: Web Search] ..."` |

---

## 4. Full Implementation

```python
"""Answer generation and web search fallback.

EP-14 / US-14-01 and US-14-03:
  * generate_answer       — LLM answer from reranked context chunks
  * web_search_fallback   — external search when graph context is empty/irrelevant
"""

from __future__ import annotations

import logging

from langchain_core.messages import HumanMessage, SystemMessage

from src.config.llm_client import LLMProtocol

from src.config.logging import get_logger
from src.models.schemas import RetrievedChunk
from src.prompts.templates import ANSWER_SYSTEM, ANSWER_USER, ANSWER_WITH_CRITIQUE_USER

logger: logging.Logger = get_logger(__name__)


# ── Context Formatter ─────────────────────────────────────────────────────────

def format_context(chunks: list[RetrievedChunk]) -> str:
    """Format reranked chunks as a numbered list for injection into the answer prompt.

    Args:
        chunks: Reranked ``RetrievedChunk`` list (passed in score-descending order).

    Returns:
        Multi-line string like::

            [1] Customer: A person who buys products. (score=0.97)
            [2] Order: A purchase transaction. (score=0.88)
    """
    if not chunks:
        return "(no context retrieved)"
    lines: list[str] = []
    for i, chunk in enumerate(chunks, start=1):
        node_type = chunk.node_type
        score = chunk.score
        lines.append(f"[{i}] {chunk.text}  [type={node_type}, score={score:.3f}]")
    return "\n".join(lines)


# ── Answer Generator ──────────────────────────────────────────────────────────

def generate_answer(
    query: str,
    chunks: list[RetrievedChunk],
    llm: LLMProtocol,
    critique: str | None = None,
) -> str:
    """Generate a grounded natural-language answer from reranked context chunks.

    If ``critique`` is provided (from the Hallucination Grader on a retry), the
    alternative ``ANSWER_WITH_CRITIQUE_USER`` template is used, which embeds the
    previous critique before the question so the model can correct its answer.

    Args:
        query:    The user's natural-language question.
        chunks:   Reranked ``RetrievedChunk`` list.
        llm:      Reasoning LLM (temperature = ``settings.llm_temperature_generation``).
        critique: Optional Hallucination Grader critique from the previous attempt.

    Returns:
        The generated answer string.
    """
    context_block = format_context(chunks)

    if critique:
        user_prompt = ANSWER_WITH_CRITIQUE_USER.format(
            context=context_block,
            critique=critique,
            question=query,
        )
    else:
        user_prompt = ANSWER_USER.format(
            context=context_block,
            question=query,
        )

    logger.debug(
        "generate_answer: query='%s', %d chunks, critique=%s.",
        query[:60], len(chunks), "yes" if critique else "no",
    )
    response = llm.invoke(
        [
            SystemMessage(content=ANSWER_SYSTEM),
            HumanMessage(content=user_prompt),
        ]
    )
    answer: str = response.content.strip()
    logger.info("Answer generated (%d chars).", len(answer))
    return answer


# ── Web Search Fallback ────────────────────────────────────────────────────────

def web_search_fallback(query: str) -> str:
    """Search the web for the query and return a labelled summary.

    Tries Tavily first (requires ``TAVILY_API_KEY`` in env); falls back to
    DuckDuckGo if Tavily is unavailable or raises.

    Args:
        query: The user's natural-language question.

    Returns:
        A string prefixed with ``"[Source: Web Search]"`` containing the
        search result summary.
    """
    logger.info("Web search fallback triggered for query: '%s'.", query[:80])

    # ── Try Tavily ──
    try:
        from langchain_community.tools.tavily_search import TavilySearchResults
        tavily = TavilySearchResults(max_results=3)
        results = tavily.invoke({"query": query})
        if results:
            summary = " ".join(
                r.get("content", "") for r in results[:3] if isinstance(r, dict)
            )
            return f"[Source: Web Search] {summary.strip()}"
    except Exception as exc:
        logger.debug("Tavily unavailable (%s) — trying DuckDuckGo.", exc)

    # ── Try DuckDuckGo ──
    try:
        from langchain_community.tools import DuckDuckGoSearchRun
        ddg = DuckDuckGoSearchRun()
        result = ddg.run(query)
        return f"[Source: Web Search] {result.strip()}"
    except Exception as exc:
        logger.warning("DuckDuckGo search also failed: %s", exc)
        return "[Source: Web Search] No external results could be retrieved."
```

---

## 5. Tests

```python
"""Unit tests for src/generation/answer_generator.py — UT-21"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from src.generation.answer_generator import format_context, generate_answer, web_search_fallback
from src.models.schemas import RetrievedChunk


# ── Helpers ────────────────────────────────────────────────────────────────────

def _chunk(name: str, text: str, score: float = 0.9) -> RetrievedChunk:
    return RetrievedChunk(
        node_id=name, node_type="BusinessConcept",
        text=text, score=score, source_type="vector", metadata={},
    )

def _make_llm(response: str) -> MagicMock:
    llm = MagicMock()
    resp = MagicMock()
    resp.content = response
    llm.invoke.return_value = resp
    return llm


# ── format_context ─────────────────────────────────────────────────────────────

class TestFormatContext:
    def test_numbered_list(self) -> None:
        chunks = [_chunk("C", "Customer: buyer"), _chunk("P", "Product: item")]
        result = format_context(chunks)
        assert "[1]" in result
        assert "[2]" in result

    def test_empty_returns_placeholder(self) -> None:
        assert "no context" in format_context([]).lower()

    def test_score_in_output(self) -> None:
        result = format_context([_chunk("X", "X: text", score=0.753)])
        assert "0.753" in result


# ── generate_answer ───────────────────────────────────────────────────────────

class TestGenerateAnswer:
    def test_returns_string(self) -> None:
        llm = _make_llm("The customer table stores buyer info.")
        answer = generate_answer("What is customer?", [_chunk("Customer", "Customer: buyer")], llm)
        assert isinstance(answer, str)
        assert len(answer) > 0

    def test_no_chunks_uses_placeholder_context(self) -> None:
        llm = _make_llm("I cannot find this information.")
        answer = generate_answer("What is X?", [], llm)
        call_args = llm.invoke.call_args[0][0]
        assert "no context" in call_args[1].content.lower()

    def test_critique_uses_alternative_template(self) -> None:
        llm = _make_llm("Corrected answer.")
        generate_answer("?", [_chunk("X", "X")], llm, critique="You mentioned TB_ORDERS which is unsupported.")
        call_args = llm.invoke.call_args[0][0]
        human_content = call_args[1].content
        assert "TB_ORDERS" in human_content

    def test_strips_whitespace_from_response(self) -> None:
        llm = _make_llm("  Answer with spaces  ")
        answer = generate_answer("?", [], llm)
        assert answer == "Answer with spaces"


# ── web_search_fallback ────────────────────────────────────────────────────────

class TestWebSearchFallback:
    def test_returns_web_search_prefix(self) -> None:
        with patch("src.generation.answer_generator.TavilySearchResults") as mock_tavily:
            mock_tool = MagicMock()
            mock_tool.invoke.return_value = [{"content": "some result"}]
            mock_tavily.return_value = mock_tool
            result = web_search_fallback("Who is a customer?")
        assert result.startswith("[Source: Web Search]")

    def test_duckduckgo_fallback(self) -> None:
        with patch("src.generation.answer_generator.TavilySearchResults", side_effect=ImportError):
            with patch("src.generation.answer_generator.DuckDuckGoSearchRun") as mock_ddg:
                mock_tool = MagicMock()
                mock_tool.run.return_value = "DDG result"
                mock_ddg.return_value = mock_tool
                result = web_search_fallback("test query")
        assert "[Source: Web Search]" in result
        assert "DDG result" in result

    def test_all_search_fails_returns_graceful_message(self) -> None:
        with patch("src.generation.answer_generator.TavilySearchResults", side_effect=ImportError):
            with patch("src.generation.answer_generator.DuckDuckGoSearchRun", side_effect=ImportError):
                result = web_search_fallback("unknown query")
        assert "[Source: Web Search]" in result
```

---

## 6. Smoke Test

```bash
python -c "
from src.generation.answer_generator import format_context
from src.models.schemas import RetrievedChunk

chunks = [
    RetrievedChunk(node_id='Customer', node_type='BusinessConcept', text='Customer: A person who buys goods', score=0.97, source_type='vector', metadata={}),
    RetrievedChunk(node_id='Order',    node_type='BusinessConcept', text='Order: A purchase transaction',    score=0.88, source_type='bm25',   metadata={}),
]
ctx = format_context(chunks)
print(ctx)
print('format_context smoke test passed.')
"
```
