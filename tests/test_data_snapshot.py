from pathlib import Path

from app.data_snapshot import build_reference_snapshot, snapshot_is_complete


def test_build_reference_snapshot_hashes_reference_files(tmp_path: Path) -> None:
    reference_dir = tmp_path / "reference"
    reference_dir.mkdir()
    (reference_dir / "joined_city_week_game_economic.csv").write_text(
        "id,value\n1,10\n2,20\n",
        encoding="utf-8",
    )
    (reference_dir / "joined_msa_week_game_economic.csv").write_text(
        "id,value\n1,30\n",
        encoding="utf-8",
    )

    snapshot = build_reference_snapshot(reference_dir)

    assert snapshot_is_complete(snapshot) is True
    assert snapshot["algorithm"] == "sha256"
    assert snapshot["file_count"] == 2
    assert len(snapshot["combined_sha256"]) == 64
    files = snapshot["files"]
    assert isinstance(files, list)
    assert [item["row_count"] for item in files] == [2, 1]
