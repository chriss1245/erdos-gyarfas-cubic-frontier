#!/bin/bash
# Resolucion por cubos (cube-and-conquer nativo de SMS) de un orden de la escalera.
# Uso: run_cubos.sh N K WORKERS
# Genera los cubos con --simple-assignment-cutoff K, comprueba que cubren todo el espacio
# con --cube-file-test y resuelve cada cubo por separado con WORKERS procesos.
# NO se usa --simplify: pierde soluciones (n=28 da 241 en vez de 251, ver BITACORA 2026-08-15).
# Los cubos se solapan, asi que la suma sobreestima el recuento; solo es fiable el veredicto
# "suma cero" = no existe ningun grafo.
set -u
N=$1; K=$2; W=${3:-6}
PY=/home/ubuntu/miniconda3/envs/eg_sms_env/bin/python
export LD_LIBRARY_PATH=/home/ubuntu/miniconda3/envs/eg_sms_env/lib:/home/ubuntu/.local/lib
SMSG=$HOME/.local/bin/smsg
OUT=resultados/escalera/cubos_n$N
mkdir -p "$OUT"
CNF=/tmp/cubos_n${N}.cnf
CYC=/tmp/cubos_cyc_4_8_16.txt
CUBES=$OUT/cubos_K${K}.txt

$PY -c "
import sms_run
sms_run.build_cnf($N, '$CNF')
sms_run.write_cycle_file('$CYC', [4,8,16])
"

echo "[$(date -Iseconds)] cubando n=$N K=$K"
$SMSG --vertices $N --all-graphs --connected --cutoff 0 --hide-graphs \
      --forbidden-subgraph-file $CYC --dimacs $CNF \
      --prerun 2 --simple-assignment-cutoff $K 2>&1 | grep '^a ' > "$CUBES"
NC=$(wc -l < "$CUBES")
echo "[$(date -Iseconds)] $NC cubos"

# Exhaustividad: si la negacion de los cubos es UNSAT (Result: 20), cubren todo el espacio.
( $SMSG --vertices $N --all-graphs --connected --cutoff 0 --hide-graphs \
        --forbidden-subgraph-file $CYC --dimacs $CNF \
        --cube-file-test "$CUBES" > "$OUT/cube_file_test.log" 2>&1
  echo "[$(date -Iseconds)] cube-file-test: $(grep -E '^Result:' "$OUT/cube_file_test.log")" ) &

solve_one() {
  local i=$1
  local t0=$SECONDS
  local out
  out=$($SMSG --vertices $N --all-graphs --connected --cutoff 0 --hide-graphs \
        --forbidden-subgraph-file $CYC --dimacs $CNF \
        --cube-file "$CUBES" --cube-line $i 2>&1)
  local rc=$?
  local c
  c=$(echo "$out" | grep 'Number of graphs:' | awk '{print $4}')
  echo "$i ${c:-ERR} $rc $((SECONDS-t0))" >> "$OUT/resultados.txt"
}
export -f solve_one
export N K CUBES CYC CNF SMSG OUT SECONDS

: > "$OUT/resultados.txt"
seq 1 "$NC" | xargs -P "$W" -I{} bash -c 'solve_one {}'
wait

awk -v nc="$NC" '{s+=$2; if($2=="ERR"||$3!=0) e++} END {
  printf "SUMA=%d ERRORES=%d CUBOS_RESUELTOS=%d/%d\n", s, e+0, NR, nc }' "$OUT/resultados.txt" \
  | tee "$OUT/SUMA.txt"
echo "[$(date -Iseconds)] fin n=$N"
