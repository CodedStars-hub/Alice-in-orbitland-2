# Observer reference geometry and local angles

Initial geometry is the sphere represented by `BODY301_RADII = (1737.4, 1737.4, 1737.4)` km in the inspected [pck00011.tpc](https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/pck00011.tpc), accessed/retrieved 2026-11-07. This is a declared model reference surface, not a DEM, measured local elevation or safe-landing surface. The engine checks the loaded radii agree with this selection.

Require Phase 1 `Observer` with `height_reference=REFERENCE_SURFACE`, `vertical_direction=RADIAL`, and `reference_id='naif:pck00011:BODY301_RADII:sphere'`. With planetocentric latitude phi, east-positive longitude lambda and signed height h metres, observer radius is 1737.4 + h/1000 km and must be positive. Position is radius times local radial up. Terrain-relative heights fail with missing-data errors: there is no invented ground elevation. Surface-normal labels are rejected even though a mathematical sphere's normal is radial; the adapter does not silently reinterpret an explicitly different vertical contract. Triaxial ellipsoid normals and DEM/datum reconciliation remain deferred.

## Local basis

For nonpolar sites in the selected realized frame:

```text
up    = (cos(phi)cos(lambda), cos(phi)sin(lambda), sin(phi))
east  = (-sin(lambda), cos(lambda), 0)
north = (-sin(phi)cos(lambda), -sin(phi)sin(lambda), cos(phi))
```

The basis is orthonormal; input basis records must satisfy pairwise dot-product checks within 1e-12. This is a software consistency tolerance, not a physical uncertainty estimate. Azimuth is atan2(east component, north component), wrapped to [0, 360): zero north, increasing eastward. Elevation is atan2(up component, horizontal norm) in [-90, 90] degrees. Range is vector norm in kilometres. Vectors are normalized before angle extraction.

Exact ±90-degree sites are rejected because this phase does not choose a pole meridian orientation for local azimuth. Near-pole north/east follows the declared longitude and formulas; it is not a uniquely privileged direction at the pole. Zero vectors and numerical zenith/nadir (normalized horizontal norm <= 1e-14) are rejected because azimuth is undefined/ill-conditioned. No arbitrary zero azimuth is emitted. These singularity policies are explicit, not guarantees about angular error. Future horizon azimuths must use the same declared local basis.

Sun/Earth target-center vectors are geometric and uncorrected, translated from Moon center to this observer. No terrain occultation or disc visibility follows from a target elevation. [ADR 0003](../adr/0003-spice-geometry.md) records this deliberately narrow scope; [validation](../validation/spice-geometry-validation.md) distinguishes synthetic geometry checks from reference comparisons.
