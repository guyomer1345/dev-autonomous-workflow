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
4. **Retention & archival law (D41) — DESIGN CLOSED (D59–D61).** Layer 0 write-law leak closures (D59–D60) +
   Layer 1 **cap-and-archive** read law (D61): the append-only tier is bounded (last-*K* on disk, rest in git),
   enforced by a deterministic `audit` script `prioritize` injects on a threshold. Build slivers remaining:
   **author the retention script** + `K`/threshold tuning; **Sessions distillation** deferred.
5. **Unified docs-root layout (Space 5/6) — DONE (D62).** `spec/` + `architecture.md` + `knowledge/` +
   `decisions/` unify under **`<project_root>/docs/`** (both modes; `.workflow/` stays at the launch root); a
   thin `llms.txt` sits at the project root. Greenfield scaffolds it; brownfield adopts-and-merges into an
   existing `docs/`.

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
- **Project-state view (user-raised).** No single synthesized "where is this project" surface (done · how it
  connects · what's left); data is scattered across `00–11`/`08`/`backlog`/`.knowledge`. Likely a *generated*
  view (a `status` skill / console screen). Prereq for **self-hosting** (driving this project with itself). → `07`.
- **Framework version-update skill (user-raised).** The package is a public repo; consuming projects install a
  snapshot that goes stale. An `/update` skill that pulls latest + **migrates** schema/format changes (not a
  blind overwrite). Follow-on to packaging (D57). → `07`.

## Recommended sequence
1. **Retention + freshness + docs-root — DONE** (D59–D62). Cap-and-archive retention (D61); docs-root unified
   under `<project_root>/docs/` (D62). This closes the whole doc-surface pass.
2. The rest of the **D36–D45 skill deltas** (waves, divergence tiers, coverage/conjunction gates).
3. **`rules/` baseline + `/start` enforcement wiring** (D40).
4. **Knowledge generation** (Space 6) → then brownfield **ingest**.
5. Waves coordination; the true-overnight runner.
6. **Website + bus** (design-first), model/effort routing, packaging.

## The one-liner
The engine **drives**; it is not yet **disciplined** (skill deltas + `rules/`) or **self-maintaining**
(retention + knowledge-generation). Those four close the foundation; everything else is enhancement.
