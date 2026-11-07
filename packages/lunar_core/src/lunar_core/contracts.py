"""Immutable scientific input records; no astronomical or terrain computation."""

from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import dataclass, fields
from datetime import UTC, datetime
from enum import StrEnum
from typing import ClassVar, Self, cast, get_args, get_origin, get_type_hints

from lunar_core.errors import InvalidScientificInput, UnsupportedCoordinateConvention


def _number(value: object, name: str) -> float:
    if type(value) not in (int, float):
        raise InvalidScientificInput(f"{name} must be a finite int or float, not bool")
    try:
        result = float(cast(int | float, value))
    except OverflowError as exc:
        raise InvalidScientificInput(f"{name} must be finite") from exc
    if not math.isfinite(result):
        raise InvalidScientificInput(f"{name} must be finite")
    return 0.0 if result == 0 else result


def _text(value: object, name: str) -> None:
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise InvalidScientificInput(f"{name} must be nonempty text without surrounding whitespace")


def _encode(value: object) -> object:
    if isinstance(value, Record):
        return value.to_dict()
    if isinstance(value, StrEnum):
        return value.value
    if isinstance(value, datetime):
        return value.isoformat().replace("+00:00", "Z")
    if isinstance(value, tuple):
        return [_encode(item) for item in value]
    return value


def _decode(expected: object, value: object) -> object:
    if isinstance(expected, type) and issubclass(expected, Record):
        return expected.from_dict(value)
    if isinstance(expected, type) and issubclass(expected, StrEnum):
        try:
            return expected(cast(str, value))
        except (ValueError, TypeError) as exc:
            error = (
                UnsupportedCoordinateConvention
                if expected in (LunarFrame, LatitudeConvention, LongitudeConvention)
                else InvalidScientificInput
            )
            raise error(f"Unsupported {expected.__name__}: {value!r}") from exc
    if expected is datetime:
        if not isinstance(value, str) or not re.fullmatch(
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-](?:[01]\d|2[0-3]):[0-5]\d)",
            value,
        ):
            raise InvalidScientificInput("UTC timestamp must be ISO 8601 with seconds and offset")
        try:
            if value.endswith("-00:00"):
                raise ValueError("Unknown UTC offset is unsupported")
            return datetime.fromisoformat(value)
        except ValueError as exc:
            raise InvalidScientificInput("Invalid or unsupported UTC timestamp") from exc
    if get_origin(expected) is tuple:
        if not isinstance(value, list):
            raise InvalidScientificInput("Serialized collections must be JSON arrays")
        return tuple(_decode(get_args(expected)[0], item) for item in value)
    return value


@dataclass(frozen=True, slots=True)
class Record:
    """Strict JSON records. Constructor calls require typed enums/nested records."""

    schema_version: ClassVar[int] = 1

    def __post_init__(self) -> None:
        hints = get_type_hints(type(self))
        for field in fields(self):
            expected, value = hints[field.name], getattr(self, field.name)
            if expected is float:
                object.__setattr__(self, field.name, _number(value, field.name))
            elif expected is str:
                _text(value, field.name)
            elif get_origin(expected) is tuple:
                item_type = get_args(expected)[0]
                if type(value) is not tuple or any(type(item) is not item_type for item in value):
                    raise InvalidScientificInput(
                        f"{field.name} must be a tuple of {item_type.__name__}"
                    )
            elif not isinstance(value, expected):
                error = (
                    UnsupportedCoordinateConvention
                    if expected in (LunarFrame, LatitudeConvention, LongitudeConvention)
                    else InvalidScientificInput
                )
                raise error(f"{field.name} must be {expected.__name__}")

    def to_dict(self) -> dict[str, object]:
        return {field.name: _encode(getattr(self, field.name)) for field in fields(self)}

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"), allow_nan=False)

    @classmethod
    def from_dict(cls, value: object) -> Self:
        if not isinstance(value, dict) or set(value) != {field.name for field in fields(cls)}:
            raise InvalidScientificInput(f"{cls.__name__} requires exactly its declared fields")
        hints = get_type_hints(cls)
        return cls(**{name: _decode(hints[name], item) for name, item in value.items()})

    @classmethod
    def from_json(cls, value: str) -> Self:
        def unique(pairs: list[tuple[str, object]]) -> dict[str, object]:
            result: dict[str, object] = {}
            for key, item in pairs:
                if key in result:
                    raise InvalidScientificInput(f"Duplicate JSON key: {key}")
                result[key] = item
            return result

        try:
            data = json.loads(value, object_pairs_hook=unique)
        except (ValueError, TypeError, RecursionError) as exc:
            raise InvalidScientificInput("Invalid scientific JSON record") from exc
        return cls.from_dict(data)


