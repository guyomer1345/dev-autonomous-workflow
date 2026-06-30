#!/usr/bin/env bash
# PreToolUse(Bash) guard for the disciplined-builder loop.
#
# Enforces the two gates that are legitimate HARD blocks — operations you never *want*
# to perform, so there is no approve-and-proceed path:
#   - secret-scan          : never commit a secret that is staged in the diff
#   - verify-before-commit : never commit an item whose verify-verdict is a fail
#
# Outward-action gating (git push / gh) is NOT here — it is an `ask` rule in
# settings.json (a deliberate human prompt with an approve path), not a forbid.
#
# Exit 2 blocks the tool call (message on stderr) and overrides allow rules; it also
# fires under bypassPermissions mode. Exit 0 lets the call proceed.
#
# Dependency: python3 (to parse the PreToolUse JSON payload). If absent, fails open.
set -uo pipefail

payload="$(cat)"
cmd="$(printf '%s' "$payload" \
  | python3 -c 'import sys,json; print(json.load(sys.stdin).get("tool_input",{}).get("command",""))' \
  2>/dev/null || true)"

block() { echo "BLOCKED by disciplined-builder guard: $1" >&2; exit 2; }

case "$cmd" in
  *"git commit"*)
    # --- secret-scan on the staged diff ---
    staged="$(git diff --cached 2>/dev/null || true)"
    if printf '%s' "$staged" | grep -Eiq \
      '(AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|(api[_-]?key|secret|password|token)["'"'"' ]*[:=]["'"'"' ]*[A-Za-z0-9/+_-]{12,})'; then
      block "possible secret in the staged diff (secret-scan). Remove it or use a placeholder before committing."
    fi

    # --- verify-before-commit (best-effort) ---
    item="$(python3 -c 'import json; print(json.load(open(".workflow/state.json")).get("current_item") or "")' 2>/dev/null || true)"
    verdict=".workflow/items/$item/verify-verdict.md"
    if [ -n "$item" ] && [ -f "$verdict" ] && grep -Eiq 'pass:[[:space:]]*false' "$verdict"; then
      block "item $item has a failing verify-verdict; run debug -> refine -> verify before committing."
    fi
    ;;
esac

exit 0
