# Memory Model — what the loop may rewrite, change, or never touch

The design law for every durable file the workflow reads or writes (D38). A file earns its place only if it
holds **non-derivable intent** or is the loop's **cross-session memory**; everything else is **generated on
demand** or **enforced by CI** — prose rots silently, code and checks fail loudly.

## Three tiers — encoded by location + filename so a skill knows its rights
| Tier | Rule | Examples |
|---|---|---|
| **VOLATILE** | rewrite freely each iteration | `.workflow/state.json`, `handoff.md` |
| **STABLE** | change **only in the same item as the code that changes it**, CI-gated | `docs/spec/`, `docs/architecture.md` |
| **APPEND-ONLY** | **supersede, never edit** | `docs/decisions/`, the per-file `# Sessions` sections |

## Consequences (binding on all skills)
- `execute` / `refine` touch STABLE files only as part of the item that changes the code.
- `document` owns STABLE doc + diagram freshness (same-item) and the APPEND-ONLY `# Sessions` log.
- A `decision-record` is never edited — a reversal is a **new** record that supersedes (status flip).
- Structural code maps are **generated, never hand-written** (D39) — not a tier, an output.
- Enforceable rules live in lint/test/CI/hooks, not prose (D40); prose shrinks to non-derivable intent.
- **Always-read files are bounded by construction (D51):** `CLAUDE.md`, `state.json`, `handoff.md`, `loop.md`
  hold current state only — rewritten in place, never grown — so the loop can't inflate its own context cost.
  History lives in git. The **retention & archival law** for the append-only tier is the read-law companion
  (D61, below): **cap-and-archive** — last-*K* on disk, the rest in git.
- **Don't duplicate state an external system owns (D55):** e.g. GitHub issue open/closed — the backlog holds
  only the `github_ref` pointer; mirroring the state locally creates drift + post-commit bookkeeping.
- **`backlog.md` is a live open queue, not append-only (D59):** rewritten in place; closed items **leave**
  (`prioritize` GCs at pick time — roadmap items `commit` flipped done, `issue` entries whose `github_ref` is
  closed). Bounded by open-WIP, not age — so it sits outside the append-only retention set.

## The read-law companion (D61)
The write law above says *who may edit*; the **retention/read law** says *how much loads*. The append-only
tier is bounded by **cap-and-archive** — last-*K* entries on disk, older entries dropped to git (the working
tree is a bounded **cache**, git the **ledger**). A deterministic **retention script** (cap each node's
`# Sessions`, GC superseded `decisions/`, prune closed `items/<id>/`, bound the `git log` cold-start via
`handoff.base_sha`) runs in an **`audit` maintenance item** that `prioritize` injects on a count/size
threshold; only the prose deletion-test over `CLAUDE.md`+`rules/` needs the LLM (mechanical → enforced, D40).
**Staleness** (a doc that's *wrong*, not *big*) is a separate diff-based signal — code changed without its node
or the architecture doc — that schedules a doc-fix, not a prune. *Open:* `K`/thresholds; Sessions
**distillation** (postmortems → lessons) is deferred.
