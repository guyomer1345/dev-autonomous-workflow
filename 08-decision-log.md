# 08 — Decision Log (provenance)

Every decision from the planning conversation: the call, why, what was rejected, and the evidence.
This folder is the source of truth and supersedes prior-session memory where they conflict.

## D1 — This spec folder is the source of truth **[DECIDED]**
The decisions captured here (originally from the planning conversation) supersede prior-session memory /
architecture notes where they conflict; prior memory is background, re-verified here. *Evidence:* user
instruction.

## D2 — Build shape: pure Claude-Code-native config package **[DECIDED]**
Skills + subagents + hooks + slash commands + MCP + CLAUDE.md, run locally on the user's own
subscription. NOT a program that drives Claude.
*Rejected:* own-loop-on-raw-API; headless cockpit + website + watchdog that drives Claude (both sit in
the request path).
*Evidence:* master rule (D3); GSD / Spec Kit precedent (config packages, ~64k / 112k stars).

## D3 — Master rule: never in Claude's request path **[DECIDED]**
Everything local; components talk via local bus + files, never by routing Claude. A hosted router on
behalf of users = prohibited.
*Evidence:* Anthropic ToS posture (third-party routing banned); carried from prior analysis, reaffirmed.

## D4 — Agents persist (correction) **[DECIDED]**
Agents hold context and are re-messageable (SendMessage); not one-shot/stateless → three-layer memory
model; orchestrator stays a thin router.
*Rejected:* the earlier "ephemeral/stateless subagents" assumption.
*Evidence:* current harness Agent/SendMessage capability; user confirmation. (A research agent repeated
the stale "stateless" claim — flagged and overridden.)

## D5 — Six-space decomposition **[DECIDED]**
Orchestrator / Agents / Website / Checkpoints / Shared disk state / Knowledge structure. Shared state
added (5th) as the connective tissue for local-only comms; Knowledge added (6th) at user's request.
*Evidence:* planning conversation.

## D6 — Open-question-resolution pattern **[DECIDED]**
planning → up to orchestrator → Investigation → Arbiter → back down; keeps the orchestrator clean.
"Arbiter" chosen over the placeholder "sequential decision maker."
*Evidence:* user's described flow.

## D7 — Operating scope: single local project / user / machine **[DECIDED]** (A1)

## D8 — Human-in-the-loop: two modes + checkpoints **[DECIDED]** (B1)
Inception (heavy) + Steering (ongoing) + in-flight checkpoints.

## D9 — Concurrency: parallel by default, serialize on collision **[DECIDED]** (B2)
→ collision model needed.

## D10 — Session lifecycle + graceful handoff **[DECIDED]** (B3)
Start command boots orchestrator + website; finite context → graceful handoff (park → document →
commit → write `handoff.md`). Reset is now definitively understood:
- Pure config **cannot** self-`/clear`/restart (`/clear` is human-only; no hook/MCP/setting; `/compact`
  + delegation ceiling ~300–500 turns / ~2–4 hrs).
- **MVP path:** website prompts human to `/clear` + restart from `handoff.md` (one click).
- **Full-autonomy path (optional, deferred):** a thin local SDK runner triggers handoff + restart with
  no human action — the only path to true overnight autonomy.
- Correction to earlier framing: the runner does **not** break the master rule. The rule bans routing
  *others'* Claude via a hosted service; a locally-run runner on the user's own auth (even if published,
  each user runs their own) is ordinary individual use. Tradeoff is purity, not legality. Caveat: verify
  SDK subscription-vs-API-key auth when building it.
*Evidence:* B3 research, definitive, doc-cited.

## D11 — No fixed dogfood target **[DECIDED]** (C1)
General design from cross-project use, not built around one project. *Evidence:* user.

## D12 — Comms: local HTTP loopback bus **[DECIDED]** (A3)
Bus = website's local backend; `state.json` for the viewer; checkpoints = explicit wait-on-bus steps.
File-watching rejected for control-flow.
*Evidence:* A3 research (native-primitive + general-IPC angles).

