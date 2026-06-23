"""Deterministic question evolution metadata."""

from __future__ import annotations


def evolve_candidates(
    candidates: list[dict[str, object]], *, prior_selected_forum_ids: set[str]
) -> dict[str, dict[str, object]]:
    """Return evolution metadata keyed by candidate ID."""
    return {
        str(candidate["candidate_id"]): _evolve_candidate(candidate, prior_selected_forum_ids=prior_selected_forum_ids)
        for candidate in candidates
    }


def _evolve_candidate(candidate: dict[str, object], *, prior_selected_forum_ids: set[str]) -> dict[str, object]:
    forum = candidate.get("forum", {})
    question_id = str(forum.get("question_id", "")) if isinstance(forum, dict) else ""
    semantic_slot = str(candidate["semantic_slot"])
    question = str(candidate.get("question", ""))
    if question_id in prior_selected_forum_ids:
        action = "strengthen"
        rationale = "Prior selection exists, so this turn should sharpen diagnostics instead of repeating the same claim."
        evolved_question = f"What stronger checks would make this prior question more reliable: {question}"
    elif semantic_slot == "identification_risk":
        action = "split"
        rationale = "Separate confounding review from direct impact estimation."
        evolved_question = f"Which confounding risks should be reviewed separately before answering: {question}"
    elif semantic_slot == "msa_week_coverage":
        action = "combine"
        rationale = "Combine market coverage with later impact tests once coverage is sufficient."
        evolved_question = f"Which covered markets should be combined with matched impact tests after asking: {question}"
    else:
        action = "carry_forward"
        rationale = "Carry the public question forward as an initial evidence workflow."
        evolved_question = question
    return {
        "action": action,
        "source_question_id": question_id,
        "parent_question_id": question_id,
        "child_question_id": f"{question_id}:{action}" if question_id else action,
        "evolved_question": evolved_question,
        "rationale": rationale,
    }
