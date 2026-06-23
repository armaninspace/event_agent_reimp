# Phase 000: Codex Engineering Surface

## Phase Goal

Create the repository structure, instructions, validation scaffolding, and audit trail needed for future Codex sessions to operate through a governed phase-based workflow.

## Requirements

- Add root `AGENTS.md` as the durable project constitution.
- Add reusable skills under `.agents/skills/`.
- Add lifecycle hook scaffolding under `.codex/hooks.json` and `.codex/hooks/`.
- Add command guardrail conventions under `.codex/rules/`.
- Add specialist role definitions under `.codex/agents/`.
- Add audit directories under `docs/`.
- Add validation, e2e, and demo scripts under `scripts/`.
- Document assumptions and limitations in an ADR.
- Validate the scaffold with `bash scripts/validate.sh`.
- Commit the phase locally if not blocked.

## Non-Goals

- Implement a product feature.
- Push, merge, publish, or perform remote operations.
- Depend on undocumented native Codex hook or rules behavior.
- Install new software unless validation requires it.

## Assumptions

- Codex may read `.agents/skills/` as a local convention in future sessions.
- `.codex/hooks.json`, `.codex/rules/`, and `.codex/agents/` may not be natively supported in every Codex environment.
- Shell, Python, and Git are available in this container.

## Affected Layers

- Repository governance
- Agent workflow documentation
- Local validation tooling
- Audit documentation

## Affected Modules

- `AGENTS.md`
- `.agents/skills/`
- `.codex/`
- `docs/`
- `scripts/`

## Dependency/Library Choices

No new dependencies are required. Hook scripts use the Python standard library. Validation scripts use POSIX shell plus common command-line tools.

## Architecture Notes

The surface is split between durable human-readable instructions, reusable skills, executable best-effort hooks, best-effort rules, role metadata, and audit documents. Enforcement is intentionally conservative because native support for some Codex surfaces is environment-dependent.

## Data/API/Config Changes

- Adds `.codex/hooks.json` as hook configuration.
- Adds `.codex/rules/default.rules` as documented command policy.
- Adds `.codex/agents/*.toml` role metadata.
- Adds documentation directories and phase artifacts.

## Demo Requirements

Demonstrate the scaffold by running validation and recording command output in `docs/demos/phase-000-codex-surface-demo.md`. This is a non-UI phase, so video is not applicable unless a walkthrough video is explicitly generated.

## Test Requirements

- Run `bash scripts/validate.sh`.
- Run `bash scripts/e2e.sh` or document that no e2e suite exists.
- Verify hook scripts execute with Python.

## Security/Sandbox Considerations

Guardrails must prompt before pushes, merges, publishing, broad destructive deletes, deleting important docs, or modifying secrets. Hook scripts must be non-destructive and avoid blocking ordinary development.

## Risks

- Native Codex support for hooks, rules, and role files may differ from this best-effort schema.
- Guardrails are advisory unless the active Codex environment loads them.
- Validation can only detect generic repository health until project-specific tests exist.

## Acceptance Criteria

- Required files and directories exist.
- Skills document the requested workflows.
- Hooks are defensive and executable.
- Rules include the requested guardrails.
- ADR documents enforcement assumptions.
- Validation passes.
- Deliverables status records created assets, tests, limitations, and next steps.
- Phase is committed locally or the blocker is documented.

## Rollback Plan

Revert the local phase commit, or remove the added `.agents/`, `.codex/`, `scripts/`, and phase-specific documentation files if the scaffold needs to be replaced.
