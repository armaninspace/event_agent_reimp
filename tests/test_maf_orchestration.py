import json
from pathlib import Path

from app.maf_orchestration import run_maf_adapter_sync, write_maf_adapter_smoke


def test_maf_adapter_runs_deterministic_workflow_without_model_calls() -> None:
    report = run_maf_adapter_sync("governed public question")

    assert report.framework_name == "Microsoft Agent Framework"
    assert report.package_name == "agent-framework"
    assert report.package_version
    assert report.workflow_name == "codex-thesis-replication-workflow"
    assert report.output_count == 1
    assert report.outputs == ["MAF deterministic orchestration accepted: governed public question"]
    assert report.reasoning_provider == "deterministic"
    assert report.reasoning_mode == "deterministic"
    assert report.model_calls_performed is False
    assert report.candidate_count == 0


def test_maf_adapter_smoke_writes_artifacts(tmp_path: Path) -> None:
    report = run_maf_adapter_sync("artifact smoke")

    json_path, markdown_path = write_maf_adapter_smoke(report, tmp_path)

    assert json_path.exists()
    assert markdown_path.exists()
    assert "Microsoft Agent Framework Adapter Smoke" in markdown_path.read_text(encoding="utf-8")


def test_maf_adapter_replay_invokes_openai_reasoning_inside_workflow(tmp_path: Path) -> None:
    replay_path = tmp_path / "openai_replay.json"
    replay_path.write_text(
        json.dumps(
            {
                "turns": {
                    "1": json.dumps(
                        {
                            "candidates": [
                                {
                                    "question": "Which city game weeks show spending lift?",
                                    "rationale": "Tests the city-week spending table.",
                                    "semantic_slot": "city_week_event_spending",
                                    "evidence_value": 8,
                                    "testability": 8,
                                    "novelty": 6,
                                    "caveat": "Observational only.",
                                    "forum_question_id": "crowd-spending",
                                },
                                {
                                    "question": "Which MSAs have sufficient coverage?",
                                    "rationale": "Tests MSA-week coverage.",
                                    "semantic_slot": "msa_week_coverage",
                                    "evidence_value": 7,
                                    "testability": 8,
                                    "novelty": 6,
                                    "caveat": "Coverage is not impact.",
                                    "forum_question_id": "market-coverage",
                                },
                                {
                                    "question": "Where could game timing be confounded?",
                                    "rationale": "Surfaces identification risks.",
                                    "semantic_slot": "identification_risk",
                                    "evidence_value": 6,
                                    "testability": 7,
                                    "novelty": 7,
                                    "caveat": "Needs external calendars.",
                                    "forum_question_id": "confounding-risk",
                                },
                            ]
                        }
                    )
                }
            }
        ),
        encoding="utf-8",
    )

    report = run_maf_adapter_sync(
        "provider-backed smoke",
        reasoning_mode="replay",
        openai_model="gpt-5",
        openai_replay_path=replay_path,
        openai_trace_dir=tmp_path / "traces",
    )

    assert report.executor_id == "codex-openai-hypothesis-generator"
    assert report.reasoning_provider == "openai"
    assert report.reasoning_mode == "replay"
    assert report.reasoning_model == "gpt-5"
    assert report.model_calls_performed is False
    assert report.candidate_count == 3
    assert len(report.candidate_questions) == 3
    assert len(report.trace_paths) == 1
    assert Path(report.trace_paths[0]).exists()
