# Build record

## Solver stack (exact commits)

| component | commit | note |
|---|---|---|
| SAT Modulo Symmetries (SMS) | `464f12f` | same pin as Balaji 2026 |
| CaDiCaL | `b023aaf` | same pin |
| Glasgow Subgraph Solver | `1217f5b` | **the SMS build script clones Glasgow at HEAD, not at a pinned commit** — record this hash when reproducing |
| nauty (geng, labelg) | 2.8.9 | ground-truth enumeration |

Full build log: `logs/sms_build.log`.

## Environment

Conda env (no sudo needed): boost, GMP, zlib, cmake, tectonic. Python 3 with
pysms (`pysms.graph_builder`) for the CNF; networkx only for the independent
detectors (`check_pow2.py`, `recount_nx.py`).

```bash
conda create -n eg_sms_env boost gmp zlib cmake tectonic
# behind a TLS-intercepting proxy:
export REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
```

Build SMS per its own `build-and-install.sh`; binaries land in `~/.local/bin/smsg`.
Runtime needs `LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$HOME/.local/lib`.

## Machine

Intel Xeon W-10885M (8 cores / 16 threads, 2.40 GHz), 31 GB RAM, Linux 6.17.
All frontier and calibration runs single-threaded; wall times in the JSONs.

## Driver conventions (src/sms_run.py)

- degree **exactly** 3 (`minDegree(3)` + `maxDegree(3)`), sequential counter by
  default, `--counter totalizer` as robustness axis;
- `--connected`, to match `geng -c` and Markström;
- `--cutoff 0`: the default minimality-check cutoff (200000) truncates complete
  symmetry breaking;
- a run that exhausts its budget is recorded as `WALL`, never as UNSAT; an
  unparseable count is `ERROR`, never zero; exit codes recorded in every JSON.

## Warnings for reproducers

- CaDiCaL's formula simplification (`--simplify`) does **not** preserve the set of
  models: on the n=28 census (forbid C4,C8) it returns 241 instead of 251. Never use
  it for counting runs. See `results/calibracion/cubos/`.
- SMS's native cube-and-conquer overlaps cubes (n=28 sums 252 vs 251 true): sound for
  a zero/nonzero verdict (coverage provable via `--cube-file-test`), unsound for exact
  counts.
- `check_pow2.py` runs its main loop under `if __name__ == "__main__"` so it can be
  imported by `recount_nx.py`.
