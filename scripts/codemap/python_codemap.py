#!/usr/bin/env python3
"""Code-map extractor (Python arm) — emits the structural knowledge layer as graph.json.

Produces a typed import graph plus two centrality signals per file, computed from the
same graph so both come for free:
  - impact        (forward PageRank: most-depended-upon)  -> change blast-radius
  - orchestration (reverse PageRank: composes many)       -> where behaviour lives

This is the GENERATED structural layer: regenerable, never authoritative prose, never
hand-edited. The durable per-file `why` and Sessions log live in the node .md files and
are authored on touch; this tool never writes those. One language arm of the per-stack
code-map generator that /start wires (Python uses the stdlib ast — no external deps;
other stacks use tree-sitter / the native parser, same graph.json contract).

Usage:  python_codemap.py [ROOT] [--out PATH] [--exclude a,b,c]
  ROOT      directory to scan (default: .). Run from the import root so module names
            match import statements (e.g. repo root for `from pkg.mod import x`).
  --out     output path (default: docs/knowledge/graph.json).
"""
import argparse
import ast
import collections
import json
import os
import sys

DEFAULT_EXCLUDE = (
    ".git", ".venv", "venv", "node_modules", "__pycache__",
    "migrations", "dist", "build", ".mypy_cache", ".pytest_cache", ".ruff_cache",
)


def discover(root, exclude):
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in exclude]
        for fn in filenames:
            if fn.endswith(".py"):
                files.append(os.path.normpath(os.path.join(dirpath, fn)))
    return sorted(files)


def module_name(path):
    """Module dotted-name relative to cwd (the import root)."""
    rel = os.path.relpath(path).replace(os.sep, ".")
    if rel.endswith(".py"):
        rel = rel[:-3]
    if rel.endswith(".__init__"):
        rel = rel[: -len(".__init__")]
    return rel


def resolve(mod, mod2file):
    """Resolve a dotted module (or a prefix of it) to a known project file, else None."""
    cand = mod
    while cand:
        if cand in mod2file:
            return mod2file[cand]
        cand = cand.rsplit(".", 1)[0] if "." in cand else ""
    return None


def import_targets(tree, self_mod):
    """Yield dotted module names this file imports (absolute + relative resolved)."""
    self_pkg = self_mod.rsplit(".", 1)[0] if "." in self_mod else ""
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.level:  # relative: climb `level` packages from self
                base = self_pkg
                for _ in range(node.level - 1):
                    base = base.rsplit(".", 1)[0] if "." in base else ""
                mod = f"{base}.{node.module}" if node.module else base
            else:
                mod = node.module or ""
            if mod:
                yield mod
                for alias in node.names:  # `from pkg import sub` may name a submodule
                    yield f"{mod}.{alias.name}"
        elif isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name


def pagerank(nodes, out_edges, damping=0.85, iterations=60):
    n = len(nodes)
    if n == 0:
        return {}
    pr = {x: 1.0 / n for x in nodes}
    for _ in range(iterations):
        nxt = {x: (1 - damping) / n for x in nodes}
        dangling = damping * sum(pr[x] for x in nodes if not out_edges.get(x)) / n
        for x in nodes:
            nxt[x] += dangling
        for src, dsts in out_edges.items():
            if dsts:
                share = damping * pr[src] / len(dsts)
                for dst in dsts:
                    nxt[dst] += share
        pr = nxt
    return pr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--out", default="docs/knowledge/graph.json")
    ap.add_argument("--exclude", default="")
    args = ap.parse_args()

    exclude = set(DEFAULT_EXCLUDE) | {e for e in args.exclude.split(",") if e}
    files = discover(args.root, exclude)
    mod2file = {module_name(p): p for p in files}

    # forward edges: file -> file it imports (deduped, intra-project only)
    fwd = collections.defaultdict(set)
    parse_failures = []
    for path in files:
        try:
            tree = ast.parse(open(path, encoding="utf-8", errors="replace").read(), filename=path)
        except SyntaxError as exc:
            parse_failures.append((path, str(exc)))
            continue
        self_mod = module_name(path)
        for mod in import_targets(tree, self_mod):
            target = resolve(mod, mod2file)
            if target and target != path:
                fwd[path].add(target)

    nodes = [os.path.relpath(p) for p in files]
    key = {p: os.path.relpath(p) for p in files}
    fwd_edges = {key[a]: [key[b] for b in sorted(bs)] for a, bs in fwd.items()}
    rev_edges = collections.defaultdict(list)
    in_deg = collections.Counter()
    for a, bs in fwd_edges.items():
        for b in bs:
            rev_edges[b].append(a)
            in_deg[b] += 1

    impact = pagerank(nodes, fwd_edges)
    orchestration = pagerank(nodes, {k: list(v) for k, v in rev_edges.items()})

    node_records = [
        {
            "path": p,
            "type": "module",
            "impact": round(impact.get(p, 0.0), 6),
            "orchestration": round(orchestration.get(p, 0.0), 6),
            "in_degree": in_deg.get(p, 0),
            "out_degree": len(fwd_edges.get(p, [])),
        }
        for p in sorted(nodes)
    ]
    edge_records = sorted(
        ({"from": a, "to": b, "kind": "import"} for a, bs in fwd_edges.items() for b in bs),
        key=lambda e: (e["from"], e["to"]),
    )

    graph = {
        "generated_by": "codemap/python",
        "root": os.path.relpath(args.root),
        "node_count": len(node_records),
        "edge_count": len(edge_records),
        "nodes": node_records,
        "edges": edge_records,
    }
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(graph, fh, indent=2)
        fh.write("\n")

    print(
        f"codemap: {len(node_records)} nodes, {len(edge_records)} edges, "
        f"{len(parse_failures)} parse failures -> {args.out}",
        file=sys.stderr,
    )
    for path, err in parse_failures[:10]:
        print(f"  parse-fail: {path}: {err}", file=sys.stderr)


if __name__ == "__main__":
    main()
