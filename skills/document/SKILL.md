---
name: document
description: Fold completed changes and the decisions behind them into the project knowledge base — the LLM-wiki nodes, typed edges, and per-file Sessions log. Runs after a phase passes its checkpoint. Reads the changelog plus the decision/event stream, not just the diff.
---

# Document

Keep the knowledge base (Space 6) current so the workflow can stay autonomous (document-as-it-goes).

## When
After a phase/item passes its checkpoint, before or with `commit`.

## Reads
`changelog` + `decision-record`s + `debug-report`s — the decision/event stream, not just the changelog.

## Do
1. Update `.knowledge/` nodes for touched files — `purpose` (intent vs actual), typed edges with their
   `why` (D13).
2. Append `# Sessions` entries where a postmortem applies (a `debug-report` maps directly:
   symptom / cause / fix / avoid).
3. Flag intent-vs-actual divergence as a signal — but **never for `provisional` items** (D23), or the
   drift alarm chases ghosts.

## Output
Updated `.knowledge/` (nodes, graph, Sessions).
