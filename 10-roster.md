# 10 — Capability Roster (Space 2 v1)

Closes the `02` open item (roster + I/O contracts + skill-vs-agent + topology). Derived by walking a full
new-project loop end-to-end (session 2026-06-29). Each capability's full contract lives in its own package
file; artifact formats live in `shared/schemas.md`. **This doc is the map** — roster, loop order,
call-graph, open items.

## Package layout **[DECIDED — D25]**
Claude-Code-native plugin source at the repo root:
- `commands/<name>.md` — human-invoked entry points (e.g. `/start`)
- `skills/<name>/SKILL.md` — procedure capabilities (model-invoked)
- `agents/<name>.md` — leaf worker capabilities
- `shared/schemas.md` — inter-capability artifact schemas
- `shared/format.md` — the authoring format every package file follows (D31/D34)
- `shared/memory-model.md` — the three-tier rule for what the loop may rewrite/change/never-touch (D38)
- `rules/<topic>.md` — thin baseline engineering rules, specialized per project by `/start` (D40)
- `templates/` — files `/start` installs into a target: `orchestrator-CLAUDE.md`, `loop.md`,
  `settings.json` (loop permission rules: `allow` local / `ask` outward) (D52/D57/D58)
- `hooks/guard.sh` — PreToolUse gate (secret-scan + verify-before-commit); installed to `.claude/hooks/` (D58)

**Driver added (D46/D47):** the orchestrator **`CLAUDE.md`** (root brief) + **`.workflow/loop.md`** (routing
graph + diagram) + **`hooks/`** (the enforced gates). (Later: `.claude-plugin/plugin.json`.) The repo is now
**both** the spec (`00`–`10`) and the package source.

## Skill vs agent **[DECIDED — D24, D27]**
- **skill** = a procedure / controller — run by the orchestrator; defines *how*; **may dispatch agents**.
- **agent** = a **leaf worker** — its own tools, persistent/re-messageable (D4); does the heavy lifting;
  **never spawns sub-agents.**
- Topology (closes `02`): **strict hub-and-spoke** — only skills/orchestrator fan out; agents are leaves.
- Consequence: the only agents are `research` and `setup-guide`; all adjudicators (`verify`, `debug`,
  `decision-engineer`) are skills.

## The adjudicate pattern **[DECIDED — D24]**
One base skill `adjudicate` (gather views → judge → confidence-gate → loop/escalate), specialized by
`verify` / `debug` / `decision-engineer`. Collapses the prior Arbiter / engineer-agent / decision-engineer
overlap into one adjudicator.

## Roster
| capability | kind | one-line job | file |
|---|---|---|---|
| start (init) | command | bootstrap the workflow; greenfield/brownfield (D28/D29) | `commands/start` |
| adjudicate | skill (base) | gather views → judge → confidence-gate | `skills/adjudicate` |
| discuss | skill | intake conversation → `spec` | `skills/discuss` |
| create-demo | skill | throwaway sandbox for product approval | `skills/create-demo` |
| prioritize | skill | order the backlog, emit the next item | `skills/prioritize` |
| planner | skill | decompose → `roadmap` / plan one item → `plan` | `skills/planner` |
| decision-engineer | skill | resolve an open build decision (adjudicate) | `skills/decision-engineer` |
| research | agent | gather info (Investigation worker) | `agents/research` |
| execute | skill | run a plan, decide nothing → `changelog` | `skills/execute` |
| verify | skill | artifact conformance (adjudicate) | `skills/verify` |
| debug | skill | root-cause behaviour ≠ intended (adjudicate) | `skills/debug` |
| refine | skill | route corrections back through planner→execute | `skills/refine` |
| checkpoint | skill | pause for a human verdict (demo / qa / setup) | `skills/checkpoint` |
| setup-guide | agent | precise human steps for a manual external task | `agents/setup-guide` |
| document | skill | fold changes + decisions into the knowledge base | `skills/document` |
| ingest | skill | brownfield: build the knowledge base + reconstructed spec from existing code | `skills/ingest` |
| commit | skill | git snapshot (Conventional Commit; the checkpoint marker) | `skills/commit` |
| create-issue | skill | capture a problem/idea → backlog + GitHub issue | `skills/create-issue` |
| close-issue | skill | close the GitHub issue a completed item resolved (commit tail) | `skills/close-issue` |

