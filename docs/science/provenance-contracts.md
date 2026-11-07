# Provenance, status and failures

Public records are defined in `lunar_core.contracts`; typed exceptions in `lunar_core.errors`. All records are frozen/slotted; collections are immutable tuples. JSON collections are arrays and nested records are objects. `from_dict`/`from_json` validate exact fields and nested content; `to_json` uses sorted keys and rejects nonfinite numbers. Serialized schema changes require review; `Record.schema_version` is 1 and participates in configuration identity, but is not an extra JSON field.

## Provenance records

- `Checksum(algorithm, digest)`: only `sha256`, with exactly 64 lowercase hexadecimal digits. Validating its shape does not verify file bytes.
- `DatasetReference(identifier, version, source_reference, checksum)`: nonempty trimmed text identifiers/version/source; source may be a resolvable URL, DOI or other traceable reference. Existence, authenticity and source licensing are not verified.
- `KernelReference(identifier, version, source_reference, checksum, role)`: adds an explicit nonempty role label. No kernel names/roles or scientific coverage are fabricated or inferred.
- `KernelManifest(kernels)`: ordered tuple of kernel references with unique identifiers. Order records intended load order; it does not execute loading. Empty manifests mean no declared kernels, not complete coverage.
- `Provenance(datasets, kernels, algorithm_identifier, algorithm_version, code_revision, configuration_identity)`: unique dataset identifiers, explicit algorithm/version, full lowercase 40- or 64-digit Git object ID, and configuration checksum. A revision identifies a declared baseline; it does not attest to a clean checkout. This milestone does not inspect file bytes, dirty state, datasets, kernels or algorithm execution.

Frame/time/observer conventions and numerical settings reside in the serialized configuration; retain that payload alongside its hash. These records form the initial scientific input/provenance contract, not a complete retrieval manifest. Future acquisition workflows must add required size, date, attribution, product coverage and processing information from the [data policy](../../data/README.md), and verify checksums against bytes. No PDS4 or W3C PROV implementation is introduced.

## Independent status axes

`ScientificStatus` requires all three axes and a nonempty `assessment_reference` identifying the assessment or its absence/reason:

| Axis | Values |
| --- | --- |
| Execution | `not_started`, `running`, `succeeded`, `failed` |
| Scientific validity | `not_assessed`, `valid_within_scope`, `invalid`, `undetermined` |
| Data completeness | `unknown`, `missing`, `incomplete`, `complete` |

Succeeded execution does not imply valid science or complete data; complete data does not imply validity. `valid_within_scope` is structurally permitted only with succeeded execution and complete data, plus an assessment reference. This consistency rule does not authenticate evidence or certify accuracy. No result is assigned this status by core computation here. An externally prepared assessment needs scope-specific evidence/domain review before that claim is justified. Numerical convergence is distinct from input/physical uncertainty and does not remove model limitations.

Missing terrain/input evidence must never imply a clear horizon or favorable mission conditions. Future consumers must propagate explicit unknown/missing/incomplete states or fail clearly; do not convert them to zero obstruction or successful constraints.

## Exception hierarchy

`InvalidScientificInput(ValueError)` covers invalid inputs; `UnsupportedCoordinateConvention` specializes unsupported frame/convention labels. `MissingScientificData(RuntimeError)` covers absent inputs; `IncompleteScientificCoverage` specializes partial spatial/domain coverage, and `UnsupportedTemporalCoverage` specializes temporal coverage. `ScientificComputationFailure(RuntimeError)` covers computation failure; `NumericalConvergenceFailure` specializes failure to satisfy a declared numerical policy. These classes carry clear caller-supplied messages; no computation is implemented merely by defining its failure type.

See [ADR 0002](../adr/0002-scientific-contracts.md), [configuration](scientific-configuration.md) and [validation strategy](../validation/strategy.md).