## D13 — Knowledge format: OKF-adapted + LLM-Wiki pattern + llms.txt manifest **[DECIDED]** (D1)
`.knowledge/` dir; per-file nodes; typed edges with `why`; `# Sessions` log; `graph.json`; steal
Aider's tree-sitter extraction for structural edges. Maintenance model deferred.
*Evidence:* D1 research + prior art (Aider repomap, Code Property Graph).

## D14 — MVP scope line **[DECIDED]**
*In:* loop, persistent agents, website, manual checkpoints + help, knowledge base, graceful handoff.
*Out (designed-for):* automated testing, test-from-anywhere, paid device/QA platform.

## D15 — Spec-only; exported to a clean folder **[DONE]**
No implementation during planning. The spec was written in the planning chat, then moved to its
permanent home (`dev-autonomous-workflow/`) — now the source of truth, edited directly. *Evidence:* user.

---

## Intake stage (session 2026-06-29; full detail in `09`)

## D16 — One spine, variable-depth intake **[DECIDED]**
The two work-loops (existing project / new project) converge on a single autonomous execution spine; the
only variable is intake depth (bug → shallow, feature → short, inception → deep). Inception's output is a
backlog → Roadmap sequences it → steady-state spine; Steering injects new items into the same backlog.
*Rejected:* modeling them as two independent loops. *Evidence:* this session; consistent with D8. → `09`.

## D17 — Definition-of-done is the autonomy gate **[DECIDED]**
Every task carries testable acceptance criteria; that (not the task type) is what makes it safe to run
unattended and gives checkpoints + test/audit something to verify against. *Evidence:* this session. → `09`.

## D18 — Three intake types + contracts **[DECIDED]**
Bug / feature / project, each with a distinct intake contract = what the user must supply before the work
goes autonomous. *Evidence:* user's task taxonomy. → `09`.

## D19 — Bug intake contract **[DECIDED]**
Autonomous-found = already reproducible → fully autonomous fix; user-reported = explained-until-reproducible
OR full-flow (the latter ends with a user-verify checkpoint); non-reproducible-after-explanation → guided
diagnosis WITH the user, never blind fix-then-verify. A fix's DoD includes a regression test. "Can replicate
≠ knows what's correct" → autonomous fixing needs recorded intent (Space 6).
*Rejected:* "reproducible ⇒ safe to autonomously fix" as sufficient. *Evidence:* user + this session. → `09`.