class LunarFrame(StrEnum):
    """Frame families only; kernel realization is not established by these labels."""

    MOON_ME = "MOON_ME"
    MOON_PA = "MOON_PA"


class LatitudeConvention(StrEnum):
    PLANETOCENTRIC = "planetocentric"


class LongitudeConvention(StrEnum):
    EAST_POSITIVE = "east_positive"


@dataclass(frozen=True, slots=True)
class LunarCoordinates(Record):
    latitude_deg: float
    longitude_deg: float
    frame: LunarFrame
    latitude_convention: LatitudeConvention
    longitude_convention: LongitudeConvention

    def __post_init__(self) -> None:
        Record.__post_init__(self)
        if not -90 <= self.latitude_deg <= 90:
            raise InvalidScientificInput("latitude_deg must be in [-90, 90]")
        longitude = self.longitude_deg % 360.0
        # At a pole longitude is a retained meridian label, not a unique position.
        object.__setattr__(
            self, "longitude_deg", 0.0 if longitude >= 360 or longitude == 0 else longitude
        )


class HeightReference(StrEnum):
    TERRAIN_RELATIVE = "terrain_relative"
    REFERENCE_SURFACE = "reference_surface"


class VerticalDirection(StrEnum):
    RADIAL = "radial"
    SURFACE_NORMAL = "surface_normal"


@dataclass(frozen=True, slots=True)
class Observer(Record):
    coordinates: LunarCoordinates
    height_m: float
    height_reference: HeightReference
    vertical_direction: VerticalDirection
    reference_id: str

    def __post_init__(self) -> None:
        Record.__post_init__(self)
        if self.height_reference is HeightReference.TERRAIN_RELATIVE and self.height_m < 0:
            raise InvalidScientificInput("terrain-relative height_m must be nonnegative")


class TimeScale(StrEnum):
    UTC = "UTC"


@dataclass(frozen=True, slots=True)
class UtcTimestamp(Record):
    value: datetime
    scale: TimeScale

    def __post_init__(self) -> None:
        Record.__post_init__(self)
        if self.value.tzinfo is None or self.value.utcoffset() is None:
            raise InvalidScientificInput("UTC timestamp requires a timezone-aware datetime")
        try:
            normalized = self.value.astimezone(UTC)
        except (OverflowError, ValueError) as exc:
            raise InvalidScientificInput("UTC timestamp is outside representable range") from exc
        object.__setattr__(self, "value", normalized)

    @classmethod
    def parse(cls, value: str) -> Self:
        return cls.from_dict({"value": value, "scale": "UTC"})


@dataclass(frozen=True, slots=True)
class UtcInterval(Record):
    start: UtcTimestamp
    end: UtcTimestamp

    def __post_init__(self) -> None:
        Record.__post_init__(self)
        if self.start.value >= self.end.value:
            raise InvalidScientificInput("UTC interval requires start strictly before end")


class SolarVisibility(StrEnum):
    CENTER = "center"
    ANY_DISC = "any_disc"
    FULL_DISC = "full_disc"
    FRACTIONAL_DISC = "fractional_disc"


