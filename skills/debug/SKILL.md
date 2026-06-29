---
name: debug
description: Find the root cause when behaviour doesn't match intent — triggered by a failed verify, a failed test, or a live error. Maps intended vs actual behaviour, judges the cause with a confidence score, and loops for more information when unsure. Hands its finding to refine; it diagnoses, it does not fix.
---

# Debug

An `adjudicate` implementation (views = {intended behaviour, actual behaviour}; domain = defects).

## When
`verify` fails, a test fails, or a live error occurs. A failed check is a valid trigger even with no live
crash.

## Do (per the `adjudicate` base)
1. Dispatch workers to map both worlds — **intended** behaviour (from spec / acceptance / knowledge base)
   vs **actual** behaviour (from code + the failure signal).
2. Judge where the divergence originates → root cause, with a confidence score.
3. confidence < threshold → call `research` (is this a known issue?) or request more tests, then re-run.

## Output
`debug-report` (symptom, cause, fix, avoid, confidence) — the same format as the Space-6 `# Sessions`
log (D13).

## Route
Hand the report to `refine`. Debug operates on **runtime behaviour** (vs `verify`, which operates on
artifacts) and diagnoses only — it does not fix.

## Calls
`research`.
