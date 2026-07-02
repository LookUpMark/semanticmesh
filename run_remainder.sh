#!/bin/bash
set -e

PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"

echo "=== Rerunning queries for AB-BEST DS03 (with dual metrics fix) ==="
.venv/bin/python -m scripts.run_pipeline --best --dataset tests/fixtures/03_advanced_healthcare/gold_standard.json --auto-neo4j --no-builder

echo "=== Running AB-BEST DS04-07 ==="
.venv/bin/python -m scripts.run_pipeline --best --datasets tests/fixtures/04_complex_manufacturing/gold_standard.json tests/fixtures/05_edgecases_incomplete/gold_standard.json tests/fixtures/06_edgecases_legacy/gold_standard.json tests/fixtures/07_stress_large_scale/gold_standard.json --auto-neo4j

echo "=== Running AB-BEST-K20 DS01-07 ==="
.venv/bin/python -m scripts.run_pipeline --study AB-BEST-K20 --all-datasets --auto-neo4j

echo "All runs completed successfully!"
