"""Opt-in, verified real-kernel checks. Missing explicitly requested assets fail."""

import math
import os
import subprocess
from dataclasses import replace
from pathlib import Path

import pytest
import spiceypy as spice
from lunar_core.contracts import (
    HeightReference,
    LatitudeConvention,
    LongitudeConvention,
    LunarCoordinates,
    LunarFrame,
    Observer,
    UtcTimestamp,
    VerticalDirection,
)
from lunar_core.errors import UnsupportedCoordinateConvention, UnsupportedTemporalCoverage
from lunar_core.spice.frames import realized_frame
from lunar_core.spice.geometry import GeometryResult, Target, target_geometry
from lunar_core.spice.kernels import KernelBundle, KernelSession
from lunar_core.spice.observer import REFERENCE_ID
from lunar_core.spice.time import utc_to_et


def observer(latitude: float, frame: LunarFrame) -> Observer:
    return Observer(
        LunarCoordinates(
            latitude,
            45,
            frame,
            LatitudeConvention.PLANETOCENTRIC,
            LongitudeConvention.EAST_POSITIVE,
        ),
        2,
        HeightReference.REFERENCE_SURFACE,
        VerticalDirection.RADIAL,
        REFERENCE_ID,
    )


@pytest.fixture
def real_session() -> object:
    cache = os.getenv("LUNAR_SPICE_CACHE")
    if cache is None:
        pytest.skip("Set LUNAR_SPICE_CACHE for verified real-kernel integration tests")
    manifest = Path(__file__).resolve().parents[3] / "data/manifests/spice-de440.json"
    bundle = KernelBundle.from_json(manifest.read_text())
    return KernelSession(bundle, Path(cache))


@pytest.mark.parametrize("frame", list(LunarFrame))
@pytest.mark.parametrize("target", list(Target))
@pytest.mark.parametrize(
    "instant", ["2000-01-01T12:00:00Z", "2022-09-30T00:00:00Z", "2024-01-01T00:00:00Z"]
)
def test_real_targets_and_reproducibility(
    real_session: KernelSession, frame: LunarFrame, target: Target, instant: str
) -> None:
    with real_session as session:
        revision = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
        result = target_geometry(
            session,
            observer(-89, frame),
            UtcTimestamp.parse(instant),
            target,
            code_revision=revision,
        )
        again = target_geometry(
            session, result.observer, result.time.utc, target, code_revision=revision
        )
        assert result.to_json() == again.to_json()
        assert GeometryResult.from_json(result.to_json()) == result
        assert all(
            math.isfinite(v)
            for v in (
                result.angles.azimuth_deg,
                result.angles.elevation_deg,
                result.angles.range_km,
            )
        )
        assert 0 <= result.angles.azimuth_deg < 360
        assert -90 <= result.angles.elevation_deg <= 90
        assert result.angles.range_km > (100_000_000 if target is Target.SUN else 300_000)
        assert result.aberration_correction == "NONE"
        assert result.kernel_identity == session.bundle.identity()
    assert spice.ktotal("ALL") == 0


@pytest.mark.parametrize(
    "frame,expected",
    [
        (LunarFrame.MOON_ME, (374008.654, -23435.970, 10141.334)),
        (LunarFrame.MOON_PA, (373997.028, -23558.987, 10284.057)),
    ],
)
def test_naif_published_moon_center_reference(
    real_session: KernelSession, frame: LunarFrame, expected: tuple[float, ...]
) -> None:
    # Published in moon_de440_250416.tf: 2022 SEP 30 TDB, ET 717768000.
    # This is a Moon-center vector comparison, not a surface/horizon reference.
    with real_session as session:
        realized = realized_frame(session, frame, 717768000.0)
        actual, _ = spice.spkpos("399", 717768000.0, realized, "NONE", "301")
        assert list(actual) == pytest.approx(expected, abs=0.00051, rel=0)


def test_time_calendar_scope_and_frames(real_session: KernelSession) -> None:
    with real_session as session:
        old = spice.timdef("GET", "CALENDAR", 32)
        try:
            spice.timdef("SET", "CALENDAR", 32, "JULIAN")
            epoch = utc_to_et(session, UtcTimestamp.parse("2000-01-01T12:00:00Z"))
            assert epoch.et_tdb_seconds_past_j2000 == pytest.approx(64.18392728473108, abs=1e-10)
            # Above is an observed regression value, NOT an independent UTC reference.
            assert spice.timdef("GET", "CALENDAR", 32) == "JULIAN"
        finally:
            spice.timdef("SET", "CALENDAR", 32, old)
        for text in ["1999-01-01T00:00:00Z", "2025-01-01T00:00:00Z"]:
            with pytest.raises(UnsupportedTemporalCoverage):
                utc_to_et(session, UtcTimestamp.parse(text))
        with pytest.raises(UnsupportedTemporalCoverage):
            realized_frame(session, LunarFrame.MOON_ME, 1e12)
        with pytest.raises(UnsupportedCoordinateConvention):
            realized_frame(session, "IAU_MOON", 0)  # type: ignore[arg-type]
        for frame in LunarFrame:
            m = spice.pxform(realized_frame(session, frame, 0), "J2000", 0)
            for i in range(3):
                for j in range(3):
                    assert sum(float(m[k, i] * m[k, j]) for k in range(3)) == pytest.approx(
                        1 if i == j else 0, abs=1e-14
                    )


def test_surface_projection_and_result_tamper_rejection(real_session: KernelSession) -> None:
    from lunar_core.errors import InvalidScientificInput
    from lunar_core.spice.observer import observer_position

    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    site = observer(-89, LunarFrame.MOON_ME)
    with real_session as session:
        result = target_geometry(
            session,
            site,
            UtcTimestamp.parse("2022-09-30T00:00:00Z"),
            Target.EARTH,
            code_revision=revision,
        )
        center, _ = spice.spkpos(
            "399", result.time.et_tdb_seconds_past_j2000, result.realized_frame, "NONE", "301"
        )
        position = observer_position(site)
        for actual, target, offset in zip(
            (result.vector_km.x, result.vector_km.y, result.vector_km.z),
            center,
            (position.x, position.y, position.z),
            strict=True,
        ):
            assert actual + offset == pytest.approx(float(target), abs=1e-10, rel=0)
        with pytest.raises(InvalidScientificInput):
            replace(result, realized_frame="IAU_MOON")
        with pytest.raises(InvalidScientificInput):
            replace(result, code_revision="main")
        with pytest.raises(InvalidScientificInput):
            replace(result, aberration_correction="LT+S")
