# HANDOFF

## Goal
Ship OWL 2 DL export/import for the SemanticMesh Knowledge Graph — interoperability with Protégé/Stardog/GraphDB plus lossless backup/restore. Template-based mapping with `rdflib`, zero LLM cost. **Complete and released as v1.6.2.**

## Current state
- **Branch `dev` = `origin/dev` = `main` = `origin/main` = `fe10675` = tag `v1.6.2`.** Working tree clean, fully pushed.
- **Feature live through 3 releases:** v1.6.0 (initial), v1.6.1 (cross-partition + `HAS_COLUMN` fixes), v1.6.2 (per-edge reification).
- **End-to-end verified on real builds:** DS01 (7 tables) and DS07 stress (58 tables). DS07 round-trip now **lossless**: 812 nodes → 812, 922 edges → 922 (all rel types exact).
- **561 unit tests pass** (530 baseline + 31 new OWL), 1 Neo4j integration test, ruff clean.
- Neo4j container `thesis-neo4j` is UP (started during validation). Container `neo4j-thesis` referenced by `pipeline-run --auto-neo4j` does NOT exist — see Constraints.

## Files touched
- `src/graph/owl_mapper.py` — created. Pure dict↔RDF mapping: `node_to_rdf`, `node_uri`, `edge_to_rdf` (per-edge `sm:Statement` reification), `to_owl_xml`, `from_owl_xml`, `from_owl_documents` (multi-file union), `_extract_nodes_edges`.
- `src/graph/owl_exporter.py` — created. `export_to_owl_files` (4 split `.owl` + `metadata.json` + SHA-256), `export_dir` (validated `\d{8}_\d{6}` + path containment), `list_exports`, `_dump_graph` (wraps `kg_registry._export_graph`).
- `src/graph/owl_importer.py` — created. `import_from_owl_text(text|list, strategy)`, `_merge_graph`, `_node_identity`, `_alias_identity` (param namespacing), `_build_node_statements`. Strategies: clean/versioned/merge.
- `src/api/models.py` — added `OwlExportRequest`, `OwlExportMeta`, `OwlImportRequest`, `OwlImportResult`.
- `src/api/demo_router.py` — 4 endpoints under `/demo/kg/owl` (export, download `{export_id}`, list, import). Auth inherited from router.
- `tests/unit/test_owl_mapper.py` (17), `test_owl_exporter.py` (8), `test_owl_importer.py` (6) — created.
- `tests/integration/test_owl_flow.py` — created. `@pytest.mark.integration`, Neo4j round-trip.
- `pyproject.toml` — added `rdflib>=7.0,<8.0`; version 1.5.3 → 1.6.2.
- `README.md` — API table row + "OWL Export / Import" usage section.
- `docs/changelogs/CHANGELOG-v1.6.0.md`, `-v1.6.1.md`, `-v1.6.2.md` — created.
- `docs/superpowers/specs/2026-07-24-owl-export-import-design.md`, `docs/superpowers/plans/2026-07-24-owl-export-import.md` — spec + plan.

## Decisions made
- **Template-based mapping, not LLM** — deterministic, fast (export 0.6s / import 2.7s on DS07), zero cost. LLM mapping rejected as non-deterministic + slow.
- **Reuse `kg_registry._export_graph()`** for the node/edge dump — no duplicated Neo4j export logic. The OWL layer consumes its dict format.
- **"Versioned" import = auto-snapshot backup, not Neo4j named graphs** — Docker `neo4j:5` is Community Edition; `CREATE DATABASE`/fabric unavailable. Rollback via existing `kg_registry.save_snapshot` before clear+rebuild.
- **Per-edge `rdf:Statement` reification** — RDF triples are unique by (s,p,o); without per-edge statements, multi-FK-to-same-table edges collapsed (DS07 lost 7/90 REFERENCES). Every edge now = base triple + distinct reified statement.
- **`embedding` vectors dropped on export/import** (regenerated on query) — mirrors `kg_registry`. The `include_embeddings` flag was dropped entirely (it was dead: `_export_graph` strips embeddings unconditionally).
- **Tesi `docs/overleaf/` intentionally NOT updated** — OWL is post-thesis work; the thesis (v1.5.6, 79pp, defended) describes v1.5.1. User confirmed: "non è il succo della tesi."
- **Subagent-driven TDD** — implementer + spec/quality review per task; final opus whole-feature review caught the path-traversal (C1).

## Constraints
- **Neo4j Community Edition** (Docker `neo4j:5`). No named graphs / `CREATE DATABASE`. `db.createGraph` will fail.
- **Container name mismatch:** the live container is `thesis-neo4j` (password `thesis_password`). `pipeline-run --auto-neo4j` hardcodes `neo4j-thesis` and `docker run` fails (exit 125, port conflict). **Use the Python API `run_builder(...)` directly** — it connects via settings to the running container.
- **`Neo4jClient.execute_cypher` rejects any string with `;`** (injection guard). Use `execute_batch([(cypher, params), ...])` for multi-write.
- **`Neo4jClient` is a context manager** with a shared singleton driver — `with Neo4jClient() as client:`; do not close.
- **Real rel types** the builder creates: `MAPPED_TO`, `HAS_COLUMN` (NOT `HAS_ATTRIBUTE`), `REFERENCES`, `MENTIONS`, `CHILD_OF`. The mapper list includes both `HAS_COLUMN` and `HAS_ATTRIBUTE` (latter kept for safety, never appears).
- **Build is stochastic** — LLM extraction varies run-to-run (DS07 node count was 815 then 812). Compare before==after within one run, not across runs.
- **No `Co-Authored-By` in commits** — permanent user rule (memory `no-commit-coauthor.md`).
- **Push/merge/release needs explicit in-turn confirmation** — trips the auto-mode safety classifier otherwise. Use single-purpose git/gh commands (compound bash denied).

