# Project overview

Evidence: [R1 and B1](README.md#evidence-register) describe intent; [L1](README.md#evidence-register) establishes the Phase 0 implementation. Detailed challenge wording and historical selection rationale have not been recovered.

Lunar Navigator is a lunar south-polar mission-window decision-support system developed in the NASA Space Apps Challenge context for the Lunar Landing Site Navigator challenge. It asks how a candidate location performs during a particular mission window under stated requirements. Intended users include researchers and mission planners; educators and public audiences can also benefit from explainable geometry.

The motivation is to make coupled terrain, Sun/Earth geometry, time, and mission constraints understandable and comparable. The supplied research favors mission-aware analysis over a generic map or unsupported automated recommendation. No comparative evaluation of existing tools has been independently verified here.

## Proposed workflows

1. **Explore the Moon:** select a site on an accurate south-polar map and inspect real scientific overlays, horizon profiles, timelines, events, uncertainties, and sources.
2. **Mission Planner:** specify duration, candidate dates, hard constraints, and preferences; distinguish unsupported requirements from evaluated results.
3. **Compare and Explain:** compare sites/windows, explain tradeoffs and constraint outcomes, and expose provenance rather than hiding all differences in a score.

## Scientific MVP and longer-term direction

The first scientific MVP is a real, reproducible single-site analysis: verified inputs and observer conventions; a terrain horizon; SPICE-derived Sun/Earth geometry; explicitly defined geometric visibility; temporal intervals and mission metrics; and a reproducibility record. It requires scoped scientific verification before accuracy claims. It is not implemented.

Multi-site/date exploration, mission evaluation, Pareto comparisons, exports, bounded background execution, caching, and integrated analyst workflows follow this foundation. Local 3D is optional; a complete lunar globe is not essential. Follow the [canonical roadmap](../development/roadmap.md), not an inferred delivery promise.

## Boundaries

Geometric sunlight is not usable electrical power. Direct-Earth geometric visibility is not link availability or reliable communication. Site suitability is neither landing-safety certification nor a probability of mission success. Missing evidence must not become a silent pass/fail. Execution completion must remain separate from scientific validity and completeness. No NASA endorsement or operational certification is claimed.

Phase 0 software and Phase 1 immutable scientific contracts exist: packaging, health/CORS API, static frontend, contracts, tests, and tooling. Scientific analysis remains unimplemented. See [implementation status](IMPLEMENTATION_STATUS.md); [modeling principles](../science/modeling-principles.md) owns the scientific limitations.
