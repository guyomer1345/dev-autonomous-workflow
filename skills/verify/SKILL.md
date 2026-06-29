---
name: verify
description: Check that what was built conforms to what was asked — plan vs changelog, and whether the intent and acceptance criteria were actually met. Operates on artifacts, not runtime behaviour. Use after execute (skippable for trivial changes); on failure, hand off to debug.
---

# Verify

An `adjudicate` implementation (views = {asked, done}). Conformance on **artifacts** — not runtime
behaviour (that's `debug`).

## Do — two checks
- **A. Plan ↔ changelog:** the changes asked for in the `plan` match the changes recorded in the
  `changelog`.
- **B. Intent met:** the `spec`/discuss intent and the plan's `acceptance_criteria` are reflected and
  actually achieved. (This is the definition-of-done gate, D17.)

Lean implementation — for small changes you may judge directly without fanning out workers.

## Output
`verify-verdict { pass, mismatches[], confidence }`.

## Route
- **pass** → `checkpoint` (human QA) → `document` / `commit`.
- **fail** → `debug`. A failed check is a valid debug trigger even with no live error.
