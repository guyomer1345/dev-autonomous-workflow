---
name: execute
description: Run a plan file step by step and record exactly what was done. Makes no decisions of its own — if it hits anything undecided, it stops and escalates. Use to carry out an approved plan, never to design or choose.
---

# Execute

Carry out a `plan` faithfully and produce a `changelog`. This is the **keystone** of the loop: because
execute decides nothing, `verify` and `document` can trust the changelog.

## Do
1. Work the plan's `steps` in order.
2. Record every action in the `changelog` (`step, files, result`).
3. Record any **divergence** from the plan formally (`step, expected, actual, why`) — never silently.

## Invariants
- **Zero autonomous decisions.** A choice the plan didn't make is a blocker, not a judgement call.
- **Escalate, never improvise.** On a blocker (an undecided option, missing info), stop and raise it up —
  the orchestrator routes it (e.g. to `decision-engineer`), then execution resumes from the resolved plan.

## Output
A `changelog` referencing the plan.

## Exit
All steps done, or a blocker raised and handed up.
