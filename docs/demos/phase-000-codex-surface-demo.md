# Phase 000 Demo: Codex Engineering Surface

## Setup

Run from the repository root:

```sh
cd /code
```

## Commands

```sh
python3 .codex/hooks/session_start_context.py
python3 .codex/hooks/stop_validation.py
bash scripts/e2e.sh
bash scripts/validate.sh
```

## Expected Behavior

- Session context reports required workflow files as present.
- Stop validation reports required Codex surface files as present.
- E2E script reports that no e2e suite exists and exits successfully.
- Validation checks required directories, files, script executability, hook execution, and detectable tests.

## Observed Behavior

All commands completed successfully.

- `session_start_context.py` reported `AGENTS.md`, phase skills, and installed software log as present.
- `stop_validation.py` reported required Codex surface files as present.
- `scripts/e2e.sh` reported no e2e suite detected and exited successfully.
- `scripts/validate.sh` checked required files, directories, executable scripts, hook execution, and available test discovery.

## Evidence

Command transcript:

```text
Codex project context
- AGENTS.md: present
- phase skills: present
- installed software log: present
- protocol: use phase docs, backlog slices, validation, demo, and status records
Stop validation passed: required Codex surface files are present.
no e2e suite detected; nothing to run
ok: AGENTS.md
ok: .codex/hooks.json
ok: .codex/hooks/pre_tool_use_policy.py
ok: .codex/hooks/stop_validation.py
ok: .codex/hooks/session_start_context.py
ok: .codex/rules/default.rules
ok: .codex/agents/planner.toml
ok: .codex/agents/implementer.toml
ok: .codex/agents/tester.toml
ok: .codex/agents/reviewer.toml
ok: .agents/skills/phase-delivery/SKILL.md
ok: .agents/skills/install-and-note/SKILL.md
ok: .agents/skills/backlog-slice/SKILL.md
ok: .agents/skills/demo-and-status/SKILL.md
ok: .agents/skills/replan-on-block/SKILL.md
ok: docs/installed-software.md
ok: docs/phases
ok: docs/backlog
ok: docs/demos
ok: docs/deliverables-status
ok: docs/adr
ok: docs/adr/0001-codex-surface.md
ok: scripts/validate.sh
ok: scripts/e2e.sh
ok: scripts/record-demo.sh
ok executable: .codex/hooks/pre_tool_use_policy.py
ok executable: .codex/hooks/stop_validation.py
ok executable: .codex/hooks/session_start_context.py
ok executable: scripts/validate.sh
ok executable: scripts/e2e.sh
ok executable: scripts/record-demo.sh
ok: hook scripts execute
skip: no project test manifest detected
no e2e suite detected; nothing to run
validation passed
```

## Known Gaps

- This is a non-UI phase.
- No walkthrough video was generated because the deliverable is repository scaffolding and command-output evidence is the appropriate demo artifact.

## Requirement Mapping

- Constitution: `AGENTS.md`
- Skills: `.agents/skills/`
- Hooks and rules: `.codex/`
- Audit trail: `docs/`
- Validation helpers: `scripts/`
