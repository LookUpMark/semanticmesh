# Part 9 — Evaluation: RAGAS, Custom Metrics & Ablation Studies

Part 9 implements the full evaluation layer of the thesis: automated RAGAS benchmarking against a gold-standard QA dataset, two custom metrics that measure system-specific properties not covered by RAGAS, and a configurable ablation runner that quantifies each component's marginal contribution.

## TASK-29: RAGAS Evaluation Pipeline

`src/evaluation/ragas_runner.py` exposes `run_ragas_evaluation(dataset_path=None) -> dict[str, float]`.

**Gold-standard dataset** (`tests/fixtures/gold_standard.json`) — 50 QA pairs spanning five query types:

| Type | Description |
|---|---|
| `direct_mapping` | "Which table stores Customer data?" |
| `attribute_lookup` | "What is the primary key of ORDER_LINE_ITEM?" |
| `multi_hop` | "What is the join path from CUSTOMER_MASTER to ORDER_LINE_ITEM?" |
| `negative` | "Is there an invoice entity in the schema?" |

**Pipeline per sample:**
1. `_run_pipeline_on_sample(sample)` — calls `run_query(question)` from the Query Graph, collects `final_answer` + `retrieved_contexts` (full reranked chunk texts)
2. If `retrieved_contexts` is empty, the runner falls back to `ground_truth_contexts` and logs a warning
3. Exceptions are caught per-sample and logged; failed samples are tracked in `failed_samples` without aborting the run

**RAGAS metrics** (computed in `_compute_ragas_metrics`):

| Metric | Measures |
|---|---|
| `faithfulness` | Are all claims in the answer supported by the retrieved context? |
| `answer_relevancy` | Does the answer address the question? |
| `context_precision` | What fraction of retrieved chunks are relevant? |
| `context_recall` | Are all relevant chunks retrieved? |

`ragas` and `datasets` are imported lazily inside `_compute_ragas_metrics`. If either is not installed, the function returns `{all: 0.0}` without crashing — useful for CI environments.

## TASK-30: Custom Metrics

`src/evaluation/custom_metrics.py` provides two metrics covering builder-graph behavior that RAGAS cannot measure.

### `cypher_healing_rate(results: list[HealingResult]) -> float`

Measures the Cypher Healing Loop's effectiveness (AB-03 ablation):

```
healed = count(initial_success=False AND final_success=True)
failed = count(initial_success=False AND final_success=False)
rate   = healed / (healed + failed)
```

Returns `0.0` when no healing attempts occurred (all first-try successes or empty list).

`HealingResult` is a lightweight class (not Pydantic) with `initial_success: bool` and `final_success: bool`.

### `hitl_confidence_agreement(proposals, gold) -> float`

Measures whether the mapping confidence score correlates with actual correctness (AB-04 ablation). For each `MappingProposal` matched to a `GoldMapping` by `table_name`:

- `confidence ∈ [0, 1]` — model's self-reported certainty
- `correct = 1.0` if `mapped_concept == gold.correct_concept` else `0.0`

Returns the **Pearson correlation** between the two vectors (pure Python, no scipy). Returns `0.0` if fewer than 2 pairs are found (avoiding undefined correlation).

`_pearson(x, y)` is the internal implementation — tested directly.

## TASK-31: Ablation Runner

`src/evaluation/ablation_runner.py` implements `run_ablation(experiment_id, dataset_path=None, run_ragas=None, doc_paths=None, ddl_paths=None) -> dict[str, float]`.

### Ablation Matrix (AB-00 … AB-20)

The current matrix contains **21 studies**:

| Group | IDs | Focus |
|---|---|---|
| Baseline | AB-00 | Full default pipeline |
| Retrieval mode | AB-01, AB-02 | Vector-only vs BM25-only |
| Reranker | AB-03, AB-04, AB-05 | Disable reranker / top-k variants |
| Chunking | AB-06, AB-07, AB-08 | Chunk size + overlap |
| Extraction budget | AB-09, AB-10 | `LLM_MAX_TOKENS_EXTRACTION` |
| Entity resolution | AB-11, AB-12, AB-13, AB-14 | Similarity threshold + blocking top-k |
| Mapping validation | AB-15, AB-16 | Schema enrichment / critic validation |
| Confidence threshold | AB-17, AB-18 | HITL threshold sensitivity |
| Generation safeguards | AB-19, AB-20 | Cypher healing / hallucination grader |

Source of truth: `ABLATION_MATRIX` in `src/evaluation/ablation_runner.py`.

### Settings Override via `_settings_override(env_overrides)`

The `Settings` class uses `@lru_cache` on `get_settings()`. The context manager:
1. Saves the current env values for each key
2. Sets the new values via `os.environ.update`
3. Calls `get_settings.cache_clear()` — forces fresh settings on next access
4. After the block, restores original values and clears the cache again

This ensures clean isolation between ablation runs and that no leaked overrides affect subsequent calls.

### Execution Model

`run_ablation(experiment_id)`:
1. Validates the ID against `ABLATION_MATRIX` → raises `ValueError` on unknown ID
2. Applies env overrides via `_settings_override`
3. Runs builder graph on fixture docs + DDL (default: `complex_schema.sql`)
4. Optionally calls `run_ragas_evaluation(dataset_path)` depending on matrix/run flag
5. Returns RAGAS metrics plus builder counters (`triplets`, `entities`, `tables_parsed`, `tables_completed`, `cypher_failed`)

---

## Evaluation Summary

The three modules fill complementary roles:

| Module | What it measures | When to run |
|---|---|---|
| `ragas_runner.py` | End-to-end answer quality (RAGAS 4-metric suite) | After each system update |
| `custom_metrics.py` | Builder-graph specific behavior (healing, HITL calibration) | After builder pipeline runs |
| `ablation_runner.py` | Per-component contribution (21 AB experiments) | Full evaluation chapter run |

Together these form the quantitative backbone of the thesis evaluation chapter, providing RAGAS metrics measured across baseline and targeted ablation conditions.

---

### Implementation References

- [`ragas_runner.py`](../implementation/part-9-evaluation/29-ragas-runner.md) — RAGAS pipeline integration
- [`custom_metrics.py`](../implementation/part-9-evaluation/30-custom-metrics.md) — `cypher_healing_rate`, `hitl_confidence_agreement`
- [`ablation_runner.py`](../implementation/part-9-evaluation/31-ablation-runner.md) — ablation matrix and settings override
