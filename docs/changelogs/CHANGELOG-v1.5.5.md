# Changelog — v1.5.5

**Date:** 2026-07-18
**Type:** Patch — thesis minor citations polish + 5 new tables + data grounding fixes (no runtime behaviour change)

## Summary

Thesis polishing release. Adds the **9 minor missing citations** flagged by the D2 citation audit (BM25, MT-Bench, GPT-4, CQRS, PEFT/LoRA, LangChain, sqlglot, gpt-5.4-nano, Collibra/Alation) and introduces **5 new tables** to improve visual structure and increase page count (75→78 pages). Fixes placement with `[H]` specifier and corrects all table data to be grounded in actual ablation results.

## Documentation Changes

### Minor citations completion (9 missing citations)
Added nine entries to `docs/overleaf/bibliography.bib` and cited them at the locations flagged in `docs/audits/AUDIT-2026-07-17-thesis.md`:
- **BM25** — `robertson2009probabilistic` (Robertson & Zaragoza, 2009), cited in ch1 §Hybrid retrieval with ablation-backed design.
- **CQRS** — `young2010cqrs` (Young, QCon 2010), cited in ch1 §Two-graph architecture.
- **Collibra/Alation** — `collibra2025`, `alation2025` (vendor documentation), cited in ch1 §Existing approaches.
- **GPT-4** — `openai2023gpt4` (OpenAI, 2023), cited in ch2 §LLM-as-a-Judge.
- **LangChain** — `langchain2023github` (GitHub repository), cited in ch3 §Phase 1: Document Ingestion.
- **sqlglot** — `sqlglot` (already in bib), now cited in ch3 §Phase 3: Schema Parsing and Enrichment (3 occurrences).
- **gpt-5.4-nano** — `openai2024gpt54nano` (model specification), cited in ch5 §Standard automated metrics (3 occurrences).
- **PEFT/LoRA** — `hu2022lora` (Hu et al., 2022), cited in ch6 §Domain-specific embedding or SLM fine-tuning.

### New tables (5 tables added)
Added five structured tables to improve thesis readability and increase page count:
- **Ch1**: Summary of Thesis Contributions (7 key contributions table)
- **Ch4**: Builder Pipeline Components (component-to-file mapping)
- **Ch4**: REST API Endpoints (7 endpoints across 3 routers)
- **Ch5**: Key Findings from Ablation Study (9 grounded findings with implications)
- **Ch6**: AB-BEST Evaluation Results Summary (7 datasets with K5 vs K20 comparison)

### Table data grounding fixes
Corrected all numerical data in tables to match actual ablation results:
- **Ch6 Results Summary**: Fixed DS02 (4.70, was 4.48), DS04 (4.45, was 4.20), DS05 (4.45, was 4.28)
- **Ch4 Builder Components**: Fixed file paths (extraction_node.py → triplet_extractor.py, etc.)
- **Ch5 Ablation Findings**: Precision-improved claims with DS01-specific context (e.g., "Neutral on DS01 v1.5.1")

### Placement and formatting improvements
- Added `\usepackage{float}` to `common/packages.tex` for `[H]` placement specifier
- Replaced `[htbp]` with `[H]` for all 5 new tables to force exact positioning
- Fixed Unicode character `≈` → `$\approx$` in Ch6 Results Summary table

## Verification

- **Build:** `latexmk -pdf` succeeds cleanly. **78 pages** (from 75 in v1.5.4), **0 undefined citations**, **0 `[?]` markers**.
- **Citations resolved:** all 9 new keys render numbered references correctly.
- **Data grounding verified:** all table numbers cross-checked against `docs/ablation/RESULTS.md`.
- **File paths verified:** all builder component paths checked against `src/` structure.
- **Table placement verified:** all 5 new tables appear at exact insertion points with `[H]` specifier.

## Notes

- This is a **thesis-only** release; no `src/` runtime behaviour changed
- Tables add 3 pages but improve visual structure significantly  
- All data now grounded in v1.5.1 ablation results re-judged with gpt-5.4-nano
- Mixed placement strategy: new tables use `[H]`, existing figures/tables retain `[htbp]`
