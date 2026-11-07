# Open questions and required experiments

Evidence: [R1/B1](README.md#evidence-register) and inspected gaps in L1. This backlog is not authorization. Statuses follow the [decision ledger](SCIENTIFIC_DECISIONS.md); resolve major choices with evidence and ADRs, not by silently editing a recommendation into a fact.

| Priority / dependency | Question and current status | Evidence or experiment needed |
| --- | --- | --- |
| Before Phase 1 | Exact requirements and scientific MVP tolerances — Unresolved | Recover original conversation/export and review authoritative challenge details; choose bounded site/date/metric acceptance cases |
| Phase 1 | Longitude interval, pole handling, planetocentric latitude, frame realization, shape, units — Unresolved | Formal contracts, compatible authoritative references, boundary/invalid-input tests |
| Phase 1 | Observer height above which surface, along which direction? — Unresolved | Define terrain elevation versus instrument height, vertical direction, and consequences for horizon geometry |
| Phases 1–2 | UTC representation, ephemeris time, leap seconds, unsupported conversions — Unresolved | Validated SPICE conversion design and leap-second/coverage failure tests; no hand-built unsupported transformations |
| Phase 2 | Kernel set, versions, load order, frames, aberration/light-time policy — Unresolved | Verified source manifests/checksums, coverage and compatibility review, reproducible reference comparisons |
| Phase 3 | Exact LOLA DEM/version, coverage, datum, no-data rules, error model — Unresolved | Inspect actual product metadata; sampling and missing-coverage tests; distinguish grid spacing from accuracy |
| Phase 4 | Near/far terrain, radial reach, curvature, azimuth sampling, interpolation — Provisional research recommendation | Synthetic obstructors and seam cases; spatial convergence, conservative coverage treatment; assess rather than adopt 0.5° precedent |
| Phase 5 | Solar apparent-direction convention and center/any/full/fraction definitions — Unresolved | Disc/horizon analytic fixtures; evaluate straight-horizon formula versus varying horizons and determine applicability |
| Phase 5 | Earth-center versus Earth-disc metric — Unresolved | Explicit observable definition and synthetic occultation cases; avoid RF/link claims |
| Phase 6 | Event tolerance, same-sign short events, tangencies, discontinuities, interval endpoints — Unresolved | Adversarial synthetic timelines and temporal convergence; state missed-event limits unless bounds justify guarantees |
| Every science phase / Phase 7 gate | Reference compatibility and independent evaluation — Unresolved | Compatible Horizons/PGDA cases, suitable LROC observations, uncertainty studies, domain review, justified tolerances |
| Phases 8–10 | API validity/completeness states and worker resource limits — Unresolved | Failure contracts and measured workload bounds; isolate execution completion from science status |
| Phase 9 | OpenLayers and lunar projection — Provisional research recommendation | Verify lunar CRS parameters, coordinates, overlays, polar behavior, and attribution before selection |
| Phase 10 | Hard constraints before preferences and explicit unknowns — Accepted but not implemented; Pareto semantics — Provisional research recommendation | Define evaluation statuses and tests proving unsupported evidence cannot silently pass/fail |
| Phase 10 | Search completeness, geographic diversity, narrow favorable sites — Unresolved | Search-resolution studies and defensible screening bounds; report only evaluated-space best candidates |
| Phases 1/11 | Provenance schemas, cache identity, JSON/CSV interoperability — Unresolved | Round-trip/reproduction tests, invalidation experiments, versioning policy; assess PDS4/PROV concepts without excess infrastructure |
| Phase 11 | Queues, database, distributed/cloud execution — Deferred | Measurements and explicit scope approval before selecting infrastructure |
| Before public release | License holder placeholder; current advisories and live CI — Unresolved | Maintainer identity, current dependency audit with exposure assessment, actual Actions results |

No real scientific benchmark, uncertainty ensemble, or independent evaluation has been demonstrated. Do not replace absent evidence with plausible numbers.
