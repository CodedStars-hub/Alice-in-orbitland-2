"""Analytic local geometry and kernel-boundary tests; no downloaded data required."""

import hashlib
from dataclasses import replace
from pathlib import Path

import pytest
import spiceypy as spice
from lunar_core.contracts import (
    Checksum,
    HeightReference,
    LatitudeConvention,
    LongitudeConvention,
    LunarCoordinates,
    LunarFrame,
    Observer,
    UtcInterval,
    UtcTimestamp,
    VerticalDirection,
)
from lunar_core.errors import (
    InvalidScientificInput,
    MissingScientificData,
    ScientificComputationFailure,
    UnsupportedTemporalCoverage,
)
from lunar_core.spice.kernels import KernelAsset, KernelBundle, KernelSession
from lunar_core.spice.observer import (
    REFERENCE_ID,
    LocalAngles,
    Vector3,
    local_angles,
    local_basis,
    observer_position,
)
from lunar_core.spice.time import utc_to_et


def observer(latitude: float = 0, longitude: float = 0) -> Observer:
    return Observer(
        LunarCoordinates(
            latitude,
            longitude,
            LunarFrame.MOON_ME,
            LatitudeConvention.PLANETOCENTRIC,
            LongitudeConvention.EAST_POSITIVE,
        ),
        0,
        HeightReference.REFERENCE_SURFACE,
        VerticalDirection.RADIAL,
        REFERENCE_ID,
    )


def synthetic_bundle(tmp_path: Path) -> KernelBundle:
    # Small synthetic FK, never represented as an authoritative lunar input.
    path = tmp_path / "synthetic.tf"
    path.write_text("KPL/FK\n\\begindata\nTEST_ONLY_VALUE = ( 1 )\n\\begintext\n")
    asset = KernelAsset(
        "synthetic:fk",
        "test",
        "synthetic",
        "FK",
        "https://example.invalid/synthetic",
        Checksum("sha256", hashlib.sha256(path.read_bytes()).hexdigest()),
        path.name,
        path.stat().st_size,
        "synthetic only",
        "test fixture",
    )
    return KernelBundle(
        "synthetic",
        (asset,),
        UtcInterval(
            UtcTimestamp.parse("2000-01-01T00:00:00Z"), UtcTimestamp.parse("2025-01-01T00:00:00Z")
        ),
        "2026-11-07",
    )


@pytest.mark.parametrize("latitude", [-89.999999, -45, 0, 45, 89.999999])
@pytest.mark.parametrize("longitude", [0, 90, 180, 359.999])
def test_local_basis_orthonormal(latitude: float, longitude: float) -> None:
    basis = local_basis(latitude, longitude)
    for v in (basis.north, basis.east, basis.up):
        assert v.dot(v) == pytest.approx(1, abs=5e-16)
    assert basis.north.dot(basis.east) == pytest.approx(0, abs=2e-16)
    assert basis.north.dot(basis.up) == pytest.approx(0, abs=2e-16)
    assert basis.east.dot(basis.up) == pytest.approx(0, abs=2e-16)


@pytest.mark.parametrize(
    "vector,azimuth",
    [
        (Vector3(0, 0, 1), 0),
        (Vector3(0, 1, 0), 90),
        (Vector3(0, 0, -1), 180),
        (Vector3(0, -1, 0), 270),
        (Vector3(0, 1, 1), 45),
        (Vector3(0, -1, -1), 225),
    ],
)
def test_cardinal_and_quadrants(vector: Vector3, azimuth: float) -> None:
    angles = local_angles(vector, local_basis(0, 0))
    assert angles.azimuth_deg == pytest.approx(azimuth)
    assert angles.elevation_deg == pytest.approx(0)
    assert LocalAngles.from_json(angles.to_json()) == angles


@pytest.mark.parametrize("vector", [Vector3(1, 0, 0), Vector3(-1, 0, 0), Vector3(0, 0, 0)])
def test_zenith_nadir_and_zero_azimuth_rejected(vector: Vector3) -> None:
    with pytest.raises(InvalidScientificInput):
        local_angles(vector, local_basis(0, 0))


@pytest.mark.parametrize("latitude", [-90, 90, 91, float("nan"), float("inf"), True])
def test_poles_and_bad_latitude(latitude: float) -> None:
    with pytest.raises(InvalidScientificInput):
        local_basis(latitude, 0)


def test_observer_semantics() -> None:
    assert observer_position(observer()) == Vector3(1737.4, 0, 0)
    assert observer_position(replace(observer(), height_m=1000)).x == pytest.approx(1738.4)
    with pytest.raises(MissingScientificData):
        observer_position(replace(observer(), height_reference=HeightReference.TERRAIN_RELATIVE))
    for bad in [
        replace(observer(), vertical_direction=VerticalDirection.SURFACE_NORMAL),
        replace(observer(), reference_id="unknown"),
        replace(observer(), height_m=-1737400),
    ]:
        with pytest.raises(InvalidScientificInput):
            observer_position(bad)


