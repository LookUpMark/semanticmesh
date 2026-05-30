# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project Overview

**Multi-Agent Framework for Semantic Discovery & GraphRAG** — Generative AI system for automated Data Governance. LangGraph-orchestrated multi-agent architecture. Bridges semantic gap between unstructured business docs (PDF) and relational DB schemas (DDL/SQL) by building Knowledge Graph on Neo4j.

**Two-Graph Architecture:**
1. **Builder Graph** (`src/graph/builder_graph.py`) — Ontology construction: triplet extraction, entity resolution, schema mapping, Cypher generation, Neo4j upsert
2. **Query Graph** (`src/generation/query_graph.py`) — Advanced Agentic RAG: hybrid retrieval, cross-encoder reranking, answer generation with hallucination grading

---

## Development Commands

**Requirements:** Python 3.11+, Neo4j 5.x

```bash
# Environment setup
source .venv/bin/activate
pip install -e ".[dev]"

# Testing
pytest tests/unit/ -v                        # Unit tests only (no external services)
pytest tests/integration/ -v                 # Integration tests (requires Neo4j)
pytest tests/unit/test_settings.py -v        # Run a specific test file
pytest -m "not integration" -v               # All tests except integration
pytest -m "integration" -v                   # Only integration tests
pytest -m "slow" -v                          # Slow tests (>10s)

# Linting and formatting
ruff check src/ tests/                       # Lint
ruff check --fix src/ tests/                 # Auto-fix
ruff format src/ tests/                      # Format

# Type checking
mypy src/                                    # Strict mode

# Neo4j (Docker — only for Neo4j, not the app)
docker run -d --name neo4j-thesis -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/your_password_here neo4j:5

# CLI entry points
pipeline-run              # Run pipeline (single/multi study, multi-dataset)
ablation-run              # Alias for pipeline-run
ragas-eval                # Run RAGAS evaluation
ai-judge                  # Run AI-as-Judge evaluation

# Utility scripts
python -m scripts.neo4j_lifecycle --help     # Neo4j DB management

# REST API (FastAPI + uvicorn)
python -m scripts.serve_api                  # Default: 127.0.0.1:8000
python -m scripts.serve_api --reload         # Dev mode (auto-reload)
# Swagger UI: http://127.0.0.1:8000/docs

# LangGraph Studio (interactive graph visualization)
langgraph dev                                # http://127.0.0.1:2024
```

---

## Project Structure

