"""Import OWL 2 DL files/text into the Neo4j Knowledge Graph.

Strategies:
  clean     — clear graph, then MERGE all nodes+edges (like kg_registry load).
  versioned — snapshot the live graph first (rollback backup via kg_registry),
              then clear + MERGE.
  merge     — MERGE only, no clear (incremental; MERGE is idempotent).

Note: Neo4j Community (Docker neo4j:5) has no named-graph/fabric support, so a
true "versioned graph" is impossible. The rollback safety the user wants is
delivered by an auto-snapshot instead — same external contract.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal

from src.config.logging import get_logger
from src.graph.neo4j_client import Neo4jClient, setup_schema
from src.graph.owl_mapper import from_owl_documents

logger = get_logger(__name__)

Strategy = Literal["clean", "versioned", "merge"]

_ALLOWED_RELS = frozenset(
    {"MAPPED_TO", "HAS_ATTRIBUTE", "HAS_COLUMN", "REFERENCES", "MENTIONS",
     "DESCRIBED_BY", "PART_OF", "INSTANCE_OF", "CONTAINS_CHUNK", "CHILD_OF"}
)

# ponytail: the node/edge → MERGE builders below mirror kg_registry._import_graph.
# A future refactor could extract a shared graph_merge() into kg_registry; left
# duplicated here to avoid coupling OWL import to kg_registry internals and to
# not disturb the 530 passing tests.


def _node_identity(node: dict) -> tuple[str, dict, tuple[str, ...]] | None:
    """Return (cypher_match_fragment, params, identity_prop_names) for MERGE.

    identity_prop_names are the node props the MERGE keys on — excluded from the
    subsequent SET so they aren't redundantly re-written (matches kg_registry).
    """
    labels = node.get("labels", [])
    props = node.get("props", {})
    if "BusinessConcept" in labels and props.get("name"):
        return "(n:BusinessConcept {name: $key})", {"key": props["name"]}, ("name",)
    if "PhysicalTable" in labels and props.get("table_name"):
        return "(n:PhysicalTable {table_name: $key})", {"key": props["table_name"]}, ("table_name",)
    if "Attribute" in labels and props.get("name"):
        return "(n:Attribute {name: $key})", {"key": props["name"]}, ("name",)
    if "Chunk" in labels and props.get("chunk_index") is not None:
        return ("(n:Chunk {chunk_index: $idx, source_doc: $src})",
                {"idx": props["chunk_index"], "src": props.get("source_doc", "")},
                ("chunk_index", "source_doc"))
    if "ParentChunk" in labels and props.get("parent_chunk_index") is not None:
        return ("(n:ParentChunk {parent_chunk_index: $idx, source_doc: $src})",
                {"idx": props["parent_chunk_index"], "src": props.get("source_doc", "")},
                ("parent_chunk_index", "source_doc"))
    if "SourceFile" in labels and props.get("path"):
        return "(n:SourceFile {path: $key})", {"key": props["path"]}, ("path",)
    return None


def _build_node_statements(nodes: list[dict]) -> list[tuple[str, dict]]:
    stmts: list[tuple[str, dict]] = []
    for node in nodes:
        ident = _node_identity(node)
        if ident is None:
            continue
        match_frag, ident_params, ident_prop_names = ident
        props = {k: v for k, v in node["props"].items()
                 if k not in ident_prop_names and k != "embedding"}
        stmts.append((f"MERGE {match_frag} SET n += $props",
                      {**ident_params, "props": props}))
    return stmts


def _alias_identity(fragment: str, params: dict, letter: str) -> tuple[str, dict]:
    """Rewrite a node-identity fragment+params to alias <letter> and namespaced $params.

    Prevents param collisions when two endpoints of an edge use the same generic
    param name (e.g. both single-key nodes use ``$key``).

    Constraint: no param name may be a prefix of another (e.g. ``$s`` and
    ``$src``), or the substring replace would corrupt the longer name. Current
    identity params (key/idx/src) satisfy this — keep it that way when adding
    new node identities.
    """
    new_frag = fragment.replace("n:", f"{letter}:").replace("(n", f"({letter}")
    new_params: dict = {}
    for k, v in params.items():
        namespaced = f"{letter}_{k}"
        new_frag = new_frag.replace(f"${k}", f"${namespaced}")
        new_params[namespaced] = v
    return new_frag, new_params


def _merge_graph(
    client: Neo4jClient,
    nodes: list[dict],
    edges: list[dict],
    *,
    clear: bool,
) -> tuple[int, int]:
    """Write nodes+edges via MERGE. Returns (nodes_merged, rels_merged)."""
    if clear:
        client.execute_cypher("MATCH (n) DETACH DELETE n")
        setup_schema(client)

    node_stmts = _build_node_statements(nodes)
    for i in range(0, len(node_stmts), 200):
        client.execute_batch(node_stmts[i: i + 200])

    # eid → identity (fragment, params, prop_names) for relationship wiring
    eid_identity: dict[str, tuple[str, dict, tuple[str, ...]]] = {}
    for node in nodes:
        ident = _node_identity(node)
        if ident:
            eid_identity[node.get("eid", "")] = ident

    rel_stmts: list[tuple[str, dict]] = []
    for edge in edges:
        rel_type = edge.get("rel_type")
        if rel_type not in _ALLOWED_RELS:
            logger.warning("Skipping unknown relationship type '%s' on import.", rel_type)
            continue
        src = eid_identity.get(edge.get("start_eid", ""))
        tgt = eid_identity.get(edge.get("end_eid", ""))
        if not src or not tgt:
            continue
        # Namespace each side's alias AND params so two single-key endpoints
        # (both using $key) don't collide when merged into one param dict.
        src_frag, src_p = _alias_identity(src[0], src[1], "a")
        tgt_frag, tgt_p = _alias_identity(tgt[0], tgt[1], "b")
        cypher = (f"MATCH {src_frag} MATCH {tgt_frag} "
                  f"MERGE (a)-[r:`{rel_type}`]->(b) SET r += $props")
        params = {**src_p, **tgt_p, "props": edge.get("props", {})}
        rel_stmts.append((cypher, params))

    for i in range(0, len(rel_stmts), 200):
        client.execute_batch(rel_stmts[i: i + 200])
    return len(node_stmts), len(rel_stmts)


def import_from_owl_text(text: str | list[str], strategy: Strategy) -> dict[str, Any]:
    """Parse OWL XML (single document or list of documents) and import into Neo4j.

    A single ``str`` is one OWL document; a ``list[str]`` is multiple documents
    (e.g. the 4 files of an export) which are parsed separately and merged.
    """
    if strategy not in ("clean", "versioned", "merge"):
        raise ValueError("unsupported_strategy: use one of clean|versioned|merge")

    texts = [text] if isinstance(text, str) else text
    nodes, edges = from_owl_documents(texts) if texts else ([], [])
    backup_id: str | None = None

    if strategy == "versioned":
        from src.graph.kg_registry import save_snapshot
        ts = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        snap = save_snapshot(name=f"pre-owl-import-{ts}",
                             description="auto-backup before OWL import")
        backup_id = snap["id"]

    with Neo4jClient() as client:
        nodes_merged, rels_merged = _merge_graph(
            client, nodes, edges, clear=(strategy != "merge")
        )

    result: dict[str, Any] = {
        "strategy": strategy,
        "nodes_merged": nodes_merged,
        "relationships_merged": rels_merged,
        "backup_snapshot_id": backup_id,
    }
    logger.info("OWL import (%s): %d nodes, %d rels.", strategy, nodes_merged, rels_merged)
    return result
