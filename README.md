# Dev-Workflow Spec — working draft

**What this is:** the full specification for an autonomous, disciplined Claude-Code-native dev
workflow ("the disciplined builder"). **Spec-only — nothing here is implemented.**

**Status:** DRAFT (design started 2026-06-25). This folder is the source of truth — the spec lives and
is edited here directly. Five open items (below) remain to close before build.

> **Home:** `/mnt/c/Users/Guy Omer/Documents/dev-autonomous-workflow/` (permanent working directory).

## How it's organized
- `00-vision.md` — product thesis, goals, the master rule, MVP scope.
- `01-orchestrator.md` — Space 1: the spine (macro-loop, router role, memory model, session lifecycle).
- `02-agents.md` — Space 2: the persistent agent roster + I/O contracts.
- `03-website.md` — Space 3: local console (visualization + your channel to the orchestrator).
- `04-checkpoints.md` — Space 4: the manual human-test gate.
- `05-shared-state.md` — Space 5: the on-disk state + the local comms bus.
- `06-knowledge.md` — Space 6: the project knowledge base (code graph + per-file memory).
- `07-open-questions.md` — everything deliberately deferred.
- `08-decision-log.md` — every decision, why, what was rejected, and the evidence.
- `09-intake.md` — the intake stage of the spine: task types + contracts, the demo skill + sandbox gate,
  the commitment model. (Extends `01`.)
- `10-roster.md` — Space 2 v1: the full capability roster (skills + agents), loop order, call-graph;
  per-capability contracts live in the package files below.

Package source (Claude-Code-native, D25): `skills/<name>/SKILL.md`, `agents/<name>.md`,
`shared/schemas.md`. The repo is both the spec and the package being built.

## Status legend
- **[DECIDED]** — closed; rationale in the decision log.
- **[OPEN]** — needs to be closed before build.
- **[DEFERRED]** — known, intentionally not specced now (post-MVP or later).

## Still to close before build
1. Macro-loop control-flow — spine wired in `10`, interrupt model decided (pure queue, D26); remaining:
   how reset/handoff slots in (`01`) and the `init`/bootstrap capability (D28).
2. Website screen list (`03`).
3. Which checkpoint help-features are MVP (`04`) — the checkpoint data model is now in `shared/schemas.md`.
4. State/artifact disk paths (`05`) — package source layout is decided (D25).

Closed this session: the agent roster v1 (`10`), the intake stage (`09`).

## Home
Permanent home: `/mnt/c/Users/Guy Omer/Documents/dev-autonomous-workflow/` — the project's working
directory and source of truth. Specs are edited here directly.
