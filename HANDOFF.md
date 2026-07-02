# HANDOFF

## Goal
Complete the v1.5.1 ablation campaign by fixing the Neo4j unique constraint violations on `PhysicalTable` nodes and properly recording the dual metric adjustment for the retrieval quality score "floor issue". Execute the final remaining dataset runs.

## Current state
- **Fixed Neo4j constraint violations:** Modified `ddl_parser.py` to force all schema identifiers to lowercase. This resolved the case-sensitivity mismatch that was causing duplicate `PhysicalTable` nodes during graph building. Tests in `test_ddl_parser.py` were updated and pass.
- **Implemented Dual Metrics:** Updated `QueryState` in `state.py`, the query graph return in `query_graph.py`, `run_pipeline.py`, and `ablation_router.py` to extract and serialize `retrieval_quality_score_raw`, `retrieval_quality_score_adjusted`, `pool_size`, and `pool_confidence_applied` into `evaluation_bundle.json`.
- **Documented Floor Issue:** Added section 8.7 to `docs/ablation/RESULTS.md` explaining the CE floor issue and how pool-aware confidence adjustments solve it.
- **Fixed Neo4j Startup Race:** Added a 5-second sleep to `neo4j_lifecycle.py::_wait_for_bolt` to prevent `ConnectionResetError` when the pipeline connects before Bolt is fully ready.
- **Running Final Campaigns:** Created and launched `run_remainder.sh` as a background task. It is currently executing the remaining ablation runs (AB-BEST DS03-07 and AB-BEST-K20 DS01-07).

## Files touched
- `src/ingestion/ddl_parser.py` - Standardized parsed identifiers to `.lower()` to fix case-mismatch during graph ingestion.
- `tests/unit/test_ddl_parser.py` - Updated to match lowercase normalization.
- `src/models/state.py` - Added raw and adjusted score fields to `QueryState`.
- `src/generation/nodes/retrieval_nodes.py` - Added dual metric fields.
- `src/generation/query_graph.py` - Appended dual metrics to `run_query` output dict.
- `scripts/run_pipeline.py` - Plumbed dual metrics to output data models.
- `src/api/ablation_router.py` - Exported dual metrics in API JSON bundles.
- `docs/ablation/RESULTS.md` - Added section 8.7 explaining the CE score floor issue.
- `docs/AI_JUDGE_PROMPT.md` - Removed mentions of deprecated Ragas parameters.
- `scripts/neo4j_lifecycle.py` - Added 5-second sleep after socket connection to ensure Bolt protocol is ready.
- `run_remainder.sh` - (New) Bash script executing the final 12 ablation runs.

## Decisions made
- **Forced lowercase identifiers** - The LLM and graph pipeline often lowercase identifiers. Forcing `ddl_parser` to emit lowercase prevents `PhysicalTable` node uniqueness violations where `USERS` and `users` clash.
- **Dual metric persistence** - Preserving both `_raw` and `_adjusted` CE scores allows the evaluation bundle to audit the cross-encoder's true performance vs the heuristic pool adjustment.
- **Skip builder for DS03** - Ran DS03 using `--no-builder` in the batch script to save 30 minutes, since its ontology was already correctly persisted in the local Neo4j Docker volume.

## Constraints
- **AI-Judge Replaces RAGAS:** Ragas is deprecated and shouldn't be executed (`--ragas` flag).
- **Neo4j Startup Latency:** The Neo4j container opens its TCP port slightly before the Bolt protocol completes initialization, requiring a brief polling sleep before running the pipeline.

## Attempts and failures
- **Query run immediately after Neo4j start** - Failed with `neo4j.exceptions.ServiceUnavailable: Connection reset by peer` because the Bolt handshake wasn't ready despite the TCP socket accepting connections. Fixed by adding a 5s grace period in `neo4j_lifecycle.py`.

## Open issues
- None blocking. The campaign script `run_remainder.sh` is currently executing.

## Next exact steps
1. Wait for the `run_remainder.sh` background task to finish (expected runtime: ~6-7 hours).
2. Review the resulting `outputs/ablation` evaluations for AB-BEST and AB-BEST-K20.
3. Commit the changes to the `dev` branch once the runs succeed.

## Commands / checks
- **Check background script logs:** `tail -f .system_generated/tasks/task-281.log` (or corresponding latest log in `.system_generated/tasks/`).
- **Run Unit Tests:** `pytest tests/unit/ -v`
- **Check Git Status:** `git status`