class EarthVisibility(StrEnum):
    CENTER = "center"
    ANY_DISC = "any_disc"
    FULL_DISC = "full_disc"
    FRACTIONAL_DISC = "fractional_disc"


@dataclass(frozen=True, slots=True)
class ScientificConfiguration(Record):
    observer: Observer
    interval: UtcInterval
    angular_resolution_deg: float
    terrain_sampling_distance_m: float
    event_refinement_tolerance_s: float
    solar_visibility: SolarVisibility
    earth_visibility: EarthVisibility

    def __post_init__(self) -> None:
        Record.__post_init__(self)
        if not 0 < self.angular_resolution_deg <= 360:
            raise InvalidScientificInput("angular_resolution_deg must be in (0, 360]")
        if self.terrain_sampling_distance_m <= 0 or self.event_refinement_tolerance_s <= 0:
            raise InvalidScientificInput("sampling distance and event tolerance must be positive")

    def identity(self) -> Checksum:
        """Identity of this schema/configuration only, not a complete scientific cache key."""
        content = f"lunar_core.configuration.v{self.schema_version}:" + self.to_json()
        return Checksum("sha256", hashlib.sha256(content.encode("utf-8")).hexdigest())


@dataclass(frozen=True, slots=True)
class Checksum(Record):
    algorithm: str
    digest: str

    def __post_init__(self) -> None:
        Record.__post_init__(self)
        if self.algorithm != "sha256" or not re.fullmatch(r"[0-9a-f]{64}", self.digest):
            raise InvalidScientificInput("checksum requires sha256 and 64 lowercase hex digits")


@dataclass(frozen=True, slots=True)
class DatasetReference(Record):
    identifier: str
    version: str
    source_reference: str
    checksum: Checksum


@dataclass(frozen=True, slots=True)
class KernelReference(Record):
    identifier: str
    version: str
    source_reference: str
    checksum: Checksum
    role: str


@dataclass(frozen=True, slots=True)
class KernelManifest(Record):
    """Tuple order is intended load order, not verified SPICE coverage."""

    kernels: tuple[KernelReference, ...]

    def __post_init__(self) -> None:
        Record.__post_init__(self)
        if len({kernel.identifier for kernel in self.kernels}) != len(self.kernels):
            raise InvalidScientificInput("kernel identifiers must be unique in load order")


@dataclass(frozen=True, slots=True)
class Provenance(Record):
    datasets: tuple[DatasetReference, ...]
    kernels: KernelManifest
    algorithm_identifier: str
    algorithm_version: str
    code_revision: str
    configuration_identity: Checksum

    def __post_init__(self) -> None:
        Record.__post_init__(self)
        if not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", self.code_revision):
            raise InvalidScientificInput("code_revision must be a full lowercase Git object ID")
        if len({dataset.identifier for dataset in self.datasets}) != len(self.datasets):
            raise InvalidScientificInput("dataset identifiers must be unique")


class ExecutionStatus(StrEnum):
    NOT_STARTED = "not_started"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class ScientificValidity(StrEnum):
    NOT_ASSESSED = "not_assessed"
    VALID_WITHIN_SCOPE = "valid_within_scope"
    INVALID = "invalid"
    UNDETERMINED = "undetermined"


class DataCompleteness(StrEnum):
    UNKNOWN = "unknown"
    MISSING = "missing"
    INCOMPLETE = "incomplete"
    COMPLETE = "complete"


@dataclass(frozen=True, slots=True)
class ScientificStatus(Record):
    execution: ExecutionStatus
    validity: ScientificValidity
    completeness: DataCompleteness
    assessment_reference: str

    def __post_init__(self) -> None:
        Record.__post_init__(self)
        if self.validity is ScientificValidity.VALID_WITHIN_SCOPE and (
            self.execution is not ExecutionStatus.SUCCEEDED
            or self.completeness is not DataCompleteness.COMPLETE
        ):
            raise InvalidScientificInput(
                "valid-within-scope requires succeeded execution/complete data"
            )
