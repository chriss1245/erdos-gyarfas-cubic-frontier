#!/bin/bash
# Escalera de ordenes pares en la clase cubica: prohibir {C4,C8,C16} DENTRO de la
# busqueda y testar las potencias grandes (C32, C64) FUERA, sobre los
# supervivientes. Si el recuento es 0 el orden queda cerrado sin mas.
set -u
PY=/home/ubuntu/miniconda3/envs/eg_sms_env/bin/python
OUT=resultados/escalera
mkdir -p "$OUT"

for n in "$@"; do
  tag="n${n}"
  echo "=== n=$n : prohibiendo C4,C8,C16 (C32+ desacoplado) ==="
  date -Iseconds
  $PY sms_run.py --n "$n" --forbid 4,8,16 --budget 604800 \
      --dump "$OUT/${tag}_survivors.txt" \
      --json "$OUT/${tag}.json" > "$OUT/${tag}.log" 2>&1
  status=$($PY -c "import json;d=json.load(open('$OUT/$tag.json'));print(d['status'],d['count'],d['elapsed'])")
  echo "n=$n -> $status"
  count=$(echo "$status" | awk '{print $2}')
  if [ "$count" != "0" ] && [ -s "$OUT/${tag}_survivors.txt" ]; then
    echo "--- supervivientes: test de C32/C64 fuera de la busqueda ---"
    $PY check_survivors.py "$OUT/${tag}_survivors.txt" | tee "$OUT/${tag}_pow2.txt" | tail -5
  fi
  date -Iseconds
done
