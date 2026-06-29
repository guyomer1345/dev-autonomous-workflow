---
name: refine
description: Decide what to do with a verify failure, a debug finding, or a newly-arisen need, and route the correction back through planner→execute. Never edits code itself — it preserves execute's zero-decision discipline by funnelling every change through the normal plan→execute→verify pipe.
---

# Refine

The **correction router**. Closes the loop after something comes back wrong or a new need appears.

## When
A `verify` failure, a `debug-report`, or a new need that arose from the just-built code.

## Do
1. Read the failure / finding.
2. Decide the corrective action.
3. Emit a **plan-delta** → `planner` (plan-one) → `execute` → `verify`. Loop until verify passes.

## Invariant
Touches **no code** itself. Every change flows through the disciplined plan → execute → verify pipe, so
`execute` stays decision-free.

## Exit
Re-verified pass.
