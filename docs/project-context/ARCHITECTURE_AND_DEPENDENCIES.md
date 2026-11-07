# Architecture and dependencies

The [architecture overview](../architecture/overview.md) and [ADR 0001](../adr/0001-monorepo-and-stack.md) are canonical. Evidence: L1 for existing components; R1 for proposed scientific responsibilities, as defined in the [evidence register](README.md#evidence-register).

## Actual Phase 0 structure

| Component | Existing responsibility | Boundary |
| --- | --- | --- |
| `packages/lunar_core` | Version metadata and typed installable package | No runtime dependencies; no scientific models; no API/UI imports |
| `apps/api` | FastAPI factory, health response, configurable explicit CORS | Declares core dependency; owns HTTP/environment concerns |
| `apps/web` | React/TypeScript/Vite static placeholder | No API calls or maps yet |
| `tests/integration` | Installed core/API smoke test | Does not comprehensively enforce import direction |
| `data/manifests` | Data-policy placeholder | No acquired inputs or scientific manifests |
| Root tooling | Make, Python check configuration/lock, npm workspace/lock, CI and optional hooks | One Python development environment and sole root npm lockfile |

Dependency direction is web → HTTP API → lunar_core. The API does not yet invoke scientific core behavior. Core must remain independently usable offline. Python 3.12 and Node 24.19.0/npm 11.x are the documented toolchains; see the root [README](../../README.md) for installation and reproducibility limits.

## Proposed scientific data flow

NASA LOLA terrain → observer-specific horizon → SPICE Sun/Earth geometry combined with that horizon → geometric visibility → temporal event detection/intervals → mission metrics → constraints → candidate comparison/optimization.

This is a dependency sketch, not a strict execution order: ephemeris geometry does not depend on terrain, and can be developed separately after shared contracts. Horizon and ephemeris outputs must agree on observer, frames, units, and time conventions before combination.

Planned core responsibilities are coordinate/time contracts, SPICE adapters, terrain sampling, horizon construction, visibility definitions, temporal analysis, constraints, and comparisons. These are not scaffolded implementations. Acquisition records and derived-data processing must follow the [data policy](../../data/README.md); scientific acceptance follows the [validation strategy](../validation/strategy.md).

## Execution, reuse, and future interfaces

R1 recommends isolated worker processes for expensive calculations. The API should eventually submit bounded work and expose explicit failures and provenance, rather than run unbounded scientific jobs in interactive requests. Worker topology and job lifecycle remain unimplemented.

A proposed reuse strategy computes a site's horizon and longer visibility timeline, then evaluates many mission windows through interval operations. Cache identity must include all scientifically relevant observer/input parameters, dataset versions/hashes, kernel set/load conventions, algorithm versions, and numerical settings. Time coverage matters for timelines. No cache schema has been selected.

Frontend mapping provisionally favors OpenLayers with a verified lunar south-polar projection; no mapping dependency is installed. JSON manifests and CSV exports are recommended, but schemas are unresolved. Execution state, scientific validity, and completeness must be distinct in future result/API contracts.

Distributed queues, databases, and cloud deployment remain deferred until authorized and justified by measured workloads. Do not introduce them merely because the planned pipeline is computationally expensive.
