# Phase Delivery

Use this skill for any substantial implementation, documentation, workflow, or validation phase.

## Required Phase Artifacts

For each phase, create or update:

- `docs/phases/<phase-id>-engineering-requirements.md`
- `docs/backlog/<phase-id>-backlog.md`
- `docs/demos/<phase-id>-demo.md`
- `docs/deliverables-status/<phase-id>-status.md`

Use stable phase identifiers such as `phase-000-codex-surface`.

## Engineering Requirements Document

Each phase engineering document must include:

- phase goal
- requirements
- non-goals
- assumptions
- affected layers
- affected modules
- dependency/library choices
- architecture notes
- data/API/config changes
- demo requirements
- test requirements
- security/sandbox considerations
- risks
- acceptance criteria
- rollback plan

Write requirements concretely enough that implementation and review can compare work against the document.

## Backlog Document

Each backlog item must include:

- stable item ID
- title
- rationale
- affected files/modules
- implementation steps
- unit test expectations
- e2e test expectations
- demo relevance
- acceptance criteria
- status

Statuses should be explicit: `pending`, `in-progress`, `done`, `blocked`, or `deferred`.

## Phase Loop

1. Create the engineering and requirements document.
2. Build a detailed backlog from that document.
3. Execute backlog items slice by slice.
4. Unit test and e2e test each slice where applicable.
5. Diagnose blockers, replan, and continue safe unblocked work.
6. Record a demo with evidence.
7. Write deliverables status.
8. Commit the phase locally.
9. Re-evaluate the plan and replace it when replanning improves success odds.
