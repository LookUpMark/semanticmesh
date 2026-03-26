# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project Overview

**Multi-Agent Framework for Semantic Discovery & GraphRAG** — A generative AI system for automated Data Governance via LangGraph-orchestrated multi-agent architecture. The system bridges the semantic gap between unstructured business documentation (PDF) and relational database schemas (DDL/SQL) by autonomously constructing a Knowledge Graph on Neo4j.

**Two-Graph Architecture:**
1. **Builder Graph** (`src/graph/builder_graph.py`) — Ontology construction: extracts triplets, resolves entities, maps schemas, generates Cypher, upserts to Neo4j
2. **Query Graph** (`src/generation/query_graph.py`) — Advanced Agentic RAG: hybrid retrieval, cross-encoder reranking, answer generation with hallucination grading

---

## Development Commands

**Requirements:**
- Python 3.11+
- Neo4j 5.x

```bash
# Environment setup
source .venv/bin/activate          # Activate virtual environment
pip install -e ".[dev]"            # Install with dev dependencies

# Testing
pytest tests/unit/ -v              # Run unit tests only
pytest tests/integration/ -v       # Run integration tests (requires Neo4j)
pytest tests/unit/test_settings.py -v  # Run a specific test file
pytest -m "not integration" -v     # Run all tests except integration
pytest -m "integration" -v         # Run only integration tests
pytest -m "slow" -v                # Run slow tests (>10s)

# Linting and type checking
ruff check src/ tests/             # Lint code
ruff check --fix src/ tests/       # Auto-fix linting issues
mypy src/                          # Type check (strict mode)

# Format with ruff
ruff format src/ tests/

# Neo4j for development (Docker)
docker run -d --name neo4j-thesis -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/your_password_here \
  neo4j:5

# CLI entry points
ragas-eval                          # Run RAGAS evaluation
ablation-run                        # Run ablation experiments

# Utility scripts (via python -m scripts)
python -m scripts.neo4j_lifecycle --help     # Neo4j database management
python -m scripts.pipeline_run --help        # Run builder/query pipeline
```

---

## Project Structure