## D20 — Required inception fields incl. audience + runtime **[DECIDED]**
Inception must capture tech stack, screens, purpose, features, **plus audience (who) and runtime/environment
(where)** — the product-side framing of engineering constraints — and data model + integrations. Output =
vision + spec + prioritized backlog. Audience/runtime feed an engineering-feasibility capability ("engineer
agent" — role real, exact agent OPEN). *Evidence:* user. → `09`, `02`.

## D21 — Demo/sandbox = throwaway product-alignment checkpoint **[DECIDED]**
A "create demo" skill emits a throwaway, minimal, non-integrated sandbox surfaced as a checkpoint;
feature-demo and project-demo are one primitive at two scales. It de-risks the *product* question only
(certifies the visual/behavioral subset of the spec), NOT engineering. Spec-first / demo-validates: the demo
is generated from the spec, change requests edit the spec and regenerate it (refine loop), and the spec state
behind the approved demo is what gets locked. Throwaway by default (no reuse as the real scaffold). Fidelity
matches the question (low-fi first).
*Rejected:* demo as the spec's producer; demo as design/engineering validation; reusing the sandbox as
scaffold. *Evidence:* user + this session. → `09`.

## D22 — The sandbox gate **[DECIDED]**
Sandbox iff (①) it's an open product decision the user owns, (②) it changes a user-visible surface, and (③)
the look/behavior is underdetermined (new pattern w/o precedent OR two materially-different valid builds).
Default = no sandbox; a genuine fence at ③ → a one-line ask. System-discovered work is never sandboxed
(escalated as steering instead). *Evidence:* user examples (A/B) + this session. → `09`.

## D23 — Three-state commitment model **[DECIDED]**
Every spec element is locked / provisional / unspecified, which dictates how a later deviation is treated:
locked → bug/drift; provisional → expected (and spawns a finalize-later backlog item — tracked debt);
unspecified → undefined behaviour → steering question, unless it hits a universal invariant
(crash / data-loss / security / broken core flow) → bug. Status defaults by fidelity + category, overridable.
Provisional changes must not trip the Space 6 drift check.
*Rejected:* monolithic demo approval; treating every demo detail as locked. *Evidence:* user's
locked-vs-change-later distinction + edge-case=undefined agreement. → `09`, `06`.

---

## Roster → package (session 2026-06-29; map in `10`, contracts in the package files)

## D24 — Capability roster v1 + skill/agent taxonomy + adjudicate base **[DECIDED]**
Derived by walking a full new-project loop end-to-end. 16 capabilities, each with an I/O contract (its
package file) over shared artifact schemas (`shared/schemas.md`); loop order + call-graph pinned (`10`).
- **skill** = procedure/controller (the *how*); **agent** = context-heavy persistent worker (D4).
  Controllers dispatch workers (e.g. `debug` the skill fans out mapping + `research` agents).
- **adjudicate** = one base skill (gather views → judge → confidence-gate → loop/escalate), specialized by
  `verify` / `debug` / `decision-engineer` — the Investigation→Arbiter pattern (D6) reified; collapses the
  prior Arbiter / engineer-agent / decision-engineer overlap into one adjudicator.
- `refine` routes corrections back through `planner`→`execute` (never fixes directly — preserves execute's
  zero-decision invariant); `verify` (artifacts) vs `debug` (runtime) split by object; one `checkpoint`
  gate behind demo/qa/setup; `planner` has decompose + plan-one modes; `document` ingests the
  decision/event stream, not just the changelog.
*Closes the `02` roster open item.* *Rejected:* a flat capability list with overlapping deciders; `refine`
as a second executor. *Evidence:* the dry-run walkthrough + user confirmation. → `10`, `02`.

## D25 — Package layout = Claude-Code-native plugin source **[DECIDED]**
The distributable is a CC-native plugin: `skills/<name>/SKILL.md`, `agents/<name>.md`, `shared/schemas.md`
at the repo root (later `commands/`, `hooks/`, `CLAUDE.md`, `.claude-plugin/plugin.json`). The repo is now
both the spec (`00`–`10`) and the package source. *Evidence:* user ("the Claude Code native default").
→ `10`, `05`.

## D26 — Interrupt model: pure queue **[DECIDED]**
The scheduler never self-preempts. In-flight work always runs to its item boundary, then `prioritize`
re-picks; ordering is urgency × dependency-readiness. Rationale: a critical bug found mid-execution is the
current item's own `verify→debug→refine` loop, not a competing backlog item, so preemption never applies;
a genuinely external emergency is handled by the human's manual override (steering), not by the machine.
This removes all parking / mini-handoff / anti-thrash machinery from `prioritize`.
*Rejected:* always-preempt (thrash); tiered-preempt-on-universal-invariants (over-engineered for MVP —
revisit only if the deferred overnight-autonomy runner makes the bounded wait unacceptable).
*Evidence:* user. → `10`, `09`.

## D27 — Agent topology: agents are leaf workers; adjudicators are skills **[DECIDED]**
**skill** = controller/procedure, run by the orchestrator, may dispatch agents. **agent** = a leaf worker
with its own tools that never spawns sub-agents. Consequences: the only agents are `research` and
`setup-guide`; all adjudicators (`verify`, `debug`, `decision-engineer`) are skills — so `decision-engineer`
is reclassified skill (was agent in the first roster draft). *Closes the `02` topology open question:*
strict hub-and-spoke, agents don't spawn agents. *Evidence:* surfaced writing the package files; user-flagged.
→ `10`, `02`.

## D28 — `init` / bootstrap capability **[DECIDED in principle]**
The workflow's start command (D10) is a capability `init` with two modes: **greenfield** (repo-setup →
scaffold workflow structure → launch console → hand to `discuss`) and **brownfield/integrate** (the above
plus an **ingest** pass that builds the initial Space-6 knowledge base + reconstructed spec from existing
code — "map to our standard"). `repo-setup` folds in as a step; `gh auth` and similar are `checkpoint`
(kind=setup) walkthroughs. Brownfield ingest depends on the still-open knowledge-ingest mechanics (`06`).
*Evidence:* user. → `10`, `01`, `06`.

