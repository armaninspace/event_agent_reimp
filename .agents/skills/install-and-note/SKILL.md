# Install And Note

Use this skill whenever Codex installs software in the container.

## Policy

Software may be installed when needed for implementation, testing, e2e validation, documentation generation, or demo recording. Prefer project-local, reproducible installs when practical. Avoid global installs unless they are required by the environment or task.

## Required Documentation

After every install, update `docs/installed-software.md` with:

- tool/package name
- version, when available
- install command
- reason installed
- classification: runtime, dev-only, test-only, or demo-only
- reproducibility or cleanup notes

## Evidence

When practical, record the command used to verify the installed version. If a version cannot be determined, state that explicitly.

## Cleanup

If software is temporary, document cleanup steps. Do not remove user-installed software unless explicitly asked.
