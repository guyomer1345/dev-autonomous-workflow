# Memory Model — what the loop may rewrite, change, or never touch

The design law for every durable file the workflow reads or writes (D38). A file earns its place only if it
holds **non-derivable intent** or is the loop's **cross-session memory**; everything else is **generated on
demand** or **enforced by CI** — prose rots silently, code and checks fail loudly.

## Three tiers — encoded by location + filename so a skill knows its rights
| Tier | Rule | Examples |
|---|---|---|
| **VOLATILE** | rewrite freely each iteration | `.workflow/state.json`, `handoff.md` |
| **STABLE** | change **only in the same item as the code that changes it**, CI-gated | `spec/`, architecture diagrams |
| **APPEND-ONLY** | **supersede, never edit** | `.workflow/decisions/`, the audit / `# Sessions` stream |

## Consequences (binding on all skills)
- `execute` / `refine` touch STABLE files only as part of the item that changes the code.
- `document` owns STABLE doc + diagram freshness (same-item) and the APPEND-ONLY `# Sessions` log.
- A `decision-record` is never edited — a reversal is a **new** record that supersedes (status flip).
- Structural code maps are **generated, never hand-written** (D39) — not a tier, an output.
- Enforceable rules live in lint/test/CI/hooks, not prose (D40); prose shrinks to non-derivable intent.

## Open
The **staleness-detection** signal and the **prune-pass** mechanism that keep STABLE/guidance files fresh are
not yet designed (D41 → `07`).
