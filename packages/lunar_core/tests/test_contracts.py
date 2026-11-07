"""Synthetic contract invariants only; no physical/scientific accuracy assertions."""

import json
from dataclasses import FrozenInstanceError, replace
from datetime import UTC, datetime, timedelta, timezone
from decimal import Decimal
from typing import Any

import pytest
from lunar_core.contracts import (
    Checksum,
    DataCompleteness,
    DatasetReference,
    EarthVisibility,
    ExecutionStatus,
    HeightReference,
    KernelManifest,
    KernelReference,
    LatitudeConvention,
    LongitudeConvention,
    LunarCoordinates,
    LunarFrame,
    Observer,
    Provenance,
    Record,
    ScientificConfiguration,
    ScientificStatus,
    ScientificValidity,
    SolarVisibility,
    TimeScale,
    UtcInterval,
    UtcTimestamp,
    VerticalDirection,
)
from lunar_core.errors import (
    IncompleteScientificCoverage,
    InvalidScientificInput,
    MissingScientificData,
    NumericalConvergenceFailure,
    ScientificComputationFailure,
    UnsupportedCoordinateConvention,
    UnsupportedTemporalCoverage,
)


def coordinates(**changes: Any) -> LunarCoordinates:
    values: dict[str, Any] = dict(
        latitude_deg=-89,
        longitude_deg=-10,
        frame=LunarFrame.MOON_ME,
        latitude_convention=LatitudeConvention.PLANETOCENTRIC,
        longitude_convention=LongitudeConvention.EAST_POSITIVE,
    )
    return LunarCoordinates(**(values | changes))


def configuration() -> ScientificConfiguration:
    return ScientificConfiguration(
        Observer(
            coordinates(),
            2,
            HeightReference.TERRAIN_RELATIVE,
            VerticalDirection.RADIAL,
            "synthetic:terrain-reference",
        ),
        UtcInterval(
            UtcTimestamp.parse("2026-01-01T00:00:00Z"), UtcTimestamp.parse("2026-01-02T00:00:00Z")
        ),
        1,
        10,
        0.1,
        SolarVisibility.FRACTIONAL_DISC,
        EarthVisibility.CENTER,
    )


@pytest.mark.parametrize("latitude", [-90, -0.0, 0, 90])
@pytest.mark.parametrize("longitude,expected", [(-360, 0), (-10, 350), (360, 0), (721, 1)])
def test_coordinates_boundaries_and_normalization(
    latitude: float, longitude: float, expected: float
) -> None:
    value = coordinates(latitude_deg=latitude, longitude_deg=longitude)
    assert value.latitude_deg == latitude
    assert value.longitude_deg == expected
    assert value.frame is LunarFrame.MOON_ME
    assert LunarCoordinates.from_json(value.to_json()) == value


def test_pole_meridian_and_frame_are_preserved() -> None:
    pole = coordinates(latitude_deg=90, longitude_deg=123)
    assert pole.longitude_deg == 123
    pa = replace(pole, frame=LunarFrame.MOON_PA)
    assert pa != pole
    assert pa.latitude_deg == pole.latitude_deg  # relabeling is not a transformation
    assert pa.to_dict()["frame"] == "MOON_PA"


@pytest.mark.parametrize("latitude", [-90.00001, 90.00001])
def test_invalid_latitude(latitude: float) -> None:
    with pytest.raises(InvalidScientificInput, match="latitude"):
        coordinates(latitude_deg=latitude)


@pytest.mark.parametrize(
    "bad",
    [True, False, "1", None, [], Decimal("1"), float("nan"), float("inf"), -float("inf"), 10**1000],
)
@pytest.mark.parametrize("field", ["latitude_deg", "longitude_deg"])
def test_invalid_coordinate_numbers(field: str, bad: object) -> None:
    with pytest.raises(InvalidScientificInput):
        coordinates(**{field: bad})


@pytest.mark.parametrize(
    "field,bad",
    [
        ("frame", "MOON_ME"),
        ("frame", "WGS84"),
        ("frame", "MOON"),
        ("latitude_convention", "planetographic"),
        ("longitude_convention", "west_positive"),
    ],
)
def test_untyped_or_unsupported_conventions(field: str, bad: str) -> None:
    with pytest.raises(UnsupportedCoordinateConvention):
        coordinates(**{field: bad})
    serialized = coordinates().to_dict() | {field: "unsupported"}
    with pytest.raises(UnsupportedCoordinateConvention):
        LunarCoordinates.from_dict(serialized)


def test_immutability_and_serialized_copy() -> None:
    config = configuration()
    with pytest.raises(FrozenInstanceError):
        config.observer.coordinates.latitude_deg = 0  # type: ignore[misc]
    with pytest.raises((FrozenInstanceError, TypeError, AttributeError)):
        config.extra = 1  # type: ignore[attr-defined]
    copy = config.to_dict()
    copy["observer"] = None
    assert config.observer.height_m == 2
    assert ScientificConfiguration.from_json(config.to_json()) == config


