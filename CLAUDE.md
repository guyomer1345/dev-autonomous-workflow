# dev-autonomous-workflow — working brief

This repo is the **spec for "the disciplined builder"**: an autonomous-but-disciplined dev workflow shipped as
a pure Claude-Code-native config package (skills + subagents + hooks + slash commands + CLAUDE.md) that a user
runs locally on their own subscription. Master rule: **never sit in Claude's request path.** Six design
spaces — orchestrator · agents · website · checkpoints · shared-state · knowledge.

> This file is working-guidance for editing **this spec repo**. It is *not* the `orchestrator-CLAUDE.md` the
> package ships into target projects (that lives in `templates/`).

## Ground yourself first (read before proposing anything)
- **`11-roadmap.md`** — the complete by-space map of what's left + the phased build sequence (canonical status).
- **`08-decision-log.md`** — every decision D1–D62: the call, why, what was rejected, the evidence.
- Then the numbered spec docs `00`–`10` + `shared/` as the topic needs.

The **spec folder is the source of truth.** Don't duplicate what it already records.

## How we work — design-first
- **Discuss and critique before capturing.** The maintainer writes his own thinking first and wants a *peer*
  who pushes back — **hard critique: find the gaps, say what's missing, no premature agreement.** Prefer crisp
  operational rules over vague wording.
- Keep decisions **in the conversation while in flux.** Only when the maintainer says a slice is closed,
  **capture it**: edit the numbered spec docs **and** add a matching `08-decision-log.md` entry (call · why ·
  rejected · evidence). **Never capture unprompted.**
- The project's own memory law applies to its docs: lean files, pointers not duplication, history in git
  (`shared/memory-model.md`; D38 / D51 / D61).

## Where we are
Foundations + the whole doc-surface pass are closed (D46–D62). For the current phase, read **Recommended
sequence** in `11-roadmap.md` — as of 2026-06-30, **Phase 1 (close the foundations): start with the D36–D45
skill-body deltas.** The 4-phase order: close foundations → define website + demo → build website → build demo.
