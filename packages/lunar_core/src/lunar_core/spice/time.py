"""UTC to ET boundary, with no hand-written leap-second arithmetic."""

import math
from dataclasses import dataclass

import spiceypy as spice
from spiceypy.utils.exceptions import SpiceyError

from lunar_core.contracts import Record, UtcTimestamp
from lunar_core.errors import (
    InvalidScientificInput,
    MissingScientificData,
    UnsupportedTemporalCoverage,
)
from lunar_core.spice.kernels import KernelSession


@dataclass(frozen=True, slots=True)
class EphemerisTime(Record):
    utc: UtcTimestamp
    et_tdb_seconds_past_j2000: float
    conversion: str


def utc_to_et(session: KernelSession, utc: UtcTimestamp) -> EphemerisTime:
    session.require_role("leapseconds")
    if not isinstance(utc, UtcTimestamp):
        raise InvalidScientificInput("Expected a UtcTimestamp")
    interval = session.bundle.supported_interval
    if not interval.start.value <= utc.value < interval.end.value:
        raise UnsupportedTemporalCoverage("UTC instant is outside declared bundle scope")
    calendar = spice.timdef("GET", "CALENDAR", 32)
    try:
        spice.timdef("SET", "CALENDAR", 32, "GREGORIAN")
        # Explicit UTC label avoids dependence on mutable SPICE time-system defaults.
        text = utc.value.strftime("%Y-%m-%d %H:%M:%S.%f") + " UTC"
        et = float(spice.str2et(text))
    except SpiceyError as exc:
        raise MissingScientificData("UTC conversion failed; verify the leap-second kernel") from exc
    finally:
        spice.timdef("SET", "CALENDAR", 32, calendar)
    if not math.isfinite(et):
        raise InvalidScientificInput("SPICE returned a nonfinite ephemeris time")
    return EphemerisTime(utc, et, "SPICE str2et; UTC to TDB seconds past J2000")
