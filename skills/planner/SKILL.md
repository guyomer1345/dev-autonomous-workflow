---
name: planner
description: Turn a settled spec or a backlog item into an executable plan. Two modes — decompose a whole project or heavy change into a phased roadmap, or plan a single item into a step-by-step plan file. Runs after discussion settles or when prioritize picks an item.
---

# Planner — spec/item → executable plan

Core principle: produce the plan others execute against; raise any real build decision rather than guessing.

## Modes
- **decompose** (new project / heavy change): `spec` → `roadmap` of phases, each with goal, deps,
  acceptance. Each phase becomes a backlog item with its own plan → execute → verify → document sub-loop.
- **plan-one** (a picked item): item + project knowledge graph → a `plan` (goal, files_touched, ordered
  verifiable steps, `acceptance_criteria` = the definition-of-done).

## Inputs
- decompose: the `spec`.
- plan-one: the picked backlog item + the project knowledge graph.

## Workflow
1. Read the `spec` (decompose) or the item + knowledge graph (plan-one).
2. Map purpose → concrete changes; list the files touched; write ordered, independently-verifiable steps.
3. Tag each `acceptance_criterion` `gate: artifact | human-qa` — `human-qa` is what later triggers a qa
   `checkpoint`; default to `artifact`.
4. **Set `risk_class`** (`code-only` · `data-additive` · `data-destructive` · `prod-touching`). When it is
   destructive, author the required **`backup`** block (`what / mechanism / verification / restore`) —
   `execute` verifies it before the destructive step and refuses the plan without it.
5. **Decision-coverage gate:** list every governing decision in `plan.decisions[]` and confirm each maps to
   ≥1 step. An unmapped decision **blocks** the plan — escalate rather than let resolved intent silently
   evaporate between the decision and execution.
6. **Promise-coverage gate (impact-scoped):** for each impact-flagged decision, map every
   `decision-record.promises[]` entry to an `acceptance_criterion` (its `test_ref`). A `universal` promise's
   criterion must be **`boundary`-tagged** — a case drawn from *outside* the implementation's own enumerated
   set, because one in-scope example can't discharge a "for-any" claim (a floor is only a floor at the edge it
   must cover; prefer a property/structural check over the complement of the build's enumeration). Write the
   resolved links + criterion ids to `.workflow/items/<id>/promises.json`; `check_promise_coverage.py` (in
   `checks.sh --check`) **blocks** an unlinked or non-boundary promise. Reversible tier-0 decisions carry no
   promises → nothing to map. This gate proves *linkage*, not adequacy — the boundary/property test is what
   makes the discharge real.
7. Raise any genuine build decision to `decision-engineer` rather than guessing (e.g. a `TBD → stack`
   pointer left by `discuss`).

## Output
`roadmap` (decompose) → backlog · or `plan` (plan-one) → `execute`. In plan-one, `planner` `mkdir`s
`.workflow/items/<id>/` on demand and writes `plan.md` there — the first per-item artifact.

## Route
→ `execute` (plan-one) · → backlog / `prioritize` (decompose).

## Calls
`decision-engineer` (when an open decision blocks the plan).
