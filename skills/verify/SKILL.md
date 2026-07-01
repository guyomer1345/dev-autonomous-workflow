---
name: verify
description: Check that built artifacts conform to what was asked — plan vs changelog, and whether the spec intent and the plan's acceptance criteria were met. Operates on artifacts, not runtime behaviour. Use after execute; on failure, hand off to debug.
---

# Verify — artifact conformance ({asked} vs {done})

Core principle: an `adjudicate` specialization — gather the two views (what was *asked*, what was *done*),
judge conformance, gate on confidence. Conformance on **artifacts only**; runtime behaviour is `debug`'s
job and live-app confirmation is `checkpoint`'s.

## Inputs
- `plan` — the asked-for changes + `acceptance_criteria`, each tagged `gate: artifact | human-qa`.
- `changelog` — what `execute` recorded doing.
- `spec` — the intent the plan serves.

## Workflow — two checks
1. **Plan ↔ changelog:** the changes the `plan` asked for match the changes the `changelog` records.
2. **Intent met:** the `spec` intent and the plan's **`artifact`-gated** `acceptance_criteria` are reflected
   and actually achieved (the definition-of-done gate).

Lean: for small changes, judge directly without fanning out workers.

## Rules
- Artifacts only — never run or observe the live app.
- Never pass/fail a `human-qa`-gated criterion; those are confirmed by a `checkpoint` (kind=qa), not here.
- **A `fail` gates only with a deterministic signal behind it** — a failing test, a type/lint violation, a
  plan↔changelog mismatch. A mismatch the model merely suspects is advisory (low confidence), not a hard fail.

## Output
`verify-verdict { pass, mismatches[], confidence }`.

## Route
- **pass** → `document` / `commit`. If the `plan` declared any `human-qa` acceptance criteria, the
  orchestrator inserts a `checkpoint` (kind=qa) first; otherwise straight through — no blanket human QA.
- **fail** → `debug`. A failed check is a valid debug trigger even with no live error.