def test_manifest_roundtrip_and_validation(tmp_path: Path) -> None:
    bundle = synthetic_bundle(tmp_path)
    assert KernelBundle.from_json(bundle.to_json()) == bundle
    assert KernelBundle.from_json(bundle.to_json()).identity() == bundle.identity()
    for path in ["../escape", "/absolute"]:
        with pytest.raises(InvalidScientificInput):
            replace(bundle.assets[0], local_path=path)
    with pytest.raises(InvalidScientificInput):
        replace(bundle, assets=(bundle.assets[0],) * 2)
    for field, value in [("byte_size", -1), ("kernel_type", "META"), ("source_url", "file:///x")]:
        with pytest.raises(InvalidScientificInput):
            replace(bundle.assets[0], **{field: value})  # type: ignore[arg-type]


def test_missing_corrupt_and_symlink_escape(tmp_path: Path) -> None:
    bundle = synthetic_bundle(tmp_path)
    path = tmp_path / bundle.assets[0].local_path
    path.write_text("changed")
    with pytest.raises(MissingScientificData):
        bundle.verify(tmp_path)
    path.unlink()
    with pytest.raises(MissingScientificData):
        bundle.verify(tmp_path)
    path.symlink_to(Path(__file__).resolve())
    with pytest.raises(MissingScientificData):
        bundle.verify(tmp_path)


def test_lifecycle_and_missing_roles(tmp_path: Path) -> None:
    bundle = synthetic_bundle(tmp_path)
    session = KernelSession(bundle, tmp_path)
    with pytest.raises(ScientificComputationFailure):
        session.require_active()
    with session:
        assert spice.ktotal("ALL") == 1
        with pytest.raises(ScientificComputationFailure):
            with KernelSession(bundle, tmp_path):
                pass
        with pytest.raises(MissingScientificData):
            utc_to_et(session, UtcTimestamp.parse("2022-01-01T00:00:00Z"))
    assert spice.ktotal("ALL") == 0
    with pytest.raises(ScientificComputationFailure):
        session.require_active()
    with KernelSession(bundle, tmp_path):
        assert spice.ktotal("ALL") == 1
    assert spice.ktotal("ALL") == 0


def test_refuse_unrelated_pool_and_cleanup_on_failure(tmp_path: Path) -> None:
    bundle = synthetic_bundle(tmp_path)
    spice.pdpool("UNRELATED", [1.0])
    try:
        with pytest.raises(ScientificComputationFailure):
            with KernelSession(bundle, tmp_path):
                pass
        assert spice.gdpool("UNRELATED", 0, 1)[0] == 1
    finally:
        spice.dvpool("UNRELATED")
    with pytest.raises(RuntimeError):
        with KernelSession(bundle, tmp_path):
            raise RuntimeError("synthetic failure")
    assert spice.ktotal("ALL") == 0
    wrong = replace(bundle, assets=(replace(bundle.assets[0], kernel_type="SPK"),))
    with pytest.raises(InvalidScientificInput):
        with KernelSession(wrong, tmp_path):
            pass
    with KernelSession(bundle, tmp_path):
        pass


def test_frame_and_time_scope_errors(tmp_path: Path) -> None:
    bundle = synthetic_bundle(tmp_path)
    fake_roles = replace(bundle, assets=(replace(bundle.assets[0], role="leapseconds"),))
    with KernelSession(fake_roles, tmp_path) as session:
        with pytest.raises(UnsupportedTemporalCoverage):
            utc_to_et(session, UtcTimestamp.parse("1999-01-01T00:00:00Z"))
        with pytest.raises(MissingScientificData):
            utc_to_et(session, UtcTimestamp.parse("2022-01-01T00:00:00Z"))


def test_cross_thread_guard_and_existing_kernel(tmp_path: Path) -> None:
    from concurrent.futures import ThreadPoolExecutor

    bundle = synthetic_bundle(tmp_path)
    with KernelSession(bundle, tmp_path) as session:
        with ThreadPoolExecutor(max_workers=1) as executor:
            with pytest.raises(ScientificComputationFailure):
                executor.submit(session.require_active).result()
    spice.furnsh(str(tmp_path / bundle.assets[0].local_path))
    try:
        with pytest.raises(ScientificComputationFailure):
            with KernelSession(bundle, tmp_path):
                pass
        assert spice.ktotal("ALL") == 1
    finally:
        spice.unload(str(tmp_path / bundle.assets[0].local_path))


def test_elevations_and_basis_rejection() -> None:
    from lunar_core.spice.observer import LocalBasis

    for x, elevation in [(1, 45), (-1, -45)]:
        value = local_angles(Vector3(x, 1, 0), local_basis(0, 0))
        assert value.elevation_deg == pytest.approx(elevation)
    with pytest.raises(InvalidScientificInput):
        LocalBasis(Vector3(1, 0, 0), Vector3(1, 0, 0), Vector3(0, 0, 1))
    with pytest.raises(InvalidScientificInput):
        local_basis(0, 10**1000)


def test_frame_inputs_fail_without_substitution(tmp_path: Path) -> None:
    from lunar_core.errors import UnsupportedCoordinateConvention
    from lunar_core.spice.frames import realized_frame

    with KernelSession(synthetic_bundle(tmp_path), tmp_path) as session:
        with pytest.raises(UnsupportedCoordinateConvention):
            realized_frame(session, "IAU_MOON", 0)  # type: ignore[arg-type]
        for et in [float("nan"), float("inf"), True, 10**1000]:
            with pytest.raises(InvalidScientificInput):
                realized_frame(session, LunarFrame.MOON_ME, et)
