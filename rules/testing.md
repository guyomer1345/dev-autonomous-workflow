# Testing — baseline

> Baseline principles. A project overrides these with a nearer file (project root, then a path-scoped
> subtree). `/start` specializes the `— enforced by:` mechanisms below to the project's actual test runner.

- Every behavioural change ships with a test that fails before it and passes after. — enforced by: test runner
- A green suite is a merge precondition; a red suite blocks the commit. — enforced by: test runner (CI + gate)
- Test behaviour at the public surface, not private internals — a safe refactor must not break tests.
- Deterministic only — no dependence on time, network, or ordering; quarantine a flaky test, never ignore it.
- Reproduce before you fix — a bug gets a failing regression test first, then the fix that turns it green.
- Coverage is a floor signal, not a target to game; an untested critical path is a gap regardless of the number.
