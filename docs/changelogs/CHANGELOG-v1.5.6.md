# Changelog — v1.5.6

**Date:** 2026-07-18  
**Type:** Patch — Italian summary completion (final thesis polish, no runtime behaviour change)

## Summary

Thesis completion release. Writes and integrates the **Italian summary** (`content/summary.tex`), completing the thesis multilingual front matter (English abstract + Italian summary). The summary is grounded on the v1.5.1/v1.5.5 results and accurately reflects the system architecture, contributions, and evaluation outcomes.

## Documentation Changes

### Italian summary
- **Written `content/summary.tex`** — Italian technical summary covering:
  - SemanticMesh framework purpose and problem statement
  - Two-graph architecture (Builder/Query) with CQRS principles
  - Two-stage entity resolution (BGE-M3 blocking + LLM judge)
  - Three self-reflection loops (Actor-Critic, Cypher healing, hallucination grader)
  - Hybrid retrieval with BM25 + graph traversal + Reciprocal Rank Fusion
  - Provider-agnostic LLM factory (5 tiers, 12 backends)
  - SHA-256 incremental update mechanism
  - Systematic ablation campaign methodology
  - Evaluation results: 210/210 grounded, 4.31/5 AI-Judge score, dataset breakdown
- **Integrated into build** — Uncommented `\sommario` environment in `thesis.tex` (lines 71–77) so the Italian summary now appears in the PDF

### Summary content grounding
All numerical claims and technical details in the Italian summary are grounded in:
- v1.5.1 ablation results re-judged with gpt-5.4-nano
- Chapter 1 (architecture and contributions)
- Chapter 3 (system design and implementation)
- Chapter 5 (evaluation methodology and results)
- Chapter 6 (empirical summary and conclusions)

## Verification

- **Build:** `latexmk -pdf` succeeds cleanly. **79 pages** (from 78 in v1.5.5 — the Italian summary adds one page), **0 undefined citations**, **0 `[?]` markers**.
- **Summary renders correctly:** Italian summary appears in the PDF after the English abstract, with proper pagination and formatting.
- **Content verified:** All technical details (210/210 grounded, 4.31/5 score, dataset breakdown) match the actual ablation results documented in `docs/ablation/RESULTS.md`.

## Notes

- This is a **thesis-only** release; no `src/` runtime behaviour changed
- The Italian summary is approximately 150 words, covering the full thesis scope concisely
- Both English abstract and Italian summary are now included in the build, providing complete multilingual front matter
