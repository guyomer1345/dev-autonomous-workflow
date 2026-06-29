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
- **Agent roster v1** — **CLOSED in `10`** (names, I/O contracts, skill-vs-agent, topology). Remaining
  slivers: the collision model (`02`) and the `prioritize` interrupt model (`09`).
- **What a checkpoint is** (`04`) — data model now in `shared/schemas.md` (demo/qa/setup + verdict).
  Remaining: which help features are MVP.
- **Website screen list** (`03`).
- **Disk layout** (`05`) — the full file tree + protocols.

## Deferred (post-MVP or later)
- **Knowledge maintenance / freshness model** (`06`).
- **Model + effort routing** map (`01`).
- **Collision model** details (`01`/`02`).
- **Arbiter** batch-vs-one input contract (`01`).
- **Optional SDK "runner"** for fully-autonomous restart (`01`) — deferred add-on; MVP uses
  human-prompted restart. Decided in principle; build + verify SDK auth (subscription vs API key) later.
- **Website stack** (`03`).
- **Automated testing**, **test-from-anywhere**, **paid device/QA platform** (`04`) — designed-for,
  not built.
