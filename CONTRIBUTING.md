# Contributing

Start with the README, AGENTS.md, architecture, and modeling principles. Discuss scope before introducing dependencies or scientific contracts. Use branches such as `feat/short-description`, `fix/short-description`, or `docs/short-description`. Use conventional commits, for example `chore: bootstrap monorepo foundation`.

Run `make install`, then `make check` and `git diff --check`. Optional local hooks: `.venv/bin/python -m pre_commit install`. Run core tests alone with `.venv/bin/python -m pytest packages/lunar_core/tests`. Hooks supplement review and CI; they do not establish scientific validity.

PR checklist:

- Explain the problem, resulting behavior, and scope.
- Include meaningful tests and exact verification results; identify checks not run.
- Preserve dependency direction and update documentation with behavior changes.
- Include no secrets, large data, generated artifacts, or nested npm lockfiles.
- State scientific assumptions, provenance, units, and validation limits for future scientific changes.
- Confirm no unsupported NASA endorsement or landing-safety claims.

Reviewers should inspect contracts, failure paths, dependency/lock changes, reproducibility, and scientific honesty. Scientific implementation requires domain review and the validation plan before any claim of verified accuracy. A passing CI run alone is insufficient. Follow SECURITY.md for sensitive reports.
