# Python Cleanup Audit

Scope: every Python file in repository.
Total files analyzed: **91**

## Summary
- high-priority-refactor: 13
- medium-refactor: 18
- light-refactor: 13
- ok: 47

## Encoding Notes
- All files decoded as UTF-8

## Per-File Analysis

| File | LOC | Code | Comments | Classes | Funcs | Max Func LOC | Long Funcs (>=60) | Status |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| notebooks/ablation/diagnostics/diagnose_ab00.py | 463 | 369 | 29 | 0 | 5 | 183 | 3 | high-priority-refactor |
| scripts/__init__.py | 0 | 0 | 0 | 0 | 0 | 0 | 0 | ok |
| scripts/neo4j_lifecycle.py | 137 | 102 | 4 | 0 | 6 | 45 | 0 | ok |
| scripts/pipeline_run.py | 237 | 190 | 10 | 0 | 3 | 112 | 1 | medium-refactor |
| scripts/run_ablation_full.py | 662 | 539 | 29 | 0 | 10 | 301 | 3 | high-priority-refactor |
| scripts/run_all_ablations.py | 515 | 365 | 39 | 0 | 11 | 118 | 3 | high-priority-refactor |
| src/config/config.py | 106 | 64 | 19 | 1 | 0 | 0 | 0 | ok |
| src/config/__init__.py | 1 | 0 | 1 | 0 | 0 | 0 | 0 | ok |
| src/config/llm_client.py | 415 | 331 | 20 | 3 | 22 | 33 | 0 | medium-refactor |
| src/config/llm_factory.py | 289 | 231 | 10 | 0 | 9 | 122 | 1 | high-priority-refactor |
| src/config/logging.py | 194 | 139 | 11 | 2 | 10 | 48 | 0 | light-refactor |
| src/config/settings.py | 148 | 107 | 14 | 1 | 2 | 15 | 0 | ok |
| src/evaluation/ablation_runner.py | 301 | 239 | 30 | 0 | 2 | 91 | 1 | medium-refactor |
| src/evaluation/custom_metrics.py | 99 | 68 | 6 | 2 | 5 | 24 | 0 | ok |
| src/evaluation/__init__.py | 1 | 0 | 1 | 0 | 0 | 0 | 0 | ok |
| src/evaluation/ragas_runner.py | 700 | 595 | 21 | 0 | 16 | 133 | 5 | high-priority-refactor |
| src/extraction/heuristic_extractor.py | 184 | 150 | 0 | 0 | 6 | 44 | 0 | light-refactor |
| src/extraction/__init__.py | 1 | 0 | 1 | 0 | 0 | 0 | 0 | ok |
| src/extraction/triplet_extractor.py | 258 | 207 | 9 | 0 | 4 | 109 | 1 | medium-refactor |
| src/generation/answer_generator.py | 150 | 117 | 3 | 0 | 3 | 86 | 1 | medium-refactor |
| src/generation/context_distiller.py | 113 | 96 | 0 | 0 | 4 | 38 | 0 | ok |
| src/generation/hallucination_grader.py | 213 | 187 | 1 | 0 | 2 | 183 | 1 | high-priority-refactor |
| src/generation/__init__.py | 1 | 0 | 1 | 0 | 0 | 0 | 0 | ok |
| src/generation/lazy_expander.py | 35 | 28 | 0 | 0 | 2 | 13 | 0 | ok |
| src/generation/query_graph.py | 666 | 553 | 17 | 0 | 20 | 67 | 2 | high-priority-refactor |
| src/graph/builder_graph.py | 547 | 438 | 28 | 0 | 14 | 85 | 3 | high-priority-refactor |
| src/graph/cypher_builder.py | 128 | 101 | 5 | 0 | 2 | 35 | 0 | ok |
| src/graph/cypher_generator.py | 125 | 96 | 5 | 0 | 3 | 66 | 1 | light-refactor |
| src/graph/cypher_healer.py | 171 | 133 | 4 | 0 | 3 | 65 | 1 | light-refactor |
| src/graph/__init__.py | 1 | 0 | 1 | 0 | 0 | 0 | 0 | ok |
| src/graph/neo4j_client.py | 186 | 134 | 13 | 1 | 8 | 27 | 0 | light-refactor |
| src/ingestion/ddl_parser.py | 194 | 147 | 8 | 1 | 4 | 96 | 1 | medium-refactor |
| src/ingestion/__init__.py | 1 | 0 | 1 | 0 | 0 | 0 | 0 | ok |
| src/ingestion/pdf_loader.py | 154 | 120 | 2 | 1 | 3 | 60 | 1 | light-refactor |
| src/ingestion/schema_enricher.py | 183 | 148 | 4 | 0 | 4 | 96 | 1 | medium-refactor |
| src/__init__.py | 1 | 0 | 1 | 0 | 0 | 0 | 0 | ok |
| src/mapping/hitl.py | 170 | 122 | 7 | 0 | 3 | 83 | 1 | medium-refactor |
| src/mapping/__init__.py | 1 | 0 | 1 | 0 | 0 | 0 | 0 | ok |
| src/mapping/rag_mapper.py | 411 | 344 | 6 | 0 | 7 | 154 | 2 | high-priority-refactor |
| src/mapping/validator.py | 175 | 140 | 6 | 0 | 3 | 91 | 1 | medium-refactor |
| src/models/__init__.py | 1 | 0 | 1 | 0 | 0 | 0 | 0 | ok |
| src/models/schemas.py | 228 | 136 | 12 | 19 | 1 | 3 | 0 | light-refactor |
| src/models/state.py | 99 | 67 | 12 | 2 | 0 | 0 | 0 | ok |
| src/prompts/few_shot.py | 114 | 86 | 5 | 0 | 4 | 28 | 0 | ok |
| src/prompts/__init__.py | 1 | 0 | 1 | 0 | 0 | 0 | 0 | ok |
| src/prompts/templates.py | 411 | 283 | 15 | 0 | 0 | 0 | 0 | medium-refactor |
| src/resolution/blocking.py | 151 | 113 | 8 | 0 | 4 | 104 | 1 | medium-refactor |
| src/resolution/entity_resolver.py | 99 | 75 | 4 | 0 | 1 | 72 | 1 | light-refactor |
| src/resolution/__init__.py | 1 | 0 | 1 | 0 | 0 | 0 | 0 | ok |
| src/resolution/llm_judge.py | 264 | 222 | 5 | 0 | 4 | 162 | 1 | high-priority-refactor |
| src/retrieval/embeddings.py | 87 | 66 | 0 | 0 | 3 | 29 | 0 | ok |
| src/retrieval/hybrid_retriever.py | 368 | 297 | 6 | 0 | 8 | 56 | 0 | medium-refactor |
| src/retrieval/__init__.py | 1 | 0 | 1 | 0 | 0 | 0 | 0 | ok |
| src/retrieval/reranker.py | 130 | 99 | 4 | 0 | 2 | 67 | 1 | light-refactor |
| tests/conftest.py | 308 | 203 | 28 | 0 | 23 | 36 | 0 | medium-refactor |
| tests/evaluation/__init__.py | 1 | 0 | 1 | 0 | 0 | 0 | 0 | ok |
| tests/evaluation/test_ablation.py | 123 | 82 | 12 | 3 | 12 | 13 | 0 | ok |
| tests/evaluation/test_ragas.py | 297 | 214 | 27 | 7 | 22 | 21 | 0 | light-refactor |
| tests/integration/__init__.py | 1 | 0 | 1 | 0 | 0 | 0 | 0 | ok |
| tests/integration/test_builder_graph.py | 628 | 486 | 47 | 5 | 13 | 176 | 4 | high-priority-refactor |
| tests/integration/test_cypher_healing.py | 282 | 203 | 26 | 1 | 9 | 65 | 1 | light-refactor |
| tests/integration/test_incremental_update.py | 434 | 360 | 20 | 2 | 5 | 241 | 2 | high-priority-refactor |
| tests/integration/test_query_graph.py | 591 | 449 | 35 | 2 | 17 | 106 | 6 | high-priority-refactor |
| tests/unit/__init__.py | 1 | 0 | 1 | 0 | 0 | 0 | 0 | ok |
| tests/unit/test_answer_generator.py | 132 | 97 | 4 | 2 | 16 | 12 | 0 | ok |
| tests/unit/test_builder_graph.py | 176 | 136 | 7 | 5 | 15 | 21 | 0 | ok |
| tests/unit/test_cypher_builder.py | 116 | 92 | 3 | 2 | 9 | 14 | 0 | ok |
| tests/unit/test_cypher_generator.py | 329 | 238 | 16 | 3 | 29 | 21 | 0 | medium-refactor |
| tests/unit/test_cypher_healer.py | 171 | 128 | 5 | 3 | 16 | 23 | 0 | ok |
| tests/unit/test_ddl_parser.py | 130 | 95 | 3 | 5 | 14 | 6 | 0 | ok |
| tests/unit/test_entity_resolver.py | 448 | 341 | 17 | 7 | 43 | 18 | 0 | medium-refactor |
| tests/unit/test_few_shot.py | 89 | 69 | 1 | 4 | 13 | 11 | 0 | ok |
| tests/unit/test_hallucination_grader.py | 103 | 80 | 2 | 1 | 11 | 12 | 0 | ok |
| tests/unit/test_heuristic_extractor.py | 86 | 64 | 0 | 3 | 9 | 38 | 0 | ok |
| tests/unit/test_hitl.py | 168 | 125 | 7 | 3 | 21 | 12 | 0 | ok |
| tests/unit/test_hybrid_retriever.py | 327 | 242 | 15 | 7 | 30 | 24 | 0 | medium-refactor |
| tests/unit/test_lazy_expander.py | 32 | 23 | 0 | 0 | 4 | 9 | 0 | ok |
| tests/unit/test_llm_client.py | 157 | 112 | 6 | 5 | 16 | 12 | 0 | ok |
| tests/unit/test_llm_factory.py | 66 | 49 | 0 | 1 | 10 | 8 | 0 | ok |
| tests/unit/test_logging.py | 35 | 23 | 1 | 4 | 4 | 4 | 0 | ok |
| tests/unit/test_neo4j_client.py | 219 | 153 | 13 | 4 | 20 | 22 | 0 | light-refactor |
| tests/unit/test_pdf_loader.py | 144 | 102 | 5 | 3 | 12 | 25 | 0 | ok |
| tests/unit/test_prompts.py | 90 | 73 | 1 | 2 | 9 | 9 | 0 | ok |
| tests/unit/test_query_graph.py | 401 | 337 | 3 | 10 | 25 | 40 | 0 | medium-refactor |
| tests/unit/test_rag_mapper.py | 325 | 254 | 13 | 4 | 24 | 29 | 0 | medium-refactor |
| tests/unit/test_reranker.py | 115 | 85 | 3 | 2 | 11 | 18 | 0 | ok |
| tests/unit/test_schema_enricher.py | 149 | 117 | 4 | 2 | 12 | 26 | 0 | ok |
| tests/unit/test_settings.py | 74 | 55 | 2 | 3 | 12 | 5 | 0 | ok |
| tests/unit/test_state.py | 77 | 61 | 2 | 2 | 9 | 24 | 0 | ok |
| tests/unit/test_triplet_extractor.py | 162 | 122 | 6 | 2 | 16 | 27 | 0 | ok |
| tests/unit/test_validator.py | 185 | 142 | 7 | 3 | 17 | 14 | 0 | light-refactor |
