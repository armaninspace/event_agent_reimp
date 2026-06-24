from app.statistical_execution import evidence_for_candidate


def test_evidence_for_candidate_filters_results_by_semantic_slot() -> None:
    report = {
        "schema_version": "phase-026.statistical-execution.v2",
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
        "causal_design": {
            "results": [
                {
                    "diagnostic_id": "causal-design:city_week:revenue_all",
                    "dataset": "city_week",
                    "outcome": "revenue_all",
                    "design_level": "same_week_same_block_matched",
                    "evidence_grade": "fragile_controlled_observational",
                }
            ]
        },
    }
    candidate = {
        "candidate_id": "turn-01-crowd-spending",
        "semantic_slot": "city_week_event_spending",
    }

    evidence = evidence_for_candidate(candidate, report)

    assert evidence["result_count"] == 1
    assert evidence["result_ids"] == ["exploratory:city_week:revenue_all"]
    assert evidence["has_adjusted_significance"] is True
    assert evidence["causal_design"]["design_count"] == 1
    assert evidence["causal_design"]["evidence_grade"] == "fragile_controlled_observational"
