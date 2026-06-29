# 06 — Knowledge Structure (Space 6)

## Goal **[DECIDED]**
A per-project, LLM-optimized knowledge base the workflow inherently builds and reads — the thing that
lets it document-as-it-goes and stay autonomous. Two halves: a **code graph** + **per-file
experiential memory**.

## Lineage **[DECIDED — D1 research]**
- **Karpathy's LLM-Wiki** = the pattern → **ADOPT** (`index.md` + append-only `log.md`,
  wikilinks/backlinks, ingest/query/lint).
- **OKF (Open Knowledge Format)** = the formalized on-disk schema → **ADAPT** (directory of markdown,
  frontmatter with a required `type`, relative-link edges, reserved `index.md`/`log.md`).
- **llms.txt** = thin root manifest / agent entry point → small role.

## Schema **[DECIDED — format only]**
`.knowledge/` committed with the repo:
```
.knowledge/
├── llms.txt          # agent entry point (H1 + summary + pointers)
├── index.md          # catalog of all nodes
├── graph.json        # machine-readable typed edge list
└── nodes/<repo-path>/<file>.md   # one node per source file
```
Per-file node:
- **frontmatter:** `type`, `path`, `purpose` (the file's job), `tags`, `last_reviewed`.
- **typed, directional edges:** `affects` / `affected_by`, each with a `why` (store `affects` as
  primary; derive `affected_by` as backlinks to avoid drift).
- **a `# Sessions` append-only log:** postmortems (`## [date] kind | title` + Symptom/Cause/Fix/Avoid)
  — the per-file debug memory.

## Purpose: code-derived vs spec-derived **[DECIDED]**
Store both: **intent** (from spec/roadmap) and **actual role** (from code). Divergence between them is
itself a signal (drift / scope creep / bug).

## Steal from prior art **[DECIDED]**
Aider repomap (tree-sitter + PageRank): auto-extract *structural* edges (imports/calls) mechanically,
so the LLM only authors the *semantic* `why` + impact judgment. (Code Property Graph validates typed
edges; nobody combines a typed impact-graph + per-file memory → open intersection.)

## Granularity **[DECIDED]**
Start file-level; leave a seam for symbol/function-level later.

## Maintenance / freshness **[OPEN — intentionally not closing now]**
How the graph + sessions stay current as code changes (regenerate vs incremental-on-edit vs a loop
step; staleness markers; an audit pass). Just need to know it exists. → see 07.
