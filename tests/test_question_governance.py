from app.question_evolution import evolve_candidates
from app.question_reflection import reflect_candidates
from app.question_tournament import run_question_tournament


def _candidate(candidate_id: str, *, score: int, testability: int = 5) -> dict[str, object]:
    return {
        "candidate_id": candidate_id,
        "evidence_value": score,
        "testability": testability,
        "novelty": 4,
        "semantic_slot": "city_week_event_spending",
        "caveat": "Observational caveat.",
        "forum": {
            "question_id": candidate_id,
            "priority": score,
            "popularity": score,
        },
    }


def test_question_tournament_ranks_candidates_and_records_transcripts() -> None:
    results = run_question_tournament([_candidate("a", score=5), _candidate("b", score=3)])

    assert results["a"]["rank"] == 1
    assert results["a"]["wins"] == 1
    assert results["b"]["losses"] == 1
    assert results["a"]["transcript"]


def test_question_reflection_marks_low_testability_for_review() -> None:
    candidates = [_candidate("risk", score=4, testability=3) | {"semantic_slot": "identification_risk"}]

    results = reflect_candidates(candidates)

    assert results["risk"]["status"] == "needs-review"
    assert "misleading_risk" in results["risk"]


def test_question_evolution_strengthens_previously_selected_questions() -> None:
    candidates = [_candidate("crowd-spending", score=5)]

    results = evolve_candidates(candidates, prior_selected_forum_ids={"crowd-spending"})

    assert results["crowd-spending"]["action"] == "strengthen"
    assert results["crowd-spending"]["parent_question_id"] == "crowd-spending"
    assert results["crowd-spending"]["child_question_id"] == "crowd-spending:strengthen"
    assert "stronger checks" in results["crowd-spending"]["evolved_question"]
