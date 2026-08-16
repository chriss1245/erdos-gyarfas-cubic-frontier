#!/usr/bin/env python3
"""Unit tests for the exact-length cycle detector in src/filter_eg.py.

The detector answers "does G contain a simple cycle of length exactly L?".
We exercise it on small graphs whose full cycle spectrum is known by hand,
including the standard traps: even cycles in bipartite graphs, cycles longer
than the girth, and graphs with no cycles at all.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from filter_eg import parse_g6, has_cycle  # noqa: E402


def g6(s):
    n, adj = parse_g6(s.encode())
    return n, adj


def cycle_lengths(n, adj, upto):
    return {L for L in range(3, upto + 1) if has_cycle(adj, n, L)}


# graph6 strings generated with networkx (nx.to_graph6_bytes), not by hand
CASES = [
    # (name, graph6, expected set of simple-cycle lengths)
    ("C4 (4-cycle)",            "Cl",     {4}),
    ("K4",                      "C~",     {3, 4}),
    ("C8 (8-cycle)",            "GhCGKC", {8}),
    ("P4 (path, acyclic)",      "Ch",     set()),
    ("K3,3",                    "EFz_",   {4, 6}),
    # 3-cube Q3: bipartite cubic, cycles of lengths 4, 6, 8
    ("Q3 (3-cube)",             "Gr`HOk", {4, 6, 8}),
    # Petersen: girth 5, cycle spectrum {5, 6, 8, 9} — famously no C4 and no C7
    ("Petersen",                "IheA@GUAo", {5, 6, 8, 9}),
]


def main():
    failures = 0
    for name, s, expected in CASES:
        n, adj = g6(s)
        got = cycle_lengths(n, adj, n)
        status = "ok " if got == expected else "FAILED"
        if got != expected:
            failures += 1
        print(f"{status}      {name}: cycle lengths {sorted(got)}"
              + ("" if got == expected else f" (expected {sorted(expected)})"))
    if failures:
        sys.exit(f"{failures} detector test(s) failed")


if __name__ == "__main__":
    main()
