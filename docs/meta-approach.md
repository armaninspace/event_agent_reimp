You are working in this repository to add a Codex-compatible “Claude-style surface” for governed engineering work: skills, hooks, rules, agent roles, documentation conventions, and a phase-based implementation loop.

Your goal is to implement the repository structure, instructions, and enforcement scaffolding needed so future Codex sessions can operate through this workflow.

Create or update the following surfaces:

* Root `AGENTS.md` as the durable project constitution.
* `.agents/skills/` for reusable procedural skills.
* `.codex/hooks.json` and `.codex/hooks/` for lifecycle hooks.
* `.codex/rules/` for command guardrails.
* `.codex/agents/` for specialist role definitions, if supported by the current Codex environment.
* `docs/` as the audit trail for installed software, engineering plans, backlog, demos, deliverables status, ADRs, and phase records.
* `scripts/` for validation, e2e, demo, and documentation checks.

Implement the following operating model.

Codex may install any software needed inside this container to complete implementation, testing, e2e validation, documentation generation, or demo recording. Whenever software is installed, update `docs/installed-software.md` with:

* tool/package name
* version, when available
* install command
* reason installed
* whether it is runtime, dev-only, test-only, or demo-only
* reproducibility or cleanup notes

Build the workflow around this phase loop:

For each phase, continue until blocked or out of phases:

1. Implement a detailed engineering and requirements document.
2. Include layers, modules, architecture, dependency/library usage, demo requirements, test requirements, risks, and acceptance criteria.
3. Based on that document, develop a detailed backlog.
4. Execute the backlog slice by slice until blocked or done.
5. Unit test and e2e test each slice.
6. If blocked, diagnose the blocker, replan, and attempt to get unblocked.
7. At the end of the phase, record a detailed demo showing what was done. For UI, dashboard, explorer, chart, report visualization, or other visual phases, this must include an illustrative video unless video tooling is blocked and the blocker is documented.
8. Write a deliverables-status document explaining what was completed in the context of the demo.
9. Commit the phase and apply a label or tag.
10. Re-evaluate the plan and replace it if replanning would improve success odds.

Create these initial documents and directories if missing:

```text
AGENTS.md
.codex/
  hooks.json
  hooks/
    pre_tool_use_policy.py
    stop_validation.py
    session_start_context.py
  rules/
    default.rules
  agents/
    planner.toml
    implementer.toml
    tester.toml
    reviewer.toml
.agents/
  skills/
    phase-delivery/
      SKILL.md
    install-and-note/
      SKILL.md
    backlog-slice/
      SKILL.md
    demo-and-status/
      SKILL.md
    replan-on-block/
      SKILL.md
docs/
  installed-software.md
  phases/
  backlog/
  demos/
  deliverables-status/
  adr/
scripts/
  validate.sh
  e2e.sh
  record-demo.sh
```

`AGENTS.md` should explain:

* this repository’s Codex operating protocol
* where skills live
* where hooks and rules live
* how phase delivery works
* how installed software must be documented
* how backlog slices are implemented and tested
* how blockers are handled
* how demos and deliverables-status docs are written
* how commits and labels/tags are handled
* that Codex must not push, merge, publish, or perform destructive actions without explicit permission

Create the following skills.

`phase-delivery/SKILL.md`:
Define the full phase lifecycle. It should instruct Codex to create:

* `docs/phases/<phase-id>-engineering-requirements.md`
* `docs/backlog/<phase-id>-backlog.md`
* `docs/demos/<phase-id>-demo.md`
* `docs/deliverables-status/<phase-id>-status.md`

Each phase engineering document must include:

* phase goal
* requirements
* non-goals
* assumptions
* affected layers
* affected modules
* dependency/library choices
* architecture notes
* data/API/config changes
* demo requirements
* test requirements
* security/sandbox considerations
* risks
* acceptance criteria
* rollback plan

Each backlog item must include:

* stable item ID
* title
* rationale
* affected files/modules
* implementation steps
* unit test expectations
* e2e test expectations
* demo relevance
* acceptance criteria
* status

`install-and-note/SKILL.md`:
Define how Codex installs software and records it under `docs/installed-software.md`.

`backlog-slice/SKILL.md`:
Define the slice loop:

