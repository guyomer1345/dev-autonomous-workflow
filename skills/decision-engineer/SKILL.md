---
name: decision-engineer
description: Resolve an open build decision — tech stack, library, architecture — by gathering the options and current market practice and weighing them against the project's spec, returning a confidence-scored verdict. The Arbiter; invoked by planner (or anything) when it hits a decision it must not guess.
---

# Decision-engineer — resolve an open build decision

Core principle: an `adjudicate` specialization (views = {option A, option B, …, market practice}; domain =
engineering choices) — the deciding end of the gather-then-judge pattern.

## When
An open decision blocks planning — a `TBD → decision-engineer` pointer in the `spec`, or a blocker raised
by `planner` / `execute`.

## Inputs
The open decision + the constraints from the `spec` (audience, runtime, scale, integrations).

## Workflow
1. Frame the decision and the spec constraints.
2. Dispatch `research` to gather options + current best practice for this and similar products.
3. Weigh options × market practice × our spec → best fit, with a confidence score.
4. confidence ≥ threshold → emit a `decision-record`; else gather more / escalate to the human.

## Output
`decision-record` `{ question, options, chosen, why, confidence, sources }`, plus its **active row** in
`docs/decisions/index.md` (`| <id> | <title> | active | - |` — the 4-column format retention later flips to a
tombstone on supersede). The spec's `TBD` flips to `locked`.

## Route
→ back to the caller (`planner` / `execute`) with the decision resolved.

## Calls
`research`.
