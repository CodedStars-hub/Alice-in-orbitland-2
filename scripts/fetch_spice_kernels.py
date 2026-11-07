"""Explicit acquisition of the reviewed manifest; never called by core or CI.

Run with .venv/bin/python scripts/fetch_spice_kernels.py. Existing mismatched
files fail instead of being overwritten. Files remain in ignored data/kernels.
"""

import hashlib
import os
import tempfile
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import urlopen

from lunar_core.spice.kernels import KernelBundle


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    bundle = KernelBundle.from_json((root / "data/manifests/spice-de440.json").read_text())
    cache = root / "data/kernels"
    cache.mkdir(parents=True, exist_ok=True)
    for asset in bundle.assets:
        target = cache / asset.local_path
        if not target.resolve().is_relative_to(cache.resolve()):
            raise ValueError("Kernel path escapes cache")
        if target.exists():
            if (
                target.stat().st_size != asset.byte_size
                or hashlib.sha256(target.read_bytes()).hexdigest() != asset.checksum.digest
            ):
                raise ValueError(f"Existing asset mismatch; inspect manually: {target}")
            continue
        if urlsplit(asset.source_url).hostname != "naif.jpl.nasa.gov":
            raise ValueError("Only reviewed NAIF sources are allowed")
        descriptor, temporary = tempfile.mkstemp(dir=cache, prefix=".download-")
        try:
            digest = hashlib.sha256()
            size = 0
            with (
                os.fdopen(descriptor, "wb") as output,
                urlopen(asset.source_url, timeout=60) as response,
            ):
                if urlsplit(response.url).hostname != "naif.jpl.nasa.gov":
                    raise ValueError("Unexpected download redirect")
                while block := response.read(1024 * 1024):
                    output.write(block)
                    digest.update(block)
                    size += len(block)
            if size != asset.byte_size or digest.hexdigest() != asset.checksum.digest:
                raise ValueError(f"Downloaded asset mismatch: {asset.identifier}")
            # Link creation fails if another process created target; never overwrite it.
            os.link(temporary, target)
        finally:
            Path(temporary).unlink(missing_ok=True)
    bundle.verify(cache)
    print(f"Verified {len(bundle.assets)} kernels in {cache}; no calculation executed")


if __name__ == "__main__":
    main()
