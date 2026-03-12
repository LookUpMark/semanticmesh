# Part 8 — Answer Generation & Query Graph

Part 8 implements the final pipeline layer: generating natural-language answers from the Knowledge Graph using Self-RAG (Self-Reflective Retrieval-Augmented Generation), grading those answers for hallucinations, falling back to web search when context is irrelevant, and wiring everything together in a LangGraph `StateGraph`.

## TASK-26: Answer Generation

`src/generation/answer_generator.py` exposes three public functions:

**`format_context(chunks)`** formats reranked `RetrievedChunk` objects as a numbered list for injection into the LLM prompt:

```
[1] Customer: A person who buys products.  [type=BusinessConcept, score=0.97]
[2] Order: A purchase transaction.          [type=BusinessConcept, score=0.88]
```

**`generate_answer(query, chunks, llm, critique=None)`** generates a grounded answer using the `ANSWER_SYSTEM` / `ANSWER_USER` prompt pair (temperature 0.3). If a `critique` from the Hallucination Grader is provided on retry, the `ANSWER_WITH_CRITIQUE_USER` template is used instead — injecting the specific unsupported claims so the model corrects them without inventing new information.

**`web_search_fallback(query)`** is triggered when the Hallucination Grader returns `action="web_search"`. It attempts Tavily first (`TAVILY_API_KEY`), falls back to DuckDuckGo, and returns a string prefixed `[Source: Web Search]`. Both search backends are imported lazily inside the function, with graceful degradation when both fail.

## TASK-27: Hallucination Grading with Self-RAG

`src/generation/hallucination_grader.py` implements `grade_answer(query, answer, chunks, llm) -> GraderDecision`.

The grader calls `GRADER_SYSTEM` / `GRADER_USER` at temperature 0.0 (deterministic audit). The LLM receives the context, the generated answer, and the original question, and must return a JSON `GraderDecision`:

| `action` | `grounded` | Meaning |
|---|---|---|
| `"pass"` | `True` | All claims are supported — accept the answer |
| `"regenerate"` | `False` | Specific unsupported claims found — inject critique and retry |
| `"web_search"` | `False` | Context is entirely irrelevant — fall back to external search |

Three safety guarantees:
- **LLM failure** → defaults to `GraderDecision(grounded=True, action="pass")` to avoid blocking the pipeline
- **Bad JSON / Pydantic error** → same conservative default
- **Inconsistency** (`grounded=True` with `action != "pass"`) → auto-corrected to `action="pass"`

## TASK-28: Query Graph with Conditional Routing

`src/generation/query_graph.py` wires all components into a compiled LangGraph `StateGraph` over `QueryState`.

**Graph topology:**

```
hybrid_retrieval → reranking → answer_generation → hallucination_grader
                                      ↑                      |
                               (regenerate)          (pass) → finalise → END
                                      |              (web_search) → web_search → END
                                      └──────────────────────┘
```

**Nodes:**

| Node | Function |
|---|---|
| `hybrid_retrieval` | `vector_search` + `bm25_search` + `graph_traversal` + `merge_results` |
| `reranking` | `rerank()` with cross-encoder |
| `answer_generation` | `generate_answer()` with optional critique injection |
| `hallucination_grader` | `grade_answer()` + loop guard |
| `web_search` | `web_search_fallback()` |
| `finalise` | assembles `final_answer` + `sources` list |

**Loop guard:** `iteration_count` in `QueryState` increments on each `answer_generation` call. When `iteration_count >= settings.max_hallucination_retries`, the grader node forces `action="web_search"` regardless of the LLM verdict, preventing infinite regeneration loops.

**`_route_after_grader(state)`** is the conditional edge function:
- `"pass"` → `"finalise"`
- `"regenerate"` → `"answer_generation"` (with critique in `last_critique`)
- `"web_search"` → `"web_search"`
- `None` / unknown → `"finalise"` (safe default)

**`build_query_graph()`** compiles the graph with `MemorySaver` checkpointing. **`run_query(user_query)`** is a convenience wrapper that builds the graph, sets an initial `QueryState`, invokes it, and returns `{"final_answer": str, "sources": list[str]}`.

## The Two-Graph Architecture

Part 8 completes the full system. Two LangGraph `StateGraph` instances work together:

1. **Builder Graph** (Part 6) — offline, batch: PDF + DDL → Knowledge Graph (Neo4j)
2. **Query Graph** (Part 8) — online, latency-sensitive: user query → grounded answer

The Builder Graph runs periodically to update the graph with new documents or schema changes. The Query Graph serves user queries against the current graph state.

---

### Implementation References

- [`answer_generator.py`](../implementation/part-8-generation/26-answer-generator.md) — `generate_answer`, `web_search_fallback`, `format_context`
- [`hallucination_grader.py`](../implementation/part-8-generation/27-hallucination-grader.md) — Self-RAG grading with `GraderDecision`
- [`query_graph.py`](../implementation/part-8-generation/28-query-graph.md) — full Query Graph wiring and routing

