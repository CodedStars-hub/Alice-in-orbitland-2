# Development workflow

[AGENTS.md](../../AGENTS.md) and [CONTRIBUTING.md](../../CONTRIBUTING.md) own engineering rules. This guide records the collaboration checkpoints from B1/R1; see the [evidence register](README.md#evidence-register).

## Start each task

Read AGENTS.md; inspect `pwd`, `git status --short --branch`, recent commits, and relevant existing files. Read the [canonical roadmap](../development/roadmap.md), [implementation status](IMPLEMENTATION_STATUS.md), relevant [scientific decisions](SCIENTIFIC_DECISIONS.md), and ADRs. Confirm the user-authorized phase. Do not build on unexplained changes or infer feature authorization from a roadmap.

Keep main stable. Reuse a suitable existing branch safely; otherwise use a focused branch matching the task and user instruction. This documentation milestone uses `docs/project-research-context`. Future examples include `feat/scientific-contracts`, `fix/...`, `test/...`, and `refactor/...`. Do not create branches unnecessarily.

## Implementation and review

Keep changes coherent and minimal. Preserve core independence, shared root Python configuration, and the sole root npm lockfile. Document assumptions, units, frames, time scales, provenance, tolerances, unsupported inputs, and scientific limitations as relevant. Accepted major decisions belong in ADRs; provisional research stays labeled.

Add meaningful behavior/failure tests. Run `make check` for code changes and `git diff --check` for every change; documentation work also requires internal-link and terminology/status review. Review the final diff and untracked files for scope, secrets, data, caches, and generated artifacts. Inspect staged files if any already exist. Report exact commands, failures, and unavailable checks. Local success is not GitHub CI or scientific validation.

For each milestone, explicitly report readiness for review, changed paths and intended staging set, required checks and actual results, proposed conventional commit message, and whether commit/push/PR/merge are appropriate. Prefer small atomic commits; do not split a coherent change artificially.

## Authorization and data safety

Do not stage, commit, push, merge, rebase, change remotes, delete branches, or rewrite history without explicit task authorization. Never use destructive reset/clean to discard work. Approval to edit documentation is not approval to implement Phase 1 or publish changes.

For this milestone: review documentation first; do not commit or push now. After review, the user may authorize staging and an atomic commit, then a branch push and PR. Verify remote CI before recommending merge; local checks alone cannot establish merge readiness.

Never commit secrets, environment files, virtual environments, node_modules, downloaded kernels/terrain, caches, or generated scientific results. Small verified manifests and reviewed fixtures follow the [data policy](../../data/README.md). Dependency upgrades need compatibility/advisory assessment; historical advisory counts are not current audit results.
