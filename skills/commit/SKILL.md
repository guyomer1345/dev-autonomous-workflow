---
name: commit
description: Snapshot project state to git after a phase is documented — the durable checkpoint marker. One commit per completed phase/item.
---

# Commit

## When
After `document`, per completed phase/item.

## Do
1. Stage the phase's changes.
2. Commit with a message tracing back to the item/plan.

## Output
A commit — the durable checkpoint marker the loop resumes from, and the one the handoff relies on (D10).

## Note
Remote push and the branch lifecycle (the parallel-work merge/conflict extension) sit beyond this skill.
