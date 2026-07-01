---
name: document
description: Fold completed changes and the decisions behind them into the project knowledge base — the LLM-wiki nodes, typed edges, and per-file Sessions log. Runs after a phase passes its checkpoint. Reads the changelog plus the decision/event stream, not just the diff.
---

# Document — keep the knowledge base current

Core principle: document-as-it-goes so the workflow can stay autonomous — fold each completed change and
the decisions behind it into the knowledge base.

## When
After a phase/item passes its checkpoint, before or with `commit`.

## Inputs
`changelog` + `decision-record`s + `debug-report`s — the decision/event stream, not just the changelog.

## Workflow
1. Update `docs/knowledge/` nodes for touched files — `purpose` (intent vs actual), typed edges with their
   `why`.
2. Refresh the **architecture doc** (inline Mermaid-C4 L1/L2) in the **same item** when the change moves
   system/container structure — STABLE, changes only with the code. *(It lives at
   `<project_root>/docs/architecture.md`; resolve `<project_root>` from `config.json`.)*
3. Append a per-file `# Sessions` entry where a postmortem applies (a `debug-report` maps directly:
   symptom / cause / fix / avoid).
4. Flag intent-vs-actual divergence as a signal.

## Rules
- **Never** flag divergence for `provisional` items, or the drift alarm chases ghosts.

## Output
Updated `docs/knowledge/` (nodes, graph, Sessions) + the architecture doc.

## Audit mode (retention + prune)
A second mode, run as a maintenance item `prioritize` injects on a count/size threshold (not after each phase).
Keeps disk + context high-signal:
- **Run the retention script** (mechanical, deterministic): cap each node's `# Sessions` to the last *K* raw
  entries (older → git, leave a one-line archive pointer); GC superseded `docs/decisions/` bodies to git + update
  `docs/decisions/index.md`; prune closed `items/<id>/`. (The `git log` cold-start bound rides `handoff.base_sha`.)
- **Deletion-test (judgment)** over `CLAUDE.md` + `rules/` — cut prose the agent no longer needs; bloat makes
  it ignore its own instructions.
- **Dead-node prune:** a deleted source file → delete its `docs/knowledge/` node.
Distillation (postmortems → lessons) is deferred.

## Route
→ `commit`.
