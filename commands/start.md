---
description: Bootstrap the disciplined-builder workflow in this project and become the orchestrator. Auto-detects greenfield (empty) vs brownfield (existing code), scaffolds workflow state, and hands off to inception or ingest.
argument-hint: "[greenfield|brownfield]  (optional — auto-detected if omitted)"
---

# /start — bootstrap the workflow (the `init` capability, D28)

Run once to turn the current directory into a workflow-driven project and initialise this session as the
**orchestrator** (Space 1). Conceptually this is `init`; it is exposed as `/start` because `/init` is a
built-in Claude Code command.

## 0. Detect mode & guard
- If `.workflow/` already exists → the project is already initialised. Do **not** clobber: report current
  state and offer to resume from `.workflow/handoff.md` instead. Stop.
- Else pick the mode: `$ARGUMENTS` if given, otherwise **detect** — existing source files present →
  **brownfield**; empty (or package only) → **greenfield**. **Confirm the detected mode with the user**
  before proceeding (mis-classifying is costly).

## 1. Shared steps (both modes)
1. **repo-setup** (D28): ensure git is initialised (`git init -b main`), a git identity is set, and a
   `.gitignore` exists. If a remote is wanted and `gh` is unauthenticated → raise `checkpoint`(kind=setup)
   → `setup-guide` for `gh auth login`. If already authenticated, create/push directly.
2. **Scaffold the workflow layout** (provisional — Space 5, EXPAND):
   ```
   .workflow/
     config.json       # project_root + run config      (committed)
     loop.md           # routing graph + diagram        (committed)
     state.json        # live position — RUNTIME, add to .gitignore
     handoff.md        # durable resume anchor          (committed)
     backlog.md        # issues + roadmap items         (committed)
     decisions/        # decision-records               (committed)
     checkpoints/      # checkpoint request/verdict logs (committed)
   spec/               # the product spec (discuss fills this)   (committed)
   .knowledge/         # code map — Space 6                      (committed)
   project/            # product code (greenfield; brownfield uses the repo root)
   ```
   Add `.workflow/state.json` to the target's `.gitignore`; everything else is committed.
3. **Install the orchestrator brief** (the driver — `01`), from the package `templates/`:
   - **greenfield:** copy `templates/orchestrator-CLAUDE.md` → the launch-root **`CLAUDE.md`** (fill
     `<project>`/`<project_root>`) and put the product under **`project/`** (its own `CLAUDE.md` left to the
     product); set `project_root: ./project`.
   - **brownfield:** the product stays at the repo root; wrap `templates/orchestrator-CLAUDE.md` in the
     **sentinel markers** and **append** it to the *existing* root `CLAUDE.md` (never clobber — idempotent via
     the markers); read that existing `CLAUDE.md` as a **primary ingest source**; set `project_root: .`.
   - Copy `templates/loop.md` → **`.workflow/loop.md`** and write **`.workflow/config.json`** (`project_root` +
     run config).
   - Copy `templates/settings.json` → **`.claude/settings.json`** (loop permission rules: `allow` local
     actions, `ask` outward) and `hooks/guard.sh` → **`.claude/hooks/guard.sh`** (secret-scan +
     verify-before-commit hard gates). `build-once-per-wave` is deferred.
   - **Surface the one-time permission message** to the human: *"This is an autonomous loop. Accept the
     workspace-trust dialog so the package can pre-approve the loop's local actions; outward actions
     (push / issues / deploy) will still ask — by design. You don't need `--dangerously-skip-permissions`."*
4. **Launch the local console** (Space 3). ⛔ STUB — website stack/screens still open.
5. **Commit** the initialised scaffold.

## 2. Greenfield (new project)  — fully supported
- Leave `spec/` and `.knowledge/` empty; they grow as the project is built.
- Hand off to **`discuss`** (inception) to build the spec from zero → then the normal loop
  (`prioritize → planner → …`).

## 3. Brownfield (integrate existing codebase)  — mostly STUB (EXPAND)
- **Ingest** the existing code → populate `.knowledge/` (code graph + per-file nodes, code-derived
  purpose) and a **reconstructed `spec/`** from the code. ⛔ STUB — depends on the Space-6 **ingest
  mechanics**, still open (`06`/`07`). For now: scaffold an empty `.knowledge/` and record a TODO to
  ingest once the mechanics exist.
- **Reconciliation checkpoint** — surface the reconstructed understanding ("here's what I think the app
  does, its screens, its stack") via `checkpoint` for the user to confirm/correct before the loop drives.
- Then hand to the normal loop.

## Expand later
- Space-6 **ingest** for brownfield (the real codebase mapping / llm-wiki build).
- The **console** launch (Space 3).
- The full **disk layout** (Space 5) — the tree above is a provisional first cut.
