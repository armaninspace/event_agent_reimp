from pathlib import Path

import pytest

from app.semantic_layer import SemanticLayer, SemanticLayerError, validate_semantic_sql, write_semantic_smoke


def _write_reference_files(reference_dir: Path) -> None:
    reference_dir.mkdir()
    (reference_dir / "joined_city_week_game_economic.csv").write_text(
        "week_start_monday,revenue_all,merchants_all,has_game\n"
        "2026-01-05,10,2,1\n"
        "2026-01-12,11,3,0\n",
        encoding="utf-8",
    )
    (reference_dir / "joined_msa_week_game_economic.csv").write_text(
        "msa_code,week_start_monday,revenue_all,merchants_all,has_game\n"
        "10000,2026-01-05,20,4,1\n",
        encoding="utf-8",
    )


def test_validate_semantic_sql_allows_whitelisted_select() -> None:
    assert validate_semantic_sql("select * from city_week_events") == ["city_week_events"]


def test_validate_semantic_sql_rejects_non_select() -> None:
    with pytest.raises(SemanticLayerError, match="Only SELECT"):
        validate_semantic_sql("delete from city_week_events")


def test_validate_semantic_sql_rejects_non_whitelisted_relation() -> None:
    with pytest.raises(SemanticLayerError, match="non-whitelisted"):
        validate_semantic_sql("select * from private_table")


def test_semantic_layer_query_applies_row_limit_and_writes_artifacts(tmp_path: Path) -> None:
    reference_dir = tmp_path / "reference"
    _write_reference_files(reference_dir)
    layer = SemanticLayer(reference_dir, row_limit=1)

    result = layer.query("select week_start_monday, revenue_all from city_week_events order by week_start_monday")
    json_path, markdown_path = write_semantic_smoke([result], tmp_path / "out")

    assert result.referenced_views == ["city_week_events"]
    assert result.row_count == 1
    assert result.columns == ["week_start_monday", "revenue_all"]
    assert result.row_preview
    assert json_path.exists()
    assert markdown_path.exists()