```
src/
├── config/           # EP-01: Infrastructure (config, settings, logging, LLM factory)
│   ├── config.py           # Application configuration defaults (dataclass)
│   ├── settings.py         # Pydantic settings with env var loading (uses config.py defaults)
│   ├── logging.py          # Structured JSON logging (get_logger, log_node_event)
│   ├── llm_factory.py      # Factory: get_reasoning_llm(), get_extraction_llm(), get_generation_llm()
│   ├── llm_client.py       # LLMProtocol + InstrumentedLLM wrapper (retry + logging)
│   ├── model_builders.py   # Helper: make_llm() for building one-off LLM instances
│   ├── provider_detection.py # Provider auto-detection from model names
│   └── tracing.py          # LangSmith tracing configuration
├── models/           # Data models and LangGraph state schemas
│   ├── schemas.py    # Pydantic v2 models: Triplet, Entity, TableSchema, MappingProposal, etc.
│   └── state.py      # BuilderState and QueryState TypedDict for LangGraph
├── prompts/          # LLM prompt templates and few-shot loaders
│   ├── templates.py  # All prompt constants (EXTRACTION_SYSTEM, MAPPING_USER, etc.)
│   └── few_shot.py   # load_cypher_examples(), load_mapping_examples()
├── utils/            # Shared utilities
│   ├── json_utils.py # JSON parsing and cleaning helpers
│   └── text_utils.py # Text processing utilities
├── ingestion/        # EP-02, EP-05: PDF and DDL processing
│   ├── pdf_loader.py      # load_pdf(), chunk_documents()
│   ├── ddl_parser.py      # parse_ddl() using sqlglot
│   └── schema_enricher.py # enrich_schema() — acronym expansion via LLM
├── extraction/       # EP-03: Triplet extraction
│   ├── triplet_extractor.py   # extract_triplets() using SLM in JSON mode
│   └── heuristic_extractor.py # Fallback rule-based extraction
├── resolution/       # EP-04: Entity resolution (blocking + LLM judge)
│   ├── blocking.py        # block_entities() — K-NN blocking with embeddings
│   ├── llm_judge.py       # judge_cluster() — LLM decides merge/separate
│   └── entity_resolver.py # resolve_entities() — orchestrator
├── mapping/          # EP-06, EP-07, EP-08: Schema-to-ontology mapping
│   ├── rag_mapper.py  # RAG-augmented mapping node (Map-Reduce pattern)
│   ├── retrieval.py   # RAG retrieval for mapping context
│   ├── validator.py   # Two-phase validation (Pydantic + Actor-Critic)
│   └── hitl.py        # Human-in-the-loop interrupt/resume logic
├── graph/            # EP-09, EP-10, EP-11: Neo4j and Cypher
│   ├── neo4j_client.py    # Neo4jClient wrapper (MERGE helpers)
│   ├── cypher_generator.py # generate_cypher() with few-shot examples
│   ├── cypher_healer.py    # Cypher Healing loop (reflection prompt)
│   ├── cypher_builder.py   # Deterministic parameterized MERGE builder (fallback)
│   ├── build_nodes.py      # Builder graph node implementations
│   └── validation_nodes.py # Validation-related nodes
├── retrieval/        # EP-12, EP-13: Hybrid retrieval
│   ├── embeddings.py       # BGE-M3 embedder (1024-dim dense vectors)
│   ├── bm25_retriever.py   # BM25 keyword retriever
│   ├── hybrid_retriever.py # Dense + BM25 + Graph traversal with RRF fusion
│   ├── reranker.py         # Cross-Encoder reranker (bge-reranker-large)
│   └── node_utils.py       # Neo4j traversal utilities
├── generation/       # EP-14, EP-15: Answer generation and query orchestration
│   ├── answer_generator.py     # generate_answer() with critique injection
│   ├── hallucination_grader.py # grade_answer() — Self-RAG paradigm
│   ├── context_distiller.py    # Context compression for generation
│   ├── lazy_expander.py        # Lazy context expansion strategy
│   ├── routing.py              # Query routing logic
│   └── nodes/                  # Query graph node implementations
│       ├── retrieval_nodes.py  # Retrieval nodes
│       ├── generation_nodes.py # Generation nodes
│       └── expansion_nodes.py  # Context expansion nodes
└── evaluation/       # EP-16: Evaluation metrics
    ├── ragas_runner.py      # run_ragas_evaluation()
    ├── custom_metrics.py    # cypher_healing_rate, hitl_confidence_agreement
    └── ablation_runner.py   # run_ablation() — toggles settings flags

scripts/                # Utility scripts for pipeline execution and analysis
├── pipeline_run.py          # Run the builder/query pipeline
├── run_ablation_full.py     # Run full ablation campaign (CLI: ablation-run)
├── run_all_ablations.py     # Run all ablation combinations
├── neo4j_lifecycle.py       # Neo4j database management (clear, schema setup)
├── analyze_ab00_trace.py    # Analyze ablation trace logs
├── manual_analysis.py       # Manual query testing and analysis
└── run_ab00_*.py           # Various ablation experiment runners

tests/
├── conftest.py       # Shared fixtures (test_settings, mock_llm, neo4j_container)
├── fixtures/         # Test data (sample_docs, sample_ddl, mock_responses)
│   └── gold_standard.json # QA pairs for RAGAS evaluation
├── unit/             # Unit tests (no external services)
└── integration/      # Integration tests (Neo4j required)

notebooks/
├── 00_interactive_demo.ipynb  # End-to-end interactive demonstration
└── ablation/                   # Ablation study analysis notebooks
    └── diagnostics/
```

---

## Critical Conventions

### Temperature Strategy
- **Extraction/Mapping/Grading nodes**: `T=0.0` (deterministic JSON output)
- **Answer Generation only**: `T=0.3` (fluency)
- Controlled via `settings.llm_model_temperature_*`

