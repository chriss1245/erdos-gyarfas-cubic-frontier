#!/usr/bin/env python3
"""Driver local de SMS (sin Modal) para la caza Erdős–Gyárfás en la clase cúbica.

Equivalente propio de `_run_smsg` del repositorio de Balaji, con tres diferencias
deliberadas:

  * grado EXACTAMENTE 3 (minDegree(3) + maxDegree(3)), no grado mínimo >= 3, para
    poder comparar con nuestros censos exhaustivos de cúbicos;
  * conectividad activada (-c), porque los censos de Markström y nuestros barridos
    con `geng -c` son de grafos conexos;
  * el cutoff del chequeo de minimalidad se puede desactivar (--cutoff 0): con el
    valor por defecto (200000) la ruptura de simetría es incompleta y puede contar
    isomorfos repetidos, lo que inflaría los recuentos.

Nunca convierte un timeout en UNSAT: si el proceso agota el presupuesto devuelve
estado WALL, y si no se puede parsear el recuento devuelve ERROR.

Uso:
    python3 sms_run.py --n 18 --forbid 16
    python3 sms_run.py --n 24 --forbid 4,8 --dump n24.g6
    python3 sms_run.py --n 32 --forbid 4,8,16 --budget 86400
"""
import argparse
import json
import os
import subprocess
import sys
import time

CONDA = "/home/ubuntu/miniconda3/envs/eg_sms_env"
SMSG = os.path.expanduser("~/.local/bin/smsg")


def write_cycle_file(path, lengths):
    """Fichero de subgrafos prohibidos: un ciclo por linea,
    'k v0 v1 v1 v2 ... v(k-1) v0' (mismo formato que usa SMS)."""
    with open(path, "w") as f:
        for k in lengths:
            edges = []
            for i in range(k):
                edges += [i, (i + 1) % k]
            f.write(f"{k} " + " ".join(map(str, edges)) + "\n")


def build_cnf(n, path, degree=3, counter="sequential"):
    """CNF de grado exactamente `degree` sobre las C(n,2) variables de arista."""
    from pysms.graph_builder import GraphEncodingBuilder

    b = GraphEncodingBuilder(n, directed=False)
    b.minDegree(degree, countertype=counter)
    b.maxDegree(degree, countertype=counter)
    with open(path, "w") as fh:
        b.print_dimacs(fh)


def parse_count(stdout):
    for line in stdout.splitlines():
        if line.strip().startswith("Number of graphs:"):
            return int(line.split(":")[1].strip())
    return None


def run(n, lengths, budget, degree=3, counter="sequential", cutoff=0,
        connected=True, dump=None, extra=None, exists=False):
    """Si `exists` es True, para en la primera solucion (control positivo: la
    respuesta correcta es SAT, no 0, y por tanto detecta sobre-restriccion)."""
    workdir = os.environ.get("SMS_WORKDIR", "/tmp")
    cnf = f"{workdir}/eg_cnf_n{n}_{degree}_{counter}.cnf"
    cyc = f"{workdir}/eg_cyc_{'_'.join(map(str, lengths))}.txt"
    build_cnf(n, cnf, degree=degree, counter=counter)
    write_cycle_file(cyc, lengths)

    cmd = [SMSG, "--vertices", str(n)]
    if not exists:
        cmd.append("--all-graphs")
    if connected:
        cmd.append("--connected")
    if dump is None and not exists:
        cmd.append("--hide-graphs")
    cmd += ["--cutoff", str(cutoff)]
    cmd += ["--forbidden-subgraph-file", cyc, "--dimacs", cnf]
    if extra:
        cmd += list(extra)

    env = dict(os.environ)
    env["LD_LIBRARY_PATH"] = f"{CONDA}/lib:{os.path.expanduser('~/.local/lib')}"

    t0 = time.monotonic()
    try:
        p = subprocess.run(cmd, capture_output=True, text=True,
                           timeout=budget, env=env)
    except subprocess.TimeoutExpired:
        return {"n": n, "forbid": lengths, "count": None, "status": "WALL",
                "elapsed": round(time.monotonic() - t0, 2), "cmd": " ".join(cmd)}
    elapsed = round(time.monotonic() - t0, 2)

    if exists:
        # returncode 10 = encontrada una solucion; 20 = ninguna (UNSAT)
        found = (p.returncode == 10)
        return {"n": n, "forbid": lengths, "count": (1 if found else 0),
                "status": ("SAT" if found else "UNSAT"),
                "elapsed": elapsed, "returncode": p.returncode,
                "cmd": " ".join(cmd), "stdout_tail": p.stdout[-800:]}

    count = parse_count(p.stdout)
    if count is None:
        status = "ERROR"
    elif count == 0:
        status = "UNSAT"
    else:
        status = "SAT"

    if dump and count:
        with open(dump, "w") as f:
            for line in p.stdout.splitlines():
                s = line.strip()
                # smsg imprime los grafos como listas de aristas; se guardan crudos
                if s and not s[0].isalpha():
                    f.write(s + "\n")

    return {"n": n, "forbid": lengths, "count": count, "status": status,
            "elapsed": elapsed, "returncode": p.returncode,
            "cmd": " ".join(cmd), "stdout_tail": p.stdout[-800:],
            "stderr_tail": p.stderr[-400:]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--forbid", required=True,
                    help="longitudes de ciclo prohibidas, p.ej. 4,8,16")
    ap.add_argument("--budget", type=float, default=3600.0, help="segundos")
    ap.add_argument("--degree", type=int, default=3)
    ap.add_argument("--counter", default="sequential",
                    choices=["sequential", "totalizer"])
    ap.add_argument("--cutoff", type=int, default=0,
                    help="cutoff del chequeo de minimalidad (0 = sin cutoff)")
    ap.add_argument("--disconnected", action="store_true")
    ap.add_argument("--exists", action="store_true",
                    help="control positivo: parar en la primera solucion")
    ap.add_argument("--dump", default=None)
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    lengths = [int(x) for x in args.forbid.split(",")]
    rec = run(args.n, lengths, args.budget, degree=args.degree,
              counter=args.counter, cutoff=args.cutoff,
              connected=not args.disconnected, dump=args.dump,
              exists=args.exists)
    print(json.dumps(rec, indent=2))
    if args.json:
        with open(args.json, "w") as f:
            json.dump(rec, f, indent=2)
    sys.exit(0 if rec["status"] in ("SAT", "UNSAT") else 1)


if __name__ == "__main__":
    main()
