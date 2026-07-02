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

## D41 — Diagrams-as-code + loop-owned freshness + prune pass **[DECIDED — mechanisms closed by D61]**
Architecture diagrams are **Mermaid C4 L1/L2 inline** in the architecture doc, updated by `document` in the
**same item as the code** (skip L3/L4 — auto-generate the code level). Two freshness behaviours the loop owns:
**staleness must be machine-detectable** (not a date a human forgets) and a periodic **prune pass** (deletion
test over `CLAUDE.md` + `rules/`) in the audit phase — bloat makes the agent ignore its own instructions. The
two **mechanisms are OPEN** (`07`) — decided that they exist, not how.
*Rejected:* separate `.mmd`/binary diagram tools (don't diff); human date-stamps; hand-maintained C4 code
level. *Evidence:* C4 + Mermaid-in-GitHub + the empty `idea-testing` `diagrams/`. → `skills/document`, `06`,
`07`.
*Closed by D61:* the prune-pass + staleness-detection mechanisms are cap-and-archive + a script/LLM-split
`audit` pass; distillation deferred.

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

## D49 — Per-mode repo layout; the launch-root constraint **[DECIDED — docs-root sliver closed by D62]**
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

## D51 — Always-read files bounded by construction; retention law deferred **[DECIDED — retention closed by D61]**
The files the orchestrator reads **every turn** — root `CLAUDE.md`, `state.json`, `handoff.md`, `loop.md` —
are **rewritten in place, never appended to**: current state only, no history, within a small size budget
(history lives in git). The master rule (context is scarce, D3) applied to disk. The complementary
**retention & archival law** for the genuinely unbounded set — the **append-only** tier (`decisions/`, the
`# Sessions` stream), plus indexed retrieval for large `.knowledge/`/`spec/` — is
**deferred to its own pass** and **closes D41** (prune-pass + staleness mechanisms); the cheap archive is
rollup-and-link with git as the cold store.
*Rejected:* letting any always-read file accumulate history (fatal to context).
*Evidence:* master rule (D3); D38 tiers (only append-only grows unbounded); + user (raised the growth-bound
concern). → `shared/memory-model.md`, `01`; OPEN → `07`/D41.
*Amended by D59:* `backlog.md` reclassified as a live open queue (closed items leave, GC'd by `prioritize`) —
removed from the append-only retention set above; only `decisions/` + the `# Sessions` stream remain unbounded.

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

## D59 — Write-law leak closures (Layer 0 of the retention pass) **[DECIDED]**
Before the retention *read* law (D41) can land, the *write* law (D38) had unwired leaks — append-only
artifacts with no writer, no on-disk home, or no stated write-mode. A three-agent doc-surface sweep mapped
them; closed as one set:
1. **Per-item dirs are created on demand.** `planner` (plan-one) `mkdir`s `.workflow/items/<id>/` when it
   writes the first per-item artifact (`plan.md`). `start.md` cannot scaffold `items/<id>/` — no `<id>`
   exists at init and git ignores empty dirs — so it scaffolds only the `items/` *role*, not an instance.
2. **`backlog.md` is a live open queue, not append-only** (corrects D51). Rewrite-in-place; closed items
   **leave** — `prioritize` GCs at pick time (drops roadmap items `commit` flipped done; filters `issue`
   entries whose `github_ref` is closed), honoring D55 (close-issue still writes no local bookkeeping). It is
   read on-demand by `prioritize`, bounded by open-WIP, not by age.
3. **`research` heavy notes are ephemeral scratch** with no durable home — the durable distillate is the
   caller's record (`decision-record` `why`+`sources[]`, or `debug-report`); notes are discardable (the
   `create-demo` throwaway pattern). No new durable surface.
4. **`document` owns the architecture doc** (inline Mermaid-C4 L1/L2), updated same-item — D41 named it owner
   but `document` never wrote it. The step is **location-agnostic** (the doc's home is the open docs-root
   question).
5. **`schemas.md` hygiene:** a **write-mode + tier** line per schema (cross-linked to `memory-model.md`) and a
   `config.json` schema; `debug-report`'s durable form is named as the per-file `# Sessions` entry; the
   `# Sessions` log is **per-file sections**, not one global stream (fixes `05`/`11` wording); the ghost
   `log.md` (Karpathy lineage in `06`) is dropped — its role is the per-file `# Sessions`.
*Rejected:* adding `items/<id>/` to the static scaffold (id is runtime, not init-time); keeping `backlog.md`
append-only (D51's lump — closed items grow it forever); a durable home for research notes (duplicates the
`decision-record`). *Evidence:* the three-agent sweep — every age-growing artifact unbounded; `checkpoints/`
and the architecture doc had **zero** writers; `items/` referenced everywhere but never scaffolded. →
`shared/schemas.md`, `shared/memory-model.md`, `05`, `06`, `11`, `skills/{planner,prioritize,document}`,
`agents/research`, `commands/start.md`; amends D51; precedes the D41 retention law (Layer 1 — closed in D61).

## D60 — `checkpoints/` demoted to reserved; disposition deferred to the outward-permission model **[DECIDED — defer]**
`.workflow/checkpoints/` was an orphan — listed as a durable append-only dir, but **no skill writes it**
(`checkpoint` only posts to the bus and blocks). Its disposition is **not a retention question**: qa/demo
verdicts are disposable (the consequence is already in git on pass / `# Sessions` on fail), but **setup /
publish-approval** verdicts are *outward-action approval events* the open outward-permission model (D35, `07`)
may want as a **durable approval ledger**. Deciding persist-vs-drop now would pre-empt that model. So
`checkpoints/` is **demoted to reserved** (writer + retention TBD), pulled out of the retention-bound set, and
its disposition folds into the outward-permission pass — whatever persists there carries its own retention rule.
*Rejected:* dropping it now (discards a possible outward-action audit trail before the model that needs it
exists); keeping it active-but-unbounded (the orphan we are fixing). *Evidence:* the skills sweep (`checkpoint`
writes only to the bus; `checkpoints/` has no writer). → `05`, `commands/start.md`, `shared/schemas.md`, `07`
(outward-permission model, D35).

## D61 — Retention/read law: cap-and-archive + mechanical/judgment split **[DECIDED — closes D41]**
The append-only tier is bounded by **read-cost** (what loads per pass), not disk — the working tree is a
**bounded cache; git is the ledger**. Closes D41's open mechanisms. Two moves:
**(1) Bound = cap-and-archive, NOT distillation.** Keep the last *K* raw entries on disk; drop older ones to
git (the file carries a one-line archive pointer). Bounds the read with **zero judgment** — counts, moves,
deletes. Per stream: **`# Sessions`** (per node) caps last-K raw + a deferred `Lessons` zone, oldest → git;
**`decisions/`** keeps a VOLATILE `index.md` (`id · title · status · one-line`) + active bodies, superseded
bodies dropped to git (tombstone in the index); **`items/<id>/`** stays committed while the item is open
(crash-survival) and the dir is **pruned once closed** in the audit pass (essence already moved:
debug-report→Sessions, decisions→`decisions/`, diff→git); the **`git log` cold-start read** is bounded by
recording `base_sha` in `handoff.md` and resuming `<base_sha>..HEAD` (one session's delta, not project age).
**(2) Mechanical vs judgment split.** The four caps are **deterministic → a shipped retention script**; only
the D41 **deletion-test over `CLAUDE.md` + `rules/`** needs an LLM. Both run in an **`audit` maintenance item**
that `prioritize` injects when a **count/size threshold** trips (machine-detectable) or every *N* items. So
retention is **enforced** (a script), not advised — D40 applied to disk hygiene. **Sessions distillation**
(postmortems → lessons) is the lossy, model-authored part and is **DEFERRED** — cap-and-archive bounds the read
without it; distillation is a later signal-quality feature.
**Prerequisites (deltas):** `decision-record` gains `status` + `supersedes`/`superseded_by`; `handoff.md` gains
`base_sha`; nodes gain an archive-pointer line; the `# Sessions` entry format is **strict/lint-parseable**
(`## [date] kind | title`) so the script can split entries.
*Rejected:* shipping distillation in v1 (model-authored compression of safety memory — high leverage if wrong);
handoff git-tags (per-item handoff → tag explosion, D54); an LLM doing the mechanical file-surgery (a script is
more reliable for memory removal). *Open:* exact `K`/thresholds (build-time tuning); authoring the script
(depends on the format/fields landing); `decisions/` final location (docs-root pass) — the design is
location-agnostic. *Staleness* (a doc that's *wrong*, not *big*) stays a separate diff-based signal that
schedules a doc-fix, not a prune. *Evidence:* the Layer-0 sweep (only append-only grows unbounded); D38 tiers;
D40 (mechanical→enforced); D54 (per-item handoff). → `shared/memory-model.md`, `shared/schemas.md`, `05`, `06`,
`skills/{document,prioritize}`, `11`, `07`; closes D41; built on D59–D60.

## D62 — Unified docs-root under `<project_root>/docs/` **[DECIDED — closes D49's sliver]**
Decides the four docs-root forks from first principles. **(1) Unify + locate:** `spec/`, the code-map, and the
inline-C4 `architecture.md` live under one **`<project_root>/docs/`** root, in **both modes** — because the
launch-root↔`project_root` line *is* the process↔product line (`.workflow/` = how it was built, `docs/` = what
was built + why), and because **brownfield forces `project_root`** (a repo's docs go in its own `docs/`), so
consistency forces greenfield to match (one rule, resolved via `config.json:project_root`). The purity counter
dissolves: extracting `project/` yields a *self-documented* product (code + spec + architecture + code-map)
while `.workflow/` — the only machinery — stays behind. Nothing in `docs/` is always-loaded, so depth costs no
hot-path context (D49/master rule). **(2) `decisions/` joins → `docs/decisions/`:** decision records are
**ADRs** (durable "why" = non-derivable intent, D38), and D38's own evidence base is ADR-immutability +
docs-as-code; they're product knowledge, not run bookkeeping, so they move docs-side while **`checkpoints/`**
(run-approval events) stays in `.workflow/`. **(3) Un-hide `.knowledge/` → `docs/knowledge/` (visible):** half
of it is the *durable hand-written* layer (D39), not pure machine output, and docs-as-code wants it reviewable
in PRs; the dotfile misrepresented it. **(4) `llms.txt` stays a thin root manifest** at `<project_root>/llms.txt`
(the convention is a root entry point) pointing **into** `docs/knowledge/` — progressive disclosure.
**Brownfield rule:** ingest **adopts-and-merges** into an existing `docs/` (write members to known subpaths,
never clobber; namespace ours on a name collision). `/start` scaffolds an empty `<project_root>/docs/` at init
so `discuss`'s spec has a home before code exists.
*Rejected:* docs at the launch root for greenfield (splits the rule across modes — brownfield can't); leaving
`decisions/` in `.workflow/` (an ADR is product knowledge, not machinery); keeping `.knowledge/` hidden
(implies untouchable, but it's half hand-written); burying `llms.txt` under `docs/` (breaks the root-manifest
convention). *Evidence:* D38 (docs-as-code + ADR immutability), D39 (hand-written experiential layer), D49
(per-mode, path-agnostic via `config.json`), master rule (on-demand → no hot-path cost). → `05`, `06`,
`commands/start.md`, `templates/orchestrator-CLAUDE.md`, `shared/{schemas,memory-model,format}.md`,
`skills/{document,execute,prioritize}`, `07`, `11`; closes D49's docs-root sliver.

---

## Alignment-scan pass (session 2026-07-01)

## D63 — Alignment scan: scan-first, then a knowledge-gated lightweight-fan-out skill **[DECIDED]**
The maintainer's "are the docs + planning aligned with the implementation?" concern is realized as a
whole-project reconciliation between the design docs + decision log and the shippable package. Two-part call:
**(1) run it first as a manual, one-off multi-agent scan** and **derive the skill from what the run teaches** —
the fan-out decomposition and the finding schema are discovered empirically, and a *complete* skill can't be
authored before knowledge generation exists anyway; **(2) the eventual skill is knowledge-gated and ships as a
lightweight agent fan-out, NOT a Workflow** — a periodic, every-project scan must not consume most of a user
session (a full Workflow is acceptable only for a one-off on our own repo). Method: **bidirectional** (the
decision log as a top-down checklist + a filtered bottom-up file sweep); each divergence classified by the
**commitment model** (locked → drift/bug · provisional → finalize-later · unspecified → steering), known tracked
gaps excluded; candidates **adversarially verified** before they count. Scheduled by the D61 `audit` trigger
(interval / threshold / after-big-change); detection is the backstop, prevention (D64) shrinks the drift upstream.
*Rejected:* skill-first (the fan-out shape is exactly what the run discovers, and a pre-knowledge-gen skill is a
stub to rewrite); a Workflow-based shipped skill (too costly for a periodic user-run scan).
*Evidence:* the 2026-07-01 run — 8 area finders + a 2-lens adversarial verify, 15 confirmed findings — surfaced a
systemic regression (D64) no eyeball pass had caught. → `11`, `06`, `09` (relates to the project-state view +
self-hosting); complements `document` freshness + brownfield `ingest`.

## D64 — No-spec-internal-refs extended to the whole package + mechanically enforced; four body fixes **[DECIDED]**
The alignment scan (D63) found a **systemic regression**: the D59–D62 doc-surface capture pass (commit
`852179e`) reintroduced **52 spec-internal reference lines** (31 `Dxx` tokens + doc-numbers + `Space N`) into the
shippable package — violating locked D34 because **D34 was advisory prose with no gate** (the project's own
D38/D40 thesis — prose rots silently, only checks fail loudly — demonstrated on itself). Calls:
- **Scope:** D34's no-refs rule covers the **entire shipped package** (`skills/ agents/ shared/ commands/
  templates/ hooks/`), not just the three dirs D34 literally named — `commands/start.md` + templates are
  runtime-loaded, so the same rationale applies (extends D46). The numbered design docs + decision log keep their
  refs (they are the down-pointing provenance).
- **Enforcement:** a committed **grep gate** (`scripts/check-no-spec-refs.sh`) fails on any leak — D40 applied to
  the meta-repo (mechanical, not advised).
- **Four fork resolutions:** `discuss` owns spawning provisional → debt tickets on the **no-demo path** (closes a
  D23 coverage hole; `create-demo` owns the demo path); `planner`'s ungoverned ~200k **session-split rule cut**
  (context exhaustion is the handoff model's job, D10/D48); `verify`'s "skippable" **narrowed** to
  skip-the-fan-out-not-the-step (D30 makes the step unskippable); the orchestrator brief **corrected** to separate
  hook-enforced gates (verify-before-commit, secret-scan) from the permission-rule outward gate from the
  **deferred** build-once-per-wave (it was mislabeled as an uncrossable hook gate no hook enforces).
- **Prevention follow-ons (OPEN → `07`):** **single-source status** (kill "done/open" duplication across
  roadmap/roster/bodies — the root of the stale-status findings) and a **capture-time blast-radius sweep** for
  cross-cutting decisions (the root of the topology/owner/over-claim findings).
*Rejected:* leaving D34 advisory (the observed regression); auto-fixing findings from AI-only judgment (D45);
relaxing D34 to allow provenance breadcrumbs in the package (leaks design artifacts into runtime context, wastes
tokens). *Evidence:* git-traced to `852179e` (+31 `Dxx`); the gate now reports zero. → `shared/format.md`,
`scripts/check-no-spec-refs.sh`, the affected package files, `10`, `11`; closes scan findings #1–15; complements
D34/D40/D46.

## D65 — Two-tier drift defense: mechanical auto-fix at the gate, semantic drift → ticket → `prioritize` → the existing loop **[DECIDED]**
Keeping docs aligned with code splits by the mechanical-vs-judgment law (D61), and **both tiers feed the normal
queue rather than blocking** (the loop never stalls):
- **Mechanical tier (per commit):** a deterministic checker (the `scripts/check-no-spec-refs.sh` no-refs gate,
  plus project lint/format/dead-node) runs at commit time and **auto-fixes what a script can fix with zero
  judgment** (strip a leaked ref, reformat), re-checks, and lets the commit proceed — and **logs what it fixed**
  (no silent masking of the upstream generator, per D59). It runs as a step in `commit` (visible in the loop)
  with a **git pre-commit hook** as the human/catch-all backstop, both calling the same script. Hard blocks stay
  reserved for the never-want-irreversible class only — secrets + committing over a failed `verify` (the existing
  `guard.sh` gates).
- **Semantic tier (judgment):** drift a script can't safely fix (a stale/contradictory/over-claimed doc, a
  missing owner) is **never auto-resolved inline** — an unreviewed commit-time agent deciding *which side is
  right* can "fix" in the wrong direction and launder a code bug into resolved docs (foreclosed by D45/D64).
  Instead the detector files a `create-issue` ticket into `backlog.md` with the evidence, **severity set from the
  commitment-class** (a locked contradiction rides high so it isn't starved; cosmetic drift sits as low `debt`).
  The **authority call is deferred to remediation:** `prioritize` schedules the ticket in normal urgency ×
  dependency order (D26), and the fix runs through the **existing loop** — `decision-engineer`/`adjudicate`
  decides authority (locked → fix the code · provisional → finalize · unspecified → **steering to the human**),
  then `planner` → `execute`/`document` → `verify` → `commit`. **No new agent.**
- **One queue, two detectors:** the fast per-commit gate and the periodic alignment scan (D63) are
  shallow-vs-deep detectors that file tickets the same way, so all drift converges on one backlog.
*Rejected:* hard-blocking doc drift (stalls the loop — hard blocks are only for the never-want-irreversible
class); auto-resolving authority inline at commit (an unreviewed AI guess that can mask a code bug — D45/D64); a
standalone **docs-engineer** agent (its sub-roles are already owned — detection by the D63 scan + `research`
readers, authority by `decision-engineer`, the edit by `execute`/`document`; a specialized doc-authoring worker
is **reserved** for heavy generative reconstruction, e.g. brownfield `ingest` spec-from-code, and added only if
the generic workers prove insufficient — `07`).
*Evidence:* this session — the alignment scan surfaced the drift, and the discussion turned on remediating it
without stalling or laundering code bugs. Builds on D63 (scan), D26 (pure queue), D40 (mechanical → enforced),
D45 (no AI-only action), D23/D64 (commitment-based authority), D33 (`create-issue` → backlog). →
`skills/{prioritize,commit,decision-engineer,execute,document}`, `hooks/`, `scripts/check-no-spec-refs.sh`,
`07`, `11`; extends D40's enforcement wiring; complements D63.

---

## Phase 1 build — skill-body deltas (session 2026-07-01)

The decided-but-unwritten D36–D45 deltas were authored into the shippable bodies (`prioritize` waves;
`execute` divergence tiers + refuse-destructive; `planner` `risk_class`+`backup` + decision-coverage gate;
`adjudicate` conjunction-of-signals, with `verify`/`debug` nods; `commit` secret-scan). `schemas.md` already
carried the fields, so this was body prose, not schema work — except one gap surfaced below. Scope call:
**pure D36–D45 now**, bodies written **forward-compatible** with the D65 gate (a light second pass on
`commit`/`prioritize` remains, tracked under the drift-defense wiring). The no-spec-refs gate stayed green.

## D66 — Prerequisite-repair rides its own commit; the divergence record gains a machine-actionable `tier` **[DECIDED — amends D54, sharpens D37]**
Authoring the deltas surfaced one genuine tension: D37 isolates a discovered **prerequisite-repair** as a
**separate commit**, but D54 fixed **one commit per item** and `execute` never commits (`commit` is a tail
skill). Resolution:
- The repair rides its **own** commit, **emitted by `commit` at the item tail** — not by `execute`, which
  stays commit-free and decision-free. An item that hits a prerequisite-repair therefore yields **two
  commits** (the isolated repair, then the planned change) — a **narrow carve-out to D54's
  one-commit-per-item**. Bookkeeping (the backlog done-flip + `handoff.md` rewrite) rides the
  **planned/completing** commit, after any repair commit.
- `changelog.divergences[]` gains a **`tier`** ∈ `{ cosmetic, prerequisite-repair, structural }` so the tier
  is **machine-actionable** — `commit` reads it to decide whether to split — rather than prose only `execute`
  understands.
*Why:* D37's point is that a stumbled-into fix stays **independently reviewable/revertible**, which a
call-out inside a bundled commit can't give. Keeping the commit in the `commit` skill (not `execute`)
preserves the **single-committer** design (Conventional-Commit formatting + the secret-scan gate live in one
place) and `execute`'s zero-decision/commit-free invariant. Typing the divergence stops a body naming a tier
the schema doesn't define — the exact doc↔implementation drift the alignment scan exists to catch (D64).
*Rejected:* one commit per item with an in-message call-out (weakens D37 — no independent revert, and edges
toward the fold-in D37 rejected); `execute` committing the repair itself (duplicates commit formatting +
secret-scan into the executor, breaks its commit-free invariant); leaving the tier as prose only
(unactionable → drifts). *Evidence:* this session — the delta-authoring pass; user picks (separate-commit for
the repair · author the full wave model now · pure D36–D45 now). → `skills/{execute,commit}`,
`shared/schemas.md`, `templates/loop.md`, `10`, `11`; amends D54, sharpens D37, complements D64.

---

## Phase 1 build — rules baseline + enforcement wiring + drift gate (session 2026-07-01)

The decided-but-unwritten D40 (`rules/` baseline + `/start` enforcement wiring) and the D65 drift-gate wiring
were authored. Shipped: four thin **`rules/*.md`** (code-style · testing · security · ops — principles only,
each enforceable one carrying an `— enforced by: <mechanism>` tag that doubles as the wiring manifest); a
**rules-file convention** in `shared/format.md`; a new **`/start` step 4** that specializes the rules and wires
the enforcement layer (auto-write greenfield, adopt-and-gap-fill brownfield, externals → setup checkpoint); the
**mechanical-gate `commit` step** (auto-fix zero-judgment drift → log → proceed; semantic drift → `create-issue`
ticket, never resolved inline) and the **`prioritize`** note that drift tickets ride the normal queue at
commitment-severity. No schema change — the fields (`commitment`, issue `severity`/`source`, divergence `tier`)
were already carried. The new `rules/` dir was added to the no-spec-refs gate; the gate stayed green. One
mechanism call surfaced its own entry below (D67). **Brownfield boundary:** rules + enforcement are adopted
now; the docs → `knowledge/` ingest stays the tracked stub.

## D67 — The mechanical drift gate ships as a generated per-project `checks.sh`; the git hook is check-only **[DECIDED — sharpens D65, extends D40]**
Authoring the drift gate forced two mechanism calls D65 left open:
- **What ships downstream is not this repo's `check-no-spec-refs.sh`.** That script enforces *this package's*
  no-spec-refs authoring law — meaningless in a consuming project. The downstream mechanical checker is a
  **`/start`-generated `.workflow/checks.sh`**, built from the project's detected enforcers (format · lint ·
  typecheck · dead-link) — the single "same script" both callers invoke.
- **One runner, two modes.** `checks.sh --fix` auto-applies zero-judgment fixes, re-stages, and logs them —
  run **in-loop by `commit`** (visible). `checks.sh --check` fails non-zero on residual drift — run by the git
  **`pre-commit` backstop** for commits made *outside* the loop. The backstop **never silently rewrites** a
  human's tree; auto-fix stays in the visible loop step.
*Why:* D65 said "both call the same script" but left the script's provenance and the fix-vs-check split open;
naming a repo-specific gate as the downstream checker would ship an inapplicable check, and a git hook that
auto-fixes + re-stages would surprise a human's manual commit.
*Rejected:* shipping `check-no-spec-refs.sh` as the project gate (checks the wrong invariant downstream); a
single-mode script that auto-fixes everywhere (silent tree rewrites under a manual commit); putting the
auto-fix only in the hook (invisible to the loop). *Evidence:* this build pass — the no-spec-refs gate is
authoring-specific; the human-manual-commit case needs a non-mutating backstop. → `commands/start.md`,
`hooks/pre-commit.sh`, `skills/commit`, `scripts/check-no-spec-refs.sh`; sharpens D65, extends D40.

## D68 — Knowledge generation: own-script per-stack code-map, two centrality lenses, three-tier node seed; ingest seeds intent from `CLAUDE.md` **[DECIDED — sharpens D39, opens brownfield ingest]**
Pressure-tested on a real full-stack repo before deciding (D63 method — run first, derive the design). Calls:
- **The generator is an own script per stack, not an external tool.** `/start` emits a `.workflow/`
  code-map generator the way it emits `checks.sh` (D67): Python uses stdlib `ast`, other stacks tree-sitter /
  the native parser — regenerable, near-zero-dep, cheap enough to re-run freely (satisfies D39's "generated →
  cannot drift"). Rejected the two external candidates on evidence: `repomix` solves the *adjacent* problem
  (pack context for an LLM — signatures + token counts), not a typed import graph; aider-repomap does produce a
  PageRank import graph but is a heavyweight Python+LLM install to drag into every consuming project.
- **Layer 1 carries TWO labeled centrality lenses from one import graph — not a single "importance" rank.**
  *Impact* (forward PageRank: most-depended-upon → blast-radius, for `debug`/`planner`) and *orchestration*
  (reverse PageRank / fan-out: where flows compose → "where does feature X live"). Both fall out of the same
  extraction for free. Treating either as "importance" would mislead the loop — proven below.
- **Three-tier node seed makes "eager graph, lazy semantics" safe.** `[G]` generated-structural (path, type,
  edge targets, the lenses) for **all** files, eager; `[X]` cheap LLM-extractive `purpose.actual` + tags for a
  prioritized set; `[D]` the durable, non-derivable `why` / intent-vs-actual / `# Sessions` — authored **on
  touch** by `document`. A not-yet-touched node is skeleton + plausible purpose, **never an empty shell that
  lies** (the D38 rot the lazy path otherwise risks). `[D]` is the layer that earns its tokens — the product.
  **The `[X]` prioritized set = the union of *both* lenses (impact ∪ orchestration) plus the spec's declared
  core flows — never impact alone**, or seeding documents the plumbing and under-serves the behavioural core
  (the same miss the two lenses exist to prevent — the impact lens buried the engine + ingestion in the run
  below); and **no consumer treats a lens as "importance"** (`debug` → orchestration + impact; `planner`
  "where does X live" → orchestration). *Principle captured; the selection mechanism is deferred to
  implementation.*
- **Brownfield ingest is a thin `ingest` skill over existing leaves, and its first job is to seed
  behavioral-core intent from the existing `CLAUDE.md` / spec.** The product narrative and "what is core" are
  **un-derivable from code** (see evidence) — they live only in the human's prose. `ingest` drives `research`
  (read code + existing docs) → `document` (write nodes/graph/reconstructed spec); **no new agent** (the
  doc-authoring agent stays reserved, D65). Reconstructed spec defaults to **unspecified**, with a
  **reconciliation checkpoint** that locks only the load-bearing invariants the human confirms (avoids D23's
  finalize-ticket flood that all-provisional would cause on a large repo). Full structural graph eager; `[D]` +
  spec lazy with a prioritized seed.
*Rejected:* an external tool as the generator (wrong problem / too heavy — above); one "importance" ranking
(buries the behavioral core — evidence); eager `[D]` authoring (expensive, and unnecessary once `[X]` seeds
the gap); all-provisional reconstructed spec (backlog flood, D23); a new doc-authoring agent (reserved until
the generic workers prove insufficient, D65). *Evidence:* the 2026-07-02 run on a real repo (stock simulator,
225 source files / 805 intra-project edges): own-script `ast` produced the typed graph + PageRank in ~9s with
zero deps and zero parse failures; PageRank **diverged from naive in-degree** (`repositories/base.py` #1 over
`log.py` despite fewer importers → recursive centrality is real signal); **yet it buried the core the
maintainer named** — the simulation engine and ingestion logic ranked low, while the orchestration lens
surfaced exactly `simulation_engine/{run_lifecycle,advance_service}`, `ingestion/ingest`, and the run/advance
routes; the product narrative ("filter by sector/cap/volatility, drop into a random market moment, trade")
appeared in **neither** lens. → `06`, `commands/start.md`, `skills/{ingest,document}`, `10`, `11`, `07`;
sharpens D39, uses D67's per-stack-generator pattern, complements D62/D63.

## D69 — Proportional-rigor decision gate: a cheap triage in `planner` → tiered depth via `decision-engineer`; no back-eval **[DECIDED — implementation deferred to `11`; formalizes the engineering-feasibility pass]**
An autonomous loop removed the senior-dev gut-check that normally catches a bad *irreversible* decision in
review — so the loop needs to inject rigor on high-stakes calls **without** stalling the fast path or burning
tokens. Reframe that makes it principled rather than a budget hack: **rigor ∝ (cost-of-being-wrong −
cost-of-reversal)**, not rigor-vs-speed — even for free you would not validate a cheap-to-reverse decision, since
trying-and-reverting beats validating up front. Calls:
- **A cheap O(seconds) triage runs on EVERY `planner` output** — an inline checklist (no dispatch) grading
  reversibility × blast-radius × approach-ambiguity. Universal on purpose: it is the net for the **silent
  critical decision** that would otherwise be built at tier-0 because nobody flagged it as a decision. It assigns
  a **rigor tier**:
  - **Tier 0 — judgment.** LLM decides from its own knowledge; proceed. The default (~85–95% of outputs).
  - **Tier 1 — research.** Dispatch `research` to weigh standard/market approaches against project fit (bounded
    fan-out → synthesise). ~5–15%.
  - **Tier 2 — pressure-test.** Run a real experiment — but **only when critical AND a cheap empirical test
    exists**; else fall back to Tier 1 and record the residual risk. Rare.
  - **Escalate.** A genuinely ambiguous / product-shaping call is not "research harder" → a one-line steering
    question to the human (reuses the sandbox fence + the unspecified→steering rule).
- **The triage lives in `planner`, not `decision-engineer`** — `decision-engineer` only fires once a decision is
  *recognised*, and the whole point is to catch the *unrecognised* ones. `planner` triages, then escalates to
  `decision-engineer` at the chosen tier (extends planner's decision-coverage gate).
- **A mechanical floor + a backstop so the LLM triage need not be perfect:** the **impact-centrality lens**
  (D68's code-map) auto-escalates any decision touching a high-blast-radius node regardless of the model's gut
  (deterministic); the periodic **alignment scan** (D63) catches misses — prevention upstream, detection as
  backstop.
- **Record a prediction, don't run a back-eval.** At Tier 1/2 the `decision-record` gains
  `predicted_outcome` / `success_signal` — **recorded rationale** (ADR consequences), checked *opportunistically*
  by the alignment scan or a human, **not** by a per-item automated eval.
*Rejected:* a **post-implementation quality "eval"/back-gate** (an AI grading AI-written code is inherently
judgment → advisory-only per D45, overlaps `verify`/`code-review`/the alignment scan, and is a token sink — the
maintainer's point: it will never say "perfect, pass"); a **binary research yes/no** gate (misses the
proportionality — a ladder is right); putting the triage **in `decision-engineer`** (misses unrecognised critical
decisions — must be upstream); **always-pressure-test** (waste on reversible decisions even when free, and
unbounded time); a **separate engineer/feasibility agent** (roster bloat — the gate reuses the existing
hub-and-spoke). *Evidence:* this session — the maintainer ran a market-weighing research pass on
tree-sitter+PageRank in a separate chat (it *confirmed* the choice, and the **process** proved its worth even on
a confirm), and we pressure-tested the same decision empirically on a real repo (D68); the discussion generalised
both into one proportional-rigor gate, with D68's impact lens supplying the mechanical criticality signal.
Builds on D22 (cheap gate → expensive validation), D23 (unspecified→steering / the fence), D43 (planner
decision-coverage), D45 (AI-only → advisory), D63/D64 (detection backstop), D68 (impact lens). →
`skills/{planner,decision-engineer}`, `shared/schemas.md` (`decision-record` gains `predicted_outcome`), `07`,
`09`, `11`; **answers the open "engineer agent?" slot (no new agent) and formalizes the engineering-feasibility
pass.** Implementation deferred (`11`).

---

## D70 — Project map + flow view: a console tab over the code-map — static skeleton, dynamic overlay **[DECIDED — feature + architecture; the runtime-capture mechanism is a direction, tracked OPEN in `07`]**
The console gets a **project-map screen** rendering the code-map `graph.json` (D68) as a cluster diagram: nodes
sized by the **impact lens**, grouped by the **directory tree**, with **semantic zoom** (cluster → file →
[later] symbol). It is the structural face of the deferred **project-state view** (`07` — "how the pieces
connect") and a **self-hosting** aid. Free-text search over node paths/labels is a nice-to-have, not MVP. Calls:
- **Two layers, complementary — the flow view is an *overlay*, not a second graph.** The static map (always
  available, no run needed) is the skeleton; a **flow** ("watch a message get sent") is a **highlighted subgraph
  laid over it**, captured by **observing an actual run** — the union of nodes that execute during one exercised
  behaviour *is* the flow (empirical, not a guessed semantic slice). A trace is a **lower bound** (only exercised
  paths); the **orchestration lens** fills un-exercised branches.
- **Noise-filter protocol (direction).** A raw trace is dominated by framework/infra. Filter =
  **baseline-subtract** (action-trace − a null/unrelated-action trace) → **specificity-rank across flows** (a node
  in every flow = infra → demote; in one flow = characteristic → promote — an IDF that sharpens as more flows are
  captured) → **static-reconcile** against the orchestration lens (fill branches; flag characteristic-but-
  disconnected nodes as noise) → optional human trim (QA-harness pattern — machine-driven where possible, human QA
  only if necessary). Runtime differential tracing is a **working direction, not decided** — a static-slice
  approach may still win for some stacks; the trace tooling is a **per-stack arm** on the same discipline as the
  code-map.
- **Interaction = a scoped intake ticket, subject to D69 — never a privileged fast-path.** Clicking a node emits a
  **normal backlog item** (payload: node ID(s) + the ask) onto the existing loopback bus (`05`) — the decided
  "website talks to the orchestrator only via bus + files, never routes Claude" model. It rides the **same
  prioritization + proportional-rigor triage (D69)** as any work; the map is a *precision scoping aid for intake*,
  **not** an edit console — else it becomes a backdoor around the disciplined intake the project exists to enforce.
- **Three reserved seams (foundation must not foreclose the view).** (1) `graph.json` node IDs stay **stable +
  addressable** — today **relative paths at module granularity** (`type:"module"`); **symbol-level** addressing is
  the existing later seam (`11` Space-5/6), needed for fine-grained node-tickets/overlays and the "change how the
  timestamp renders" case. (2) A **reserved bus action** "node/subgraph → ticket" (`05`), UX deferred. (3) A
  **reserved flow-overlay layer** in the console data contract (`03`) — a labelled list of node IDs + edges the
  renderer can highlight. Build nothing now; reserve the seams.
- **Per-stack arm rule (resolves D68's "others follow").** No calendar trigger, no speculative arms. **(a)** the
  code-map has a **stack-agnostic degraded fallback** (directory tree + shallow import graph) so "no arm" ≠ "no
  map"; **(b)** a new arm is **demand-built** the first time a real target in that stack hits `ingest`/`/start`,
  against the fixed `graph.json` contract (both lenses, stable IDs); **(c)** the **Phase-4 demo forces exactly one
  more arm**, so we ship with ≥2 proving the contract generalizes. Same rule governs the trace-capture arm.
- **Remote control.** The console stays **local-served by default**; an opt-in **"remote control" mode** serves it
  over a temporary **Cloudflare tunnel** (already in `00`'s vision for QA phone-ping — one capability, two
  consumers). Tunneling breaks the loopback trust model (anyone who can POST can steer the orchestrator), so remote
  mode ships **off by default + an explicit "unsafe" warning now**; **auth (Cloudflare Access / token) is a
  reserved future requirement**, not built now (nothing important is wired to it yet → not worth targeting).
- **Undecided (→ `07`):** map as its **own tab vs the console home/overview**; a captured flow as a **first-class
  knowledge artifact** (versioned, regenerable, `06`) vs **ephemeral**; the capture **trigger/boundary** UX (leans
  on the QA harness).
*Rejected:* **algorithmic community detection** for clustering (unstable run-to-run, doesn't match devs' mental
model — directories are stable + self-labeling); **live browser→Claude routing** (violates the master rule +
`03`/`05` — the bus is a ticket channel, not a request path); **static-only semantic slicing** as *the* flow
mechanism (nothing in `graph.json` defines "the message flow" — observing a run is more grounded); a **privileged
node-ticket fast-path** (backdoor around D69); **pre-committing a language set** for arms (speculative — fallback +
demand-build is leaner). *Evidence:* the code-map already emits `graph.json` with both lenses (D68) and the WhatsApp
"dive into the message-send flow, then re-scope the timestamp render" case — the visualization is a read-out of an
artifact the knowledge space already produces, and the runtime-capture idea dissolves the semantic-slicing problem
by *observing* rather than *inferring* the flow. Builds on D68 (code-map + two lenses = the map's data), D69
(node-tickets ride the proportional-rigor triage), `03`/`05` (loopback bus, never routes Claude), `00` (tunnel
in-vision), the `07` project-state view (this is its "how pieces connect" face) + the `11` symbol-level seam.
**Feature + architecture DECIDED; runtime-capture mechanism a direction (OPEN in `07`); build deferred to Phase 2/3.**
→ `03`, `05`, `07`, `11`.

## D71 — Retention script built: the deterministic `audit` enforcer (shipped stdlib Python) **[DECIDED + BUILT — implements D61]**
The cap-and-archive retention law (D61) becomes an enforced artifact: **`scripts/retention.py`** (stdlib Python,
idempotent), shipped like the code-map extractor and run in the `audit` maintenance item. Four build decisions,
each the leaner of the alternatives:
- **Archive-state = an inline visible marker, not a manifest or frontmatter counters.** Correctness comes from
  *counting* entries > K, so a marker is needed only for human/PR traceability of what left the working tree: a
  one-line `<!-- retention: N Sessions entries archived -> git @ <sha> -->` at the **`# Sessions` head** (parsed
  back so N **accumulates** across passes), and a `docs/decisions/index.md` tombstone row `| id | title |
  superseded->X | git <sha> |`. No new file.
- **Closed-item prune is gated on a `document`-written `promoted.json` marker.** A mechanical script can't judge
  whether an item's essence was folded (debug-report→Sessions, decisions→`decisions/`); pruning a closed-but-
  unpromoted dir would destroy the only durable copy. So the prune touches **only** dirs carrying
  `promoted.json {promoted:true}`; unmarked → skipped. The safety gate is a fact `document` asserts, never a guess.
- **Thresholds are config-overridable with shipped defaults.** `config.retention` = `sessions_k` (the script's
  only knob) + the `prioritize` scheduling trips `decisions_active_n` / `items_closed_m` / `every_p_items`; absent
  → 10 / 30 / 10 / 15. Cheap now, avoids a retrofit when a real project wants different numbers.
- **Shipped-shared stdlib Python — not per-stack-generated, not bash.** Retention edits only our OWN stack-agnostic
  `.workflow/`+`docs/` layout, so per-stack generation (à la `checks.sh`/`codemap.sh`) buys nothing. Python over
  bash because the work is date-arithmetic + text-parse + rewrite — where portable bash (macOS bash-3.2 / BSD vs
  GNU `sed`/`date` / Git-Bash) is fragile, while stdlib Python is byte-identical cross-OS and is **already a hard
  package dependency** (the code-map extractor). Emergent rule: **thin shell glue = bash; parse/rewrite = Python.**
Deletions are made in the working tree and left **staged for the `audit` item's `commit`** (`git add -A`); content
stays recoverable at the recorded anchor. Two refinements to the pressure-tested previews: the marker lives at the
**section head** (so `document`'s append-only entries land below it, not after it) and the item marker is
**`promoted.json`** (not the loop's `state.json` — name collision). **Validated** on a git fixture: the three caps
fire, N accumulates (2→5), and a re-run is a clean no-op; archived content recoverable via `git show <anchor>:path`.
*Scope:* the three size-caps only. The prose deletion-test over `CLAUDE.md`+`rules/` stays a separate model-run
step in the same audit item (judgment, not the script); `base_sha` bounding the git-log read is a read convention,
not a script action; **dead-node prune** (deleted source → delete node) is a staleness signal owned by `document`,
not this size-cap script; **Sessions distillation** stays deferred (D61).
*Rejected:* frontmatter counters / a separate `archive-index.json` (correctness needs neither — counting decides,
the marker is only for humans); pruning by "closed" alone (unsafe without the promotion fact); hardcoded thresholds
(config is a cheap hedge); per-stack generation (the layout is identical everywhere); bash (OS-divergent for
parse-heavy work, and no dependency saving since Python is already required). *Evidence:* D61 (the law implemented),
D67 (the `checks.sh` shipped-mechanical-enforcer precedent), D68 (the sibling stdlib-Python shipped script + the
"Python already required" fact). → `scripts/retention.py`, `skills/{document,decision-engineer,prioritize}`,
`commands/start.md`, `shared/{schemas,memory-model}.md`, `11`; implements D61.

---

## Not yet decided (tracked in `07`)
Knowledge graph regenerate-vs-incremental; model/effort map; collision **independence test** (waves grouping
decided, D36); Arbiter input contract; autonomous reset mechanism; website stack. Intake follow-ons:
engineering-feasibility pass **designed as the proportional-rigor gate (D69), implementation deferred**;
demo-skill mechanics; commitment-status storage. `init` follow-ons: brownfield
ingest **designed (D68) — the `ingest` skill is being authored**; console launch, full disk-layout protocols
still open (the `spec/`+`.knowledge/` docs-root placement closed — D62). Skill-review follow-ons:
incidental-issue-resolution detection — deferred; outward-action permission mechanics (D35). Adoption
follow-ons: the **retention & archival law** is **closed** (D59–D60 write-law leaks + D61 cap-and-archive read
law) and the **retention script is built** (D71); what remains is **Sessions distillation** (deferred) and
`K`/threshold tuning against real runs. Plus whether `verify` samples the real diff vs trusts the `changelog` (#8). **Two new (user-raised):**
a synthesized **project-state view**, and a **framework version-update** skill. **Alignment pass (D63/D64):**
authoring the alignment-scan **skill** is knowledge-gated (D63); two prevention follow-ons — **single-source
status** and a **capture-time blast-radius sweep** — are undecided (D64). The **doc-authoring agent** is
reserved (D65). The **drift-gate wiring** is **authored** (D65/D67 — `commit` mechanical step + `pre-commit`
backstop + generated `checks.sh`); what remains is `checks.sh`'s per-stack generator, which rides the `/start`
enforcement-wiring build. All → `07`.
