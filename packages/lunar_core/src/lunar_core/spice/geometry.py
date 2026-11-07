"""Uncorrected target-center vectors for a declared lunar surface observer."""

import hashlib
import re
from dataclasses import dataclass
from enum import StrEnum

import spiceypy as spice
from spiceypy.utils.exceptions import SpiceyError

from lunar_core.contracts import (
    Checksum,
    DataCompleteness,
    ExecutionStatus,
    Observer,
    Record,
    ScientificStatus,
    ScientificValidity,
    UtcTimestamp,
)
from lunar_core.errors import (
    InvalidScientificInput,
    MissingScientificData,
    UnsupportedTemporalCoverage,
)
from lunar_core.spice.frames import REALIZATIONS, realized_frame
from lunar_core.spice.kernels import KernelBundle, KernelSession
from lunar_core.spice.observer import (
    RADIUS_KM,
    REFERENCE_ID,
    LocalAngles,
    Vector3,
    local_angles,
    local_basis,
    observer_position,
)
from lunar_core.spice.time import EphemerisTime, utc_to_et


class Target(StrEnum):
    SUN = "10"
    EARTH = "399"


@dataclass(frozen=True, slots=True)
class GeometryResult(Record):
    observer: Observer
    observer_identity: Checksum
    target: Target
    time: EphemerisTime
    realized_frame: str
    vector_km: Vector3
    angles: LocalAngles
    aberration_correction: str
    reference_geometry: str
    kernel_manifest: KernelBundle
    kernel_identity: Checksum
    algorithm_version: str
    code_revision: str
    spiceypy_version: str
    toolkit_version: str
    status: ScientificStatus

    def __post_init__(self) -> None:
        Record.__post_init__(self)
        observer_hash = Checksum(
            "sha256", hashlib.sha256(self.observer.to_json().encode()).hexdigest()
        )
        if (
            self.observer_identity != observer_hash
            or self.kernel_identity != self.kernel_manifest.identity()
        ):
            raise InvalidScientificInput(
                "Geometry provenance identities do not match embedded inputs"
            )
        if self.realized_frame != REALIZATIONS[self.observer.coordinates.frame]:
            raise InvalidScientificInput(
                "Geometry frame does not match declared observer realization"
            )
        if self.aberration_correction != "NONE" or self.reference_geometry != REFERENCE_ID:
            raise InvalidScientificInput("Unsupported correction/reference geometry in result")
        if not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", self.code_revision):
            raise InvalidScientificInput("Geometry result requires a full lowercase code revision")


def target_geometry(
    session: KernelSession,
    observer: Observer,
    utc: UtcTimestamp,
    target: Target,
    *,
    code_revision: str,
) -> GeometryResult:
    if not isinstance(code_revision, str) or not re.fullmatch(
        r"(?:[0-9a-f]{40}|[0-9a-f]{64})", code_revision
    ):
        raise InvalidScientificInput("Supply the full lowercase code revision used for this run")
    if not isinstance(observer, Observer):
        raise InvalidScientificInput("Expected a validated Observer")
    if not isinstance(target, Target):
        raise InvalidScientificInput("Target must be Sun (10) or Earth center (399)")
    session.require_role("ephemeris")
    session.require_role("constants")
    time = utc_to_et(session, utc)
    frame = realized_frame(session, observer.coordinates.frame, time.et_tdb_seconds_past_j2000)
    position = observer_position(observer)
    try:
        radii = spice.bodvrd("MOON", "RADII", 3)[1]
        if any(float(r) != RADIUS_KM for r in radii):
            raise MissingScientificData("Loaded lunar radii do not match declared reference sphere")
        relative, _ = spice.spkpos(
            target.value, time.et_tdb_seconds_past_j2000, frame, "NONE", "301"
        )
    except SpiceyError as exc:
        raise UnsupportedTemporalCoverage("Target ephemeris/frame coverage unavailable") from exc
    vector = Vector3(
        float(relative[0]) - position.x,
        float(relative[1]) - position.y,
        float(relative[2]) - position.z,
    )
    angles = local_angles(
        vector, local_basis(observer.coordinates.latitude_deg, observer.coordinates.longitude_deg)
    )
    return GeometryResult(
        observer,
        Checksum("sha256", hashlib.sha256(observer.to_json().encode()).hexdigest()),
        target,
        time,
        frame,
        vector,
        angles,
        "NONE",
        REFERENCE_ID,
        session.bundle,
        session.bundle.identity(),
        "lunar_core.spice.geometry.v1",
        code_revision,
        spice.__version__,
        spice.tkvrsn("TOOLKIT"),
        ScientificStatus(
            ExecutionStatus.SUCCEEDED,
            ScientificValidity.NOT_ASSESSED,
            DataCompleteness.COMPLETE,
            "Geometric center direction only; no terrain, visibility or physical validation",
        ),
    )
