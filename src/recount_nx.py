#!/usr/bin/env python3
"""Segundo detector (networkx) para los censos sin C16: cuenta, sobre graph6 de stdin,
cuantos grafos NO contienen C_L, y verifica de paso orden y 3-regularidad.

Independiente de filter_eg: reutiliza el DFS de check_pow2.py (networkx).

Uso:  ... | venv/bin/python recount_nx.py L N_ESPERADO etiqueta
"""
import sys
import networkx as nx

from check_pow2 import has_cycle


def main():
    L = int(sys.argv[1])
    n_exp = int(sys.argv[2])
    tag = sys.argv[3] if len(sys.argv) > 3 else "?"
    tot = free = badn = baddeg = 0
    for line in sys.stdin:
        g6 = line.strip()
        if not g6:
            continue
        tot += 1
        G = nx.from_graph6_bytes(g6.encode())
        if G.number_of_nodes() != n_exp:
            badn += 1
        if any(d != 3 for _, d in G.degree()):
            baddeg += 1
        if not has_cycle(G, L):
            free += 1
    print(f"[{tag}] tot={tot} sinC{L}={free} mal_n={badn} mal_grado={baddeg}", flush=True)


if __name__ == "__main__":
    main()
