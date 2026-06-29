---
name: discuss
description: First step of any new intake — a new project or a new feature — before planning. Runs the requirements conversation with the user and produces the spec. Use when the user wants to start something new and the goal isn't yet captured as a written, testable spec.
---

# Discuss

Turn a user's intent into a written `spec` (see `shared/schemas.md`). Requirements only — **never decide
the tech stack or any engineering choice here.**

## When
The first capability in any new intake loop (project or feature), ahead of `create-demo` and `planner`.

## Do
1. Let the user describe what they want; reflect it back until the idea is formed.
2. Drive the spec to completeness against the required fields:
   - **project (inception):** audience, runtime, purpose, screens, features, data_model, integrations,
     tech_stack. (D20)
   - **feature:** purpose, and visuals + acceptance criteria if it has a visible surface.
3. Tag every field with a **commitment level** — locked / provisional / unspecified (D23). Default detail
   and styling to *provisional*; flow and scope to *locked-candidate*.
4. For any genuine engineering decision (stack, library, architecture), **do not decide** — record
   `TBD → decision-engineer` as a pointer. If the user states a firm preference, record it as `locked`.

## Output
A `spec`, every field commitment-tagged, with `TBD → adjudicator` pointers where decisions are open.

## Exit
Every required field is filled or explicitly provisional/TBD. Hand off to the sandbox-gate check
(`create-demo`), then `planner`.
