# Codex Operating Protocol

This repository uses a Codex-compatible engineering surface for governed, phase-based work. Future sessions should treat this file as the durable project constitution and prefer the local workflow documents over ad hoc process.

## Surfaces

- Reusable procedural skills live under `.agents/skills/`.
- Codex lifecycle hook scaffolding lives under `.codex/hooks.json` and `.codex/hooks/`.
- Command guardrail conventions live under `.codex/rules/`.
- Specialist role definitions live under `.codex/agents/` as documented conventions.
- Audit documents live under `docs/`.
- Validation, e2e, and demo helpers live under `scripts/`.

## Phase Delivery

Use the `phase-delivery` skill for meaningful project work. Each phase must create or update:

- `docs/phases/<phase-id>-engineering-requirements.md`
- `docs/backlog/<phase-id>-backlog.md`
- `docs/demos/<phase-id>-demo.md`
- `docs/deliverables-status/<phase-id>-status.md`

The phase engineering document defines requirements, non-goals, assumptions, affected layers and modules, dependencies, architecture, data/API/config changes, demo and test requirements, security considerations, risks, acceptance criteria, and rollback.

The backlog document decomposes the phase into stable, testable slices. Each slice should be small enough to implement, validate, document, and demo independently when practical.

## Installed Software

Codex may install software inside the container when needed for implementation, testing, e2e validation, documentation, or demo recording. Every install must be recorded in `docs/installed-software.md` with:

- tool or package name
- version, when available
- install command
- reason installed
- classification as runtime, dev-only, test-only, or demo-only
- reproducibility or cleanup notes

## Backlog Slice Loop

Use the `backlog-slice` skill for implementation work:

1. Restate the slice goal.
2. Inspect relevant files.
3. Implement the smallest coherent change.
4. Add or update tests.
5. Run targeted tests.
6. Run relevant e2e checks.
7. Update docs and backlog status.
8. Record evidence.

## Blockers

Use the `replan-on-block` skill when blocked. Diagnose the root cause, attempt safe unblock paths, document evidence, mark unresolved items blocked, add a replan section, and continue unblocked work where possible.

## Demos And Status

Use the `demo-and-status` skill at phase end. Demo documents must include setup, commands, expected behavior, observed behavior, evidence, known gaps, and requirement mapping.

UI, dashboard, explorer, chart, report visualization, or other visual phases must reference an illustrative video under `demos/` unless video tooling is blocked and the blocker is documented. Non-UI phases must include command-output evidence and either a generated walkthrough video or a clear non-applicability rationale.

Deliverables-status documents must summarize completed work, blocked or deferred work, changed files, dependencies installed, tests run, demo evidence, video path or rationale, acceptance criteria status, risks, next phase, commit hash when available, and label or tag.

## Commits, Labels, And Tags

At the end of a phase, commit the completed phase locally and apply a label or tag when appropriate and explicitly safe. Do not push, merge, publish, or perform destructive actions without explicit user permission.

## Safety Rules

Codex must not:

- push to remotes without explicit permission
- merge pull requests without explicit permission
- publish packages, images, releases, or external artifacts without explicit permission
- run destructive commands such as broad `rm -rf` without explicit permission
- delete important project documentation without explicit permission
- modify secrets or environment files without explicit permission

Normal read, list, test, build, formatting, documentation, and local commit commands are allowed when they support the current task.
