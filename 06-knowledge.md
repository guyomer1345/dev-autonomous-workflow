# 06 — Knowledge Structure (Space 6)

## Goal **[DECIDED]**
A per-project, LLM-optimized knowledge base the workflow inherently builds and reads — the thing that
lets it document-as-it-goes and stay autonomous. Two halves: a **code graph** + **per-file
experiential memory**.

## Lineage **[DECIDED — D1 research]**
- **Karpathy's LLM-Wiki** = the pattern → **ADOPT** (`index.md` + an append-only log,
  wikilinks/backlinks, ingest/query/lint). *Our schema carries the append-only log as the per-file
  `# Sessions` sections inside each node, not a separate `log.md` (D59).*
- **OKF (Open Knowledge Format)** = the formalized on-disk schema → **ADAPT** (directory of markdown,
  frontmatter with a required `type`, relative-link edges, reserved `index.md`/`log.md`).
- **llms.txt** = thin root manifest / agent entry point → small role.

## Schema **[DECIDED — format only; located by D62]**
`docs/knowledge/` committed with the repo; a thin `llms.txt` sits at `<project_root>/` and points in (D62):
```
<project_root>/
├── llms.txt              # agent entry point (H1 + summary + pointers)
└── docs/knowledge/
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

## Generated vs durable — the split **[DECIDED — D39, sharpens the above]**
The two halves sit on opposite sides of the design law (`shared/memory-model.md`, D38): the **structural
graph** (`graph.json`, imports/calls) is **generated** (tree-sitter/repomap) — regenerable, never
authoritative prose, never hand-edited (a hand-maintained map goes stale and lies). The **experiential
memory** (per-file `why` + the `# Sessions` postmortems) is the **only durable hand-written layer** — the
non-derivable intent that earns its tokens. (Code Property Graph is overkill for context — security-scan
step only.)

## Granularity **[DECIDED]**
Start file-level; leave a seam for symbol/function-level later.

## Maintenance / freshness **[DECIDED — D61 closed the mechanisms]**
The structural graph regenerates (it cannot drift); `document` keeps durable docs + the inline-C4 architecture
doc fresh in the **same item as the code**; an `audit` pass keeps guidance high-signal. **Retention (D61):**
each node's `# Sessions` is **cap-and-archived** — last-*K* raw entries on disk, older entries dropped to git
with a one-line archive pointer; a deterministic script does this, so the entry format is **strict/lint-parseable**
(`## [date] kind | title`) to split entries mechanically. A `Lessons` zone (distilled patterns) is left as a
**deferred** signal-quality feature. **Staleness** = a diff-based signal (code changed without its node) that
schedules a doc-fix, not a prune. Still open: regenerate-vs-incremental for the graph (`07`).
