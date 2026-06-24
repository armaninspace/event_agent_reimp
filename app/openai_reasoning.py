"""OpenAI-backed hypothesis generation for the friends loop."""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Protocol

from app.question_forum import QuestionForumRecord


DEFAULT_OPENAI_MODEL = "gpt-5"
ALLOWED_REASONING_MODES = frozenset({"deterministic", "openai", "replay"})
REQUIRED_CANDIDATE_FIELDS = frozenset(
    {
        "question",
        "rationale",
        "semantic_slot",
        "evidence_value",
        "testability",
        "novelty",
        "caveat",
    }
)


class TextGenerationClient(Protocol):
    """Minimal text generation protocol for live OpenAI and tests."""

    def create_text(self, *, model: str, prompt: str) -> str:
        """Return model output text for a prompt."""


@dataclass(frozen=True)
class OpenAIReasoningConfig:
    """Configuration for OpenAI-backed hypothesis generation."""

    mode: str = "deterministic"
    model: str = DEFAULT_OPENAI_MODEL
    trace_dir: Path | None = None
    replay_path: Path | None = None

    @classmethod
    def from_env(
        cls,
        *,
        mode: str = "deterministic",
        model: str | None = None,
        trace_dir: Path | None = None,
        replay_path: Path | None = None,
    ) -> "OpenAIReasoningConfig":
        """Create config using explicit values first, then environment defaults."""
        resolved_mode = _normalize_mode(mode)
        resolved_model = model or os.environ.get("OPENAI_MODEL") or DEFAULT_OPENAI_MODEL
        return cls(mode=resolved_mode, model=resolved_model, trace_dir=trace_dir, replay_path=replay_path)


@dataclass(frozen=True)
class OpenAIProposal:
    """One normalized model-generated candidate proposal."""

    question: str
    rationale: str
    semantic_slot: str
    evidence_value: int
    testability: int
    novelty: int
    caveat: str
    forum_question_id: str

    def to_dict(self) -> dict[str, object]:
        """Return JSON-serializable proposal data."""
        return asdict(self)


@dataclass(frozen=True)
class OpenAIProposalBatch:
    """Parsed model output plus provenance needed for audit and replay."""

    mode: str
    provider: str
    model: str
    prompt_hash: str
    output_hash: str
    raw_output: str
    model_calls_performed: bool
    proposals: list[OpenAIProposal]
    trace_path: str | None = None

    def to_dict(self) -> dict[str, object]:
        """Return JSON-serializable proposal batch data."""
        data = asdict(self)
        data["proposals"] = [proposal.to_dict() for proposal in self.proposals]
        return data


class OpenAIResponsesClient:
    """Thin wrapper over the official OpenAI Python SDK Responses API."""

    def create_text(self, *, model: str, prompt: str) -> str:
        """Call OpenAI and return response output text."""
        if not os.environ.get("OPENAI_API_KEY"):
            raise RuntimeError(
                "OPENAI_API_KEY is required for reasoning_mode='openai'. "
                "Set it in the process environment before running a live model-backed loop."
            )
        from openai import OpenAI

        client = OpenAI()
        response = client.responses.create(model=model, input=prompt)
        output_text = getattr(response, "output_text", None)
        if isinstance(output_text, str) and output_text.strip():
            return output_text
        output = getattr(response, "output", None)
        if isinstance(output, list):
            chunks: list[str] = []
            for item in output:
                content = getattr(item, "content", None)
                if isinstance(content, list):
                    for content_item in content:
                        text = getattr(content_item, "text", None)
                        if isinstance(text, str):
                            chunks.append(text)
            if chunks:
                return "\n".join(chunks)
        raise RuntimeError("OpenAI response did not contain output_text.")


