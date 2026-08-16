#!/bin/bash
# Verdad de tierra para el propagador de C16: cuenta cubicos conexos SIN C16 por
# enumeracion con geng, repartida en W trozos con res/mod. Son anclas NO-CERO, que son
# las unicas que detectan una tuberia sobre-restringida.
# Uso: run_groundtruth.sh N [W]
# Se ejecuta con nice para no robarle CPU al run secuencial del registro.
set -u
N=$1; W=${2:-6}
OUT=resultados/calibracion/groundtruth_n$N
mkdir -p "$OUT"
GENG=./nauty2_8_9/geng

echo "[$(date -Iseconds)] n=$N en $W trozos"
for r in $(seq 0 $((W-1))); do
  ( nice -n 15 $GENG -c -d3 -D3 -q $N $r/$W 2>/dev/null \
    | nice -n 15 python3 count_c16free.py 16 "n${N}r${r}" > "$OUT/r$r.txt" 2> "$OUT/r$r.err" ) &
done
wait

python3 - "$OUT" "$N" <<'EOF'
import re, sys, glob, os
out, n = sys.argv[1], sys.argv[2]
tot = free = 0
for f in sorted(glob.glob(os.path.join(out, "r*.txt"))):
    m = re.search(r"FIN: ([\d,]+) grafos, (\d+) sin C16", open(f).read())
    if not m:
        print("TROZO INCOMPLETO:", f); sys.exit(1)
    tot += int(m.group(1).replace(",", "")); free += int(m.group(2))
line = f"n={n}: {tot} cubicos conexos, {free} sin C16"
print(line)
open(os.path.join(out, "TOTAL.txt"), "w").write(line + "\n")
EOF
echo "[$(date -Iseconds)] fin n=$N"
