# Scientific configuration contracts

This page specifies the Phase 1 contract-only API. The separate [Phase 2 SPICE adapter](spice-integration.md) now computes the explicitly supported geometry; contract objects alone do not load assets or perform those operations.

`ScientificConfiguration` groups an `Observer`, `UtcInterval`, three required numerical settings and independent Sun/Earth visibility definitions. There are no scientific numerical defaults.

| Field | Unit / validation | Meaning and limit |
| --- | --- | --- |
| `angular_resolution_deg` | Degrees, finite, 0 < value <= 360 | Requested horizon azimuth sampling step; no grid or optimum selected |
| `terrain_sampling_distance_m` | Metres, finite, strictly positive | Requested radial terrain sampling distance; not DEM accuracy |
| `event_refinement_tolerance_s` | Seconds, finite, strictly positive | Requested event refinement tolerance; not an achieved error or completeness guarantee |

Both `SolarVisibility` and `EarthVisibility` expose `center`, `any_disc`, `full_disc`, and `fractional_disc`. Center refers to a geometric center direction; any/full refer to some/all of the apparent disc being unobstructed; fractional refers to visible geometric disc area. Contact equality, apparent-direction corrections, extended-disc shape and horizon integration remain future algorithm decisions. The labels do not implement the provisional solar formula or an Earth-disc algorithm. Sun and Earth enums are distinct even where labels match.

`configuration.identity()` hashes a deterministic UTF-8 serialization prefixed with `lunar_core.configuration.v1:` using SHA-256. JSON keys are sorted and separators compact; numeric fields normalize to floats and UTC timestamps normalize to Z. Pole longitude labels are retained. Exact floating-point values affect identity; no tolerance-based equivalence is attempted. This is a versioned local configuration identity, not an interoperable universal JSON canonicalization standard or a complete scientific cache key. Input file/kernel hashes, algorithm versions and realization settings must also participate in future cache identity.

Records reject invalid types and nonfinite values; serialized records require exact fields. No assets are loaded, coverage checked, sampling performed, visibility computed, or refinement executed. Tiny positive settings are structurally valid but may be impractical; resource and scientifically justified bounds belong to future algorithm/workload contracts.

Geometric sunlight is not power, Earth visibility is not a reliable communications link, and neither establishes landing safety. See [coordinate contracts](coordinate-contracts.md), [time contracts](time-contracts.md), [provenance contracts](provenance-contracts.md), and [modeling principles](modeling-principles.md).
