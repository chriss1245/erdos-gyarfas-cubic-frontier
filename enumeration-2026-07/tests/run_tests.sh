#!/bin/bash
# Correctness test suite for the Erdős–Gyárfás search pipeline.
#
# Usage:  NAUTY=/path/to/nauty2_8_9 tests/run_tests.sh [quick|full]
#
#   quick (~2 min):  cross-implementation agreement on small n, positive
#                    controls with nonzero expected counts, one negative control.
#   full  (~45 min): everything in quick, plus the golden validations against
#                    Markström's published censuses (n=24: 4 graphs, n=26: 23).
#
# Every expected number here comes from an INDEPENDENT source: either
# Markström 2004 (Table 3 / Fig. 14) or a from-scratch filter implementation
# (src/filter_eg.py, pure Python) run over the unpruned generator.
set -eu
cd "$(dirname "$0")/.."
MODE=${1:-quick}
NAUTY=${NAUTY:-../nauty2_8_9}
PASS=0; FAIL=0

check() { # check <label> <expected> <actual>
    if [ "$2" = "$3" ]; then
        echo "ok       $1 = $3"; PASS=$((PASS+1))
    else
        echo "FAILED   $1: expected $2, got $3"; FAIL=$((FAIL+1))
    fi
}

echo "== unit tests: cycle detectors on known graphs =="
python3 tests/test_detectors.py && PASS=$((PASS+1)) || FAIL=$((FAIL+1))

echo "== cross-implementation: geng_eg2 vs unpruned geng + pure-Python filter (n=12) =="
# every cubic graph on 12 vertices, C4 allowed: count those with no C8 two ways
A=$("$NAUTY"/geng -c -d3 -D3 -q 12 | python3 tests/count_c8free.py)
B=$(./geng_eg2 -c -d3 -D3 -q 12 | wc -l)
check "n=12 cubic, no C8 (indep. filter vs pruned generator)" "$A" "$B"

echo "== positive controls (nonzero counts, precomputed with the independent filter) =="
check "n=14 cubic, no C8, C4 allowed"        15 "$(./geng_eg2 -c -d3 -D3 -q 14 | wc -l)"
check "n=18 cubic, no C8/C16, C4 allowed"    67 "$(./geng_eg2 -c -d3 -D3 -q 18 | wc -l)"

echo "== negative control (known-zero from Markström 2004) =="
check "n=20 cubic, no C4/C8/C16"              0 "$(./geng_eg2 -c -d3 -D3 -q -f 20 | wc -l)"

if [ "$MODE" = full ]; then
    echo "== golden validation: Markström 2004, Table 3 (single core, ~45 min) =="
    S24=$(./geng_eg -c -d3 -D3 -q -f 24 | sort)
    check "n=24 census size, no C4/C8"        4 "$(printf '%s\n' "$S24" | grep -c .)"
    check "n=24 census matches shipped data" OK \
        "$([ "$S24" = "$(sort data/n24_no-c4c8_survivors.g6)" ] && echo OK || echo DIFF)"
    check "n=26 census size, no C4/C8"       23 "$(./geng_eg -c -d3 -D3 -q -f 26 | wc -l)"
fi

echo "== $PASS passed, $FAIL failed =="
[ "$FAIL" -eq 0 ]
