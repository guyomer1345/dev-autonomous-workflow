---
name: refine
description: Decide what to do with a verify failure, a debug finding, or a newly-arisen need, and route the correction back through planner→execute. Never edits code itself — it preserves execute's zero-decision discipline by funnelling every change through the normal plan→execute→verify pipe.
---

# Refine — the correction router

Core principle: closes the loop after something comes back wrong or a new need appears — by routing, never
by editing code, so `execute` stays decision-free.

## When
A `verify` failure, a `debug-report`, or a new need that arose from the just-built code.

## Inputs
A `verify-verdict` (fail), a `debug-report`, or a stated new need.

## Workflow
1. Read the failure / finding.
2. Decide the corrective action.
3. Emit a **plan-delta** → `planner` (plan-one) → `execute` → `verify`. Loop until verify passes.

## Rules
- Touches **no code** itself. Every change flows through the disciplined plan → execute → verify pipe.

## Output
A plan-delta handed to `planner`.

## Route
→ `planner` (plan-one) → `execute` → `verify`; loop until re-verified pass.
