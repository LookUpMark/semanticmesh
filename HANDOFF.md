# HANDOFF

## Goal
Complete the v1.5.1 ablation campaign with dual metrics (retrieval_quality_score_raw/adjusted, pool_size, pool_confidence_applied) for both AB-BEST and AB-BEST-K20 configurations across 7 datasets (DS01-07).

## Current state
- **AB-BEST (7/7):** ✅ COMPLETED - All datasets grounded=100% with dual metrics
  - DS01-07 evaluation bundles generated 2026-07-03 09:12-10:54 UTC
  - Dual metrics confirmed in per_question data (_raw, _adjusted, pool_size, pool_confidence_applied)
- **AB-BEST-K20 (2/7):** ⏸️ STOPPED at DS02
  - DS01-02: ✅ grounded=100% (completed 11:00-11:11 UTC)
  - DS03-07: ⏸️ NOT STARTED
  - Campaign stopped via user request after DS02 completion
- **Environment:** Linux setup with uv package manager, thesis-neo4j Docker container active
- **Branch:** dev (up to date with origin/dev)

## Files touched
- `src/graph/build_nodes.py` - Contains case-variant dedup fix (lines 424-449) preventing ConstraintError when LLM creates UPPERCASE PhysicalTable nodes
- `pyproject.toml` - langchain-core/text-splitters bounds fixed to >=1.0,<2.0 (resolves compatibility with langchain 1.x)
- `run_remainder_linux.sh` - Campaign script for Linux (sets NEO4J_CONTAINER_NAME=thesis-neo4j, runs all datasets for both studies)
- `outputs/ablation/AB-BEST/datasets/*/evaluation_bundle.json` - 7 completed bundles with dual metrics
- `outputs/ablation/AB-BEST-K20/datasets/01_basics_ecommerce/evaluation_bundle.json` - K20 DS01 completed
- `outputs/ablation/AB-BEST-K20/datasets/02_intermediate_finance/evaluation_bundle.json` - K20 DS02 completed

## Decisions made
- **Re-run all AB-BEST DS01-07** - Existing bundles lacked dual metrics (generated before code change) and may have been affected by case-variant bug inconsistently
- **Stop at DS02 for K20** - User requested pause; DS01-02 provide initial K20 data point vs AB-BEST comparison
- **Use uv package manager** - No .venv existed; uv preferred over pip for Python 3.13
- **Set NEO4J_CONTAINER_NAME=thesis-neo4j** - Local container uses different name than handoff's neo4j-thesis

## Constraints
- **Neo4j container naming:** Local container is `thesis-neo4j` (not `neo4j-thesis` from handoff)
- **Python version:** 3.13.13 (uv managed)
- **LLM non-determinism:** Langfuse callback incompatibility (langfuse 2.60.10 vs langchain 1.3.11) causes warnings but doesn't affect results
- **Dataset independence:** Each run clears graph (--clear-graph=True in builder), so datasets can run independently

## Attempts and failures
- **Case-variant dedup bug** - Attempted to run DS04 fresh, got ConstraintError on `tb_category`. Root cause: LLM-healed Cypher creates UPPERCASE PhysicalTable (TB_CATEGORY) while FK stub creates lowercase (tb_category). SET with case-insensitive WHERE matched both → collision. Fixed by dedup in build_nodes.py (keeper selection + DETACH DELETE variants).
- **Langchain dependency conflict** - Initial `uv pip install -e .` failed due to pyproject.toml pinning `langchain-core>=0.3,<1.0` incompatible with `langchain>=1.0`. Fixed by updating bounds to >=1.0,<2.0.
- **Pytest import errors** - Missing testcontainers module. Installed with uv pip install.

## Open issues
- **Langfuse tracing incompatibility:** langfuse 2.60.10's CallbackHandler imports `langchain.callbacks.base` which doesn't exist in langchain 1.3.11 (moved to langchain_core). Warnings appear but don't affect results. Can fix by downgrading langfuse or patching import path.
- **AB-BEST-K20 DS03-07 remaining:** 5 datasets (~3-4 hours estimated) not yet run.

## Next exact steps
1. **Resume AB-BEST-K20 campaign** (when ready):
   ```bash
   bash run_remainder_linux.sh
   ```
   This will re-run DS01-02 (already complete, safe to skip) + DS03-07.
   To skip completed datasets, modify script to start at DS03 or use `--datasets` flag explicitly.

2. **Verify dual metrics** in completed bundles:
   ```bash
   .venv/bin/python -c "import json; d=json.load(open('outputs/ablation/AB-BEST/datasets/01_basics_ecommerce/evaluation_bundle.json')); print(d['per_question'][0].get('retrieval_quality_score_raw'))"
   ```

3. **Commit completed results** (when satisfied):
   ```bash
   git add outputs/ablation/AB-BEST/ outputs/ablation/AB-BEST-K20/ run_remainder_linux.sh
   git commit -m "feat(ablation): complete AB-BEST campaign and start AB-BEST-K20 with dual metrics"
   ```

## Commands / checks
- **Check bundle grounding:**
  ```bash
  .venv/bin/python -c "import json; d=json.load(open('outputs/ablation/AB-BEST/datasets/01_basics_ecommerce/evaluation_bundle.json')); print(d['query_report']['grounded_rate'])"
  ```
- **Verify dual metrics present:**
  ```bash
  .venv/bin/python -c "import json; d=json.load(open('outputs/ablation/AB-BEST/datasets/01_basics_ecommerce/evaluation_bundle.json')); print('dual_metrics' in d or any('retrieval_quality_score' in str(q) for q in d.get('per_question',[])))"
  ```
- **Check Neo4j container status:**
  ```bash
  docker ps | grep thesis-neo4j
  ```
- **Run single dataset test:**
  ```bash
  NEO4J_CONTAINER_NAME=thesis-neo4j NEO4J_URI=bolt://localhost:7687 .venv/bin/python -m scripts.run_pipeline --best --dataset tests/fixtures/04_complex_manufacturing/gold_standard.json --auto-neo4j
  ```

## References
- commit `cbbb7e5` - feat: update dependencies and improve node graph building (langchain-core >=1.0, case-variant dedup, run_remainder_linux.sh)
- commit `2316d38` - fix(pipeline): resolve case-sensitivity in DDL, implement pool-aware dual metrics for retrieval, and document floor issue
- docs/ablation/RESULTS.md section 8.7 - CE score floor issue and pool-aware confidence adjustments
- tests/fixtures/ - 7 dataset fixtures: 01_basics_ecommerce, 02_intermediate_finance, 03_advanced_healthcare, 04_complex_manufacturing, 05_edgecases_incomplete, 06_edgecases_legacy, 07_stress_large_scale
