# Installed Software

This document records software installed by Codex during project work.

## Phase 000

No new software was installed during `phase-000-codex-surface`.

Existing container tooling was used for scaffolding and validation:

| Tool/package | Version | Install command | Reason installed | Classification | Reproducibility or cleanup notes |
| --- | --- | --- | --- | --- | --- |
| bash | pre-existing | N/A | Run scaffold and validation scripts | dev-only | Provided by the container image |
| python3 | pre-existing | N/A | Run hook scaffolding scripts | dev-only | Provided by the container image |
| git | pre-existing | N/A | Local phase commit | dev-only | Provided by the container image |

## Phase 001

| Tool/package | Version | Install command | Reason installed | Classification | Reproducibility or cleanup notes |
| --- | --- | --- | --- | --- | --- |
| agent-framework | 1.9.0 | `python3 -m pip install agent-framework` | Microsoft Agent Framework runtime for Python agent phases | runtime | Installed in the agent user site-packages; reproduce through `pyproject.toml` dependency `agent-framework>=1.9.0,<2.0.0` |
