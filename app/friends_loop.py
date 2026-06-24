"""Deterministic friends-loop orchestration skeleton."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field, replace
from pathlib import Path

from app.hypothesis_routing import classify_question
from app.notebook_workspace import write_turn_notebook
from app.notebook_knowledge_base import load_notebook_knowledge_summary
from app.openai_reasoning import OpenAIHypothesisGenerator, OpenAIProposal, OpenAIReasoningConfig
from app.question_forum import DEFAULT_FORUM_PATH, QuestionForumRecord, load_question_forum
from app.question_evolution import evolve_candidates
from app.question_reflection import reflect_candidates
from app.question_tournament import run_question_tournament
from app.reference_data import build_reference_quality_report
from app.reporting import render_business_report, render_playback_ui
from app.statistical_execution import build_statistical_execution_report, evidence_for_candidate


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
    forum: dict[str, object]
    reasoning: dict[str, object] = field(default_factory=lambda: {"provider": "deterministic", "mode": "deterministic"})

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

    def __init__(self, forum_records: list[QuestionForumRecord]) -> None:
        self._forum_records = {record.question_id: record for record in forum_records}

    def propose(self, *, turn: int, prior_selected_ids: set[str]) -> list[Candidate]:
        """Return deterministic candidate proposals."""
        candidates = [
            Candidate(
                candidate_id=f"turn-{turn:02d}-crowd-spending",
                question=self._question("crowd-spending", DEFAULT_QUESTIONS[0]),
                rationale=self._rationale(
                    "crowd-spending",
                    "High-attendance weeks are the clearest public question for the available files.",
                ),
                semantic_slot="city_week_event_spending",
                evidence_value=5,
                testability=5,
                novelty=1 if "turn-01-crowd-spending" in prior_selected_ids else 4,
                caveat="Observational data cannot prove that crowds caused spending changes.",
                forum=self._forum_metadata("crowd-spending"),
                reasoning={"provider": "deterministic", "mode": "deterministic", "model_calls_performed": False},
            ),
            Candidate(
                candidate_id=f"turn-{turn:02d}-market-coverage",
                question=self._question("market-coverage", DEFAULT_QUESTIONS[1]),
                rationale=self._rationale(
                    "market-coverage",
                    "Coverage checks identify which markets can support later statistical comparisons.",
                ),
                semantic_slot="msa_week_coverage",
                evidence_value=4,
                testability=5,
                novelty=5,
                caveat="Coverage strength is not the same as evidence of impact.",
                forum=self._forum_metadata("market-coverage"),
                reasoning={"provider": "deterministic", "mode": "deterministic", "model_calls_performed": False},
            ),
            Candidate(
                candidate_id=f"turn-{turn:02d}-confounding-risk",
                question=self._question("confounding-risk", DEFAULT_QUESTIONS[2]),
                rationale=self._rationale(
                    "confounding-risk",
                    "A skeptic needs to surface where event timing may coincide with other spending drivers.",
                ),
                semantic_slot="identification_risk",
                evidence_value=4,
                testability=3,
                novelty=4,
                caveat="This is a review task until matched controls exist.",
                forum=self._forum_metadata("confounding-risk"),
                reasoning={"provider": "deterministic", "mode": "deterministic", "model_calls_performed": False},
            ),
        ]
        return sorted(candidates, key=lambda candidate: candidate.candidate_id)

    def _question(self, question_id: str, fallback: str) -> str:
        record = self._forum_records.get(question_id)
        return record.question if record else fallback

    def _rationale(self, question_id: str, fallback: str) -> str:
        record = self._forum_records.get(question_id)
        return record.rationale if record else fallback

    def _forum_metadata(self, question_id: str) -> dict[str, object]:
        record = self._forum_records.get(question_id)
        if record:
            return record.candidate_metadata()
        return {
            "question_id": question_id,
            "kind": "fallback",
            "persona": "system fallback",
            "priority": 0,
            "popularity": 0,
            "source_url": "local://question-forum/fallback",
            "status": "proposed",
            "tags": ["fallback"],
        }

    def forum_metadata_for_openai(self, proposal: OpenAIProposal) -> dict[str, object]:
        """Return source forum metadata for an OpenAI proposal."""
        record = self._forum_records.get(proposal.forum_question_id)
        if record:
            metadata = record.candidate_metadata()
            metadata["source"] = "openai_selected_forum_record"
            return metadata
        return {
            "question_id": proposal.forum_question_id,
            "kind": "model-generated",
            "persona": "OpenAI hypothesis generator",
            "priority": 0,
            "popularity": 0,
            "source_url": "openai://responses",
            "status": "proposed",
            "tags": ["openai-generated"],
            "source": "openai_generated",
        }


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
    question_forum_path: Path = DEFAULT_FORUM_PATH,
    reasoning_mode: str = "deterministic",
    openai_model: str | None = None,
    openai_trace_dir: Path | None = None,
    openai_replay_path: Path | None = None,
    prior_notebook_knowledge_path: Path | None = None,
) -> dict[str, object]:
    """Run a deterministic friends question loop and write durable artifacts."""
    forum_records = load_question_forum(question_forum_path) if question_forum_path.exists() else []
    spark = Spark(forum_records)
    normalized_reasoning_mode = reasoning_mode.strip().lower()
    resolved_openai_trace_dir = (
        openai_trace_dir
        if openai_trace_dir is not None
        else output_dir / "openai-reasoning"
        if normalized_reasoning_mode in {"openai", "replay"}
        else None
    )
    reasoning_config = OpenAIReasoningConfig.from_env(
        mode=reasoning_mode,
        model=openai_model,
        trace_dir=resolved_openai_trace_dir,
        replay_path=openai_replay_path,
    )
    openai_generator = (
        OpenAIHypothesisGenerator(config=reasoning_config) if reasoning_config.mode in {"openai", "replay"} else None
    )
    skeptic = Skeptic()
    mapper = Mapper()
    moderator = Moderator()
    data_agent = DataAgent()
    telemetry = TelemetryRecorder()
    statistical_execution_report = build_statistical_execution_report(reference_dir)
    notebook_knowledge_summary = load_notebook_knowledge_summary(prior_notebook_knowledge_path)
    prior_selected_ids: set[str] = set()
    prior_selected_forum_ids: set[str] = set()
    selected_semantic_slot_counts: dict[str, int] = {}
    prior_knowledge_duplicate_candidate_count = 0
    turns: list[dict[str, object]] = []

    telemetry.record(
        event_type="memory.seeded",
        turn=0,
        actor="DataAgent",
        summary="Seeded deterministic in-memory loop state.",
        payload={"prior_selected_ids": []},
    )
    telemetry.record(
        event_type="forum.loaded",
        turn=0,
        actor="Spark",
        summary=f"Loaded {len(forum_records)} QuestionForum records.",
        payload={
            "forum_path": str(question_forum_path),
            "question_ids": [record.question_id for record in forum_records],
        },
    )
    telemetry.record(
        event_type="reasoning.configured",
        turn=0,
        actor="Spark",
        summary=f"Configured {reasoning_config.mode} hypothesis reasoning.",
        payload={
            "mode": reasoning_config.mode,
            "provider": "openai" if reasoning_config.mode in {"openai", "replay"} else "deterministic",
            "model": reasoning_config.model if reasoning_config.mode in {"openai", "replay"} else None,
            "trace_dir": str(reasoning_config.trace_dir) if reasoning_config.trace_dir else None,
            "replay_path": str(reasoning_config.replay_path) if reasoning_config.replay_path else None,
        },
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
            summary=(
                "Read reference data quality context and "
                f"{notebook_knowledge_summary['entry_count']} prior notebook knowledge entries."
            ),
            payload={
                "reference_dir": str(reference_dir),
                "notebook_knowledge": notebook_knowledge_summary,
            },
        )
        if openai_generator is None:
            candidates = spark.propose(turn=turn, prior_selected_ids=prior_selected_ids)
        else:
            openai_batch = openai_generator.propose(
                turn=turn,
                forum_records=forum_records,
                prior_selected_ids=prior_selected_ids,
                prior_selected_forum_ids=prior_selected_forum_ids,
                notebook_knowledge_summary=notebook_knowledge_summary,
            )
            candidates = _openai_candidates(
                turn=turn,
                proposals=openai_batch.proposals,
                spark=spark,
                notebook_knowledge_summary=notebook_knowledge_summary,
                reasoning={
                    "provider": openai_batch.provider,
                    "mode": openai_batch.mode,
                    "model": openai_batch.model,
                    "prompt_hash": openai_batch.prompt_hash,
                    "output_hash": openai_batch.output_hash,
                    "model_calls_performed": openai_batch.model_calls_performed,
                    "trace_path": openai_batch.trace_path,
                },
            )
            prior_knowledge_duplicate_candidate_count += sum(
                1 for candidate in candidates if bool(candidate.reasoning.get("prior_knowledge_duplicate"))
            )
            telemetry.record(
                event_type="openai.reasoning.completed",
                turn=turn,
                actor="Spark",
                summary=f"Generated {len(candidates)} OpenAI-backed candidates.",
                payload={
                    "mode": openai_batch.mode,
                    "provider": openai_batch.provider,
                    "model": openai_batch.model,
                    "model_calls_performed": openai_batch.model_calls_performed,
                    "prompt_hash": openai_batch.prompt_hash,
                    "output_hash": openai_batch.output_hash,
                    "trace_path": openai_batch.trace_path,
                    "prior_notebook_knowledge_entry_count": notebook_knowledge_summary["entry_count"],
                    "prior_knowledge_duplicate_candidate_count": sum(
                        1 for candidate in candidates if bool(candidate.reasoning.get("prior_knowledge_duplicate"))
                    ),
                    "candidate_ids": [candidate.candidate_id for candidate in candidates],
                },
            )
        candidates = _annotate_semantic_slot_usage(
            candidates,
            selected_semantic_slot_counts=selected_semantic_slot_counts,
        )
        telemetry.record(
            event_type="board.proposed",
            turn=turn,
            actor="Spark",
            summary=f"Proposed {len(candidates)} candidates.",
            payload={
                "candidate_ids": [candidate.candidate_id for candidate in candidates],
                "forum_question_ids": [str(candidate.forum["question_id"]) for candidate in candidates],
            },
        )
        reviews = skeptic.review(candidates)
        mapped = mapper.map_candidates(candidates=candidates, reference_dir=reference_dir)
        candidate_records = [candidate.to_dict() for candidate in candidates]
        tournament = run_question_tournament(candidate_records)
        reflections = reflect_candidates(candidate_records)
        evolutions = evolve_candidates(candidate_records, prior_selected_forum_ids=prior_selected_forum_ids)
        ranked = sorted(candidates, key=lambda candidate: int(tournament[candidate.candidate_id]["rank"]))
        selected = _select_diverse_candidate(
            ranked,
            reflections=reflections,
            selected_semantic_slot_counts=selected_semantic_slot_counts,
        )
        rejected = [candidate for candidate in ranked if candidate.candidate_id != selected.candidate_id]
        classification = classify_question(selected.question)
        prior_selected_ids.add(selected.candidate_id)
        prior_selected_forum_ids.add(str(selected.forum["question_id"]))
        selected_semantic_slot_counts[selected.semantic_slot] = selected_semantic_slot_counts.get(selected.semantic_slot, 0) + 1
        telemetry.record(
            event_type="tournament.completed",
            turn=turn,
            actor="Moderator",
            summary="Completed pairwise candidate tournament.",
            payload={"ranks": {candidate_id: item["rank"] for candidate_id, item in tournament.items()}},
        )
        telemetry.record(
            event_type="reflection.completed",
            turn=turn,
            actor="Skeptic",
            summary="Completed reviewer reflection pass.",
            payload={"statuses": {candidate_id: item["status"] for candidate_id, item in reflections.items()}},
        )
        telemetry.record(
            event_type="evolution.completed",
            turn=turn,
            actor="Spark",
            summary="Completed question evolution pass.",
            payload={"actions": {candidate_id: item["action"] for candidate_id, item in evolutions.items()}},
        )
        telemetry.record(
            event_type="board.ranked",
            turn=turn,
            actor="Moderator",
            summary=f"Selected {selected.candidate_id}.",
            payload={
                "ranked_candidate_ids": [candidate.candidate_id for candidate in ranked],
                "selected_candidate_id": selected.candidate_id,
                "rejected_candidate_ids": [candidate.candidate_id for candidate in rejected],
                "selected_semantic_slot_counts": dict(sorted(selected_semantic_slot_counts.items())),
                "tournament_ranks": {candidate_id: item["rank"] for candidate_id, item in tournament.items()},
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
            payload={
                "candidate_id": selected.candidate_id,
                "route": classification.route,
                "forum": selected.forum,
            },
        )
        telemetry.record(
            event_type="workflow.stage",
            turn=turn,
            actor="DataAgent",
            summary=f"Recorded workflow route {classification.route}.",
            payload={"route": classification.route},
        )
        selected_record = _candidate_record(selected, tournament, reflections, evolutions)
        statistical_evidence = evidence_for_candidate(selected_record, statistical_execution_report)
        turn_record = {
            "turn": turn,
            "selected_candidate": selected_record,
            "rejected_candidates": [_candidate_record(candidate, tournament, reflections, evolutions) for candidate in rejected],
            "classification": classification.to_dict(),
            "statistical_evidence": statistical_evidence,
            "reviews": reviews,
            "mapping": mapped,
        }
        telemetry.record(
            event_type="statistics.attached",
            turn=turn,
            actor="DataAgent",
            summary="Attached candidate-scoped statistical execution evidence.",
            payload={
                "candidate_id": selected.candidate_id,
                "result_count": statistical_evidence["result_count"],
                "has_adjusted_significance": statistical_evidence["has_adjusted_significance"],
            },
        )
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
            "reasoning_mode": reasoning_config.mode,
            "reasoning_provider": "openai" if reasoning_config.mode in {"openai", "replay"} else "deterministic",
            "openai_model": reasoning_config.model if reasoning_config.mode in {"openai", "replay"} else None,
            "prior_notebook_knowledge_entry_count": notebook_knowledge_summary["entry_count"],
            "prior_notebook_knowledge_path": notebook_knowledge_summary["source_path"],
            "prior_knowledge_duplicate_candidate_count": prior_knowledge_duplicate_candidate_count,
            "selected_semantic_slot_counts": dict(sorted(selected_semantic_slot_counts.items())),
            "selected_unique_semantic_slot_count": len(selected_semantic_slot_counts),
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


def _candidate_record(
    candidate: Candidate,
    tournament: dict[str, dict[str, object]],
    reflections: dict[str, dict[str, object]],
    evolutions: dict[str, dict[str, object]],
) -> dict[str, object]:
    data = candidate.to_dict()
    data["tournament"] = tournament[candidate.candidate_id]
    data["reflection"] = reflections[candidate.candidate_id]
    data["evolution"] = evolutions[candidate.candidate_id]
    return data


def _annotate_semantic_slot_usage(
    candidates: list[Candidate],
    *,
    selected_semantic_slot_counts: dict[str, int],
) -> list[Candidate]:
    annotated = []
    for candidate in candidates:
        prior_count = selected_semantic_slot_counts.get(candidate.semantic_slot, 0)
        annotated.append(
            replace(
                candidate,
                reasoning={
                    **candidate.reasoning,
                    "semantic_slot_prior_selection_count": prior_count,
                },
            )
        )
    return annotated


def _select_diverse_candidate(
    ranked: list[Candidate],
    *,
    reflections: dict[str, dict[str, object]],
    selected_semantic_slot_counts: dict[str, int],
) -> Candidate:
    eligible = [candidate for candidate in ranked if reflections[candidate.candidate_id]["status"] != "not-answerable"]
    pool = eligible if eligible else ranked
    non_duplicate_pool = [
        candidate for candidate in pool if not bool(candidate.reasoning.get("prior_knowledge_duplicate"))
    ]
    selection_pool = non_duplicate_pool if non_duplicate_pool else pool
    minimum_prior_count = min(selected_semantic_slot_counts.get(candidate.semantic_slot, 0) for candidate in selection_pool)
    least_used = [
        candidate
        for candidate in selection_pool
        if selected_semantic_slot_counts.get(candidate.semantic_slot, 0) == minimum_prior_count
    ]
    return least_used[0]


def _openai_candidates(
    *,
    turn: int,
    proposals: list[OpenAIProposal],
    spark: Spark,
    notebook_knowledge_summary: dict[str, object],
    reasoning: dict[str, object],
) -> list[Candidate]:
    recent_seed_questions = [
        question for question in notebook_knowledge_summary.get("recent_seed_questions", []) if isinstance(question, str)
    ]
    duplicate_threshold = 0.62
    candidate_records: list[Candidate] = []
    for index, proposal in enumerate(proposals, start=1):
        similarity = _prior_question_similarity(proposal.question, recent_seed_questions)
        is_duplicate = similarity >= duplicate_threshold
        candidate_records.append(
            Candidate(
                candidate_id=f"turn-{turn:02d}-openai-{index:02d}-{_slug(proposal.semantic_slot)}",
                question=proposal.question,
                rationale=proposal.rationale,
                semantic_slot=proposal.semantic_slot,
                evidence_value=proposal.evidence_value,
                testability=proposal.testability,
                novelty=1 if is_duplicate else proposal.novelty,
                caveat=proposal.caveat,
                forum=spark.forum_metadata_for_openai(proposal),
                reasoning={
                    **reasoning,
                    "proposal_index": index,
                    "prior_knowledge_duplicate": is_duplicate,
                    "prior_knowledge_similarity": round(similarity, 3),
                    "prior_knowledge_duplicate_threshold": duplicate_threshold,
                },
            )
        )
    return sorted(candidate_records, key=lambda candidate: candidate.candidate_id)


def _prior_question_similarity(question: str, prior_questions: list[str]) -> float:
    question_tokens = _question_tokens(question)
    if not question_tokens:
        return 0.0
    scores = []
    for prior_question in prior_questions:
        prior_tokens = _question_tokens(prior_question)
        if prior_tokens:
            scores.append(len(question_tokens & prior_tokens) / len(question_tokens | prior_tokens))
    return max(scores, default=0.0)


def _question_tokens(question: str) -> set[str]:
    stop_words = {
        "a",
        "after",
        "and",
        "are",
        "do",
        "for",
        "have",
        "in",
        "of",
        "the",
        "to",
        "which",
        "with",
    }
    return {token for token in re.findall(r"[a-z0-9]+", question.casefold()) if token not in stop_words}


def _slug(value: str) -> str:
    return "".join(character if character.isalnum() else "-" for character in value.lower()).strip("-")


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
