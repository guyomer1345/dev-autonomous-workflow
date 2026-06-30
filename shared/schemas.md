# Shared Artifact Schemas

The data formats that flow between capabilities. One source of truth — skills/agents reference these by
name. On-disk storage paths are still TBD (disk layout).

## spec
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

## roadmap  · produced by `planner` (decompose mode)
- `phases[]` — `{ name, goal, depends_on[], acceptance, commitment }`

## plan  · produced by `planner` (plan-one mode)
- `goal`
- `source_spec_ref`
- `decisions[]` — refs (by `id`) to the `decision-record`s this plan implements; every one must map to ≥1
  step or `planner` blocks the plan (D43 coverage gate).
- `risk_class` ∈ `{ code-only, data-additive, data-destructive, prod-touching }` (D42).
- `backup` — required when `risk_class` is destructive: `{ what, mechanism, verification, restore }`.
  `execute` refuses a destructive plan without it and runs+verifies it before the destructive step.
- `files_touched[]`
- `steps[]` — ordered, each independently verifiable
- `acceptance_criteria[]` — the definition-of-done; each `{ criterion, gate: artifact | human-qa }`.
  `artifact` → checked by `verify`; `human-qa` → confirmed by a `checkpoint` (kind=qa). **Every criterion is
  one or the other** — `planner` emits no un-checkable criterion (D30). A plan with zero `human-qa` criteria
  never triggers a QA checkpoint.

## changelog  · produced by `execute`
- `plan_ref`
- `actions[]` — `{ step, files, result }`
- `divergences[]` — `{ step, expected, actual, why }`

## verify-verdict  · produced by `verify`
- `pass`
- `mismatches[]` — `{ expected, actual }`
- `confidence`

## decision-record  · produced by `decision-engineer`
- `id` — stable id (e.g. `D-001`); `plan.decisions[]` reference these, and coverage is checked id → step
- `question`
- `options[]`
- `chosen`, `why`
- `confidence`
- `sources[]`

## debug-report  · produced by `debug` (also the knowledge-base `# Sessions` entry format)
- `symptom`, `cause`, `fix`, `avoid`
- `confidence`

## checkpoint  · the `checkpoint` gate
- `request` — `{ kind: demo|qa|setup, what, expected, how?(←setup-guide), blocking: true }`
- `verdict` — `{ pass, notes }`  · pass → continue · fail → debug→refine

## issue  · produced by `create-issue`, closed by `close-issue`
- `{ title, kind: bug|feature|debt, description, severity, source }`
- `github_ref` — the mirrored GitHub issue number (`create-issue` opens it; `close-issue` closes it)
- **open/closed state lives in GitHub** (source of truth) — the backlog holds only `github_ref`, never a
  duplicated local `state` (D55), so `close-issue` writes no local loop-bookkeeping.

## state.json  · the live loop pointer (volatile, gitignored) — D53
- `status` ∈ `{ intake, building, idle }`
- `node` — current loop node; value ∈ the `loop.md` node labels (e.g. `planner:plan-one`, `verify`)
- `current_item` — backlog id or `null` · `wave` — wave id or `null` · `note` — human-readable cursor

## handoff.md  · the durable resume anchor (committed) — D53
- `current_item`, `loop_position`, `parked[]`. A cold start reads this + `git log` and rebuilds position.

## per-item artifacts  · on disk — D53
`plan` / `changelog` / `verify-verdict` / `debug-report` live under `.workflow/items/<id>/`; `decision-record`s
and `checkpoint`s stay global under `.workflow/decisions/` and `.workflow/checkpoints/`.
