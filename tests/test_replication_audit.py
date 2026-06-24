from app.replication_audit import run_replication_audit


def test_replication_audit_passes_against_latest_phase_artifacts() -> None:
    audit = run_replication_audit()

    assert audit.required_source_files_present is True
    assert audit.completed_twenty_turns is True
    assert audit.stopped_early is False
    assert audit.workflow_task_statistical_misroutes == 0
    assert audit.selected_candidates_have_required_metadata is True
    assert audit.turns_have_statistical_evidence is True
    assert audit.data_snapshot_complete is True
    assert audit.data_snapshot_combined_sha256 is not None
    assert audit.correction_notebook_present is True
    assert audit.correction_notebook_executed is True
    assert audit.selected_forum_metadata_count == 20
    assert audit.selected_tournament_metadata_count == 20
    assert audit.selected_reflection_metadata_count == 20
    assert audit.selected_evolution_metadata_count == 20
    assert audit.selected_evolution_variant_count == 20
    assert audit.selected_openai_reasoning_count == 20
    assert audit.openai_model_calls_performed is False
    assert audit.reasoning_provider == "openai"
    assert audit.reasoning_mode == "replay"
    assert audit.maf_adapter_present is True
    assert audit.maf_reasoning_provider == "openai"
    assert audit.maf_reasoning_mode == "replay"
    assert audit.maf_model_calls_performed is False
    assert audit.maf_candidate_count == 3
    assert audit.statistical_evidence_turn_count == 20
    assert audit.business_report_statistical_sections == 20
    assert audit.business_report_statistical_tables == 20
    assert audit.final_status == "replicated_with_known_limits"
