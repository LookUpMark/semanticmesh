"""Deterministic parameterized Cypher builder for Neo4j upserts.

Generates MERGE-based Cypher with ``$parameter`` placeholders so that all
string values (DDL source, column names, definitions with embedded quotes, etc.)
are handled safely by the Neo4j driver without manual escaping.

This complements the LLM-based :mod:`cypher_generator` (which is used for the
self-reflection demonstration in the thesis) and is used as the actual upsert
executor in the Builder Graph node, making graph writes reliable regardless of
LLM output quality.
"""

from __future__ import annotations

import json

from src.models.schemas import EnrichedTableSchema, Entity, MappingProposal
from src.utils.text_utils import normalize_concept_name

_UPSERT_CYPHER = """\
MERGE (bc:BusinessConcept {name: $concept_name})
ON CREATE SET bc.definition = $definition,
              bc.mapping_reasoning = $mapping_reasoning,
              bc.provenance_text = $provenance_text,
              bc.source_doc = $source_doc,
              bc.synonyms = $synonyms,
              bc.confidence_score = $confidence_score,
              bc.created_at = datetime()
ON MATCH SET  bc.definition = $definition,
              bc.mapping_reasoning = $mapping_reasoning,
              bc.confidence_score = $confidence_score,
              bc.updated_at = datetime()

MERGE (pt:PhysicalTable {table_name: $table_name})
ON CREATE SET pt.schema_name = $schema_name,
              pt.column_names = $column_names,
              pt.column_types = $column_types,
              pt.ddl_source = $ddl_source,
              pt.source_file = $source_file,
              pt.created_at = datetime()
ON MATCH SET  pt.ddl_source = $ddl_source,
              pt.source_file = $source_file,
              pt.updated_at = datetime()

MERGE (bc)-[r:MAPPED_TO]->(pt)
ON CREATE SET r.confidence = $confidence,
              r.validated_by = 'llm_judge',
              r.created_at = datetime()
ON MATCH SET  r.confidence = $confidence,
              r.updated_at = datetime()
"""


def build_upsert_cypher(
    proposal: MappingProposal,
    table: EnrichedTableSchema,
    entity: Entity | None = None,
) -> tuple[str, dict]:
    """Build a parameterized MERGE Cypher and a params dict.

    Args:
        proposal: The validated :class:`~src.models.schemas.MappingProposal`.
        table:    The :class:`~src.models.schemas.EnrichedTableSchema` for the
                  table being mapped.
        entity:   Optional resolved :class:`~src.models.schemas.Entity` — when
                  provided its ``definition``, ``provenance_text``,
                  ``source_doc`` and ``synonyms`` are propagated to the graph
                  node.

    Returns:
        A ``(cypher_template, params)`` tuple ready for
        ``Neo4jClient.execute_cypher(cypher, params)``.
    """
    column_names = [c.name for c in table.columns]
    column_types = json.dumps({c.name: c.data_type for c in table.columns})

    params: dict = {
        "concept_name": normalize_concept_name(proposal.mapped_concept or "Unknown"),
        "definition": entity.definition if entity else "",
        "mapping_reasoning": proposal.reasoning or "",
        "provenance_text": entity.provenance_text if entity else "",
        "source_doc": entity.source_doc if entity else "",
        "synonyms": entity.synonyms if entity else [],
        "confidence_score": proposal.confidence,
        "table_name": table.table_name,
        "schema_name": table.schema_name,
        "column_names": column_names,
        "column_types": column_types,
        "ddl_source": table.ddl_source or "",
        "source_file": table.source_file or "",
        "confidence": proposal.confidence,
    }
    return _UPSERT_CYPHER, params


_FK_CYPHER = """\
MERGE (src:PhysicalTable {table_name: $src_table})
MERGE (tgt:PhysicalTable {table_name: $tgt_table})
MERGE (src)-[r:REFERENCES {column: $fk_column}]->(tgt)
ON CREATE SET r.references_column = $ref_column, r.created_at = datetime()
"""


def build_fk_cypher(table: EnrichedTableSchema) -> list[tuple[str, dict]]:
    """Build REFERENCES edge statements for every FK column in a table.

    Creates stub ``PhysicalTable`` nodes for referenced tables if they do not
    yet exist; the stub will be fully populated when that table is processed.

    Args:
        table: The enriched table whose FK columns should be wired.

    Returns:
        A list of ``(cypher, params)`` tuples — one per FK column.
        Returns an empty list if the table has no FK columns.
    """
    statements: list[tuple[str, dict]] = []
    for col in table.columns:
        if col.is_foreign_key and col.references:
            parts = col.references.split(".", 1)
            tgt_table = parts[0]
            ref_column = parts[1] if len(parts) > 1 else ""
            statements.append(
                (
                    _FK_CYPHER,
                    {
                        "src_table": table.table_name,
                        "tgt_table": tgt_table,
                        "fk_column": col.name,
                        "ref_column": ref_column,
                    },
                )
            )
    return statements
