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
1. **GC the queue first:** drop done items so `backlog.md` stays a live *open* queue, not a ledger —
   roadmap items `commit` flipped done, and `issue` entries whose `github_ref` is closed on GitHub.
2. **Schedule maintenance:** if a retention threshold is tripped — a node's `# Sessions` > *K*,
   `docs/decisions/` active > *N*, or `items/` closed > *M* — or every *N* items, inject a `document:audit` item.
3. Make eligible only items whose `depends_on` are already done.
4. Order eligible items by **urgency × dependency-readiness**.
5. Emit the top item as "next".

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
