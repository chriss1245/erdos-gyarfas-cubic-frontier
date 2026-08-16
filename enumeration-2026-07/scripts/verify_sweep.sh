#!/bin/bash
# Integrity checker for a finished sweep directory produced by src/run_eg.sh.
#
# Usage: scripts/verify_sweep.sh <run-dir> <expected-shard-count>
#
# Verifies, for shards 0 .. N-1:
#   1. every shard has its .done marker;
#   2. every shard log ends with geng's ">Z ... graphs generated" summary
#      (i.e. the generator terminated normally, it was not killed);
#   3. reports the total number of graphs output (counterexample candidates)
#      and the total core-seconds.
# Exit status 0 iff checks 1-2 pass for all shards.
set -eu
DIR=$1; N=$2
missing_done=0; missing_z=0; total_out=0

for r in $(seq 0 $((N-1))); do
    [ -f "$DIR/s$r.done" ] || { echo "FALTA .done: shard $r"; missing_done=$((missing_done+1)); }
    grep -q '>Z' "$DIR/s$r.log" 2>/dev/null \
        || { echo "SIN TERMINACIÓN >Z: shard $r"; missing_z=$((missing_z+1)); }
    # grep -c exits 1 on a zero count, which is the normal case here — mask it
    [ -f "$DIR/s$r.g6" ] && total_out=$((total_out + $(grep -c . "$DIR/s$r.g6" || true)))
done

echo "shards esperados:            $N"
echo "shards sin .done:            $missing_done"
echo "shards sin terminación >Z:   $missing_z"
echo "grafos emitidos (candidatos): $total_out"
grep -h '>Z' "$DIR"/s*.log | awk '{s+=$(NF-1)} END {printf "core-segundos totales:        %.0f (%.1f core-h)\n", s, s/3600}'

[ "$missing_done" -eq 0 ] && [ "$missing_z" -eq 0 ]
