# Phase 009: Hypothesis Classification And Routing

## Phase Goal

Add deterministic hypothesis/workflow classification and routing so workflow tasks do not enter statistical testing, and make the 20-turn regression measure workflow-task statistical misroutes from real turn metadata.

## Requirements

- Implement classifier outcomes:
  - `statistical_hypothesis`
  - `eda_question`
  - `workflow_task`
- Workflow trigger words must include notebook, wiki, prompt, report, UI, and logging.
- Formal statistical hypotheses require H0, H1, population, unit, exposure, comparison, outcome, direction, test family, alpha, and decision rule.
- Add routing metadata to selected candidates.
- Add telemetry for `hypothesis.classified`, `question.submitted`, and `workflow.stage`.
- Regression summary must compute workflow-task statistical misroutes from turn metadata.
- Add tests for workflow-task classification and misroute counting.

## Non-Goals

- Run statistical tests.
- Implement formal hypothesis authoring UI.
- Live LLM classification.

## Assumptions

- Deterministic keyword and field-based classification is sufficient for this phase.
- Current friends-loop questions are EDA questions unless they satisfy formal hypothesis fields.
- Statistical execution remains deferred.

## Affected Layers

- Governance/routing
- Telemetry
- Regression validation
- Tests

## Affected Modules

- `app/hypothesis_routing.py`
- `app/friends_loop.py`
- `app/phase_regression.py`
- `tests/test_hypothesis_routing.py`
- `tests/test_friends_loop.py`
- `tests/test_phase_regression.py`

## Dependency/Library Choices

No new dependencies are required.

## Architecture Notes

Classification is isolated in `app.hypothesis_routing`. The friends loop records routing metadata without executing statistical tests. Regression treats a workflow task routed to `statistical_test` as a misroute.

## Data/API/Config Changes

- Turn records gain `classification` metadata.
- Telemetry gains classification and workflow-stage events.
- Regression summary computes `workflow_task_statistical_misroutes`.

## Demo Requirements

- Run 20-turn regression.
- Show misroutes are zero.
- Show classifier tests pass.

## Test Requirements

- Workflow artifact words classify as `workflow_task`.
- Formal hypothesis field set classifies as `statistical_hypothesis`.
- Current loop has zero workflow-task statistical misroutes.
- Validation passes.

## Security/Sandbox Considerations

- Do not log private chain-of-thought.
- Keep public rationale/caveats only.
- Do not run statistical execution yet.

## Risks

- Keyword classifier is intentionally simple.
- Later LLM-driven classification must preserve deterministic regression checks.

## Acceptance Criteria

- Notebook/wiki/report/UI/logging questions classify as workflow tasks.
- Workflow-task statistical misroutes are zero in 20-turn regression.
- Tests and validation pass.

## Rollback Plan

Revert Phase 009 commit or remove classifier integration, tests, artifacts, and docs.
