# Scientific and architectural decision inventory

Evidence codes and status definitions are in the [index](README.md). R1 is supplied research, not verified original literature. No scientific decision is **Empirically validated**. Accepted policy does not imply implemented scientific behavior. Proposed changes require explicit review and, where appropriate, an ADR.

## D01 — Monorepo and stack

- **Status:** Accepted and implemented.
- **Selected/proposed approach:** Independent Python core, FastAPI, React/TypeScript/Vite; root check configuration and sole npm lockfile.
- **Reasoning and alternatives:** Keep contracts/review together and core reusable. ADR 0001 compares separate repositories, coupling, and extra workspace/container infrastructure.
- **Scientific assumptions:** No science assumptions established by stack choice.
- **Dependencies:** Python/Node toolchains and packaging.
- **Implementation consequences:** Preserve web → API → core and offline core use.
- **Validation requirements/evidence:** Local packaging, API/UI smoke checks pass; see implementation status.
- **Remaining risks:** Import isolation is not comprehensively enforced by current tests.
- **Source:** L1; ADR 0001.

## D02 — Coordinates and frames

- **Status:** Provisional research recommendation.
- **Selected/proposed approach:** East-positive longitude and planetocentric latitude; explicitly select compatible lunar frame realization.
- **Reasoning and alternatives:** Make conventions explicit; MOON_ME/MOON_PA require assessment. No documented final alternative selection.
- **Scientific assumptions:** Lunar geometry, not terrestrial WGS84; shape/reference surface unresolved.
- **Dependencies:** Authoritative frame/product definitions and Phase 1 contracts.
- **Implementation consequences:** Specify normalization/poles/units; reject unsupported transformations.
- **Validation requirements/evidence:** Boundary, invalid-input and compatible transformation checks.
- **Remaining risks:** Frame realization, normalization and numerical tolerances remain open.
- **Source:** R1.

## D03 — Observer height

- **Status:** Unresolved.
- **Selected/proposed approach:** No height/reference-surface convention selected.
- **Reasoning and alternatives:** Horizon depends on observer position; terrain elevation and instrument height must be distinguished. Alternatives not finalized.
- **Scientific assumptions:** Vertical direction/reference surface require specification.
- **Dependencies:** D02 and terrain metadata.
- **Implementation consequences:** Include height and its meaning in observer/provenance contracts.
- **Validation requirements/evidence:** Synthetic observer/surface cases and height sensitivity.
- **Remaining risks:** Ambiguous heights can contaminate all visibility results.
- **Source:** R1; L1 modeling principles.

## D04 — SPICE geometry and time

- **Status:** Accepted but not implemented.
- **Selected/proposed approach:** SPICE direction with validated UTC/ephemeris-time and leap-second/kernel handling; exact integration unresolved.
- **Reasoning and alternatives:** Reproducible ephemerides/frame transforms. Other approaches were not verified as historically rejected.
- **Scientific assumptions:** Aberration/light-time and apparent-direction conventions unresolved.
- **Dependencies:** Verified kernel roles, hashes, load order, coverage and frame contracts.
- **Implementation consequences:** Explicit offline coverage/error handling; no unsupported hand-built conversions.
- **Validation requirements/evidence:** Conversion tests and compatible Horizons consistency comparisons.
- **Remaining risks:** Kernel compatibility; Horizons may share ephemerides and is not independent physical validation.
- **Source:** R1; L1 roadmap/data policy.

## D05 — Terrain source

- **Status:** Accepted but not implemented.
- **Selected/proposed approach:** LOLA source family; no exact DEM/version selected.
- **Reasoning and alternatives:** South-polar elevation direction; PGDA/PDS ODE discovery and LROC comparison products are supplied recommendations.
- **Scientific assumptions:** Grid spacing is not accuracy; datum/coverage/error model unresolved.
- **Dependencies:** D02/D03 and verified product metadata.
- **Implementation consequences:** Checksum manifests, no-data handling and processing lineage.
- **Validation requirements/evidence:** Sampling, metadata compatibility, missing coverage and terrain uncertainty studies.
- **Remaining risks:** No actual product has been acquired or validated.
- **Source:** R1; L1 roadmap/data policy.

## D06 — Horizon function

