# ADR 0002: Immutable scientific contracts

Status: accepted for the authorized Phase 1 implementation, subject to PR review; no physical validation claimed.

## Context

Phase 1 is authorized to define coordinates, observer/time/configuration/provenance/status and failures, but not SPICE, terrain or scientific algorithms. Research recommendations remain provisional outside the explicitly selected representation rules below. [ADR 0001](0001-monorepo-and-stack.md) requires an independently installable core free of API/UI dependencies.

## Decision

Use Python 3.12 frozen/slotted dataclasses, StrEnum and immutable tuples, without adding runtime dependencies. A small shared record codec checks declared types/fields, rejects unknown fields and duplicate JSON keys, and recursively serializes records. Public domain types live in `lunar_core.contracts`; errors live in `lunar_core.errors`; the record base is serialization plumbing, not a general modeling framework.

Select east-positive degrees, planetocentric latitude [-90, 90] and longitude [0, 360). Retain pole meridian labels without computing a tangent basis. Require a distinct symbolic MOON_ME or MOON_PA family, but do not select a kernel realization or implement transformations. Select neither a lunar reference shape nor a global vertical direction: require explicit height reference, vertical label and reference ID. Terrain-relative heights are nonnegative; reference-surface elevations may be signed.

Require timezone-aware UTC inputs, normalize offsets and serialize Z. Restrict parsing to documented ISO precision; reject leap-second labels rather than invent leap arithmetic. Intervals require strict order and denote [start, end). No ET representation/conversion or physical-duration operation is provided.

Require sampling units and settings with no numerical defaults. Represent Sun/Earth disc choices independently without calculating visibility. Separate execution, validity and completeness; require an assessment reference. Store declared dataset/kernel/version/checksum/algorithm/revision/configuration identity without pretending metadata validation verifies assets or science.

## Alternatives and consequences

Pydantic could provide richer validation but would add a runtime dependency to a currently dependency-free core; API's existing use does not justify coupling. Mutable dictionaries weaken invariants. Per-class hand-written codecs duplicate nested validation; the limited dataclass codec handles only the field kinds used here. Generic quantities/coordinate transformation frameworks, automatic kernel loading and speculative scientific abstractions are deferred.

Frozen records support ordinary immutability and deterministic serialization, not a security boundary. The public representation is version 1; changes need compatibility review. Hash identity is configuration-only and must not serve alone as a full scientific cache identity. Labeling frames/heights preserves intent but does not make an observer computable until compatible assets and realizations are verified.

## Verification and limitations

Tests cover invalid inputs, boundaries, polar labels, serialization, immutability, time parsing/ordering, settings, provenance, status distinctions and exception hierarchy. These are software contract checks, not numerical convergence, reference agreement or physical validation. No NASA datasets/kernels or fabricated outputs are included. SPICE/LOLA integration, algorithms, uncertainty propagation and mission evaluation remain future phases.

See [coordinates](../science/coordinate-contracts.md), [time](../science/time-contracts.md), [configuration](../science/scientific-configuration.md) and [provenance](../science/provenance-contracts.md) for exact semantics and constraints.