```
src/
├── config/           # Infrastructure: config, settings, logging, LLM factory, provider detection, tracing
│   ├── config.py           # Application configuration defaults (dataclass)
│   ├── settings.py         # Pydantic settings with env var loading (uses config.py defaults)
│   ├── llm_factory.py      # Factory: get_reasoning_llm(), get_extraction_llm(), get_generation_llm()
│   ├── llm_client.py       # LLMProtocol + InstrumentedLLM wrapper (retry + logging)
│   ├── model_builders.py   # make_llm() for building one-off LLM instances
│   ├── provider_detection.py # Provider auto-detection from model names (fallback, deprecated as primary)
│   └── tracing.py          # LangSmith + Langfuse tracing configuration
├── models/           # Pydantic v2 schemas + LangGraph state TypedDicts
│   ├── schemas.py          # Triplet, Entity, TableSchema, MappingProposal, etc.
│   └── state.py            # BuilderState, QueryState for LangGraph
├── prompts/          # LLM prompt templates and few-shot loaders
│   ├── templates.py        # All prompt constants (EXTRACTION_SYSTEM, MAPPING_USER, etc.)
│   └── few_shot.py         # load_cypher_examples(), load_mapping_examples()
├── utils/            # Shared utilities
│   ├── json_utils.py       # clean_json(), reflect_on_json()
│   ├── text_utils.py       # Text normalization, chunking helpers
│   └── query_utils.py      # Query-related utilities
├── ingestion/        # PDF and DDL processing
│   ├── pdf_loader.py       # load_pdf(), chunk_documents() with SHA-256 incremental detection
│   ├── ddl_parser.py       # parse_ddl() using sqlglot
│   └── schema_enricher.py  # enrich_schema() — acronym expansion via LLM
├── extraction/       # Triplet extraction
│   ├── triplet_extractor.py   # extract_triplets() using SLM in JSON mode
│   └── heuristic_extractor.py # Fallback rule-based extraction (spaCy NLP)
├── resolution/       # Entity resolution (blocking + LLM judge)
│   ├── blocking.py         # block_entities() — K-NN blocking with BGE-M3 embeddings
│   ├── llm_judge.py        # judge_cluster() — LLM decides merge/separate
│   └── entity_resolver.py  # resolve_entities() — orchestrator
├── mapping/          # Schema-to-ontology mapping
│   ├── rag_mapper.py       # RAG-augmented mapping node (Map-Reduce pattern)
│   ├── retrieval.py        # RAG retrieval for mapping context
│   ├── validator.py        # Two-phase validation (Pydantic + Actor-Critic)
│   └── hitl.py             # Human-in-the-loop interrupt/resume logic
├── graph/            # Neo4j and Cypher
│   ├── neo4j_client.py     # Neo4jClient wrapper (MERGE helpers, UNWIND batch writes)
│   ├── cypher_generator.py # generate_cypher() with few-shot examples
│   ├── cypher_healer.py    # Cypher Healing loop (reflection prompt)
│   ├── cypher_builder.py   # Deterministic parameterized MERGE builder (fallback)
│   ├── build_nodes.py      # Builder graph node implementations
│   ├── validation_nodes.py # Validation-related nodes
│   └── parallel_mapping.py # ThreadPool parallel mapping+validation (mapping_concurrency)
├── retrieval/        # Hybrid retrieval
│   ├── embeddings.py       # BGE-M3 embedder (1024-dim dense vectors)
│   ├── bm25_retriever.py   # BM25 keyword retriever
│   ├── hybrid_retriever.py # Dense + BM25 + Graph traversal with RRF fusion
│   ├── reranker.py         # Cross-Encoder reranker (bge-reranker-v2-m3)
│   └── node_utils.py       # Neo4j traversal utilities
├── generation/       # Answer generation and query orchestration
│   ├── answer_generator.py     # generate_answer() with critique injection
│   ├── hallucination_grader.py # grade_answer() — Self-RAG paradigm
│   ├── context_distiller.py    # Context compression for generation
│   ├── lazy_expander.py        # Lazy context expansion strategy
│   ├── routing.py              # Query routing logic
│   └── nodes/                  # Query graph node implementations
│       ├── retrieval_nodes.py  # Retrieval nodes
│       ├── generation_nodes.py # Generation nodes
│       └── expansion_nodes.py  # Context expansion nodes
├── api/              # REST API (FastAPI)
│   ├── app.py               # Application factory + routers
│   ├── demo_router.py       # Demo endpoints: build, query, pipeline (async with polling)
│   ├── ablation_router.py   # Ablation endpoints: run preset/custom, status, matrix
│   ├── auth.py              # API key auth (X-API-Key header, disabled when API_KEY unset)
│   ├── jobs.py              # In-memory job store
│   └── models.py            # Pydantic request/response models
└── evaluation/       # Evaluation metrics
    ├── ragas_runner.py      # run_ragas_evaluation()
    ├── custom_metrics.py    # cypher_healing_rate, hitl_confidence_agreement
    ├── ablation_runner.py   # run_ablation() — toggles settings flags
    └── bundle_writer.py     # write_evaluation_bundle() — JSON bundle for AI-as-Judge

scripts/                # Utility scripts
├── serve_api.py             # REST API server (FastAPI + uvicorn)
├── neo4j_lifecycle.py       # Neo4j database management (clear, schema setup)
├── run_pipeline.py          # Unified pipeline runner (CLI: pipeline-run / ablation-run)
├── run_ai_judge.py          # AI-as-Judge evaluation (CLI: ai-judge)
└── generate_ablation_report.py  # Ablation report generation

tests/
├── conftest.py              # Shared fixtures (test_settings, mock_llm, neo4j_container)
├── fixtures/                # Numbered datasets (00_legacy/ through 07_stress_large_scale/)
│                            # Each: business_glossary, data_dictionary, schema.sql, gold_standard.json
├── unit/                    # Unit tests (no external services)
├── integration/             # Integration tests (Neo4j required)
└── evaluation/              # Evaluation tests (ablation, gold standard loader, RAGAS)
```

---

## Critical Conventions

### Temperature Strategy
- **Extraction/Mapping/Grading nodes**: `T=0.0` (deterministic JSON output)
- **Answer Generation only**: `T=0.3` (fluency)
- Controlled via `settings.llm_model_temperature_*`