### LLM Usage Patterns
- Always import from `src.config.llm_factory`: `get_reasoning_llm()`, `get_extraction_llm()`, `get_generation_llm()`
- Never construct LLM instances directly in pipeline nodes
- Type annotate as `llm: LLMProtocol` (provider-agnostic)
- The factory returns `InstrumentedLLM` wrappers with retry and logging
- **Provider auto-detection:** `llm_factory.detect_provider(model)` in `provider_detection.py` selects the provider from the model name:
  - `"provider/model"` (contains `/`) → **OpenRouter** (e.g. `openai/gpt-oss-120b`, `anthropic/claude-3.5-sonnet`, `meta-llama/llama-3.3-70b-instruct:free`)
  - `gpt-*`, `o1-*`, `o3-*` (no slash) → **OpenAI** direct (requires `OPENAI_API_KEY`)
  - `claude-*` (no slash) → **Anthropic** direct (requires `ANTHROPIC_API_KEY`, `langchain-anthropic`)
  - Anything else → **LM Studio** local (`LMSTUDIO_BASE_URL`, default `http://localhost:1234/v1`)
- Use `make_llm(model, temperature, max_tokens, role)` from `model_builders.py` to build one-off LLM instances from any provider
- Call `reconfigure_from_env()` after changing `os.environ` in notebooks — clears both the settings cache (`reload_settings()`) and the LLM `lru_cache`

### Neo4j Cypher Conventions
- Always use `MERGE`, never bare `CREATE` (idempotent upserts)
- Cypher is generated by LLM with few-shot examples, validated via EXPLAIN dry-run, and auto-fixed via Cypher Healing loop
- If healing exhausts all attempts (`cypher_failed=True`), `_node_build_graph` falls back to `cypher_builder.build_upsert_cypher` — a deterministic parameterized builder immune to LLM quoting errors
- Vector index OPTIONS keys must use backtick-quoting in Neo4j 5.x: `` `vector.dimensions` `` (not `'vector.dimensions'`)
- `setup_schema(client)` must be called explicitly in both `run_builder()` and `run_query()` before any reads/writes

### Error Handling
- Per-item catch + log + skip; never crash the pipeline
- Use `get_logger(__name__)` for logging
- Use `log_node_event()` at the END of every LangGraph node
- Use `log_retry_event()` before each reflection retry

### State Management
- LangGraph state is `TypedDict` (`BuilderState`, `QueryState`) defined in `src/models/state.py`
- Nodes receive full state, return fields to update: `return {"triplets": new_triplets}`
- Use `NodeTimer` context manager for timing node execution

### Tracing and Debugging
- **LangSmith tracing**: Configure via `LANGCHAIN_TRACING_V2` and `LANGCHAIN_API_KEY` env vars
- **Trace analysis**: `scripts/analyze_ab00_trace.py` — analyzes LangSmith traces for ablation experiments
- **Debug runners**: `scripts/run_ab00_debug.py`, `scripts/run_ab00_logged.py` — pipeline runs with enhanced logging
- **Manual testing**: `scripts/manual_analysis.py` — interactive query testing and analysis

### Actor-Critic Best-Proposal Tracking
- `BuilderState` carries a `best_proposal: MappingProposal | None` field alongside `mapping_proposal`
- `_node_validate_mapping` updates `best_proposal` whenever a Pydantic-valid proposal with higher confidence is seen
- On critic exhaustion (`attempts >= max_reflection_attempts`), the node returns `best_proposal` (highest confidence seen across all retries) instead of the last rejected proposal
- Logged at WARNING level with concept name and confidence for observability

### Critic Entity Context Ordering
- `critic_review()` in `validator.py` sorts entities by name length ascending before slicing to `[:20]`
- Shorter names = concept-level (e.g. "Customer", "Product") → appear first in critic context
- Longer names = attribute-level (e.g. "unique numeric identifier for the customer") → cut off
- Prevents false rejections when the critic cannot find the concept name in its context window

### HITL (Human-in-the-Loop)
- Confidence threshold controlled by `settings.confidence_threshold` (default 0.90)
- Below threshold → `state["hitl_required"] = True`, triggers `interrupt()`
- Resume logic in `src/mapping/hitl.py`

### Ablation Flags
Settings boolean flags to disable pipeline components:
- `enable_schema_enrichment` — Skip acronym expansion
- `enable_cypher_healing` — Skip Cypher auto-fix
- `enable_critic_validation` — Skip Actor-Critic validation
- `enable_reranker` — Skip cross-encoder reranking
- `enable_hallucination_grader` — Skip hallucination grading
- `retrieval_mode` — "hybrid" | "vector" | "bm25"

> **Note:** `er_similarity_threshold` default is now `0.75` (previously `0.85`).

