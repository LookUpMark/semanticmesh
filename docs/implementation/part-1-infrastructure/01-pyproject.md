# Part 1 — `pyproject.toml` + `.env.example`

## 1. Purpose & Context

**Epic:** EP-01 — Infrastructure & Configuration  
**US:** US-01-01 — Environment & Dependency Management

`pyproject.toml` is the single source of truth for all project dependencies, build configuration, and tool settings. Implements PEP 621. The `.env.example` is the canonical reference for all environment variables.

---

## 2. Prerequisites

None. This is step 1.

---

## 3. Files Modified

| File | Action |
|---|---|
| `pyproject.toml` | Fill `dependencies` and `dev` arrays; add `[project.scripts]` |
| `.env.example` | Already present — verify completeness |

---

## 4. Full Implementation

### `pyproject.toml`

```toml
[project]
name = "thesis"
version = "0.1.0"
description = "Multi-Agent Framework for Semantic Discovery & GraphRAG"
readme = "README.md"
license = { text = "MIT" }
requires-python = ">=3.11"
authors = [{ name = "Marc'Antonio Lopez" }]

dependencies = [
    "langgraph>=0.2",
    "langchain>=0.3",
    "langchain-openrouter>=0.1",
    "langchain-community>=0.3",
    "neo4j>=5.0",
    "pydantic>=2.7",
    "pydantic-settings>=2.3",
    "sentence-transformers>=3.0",
    "FlagEmbedding>=1.2",
    "pymupdf>=1.24",
    "sqlglot>=25.0",
    "ragas>=0.2",
    "rank-bm25>=0.2",
    "httpx>=0.27",
    "python-json-logger>=2.0",
    "tiktoken>=0.7",
    "scikit-learn>=1.4",
    "faiss-cpu>=1.8",
    "langchain-tavily>=0.1",
    "tenacity>=8.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23",
    "pytest-mock>=3.14",
    "testcontainers[neo4j]>=4.7",
    "ruff>=0.4",
    "mypy>=1.10",
    "types-requests>=2.32",
]

[project.scripts]
ragas-eval = "src.evaluation.ragas_runner:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
target-version = "py311"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "A", "SIM", "TCH"]

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
markers = [
    "integration: marks tests requiring external services (Neo4j)",
    "slow: marks tests that take > 10s",
]
```

### Dependency Rationale

| Package | Min Version | Purpose |
|---|---|---|
| `langgraph` | `>=0.2` | DAG state machine, `interrupt()`, checkpointing |
| `langchain` | `>=0.3` | Prompt templates, chain composition, tool calls |
| `langchain-openrouter` | `>=0.1` | `ChatOpenRouter` — thesis LLM client (OpenRouter Free Tier); architecture-level swap point |
| `tenacity` | `>=8.0` | Exponential-backoff retry for rate-limit / timeout errors in `InstrumentedLLM` |
| `langchain-community` | `>=0.3` | Tavily/DuckDuckGo search tools |
| `neo4j` | `>=5.0` | Official Neo4j Python driver |
| `pydantic` | `>=2.7` | Schema validation on all LLM outputs |
| `pydantic-settings` | `>=2.3` | `BaseSettings` + `.env` loading |
| `sentence-transformers` | `>=3.0` | BGE-M3 embedding model |
| `FlagEmbedding` | `>=1.2` | BGE-M3 advanced features + `FlagReranker` |
| `pymupdf` | `>=1.24` | PDF text extraction (fitz) |
| `sqlglot` | `>=25.0` | DDL SQL parsing with dialect auto-detection |
| `ragas` | `>=0.2` | Automated RAG quality evaluation |
| `rank-bm25` | `>=0.2` | BM25Okapi keyword search |
| `httpx` | `>=0.27` | Async HTTP client |
| `python-json-logger` | `>=2.0` | JSON-formatted structured logging |
| `tiktoken` | `>=0.7` | Token count estimation for chunking |
| `scikit-learn` | `>=1.4` | `NearestNeighbors` for K-NN blocking |
| `faiss-cpu` | `>=1.8` | Fast vector similarity (ER blocking) |
| `langchain-tavily` | `>=0.1` | Web search fallback tool |

### `.env.example`

Already exists at the repo root. Verify it contains all variables from `REQUIREMENTS.md §8`. Key groups:

```bash
# Neo4j, LLM endpoint, LLM models, temperatures,
# embedding/reranker models, ER thresholds,
# loop guards (max_reflection_attempts, etc.),
# chunk size/overlap, retrieval top-K values,
# ablation flags (enable_schema_enrichment, retrieval_mode, etc.),
# LOG_LEVEL
```

---

## 5. Tests

`pyproject.toml` has no direct unit tests. Validate via install:

```bash
# Verify the metadata is valid PEP 621
pip install --dry-run -e ".[dev]"

# Verify ruff config
ruff check src/ --select E,F,W,I

# Verify mypy config
mypy src/ --ignore-missing-imports
```

---

## 6. Smoke Test

```bash
pip install -e ".[dev]"
python -c "import langgraph, langchain_openrouter, neo4j, pydantic, sqlglot, tenacity; print('All imports OK')"
```

Expected output: `All imports OK`
