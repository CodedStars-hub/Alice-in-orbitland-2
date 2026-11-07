"""Radial spherical observer and analytically defined local tangent basis."""

import math
from dataclasses import dataclass

from lunar_core.contracts import HeightReference, Observer, Record, VerticalDirection
from lunar_core.errors import InvalidScientificInput, MissingScientificData

REFERENCE_ID = "naif:pck00011:BODY301_RADII:sphere"
RADIUS_KM = 1737.4


@dataclass(frozen=True, slots=True)
class Vector3(Record):
    x: float
    y: float
    z: float

    def dot(self, other: "Vector3") -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z


@dataclass(frozen=True, slots=True)
class LocalBasis(Record):
    north: Vector3
    east: Vector3
    up: Vector3

    def __post_init__(self) -> None:
        Record.__post_init__(self)
        axes = (self.north, self.east, self.up)
        for i, first in enumerate(axes):
            for j, second in enumerate(axes):
                if abs(first.dot(second) - (1 if i == j else 0)) > 1e-12:
                    raise InvalidScientificInput("Local basis must be orthonormal within 1e-12")


def local_basis(latitude_deg: float, longitude_deg: float) -> LocalBasis:
    # Reuse coordinate validation at the caller boundary; this helper validates too.
    if type(latitude_deg) not in (float, int) or type(longitude_deg) not in (float, int):
        raise InvalidScientificInput("Local basis requires finite numeric degrees")
    try:
        latitude_deg, longitude_deg = float(latitude_deg), float(longitude_deg)
    except OverflowError as exc:
        raise InvalidScientificInput("Local basis degrees overflow floating-point range") from exc
    if not math.isfinite(latitude_deg) or not math.isfinite(longitude_deg):
        raise InvalidScientificInput("Local basis requires finite numeric degrees")
    if not -90 < latitude_deg < 90:
        raise InvalidScientificInput("Local north/east is undefined at exact poles")
    lat, lon = math.radians(latitude_deg), math.radians(longitude_deg % 360)
    a, b, c, d = math.sin(lat), math.cos(lat), math.sin(lon), math.cos(lon)
    return LocalBasis(Vector3(-a * d, -a * c, b), Vector3(-c, d, 0), Vector3(b * d, b * c, a))


def observer_position(observer: Observer) -> Vector3:
    if not isinstance(observer, Observer):
        raise InvalidScientificInput("Expected a validated Observer")
    if observer.height_reference is HeightReference.TERRAIN_RELATIVE:
        raise MissingScientificData(
            "Terrain-relative observer requires terrain elevation; not available"
        )
    if (
        observer.reference_id != REFERENCE_ID
        or observer.vertical_direction is not VerticalDirection.RADIAL
    ):
        raise InvalidScientificInput(
            "Only radial height above the named pck00011 sphere is supported"
        )
    radius = RADIUS_KM + observer.height_m / 1000.0
    if radius <= 0:
        raise InvalidScientificInput("Observer radius must be positive")
    basis = local_basis(observer.coordinates.latitude_deg, observer.coordinates.longitude_deg)
    return Vector3(radius * basis.up.x, radius * basis.up.y, radius * basis.up.z)


@dataclass(frozen=True, slots=True)
class LocalAngles(Record):
    azimuth_deg: float
    elevation_deg: float
    range_km: float

    def __post_init__(self) -> None:
        Record.__post_init__(self)
        if not 0 <= self.azimuth_deg < 360 or not -90 <= self.elevation_deg <= 90:
            raise InvalidScientificInput("Angles outside azimuth/elevation ranges")
        if self.range_km <= 0:
            raise InvalidScientificInput("Range must be positive")


def local_angles(vector: Vector3, basis: LocalBasis) -> LocalAngles:
    norm = math.hypot(vector.x, vector.y, vector.z)
    if norm == 0 or not math.isfinite(norm):
        raise InvalidScientificInput("Target vector must have finite nonzero norm")
    unit = Vector3(vector.x / norm, vector.y / norm, vector.z / norm)
    n, e, u = unit.dot(basis.north), unit.dot(basis.east), unit.dot(basis.up)
    horizontal = math.hypot(n, e)
    if horizontal <= 1e-14:
        raise InvalidScientificInput(
            "Azimuth undefined at numerical zenith/nadir (horizontal <= 1e-14)"
        )
    azimuth = math.degrees(math.atan2(e, n)) % 360
    return LocalAngles(
        0.0 if azimuth >= 360 else azimuth, math.degrees(math.atan2(u, horizontal)), norm
    )
