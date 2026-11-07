# Project context

This directory preserves project intent, supplied research, and implementation evidence. Start here when onboarding; it does not authorize the next development phase.

## Navigation and ownership

| Document | Purpose |
| --- | --- |
| [Project overview](PROJECT_OVERVIEW.md) | Users, objectives, workflows, MVP, and boundaries |
| [Research synthesis](RESEARCH_SYNTHESIS.md) | RC-01–RC-15, implications, and validation gaps |
| [Scientific decisions](SCIENTIFIC_DECISIONS.md) | Status-bearing decision inventory |
| [Architecture guide](ARCHITECTURE_AND_DEPENDENCIES.md) | Actual components versus proposed scientific data flow |
| [Implementation status](IMPLEMENTATION_STATUS.md) | Revision-specific evidence and verification limits |
| [Development workflow](DEVELOPMENT_WORKFLOW.md) | Review and Git checkpoints |
| [Open questions](OPEN_QUESTIONS.md) | Decisions and experiments blocking future phases |

Canonical sources remain [AGENTS.md](../../AGENTS.md), [architecture](../architecture/overview.md), [ADR 0001](../adr/0001-monorepo-and-stack.md), [modeling principles](../science/modeling-principles.md), [validation strategy](../validation/strategy.md), [data policy](../../data/README.md), [contributing](../../CONTRIBUTING.md), and the [roadmap](../development/roadmap.md). This directory links those policies rather than replacing them. Record future accepted architectural decisions in ADRs and update this index/ledger to point to them.

## Evidence register

- **R1 — Supplied research summary:** user-provided “Lunar Navigator — Prompt 00B: Persistent Research Knowledge and Project Context”, received 2026-11-07. Its scientific content is preserved in this directory; it is research context, not independent literature verification.
- **B1 — Supplied onboarding brief:** “LUNAR NAVIGATOR — MASTER PROJECT ONBOARDING, RESEARCH CONSOLIDATION & REPOSITORY AUDIT”, received 2026-11-07. Establishes vision, RC numbering, and the earlier 0–14 roadmap.
- **L1 — Inspected implementation:** local bootstrap revision `c582d144ce5f31de79d55af3ff2e5faed765b9fe`, plus the documentation changes described here. Source files and canonical documents are directly inspectable.
- **V1 — Local verification:** commands and limits recorded in [implementation status](IMPLEMENTATION_STATUS.md). Software checks are not scientific validation.
- **H1 — Historical conversation:** [shared ChatGPT link](https://chatgpt.com/share/6aef572d-3ad4-83ee-9b74-e758f5a31c2a), inaccessible during onboarding. No conclusions are attributed to direct inspection of it.
- **G1 — Repository:** [GitHub repository](https://github.com/CodedStars-hub/Alice-in-orbitland-2). During this milestone, `git ls-remote origin refs/heads/main` confirmed the remote main revision matched L1. Live source/PR/Actions inspection was not performed.

No scientific publication or NASA/NAIF/PDS technical reference was accessed and verified for this documentation milestone. Provider and tool names below identify research directions, not verified citations or finalized asset selections. The official challenge page search summary was visible during onboarding, but its full content was inaccessible; detailed requirements still require review.

## Evidence classification

Use exactly these decision statuses: **Accepted and implemented**, **Accepted but not implemented**, **Provisional research recommendation**, **Deferred**, **Unresolved**, **Empirically validated**. Status describes the stated decision's scope, not every related feature. “Empirically validated” requires linked evidence, conditions, and tolerances; no scientific decision currently has that status. A research recommendation remains provisional until explicitly accepted.
