from pathlib import Path

from app.causal_diagnostics import build_causal_design_report, diagnostics_for_semantic_slot, summarize_designs


def test_build_causal_design_report_grades_matched_controls(tmp_path: Path) -> None:
    reference_dir = tmp_path / "reference"
    reference_dir.mkdir()
    city = (
        "week_start_monday,event_msa_block_id,has_game,revenue_all,merchants_all\n"
        "2026-01-05,a,1,12,3\n"
        "2026-01-05,a,0,8,2\n"
        "2026-01-05,a,0,10,3\n"
    )
    msa = (
        "week_start_monday,msa_block_id,has_game,revenue_all,merchants_all\n"
        "2026-01-05,b,1,20,5\n"
        "2026-01-05,b,0,15,4\n"
    )
    (reference_dir / "joined_city_week_game_economic.csv").write_text(city, encoding="utf-8")
    (reference_dir / "joined_msa_week_game_economic.csv").write_text(msa, encoding="utf-8")

    report = build_causal_design_report(reference_dir)

    assert report["schema_version"] == "phase-026.causal-design-diagnostics.v1"
    assert report["diagnostic_count"] == 4
    assert report["controlled_result_count"] == 4
    city_diagnostics = diagnostics_for_semantic_slot(report, "city_week_event_spending")
    summary = summarize_designs(city_diagnostics)
    assert summary["design_count"] == 2
    assert summary["strongest_design_level"] == "same_week_same_block_matched"
    assert summary["evidence_grade"] == "fragile_controlled_observational"
    assert summary["claim_boundary"] == "controlled observational evidence; not causal proof"
