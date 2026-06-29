---
name: checkpoint
description: Pause autonomous work to get a human verdict on the live app, then resume on the answer. Three kinds — demo (approve a sandbox), qa (test a built feature), setup (perform a manual external action). Blocks on the local bus; routes pass→continue, fail→debug.
---

# Checkpoint

The human-in-the-loop gate (Space 4). The human counterpart of `verify`: where verify checks artifacts,
the checkpoint asks a person to confirm the live app — the real "does it work" signal in MVP (autonomous
testing is out of scope, D14).

## Kinds
- **demo** — approve a `create-demo` sandbox.
- **qa** — test a built feature against its acceptance criteria.
- **setup** — perform a manual external action; calls `setup-guide` for precise steps.

## Do
1. Assemble the `request` `{ kind, what, expected, how?(←setup-guide), blocking: true }`.
2. Post it to the console and **block on the local bus** — an explicit wait step, not a hook exit-code
   trick (D12).
3. Receive the `verdict` `{ pass, notes }`.

## Route
- **pass** → `document` / `commit` (for kind=demo, lock the spec state instead).
- **fail** → `debug` → `refine`.

## Calls
`setup-guide` (kind=setup).
