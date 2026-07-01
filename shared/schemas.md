# Shared Artifact Schemas

The data formats that flow between capabilities. One source of truth — skills/agents reference these by
name. On-disk paths are fixed; each schema notes its **write-mode** (rewrite-in-place · append ·
new-record-supersede · create-per-item) and **tier** (see `shared/memory-model.md`). *Retention bounds (the
read law) live in `shared/memory-model.md`.*

## spec  · *rewrite-in-place · STABLE (changes only with the code it specifies)*
The product definition `discuss` produces and the whole build runs against.
- `audience` — who it's for
- `runtime` — where it runs
- `purpose`
- `screens[]` — `{ name, role, commitment }`
- `features[]` — `{ name, purpose, acceptance_criteria, commitment }`
- `data_model`
- `integrations[]` — `{ name, kind: auth|payments|…, → triggers a setup checkpoint }`
- `tech_stack` — value | `"TBD → decision-engineer"`
- `commitment` ∈ `{ locked, provisional, unspecified }` — tagged per element

## roadmap  · produced by `planner` (decompose mode) · *emitted as items into the live `backlog.md` queue*
- `phases[]` — `{ name, goal, depends_on[], acceptance, commitment }`

## plan  · produced by `planner` (plan-one mode) · *created per item under `.workflow/items/<id>/` (planner `mkdir`s it on demand); committed while the item is open (crash-survival), the dir pruned once closed by the audit pass*
- `goal`
- `source_spec_ref`
- `decisions[]` — refs (by `id`) to the `decision-record`s this plan implements; every one must map to ≥1
  step or `planner` blocks the plan (coverage gate).
- `risk_class` ∈ `{ code-only, data-additive, data-destructive, prod-touching }`.
- `backup` — required when `risk_class` is destructive: `{ what, mechanism, verification, restore }`.
  `execute` refuses a destructive plan without it and runs+verifies it before the destructive step.
- `files_touched[]`
- `steps[]` — ordered, each independently verifiable
- `acceptance_criteria[]` — the definition-of-done; each `{ criterion, gate: artifact | human-qa }`.
  `artifact` → checked by `verify`; `human-qa` → confirmed by a `checkpoint` (kind=qa). **Every criterion is
  one or the other** — `planner` emits no un-checkable criterion. A plan with zero `human-qa` criteria
  never triggers a QA checkpoint.

## changelog  · produced by `execute` · *append within the item's lifetime; `.workflow/items/<id>/`; item-scoped ephemeral*
- `plan_ref`
- `actions[]` — `{ step, files, result }`
- `divergences[]` — `{ step, expected, actual, why }`

## verify-verdict  · produced by `verify` · *created per item in `.workflow/items/<id>/`; item-scoped ephemeral*
- `pass`
- `mismatches[]` — `{ expected, actual }`
- `confidence`

## decision-record  · produced by `decision-engineer` · *append-only — one record per decision; a reversal is a NEW record that supersedes (status flip), never an edit; global under `<project_root>/docs/decisions/`*
- `id` — stable id (e.g. `D-001`); `plan.decisions[]` reference these, and coverage is checked id → step
- `status` ∈ `{ active, superseded }` · `supersedes` / `superseded_by` — the reversal chain; a flip writes a
  NEW record and sets these. Retention GCs superseded bodies to git, keeping a tombstone in
  `decisions/index.md`
- `question`
- `options[]`
- `chosen`, `why`
- `confidence`
- `sources[]` — the durable distillate of any `research` dispatched for this decision (the heavy research
  notes are ephemeral scratch, discarded)

## debug-report  · produced by `debug` · *item-scoped ephemeral in `.workflow/items/<id>/`; its **durable form** is the per-file `# Sessions` entry `document` promotes — a report not promoted leaves no durable trace*
- `symptom`, `cause`, `fix`, `avoid`
- `confidence`

## checkpoint  · the `checkpoint` gate · *RESERVED — `.workflow/checkpoints/` is demoted pending the outward-permission model; today the verdict is a bus message, not a written record*
- `request` — `{ kind: demo|qa|setup, what, expected, how?(←setup-guide), blocking: true }`
- `verdict` — `{ pass, notes }`  · pass → continue · fail → debug→refine

## issue  · produced by `create-issue`, closed by `close-issue` · *filed into `backlog.md` — a **live open queue** (rewrite-in-place; closed entries leave, GC'd by `prioritize`), not append-only*
- `{ title, kind: bug|feature|debt, description, severity, source }`
- `github_ref` — the mirrored GitHub issue number (`create-issue` opens it; `close-issue` closes it)
- **open/closed state lives in GitHub** (source of truth) — the backlog holds only `github_ref`, never a
  duplicated local `state`, so `close-issue` writes no local loop-bookkeeping; `prioritize` drops a
  closed entry at pick time.

## config.json  · written once by `/start`, read on demand · *rewrite-in-place · static after init (committed)*
- `project_root` — `./project` (greenfield) | `.` (brownfield); makes code-touching skills path-agnostic
- `run` — per-project run config (model/effort routing, wave caps — fields grow as those land)

## state.json  · the live loop pointer (volatile, gitignored) · *rewritten in place each iteration*
- `status` ∈ `{ intake, building, idle }`
- `node` — current loop node; value ∈ the `loop.md` node labels (e.g. `planner:plan-one`, `verify`)
- `current_item` — backlog id or `null` · `wave` — wave id or `null` · `note` — human-readable cursor

## handoff.md  · the durable resume anchor (committed) · *rewritten whole each handoff, never appended*
- `current_item`, `loop_position`, `parked[]`, `base_sha` — the commit it was written against; a cold start
  reads this + `git log <base_sha>..HEAD` (bounded to one session's delta) and rebuilds position.

## per-item artifacts  · on disk
`plan` / `changelog` / `verify-verdict` / `debug-report` live under `.workflow/items/<id>/` — `planner`
`mkdir`s the dir on demand when it writes `plan.md`; the dir is **item-scoped**, committed while the item
is open (crash-survival) and **pruned once closed** by the `audit` pass. `decision-record`s stay global +
append-only under `<project_root>/docs/decisions/`, with a VOLATILE `index.md` + superseded bodies GC'd to git;
`checkpoints/` is **reserved**. Rule: per-item ephemeral artifacts are item-scoped; cross-item memory is
type-scoped.
