# ADR 0001: Monorepo and initial stack

Status: accepted for Phase 0.

## Context

A small research project needs reproducible developer workflows and reviewable boundaries before scientific implementation. Python will support scientific tooling; a browser interface will eventually communicate through a versioned API. No simulation or operational infrastructure is authorized now.

## Decision

Use Python 3.12, standalone `lunar_core`, FastAPI, React/TypeScript/Vite, npm workspaces, pytest/Ruff/mypy, ESLint/Vitest, and GitHub Actions. Use one root virtual environment and version-pinned Python dependency lock, with editable local distributions. Use one root npm lockfile. Keep scientific core independent of transport. Centralize checks with Make; CI runs the same commands.

## Alternatives

Separate repositories add release coordination before stable contracts exist. A single coupled Python application prevents independent core use. A Python workspace manager could offer richer locking but adds another bootstrap tool. Containers, distributed workers, databases, and deployment systems introduce operational work without current requirements. These are deferred, not ruled out permanently.

## Consequences

Cross-component changes are reviewable together and core remains reusable. Developers need both toolchains and Make. Python lock regeneration requires deliberate dependency review; version pins do not guarantee identical artifacts across platforms. CI checks Linux with Python 3.12 and Node 24. Future support expansion needs explicit matrix and lock validation. No claim of scientific validity follows from this stack choice.
