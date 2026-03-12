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
1. `_run_pipeline_on_sample(sample)` — calls `run_query(question)` from the Query Graph, collects `final_answer` + `sources` (node IDs); falls back to `ground_truth_contexts` if the graph returns no sources
2. Exceptions are caught per-sample and logged; failed samples are tracked in `failed_samples` without aborting the run

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

`src/evaluation/ablation_runner.py` implements `run_ablation(experiment_id, dataset_path=None) -> dict[str, float]`.

### Ablation Matrix (all 6 experiments)

| ID | Component Ablated | Setting Toggled | Primary Metric |
|---|---|---|---|
| AB-01 | Schema Enrichment | `ENABLE_SCHEMA_ENRICHMENT=false` | `context_precision` |
| AB-02 | Hybrid Retrieval | `RETRIEVAL_MODE=vector` + `ENABLE_RERANKER=false` | `context_precision` |
| AB-03 | Cypher Healing | `ENABLE_CYPHER_HEALING=false` | `faithfulness` |
| AB-04 | Actor-Critic Validation | `ENABLE_CRITIC_VALIDATION=false` | `context_precision` |
| AB-05 | Cross-Encoder Reranker | `ENABLE_RERANKER=false` | `context_precision` |
| AB-06 | Hallucination Grader | `ENABLE_HALLUCINATION_GRADER=false` | `faithfulness` |

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
3. Calls `run_ragas_evaluation(dataset_path)` inside the override context
4. Returns the 4-metric dict

---

## Evaluation Summary

The three modules fill complementary roles:

| Module | What it measures | When to run |
|---|---|---|
| `ragas_runner.py` | End-to-end answer quality (RAGAS 4-metric suite) | After each system update |
| `custom_metrics.py` | Builder-graph specific behavior (healing, HITL calibration) | After builder pipeline runs |
| `ablation_runner.py` | Per-component contribution (6 AB experiments) | Full evaluation chapter run |

Together these form the quantitative backbone of the thesis evaluation chapter, providing RAGAS metrics measured under 7 distinct conditions (1 baseline + 6 ablations).

---

### Implementation References

- [`ragas_runner.py`](../implementation/part-9-evaluation/29-ragas-runner.md) — RAGAS pipeline integration
- [`custom_metrics.py`](../implementation/part-9-evaluation/30-custom-metrics.md) — `cypher_healing_rate`, `hitl_confidence_agreement`
- [`ablation_runner.py`](../implementation/part-9-evaluation/31-ablation-runner.md) — ablation matrix and settings override
