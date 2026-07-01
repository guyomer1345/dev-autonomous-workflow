#!/usr/bin/env bash
# Git-native pre-commit backstop for the disciplined-builder loop.
#
# The mechanical drift tier has two callers of the SAME project check runner
# (`.workflow/checks.sh`, generated per-stack by /start's enforcement wiring):
#   - the `commit` skill runs it with `--fix` — auto-applies zero-judgment fixes
#     (reformat, strip a stale reference), re-stages, logs what it fixed, and the
#     commit proceeds. This is the in-loop, visible path.
#   - THIS hook is the catch-all backstop for commits made outside the loop (a
#     human's manual `git commit`). It runs the runner in CHECK-ONLY mode and
#     never rewrites the human's tree silently — on a failure it blocks and points
#     at the fix, rather than reformatting behind the committer's back.
#
# Installed by /start to `.git/hooks/pre-commit`. Distinct from guard.sh, which is
# the PreToolUse(Bash) harness gate for the never-want-irreversible hard blocks
# (secret-scan + verify-before-commit).
#
# Fails OPEN: if no project check runner is wired yet, the commit proceeds.
set -uo pipefail

runner=".workflow/checks.sh"
[ -x "$runner" ] || [ -f "$runner" ] || exit 0

if ! bash "$runner" --check; then
  echo "BLOCKED by disciplined-builder pre-commit: mechanical checks failed." >&2
  echo "Fix: run the commit skill (auto-fixes what it can) or 'bash $runner --fix', then re-stage." >&2
  exit 1
fi

exit 0
