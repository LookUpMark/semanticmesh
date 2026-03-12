# Part 6 — Neo4j Graph & Cypher

With validated mappings between tables and concepts, the next step is to persist them in a Knowledge Graph on Neo4j. Part 6 implements the Neo4j integration, Cypher statement generation with few-shot learning, self-healing for syntax errors, and the complete Builder Graph that orchestrates everything.

## TASK-19: Neo4j Wrapper with MERGE Helpers

Working directly with the Neo4j driver can be verbose and error-prone. Each query must be constructed as a string, parameters must be passed correctly to prevent injection, and sessions must be managed carefully to avoid connection leaks. The `Neo4jClient` in `src/graph/neo4j_client.py` encapsulates all this complexity.

The three helper methods — `upsert_concept()`, `upsert_table()`, and `upsert_mapping()` — hide the complexity of Cypher MERGE. The MERGE is crucial for this system: it combines CREATE and MATCH in one atomic operation that creates the node if it doesn't exist, or updates it if it already exists. This makes upserts idempotent — we can run the same upsert multiple times without creating duplicates.

The distinction between ON CREATE SET and ON MATCH SET is important. Some properties, like concept name or table name, should never change — they go in ON CREATE SET. Other properties, like a concept's definition or a table's DDL source, should be updated on re-ingestion — they go in ON MATCH SET. This distinction enables incremental system behavior: we can re-ingest updated documents and the graph will update accordingly.

## TASK-20: Cypher Generation with Few-Shot Examples

Generating correct Cypher is non-trivial. The LLM must remember MERGE syntax with its placeholders, format column lists correctly, and use parameters appropriately. Even small syntax errors — a missing comma, an unclosed quote — can cause failures.

The few-shot approach solves this problem by providing concrete examples of correct Cypher. The system has a bank of examples, and for each table selects the most relevant ones based on similarity (column count, data types, etc.). This gives the LLM a template to follow, dramatically reducing errors.

An important detail is that all values are passed as parameters — `$concept_name`, `$concept_definition`, etc. — rather than being hardcoded in the Cypher string. This prevents Cypher injection and improves performance because Neo4j can cache query plans.

The result is a `CypherStatement` containing both the Cypher string and parameters in a separate dict. This allows executing the query with `session.run(cypher, **params)`, which is both secure and efficient.

## TASK-21: Self-Healing for Cypher Errors

Despite few-shot examples, errors happen. The LLM might generate slightly malformed syntax, might forget a comma, or might use a keyword incorrectly. Instead of failing completely, the system implements self-healing.

The `heal_cypher()` function performs a "dry-run" using EXPLAIN — this validates syntax without modifying the database. If it finds an error, it injects the error into a reflection prompt and asks the LLM to correct the Cypher. This loop continues up to three attempts or until the Cypher is valid.

The reflection prompt is designed specifically for healing: it contains the broken Cypher, the exact error message from Neo4j, and instructions to correct only the specific error without unnecessarily restructuring the query. This focus reduces the chance that the LLM introduces new errors while trying to fix the original one.

In practice, self-healing has a very high success rate. Most errors are minor syntax issues that the LLM corrects on the first attempt. More severe errors — for example, trying to use a feature that doesn't exist in that Neo4j version — might require two or three attempts but are eventually resolved. Only in rare cases does the system fail after three attempts, and in those cases the error is logged for manual investigation.

## TASK-22: Complete Builder Graph

The `BuilderGraph` in `src/graph/builder_graph.py` is where all components from previous parts are assembled into a complete pipeline. It executes sequentially: PDF ingestion, DDL parsing, schema enrichment, triplet extraction, entity resolution, table-to-concept mapping, Cypher generation, and Neo4j upsert.

The graph uses LangGraph's conditional routing mechanism to handle special cases. After mapping, if confidence is low, the graph interrupts and waits for human review. If the grader approves, it continues to Cypher generation. If rejected, it can regenerate with feedback.

Using LangGraph to orchestrate this pipeline has numerous advantages. First, visualization — we can generate a graph clearly showing data flow and decision points. Second, debugging — we can inspect state at each node to see what happened. Third, flexibility — adding new nodes or modifying routing is a matter of adding or modifying functions, not rewriting complex logic.

The integration test for the Builder Graph executes the entire pipeline with real data, verifying that the resulting Neo4j graph contains the correct nodes and relationships. This end-to-end test is the final proof that all components work together correctly.

## From Ingestion to Graph

This part represents an important transition in the project. In previous parts, we extracted and processed data. Here, we finally make that data persistent in a structured Knowledge Graph on Neo4j. This graph becomes the source of truth for the system — it's what the Query Graph (Part 8) will query to answer user questions.

The journey from raw PDFs and SQL DDL to a queryable Knowledge Graph is complex, but each step is now well-defined and tested. Ingestion extracts and cleans data. Extraction and entity resolution identify business concepts. Mapping aligns database tables to concepts. Cypher generator translates these alignments into graph statements. And the Builder Graph orchestrates everything.

---

### References

For implementation details of each task, consult the detailed guides:
- [`neo4j_client.py`](../implementation/part-6-graph/19-neo4j-client.md) — Neo4j wrapper with MERGE helpers
- [`cypher_generator.py`](../implementation/part-6-graph/20-cypher-generator.md) — Cypher generation with few-shot
- [`cypher_healer.py`](../implementation/part-6-graph/21-cypher-healer.md) — Self-healing for errors
- [`builder_graph.py`](../implementation/part-6-graph/22-builder-graph.md) — Complete Builder Graph
