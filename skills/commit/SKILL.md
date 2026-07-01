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
2. **Secret-scan the staged diff first.** Look for key prefixes, private-key headers, and
   `password` / `secret` / `api_key` / `token` set to a real (non-placeholder) literal. On a hit, **stop and
   escalate** — never commit the secret; once in history it lives there forever. (A guard hook re-checks this
   deterministically as the backstop — the step keeps it visible in the loop.)
3. **Split out a prerequisite-repair, if any.** If the `changelog` recorded a `prerequisite-repair`
   divergence, commit that repair as its **own** commit first — typed and scanned like any other — so the
   stumbled-into fix stays reviewable and revertible apart from the planned change.
4. Write the planned change as a **Conventional Commit** — `type(scope): summary`, type from the item's `kind`
   (`bug → fix`, `feature → feat`, `debt → refactor`/`chore`).
5. Add linking trailers:
   - `Refs: item #<backlog-id>` — always.
   - `Closes: #<github-issue>` — when this item resolves a tracked issue.

## Rules
- One commit for the item's planned change; a recorded `prerequisite-repair` rides its **own** preceding
  commit (the only split). Never bundle otherwise-unrelated items.
- The message must trace back to the item — no bare "wip"/"fix" subjects.
- Bookkeeping rides the **planned** commit: the backlog item's done-flip and the `handoff.md` rewrite happen
  **before** it (after any prerequisite-repair commit), so the completing commit captures them. `close-issue`
  is the only post-commit tail step.

## Output
A commit — the checkpoint marker. Its `Closes:` trailer names the issue that `close-issue` then closes.

## Route
→ `close-issue` (close the GitHub issue this item resolved), then the loop picks the next item.

## References
Remote push and the branch lifecycle (the parallel-work merge/conflict extension) sit beyond this skill.
Commit is local and autonomous; **push is an outward action — gated behind explicit human permission** (the
loop keeps committing and queues the push for approval).