def test_height_semantics() -> None:
    observer = configuration().observer
    with pytest.raises(InvalidScientificInput):
        replace(observer, height_m=-1)
    elevation = replace(
        observer,
        height_reference=HeightReference.REFERENCE_SURFACE,
        height_m=-100,
        reference_id="synthetic:reference-surface",
    )
    assert elevation.height_m == -100
    assert elevation.height_reference != observer.height_reference
    assert replace(elevation, vertical_direction=VerticalDirection.SURFACE_NORMAL) != elevation
    with pytest.raises(InvalidScientificInput):
        replace(observer, height_reference="terrain_relative")  # type: ignore[arg-type]


@pytest.mark.parametrize("bad", [True, "2", float("nan"), float("inf")])
def test_invalid_height(bad: Any) -> None:
    with pytest.raises(InvalidScientificInput):
        replace(configuration().observer, height_m=bad)


def test_utc_offset_normalization_and_roundtrip() -> None:
    stamp = UtcTimestamp.parse("2026-01-01T05:30:00.123456+05:30")
    assert stamp.value == datetime(2026, 1, 1, 0, 0, 0, 123456, tzinfo=UTC)
    assert stamp.to_dict() == {"value": "2026-01-01T00:00:00.123456Z", "scale": "UTC"}
    assert UtcTimestamp.from_json(stamp.to_json()) == stamp
    assert (
        UtcTimestamp(
            datetime(2026, 1, 1, 1, tzinfo=timezone(timedelta(hours=1))), TimeScale.UTC
        ).value.hour
        == 0
    )


@pytest.mark.parametrize(
    "text",
    [
        "2026-01-01",
        "2026-01-01T00:00:00",
        "not-a-date",
        "2016-12-31T23:59:60Z",
        "2026-01-01T00:00:00-00:00",
        "2026-01-01T00:00:00+01:99",
        "2026-02-30T00:00:00Z",
        "2026-01-01T00:00:00.1234567Z",
    ],
)
def test_unsupported_utc_text(text: str) -> None:
    with pytest.raises(InvalidScientificInput):
        UtcTimestamp.parse(text)


def test_naive_and_wrong_time_types() -> None:
    with pytest.raises(InvalidScientificInput, match="timezone-aware"):
        UtcTimestamp(datetime(2026, 1, 1), TimeScale.UTC)
    with pytest.raises(InvalidScientificInput):
        UtcTimestamp.from_dict({"value": "2026-01-01T00:00:00Z", "scale": "ET"})
    with pytest.raises(InvalidScientificInput):
        UtcTimestamp("2026-01-01T00:00:00Z", TimeScale.UTC)  # type: ignore[arg-type]


@pytest.mark.parametrize("end", ["2026-01-01T00:00:00Z", "2025-12-31T00:00:00Z"])
def test_interval_requires_strict_order(end: str) -> None:
    with pytest.raises(InvalidScientificInput, match="strictly before"):
        UtcInterval(UtcTimestamp.parse("2026-01-01T00:00:00Z"), UtcTimestamp.parse(end))


@pytest.mark.parametrize(
    "field",
    ["angular_resolution_deg", "terrain_sampling_distance_m", "event_refinement_tolerance_s"],
)
@pytest.mark.parametrize("bad", [0, -1, True, "1", float("nan"), float("inf")])
def test_configuration_bounds(field: str, bad: Any) -> None:
    with pytest.raises(InvalidScientificInput):
        replace(configuration(), **{field: bad})


def test_visibility_choices_and_config_identity() -> None:
    config = configuration()
    with pytest.raises(InvalidScientificInput):
        replace(config, angular_resolution_deg=360.001)
    for solar in SolarVisibility:
        for earth in EarthVisibility:
            selected = replace(config, solar_visibility=solar, earth_visibility=earth)
            assert ScientificConfiguration.from_json(selected.to_json()) == selected
    normalized = replace(
        config, observer=replace(config.observer, coordinates=coordinates(longitude_deg=350))
    )
    assert normalized.identity() == config.identity()
    assert replace(config, terrain_sampling_distance_m=11).identity() != config.identity()
    with pytest.raises(InvalidScientificInput):
        replace(config, earth_visibility=SolarVisibility.CENTER)  # type: ignore[arg-type]


