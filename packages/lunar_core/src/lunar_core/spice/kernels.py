"""Verified local assets and exclusive ownership of the process-global SPICE pool."""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from threading import Lock, get_ident
from types import TracebackType
from typing import Self
from urllib.parse import urlsplit

import spiceypy as spice
from spiceypy.utils.exceptions import NotFoundError, SpiceyError

from lunar_core.contracts import Checksum, Record, UtcInterval
from lunar_core.errors import (
    InvalidScientificInput,
    MissingScientificData,
    ScientificComputationFailure,
)

_LOCK = Lock()


@dataclass(frozen=True, slots=True)
class KernelAsset(Record):
    identifier: str
    version: str
    role: str
    kernel_type: str
    source_url: str
    checksum: Checksum
    local_path: str
    byte_size: float
    coverage_note: str
    redistribution_note: str

    def __post_init__(self) -> None:
        Record.__post_init__(self)
        if self.kernel_type not in {"LSK", "SPK", "PCK", "FK"}:
            raise InvalidScientificInput("Unsupported kernel type; meta-kernels are not accepted")
        if urlsplit(self.source_url).scheme != "https" or not urlsplit(self.source_url).netloc:
            raise InvalidScientificInput("Kernel source must be an explicit HTTPS URL")
        if self.byte_size <= 0 or not self.byte_size.is_integer():
            raise InvalidScientificInput("Kernel byte size must be a positive integer")
        if Path(self.local_path).is_absolute() or ".." in Path(self.local_path).parts:
            raise InvalidScientificInput(
                "Kernel path must stay inside the supplied cache directory"
            )


@dataclass(frozen=True, slots=True)
class KernelBundle(Record):
    identifier: str
    assets: tuple[KernelAsset, ...]
    supported_interval: UtcInterval
    retrieval_date: str

    def __post_init__(self) -> None:
        Record.__post_init__(self)
        try:
            date.fromisoformat(self.retrieval_date)
        except ValueError as exc:
            raise InvalidScientificInput("retrieval_date must be an ISO date") from exc
        if not self.assets or len({a.local_path for a in self.assets}) != len(self.assets):
            raise InvalidScientificInput(
                "Bundle needs unique local asset paths in explicit load order"
            )
        if len({a.identifier for a in self.assets}) != len(self.assets):
            raise InvalidScientificInput("Kernel identifiers must be unique")

    def identity(self) -> Checksum:
        return Checksum("sha256", hashlib.sha256(self.to_json().encode()).hexdigest())

    def verify(self, cache: Path) -> tuple[Path, ...]:
        root = cache.resolve()
        paths = []
        for asset in self.assets:
            path = (root / asset.local_path).resolve()
            if not path.is_relative_to(root) or not path.is_file():
                raise MissingScientificData(f"Missing or out-of-cache kernel: {asset.local_path}")
            digest = hashlib.sha256()
            try:
                with path.open("rb") as stream:
                    for block in iter(lambda: stream.read(1024 * 1024), b""):
                        digest.update(block)
                size = path.stat().st_size
            except OSError as exc:
                raise MissingScientificData(f"Cannot read kernel: {asset.identifier}") from exc
            if size != asset.byte_size or digest.hexdigest() != asset.checksum.digest:
                raise MissingScientificData(f"Kernel size/checksum mismatch: {asset.identifier}")
            paths.append(path)
        return tuple(paths)


class KernelSession:
    """Own an initially empty pool in a dedicated single-threaded process.

    No unrelated SPICE caller is allowed during this context. The lock protects
    cooperating sessions only; it cannot police arbitrary external CSPICE calls.
    """

    def __init__(self, bundle: KernelBundle, cache: Path):
        self._bundle = bundle
        self._cache = cache
        self._active = False
        self._owner = (0, 0)

    @property
    def bundle(self) -> KernelBundle:
        return self._bundle

    def require_active(self) -> None:
        if not self._active or self._owner != (os.getpid(), get_ident()):
            raise ScientificComputationFailure(
                "SPICE session inactive or used from another thread/process"
            )

    def require_role(self, role: str) -> None:
        self.require_active()
        if not any(asset.role == role for asset in self.bundle.assets):
            raise MissingScientificData(f"Required kernel role absent: {role}")

    def __enter__(self) -> Self:
        if not _LOCK.acquire(blocking=False):
            raise ScientificComputationFailure("Another SPICE session owns the process pool")
        owned = False
        try:
            try:
                variables = spice.gnpool("*", 0, 1)
                has_variables = len(variables) > 0
            except NotFoundError:
                has_variables = False
            if spice.ktotal("ALL") or has_variables:
                raise ScientificComputationFailure(
                    "Refusing to alter an existing SPICE kernel pool"
                )
            paths = self.bundle.verify(self._cache)
            owned = True
            for asset, path in zip(self.bundle.assets, paths, strict=True):
                architecture, kernel_type = spice.getfat(str(path))
                if kernel_type != asset.kernel_type:
                    raise InvalidScientificInput(f"Kernel type mismatch for {asset.identifier}")
                # Check the KPL header in addition to getfat classification.
                if architecture == "KPL":
                    header = path.read_text().splitlines()[0].strip()
                    if header != f"KPL/{asset.kernel_type}":
                        raise InvalidScientificInput(f"Kernel header mismatch: {asset.identifier}")
                spice.furnsh(str(path))
            self._owner = (os.getpid(), get_ident())
            self._active = True
            return self
        except BaseException as error:
            try:
                if owned:
                    spice.kclear()
            finally:
                _LOCK.release()
            if isinstance(error, SpiceyError):
                raise ScientificComputationFailure("SPICE kernel loading failed") from error
            raise

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.require_active()
        try:
            spice.kclear()  # Only our exclusively owned, initially empty pool.
        except SpiceyError as error:
            raise ScientificComputationFailure("Failed to clear owned SPICE pool") from error
        finally:
            self._active = False
            _LOCK.release()
