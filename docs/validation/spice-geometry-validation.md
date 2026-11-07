# SPICE geometry verification evidence

Snapshot: 2026-11-07, local Python 3.12.15, SpiceyPy 8.3.0, NumPy 2.5.4, CSPICE N0067. Inputs are the five verified assets in [spice-de440.json](../../data/manifests/spice-de440.json). This is scoped implementation/reference evidence, not a landing-safety or physical-accuracy certification.

## Reproduction and test levels

```sh
make install
make check
.venv/bin/python -m pytest packages/lunar_core/tests
.venv/bin/python scripts/fetch_spice_kernels.py
LUNAR_SPICE_CACHE=data/kernels .venv/bin/python -m pytest packages/lunar_core/tests
.venv/bin/python -m pip check
.venv/bin/python -m pre_commit run --all-files
```

Default CI needs no downloads: real-kernel tests skip only when LUNAR_SPICE_CACHE is absent. An explicitly supplied missing/corrupt bundle fails. Never replace missing ephemerides with fake vectors. Synthetic fixtures are clearly labeled, small test-owned text kernels and analytic directions, not observed lunar outputs.

Unit/synthetic coverage includes byte/path/type boundaries, missing kernels/roles, corrupted inputs, symlink escape, lifecycle/cleanup, refusal of unrelated pool variables/files, nested/thread guards, coordinate/reference/height rejection, local orthogonality, cardinal/quadrant/elevation checks and singularities. Real tests cover both realized frames and targets at three epochs, identical-input repeatability, JSON round trips, finite output/range checks, scoped time failure, orientation coverage, Gregorian conversion despite a changed global calendar, and published reference vectors. Range sanity checks are not independent orbital validation.

## Published reference comparison

The inspected [NAIF frame-kernel example](https://naif.jpl.nasa.gov/pub/naif/generic_kernels/fk/satellites/moon_de440_250416.tf) gives geometric Earth-center position relative to Moon center at ET 717768000 seconds (2022 SEP 30 TDB), using NONE. It prints position components to 0.001 km. Our DE440s/DE440 orientation bundle yields component residuals in km:

| Realized frame | x residual | y residual | z residual |
| --- | --- | --- | --- |
| MOON_ME_DE440_ME421 | +0.0003868651693 | -0.0001390492944 | -0.0000654627784 |
| MOON_PA_DE440 | +0.0003231774317 | -0.0002902960114 | +0.0000735404046 |

The test uses absolute 0.00051 km per component, slightly above half a printed unit to allow floating-point comparison at the rounded reference precision. This comparison is Moon-centered, not a validation of surface azimuth or terrain. The source example uses full DE440; our short DE440s subset agrees at the displayed precision for this case. Shared ephemerides/kernel definitions limit independence. No claim of sub-metre physical accuracy follows from agreement with rounded output. JPL Horizons and independent surface-observer reference comparisons remain deferred.

## Observed numerical behavior

- At ET 0, maximum elementwise residual of R-transpose-R from identity was 2.220446049250313e-16 (ME) and 1.1102230246251565e-16 (PA).
- On latitudes {-89.999999,-45,0,45,89.999999} degrees and longitudes {0,90,180,359.999}, maximum local-basis dot-product identity residual was 3.308722450212111e-24. This sampled check is not a global error bound or a terrain convergence study.
- UTC 2000-01-01T12:00:00Z converted to ET 64.18392728473108; 2022-09-30T00:00:00Z to 717768069.1823508; 2024-01-01T00:00:00Z to 757339269.1839061. SPICE UTC round trips at six fractional digits reproduced those input instants. These are observed regression/round-trip values, not independently sourced expected UTC-to-ET truth.
- Exact poles and numerical zenith/nadir are rejected; near-pole tests exercise a stated finite set. No numerical guarantee for arbitrary near-singular inputs is asserted.

These implementation checks do not quantify terrain, reference-surface or ephemeris physical uncertainty. No spatial/time discretization convergence is applicable to a single instantaneous ephemeris call; future horizon/event algorithms need separate convergence studies. This scope has no physical uncertainty model. See [validation strategy](strategy.md).

## Local check outcomes

Final local runs: `make check` / pre-commit project checks pass with 155 Python tests passed and 16 optional real-kernel tests skipped, plus one frontend test, lint, types and build. Independent default core tests: 150 passed, 16 skipped. With `LUNAR_SPICE_CACHE=data/kernels`, the complete Python suite passed all 171 tests; the core accounts for 166. The 61 added cases comprise 44 unit/synthetic, 16 opt-in real-kernel and one acquisition integration case.

`pip check` passed; installed third-party versions match the root lock. Standalone `python -I` core SPICE import passed without importing FastAPI/lunar_api. Pre-commit, local documentation links, whitespace and data/secret scope checks run before commit. Existing Starlette/AnyIO deprecation and unavailable pip-cache warnings remain; neither prevented completion. Remote CI is checked after push and is not inferred from these local results.
