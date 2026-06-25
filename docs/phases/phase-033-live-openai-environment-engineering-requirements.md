# Phase 033: Live OpenAI Environment

## Phase Goal

Produce a full live OpenAI-backed environment run using the caller-provided `.env` credentials.

## Requirements

- Load `.env` into the process environment without printing secrets.
- Run a one-turn live OpenAI smoke workflow.
- Run a 20-turn live OpenAI phase regression.
- Run a live Microsoft Agent Framework smoke workflow.
- Refresh the replication audit against the live artifacts.
- Make audit known limits mode-aware so live evidence is not mislabeled as replay evidence.

## Non-Goals

- Committing `.env` or any secret value.
- Printing API keys.
- Claiming observational evidence is causal proof.

## Acceptance Criteria

- Live smoke reports `model_calls_performed=True`.
- Phase regression reports `reasoning_mode=openai`.
- Phase regression reports `openai_model_calls_performed=True`.
- MAF smoke reports `reasoning_mode=openai` and `model_calls_performed=True`.
- Audit reports live OpenAI and live MAF evidence.
- Full validation passes.
