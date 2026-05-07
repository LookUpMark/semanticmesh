# Changelog — v1.2.0

**Date:** 2026-05-07

## Summary

Observability & traceability release — full LangSmith + Langfuse integration for dual-backend LLM call tracing, pipeline visualization, and cost/token analytics. Zero-overhead when not configured (opt-in via environment variables).

## New Features

### Observability Integration (`src/config/observability.py`)

- **LangSmith support**: Auto-enabled when `LANGCHAIN_TRACING_V2=true` + `LANGCHAIN_API_KEY` are set. LangChain/LangGraph natively trace all LLM calls, graph node transitions, and state snapshots to Smith dashboard.
- **Langfuse support**: `LangchainCallbackHandler` injected into every LLM `.invoke()`/`.ainvoke()` call via `InstrumentedLLM._inject_observability_callbacks()`. Captures token usage, latency, cost, and full prompt/response pairs.
- **Dual-backend**: Both can run simultaneously. LangSmith uses internal LangChain hooks (env-var-based), Langfuse uses explicit callback injection.
- **Zero overhead**: When keys are not configured, `get_observability_callbacks()` returns an empty list — no performance penalty.

### Pipeline Metadata Tagging

- **Builder Graph**: Each `graph.invoke()` includes metadata with `study_id`, `job_id`, document count, DDL file count, and tags `["builder", study_id]`.
- **Query Graph**: Each `graph.invoke()` includes metadata with `study_id`, `query_index`, question (first 100 chars), session_id, and tags `["query", study_id]`.
- Enables filtering in LangSmith/Langfuse dashboards by study, pipeline type, or custom criteria.

### LangGraph Studio Support

- **`langgraph.json`**: Configuration file for LangGraph Studio desktop app. References `build_builder_graph` and `build_query_graph` entry points for real-time graph visualization and step-through debugging.

## Changes

### `src/config/llm_client.py`

- `InstrumentedLLM.invoke()`: Calls `_inject_observability_callbacks()` before model invocation.
- `InstrumentedLLM.ainvoke()`: Same injection for async path.
- New method `_inject_observability_callbacks(kwargs)`: Merges active Langfuse callbacks into `config.callbacks` kwarg.

### `src/config/settings.py`

- Added observability fields: `langchain_tracing_v2`, `langchain_api_key`, `langchain_project`, `langfuse_public_key`, `langfuse_secret_key`, `langfuse_host`.

### `src/api/app.py`

- Startup event: Logs which observability backends are active.
- Shutdown event: Calls `flush_observability()` to ensure pending Langfuse data is sent.

### `pyproject.toml`

- Added `langfuse>=2.0,<4.0` to dependencies.

### `.env.example`

- Added LangSmith section (`LANGCHAIN_TRACING_V2`, `LANGCHAIN_API_KEY`, `LANGCHAIN_PROJECT`).
- Added Langfuse section (`LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST`).

### `.gitignore`

- Added `.langfuse/` directory exclusion.

## Documentation

- **`README.md`**: New "Observability" subsection under Configuration with env var snippets and link to detailed docs. Updated Table of Contents.
- **`docs/RUNNING_SERVICES.md`**: Full observability section with architecture ASCII diagram, setup instructions for both backends, verification steps.
- **`docs/study-guide/02-config/03-logging-tracing.md`**: Extended with Langfuse integration details, `observability.py` API reference, file listing.

## Migration Guide

No breaking changes. To enable observability:

```bash
# Add to your .env:

# LangSmith (free tier: 5k traces/month)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls-...
LANGCHAIN_PROJECT=semanticmesh

# Langfuse (hobby tier: 50k observations/month)
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com
```

Then restart the server. Verify with startup logs:
```
INFO  Observability: LangSmith tracing ENABLED
INFO  Observability: Langfuse tracing ENABLED
```
