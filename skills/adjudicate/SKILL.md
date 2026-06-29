---
name: adjudicate
description: Base procedure for any "gather competing views of reality, then judge" task. Not invoked directly — specialized by verify, debug, and decision-engineer. Reference it when building a capability that must compare realities and return a confidence-scored verdict.
---

# Adjudicate (base)

The shared spine for every adjudication capability. An implementation supplies only **which views** to
gather and **how to judge** — the procedure and the I/O contract are fixed here. (This is the
Investigation → Arbiter pattern, D6, reified.)

## Contract
- **In:** a question + a view-set (which realities to gather) + a confidence threshold.
- **Out:** `{ verdict, confidence, escalate? }`.

## Procedure
1. **Fan out** workers to gather each view independently — heavy context stays with the workers; they
   return thin summaries (three-layer memory, D4).
2. **Compare & judge** the views per the implementation's rubric.
3. **Score confidence** in the verdict.
4. **Gate:**
   - confidence ≥ threshold → emit the verdict.
   - confidence < threshold → gather more (more workers / more tests / `research`) and re-run.
   - views irreconcilable → escalate up to the orchestrator (and the human if needed).

## Implementations
- `verify` — views = {asked, done}; judge conformance. (lean — may skip the fan-out)
- `debug` — views = {intended behaviour, actual behaviour}; judge root cause.
- `decision-engineer` — views = {option A, option B, …, market practice}; judge best fit.
