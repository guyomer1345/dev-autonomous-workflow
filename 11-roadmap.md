# 11 — Roadmap (what's left to build)

Living map of remaining work after the orchestrator foundation landed (sessions through 2026-06-30). The
six-space design lives in `00`–`10`; this doc tracks **status + sequence**, not new design. Update as items close.

## Done / proven
- **Space 1 — Orchestrator.** Root-`CLAUDE.md` driver, the loop spine (`.workflow/loop.md`), the
  read→place→advance control algorithm, the resume model (`state.json` / `handoff.md` / git), and the
  autonomous **permission model** (broad-allow + `ask` outward + `guard.sh` hook) — all **dogfood-validated**
  end-to-end (happy + fail/decision paths), **zero local prompts** after workspace trust (D46–D58).
- **Space 2 — Roster + contracts.** 17 skills + 2 agents, I/O schemas, hub-and-spoke topology (D24–D34, D53).
- **Space 5 — Disk layout.** `.workflow/` tree + per-item / `state.json` / `handoff.md` schemas (D53).

## Remaining — core to a credible v1 (no website needed)
1. **Skill behaviors — the D36–D45 deltas (Space 2).** Bodies are still v1; author the decided behaviors:
   **waves** (D36), **execute divergence tiers** (D37), **decision-coverage gate** (D43),
   **conjunction-of-signals** (D45), **document freshness/prune** (D41). The engine is correct but
   single-lane and literal until these land.
2. **`rules/` baseline + `/start` enforcement wiring (D40, Space 2).** Per-project lint/test/CI/hook gates,
   nearest-file-wins — what makes output *disciplined*, not just working. Not authored.
3. **Knowledge generation (Space 6).** The **generated** code-map (D39) the loop reads; `document` writes
   `.knowledge` semi-by-hand today. `planner` / `debug` depend on it, and brownfield ingest builds on it.
4. **Retention & archival law (D41, Space 5/6).** Bound the **append-only** tier (`decisions/`, the Sessions
   stream, `backlog.md`) — rollup + git-as-cold-store + a staleness/prune mechanism. **← next chat.**
5. **Unified docs-root layout (Space 5/6 — open in `05`/`07`).** Draw the top-level box: whether `spec/` +
   `.knowledge/` + the inline-C4 architecture doc unify under one `docs/` root, and whether that root sits at
   the launch root or under `<project_root>` (D49). The `/diagrams`-folder question is already settled (inline
   Mermaid-C4, D41 — a standalone `diagrams/` was rejected). Every greenfield scaffold + brownfield ingest
   converts a project to this layout. **← next chat (same doc surface as retention).**

## Remaining — important, stageable
- **Checkpoint triggers + MVP help (Space 4).** Conversational checkpoints work; demo/setup trigger rules and
  which help features are MVP are still open (the richer ones need the bus).
- **True-overnight reset (Space 1).** MVP = human-prompted `/clear` + restart from `handoff.md`; fully
  unattended overnight needs the optional **SDK runner** (deferred in principle).
- **Waves coordination (Space 1/2).** `build-once-per-wave` + the collision **independence test**. Only bites
  once agents run in parallel; single-stream works without it.

## Deferred (explicitly later)
- **Website + comms bus (Space 3 + 5).** Design not closed (screens/windows). For a present human, checkpoints
  already work conversationally; the bus enables away-from-terminal monitoring/approval **and** the airtight
  outward-gate (the chaining / full-bypass checkpoint-queue, see `07`).
- **Model/effort routing (Space 1).**
- **Packaging/distribution.** Plugin packaging, templates' home, `shared/` resolution, first-launch trust-UX
  doc (D57/D58).

## Recommended sequence
1. **Next chat:** retention & archival law (D41) **+** the `document`/knowledge freshness delta **+** the
   **unified docs-root layout** — one coherent pass on the same doc surface (`document` *owns* the prune; the
   Sessions stream is what retention bounds; the docs-root is the box around `spec/` + `.knowledge/` + the
   architecture doc).
2. The rest of the **D36–D45 skill deltas** (waves, divergence tiers, coverage/conjunction gates).
3. **`rules/` baseline + `/start` enforcement wiring** (D40).
4. **Knowledge generation** (Space 6) → then brownfield **ingest**.
5. Waves coordination; the true-overnight runner.
6. **Website + bus** (design-first), model/effort routing, packaging.

## The one-liner
The engine **drives**; it is not yet **disciplined** (skill deltas + `rules/`) or **self-maintaining**
(retention + knowledge-generation). Those four close the foundation; everything else is enhancement.