class OpenAIHypothesisGenerator:
    """Generate candidate research hypotheses using OpenAI or replay traces."""

    def __init__(self, *, config: OpenAIReasoningConfig, client: TextGenerationClient | None = None) -> None:
        if config.mode not in {"openai", "replay"}:
            raise ValueError(f"OpenAIHypothesisGenerator does not support mode={config.mode!r}.")
        self._config = config
        self._client = client or OpenAIResponsesClient()

    def propose(
        self,
        *,
        turn: int,
        forum_records: list[QuestionForumRecord],
        prior_selected_ids: set[str],
        prior_selected_forum_ids: set[str],
        notebook_knowledge_summary: dict[str, object] | None = None,
    ) -> OpenAIProposalBatch:
        """Return parsed proposals from live OpenAI or an explicit replay trace."""
        prompt = build_hypothesis_prompt(
            turn=turn,
            forum_records=forum_records,
            prior_selected_ids=prior_selected_ids,
            prior_selected_forum_ids=prior_selected_forum_ids,
            notebook_knowledge_summary=notebook_knowledge_summary,
        )
        prompt_hash = _sha256(prompt)
        if self._config.mode == "replay":
            raw_output = _load_replay_output(self._config.replay_path, turn=turn)
            model_calls_performed = False
        else:
            raw_output = self._client.create_text(model=self._config.model, prompt=prompt)
            model_calls_performed = True
        proposals = parse_openai_proposals(raw_output, forum_records=forum_records)
        batch = OpenAIProposalBatch(
            mode=self._config.mode,
            provider="openai",
            model=self._config.model,
            prompt_hash=prompt_hash,
            output_hash=_sha256(raw_output),
            raw_output=raw_output,
            model_calls_performed=model_calls_performed,
            proposals=proposals,
        )
        trace_path = self._write_trace(batch=batch, prompt=prompt, turn=turn)
        if trace_path is None:
            return batch
        return OpenAIProposalBatch(**{**batch.to_dict(), "trace_path": str(trace_path), "proposals": proposals})

    def _write_trace(self, *, batch: OpenAIProposalBatch, prompt: str, turn: int) -> Path | None:
        if self._config.trace_dir is None:
            return None
        self._config.trace_dir.mkdir(parents=True, exist_ok=True)
        path = self._config.trace_dir / f"turn-{turn:02d}-openai-reasoning.json"
        payload = batch.to_dict()
        payload["prompt"] = prompt
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return path


def build_hypothesis_prompt(
    *,
    turn: int,
    forum_records: list[QuestionForumRecord],
    prior_selected_ids: set[str],
    prior_selected_forum_ids: set[str],
    notebook_knowledge_summary: dict[str, object] | None = None,
) -> str:
    """Build the prompt sent to OpenAI for hypothesis generation."""
    forum_payload = [
        {
            "question_id": record.question_id,
            "kind": record.kind,
            "persona": record.persona,
            "question": record.question,
            "rationale": record.rationale,
            "priority": record.priority,
            "popularity": record.popularity,
            "tags": record.tags,
        }
        for record in forum_records[:20]
    ]
    contract = {
        "candidates": [
            {
                "question": "Stakeholder-readable empirical question.",
                "rationale": "Why this is valuable and testable with the local city/MSA weekly event data.",
                "semantic_slot": "city_week_event_spending | msa_week_coverage | identification_risk",
                "evidence_value": "integer 0-10",
                "testability": "integer 0-10",
                "novelty": "integer 0-10",
                "caveat": "One sentence limitation.",
                "forum_question_id": "source forum question_id when applicable",
            }
        ]
    }
    return "\n".join(
        [
            "You are the hypothesis-generation agent for a Python replication of an event-spending thesis.",
            "Generate exactly three candidate research questions for the next friends-loop turn.",
            "Use the provided public QuestionForum records and avoid repeating already selected forum IDs.",
            "Return only strict JSON. Do not wrap it in markdown.",
            "",
            f"Turn: {turn}",
            f"Prior selected candidate IDs: {sorted(prior_selected_ids)}",
            f"Prior selected forum IDs: {sorted(prior_selected_forum_ids)}",
            "Prior notebook knowledge summary:",
            json.dumps(notebook_knowledge_summary or {}, indent=2, sort_keys=True),
            "",
            "Available semantic slots: city_week_event_spending, msa_week_coverage, identification_risk",
            "Scoring fields must be integers from 0 to 10.",
            "",
            "Output contract:",
            json.dumps(contract, indent=2, sort_keys=True),
            "",
            "QuestionForum records:",
            json.dumps(forum_payload, indent=2, sort_keys=True),
        ]
    )


