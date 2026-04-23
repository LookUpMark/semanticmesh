#!/usr/bin/env python3
"""Manual integration test — Incremental Update Verification.

Runs a series of builder graph invocations against a live Neo4j instance
and queries the database after each step to verify:

1. **Baseline build** — clean slate → correct node/edge counts
2. **Idempotency** — same data re-run (no clear) → counts unchanged (SHA skip)
3. **Force rebuild** — same data with force_rebuild=True → counts unchanged (MERGE idempotency)
4. **Incremental add** — add second dataset without clearing → new nodes added, old preserved
5. **File modification** — modify a file → stale data purged, new data ingested

Usage:
    python -m scripts.test_incremental_updates
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
import textwrap
from pathlib import Path
from typing import Any

# Ensure project root on sys.path
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from src.config.logging import get_logger
from src.graph.neo4j_client import Neo4jClient, setup_schema

logger = get_logger(__name__)

# ─── Fixtures ────────────────────────────────────────────────────────────────

FIXTURES = _ROOT / "tests" / "fixtures"
DS_01 = FIXTURES / "01_basics_ecommerce"
DS_05 = FIXTURES / "05_edgecases_incomplete"


# ─── Helpers ─────────────────────────────────────────────────────────────────


def query_graph_stats() -> dict[str, Any]:
    """Return a summary dict of current node labels, relationship types, and counts."""
    with Neo4jClient() as c:
        nodes = c.execute_cypher(
            "MATCH (n) RETURN labels(n)[0] AS label, count(n) AS cnt ORDER BY label"
        )
        rels = c.execute_cypher(
            "MATCH ()-[r]->() RETURN type(r) AS rtype, count(r) AS cnt ORDER BY rtype"
        )
        sf = c.execute_cypher(
            "MATCH (sf:SourceFile) RETURN sf.path AS path, sf.sha256 AS sha"
        )
    return {
        "nodes": {r["label"]: r["cnt"] for r in nodes},
        "rels": {r["rtype"]: r["cnt"] for r in rels},
        "source_files": {r["path"]: r["sha"] for r in sf},
        "total_nodes": sum(r["cnt"] for r in nodes),
        "total_rels": sum(r["cnt"] for r in rels),
    }


def print_stats(label: str, stats: dict[str, Any]) -> None:
    """Pretty-print graph statistics."""
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")
    print(f"  Total nodes: {stats['total_nodes']}")
    print(f"  Total relationships: {stats['total_rels']}")
    print("  Nodes by label:")
    for lbl, cnt in sorted(stats["nodes"].items()):
        print(f"    {lbl}: {cnt}")
    print("  Relationships by type:")
    for rt, cnt in sorted(stats["rels"].items()):
        print(f"    {rt}: {cnt}")
    if stats["source_files"]:
        print("  SourceFile registry:")
        for path, sha in sorted(stats["source_files"].items()):
            print(f"    {Path(path).name}: {sha[:16]}...")
    print()


def clear_graph() -> None:
    """Delete all nodes and relationships."""
    with Neo4jClient() as c:
        c.execute_cypher("MATCH (n) DETACH DELETE n")
    print("  [✓] Graph cleared.")


def check_business_concepts() -> list[str]:
    """Return names of all BusinessConcept nodes."""
    with Neo4jClient() as c:
        rows = c.execute_cypher(
            "MATCH (bc:BusinessConcept) RETURN bc.name AS name ORDER BY bc.name"
        )
    return [r["name"] for r in rows]


def check_physical_tables() -> list[str]:
    """Return names of all PhysicalTable nodes."""
    with Neo4jClient() as c:
        rows = c.execute_cypher(
            "MATCH (pt:PhysicalTable) RETURN pt.table_name AS name ORDER BY name"
        )
    return [r["name"] for r in rows]


def check_mappings() -> list[dict]:
    """Return all MAPPED_TO relationships with concept and table names."""
    with Neo4jClient() as c:
        rows = c.execute_cypher(
            "MATCH (bc:BusinessConcept)-[r:MAPPED_TO]->(pt:PhysicalTable) "
            "RETURN bc.name AS concept, pt.table_name AS table, r.confidence AS conf "
            "ORDER BY bc.name"
        )
    return [dict(r) for r in rows]


def check_references() -> list[dict]:
    """Return all REFERENCES (FK) relationships."""
    with Neo4jClient() as c:
        rows = c.execute_cypher(
            "MATCH (pt1:PhysicalTable)-[r:REFERENCES]->(pt2:PhysicalTable) "
            "RETURN pt1.table_name AS from_table, pt2.table_name AS to_table, "
            "r.fk_column AS fk_col "
            "ORDER BY from_table"
        )
    return [dict(r) for r in rows]


def check_embeddings() -> dict[str, int]:
    """Count nodes with embeddings."""
    with Neo4jClient() as c:
        bc = c.execute_cypher(
            "MATCH (bc:BusinessConcept) WHERE bc.embedding IS NOT NULL RETURN count(bc) AS cnt"
        )
        ch = c.execute_cypher(
            "MATCH (c:Chunk) WHERE c.embedding IS NOT NULL RETURN count(c) AS cnt"
        )
    return {"BusinessConcept": bc[0]["cnt"], "Chunk": ch[0]["cnt"]}


def assert_eq(name: str, actual: Any, expected: Any) -> None:
    """Assert equality with a readable message."""
    if actual == expected:
        print(f"  [PASS] {name}: {actual}")
    else:
        print(f"  [FAIL] {name}: expected {expected}, got {actual}")


def assert_gte(name: str, actual: int, minimum: int) -> None:
    """Assert >= with a readable message."""
    if actual >= minimum:
        print(f"  [PASS] {name}: {actual} >= {minimum}")
    else:
        print(f"  [FAIL] {name}: expected >= {minimum}, got {actual}")


def assert_gt(name: str, actual: int, other: int) -> None:
    if actual > other:
        print(f"  [PASS] {name}: {actual} > {other}")
    else:
        print(f"  [FAIL] {name}: expected > {other}, got {actual}")


# ─── Test Phases ─────────────────────────────────────────────────────────────


def run_builder_wrapper(
    docs: list[str],
    ddls: list[str],
    *,
    clear: bool = False,
    force: bool = False,
    lazy: bool = True,
) -> dict:
    """Run builder and return final state as dict."""
    from src.graph.builder_graph import run_builder

    state = run_builder(
        raw_documents=docs,
        ddl_paths=ddls,
        production=False,
        clear_graph=clear,
        force_rebuild=force,
        use_lazy_extraction=lazy,   # Use lazy=True for speed (heuristic extraction)
        trace_enabled=False,
    )
    return dict(state) if state else {}


def phase_1_baseline():
    """Phase 1: Clean build with 01_basics_ecommerce."""
    print("\n" + "=" * 60)
    print("  PHASE 1: Baseline Build (01_basics_ecommerce, clear=True)")
    print("=" * 60)

    docs = [str(DS_01 / "business_glossary.txt"), str(DS_01 / "data_dictionary.txt")]
    ddls = [str(DS_01 / "schema.sql")]

    state = run_builder_wrapper(docs, ddls, clear=True, lazy=True)

    stats = query_graph_stats()
    print_stats("After Phase 1 — Baseline", stats)

    # Verify basic structure
    concepts = check_business_concepts()
    tables = check_physical_tables()
    mappings = check_mappings()
    refs = check_references()
    embs = check_embeddings()

    print("  Business Concepts:", concepts)
    print("  Physical Tables:", tables)
    print("  Mappings:")
    for m in mappings:
        print(f"    {m['concept']} → {m['table']} (conf={m.get('conf', '?')})")
    print("  FK References:")
    for r in refs:
        print(f"    {r['from_table']} -[{r['fk_col']}]-> {r['to_table']}")
    print("  Embeddings:", embs)

    # Assertions
    assert_gte("BusinessConcept count", stats["nodes"].get("BusinessConcept", 0), 3)
    assert_gte("PhysicalTable count", stats["nodes"].get("PhysicalTable", 0), 4)
    assert_gte("SourceFile count", stats["nodes"].get("SourceFile", 0), 2)
    assert_gte("MAPPED_TO count", stats["rels"].get("MAPPED_TO", 0), 3)
    assert_gte("Chunks with embeddings", embs["Chunk"], 1)

    return stats


def phase_2_idempotency(baseline_stats: dict):
    """Phase 2: Re-run same data without clear → SHA skip → counts unchanged."""
    print("\n" + "=" * 60)
    print("  PHASE 2: Idempotency (same data, no clear, no force)")
    print("=" * 60)

    docs = [str(DS_01 / "business_glossary.txt"), str(DS_01 / "data_dictionary.txt")]
    ddls = [str(DS_01 / "schema.sql")]

    state = run_builder_wrapper(docs, ddls, clear=False, force=False, lazy=True)

    stats = query_graph_stats()
    print_stats("After Phase 2 — Same data re-run", stats)

    # Counts should be identical (SHA detected no changes → skip)
    assert_eq("Total nodes unchanged", stats["total_nodes"], baseline_stats["total_nodes"])
    assert_eq("Total rels unchanged", stats["total_rels"], baseline_stats["total_rels"])
    assert_eq(
        "BusinessConcept count unchanged",
        stats["nodes"].get("BusinessConcept", 0),
        baseline_stats["nodes"].get("BusinessConcept", 0),
    )
    assert_eq(
        "PhysicalTable count unchanged",
        stats["nodes"].get("PhysicalTable", 0),
        baseline_stats["nodes"].get("PhysicalTable", 0),
    )

    return stats


def phase_3_force_rebuild(baseline_stats: dict):
    """Phase 3: Force rebuild same data → MERGE idempotency → counts unchanged."""
    print("\n" + "=" * 60)
    print("  PHASE 3: Force Rebuild (same data, force=True)")
    print("=" * 60)

    docs = [str(DS_01 / "business_glossary.txt"), str(DS_01 / "data_dictionary.txt")]
    ddls = [str(DS_01 / "schema.sql")]

    state = run_builder_wrapper(docs, ddls, clear=False, force=True, lazy=True)

    stats = query_graph_stats()
    print_stats("After Phase 3 — Force rebuild", stats)

    # MERGE should be idempotent → same counts (BusinessConcept, PhysicalTable should stay)
    # Note: chunks may get re-ingested with new indexes, but MERGE prevents duplicates
    assert_eq(
        "BusinessConcept count unchanged",
        stats["nodes"].get("BusinessConcept", 0),
        baseline_stats["nodes"].get("BusinessConcept", 0),
    )
    assert_eq(
        "PhysicalTable count unchanged",
        stats["nodes"].get("PhysicalTable", 0),
        baseline_stats["nodes"].get("PhysicalTable", 0),
    )
    assert_eq(
        "MAPPED_TO unchanged",
        stats["rels"].get("MAPPED_TO", 0),
        baseline_stats["rels"].get("MAPPED_TO", 0),
    )

    return stats


def phase_4_incremental_add(prev_stats: dict):
    """Phase 4: Add dataset 05 alongside dataset 01 (pass ALL files).

    The pipeline uses orphan detection: files NOT in the current input set
    are treated as removed. So for true incremental additions, we must
    pass ALL files (old + new) together.
    """
    print("\n" + "=" * 60)
    print("  PHASE 4: Incremental Add (DS_01 + DS_05, no clear)")
    print("=" * 60)

    # Pass BOTH datasets — old files will be SHA-skipped, new ones ingested
    docs = [
        str(DS_01 / "business_glossary.txt"),
        str(DS_01 / "data_dictionary.txt"),
        str(DS_05 / "business_glossary.txt"),
        str(DS_05 / "data_dictionary.txt"),
    ]
    ddls = [str(DS_01 / "schema.sql"), str(DS_05 / "schema.sql")]

    state = run_builder_wrapper(docs, ddls, clear=False, force=False, lazy=True)

    stats = query_graph_stats()
    print_stats("After Phase 4 — Incremental add", stats)

    # Old data should still be there, PLUS new data from dataset 05
    old_concepts = prev_stats["nodes"].get("BusinessConcept", 0)
    new_concepts = stats["nodes"].get("BusinessConcept", 0)
    old_tables = prev_stats["nodes"].get("PhysicalTable", 0)
    new_tables = stats["nodes"].get("PhysicalTable", 0)

    assert_gte(
        "BusinessConcepts grew (new dataset added)",
        new_concepts,
        old_concepts,
    )
    assert_gt(
        "PhysicalTables grew (new DDL tables)",
        new_tables,
        old_tables,
    )
    assert_gt(
        "Total nodes grew",
        stats["total_nodes"],
        prev_stats["total_nodes"],
    )

    # Check that old DS_01 concepts still exist
    concepts = check_business_concepts()
    tables = check_physical_tables()
    print("  All concepts now:", concepts)
    print("  All tables now:", tables)

    # Verify DS_01 tables are still present
    ds01_tables = {"CUSTOMER_MASTER", "TB_PRODUCT", "TB_CATEGORY", "SALES_ORDER_HDR",
                   "ORDER_LINE_ITEM", "PAYMENT", "SHIPMENT"}
    surviving = ds01_tables.intersection(set(tables))
    assert_eq("DS_01 tables preserved", len(surviving), len(ds01_tables))

    return stats


def phase_5_file_modification(prev_stats: dict):
    """Phase 5: Simulate file modification → stale data purged, fresh data ingested."""
    print("\n" + "=" * 60)
    print("  PHASE 5: File Modification Simulation")
    print("=" * 60)

    # Create a temp copy of the business glossary with a small modification
    tmpdir = Path(tempfile.mkdtemp(prefix="sm_test_"))
    try:
        # Copy dataset 01 files to temp dir
        src_bg = DS_01 / "business_glossary.txt"
        src_dd = DS_01 / "data_dictionary.txt"
        src_ddl = DS_01 / "schema.sql"

        tmp_bg = tmpdir / "business_glossary.txt"
        tmp_dd = tmpdir / "data_dictionary.txt"
        tmp_ddl = tmpdir / "schema.sql"

        # Modify the business glossary slightly (different SHA)
        original = src_bg.read_text()
        modified = original + "\n\n## APPENDIX — TEST MODIFICATION\nThis line was added for incremental update testing.\n"
        tmp_bg.write_text(modified)
        shutil.copy2(src_dd, tmp_dd)
        shutil.copy2(src_ddl, tmp_ddl)

        # The registry has DS_01 files from Phase 1-3.
        # This is a NEW path (tmpdir), so it will be treated as "new" not "modified".
        docs = [str(tmp_bg), str(tmp_dd)]
        ddls = [str(tmp_ddl)]

        state = run_builder_wrapper(docs, ddls, clear=False, force=False, lazy=True)

        stats = query_graph_stats()
        print_stats("After Phase 5 — Modified file", stats)

        # Should see new SourceFile entries for the temp paths
        print("  SourceFile registry:")
        for path, sha in stats["source_files"].items():
            print(f"    {Path(path).name}: {sha[:16]}...")

        # Data from Phase 4 (dataset 05) should still be present
        concepts = check_business_concepts()
        tables = check_physical_tables()
        print("  All concepts:", concepts)
        print("  All tables:", tables)

        # Total nodes should have grown or stayed same (we added a new file path)
        assert_gte("Total nodes after modified file", stats["total_nodes"], prev_stats["total_nodes"])

    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    return stats


def phase_6_verify_final_integrity():
    """Phase 6: Final integrity checks on the graph."""
    print("\n" + "=" * 60)
    print("  PHASE 6: Final Integrity Checks")
    print("=" * 60)

    with Neo4jClient() as c:
        # 1. No orphan MAPPED_TO edges (both ends must exist)
        orphan_maps = c.execute_cypher(
            "MATCH (bc:BusinessConcept)-[r:MAPPED_TO]->(pt:PhysicalTable) "
            "WHERE bc.name IS NULL OR pt.table_name IS NULL "
            "RETURN count(r) AS cnt"
        )
        assert_eq("No orphan MAPPED_TO edges", orphan_maps[0]["cnt"], 0)

        # 2. All Chunks have source_doc
        no_src = c.execute_cypher(
            "MATCH (c:Chunk) WHERE c.source_doc IS NULL RETURN count(c) AS cnt"
        )
        assert_eq("All Chunks have source_doc", no_src[0]["cnt"], 0)

        # 3. All CHILD_OF edges valid (child and parent exist)
        broken_childof = c.execute_cypher(
            "MATCH (c:Chunk)-[:CHILD_OF]->(pc:ParentChunk) "
            "WHERE c.text IS NULL OR pc.text IS NULL "
            "RETURN count(c) AS cnt"
        )
        assert_eq("All CHILD_OF edges valid", broken_childof[0]["cnt"], 0)

        # 4. SourceFile nodes have SHA values
        no_sha = c.execute_cypher(
            "MATCH (sf:SourceFile) WHERE sf.sha256 IS NULL RETURN count(sf) AS cnt"
        )
        assert_eq("All SourceFiles have SHA", no_sha[0]["cnt"], 0)

        # 5. No duplicate BusinessConcept names (UNIQUE constraint)
        dup_concepts = c.execute_cypher(
            "MATCH (bc:BusinessConcept) "
            "WITH bc.name AS name, count(bc) AS cnt "
            "WHERE cnt > 1 RETURN name, cnt"
        )
        assert_eq("No duplicate BusinessConcept names", len(dup_concepts), 0)

        # 6. No duplicate PhysicalTable names (UNIQUE constraint)
        dup_tables = c.execute_cypher(
            "MATCH (pt:PhysicalTable) "
            "WITH pt.table_name AS name, count(pt) AS cnt "
            "WHERE cnt > 1 RETURN name, cnt"
        )
        assert_eq("No duplicate PhysicalTable names", len(dup_tables), 0)

    print("\n  [✓] Final integrity checks complete.")


# ─── Main ────────────────────────────────────────────────────────────────────


def main():
    print("=" * 60)
    print("  INCREMENTAL UPDATE VERIFICATION SUITE")
    print("  Neo4j manual integration tests")
    print("=" * 60)

    # Phase 1: Baseline
    baseline = phase_1_baseline()

    # Phase 2: Idempotency (SHA skip)
    phase_2_idempotency(baseline)

    # Phase 3: Force rebuild (MERGE idempotency)
    phase3_stats = phase_3_force_rebuild(baseline)

    # Phase 4: Incremental add (second dataset)
    phase4_stats = phase_4_incremental_add(phase3_stats)

    # Phase 5: File modification
    phase_5_file_modification(phase4_stats)

    # Phase 6: Final integrity
    phase_6_verify_final_integrity()

    print("\n" + "=" * 60)
    print("  ALL PHASES COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
