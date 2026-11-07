# Coordinate and observer contracts

This page specifies the Phase 1 contract-only API. The separate [Phase 2 SPICE adapter](spice-integration.md) now computes the explicitly supported geometry; contract objects alone do not load assets or perform those operations.

Implemented contract API: `lunar_core.contracts`; decision: [ADR 0002](../adr/0002-scientific-contracts.md). These are input representations, not validated positions or coordinate transformations.

`LunarCoordinates` requires `latitude_deg`, `longitude_deg`, `LunarFrame`, `LatitudeConvention.PLANETOCENTRIC`, and `LongitudeConvention.EAST_POSITIVE`. Direct constructors require enum instances; JSON uses their string values. Built-in int/float values are accepted and stored as floats; bool, strings, Decimal, NaN, infinities, and overflowing integers are rejected. Latitude is inclusive [-90, 90]. Longitude is normalized modulo 360 into [0, 360); signed zero is canonicalized. Binary floating-point rounding can lose small offsets, especially for large magnitudes. Normalization is representation-only, not a frame transformation.

At either exact pole, longitude is retained as a meridian label, not a unique physical position. Equal pole positions with different longitude labels are not necessarily equal records or configuration identities; no local tangent basis is computed. No terrestrial WGS84 shape/datum is assumed.

`LunarFrame.MOON_ME` and `LunarFrame.MOON_PA` are distinct supported symbolic frame families. Unknown names and unsupported conventions are rejected. Neither label establishes a particular ephemeris/kernel realization. Replacing a label is not a coordinate transformation and must not be used as one. Future SPICE integration must resolve and verify frame definitions, kernels and coverage; incompatible assets must fail rather than be silently relabeled. See [NAIF frame requirements](https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/frames.html), accessed 2026-11-07, for kernel-dependent frame transformations.

## Observer height

`Observer` requires coordinates, finite `height_m`, `height_reference`, `vertical_direction`, and a nonempty `reference_id`. The reference ID is a caller-supplied traceable terrain/reference-surface identifier, not an automatically verified datum.

- `HeightReference.TERRAIN_RELATIVE`: nonnegative instrument/observer offset above the declared terrain reference.
- `HeightReference.REFERENCE_SURFACE`: signed absolute elevation relative to a declared lunar reference surface; negative values are permitted.
- `VerticalDirection.RADIAL` and `SURFACE_NORMAL` are separate required labels. Neither is inferred, converted, or numerically realized.

These labels preserve unresolved physical choices rather than select a lunar shape or normal. A future geometry adapter must verify the referenced surface, origin and vertical direction before converting to Cartesian position. Terrain-relative height is not absolute lunar elevation. No DEM sampling, surface normal, observer position, horizon or SPICE calculation exists.

## Serialization example

```json
{"latitude_deg":-89.0,"longitude_deg":350.0,"frame":"MOON_ME","latitude_convention":"planetocentric","longitude_convention":"east_positive"}
```

All record types provide `to_dict`, `from_dict`, `to_json`, and `from_json`. Fields are exact: missing/unknown fields and duplicate JSON keys are rejected; nested records are JSON objects. Numeric strings are not coerced. Frozen, slotted dataclasses and tuples prevent ordinary mutation; serialized dictionaries are independent copies. As with Python frozen dataclasses generally, this is not a defense against deliberate low-level mutation. Software tests verify these rules, not physical lunar accuracy.