---

## Key Architecture Patterns

### Two-Stage Entity Resolution
1. **Blocking** — K-NN blocking with BGE-M3 embeddings, groups candidates by similarity threshold
2. **LLM Judge** — LLM decides whether to merge each cluster or keep variants separate

### Self-Reflection Loops
- **Actor-Critic**: LLM generates mapping → LLM critic validates → if rejected, inject critique and retry (max `settings.max_reflection_attempts`, then auto-accept)
- **Cypher Healing**: Generate Cypher → EXPLAIN dry-run on Neo4j → if `CypherSyntaxError`, inject error into reflection prompt and retry → if healing exhausted, fall back to deterministic builder

### FK Edge Upserts
- `build_fk_cypher(table)` in `cypher_builder.py` generates `(:PhysicalTable)-[:REFERENCES {fk_column, ref_column}]->(:PhysicalTable)` edges
- Called from `_node_build_graph` after the main table upsert — creates stub `PhysicalTable` nodes for referenced tables not yet processed
- All MERGE-based, idempotent — safe to re-run

### Embeddings & Reranker (GPU considerations)
- BGE-M3 (`get_embeddings()`): `FlagModel(model_name, use_fp16=False, devices=["cpu"])` — must run on CPU when GPU is shared with LM Studio
- bge-reranker-large (`get_reranker()`): `FlagReranker(model_name, use_fp16=False, device="cpu")` — same reason
- Reranker CUDA guard: `get_reranker()` temporarily sets `CUDA_VISIBLE_DEVICES=""` during `FlagReranker.__init__` to prevent OOM on shared GPUs; the env var is restored after init
- Do NOT pass `show_progress_bar` to `model.encode()` — FlagEmbedding propagates kwargs to tokenizer which rejects it

### Hybrid Retrieval with RRF
- Three channels: Dense vector (BGE-M3), BM25 keyword (`bm25_retriever.py`), Graph traversal (Neo4j)
- Reciprocal Rank Fusion merges results without tuning weights
- Final reranking with cross-encoder (bge-reranker-large)

### Self-Reflection Loops
All JSON-producing LLM nodes implement self-reflection on parse/validation failure using `REFLECTION_TEMPLATE` (PT-05). Retries are bounded by `settings.max_reflection_attempts` (default 3). Nodes with self-reflection:
- `triplet_extractor.py` — via `_reflect_on_json()` helper; when `raw_json==""` (token cap hit) uses `truncated=True` variant that instructs "extract at most 10 triplets, be concise"
- `rag_mapper.py` — inline `_clean_json()` + REFLECTION_TEMPLATE retry; markdown fences stripped before `json.loads`
- `llm_judge.py` — inline `_clean_json()` + REFLECTION_TEMPLATE retry; markdown fences stripped before `json.loads`
- `hallucination_grader.py` — inline REFLECTION_TEMPLATE retry; emits only `pass | regenerate` (`web_search` action removed); after `max_hallucination_retries`, forces `action="pass"` (accepts current answer)
- `validator.py` (Actor-Critic) — explicit reflection loop (pre-existing)
- `cypher_healer.py` — Cypher-specific reflection loop (pre-existing)

### Fallback Extraction
- **`heuristic_extractor.py`**: Rule-based triplet extraction using spaCy NLP — serves as fallback when LLM extraction fails

### LLM Routing Architecture
- `detect_provider(model)` infers provider from model name — no manual routing config needed
- `make_llm(model, temperature, max_tokens, role)` builds the correct `ChatOpenAI`/`ChatAnthropic` instance
- `reconfigure_from_env()` clears all LRU caches; call it after changing `os.environ` in notebooks
- All pipeline nodes use `LLMProtocol` structural type — no code changes needed when switching providers
- Default split: reasoning/generation → OpenRouter; extraction → auto-detected from model name

### Utility Functions
Common utilities in `src/utils/`:
- **`json_utils.py`**: `clean_json()` — strips markdown fences, fixes trailing commas; `safe_json_loads()` — with error logging
- **`text_utils.py`**: Text normalization, chunking helpers

