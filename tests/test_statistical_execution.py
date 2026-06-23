from app.statistical_execution import evidence_for_candidate


def test_evidence_for_candidate_filters_results_by_semantic_slot() -> None:
    report = {
        "schema_version": "phase-017.statistical-execution.v1",
        "method": "Benjamini-Hochberg FDR correction",
        "results": [
            {
                "result_id": "exploratory:city_week:revenue_all",
                "dataset": "city_week",
                "family": "exploratory",
                "adjusted_p_value": 0.01,
            },
            {
                "result_id": "matched:msa_week:revenue_all",
                "dataset": "msa_week",
                "family": "matched",
                "adjusted_p_value": 0.2,
            },
        ],
    }
    candidate = {
        "candidate_id": "turn-01-crowd-spending",
        "semantic_slot": "city_week_event_spending",
    }

    evidence = evidence_for_candidate(candidate, report)

    assert evidence["result_count"] == 1
    assert evidence["result_ids"] == ["exploratory:city_week:revenue_all"]
    assert evidence["has_adjusted_significance"] is True