def test_provenance_roundtrip_order_and_empty_inputs() -> None:
    checksum = Checksum("sha256", "a" * 64)  # Synthetic digest, not an acquired input.
    one = KernelReference("synthetic:k1", "test", "synthetic:source", checksum, "test-role")
    two = replace(one, identifier="synthetic:k2")
    manifest = KernelManifest((one, two))
    dataset = DatasetReference("synthetic:dem", "test", "synthetic:source", checksum)
    provenance = Provenance(
        (dataset,), manifest, "synthetic:algorithm", "test", "b" * 40, configuration().identity()
    )
    assert Provenance.from_json(provenance.to_json()) == provenance
    assert manifest.to_dict()["kernels"] == [one.to_dict(), two.to_dict()]
    assert KernelManifest(()).kernels == ()  # Empty means no declared assets, not coverage.
    with pytest.raises(InvalidScientificInput, match="unique"):
        KernelManifest((one, one))
    with pytest.raises(InvalidScientificInput):
        KernelManifest([one])  # type: ignore[arg-type]
    with pytest.raises(InvalidScientificInput):
        replace(provenance, datasets=(dataset, dataset))
    with pytest.raises(InvalidScientificInput):
        replace(provenance, code_revision="main")
    with pytest.raises(InvalidScientificInput):
        replace(dataset, version=" ")


@pytest.mark.parametrize(
    "algorithm,digest",
    [("md5", "a" * 64), ("sha256", "A" * 64), ("sha256", "g" * 64), ("sha256", "a" * 63)],
)
def test_bad_checksums(algorithm: str, digest: str) -> None:
    with pytest.raises(InvalidScientificInput):
        Checksum(algorithm, digest)


def test_execution_is_not_scientific_validity() -> None:
    status = ScientificStatus(
        ExecutionStatus.SUCCEEDED,
        ScientificValidity.UNDETERMINED,
        DataCompleteness.MISSING,
        "synthetic:assessment",
    )
    assert ScientificStatus.from_json(status.to_json()) == status
    assert status.execution is ExecutionStatus.SUCCEEDED
    assert status.validity is not ScientificValidity.VALID_WITHIN_SCOPE
    with pytest.raises(InvalidScientificInput):
        replace(status, validity=ScientificValidity.VALID_WITHIN_SCOPE)
    complete = replace(
        status, completeness=DataCompleteness.COMPLETE, validity=ScientificValidity.NOT_ASSESSED
    )
    assert complete.validity is ScientificValidity.NOT_ASSESSED


@pytest.mark.parametrize(
    "text",
    [
        "{}",
        '{"unknown":1}',
        "[]",
        "null",
        "invalid",
        '{"algorithm":"sha256","algorithm":"sha256","digest":"' + "a" * 64 + '"}',
    ],
)
def test_strict_json_schema(text: str) -> None:
    with pytest.raises(InvalidScientificInput):
        Checksum.from_json(text)


def test_all_records_have_json_compatible_values() -> None:
    records: list[Record] = [
        configuration(),
        configuration().interval,
        configuration().observer,
        coordinates(),
    ]
    for record in records:
        assert json.loads(record.to_json()) == record.to_dict()
        assert type(record).from_dict(record.to_dict()) == record


@pytest.mark.parametrize(
    "error,base",
    [
        (UnsupportedCoordinateConvention, InvalidScientificInput),
        (IncompleteScientificCoverage, MissingScientificData),
        (UnsupportedTemporalCoverage, IncompleteScientificCoverage),
        (NumericalConvergenceFailure, ScientificComputationFailure),
    ],
)
def test_exception_hierarchy(error: type[Exception], base: type[Exception]) -> None:
    with pytest.raises(base, match="synthetic failure"):
        raise error("synthetic failure")


def test_floating_point_longitude_edge_and_signed_zero() -> None:
    assert 0 <= coordinates(longitude_deg=-1e-100).longitude_deg < 360
    assert (
        coordinates(latitude_deg=-0.0, longitude_deg=-0.0).to_json()
        == coordinates(latitude_deg=0.0, longitude_deg=0.0).to_json()
    )


@pytest.mark.parametrize(
    "field", ["coordinates", "height_reference", "vertical_direction", "reference_id"]
)
def test_observer_rejects_missing_semantics(field: str) -> None:
    serialized = configuration().observer.to_dict()
    serialized[field] = None
    with pytest.raises(InvalidScientificInput):
        Observer.from_dict(serialized)


def test_status_rejects_invalid_consistency_and_empty_assessment() -> None:
    with pytest.raises(InvalidScientificInput):
        ScientificStatus(
            ExecutionStatus.RUNNING,
            ScientificValidity.VALID_WITHIN_SCOPE,
            DataCompleteness.COMPLETE,
            "synthetic:assessment",
        )
    with pytest.raises(InvalidScientificInput):
        ScientificStatus(
            ExecutionStatus.SUCCEEDED, ScientificValidity.NOT_ASSESSED, DataCompleteness.UNKNOWN, ""
        )


def test_serialization_rejects_nested_unknown_fields_and_nonfinite() -> None:
    config = configuration().to_dict()
    observer = config["observer"]
    assert isinstance(observer, dict)
    observer["unknown"] = True
    with pytest.raises(InvalidScientificInput):
        ScientificConfiguration.from_dict(config)
    payload = coordinates().to_json().replace('"latitude_deg":-89.0', '"latitude_deg":NaN')
    with pytest.raises(InvalidScientificInput):
        LunarCoordinates.from_json(payload)
