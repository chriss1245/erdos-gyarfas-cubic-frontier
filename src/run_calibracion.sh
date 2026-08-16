#!/bin/bash
# Bateria de calibracion de SMS contra nuestros censos exhaustivos (clase cubica, conexos).
# Cada linea: n, longitudes prohibidas, valor esperado (o "?" si no lo conocemos).
set -u
PY=/home/ubuntu/miniconda3/envs/eg_sms_env/bin/python
OUT=resultados/calibracion
mkdir -p "$OUT"

run () {  # run N FORBID EXPECTED BUDGET
  local n=$1 forbid=$2 exp=$3 budget=$4
  local tag="n${n}_$(echo "$forbid" | tr ',' '-')"
  $PY sms_run.py --n "$n" --forbid "$forbid" --budget "$budget" \
      --json "$OUT/sms_$tag.json" > "$OUT/sms_$tag.log" 2>&1
  local got
  got=$($PY -c "import json;d=json.load(open('$OUT/sms_$tag.json'));print(d['count'],d['status'],d['elapsed'])" 2>/dev/null)
  echo "n=$n forbid=$forbid esperado=$exp obtenido=$got"
}

echo "=== C16 solo (verdad de tierra propia, Fase 0) ==="
run 20 16 12709 7200

echo "=== C4,C8 (censo de Markstrom + nuestro barrido) ==="
run 24 4,8 4 7200
run 26 4,8 23 14400
run 28 4,8 251 43200

echo "=== C4,C8,C16 (nuestro barrido exhaustivo: cero) ==="
run 24 4,8,16 0 7200
run 26 4,8,16 0 14400
run 28 4,8,16 0 43200
run 30 4,8,16 0 86400
