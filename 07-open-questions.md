# 07 — Open Questions Register

Deliberately deferred — known unknowns, to close during build or later.

## Must close before build
- **Rest of the macro-loop** (`01`) — the phase set (execute → test → document → audit → next) + how
  checkpoint / reset slot in. *Intake stage now closed in `09` (inception/steering covered there).*
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
- **Disk layout** (`05`) — the full file tree + protocols; incl. the exact diagrams location (D41).
- **Adoption follow-ons (D38–D45)** — the **prune-pass** mechanism and **staleness-detection** signal that
  keep STABLE/guidance files fresh (D41); whether `verify` samples the real `git diff` vs trusts the
  `changelog` (#8); authoring the thin baseline `rules/` + `/start` enforcement wiring (D40).

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
