# Implementation status

Snapshot: 2026-11-07. Implementation baseline: `c582d144ce5f31de79d55af3ff2e5faed765b9fe` (`chore: bootstrap lunar navigator monorepo`). This documentation milestone is on `docs/project-research-context`, not committed. Update this record when implementation or evidence changes; it is not a live CI badge.

## Evidence-backed state

Phase 0 is implemented. Phase 1 has not started. Core contains only package/version metadata and a typed marker. API provides `/api/v1/health` and explicit configurable CORS. Health returns process availability and `scientific_features: not_implemented`; it is not data/scientific readiness. Frontend is static and does not call the API. Packaging, root checks/locks, optional pre-commit hooks, and Linux GitHub Actions configuration exist.

No scientific contracts, SPICE integration/kernels, terrain, horizons, visibility, temporal simulation, mission evaluation, optimization, maps, worker service, database, authentication, exports, cloud deployment, or real scientific benchmark exists. The new context documents preserve plans rather than implementing these features.

## Existing test coverage

- Three API tests: health response, allowed/disallowed CORS response headers, wildcard rejection.
- One core test: installed distribution version matches package metadata.
- One integration smoke test: core/API co-install and health reports scientific features absent.
- One frontend test: project identity and scientific-limitations messaging.

These are bootstrap behavior tests, not scientific verification. The integration smoke test does not enforce all import boundaries. CORS tests exercise an environment-configured single origin, but lack explicit coverage of empty configurations, multiple/custom nondefault origins, malformed origins/ports, and preflight behavior. No coverage percentage was measured.

## Verification evidence

During onboarding on 2026-11-07, Python 3.12.15, Node 24.19.0 and npm 11.17.0 were observed. Existing dependencies were used without installing/upgrading them.

| Command/check | Observed result |
| --- | --- |
| `make check` | Passed: Ruff lint/format, ESLint, strict mypy (6 files), TypeScript, 5 Python tests, 1 Vitest test, frontend production build |
| `.venv/bin/python -B -m pytest -p no:cacheprovider packages/lunar_core/tests` | 1 passed, separately from API/integration suites; not a clean-environment install test |
| `.venv/bin/python -m pip check` | No broken requirements; pip cache-directory warning did not prevent completion |
| `npm ls --depth=0` | Expected direct dependencies resolved |
| Installed Python versions versus `requirements-dev.lock` | No mismatches |
| npm dependency/devDependency/engine sections versus root lock | No mismatches; lockfile version 3 |
| `git diff --check` | Passed on the clean onboarding baseline |

Python tests emitted a Starlette/AnyIO `BlockingPortal` deprecation warning. No scientific accuracy follows from these results. Checks may generate ignored build/cache artifacts.

During Prompt 00B, `git ls-remote origin refs/heads/main` confirmed remote main matched the baseline hash before branch creation. No fetch, commit, push, merge, rebase, or remote change was performed. Documentation verification is recorded below after execution.

## Documentation milestone verification

- A local Python Markdown check passed for all 10 changed/new documents: 51 relative links (including fragments), final newlines, and trailing whitespace; eight context documents and all 15 RC headings were confirmed.
- `git diff --check` passed. Tracked diff, all new document contents, untracked paths, and scope were reviewed; only documentation/AGENTS.md changed and the staged diff is empty.
- `git diff --stat` reports the two tracked modifications; the eight new untracked documents are additional and do not appear in that statistic until staged.
- No application checks were rerun for documentation-only changes. The software results above are explicitly the earlier onboarding baseline, not a new CI run. No scientific validation was performed.

## Limits and maintenance items

Live GitHub source/PR/Actions state was not inspected. CI is configured, not verified as passing. No fresh install, clean-environment core install, browser interaction test, vulnerability audit, or scientific reference run was performed. The README's historical 10 moderate advisory entries are not a current audit count. Python dependency pins are not artifact-hash locks. The MIT license retains a copyright-holder placeholder. These are review items, not evidence of scientific failure or production exposure.

Next implementation milestone: explicitly scoped Phase 1 contracts, after documentation review and separate authorization. See the [roadmap](../development/roadmap.md) and [open questions](OPEN_QUESTIONS.md).
