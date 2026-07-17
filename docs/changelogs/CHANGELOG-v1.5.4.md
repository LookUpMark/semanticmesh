# Changelog — v1.5.4

**Date:** 2026-07-17
**Type:** Patch — thesis bibliography completion (4 missing citations) + final abstract + biber-resolved build (no runtime behaviour change)

## Summary

Follow-up to the v1.5.3 thesis audit. Resolves the four **significant missing-citation** recommendations flagged by the D2 citation audit (GSM8K, HotpotQA, FEVER, bge-reranker-v2-m3) by adding the bib entries and the corresponding `\cite{}` calls, writes the thesis abstract (previously an empty placeholder commented out of the build), and produces a clean `biber`-resolved PDF for the first time. No `src/` runtime behaviour changed.

## Documentation Changes

### Bibliography completion (4 missing citations)
Added four entries to `docs/overleaf/bibliography.bib` and cited them at the locations flagged in `docs/audits/AUDIT-2026-07-17-thesis.md`:
- **GSM8K** — `cobbe2021gsm8k` (Cobbe et al., 2021), cited in ch2 §Reasoning and Acting Patterns.
- **HotpotQA** — `yang2018hotpotqa` (Yang et al., EMNLP 2018), cited in ch2 §Agentic RAG (ReAct).
- **FEVER** — `thorne2018fever` (Thorne et al., NAACL 2018), cited in ch2 §Agentic RAG (ReAct).
- **bge-reranker-v2-m3** — `xiao2023cpack` (Xiao et al., 2023, C-Pack), cited in ch3 §Query Phase 2 (reranker).

### Abstract
- Wrote `docs/overleaf/content/abstract.tex` (previously a 1-line placeholder). English, grounded on v1.5.1 results: the semantic-gap motivation, the CQRS two-graph architecture, the two-stage entity resolution, the self-reflection loops (Actor-Critic, Cypher healing, hallucination grader), the hybrid retrieval + RRF + cross-encoder pipeline, and the ablation evidence (AB-BEST 210/210 grounded, 4.31/5, k5 vs k20 recall decoupled from judged quality).
- Uncommented the `abstract` environment in `thesis.tex` (lines 57–59) so it appears in the build.

### `.gitignore`
Hardened the LaTeX build-artifacts section with the glossaries/SyncTeX patterns that a future `makeglossaries`/beamer run would emit (the thesis already `\input`s `glossaries.tex`).

## Verification

- **Build:** `latexmk -pdf` succeeds end-to-end now that `biber` is available. **74 pages** (was 73 — the new abstract adds one page), **0 undefined citations**, **0 `[?]` markers** in the rendered PDF.
- **Citations resolved:** the four new keys now render numbered references (e.g. HotpotQA [33], FEVER [34], C-Pack [50]) instead of `[?]`.
- **Tooling note:** `biber` is installed via the Arch `biber` package, but its binary lives in `/usr/bin/vendor_perl/`, which is not on the default PATH; the build requires `PATH="/usr/bin/vendor_perl:$PATH" latexmk -pdf thesis.tex`.

## Known follow-ups (not in this release)

- 9 **minor** missing-citation recommendations from D2 (BM25, MT-Bench, GPT-4, CQRS, PEFT/LoRA, LangChain, sqlglot duplicate-cite, gpt-5.4-nano, Collibra/Alation) — left as reported, not significant enough to add new bib entries.
- The `content/summary.tex` (Italian summary) is still Lorem ipsum and remains commented out of the build.
