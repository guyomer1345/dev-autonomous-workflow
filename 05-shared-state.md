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

## Disk layout **[OPEN — assemble]**
Known pieces to place:
- `handoff.md` — orchestrator reset/handoff state.
- `state.json` — live state for the website.
- the roadmap / todos.
- `.knowledge/` — the knowledge base (Space 6).
- checkpoint request/verdict records.

To close: the full file tree + read/write ownership + the request/response protocol.
