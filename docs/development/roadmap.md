# Development roadmap

Only Phase 0 is authorized and implemented here. Later phases require explicit scope approval and review; this sequence is a plan, not a delivery or accuracy commitment.

0. Repository foundation: packaging, health API, restrained placeholder, quality tooling, documentation, CI configuration.
1. Scientific contracts: units, frames, time scales, observer/site definitions, numerical policies, provenance, missing-data behavior, and synthetic test cases.
2. SPICE integration: verified kernel manifests, offline loading, coverage/error handling, frame/time conversions, reference comparisons.
3. Terrain ingestion: LOLA attribution, datum/frame contracts, checksum verification, preprocessing provenance and resolution studies.
4. Horizon geometry: synthetic cases, terrain-aware occlusion, discretization and convergence assessment.
5. Visibility geometry: sunlight definitions, finite-disk assumptions, Earth visibility definitions; keep power and link reliability separate.
6. Temporal analysis: sampling, event boundaries, durations, uncertainty and mission-window constraints.
7. Validation: independent comparisons, convergence evidence, reproducible bundles, domain review, documented applicability limits. Validation work also accompanies every earlier scientific phase.
8. Scientific API: versioned validated contracts, explicit unsupported/missing states, bounded workloads and provenance delivery.
9. Research UI: maps, configuration, results, comparisons, and visible limitations backed by actual API capabilities.
10. Mission-specific optimization: transparent objectives/constraints, sensitivity analysis, and no landing-safety certification.
11. Deployment: security, operational budgets, observability, data distribution, and hosting decisions based on measured requirements.
