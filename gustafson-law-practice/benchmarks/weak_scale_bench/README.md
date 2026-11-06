# Weak-scaling benchmark (Task 22)

Requirements: Python ≥ 3.8, `numpy`. (Plots: `matplotlib`.) Linux/macOS (uses `fork`).

```bash
cd benchmarks/weak_scale_bench
python3 weak_bench.py                         # auto thread counts: 1,hw/2,2,4,8,hw ; 5 runs each
python3 weak_bench.py --threads 1 2 4 8 16 --runs 5 --k 20000000 --out ../results.csv
```
Each worker integrates a constant K points of 4/(1+x²) on [0,1]; total work = P·K, ideal runtime constant.
The wall-clock includes pool start-up and final `fsum` reduction (the measured serial fraction).
Choose `--k` so that 1-worker time is ≳ 0.5 s. Pin frequency / disable turbo for cleaner data if possible.
Then: `python3 ../fit_gustafson.py && python3 ../make_plots.py`.
