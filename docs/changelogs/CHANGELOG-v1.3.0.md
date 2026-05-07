# Changelog — v1.3.0

**Release date:** 2026-05-07

## Highlights

- **Per-tier LLM configuration** — Each LLM tier (Reasoning, Extraction, Generation, Midtier) now supports explicit provider, model, endpoint, and reasoning effort via dedicated env vars (`LLM_PROVIDER_<TIER>`, `LLM_MODEL_<TIER>`, `LLM_ENDPOINT_<TIER>`, `LLM_EFFORT_<TIER>`)
- **LLM usage tracking** — Global token/call counter with formatted table summary at pipeline end
- **API session logging** — Structured JSON logs for API sessions with usage stats on shutdown
- **Architecture diagrams** — 16 Mermaid-to-PNG diagrams for thesis documentation (Builder Graph, Query Graph + 14 component diagrams)

## Features

### Per-Tier LLM Configuration (`src/config/`)
- Explicit per-tier env vars: `LLM_PROVIDER_REASONING`, `LLM_MODEL_REASONING`, `LLM_ENDPOINT_REASONING`, `LLM_EFFORT_REASONING` (same for EXTRACTION, GENERATION, MIDTIER)
- Fallback chain: explicit tier → global `LLM_PROVIDER` → `detect_provider(model)` from model name
- Updated `llm_factory.py` with new routing logic
- Updated `settings.py` and `config.py` with per-tier fields
- Updated `model_builders.py` for provider/endpoint passthrough

### LLM Usage Tracker (`src/config/llm_client.py`)
- `UsageTracker` class: thread-safe token/call accumulator per model
- Auto-integrated into `InstrumentedLLM` wrapper
- `get_global_usage()` for programmatic access
- Formatted summary table in `scripts/run_pipeline.py`

### API Session Logging (`src/api/app.py`)
- Structured startup/shutdown logging
- JSON usage dump to `outputs/api/` on shutdown
- Request timing middleware

### Architecture Diagrams (`docs/images/`)
- `scripts/export_mermaid_png.py` — Playwright-based Mermaid→PNG exporter
- `docs/images/component_diagrams.md` — 14 component Mermaid sources
- 16 PNG outputs: Builder Graph, Query Graph, Configuration System, Data Models, Prompt Engineering, Utilities, Ingestion, Triplet Extraction, Entity Resolution, RAG Mapping & Validation, Graph Construction, Retrieval, Answer Generation & Grading, REST API, Evaluation, Ablation Framework
- `docs/images/thesis_figures.tex` — LaTeX snippets for inclusion

## Documentation

- README.md updated with Mermaid architecture diagrams and per-tier config table
- `.env.example` expanded with all per-tier env vars
- `docs/RUNNING_SERVICES.md` — Service deployment guide
- `docs/study-guide/02-config/03-logging-tracing.md` — Updated logging docs

## Fixes

- Fixed `test_llm_factory.py` and `test_llm_client.py` for new per-tier logic
- Fixed `conftest.py` mock for `_inject_observability_callbacks`
- Provider detection extended with new model prefixes

## Removed

- `scripts/test_api_features.py` (replaced by proper test suite)
- `scripts/test_incremental_updates.py` (replaced by proper test suite)

## Stats

- 41 files changed, +1650 / -1441 lines
