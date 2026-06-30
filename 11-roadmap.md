# 11 — Roadmap (what's left to build)

Living map of remaining work after the orchestrator + doc-surface foundations landed (sessions through
2026-06-30). The six-space design lives in `00`–`10`; this doc tracks **status + sequence**, not new design.
Each open item is tagged **[core]** (needed for a credible v1), **[stageable]** (real work, slot it in when it
pays off), or **[later]** (deliberately deferred). Update as items close.

## Done / proven
- **Space 1 — Orchestrator.** Root-`CLAUDE.md` driver, the `.workflow/loop.md` spine, the
  read→place→advance algorithm, the resume model (`state.json` / `handoff.md` / git), and the autonomous
  **permission model** (broad-allow + `ask` outward + `guard.sh`) — **dogfood-validated** end-to-end, zero
  local prompts after trust (D46–D58).
- **Space 2 — Roster + contracts.** 17 skills + 2 agents, I/O schemas, hub-and-spoke topology (D24–D34, D53).
- **Space 5 — Disk layout + retention.** `.workflow/` tree + schemas (D53); the **retention/read law**
  (cap-and-archive, D59–D61); the **unified `<project_root>/docs/` root** (D62).
- **Space 6 (partial) — Document freshness/prune.** `document` owns same-item freshness + the `audit` prune
  (D61); the knowledge *schema* is set (D38/D39).

## What's left — by space (every open thread)

### Space 1 — Orchestrator  *(core driver done)*
- **Waves coordination** — `build-once-per-wave` + the **collision independence test** (when two items can
  share a wave). Only bites once agents run in parallel. **[stageable]**
- **True-overnight reset** — MVP is human-prompted `/clear` + restart from `handoff.md`; unattended overnight
  needs the optional **SDK runner**. **[later]**
- **Model + effort routing** — per-task model/effort map (graph-maintenance cheap, planning expensive). **[later]**
- **Arbiter input contract** — decide a batch in dependency order vs one at a time. **[later]**

### Space 2 — Skills & agents  *(roster closed; bodies still v1)*
- **The D36–D45 skill-body deltas** — decided, not yet authored into the bodies: `prioritize` **waves** (D36);
  `execute` **divergence tiers** (D37) + refuse-destructive-without-backup (D42); `planner` **risk_class +
  backup** (D42) + **decision-coverage gate** (D43); `adjudicate` **conjunction-of-signals** (D45 →
  verify/debug/decision-engineer); `commit` **secret-scan** body (D44). **[core]**
- **`rules/` baseline + `/start` enforcement wiring** (D40) — per-project lint/test/CI/hook gates,
  nearest-file-wins. What makes output *disciplined*, not just working. Not authored. **[core]**
- **Engineer agent?** — a possible roster slot for a deep-implementation / feasibility agent (`02`/`09`). **[stageable]**

### Space 3 — Website / console + bus  *(role decided; unbuilt — NOT merely "later")*
- **C1 — read-only console** — render live loop state (roadmap, knowledge graph, activity, checkpoints) from
  files that already exist (`state.json`/`backlog`/`handoff`/`loop.md`/git). No bus needed → the quickest
  visible payoff. **[stageable, doable now]**
- **C2 — comms bus** (the local HTTP loopback, Space 5) — **on the critical path for unattended autonomy:** the
  dogfood showed every step self-drives *except* the blocking qa `checkpoint`, which needs the bus to deliver
  the human verdict away from the terminal; it also unblocks the airtight outward-gate (the `cd x && push`
  chaining-gap checkpoint-queue). **[core for unattended autonomy]**
- **Open design** — the screen list; the "contact the orchestrator" UX; stream-live vs snapshots; the
  stack. **[design-first]**

