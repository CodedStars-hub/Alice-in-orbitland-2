# ADR 0003: Reproducible DE440 geometric lunar directions

Status: accepted for authorized Phase 2 implementation, pending PR review; scoped software/reference evidence does not establish physical certification.

## Context and source basis

[ADR 0002](0002-scientific-contracts.md) supplied immutable symbolic inputs without frame or surface realization. Phase 2 authorizes SpiceyPy, verified local NAIF kernels and real Sun/Earth geometry. Source documents and exact assets are linked in [integration](../science/spice-integration.md), [frames](../science/lunar-reference-frames.md), [observer](../science/observer-geometry.md) and the [manifest](../../data/manifests/spice-de440.json). No new decision IDs replace D01–D17.

## Decision

Separate asset/session, time, frame, observer and target-result modules in core. Pin SpiceyPy 8.3.0 and its resolved NumPy dependency in the root lock. Contract-only imports remain independent of SPICE; installing core now includes the binding. Use an exclusive initially empty process pool, controlled cleanup and an owner thread/process guard; never clear an unrelated pool. Future parallel workloads require process isolation.

Use explicit MOON_ME_DE440_ME421 / MOON_PA_DE440 frame mapping, epoch-dependent orientation checks, a 1737.4 km reference sphere with declared radial reference-surface offsets, and reject unresolved terrain/normal/polar cases. Use geometric target centers (10, 399) relative to Moon 301 with correction NONE. Subtract observer position in the same epoch/frame. Apparent/disc corrections are deliberately deferred rather than mixed with these geometric vectors. UTC conversion is delegated to SPICE; the reviewed bundle scope is [2000-01-01, 2025-01-01) UTC.

Return typed serializable vectors, local angles/range, input identity, actual manifest, software versions/revision and separate status axes. Success/complete means execution/input completeness in this supported geometric scope; validity remains not assessed. No code automatically grants a scientific validation status.

## Alternatives and consequences

Generic aliases or IAU_MOON fallback could obscure kernel realization. Light-time/aberration corrections require careful surface-observer treatment and are deferred; choosing NONE is scientifically explicit but does not produce apparent sunlight. A full ellipsoid/DEM observer requires conventions/data not yet selected. Reusing arbitrary existing pools or allowing concurrent loads risks hidden state. Automatic runtime downloads would undermine offline reproducibility; acquisition is an explicit reviewed-manifest script outside core.

Large assets remain ignored; CI runs deterministic synthetic checks without downloads and skips opt-in integration tests unless a verified local bundle is explicitly supplied. Size/SHA checks establish byte identity, not source authenticity or physical accuracy. The current manifest is a reviewed demonstration bundle, not universal mission coverage. Version/platform/reference differences must be documented rather than silently increasing tolerances.

## Verification and deferred work

See [evidence](../validation/spice-geometry-validation.md) for actual commands, measured residuals, numerical checks and limits. Published NAIF frame-example comparison is source-related consistency evidence; Horizons comparison and independent physical uncertainty assessment remain deferred. No terrain, horizons, occultation, temporal events, optimization, database or deployment are introduced. [Research traceability](../project-context/RESEARCH_TRACEABILITY.md) maps stable decisions and future gaps.
