# 04 — Checkpoints (Space 4: the manual human-test gate)

## MVP scope **[DECIDED]**
Structured **manual** checkpoints surfaced through the website. Flow:

> orchestrator hits a checkpoint → blocks (waits on the bus) → posts to the website WHAT to verify and
> HOW (doc links, screenshots of where a setting lives, step-by-step) → optionally a screen-share so
> Claude gives live feedback → human reports pass/fail + notes → bus delivers the verdict →
> orchestrator resumes.

## Block/resume mechanism **[DECIDED — A3 research]**
A checkpoint is an **explicit orchestrator step that waits on the local bus** for the verdict — NOT a
hook exit-code trick (a `Stop` hook exiting 2 forces *continue*, not pause).

## Motivating example (user)
Setting up a Polar account: each time Claude said to change a setting, the human had to go find exactly
where it lives in Polar's docs/UI. The workflow should instead surface the doc location / a screenshot,
or take a screen-share and give live feedback.

## To close **[OPEN]**
- **What a checkpoint IS** (the data model) — awaiting more examples from Guy.
- What triggers a checkpoint (who decides one is needed). *(kind=qa resolved — the plan's `human-qa`-gated
  acceptance criteria, D30; demo/setup triggers still open.)*
- Which help features are MVP (doc links / screenshots / screen-share / live feedback).

## Out of scope (designed-for, not built) **[DEFERRED]**
Automated testing; test-from-anywhere (run-while-away → test env → Cloudflare tunnel → phone ping);
the paid device/QA platform.
