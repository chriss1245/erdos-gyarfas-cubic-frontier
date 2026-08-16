#!/usr/bin/env python3
"""Count stdin graph6 graphs containing no cycle of length 8 nor 16.

Independent reference for the pruned generator: uses only src/filter_eg.py
(pure Python, no third-party dependencies).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from filter_eg import parse_g6, has_cycle  # noqa: E402

count = 0
for line in sys.stdin.buffer:
    raw = line.strip()
    if not raw:
        continue
    n, adj = parse_g6(raw)
    if not has_cycle(adj, n, 8) and (n < 16 or not has_cycle(adj, n, 16)):
        count += 1
print(count)
