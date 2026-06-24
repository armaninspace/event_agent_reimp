import json
from pathlib import Path

import pytest

from app.friends_loop import run_friends_question_loop
from app.openai_reasoning import (
    OpenAIHypothesisGenerator,
    OpenAIReasoningConfig,
    OpenAIResponsesClient,
    parse_openai_proposals,
)
from app.question_forum import load_question_forum


def _raw_candidates() -> str:
    return json.dumps(
        {
            "candidates": [
                {
                    "question": "Which city game weeks show the largest spending lift after accounting for baseline weeks?",
                    "rationale": "This tests the headline spending question against the city-week table.",
                    "semantic_slot": "city_week_event_spending",
                    "evidence_value": 8,
                    "testability": 8,
                    "novelty": 5,
                    "caveat": "The result remains observational without matched controls.",
                    "forum_question_id": "crowd-spending",
                },
                {
                    "question": "Which MSAs have enough game and non-game weeks for a stable comparison?",
                    "rationale": "Coverage determines where later statistical tests are credible.",
                    "semantic_slot": "msa_week_coverage",
                    "evidence_value": 7,
                    "testability": 9,
                    "novelty": 6,
                    "caveat": "Coverage does not estimate impact by itself.",
                    "forum_question_id": "market-coverage",
                },
                {
                    "question": "Where do game weeks overlap with likely confounders in the weekly spending data?",
                    "rationale": "A skeptical pass identifies markets where timing may bias conclusions.",
                    "semantic_slot": "identification_risk",
                    "evidence_value": 6,
                    "testability": 7,
                    "novelty": 7,
                    "caveat": "Confounding review needs external calendars for full resolution.",
                    "forum_question_id": "confounding-risk",
                },
            ]
        }
    )


def _write_reference_files(reference_dir: Path) -> None:
    reference_dir.mkdir()
    (reference_dir / "joined_city_week_game_economic.csv").write_text(
        "cityid,cityname,stateabbrev,week_start_monday,revenue_all,merchants_all,has_game,game_count\n"
        "1,Alpha,AA,2026-01-05,10.0,2.0,1,1\n"
        "2,Beta,BB,2026-01-12,12.0,3.0,0,0\n",
        encoding="utf-8",
    )
    (reference_dir / "joined_msa_week_game_economic.csv").write_text(
        "msa,msa_code,week_start_monday,revenue_all,merchants_all,has_game,game_count,msa_block_id\n"
        "Metro A,10000,2026-01-05,20.0,3.0,1,1,block-a\n",
        encoding="utf-8",
    )


class FakeTextClient:
    def __init__(self, output: str) -> None:
        self.output = output
        self.calls: list[dict[str, str]] = []

    def create_text(self, *, model: str, prompt: str) -> str:
        self.calls.append({"model": model, "prompt": prompt})
        return self.output


def test_parse_openai_proposals_requires_three_valid_candidates() -> None:
    forum_records = load_question_forum()

    proposals = parse_openai_proposals(_raw_candidates(), forum_records=forum_records)

    assert len(proposals) == 3
    assert proposals[0].forum_question_id == "crowd-spending"
    assert proposals[0].semantic_slot == "city_week_event_spending"


def test_openai_generator_live_uses_client_and_writes_trace(tmp_path: Path) -> None:
    forum_records = load_question_forum()
    client = FakeTextClient(_raw_candidates())
    generator = OpenAIHypothesisGenerator(
        config=OpenAIReasoningConfig(mode="openai", model="gpt-5", trace_dir=tmp_path),
        client=client,
    )

    batch = generator.propose(
        turn=1,
        forum_records=forum_records,
        prior_selected_ids=set(),
        prior_selected_forum_ids=set(),
        notebook_knowledge_summary={"entry_count": 2, "latest_seed_question": "Prior question?"},
    )

    assert len(client.calls) == 1
    assert "Prior question?" in client.calls[0]["prompt"]
    assert batch.provider == "openai"
    assert batch.mode == "openai"
    assert batch.model_calls_performed is True
    assert batch.trace_path
    assert Path(batch.trace_path).exists()
    trace = json.loads(Path(batch.trace_path).read_text(encoding="utf-8"))
    assert trace["provider"] == "openai"
    assert trace["model_calls_performed"] is True
    assert trace["prompt_hash"]
    assert trace["raw_output"]


def test_openai_live_mode_requires_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(RuntimeError, match="OPENAI_API_KEY is required"):
        OpenAIResponsesClient().create_text(model="gpt-5", prompt="Generate one question.")


def test_friends_loop_replay_marks_openai_reasoning_without_live_call(tmp_path: Path) -> None:
    reference_dir = tmp_path / "reference"
    _write_reference_files(reference_dir)
    replay_path = tmp_path / "openai_replay.json"
    replay_path.write_text(json.dumps({"turns": {"1": _raw_candidates()}}), encoding="utf-8")

    session = run_friends_question_loop(
        turn_count=1,
        output_dir=tmp_path / "run",
        reference_dir=reference_dir,
        reasoning_mode="replay",
        openai_model="gpt-5",
        openai_replay_path=replay_path,
    )

    selected = session["turns"][0]["selected_candidate"]
    assert selected["reasoning"]["provider"] == "openai"
    assert selected["reasoning"]["mode"] == "replay"
    assert selected["reasoning"]["model_calls_performed"] is False
    assert selected["reasoning"]["trace_path"]
    telemetry = json.loads(Path(session["artifact_paths"]["telemetry_json"]).read_text(encoding="utf-8"))
    openai_events = [event for event in telemetry if event["event_type"] == "openai.reasoning.completed"]
    assert len(openai_events) == 1
    assert openai_events[0]["payload"]["model_calls_performed"] is False


def test_friends_loop_replay_reads_prior_notebook_knowledge(tmp_path: Path) -> None:
    reference_dir = tmp_path / "reference"
    _write_reference_files(reference_dir)
    replay_path = tmp_path / "openai_replay.json"
    replay_path.write_text(json.dumps({"turns": {"1": _raw_candidates()}}), encoding="utf-8")
    knowledge_path = tmp_path / "notebook-knowledge.json"
    knowledge_path.write_text(
        json.dumps(
            {
                "entry_count": 1,
                "entries": [
                    {
                        "seed_question": "Prior notebook seed?",
                        "semantic_slot": "city_week_event_spending",
                        "source_cell_ids": ["turn-01-validation-code"],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    session = run_friends_question_loop(
        turn_count=1,
        output_dir=tmp_path / "run",
        reference_dir=reference_dir,
        reasoning_mode="replay",
        openai_model="gpt-5",
        openai_replay_path=replay_path,
        prior_notebook_knowledge_path=knowledge_path,
    )

    assert session["session_summary"]["prior_notebook_knowledge_entry_count"] == 1
    telemetry = json.loads(Path(session["artifact_paths"]["telemetry_json"]).read_text(encoding="utf-8"))
    knowledge_events = [event for event in telemetry if event["event_type"] == "knowledge.read"]
    assert knowledge_events[0]["payload"]["notebook_knowledge"]["latest_seed_question"] == "Prior notebook seed?"
    trace_path = Path(session["turns"][0]["selected_candidate"]["reasoning"]["trace_path"])
    assert "Prior notebook seed?" in trace_path.read_text(encoding="utf-8")
