---
name: debug
description: Find the root cause when behaviour doesn't match intent — triggered by a failed verify, a failed test, or a live error. Maps intended vs actual behaviour, judges the cause with a confidence score, and loops for more information when unsure. Hands its finding to refine; it diagnoses, it does not fix.
---

# Debug — root-cause behaviour ≠ intended

Core principle: an `adjudicate` specialization (views = {intended behaviour, actual behaviour}; domain =
defects). Operates on **runtime behaviour** — the counterpart of `verify`, which operates on artifacts.

## When
`verify` fails, a test fails, or a live error occurs. A failed check is a valid trigger even with no live
crash.

## Inputs
- `verify-verdict` (fail) / test output / the live error signal — the **actual** behaviour.
- `spec` + `acceptance_criteria` + knowledge base — the **intended** behaviour.

## Workflow
1. Dispatch workers to map both worlds — intended vs actual behaviour (from code + the failure signal).
2. Judge where the divergence originates → root cause, with a confidence score.
3. confidence < threshold → call `research` (is this a known issue?) or request more tests, then re-run.

## Rules
- Diagnoses only — it does **not** fix; the fix routes through `refine`.

## Output
`debug-report` `{ symptom, cause, fix, avoid, confidence }` — the same format as the knowledge-base
`# Sessions` log.

## Route
→ `refine` (hand off the report).

## Calls
`research`.