### Space 4 — Checkpoints & the demo skill
- **Demo skill mechanics** — `create-demo`'s *body* exists, but **how the sandbox is served/run, the
  refine-round limits, and where it lives on disk** are open (`09`). The product-alignment loop ("did we agree
  *what* to build") depends on it. **[core]**
- **Checkpoint data model + triggers** — finalize "what a checkpoint IS" (more examples), the **demo/setup
  triggers** (qa resolved via D30), and **which help features are MVP** (doc links / screenshots /
  screen-share / live feedback). **[stageable]** *(richer help needs the bus.)*
- **Engineering-feasibility pass** — the spike that de-risks the technical unknowns the demo deliberately
  skips (`09`). **[stageable]**
- **Automated testing · test-from-anywhere · paid device/QA platform** — designed-for, not built. **[later]**

### Space 5 — Shared state & bus
- **Read/write ownership per file + the request/response protocol** — the bus contract (couples with Space 3
  C2). **[core with C2]**
- **Outward-action permission mechanics** — standing pre-auth vs per-action, batching/queuing; the robust gate
  (beyond `ask` prefix-match) needs the bus checkpoint-queue (D35). **[stageable → core with bus]**
- **Symbol-level knowledge paths** — the seam left in Space-6 granularity. **[later]**

### Space 6 — Knowledge generation & ingest
- **Knowledge generation** — the **generated** code-map (D39, tree-sitter/repomap) the loop reads; today
  `document` writes `docs/knowledge/` semi-by-hand. `planner`/`debug` depend on it. **[core]**
- **Brownfield ingest** — build `docs/knowledge/` + a reconstructed `docs/spec/` from existing code; `/start`
  brownfield is a STUB until this exists. Builds on knowledge generation. **[core for brownfield]**
- **Retention script** — author the deterministic `audit` script (cap-and-archive, GC, prune) + tune
  `K`/thresholds; **Sessions distillation** deferred (D61). **[stageable]**
- **Graph regenerate-vs-incremental** — the mechanism for keeping the generated graph current. **[later]**

### Cross-cutting — packaging, validation, self-hosting
- **Packaging/distribution** — plugin packaging (`.claude-plugin/`), `shared/` resolution, first-launch
  **trust-UX doc** (D57/D58). **[stageable]**
- **Validation gaps** — real orchestrator→agent **dispatch** in a harness run; `@import`-survives-`/compact`;
  whether `verify` samples the real `git diff` vs trusts the `changelog` (#8). **[stageable]**
- **Commitment-status storage** — where locked/provisional/unspecified is recorded (spec vs node
  frontmatter, `09`). **[stageable]**
- **Project-state view (user-raised)** — a synthesized "where is this project" surface (done · how it
  connects · what's left); likely **generated** (a `status` skill / console screen). Prereq for
  **self-hosting** this project with itself. **[stageable]**
- **Framework version-update skill (user-raised)** — `/update` pulls the latest public-repo package +
  **migrates** schema/format changes (not a blind overwrite). Follow-on to packaging. **[stageable]**

## Recommended sequence — phased (user-set, 2026-06-30)
**Phase 1 — Close the foundations + guiding documents.** Finish the decided-but-unwritten core at the spec
level so the engine is *disciplined + knowledge-complete* before any UI: the **D36–D45 skill-body deltas**,
the **`rules/` baseline + `/start` enforcement wiring** (D40), **knowledge generation** → **brownfield
ingest**, the **retention script** (D61), and a coherence/completeness pass tying up the remaining `[core]`
guiding-doc loose ends. *(Next chat starts here — first item: the D36–D45 skill-body deltas.)*
**Phase 2 — Define the website + demo (design, not build).** Close the Space-3 and Space-4 *design* questions
as a complete spec: the website screen list / contact-UX / stream-vs-snapshot / stack, **and** the demo skill
mechanics (serving/running the sandbox, refine limits, on-disk location) + the checkpoint data model /
triggers.
**Phase 3 — Build the website** (C1 console → C2 bus).
**Phase 4 — Build the demo.**
Everything `[stageable]`/`[later]` — waves coordination, the SDK overnight runner, model/effort routing,
packaging, the state-view, the version-update skill — slots around these phases as it pays off.

## The one-liner
The engine **drives** and is now **self-maintaining** (retention + freshness + docs-root). What's left is to
make it **disciplined** (the skill deltas + `rules/`), **knowledge-complete** (generation → ingest),
**visible** (the console + bus), and **alignment-ready** (the demo + checkpoint mechanics). The bus is the one
"enhancement" that's actually on the critical path for *unattended* autonomy — not merely later.
