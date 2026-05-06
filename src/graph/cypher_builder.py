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
ON MATCH SET  bc.definition = CASE WHEN bc.definition IS NULL OR bc.definition = ''
              THEN $definition ELSE bc.definition END,
              bc.mapping_reasoning = $mapping_reasoning,
              bc.provenance_text = CASE WHEN bc.provenance_text IS NULL
              OR bc.provenance_text = ''
              THEN $provenance_text ELSE bc.provenance_text END,
              bc.source_doc = CASE WHEN bc.source_doc IS NULL
              OR bc.source_doc = ''
              THEN $source_doc ELSE bc.source_doc END,
              bc.synonyms = CASE WHEN bc.synonyms IS NULL
              OR size(bc.synonyms) = 0
              THEN $synonyms ELSE bc.synonyms END,
              bc.confidence_score = $confidence_score,
              bc.updated_at = datetime()

MERGE (pt:PhysicalTable {table_name: $table_name})
ON CREATE SET pt.name = $table_name,
              pt.schema_name = $schema_name,
              pt.column_names = $column_names,
              pt.column_types = $column_types,
              pt.ddl_source = $ddl_source,
              pt.source_file = $source_file,
              pt.comment = $table_comment,
              pt.enriched_table_name = $enriched_table_name,
              pt.table_description = $table_description,
              pt.enriched_columns = $enriched_columns,
              pt.created_at = datetime()
ON MATCH SET  pt.schema_name = CASE WHEN pt.schema_name IS NULL
              THEN $schema_name ELSE pt.schema_name END,
              pt.column_names = CASE WHEN pt.column_names IS NULL
              OR size(pt.column_names) = 0
              THEN $column_names ELSE pt.column_names END,
              pt.column_types = CASE WHEN pt.column_types IS NULL
              OR pt.column_types = ''
              THEN $column_types ELSE pt.column_types END,
              pt.ddl_source = $ddl_source,
              pt.source_file = $source_file,
              pt.comment = CASE WHEN pt.comment IS NULL OR pt.comment = ''
              THEN $table_comment ELSE pt.comment END,
              pt.enriched_table_name = CASE WHEN pt.enriched_table_name IS NULL
              THEN $enriched_table_name ELSE pt.enriched_table_name END,
              pt.table_description = CASE WHEN pt.table_description IS NULL
              OR pt.table_description = ''
              THEN $table_description ELSE pt.table_description END,
              pt.enriched_columns = CASE WHEN pt.enriched_columns IS NULL
              OR pt.enriched_columns = ''
              THEN $enriched_columns ELSE pt.enriched_columns END,
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

    # Build enriched column JSON (list of {original, enriched} dicts)
    enriched_cols_json = ""
    if hasattr(table, "enriched_columns") and table.enriched_columns:
        enriched_cols_json = json.dumps(
            [
                {"original": ec.original_name, "enriched": ec.enriched_name}
                for ec in table.enriched_columns
            ]
        )

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
        "table_comment": table.comment or "",
        "enriched_table_name": getattr(table, "enriched_table_name", None),
        "enriched_columns": enriched_cols_json,
        "table_description": getattr(table, "table_description", None) or "",
        "confidence": proposal.confidence,
    }
    return _UPSERT_CYPHER, params


_FK_CYPHER = """\
MERGE (src:PhysicalTable {table_name: $src_table})
ON CREATE SET src.name = $src_table
MERGE (tgt:PhysicalTable {table_name: $tgt_table})
ON CREATE SET tgt.name = $tgt_table
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


_ATTRIBUTE_CYPHER = """\
MERGE (a:Attribute {name: $attr_name})
ON CREATE SET a.table_name = $table_name,
              a.column_name = $column_name,
              a.data_type = $data_type,
              a.nullable = $nullable,
              a.is_pk = $is_pk,
              a.is_fk = $is_fk,
              a.fk_target = $fk_target,
              a.enriched_name = $enriched_name,
              a.description = $description,
              a.created_at = datetime()
ON MATCH SET  a.data_type = $data_type,
              a.nullable = $nullable,
              a.is_pk = $is_pk,
              a.is_fk = $is_fk,
              a.fk_target = $fk_target,
              a.enriched_name = $enriched_name,
              a.description = $description,
              a.updated_at = datetime()
WITH a
MATCH (pt:PhysicalTable {table_name: $table_name})
MERGE (pt)-[:HAS_COLUMN]->(a)
"""


def build_attribute_cypher(table: EnrichedTableSchema) -> list[tuple[str, dict]]:
    """Build MERGE statements for Attribute nodes (one per column).

    Each column becomes an individually retrievable node in the KG with its own
    embedding, enabling direct vector search for specific columns without
    needing the full DDL parent chunk.

    Args:
        table: The enriched table whose columns should be upserted.

    Returns:
        A list of ``(cypher, params)`` tuples — one per column.
    """
    # Build enriched name lookup
    enriched_map: dict[str, str] = {}
    if table.enriched_columns:
        enriched_map = {ec.original_name: ec.enriched_name for ec in table.enriched_columns}

    statements: list[tuple[str, dict]] = []
    for col in table.columns:
        nullable = not col.is_primary_key and col.name not in _get_not_null_columns(table)
        enriched_name = enriched_map.get(col.name, col.name)
        fk_target = col.references or ""

        # Build description text (used for embedding)
        nullable_str = "nullable" if nullable else "NOT NULL"
        desc = f"{table.table_name}.{col.name} ({col.data_type}, {nullable_str}) — {enriched_name}."
        if table.table_description:
            desc += f" Column in table {table.table_name}: {table.table_description}"

        statements.append(
            (
                _ATTRIBUTE_CYPHER,
                {
                    "attr_name": f"{table.table_name}.{col.name}",
                    "table_name": table.table_name,
                    "column_name": col.name,
                    "data_type": col.data_type,
                    "nullable": nullable,
                    "is_pk": col.is_primary_key,
                    "is_fk": col.is_foreign_key,
                    "fk_target": fk_target,
                    "enriched_name": enriched_name,
                    "description": desc,
                },
            )
        )
    return statements


def _get_not_null_columns(table: EnrichedTableSchema) -> set[str]:
    """Heuristic: columns that are PK or have NOT NULL in DDL source."""
    not_null: set[str] = set()
    ddl = (table.ddl_source or "").upper()
    for col in table.columns:
        if col.is_primary_key:
            not_null.add(col.name)
        elif f"{col.name.upper()} " in ddl:
            # Check if NOT NULL follows the column name in DDL
            idx = ddl.find(col.name.upper())
            if idx >= 0:
                segment = ddl[idx : idx + len(col.name) + 50]
                if "NOT NULL" in segment and "DEFAULT" not in segment.split("NOT NULL")[0][-10:]:
                    not_null.add(col.name)
    return not_null
