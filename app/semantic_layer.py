"""Governed DuckDB semantic layer over final runtime CSVs."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

import duckdb


WHITELISTED_VIEWS = {"city_week_events", "msa_week_events"}
RELATION_PATTERN = re.compile(r"\b(?:from|join)\s+([a-zA-Z_][a-zA-Z0-9_]*)", re.IGNORECASE)


@dataclass(frozen=True)
class SemanticQueryResult:
    """Rows and telemetry for a governed semantic query."""

    sql: str
    referenced_views: list[str]
    columns: list[str]
    rows: list[dict[str, object]]
    row_count: int
    row_preview: list[dict[str, object]]

    def to_dict(self) -> dict[str, object]:
        """Return JSON-serializable query result."""
        return asdict(self)


class SemanticLayerError(ValueError):
    """Raised when semantic SQL violates guardrails."""


class SemanticLayer:
    """Small governed DuckDB query surface."""

    def __init__(self, reference_dir: Path, *, row_limit: int = 50) -> None:
        self.reference_dir = reference_dir
        self.row_limit = row_limit
        self.connection = duckdb.connect(database=":memory:")
        self._create_views()

    def query(self, sql: str) -> SemanticQueryResult:
        """Execute a SELECT-only whitelisted query with telemetry."""
        referenced_views = validate_semantic_sql(sql)
        limited_sql = f"select * from ({sql.rstrip().rstrip(';')}) as semantic_subquery limit {self.row_limit}"
        cursor = self.connection.execute(limited_sql)
        columns = [description[0] for description in cursor.description]
        row_tuples = cursor.fetchall()
        rows = [dict(zip(columns, row, strict=False)) for row in row_tuples]
        return SemanticQueryResult(
            sql=sql,
            referenced_views=referenced_views,
            columns=columns,
            rows=rows,
            row_count=len(rows),
            row_preview=rows[:5],
        )

    def _create_views(self) -> None:
        city_path = (self.reference_dir / "joined_city_week_game_economic.csv").as_posix()
        msa_path = (self.reference_dir / "joined_msa_week_game_economic.csv").as_posix()
        self.connection.execute(
            f"create view city_week_events as select * from read_csv_auto('{city_path}', header=true)"
        )
        self.connection.execute(
            f"create view msa_week_events as select * from read_csv_auto('{msa_path}', header=true)"
        )


def validate_semantic_sql(sql: str) -> list[str]:
    """Validate SELECT-only SQL and return referenced whitelisted views."""
    stripped = sql.strip().rstrip(";")
    if not re.match(r"^select\b", stripped, flags=re.IGNORECASE):
        raise SemanticLayerError("Only SELECT queries are allowed.")
    if re.search(r"\b(insert|update|delete|drop|alter|create|copy|attach|detach|pragma)\b", stripped, re.IGNORECASE):
        raise SemanticLayerError("Mutating or administrative SQL is not allowed.")
    referenced = sorted({match.group(1) for match in RELATION_PATTERN.finditer(stripped)})
    if not referenced:
        raise SemanticLayerError("Query must reference a whitelisted view.")
    disallowed = [view for view in referenced if view not in WHITELISTED_VIEWS]
    if disallowed:
        raise SemanticLayerError(f"Query references non-whitelisted relation(s): {', '.join(disallowed)}")
    return referenced


def write_semantic_smoke(results: list[SemanticQueryResult], output_dir: Path) -> tuple[Path, Path]:
    """Write semantic smoke JSON and Markdown artifacts."""
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": "phase-011.semantic-smoke.v1",
        "results": [result.to_dict() for result in results],
    }
    json_path = output_dir / "semantic_smoke.json"
    markdown_path = output_dir / "semantic_smoke.md"
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    markdown_path.write_text(render_semantic_smoke_markdown(payload), encoding="utf-8")
    return json_path, markdown_path


def render_semantic_smoke_markdown(payload: dict[str, object]) -> str:
    """Render semantic smoke output as Markdown."""
    lines = ["# Semantic Smoke Report", "", f"Schema: {payload['schema_version']}", ""]
    for result in payload["results"]:
        lines.extend(
            [
                f"## Query: {result['sql']}",
                "",
                f"- Referenced views: {', '.join(result['referenced_views'])}",
                f"- Columns: {', '.join(result['columns'])}",
                f"- Rows returned: {result['row_count']}",
                "",
            ]
        )
    return "\n".join(lines)
