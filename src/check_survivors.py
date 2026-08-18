#!/usr/bin/env python3
"""Test a posteriori de las potencias de 2 sobre supervivientes de la escalera.

La escalera prohíbe {C4, C8, C16} DENTRO de la búsqueda (ver nota, "decoupling");
las potencias grandes (C32, C64, ...) quedan fuera y hay que testarlas aquí, sobre
los supervivientes que vuelque sms_run.py --dump (una línea por grafo, lista de
aristas estilo [(0,21),(0,22),...]). Reutiliza el detector de ciclos de filter_eg
(independiente de SMS) y re-comprueba también 4/8/16 como defensa.

Un grafo sin NINGÚN ciclo de longitud potencia de 2 es un contraejemplo de
Erdős–Gyárfás.

Uso:    python3 check_survivors.py supervivientes.txt
Salida: una línea por grafo + resumen. Código de salida 1 si hay contraejemplo.
"""
import ast
import sys

from filter_eg import has_cycle


def main():
    path = sys.argv[1]
    tot = contraejemplos = 0
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            edges = ast.literal_eval(line)
            # cúbico: ningún vértice aislado, todos aparecen en alguna arista
            n = max(max(e) for e in edges) + 1
            adj = [[] for _ in range(n)]
            for a, b in edges:
                adj[a].append(b)
                adj[b].append(a)
            tot += 1
            lengths = []
            L = 4
            while L <= n:
                lengths.append(L)
                L *= 2
            found = {L: has_cycle(adj, n, L) for L in lengths}
            print(f"grafo {tot}: n={n} " +
                  " ".join(f"C{L}={'si' if v else 'no'}" for L, v in found.items()))
            if not any(found.values()):
                contraejemplos += 1
                print(f"!!! CONTRAEJEMPLO ERDOS-GYARFAS: {line}")
    print(f"total={tot} contraejemplos={contraejemplos}")
    return 1 if contraejemplos else 0


if __name__ == "__main__":
    sys.exit(main())
