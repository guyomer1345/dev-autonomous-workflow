# 05 — Shared State + Comms Bus (Space 5)

## Why it's its own space **[DECIDED]**
Because agents are persistent but the orchestrator stays lean, and the website is local-only, every
connection between spaces runs through **disk artifacts + a local bus**. Designed deliberately so it
doesn't grow ad hoc.

## The comms bus **[DECIDED — A3 research]**
A **local HTTP loopback service** (the website's backend) is the message channel.
- website → orchestrator: POST to localhost (verdicts, instructions); orchestrator reads via curl / a
  local MCP tool.
- orchestrator → website: orchestrator writes `state.json`; website reads it (inotify / poll).
- File-watching is **rejected for control-flow** (fragile, polling, races); fine only for one-way
  state display.

## Disk layout **[PROVISIONAL first cut — D29; EXPAND]**
`init` (`commands/start.md`) scaffolds this provisional layout in a target project:
```
<launch root>      # where Claude runs = the orchestrator's home
  CLAUDE.md         # orchestrator brief (greenfield: here; brownfield: a marked block in the existing one)
  .workflow/
    config.json     # project_root (./project | .) + run config    (committed)
    loop.md         # routing graph + diagram (fixed topology)      (committed)
    state.json      # live position (item/phase/wave) — RUNTIME, gitignored
    handoff.md      # durable resume anchor                         (committed)
    backlog.md      # issues + roadmap items                        (committed)
    decisions/      # decision-records (append-only, global)        (committed)
    checkpoints/    # checkpoint request/verdict records (global)   (committed)
    items/<id>/     # per-item working artifacts: plan/changelog/verdict/debug-report  (committed)
  spec/             # the product spec (discuss fills it)           (committed)
  .knowledge/       # code map — Space 6                            (committed)
  <project_root>/   # product code (greenfield: project/ ; brownfield: the repo root itself)
```
**Commit policy:** everything durable is committed; only `.workflow/state.json` (a regenerable view for
the console) is gitignored.

**Memory tiers (D38 — `shared/memory-model.md`):** every durable file is **volatile** (rewrite freely:
`state.json`, `handoff.md`), **stable** (change only with the code that changes it, CI-gated: `spec/`,
architecture diagrams under `spec/` or a `diagrams/` sibling), or **append-only** (supersede, never edit:
`decisions/`, the `# Sessions` stream). Skills key off location + filename to know their rights.

**Resume model (D48).** `state.json` is the volatile live pointer (rewritten in place); `handoff.md` is the
durable resume anchor (program counter — current item + loop position + parked work); **git history is the
append-only completed-step log** (each item ends in a `commit`). Mid-run the orchestrator reads `state.json`;
a cold start reads `handoff.md` + `git log` and rebuilds. **Bounded by construction (D51):** every
always-read file (`CLAUDE.md`, `state.json`, `handoff.md`, `loop.md`) holds current state only — never history.

Still to close: read/write ownership per file + the request/response protocol; whether `spec/` and
`.knowledge/` merge under a single docs root (and whether they sit at the launch root or under
`<project_root>`, D49); symbol-level knowledge paths; the exact diagrams location.
