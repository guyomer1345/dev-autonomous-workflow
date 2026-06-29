---
name: prioritize
description: Order the backlog and emit the next work item. Runs on every backlog change and whenever a phase completes. Pure queue — never preempts in-flight work; the machine finishes the current item, then re-picks.
---

# Prioritize — order the backlog, emit the next item

Core principle: a **pure queue** — the machine never preempts itself; it finishes the current item, then
re-picks.

## When
On any backlog change (a new roadmap, a new issue) and whenever a phase/item completes.

## Inputs
The backlog (items with `depends_on`, `kind`, `severity`).

## Workflow
1. Make eligible only items whose `depends_on` are already done.
2. Order eligible items by **urgency × dependency-readiness**.
3. Emit the top item as "next".

## Rules
- **Never preempt in-flight work.** A bug found *during* the current item is handled inside that item's own
  `verify → debug → refine` loop — it is not a competing backlog item, so it never reaches prioritize as an
  interrupt.
- The only preempt path is the **human's manual override** (steering: "do this now") — a human action, not
  an autonomous scheduling decision.

## Output
The next-item pointer (+ the updated ordering).

## Route
→ the orchestrator runs the emitted item (`planner` / its sub-loop).