1. Restate slice goal.
2. Inspect relevant files.
3. Implement the smallest coherent change.
4. Add or update tests.
5. Run targeted tests.
6. Run relevant e2e checks.
7. Update docs and backlog status.
8. Record evidence.

`demo-and-status/SKILL.md`:
Define phase-end demo and status reporting. The demo doc should include setup, commands, UI steps, expected behavior, observed behavior, screenshots/logs/transcripts when available, known gaps, and requirement mapping. For any UI, dashboard, explorer, chart, report visualization, or other visual phase, the demo doc must reference an illustrative video under `demos/` or document why video recording/generation was blocked. For non-UI phases, the demo doc must include either a generated walkthrough video or an explicit non-applicability rationale with command-output evidence. The status doc should include completed items, blocked/deferred items, files changed, dependencies installed, tests run, demo evidence, video path or video-blocker rationale, acceptance criteria status, risks, next phase, commit hash, and label/tag.

`replan-on-block/SKILL.md`:
Define blocker handling and replanning. Codex should identify the root cause, attempt a safe unblock path, mark the item blocked if unresolved, create a replan section, and continue with unblocked work where possible.

Create hooks scaffolding.

`.codex/hooks.json` should wire lifecycle hooks for:

* session/context loading, if supported
* pre-tool command policy checks
* stop/final validation

Use safe, portable scripts. If exact Codex hook schema support is uncertain in this environment, create a conservative `hooks.json` with comments avoided if JSON is required, and document assumptions in `docs/adr/0001-codex-surface.md`.

Create hook scripts:

* `.codex/hooks/pre_tool_use_policy.py`
* `.codex/hooks/stop_validation.py`
* `.codex/hooks/session_start_context.py`

These scripts should be defensive and non-destructive. They should validate obvious policy issues, check for required docs, and print actionable messages. They should not block normal development unless a serious issue is detected.

Create rules scaffolding.

`.codex/rules/default.rules` should include guardrails for:

* prompt before `git push`
* forbid or prompt before PR merge
* prompt before destructive `rm -rf`
* prompt before deleting important docs
* prompt before modifying secrets or env files
* allow normal read/list/test/build commands

If the exact rules syntax is uncertain, add a best-effort rules file and document the assumption in `docs/adr/0001-codex-surface.md`.

Create specialist agent role files under `.codex/agents/`:

* `planner.toml`: focuses on engineering docs, requirements, ADRs, and backlog decomposition.
* `implementer.toml`: focuses on small coherent implementation slices.
* `tester.toml`: focuses on unit, integration, and e2e testing.
* `reviewer.toml`: focuses on diff review, risk review, docs alignment, and acceptance criteria.

If this Codex environment does not support `.codex/agents`, still create the files as documented conventions and note that in the ADR.

Create scripts:

`scripts/validate.sh` should check for required directories, required phase docs where applicable, executable scripts, and basic repo health. It should run available project tests when detectable, but not invent commands that do not exist.

`scripts/e2e.sh` should run available e2e tests if the repo has them. If none exist, it should print a clear message and exit successfully or neutrally.

`scripts/record-demo.sh` should provide a repeatable demo-recording scaffold. If real video recording tools are unavailable, it should create or update a demo markdown template with an explicit video-blocker or non-applicability section.

Create `docs/adr/0001-codex-surface.md` explaining:

* why the surface is split across `AGENTS.md`, `.agents/skills`, `.codex/hooks`, `.codex/rules`, `.codex/agents`, `scripts`, and `docs`
* what is enforced vs documented convention
* assumptions about Codex support
* future improvements
* risks and mitigations

After creating the scaffolding:

1. Run formatting or validation commands that are already available.
2. Run `bash scripts/validate.sh`.
3. Fix issues found by validation.
4. Update `docs/deliverables-status/phase-000-codex-surface-status.md` with what was created, what was tested, known limitations, and recommended next steps.
5. Commit the changes with:

```bash
git add .
git commit -m "phase(000): add codex engineering surface"
```

Do not push. Do not merge. Do not publish. Do not delete existing user work. If committing is blocked, document the reason in the deliverables-status file and continue with all other possible work.

Proceed now using best effort. Do not stop to ask clarification unless the repository state makes safe progress impossible.