### LLM Usage Patterns
- Import from `src.config.llm_factory`: `get_reasoning_llm()`, `get_extraction_llm()`, `get_generation_llm()`, `get_lightweight_llm()`, `get_midtier_llm()`
- Never construct LLM instances directly in pipeline nodes
- Type annotate as `llm: LLMProtocol` (provider-agnostic)
- Factory returns `InstrumentedLLM` wrappers with retry + logging
- **Factory tiers:** `get_reasoning_llm()` (main reasoning), `get_extraction_llm()` (JSON extraction), `get_generation_llm()` (answer gen, T=0.3), `get_lightweight_llm()` (reuses extraction model), `get_midtier_llm()` (mini model, RAG mapping, Actor-Critic, hallucination grading)
- **Explicit per-tier configuration** (preferred): each tier has 4 env vars:
  - `LLM_PROVIDER_<TIER>` — explicit provider name (`openai`, `openrouter`, `anthropic`, `lmstudio`, `ollama`, etc.)
  - `LLM_MODEL_<TIER>` — model identifier (e.g. `gpt-5.4-nano-2026-03-17`)
  - `LLM_ENDPOINT_<TIER>` — base URL (empty = provider default)
  - `LLM_EFFORT_<TIER>` — reasoning effort: `minimal`|`low`|`medium`|`high`|empty (only for OpenAI reasoning models)
  - Tiers: `REASONING`, `EXTRACTION`, `GENERATION`, `MIDTIER`. `lightweight` reuses extraction settings.
- **Fallback chain** (backward compat): explicit tier > global `LLM_PROVIDER` > `detect_provider(model)` from model name prefix
- **Free→Paid fallback:** Models ending `:free` auto-fallback to paid on HTTP 429 via `FallbackLLM` wrapper
- **OpenAI reasoning models** (`o1-*`, `o2-*`, `o3-*`, `o4-*`, `gpt-5*`): special `reasoning_effort` param handling
- Use `make_llm(model, temperature, max_tokens, role, provider=..., provider_base_url=...)` from `llm_factory.py` for one-off LLM instances
- Call `reconfigure_from_env()` after changing `os.environ` in notebooks — clears settings cache and LLM `lru_cache`

### Neo4j Cypher Conventions
- Always `MERGE`, never bare `CREATE` (idempotent upserts)
- UNWIND batch writes for ~87% Neo4j write reduction over individual MERGE operations
- Cypher generated by LLM with few-shot examples, validated via EXPLAIN dry-run, auto-fixed via Cypher Healing loop
- If healing exhausts attempts (`cypher_failed=True`), falls back to `cypher_builder.build_upsert_cypher` — deterministic parameterized builder immune to LLM quoting errors
- Vector index OPTIONS keys need backtick-quoting in Neo4j 5.x: `` `vector.dimensions` `` (not `'vector.dimensions'`)
- `setup_schema(client)` must be called explicitly in `run_builder()` and `run_query()` before any reads/writes

### Error Handling
- Per-item catch + log + skip; never crash pipeline
- Use `get_logger(__name__)` for logging
- `log_node_event()` at END of every LangGraph node
- `log_retry_event()` before each reflection retry

### State Management
- LangGraph state = `TypedDict` (`BuilderState`, `QueryState`) in `src/models/state.py`
- Nodes receive full state, return fields to update: `return {"triplets": new_triplets}`
- Use `NodeTimer` context manager for timing node execution

### Tracing and Observability
- **LangSmith tracing**: Configure via `LANGCHAIN_TRACING_V2` and `LANGCHAIN_API_KEY` env vars
- **Langfuse**: Configure via `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST`
- **LangGraph Studio**: Run `langgraph dev` for interactive graph visualization and step-through debugging
- **Debug trace system**: Enable via `settings.enable_debug_trace` — writes per-query traces to `settings.trace_output_dir`

### Self-Reflection Loops
All JSON-producing LLM nodes self-reflect on parse/validation failure using `REFLECTION_TEMPLATE` (PT-05). Retries bounded by `settings.max_reflection_attempts` (default 3). Nodes with self-reflection:
- **Actor-Critic validation** (`validator.py`): LLM generates mapping → critic validates → if rejected, inject critique + retry (then auto-accept). `BuilderState` tracks `best_proposal` across retries.
- **Cypher Healing** (`cypher_healer.py`): Generate Cypher → EXPLAIN dry-run → if `CypherSyntaxError`, inject error + retry → if exhausted, fall back to deterministic builder
- **Triplet extraction** (`triplet_extractor.py`): via `_reflect_on_json()`; when `raw_json==""` (token cap hit) uses `truncated=True` variant
- **RAG mapping** (`rag_mapper.py`), **LLM judge** (`llm_judge.py`): `clean_json()` + REFLECTION_TEMPLATE retry
- **Hallucination grader** (`hallucination_grader.py`): emits `pass | regenerate`; after `max_hallucination_retries`, forces `action="pass"`

