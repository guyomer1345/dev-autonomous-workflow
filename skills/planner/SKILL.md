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
4. Raise any genuine build decision to `decision-engineer` rather than guessing (e.g. a `TBD → stack`
   pointer left by `discuss`).
5. **Session-sizing:** in plan-one, split the plan if one ≤200k-token session can't finish it, or if it
   spans more than one logical unit. Each split is its own plan/item.

## Output
`roadmap` (decompose) → backlog · or `plan` (plan-one) → `execute`.

## Route
→ `execute` (plan-one) · → backlog / `prioritize` (decompose).

## Calls
`decision-engineer` (when an open decision blocks the plan).
