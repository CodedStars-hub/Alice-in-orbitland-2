# Lunar Navigator

A NASA Space Apps Challenge project exploring lunar south-pole site and mission-window analysis. The long-term aim is terrain-aware geometric sunlight, geometric Earth visibility, mission constraints, and candidate comparisons using NAIF SPICE and NASA LOLA terrain data.

**Phase 1 contracts implemented, pending PR review:** immutable coordinate, observer, UTC, configuration, provenance and status contracts now accompany the Phase 0 packages, health API, React development placeholder, tests, tooling, and documentation. No astronomical/terrain calculations, datasets, optimization, map UI, authentication, database, or deployment exist. This is a decision-support research tool, not a landing-safety certification system. No NASA endorsement or scientific verification is claimed.

## Architecture

- `apps/web`: React + TypeScript + Vite; future HTTP client of the API.
- `apps/api`: FastAPI HTTP boundary, depending on `lunar_core`.
- `packages/lunar_core`: standalone scientific package with immutable input contracts, no runtime dependencies or physical models; never imports the API or frontend.
- `tests/integration`: installed-component smoke tests.
- `data/manifests`: future small, reviewable provenance records; no downloaded data.

See [architecture](docs/architecture/overview.md), [decision record](docs/adr/0001-monorepo-and-stack.md), [modeling principles](docs/science/modeling-principles.md), and [validation strategy](docs/validation/strategy.md).

## Prerequisites and quick start

Use Python 3.12 (`.python-version`), Node 24.19.0 (`.nvmrc`), npm 11.x, Git, and Make. The default system Python may differ; commands deliberately use `python3.12`. No AWS account, scientific data, or secrets are required. POSIX shell instructions:

```sh
nvm use                    # if using nvm
make install
make check
make api                   # terminal 1: http://127.0.0.1:8000
make web                   # terminal 2: http://127.0.0.1:5173
curl http://127.0.0.1:8000/api/v1/health
```

Health returns `{"status":"ok","scientific_features":"not_implemented"}`. It does not certify scientific readiness or data availability. The frontend is a static development placeholder and does not call the API yet.

## Development

| Command | Purpose |
| --- | --- |
| `make install` | Create `.venv`, install locked tools and editable Python packages, run `npm ci` |
| `make lint` | Ruff lint/format checks and ESLint |
| `make typecheck` | Strict mypy and TypeScript checks |
| `make test` | Python tests and Vitest smoke test |
| `make build` | Type-check and build the frontend |
| `make check` | All quality checks above |
| `.venv/bin/python -m pytest packages/lunar_core/tests` | Independently test installed core |
| `.venv/bin/python -m pre_commit install` | Enable hygiene and project checks on commits |

Python uses one root development environment, centralized check configuration, and two independent src-layout distributions. Core can be installed alone with `python3.12 -m pip install ./packages/lunar_core`. The API's declared core dependency is satisfied by the editable local installation. No runtime dependency points back toward the API.

`requirements-dev.lock` pins the resolved Python development/runtime graph; editable projects are installed separately with the pinned build backend. To update intentionally, use a fresh Python 3.12 environment, install the desired direct versions and `setuptools==80.9.0`, freeze the resolved third-party packages to the lock, then run all checks. Review transitive changes. The lock is version-pinned, not an artifact hash lock; wheels and platform-specific resolution can vary. CI provides a Linux check of the same commands.

npm uses **one root `package-lock.json`** for the workspace. Run `npm install` from the root for intentional updates; use `npm ci` for reproduction. Do not create nested lockfiles. At bootstrap verification, npm reported 10 moderate advisory entries through minimatch in the ESLint/typescript-eslint development dependency graph. High/critical findings in the initial Vite/Vitest versions were resolved by updates. The remaining advisory must be reviewed during toolchain updates; the current quality checks pass, but do not establish absence of dependency vulnerabilities. TypeScript/ESLint, single quotes and semicolons in TS, two-space indentation, and EditorConfig define frontend conventions; Ruff formats Python.

CORS defaults to the two explicit Vite localhost origins. Override with comma-separated `LUNAR_CORS_ORIGINS` (explicit HTTP(S) origins without trailing slash), or an empty value to disable browser cross-origin access. Credentials are disabled. Server-to-server requests do not rely on CORS. Development servers bind to loopback.

Contract API: `lunar_core.contracts` and `lunar_core.errors`. Start with [ADR 0002](docs/adr/0002-scientific-contracts.md), [coordinate contracts](docs/science/coordinate-contracts.md), [time contracts](docs/science/time-contracts.md), [configuration](docs/science/scientific-configuration.md), and [provenance](docs/science/provenance-contracts.md).

Read [data safety](data/README.md), [contributing](CONTRIBUTING.md), [security](SECURITY.md), and the [roadmap](docs/development/roadmap.md). CI is configured; a local pass does not establish a GitHub Actions run or scientific validation.
