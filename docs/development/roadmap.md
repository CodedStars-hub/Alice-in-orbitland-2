# Development roadmap

This is the canonical roadmap. Phase 0 software is completed at bootstrap revision `c582d14`; Phase 1 input contracts are implemented on the feature branch, pending PR/CI review; no astronomical/terrain calculations exist. Later implementation requires explicit task authorization. Plans are not delivery, accuracy, or operational-readiness commitments.

## Phases and acceptance focus

| Phase | Milestone | Scope / acceptance focus | Status |
| --- | --- | --- | --- |
| 0 | Repository foundation | Independent packages, health API/CORS, honest placeholder, tests/tooling, CI configuration and policies | Completed software foundation; CI execution not verified |
| 1 | Scientific contracts | Units, frame/shape/time conventions, site/observer height, numerical policies, provenance and missing-data states; synthetic boundary/failure tests | Implemented contracts; pending PR/CI review |
| 2 | SPICE integration | Verified offline kernel manifests, coverage/error handling, frame/time conversions and compatible reference comparisons | Planned |
| 3 | Terrain ingestion | Select/verify LOLA product; datum/frame/no-data contracts, checksums, processing provenance, sampling and uncertainty studies | Planned |
| 4 | Horizon geometry | Observer-specific terrain horizon, coverage handling, synthetic cases and discretization/convergence assessment | Planned |
| 5 | Visibility geometry | Defined solar/Earth center/disc observables, finite-disc assumptions; distinguish power/link reliability | Planned |
| 6 | Temporal analysis | Event detection/refinement, interval algebra, durations, simultaneous visibility, tolerances and missed-event limitations | Planned |
| 7 | Scientific validation gate | Compatible references, convergence, reproducible single-site analysis bundle, domain review and applicability limits | Planned; validation accompanies phases 1–6 |
| 8 | Scientific API | Versioned contracts, explicit missing/unsupported/validity/completeness states, bounded execution and provenance delivery | Planned |
| 9 | Research UI and location-first analysis | Verified lunar map/projection, configuration, real results, synchronized timelines/events/horizon profiles, uncertainty; end-to-end single-site workflow | Planned |
| 10 | Mission evaluation and site/date optimization | Hard constraints before preferences, undetermined states, explainable/Pareto comparisons; horizon/timeline reuse and measured hierarchical search | Planned; mission evaluation precedes optimization |
| 11 | Reliability, exports, deployment and demonstration | Measured caching/background-job needs, JSON/CSV reproduction exports, resource budgets, security/observability, final scientific evidence review and scoped demonstration; hosting only when authorized | Planned; infrastructure deferred |

## Reconciliation of earlier numbering

The supplied onboarding brief used phases 0–14, while the repository's published bootstrap roadmap used 0–11. Preserve existing repository numbering rather than renumbering completed/published milestones. The supplied Prompt 00B research summary is recorded as R1 in the [context evidence register](../project-context/README.md#evidence-register).

| Earlier research phase | Canonical phase | Preservation |
| --- | --- | --- |
| 0–8: foundation through scientific API | 0–8 | Same broad sequence; Phase 1 remains contracts |
| 9: frontend and mapping | 9 | Research UI foundation |
| 10: location-first site analysis | 9 | Explicit integrated single-site workflow |
| 11: mission constraints/suitability | 10 | Explicit prerequisite submilestone before search |
| 12: multi-site/date optimization | 10 | Comparison/search after reliable mission evaluation |
| 13: reliability/cache/jobs/exports | 11 | Explicit reliability/reproduction submilestone |
| 14: final validation/deployment/demo | 7 and 11 | Initial scientific gate in 7; final scope-specific review/demo in 11 |

## Critical path and sequencing

Contracts precede SPICE and terrain; those branches can be developed independently once compatible observer/frame/time contracts exist. Terrain precedes horizon; horizon and celestial geometry combine into visibility; visibility definitions precede temporal metrics. Scientific verification and provenance accompany every step, rather than being postponed to Phase 7.

The first major scientific milestone is a reproducible single-site analysis with scoped evidence, before large-scale optimization. Phase 9 connects that evidence to an analyst workflow. Design resource limits and execution isolation before exposing costly scientific APIs; Phase 11 hardens measured needs rather than postponing basic bounds. Define provenance in Phase 1 and carry it through every artifact; exports in Phase 11 are not permission to defer reproducibility. Final validation repeats as necessary for the released scope.

See [implementation status](../project-context/IMPLEMENTATION_STATUS.md), [decision inventory](../project-context/SCIENTIFIC_DECISIONS.md), and [open questions](../project-context/OPEN_QUESTIONS.md). None of these milestones authorizes power simulation, RF guarantees, landing-safety certification, or NASA endorsement claims.
