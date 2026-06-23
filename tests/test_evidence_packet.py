import json
from datetime import UTC, datetime
from pathlib import Path

from app.evidence_packet import build_static_evidence_packet, write_evidence_packet


def _write_runtime_csvs(reference_dir: Path) -> None:
    reference_dir.mkdir()
    (reference_dir / "joined_city_week_game_economic.csv").write_text(
        "cityid,week_start_monday,revenue_all,merchants_all,has_game,game_count\n"
        "1,2026-01-05,10.0,2.0,1,1\n",
        encoding="utf-8",
    )
    (reference_dir / "joined_msa_week_game_economic.csv").write_text(
        "msa_code,week_start_monday,revenue_all,merchants_all,has_game,game_count,msa_block_id\n"
        "10000,2026-01-05,20.0,3.0,0,0,block-a\n",
        encoding="utf-8",
    )


def test_build_static_evidence_packet_has_required_shape(tmp_path: Path) -> None:
    reference_dir = tmp_path / "reference"
    _write_runtime_csvs(reference_dir)

    packet = build_static_evidence_packet(
        reference_dir=reference_dir,
        question="Does game exposure change spending?",
        generated_at=datetime(2026, 1, 1, tzinfo=UTC),
    )

    assert packet["schema_version"] == "phase-001.static-evidence-packet.v1"
    assert packet["question"] == "Does game exposure change spending?"
    assert "hypothesis" in packet
    assert "design" in packet
    assert "result" in packet
    assert "caveat" in packet
    assert "audit_log" in packet
    assert packet["data_profile"]["city_week"]["row_count"] == 1
    assert packet["data_profile"]["msa_week"]["row_count"] == 1
    assert packet["result"]["all_required_columns_present"] is True


def test_write_evidence_packet_creates_json_and_markdown(tmp_path: Path) -> None:
    reference_dir = tmp_path / "reference"
    _write_runtime_csvs(reference_dir)
    packet = build_static_evidence_packet(reference_dir=reference_dir)

    artifacts = write_evidence_packet(packet, tmp_path / "run")

    assert artifacts.json_path.exists()
    assert artifacts.markdown_path.exists()
    loaded = json.loads(artifacts.json_path.read_text(encoding="utf-8"))
    assert loaded["schema_version"] == packet["schema_version"]
    assert "Static Evidence Packet" in artifacts.markdown_path.read_text(encoding="utf-8")
