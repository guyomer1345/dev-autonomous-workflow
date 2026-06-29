---
name: planner
description: Turn a settled spec or a backlog item into an executable plan. Two modes — decompose a whole project or heavy change into a phased roadmap, or plan a single item into a step-by-step plan file. Runs after discussion settles or when prioritize picks an item.
---

# Planner

## Modes
- **decompose** (new project / heavy change): `spec` → `roadmap` of phases, each with goal, deps,
  acceptance. Each phase becomes a backlog item with its own plan → execute → verify → document sub-loop.
- **plan-one** (a picked item): item + project knowledge graph → a `plan` (goal, files_touched, ordered
  verifiable steps, `acceptance_criteria` = the definition-of-done, D17).

## Do
1. Read the `spec` (decompose) or the item + knowledge graph (plan-one).
2. Map purpose → concrete changes; list the files touched; write ordered, independently-verifiable steps.
3. Raise any genuine build decision to `decision-engineer` rather than guessing (e.g. a `TBD → stack`
   pointer left by `discuss`).
4. **Session-sizing (D10):** in plan-one, split the plan if one ≤200k-token session can't finish it, or
   if it spans more than one logical unit. Each split is its own plan/item.

## Output
`roadmap` (decompose) → backlog · or `plan` (plan-one) → `execute`.

## Calls
`decision-engineer` (when an open decision blocks the plan).
