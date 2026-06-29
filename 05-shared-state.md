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
.workflow/
  state.json        # live console state — RUNTIME, gitignored
  handoff.md        # orchestrator reset/handoff state   (committed)
  backlog.md        # issues + roadmap items             (committed)
  decisions/        # decision-records                   (committed)
  checkpoints/      # checkpoint request/verdict records (committed)
spec/               # the product spec (discuss fills it)(committed)
.knowledge/         # knowledge base — Space 6           (committed)
```
**Commit policy:** everything durable is committed; only `.workflow/state.json` (a regenerable view for
the console) is gitignored.

Still to close: read/write ownership per file + the request/response protocol; whether `spec/` and
`.knowledge/` merge under a single docs root; symbol-level knowledge paths.
