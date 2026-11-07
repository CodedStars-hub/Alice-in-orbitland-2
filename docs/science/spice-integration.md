# SPICE integration

Phase 2 implements `lunar_core.spice`: `kernels` (asset records/session), `time` (UTC→ET), `frames` (DE440 mapping/coverage), `observer` (sphere/local basis), and `geometry` (Sun/Earth target-center results). Core remains independent of HTTP and UI. SpiceyPy 8.3.0 is a direct runtime dependency; NumPy 2.5.4 is pinned transitively in the root lock. Local wheels report CSPICE N0067. See [SpiceyPy installation](https://spiceypy.readthedocs.io/en/stable/installation.html), accessed 2026-11-07.

## Reviewed bundle and acquisition

The exact five assets, HTTPS source URLs, observed SHA-256 hashes, byte sizes, versions, roles/types, load order, coverage notes and retrieval date are in [spice-de440.json](../../data/manifests/spice-de440.json). Hashes were computed from bytes obtained directly from NAIF on 2026-11-07; they are local retrieval identities, not independently published NAIF SHA-256 attestations. No kernel bytes are committed. Redistribution notes point to [NAIF rules](https://naif.jpl.nasa.gov/naif/rules.html); obtain assets from NAIF and preserve attribution rather than assuming the repository MIT license applies to them.

The order is naif0012.tls, pck00011.tpc, moon_pa_de440_200625.bpc, moon_de440_250416.tf, de440s.bsp. The review scope is UTC [2000-01-01, 2025-01-01), deliberately narrower than the binary coverage; extending it requires leap-second and coverage review. LSK contents do not predict future leap seconds. Metadata coverage notes do not replace runtime SPICE coverage checks.

```sh
make install
.venv/bin/python scripts/fetch_spice_kernels.py
LUNAR_SPICE_CACHE=data/kernels .venv/bin/python -m pytest packages/lunar_core/tests
```

Acquisition is explicit, separate from core and CI. It verifies size/hash, fails on existing mismatched files, and never silently downloads during a calculation. Cache files must remain unchanged during a session. The script uses the reviewed manifest and ignores no checksum errors. `KernelBundle.verify(cache)` checks readable paths confined to the cache, size and bytes; `identity()` hashes the complete manifest, including load order and metadata. It does not verify provider authenticity beyond the declared retrieval record.

## Exclusive lifecycle

`with KernelSession(bundle, cache) as session:` requires an initially empty SPICE kernel/file pool and no kernel-pool variables. It refuses to clear unrelated consumers. It verifies every asset before loading, rejects meta-kernels, checks actual kernel types/headers, and clears only the exclusively owned pool on exit or partial-load failure. Missing/corrupt inputs fail explicitly. Sessions cannot nest; access is restricted to the creating process/thread.

SPICE state is process-global. The cooperating-session lock is not protection against arbitrary outside SpiceyPy calls. Use a dedicated single-threaded process; do not call SPICE outside the session, mutate its state, fork an active session, or use this inside concurrent API requests. Future concurrency requires independent worker processes, not shared-pool threads. No workers/queues are implemented. Read-only bundle access preserves the declared manifest used by calculations; private Python attributes are not a security boundary.

## Time and result semantics

`utc_to_et(session, UtcTimestamp)` uses `str2et` with explicit UTC labeling and a temporary Gregorian calendar setting restored afterward. It records normalized input UTC, conversion description and TDB seconds past J2000. No Unix-time substitution or manual leap arithmetic exists. Phase 1 still rejects explicit leap-second timestamp labels. See [NAIF str2et](https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/str2et_c.html), accessed 2026-11-07.

`target_geometry(session, observer, utc, Target.SUN|EARTH, code_revision=<full Git SHA>)` returns an immutable JSON-round-trippable `GeometryResult`. Fields include observer identity, target NAIF ID, UTC/ET, realized frame, vector kilometres, local degrees/range km, `NONE` correction, reference geometry, actual kernel manifest/hash, algorithm version, declared code revision, SpiceyPy/toolkit versions and separate execution/validity/completeness status. Code revision is caller-declared; it does not attest to a clean checkout. Preserve exact run configuration and dirty-state information externally if running modified code.

`NONE` selects simultaneous geometric target-center positions, without light-time or stellar-aberration corrections. It is intentionally not apparent-disc geometry. Moon-center target vectors from `spkpos(target, et, frame, 'NONE', '301')` are translated by subtracting the observer position in the same frame/epoch. Sun is 10, Earth center is 399; Earth-Moon barycenter 3 is never substituted. See [NAIF spkpos](https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkpos_c.html), accessed 2026-11-07.

Complete status refers only to the supported geometry inputs. Scientific validity remains `not_assessed`; success is not physical validation. No disc occultation, terrain obstruction, illumination fraction, power, communications reliability or landing safety is computed. See [frames](lunar-reference-frames.md), [observer geometry](observer-geometry.md), [validation evidence](../validation/spice-geometry-validation.md), and [ADR 0003](../adr/0003-spice-geometry.md).
