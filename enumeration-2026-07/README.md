# Erdős–Gyárfás conjecture: exhaustive verification for cubic graphs on ≤ 30 vertices

Code, data and logs for the computational result:

> **Theorem.** Every connected cubic graph on at most 30 vertices contains a cycle of
> length 4, 8 or 16. Consequently, a smallest *cubic* counterexample to the
> Erdős–Gyárfás conjecture ("every graph with minimum degree ≥ 3 contains a cycle of
> length a power of 2", [erdosproblems.com/64](https://www.erdosproblems.com/64))
> has at least 32 vertices.

This extends the exhaustive verification of Markström (2004), which covered cubic
graphs on fewer than 29 vertices, and is the first movement of that frontier since.

## Method in one paragraph

Connected cubic graphs are generated with `geng` (nauty 2.8.9) using its built-in
square-free filter (`-f`, no 4-cycles) and its `PREPRUNE`/`PRUNE` hooks to reject any
partial graph containing an 8-cycle or a 16-cycle. Soundness of the pruning rests on
two facts: (1) *monotonicity* — `geng` adds vertices one at a time together with all
their incident edges and never removes an edge, so a forbidden cycle, once present,
persists; and (2) *anchoring* — every cycle first appears exactly when its
highest-numbered vertex is added, and `PRUNE` is called at every order, so a
depth-first search for cycles of length exactly L anchored at the newest vertex is
exhaustive. On 30 vertices a 32-cycle cannot occur, so any graph output by the pruned
generator would be a counterexample; the n=30 sweep output **zero graphs** across
1008 independent shards (348.7 core-hours).

## Repository layout

```
src/prune_c8.c       PRUNE hook: reject 8-cycles (census variant, geng_eg)
src/prune_c8c16.c    PREPRUNE+PRUNE hooks: reject 8- and 16-cycles (hunt variant, geng_eg2)
src/filter_eg.py     independent pure-Python pipeline filter (validation)
src/check_pow2.py    independent networkx-based verifier (validation)
src/run_eg.sh        resumable sharded sweep driver (res/mod, one .done marker per shard)
data/                graph6 censuses: the 4 (n=24) and 23 (n=26) cubic graphs with no C4/C8
logs/                complete geng logs of the n=28 (112 shards) and n=30 (1008 shards) sweeps
tests/               correctness test suite (see below)
scripts/verify_sweep.sh   integrity checker for sweep log/output directories
Makefile             builds geng_eg / geng_eg2 against a nauty source tree
```

The C sources are **verbatim** the files compiled for the sweeps (comments in
Spanish); they are deliberately left byte-identical to preserve provenance. Each file
header contains its exact compilation command.

## Reproducing

1. Download [nauty 2.8.9](https://pallini.di.uniroma1.it/), `./configure && make`
   (this produces the `*W1.o` objects the Makefile links against).
2. `make NAUTY=/path/to/nauty2_8_9` — builds `geng_eg` and `geng_eg2`.
3. Quick test suite (~2 min): `make test NAUTY=/path/to/nauty2_8_9`.
   Full golden validation (~45 min, single core): `make test-full`.
4. Re-run any shard of the sweep and compare with the corresponding log, e.g.
   shard 123: `./geng_eg2 -c -d3 -D3 -f 30 123/1008` (expected: no output, and a
   final `>Z 0 graphs generated` line matching `logs/` after extraction).
5. Full sweep (~350 core-hours): `./src/run_eg.sh 30 1008 <parallel-jobs>` — resumable,
   each completed shard leaves a `.done` marker and is skipped on relaunch.
6. Integrity check of a finished sweep directory:
   `./scripts/verify_sweep.sh <run-dir> <expected-shard-count>`.

## Validation performed (all reproducible via the test suite)

| test | expected | result |
|---|---|---|
| n=20, 22 cubic without C4/C8 | 0, 0 (Markström) | 0, 0 ✓ |
| n=24 census without C4/C8 | 4 graphs (Markström Table 3) | same 4 graph6, by 2 independent implementations ✓ |
| n=26 census without C4/C8 | 23 (Markström Table 3) | 23, all containing C16 ✓ |
| n=28 without C4/C8/C16 | 0 (implied by Markström) | 0 ✓ |
| n=14, 18 cubic without C8(/C16), C4 allowed | plain geng + independent filter | 15=15, 67=67 ✓ |
| n=30 without C4/C8/C16 | **unknown (new territory)** | **0 — the theorem** |

## Requirements

- gcc, GNU make, bash (any Linux/macOS)
- nauty 2.8.9 (not included; see its own license)
- Python 3.8+ for the validation tools; `networkx` only for `check_pow2.py`

## Citation

See `CITATION.cff`. Paper: [[arXiv id pending]].

## Acknowledgements

The search pipeline was developed with the assistance of Claude (Anthropic).
[[Company acknowledgement pending]]
