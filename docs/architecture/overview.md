# Architecture overview

The monorepo keeps contracts and review history together while preserving installable component boundaries. One Python 3.12 development environment installs two src-layout distributions; npm workspaces manage the web app with one root lockfile. Root Python configuration and Make targets avoid duplicated quality settings.

Dependency direction is web → versioned HTTP API → lunar_core. The frontend currently renders only a placeholder. The API owns transport and environment configuration. Core owns future scientific domain behavior and has no runtime dependencies yet. It must never import FastAPI, UI code, or application configuration. Integration tests exercise installed boundaries; component tests belong beside their component.

Implemented: `/api/v1/health`, explicit configurable CORS, core import/version metadata, placeholder page, and tooling. No scientific endpoint, data loader, persistent store, scheduler, or distributed service exists.

Planned only: scientific contracts for units/frames/time, SPICE ephemeris adapters, terrain ingestion, local horizon construction, sunlight and Earth visibility geometry, temporal windows, mission constraints, and comparison/optimization. These are future responsibilities, not scaffolded pseudo-implementations. Provenance and validation must accompany their design. The core should remain usable offline without an HTTP server. API schemas must distinguish missing/unsupported results from computed values.
