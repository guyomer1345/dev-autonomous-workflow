---
name: prioritize
description: Order the backlog and emit the next wave of independent work items. Runs on every backlog change and whenever a phase completes. Pure queue — never preempts in-flight work; the machine finishes the current item, then re-picks.
---

# Prioritize — order the backlog, emit the next wave

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
5. **Group into a wave.** Walking from the top, gather the independent items that can run together — ones
   that don't collide (they touch disjoint files / modules / areas). A colliding or dependent item falls to
   a later wave. The overlap test is a conservative heuristic (when in doubt, serialize) and will sharpen as
   the collision model firms up.
6. Emit that set as the next **wave**. With a single agent a wave is one item (the degenerate case);
   fanning a wave out in parallel is the coordinator's job, still to come.

## Rules
- **Never preempt in-flight work.** A bug found *during* the current item is handled inside that item's own
  `verify → debug → refine` loop — it is not a competing backlog item, so it never reaches prioritize as an
  interrupt.
- The only preempt path is the **human's manual override** (steering: "do this now") — a human action, not
  an autonomous scheduling decision.

## Output
The next **wave** — the independent items to run together (+ the updated ordering). Serial execution runs a
wave of one.

## Route
→ the orchestrator runs each item in the wave through `planner` / its sub-loop. Build/test hooks run **once
per wave**, not once per item — parallel agents sharing a build otherwise collide on it.
