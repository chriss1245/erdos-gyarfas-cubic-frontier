#!/bin/bash
# Barrido Erdős–Gyárfás reanudable con geng_eg2 (cúbicos sin C4/C8/C16).
# Uso: ./run_eg.sh N MOD [JOBS]   p.ej. ./run_eg.sh 28 112 14
# Cada shard completado deja resultados/eg/nN_modMOD/sR.done — relanzar el
# mismo comando tras un apagado salta lo ya hecho.
set -u
cd "$(dirname "$0")"

N=$1; MOD=$2; JOBS=${3:-14}
DIR="resultados/eg/n${N}_mod${MOD}"
mkdir -p "$DIR"

run_shard() {
    local r=$1
    local out="$DIR/s$r.g6" log="$DIR/s$r.log" done="$DIR/s$r.done"
    [ -f "$done" ] && return 0
    ./nauty2_8_9/geng_eg2 -c -d3 -D3 -f "$N" "$r/$MOD" >"$out" 2>"$log" \
        && grep -q '>Z' "$log" && touch "$done"
    if [ -s "$out" ]; then
        echo "$(date -Is) ¡¡CANDIDATO A CONTRAEJEMPLO!! shard $r/$MOD n=$N:" | tee -a "$DIR/ALERTA.txt"
        cat "$out" | tee -a "$DIR/ALERTA.txt"
    fi
}
export -f run_shard; export DIR N MOD

seq 0 $((MOD-1)) | xargs -P "$JOBS" -I{} bash -c 'run_shard {}'

DONE=$(ls "$DIR"/*.done 2>/dev/null | wc -l)
echo "== n=$N: $DONE/$MOD shards completos =="
if [ "$DONE" -eq "$MOD" ]; then
    cat "$DIR"/s*.g6 > "$DIR/survivors.g6"
    echo "== BARRIDO COMPLETO. supervivientes: $(wc -l < "$DIR/survivors.g6") =="
    grep -h '>Z' "$DIR"/s*.log | awk '{s+=$(NF-1)} END {print "== core-segundos totales: " s " =="}'
fi
