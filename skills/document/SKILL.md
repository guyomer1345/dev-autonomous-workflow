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
1. Update `.knowledge/` nodes for touched files — `purpose` (intent vs actual), typed edges with their
   `why`.
2. Append `# Sessions` entries where a postmortem applies (a `debug-report` maps directly:
   symptom / cause / fix / avoid).
3. Flag intent-vs-actual divergence as a signal.

## Rules
- **Never** flag divergence for `provisional` items, or the drift alarm chases ghosts.

## Output
Updated `.knowledge/` (nodes, graph, Sessions).

## Route
→ `commit`.