## D29 — `init` / `/start` bootstrap, design v1 **[DECIDED — partial; expand]**
The bootstrap capability (D28) is realised as a human-invoked **slash command `/start`** (conceptually
"init"; not `/init`, which is a Claude Code built-in) → `commands/start.md`. Adds a third primitive class:
**commands = human-invoked entry points** (alongside skills = model-invoked, agents = leaf workers, D27).
- **Mode detect + idempotency:** detect greenfield (empty) vs brownfield (existing code), confirm with the
  user; if `.workflow/` already exists, don't clobber (offer resume from `handoff.md`).
- **Shared steps:** repo-setup; scaffold the workflow layout; install orchestrator framing (CLAUDE.md —
  STUB); launch console (STUB); commit.
- **Greenfield:** empty spec/knowledge → hand to `discuss` (inception). **Fully buildable now.**
- **Brownfield:** ingest existing code → `.knowledge/` + reconstructed spec, then a reconciliation
  checkpoint. **Mostly STUB** — depends on the open Space-6 ingest mechanics (`06`).
- **Provisional disk layout (Space 5, EXPAND):** `.workflow/` (state.json runtime/gitignored; handoff,
  backlog, decisions/, checkpoints/ committed) + `spec/` + `.knowledge/`.
*Evidence:* user (design what's buildable now, note the rest to expand). → `10`, `01`, `05`, `06`.

## Skill review + format pass (session 2026-06-29)

## D30 — Human QA is plan-declared, not a blanket post-verify gate **[DECIDED]**
The plan owns the "does a human need to look at this?" decision, upstream where intent lives. Each
`acceptance_criterion` is tagged `gate: artifact | human-qa`: `artifact` criteria are checked by
`verify`; `human-qa` criteria are confirmed by a `checkpoint` (kind=qa) on the live app. `verify` stays a
**pure artifact check** and always routes `pass → document/commit`; the orchestrator inserts a qa
checkpoint *only* when the plan declared ≥1 `human-qa` criterion. Most changes (internal/refactor) declare
none and flow straight through — no human gate after every verify.
*Rejected:* the old `verify` route `pass → checkpoint (human QA) → document/commit`, which implied
mandatory human QA on every pass; a `needs_human_qa` flag computed *by* verify (puts product-intent logic
into an artifact checker). *Evidence:* user, this session. → `shared/schemas.md` (plan), `skills/verify`,
`skills/planner` (tags the gate), closes the `04` open item "who decides a checkpoint is needed" for kind=qa.

## D31 — Canonical authoring format for skills & agents **[DECIDED]**
Every package file follows one canonical shape so the roster reads as a graph of typed nodes
(`Inputs → … → Output → Route`). A **menu, not a mandatory skeleton**: a required spine + optional sections
included only when they earn their tokens. Definitions live in the contract sections (Inputs/Output name
`schemas.md` artifacts) — the current files are under-*defined* (jargon like `adjudicate`, implicit artifact
contents), not under-described; the fix is defining contracts, not adding prose. Recorded in
`shared/format.md`; imperative node-names kept on purpose (they double as routing-graph labels).
*Rejected:* a mandatory all-sections skeleton (fights "concise is key", forces padding); the
background-research read of "don't template at all" (over-applies generic large-skill guidance to small
orchestrated nodes — Anthropic separately endorses a "cohesive skill library"); "describe more" via prose.
*Evidence:* Anthropic skill-authoring best-practices doc + this session. → `shared/format.md`, applied
skill-by-skill starting with `verify`.

## D32 — Commit message convention **[DECIDED]**
`commit` writes **Conventional Commits** + linking trailers. Type from the item's `kind`
(`bug → fix`, `feature → feat`, `debt → refactor`/`chore`); `Refs: item #<backlog-id>` always;
`Closes: #<gh-issue>` when the commit resolves a tracked issue. Rationale: the commit log becomes
machine-readable loop state, and the trailer is the hinge `close-issue` keys off.
*Evidence:* user. → `skills/commit`.

## D33 — Issue lifecycle: real GitHub issues + close-at-commit-tail **[DECIDED]**
`create-issue` **dual-writes**: files the backlog `issue` **and** opens a real GitHub issue
(`gh issue create`, labels from `kind`/`severity`), storing the number as `issue.github_ref`. GitHub is the
durable external tracker; the backlog references it. A new leaf-tail skill **`close-issue`** closes the
resolved issue at **item completion (commit tail)** — not after `execute` (which runs pre-`verify`, so
closing there would retire work that may still fail). MVP: close the completed item's own `github_ref` 1:1
and comment the commit SHA.
*Rejected:* closing after `execute` (wrong point in the loop); relying on the `Closes:` commit keyword to
auto-close (only fires once pushed, and push is out of `commit`'s scope, so an explicit `gh issue close` is
needed regardless); building incidental-resolution detection now (deferred).
*Evidence:* user (delegated the create-issue mechanics), this session.
→ `skills/create-issue`, `skills/close-issue` (new), `shared/schemas.md` (issue), `10`.

## D34 — Package files carry no spec-internal references **[DECIDED]**
The shippable package (`skills/`, `agents/`, `shared/`) states behaviour and rationale in plain language
with **no spec-internal citations** — neither decision IDs (`Dxx`) nor design-doc numbers (`05`, `09`, …).
Those are provenance and live only in the numbered design docs (`00`–`10`) and this log. Provenance is
**one-directional**: the log names the file a decision governs; the file never cites back (only the
citation is removed — the rationale stays inline). Temporary markers are fine *during* design, not in the
finished file.
*Rejected:* leaving internal IDs in package files (leaks design-process artifacts into the runtime context,
costs tokens, means nothing to a Claude using the skill). *Evidence:* user, this session.
→ applied across `skills/`, `agents/`, `shared/`; rule added to `shared/format.md`.

## D35 — Local work autonomous; outward actions gated **[DECIDED]**
The workflow runs **local/reversible work autonomously** (edits, `commit` — local only) but **gates every
outward, side-effecting action behind explicit human permission**: `git push`, `gh issue create`
(`create-issue`), `gh issue close` (`close-issue`), and later deploys / message-sends. The loop **never
stalls** on this — it keeps committing locally and **queues** outward actions for approval; one approval can
release a batch. **Default = gated** (a checkpoint-style "authorize an outward action" — a new flavour
distinct from demo/qa/setup, which verify or do); users may **opt into standing pre-authorization**, a
config allowlist exactly like Claude Code's own Bash permission rules.
*Why:* validated live this session — the harness let commits proceed but **gated a push to `main`** and
required explicit human auth. Mirrors the master rule (D3) and the existing commit/push split (commit =
autonomous checkpoint marker; push = beyond the skill).
*Rejected:* treating push / `gh` actions as fully autonomous (publishes irreversibly; surprises the user;
would demand standing outward permission they may not grant). *Mechanics OPEN → `07`* (per-action vs
standing, batching, which checkpoint kind).
*Evidence:* user + live harness behaviour, this session. → `04`, `skills/commit`, `skills/create-issue`,
`skills/close-issue`, `07`.

---

## Not yet decided (tracked in `07`)
Knowledge maintenance / ingest mechanics; model/effort map; collision details; Arbiter input contract;
autonomous reset mechanism; website stack. Intake follow-ons: engineering-feasibility pass; demo-skill
mechanics; commitment-status storage. `init` follow-ons: brownfield ingest, console launch, orchestrator
CLAUDE.md, full disk layout. Skill-review follow-ons: incidental-issue-resolution detection (`close-issue`
beyond 1:1) — deferred; outward-action permission mechanics (D35) — see `07`.
