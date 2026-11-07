# Lunar reference frames: supported Phase 2 scope

The selected [NAIF frame kernel](https://naif.jpl.nasa.gov/pub/naif/generic_kernels/fk/satellites/moon_de440_250416.tf), accessed and retrieved 2026-11-07, explicitly pairs with moon_pa_de440_200625.bpc. The pinned manifest records both identities. Kernel names alone do not establish compatibility; bytes and epoch-dependent transformations must also be available.

| Phase 1 symbolic label | Explicit realized SPICE frame | ID |
| --- | --- | --- |
| MOON_ME | MOON_ME_DE440_ME421 | 31009 |
| MOON_PA | MOON_PA_DE440 | 31008 |

These are distinct realizations. The ME frame uses a fixed rotation from the DE440 PA frame, aligned closely with the DE421 ME system. The kernel provides their definitions and relative rotation; the adapter does not invent it. No coordinate relabeling or implicit IAU_MOON substitution is permitted. Coordinates are interpreted in the explicitly selected realization; callers must ensure their source coordinates use it. No general site-coordinate transformation API is provided in this milestone.

`realized_frame` requires declared frame/orientation roles and calls `pxform(realization, 'J2000', et)` to resolve orientation at that epoch. Missing definitions or temporal orientation coverage fail clearly. The constants PCK is used for size only; its IAU_MOON orientation is not the selected geometry frame. Geometric output is expressed in the realized lunar frame at the observation epoch.

Supported longitude remains east-positive [0, 360), latitude planetocentric. A spherical reference surface does not make PA and ME interchangeable. Reference-frame choice affects coordinates/local directions; terrain products must be explicitly reconciled in Phase 3. The current bundle scope is narrower than raw binary coverage and has no accuracy certification. See [coordinate contracts](coordinate-contracts.md), [observer geometry](observer-geometry.md), and [validation](../validation/spice-geometry-validation.md).
