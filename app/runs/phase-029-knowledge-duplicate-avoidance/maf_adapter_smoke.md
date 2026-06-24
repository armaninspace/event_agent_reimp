# Microsoft Agent Framework Adapter Smoke

Schema: phase-025.maf-openai-bridge.v1
Framework: Microsoft Agent Framework
Package: agent-framework 1.9.0
Workflow: codex-thesis-replication-workflow
Executor: codex-openai-hypothesis-generator
Reasoning provider: openai
Reasoning mode: replay
Reasoning model: gpt-5
Model calls performed: False
Candidate count: 3
Output count: 1

## Candidate Questions

- Which city game weeks show the largest spending lift after accounting for baseline weeks?
- Which MSAs have enough game and non-game weeks for a stable comparison?
- Where do game weeks overlap with likely confounders in the weekly spending data?

## Outputs

- {"candidate_count": 3, "candidate_questions": ["Which city game weeks show the largest spending lift after accounting for baseline weeks?", "Which MSAs have enough game and non-game weeks for a stable comparison?", "Where do game weeks overlap with likely confounders in the weekly spending data?"], "message": "replicate governed thesis workflow", "mode": "replay", "model": "gpt-5", "model_calls_performed": false, "output_hash": "3968c0b9d6714dcb4a1946c2d568ebe869536184bf9b11926361ab41dd2397bf", "prompt_hash": "99bf911f313119552813c67b70597a9b6a12821a2e88be75d10b1c98c590b4cf", "provider": "openai", "trace_path": "app/runs/phase-029-knowledge-duplicate-avoidance/openai-reasoning/turn-01-openai-reasoning.json"}
