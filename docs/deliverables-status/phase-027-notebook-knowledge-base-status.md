# Phase 027 Deliverables Status: Notebook Knowledge Base

## Completed Items

- Added `app/notebook_knowledge_base.py`.
- Added structured notebook knowledge JSON generation.
- Added compact notebook knowledge Markdown generation.
- Integrated knowledge-base writing after notebook execution.
- Added notebook workspace summary flags.
- Added phase-regression knowledge fields.
- Added audit knowledge fields.
- Added focused tests.
- Ran MAF replay smoke.
- Ran 20-turn OpenAI replay phase regression.
- Refreshed replication audit against Phase 027.

## Blocked/Deferred Items

- Candidate policy does not yet use notebook knowledge as follow-up seeds.
- Live OpenAI evidence remains blocked by missing `OPENAI_API_KEY`.

## Files Changed

- `app/notebook_knowledge_base.py`
- `app/notebook_workspace.py`
- `app/phase_regression.py`
- `app/replication_audit.py`
- `scripts/run_phase_regression.py`
- `scripts/run_replication_audit.py`
- `tests/test_notebook_knowledge_base.py`
- `tests/test_notebook_workspace.py`
- `tests/test_replication_audit.py`
- `app/runs/phase-027-notebook-knowledge-base/`
- `docs/phases/phase-027-notebook-knowledge-base-engineering-requirements.md`
- `docs/backlog/phase-027-notebook-knowledge-base-backlog.md`
- `docs/demos/phase-027-notebook-knowledge-base-demo.md`
- `docs/deliverables-status/phase-027-notebook-knowledge-base-status.md`

## Dependencies Installed

No new dependencies were installed.

## Tests Run

- `python3 -m pytest tests/test_notebook_knowledge_base.py tests/test_notebook_workspace.py tests/test_phase_regression.py -q`: passed, 9 tests.
- `python3 scripts/run_maf_adapter_smoke.py --reasoning-mode replay --openai-model gpt-5 --openai-replay-path data/reference/openai_hypothesis_replay.json --output-dir app/runs/phase-027-notebook-knowledge-base`: passed.
- `python3 scripts/run_phase_regression.py --phase-id phase-027-notebook-knowledge-base --turns 20 --reasoning-mode replay --openai-model gpt-5 --openai-replay-path data/reference/openai_hypothesis_replay.json`: passed.
- `python3 scripts/run_replication_audit.py --run-dir app/runs/phase-027-notebook-knowledge-base --output-dir app/runs/phase-027-notebook-knowledge-base`: passed.
- `python3 -m pytest tests/test_notebook_knowledge_base.py tests/test_notebook_workspace.py tests/test_phase_regression.py tests/test_replication_audit.py -q`: passed, 10 tests.
- `bash scripts/validate.sh`: passed, 61 tests.

## Demo Evidence

See `docs/demos/phase-027-notebook-knowledge-base-demo.md`.

Generated artifacts:

- `app/runs/phase-027-notebook-knowledge-base/notebooks/notebook-knowledge.json`
- `app/runs/phase-027-notebook-knowledge-base/notebooks/notebook-knowledge.md`
- `app/runs/phase-027-notebook-knowledge-base/phase_regression_summary.json`
- `app/runs/phase-027-notebook-knowledge-base/replication_audit.json`

## Acceptance Criteria Status

- `notebook-knowledge.json` exists in the Phase 027 notebook workspace: passed.
- `notebook-knowledge.md` exists in the Phase 027 notebook workspace: passed.
- Phase regression reports `notebook_knowledge_present=True`: passed.
- Audit reports `notebook_knowledge_entry_count=20`: passed.
- Full validation passes: passed.

## Risks

- Knowledge extraction is compact and may need richer validation-contract extraction later.
- Candidate policy does not yet consume the knowledge base.

## Commit Status

Pending until local commit completes.