## Attempts and failures
- **Multi-document XML concatenation invalid** — exporter emits 4 complete XML files; joining with `"\n"` = "junk after document element". Fixed: `from_owl_documents()` parses each separately, unions RDF triples.
- **Rel param `$key` collision** — two single-key endpoints (BusinessConcept + PhysicalTable, both `$key`) collided in merged params. Fixed: `_alias_identity` namespaces to `a_key`/`b_key`.
- **Cross-partition edge drop (DS01)** — `MENTIONS` (Chunk→BusinessConcept) lost: per-file RDF build only knew that file's nodes. Fixed: every edge carries both endpoint nodes into its partition file.
- **`HAS_COLUMN` missing (DS01)** — mapper had the non-existent `HAS_ATTRIBUTE`. 42 edges dropped. Fixed: added `HAS_COLUMN`.
- **RDF duplicate-pair collapse (DS07)** — 7/90 REFERENCES lost. Fixed via per-edge reification (v1.6.2).
- **Path traversal in download endpoint (C1)** — `export_id` joined unvalidated. Fixed: regex `\d{8}_\d{6}` + `is_relative_to` containment.
- **Dead `include_embeddings` flag** — `_export_graph` strips embeddings first, so the flag never worked. Dropped entirely.
- **`datetime.utcnow()` deprecated** (Python 3.13) — exporter used it; kg_registry uses `datetime.now(UTC)`. Fixed for consistency.
- **Cypher syntax bug** — props placed outside `[r:TYPE {...}]` brackets; mock tests missed it (don't execute Cypher). Caught by inspecting built string. Fixed.

## Open issues
- **1 flaky unit test** in the full suite (non-OWL, testcontainers-related): one run in ~4 shows "1 failed, 560 passed", reproduces 561 clean on re-run. Pre-existing, not introduced by OWL work. Not investigated.
- **Thesis not updated** — intentional (see Decisions). If ever needed: add a new chapter/appendix, requires `biber` build (`PATH="/usr/bin/vendor_perl:$PATH" latexmk -pdf`).

## Next exact steps
None — feature complete, released, verified end-to-end. Optional future work (not immediate):
- Investigate the flaky testcontainers unit test if it surfaces.
- Add a dedicated "OWL export/import" study-guide chapter under `docs/study-guide/` if the module should be part of the learning material (currently only README + CHANGELOG document it).

## Commands / checks
- **Unit suite:** `.venv/bin/python -m pytest tests/unit/ -m "not slow" -q` → expect ~561 passed.
- **OWL unit tests:** `.venv/bin/python -m pytest tests/unit/test_owl_mapper.py tests/unit/test_owl_exporter.py tests/unit/test_owl_importer.py -q` → 31 passed.
- **Integration (Neo4j up):** `.venv/bin/python -m pytest tests/integration/test_owl_flow.py -m integration -q`
- **Lint:** `.venv/bin/python -m ruff check src/graph/owl_mapper.py src/graph/owl_exporter.py src/graph/owl_importer.py src/api/demo_router.py src/api/models.py`
- **Start Neo4j:** `docker start thesis-neo4j` (password `thesis_password`).
- **Real e2e round-trip** (builds DS01, costs LLM tokens): `.venv/bin/python /tmp/owl_e2e.py` (script left in /tmp; recreatable — points `run_builder` at `tests/fixtures/01_basics_ecommerce`).
- **Git sync check:** `git status --short && git log --oneline -1 && git rev-list --count origin/dev..dev` (clean / 0).
- **Releases:** `gh release list` (expect v1.6.0, v1.6.1, v1.6.2 at top).

## References
- commit `fe10675` — v1.6.2: lossless edge round-trip via per-edge reification (tag `v1.6.2`, HEAD)
- commit `8f63422` — fix(owl): per-edge reification preserves duplicate-pair relationships
- commit `be5d587` — v1.6.1: OWL round-trip fixes (cross-partition + HAS_COLUMN)
- commit `501eb35` — fix(owl): preserve cross-partition edges + HAS_COLUMN rel type
- commit `a33bd2a` — v1.6.0: OWL export/import feature (initial)
- commit `961a51e` — fix(owl): final-review security (path traversal C1) + correctness findings
- commit `8b96591` — chore: add rdflib dependency
- Spec: `docs/superpowers/specs/2026-07-24-owl-export-import-design.md`
- Plan: `docs/superpowers/plans/2026-07-24-owl-export-import.md`
- Releases: https://github.com/LookUpMark/semanticmesh/releases/tag/v1.6.2 (+ v1.6.1, v1.6.0)
- Memory: `no-commit-coauthor.md` (commit rule), `thesis-build-biber-path.md` (biber PATH)
