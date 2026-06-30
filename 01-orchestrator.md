# 01 — Orchestrator (Space 1: the spine)

## Role **[DECIDED]**
The one long-running Claude Code session the human talks to. It is a **thin dispatcher/router**, not a
doer — it holds the vision/goals and routes work to agents, keeping its own context as clean as
possible. Its context window is the scarce resource.

## Three-layer memory model **[DECIDED]**
1. **Orchestrator** = thin router; only distilled questions + decisions flow through it.
2. **Persistent agents** = working memory; each specialist holds its own deep context and can be
   re-messaged (SendMessage). (Corrects the earlier "ephemeral/stateless" assumption — see D4.)
3. **Shared disk state** (Space 5) = durable artifacts; heavy outputs live on disk, agents pass thin
   pointers/summaries up.

## The open-question-resolution pattern **[DECIDED]**
The core autonomy primitive — how any agent unblocks itself without dirtying the orchestrator or
stopping to ask the human:

> Agent hits an open question → reports it UP to the orchestrator → orchestrator (knowing the vision)
> spawns an **Investigation agent** (best practices in comparable products) → then an **Arbiter**
> (makes the call) → reports the decision UP → orchestrator hands it back DOWN to the still-alive
> originating agent, which continues.

- Arbiter open detail: decides a batch in dependency order vs one at a time (changes its input
  contract). **[OPEN]**

## Concurrency **[DECIDED]**
Parallel by default — run as many agents concurrently as the work allows; serialize only when tasks
collide. Realized as **waves** (D36): `prioritize` groups independent ready items into a wave, runs it in
parallel, then re-picks; dependents fall to the next wave; build hooks run **once per wave** (parallel
agents hitting build tools cause lock contention). Still needs a **collision model** — the independence
test itself (file/module/area overlap). **[grouping DECIDED (D36); independence test OPEN — see 07]**

## Session lifecycle **[DECIDED / partly OPEN]**
- PC must be on (Claude can't run with the machine off).
- Start: a command from a clean session initializes it as the orchestrator + launches the website.
- Finite context → graceful **reset/handoff**: park/finish open tasks, `document`, `commit`, then rewrite
  `handoff.md` as the **durable resume anchor** (current item + loop position + parked work). The split:
  `state.json` = volatile live pointer · `handoff.md` = durable anchor · **git history = the append-only
  completed-step log**; a new session resumes from `handoff.md` + `git log` (committed items never rerun).
- **Reset mechanism [DECIDED — research definitive]:** Pure Claude Code **cannot** self-`/clear` or
  auto-restart — `/clear` is a human-only TUI command; no hook/MCP/setting triggers it; `/compact` +
  delegation only pushes the ceiling to ~300–500 turns (~2–4 hrs) before thrashing.
  - **Shared by both paths:** the graceful handoff (park → document → commit → write `handoff.md`)
    happens regardless. Spec it cleanly so the runner below is a small add-on, not a redesign.
  - **MVP (pure config):** at the limit, the website prompts the human to `/clear` + restart from
    `handoff.md`. One click — the only non-autonomous step.
  - **Full autonomy (optional, deferred):** a thin **local SDK "runner"** wraps the session, detects
    context-fill, triggers the handoff, and starts a fresh session from `handoff.md` — no human action.
    The ONLY path to true overnight autonomy. Legal for personal use AND distributable (each user runs
    it on their OWN auth — never routes *others'* Claude). Tradeoff = purity (config + a small program),
    not legality. Caveat to verify later: SDK auth on subscription vs API key.

## The macro-loop **[DECIDED — spine in `10`; driver above]**
The full spine (`prioritize → discuss/create-demo → planner → execute → verify → debug/refine → checkpoint
→ document → commit → close-issue`) lives in `10` and renders as the routing graph in `.workflow/loop.md`;
the orchestrator drives it via the control algorithm in *The orchestrator `CLAUDE.md`* above. Checkpoint =
`04`; reset = the handoff/resume model in Session lifecycle.
- **Intake stage is now specced in `09`** (task types + contracts, the demo skill + sandbox gate, the
  commitment model; inception + steering covered there). The remaining execute → test → document → audit
  → next phases are still open here.

## The orchestrator `CLAUDE.md` — the driver **[DECIDED]**
The package shipped **no driver** until this: the target project's **root `CLAUDE.md`** is the orchestrator's
always-loaded operating brief (re-injected after `/compact`). "Orchestrator" is its *role* — the always-loaded
session at the launch root **is** the orchestrator — not a separate file. Written lean (a frame, not the
per-capability *how*), it encodes:
- **Identity** — thin router + the three-layer memory model above; *bounded by construction* — the files it
  reads every turn (`CLAUDE.md`, `state.json`, `handoff.md`, `loop.md`) are rewritten in place, never grown.
- **The loop** — a *pointer* to `.workflow/loop.md` (routing graph + diagram), read on demand to route
  (definition vs position — `loop.md` is the fixed topology, `state.json` the live pin).
- **The control algorithm** — *read* `state.json` (cold start: `handoff.md` + `git log`) → *place* (mid-item
  continue; between items `prioritize`) → *advance* (look up the node's edges, dispatch, follow the result,
  write `state.json`).
- **Invariants split** — **enforced** (secret-scan + verify-before-commit = `hooks/guard.sh`; outward-action
  gate = settings `ask` rule; build-once-per-wave deferred) vs **disposition** (hub-and-spoke; pure queue;
  resolve-don't-stall via `research`→`decision-engineer`; mind the tiers).
- **Checkpoints** (block on the bus) and **handoff/resume**.

Driving model: `CLAUDE.md` is **advisory context, not enforced configuration** — so the loop *sequence* runs
model-on-rails while the **hard gates are deterministic hooks**. Layout is per-mode (greenfield launch-root +
`project/`; brownfield a marked block in the existing root `CLAUDE.md`) — see `commands/start.md` + `05`.

## Model + effort routing **[DEFERRED]**
Not every task runs at the same model/effort. The orchestrator assigns a model+effort per task type
(e.g. graph-maintenance cheap; Arbiter/planning expensive). Exact mapping not specced now.
