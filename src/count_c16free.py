#!/usr/bin/env python3
"""Verdad de tierra para calibrar el propagador de C16 de SMS.

Cuenta, sobre graph6 leidos de stdin, cuantos grafos NO contienen ciclo de la
longitud pedida (por defecto 16). El recuento es distinto de cero, que es lo que
hace util el test: una tuberia sobre-restringida devuelve 0 y pasa cualquier
comprobacion cuya respuesta correcta sea 0.

Puro python, sin dependencias; reutiliza el parser y el DFS con bitmask de
filter_eg.py (n <= 62).

Uso:  geng -c -d3 -D3 N | python3 count_c16free.py 16 [etiqueta] [--dump FICHERO]
"""
import sys
import time

from filter_eg import has_cycle, parse_g6


def main():
    L = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    tag = sys.argv[2] if len(sys.argv) > 2 else "?"
    dump = None
    if "--dump" in sys.argv:
        dump = open(sys.argv[sys.argv.index("--dump") + 1], "wb")

    t0 = time.time()
    tot = free = 0
    for line in sys.stdin.buffer:
        raw = line.strip()
        if not raw:
            continue
        tot += 1
        if tot % 500_000 == 0:
            r = tot / (time.time() - t0)
            print(f"[{tag}] {tot:,} procesados, {free} sin C{L} ({r:,.0f}/s)",
                  file=sys.stderr, flush=True)
        n, adj = parse_g6(raw)
        if L > n or not has_cycle(adj, n, L):
            free += 1
            if dump:
                dump.write(raw + b"\n")

    dt = time.time() - t0
    if dump:
        dump.close()
    print(f"[{tag}] FIN: {tot:,} grafos, {free} sin C{L}, {dt:.1f}s "
          f"({tot / max(dt, 1e-9):,.0f}/s)", flush=True)


if __name__ == "__main__":
    main()
