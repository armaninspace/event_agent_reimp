# Phase 009 Backlog: Hypothesis Classification And Routing

## P009-001: Implement Classifier

- Stable item ID: `P009-001`
- Title: Add deterministic hypothesis routing classifier
- Rationale: Workflow tasks must not enter statistical testing.
- Affected files/modules: `app/hypothesis_routing.py`
- Implementation steps: Add routing dataclass, workflow keyword detection, formal hypothesis field checks, and route decisions.
- Unit test expectations: Workflow and formal hypothesis examples classify correctly.
- E2E test expectations: 20-turn regression reports zero misroutes.
- Demo relevance: Summary includes misroute count.
- Acceptance criteria: Required outcomes are supported.
- Status: done

## P009-002: Integrate Routing Into Loop

- Stable item ID: `P009-002`
- Title: Add classification metadata and telemetry
- Rationale: Regression needs real turn metadata for misroute checks.
- Affected files/modules: `app/friends_loop.py`
- Implementation steps: Classify selected candidates, add turn metadata, emit classification and workflow-stage telemetry.
- Unit test expectations: Turn records include classification.
- E2E test expectations: Regression consumes metadata.
- Demo relevance: Telemetry records routing.
- Acceptance criteria: Each selected candidate has routing metadata.
- Status: done

## P009-003: Update Regression Misroute Calculation

- Stable item ID: `P009-003`
- Title: Compute workflow-task statistical misroutes
- Rationale: Misroute count should be measured, not hard-coded.
- Affected files/modules: `app/phase_regression.py`
- Implementation steps: Count selected turns where classification is workflow task and route is statistical test.
- Unit test expectations: Misroute helper is tested.
- E2E test expectations: 20-turn regression reports zero.
- Demo relevance: Summary records zero misroutes.
- Acceptance criteria: Misroute count comes from session metadata.
- Status: done

## P009-004: Validate, Demo, Status, Commit

- Stable item ID: `P009-004`
- Title: Close Phase 009
- Rationale: Phase protocol requires validation, demo, status, and local commit.
- Affected files/modules: Phase 009 docs and repository state.
- Implementation steps: Run tests, 20-turn regression, e2e, validation, document evidence, and commit locally.
- Unit test expectations: `python3 -m pytest -q` passes.
- E2E test expectations: `bash scripts/e2e.sh` exits successfully or neutrally.
- Demo relevance: Phase demo is updated.
- Acceptance criteria: Phase 009 is locally committed.
- Status: done
