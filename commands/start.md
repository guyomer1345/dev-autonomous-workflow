---
description: Bootstrap the disciplined-builder workflow in this project and become the orchestrator. Auto-detects greenfield (empty) vs brownfield (existing code), scaffolds workflow state, and hands off to inception or ingest.
argument-hint: "[greenfield|brownfield]  (optional — auto-detected if omitted)"
---

# /start — bootstrap the workflow (the `init` capability)

Run once to turn the current directory into a workflow-driven project and initialise this session as the
**orchestrator**. Conceptually this is `init`; it is exposed as `/start` because `/init` is a
built-in Claude Code command.

## 0. Detect mode & guard
- If `.workflow/` already exists → the project is already initialised. Do **not** clobber: report current
  state and offer to resume from `.workflow/handoff.md` instead. Stop.
- Else pick the mode: `$ARGUMENTS` if given, otherwise **detect** — existing source files present →
  **brownfield**; empty (or package only) → **greenfield**. **Confirm the detected mode with the user**
  before proceeding (mis-classifying is costly).

## 1. Shared steps (both modes)
1. **repo-setup:** ensure git is initialised (`git init -b main`), a git identity is set, and a
   `.gitignore` exists. If a remote is wanted and `gh` is unauthenticated → raise `checkpoint`(kind=setup)
   → `setup-guide` for `gh auth login`. If already authenticated, create/push directly.
2. **Scaffold the workflow layout** (provisional — EXPAND):
   ```
   .workflow/
     config.json       # project_root + run config      (committed)
     loop.md           # routing graph + diagram        (committed)
     checks.sh         # mechanical-gate runner (generated per-stack; --fix / --check) (committed)
     state.json        # live position — RUNTIME, add to .gitignore
     handoff.md        # durable resume anchor          (committed)
     backlog.md        # live OPEN queue (issues + roadmap; closed leave) (committed)
     checkpoints/      # RESERVED — demoted; no writer yet
   <project_root>/     # the product (greenfield: project/ ; brownfield: repo root)
     llms.txt          # thin agent entry point → docs/knowledge/  (committed)
     rules/            # engineering rules — specialized baseline, subtree-overridable (committed)
     docs/             # docs-root — durable product knowledge
       spec/           # product spec (discuss fills this)   (committed)
       architecture.md # inline Mermaid-C4 (document-owned)  (committed)
       knowledge/      # code map                            (committed)
       decisions/      # decision-records = ADRs (append-only) (committed)
   ```
   `.workflow/items/<id>/` is **not** scaffolded here — `planner` `mkdir`s each per item on demand.
   Add `.workflow/state.json` to the target's `.gitignore`; everything else is committed.
3. **Install the orchestrator brief** (the driver), from the package `templates/`:
   - **greenfield:** copy `templates/orchestrator-CLAUDE.md` → the launch-root **`CLAUDE.md`** (fill
     `<project>`/`<project_root>`) and put the product under **`project/`** (its own `CLAUDE.md` left to the
     product); set `project_root: ./project`.
   - **brownfield:** the product stays at the repo root; wrap `templates/orchestrator-CLAUDE.md` in the
     **sentinel markers** and **append** it to the *existing* root `CLAUDE.md` (never clobber — idempotent via
     the markers); read that existing `CLAUDE.md` as a **primary ingest source**; set `project_root: .`.
   - Copy `templates/loop.md` → **`.workflow/loop.md`** and write **`.workflow/config.json`** (`project_root` +
     run config).
   - Copy `templates/settings.json` → **`.claude/settings.json`** (loop permission rules: `allow` local
     actions, `ask` outward) and `hooks/{guard.sh,pre-commit.sh}` → **`.claude/hooks/`** (guard = secret-scan +
     verify-before-commit hard gates; pre-commit = the mechanical-gate backstop, registered in step 4).
     `build-once-per-wave` is deferred.
   - **Surface the one-time permission message** to the human: *"This is an autonomous loop. Accept the
     workspace-trust dialog so the package can pre-approve the loop's local actions; outward actions
     (push / issues / deploy) will still ask — by design. You don't need `--dangerously-skip-permissions`."*
4. **Specialize rules + wire enforcement** (the disciplined layer — auto-write greenfield, adopt-and-gap-fill
   brownfield):
   - **Seed the rules.** Copy the package baseline `rules/*.md` → **`<project_root>/rules/`**. Detect the
     stack (languages, frameworks, package manager) and rewrite each `— enforced by: <mechanism>` tag with the
     project's *concrete* tool (e.g. `formatter` → `prettier`/`black`/`gofmt`), so the agent reads real commands.
     Nearest-file-wins: this project copy is the floor a subtree `rules/` can override.
   - **Wire the enforcers named by the tags.** For each enforceable principle, install the concrete gate from
     the detected stack: `.editorconfig`, formatter, linter, typechecker (where the language has one), the
     test-runner script, a dependency-audit step, and a **CI workflow** that runs format-check + lint +
     typecheck + test on push/PR. **Greenfield:** write these from the detected stack. **Brownfield:** *adopt*
     what already exists — never clobber a config the project ships; record the existing tool as the enforcer
     in the specialized `rules/`, and only **gap-fill** the missing ones.
   - **Generate `.workflow/checks.sh`** — the one mechanical-gate runner both callers share: a
     `--fix` mode (format + lint-fix + strip a stale reference, for the `commit` skill to run in-loop) and a
     `--check` mode (fail non-zero on residual drift, for the git hook). It wraps the concrete tools just wired.
   - **Register the git backstop.** Install the shipped `pre-commit.sh` as git's `.git/hooks/pre-commit` (copy
     or symlink — git requires the exact name `pre-commit`) so a commit made *outside* the loop still hits
     `checks.sh --check`.
   - **Externals → checkpoint.** Anything needing an account or a provider choice (CI host, deploy creds) is an
     outward/setup step → raise `checkpoint`(kind=setup) → `setup-guide`, don't guess.
5. **Launch the local console.** ⛔ STUB — website stack/screens still open.
6. **Commit** the initialised scaffold.

## 2. Greenfield (new project)  — fully supported
- Scaffold an empty `<project_root>/docs/` (spec, architecture, knowledge, decisions); it grows as the project
  is built.
- Hand off to **`discuss`** (inception) to build the spec from zero → then the normal loop
  (`prioritize → planner → …`).

## 3. Brownfield (integrate existing codebase)  — mostly STUB (EXPAND)
- **Rules + enforcement are already adopted** by shared step 4 (adopt existing configs, gap-fill the missing
  enforcers, layer our `rules/` on top). That is the *habits* half of integration and is **supported now**;
  the **docs → knowledge** half below is the part still stubbed.
- **Ingest** the existing code → populate `docs/knowledge/` (code graph + per-file nodes) and a
  **reconstructed `docs/spec/`**. **Adopt an existing `docs/`** if present — write members to known subpaths,
  never clobber; namespace ours on a name collision. ⛔ STUB — depends on the **ingest mechanics**, still
  open. For now: scaffold an empty `docs/knowledge/` and record a TODO to ingest once the mechanics exist.
- **Reconciliation checkpoint** — surface the reconstructed understanding ("here's what I think the app
  does, its screens, its stack") via `checkpoint` for the user to confirm/correct before the loop drives.
- Then hand to the normal loop.

## Expand later
- Brownfield **ingest** (the real codebase mapping / llm-wiki build).
- The **console** launch.
- The full **disk layout** — the tree above is a provisional first cut.