- **Status:** Provisional research recommendation.
- **Selected/proposed approach:** Reusable H(azimuth), fine near terrain/coarser distant terrain.
- **Reasoning and alternatives:** Reuse obstruction across time; single/multiresolution alternatives require measurement.
- **Scientific assumptions:** Curvature, radial reach, interpolation and coverage explicit; about 0.5° is an unverified reported precedent, not a setting.
- **Dependencies:** Observer geometry and compatible terrain.
- **Implementation consequences:** Cache/provenance must include scientifically relevant settings.
- **Validation requirements/evidence:** Synthetic occluders, spatial convergence and coverage tests.
- **Remaining risks:** Distant terrain, narrow obstructions and interpolation can bias visibility.
- **Source:** R1.

## D07 — Solar disc

- **Status:** Provisional research recommendation.
- **Selected/proposed approach:** Separate center/any/full/fraction; assess analytic straight-horizon circular-disc model in research synthesis.
- **Reasoning and alternatives:** Finite extent matters near grazing; binary center visibility alone cannot represent fractional area.
- **Scientific assumptions:** Locally straight horizon approximation; apparent geometry convention unresolved.
- **Dependencies:** D04/D06 and angular radius.
- **Implementation consequences:** Name observables explicitly; do not label area fraction as usable power.
- **Validation requirements/evidence:** Contact/center cases and comparison with varying-horizon disc calculations.
- **Remaining risks:** Approximation may fail across complex terrain; no validation evidence.
- **Source:** R1.

## D08 — Earth observable

- **Status:** Unresolved.
- **Selected/proposed approach:** Geometric Earth visibility planned; center versus finite-disc definition not selected.
- **Reasoning and alternatives:** Different observables answer different questions; neither establishes a link.
- **Scientific assumptions:** Libration/observer/terrain required; no RF assumptions established.
- **Dependencies:** D04/D06.
- **Implementation consequences:** Explicit visibility definitions; separate unsupported communications claims.
- **Validation requirements/evidence:** Synthetic occultation and compatible geometry references.
- **Remaining risks:** Any visible disc need not imply ground-station availability.
- **Source:** R1; L1 modeling principles.

## D09 — Temporal events

- **Status:** Provisional research recommendation.
- **Selected/proposed approach:** Coarse sampling, adaptive refinement, root finding and interval analysis.
- **Reasoning and alternatives:** Reuse timelines for metrics/windows; fixed sampling alone risks missed events.
- **Scientific assumptions:** No completeness guarantee; continuity and event bounds need justification.
- **Dependencies:** Defined visibility functions and time contracts.
- **Implementation consequences:** Explicit interval endpoints, duration units and tolerances.
- **Validation requirements/evidence:** Short same-sign events, tangencies/discontinuities and temporal convergence.
- **Remaining risks:** Refinement cannot recover every unbracketed event without further bounds.
- **Source:** R1.

## D10 — Constraints and comparison

- **Status:** Accepted but not implemented.
- **Selected/proposed approach:** Hard constraints before preferences; missing/unsupported evidence undetermined.
- **Reasoning and alternatives:** Explainable suitability; weighted scores are not success probabilities. Pareto approach remains provisional.
- **Scientific assumptions:** Mission requirements and uncertainty semantics need formalization.
- **Dependencies:** Verified metrics and mission inputs.
- **Implementation consequences:** Keep reasons/statuses and evaluated scope alongside results.
- **Validation requirements/evidence:** Constraint truth tables, unsupported evidence and robustness cases.
- **Remaining risks:** Aggregation can hide scientific differences or false certainty.
- **Source:** R1; L1 missing-data principles.

## D11 — Site/date search

- **Status:** Provisional research recommendation.
- **Selected/proposed approach:** Cache site horizon/long timelines; interval window evaluation and hierarchical screening.
- **Reasoning and alternatives:** Reduce repeated work; exhaustive/refined approaches need measured tradeoffs.
- **Scientific assumptions:** Screening can miss narrow favorable sites; no global-optimum claim.
- **Dependencies:** Validated single-site analysis and D12.
- **Implementation consequences:** Record search domain/resolution; report best evaluated candidate.
- **Validation requirements/evidence:** Search resolution studies, conservative bounds and diversity evaluation.
- **Remaining risks:** Search completeness and performance/accuracy tradeoffs unresolved.
- **Source:** R1.

