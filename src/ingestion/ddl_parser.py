"""Deterministic SQL DDL parser using sqlglot.

EP-05: Converts raw SQL DDL text into structured TableSchema objects.
No LLM involved. Supports mysql, postgres, tsql, oracle dialects.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

import sqlglot
import sqlglot.expressions as exp

from src.config.logging import get_logger
from src.models.schemas import ColumnSchema, TableSchema

if TYPE_CHECKING:
    import logging
    from pathlib import Path

logger: logging.Logger = get_logger(__name__)


class DDLParseError(Exception):
    """Raised when DDL cannot be parsed into at least one TableSchema."""


def _normalise_type(data_type: str) -> str:
    """Strip length/precision details for cleaner stored types.

    Examples:
        "VARCHAR(200)" → "VARCHAR"
        "DECIMAL(10,2)" → "DECIMAL"
        "BIGINT" → "BIGINT"
    """
    return re.sub(r"\(.*\)", "", data_type).strip().upper()


def _extract_table(create_expr: exp.Create, ddl_source: str) -> TableSchema | None:
    """Extract a single TableSchema from a parsed CREATE TABLE expression.

    Returns None if the expression is not a CREATE TABLE or has no columns.
    """
    # Only handle CREATE TABLE (not CREATE INDEX, VIEW, etc.)
    if create_expr.args.get("kind", "").upper() != "TABLE":
        return None

    table_ref = create_expr.find(exp.Table)
    if table_ref is None:
        return None

    table_name: str = table_ref.name.upper()
    schema_name: str | None = table_ref.db.upper() if table_ref.db else None

    # Collect all primary key column names declared inline or via table constraint
    pk_columns: set[str] = set()
    schema_def = create_expr.find(exp.Schema)
    if schema_def is None:
        return None

    for constraint in schema_def.find_all(exp.PrimaryKey):
        for col in constraint.find_all(exp.Column):
            pk_columns.add(col.name.upper())

    # Build ColumnSchema list
    columns: list[ColumnSchema] = []
    for col_def in schema_def.find_all(exp.ColumnDef):
        col_name = col_def.name.upper()
        data_type_expr = col_def.find(exp.DataType)
        data_type = _normalise_type(str(data_type_expr)) if data_type_expr else "UNKNOWN"

        is_pk = col_name in pk_columns
        is_fk = False
        references: str | None = None

        # Inline PRIMARY KEY constraint
        for col_constraint in col_def.find_all(exp.ColumnConstraint):
            kind = col_constraint.args.get("kind")
            if isinstance(kind, exp.PrimaryKeyColumnConstraint):
                is_pk = True
            if isinstance(kind, exp.Reference):
                is_fk = True
                ref_table = kind.find(exp.Table)
                ref_col = kind.find(exp.Column)
                if ref_table and ref_col:
                    references = f"{ref_table.name.upper()}.{ref_col.name.upper()}"

        columns.append(
            ColumnSchema(
                name=col_name,
                data_type=data_type,
                is_primary_key=is_pk,
                is_foreign_key=is_fk,
                references=references,
            )
        )

    # Table-level FOREIGN KEY constraints
    for fk_constraint in schema_def.find_all(exp.ForeignKey):
        # FK columns are Identifiers in fk_constraint.expressions
        fk_cols = [
            e.name.upper() if hasattr(e, "name") else str(e.this).upper()
            for e in fk_constraint.expressions
        ]
        reference = fk_constraint.find(exp.Reference)
        if reference:
            ref_table = reference.find(exp.Table)
            ref_schema = reference.find(exp.Schema)
            # Referenced columns are Identifiers in the Schema's expressions
            ref_cols = (
                [
                    e.name.upper() if hasattr(e, "name") else str(e.this).upper()
                    for e in ref_schema.expressions
                ]
                if ref_schema
                else []
            )
            for i, fk_col_name in enumerate(fk_cols):
                for column_schema in columns:
                    if column_schema.name == fk_col_name:
                        column_schema.is_foreign_key = True
                        if ref_table and i < len(ref_cols):
                            column_schema.references = f"{ref_table.name.upper()}.{ref_cols[i]}"

    if not columns:
        logger.warning("Table '%s' has no parseable columns — skipping.", table_name)
        return None

    return TableSchema(
        table_name=table_name,
        schema_name=schema_name,
        columns=columns,
        ddl_source=ddl_source,
    )


def parse_ddl(ddl_text: str, dialect: str = "mysql") -> list[TableSchema]:
    """Parse all CREATE TABLE statements in a DDL text block.

    Args:
        ddl_text: Raw SQL DDL containing one or more CREATE TABLE statements.
        dialect: sqlglot dialect for parsing. Options: "mysql", "postgres",
                 "tsql", "oracle". Defaults to "mysql" (most permissive).

    Returns:
        List of ``TableSchema`` objects, one per CREATE TABLE statement found.

    Raises:
        DDLParseError: If no CREATE TABLE statements could be parsed.
    """
    try:
        statements = sqlglot.parse(ddl_text, dialect=dialect, error_level=sqlglot.ErrorLevel.WARN)
    except Exception as exc:
        raise DDLParseError(f"sqlglot failed to tokenise DDL: {exc}") from exc

    tables: list[TableSchema] = []
    for stmt in statements:
        if stmt is None:
            continue
        if not isinstance(stmt, exp.Create):
            continue
        # Use the statement's own SQL string as ddl_source
        table_ddl_source = stmt.sql(dialect=dialect)
        schema = _extract_table(stmt, ddl_source=table_ddl_source)
        if schema is not None:
            tables.append(schema)
            logger.debug("Parsed table '%s' (%d columns)", schema.table_name, len(schema.columns))

    if not tables:
        raise DDLParseError("No CREATE TABLE statements could be parsed from the input DDL.")

    logger.info("Parsed %d table(s) from DDL input.", len(tables))
    return tables


def parse_ddl_file(path: Path, dialect: str = "mysql") -> list[TableSchema]:
    """Load a .sql file and parse it with ``parse_ddl``.

    Args:
        path: Path to the SQL file.
        dialect: sqlglot dialect.

    Returns:
        List of ``TableSchema`` objects.

    Raises:
        FileNotFoundError: If the file does not exist.
        DDLParseError: propagated from ``parse_ddl``.
    """
    if not path.exists():
        raise FileNotFoundError(f"DDL file not found: {path}")
    ddl_text = path.read_text(encoding="utf-8")
    return parse_ddl(ddl_text, dialect=dialect)
