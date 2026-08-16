# Erdős–Gyárfás conjecture: calibrated SAT-modulo-symmetries verification for cubic graphs on ≤ 40 vertices

Code, data and logs for the computational result:

> **Theorem.** Every connected cubic graph on at most 40 vertices contains a cycle of
> length 4, 8 or 16. Consequently, a smallest *cubic* counterexample to the
> Erdős–Gyárfás conjecture ("every graph with minimum degree ≥ 3 contains a cycle of
> length a power of 2", [erdosproblems.com/64](https://www.erdosproblems.com/64))
> has at least 42 vertices.

Previous exhaustive bounds for the cubic class: Markström (2004) covered n ≤ 28;
the July 2026 enumeration included here (`enumeration-2026-07/`) covered n = 30.
Balaji (2026, Zenodo 10.5281/zenodo.21190438) reports minimum degree ≥ 3 up to
n ≤ 31 via SAT modulo symmetries, pending independent reproduction.

Full write-up: `paper/nota.pdf`.

## Method

One SAT-modulo-symmetries (SMS) call per even order n decides: *is there a connected
cubic graph on n vertices with no C4, C8 or C16 subgraph?* Larger powers of two (C32,
C64) are deliberately left out of the search and would be tested a posteriori on
survivors — vacuously, since every order returns zero graphs. The propagator stack is
SMS + Glasgow subgraph solver + CaDiCaL. Two non-default choices: degree exactly 3
(sequential-counter cardinality encoding, totalizer as robustness axis), and the
minimality-check cutoff disabled (`--cutoff 0`; the default 200000 truncates symmetry
breaking). Timeouts are never reported as UNSAT; unparseable counts are errors, not
zeros.

## Why trust an UNSAT answer: calibration

The dangerous failure mode of a SAT+propagator pipeline is over-constraint: it returns
zero everywhere and passes every test whose correct answer is zero. The instrument is
therefore required to reproduce **thirteen reference censuses of connected cubic
graphs, nine of them nonzero**, before any frontier claim:

| order | forbidden | expected | SMS |
|---|---|---|---|
| 10 | C16 | 19 | 19 |
| 14 | C16 | 509 | 509 |
| 16 | C16 | 219 | 219 |
| 18 | C16 | 1471 | 1471 |
| 20 | C16 | 12709 | 12709 |
| 22 | C16 | 52781 | 52781 |
| 24 | C4,C8 | 4 (Markström) | 4, same graphs |
| 26 | C4,C8 | 23 (Markström) | 23, same graphs |
| 28 | C4,C8 | 251 (Markström) | 251 |
| 24,26,28,30 | C4,C8,C16 | 0 | 0 |

Ground truth comes from three independent sources: Markström's published Table 3; the
July 2026 exhaustive enumeration (`enumeration-2026-07/`, 348.7 core-hours at n=30);
and fresh C16-free censuses at n = 14–22 (`data/c16-free-censuses/`), counted with a
bitmask DFS (`src/count_c16free.py`) and re-verified with an independent
networkx-based detector (`src/recount_nx.py`); census totals match OEIS A002851, and
at n = 24, 26 the SMS output coincides with the enumeration **as a set** after
canonical labelling (`labelg`). At n = 22 the six `res/mod` shards sum to 7 319 447
(the full census), with 52 781 distinct canonical forms and zero duplicates.

Robustness and controls:

- **Totalizer re-decision**: a structurally different CNF reproduces 251 (n=28),
  1471 (n=18), and zero at n = 30, 32, 36 **and 40** — the headline order is decided
  twice (17 207 s vs 18 922 s).
- **Positive controls at and beyond the frontier**: forbidding only {C4, C8}, where
  solutions must exist, SMS returns SAT at n = 32, 34, 36, 38, 40, 42, 44. Zeros are
  therefore not an artifact of vacuous unsatisfiability at large orders.

## Frontier result

| n | cubic graphs with no C4, C8, C16 | single-core time |
|---|---|---|
| 30 | 0 | 187 s |
| 32 | 0 | 505 s |
| 34 | 0 | 1188 s |
| 36 | 0 | 3366 s |
| 38 | 0 | 8157 s |
| 40 | 0 | 18922 s |

Growth ≈ ×2.3–2.8 per two vertices. Machine: Intel Xeon W-10885M, single-threaded.

## Repository layout

```
paper/                    nota.tex, nota.pdf, referencias.md
src/                      SMS driver (sms_run.py), ladder/calibration scripts,
                          ground-truth generators and both cycle detectors
results/calibracion/      one JSON per calibration/robustness/control run
                          (count, status, elapsed, exit code, exact command line),
                          RESULTADOS.md, c16_groundtruth.md, cube-and-conquer study
results/escalera/         frontier runs n = 32..40 (JSON + log)
data/c16-free-censuses/   graph6: cubic connected, no C16, n = 14..22
data/markstrom-class/     graph6: cubic connected, no C4/C8, n = 24, 26
logs/                     SMS/CaDiCaL/Glasgow build log
enumeration-2026-07/      the complete July 2026 enumeration apparatus (geng + C
                          pruning hooks) used as independent ground truth, as archived
BUILD.md                  toolchain versions and build instructions
SHA256SUMS                checksums of every file
```

## Reproducing

See `BUILD.md`. The frontier runs are single commands, e.g.:

```bash
python sms_run.py --n 40 --forbid 4,8,16 --budget 604800 --json n40.json
```

## What is not claimed

No machine-checkable proof certificate accompanies the UNSAT results: clauses
contributed by the subgraph propagator are not RUP/RAT-derivable from the encoding
alone, so a generic checker cannot validate them. The claim rests on a calibrated
instrument, not a certified one; see the paper's "What is not claimed" section.
Independent reproduction is welcome — the JSONs record exact command lines.

## Author

Christopher Andre Manzano Vimos — WhiteBox ML, Madrid —
[ORCID 0009-0000-4270-4610](https://orcid.org/0009-0000-4270-4610)

The computational pipeline was developed with the assistance of Claude (Anthropic);
the author is responsible for the design of the experiments, the verification
protocol and all claims.