### Critic Entity Context Ordering
- `critic_review()` in `validator.py` sorts entities by name length ascending before slicing `[:20]`
- Shorter names = concept-level ("Customer", "Product") → appear first; longer names = attribute-level → cut off
- Prevents false rejections when critic can't find concept name in context window

### HITL (Human-in-the-Loop)
- Confidence threshold: `settings.confidence_threshold` (default 0.90)
- Below threshold → `state["hitl_required"] = True`, triggers `interrupt()`
- Resume logic in `src/mapping/hitl.py`

### Ablation Flags
Settings boolean flags to disable pipeline components:
- `enable_schema_enrichment` — Skip acronym expansion
- `enable_cypher_healing` — Skip Cypher auto-fix
- `enable_critic_validation` — Skip Actor-Critic validation
- `enable_reranker` — Skip cross-encoder reranking
- `enable_hallucination_grader` — Skip hallucination grading
- `enable_retrieval_quality_gate` — Skip retrieval quality gating
- `enable_grader_consistency_validator` — Skip grader consistency checks
- `enable_spacy_heuristics` — Skip spaCy heuristic extraction
- `enable_lazy_expansion` — Skip lazy context expansion
- `use_lazy_extraction` — Enable lazy extraction mode
- `retrieval_mode` — "hybrid" | "vector" | "bm25"

> `er_similarity_threshold` default: `0.75`. `reranker_top_k` default: `5` (AB-BEST optimum, validated cross-dataset).

---

## Key Architecture Patterns

### Two-Stage Entity Resolution
1. **Blocking** — K-NN blocking with BGE-M3 embeddings, groups candidates by similarity threshold
2. **LLM Judge** — LLM decides merge or keep separate

### Parallel Mapping (Performance)
- When `mapping_concurrency > 1` (default 5), all tables are mapped+validated concurrently via `ThreadPoolExecutor` before sequential graph writes
- Results stored in `precomputed_proposals` state field; `rag_mapping`/`validate_mapping` nodes consume them without redundant LLM calls
- ~5x speedup on datasets with 50+ tables

### Duplicate Concept Handling
- When two tables map to the same `BusinessConcept`, `build_nodes.py` detects the existing node and re-links the `PhysicalTable` via `MAPPED_TO` instead of attempting a rename (which would violate the unique constraint)

### FK Edge Upserts
- `build_fk_cypher(table)` in `cypher_builder.py` generates `(:PhysicalTable)-[:REFERENCES {fk_column, ref_column}]->(:PhysicalTable)` edges
- Called from `_node_build_graph` after main table upsert — creates stub `PhysicalTable` nodes for unprocessed referenced tables
- All MERGE-based, idempotent — safe to re-run

### Incremental Ingestion
- SHA-256 change detection skips unchanged documents on re-runs

### Embeddings & Reranker (GPU auto-detection)
- BGE-M3 (`get_embeddings()`): auto-detects GPU via `torch.cuda.is_available()` — `devices=["cuda:0"]` + `use_fp16=True` if available, else CPU
- bge-reranker-v2-m3 (`get_reranker()`): same auto-detection — `device="cuda:0"` + `use_fp16=True` if available, else CPU
- Do NOT pass `show_progress_bar` to `model.encode()` — FlagEmbedding propagates kwargs to tokenizer which rejects it

### Hybrid Retrieval with RRF
- Three channels: Dense vector (BGE-M3), BM25 keyword (`bm25_retriever.py`), Graph traversal (Neo4j)
- Reciprocal Rank Fusion merges results without weight tuning
- Final reranking with cross-encoder (bge-reranker-v2-m3)

### REST API (FastAPI)
- **`src/api/app.py`**: Application factory with demo + ablation routers + config endpoints
- **Authentication**: `X-API-Key` header when `API_KEY` env var is set; disabled (dev mode) when unset
- **Demo API** (`/api/v1/demo/`): Async E2E pipeline — build, query, pipeline endpoints with job polling/SSE streaming; graph stats/data; KG snapshots CRUD; conversations CRUD
- **Ablation API** (`/api/v1/ablation/`): Run preset/custom studies, matrix, datasets, bundles, AI-Judge payloads
- **Config API** (`/api/v1/config`): `GET` returns non-sensitive settings; `POST` applies runtime overrides (no restart)
- Swagger UI at `/docs`, ReDoc at `/redoc`, health check at `/health` (no auth)

