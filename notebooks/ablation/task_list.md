# Ablation Campaign Task List (Testing Branch)

Date start: 2026-03-16  
Constraint: reasoning/extraction models fixed to GPT-OSS (`openai/gpt-oss-120b`, `openai/gpt-oss-20b`)

## Scope agreed

Excluded from this campaign:
- Extraction concurrency studies
- Retries studies (`max_reflection_attempts`, `max_hallucination_retries`, stress on healing loops)
- Concurrency stress by provider protocol
- Multi-run stability burn-in (too expensive)

Included:
- Retrieval mode
- Reranker (on/off + top_k)
- Chunking strategy
- Extraction max tokens
- Entity resolution thresholds
- Schema enrichment
- Critic validation + confidence threshold
- Cypher healing
- Hallucination grader
- RAGAS metrics collection per run

## Run checklist (sequential)

- [x] AB-00 Baseline
  - `RETRIEVAL_MODE=hybrid`, `ENABLE_RERANKER=true`, `RERANKER_TOP_K=10`
  - `CHUNK_SIZE=256`, `CHUNK_OVERLAP=32`, `LLM_MAX_TOKENS_EXTRACTION=8192`
  - `ER_SIMILARITY_THRESHOLD=0.75`, `ER_BLOCKING_TOP_K=10`
  - `ENABLE_SCHEMA_ENRICHMENT=true`, `ENABLE_CRITIC_VALIDATION=true`
  - `CONFIDENCE_THRESHOLD=0.90`, `ENABLE_CYPHER_HEALING=true`, `ENABLE_HALLUCINATION_GRADER=true`

- [ ] AB-01 Retrieval mode = vector (`RETRIEVAL_MODE=vector`)
- [ ] AB-02 Retrieval mode = bm25 (`RETRIEVAL_MODE=bm25`) *(attempted; timed out, rerun pending)*

- [ ] AB-03 Reranker OFF (`ENABLE_RERANKER=false`)
- [ ] AB-04 Reranker top_k = 5 (`RERANKER_TOP_K=5`)
- [ ] AB-05 Reranker top_k = 20 (`RERANKER_TOP_K=20`)

- [ ] AB-06 Chunking 128/16 (`CHUNK_SIZE=128`, `CHUNK_OVERLAP=16`)
- [ ] AB-07 Chunking 384/48 (`CHUNK_SIZE=384`, `CHUNK_OVERLAP=48`)
- [ ] AB-08 Chunking 512/64 (`CHUNK_SIZE=512`, `CHUNK_OVERLAP=64`)

- [ ] AB-09 Extraction max tokens = 4096 (`LLM_MAX_TOKENS_EXTRACTION=4096`)
- [ ] AB-10 Extraction max tokens = 16384 (`LLM_MAX_TOKENS_EXTRACTION=16384`)

- [ ] AB-11 ER threshold = 0.65 (`ER_SIMILARITY_THRESHOLD=0.65`)
- [ ] AB-12 ER threshold = 0.85 (`ER_SIMILARITY_THRESHOLD=0.85`)
- [ ] AB-13 ER blocking top_k = 5 (`ER_BLOCKING_TOP_K=5`)
- [ ] AB-14 ER blocking top_k = 20 (`ER_BLOCKING_TOP_K=20`)

- [ ] AB-15 Schema enrichment OFF (`ENABLE_SCHEMA_ENRICHMENT=false`)
- [ ] AB-16 Critic validation OFF (`ENABLE_CRITIC_VALIDATION=false`)
- [ ] AB-17 Confidence threshold = 0.70 (`CONFIDENCE_THRESHOLD=0.70`)
- [ ] AB-18 Confidence threshold = 0.85 (`CONFIDENCE_THRESHOLD=0.85`)

- [ ] AB-19 Cypher healing OFF (`ENABLE_CYPHER_HEALING=false`)
- [ ] AB-20 Hallucination grader OFF (`ENABLE_HALLUCINATION_GRADER=false`)

## Results log (append-only)

| Ablation | Status | Builder(s) | Query(s) | Total(s) | Triplets | Entities | Tables | Grounded | Positive | RAGAS faithfulness | RAGAS answer_rel | RAGAS ctx_prec | RAGAS ctx_recall | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---|

## Operational notes

- RAGAS currently not reliable in this campaign environment:
  - one run failed with missing evaluator API key (`OPENAI_API_KEY` required by default evaluator stack),
  - full 50-sample RAGAS pass is also significantly costly in wall-clock and tokens.
- For now, campaign proceeds with core pipeline metrics; RAGAS can be re-enabled later with a dedicated evaluator configuration.
