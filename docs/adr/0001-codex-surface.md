# ADR 0001: Codex Engineering Surface

## Status

Accepted

## Context

The repository needs a Codex-compatible surface for governed engineering work: skills, hooks, rules, specialist roles, documentation conventions, and a phase-based implementation loop.

## Decision

Split the surface across:

- `AGENTS.md` for durable repository-wide protocol.
- `.agents/skills/` for reusable procedural skills.
- `.codex/hooks.json` and `.codex/hooks/` for best-effort lifecycle scripts.
- `.codex/rules/` for command guardrail conventions.
- `.codex/agents/` for specialist role definitions.
- `scripts/` for repeatable validation, e2e, and demo helpers.
- `docs/` for installed software records, phase plans, backlog, demos, deliverables status, and ADRs.

## Enforced Versus Convention

Enforced locally:

- `scripts/validate.sh` checks required files and directories.
- Hook scripts are executable and can be run directly.
- Hook scripts return non-zero for obvious serious policy issues when invoked with matching command text.

Documented convention:

- Native loading of `.codex/hooks.json`.
- Native interpretation of `.codex/rules/default.rules`.
- Native use of `.codex/agents/*.toml` specialist roles.
- Phase labels or tags beyond local Git commits.

## Assumptions About Codex Support

The exact hook schema, rule syntax, and agent role support can vary by Codex environment. The files are intentionally conservative and comment-free where JSON requires it. If a future environment exposes a stricter schema, this scaffold should be adapted and this ADR amended.

## Future Improvements

- Replace best-effort rule syntax with the exact supported schema when available.
- Add project-specific test discovery once application code exists.
- Add automated phase artifact linting.
- Add real demo video capture when a UI or visual deliverable exists.
- Add optional tag creation after the user approves the tag naming policy.

## Risks And Mitigations

- Risk: Hook and rule files may not be loaded natively.
  Mitigation: Keep scripts directly runnable and document conventions in `AGENTS.md`.
- Risk: Validation is too generic before product code exists.
  Mitigation: Detect common manifests and add project-specific checks in future phases.
- Risk: Guardrails block ordinary work.
  Mitigation: Hook scripts only flag serious patterns and remain non-destructive.
