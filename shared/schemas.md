# Shared Artifact Schemas

The data formats that flow between capabilities. One source of truth — skills/agents reference these by
name. On-disk storage paths are still TBD (disk layout, `05`).

## spec
The product definition `discuss` produces and the whole build runs against.
- `audience` — who it's for (D20)
- `runtime` — where it runs (D20)
- `purpose`
- `screens[]` — `{ name, role, commitment }`
- `features[]` — `{ name, purpose, acceptance_criteria, commitment }`
- `data_model`
- `integrations[]` — `{ name, kind: auth|payments|…, → triggers a setup checkpoint }`
- `tech_stack` — value | `"TBD → decision-engineer"`
- `commitment` ∈ `{ locked, provisional, unspecified }` (D23) — tagged per element

## roadmap  · produced by `planner` (decompose mode)
- `phases[]` — `{ name, goal, depends_on[], acceptance, commitment }`

## plan  · produced by `planner` (plan-one mode)
- `goal`
- `source_spec_ref`
- `files_touched[]`
- `steps[]` — ordered, each independently verifiable
- `acceptance_criteria` — the definition-of-done (D17)

## changelog  · produced by `execute`
- `plan_ref`
- `actions[]` — `{ step, files, result }`
- `divergences[]` — `{ step, expected, actual, why }`

## verify-verdict  · produced by `verify`
- `pass`
- `mismatches[]` — `{ expected, actual }`
- `confidence`

## decision-record  · produced by `decision-engineer`
- `question`
- `options[]`
- `chosen`, `why`
- `confidence`
- `sources[]`

## debug-report  · produced by `debug` (also the Space-6 `# Sessions` entry format, D13)
- `symptom`, `cause`, `fix`, `avoid`
- `confidence`

## checkpoint  · the `checkpoint` gate
- `request` — `{ kind: demo|qa|setup, what, expected, how?(←setup-guide), blocking: true }`
- `verdict` — `{ pass, notes }`  · pass → continue · fail → debug→refine

## issue  · produced by `create-issue`
- `{ title, kind: bug|feature|debt, description, severity, source }`
