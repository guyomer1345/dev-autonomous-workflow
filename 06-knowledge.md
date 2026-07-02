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
    ├── graph.json        # machine-readable typed edge list + per-node centrality (impact & orchestration)
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
edges; nobody combines a typed impact-graph + per-file memory → open intersection.) We steal the
*approach*, not the *tool* — see the generator decision below (D68).

## Generated vs durable — the split **[DECIDED — D39, sharpens the above]**
The two halves sit on opposite sides of the design law (`shared/memory-model.md`, D38): the **structural
graph** (`graph.json`, imports/calls) is **generated** (mechanically, from imports/calls) — regenerable, never
authoritative prose, never hand-edited (a hand-maintained map goes stale and lies). The **experiential
memory** (per-file `why` + the `# Sessions` postmortems) is the **only durable hand-written layer** — the
non-derivable intent that earns its tokens. (Code Property Graph is overkill for context — security-scan
step only.)

## Generation, the two lenses & the node seed **[DECIDED — D68, pressure-tested on a real repo]**
- **Generator = an own script per stack, not an external tool.** `/start` emits a `.workflow/` code-map
  generator the same way it emits `checks.sh`: Python via stdlib `ast`, other stacks via a zero-dep
  regex-extraction + per-language resolver arm (tree-sitter reserved for parse-hard languages — D74). Regenerable,
  near-zero-dep, cheap to re-run. *External tools were tested and rejected:*
  `repomix` packs context (signatures + token counts), not a typed import graph; aider-repomap does the graph
  but is a heavyweight install to ship into every consuming project.
- **`graph.json` carries TWO centrality lenses, not one "importance" rank** — both fall out of the same
  import graph for free:
  - **impact** (forward PageRank — most-depended-upon): *"if this changes, what ripples?"* → `debug` /
    `planner` blast-radius.
  - **orchestration** (reverse PageRank / fan-out — composes many): *"where does behaviour live / where does
    feature X go?"*
  Neither is "importance." The run showed impact centrality surfaces the *data foundation* (models, config,
  base) and buries the *behavioural core*; orchestration surfaces the engine + ingestion + flow routes. The
  **product narrative itself** (what the app is *for*, what counts as core) is in neither lens — it is pure
  intent, carried only by the durable layer + the ingested `CLAUDE.md`/spec.
- **Three-tier node seed** (makes "eager graph, lazy semantics" safe — a lazy node is never an empty shell):
  - `[G]` **generated-structural** — path, type, edge targets, the two lenses. **All files, eager.**
  - `[X]` **generated-extractive** — a cheap LLM-summarised `purpose.actual` + tags, for a prioritised set.
    **The prioritised set = both lenses (impact ∪ orchestration) ∪ the spec's declared core flows — never
    impact alone**, else seeding documents the plumbing and skips the behavioural core (the miss the two lenses
    exist to prevent). Mechanism deferred to implementation.
  - `[D]` **durable** — the non-derivable `why` / intent-vs-actual / `# Sessions`. **Authored on touch** by
    `document`. This is the layer that earns its tokens — the product.

## Multi-language coverage **[DECIDED — D72, research-ranked by prevalence]**
Coverage is **three tiers**, not D70's arm-vs-fallback binary (whose fallback was never built — so *today* a
non-Python repo gets no graph at all, empty not degraded). What varies by language is only **edge resolution**;
the node set + directory clusters are identical everywhere and the two lenses inherit edge quality — so the cost
of a language is its **resolver**, not its parser.
- **Tier 0 — generic floor** (dir tree + shallow-regex imports, zero-dep): the long-tail safety net so an
  un-armed repo still gets nodes + clusters. The floor, not the strategy. **Node-recognition ≠ edge-extraction**
  (D75): the floor *nodes* any recognized source language (so an exotic-language repo still gets nodes+clusters —
  "never nothing"), and adds *edges* only for the subset with an import regex; resolution is family-scoped
  (intra-language, C/C++ share). Graphless data/markup/config/doc artifacts are excluded (no import graph).
- **The default precise arm = zero-dep** (D74): the floor's regex extraction + a real per-language **resolver**.
  The cost is the resolver, not the parser — Python (stdlib `ast`) and **JS/TS** (tsconfig/jsconfig `paths`+`baseUrl`
  aliases + TS extension/index/barrel resolution) are both this. A precise arm subclasses the floor, so no-config →
  it degrades exactly to the floor.
- **tree-sitter = reserved, not the mechanism** (D74 revises D72). Reach for it only where a language's *lexical
  structure* genuinely defeats regex extraction (e.g. C/C++ preprocessor/templates), shipped as a **graceful
  optional upgrade** (absent → the floor). Rejected as the default: the Python binding is version-fragile across
  environments, and for JS/TS the value was resolution, not parsing.
**Build set = prevalence, not ease** (Octoverse/SO/RedMonk 2024–25): Python (done) → JS/TS (one arm) → Java → C#
→ C++ — GitHub's "~80% of new repos = six languages" set — then Go / Rust / PHP. Because repos are polyglot
(median ~3 / mean ~4.5 languages), ~5 arms resolve most of *most* repos. Ease breaks ties on **order only**: Go is
pulled early (compiler-grade graph, near-free), C++ sequences last in-wave (needs `compile_commands.json`).
Graphless artifacts (SQL, HTML/CSS, shell, JSON/YAML, Markdown, Dockerfile, HCL) are **not** arms — no
file-to-file import graph. Arms are **not demand-gated** — validation is free (any public repo), so the common set
is built up front; the Phase-4 demo forces exercising ≥1 non-Python arm.
**Built (D73/D74):** the shared engine + tier-0 floor + two precise arms ship as `scripts/codemap/codemap.py` —
one language-agnostic driver over pluggable arms (add a language = `extensions` + `index()` + `edges()`, driver
untouched). Precise arms: **Python** (`ast`) and **JS/TS** (`JsTsArm` — tsconfig `paths`/`baseUrl` + extension/index
resolution; beats the floor 4-vs-1 on an alias fixture; no tsconfig → == the floor). Every other recognized source
language falls to the floor — noded regardless (D75), with edges where a regex exists. Next arms (Java, C#, Go, …)
are zero-dep resolver arms like `JsTsArm`; tree-sitter stays reserved for parse-hard languages.

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
