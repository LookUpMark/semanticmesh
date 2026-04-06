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


# ── DDL Pre-strip ──────────────────────────────────────────────────────────────

# Matches CREATE FUNCTION / PROCEDURE with $$ ... $$ dollar-quoted bodies (PL/pgSQL)
_DOLLAR_BODY_RE = re.compile(
    r"CREATE\s+(?:OR\s+REPLACE\s+)?(?:FUNCTION|PROCEDURE)\b[^;]*?\$\$.*?\$\$[^;]*;",
    re.IGNORECASE | re.DOTALL,
)

# Matches CREATE TRIGGER (may span multiple lines until a final semicolon)
_TRIGGER_RE = re.compile(
    r"CREATE\s+(?:OR\s+REPLACE\s+)?TRIGGER\b[^;]*;",
    re.IGNORECASE | re.DOTALL,
)

# Matches CREATE TYPE ... AS ENUM (...); — captures type name for later replacement
_TYPE_RE = re.compile(
    r"CREATE\s+TYPE\s+(\w+)\b[^;]*;",
    re.IGNORECASE | re.DOTALL,
)

# Matches CREATE [UNIQUE] INDEX statements
_INDEX_RE = re.compile(
    r"CREATE\s+(?:UNIQUE\s+)?INDEX\b[^;]*;",
    re.IGNORECASE | re.DOTALL,
)

# Matches ALTER TABLE statements
_ALTER_RE = re.compile(
    r"\bALTER\s+TABLE\b[^;]*;",
    re.IGNORECASE | re.DOTALL,
)

# Matches standalone COMMENT ON statements
_COMMENT_ON_RE = re.compile(
    r"\bCOMMENT\s+ON\b[^;]*;",
    re.IGNORECASE | re.DOTALL,
)

# Matches GRANT / REVOKE statements (two-sided boundaries to avoid false matches)
_GRANT_RE = re.compile(
    r"(?:\bGRANT\b|\bREVOKE\b)[^;]*;",
    re.IGNORECASE | re.DOTALL,
)

# Matches SET / BEGIN / COMMIT / ROLLBACK utility statements (two-sided boundaries)
_UTILITY_RE = re.compile(
    r"(?:\bSET\b|\bBEGIN\b|\bCOMMIT\b|\bROLLBACK\b)[^;]*;",
    re.IGNORECASE | re.DOTALL,
)

# Matches INSERT INTO statements (may span multiple lines for VALUES)
_INSERT_RE = re.compile(
    r"\bINSERT\s+INTO\b[^;]*;",
    re.IGNORECASE | re.DOTALL,
)

# Matches DROP TABLE / VIEW / INDEX / TYPE etc.
_DROP_RE = re.compile(
    r"\bDROP\s+(?:TABLE|VIEW|INDEX|TYPE|SEQUENCE|FUNCTION|PROCEDURE|TRIGGER)"
    r"\b[^;]*;",
    re.IGNORECASE | re.DOTALL,
)

# Matches CREATE VIEW / SEQUENCE statements
_CREATE_OTHER_RE = re.compile(
    r"CREATE\s+(?:OR\s+REPLACE\s+)?(?:VIEW|SEQUENCE)\b[^;]*;",
    re.IGNORECASE | re.DOTALL,
)

# Matches SQL Server bracket-quoted identifiers: [Group] → "Group"
_BRACKET_IDENT_RE = re.compile(r"\[(\w+)\]")


def _strip_non_table_ddl(ddl_text: str) -> str:
    """Remove non-CREATE-TABLE statements and normalise dialect quirks.

    Processing order:
    1. Normalise SQL Server ``[identifier]`` → ``"identifier"`` (P4).
    2. Collect and strip ``CREATE TYPE`` definitions; replace custom type
       names with ``VARCHAR`` in the remaining DDL (P3).
    3. Strip all other non-CREATE-TABLE statements (P1/P2).
    """
    # ── P4: Bracket notation → standard double-quote identifiers ───────────
    result = _BRACKET_IDENT_RE.sub(r'"\1"', ddl_text)

    # ── P3: Strip CREATE TYPE and replace custom type names with VARCHAR ───
    custom_types: list[str] = []
    for m in _TYPE_RE.finditer(result):
        custom_types.append(m.group(1))
    result = _TYPE_RE.sub("", result)

    for type_name in custom_types:
        # Replace the custom type name used as a column type with VARCHAR.
        # Only match when the name appears as a standalone token (word boundary).
        result = re.sub(rf"\b{re.escape(type_name)}\b", "VARCHAR", result)

    # ── P1/P2: Strip remaining non-CREATE-TABLE statements ────────────────
    for pattern in (
        _DOLLAR_BODY_RE,
        _TRIGGER_RE,
        _INDEX_RE,
        _ALTER_RE,
        _COMMENT_ON_RE,
        _GRANT_RE,
        _UTILITY_RE,
        _INSERT_RE,
        _DROP_RE,
        _CREATE_OTHER_RE,
    ):
        result = pattern.sub("", result)
    return result


# Matches CHECK (...) constraints (possibly nested parens) in DDL source
_CHECK_RE = re.compile(
    r",?\s*CHECK\s*\((?:[^()]*|\((?:[^()]*|\([^()]*\))*\))*\)",
    re.IGNORECASE,
)

# Matches single-quoted string literals inside CHECK values: 'PENDING' → PENDING
_CHECK_QUOTE_RE = re.compile(r"'([^']*)'")


def _strip_check_constraints(ddl_source: str) -> str:
    """Sanitise CHECK constraint clauses in a CREATE TABLE DDL string.

    Single quotes inside CHECK values (e.g. STATUS_CODE IN ('PENDING','DONE'))
    cause Cypher syntax errors if the LLM inlines the ddl_source as a string
    literal.  Instead of removing the constraints entirely (which would lose
    valuable schema semantics like allowed status values), we preserve them
    but strip all single quotes from the enum values:

        CHECK (STATUS_CODE IN ('PENDING','CONFIRMED'))
        → CHECK (STATUS_CODE IN (PENDING,CONFIRMED))

    The unquoted form is safe for Cypher inlining and still lets the KG
    answer questions about allowed column values (e.g. order statuses).
    """

    def _remove_value_quotes(m: re.Match) -> str:
        return _CHECK_QUOTE_RE.sub(r"\1", m.group(0))

    return _CHECK_RE.sub(_remove_value_quotes, ddl_source)


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
    if create_expr.args.get("kind", "").upper() != "TABLE":
        return None

    table_ref = create_expr.find(exp.Table)
    if table_ref is None:
        return None

    table_name: str = table_ref.name.upper()
    schema_name: str | None = table_ref.db.upper() if table_ref.db else None

    pk_columns: set[str] = set()
    schema_def = create_expr.find(exp.Schema)
    if schema_def is None:
        return None

    for constraint in schema_def.find_all(exp.PrimaryKey):
        for col in constraint.find_all(exp.Column):
            pk_columns.add(col.name.upper())

    columns: list[ColumnSchema] = []
    for col_def in schema_def.find_all(exp.ColumnDef):
        col_name = col_def.name.upper()
        data_type_expr = col_def.find(exp.DataType)
        data_type = _normalise_type(str(data_type_expr)) if data_type_expr else "UNKNOWN"

        is_pk = col_name in pk_columns
        is_fk = False
        references: str | None = None

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
    ddl_text = _strip_non_table_ddl(ddl_text)
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
        table_ddl_source = _strip_check_constraints(stmt.sql(dialect=dialect))
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