### Scripts and Notebooks
- **`scripts/neo4j_lifecycle.py`**: Database management — clear database, setup constraints/indexes
- **`scripts/pipeline_run.py`**: Run builder/query pipeline from command line
- **`scripts/run_ablation_full.py`**: Full ablation campaign runner (CLI: `ablation-run`)
- **`notebooks/00_interactive_demo.ipynb`**: End-to-end interactive demonstration
- **`notebooks/ablation/`**: Analysis notebooks for ablation study results

---

## Testing Guidelines

### Unit Tests
- No external services (no Neo4j, no real LLM calls)
- Use `mock_llm` fixture that returns fixed JSON from `tests/fixtures/mock_responses/`
- Use `test_settings` fixture to override env vars to safe test values

### Integration Tests
- Marked with `@pytest.mark.integration` — require Neo4j
- Use `neo4j_container` fixture (testcontainers, session-scoped)
- Use `neo4j_client` fixture (connected to test container)

### Test Markers
Use pytest markers to select test categories:
- `integration`: Tests requiring external services (Neo4j)
- `slow`: Tests that take > 10s to run

Example: `pytest -m "not integration" -v` runs all non-integration tests

### Test Fixtures
- Sample docs: `tests/fixtures/sample_docs/` (business glossary, data dictionary)
- Sample DDL: `tests/fixtures/sample_ddl/` (simple_schema.sql, complex_schema.sql)
- Mock responses: `tests/fixtures/mock_responses/` (fixed LLM outputs)
- Gold standard: `tests/fixtures/gold_standard.json` (QA pairs for RAGAS)

---

## Documentation References

- **Implementation guides**: `docs/implementation/00-overview.md` — Zero-to-hero guides for each file
- **Task tracking**: `docs/implementation/TASK.md` — Detailed task list with prerequisites
- **Specifications**: `docs/draft/SPECS.md` — Architecture, state schemas, node specs
- **Requirements**: `docs/draft/REQUIREMENTS.md` — Epic/user story breakdown
- **Prompts**: `docs/draft/PROMPTS.md` — All prompt template definitions (PT-01 through PT-11)

---

## Configuration

The application uses a two-tier configuration system:

1. **`src/config/config.py`** — Non-sensitive defaults (dataclass)
   - Model names, temperatures, thresholds, feature flags
   - All defaults are visible in code for easy modification
   - Can be overridden via environment variables

2. **`.env` file** — Sensitive values only
   - API keys (none required for LM Studio)
   - Passwords (`NEO4J_PASSWORD`)

### Accessing Configuration

```python
from src.config.settings import get_settings

settings = get_settings()
# Access any config value:
model = settings.llm_model_reasoning
threshold = settings.confidence_threshold
```

### Environment Variables

Sensitive values in `.env`:

| Category | Key Variables |
|----------|---------------|
| **Neo4j** | `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD` |
| **LLM (cloud)** | `OPENROUTER_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY` |
| **LLM (local)** | `LMSTUDIO_BASE_URL` (default: `http://localhost:1234/v1`) |

Non-sensitive defaults (in `config.py`, overrideable via env):

| Category | Key Variables |
|----------|---------------|
| **LLM** | `LLM_MODEL_REASONING`, `LLM_MODEL_EXTRACTION`, `LLM_TEMPERATURE_*`, `LLM_MAX_TOKENS_EXTRACTION`, `LLM_MAX_TOKENS_REASONING` |
| **Embeddings** | `EMBEDDING_MODEL`, `RERANKER_MODEL` |
| **Entity Resolution** | `ER_BLOCKING_TOP_K`, `ER_SIMILARITY_THRESHOLD` |
| **Thresholds** | `CONFIDENCE_THRESHOLD`, `MAX_REFLECTION_ATTEMPTS`, `MAX_CYPHER_HEALING_ATTEMPTS` |
| **Chunking** | `CHUNK_SIZE`, `CHUNK_OVERLAP` |
| **Retrieval** | `RETRIEVAL_VECTOR_TOP_K`, `RETRIEVAL_BM25_TOP_K`, `RETRIEVAL_GRAPH_DEPTH` |
| **Ablation** | `ENABLE_SCHEMA_ENRICHMENT`, `ENABLE_CYPHER_HEALING`, `RETRIEVAL_MODE`, etc. |
| **Logging** | `LOG_LEVEL` |
