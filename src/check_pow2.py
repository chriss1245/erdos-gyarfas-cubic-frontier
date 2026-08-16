#!/usr/bin/env python3
"""Verifica ciclos potencia de 2 en grafos graph6 (stdin). Independiente de filter_eg."""
import sys
import networkx as nx


def has_cycle(G, L):
    for s in sorted(G.nodes()):
        stack = [(s, frozenset([s]), 1)]
        while stack:
            u, vis, d = stack.pop()
            for w in G[u]:
                if w == s and d == L:
                    return True
                elif w > s and w not in vis and d < L:
                    stack.append((w, vis | {w}, d + 1))
    return False


if __name__ == "__main__":
    for line in sys.stdin:
        g6 = line.strip()
        if not g6:
            continue
        G = nx.from_graph6_bytes(g6.encode())
        n = G.number_of_nodes()
        status = {L: has_cycle(G, L) for L in (4, 8, 16, 32) if L <= n}
        print(f"{g6}  n={n} " + " ".join(f"C{L}={v}" for L, v in status.items()))
        if not any(status.values()):
            print(f"!!! POSIBLE CONTRAEJEMPLO ERDŐS–GYÁRFÁS: {g6}")
