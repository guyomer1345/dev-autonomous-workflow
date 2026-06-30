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

## Inspiration / adoption pass — workflow-kit + GSD (session 2026-06-29)

A full read of the user's prior `workflow-kit` (the human-driven `/stage-a → execute → verify → refine →
document` kit that inspired this project), the GSD ("Get Stuff Done") spec-driven system, and best-practice
research. Framing: **both inspirations are human-driven; this project is the autonomous version**, so the
transferable parts are the *content of each phase* and the *discipline gates* — and the gates matter **more**
here, because no human watches each step. Verbosity deliberately **not** taken (their prose is one team's
scar tissue; this roster stays terse, D31).

## D36 — Waves = the collision-model realization **[DECIDED]**
Parallelism (D9) is realized as **waves**: `prioritize` dependency-analyses the ready set, groups independent
items into a wave, runs the wave in parallel, then re-picks; dependent items fall to the next wave. Build
hooks run **once per wave** (parallel agents hitting build tools cause lock contention). Partially closes the
collision open: the *grouping mechanism* is decided; the *independence test* (file/module/area overlap) stays
open.
*Rejected:* ad-hoc per-item independence checks; always-sequential. *Evidence:* GSD waves + user. → `01`,
`10`/`prioritize`, `07`.

## D37 — Execute divergence convergence tiers **[DECIDED]**
`execute`'s divergence handling is tiered: **cosmetic** (helper moved, line drift) → adapt + record;
**discovered-prerequisite-repair** (in-scope-adjacent fix the plan didn't name) → apply as a **separate
commit**, record, continue; **structural** (plan assumes something untrue) → stop + escalate. Preserves
execute's zero-decision invariant — the escalation *is* the decision boundary, and a prerequisite repair is
never silently folded into a planned commit.
*Rejected:* a flat "record a divergence" with no tiering; rolling prerequisite repairs into planned commits
(hides that the executor stumbled into them). *Evidence:* workflow-kit execute taxonomy + user. →
`skills/execute`, `10`.

## D38 — Knowledge/docs design law + three-tier memory invariant **[DECIDED]**
**The law:** a file earns its place only if it holds **non-derivable intent** or is the loop's **cross-session
memory**; everything else is **generated on demand** or **enforced by CI** — because prose rots silently while
code and checks fail loudly. **Three-tier memory invariant** every skill obeys:
- **VOLATILE** — rewrite freely each iteration (`state.json`, `handoff.md`).
- **STABLE** — change only in the **same item as the code that changes it**, CI-gated (`spec/`, diagrams).
- **APPEND-ONLY** — supersede, never edit (`decisions/`, the audit / `# Sessions` stream).
*Rejected:* undated prose docs a human must refresh (the observed rot); Diátaxis's four-quadrant tree
(multiplies surface a loop must keep in sync). *Evidence:* best-practice research (primary: ADR immutability,
CLAUDE.md size discipline, docs-as-code) + the `idea-testing` rot pattern (empty `diagrams/`, undated
research, documented-not-enforced `logging.md`). → `05`, `06`, `shared/memory-model.md`, `07`.

## D39 — Space-6 split: generated structure vs experiential memory **[DECIDED — sharpens D13]**
The two halves of Space 6 sit on opposite sides of D38's law. **Structural code graph = GENERATED**
(tree-sitter/repomap, regenerable, never authoritative prose, never hand-edited — a hand-maintained map goes
stale and lies). **Experiential per-file memory = the only durable hand-written layer** (the non-derivable
`why` + the `# Sessions` postmortems). Names the boundary D13 already leaned toward.
*Rejected:* a hand-maintained structural map; Code Property Graph as agent context (overkill — security-scan
step only). *Evidence:* Aider repomap (generated → cannot drift) + research. → `06`.

