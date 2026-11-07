# Validation strategy

Status: scientifically unvalidated. Current tests verify packaging, HTTP behavior, CORS, frontend messaging, and Phase 1 contract invariants (coordinates, observer/time/configuration, serialization, provenance/status and typed failures). These are software verification, not physical model validation. No real simulation is authorized or executed in Phase 0.

Future scientific implementation must begin with explicit contracts and acceptance tolerances justified by requirements:

1. Synthetic tests: analytically tractable geometry and controlled terrain; test degenerate inputs, units, frames, time boundaries, missing coverage, and failure behavior. Synthetic fixtures must be clearly labeled and never presented as observed lunar data.
2. Convergence tests: vary spatial resolution, horizon discretization, time step, and relevant numerical settings. Quantify sensitivity and event-boundary uncertainty; do not assume finer sampling guarantees correctness.
3. Reference comparisons: compare independently derived calculations or authoritative published reference cases with compatible frames, time scales, terrain, kernels, and definitions. Record differences, tolerances, and unresolved discrepancies. Agreement alone does not prove validity.
4. Provenance: retain input checksums, source/version, kernel load order, software versions, configuration, assumptions, and reproducible execution instructions. Distinguish code verification, model validation, and mission applicability.
5. Review: require domain review before scientific accuracy claims. Publish scope-specific evidence and known limitations; no universal validation badge or landing-safety claim.

Offline reference runs must fail on missing/mismatched inputs rather than silently replacing them. Large data and results stay outside Git. CI should use small deterministic tests; future data-dependent checks need explicit assets and a separately documented workflow. No reference agreement or convergence results exist today.

Phase 2 now adds synthetic SPICE-boundary/local-geometry checks and opt-in verified-kernel integration. The [SPICE evidence report](spice-geometry-validation.md) records limited published NAIF Moon-center reference consistency and measured numerical checks separately from physical uncertainty and deferred independent comparisons. No global scientific-validity claim follows.
