# Research synthesis: RC-01–RC-15

All research statements below derive from supplied summaries [R1/B1](README.md#evidence-register), not direct inspection of the historical conversation or independently verified publications. Repository alignment is checked against L1. Status definitions are in the [index](README.md#evidence-classification); detailed decision records are in the [ledger](SCIENTIFIC_DECISIONS.md). No real scientific benchmark is demonstrated.

## RC-01 — Mission requirements and existing systems

- **Question:** How can users compare sites and mission dates meaningfully?
- **Supplied findings:** R1/B1 favor mission-aware comparison and explainable tradeoffs; no historical existing-tool evaluation was recovered.
- **Decisions/status:** Provisional research recommendation: three integrated workflows; certification claims are excluded by accepted modeling policy.
- **Technical implications:** Define a bounded single-site use case before optimization.
- **Limitations and remaining validation:** Detailed challenge requirements, original selection rationale, and comparative tool evidence still need recovery.

## RC-02 — Lunar geodesy and coordinate systems

- **Question:** Which coordinate and observer conventions make results reproducible?
- **Supplied findings:** MOON_ME and MOON_PA require explicit selection and compatible transformations; terrestrial WGS84 is not a lunar substitute.
- **Decisions/status:** Provisional research recommendation: east-positive longitude and planetocentric latitude. Exact frame realization, normalization, reference surface, and height remain Unresolved.
- **Technical implications:** Contracts must identify frame, units, shape, and height semantics; do not implement unsupported transformations.
- **Limitations and remaining validation:** Verify authoritative conventions and boundary cases, poles, normalization, and permitted transformations.

## RC-03 — SPICE ephemerides and celestial positioning

- **Question:** How should Sun/Earth geometry and time conversion be obtained?
- **Supplied findings:** R1 distinguishes UTC from SPICE ephemeris time and calls for validated SPICE leap-second/kernel mechanisms.
- **Decisions/status:** Accepted but not implemented: SPICE integration direction in the roadmap; exact toolkit dependency, kernels, and correction policies remain Unresolved.
- **Technical implications:** Kernel roles, versions, hashes, load order, coverage, and failures must be explicit. Ephemerides do not model terrain.
- **Limitations and remaining validation:** Check conversions, coverage, frames, observer geometry, and compatible Horizons comparisons; shared ephemerides limit independence.

## RC-04 — Lunar terrain and elevation datasets

- **Question:** Which terrain supports defensible south-polar horizons?
- **Supplied findings:** LOLA is the intended primary source; PGDA/PDS ODE are discovery directions and LROC imagery/stereo may support selected comparisons.
- **Decisions/status:** Accepted but not implemented: LOLA source direction. Exact DEM/version/coverage/datum/error model are Unresolved.
- **Technical implications:** Preserve metadata and checksums; distinguish grid spacing from vertical accuracy; reject or explicitly represent incomplete coverage. Missing terrain or other required scientific inputs must never imply an unobstructed horizon or favorable visibility.
- **Limitations and remaining validation:** Review actual product metadata and sampling/uncertainty behavior; no product identifier is asserted here.

## RC-05 — Terrain horizon and obstruction modeling

- **Question:** How can terrain obstruction be reused across time?
- **Supplied findings:** R1 proposes H(azimuth), multiresolution near/far terrain, and explicit observer geometry. It reports literature precedents of about 0.5° azimuth sampling without a verified citation.
- **Decisions/status:** Provisional research recommendation: reusable multiresolution horizon; 0.5° is not a selected or optimal setting.
- **Technical implications:** Include height, curvature, radial reach, interpolation, coverage, and numerical settings in provenance and reuse identity.
- **Limitations and remaining validation:** Synthetic geometry, discontinuities/seams, spatial convergence, and terrain-coverage uncertainty are required.

## RC-06 — Solar illumination modeling

- **Question:** Which portion of the solar disc is geometrically visible?
- **Supplied findings:** Finite angular extent matters near grazing conditions. Center, any-disc, full-disc, and fractional visibility are different observables.
- **Decisions/status:** Provisional research recommendation: analytic circular-disc/straight-horizon approximation below. No algorithm is validated or implemented.
- **Technical implications:** Use a declared apparent-direction convention and domain of applicability; report geometry separately from power.
- **Limitations and remaining validation:** Test contact/central cases, varying horizons across the disc, angular radius, and numerical stability.

## RC-07 — Earth visibility and communication geometry

- **Question:** What geometric Earth observable should be reported?
- **Supplied findings:** Observer geometry, libration, and terrain matter; center and finite-disc visibility differ.
- **Decisions/status:** Accepted but not implemented: geometric visibility direction; exact center/disc observable is Unresolved.
- **Technical implications:** Keep results distinct from station availability, link budgets, RF performance, and reliable communication.
- **Limitations and remaining validation:** Synthetic disc/terrain obstruction and compatible geometry comparisons are needed.

## RC-08 — Temporal simulation and event detection

- **Question:** How should visibility intervals and duration metrics be derived?
- **Supplied findings:** R1 proposes coarse sampling, adaptive refinement, root finding, and interval analysis. Same-sign short events, grazing, and horizon discontinuities can defeat simple transition detection.
- **Decisions/status:** Provisional research recommendation: adaptive event pipeline, with no general completeness guarantee.
- **Technical implications:** Report total sunlight, longest continuous darkness, longest geometric Earth obstruction, and simultaneous visibility under explicit definitions.
- **Limitations and remaining validation:** Adversarial short/tangent events, interval boundaries, temporal convergence, and justified missed-event bounds/tolerances.

## RC-09 — Scientific verification and uncertainty

- **Question:** What evidence supports each scientific claim?
- **Supplied findings:** Synthetic geometry, coordinate/time checks, Horizons consistency, compatible PGDA products, suitable LROC shadows, convergence, and supported terrain ensembles were recommended.
- **Decisions/status:** Accepted but not implemented: scientific validation gates; no scientific benchmark demonstrated.
- **Technical implications:** Separate numerical uncertainty, physical uncertainty, and model limitations. Horizons may share ephemerides and is not fully independent physical validation.
- **Limitations and remaining validation:** Select compatible reference cases, tolerances, uncertainty support, and domain review; passing software tests alone is insufficient.

## RC-10 — Mission constraints and suitability

- **Question:** How should evidence become explainable mission evaluation?
- **Supplied findings:** Hard constraints precede soft preferences; unsupported/missing evidence is undetermined. Suitability is not mission-success probability.
- **Decisions/status:** Accepted but not implemented: explicit unknowns; Provisional research recommendation: Pareto tradeoffs rather than one opaque weighted score.
- **Technical implications:** Define constraint states and reasons, mission duration/start windows, darkness and Earth-obstruction limits, and uncertainty semantics.
- **Limitations and remaining validation:** Truth-table/failure tests, unsupported constraints, sensitivity, and robustness studies.

## RC-11 — Multi-site and multi-date optimization

- **Question:** How can many candidate windows be evaluated efficiently?
- **Supplied findings:** R1 proposes horizon/timeline reuse, interval operations, hierarchical spatial search, and coarse screening. Narrow favorable sites can be missed.
- **Decisions/status:** Provisional research recommendation: reuse and hierarchical search; global optimality is unsupported.
- **Technical implications:** Cache scientifically complete identities; report the best evaluated candidate and search domain/settings.
- **Limitations and remaining validation:** Compare search resolutions, geographic diversity, filtering bounds, and accuracy/performance tradeoffs after single-site validation.

## RC-12 — Visualization and analyst workflows

- **Question:** How should users inspect and explain real results?
- **Supplied findings:** Explore the Moon, Mission Planner, and Compare and Explain share maps, synchronized timelines, event navigation, horizon profiles, uncertainty, and provenance.
- **Decisions/status:** Provisional research recommendation: accurate 2D south-polar map with OpenLayers and verified lunar projection. Local 3D is Deferred; a full globe is not essential.
- **Technical implications:** React/TypeScript is implemented, but no maps/API scientific results exist. Do not fabricate overlays.
- **Limitations and remaining validation:** Verify lunar projection, map coordinates/overlays, event synchronization, status presentation, and attribution.

## RC-13 — Performance, reliability and system architecture

- **Question:** How should computation stay reusable and bounded?
- **Supplied findings:** Independent Python core, FastAPI, and React foundation exists. R1 recommends isolated worker processes and scientific cache identities.
- **Decisions/status:** Accepted and implemented: stack/boundaries. Provisional research recommendation: process isolation. Distributed queues/databases/cloud are Deferred.
- **Technical implications:** Keep core offline-capable; separate execution completion from validity/completeness; measure before infrastructure selection.
- **Limitations and remaining validation:** Independent packaging checks, failure/resource tests, cache invalidation, and workload measurements; current smoke tests are limited.

## RC-14 — Data provenance and scientific interoperability

- **Question:** What is required to reproduce a result?
- **Supplied findings:** Record dataset IDs/hashes, kernels, frames/time, observer, algorithms/settings, and scientific status.
- **Decisions/status:** Accepted but not implemented: scientific result provenance under existing data policy. Provisional research recommendation: JSON manifests/CSV; PDS4/W3C PROV concepts may guide later interoperability.
- **Technical implications:** Preserve input/derived lineage and immutable identity; fail on mismatched assets; no standards-heavy framework is selected.
- **Limitations and remaining validation:** Schema/version review, checksum failure and reproduction tests, export round trips, and lunar GIS compatibility.

## RC-15 — Independent evaluation and operational readiness

- **Question:** What constitutes a releasable demonstration?
- **Supplied findings:** A scoped scientifically validated demonstration is the goal, not NASA-certified operational planning.
- **Decisions/status:** Accepted but not implemented: evidence gates and domain review. Operational certification is unsupported.
- **Technical implications:** Contracts → SPICE → terrain → horizon → visibility → temporal analysis → validation → workflows → mission evaluation/optimization. Validation accompanies every phase.
- **Limitations and remaining validation:** Define benchmark hierarchy, external review, release gates, reproducible demo scope, and documented applicability limits.

## Provisional solar-disc formula

R1 supplies this analytic approximation for a straight local horizon crossing a circular apparent solar disc. Let delta be solar-center elevation minus horizon elevation, r > 0 the apparent angular radius in the same angular units, and x = delta/r:

```text
f = 0                                      when x <= -1
f = 1                                      when x >=  1
f = (acos(-x) + x * sqrt(1 - x*x)) / pi      otherwise
```

This is a proposed geometric visible-area fraction, not a power model or evidence of validation. It assumes a locally straight horizon across the disc; a varying terrain horizon may invalidate that simplification. Domain checks, contact/center cases, numerical behavior near endpoints, apparent-direction conventions, and comparisons against more complete disc/horizon calculations are future work. No formula is implemented by this documentation.
