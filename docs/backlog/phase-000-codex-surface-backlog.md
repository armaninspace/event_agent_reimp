# Phase 000 Backlog: Codex Engineering Surface

## P000-001: Create Project Constitution

- Stable item ID: `P000-001`
- Title: Create root `AGENTS.md`
- Rationale: Future Codex sessions need durable operating instructions.
- Affected files/modules: `AGENTS.md`
- Implementation steps: Define protocol, surfaces, phase delivery, installed software logging, slice loop, blockers, demos/status, commits, and safety rules.
- Unit test expectations: Not applicable for documentation.
- E2E test expectations: `bash scripts/validate.sh` checks the file exists.
- Demo relevance: Validation output demonstrates presence.
- Acceptance criteria: `AGENTS.md` contains requested protocol sections.
- Status: done

## P000-002: Create Skills

- Stable item ID: `P000-002`
- Title: Add reusable workflow skills
- Rationale: Codex needs procedural instructions for repeatable phase work.
- Affected files/modules: `.agents/skills/*/SKILL.md`
- Implementation steps: Add `phase-delivery`, `install-and-note`, `backlog-slice`, `demo-and-status`, and `replan-on-block`.
- Unit test expectations: Not applicable for documentation.
- E2E test expectations: `bash scripts/validate.sh` checks required skill files exist.
- Demo relevance: Validation output demonstrates presence.
- Acceptance criteria: Each requested skill exists and includes required workflow details.
- Status: done

## P000-003: Create Codex Hook, Rule, And Agent Scaffolding

- Stable item ID: `P000-003`
- Title: Add `.codex` lifecycle and role conventions
- Rationale: The repo needs best-effort enforcement and specialist role documentation.
- Affected files/modules: `.codex/hooks.json`, `.codex/hooks/`, `.codex/rules/default.rules`, `.codex/agents/`
- Implementation steps: Add conservative JSON hook config, non-destructive Python hooks, guardrail rules, and TOML role files.
- Unit test expectations: Hook scripts execute with `python3`.
- E2E test expectations: `bash scripts/validate.sh` checks required files and executability.
- Demo relevance: Validation and hook command output demonstrate behavior.
- Acceptance criteria: Required `.codex` files exist and assumptions are documented.
- Status: done

## P000-004: Create Audit Docs And ADR

- Stable item ID: `P000-004`
- Title: Add phase, backlog, demo, status, installed software, and ADR docs
- Rationale: Future phases need an audit trail.
- Affected files/modules: `docs/installed-software.md`, `docs/phases/`, `docs/backlog/`, `docs/demos/`, `docs/deliverables-status/`, `docs/adr/`
- Implementation steps: Create required directories, phase documents, and ADR.
- Unit test expectations: Not applicable for documentation.
- E2E test expectations: `bash scripts/validate.sh` checks required docs.
- Demo relevance: Demo and status documents are phase deliverables.
- Acceptance criteria: Docs exist and explain completed work, assumptions, and limitations.
- Status: done

## P000-005: Create Validation And Demo Scripts

- Stable item ID: `P000-005`
- Title: Add script scaffolding
- Rationale: Future sessions need repeatable validation, e2e, and demo commands.
- Affected files/modules: `scripts/validate.sh`, `scripts/e2e.sh`, `scripts/record-demo.sh`
- Implementation steps: Implement defensive scripts that infer available tests without inventing commands.
- Unit test expectations: Script shell syntax passes via execution.
- E2E test expectations: `bash scripts/e2e.sh` exits neutrally when no e2e suite exists.
- Demo relevance: Scripts produce evidence for demo docs.
- Acceptance criteria: Scripts are executable and validation passes.
- Status: done

## P000-006: Validate And Commit

- Stable item ID: `P000-006`
- Title: Run validation and create local commit
- Rationale: The phase should end with evidence and a local checkpoint.
- Affected files/modules: repository state
- Implementation steps: Run available validation commands, fix issues, update status, `git add .`, and commit.
- Unit test expectations: Hook scripts and shell scripts run.
- E2E test expectations: `bash scripts/e2e.sh` runs.
- Demo relevance: Command output is recorded in the demo document.
- Acceptance criteria: Validation passes and local commit exists, or blocker is documented.
- Status: done
