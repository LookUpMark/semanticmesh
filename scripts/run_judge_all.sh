#!/usr/bin/env bash
# Run AI Judge for all studies AB-01→AB-20 across DS01→DS06
# Skips bundles that already have ai_judge.md

set -euo pipefail

BASE="notebooks/ablation/ablation_results"
JUDGE_MODEL="gpt-5.4-mini"
DATASETS=(01_basics_ecommerce 02_intermediate_finance 03_advanced_healthcare 04_complex_manufacturing 05_edgecases_incomplete 06_edgecases_legacy)
STUDIES=(AB-01 AB-02 AB-03 AB-04 AB-05 AB-06 AB-07 AB-08 AB-09 AB-10 AB-11 AB-12 AB-13 AB-14 AB-15 AB-16 AB-17 AB-18 AB-19 AB-20)

total_judged=0
total_skipped=0

for AB in "${STUDIES[@]}"; do
    BUNDLES=()
    for DS in "${DATASETS[@]}"; do
        B="$BASE/$AB/$DS/evaluation_bundle.json"
        JUDGE="$BASE/$AB/$DS/ai_judge.md"
        if [ -f "$B" ] && [ ! -f "$JUDGE" ]; then
            BUNDLES+=("$B")
        fi
    done

    if [ ${#BUNDLES[@]} -eq 0 ]; then
        echo "[SKIP] $AB — all datasets already judged"
        total_skipped=$((total_skipped + 6))
        continue
    fi

    echo ""
    echo "========================================"
    echo "  $AB — judging ${#BUNDLES[@]} bundles"
    echo "========================================"
    python scripts/run_ai_judge.py \
        --bundles "${BUNDLES[@]}" \
        --output "$BASE/$AB/AI_JUDGE.md" \
        --judge "$JUDGE_MODEL"
    total_judged=$((total_judged + ${#BUNDLES[@]}))
    echo "  [DONE] $AB"
done

echo ""
echo "=========================================="
echo "  AI JUDGE COMPLETE"
echo "  Judged: $total_judged   Skipped: $total_skipped"
echo "=========================================="