## D12 — Cache identity

- **Status:** Unresolved.
- **Selected/proposed approach:** Include relevant inputs, observer, dataset/kernel versions/hashes and algorithm/settings; schema unselected.
- **Reasoning and alternatives:** Avoid incompatible reuse; cache granularity alternatives not evaluated.
- **Scientific assumptions:** Horizon/time-series dependencies differ; timeline coverage matters.
- **Dependencies:** Provenance contracts and measured workloads.
- **Implementation consequences:** Version identity and invalidation explicitly.
- **Validation requirements/evidence:** Parameter/version changes must invalidate relevant artifacts.
- **Remaining risks:** Incomplete identity can silently reuse scientifically incompatible results.
- **Source:** R1.

## D13 — Mapping and workflows

- **Status:** Provisional research recommendation.
- **Selected/proposed approach:** 2D lunar south-polar map; OpenLayers with verified projection; three workflows.
- **Reasoning and alternatives:** Expose real results without requiring full 3D globe. Library alternatives not finalized.
- **Scientific assumptions:** Correct lunar projection/overlay conventions required.
- **Dependencies:** Scientific API, CRS review, attribution and genuine outputs.
- **Implementation consequences:** No fake overlays; synchronized timelines/events and visible uncertainty.
- **Validation requirements/evidence:** Coordinate/projection and UI result/status checks.
- **Remaining risks:** Library recommendation is not an installed or accepted final choice.
- **Source:** R1.

## D14 — Scientific provenance

- **Status:** Accepted but not implemented.
- **Selected/proposed approach:** Exact input IDs/hashes, kernels, frames/time, observer, algorithms/settings and science status.
- **Reasoning and alternatives:** Reproduction and auditability; existing policy is implemented as documentation, result recording is not.
- **Scientific assumptions:** No manifest field values may be invented.
- **Dependencies:** Verified assets and scientific contracts.
- **Implementation consequences:** Fail on mismatch; preserve derived lineage; JSON/CSV schemas remain provisional.
- **Validation requirements/evidence:** Reproduction, checksum failures, export round trips and version review.
- **Remaining risks:** PDS4/PROV are guiding concepts, not selected infrastructure.
- **Source:** R1; L1 data policy.

## D15 — Validation gates

- **Status:** Accepted but not implemented.
- **Selected/proposed approach:** Synthetic verification, convergence, compatible references and domain review.
- **Reasoning and alternatives:** Evidence must support scoped claims; bootstrap tests cannot validate physics.
- **Scientific assumptions:** Separate numerical/physical uncertainty and model limitations.
- **Dependencies:** Defined requirements/tolerances and appropriate reference assets.
- **Implementation consequences:** Record applicability and discrepancies; completion differs from validity/completeness.
- **Validation requirements/evidence:** Future benchmark hierarchy and independent review; none demonstrated.
- **Remaining risks:** Shared reference inputs limit independence; uncertainty ensembles need support.
- **Source:** R1; L1 validation strategy.

## D16 — Execution isolation

- **Status:** Provisional research recommendation.
- **Selected/proposed approach:** Isolated worker processes for expensive calculations.
- **Reasoning and alternatives:** Protect API responsiveness; topology must follow measurements.
- **Scientific assumptions:** No distributed scale or resource budget established.
- **Dependencies:** Bounded workload and failure contracts.
- **Implementation consequences:** Keep science independent from execution/transport; no worker implemented.
- **Validation requirements/evidence:** Resource, cancellation/failure and reproducibility checks.
- **Remaining risks:** Premature complexity or unbounded compute exposure.
- **Source:** R1.

## D17 — Operational infrastructure and optional 3D

- **Status:** Deferred.
- **Selected/proposed approach:** Distributed queues, databases, cloud hosting and optional local 3D postponed.
- **Reasoning and alternatives:** Single-site scientific evidence comes first; alternatives depend on workload/product need.
- **Scientific assumptions:** No operational certification or production readiness assumed.
- **Dependencies:** Explicit authorization and measurements.
- **Implementation consequences:** Do not install infrastructure or build globe during contracts work.
- **Validation requirements/evidence:** Scope-specific reliability/security/release review when authorized.
- **Remaining risks:** Roadmap presence must not be treated as implementation permission.
- **Source:** R1; L1 ADR/roadmap.
