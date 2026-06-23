"""Deterministic pairwise candidate tournament."""

from __future__ import annotations


def run_question_tournament(candidates: list[dict[str, object]]) -> dict[str, dict[str, object]]:
    """Rank candidates with deterministic pairwise comparisons."""
    stats = {
        str(candidate["candidate_id"]): {
            "candidate_id": str(candidate["candidate_id"]),
            "wins": 0,
            "losses": 0,
            "score": _candidate_score(candidate),
            "component_scores": {
                "public_interest": _forum_number(candidate, "popularity"),
                "novelty": int(candidate["novelty"]),
                "testability": int(candidate["testability"]),
                "evidence_value": int(candidate["evidence_value"]),
                "policy_business_relevance": _forum_number(candidate, "priority"),
            },
            "transcript": [],
        }
        for candidate in candidates
    }
    by_id = {str(candidate["candidate_id"]): candidate for candidate in candidates}
    ids = sorted(by_id)
    for left_index, left_id in enumerate(ids):
        for right_id in ids[left_index + 1 :]:
            winner_id, loser_id, reason = _compare(by_id[left_id], by_id[right_id])
            stats[winner_id]["wins"] += 1
            stats[loser_id]["losses"] += 1
            transcript = f"{winner_id} beats {loser_id}: {reason}"
            stats[winner_id]["transcript"].append(transcript)
            stats[loser_id]["transcript"].append(transcript)

    ranked_ids = sorted(ids, key=lambda candidate_id: (-stats[candidate_id]["wins"], stats[candidate_id]["losses"], -stats[candidate_id]["score"], candidate_id))
    for rank, candidate_id in enumerate(ranked_ids, start=1):
        stats[candidate_id]["rank"] = rank
    return stats


def _compare(left: dict[str, object], right: dict[str, object]) -> tuple[str, str, str]:
    left_score = _candidate_score(left)
    right_score = _candidate_score(right)
    if left_score > right_score:
        return str(left["candidate_id"]), str(right["candidate_id"]), "higher combined governance score"
    if right_score > left_score:
        return str(right["candidate_id"]), str(left["candidate_id"]), "higher combined governance score"
    left_id = str(left["candidate_id"])
    right_id = str(right["candidate_id"])
    if left_id < right_id:
        return left_id, right_id, "stable candidate-id tie break"
    return right_id, left_id, "stable candidate-id tie break"


def _candidate_score(candidate: dict[str, object]) -> int:
    return (
        int(candidate["evidence_value"])
        + int(candidate["testability"])
        + int(candidate["novelty"])
        + _forum_number(candidate, "priority")
        + _forum_number(candidate, "popularity")
    )


def _forum_number(candidate: dict[str, object], field: str) -> int:
    forum = candidate.get("forum", {})
    if not isinstance(forum, dict):
        return 0
    value = forum.get(field, 0)
    return int(value) if isinstance(value, int) else 0
