# Instructions for future agents

## Scope and architecture

Respect the user-authorized phase. Phase 0 contains infrastructure only. Do not add scientific models, fake outputs, SPICE downloads, optimization, maps, authentication, databases, or cloud deployment without explicit authorization. Read architecture and science documents before changing contracts.

Dependency direction: web → HTTP API → lunar_core. Core must be independently installable, typed, and free of API/UI dependencies. Keep shared Python check configuration at the root and the sole npm lockfile at the root. Prefer minimal dependencies and direct implementations over speculative abstractions.

## Scientific honesty

Never fabricate datasets, simulation output, reference agreement, convergence, uncertainty, or validation. Distinguish planned behavior from implemented behavior. Health means process availability only. Geometric sunlight is not power; Earth line-of-sight is not reliable communication; site analysis is not landing-safety certification. Record units, frames, time scales, provenance, assumptions, numerical tolerances, and limitations when scientific work is eventually authorized. No NASA endorsement claims.

## Verification

Run `make check` for code changes and `git diff --check` for every change. Add meaningful behavior tests for new behavior, including failure paths where material. Core must remain independently testable. Report exact commands, results, and unavailable checks truthfully. Do not equate bootstrap tests with scientific validation or claim CI ran from local results.

## Git and data safety

Inspect `pwd`, `git status --short --branch`, `git log`, and existing files first. Preserve user changes; adapt to existing work. Never use destructive reset/clean, force push, or rebase. Do not stage, commit, push, merge, create remotes, or change remotes unless the user explicitly authorizes those actions in a later task. Never stage secrets, environment files, kernels, NASA datasets, caches, generated results, or virtual environments. Inspect the final diff and untracked files. Keep small text provenance manifests and explicitly reviewed small fixtures trackable. Report changed paths, checks, limitations, and a suggested conventional commit message at completion.

## Project-context navigation

At the start of each task, read this file, inspect the current Git status and branch, and review the [canonical roadmap](docs/development/roadmap.md), [implementation status](docs/project-context/IMPLEMENTATION_STATUS.md), relevant [scientific decisions](docs/project-context/SCIENTIFIC_DECISIONS.md), and applicable [ADRs](docs/adr/0001-monorepo-and-stack.md). Use the [project-context index](docs/project-context/README.md) for the overview, RC-01–RC-15 synthesis, architecture guide, workflow, open questions, evidence sources, and decision-status definitions. Supplied research summaries are not directly verified original sources; provisional recommendations are not accepted contracts. Update evidence/status documents with approved milestones and preserve the canonical policy ownership described in the index. A roadmap does not authorize implementation.
