---
name: create-issue
description: Capture a problem, bug, or "do this later" into the backlog without addressing it now. The side-door into the loop — issues are later consumed by planner. Used for found bugs, deferred work, and every provisional spec item (tracked debt).
---

# Create-issue

## When
A bug / unwanted behaviour surfaces, the user wants something noted for later, or a `provisional` spec
item needs a finalize-later ticket (D23).

## Do
Write an `issue` `{ title, kind: bug|feature|debt, description, severity, source }` → backlog.

## Note
`severity` is set here (e.g. a universal-invariant-class bug). It feeds `prioritize`'s ordering — but the
machine never self-preempts (pure queue, D26).

## Exit
Issue filed; `prioritize` re-runs.
