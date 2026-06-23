"""Deterministic friends-loop orchestration skeleton."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from app.hypothesis_routing import classify_question
from app.notebook_workspace import write_turn_notebook
from app.reference_data import build_reference_quality_report
from app.reporting import render_business_report, render_playback_ui


DEFAULT_QUESTIONS = (
    "Do big sports crowds actually turn into more local spending?",
    "Which markets have enough event exposure for a careful spending comparison?",
    "Where should a skeptic worry that game weeks and spending are confounded?",
)


@dataclass(frozen=True)
class Candidate:
    """Public candidate proposed by the friends loop."""

    candidate_id: str
    question: str
    rationale: str
    semantic_slot: str
    evidence_value: int
    testability: int
    novelty: int
    caveat: str

    @property
    def score(self) -> int:
        """Deterministic ranking score."""
        return self.evidence_value + self.testability + self.novelty

    def to_dict(self) -> dict[str, object]:
        """Return JSON-serializable candidate data."""
        data = asdict(self)
        data["score"] = self.score
        return data


@dataclass(frozen=True)
class TelemetryEvent:
    """Structured telemetry event for loop playback and tests."""

    event_id: str
    sequence: int
    time_offset_ms: int
    event_type: str
    turn: int
    actor: str
    summary: str
    payload: dict[str, object]

    def to_dict(self) -> dict[str, object]:
        """Return JSON-serializable telemetry event data."""
        return asdict(self)


class TelemetryRecorder:
    """Collect deterministic structured telemetry events."""

    def __init__(self) -> None:
        self._events: list[TelemetryEvent] = []

    @property
    def events(self) -> list[TelemetryEvent]:
        """Return recorded events."""
        return list(self._events)

    def record(self, *, event_type: str, turn: int, actor: str, summary: str, payload: dict[str, object]) -> None:
        """Record one event with stable sequence and synthetic timing."""
        sequence = len(self._events) + 1
        self._events.append(
            TelemetryEvent(
                event_id=f"evt-{sequence:04d}",
                sequence=sequence,
                time_offset_ms=(sequence - 1) * 10,
                event_type=event_type,
                turn=turn,
                actor=actor,
                summary=summary,
                payload=payload,
            )
        )


class Spark:
    """Proposes public, stakeholder-readable research candidates."""

    def propose(self, *, turn: int, prior_selected_ids: set[str]) -> list[Candidate]:
        """Return deterministic candidate proposals."""
        candidates = [
            Candidate(
                candidate_id=f"turn-{turn:02d}-crowd-spending",
                question=DEFAULT_QUESTIONS[0],
                rationale="High-attendance weeks are the clearest public question for the available files.",
                semantic_slot="city_week_event_spending",
                evidence_value=5,
                testability=5,
                novelty=3 if "turn-01-crowd-spending" in prior_selected_ids else 4,
                caveat="Observational data cannot prove that crowds caused spending changes.",
            ),
            Candidate(
                candidate_id=f"turn-{turn:02d}-market-coverage",
                question=DEFAULT_QUESTIONS[1],
                rationale="Coverage checks identify which markets can support later statistical comparisons.",
                semantic_slot="msa_week_coverage",
                evidence_value=4,
                testability=5,
                novelty=5,
                caveat="Coverage strength is not the same as evidence of impact.",
            ),
            Candidate(
                candidate_id=f"turn-{turn:02d}-confounding-risk",
                question=DEFAULT_QUESTIONS[2],
                rationale="A skeptic needs to surface where event timing may coincide with other spending drivers.",
                semantic_slot="identification_risk",
                evidence_value=4,
                testability=3,
                novelty=4,
                caveat="This is a review task until matched controls exist.",
            ),
        ]
        return sorted(candidates, key=lambda candidate: candidate.candidate_id)


class Skeptic:
    """Reviews candidates for claim and identification boundaries."""

    def review(self, candidates: list[Candidate]) -> dict[str, dict[str, object]]:
        """Return deterministic public review notes."""
        return {
            candidate.candidate_id: {
                "status": "pass" if candidate.testability >= 4 else "needs-review",
                "claim_boundary": candidate.caveat,
            }
            for candidate in candidates
        }


class Mapper:
    """Links candidates to data quality context."""

    def map_candidates(self, *, candidates: list[Candidate], reference_dir: Path) -> dict[str, dict[str, object]]:
        """Return semantic/data context for each candidate."""
        report = build_reference_quality_report(reference_dir)
        return {
            candidate.candidate_id: {
                "semantic_slot": candidate.semantic_slot,
                "all_required_columns_present": report.all_required_columns_present,
                "all_required_values_present": report.all_required_values_present,
                "dataset_warnings": report.warnings,
            }
            for candidate in candidates
        }


class Moderator:
    """Ranks and selects candidates deterministically."""

    def rank(self, candidates: list[Candidate]) -> list[Candidate]:
        """Return candidates sorted by score descending and ID ascending."""
        return sorted(candidates, key=lambda candidate: (-candidate.score, candidate.candidate_id))

    def select(self, candidates: list[Candidate]) -> tuple[Candidate, list[Candidate]]:
        """Select the top candidate and reject the rest."""
        ranked = self.rank(candidates)
        return ranked[0], ranked[1:]


class DataAgent:
    """Writes durable loop artifacts."""

    def write_artifacts(self, *, session: dict[str, object], telemetry: list[TelemetryEvent], output_dir: Path) -> dict[str, str]:
        """Write session, telemetry, and decision-summary artifacts."""
        output_dir.mkdir(parents=True, exist_ok=True)
        session_json = output_dir / "friends_loop_session.json"
        session_md = output_dir / "friends_loop_session.md"
        telemetry_json = output_dir / "friends_loop_telemetry.json"
        decision_summary = output_dir / "discovery_decision_summary.md"
        business_report = output_dir / "business_evidence_report.html"
        playback_ui = output_dir / "ui" / "index.html"

        session_json.write_text(json.dumps(session, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        session_md.write_text(_render_session_markdown(session), encoding="utf-8")
        telemetry_json.write_text(
            json.dumps([event.to_dict() for event in telemetry], indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        decision_summary.write_text(_render_decision_summary(session), encoding="utf-8")
        business_report.write_text(render_business_report(session), encoding="utf-8")
        playback_ui.parent.mkdir(parents=True, exist_ok=True)
        playback_ui.write_text(render_playback_ui([event.to_dict() for event in telemetry]), encoding="utf-8")
        return {
            "session_json": str(session_json),
            "session_markdown": str(session_md),
            "telemetry_json": str(telemetry_json),
            "discovery_decision_summary": str(decision_summary),
            "business_evidence_report": str(business_report),
            "playback_ui": str(playback_ui),
        }


def run_friends_question_loop(
    *,
    turn_count: int = 2,
    output_dir: Path = Path("app/runs/phase-003-friends-loop-skeleton/friends-question-loop"),
    reference_dir: Path = Path("data/reference"),
    notebook_dir: Path | None = None,
) -> dict[str, object]:
    """Run a deterministic friends question loop and write durable artifacts."""
    spark = Spark()
    skeptic = Skeptic()
    mapper = Mapper()
    moderator = Moderator()
    data_agent = DataAgent()
    telemetry = TelemetryRecorder()
    prior_selected_ids: set[str] = set()
    turns: list[dict[str, object]] = []

    telemetry.record(
        event_type="memory.seeded",
        turn=0,
        actor="DataAgent",
        summary="Seeded deterministic in-memory loop state.",
        payload={"prior_selected_ids": []},
    )

    for turn in range(1, turn_count + 1):
        telemetry.record(
            event_type="turn.started",
            turn=turn,
            actor="Moderator",
            summary=f"Started turn {turn}.",
            payload={"turn": turn},
        )
        telemetry.record(
            event_type="knowledge.read",
            turn=turn,
            actor="Mapper",
            summary="Read reference data quality context.",
            payload={"reference_dir": str(reference_dir)},
        )
        candidates = spark.propose(turn=turn, prior_selected_ids=prior_selected_ids)
        telemetry.record(
            event_type="board.proposed",
            turn=turn,
            actor="Spark",
            summary=f"Proposed {len(candidates)} candidates.",
            payload={"candidate_ids": [candidate.candidate_id for candidate in candidates]},
        )
        reviews = skeptic.review(candidates)
        mapped = mapper.map_candidates(candidates=candidates, reference_dir=reference_dir)
        ranked = moderator.rank(candidates)
        selected, rejected = moderator.select(candidates)
        classification = classify_question(selected.question)
        prior_selected_ids.add(selected.candidate_id)
        telemetry.record(
            event_type="board.ranked",
            turn=turn,
            actor="Moderator",
            summary=f"Selected {selected.candidate_id}.",
            payload={
                "ranked_candidate_ids": [candidate.candidate_id for candidate in ranked],
                "selected_candidate_id": selected.candidate_id,
                "rejected_candidate_ids": [candidate.candidate_id for candidate in rejected],
            },
        )
        telemetry.record(
            event_type="discussion.message",
            turn=turn,
            actor="Skeptic",
            summary="Recorded public caveat for selected candidate.",
            payload={"selected_candidate_id": selected.candidate_id, "caveat": selected.caveat},
        )
        telemetry.record(
            event_type="hypothesis.classified",
            turn=turn,
            actor="Moderator",
            summary=f"Classified selected candidate as {classification.classification}.",
            payload=classification.to_dict(),
        )
        telemetry.record(
            event_type="question.submitted",
            turn=turn,
            actor="Moderator",
            summary="Submitted selected public question to the routed workflow.",
            payload={"candidate_id": selected.candidate_id, "route": classification.route},
        )
        telemetry.record(
            event_type="workflow.stage",
            turn=turn,
            actor="DataAgent",
            summary=f"Recorded workflow route {classification.route}.",
            payload={"route": classification.route},
        )
        turn_record = {
            "turn": turn,
            "selected_candidate": selected.to_dict(),
            "rejected_candidates": [candidate.to_dict() for candidate in rejected],
            "classification": classification.to_dict(),
            "reviews": reviews,
            "mapping": mapped,
        }
        if notebook_dir is not None:
            notebook_artifacts = write_turn_notebook(notebook_dir, turn=turn_record)
            turn_record["notebook_artifacts"] = notebook_artifacts.to_dict()
            telemetry.record(
                event_type="notebook.created",
                turn=turn,
                actor="DataAgent",
                summary=f"Wrote scaffolded notebook for turn {turn}.",
                payload=notebook_artifacts.to_dict(),
            )
            telemetry.record(
                event_type="wiki.updated",
                turn=turn,
                actor="DataAgent",
                summary=f"Updated notebook workspace wiki for turn {turn}.",
                payload={"notebook_dir": str(notebook_dir)},
            )
        telemetry.record(
            event_type="turn.completed",
            turn=turn,
            actor="DataAgent",
            summary=f"Completed turn {turn}.",
            payload={"selected_candidate_id": selected.candidate_id},
        )
        turns.append(turn_record)

    session: dict[str, object] = {
        "schema_version": "phase-003.friends-loop-session.v1",
        "session_summary": {
            "requested_turns": turn_count,
            "completed_turns": len(turns),
            "stopped_early": False,
        },
        "turns": turns,
    }
    artifact_paths = data_agent.write_artifacts(session=session, telemetry=telemetry.events, output_dir=output_dir)
    session["artifact_paths"] = artifact_paths
    # Rewrite after artifact paths are known.
    data_agent.write_artifacts(session=session, telemetry=telemetry.events, output_dir=output_dir)
    return session


def _render_session_markdown(session: dict[str, object]) -> str:
    turns = session["turns"]
    assert isinstance(turns, list)
    lines = ["# Friends Loop Session", ""]
    summary = session["session_summary"]
    assert isinstance(summary, dict)
    lines.extend(
        [
            f"Requested turns: {summary['requested_turns']}",
            f"Completed turns: {summary['completed_turns']}",
            f"Stopped early: {summary['stopped_early']}",
            "",
        ]
    )
    for turn in turns:
        selected = turn["selected_candidate"]
        rejected = turn["rejected_candidates"]
        assert isinstance(selected, dict)
        assert isinstance(rejected, list)
        lines.extend(
            [
                f"## Turn {turn['turn']}",
                "",
                f"Selected: {selected['candidate_id']}",
                f"Question: {selected['question']}",
                f"Rejected: {', '.join(candidate['candidate_id'] for candidate in rejected)}",
                "",
            ]
        )
    return "\n".join(lines)


def _render_decision_summary(session: dict[str, object]) -> str:
    turns = session["turns"]
    assert isinstance(turns, list)
    lines = ["# Discovery Decision Summary", ""]
    for turn in turns:
        selected = turn["selected_candidate"]
        rejected = turn["rejected_candidates"]
        assert isinstance(selected, dict)
        assert isinstance(rejected, list)
        lines.extend(
            [
                f"## Turn {turn['turn']}",
                "",
                f"Selected candidate: {selected['candidate_id']}",
                f"Score: {selected['score']}",
                f"Public rationale: {selected['rationale']}",
                f"Caveat: {selected['caveat']}",
                f"Rejected candidates: {', '.join(candidate['candidate_id'] for candidate in rejected)}",
                "",
            ]
        )
    return "\n".join(lines)