def parse_openai_proposals(raw_output: str, *, forum_records: list[QuestionForumRecord]) -> list[OpenAIProposal]:
    """Parse and validate model output into normalized proposals."""
    data = _json_from_output(raw_output)
    candidates = data.get("candidates") if isinstance(data, dict) else None
    if not isinstance(candidates, list):
        raise ValueError("OpenAI hypothesis output must contain a candidates list.")
    if len(candidates) < 3:
        raise ValueError("OpenAI hypothesis output must contain at least three candidates.")
    forum_ids = {record.question_id for record in forum_records}
    proposals = [_proposal_from_candidate(item, forum_ids=forum_ids, index=index) for index, item in enumerate(candidates[:3])]
    questions = [proposal.question.casefold() for proposal in proposals]
    if len(set(questions)) != len(questions):
        raise ValueError("OpenAI hypothesis output contains duplicate candidate questions.")
    return proposals


def _proposal_from_candidate(item: object, *, forum_ids: set[str], index: int) -> OpenAIProposal:
    if not isinstance(item, dict):
        raise ValueError(f"OpenAI candidate {index} must be an object.")
    missing = sorted(REQUIRED_CANDIDATE_FIELDS - item.keys())
    if missing:
        raise ValueError(f"OpenAI candidate {index} is missing fields: {', '.join(missing)}.")
    forum_question_id = str(item.get("forum_question_id") or f"openai-generated-{index + 1}")
    if forum_question_id not in forum_ids and not forum_question_id.startswith("openai-generated-"):
        forum_question_id = f"openai-generated-{index + 1}"
    return OpenAIProposal(
        question=_non_empty_string(item["question"], field="question", index=index),
        rationale=_non_empty_string(item["rationale"], field="rationale", index=index),
        semantic_slot=_semantic_slot(item["semantic_slot"], index=index),
        evidence_value=_bounded_int(item["evidence_value"], field="evidence_value", index=index),
        testability=_bounded_int(item["testability"], field="testability", index=index),
        novelty=_bounded_int(item["novelty"], field="novelty", index=index),
        caveat=_non_empty_string(item["caveat"], field="caveat", index=index),
        forum_question_id=forum_question_id,
    )


def _json_from_output(raw_output: str) -> dict[str, object]:
    text = raw_output.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("OpenAI hypothesis output was not valid JSON.") from exc
    if not isinstance(data, dict):
        raise ValueError("OpenAI hypothesis output must be a JSON object.")
    return data


def _load_replay_output(replay_path: Path | None, *, turn: int) -> str:
    if replay_path is None:
        raise ValueError("reasoning_mode='replay' requires openai_replay_path.")
    data = json.loads(replay_path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and "turns" in data:
        turns = data["turns"]
        if not isinstance(turns, dict):
            raise ValueError("OpenAI replay turns must be an object keyed by turn number.")
        raw_output = turns.get(str(turn)) or turns.get(f"{turn:02d}") or turns.get("default")
    elif isinstance(data, dict):
        raw_output = data.get("raw_output")
    else:
        raw_output = None
    if not isinstance(raw_output, str) or not raw_output.strip():
        raise ValueError(f"OpenAI replay does not contain raw output for turn {turn}.")
    return raw_output


def _normalize_mode(mode: str) -> str:
    normalized = mode.strip().lower()
    if normalized not in ALLOWED_REASONING_MODES:
        raise ValueError(f"Unsupported reasoning mode: {mode}. Expected one of {sorted(ALLOWED_REASONING_MODES)}.")
    return normalized


def _semantic_slot(value: object, *, index: int) -> str:
    slot = _non_empty_string(value, field="semantic_slot", index=index)
    allowed = {"city_week_event_spending", "msa_week_coverage", "identification_risk"}
    if slot not in allowed:
        raise ValueError(f"OpenAI candidate {index} semantic_slot must be one of {sorted(allowed)}.")
    return slot


def _bounded_int(value: object, *, field: str, index: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"OpenAI candidate {index} {field} must be an integer.")
    if not 0 <= value <= 10:
        raise ValueError(f"OpenAI candidate {index} {field} must be between 0 and 10.")
    return value


def _non_empty_string(value: object, *, field: str, index: int) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"OpenAI candidate {index} {field} must be a non-empty string.")
    return value.strip()


def _sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()
