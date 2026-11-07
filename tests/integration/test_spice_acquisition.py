"""Explicit acquisition script must fail on existing corrupt bytes, without network."""

import hashlib
import runpy
from pathlib import Path
from types import FunctionType

import pytest
from lunar_core.contracts import Checksum, UtcInterval, UtcTimestamp
from lunar_core.spice.kernels import KernelAsset, KernelBundle


def test_existing_assets_are_verified_and_never_overwritten(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    namespace = runpy.run_path(
        str(Path(__file__).resolve().parents[2] / "scripts/fetch_spice_kernels.py")
    )
    main = namespace["main"]
    assert isinstance(main, FunctionType)
    monkeypatch.setitem(
        main.__globals__, "__file__", str(tmp_path / "scripts/fetch_spice_kernels.py")
    )
    cache = tmp_path / "data/kernels"
    cache.mkdir(parents=True)
    path = cache / "synthetic.tf"
    path.write_text("KPL/FK\n")
    asset = KernelAsset(
        "synthetic",
        "test",
        "synthetic",
        "FK",
        "https://example.invalid/no-network",
        Checksum("sha256", hashlib.sha256(path.read_bytes()).hexdigest()),
        path.name,
        path.stat().st_size,
        "synthetic",
        "test-only",
    )
    bundle = KernelBundle(
        "synthetic",
        (asset,),
        UtcInterval(
            UtcTimestamp.parse("2000-01-01T00:00:00Z"), UtcTimestamp.parse("2025-01-01T00:00:00Z")
        ),
        "2026-11-07",
    )
    manifest = tmp_path / "data/manifests/spice-de440.json"
    manifest.parent.mkdir()
    manifest.write_text(bundle.to_json())
    main()  # Existing correct bytes require no network.
    path.write_text("corrupt")
    with pytest.raises(ValueError, match="Existing asset mismatch"):
        main()
    assert path.read_text() == "corrupt"
    path.unlink()
    with pytest.raises(ValueError, match="Only reviewed NAIF"):
        main()