---

## Testing Guidelines

### Unit Tests
- No external services (no Neo4j, no real LLM calls)
- Use `mock_llm` fixture — returns fixed JSON from `tests/fixtures/00_legacy/mock_responses/`
- Use `test_settings` fixture — overrides env vars to safe test values

### Integration Tests
- Marked with `@pytest.mark.integration` — require Neo4j
- Use `neo4j_container` fixture (testcontainers, session-scoped)
- Use `neo4j_client` fixture (connected to test container)

### Test Markers
- `integration`: Tests requiring external services (Neo4j)
- `slow`: Tests taking >10s

### Test Fixtures
- Numbered dataset directories: `00_legacy/` through `07_stress_large_scale/`
- Each dataset: `business_glossary.*`, `data_dictionary.*`, `schema.sql`, `gold_standard.json`
- `00_legacy/` also has `mock_responses/` (fixed LLM outputs) and `smoke/` subdirs

---

## Configuration

Two-tier config system:

1. **`src/config/config.py`** — Non-sensitive defaults (dataclass). Overridable via env vars.
2. **`.env` file** — Sensitive values only. Copy from `.env.example`.

### Accessing Configuration

```python
from src.config.settings import get_settings
settings = get_settings()
```

### Key Environment Variables

| Category | Key Variables |
|----------|---------------|
| **Neo4j** | `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD` |
| **LLM (per-tier)** | `LLM_PROVIDER_<TIER>`, `LLM_MODEL_<TIER>`, `LLM_ENDPOINT_<TIER>`, `LLM_EFFORT_<TIER>` (tiers: `REASONING`, `EXTRACTION`, `GENERATION`, `MIDTIER`) |
| **LLM (cloud keys)** | `OPENAI_API_KEY`, `OPENROUTER_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, `MISTRAL_API_KEY`, `COHERE_API_KEY`, `GROQ_API_KEY` |
| **LLM (local)** | `LMSTUDIO_BASE_URL` (default: `http://localhost:1234/v1`) |
| **Observability** | `LANGCHAIN_TRACING_V2`, `LANGCHAIN_API_KEY`, `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY` |
| **Embeddings** | `EMBEDDING_MODEL`, `RERANKER_MODEL` |
| **Thresholds** | `CONFIDENCE_THRESHOLD`, `MAX_REFLECTION_ATTEMPTS`, `MAX_CYPHER_HEALING_ATTEMPTS`, `ER_SIMILARITY_THRESHOLD` |
| **Retrieval** | `RETRIEVAL_VECTOR_TOP_K`, `RETRIEVAL_BM25_TOP_K`, `RETRIEVAL_GRAPH_DEPTH`, `RETRIEVAL_MODE` |

---

## Documentation References

| Document | Description |
|----------|-------------|
| `docs/draft/SPECS.md` | Architecture, state schemas, node specs |
| `docs/draft/REQUIREMENTS.md` | Epic/user story breakdown |
| `docs/draft/PROMPTS.md` | All prompt template definitions (PT-01 through PT-11) |
| `docs/draft/ADR.md` | Architecture Decision Records (15 ADRs) |
| `docs/draft/ABLATION.md` | Ablation study design |
| `docs/draft/DATASET.md` | Dataset specifications |
| `docs/draft/TEST_PLAN.md` | Test strategy and test case catalogue |
| `docs/AI_JUDGE_PROMPT.md` | System prompt for AI-as-Judge evaluation |
| `docs/RUNNING_SERVICES.md` | Service deployment guide |
| `docs/ablation/RESULTS.md` | Full ablation results |
| `docs/study-guide/` | Module-by-module study guide (15 chapters) |
| `docs/changelogs/` | Version changelogs (v1.0.0 → v1.4.2) |
| `docs/audits/` | Security audit reports |

---

## Documenti Wiki Integration

SemanticMesh is a source within the Documenti wiki (`~/Documenti/wiki/`). When working on semanticmesh within the Documenti context, use `/wiki-ingest` to update wiki pages after significant changes. See `~/Documenti/CLAUDE.md` and `~/Documenti/AGENTS.md` for full wiki operations.
