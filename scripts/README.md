# Scripts

`fetch_spice_kernels.py` explicitly acquires the reviewed Phase 2 manifest into ignored `data/kernels`, verifies bytes and fails on mismatched existing assets. It is never called by core or CI. See [SPICE integration](../docs/science/spice-integration.md). Shared check/install commands remain in the root Makefile.
