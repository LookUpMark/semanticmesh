#!/bin/bash
# v1.5.1 ablation campaign — full re-run on Linux.
# Re-runs ALL datasets because:
#   1. Case-variant dedup fix (build_nodes.py) changes graph builds.
#   2. Existing DS01-03 bundles predate the dual-metrics code (retrieval_quality_score_raw/adjusted,
#      pool_size, pool_confidence_applied) — the v1.5.1 deliverable.
set -e

export NEO4J_CONTAINER_NAME=thesis-neo4j
export NEO4J_URI=bolt://localhost:7687

echo "=== [1/2] AB-BEST  DS01-07 (best config, all datasets) ==="
.venv/bin/python -m scripts.run_pipeline --best --all-datasets --auto-neo4j

echo "=== [2/2] AB-BEST-K20  DS01-07 (K20 retrieval pool, all datasets) ==="
.venv/bin/python -m scripts.run_pipeline --study AB-BEST-K20 --all-datasets --auto-neo4j

echo "All runs completed successfully!"
