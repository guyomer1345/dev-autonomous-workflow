# 07 — Open Questions Register

Deliberately deferred — known unknowns, to close during build or later.

## Must close before build
- **Rest of the macro-loop** — **CLOSED**: the spine lives in `10` + renders as `.workflow/loop.md` (D47);
  the **orchestrator `CLAUDE.md` driver** is specced in `01` (D46); checkpoint = `04`, reset = the
  handoff/resume model (D48). *Intake stage closed in `09`.*
- **Intake follow-ons** (`09`) — engineering-feasibility pass; demo-skill mechanics (serving,
  refine-round limits, on-disk location); commitment-status storage (spec doc vs Space 6 node frontmatter).
  *(Interrupt model closed: pure queue, D26.)*
- **`init` / bootstrap capability** (`10`, D28) — greenfield is straightforward; brownfield **ingest**
  (build the knowledge base + reconstructed spec from existing code) depends on Space-6 ingest mechanics.
- **Commit-message convention** — **CLOSED (D32):** Conventional Commits + `Refs:`/`Closes:` trailers.
  Remaining sliver: whether the workflow's own generated commits carry the `Co-Authored-By` trailer.
- **Agent roster v1** — **CLOSED in `10`** (names, I/O contracts, skill-vs-agent, topology). Remaining
  sliver: the collision-model **independence test** (`02`) — waves decided the grouping (D36); the
  `prioritize` interrupt model is closed (pure queue, D26).
- **What a checkpoint is** (`04`) — data model now in `shared/schemas.md` (demo/qa/setup + verdict).
  Remaining: which help features are MVP.
- **Outward-action permission model** (`04`, D35) — mechanics of the local-autonomous / outward-gated
  boundary: per-action checkpoint vs standing pre-authorization (config allowlist), batching/queuing of
  pending outward actions, and whether this is a new checkpoint kind (`publish`) or a flavour of the
  existing gate. Affects `commit`'s deferred push, `create-issue` (`gh issue create`), `close-issue`
  (`gh issue close`). MVP-safe default = always-gated per-action; the open part is standing auth + batching.
  *Surfaced 2026-06-29 (live: the harness gated a push to `main`).*
- **Website screen list** (`03`).
- **Disk layout** (`05`) — the full file tree + protocols; the exact diagrams location (D41); and whether
  `spec/`+`.knowledge/` sit at the launch root or under `<project_root>` (D49).
- **Orchestrator hooks** (D58) — `hooks/guard.sh` now enforces **secret-scan** + **verify-before-commit**
  (hard blocks); **outward-action** gating is the settings `ask` rule (deliberate prompt). Still open:
  **build-once-per-wave** (a wave-coordinator, not a command gate); **outward gating under full bypass**; and
  the **command-chaining gap** — broad `Bash` allow + `ask` prefix-match misses `cd x && git push`, so the
  robust outward gate ultimately needs the guard-hook/bus checkpoint-queue, not just `ask` rules.
- **First-launch workspace trust** (D58) — the shipped `settings.json` + hooks are **ignored until the folder
  is trusted**, and the trust **dialog doesn't render in some terminals (e.g. WSL)**; `/start` + setup docs must
  give the manual `hasTrustDialogAccepted` flag method, not just "accept the dialog." (Validated: after trust,
  the dogfood run took **zero** local permission prompts.)
- **`@import`-survives-`/compact`** — a one-session test; if it re-resolves, the brownfield install (D50) can
  switch from the inline marked block to a cleaner `@import`.
- **Console + comms bus** (`03`/`05`) — the **critical-path runtime dependency**: the dogfood showed every
  step autonomy-drives *except* the blocking qa `checkpoint`, which needs the bus to deliver the human verdict.
- **Real dispatch validation** — the dogfood *simulated* the `research` agent dispatch; the orchestrator→agent
  call + structured return is validated in the harness-real run.
- **Package install** — loose `.claude/` files are MVP (D57); plugin packaging + `shared/` resolution open.
- **Adoption follow-ons (D38–D51)** — the **retention & archival law** for the append-only tier + the
  **prune-pass** mechanism + **staleness-detection** signal (D41/D51); whether `verify` samples the real
  `git diff` vs trusts the `changelog` (#8); authoring the thin baseline `rules/` + `/start` enforcement
  wiring (D40).

## Deferred (post-MVP or later)
- **Knowledge graph regenerate-vs-incremental** (`06`) — shape decided (D38/D41), mechanism deferred.
- **Model + effort routing** map (`01`).
- **Collision-model independence test** (`01`/`02`) — waves grouping decided (D36).
- **Arbiter** batch-vs-one input contract (`01`).
- **Optional SDK "runner"** for fully-autonomous restart (`01`) — deferred add-on; MVP uses
  human-prompted restart. Decided in principle; build + verify SDK auth (subscription vs API key) later.
- **Website stack** (`03`).
- **Automated testing**, **test-from-anywhere**, **paid device/QA platform** (`04`) — designed-for,
  not built.