## D40 — Baseline rules + `/start` enforcement wiring **[DECIDED]**
The package ships a **thin baseline `rules/`** (code-style / testing / security / ops — *principles only*, not
workflow-kit's volume); projects override via **nearest-file-wins** (package < project < path-scoped).
`/start` **specializes** them per project **and wires the enforcement layer** — `.editorconfig`,
linter/formatter/typechecker config, test runner, and the **CI/hook gates** that make enforceable rules fail
loudly. The orchestrator `CLAUDE.md` (≤~200 lines) holds only non-enforceable behavioural guidance, governed
by the deletion test (*"would removing this line cause a specific mistake? if not, cut it"*). Discipline is
mostly **CI-enforced, not prose** — closes the day-one "no baseline guardrail" gap.
*Rejected:* shipping all discipline as prose (the documented-not-enforced rot); folding everything into
`CLAUDE.md`. *Evidence:* Google eng-practices (nearest-file-wins) + Cursor/Claude rules conventions +
`idea-testing` `logging.md` rot + user. → new package `rules/`, `commands/start`, `10`; complements D34.

## D41 — Diagrams-as-code + loop-owned freshness + prune pass **[DECIDED; mechanisms OPEN]**
Architecture diagrams are **Mermaid C4 L1/L2 inline** in the architecture doc, updated by `document` in the
**same item as the code** (skip L3/L4 — auto-generate the code level). Two freshness behaviours the loop owns:
**staleness must be machine-detectable** (not a date a human forgets) and a periodic **prune pass** (deletion
test over `CLAUDE.md` + `rules/`) in the audit phase — bloat makes the agent ignore its own instructions. The
two **mechanisms are OPEN** (`07`) — decided that they exist, not how.
*Rejected:* separate `.mmd`/binary diagram tools (don't diff); human date-stamps; hand-maintained C4 code
level. *Evidence:* C4 + Mermaid-in-GitHub + the empty `idea-testing` `diagrams/`. → `skills/document`, `06`,
`07`.

## D42 — Plan risk-class + Backup contract **[DECIDED]**
The `plan` carries **`risk_class`** ∈ `{code-only, data-additive, data-destructive, prod-touching}` and, when
destructive, a required **`backup`** block (what / mechanism / verification / restore). `planner` sets the
class; `execute` **refuses** a destructive plan with no verified backup, runs+verifies the backup **before**
the destructive step, and records it. The **local-irreversible** twin of D35 (which gates only outward
actions) — an unattended executor must not run a `DROP`/migration without a proven rollback.
*Rejected:* relying on D35 (covers push/`gh`, not a local destructive op); operator confidence as the gate.
*Evidence:* workflow-kit `risk_class`/Backup, sharpened for unattended execution + user ratify. →
`shared/schemas.md` (plan), `skills/planner`, `skills/execute`.

## D43 — Decision-coverage gate **[DECIDED]**
`planner` cross-checks that **every decision** in the item's decision records maps to **≥1 plan step**; an
unmapped decision **blocks/escalates** the plan. The `plan` gains a `decisions[]` reference so coverage is
machine-checkable; the records live in the product's append-only `decisions/` (D38). Stops resolved intent
from silently evaporating between `discuss`/`decision-engineer` and `execute`.
*Rejected:* trusting decisions to survive into the plan implicitly. *Evidence:* GSD decision-coverage gate +
user ratify. → `shared/schemas.md` (plan), `skills/planner`; connects D24 (`document` ingests the decision
stream).

## D44 — Secret-scan gate in `commit` **[DECIDED]**
Before committing, `commit` scans the staged diff for high-signal secret patterns (key prefixes, private-key
headers, `password|secret|api_key|token` set to a non-placeholder literal); on a hit it **stops and
escalates** rather than committing. An autonomous committer needs this more than a human one — a committed
secret lives in history forever.
*Rejected:* trusting the executor never to stage a secret. *Evidence:* workflow-kit `commit` secret scan +
user; fits D32/D35. → `skills/commit`.

## D45 — Conjunction-of-signals for AI judges **[DECIDED]**
In `adjudicate`: an LLM verdict **gates** (fail/block) only when a **deterministic signal corroborates** it (a
failing test, a thrown error, a lint/type violation, a tree mismatch); an AI-only finding is **advisory /
low-confidence**, never a hard gate. Propagates to `verify` / `debug` / `decision-engineer` (which specialize
`adjudicate`, D24). False-positive control so AI judgment alone can't stall or whipsaw the loop.
*Rejected:* AI-verdict-alone gating. *Evidence:* workflow-kit `verify-ui` conjunction rule, generalized +
user ratify. → `skills/adjudicate`; strengthens D24's confidence-gate.

## D46 — Orchestrator `CLAUDE.md` = the launch-root brief; advisory backbone + hooks enforce **[DECIDED]**
The package's driver is the target project's **root `CLAUDE.md`** (Claude Code's always-loaded,
post-`/compact`-re-injected brief) — "orchestrator" names its *role*, not a separate file; the always-loaded
session at the launch root **is** the orchestrator. Written lean (a frame, not the per-capability *how*), it
encodes: identity + three-layer memory (D4), a pointer to the loop, the read→place→advance control algorithm,
the invariants, checkpoints, handoff. Because `CLAUDE.md` is **advisory context, not enforced configuration**,
the loop *sequence* runs model-on-rails while the **non-negotiable invariants become deterministic hooks**
(no commit before `verify` passes; secret-scan D44; outward-action gate D35; build-once-per-wave D36) — the
brief marks which lines are hook-enforced vs disposition. Exempt from `shared/format.md` (it is the
always-loaded brief, not a typed node) but shares the voice + carries no spec-internal refs (D34).
*Rejected:* `CLAUDE.md` prose as enforced control flow (Claude treats it as context, not config); a
workflow-script driving the whole loop (poor fit for a long-running human-in-the-loop session).
*Evidence:* Claude Code docs (CLAUDE.md advisory; hooks enforce; root survives `/compact`); industry —
hard-code routing, LLM inside nodes (Anthropic *Building Effective Agents*, LangGraph, Step Functions,
Temporal); + user ratify. → `01`, `commands/start.md`, future `hooks/`.

## D47 — Loop graph lives in a pointed-to file; definition vs position **[DECIDED]**
The routing graph (nodes + pass/fail edges + Mermaid diagram) is the single source of truth in
**`.workflow/loop.md`**; the root `CLAUDE.md` carries only a **pointer** and the orchestrator **reads it on
demand** to route. The pointer (plain text) survives `/compact`; the file is read fresh — so we never depend
on `@import` re-resolution (undocumented). Split **definition** (the fixed topology — STABLE) from
**position** (`state.json` — volatile); `loop.md` never accumulates run-history. Each skill keeps a
**one-line local `Route`** (its own successors, self-description); `loop.md` owns the global graph; `10`
stays a design doc, not loaded at runtime.
*Rejected:* inlining the full graph in `CLAUDE.md` (triple-maintenance vs `10` + skill `Route`s);
`@import`-ing the graph (compaction re-resolution undocumented); stripping `Route` from skills (breaks D31
format, makes skills non-self-describing).
*Evidence:* single-source-of-truth for the graph (LangGraph `StateGraph`, Step Functions ASL, Airflow DAG);
Claude Code `@import` is eager + 4-hop but compaction behaviour unconfirmed; + user (his "point at a live
graph file" proposal). → `01`, `05`, `.workflow/loop.md`.

## D48 — Resume/state model: volatile pointer + durable anchor + git log **[DECIDED]**
"Where am I in the loop" splits per durable-execution practice: **`state.json`** = the volatile live pointer
(item / phase / wave; gitignored console view, rewritten in place); **`handoff.md`** = the durable resume
anchor (program counter — current item + loop position + parked work, committed); **git history** = the
append-only completed-step log (each item ends in a `commit`, D32). Mid-run reads `state.json`; a cold start
reads `handoff.md` + `git log` and rebuilds. Replay is idempotent — `prioritize` (pure queue, D26) never
re-picks a committed item.
*Rejected:* `handoff.md` only (conflates console view + anchor, loses live state); `state.json` only
(gitignored — not durable across clone/machine, too fragile as the authority).
*Evidence:* Temporal event-sourced history + replay; LangGraph checkpoint `next` pointer + idempotency keys;
Martin Fowler event sourcing; + user ratify. → `01` (session lifecycle), `05`.

## D49 — Per-mode repo layout; the launch-root constraint **[DECIDED]**
Only the **launch-root `CLAUDE.md`** (and parents) is always-loaded + re-injected post-`/compact`; a subdir
`CLAUDE.md` loads on-demand and is not restored. So the orchestrator brief must be the launch-root brief, and
layout splits by mode (D28/D29): **greenfield** — the launch root holds the orchestrator `CLAUDE.md` +
`skills/`/`agents/`/`commands/`/`loop.md`, and the product lives in **`project/`** with its own untouched
`CLAUDE.md`. **brownfield** — the product stays at the repo root (no relocation), the workflow machinery is
added in subdirs, and the orchestrator framing is a marked block in their root `CLAUDE.md` (D50). A committed
**`.workflow/config.json`** carries `project_root` (`./project` | `.`) so code-touching skills stay
path-agnostic.
*Rejected:* always-product-subdir (relocating a live brownfield repo breaks paths/CI + nested-git friction);
always-flat-root + marked block (gives up the clean greenfield `CLAUDE.md` separation).
*Evidence:* Claude Code load/compaction hierarchy (only launch-root re-injected); + user (his `workflowdir/`
+ `project/` proposal) + ratify. → `commands/start.md`, `05`, `10`.

## D50 — Brownfield `CLAUDE.md` install = inline marked self-gating block **[DECIDED]**
Integrating into a project that already has a root `CLAUDE.md`, `/start` **appends a sentinel-marked block**
to it (inline = guaranteed `/compact` survival), idempotent on install/update/uninstall via the markers,
never touching user content. The block **self-gates** ("act as orchestrator only when a run is active; else
an ordinary session") so casual human sessions in the repo aren't hijacked. The existing `CLAUDE.md` is also
read as a **primary ingest source** for `rules/` + the reconstructed `spec/` (highest-signal artifact in the
repo).
*Rejected:* `@import`-ing a separate orchestrator file (cleaner separation, but compaction re-resolution
undocumented — too risky for the bootloader; kept as a cheap one-session test to adopt later); always-on
(no self-gate — intrusive on a shared repo).
*Evidence:* root text survives `/compact` (confirmed) vs `@import` (unconfirmed); marked-block idempotency
precedent; + user. → `commands/start.md`, `06` (ingest).

## D51 — Always-read files bounded by construction; retention law deferred **[DECIDED + OPEN]**
The files the orchestrator reads **every turn** — root `CLAUDE.md`, `state.json`, `handoff.md`, `loop.md` —
are **rewritten in place, never appended to**: current state only, no history, within a small size budget
(history lives in git). The master rule (context is scarce, D3) applied to disk. The complementary
**retention & archival law** for the genuinely unbounded set — the **append-only** tier (`decisions/`, the
`# Sessions` stream) + `backlog.md` closed items, plus indexed retrieval for large `.knowledge/`/`spec/` — is
**deferred to its own pass** and **closes D41** (prune-pass + staleness mechanisms); the cheap archive is
rollup-and-link with git as the cold store.
*Rejected:* letting any always-read file accumulate history (fatal to context).
*Evidence:* master rule (D3); D38 tiers (only append-only grows unbounded); + user (raised the growth-bound
concern). → `shared/memory-model.md`, `01`; OPEN → `07`/D41.

## D52 — Orchestrator dogfood: the driver is validated **[DECIDED — validated]**
A throwaway greenfield repo (`~/Documents/dogfood-orchestrator`) was scaffolded with the package + authored
`CLAUDE.md`/`loop.md`/`config.json`, and Claude **drove it as the orchestrator** (design-drive simulation)
across two tasks — a happy-path feature (G1) and a fail/decision feature (G2). The `read → place → advance`
control algorithm held across **both** the happy path and the failure/decision/human-gate paths
(`decision-engineer → research → decision-record`; `verify-fail → debug → refine → planner → execute →
re-verify-pass`; a real qa `checkpoint`; `create-issue → close-issue` with outward gating). Confirmed live:
the loop-graph pointer (lean `CLAUDE.md` + on-demand `loop.md`); the resume model (cold-start reconstruction
from `handoff.md` + `git log`); gitignored `state.json`; plan-declared QA (D30 — G1 no checkpoint, G2 one);
conjunction-of-signals (D45 — a real `KeyError` gated, not an AI hunch). Surfaced findings → **D53–D57**.
*Evidence:* two-task simulation, real Bash/edits/commits (3 clean commits). → `10` build status.

## D53 — Disk layout + artifact/state schemas (dogfood) **[DECIDED]**
Closes `schemas.md`'s "paths TBD." **Per-item working artifacts** live under `.workflow/items/<id>/`
(`plan.md`, `changelog.md`, `verdict.md`, `debug-report.md`); **per-type append-only records** stay global
(`.workflow/decisions/`, `.workflow/checkpoints/`). The **resume contract** gets real schemas: `state.json`
`{ status, node, current_item, wave, note }` (`node` ∈ the `loop.md` node labels) and `handoff.md`
`{ current_item, loop_position, parked[] }`. Rule: per-item ephemeral artifacts are item-scoped; cross-item
memory is type-scoped.
*Rejected:* a flat `.workflow/` (plan/changelog/verdict collide across items); leaving paths TBD (resume needs
a defined `state.json`). *Evidence:* dogfood (had to invent `items/<id>/`). → `shared/schemas.md`, `05`.

## D54 — Item-tail ordering: bookkeeping rides the item commit **[DECIDED]**
The completion tail flips the backlog item → **done** and rewrites `handoff.md` **before** `commit`, so the
durable bookkeeping is captured by the item's own commit. (Sim-1 committed first and left them orphaned;
sim-2 with flip-first produced a clean tree.) `close-issue` is the one **post-commit** step (it needs the
commit SHA) and writes no loop-bookkeeping (see D55).
*Rejected:* commit-then-flip (orphans durable files); a separate bookkeeping commit (breaks
one-commit-per-item). *Evidence:* dogfood (clean vs dirty tree). → `01`, `10`, `skills/commit`.

## D55 — GitHub owns issue open/closed state **[DECIDED]**
The backlog `issue` carries only `github_ref` (+ local `kind`/`severity`/`source`); the **open/closed state
lives in GitHub**, not duplicated in `backlog.md`. So `close-issue` (post-commit) changes no local
loop-bookkeeping — it just closes the GitHub issue + comments the SHA. Removes the post-commit orphan and a
stale duplicate.
*Rejected:* mirroring `state ∈ {open,closed}` locally (duplicates state an external system owns → drift +
post-commit bookkeeping). *Evidence:* dogfood (the close-issue ordering snag). → `shared/schemas.md` (issue),
`skills/close-issue`, `skills/create-issue`, `shared/memory-model.md`.

## D56 — `decision-record` id + machine-checkable coverage **[DECIDED — sharpens D43]**
The `decision-record` gains an **`id`** (e.g. `D-001`); `plan.decisions[]` holds those ids; the D43 coverage
gate checks each id maps to ≥1 step. Makes the decision↔plan link real, not convention.
*Rejected:* referencing decisions by prose/title (not machine-checkable). *Evidence:* dogfood (the plan's
`decisions:[D-001]` had no id field to point at). → `shared/schemas.md` (decision-record, plan).

## D57 — Package install location for MVP **[DECIDED — partial]**
The capability package installs as **loose `.claude/` files** in the target — `.claude/commands/`,
`.claude/skills/<name>/SKILL.md`, `.claude/agents/<name>.md` — so `/start` + skills are harness-discoverable;
`shared/` co-locates and is referenced by relative path. Resolves the D25/D49 "at the launch root" ambiguity
for MVP. **Open:** plugin packaging (`.claude-plugin/plugin.json`) + robust `shared/` resolution.
*Rejected:* package dirs at the bare repo root (Claude Code discovers commands/skills under `.claude/`).
*Evidence:* dogfood install. → `10`, `commands/start.md`; OPEN → `07`.

## D58 — Autonomous permission model: shipped allowlist + `ask` gate + guard hook **[DECIDED]**
The harness-real `/start` ran but **prompted constantly for routine local actions** (fatigue) and **pushed to
`origin/main`** — the outward gate (D35) wasn't enforced (advisory prose only), so it collapsed into the same
prompt stream and got approved. Both are one problem: permission-prompts as the *only* enforcement. Fix
(Claude Code best practice): the package **ships `.claude/settings.json`** with `permissions.allow` **broad for
local** work (`Bash` + `Edit`/`Write`/`Read` + `Task`/`Web*`) → prompt-free, and a **thorough `ask` list** for
**outward** actions (`git push`, `gh`, publish/deploy/cloud CLIs, `ssh`/`scp`/`rsync`, `curl`/`wget`) → a
deliberate gate. (Broad-allow chosen over an enumerated safelist because per-toolchain enumeration can't
anticipate every project and `cd x && cmd` chaining defeats prefix-matched allows.) Precedence is **deny > ask > allow**,
so local runs silently while outward always asks — exactly D35, *without* full bypass. The "never do this"
gates become a **PreToolUse hook** (`hooks/guard.sh`): **secret-scan** (block a staged secret) +
**verify-before-commit** (block a commit whose item's verify failed) — legitimate hard-blocks (exit 2, which
overrides allow and fires even under bypass). `/start` surfaces a **one-time message** (accept the
workspace-trust dialog; outward stays gated; you don't need `--dangerously-skip-permissions`). Modes are
**user-controlled** — a `CLAUDE.md`/command cannot set them, so `/start` only recommends.
*Rejected:* recommending full `--dangerously-skip-permissions` (auto-approves outward → destroys D35);
hard-blocking `git push` in the hook (kills the approve-and-push flow — outward is an *ask*, not a forbid);
leaving gates as advisory prose (the run pushed). *Still open:* **build-once-per-wave** (a wave-coordinator,
not a command gate) and **outward gating under full bypass** (needs the console/bus checkpoint-queue).
*Evidence:* dogfood `/start` (constant prompts + a push to `origin/main`); Claude Code permission/hook docs
(deny>ask>allow; hooks precede + override permission rules; modes user-controlled). → `commands/start.md`,
`templates/settings.json`, `hooks/guard.sh`, `01`, `10`, `07`; realizes D46, protects D35.

---

## Not yet decided (tracked in `07`)
Knowledge graph regenerate-vs-incremental; model/effort map; collision **independence test** (waves grouping
decided, D36); Arbiter input contract; autonomous reset mechanism; website stack. Intake follow-ons:
engineering-feasibility pass; demo-skill mechanics; commitment-status storage. `init` follow-ons: brownfield
ingest, console launch, full disk layout (incl. `spec/`+`.knowledge/` placement). Skill-review follow-ons:
incidental-issue-resolution detection — deferred; outward-action permission mechanics (D35). Adoption
follow-ons (D38–D51): the **retention & archival law** + the **prune-pass** mechanism + the
**staleness-detection** signal (D41/D51), and whether `verify` samples the real diff vs trusts the
`changelog` (#8). All → `07`.
