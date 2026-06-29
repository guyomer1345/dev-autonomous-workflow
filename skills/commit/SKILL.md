---
name: commit
description: Snapshot project state to git after a phase is documented — the durable checkpoint marker the loop resumes from. One commit per completed phase/item, written as a Conventional Commit linked back to its work item. Use at the tail of a completed item, after document.
---

# Commit — the durable checkpoint marker

Core principle: one commit per completed phase/item. The commit is what the loop resumes from and what the
handoff relies on, so its message is machine-readable loop state, not just prose.

## When
After `document`, per completed phase/item.

## Inputs
- the completed item's staged changes
- the `plan` / backlog item it traces back to (for the id) and any `issue` it resolves (for `github_ref`).

## Workflow
1. Stage the item's changes.
2. Write a **Conventional Commit** — `type(scope): summary`, type from the item's `kind`
   (`bug → fix`, `feature → feat`, `debt → refactor`/`chore`).
3. Add linking trailers:
   - `Refs: item #<backlog-id>` — always.
   - `Closes: #<github-issue>` — when this item resolves a tracked issue.

## Rules
- One commit per completed item; never bundle unrelated items.
- The message must trace back to the item — no bare "wip"/"fix" subjects.

## Output
A commit — the checkpoint marker. Its `Closes:` trailer names the issue that `close-issue` then closes.

## Route
→ `close-issue` (close the GitHub issue this item resolved), then the loop picks the next item.

## References
Remote push and the branch lifecycle (the parallel-work merge/conflict extension) sit beyond this skill.
Commit is local and autonomous; **push is an outward action — gated behind explicit human permission** (the
loop keeps committing and queues the push for approval).
