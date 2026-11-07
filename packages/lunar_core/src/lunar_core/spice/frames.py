"""Explicit DE440 frame realizations, never an IAU_MOON fallback."""

import math

import spiceypy as spice
from spiceypy.utils.exceptions import SpiceyError

from lunar_core.contracts import LunarFrame
from lunar_core.errors import (
    InvalidScientificInput,
    UnsupportedCoordinateConvention,
    UnsupportedTemporalCoverage,
)
from lunar_core.spice.kernels import KernelSession

REALIZATIONS = {
    LunarFrame.MOON_ME: "MOON_ME_DE440_ME421",
    LunarFrame.MOON_PA: "MOON_PA_DE440",
}


def realized_frame(session: KernelSession, symbolic: LunarFrame, et: float) -> str:
    session.require_active()
    if not isinstance(symbolic, LunarFrame) or symbolic not in REALIZATIONS:
        raise UnsupportedCoordinateConvention(
            "Only explicit DE440 ME/PA realizations are supported"
        )
    if type(et) not in (int, float):
        raise InvalidScientificInput("ET must be a finite number of TDB seconds past J2000")
    try:
        finite = math.isfinite(et)
    except OverflowError:
        finite = False
    if not finite:
        raise InvalidScientificInput("ET must be finite")
    session.require_role("lunar_frames")
    session.require_role("lunar_orientation")
    name = REALIZATIONS[symbolic]
    try:
        # Resolving at the observation epoch also verifies orientation coverage.
        spice.pxform(name, "J2000", et)
    except SpiceyError as exc:
        raise UnsupportedTemporalCoverage(f"Frame unavailable at requested ET: {name}") from exc
    return name
