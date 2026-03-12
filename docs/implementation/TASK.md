# Implementation Task List

> **Project:** Multi-Agent Framework for Semantic Discovery & GraphRAG  
> **Author:** Marc'Antonio Lopez  
> **Status:** Phase 1 in progress — TASK-01 completed.  
> **Last updated:** March 2026

Follow the tasks in the numbered order below. Each task lists its prerequisites, the file(s) to implement, the corresponding test file(s), and the documentation references to anchor the implementation.

---

## Table of Contents

- [Part 1 — Infrastructure & Configuration](#part-1--infrastructure--configuration)
- [Part 2 — Data Models & Prompts](#part-2--data-models--prompts)
- [Part 3 — Ingestion](#part-3--ingestion)
- [Part 4 — Extraction & Entity Resolution](#part-4--extraction--entity-resolution)
- [Part 5 — Semantic Mapping](#part-5--semantic-mapping)
- [Part 6 — Graph & Cypher](#part-6--graph--cypher)
- [Part 7 — Retrieval](#part-7--retrieval)
- [Part 8 — Generation & Query Graph](#part-8--generation--query-graph)
- [Part 9 — Evaluation](#part-9--evaluation)
- [Test Fixtures & Conftest](#test-fixtures--conftest)

---

## Part 1 — Infrastructure & Configuration

---

### [DONE] TASK-01 — `pyproject.toml` + `.env.example`

**Epic:** EP-01 · **Priority:** P0 · **Prerequisites:** none

Populate `pyproject.toml` with all direct and dev dependencies (PEP 621 format). Verify that `.env.example` documents every environment variable with a safe placeholder. Add `[tool.pytest.ini_options]`, `[tool.ruff]`, and `[tool.coverage]` sections.

**File(s) to implement:**
- `pyproject.toml`
- `.env.example`

**Test file(s):** _(no automated tests — verified by `pip install -e .[test]` succeeding cleanly)_

**Documentation references:**
- `docs/implementation/part-1-infrastructure/01-pyproject.md` — full `pyproject.toml` and `.env.example` content
- `docs/draft/REQUIREMENTS.md` §EP-01 / US-01-01 — dependency table and version constraints

---

### [DONE] TASK-02 — `src/config/settings.py`

**Epic:** EP-01 · **Priority:** P0 · **Prerequisites:** TASK-01

Implement the `Settings` class using `pydantic_settings.BaseSettings`. Expose a `get_settings()` cached factory and a module-level `settings` singleton. Every configurable parameter (Neo4j URI, LLM model slugs, thresholds, chunking sizes, retrieval K values, ablation flags) must be a typed field.

**File(s) to implement:**
- `src/config/settings.py`

**Test file(s):**
- `tests/unit/test_settings.py` (UT-01)

**Documentation references:**
- `docs/implementation/part-1-infrastructure/02-settings.md` — full class definition with all fields
- `docs/draft/REQUIREMENTS.md` §EP-01 / US-01-02 — `Settings` field list and `model_config`
- `docs/draft/SPECS.md` §3.3 — temperature strategy and threshold values

---

### [DONE] TASK-03 — `src/config/logging.py`

**Epic:** EP-01 · **Priority:** P0 · **Prerequisites:** TASK-02

Configure structured JSON logging using `python-json-logger`. Every LangGraph node must log `node_name`, `input_summary`, `output_summary`, `duration_ms`, and `model_used`. Reflection/retry events log `attempt_number`, `error_injected`, and `correction_applied`. Log level controlled by `LOG_LEVEL` env var.

**File(s) to implement:**
- `src/config/logging.py`

**Test file(s):** _(verified by presence of structured JSON in stderr during integration tests)_

**Documentation references:**
- `docs/implementation/part-1-infrastructure/03-logging.md` — full logging setup
- `docs/draft/REQUIREMENTS.md` §EP-01 / US-01-03

---

### [DONE] TASK-04 — `src/config/llm_factory.py`

**Epic:** EP-01 · **Priority:** P0 · **Prerequisites:** TASK-02, TASK-03

Implement the factory that returns the correct `BaseChatModel` instance based on `settings.llm_model_reasoning` or `settings.llm_model_extraction`. Wraps the model in `InstrumentedLLM` (see TASK-04b). Provides three factory functions: `get_reasoning_llm()`, `get_extraction_llm()`, `get_generation_llm()`.

**File(s) to implement:**
- `src/config/llm_factory.py`

**Test file(s):** _(tested indirectly via unit tests that inject mock LLMs)_

**Documentation references:**
- `docs/implementation/part-1-infrastructure/04-llm-factory.md` — factory functions and provider switching logic

---

### [DONE] TASK-04b — `src/config/llm_client.py`

**Epic:** EP-01 · **Priority:** P0 · **Prerequisites:** TASK-04

Implement `LLMProtocol` (structural `typing.Protocol` satisfied by any `BaseChatModel`) and `InstrumentedLLM` (concrete wrapper adding retry with exponential backoff, token-usage logging, and latency measurement).

**File(s) to implement:**
- `src/config/llm_client.py`

**Test file(s):** _(covered by `test_settings.py` and node-level unit tests)_

**Documentation references:**
- `docs/implementation/part-1-infrastructure/04b-llm-client.md` — `LLMProtocol` definition and `InstrumentedLLM` wrapper

---

## Part 2 — Data Models & Prompts

---

### [DONE] TASK-05 — `src/models/schemas.py`

**Epic:** EP-06 data models · **Priority:** P0 · **Prerequisites:** TASK-01

Define all Pydantic v2 data models used across the pipeline: `Triplet`, `TripletExtractionResponse`, `Entity`, `EntityCluster`, `TableSchema`, `EnrichedTableSchema`, `Mapping`, `MappingProposal`, `CriticReview`, `HallucinationGrade`, `Chunk`, `Document`.

**File(s) to implement:**
- `src/models/schemas.py`

**Test file(s):** _(schema correctness tested in all node-level unit tests that call `model_validate_json`)_

**Documentation references:**
- `docs/implementation/part-2-models-prompts/05-schemas.md` — full Pydantic model definitions
- `docs/draft/REQUIREMENTS.md` §6 — Data Models & Schemas
- `docs/draft/SPECS.md` §3.3 — `BuilderState` / `QueryState` field types

---

### [DONE] TASK-06 — `src/models/state.py`

**Epic:** EP-11, EP-15 · **Priority:** P0 · **Prerequisites:** TASK-05

Implement `BuilderState` and `QueryState` as `TypedDict` subclasses for LangGraph. Every field must match the type annotations in SPECS.md §3.3 and the node input/output contracts in §4.2.

**File(s) to implement:**
- `src/models/state.py`

**Test file(s):** _(verified structurally at graph compilation time in integration tests)_

**Documentation references:**
- `docs/implementation/part-2-models-prompts/06-state.md` — full `TypedDict` definitions
- `docs/draft/SPECS.md` §3.3 — state schema with all fields and comments

---

### TASK-07 — `src/prompts/templates.py` [DONE]

**Epic:** prompting · **Priority:** P0 · **Prerequisites:** TASK-05

Implement all prompt template constants (PT-01 through PT-11) as Python string constants with `{variable_name}` placeholders. Constants: `EXTRACTION_SYSTEM`, `EXTRACTION_USER`, `ER_JUDGE_SYSTEM`, `ER_JUDGE_USER`, `MAPPING_SYSTEM`, `MAPPING_USER`, `CRITIC_SYSTEM`, `CRITIC_USER`, `REFLECTION_TEMPLATE`, `CYPHER_SYSTEM`, `CYPHER_USER`, `CYPHER_FIX_USER`, `ANSWER_SYSTEM`, `ANSWER_USER`, `ANSWER_WITH_CRITIQUE_USER`, `GRADER_SYSTEM`, `GRADER_USER`, `ENRICHMENT_SYSTEM`, `ENRICHMENT_USER`.

**File(s) to implement:**
- `src/prompts/templates.py`

**Test file(s):**
- `tests/unit/test_prompts.py` (UT-16)

**Documentation references:**
- `docs/implementation/part-2-models-prompts/07-templates.md` — verbatim prompt text for all templates
- `docs/draft/PROMPTS.md` §3 — complete PT-01–PT-11 definitions
- `docs/draft/SPECS.md` §6.1 — per-node persona and technique table

---

### TASK-08 — `src/prompts/few_shot.py` [DONE]

**Epic:** EP-06, EP-09 · **Priority:** P0 · **Prerequisites:** TASK-07

Implement `load_cypher_examples()` and `load_mapping_examples()` that read `src/data/few_shot_cypher.json` and `src/data/few_shot_mapping.json` respectively. Implement `format_cypher_few_shot(n: int) -> str` that formats the top-n examples into the prompt template block used by `Generate_Cypher`.

**File(s) to implement:**
- `src/prompts/few_shot.py`

**Test file(s):**
- `tests/unit/test_prompts.py` (UT-16)

**Documentation references:**
- `docs/implementation/part-2-models-prompts/08-few-shot.md` — loader and formatter logic
- `docs/draft/SPECS.md` §6.2 — few-shot template format
- `docs/draft/PROMPTS.md` §4 — FEW-01 and FEW-02 example banks

---

## Part 3 — Ingestion

---

### TASK-09 — `src/ingestion/pdf_loader.py` [DONE]

**Epic:** EP-02 · **Priority:** P0 · **Prerequisites:** TASK-05, TASK-06

Implement `load_pdf(path: Path) -> list[Document]` using `pymupdf` (fitz). Implement `chunk_documents(docs: list[Document]) -> list[Chunk]` using `RecursiveCharacterTextSplitter` with `chunk_size=settings.chunk_size` and `chunk_overlap=settings.chunk_overlap`. Each chunk must carry `source`, `page`, and `chunk_index` metadata.

**File(s) to implement:**
- `src/ingestion/pdf_loader.py`

**Test file(s):**
- `tests/unit/test_pdf_loader.py` (UT-02)

**Documentation references:**
- `docs/implementation/part-3-ingestion/09-pdf-loader.md` — full implementation with chunker
- `docs/draft/REQUIREMENTS.md` §EP-02 / US-02-01, US-02-02

---

### TASK-10 — `src/ingestion/ddl_parser.py` [DONE]

**Epic:** EP-05 · **Priority:** P0 · **Prerequisites:** TASK-05

Implement `parse_ddl(sql: str) -> list[TableSchema]` using `sqlglot`. Each `TableSchema` must contain `table_name`, `schema_name`, `column_names`, `column_types`, and `ddl_source` (the raw DDL fragment). System tables (e.g., audit/log tables) must be detectable via a naming heuristic.

**File(s) to implement:**
- `src/ingestion/ddl_parser.py`

**Test file(s):**
- `tests/unit/test_ddl_parser.py` (UT-03)

**Documentation references:**
- `docs/implementation/part-3-ingestion/10-ddl-parser.md` — sqlglot parsing logic with system-table detection
- `docs/draft/REQUIREMENTS.md` §EP-05
- `docs/draft/DATASET.md` §3 — DDL fixture schemas for `simple_schema.sql` and `complex_schema.sql`

---

### TASK-11 — `src/ingestion/schema_enricher.py` [DONE]

**Epic:** EP-05b · **Priority:** P0 · **Prerequisites:** TASK-07, TASK-10

Implement `enrich_schema(tables: list[TableSchema], llm) -> list[EnrichedTableSchema]` using the `ENRICHMENT_SYSTEM` / `ENRICHMENT_USER` prompt templates. Expands abbreviated table/column names (e.g., `TB_CST` → `"Customer Table"`) and adds natural-language descriptions. Validates output with Pydantic; falls back to raw identifier on validation failure.

**File(s) to implement:**
- `src/ingestion/schema_enricher.py`

**Test file(s):**
- `tests/unit/test_schema_enricher.py` (UT-17)

**Documentation references:**
- `docs/implementation/part-3-ingestion/11-schema-enricher.md` — enrichment node implementation
- `docs/draft/SPECS.md` §4.2 — `LLM_Schema_Enrichment` node spec
- `docs/draft/PROMPTS.md` §3 / PT-11 — `ENRICHMENT_SYSTEM` and `ENRICHMENT_USER` templates

---

## Part 4 — Extraction & Entity Resolution

---

### TASK-12 — `src/extraction/triplet_extractor.py` [DONE]

**Epic:** EP-03 · **Priority:** P0 · **Prerequisites:** TASK-05, TASK-07, TASK-09

Implement `extract_triplets(chunk: Chunk, llm) -> list[Triplet]` using the SLM in JSON Mode with `EXTRACTION_SYSTEM` / `EXTRACTION_USER`. Enforce Pydantic validation on output; return empty list (not raise) on `ValidationError`. Implement batch variant `extract_all(chunks: list[Chunk], llm) -> list[Triplet]`.

**File(s) to implement:**
- `src/extraction/triplet_extractor.py`

**Test file(s):**
- `tests/unit/test_triplet_extractor.py` (UT-04)

**Documentation references:**
- `docs/implementation/part-4-extraction-er/12-triplet-extractor.md` — full node implementation
- `docs/draft/REQUIREMENTS.md` §EP-03 / US-03-01 — Pydantic schema, persona, temperature
- `docs/draft/PROMPTS.md` §3 / PT-01 — `EXTRACTION_SYSTEM` and `EXTRACTION_USER`
- `docs/draft/SPECS.md` §4.2 — `Extract_Triplets_SLM` node spec

---

### TASK-13 — `src/resolution/blocking.py` [DONE]

**Epic:** EP-04 Stage 1 · **Priority:** P0 · **Prerequisites:** TASK-05, TASK-12

Implement `block_entities(entities: list[str], embeddings) -> list[EntityCluster]`. Embed all unique entity strings with BGE-M3. Group pairs with cosine similarity ≥ `settings.er_similarity_threshold` using K-NN (`faiss` or `sklearn.NearestNeighbors`, `k = settings.er_blocking_top_k`). Returns clusters of candidate duplicates for LLM judging.

**File(s) to implement:**
- `src/resolution/blocking.py`

**Test file(s):**
- `tests/unit/test_entity_resolver.py` (UT-05)

**Documentation references:**
- `docs/implementation/part-4-extraction-er/13-blocking.md` — K-NN blocking logic
- `docs/draft/REQUIREMENTS.md` §EP-04 / US-04-01

---

### TASK-14 — `src/resolution/llm_judge.py` [DONE]

**Epic:** EP-04 Stage 2 · **Priority:** P0 · **Prerequisites:** TASK-07, TASK-13

Implement `judge_cluster(cluster: EntityCluster, llm) -> EntityResolutionDecision` using `ER_JUDGE_SYSTEM` / `ER_JUDGE_USER`. The LLM decides whether to merge the cluster into one canonical entity or keep variants separate. Response validated with Pydantic.

**File(s) to implement:**
- `src/resolution/llm_judge.py`

**Test file(s):**
- `tests/unit/test_entity_resolver.py` (UT-06)

**Documentation references:**
- `docs/implementation/part-4-extraction-er/14-llm-judge.md` — judge logic and response parsing
- `docs/draft/PROMPTS.md` §3 / PT-02 — `ER_JUDGE_SYSTEM` and `ER_JUDGE_USER`

---

### TASK-15 — `src/resolution/entity_resolver.py` [DONE]

**Epic:** EP-04 · **Priority:** P0 · **Prerequisites:** TASK-13, TASK-14

Implement `resolve_entities(triplets: list[Triplet], embeddings, llm) -> list[Entity]`. Orchestrates blocking → judge → merge: extracts unique subject/object strings, calls `block_entities`, runs `judge_cluster` on each candidate group, merges confirmed duplicates into canonical `Entity` objects.

**File(s) to implement:**
- `src/resolution/entity_resolver.py`

**Test file(s):**
- `tests/unit/test_entity_resolver.py` (UT-05, UT-06)

**Documentation references:**
- `docs/implementation/part-4-extraction-er/15-entity-resolver.md` — orchestrator combining blocking and judge
- `docs/draft/SPECS.md` §4.2 — `Agentic_Entity_Resolution` node spec
- `docs/draft/REQUIREMENTS.md` §EP-04

---

## Part 5 — Semantic Mapping

---

### [DONE] TASK-16 — `src/mapping/rag_mapper.py`

**Epic:** EP-06 · **Priority:** P0 · **Prerequisites:** TASK-07, TASK-08, TASK-11, TASK-15

Implement the Map-Reduce mapping node: for each `EnrichedTableSchema`, retrieve top-K `Chunk`s via hybrid search, call the LLM with `MAPPING_SYSTEM` / `MAPPING_USER` + few-shot examples, and return a `MappingProposal`. One table per LLM call — never batch. Validates output with `MappingProposal` Pydantic model.

**File(s) to implement:**
- `src/mapping/rag_mapper.py`

**Test file(s):**
- `tests/unit/test_rag_mapper.py` (UT-07)

**Documentation references:**
- `docs/implementation/part-5-mapping/16-rag-mapper.md` — Map-Reduce node implementation
- `docs/draft/SPECS.md` §4.2 — `Retrieval_Augmented_Mapping_LLM` node spec
- `docs/draft/PROMPTS.md` §3 / PT-03 — `MAPPING_SYSTEM` and `MAPPING_USER`
- `docs/draft/REQUIREMENTS.md` §EP-06

---

### [DONE] TASK-17 — `src/mapping/validator.py`

**Epic:** EP-07 · **Priority:** P0 · **Prerequisites:** TASK-07, TASK-16

Implement the two-phase Actor-Critic validator:
1. **Pydantic check**: validate `MappingProposal` schema structure; return `ValidationError` string on failure.
2. **LLM critic**: call `CRITIC_SYSTEM` / `CRITIC_USER`; if `approved=false`, return critique string for Reflection Prompt.

Implement `validate_mapping(proposal: MappingProposal, table: EnrichedTableSchema, entities: list[Entity], llm) -> CriticReview`.

**File(s) to implement:**
- `src/mapping/validator.py`

**Test file(s):**
- `tests/unit/test_validator.py` (UT-08)

**Documentation references:**
- `docs/implementation/part-5-mapping/17-validator.md` — two-phase validation logic
- `docs/draft/SPECS.md` §4.3 — Self-Reflection Loop pattern
- `docs/draft/PROMPTS.md` §3 / PT-04, PT-05 — `CRITIC_SYSTEM`, `CRITIC_USER`, `REFLECTION_TEMPLATE`

---

### [DONE] TASK-18 — `src/mapping/hitl.py`

**Epic:** EP-08 · **Priority:** P1 · **Prerequisites:** TASK-06, TASK-17

Implement the HITL interrupt payload builder and resume handler for LangGraph. When confidence < `settings.confidence_threshold`, set `state["hitl_required"] = True` and surface the mapping proposal for human review. On resume, incorporate the human-corrected mapping back into state.

**File(s) to implement:**
- `src/mapping/hitl.py`

**Test file(s):**
- `tests/integration/test_builder_graph.py` (IT-05)

**Documentation references:**
- `docs/implementation/part-5-mapping/18-hitl.md` — LangGraph `interrupt()` pattern and resume logic
- `docs/draft/SPECS.md` §4.1 — HITL Breakpoint node in the flow diagram
- `docs/draft/REQUIREMENTS.md` §EP-08

---

## Part 6 — Graph & Cypher

---

### [DONE] TASK-19 — `src/graph/neo4j_client.py`

**Epic:** EP-10 · **Priority:** P0 · **Prerequisites:** TASK-02

Implement `Neo4jClient` wrapping the official `neo4j` Python driver. Expose:
- `execute(cypher: str, params: dict) -> list[dict]` — general read/write
- `upsert_concept(...)`, `upsert_table(...)`, `upsert_mapping(...)` — convenience MERGE wrappers
- `test_connection() -> bool` — health check
- Context manager support (`__enter__` / `__exit__` for session lifecycle)

**File(s) to implement:**
- `src/graph/neo4j_client.py`

**Test file(s):**
- `tests/unit/test_neo4j_client.py` (UT-11)

**Documentation references:**
- `docs/implementation/part-6-graph/19-neo4j-client.md` — driver wrapper with MERGE helpers
- `docs/draft/SPECS.md` §2.3 — Cypher MERGE upsert patterns
- `docs/draft/REQUIREMENTS.md` §EP-10

---

### [DONE] TASK-20 — `src/graph/cypher_generator.py`

**Epic:** EP-09 · **Priority:** P0 · **Prerequisites:** TASK-07, TASK-08, TASK-17

Implement `generate_cypher(mapping: MappingProposal, llm) -> str` using `CYPHER_SYSTEM` / `CYPHER_USER` + dynamic few-shot examples from `format_cypher_few_shot(n=settings.few_shot_cypher_examples)`. Output must contain only valid Cypher MERGE statements.

**File(s) to implement:**
- `src/graph/cypher_generator.py` ✅

**Test file(s):**
- `tests/unit/test_cypher_generator.py` (UT-12) ✅ — 24 tests

**Documentation references:**
- `docs/implementation/part-6-graph/20-cypher-generator.md` — generation node implementation
- `docs/draft/SPECS.md` §6.2 — few-shot template format for Cypher
- `docs/draft/PROMPTS.md` §3 / PT-06 — `CYPHER_SYSTEM` and `CYPHER_USER`

---

### TASK-21 — `src/graph/cypher_healer.py`

**Epic:** EP-09 · **Priority:** P0 · **Prerequisites:** TASK-07, TASK-19, TASK-20

Implement the Cypher Healing loop: attempt dry-run execution against Neo4j sandbox; on `CypherSyntaxError`, inject the native exception string into `CYPHER_FIX_USER` (Reflection Prompt) and retry. Max `settings.max_cypher_healing_attempts` retries before returning failure.

**File(s) to implement:**
- `src/graph/cypher_healer.py`

**Test file(s):**
- `tests/unit/test_cypher_healer.py` (UT-10)
- `tests/integration/test_cypher_healing.py` (IT-04)

**Documentation references:**
- `docs/implementation/part-6-graph/21-cypher-healer.md` — healing loop logic
- `docs/draft/SPECS.md` §4.1 — `Test_Cypher_Execution` → `Fix_Cypher_LLM` loop
- `docs/draft/PROMPTS.md` §3 / PT-07 — `CYPHER_FIX_USER` reflection template

---

### TASK-22 — `src/graph/builder_graph.py`

**Epic:** EP-11 · **Priority:** P0 · **Prerequisites:** TASK-06, TASK-09–TASK-21

Wire the complete Builder Graph as a LangGraph `StateGraph` using `BuilderState`. Define all nodes, conditional edges (confidence gate, critic loop, cypher healing loop), and the HITL interrupt. Compile and expose `builder_graph: CompiledGraph`.

**File(s) to implement:**
- `src/graph/builder_graph.py`

**Test file(s):**
- `tests/integration/test_builder_graph.py` (IT-01, IT-02, IT-03, IT-05)
- `tests/integration/test_incremental_update.py` (IT-08)

**Documentation references:**
- `docs/implementation/part-6-graph/22-builder-graph.md` — full `StateGraph` wiring code
- `docs/draft/SPECS.md` §4.1 — Builder Graph flow diagram
- `docs/draft/SPECS.md` §4.3 — Self-Reflection Loop sequence diagram
- `docs/draft/SPECS.md` §4.4 — Incremental upsert strategy

---

## Part 7 — Retrieval

---

### TASK-23 — `src/retrieval/embeddings.py`

**Epic:** EP-12 · **Priority:** P0 · **Prerequisites:** TASK-02

Implement `BGEEmbedder` wrapping `FlagEmbedding` / `BGEM3FlagModel`. Expose:
- `embed_texts(texts: list[str]) -> list[list[float]]` — batch dense embedding (1024-dim)
- `embed_query(text: str) -> list[float]` — single query embedding
Embedding dimension **must** be 1024 to match the Neo4j vector index.

**File(s) to implement:**
- `src/retrieval/embeddings.py`

**Test file(s):**
- `tests/unit/test_hybrid_retriever.py` (UT-12, via mock embedder)

**Documentation references:**
- `docs/implementation/part-7-retrieval/23-embeddings.md` — `BGEEmbedder` wrapper
- `docs/draft/ADR.md` §ADR-04 — BGE-M3 rationale, 1024-dim constraint

---

### TASK-24 — `src/retrieval/hybrid_retriever.py`

**Epic:** EP-12 · **Priority:** P0 · **Prerequisites:** TASK-19, TASK-23

Implement `HybridRetriever` combining three retrieval channels:
1. **Dense vector** (BGE-M3 + Neo4j vector index)
2. **BM25 keyword** (Neo4j full-text index via `rank-bm25`)
3. **Graph traversal** (Neo4j Cypher, hop depth = `settings.retrieval_graph_depth`)

Merge results via Reciprocal Rank Fusion. Expose `retrieve(query: str, top_k: int) -> list[Chunk]`.

**File(s) to implement:**
- `src/retrieval/hybrid_retriever.py`

**Test file(s):**
- `tests/unit/test_hybrid_retriever.py` (UT-12)

**Documentation references:**
- `docs/implementation/part-7-retrieval/24-hybrid-retriever.md` — three-channel retrieval and RRF fusion
- `docs/draft/SPECS.md` §5.2 — Hybrid Retrieval mechanism breakdown table
- `docs/draft/REQUIREMENTS.md` §EP-12

---

### TASK-25 — `src/retrieval/reranker.py`

**Epic:** EP-13 · **Priority:** P0 · **Prerequisites:** TASK-24

Implement `CrossEncoderReranker` wrapping `FlagReranker` (`bge-reranker-large`). Expose `rerank(query: str, chunks: list[Chunk], top_k: int) -> list[Chunk]`. Scores each `(query, chunk.text)` pair with joint transformer attention; returns the top-K highest scoring chunks only.

**File(s) to implement:**
- `src/retrieval/reranker.py`

**Test file(s):**
- `tests/unit/test_reranker.py` (UT-13)

**Documentation references:**
- `docs/implementation/part-7-retrieval/25-reranker.md` — `CrossEncoderReranker` implementation
- `docs/draft/SPECS.md` §5.1 — `Cross_Encoder_Reranking` node
- `docs/draft/ADR.md` §ADR-04 — `bge-reranker-large` rationale

---

## Part 8 — Generation & Query Graph

---

### TASK-26 — `src/generation/answer_generator.py`

**Epic:** EP-14 · **Priority:** P0 · **Prerequisites:** TASK-07, TASK-25

Implement two functions in the same file:

1. `generate_answer(query: str, chunks: list[RetrievedChunk], llm, critique: str | None = None) -> str` — On first call uses `ANSWER_SYSTEM` / `ANSWER_USER`. On retry (when `critique` is set) uses `ANSWER_WITH_CRITIQUE_USER`; the critique is injected as a hard grounding constraint. Temperature: 0.3.
2. `web_search_fallback(query: str) -> str` — Fires when the Hallucination Grader returns `action="web_search"`. Calls DuckDuckGo / Tavily, returns a string prefixed with `[Source: Web Search]`. Consumed by the `_node_web_search` node in `query_graph.py`.

Also implement the helper `format_context(chunks: list[RetrievedChunk]) -> str` (numbered context block shared by both the generator and the grader).

**File(s) to implement:**
- `src/generation/answer_generator.py`

**Test file(s):**
- `tests/unit/test_answer_generator.py` (UT-14)
- `tests/unit/test_web_search_fallback.py` (UT-18)

**Documentation references:**
- `docs/implementation/part-8-generation/26-answer-generator.md` — full implementation including `web_search_fallback`
- `docs/draft/PROMPTS.md` §3 / PT-08, PT-09 — `ANSWER_USER` and `ANSWER_WITH_CRITIQUE_USER`
- `docs/draft/SPECS.md` §5.1 — `Web_Search_Fallback` node in Query Graph diagram
- `docs/draft/SPECS.md` §6.1 — Answer Generation persona and temperature

---

### TASK-27 — `src/generation/hallucination_grader.py`

**Epic:** EP-14 · **Priority:** P0 · **Prerequisites:** TASK-07, TASK-26

Implement `grade_answer(answer: str, chunks: list[Chunk], llm) -> HallucinationGrade`. Uses `GRADER_SYSTEM` / `GRADER_USER` (Self-RAG paradigm). Returns a structured `HallucinationGrade` with `grounded: bool`, `critique: str | None`, and `action: Literal["pass", "regenerate", "web_search"]`. Temperature: 0.0.

**File(s) to implement:**
- `src/generation/hallucination_grader.py`

**Test file(s):**
- `tests/unit/test_hallucination_grader.py` (UT-15)

**Documentation references:**
- `docs/implementation/part-8-generation/27-hallucination-grader.md` — grader implementation
- `docs/draft/SPECS.md` §5.3 — Hallucination Grader Critique Protocol (JSON format)
- `docs/draft/PROMPTS.md` §3 / PT-10 — `GRADER_SYSTEM` and `GRADER_USER`

---

### TASK-28 — `src/generation/query_graph.py`

**Epic:** EP-15 · **Priority:** P0 · **Prerequisites:** TASK-06, TASK-24–TASK-27

Wire the complete Query Graph as a LangGraph `StateGraph` using `QueryState`. Nodes: `Hybrid_Retrieval` → `Cross_Encoder_Reranking` → `Answer_Generation_LLM` → `Hallucination_Grader` → conditional routing to `Web_Search_Fallback` or output. Loop guard on `iteration_count`. Compile and expose `query_graph: CompiledGraph`.

**File(s) to implement:**
- `src/generation/query_graph.py`

**Test file(s):**
- `tests/integration/test_query_graph.py` (IT-06, IT-07)

**Documentation references:**
- `docs/implementation/part-8-generation/28-query-graph.md` — full Query Graph wiring
- `docs/draft/SPECS.md` §5.1 — Query Graph workflow diagram
- `docs/draft/SPECS.md` §3.3 — `QueryState` TypedDict

---

## Part 9 — Evaluation

---

### TASK-29 — `src/evaluation/ragas_runner.py`

**Epic:** EP-16 · **Priority:** P1 · **Prerequisites:** TASK-28

Implement `run_ragas_evaluation(dataset_path: Path) -> dict[str, float]`. Loads `tests/fixtures/gold_standard.json`, runs each `(question, ground_truth, gold_context)` triple through the Query Graph, and computes RAGAS metrics: Context Precision, Context Recall, Faithfulness, Answer Relevance.

**File(s) to implement:**
- `src/evaluation/ragas_runner.py`

**Test file(s):**
- `tests/evaluation/test_ragas.py`

**Documentation references:**
- `docs/implementation/part-9-evaluation/29-ragas-runner.md` — RAGAS pipeline integration
- `docs/draft/SPECS.md` §7.2 — metric definitions and target thresholds
- `docs/draft/DATASET.md` §6 — gold standard dataset format

---

### TASK-30 — `src/evaluation/custom_metrics.py`

**Epic:** EP-16 · **Priority:** P1 · **Prerequisites:** TASK-22, TASK-29

Implement two custom metrics not covered by RAGAS:
- `cypher_healing_rate(results: list[HealingResult]) -> float` — `healed / (healed + failed)`
- `hitl_confidence_agreement(proposals: list[MappingProposal], gold: list[GoldMapping]) -> float` — correlation between auto-approved confidence and gold-standard accuracy

**File(s) to implement:**
- `src/evaluation/custom_metrics.py`

**Test file(s):**
- `tests/evaluation/test_ragas.py`

**Documentation references:**
- `docs/implementation/part-9-evaluation/30-custom-metrics.md` — metric implementations
- `docs/draft/SPECS.md` §7.2 — `cypher_healing_rate` and `hitl_confidence_agreement` formulas

---

### TASK-31 — `src/evaluation/ablation_runner.py`

**Epic:** EP-16 · **Priority:** P1 · **Prerequisites:** TASK-22, TASK-28, TASK-29, TASK-30

Implement `run_ablation(experiment_id: str) -> dict[str, float]` that toggles the relevant `settings` flag (e.g., `ENABLE_SCHEMA_ENRICHMENT=False`), runs the appropriate pipeline (Builder or Query Graph), and records all primary and secondary metrics. Covers AB-01 through AB-06.

**File(s) to implement:**
- `src/evaluation/ablation_runner.py`

**Test file(s):**
- `tests/evaluation/test_ablation.py`

**Documentation references:**
- `docs/implementation/part-9-evaluation/31-ablation-runner.md` — ablation runner scaffolding
- `docs/draft/ABLATION.md` §2 — Ablation Matrix with all 6 experiments
- `docs/draft/ABLATION.md` Appendix — configuration flags

---

## Test Fixtures & Conftest

---

### TASK-F1 — `tests/conftest.py`

**Prerequisites:** TASK-02, TASK-19

Implement shared pytest fixtures: `test_settings` (overrides env to safe test values), `mock_llm` (returns fixed JSON from `tests/fixtures/mock_responses/`), `neo4j_container` (session-scoped `testcontainers.Neo4jContainer`), `neo4j_client` (connected to test container). All integration tests depend on this.

**File(s) to implement:**
- `tests/conftest.py`

**Documentation references:**
- `docs/draft/TEST_PLAN.md` §2.4 — core fixture definitions
- `docs/draft/REQUIREMENTS.md` §EP-01 / US-01-02 — test settings values

---

### TASK-F2 — Test Fixture Files

**Prerequisites:** TASK-F1

Create or verify all fixture files referenced by the test suite:

| File | Description |
|---|---|
| `tests/fixtures/sample_docs/business_glossary.txt` | E-commerce business glossary (see DATASET.md §2.3) |
| `tests/fixtures/sample_docs/data_dictionary.txt` | Table-level data dictionary (see DATASET.md §2.3) |
| `tests/fixtures/sample_ddl/simple_schema.sql` | 3 tables, 1 FK |
| `tests/fixtures/sample_ddl/complex_schema.sql` | 9 tables (8 business + 1 system), multi-FK |
| `tests/fixtures/sample_ddl/system_tables.sql` | 3 system/audit tables with no mappable concept |
| `tests/fixtures/mock_responses/extraction_response.json` | Fixed SLM triplet extraction output |
| `tests/fixtures/mock_responses/er_judge_merge.json` | ER judge decision: merge=true |
| `tests/fixtures/mock_responses/er_judge_separate.json` | ER judge decision: merge=false |
| `tests/fixtures/mock_responses/mapping_high_confidence.json` | Mapping with confidence ≥ 0.90 |
| `tests/fixtures/mock_responses/mapping_null.json` | Mapping with mapped_concept=null |
| `tests/fixtures/mock_responses/critic_approved.json` | Critic approved=true response |
| `tests/fixtures/mock_responses/critic_rejected.json` | Critic approved=false with critique |
| `tests/fixtures/mock_responses/enrichment_response.json` | Schema enrichment LLM output |
| `tests/fixtures/mock_responses/grader_faithful.json` | Grader grounded=true response |
| `tests/fixtures/mock_responses/grader_hallucinated.json` | Grader grounded=false with critique |
| `tests/fixtures/mock_responses/grader_web_search.json` | Grader action=web_search response |
| `tests/fixtures/gold_standard.json` | 20 QA pairs with ground truth and gold context chunks |

**Documentation references:**
- `docs/draft/DATASET.md` §2.3 — exact text content for `.txt` fixture files
- `docs/draft/DATASET.md` §6 — `gold_standard.json` schema
- `docs/draft/TEST_PLAN.md` §6 — fixture and mock inventory

---

## Summary Table

| Task | Source File | Test File | Epic | Priority |
|---|---|---|---|---|
| TASK-01 | `pyproject.toml`, `.env.example` | — | EP-01 | P0 |
| TASK-02 | `src/config/settings.py` | `test_settings.py` | EP-01 | P0 |
| TASK-03 | `src/config/logging.py` | — | EP-01 | P0 |
| TASK-04 | `src/config/llm_factory.py` | — | EP-01 | P0 |
| TASK-04b | `src/config/llm_client.py` | — | EP-01 | P0 |
| TASK-05 | `src/models/schemas.py` | — | EP-06 | P0 |
| TASK-06 | `src/models/state.py` | — | EP-11/15 | P0 |
| TASK-07 | `src/prompts/templates.py` | `test_prompts.py` | prompts | P0 |
| TASK-08 | `src/prompts/few_shot.py` | `test_prompts.py` | EP-06/09 | P0 |
| TASK-09 | `src/ingestion/pdf_loader.py` | `test_pdf_loader.py` | EP-02 | P0 |
| TASK-10 | `src/ingestion/ddl_parser.py` | `test_ddl_parser.py` | EP-05 | P0 |
| TASK-11 | `src/ingestion/schema_enricher.py` | `test_schema_enricher.py` | EP-05b | P0 |
| TASK-12 | `src/extraction/triplet_extractor.py` | `test_triplet_extractor.py` | EP-03 | P0 |
| TASK-13 | `src/resolution/blocking.py` | `test_entity_resolver.py` | EP-04 | P0 |
| TASK-14 | `src/resolution/llm_judge.py` | `test_entity_resolver.py` | EP-04 | P0 |
| TASK-15 | `src/resolution/entity_resolver.py` | `test_entity_resolver.py` | EP-04 | P0 |
| TASK-16 | `src/mapping/rag_mapper.py` | `test_rag_mapper.py` | EP-06 | P0 |
| TASK-17 | `src/mapping/validator.py` | `test_validator.py` | EP-07 | P0 |
| TASK-18 | `src/mapping/hitl.py` | `test_builder_graph.py` | EP-08 | P1 |
| TASK-19 | `src/graph/neo4j_client.py` | `test_neo4j_client.py` | EP-10 | P0 |
| TASK-20 | `src/graph/cypher_generator.py` | `test_cypher_generator.py` | EP-09 | P0 |
| TASK-21 | `src/graph/cypher_healer.py` | `test_cypher_healer.py` | EP-09 | P0 |
| TASK-22 | `src/graph/builder_graph.py` | `test_builder_graph.py` | EP-11 | P0 |
| TASK-23 | `src/retrieval/embeddings.py` | `test_hybrid_retriever.py` | EP-12 | P0 |
| TASK-24 | `src/retrieval/hybrid_retriever.py` | `test_hybrid_retriever.py` | EP-12 | P0 |
| TASK-25 | `src/retrieval/reranker.py` | `test_reranker.py` | EP-13 | P0 |
| TASK-26 | `src/generation/answer_generator.py` | `test_answer_generator.py`, `test_web_search_fallback.py` | EP-14 | P0 |
| TASK-27 | `src/generation/hallucination_grader.py` | `test_hallucination_grader.py` | EP-14 | P0 |
| TASK-28 | `src/generation/query_graph.py` | `test_query_graph.py` | EP-15 | P0 |
| TASK-29 | `src/evaluation/ragas_runner.py` | `test_ragas.py` | EP-16 | P1 |
| TASK-30 | `src/evaluation/custom_metrics.py` | `test_ragas.py` | EP-16 | P1 |
| TASK-31 | `src/evaluation/ablation_runner.py` | `test_ablation.py` | EP-16 | P1 |
| TASK-F1 | `tests/conftest.py` | — | infra | P0 |
| TASK-F2 | `tests/fixtures/**` | — | infra | P0 |