## Loop order (the spine)
```
backlog
  → prioritize (pick next)
  → discuss  ┐ intake (09)
  → create-demo ┘ (if the gate fires)
  → planner ──► decision-engineer ──► research
  → execute (→ changelog)
  → verify ──on-fail──► debug ──► refine (routes correction back to planner→execute)
  → checkpoint (qa: only if the plan declared human-qa criteria; setup for kind=setup)
  → document (→ Space 6 Sessions)
  → commit (the checkpoint marker)
  → close-issue (close the GitHub issue the item resolved)

create-issue → backlog   (side-door, from anywhere)
research                  (service, callable from anywhere)
```

## Call-graph (who calls whom)
- `planner` → `decision-engineer` → `research`
- `create-demo` → `checkpoint`
- `checkpoint`(setup) → `setup-guide`  *(leaf: does its own research)*
- `verify` → `debug` → `refine` → `planner` → `execute`
- `debug` → `research`
- any → `create-issue` · any → `research`
- item-complete tail: `verify`(pass) → `document` → `commit` → `close-issue`

## Build status
- **All 17 capability files written** (`skills/`, `agents/`) + `shared/schemas.md`. Roster v1 complete
  (added `close-issue`, D33).
- **Authoring-format pass complete (D31/D34):** all 15 skills + 2 agents follow `shared/format.md` and
  carry no spec-internal refs (grep-gated — `scripts/check-no-spec-refs.sh`).
- **Dogfood-validated (D52):** the orchestrator design *drives* — a throwaway greenfield repo ran two tasks
  (happy + fail/decision) end-to-end; MVP install = loose `.claude/` files (D57). Findings → D53–D57.

## `init` / `/start`  **[BUILT v1 — D29 → `commands/start.md`]**
The bootstrap command (D10/D28). **greenfield** = repo-setup → scaffold → (stub) console → hand to
`discuss`; **fully supported now.** **brownfield/integrate** = the shared scaffold plus the Space-6
**`ingest` skill** + reconciliation checkpoint; ingest **mechanics decided (D68)**, the **`ingest` skill
authored**, and the **Python code-map extractor built + wired into `/start` step 4** — brownfield now ingests
Python stacks end-to-end; other-language extractor arms are the follow-on. Orchestrator `CLAUDE.md` driver now
specced (D46–D49). Stubbed sub-steps to expand: console launch (`03`), full disk layout (`05`).

## Adoption deltas — workflow-kit + GSD (D36–D45, +D40/D65/D67)
Skill bodies **authored** (session 2026-07-01); each delta maps to its landed home:
- `prioritize` — **waves**: dependency-group the ready set; run a wave; re-pick (D36). **+ drift tickets ride
  the normal queue at commitment-severity** (D65).
- `execute` — **divergence tiers** (cosmetic / prerequisite-repair-as-separate-commit / structural-stop, D37);
  **refuse** a destructive `plan` with no verified `backup`, run+verify it first (D42).
- `planner` — set `risk_class` + require `backup` when destructive (D42); **decision-coverage gate** —
  every `decision-record` maps to ≥1 step or block (D43); emit **no un-checkable** acceptance criterion (D30).
- `adjudicate` — **conjunction-of-signals**: an LLM verdict gates only with a corroborating deterministic
  signal; AI-only → advisory (D45). Propagates to `verify`/`debug`/`decision-engineer`.
- `commit` — **secret-scan** the staged diff, stop on a hit (D44); **+ mechanical-gate step** (`checks.sh --fix`
  → log; semantic drift → `create-issue`, never resolved inline) (D65/D67).
- thin **`rules/`** baseline (enforced-by tags) + **`/start` step-4 enforcement wiring** + git `pre-commit`
  backstop + generated `.workflow/checks.sh`, nearest-file-wins (D40/D65/D67). **Remaining:** the per-stack
  `checks.sh` generator (a `/start` runtime detail).
- **Also landed earlier:** `document` same-item doc + Mermaid-C4 freshness + audit prune (D41);
  `shared/memory-model.md` (D38); `shared/schemas.md` plan `risk_class`/`backup`/`decisions[]`.

## Still open
- The **collision-model independence test** — when two items are independent enough to share a wave (`02` / `07`).
- `init` **brownfield-ingest** — mechanics decided (D68); `ingest` skill + the Python code-map extractor built
  and wired into `/start`. Remaining: other-language extractor arms (same `graph.json` contract).
- D41 freshness mechanisms (staleness signal, prune pass) + #8 (verify reads diff?) — `07`.
