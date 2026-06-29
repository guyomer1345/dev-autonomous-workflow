---
name: create-demo
description: Build a throwaway, low-fidelity sandbox of a user-facing change so the user can approve the look and behaviour before it is really built. Use only when the sandbox gate passes — a user-owned, visible, under-determined change. Skip for backend work, refactors, or anything the spec already pins down.
---

# Create-demo

A throwaway alignment artifact, surfaced as a checkpoint, that de-risks the **product** question ("did we
agree *what* to build?") — never the engineering question.

## Gate — build a demo only if ALL hold (D22)
1. an open product decision the **user** owns (system-discovered work never gets a demo);
2. it changes what the user sees or touches (not backend / refactor / internal);
3. the look/behaviour is **under-determined** — a new interaction pattern with no precedent, OR a
   competent build could ship two materially-different versions the user would care between.

Default = **no demo**. A genuine fence on (3) → a one-line yes/no to the user. (The gate is evaluated
per work-item, not just at inception.)

## Do
1. Generate a **minimal, non-integrated** sandbox of the visual/behavioural slice of the `spec` — no
   backend, no real data.
2. **Fidelity matches the question:** low-fi first (validate scope/flow), high-fi only when the look
   itself is the decision.
3. Surface it via `checkpoint` (kind = demo).
4. On "change X": edit the **spec**, then **regenerate** — never edit the demo in place. Repeat until
   approved.

## Invariants
- **Throwaway** — never reused as the real scaffold (D21).
- The spec state that produced the approved demo is what gets **locked**.
- Each `provisional` item in the approved spec spawns a `create-issue` (kind = debt) — tracked debt (D23).

## Exit
User approves → spec commitment levels recorded → hand to `planner`.
