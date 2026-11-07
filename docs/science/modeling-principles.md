# Modeling principles

A scoped geometric SPICE adapter is implemented but physical site analysis is not validated; see [ADR 0003](../adr/0003-spice-geometry.md). Phase 1 provides immutable input contracts and metadata only; see [ADR 0002](../adr/0002-scientific-contracts.md). Future work must define coordinate frames, lunar shape/datum, units, time scales, kernel coverage, terrain resolution, sampling, tolerances, and uncertainty before producing results.

Geometric sunlight describes whether a modeled solar direction or disk is obstructed under stated terrain and geometry assumptions. It is not electrical power. Power additionally depends on incidence, array geometry, efficiency, temperature, degradation, storage, operations, and other mission assumptions. Finite solar disk and partial occultation need explicit treatment.

Geometric Earth line-of-sight describes modeled visibility under stated terrain and observer assumptions. It is not reliable communication. A link also depends on antennas, pointing, frequency, link budgets, ground stations, Earth geometry, scheduling, and operational constraints. Earth-center and extended-Earth visibility must not be conflated.

Site suitability is conditional on selected metrics and mission constraints. It does not certify landing safety. Slopes, hazards, navigation, dynamics, uncertainty, and mission assurance require separate qualified analysis. This project must never present a candidate ranking as a safe landing authorization.

Report unavailable values explicitly. Preserve provenance and assumptions alongside future results; avoid false precision. NASA/NAIF data usage does not imply NASA endorsement.
