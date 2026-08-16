#!/usr/bin/env python3
"""Filtro Erdős–Gyárfás. Entrada: graph6 por stdin (cúbicos sin C4, de geng).
Descarta los que tienen C8; a los supervivientes les busca C16 (y C32 si n>=32).
Superviviente sin ningún ciclo de longitud potencia de 2 => CONTRAEJEMPLO.

Puro python, sin dependencias; bitmasks para el DFS (n <= 62).
Uso:  geng -c -d3 -D3 -f N [res/mod] | python3 filter_eg.py [etiqueta]
"""
import sys
import time


def parse_g6(raw):
    v = [c - 63 for c in raw]
    n = v[0]
    adj = [[] for _ in range(n)]
    pos, taken = 1, 0
    cur = v[1] if len(v) > 1 else 0
    for j in range(1, n):
        for i in range(j):
            if taken == 6:
                pos += 1
                cur = v[pos]
                taken = 0
            if cur & (1 << (5 - taken)):
                adj[i].append(j)
                adj[j].append(i)
            taken += 1
    return n, adj


def has_cycle(adj, n, L):
    """¿Existe ciclo simple de longitud exactamente L? (ancla = vértice mínimo)."""
    for s in range(n):
        stack = [(s, 1 << s, 0)]
        while stack:
            u, mask, d = stack.pop()
            nd = d + 1
            for w in adj[u]:
                if w == s:
                    if nd == L:
                        return True
                elif w > s and not (mask & (1 << w)) and nd < L:
                    stack.append((w, mask | (1 << w), nd))
    return False


def main():
    tag = sys.argv[1] if len(sys.argv) > 1 else "?"
    t0 = time.time()
    tot = surv = shown = 0
    for line in sys.stdin.buffer:
        raw = line.strip()
        if not raw:
            continue
        tot += 1
        if tot % 2_000_000 == 0:
            r = tot / (time.time() - t0)
            print(f"[{tag}] {tot:,} procesados, {surv} sin C4/C8 ({r:,.0f}/s)",
                  file=sys.stderr, flush=True)
        n, adj = parse_g6(raw)
        if has_cycle(adj, n, 8):
            continue
        surv += 1
        pow2 = [L for L in (16, 32) if L <= n]
        bad = next((L for L in pow2 if has_cycle(adj, n, L)), None)
        if bad is None:
            print(f"[{tag}] " + "!" * 60, flush=True)
            print(f"[{tag}] ¡¡¡CONTRAEJEMPLO ERDŐS–GYÁRFÁS!!!  n={n}  "
                  f"graph6: {raw.decode()}", flush=True)
            print(f"[{tag}] " + "!" * 60, flush=True)
        else:
            shown += 1
            if shown <= 25:
                print(f"[{tag}] sin C4/C8 (pero C{bad}): {raw.decode()}", flush=True)
    dt = time.time() - t0
    print(f"[{tag}] FIN: {tot:,} grafos, {surv} sin C4/C8, {dt:.1f}s "
          f"({tot / max(dt, 1e-9):,.0f}/s)", flush=True)


if __name__ == "__main__":
    main()
