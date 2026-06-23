from app.hypothesis_routing import classify_question, count_workflow_statistical_misroutes


def test_workflow_artifact_question_classifies_as_workflow_task() -> None:
    result = classify_question("Which notebook and report should the UI show next?")

    assert result.classification == "workflow_task"
    assert result.route == "workflow_review"


def test_complete_formal_hypothesis_classifies_as_statistical_hypothesis() -> None:
    payload = {
        "h0": "No difference",
        "h1": "Game weeks differ",
        "population": "MSA weeks",
        "unit": "MSA-week",
        "exposure": "has_game",
        "comparison": "matched no-game weeks",
        "outcome": "revenue_all",
        "direction": "greater",
        "test_family": "paired",
        "alpha": 0.05,
        "decision_rule": "reject if p < alpha",
    }

    result = classify_question("Do game weeks increase revenue?", formal_hypothesis=payload)

    assert result.classification == "statistical_hypothesis"
    assert result.route == "statistical_test"
    assert result.required_fields_missing == []


def test_incomplete_data_question_classifies_as_eda() -> None:
    result = classify_question("Which markets have enough event exposure?")

    assert result.classification == "eda_question"
    assert result.route == "eda_review"


def test_count_workflow_statistical_misroutes() -> None:
    turns = [
        {"classification": {"classification": "workflow_task", "route": "statistical_test"}},
        {"classification": {"classification": "workflow_task", "route": "workflow_review"}},
        {"classification": {"classification": "eda_question", "route": "eda_review"}},
    ]

    assert count_workflow_statistical_misroutes(turns) == 1
