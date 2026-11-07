# Scientific data policy

No NASA terrain data or SPICE kernels were included or downloaded in Phase 0. Phase 2 adds a reviewed [NAIF manifest](manifests/spice-de440.json) and explicit acquisition script; kernel bytes stay ignored. NASA data must not be blindly committed: products can be very large, have specific usage/attribution requirements, change upstream, and depend on compatible frames, time coverage, and processing assumptions.

Future acquisitions must have a small text manifest under `manifests/` identifying the provider, exact product/version, canonical retrieval URL, retrieval date, applicable attribution/terms, byte size, and SHA-256 checksum. Record SPICE kernel roles/load order and time coverage, terrain reference frame, datum, units, resolution, and processing software/configuration as relevant. Never invent manifest values.

Verify downloaded bytes against the recorded checksum before use. Store raw assets in ignored `data/raw/`, processed assets in `data/processed/`, kernels in `data/kernels/`, and generated outputs in ignored `results/`. Preserve raw inputs; record transforms and checksums for derived inputs. Ignore rules are safeguards, not a substitute for reviewing `git status`.

Offline reproduction must use a documented local data bundle with verified checksums, pinned software, exact configuration, and no silent network fallback. Missing or mismatched assets must fail clearly. Phase 0 provides no downloader or bundle. Small text manifests and reviewed text synthetic fixtures may be committed; binary fixtures require an explicit size/provenance review and narrowly scoped ignore exceptions.
