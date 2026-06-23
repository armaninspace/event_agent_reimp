"""Deterministic hypothesis classification and routing."""

from __future__ import annotations

from dataclasses import asdict, dataclass


WORKFLOW_KEYWORDS = ("notebook", "wiki", "prompt", "report", "ui", "logging", "telemetry", "artifact")
FORMAL_HYPOTHESIS_FIELDS = (
    "h0",
    "h1",
    "population",
    "unit",
    "exposure",
    "comparison",
    "outcome",
    "direction",
    "test_family",
    "alpha",
    "decision_rule",
)


@dataclass(frozen=True)
class ClassificationResult:
    """Classification and routing result for one candidate/question."""

    classification: str
    route: str
    rationale: str
    required_fields_present: list[str]
    required_fields_missing: list[str]

    def to_dict(self) -> dict[str, object]:
        """Return JSON-serializable classification result."""
        return asdict(self)


def classify_question(question: str, *, formal_hypothesis: dict[str, object] | None = None) -> ClassificationResult:
    """Classify a public question or formal hypothesis payload."""
    lowered = question.lower()
    if any(keyword in lowered for keyword in WORKFLOW_KEYWORDS):
        return ClassificationResult(
            classification="workflow_task",
            route="workflow_review",
            rationale="Question refers to workflow/artifact surfaces rather than a statistical hypothesis.",
            required_fields_present=[],
            required_fields_missing=list(FORMAL_HYPOTHESIS_FIELDS),
        )

    formal_hypothesis = formal_hypothesis or {}
    present = [field for field in FORMAL_HYPOTHESIS_FIELDS if formal_hypothesis.get(field) not in (None, "")]
    missing = [field for field in FORMAL_HYPOTHESIS_FIELDS if field not in present]
    if not missing:
        return ClassificationResult(
            classification="statistical_hypothesis",
            route="statistical_test",
            rationale="Formal hypothesis includes all required statistical fields.",
            required_fields_present=present,
            required_fields_missing=[],
        )

    return ClassificationResult(
        classification="eda_question",
        route="eda_review",
        rationale="Question is data-oriented but lacks the full formal hypothesis contract.",
        required_fields_present=present,
        required_fields_missing=missing,
    )


def count_workflow_statistical_misroutes(turns: list[dict[str, object]]) -> int:
    """Count workflow tasks incorrectly routed to statistical testing."""
    count = 0
    for turn in turns:
        classification = turn.get("classification")
        if not isinstance(classification, dict):
            continue
        if classification.get("classification") == "workflow_task" and classification.get("route") == "statistical_test":
            count += 1
    return count
