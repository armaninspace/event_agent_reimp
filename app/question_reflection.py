"""Deterministic reviewer reflection for candidate questions."""

from __future__ import annotations


def reflect_candidates(candidates: list[dict[str, object]]) -> dict[str, dict[str, object]]:
    """Return reflection metadata keyed by candidate ID."""
    return {str(candidate["candidate_id"]): reflect_candidate(candidate) for candidate in candidates}


def reflect_candidate(candidate: dict[str, object]) -> dict[str, object]:
    """Return one candidate reflection record."""
    testability = int(candidate["testability"])
    semantic_slot = str(candidate["semantic_slot"])
    if testability >= 4:
        status = "pass"
        answerability = "answerable with current reference files as an exploratory workflow"
    elif semantic_slot == "identification_risk":
        status = "needs-review"
        answerability = "reviewable with current files but not a direct impact test"
    else:
        status = "not-answerable"
        answerability = "not answerable with current data and design metadata"
    return {
        "status": status,
        "misleading_risk": str(candidate["caveat"]),
        "weakening_evidence": "Sparse exposure, missing controls, or inconsistent matched results would weaken this question.",
        "answerability": answerability,
    }
