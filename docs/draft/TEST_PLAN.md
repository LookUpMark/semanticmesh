# Test Plan

> **Project:** Multi-Agent Framework for Semantic Discovery & GraphRAG
> **Version:** 1.0 — March 2026
> **Companion documents:** [SPECS.md](./SPECS.md), [REQUIREMENTS.md](./REQUIREMENTS.md), [DATASET.md](./DATASET.md)
> **Purpose:** Complete test strategy for every component of the system. An AI coding agent must implement these tests alongside the production code — not after.

---

## Table of Contents

1. [Testing Philosophy](#1-testing-philosophy)
2. [Test Infrastructure](#2-test-infrastructure)
3. [Unit Tests by Module](#3-unit-tests-by-module)
   - [UT-01 — Settings & Configuration](#ut-01--settings--configuration)
   - [UT-02 — PDF Loader & Chunking](#ut-02--pdf-loader--chunking)
   - [UT-03 — DDL Parser](#ut-03--ddl-parser)
   - [UT-04 — Triplet Extraction](#ut-04--triplet-extraction)
   - [UT-05 — Entity Resolution (Stage 1 — Blocking)](#ut-05--entity-resolution-stage-1--blocking)
   - [UT-06 — Entity Resolution (Stage 2 — LLM Judge)](#ut-06--entity-resolution-stage-2--llm-judge)
   - [UT-07 — RAG Mapping Node](#ut-07--rag-mapping-node)
   - [UT-08 — Mapping Validator & Critic](#ut-08--mapping-validator--critic)
   - [UT-09 — Cypher Generator](#ut-09--cypher-generator)
   - [UT-10 — Cypher Healing Loop](#ut-10--cypher-healing-loop)
   - [UT-11 — Neo4j Client](#ut-11--neo4j-client)
   - [UT-12 — Hybrid Retrieval](#ut-12--hybrid-retrieval)
   - [UT-13 — Cross-Encoder Reranking](#ut-13--cross-encoder-reranking)
   - [UT-14 — Answer Generation](#ut-14--answer-generation)
   - [UT-15 — Hallucination Grader](#ut-15--hallucination-grader)
   - [UT-16 — Prompt Templates](#ut-16--prompt-templates)
   - [UT-17 — Schema Enrichment](#ut-17--schema-enrichment)
   - [UT-18 — Web Search Fallback](#ut-18--web-search-fallback)
4. [Integration Tests](#4-integration-tests)
   - [IT-01 — Builder Graph End-to-End (Small Schema)](#it-01--builder-graph-end-to-end-small-schema)
   - [IT-02 — Idempotency (Double Run)](#it-02--idempotency-double-run)
   - [IT-03 — Self-Reflection Loop (Mapping)](#it-03--self-reflection-loop-mapping)
   - [IT-04 — Cypher Healing Loop (Full)](#it-04--cypher-healing-loop-full)
   - [IT-05 — HITL Interrupt & Resume](#it-05--hitl-interrupt--resume)
   - [IT-06 — Query Graph End-to-End](#it-06--query-graph-end-to-end)
   - [IT-07 — Hallucination Grader Loop (Full)](#it-07--hallucination-grader-loop-full)
   - [IT-08 — Incremental Delta Update](#it-08--incremental-delta-update)
5. [RAGAS Evaluation Tests](#5-ragas-evaluation-tests)
6. [Test Fixtures & Mocks](#6-test-fixtures--mocks)
7. [CI Pipeline](#7-ci-pipeline)
8. [Test Coverage Targets](#8-test-coverage-targets)

---

## 1. Testing Philosophy

### 1.1 Core Principles

| Principle | Application |
|---|---|
| **Test nodes in isolation** | Every LangGraph node is a pure function (or near-pure). LLM and DB calls are always injectable — never hardcoded. |
| **Mock LLM calls in unit tests** | Never call a real LLM in a unit test. Use `unittest.mock.patch` or `pytest-mock` to return fixed JSON responses. |
| **Use real Neo4j for integration tests** | Integration tests run against a real Neo4j instance (Dockerised, cleaned between runs). |
| **Test the unhappy path first** | Self-reflection loops, healing, and fallback paths are the most critical — test them before happy paths. |
| **Property-based invariants** | Idempotency and MERGE semantics are tested with double-run assertions, not just single-run output checks. |

### 1.2 Test Naming Convention

```
test_{module}_{scenario}_{expected_outcome}

Examples:
test_extractor_valid_chunk_returns_triplets
test_extractor_empty_chunk_returns_empty_list
test_extractor_invalid_json_returns_empty_not_crash
test_cypher_generator_syntax_error_triggers_healing
test_builder_graph_double_run_graph_state_identical
```

### 1.3 Dependency Injection Pattern

All node functions must accept their dependencies as parameters (not import them globally) to enable easy mocking:

```python
# ✅ Correct — testable
def extract_triplets(chunk: Chunk, llm: BaseChatModel) -> list[Triplet]:
    ...

# ❌ Wrong — untestable without monkey-patching
def extract_triplets(chunk: Chunk) -> list[Triplet]:
    llm = ChatOpenRouter(...)  # hardcoded
    ...
```

---

## 2. Test Infrastructure

### 2.1 pytest Configuration (`pyproject.toml`)

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
markers = [
    "unit: pure unit tests with mocked dependencies",
    "integration: tests requiring real Neo4j + LLM",
    "slow: tests that take > 10 seconds",
    "ragas: RAGAS evaluation benchmark tests",
]
filterwarnings = ["ignore::DeprecationWarning"]

[tool.coverage.run]
source = ["src"]
omit = ["src/prompts/templates.py"]  # prompt strings don't need branch coverage

[tool.coverage.report]
fail_under = 80
```

### 2.2 Required Test Dependencies

```toml
[project.optional-dependencies]
test = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23",
    "pytest-mock>=3.12",
    "pytest-cov>=5.0",
    "testcontainers[neo4j]>=4.0",  # Dockerised Neo4j for integration tests
    "respx>=0.21",                  # HTTP mock for LLM API calls
    "faker>=25.0",                  # Synthetic data generation
]
```

### 2.3 Test Directory Structure

```
tests/
├── conftest.py                  # Shared fixtures (settings, mock LLM, Neo4j)
├── unit/
│   ├── test_settings.py
│   ├── test_pdf_loader.py
│   ├── test_ddl_parser.py
│   ├── test_triplet_extractor.py
│   ├── test_entity_resolver.py
│   ├── test_schema_enricher.py
│   ├── test_rag_mapper.py
│   ├── test_validator.py
│   ├── test_cypher_generator.py
│   ├── test_cypher_healer.py
│   ├── test_neo4j_client.py
│   ├── test_hybrid_retriever.py
│   ├── test_reranker.py
│   ├── test_answer_generator.py
│   ├── test_hallucination_grader.py
│   ├── test_prompts.py
│   └── test_web_search_fallback.py
├── integration/
│   ├── test_builder_graph.py
│   ├── test_query_graph.py
│   ├── test_cypher_healing.py
│   └── test_incremental_update.py
├── evaluation/
│   ├── test_ragas.py
│   └── test_ablation.py
└── fixtures/
    ├── sample_docs/
    │   ├── business_glossary.txt    # Plain text fixture (see DATASET.md §2.3)
    │   └── data_dictionary.txt
    ├── sample_ddl/
    │   ├── simple_schema.sql        # 3 tables, 1 FK
    │   ├── complex_schema.sql       # 9 tables (8 business + 1 system), multi-FK
    │   └── system_tables.sql        # 3 system tables, no business concept mappings
    ├── mock_responses/
    │   ├── extraction_response.json
    │   ├── er_judge_merge.json
    │   ├── er_judge_separate.json
    │   ├── mapping_high_confidence.json
    │   ├── mapping_null.json
    │   ├── critic_approved.json
    │   ├── critic_rejected.json
    │   ├── enrichment_response.json
    │   ├── grader_faithful.json
    │   ├── grader_hallucinated.json
    │   └── grader_web_search.json
    └── gold_standard.json           # See DATASET.md for full spec
```

### 2.4 Core Fixtures (`tests/conftest.py`)

```python
import pytest
from unittest.mock import MagicMock, AsyncMock
from testcontainers.neo4j import Neo4jContainer
from src.config.settings import Settings
from src.graph.neo4j_client import Neo4jClient

@pytest.fixture(scope="session")
def test_settings() -> Settings:
    """Override settings with test values — never reads from .env"""
    return Settings(
        neo4j_uri="bolt://localhost:7688",  # test port
        neo4j_user="neo4j",
        neo4j_password="test_password",
        openrouter_api_key="sk-or-test",
        llm_model_reasoning="test-model",
        llm_model_extraction="test-slm",
        embedding_model="BAAI/bge-m3",
        reranker_model="BAAI/bge-reranker-large",
    )

@pytest.fixture(scope="session")
def neo4j_container():
    """Spin up a real Neo4j Docker container for integration tests."""
    with Neo4jContainer("neo4j:5.18") as container:
        yield container

@pytest.fixture
def mock_llm():
    """Mock LLM that returns a fixed JSON string."""
    llm = MagicMock()
    llm.invoke = MagicMock()
    return llm

@pytest.fixture
def mock_embeddings():
    """Mock embeddings that return fixed 1024-dim vectors."""
    embedder = MagicMock()
    embedder.embed_documents = MagicMock(
        return_value=[[0.1] * 1024]
    )
    embedder.embed_query = MagicMock(
        return_value=[0.1] * 1024
    )
    return embedder
```

---

## 3. Unit Tests by Module

---

### UT-01 — Settings & Configuration

**File:** `tests/unit/test_settings.py`

| Test ID | Scenario | Expected |
|---|---|---|
| UT-01-01 | All required env vars present | `Settings` instantiates without error |
| UT-01-02 | Missing `NEO4J_PASSWORD` | `ValidationError` raised |
| UT-01-03 | `CONFIDENCE_THRESHOLD=1.5` (out of range) | `ValidationError` raised |
| UT-01-04 | `LLM_TEMPERATURE_EXTRACTION=0.5` | Value stored correctly |
| UT-01-05 | Settings is singleton | `settings is settings` (same object) |

```python
def test_settings_missing_password_raises():
    with pytest.raises(ValidationError):
        Settings(neo4j_uri="bolt://x", neo4j_user="u")  # no password

def test_settings_default_temperatures():
    s = Settings(_env_file=None, neo4j_uri="bolt://x", neo4j_user="u", neo4j_password="p",
                 openrouter_api_key="sk-or-test",
                 llm_model_reasoning="m", llm_model_extraction="s")
    assert s.llm_temperature_extraction == 0.0
    assert s.llm_temperature_generation == 0.3
```

---

### UT-02 — PDF Loader & Chunking

**File:** `tests/unit/test_pdf_loader.py`

| Test ID | Scenario | Expected |
|---|---|---|
| UT-02-01 | Valid PDF → `load_pdf()` | Returns `list[Document]` with non-empty text |
| UT-02-02 | Non-existent file path | Raises `IngestionError` |
| UT-02-03 | Valid documents → `chunk_documents()` | Returns `list[Chunk]`; each chunk ≤512 tokens |
| UT-02-04 | Chunk overlap | Consecutive chunks share ≤64 tokens at boundary |
| UT-02-05 | Chunk metadata | Each chunk has `source`, `page`, `chunk_index` in metadata |
| UT-02-06 | Single-sentence document | Returns exactly one chunk |

```python
def test_chunk_max_tokens():
    docs = [Document(text="word " * 600, metadata={"source": "test.pdf", "page": 1})]
    chunks = chunk_documents(docs)
    for chunk in chunks:
        token_count = len(tiktoken.get_encoding("cl100k_base").encode(chunk.text))
        assert token_count <= 512
```

---

### UT-03 — DDL Parser

**File:** `tests/unit/test_ddl_parser.py`

| Test ID | Scenario | Expected |
|---|---|---|
| UT-03-01 | Simple `CREATE TABLE` | Returns 1 `TableSchema` with correct column count |
| UT-03-02 | `CREATE TABLE` with FK | `ColumnSchema.is_foreign_key=True`, `references` populated |
| UT-03-03 | `CREATE TABLE` with PK | `ColumnSchema.is_primary_key=True` |
| UT-03-04 | Multi-table DDL | Returns N `TableSchema` objects |
| UT-03-05 | Invalid SQL | Raises `DDLParseError` |
| UT-03-06 | DDL with column comments | `ColumnSchema.comment` populated |
| UT-03-07 | T-SQL dialect (`NVARCHAR`, `IDENTITY`) | Parsed correctly |
| UT-03-08 | No LLM called | `mock_llm.invoke` never called |

```python
SIMPLE_DDL = """
CREATE TABLE CUSTOMER (
    CUST_ID INT PRIMARY KEY,
    NAME VARCHAR(200) NOT NULL,
    EMAIL VARCHAR(150)
);
"""

def test_parse_simple_ddl():
    tables = parse_ddl(SIMPLE_DDL)
    assert len(tables) == 1
    assert tables[0].table_name == "CUSTOMER"
    assert len(tables[0].columns) == 3
    pk_col = next(c for c in tables[0].columns if c.name == "CUST_ID")
    assert pk_col.is_primary_key is True

def test_parse_invalid_ddl_raises():
    with pytest.raises(DDLParseError):
        parse_ddl("THIS IS NOT SQL")
```

---

### UT-04 — Triplet Extraction

**File:** `tests/unit/test_triplet_extractor.py`

| Test ID | Scenario | Expected |
|---|---|---|
| UT-04-01 | Valid chunk + LLM returns valid JSON | Returns `list[Triplet]` matching schema |
| UT-04-02 | LLM returns invalid JSON | Returns `[]`, does NOT crash |
| UT-04-03 | LLM returns JSON missing `provenance_text` | Pydantic `ValidationError` caught, returns `[]` |
| UT-04-04 | Empty chunk text | Returns `[]` |
| UT-04-05 | Batch extraction | Processes N chunks, returns flat `list[Triplet]` |
| UT-04-06 | `confidence` > 1.0 in LLM response | Pydantic `ValidationError` caught, returns `[]` |
| UT-04-07 | LLM called with `temperature=0.0` | Verified via mock call args |
| UT-04-08 | Provenance verbatim | `triplet.provenance_text` appears in `chunk.text` |

```python
VALID_EXTRACTION_RESPONSE = json.dumps({
    "triplets": [{
        "subject": "Customer",
        "predicate": "purchases",
        "object": "Product",
        "provenance_text": "A Customer purchases a Product through the order system.",
        "confidence": 0.95
    }]
})

def test_extraction_valid_response(mock_llm):
    mock_llm.invoke.return_value.content = VALID_EXTRACTION_RESPONSE
    chunk = Chunk(text="A Customer purchases a Product through the order system.",
                  chunk_index=0, metadata={})
    triplets = extract_triplets(chunk, llm=mock_llm)
    assert len(triplets) == 1
    assert triplets[0].subject == "Customer"

def test_extraction_invalid_json_returns_empty(mock_llm):
    mock_llm.invoke.return_value.content = "NOT JSON AT ALL"
    chunk = Chunk(text="Some text.", chunk_index=0, metadata={})
    result = extract_triplets(chunk, llm=mock_llm)
    assert result == []
```

---

### UT-05 — Entity Resolution (Stage 1 — Blocking)

**File:** `tests/unit/test_entity_resolver.py`

| Test ID | Scenario | Expected |
|---|---|---|
| UT-05-01 | Identical strings | Grouped into 1 cluster |
| UT-05-02 | Semantically similar strings (mocked embeddings) | Grouped if cosine similarity ≥ threshold |
| UT-05-03 | Semantically dissimilar strings | Returned as separate clusters |
| UT-05-04 | Single entity | Returns 1 cluster with 1 variant |
| UT-05-05 | Empty input | Returns `[]` |
| UT-05-06 | Threshold boundary case | At exactly `er_similarity_threshold`, groups together |

```python
def test_blocking_similar_entities(mock_embeddings):
    # Mock embeddings: "Customer" and "Customers" → very similar vectors
    mock_embeddings.embed_documents.return_value = [
        [1.0] + [0.0] * 1023,    # "Customer"
        [0.99] + [0.01] * 1023,  # "Customers" — near-identical
        [0.0] + [1.0] * 1023,    # "Invoice" — different
    ]
    clusters = block_entities(["Customer", "Customers", "Invoice"], mock_embeddings)
    # Expect 2 clusters: {Customer, Customers} and {Invoice}
    assert len(clusters) == 2
```

---

### UT-06 — Entity Resolution (Stage 2 — LLM Judge)

**File:** `tests/unit/test_entity_resolver.py`

| Test ID | Scenario | Expected |
|---|---|---|
| UT-06-01 | LLM returns `merge=true` | All variants collapsed to `canonical_name` |
| UT-06-02 | LLM returns `merge=false` | Variants kept as distinct `Entity` objects |
| UT-06-03 | LLM returns invalid JSON | `ValidationError` caught; cluster treated as `merge=false` |
| UT-06-04 | Provenance injected | LLM prompt includes `provenance_json` for each variant |
| UT-06-05 | Single-variant cluster | LLM NOT called (no ambiguity to resolve) |

```python
def test_er_judge_merge(mock_llm):
    mock_llm.invoke.return_value.content = json.dumps({
        "merge": True, "canonical_name": "Customer", "reasoning": "Same concept."
    })
    cluster = EntityCluster(canonical_candidate="Customer",
                            variants=["Customer", "Customers", "CUST"],
                            avg_similarity=0.92)
    triplets = [Triplet(subject="Customer", predicate="has", object="Order",
                        provenance_text="A Customer has one or more Orders.", confidence=0.9)]
    entities = resolve_clusters([cluster], triplets, llm=mock_llm)
    assert len(entities) == 1
    assert entities[0].name == "Customer"
```

---

### UT-07 — RAG Mapping Node

**File:** `tests/unit/test_rag_mapper.py`

| Test ID | Scenario | Expected |
|---|---|---|
| UT-07-01 | Table + entities → high-confidence mapping | Returns `MappingProposal` with `confidence >= 0.9` |
| UT-07-02 | Table with no matching concept | Returns `MappingProposal` with `mapped_concept=None` |
| UT-07-03 | LLM returns invalid JSON | `ValidationError` caught; propagated as error for Actor-Critic |
| UT-07-04 | LLM called with `temperature=0.0` | Verified via mock call args |
| UT-07-05 | Few-shot examples injected | Prompt contains `few_shot_examples` content |
| UT-07-06 | Map-Reduce: 1 table per call | LLM called once per table (not once for all tables) |

---

### UT-08 — Mapping Validator & Critic

**File:** `tests/unit/test_validator.py`

| Test ID | Scenario | Expected |
|---|---|---|
| UT-08-01 | Valid proposal dict | Returns `(MappingProposal, None)` |
| UT-08-02 | Missing required field | Returns `(None, error_string)` |
| UT-08-03 | `confidence=1.5` (out of range) | Returns `(None, error_string)` |
| UT-08-04 | Critic approves valid mapping | Returns `CriticDecision(approved=True, critique=None)` |
| UT-08-05 | Critic rejects wrong mapping | Returns `CriticDecision(approved=False, critique="<specific text>")` |
| UT-08-06 | Critic critique is specific | `critique` string contains a column or concept name |
| UT-08-07 | Critic called with `temperature=0.0` | Verified via mock |

```python
def test_pydantic_validation_missing_field():
    bad_dict = {"table_name": "CUSTOMER"}  # missing mapped_concept, confidence, reasoning
    result, error = validate_schema(bad_dict)
    assert result is None
    assert error is not None
    assert "confidence" in error  # error names the missing field

def test_critic_critique_is_specific(mock_llm):
    mock_llm.invoke.return_value.content = json.dumps({
        "approved": False,
        "critique": "The mapped concept 'Customer' has purchase-focused definition, but table TB_PRODUCT has only product catalogue columns (PRODUCT_ID, SKU, CATEGORY_ID). Incompatible.",
        "suggested_correction": "Product"
    })
    proposal = MappingProposal(table_name="TB_PRODUCT", mapped_concept="Customer",
                               confidence=0.6, reasoning="Both relate to commerce.")
    decision = critic_review(proposal, table=mock_table, entities=[], llm=mock_llm)
    assert not decision.approved
    # Critique must name a specific column or concept
    assert any(name in decision.critique for name in ["TB_PRODUCT", "Customer", "PRODUCT_ID", "SKU"])
```

---

### UT-09 — Cypher Generator

**File:** `tests/unit/test_cypher_generator.py`

| Test ID | Scenario | Expected |
|---|---|---|
| UT-09-01 | Valid mapping → Cypher | Output string contains `MERGE`, `BusinessConcept`, `PhysicalTable`, `MAPPED_TO` |
| UT-09-02 | Cypher contains no bare `CREATE` | `re.search(r'^CREATE\b', cypher, re.MULTILINE)` returns None |
| UT-09-03 | All values parameterised | No string literals in Cypher (no single-quoted values) |
| UT-09-04 | Few-shot examples injected | `mock_llm.invoke` call args contain example content |
| UT-09-05 | Null-mapping table | Cypher contains only `PhysicalTable` MERGE, no `MAPPED_TO` |
| UT-09-06 | `temperature=0.0` | Verified via mock call args |

```python
def test_generated_cypher_uses_merge_not_create(mock_llm):
    mock_llm.invoke.return_value.content = VALID_CYPHER_WITH_MERGE
    cypher = generate_cypher(mock_mapping, mock_table, mock_entity, [], llm=mock_llm)
    assert "MERGE" in cypher
    # No bare CREATE (CREATE INDEX, CREATE CONSTRAINT allowed but not CREATE node/rel)
    bare_creates = re.findall(r'\bCREATE\s+\(', cypher)
    assert bare_creates == []

def test_generated_cypher_has_no_hardcoded_strings(mock_llm):
    mock_llm.invoke.return_value.content = VALID_CYPHER_WITH_MERGE
    cypher = generate_cypher(mock_mapping, mock_table, mock_entity, [], llm=mock_llm)
    # No single-quoted string literals (all values should be $params)
    string_literals = re.findall(r"'[^']*'", cypher)
    assert string_literals == []
```

---

### UT-10 — Cypher Healing Loop

**File:** `tests/unit/test_cypher_generator.py`

| Test ID | Scenario | Expected |
|---|---|---|
| UT-10-01 | First attempt succeeds | No healing call made |
| UT-10-02 | First attempt fails, second succeeds | `Fix_Cypher_LLM` called exactly once |
| UT-10-03 | All attempts fail | Returns `(None, cypher_failed=True)` after `max_healing_attempts` |
| UT-10-04 | Healing prompt contains original error | `REFLECTION_TEMPLATE` used with Neo4j exception string |
| UT-10-05 | Healing respects `max_cypher_healing_attempts` setting | Loop exits at correct count |

```python
def test_cypher_healing_max_retries(mock_llm, mock_neo4j):
    # LLM always returns broken Cypher
    mock_llm.invoke.return_value.content = "INVALID CYPHER"
    mock_neo4j.execute_cypher.side_effect = CypherSyntaxError("Syntax error")

    result, failed = cypher_generate_and_heal(
        mapping=mock_mapping, table=mock_table, entity=mock_entity,
        llm=mock_llm, client=mock_neo4j, max_attempts=3
    )
    assert failed is True
    assert mock_llm.invoke.call_count == 1 + 3  # 1 gen + 3 fix attempts
```

---

### UT-11 — Neo4j Client

**File:** `tests/unit/test_neo4j_client.py`

| Test ID | Scenario | Expected |
|---|---|---|
| UT-11-01 | Valid connection params | Client initialises without error |
| UT-11-02 | `execute_cypher` returns results | Returns `list[dict]` |
| UT-11-03 | `execute_batch` runs in one transaction | All statements in single `session.execute_write` call |
| UT-11-04 | `ServiceUnavailable` → auto-retry | Retries up to 3 times with backoff |
| UT-11-05 | Context manager `__exit__` | Driver session properly closed |
| UT-11-06 | `setup_schema` is idempotent | Running twice does not raise error |

---

### UT-12 — Hybrid Retrieval

**File:** `tests/unit/test_hybrid_retriever.py`

| Test ID | Scenario | Expected |
|---|---|---|
| UT-12-01 | `vector_search` returns `RetrievedChunk` list | `source_type="vector"` |
| UT-12-02 | `bm25_search` finds exact keyword | Returns chunk containing the keyword |
| UT-12-03 | `graph_traversal` expands to neighbours | Returns chunks with `source_type="graph"` |
| UT-12-04 | `merge_results` deduplicates by `node_id` | No duplicate `node_id` in merged output |
| UT-12-05 | `merge_results` keeps highest score | When same node from vector + BM25, keeps max score |
| UT-12-06 | Empty retrieval | Returns `[]`, does not crash |

---

### UT-13 — Cross-Encoder Reranking

**File:** `tests/unit/test_reranker.py`

| Test ID | Scenario | Expected |
|---|---|---|
| UT-13-01 | N chunks → Top-K output | Output length ≤ `settings.reranker_top_k` |
| UT-13-02 | Output sorted descending | `chunks[0].reranker_score >= chunks[-1].reranker_score` |
| UT-13-03 | `reranker_score` added to metadata | `chunk.reranker_score is not None` |
| UT-13-04 | Less than Top-K input | Returns all input chunks |
| UT-13-05 | Empty input | Returns `[]` |

---

### UT-14 — Answer Generation

**File:** `tests/unit/test_answer_generator.py`

| Test ID | Scenario | Expected |
|---|---|---|
| UT-14-01 | First attempt (no critique) | Uses `ANSWER_USER` template |
| UT-14-02 | Retry with critique | Uses `ANSWER_WITH_CRITIQUE_USER` template; critique text in prompt |
| UT-14-03 | Called with `temperature=0.3` | Verified via mock |
| UT-14-04 | `web_search_fallback` called | Returns string with `"[Source: Web Search]"` prefix |

---

### UT-15 — Hallucination Grader

**File:** `tests/unit/test_hallucination_grader.py`

| Test ID | Scenario | Expected |
|---|---|---|
| UT-15-01 | Grounded answer | Returns `GraderDecision(grounded=True, action="pass")` |
| UT-15-02 | Hallucinated entity | Returns `grounded=False`, `action="regenerate"`, `critique` names entity |
| UT-15-03 | Irrelevant context | Returns `action="web_search"` |
| UT-15-04 | LLM returns invalid JSON | Falls back to `GraderDecision(grounded=False, action="regenerate", critique="Grader error")` |
| UT-15-05 | Critique is specific | `critique` contains the name of a specific table or concept |
| UT-15-06 | Called with `temperature=0.0` | Verified via mock |

```python
def test_grader_hallucination_critique_is_specific(mock_llm):
    mock_llm.invoke.return_value.content = json.dumps({
        "grounded": False,
        "critique": "Table TB_ORDERS is not mentioned in any retrieved context chunk. Reformulate omitting TB_ORDERS.",
        "action": "regenerate"
    })
    decision = grade_answer("What orders exist?", "TB_ORDERS has 5M records.", [], llm=mock_llm)
    assert not decision.grounded
    assert "TB_ORDERS" in decision.critique
```

---

### UT-16 — Prompt Templates

**File:** `tests/unit/test_prompts.py`

| Test ID | Scenario | Expected |
|---|---|---|
| UT-16-01 | `EXTRACTION_SYSTEM` imported | Is a non-empty string |
| UT-16-02 | `REFLECTION_TEMPLATE.format(...)` | All `{placeholders}` resolved without `KeyError` |
| UT-16-03 | No prompt contains hardcoded model names | None of the templates contain "gpt-4o", "qwen", etc. |
| UT-16-04 | All templates have output constraint clause | Each system prompt contains "Output ONLY valid JSON" or equivalent |

```python
def test_all_system_prompts_have_output_constraint():
    system_prompts = [EXTRACTION_SYSTEM, ER_JUDGE_SYSTEM, MAPPING_SYSTEM,
                      CRITIC_SYSTEM, CYPHER_SYSTEM, ANSWER_SYSTEM, GRADER_SYSTEM,
                      ENRICHMENT_SYSTEM]
    for prompt in system_prompts:
        assert "Output ONLY" in prompt or "Return only" in prompt, \
            f"Missing output constraint in prompt: {prompt[:80]}..."
```

---

### UT-17 — Schema Enrichment

**File:** `tests/unit/test_schema_enricher.py`

| Test ID | Scenario | Expected |
|---|---|---|
| UT-17-01 | Abbreviated table name (`TB_CST`) | Returns enriched name `"Customer Table"` |
| UT-17-02 | Already readable name (`CUSTOMER_MASTER`) | Returns name unchanged or trivially reformatted |
| UT-17-03 | Abbreviated column names (`CUST_ID`, `ORD_DT`) | Each column gets a human-readable alias |
| UT-17-04 | LLM returns valid JSON | Output validates against `EnrichedTableSchema` Pydantic model |
| UT-17-05 | LLM returns invalid JSON | `ValidationError` caught; original `TableSchema` passed through unenriched (does not crash) |
| UT-17-06 | `temperature=0.0` | Verified via mock call args |
| UT-17-07 | Enrichment preserves original fields | `table_name`, `columns`, `ddl_source` unchanged on enriched output |
| UT-17-08 | Batch enrichment | Processing N tables returns N enriched results |

```python
VALID_ENRICHMENT_RESPONSE = json.dumps({
    "enriched_table_name": "Customer Table",
    "enriched_columns": [
        {"original": "CUST_ID", "enriched": "Customer ID"},
        {"original": "FULL_NAME", "enriched": "Full Name"},
        {"original": "REGION_CODE", "enriched": "Region Code"}
    ],
    "table_description": "Master record for all registered platform customers."
})

def test_enrichment_abbreviated_table(mock_llm):
    mock_llm.invoke.return_value.content = VALID_ENRICHMENT_RESPONSE
    table = TableSchema(table_name="TB_CST", columns=[
        ColumnSchema(name="CUST_ID", data_type="INT", is_primary_key=True),
    ], ddl_source="CREATE TABLE TB_CST (CUST_ID INT PRIMARY KEY)")
    result = enrich_schema(table, llm=mock_llm)
    assert result.enriched_table_name is not None
    assert result.table_name == "TB_CST"  # original preserved

def test_enrichment_invalid_json_falls_through(mock_llm):
    mock_llm.invoke.return_value.content = "NOT VALID JSON"
    table = TableSchema(table_name="TB_CST", columns=[], ddl_source="...")
    result = enrich_schema(table, llm=mock_llm)
    assert result.enriched_table_name is None  # unenriched fallback
```

---

### UT-18 — Web Search Fallback

**File:** `tests/unit/test_web_search_fallback.py`

| Test ID | Scenario | Expected |
|---|---|---|
| UT-18-01 | Web search returns result | Output string starts with `"[Source: Web Search]"` |
| UT-18-02 | Web search raises exception | Falls back to `"I cannot answer this question."` message |
| UT-18-03 | Web search tool is injectable | Function accepts search tool as dependency parameter |

```python
def test_web_search_fallback_prefix(mock_search_tool):
    mock_search_tool.invoke.return_value = "Neo4j is a graph database."
    result = web_search_fallback("What is Neo4j?", search_tool=mock_search_tool)
    assert result.startswith("[Source: Web Search]")

def test_web_search_fallback_error_handling(mock_search_tool):
    mock_search_tool.invoke.side_effect = Exception("API unavailable")
    result = web_search_fallback("What is Neo4j?", search_tool=mock_search_tool)
    assert "cannot answer" in result.lower()
```

---

## 4. Integration Tests

All integration tests require:
- Real Neo4j container (via `testcontainers[neo4j]`)
- Mock LLM (never real API calls in automated tests)
- `pytest.mark.integration`

---

### IT-01 — Builder Graph End-to-End (Small Schema)

**File:** `tests/integration/test_builder_graph.py`
**Fixtures:** `simple_schema.sql` + `business_glossary.pdf` (or mock text)

**Test scenario:**
1. Invoke `builder_graph` with 3-table schema + matching business doc
2. Assert Knowledge Graph contains expected nodes and relationships

```python
@pytest.mark.integration
def test_builder_graph_creates_expected_nodes(neo4j_container, mock_llm_sequence):
    """
    mock_llm_sequence: a mock LLM that returns pre-defined responses in order
    (extraction → ER → mapping → validation → cypher)
    """
    graph = build_builder_graph(llm=mock_llm_sequence, settings=test_settings)
    result = graph.invoke({"raw_documents": SAMPLE_DOCS, "ddl_statements": SIMPLE_DDL})

    client = Neo4jClient(test_settings)
    with client:
        concepts = client.execute_cypher("MATCH (n:BusinessConcept) RETURN n.name AS name", {})
        tables = client.execute_cypher("MATCH (n:PhysicalTable) RETURN n.table_name AS name", {})
        mappings = client.execute_cypher("MATCH ()-[r:MAPPED_TO]->() RETURN count(r) AS cnt", {})

    concept_names = {r["name"] for r in concepts}
    assert "Customer" in concept_names
    assert "CUSTOMER_MASTER" in {r["name"] for r in tables}
    assert mappings[0]["cnt"] >= 1
```

---

### IT-02 — Idempotency (Double Run)

**File:** `tests/integration/test_builder_graph.py`

```python
@pytest.mark.integration
def test_builder_graph_double_run_idempotent(neo4j_container, mock_llm_sequence):
    """Running the Builder twice on the same input must produce identical graph state."""
    graph = build_builder_graph(llm=mock_llm_sequence, settings=test_settings)

    graph.invoke({"raw_documents": SAMPLE_DOCS, "ddl_statements": SIMPLE_DDL})
    snapshot_1 = get_graph_snapshot(neo4j_container)

    graph.invoke({"raw_documents": SAMPLE_DOCS, "ddl_statements": SIMPLE_DDL})
    snapshot_2 = get_graph_snapshot(neo4j_container)

    assert snapshot_1["node_count"] == snapshot_2["node_count"]
    assert snapshot_1["edge_count"] == snapshot_2["edge_count"]
    assert snapshot_1["concept_names"] == snapshot_2["concept_names"]
```

---

### IT-03 — Self-Reflection Loop (Mapping)

```python
@pytest.mark.integration
def test_mapping_reflection_loop_recovers(neo4j_container):
    """
    LLM Actor returns invalid JSON on attempt 1, valid JSON on attempt 2.
    Assert: graph still built correctly; reflection_attempts == 1 in final state.
    """
    responses = [
        "NOT VALID JSON",                  # attempt 1: fails
        json.dumps(VALID_MAPPING_RESPONSE) # attempt 2: succeeds
    ]
    mock_llm = MockSequenceLLM(responses)
    graph = build_builder_graph(llm=mock_llm, settings=test_settings)
    final_state = graph.invoke({"raw_documents": SAMPLE_DOCS, "ddl_statements": SIMPLE_DDL})

    assert final_state["reflection_attempts"] == 1
    assert final_state["failed_mappings"] == []
```

---

### IT-04 — Cypher Healing Loop (Full)

```python
@pytest.mark.integration
def test_cypher_healing_succeeds_on_second_attempt(neo4j_container):
    """Broken Cypher on attempt 1 → healed Cypher on attempt 2 → graph updated."""
    cypher_responses = [BROKEN_CYPHER, VALID_CYPHER]
    mock_llm = MockSequenceLLM(pre_mapping_responses + cypher_responses)
    graph = build_builder_graph(llm=mock_llm, settings=test_settings)
    final_state = graph.invoke({"raw_documents": SAMPLE_DOCS, "ddl_statements": SIMPLE_DDL})

    assert final_state["healing_attempts"] == 1
    assert final_state["failed_mappings"] == []
```

---

### IT-05 — HITL Interrupt & Resume

```python
@pytest.mark.integration
def test_hitl_interrupt_and_resume(neo4j_container):
    """
    Low-confidence mapping triggers HITL.
    Human provides correction.
    Graph resumes and commits the human-corrected mapping.
    """
    # First: low-confidence mapping response
    mock_llm = MockLLM(response=LOW_CONFIDENCE_MAPPING_RESPONSE)
    graph = build_builder_graph(llm=mock_llm, settings=test_settings, checkpointer=MemorySaver())
    thread_id = {"configurable": {"thread_id": "test-hitl-1"}}

    # Run until interrupt
    for event in graph.stream({"raw_documents": SAMPLE_DOCS, "ddl_statements": SIMPLE_DDL}, thread_id):
        if "__interrupt__" in event:
            break

    # Simulate human approval with correction
    graph.invoke(Command(resume={"action": "correct", "mapped_concept": "CustomerAccount"}), thread_id)

    # Verify the human-corrected concept is in the graph
    client = Neo4jClient(test_settings)
    with client:
        result = client.execute_cypher(
            "MATCH (n:BusinessConcept {name: 'CustomerAccount'}) RETURN n", {}
        )
    assert len(result) == 1
```

---

### IT-06 — Query Graph End-to-End

```python
@pytest.mark.integration
def test_query_graph_returns_grounded_answer(neo4j_container):
    """
    Pre-populated graph + valid user query → grounded final answer.
    """
    populate_test_graph(neo4j_container)  # insert known nodes

    mock_llm = MockLLM(responses=[VALID_ANSWER, GRADER_PASS_RESPONSE])
    graph = build_query_graph(llm=mock_llm, settings=test_settings)
    result = graph.invoke({"user_query": "Which table stores customer data?"})

    assert result["final_answer"] != ""
    assert "[Source: Web Search]" not in result["final_answer"]
    assert result["sources"] != []
```

---

### IT-07 — Hallucination Grader Loop (Full)

```python
@pytest.mark.integration
def test_hallucination_loop_max_retries_triggers_web_search(neo4j_container):
    """
    Grader always returns hallucination detected.
    After max_hallucination_retries, pipeline falls back to web search.
    """
    mock_llm = MockLLM(responses=[
        "Answer with hallucination",        # gen attempt 1
        json.dumps(GRADER_HALLUCINATION),   # grader 1
        "Another hallucination",            # gen attempt 2
        json.dumps(GRADER_HALLUCINATION),   # grader 2
        "Third hallucination",              # gen attempt 3
        json.dumps(GRADER_HALLUCINATION),   # grader 3 → triggers web_search
        "Web search result",                # web fallback
    ])
    graph = build_query_graph(llm=mock_llm, settings=test_settings)
    result = graph.invoke({"user_query": "What is the schema of TB_UNKNOWN?"})

    assert "[Source: Web Search]" in result["final_answer"]
```

---

### IT-08 — Incremental Delta Update

```python
@pytest.mark.integration
def test_delta_update_adds_without_replacing(neo4j_container):
    """
    After initial ingestion, adding a new table DDL must:
    - Add the new table node
    - Not delete or duplicate existing nodes
    """
    # Initial run
    graph.invoke({"ddl_statements": [TABLE_A_DDL], "raw_documents": DOCS})
    count_before = get_node_count(neo4j_container)

    # Delta run: add TABLE_B only
    graph.invoke({"ddl_statements": [TABLE_B_DDL], "raw_documents": []})
    count_after = get_node_count(neo4j_container)

    assert count_after > count_before                  # new node added
    assert is_node_present("TABLE_A", neo4j_container) # original not deleted
    assert is_node_present("TABLE_B", neo4j_container) # new node present
```

---

## 5. RAGAS Evaluation Tests

**File:** `tests/evaluation/test_ragas.py`
**Markers:** `pytest.mark.ragas`, `pytest.mark.slow`

These tests run against a **real LLM** and a **real Neo4j** instance. They are excluded from the standard CI pipeline and run separately as part of the monthly evaluation milestone.

```python
@pytest.mark.ragas
@pytest.mark.slow
def test_ragas_faithfulness_above_threshold(live_neo4j, live_llm):
    """Faithfulness metric must be >= 0.95 on the gold standard dataset."""
    report = run_evaluation(gold_standard_dataset, build_query_graph(live_llm))
    assert report.faithfulness >= 0.95, \
        f"Faithfulness {report.faithfulness:.3f} below target 0.95"

@pytest.mark.ragas
@pytest.mark.slow
def test_ragas_context_precision_above_threshold(live_neo4j, live_llm):
    assert report.context_precision >= 0.85

@pytest.mark.ragas
@pytest.mark.slow
def test_ragas_context_recall_above_threshold(live_neo4j, live_llm):
    assert report.context_recall >= 0.90

@pytest.mark.ragas
@pytest.mark.slow
def test_cypher_healing_rate_above_threshold(live_neo4j, live_llm):
    assert report.cypher_healing_rate >= 0.80
```

---

## 6. Test Fixtures & Mocks

### 6.1 Mock LLM Responses

All mock response files are in `tests/fixtures/mock_responses/`. The agent must create these as JSON files:

**`extraction_response.json`:**
```json
{
  "triplets": [
    {
      "subject": "Customer",
      "predicate": "places",
      "object": "SalesOrder",
      "provenance_text": "A Customer places one or more SalesOrders through the e-commerce portal.",
      "confidence": 0.95
    },
    {
      "subject": "SalesOrder",
      "predicate": "contains",
      "object": "OrderLineItem",
      "provenance_text": "Each SalesOrder contains one or more OrderLineItems, each referring to a Product.",
      "confidence": 0.93
    }
  ]
}
```

**`mapping_high_confidence.json`:**
```json
{
  "table_name": "CUSTOMER_MASTER",
  "mapped_concept": "Customer",
  "confidence": 0.97,
  "reasoning": "The CUSTOMER_MASTER table stores individual customer identity and contact data (CUST_ID, FULL_NAME, EMAIL, REGION_CODE), directly matching the Customer business concept definition which describes entities that purchase goods or services.",
  "alternative_concepts": []
}
```

**`mapping_null.json`:**
```json
{
  "table_name": "SYS_AUDIT_LOG",
  "mapped_concept": null,
  "confidence": 0.0,
  "reasoning": "This is a system-level audit log table recording database change events. It has no corresponding business concept in the glossary.",
  "alternative_concepts": []
}
```

**`grader_pass.json`:**
```json
{
  "grounded": true,
  "critique": null,
  "action": "pass"
}
```

**`grader_hallucination.json`:**
```json
{
  "grounded": false,
  "critique": "Table TB_ORDERS is not mentioned in any of the retrieved context chunks. The answer claims TB_ORDERS has 5 million records, but this information is not present in the context. Reformulate the answer omitting TB_ORDERS.",
  "action": "regenerate"
}
```

### 6.2 Sample DDL Fixtures

**`tests/fixtures/sample_ddl/simple_schema.sql`** — 3-table schema used in most unit tests:

```sql
CREATE TABLE CUSTOMER_MASTER (
    CUST_ID     INT PRIMARY KEY,
    FULL_NAME   VARCHAR(200) NOT NULL,
    EMAIL       VARCHAR(150),
    REGION_CODE VARCHAR(10)
);

CREATE TABLE TB_PRODUCT (
    PRODUCT_ID   INT PRIMARY KEY,
    SKU          VARCHAR(50) UNIQUE NOT NULL,
    PRODUCT_NAME VARCHAR(300),
    UNIT_PRICE   DECIMAL(10,2),
    IS_ACTIVE    BOOLEAN DEFAULT TRUE
);

CREATE TABLE SALES_ORDER_HDR (
    ORDER_ID    BIGINT PRIMARY KEY,
    CUST_ID     INT NOT NULL REFERENCES CUSTOMER_MASTER(CUST_ID),
    ORDER_DATE  DATE NOT NULL,
    TOTAL_AMT   DECIMAL(12,2),
    STATUS_CODE VARCHAR(20)
);
```

---

## 7. CI Pipeline

### 7.1 GitHub Actions (`/.github/workflows/test.yml`)

```yaml
name: Tests

on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install -e ".[test]"
      - run: pytest tests/unit -m unit --cov=src --cov-report=xml -v

  integration-tests:
    runs-on: ubuntu-latest
    services:
      neo4j:
        image: neo4j:5.18
        env:
          NEO4J_AUTH: neo4j/test_password
        ports: ["7687:7687"]
    steps:
      - uses: actions/checkout@v4
      - run: pip install -e ".[test]"
      - run: pytest tests/integration -m integration -v
        env:
          NEO4J_URI: bolt://localhost:7687
          NEO4J_PASSWORD: test_password

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install ruff mypy
      - run: ruff check .
      - run: mypy src --strict
```

---

## 8. Test Coverage Targets

| Module | Unit Coverage Target | Notes |
|---|---|---|
| `src/config/settings.py` | 90% | Critical config |
| `src/ingestion/` | 85% | PDF + DDL + Schema Enrichment |
| `src/extraction/` | 90% | LLM node — unhappy paths critical |
| `src/resolution/` | 85% | 2-stage ER |
| `src/mapping/` | 90% | Actor-Critic loop |
| `src/graph/cypher_generator.py` | 90% | Healing loop |
| `src/graph/neo4j_client.py` | 80% | DB client |
| `src/retrieval/` | 85% | Hybrid retrieval |
| `src/generation/` | 90% | Grader loop |
| `src/prompts/templates.py` | 60% | String constants |
| **Overall** | **80%** | Enforced by `--cov-fail-under=80` |
