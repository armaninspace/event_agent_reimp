# Microsoft Agent Framework Adapter Smoke

Schema: phase-025.maf-openai-bridge.v1
Framework: Microsoft Agent Framework
Package: agent-framework 1.9.0
Workflow: codex-thesis-replication-workflow
Executor: codex-openai-hypothesis-generator
Reasoning provider: openai
Reasoning mode: openai
Reasoning model: gpt-5
Model calls performed: True
Candidate count: 3
Output count: 1

## Candidate Questions

- By how much does city-level weekly card spending increase during high-attendance sports event weeks compared with matched non-event weeks in the same season?
- Which MSAs have sufficient counts of event and non-event weeks (e.g., at least 8 each) to support stable within-MSA spending comparisons?
- In which cities do event weeks systematically coincide with holidays or seasonally high-spending weeks, indicating elevated confounding risk for event–spending estimates?

## Outputs

- {"candidate_count": 3, "candidate_questions": ["By how much does city-level weekly card spending increase during high-attendance sports event weeks compared with matched non-event weeks in the same season?", "Which MSAs have sufficient counts of event and non-event weeks (e.g., at least 8 each) to support stable within-MSA spending comparisons?", "In which cities do event weeks systematically coincide with holidays or seasonally high-spending weeks, indicating elevated confounding risk for event\u2013spending estimates?"], "message": "replicate governed thesis workflow", "mode": "openai", "model": "gpt-5", "model_calls_performed": true, "output_hash": "5c3086a4132981c7eb136da79eba557f031ebd56d05d31b6213c2f68e729822a", "prompt_hash": "99bf911f313119552813c67b70597a9b6a12821a2e88be75d10b1c98c590b4cf", "provider": "openai", "trace_path": "app/runs/phase-033-live-openai-environment/openai-reasoning/turn-01-openai-reasoning.json"}
